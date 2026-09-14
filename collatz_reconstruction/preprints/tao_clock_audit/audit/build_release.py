"""Generate and verify this draft's own package; never touches the workbench."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PORTABLE = ["main.tex", "bibliography.tex", "README.md", "source_manifest.json", "proof_registry.json",
            "verify.py", "certificates/check_finite.py", "sections/clocks.tex", "sections/transport.tex",
            "sections/consequences.tex", "sections/repairs.tex", "sections/versions.tex"]


def identity(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def run(command):
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if result.returncode:
        raise RuntimeError(f"Command failed: {command}\n{result.stdout}\n{result.stderr}")
    return result


def main():
    records = [{"path": name, **identity(ROOT / name)} for name in sorted(PORTABLE)]
    (ROOT / "MANIFEST.json").write_text(json.dumps({"schema_version": 1, "files": records,
        "scope": "Portable authored source only; no private audit files or source literature included"}, indent=2) + "\n", encoding="utf-8")
    verification = json.loads(run([sys.executable, "verify.py"]).stdout)
    out = ROOT / "output/pdf"
    out.mkdir(parents=True, exist_ok=True)
    for attempt in range(2):
        result = run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-file-line-error",
                      "-jobname=tao_clock_audit", "-output-directory=output/pdf", "main.tex"])
        (ROOT / f"audit/tex_pass_{attempt + 1}.log").write_text(result.stdout + result.stderr, encoding="utf-8")
    log = (out / "tao_clock_audit.log").read_text(encoding="utf-8", errors="replace")
    rejected = [line for line in log.splitlines() if any(term in line for term in
        ("Overfull", "Underfull", "Warning:", "undefined", "multiply defined", "Label(s) may have changed"))]
    if rejected:
        raise RuntimeError("TeX QA diagnostics: " + "\n".join(rejected))
    import fitz
    pdf = out / "tao_clock_audit.pdf"
    doc = fitz.open(pdf)
    page_count = len(doc)
    fulltext = "\n".join(page.get_text() for page in doc)
    if "??" in fulltext:
        raise RuntimeError("Unresolved rendered reference")
    for page in doc:
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    x0, y0, x1, y1 = span["bbox"]
                    if not (40 <= x0 <= x1 <= page.rect.width - 40 and 35 <= y0 <= y1 <= page.rect.height - 30):
                        raise RuntimeError(f"Text outside page guard: page {page.number + 1}, {span}")
    doc.close()
    (ROOT / "audit/rendered_text.txt").write_text(fulltext, encoding="utf-8")
    images = ROOT / "tmp/pdfs" / identity(pdf)["sha256"][:16]
    images.mkdir(parents=True, exist_ok=True)
    run(["pdftoppm", "-r", "90", "-png", str(pdf), str(images / "page")])
    from PIL import Image, ImageOps, ImageDraw
    page_paths = sorted(images.glob("page-*.png"), key=lambda p: int(re.search(r"(\d+)\.png$", p.name).group(1)))
    if len(page_paths) != page_count:
        raise RuntimeError("Wrong rendered-page count")
    for offset in range(0, page_count, 4):
        selected = page_paths[offset:offset + 4]
        with Image.open(selected[0]) as sample:
            width, height = sample.size
        sheet = Image.new("RGB", (2 * width, 2 * (height + 25)), "#d0d0d0")
        draw = ImageDraw.Draw(sheet)
        for k, path in enumerate(selected):
            left, top = (k % 2) * width, (k // 2) * (height + 25)
            draw.text((left + 8, top + 6), f"Page {offset + k + 1}", fill="black")
            with Image.open(path) as page_image:
                sheet.paste(page_image, (left, top + 25))
        sheet.save(images / f"sheet-{offset // 4 + 1}.png")
    archive = ROOT / "output/tao_clock_audit_source.zip"
    names = sorted(PORTABLE + ["MANIFEST.json"])
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as bundle:
        for name in names:
            info = zipfile.ZipInfo(name, date_time=(2026, 9, 4, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            bundle.writestr(info, (ROOT / name).read_bytes())
    with zipfile.ZipFile(archive) as bundle:
        if sorted(bundle.namelist()) != names:
            raise RuntimeError("Archive membership mismatch")
        for name in names:
            if bundle.read(name) != (ROOT / name).read_bytes():
                raise RuntimeError("Archive byte mismatch: " + name)
        bad = bundle.testzip()
        if bad:
            raise RuntimeError("Archive CRC error: " + bad)
    receipt = {"updated_utc": datetime.now(timezone.utc).isoformat(), "status": "compiled_and_machine_verified_visual_review_pending",
        "source_verification": verification, "pdf": {"path": "output/pdf/tao_clock_audit.pdf", "pages": page_count, **identity(pdf)},
        "source_archive": {"path": "output/tao_clock_audit_source.zip", "entries": len(names), **identity(archive)},
        "tex_diagnostics": rejected, "page_text_guard": "PASS", "visual_review": "pending",
        "render_directory": images.relative_to(ROOT).as_posix(),
        "lean_launched": False, "public_upload": False}
    (ROOT / "audit/release_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
