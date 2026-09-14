from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "research_companion"
MANIFEST = ROOT / "MANIFEST.json"
OUTPUT = "output/pdf/collatz_research_companion.pdf"
EXPECTED = [
    "README.md",
    "bibliography.tex",
    "certificates/arctangent_relation_lattice_checks.py",
    "certificates/finite_actions_checks.py",
    "chapters/01_weighted_path_and_finite_residue_actions.tex",
    "chapters/02_two_adic_survivor_coding_and_exact_interface_boundaries.tex",
    "main.tex",
    "provenance.json",
    "validate_package.py",
]


if not __debug__:
    raise RuntimeError("manifest update refuses optimized Python")


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


actual = {
    path.relative_to(ROOT).as_posix()
    for path in ROOT.rglob("*")
    if path.is_file()
    and path != MANIFEST
    and path.relative_to(ROOT).as_posix() != OUTPUT
    and "__pycache__" not in path.parts
    and path.relative_to(ROOT).parts[0] != "tmp"
}
assert actual == set(EXPECTED), {
    "missing": sorted(set(EXPECTED) - actual),
    "unexpected": sorted(actual - set(EXPECTED)),
}

output_path = ROOT / OUTPUT
assert output_path.is_file()
assert output_path.read_bytes().startswith(b"%PDF-")

manifest = {
    "schema_version": "1.0",
    "files": {
        name: {
            "bytes": (ROOT / name).stat().st_size,
            "sha256": digest(ROOT / name),
        }
        for name in EXPECTED
    },
    "output_pdf": {
        "path": OUTPUT,
        "bytes": output_path.stat().st_size,
        "sha256": digest(output_path),
    },
    "resolved_ids": [],
}
MANIFEST.write_text(
    json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)

reloaded = json.loads(MANIFEST.read_text(encoding="utf-8"))
assert list(reloaded["files"]) == EXPECTED
assert reloaded["output_pdf"]["bytes"] == 572830
assert reloaded["output_pdf"]["sha256"] == (
    "8fecd942b3a8370a9457bdad32619640dbc1eb8f67c6f75e529c32e18b3c00b8"
)
print(
    json.dumps(
        {
            "status": "PASS",
            "manifested_source_files": len(EXPECTED),
            "output_pdf": reloaded["output_pdf"],
        },
        indent=2,
        sort_keys=True,
    )
)
