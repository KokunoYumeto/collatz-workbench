"""Refresh only the README manifest entry and portable ZIP; preserve the PDF."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def identity(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def require(value, message):
    if not value:
        raise RuntimeError(message)


def main():
    receipt_path = ROOT / "audit/release_receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    pdf_path = ROOT / receipt["pdf"]["path"]
    original_pdf = identity(pdf_path)
    require(original_pdf["sha256"] == receipt["pdf"]["sha256"], "Reference PDF already differs")
    manifest_path = ROOT / "MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    changed = []
    for record in manifest["files"]:
        actual = identity(ROOT / record["path"])
        if actual["sha256"] != record["sha256"] or actual["bytes"] != record["bytes"]:
            require(record["path"] == "README.md", "Unexpected changed portable file: " + record["path"])
            record.update(actual)
            changed.append(record["path"])
    require(changed == ["README.md"], "Expected exactly the authorized README change")
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    verified = subprocess.run([sys.executable, "verify.py"], cwd=ROOT,
        capture_output=True, text=True, encoding="utf-8", check=True)
    verification = json.loads(verified.stdout)
    require(verification["status"] == "PASS", "Portable verifier failed")
    names = sorted([record["path"] for record in manifest["files"]] + ["MANIFEST.json"])
    archive = ROOT / "output/tao_clock_audit_source.zip"
    prior_archive = identity(archive)
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as bundle:
        for name in names:
            info = zipfile.ZipInfo(name, date_time=(2026, 9, 4, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            bundle.writestr(info, (ROOT / name).read_bytes())
    with zipfile.ZipFile(archive) as bundle:
        require(sorted(bundle.namelist()) == names, "Archive membership mismatch")
        require(bundle.testzip() is None, "Archive CRC error")
        for name in names:
            require(bundle.read(name) == (ROOT / name).read_bytes(), "Archive byte mismatch: " + name)
    require(identity(pdf_path) == original_pdf, "Reference PDF changed")
    receipt["updated_utc"] = datetime.now(timezone.utc).isoformat()
    receipt["source_verification"] = verification
    receipt["source_archive"] = {"path": "output/tao_clock_audit_source.zip", "entries": len(names), **identity(archive)}
    receipt["readme_package_refresh"] = {
        "reason": "Current user authorized a maintained working Overleaf project; remove obsolete no-upload wording",
        "changed_portable_content": changed,
        "prior_archive": prior_archive,
        "pdf_unchanged": True,
        "tex_unchanged": True,
        "upload_performed_by_this_script": False,
    }
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "archive": receipt["source_archive"],
        "pdf_unchanged": True, "changed": changed}, indent=2))


if __name__ == "__main__":
    main()
