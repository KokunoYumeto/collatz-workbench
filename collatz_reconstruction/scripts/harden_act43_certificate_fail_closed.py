from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CERT_REL = "research_companion/certificates/groupoid_motivic_interface_checks.py"
OLD_BYTES = 17_335
OLD_SHA256 = "99767e2abeb82b433b5b4cd12da07a199ac22782010b5b11d5a583e80ce109d7"
NEW_BYTES = 17_495
NEW_SHA256 = "ca460277a54e016a6ef84377cde5cc2e670f08c6cf3f57073f2a3c62d6400916"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_exact(relative: str, old: str, new: str, expected_count: int) -> None:
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != expected_count:
        raise RuntimeError(
            f"{relative}: expected {expected_count} occurrences of {old!r}, found {count}"
        )
    path.write_text(text.replace(old, new), encoding="utf-8")


def main() -> None:
    certificate = ROOT / CERT_REL
    if certificate.stat().st_size != NEW_BYTES or digest(certificate) != NEW_SHA256:
        raise RuntimeError("hardened certificate identity mismatch")

    manifest_path = ROOT / "research_companion/MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    entry = manifest["files"]["certificates/groupoid_motivic_interface_checks.py"]
    if entry != {"bytes": OLD_BYTES, "sha256": OLD_SHA256}:
        raise RuntimeError(f"unexpected pre-update manifest entry: {entry}")
    entry.update({"bytes": NEW_BYTES, "sha256": NEW_SHA256})
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    replace_exact("state/chatnotes_intake.jsonl", f'"certificate_bytes":{OLD_BYTES}', f'"certificate_bytes":{NEW_BYTES}', 1)
    replace_exact("state/chatnotes_intake.jsonl", OLD_SHA256, NEW_SHA256, 1)
    replace_exact("state/claims.jsonl", OLD_SHA256, NEW_SHA256, 4)
    replace_exact("state/programmes.jsonl", f'"bytes":{OLD_BYTES}', f'"bytes":{NEW_BYTES}', 2)
    replace_exact("state/programmes.jsonl", OLD_SHA256, NEW_SHA256, 2)

    print(
        json.dumps(
            {
                "schema_version": "1.0",
                "status": "PASS",
                "certificate": {
                    "path": CERT_REL,
                    "bytes": NEW_BYTES,
                    "sha256": NEW_SHA256,
                    "optimized_python": "FAIL_CLOSED",
                },
                "updated": [
                    "research_companion/MANIFEST.json",
                    "state/chatnotes_intake.jsonl",
                    "state/claims.jsonl",
                    "state/programmes.jsonl",
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
