#!/usr/bin/env python3
"""Stage and verify the signed fixed-content necklace Overleaf revision.

This script is specific to the ACT51 local closure.  ``prepare`` changes only
the existing canonical staging tree and writes a local receipt.  ``verify-stage``
is read-only.  ``verify-zip`` checks a fresh source download against every
manifested byte and the explicit historical-extra set.  It creates no project,
publishes nothing, and launches no Lean process.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
STAGE = ROOT / "overleaf/sync_20260904/canonical_project"
RECEIPT = ROOT / "overleaf/sync_20260904/signed_necklace_stage_receipt.json"
PROJECT_ID = "6a91f06e408dd545780c660f"

BASELINE = {
    "MANIFEST.json": "0330adb2fd233200e984d897187d8e0f887880760cef19d86ec5f36b9b29aef6",
    "SOURCE_MAP.json": "e23839b8a152c07dd6a0cd91e0edd824854de7cda4c8a051955e212cad311625",
    "PACKAGE_STATUS.json": "ceed6dff40824faf16130167e2b29c52982ba5d40105ced9d86a77ef64924be5",
    "README.md": "e329569e55fa63d78c658588004de3c52df5f492b734343dc6bc36ef40c5e90e",
    "companion/bibliography.tex": "0ce7c2289625ea88ab9606061b54777f2d362c1bfce3eaf803c36b65b1d98fc8",
    "companion/chapters/04_affine_packets_parity_necklaces_and_residue_automata.tex": "b901360a646d18b5191c75f6c290c8b62733d2939049490b1ff7759b0eca8889",
    "critical/chapters/06_affine_packet_source_audit.tex": "d1b521131814e35faf2d84082d7150fa1db3f4eef0b8be933e68c10e013e583e",
    "critical/chapters/99_source_register.tex": "4de061d4f619fe4aac728ea6dcbd4b23c6fb3785230994627eb288427e25d2bc",
}

SOURCES = {
    "research_companion/bibliography.tex": "5c2737630d5e8e1c597c78bdfb12b26b7fdd424ea1d9f0e1e6f0004859518ad1",
    "research_companion/chapters/04_affine_packets_parity_necklaces_and_residue_automata.tex": "f5a25459b6f0088d14158426b6ca6085c021b5722c972a495bcd2ece7887663e",
    "research_companion/certificates/affine_signed_necklace_checks.py": "8e51437eb64c5c9cee6601d6fe654383302a3ee3d1430c52981ec9b773c29c97",
    "tex/chapters/06_affine_packet_source_audit.tex": "8a4de14fddc13259bb6144866a9924ec9fa58b37477786e0f0a0b789188d91db",
    "tex/chapters/99_source_register.tex": "791a8c4bd83e11c3987d6d432ac5c7db0e25c063499159b92df6f1d04a02ba1c",
    "research_companion/audit/affine_signed_necklace_package_visual_20260905.json": "9ea79f1eb40a41e125d570b663f68af64a7cc46dba3cc20d3f391714008a53fe",
    "research_companion/audit/package_validation/run_20260904T233943Z/watch_receipt.json": "8f257f43fd2f706f5fc12028e8f83026612cf5e0357928c2e374955eb10b8da5",
    "research_companion/audit/package_validation/run_20260904T233943Z/validator_stdout.json": "d49975c27e2f02d25bbc35f71093881ff61bbaf65b9a3e25925bd13035917de1",
    "research_companion/output/pdf/collatz_research_companion.pdf": "074dcc1be3c5a66f28a8568a725d0a0093583faabff888bac177d24c6360119b",
    "output/pdf/collatz_working_corpus.pdf": "24fa733fa1ba7a39a371b64d6d679912c2af15f4fc014ff8eadc9ad4aa209899",
}

SEMANTIC_PATHS = (
    "companion/bibliography.tex",
    "companion/chapters/04_affine_packets_parity_necklaces_and_residue_automata.tex",
    "companion/certificates/affine_signed_necklace_checks.py",
    "critical/chapters/06_affine_packet_source_audit.tex",
    "critical/chapters/99_source_register.tex",
)
ROOT_METADATA_PATHS = (
    "SOURCE_MAP.json",
    "PACKAGE_STATUS.json",
    "README.md",
    "MANIFEST.json",
)
UPLOAD_PATHS = SEMANTIC_PATHS + ROOT_METADATA_PATHS

EXPECTED_REMOTE_EXTRAS = frozenset(
    {
        "chapters/00_scope_and_method.tex",
        "chapters/01_literature_spine.tex",
        "chapters/01a_crandall_1978.tex",
        "chapters/01b_siegel_hydra_numen.tex",
        "chapters/01c_debruijn_graphs.tex",
        "chapters/01d_primary_parity_dependencies.tex",
        "chapters/01e_steuding_continued_fraction.tex",
        "chapters/01f_everett_1977.tex",
        "chapters/01g_tao_fourier_renewal.tex",
        "chapters/01h_tao_valuation_law.tex",
        "chapters/01i_tao_first_passage_stabilisation.tex",
        "chapters/01j_tao_main_theorem_reduction.tex",
        "chapters/01k_computational_verification.tex",
        "chapters/99_source_register.tex",
        "collatz_canonical_project_current_20260904.zip",
    }
)


def sha_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def identity(path: str, payload: bytes) -> dict:
    return {"path": path, "bytes": len(payload), "sha256": sha_bytes(payload)}


def transactional_write(payloads: dict[Path, bytes]) -> None:
    token = uuid4().hex
    originals = {path: path.read_bytes() if path.exists() else None for path in payloads}
    staged: dict[Path, Path] = {}
    committed: list[Path] = []
    try:
        for path, payload in payloads.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            temporary = path.with_name(f".{path.name}.act52-{token}.tmp")
            temporary.write_bytes(payload)
            require(temporary.read_bytes() == payload, f"staging write failed: {path}")
            staged[path] = temporary
        try:
            for path, temporary in staged.items():
                os.replace(temporary, path)
                committed.append(path)
        except Exception:
            for path in reversed(committed):
                original = originals[path]
                if original is None:
                    path.unlink(missing_ok=True)
                else:
                    rollback = path.with_name(f".{path.name}.act52-{token}.rollback")
                    rollback.write_bytes(original)
                    os.replace(rollback, path)
            raise
    finally:
        for temporary in staged.values():
            temporary.unlink(missing_ok=True)
        for path in payloads:
            path.with_name(f".{path.name}.act52-{token}.rollback").unlink(missing_ok=True)


def apply_transformations(source: bytes, transformations: list[dict]) -> bytes:
    text = source.decode("utf-8")
    seen: set[tuple[str, str]] = set()
    for transformation in transformations:
        before = transformation["before"]
        after = transformation["after"]
        key = (before, after)
        if key in seen:
            continue
        seen.add(key)
        require(before in text, f"declared transformation source text absent: {before}")
        text = text.replace(before, after)
    return text.encode("utf-8")


def update_mapping_record(
    source_map: dict,
    source_path: str,
    package_path: str,
    transformations: list[dict] | None = None,
) -> bytes:
    source = (ROOT / source_path).read_bytes()
    matches = [row for row in source_map["files"] if row.get("package_path") == package_path]
    if matches:
        require(len(matches) == 1, f"duplicate mapping row: {package_path}")
        row = matches[0]
        require(row.get("source_path") == source_path, f"source mapping drift: {package_path}")
        if transformations is None:
            transformations = row.get("mechanical_transformations", [])
    else:
        require(transformations == [], f"new transformed mapping requires explicit handling: {package_path}")
        row = {
            "package_path": package_path,
            "source_path": source_path,
            "mechanical_transformations": [],
            "prior_cross_document_reference_repair": False,
        }
        source_map["files"].append(row)
    assert transformations is not None
    staged = apply_transformations(source, transformations)
    row.update(
        source_sha256=sha_bytes(source),
        staged_intermediate_sha256=sha_bytes(source),
        sha256=sha_bytes(staged),
        bytes=len(staged),
        mechanical_transformations=transformations,
    )
    return staged


def build_readme() -> bytes:
    path = STAGE / "README.md"
    text = path.read_text(encoding="utf-8")
    anchor = (
        "The affine analytic delivery is verified by `overleaf/sync_20260904/"
        "affine_analytic_remote_receipt.json`; `main.tex` and `research_companion.tex` "
        "compile in this project to 184 and 57 pages respectively.\n"
    )
    addition = (
        anchor
        + "The local canonical staging tree additionally contains the signed fixed-content "
        "necklace revision. Its verified live builds have 185 critical-reader pages and 59 "
        "companion pages; the exact nine-path remote update is pending.\n"
    )
    require(text.count(anchor) == 1, "README remote-baseline anchor drifted")
    text = text.replace(anchor, addition)
    old = (
        "The source files are current; dates printed on older live title pages are preserved. "
        "This is a working research project, not a publication, complete corpus, or new claim "
        "audit. Compilation verifies source/reference integrity. Existing certificate scripts "
        "are included intact but were not rerun for this synchronization. The separate Tao "
        "draft's mathematical status is stated in its abstract and source manifest."
    )
    new = (
        "The staged source files are current for the signed fixed-content revision; dates "
        "printed on older live title pages are preserved. This is a working research project, "
        "not a publication or complete corpus. The companion's seven portable certificates "
        "were rerun by the 18-source package validator, which also performed two isolated "
        "byte-identical builds. The separate Tao draft's mathematical status is stated in its "
        "abstract and source manifest."
    )
    require(text.count(old) == 1, "README certificate-status paragraph drifted")
    text = text.replace(old, new)
    command_anchor = "    python companion/certificates/affine_packet_series_checks.py\n"
    require(text.count(command_anchor) == 1, "README certificate command anchor drifted")
    text = text.replace(
        command_anchor,
        command_anchor + "    python companion/certificates/affine_signed_necklace_checks.py\n",
    )
    text += (
        "\n## Signed fixed-content necklace checkpoint\n\n"
        "For fixed odd-step length `m` and exponent budget `A`, the companion separates "
        "primitive pointed exponent words, cyclic rational orbits, and individual orbit "
        "points. It proves the classical fixed-content Möbius count, transports it through "
        "the exact packet--parity correspondence, and partitions the rational orbits by the "
        "sign of `2^A-3^m`. Stanley supplies the classical enumeration; Lagarias supplies the "
        "rational-cycle coordinates. No integrality, termination, novelty, or priority claim "
        "is made.\n"
    )
    return text.encode("utf-8")


def prepare_payloads() -> tuple[dict[str, bytes], dict]:
    source_map = read_json(STAGE / "SOURCE_MAP.json")
    require(source_map.get("canonical_project") == PROJECT_ID, "wrong canonical project")

    payloads: dict[str, bytes] = {}
    payloads["companion/bibliography.tex"] = update_mapping_record(
        source_map,
        "research_companion/bibliography.tex",
        "companion/bibliography.tex",
    )
    payloads[
        "companion/chapters/04_affine_packets_parity_necklaces_and_residue_automata.tex"
    ] = update_mapping_record(
        source_map,
        "research_companion/chapters/04_affine_packets_parity_necklaces_and_residue_automata.tex",
        "companion/chapters/04_affine_packets_parity_necklaces_and_residue_automata.tex",
    )
    payloads["companion/certificates/affine_signed_necklace_checks.py"] = update_mapping_record(
        source_map,
        "research_companion/certificates/affine_signed_necklace_checks.py",
        "companion/certificates/affine_signed_necklace_checks.py",
        [],
    )

    critical_row = next(
        row
        for row in source_map["files"]
        if row.get("package_path") == "critical/chapters/06_affine_packet_source_audit.tex"
    )
    critical_transformations = list(critical_row["mechanical_transformations"])
    critical_transformations.extend(
        [
            {
                "type": "Displayed resource path prefix",
                "before": "\\path{research_companion/}",
                "after": "\\path{companion/}",
            },
            {
                "type": "Displayed resource path prefix",
                "before": "\\path{certificates/affine_signed_necklace_checks.py}",
                "after": "\\path{companion/certificates/affine_signed_necklace_checks.py}",
            },
        ]
    )
    payloads["critical/chapters/06_affine_packet_source_audit.tex"] = update_mapping_record(
        source_map,
        "tex/chapters/06_affine_packet_source_audit.tex",
        "critical/chapters/06_affine_packet_source_audit.tex",
        critical_transformations,
    )
    payloads["critical/chapters/99_source_register.tex"] = update_mapping_record(
        source_map,
        "tex/chapters/99_source_register.tex",
        "critical/chapters/99_source_register.tex",
    )

    companion_entry = next(
        row for row in source_map["entries"] if row.get("entrypoint") == "research_companion.tex"
    )
    companion_entry["labels"] = 176
    companion_entry["references"] = 123
    critical_entry = next(row for row in source_map["entries"] if row.get("entrypoint") == "main.tex")
    require(
        (critical_entry.get("labels"), critical_entry.get("references")) == (631, 587),
        "critical closure metrics drifted",
    )
    source_map["signed_fixed_content_necklace_revision"] = {
        "updated_utc": datetime.now(timezone.utc).isoformat(),
        "claim": "CLM-COL-000200",
        "source": "SRC-COL-000052",
        "paths": list(SEMANTIC_PATHS),
        "scope": "Primitive fixed-content packet words, exact-period rational orbits, individual orbit points, and the exact denominator-sign partition.",
        "local_package_visual_receipt": "research_companion/audit/affine_signed_necklace_package_visual_20260905.json",
        "portable_manifested_sources": 18,
        "portable_certificates": 7,
        "live_builds": {
            "research_companion.tex": {
                "pages": 59,
                "sha256": SOURCES["research_companion/output/pdf/collatz_research_companion.pdf"],
            },
            "main.tex": {
                "pages": 185,
                "sha256": SOURCES["output/pdf/collatz_working_corpus.pdf"],
            },
        },
        "remote_status": "exact_nine_path_update_pending",
        "new_project": False,
    }
    payloads["SOURCE_MAP.json"] = json_bytes(source_map)

    status = read_json(STAGE / "PACKAGE_STATUS.json")
    status["status"] = (
        "Signed fixed-content necklace revision locally built, visually inspected, and "
        "portable-package validated; exact canonical remote update pending."
    )
    status["local_workbench_unchanged"] = False
    status["certificates_executed_for_sync"] = True
    status["portable_research_companion_validation"] = {
        "status": "PASS",
        "scope": "All 18 manifested portable sources, seven-file TeX closure, seven certificates, two isolated deterministic rebuilds, declared PDF identity, and the specified 59-page visual closure.",
        "watch_receipt": "research_companion/audit/package_validation/run_20260904T233943Z/watch_receipt.json",
        "watch_receipt_sha256": SOURCES[
            "research_companion/audit/package_validation/run_20260904T233943Z/watch_receipt.json"
        ],
        "validator_stdout": "research_companion/audit/package_validation/run_20260904T233943Z/validator_stdout.json",
        "validator_stdout_sha256": SOURCES[
            "research_companion/audit/package_validation/run_20260904T233943Z/validator_stdout.json"
        ],
        "cap_bytes": 5_000_000_000,
        "peak_aggregate_rss_bytes": 228_900_864,
        "peak_aggregate_private_bytes": 283_963_392,
        "process_tree_clear": True,
        "output_pdf": {
            "declared_pdf": "research_companion/output/pdf/collatz_research_companion.pdf",
            "declared_pdf_sha256": SOURCES[
                "research_companion/output/pdf/collatz_research_companion.pdf"
            ],
            "pages": 59,
            "directly_inspected_pages": [2, 44, 45, 46, 57, 58],
            "material_visual_defects": [],
        },
        "remote_action": False,
    }
    status["signed_fixed_content_necklace_revision"] = {
        "status": "local_build_visual_and_portable_validation_pass_remote_sync_pending",
        "claim": "CLM-COL-000200",
        "source": "SRC-COL-000052",
        "scope": "Exact fixed-content Möbius count, packet--parity transport, denominator-sign partition, and separation of pointed words, cyclic rational orbits, and orbit points.",
        "classical_lineage": ["Stanley2024", "Lagarias1990", "LaarhovenDeWeger2012"],
        "local_builds": source_map["signed_fixed_content_necklace_revision"]["live_builds"],
        "visual_QA": {
            "status": "PASS",
            "companion_pages": [2, 44, 45, 46, 57, 58],
            "critical_pages": [3, 171, 172, 174, 176, 177, 178],
            "receipt": "research_companion/audit/affine_signed_necklace_package_visual_20260905.json",
        },
        "remote_action": False,
        "pending_upload_paths": list(UPLOAD_PATHS),
        "new_project": False,
    }
    payloads["PACKAGE_STATUS.json"] = json_bytes(status)
    payloads["README.md"] = build_readme()

    current_paths = {
        path.relative_to(STAGE).as_posix(): path.read_bytes()
        for path in STAGE.rglob("*")
        if path.is_file() and path.name != "MANIFEST.json"
    }
    current_paths.update({key: value for key, value in payloads.items() if key != "MANIFEST.json"})
    require(len(current_paths) == 50, f"expected 50 canonical children, got {len(current_paths)}")
    manifest = {
        "schema_version": 1,
        "hash": "sha256",
        "files": [identity(path, current_paths[path]) for path in sorted(current_paths)],
    }
    payloads["MANIFEST.json"] = json_bytes(manifest)
    return payloads, manifest


def verify_stage() -> dict:
    manifest_payload = (STAGE / "MANIFEST.json").read_bytes()
    manifest = json.loads(manifest_payload.decode("utf-8"))
    require(manifest.get("schema_version") == 1, "unexpected manifest schema")
    require(manifest.get("hash") == "sha256", "manifest hash algorithm is not sha256")
    records = manifest.get("files")
    require(isinstance(records, list) and len(records) == 50, "manifest must have 50 children")
    paths = [record.get("path") for record in records]
    require(len(set(paths)) == 50, "duplicate manifest path")
    actual_paths = {
        path.relative_to(STAGE).as_posix()
        for path in STAGE.rglob("*")
        if path.is_file() and path.name != "MANIFEST.json"
    }
    require(actual_paths == set(paths), "manifest/stage path-set mismatch")
    for record in records:
        payload = (STAGE / record["path"]).read_bytes()
        require(identity(record["path"], payload) == record, f"manifest mismatch: {record['path']}")

    source_map = read_json(STAGE / "SOURCE_MAP.json")
    require(source_map.get("canonical_project") == PROJECT_ID, "source map project drift")
    require(len(source_map.get("files", [])) == 47, "source map must have 47 file rows")
    for package_path in SEMANTIC_PATHS:
        rows = [row for row in source_map["files"] if row.get("package_path") == package_path]
        require(len(rows) == 1, f"mapping row count mismatch: {package_path}")
        row = rows[0]
        source = (ROOT / row["source_path"]).read_bytes()
        staged = apply_transformations(source, row.get("mechanical_transformations", []))
        require(row["source_sha256"] == sha_bytes(source), f"source hash drift: {package_path}")
        require(row["sha256"] == sha_bytes(staged), f"mapped hash drift: {package_path}")
        require((STAGE / package_path).read_bytes() == staged, f"staged bytes drift: {package_path}")

    v5_tokens = ("V5", "Tao5", "1909.03562v5")
    tao_files = [STAGE / "tao_preprint.tex", *sorted((STAGE / "tao").rglob("*.tex"))]
    hits = [str(path) for path in tao_files if any(token.lower() in path.read_text(encoding="utf-8").lower() for token in v5_tokens)]
    require(not hits, f"reader-facing Tao V5 material found: {hits}")
    return {
        "status": "PASS",
        "manifested_children": 50,
        "source_map_rows": 47,
        "upload_paths": list(UPLOAD_PATHS),
        "manifest_sha256": sha_bytes(manifest_payload),
        "tao_reader_facing_v5_hits": 0,
    }


def prepare() -> None:
    require(not RECEIPT.exists(), f"stage receipt already exists: {RECEIPT}")
    for relative, expected in BASELINE.items():
        require(sha(STAGE / relative) == expected, f"baseline drift: {relative}")
    for relative, expected in SOURCES.items():
        require(sha(ROOT / relative) == expected, f"source drift: {relative}")
    baseline_manifest = read_json(STAGE / "MANIFEST.json")
    require(len(baseline_manifest.get("files", [])) == 49, "baseline must have 49 children")
    require(
        not (STAGE / "companion/certificates/affine_signed_necklace_checks.py").exists(),
        "new certificate already exists in baseline stage",
    )

    payloads, manifest = prepare_payloads()
    before = {
        path: identity(path, (STAGE / path).read_bytes())
        for path in BASELINE
        if (STAGE / path).is_file()
    }
    after = {path: identity(path, payload) for path, payload in payloads.items()}
    changed = sorted(
        path
        for path, record in after.items()
        if path not in before or before[path]["sha256"] != record["sha256"]
    )
    require(changed == sorted(UPLOAD_PATHS), f"unexpected nine-path delta: {changed}")
    receipt = {
        "schema_version": 1,
        "receipt_id": "SIGNED-NECKLACE-STAGE-20260905",
        "recorded_utc": datetime.now(timezone.utc).isoformat(),
        "status": "prepared_local_stage_remote_upload_pending",
        "project_id": PROJECT_ID,
        "upload_paths": list(UPLOAD_PATHS),
        "manifested_children": len(manifest["files"]),
        "before": before,
        "after": after,
        "local_closure_receipt": "research_companion/audit/affine_signed_necklace_package_visual_20260905.json",
        "remote_sync_complete": False,
        "new_project": False,
        "Lean_launched": False,
        "AGENTS_edits": False,
    }
    writes = {STAGE / path: payload for path, payload in payloads.items()}
    writes[RECEIPT] = json_bytes(receipt)
    transactional_write(writes)
    result = verify_stage()
    print(json.dumps({**result, "stage_receipt": str(RECEIPT.relative_to(ROOT))}, indent=2))


def verify_remote_zip(path: Path) -> dict:
    require(path.is_file(), f"source ZIP absent: {path}")
    local_manifest_payload = (STAGE / "MANIFEST.json").read_bytes()
    local_manifest = json.loads(local_manifest_payload.decode("utf-8"))
    stage_result = verify_stage()
    expected_paths = {record["path"] for record in local_manifest["files"]}
    with ZipFile(path) as archive:
        infos = [info for info in archive.infolist() if not info.is_dir()]
        names = [info.filename for info in infos]
        require(len(names) == len(set(names)), "duplicate ZIP members")
        members = {info.filename: info for info in infos}
        require(members.get("MANIFEST.json") is not None, "remote MANIFEST.json absent")
        require(
            archive.read(members["MANIFEST.json"]) == local_manifest_payload,
            "remote MANIFEST.json differs from local stage",
        )
        extras = set(names) - expected_paths - {"MANIFEST.json"}
        require(extras == EXPECTED_REMOTE_EXTRAS, f"remote extra-set mismatch: {sorted(extras)}")
        for record in local_manifest["files"]:
            name = record["path"]
            require(name in members, f"remote manifested child absent: {name}")
            payload = archive.read(members[name])
            require(identity(name, payload) == record, f"remote manifest mismatch: {name}")
            require(payload == (STAGE / name).read_bytes(), f"remote/local byte mismatch: {name}")
    return {
        **stage_result,
        "status": "PASS_REMOTE_SOURCE_IDENTITY",
        "zip": path.name,
        "zip_bytes": path.stat().st_size,
        "zip_sha256": sha(path),
        "remote_files_total": 66,
        "manifested_children_verified": 50,
        "manifest_verified": True,
        "historical_extras_verified": 15,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="mode", required=True)
    subparsers.add_parser("prepare")
    subparsers.add_parser("verify-stage")
    zip_parser = subparsers.add_parser("verify-zip")
    zip_parser.add_argument("source_zip", type=Path)
    args = parser.parse_args()
    if args.mode == "prepare":
        prepare()
    elif args.mode == "verify-stage":
        print(json.dumps(verify_stage(), indent=2))
    else:
        print(json.dumps(verify_remote_zip(args.source_zip.resolve()), indent=2))


if __name__ == "__main__":
    main()
