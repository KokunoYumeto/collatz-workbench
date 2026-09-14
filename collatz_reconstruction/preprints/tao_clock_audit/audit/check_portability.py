"""Independently rebuild only the portable authored source in fresh scratch."""
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
import hashlib
import json
import re
import stat
import subprocess
import sys
import tempfile
import zipfile

import fitz

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "output/tao_clock_audit_source.zip"
REFERENCE = ROOT / "output/pdf/tao_clock_audit.pdf"
PDFLATEX = Path(r"C:\Users\LOCAL_USER\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe")
RECEIPT = ROOT / "audit/portability_receipt.json"


def require(value, message):
    if not value:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def identify(path):
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": digest(data)}


def main():
    receipt = {
        "updated_utc": datetime.now(timezone.utc).isoformat(),
        "status": "RUNNING",
        "scope": "Isolated source-package verification and PDF rebuild, not an independent mathematical proof audit",
        "commands": [],
        "lean_launched": False,
        "upload_performed": False,
    }
    if RECEIPT.exists():
        previous = json.loads(RECEIPT.read_text(encoding="utf-8"))
        receipt["previous_attempt"] = {
            "status": previous["status"],
            "updated_utc": previous["updated_utc"],
            "isolated_root": previous.get("isolated_root"),
            "error": previous.get("error"),
            "diagnostics": previous.get("final_tex_diagnostics", []),
            "resolution": "Previous check retained for chronology with its original status and diagnostics; the current package is checked afresh.",
        }
    try:
        receipt["source_archive"] = identify(ARCHIVE)
        receipt["reference_pdf"] = identify(REFERENCE)
        release = json.loads((ROOT / "audit/release_receipt.json").read_text(encoding="utf-8"))
        expected_pages = release["pdf"]["pages"]
        require(expected_pages > 0, "Invalid release page count")
        require(release["pdf"]["sha256"] == receipt["reference_pdf"]["sha256"],
                "Release PDF identity mismatch")
        require(release["source_archive"]["sha256"] == receipt["source_archive"]["sha256"],
                "Release ZIP identity mismatch")
        manifest_bytes = (ROOT / "MANIFEST.json").read_bytes()
        manifest = json.loads(manifest_bytes)
        records = manifest["files"]
        paths = [record["path"] for record in records]
        require(len(paths) == len(set(paths)), "Duplicate manifest member")
        expected = set(paths) | {"MANIFEST.json"}
        tmp_root = ROOT / "tmp"
        tmp_root.mkdir(exist_ok=True)
        isolated = Path(tempfile.mkdtemp(prefix="portable_check_", dir=tmp_root))
        receipt["isolated_root"] = str(isolated)
        with zipfile.ZipFile(ARCHIVE) as archive:
            infos = archive.infolist()
            names = [info.filename for info in infos]
            require(len(names) == len(set(names)), "Duplicate ZIP member")
            require(set(names) == expected, "ZIP membership differs from manifest plus MANIFEST.json")
            require(archive.testzip() is None, "ZIP CRC check failed")
            for info in infos:
                relative = PurePosixPath(info.filename)
                require(not relative.is_absolute() and ".." not in relative.parts,
                        "Absolute or parent ZIP path")
                require(":" not in info.filename and "\\" not in info.filename,
                        "Nonportable ZIP path")
                require(not info.is_dir(), "Unexpected ZIP directory entry")
                mode = info.external_attr >> 16
                require(not stat.S_ISLNK(mode), "ZIP symlink entry")
                destination = isolated.joinpath(*relative.parts).resolve()
                require(destination.is_relative_to(isolated.resolve()), "Extraction escaped scratch")
                payload = archive.read(info)
                require(payload == (ROOT / info.filename).read_bytes(),
                        "Archive and current authored source differ: " + info.filename)
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(payload)
        receipt["archive_checks"] = {
            "status": "PASS", "entries": len(expected), "exact_membership": True,
            "crc": "PASS", "safe_paths": True, "no_symlinks": True,
            "all_entries_equal_current_authored_sources": True,
            "manifest_sha256": digest(manifest_bytes),
        }

        def run(command, log_name):
            result = subprocess.run(command, cwd=isolated, capture_output=True,
                                    text=True, encoding="utf-8", errors="replace", timeout=180)
            output = result.stdout + result.stderr
            log = isolated / log_name
            log.write_text(output, encoding="utf-8")
            receipt["commands"].append({"argv": [str(x) for x in command],
                "cwd": str(isolated), "exit_code": result.returncode,
                "output_log": str(log), "output_sha256": digest(output.encode("utf-8"))})
            require(result.returncode == 0, "Command failed; inspect " + str(log))
            return output

        verification = run([sys.executable, "verify.py"], "verify_output.json")
        receipt["extracted_verification"] = json.loads(verification)
        require(receipt["extracted_verification"]["status"] == "PASS", "Extracted verifier did not pass")
        (isolated / "output/pdf").mkdir(parents=True)
        tex_command = [str(PDFLATEX), "-interaction=nonstopmode", "-halt-on-error",
            "-jobname=tao_clock_audit", "-output-directory=output/pdf", "main.tex"]
        run(tex_command, "tex_pass_1.log")
        run(tex_command, "tex_pass_2.log")
        tex_passes = 2
        rerun_pattern = re.compile(r"Rerun to|Please rerun|Label\(s\) may have changed|Warning:.*(?:Rerun|has changed)", re.I)
        for attempt in range(3, 5):
            interim_log = (isolated / "output/pdf/tao_clock_audit.log").read_text(
                encoding="utf-8", errors="replace")
            if not rerun_pattern.search(interim_log):
                break
            run(tex_command, f"tex_pass_{attempt}.log")
            tex_passes = attempt
        receipt["tex_passes"] = tex_passes
        receipt["maximum_tex_passes"] = 4
        final_log = (isolated / "output/pdf/tao_clock_audit.log").read_text(
            encoding="utf-8", errors="replace")
        pattern = re.compile(r"Overfull|Underfull|undefined|multiply defined|Rerun to|Please rerun|Label\(s\) may have changed|Warning:", re.I)
        rejected = [line for line in final_log.splitlines() if pattern.search(line)]
        receipt["final_tex_diagnostics"] = rejected
        require(not rejected, "Final TeX diagnostic check failed")
        rebuilt = isolated / "output/pdf/tao_clock_audit.pdf"
        receipt["rebuilt_pdf"] = identify(rebuilt)
        with fitz.open(REFERENCE) as reference, fitz.open(rebuilt) as actual:
            require(len(actual) == len(reference) == expected_pages, "PDF page count mismatch")
            page_checks = []
            for index, (left, right) in enumerate(zip(reference, actual), 1):
                require(left.rect == right.rect, "PDF page geometry mismatch")
                original_text, rebuilt_text = left.get_text(), right.get_text()
                require(original_text == rebuilt_text, "PDF text mismatch on page " + str(index))
                page_checks.append({"page": index, "text_sha256": digest(original_text.encode("utf-8")),
                                    "exact_text_equal": True, "geometry_equal": True})
            receipt["pdf_comparison"] = {"status": "PASS", "pages": len(actual),
                "comparison": "Exact per-page extracted text and page rectangles; byte-identical PDF not required because build metadata may vary",
                "page_checks": page_checks,
                "visual_scope": "No new visual assertion; root agent separately inspected all final rendered pages"}
        require(identify(ARCHIVE) == receipt["source_archive"], "Source ZIP changed during check")
        require(identify(REFERENCE) == receipt["reference_pdf"], "Reference PDF changed during check")
        require((ROOT / "MANIFEST.json").read_bytes() == manifest_bytes, "Source manifest changed")
        receipt["status"] = "PASS"
    except Exception as error:
        receipt["status"] = "FAIL"
        receipt["error"] = str(error)
        raise
    finally:
        receipt["finished_utc"] = datetime.now(timezone.utc).isoformat()
        RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": receipt["status"], "receipt": str(RECEIPT),
        "entries": receipt["archive_checks"]["entries"],
        "pages": receipt["pdf_comparison"]["pages"],
        "isolated_root": receipt["isolated_root"]}, indent=2))


if __name__ == "__main__":
    main()
