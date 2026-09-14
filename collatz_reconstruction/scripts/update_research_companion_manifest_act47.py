"""Regenerate the portable research-companion manifest from its exact files."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "research_companion"
EXCLUDED_ROOTS = {"tmp", "audit", "output"}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    old = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))
    files = {}
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.name == "MANIFEST.json" or "__pycache__" in path.parts:
            continue
        relative = path.relative_to(ROOT)
        if relative.parts[0] in EXCLUDED_ROOTS:
            continue
        files[relative.as_posix()] = {"bytes": path.stat().st_size, "sha256": sha(path)}
    output = ROOT / "output/pdf/collatz_research_companion.pdf"
    manifest = {
        "schema_version": "1.0",
        "files": files,
        "output_pdf": {
            "path": "output/pdf/collatz_research_companion.pdf",
            "bytes": output.stat().st_size,
            "sha256": sha(output),
        },
        "resolved_ids": old.get("resolved_ids", []),
    }
    (ROOT / "MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": "PASS", "manifested_files": len(files), "output_sha256": sha(output)}))


if __name__ == "__main__":
    main()
