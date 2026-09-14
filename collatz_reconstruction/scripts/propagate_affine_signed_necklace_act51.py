from __future__ import annotations

import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECEIPT_ID = "ACT-COL-000051"
CLAIM_ID = "CLM-COL-000200"
SOURCE_ID = "SRC-COL-000052"

EXPECTED = {
    "state/source_registry.jsonl": "619ce968d1c97801a74e5e9e8e627fec1296078b50689c3bf1dbcae596078a87",
    "state/claims.jsonl": "3d2a76fc9e56b63af701d146a17b347c78c3880c053f28e448fd25e556d2aac9",
    "state/programmes.jsonl": "0fdd922c4c9e0edff3e40b9096250ddac9769b6ca3bb8f83d1aca5832dcb8664",
    "state/affine_packet_current.json": "edf01cb4a8f351d055fa3a989da2fff11b9f3606760bf6c278ae01c93e61cffa",
    "state/affine_analytic_current.json": "b721cba8e82cc361e5cd146652df7cea613ba2c819ca42651ea43a1fbe84565c",
    "state/project_state.json": "ec48f3c08a72c5bd398dd7a8b18c28e60a6504a20b5b09123d0e60fea4d86beb",
    "state/coverage.json": "219304ac0f1b6f358517365d72896c8d8b9153bdc9bba5c2d45df58ddf87e681",
    "state/overleaf_current.json": "38c0339829ec42c51604020e3093e777b54c23c320f73e6db1cf788b6abb5895",
    "state/action_receipts.jsonl": "66656c3984a8fcae4294b16156165bcd33b0a745383ce73406b0c4e8831ccac2",
}

SUPPORT = {
    "TODO.md": "61c437ed6475cf08c46292c95c800792ab8ae223da635f442ad0ef920e72996e",
    "research_companion/chapters/04_affine_packets_parity_necklaces_and_residue_automata.tex": "f5a25459b6f0088d14158426b6ca6085c021b5722c972a495bcd2ece7887663e",
    "tex/chapters/06_affine_packet_source_audit.tex": "8a4de14fddc13259bb6144866a9924ec9fa58b37477786e0f0a0b789188d91db",
    "research_companion/certificates/affine_signed_necklace_checks.py": "8e51437eb64c5c9cee6601d6fe654383302a3ee3d1430c52981ec9b773c29c97",
    "research_companion/audit/affine_signed_necklace_checks_20260905.json": "2518cb91702a3ea91f8e3e519d9b69d8c31e0bb79c94170a920dbd06cf1e1a94",
    "research_companion/audit/affine_signed_necklace_reconstruction_20260905.json": "0ff92a85fe32277c73baad82ee0b381a4a0f52f903d1efa0e491d5e19bcfcb61",
    "research_companion/audit/affine_signed_necklace_package_visual_20260905.json": "9ea79f1eb40a41e125d570b663f68af64a7cc46dba3cc20d3f391714008a53fe",
    "research_companion/MANIFEST.json": "bc1ab3bb5ec00432623cb259281c2b25cd6565df10072cf4ef602bb156144828",
    "research_companion/output/pdf/collatz_research_companion.pdf": "074dcc1be3c5a66f28a8568a725d0a0093583faabff888bac177d24c6360119b",
    "output/pdf/collatz_working_corpus.pdf": "24fa733fa1ba7a39a371b64d6d679912c2af15f4fc014ff8eadc9ad4aa209899",
    "research_companion/audit/package_validation/run_20260904T233943Z/watch_receipt.json": "8f257f43fd2f706f5fc12028e8f83026612cf5e0357928c2e374955eb10b8da5",
    "research_companion/audit/package_validation/run_20260904T233943Z/validator_stdout.json": "d49975c27e2f02d25bbc35f71093881ff61bbaf65b9a3e25925bd13035917de1",
}


def sha(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def read_json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def read_jsonl(relative: str) -> list[dict]:
    return [
        json.loads(line)
        for line in (ROOT / relative).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def jsonl_bytes(records: list[dict]) -> bytes:
    return (
        "\n".join(
            json.dumps(record, ensure_ascii=False, separators=(",", ":"))
            for record in records
        )
        + "\n"
    ).encode("utf-8")


def file_record(relative: str) -> dict:
    path = ROOT / relative
    return {"path": relative, "bytes": path.stat().st_size, "sha256": sha(path)}


def put_file_record(records: list[dict], relative: str) -> None:
    current = file_record(relative)
    for index, record in enumerate(records):
        if record.get("path") == relative:
            records[index] = current
            return
    records.append(current)


def commit(outputs: dict[str, bytes]) -> None:
    staged: list[tuple[Path, Path]] = []
    originals: dict[Path, bytes] = {}
    replaced: list[Path] = []
    try:
        for relative, payload in outputs.items():
            target = ROOT / relative
            originals[target] = target.read_bytes()
            descriptor, temporary = tempfile.mkstemp(
                prefix=f".{target.name}.act51-", suffix=".tmp", dir=target.parent
            )
            os.close(descriptor)
            temporary_path = Path(temporary)
            temporary_path.write_bytes(payload)
            staged.append((target, temporary_path))
        try:
            for target, temporary_path in staged:
                os.replace(temporary_path, target)
                replaced.append(target)
        except Exception:
            for target in reversed(replaced):
                target.write_bytes(originals[target])
            raise
    finally:
        for _, temporary_path in staged:
            temporary_path.unlink(missing_ok=True)


def main() -> None:
    for relative, expected in {**EXPECTED, **SUPPORT}.items():
        require(sha(ROOT / relative) == expected, f"preflight hash mismatch: {relative}")

    now = datetime.now(timezone.utc).isoformat()
    chapter = file_record(
        "research_companion/chapters/04_affine_packets_parity_necklaces_and_residue_automata.tex"
    )
    critical = file_record("tex/chapters/06_affine_packet_source_audit.tex")
    certificate = file_record(
        "research_companion/certificates/affine_signed_necklace_checks.py"
    )
    certificate_execution = file_record(
        "research_companion/audit/affine_signed_necklace_checks_20260905.json"
    )
    reconstruction = file_record(
        "research_companion/audit/affine_signed_necklace_reconstruction_20260905.json"
    )
    package_visual = file_record(
        "research_companion/audit/affine_signed_necklace_package_visual_20260905.json"
    )
    portable_manifest = file_record("research_companion/MANIFEST.json")
    companion_pdf = file_record(
        "research_companion/output/pdf/collatz_research_companion.pdf"
    )
    critical_pdf = file_record("output/pdf/collatz_working_corpus.pdf")
    validation_receipt = file_record(
        "research_companion/audit/package_validation/run_20260904T233943Z/watch_receipt.json"
    )
    validation_stdout = file_record(
        "research_companion/audit/package_validation/run_20260904T233943Z/validator_stdout.json"
    )

    signed = {
        "claim": CLAIM_ID,
        "source": SOURCE_ID,
        "raw_locator": "CHATINT-COL-000002 physical lines 1041-1083",
        "proof": {**chapter, "label": "thm:signed-fixed-content-necklace-count"},
        "critical_crosswalk": critical,
        "certificate": certificate,
        "execution_receipt": certificate_execution,
        "audit": reconstruction,
        "package_visual_receipt": package_visual,
        "portable_manifest": portable_manifest,
        "companion_pdf": {**companion_pdf, "pages": 59},
        "critical_pdf": {**critical_pdf, "pages": 185},
        "package_validation_receipt": validation_receipt,
        "package_validation_stdout": validation_stdout,
        "morphisms_used": ["MOR-COL-000064", "MOR-COL-000065"],
        "typed_source_repairs": [
            "raw line 1083 word/orbit/point conflation",
            "antecedent pointed-periodic-word biconditional already repaired by CLM-COL-000193",
            "finite-strip table reading order repaired during page-level visual inspection",
        ],
        "package_validation_complete": True,
        "page_QA_complete": True,
        "remote_sync_complete": False,
        "whole_raw_reconciliation_complete": False,
    }

    sources = read_jsonl("state/source_registry.jsonl")
    source = next(record for record in sources if record.get("source_id") == SOURCE_ID)
    source["audit"] = {
        "path": reconstruction["path"],
        "sha256": reconstruction["sha256"],
        "status": "direct_page_and_formula_crosswalk",
    }

    claims = read_jsonl("state/claims.jsonl")
    claim = next(record for record in claims if record.get("claim_id") == CLAIM_ID)
    formal = claim["formal_status"]
    formal["execution_receipt_sha256"] = certificate_execution["sha256"]
    formal["reconstruction_audit_sha256"] = reconstruction["sha256"]
    formal["portable_package_validation"] = {
        "status": "PASS",
        "manifested_source_files": 18,
        "portable_certificates": 7,
        "isolated_reproducible_builds": 2,
        "receipt": validation_receipt,
    }
    formal["page_QA"] = {
        "status": "PASS",
        "receipt": package_visual,
        "companion_pages_inspected": [2, 44, 45, 46, 57, 58],
        "critical_pages_inspected": [3, 171, 172, 174, 176, 177, 178],
    }

    programmes = read_jsonl("state/programmes.jsonl")
    programme = next(
        record for record in programmes if record.get("programme_id") == "PRG-COL-0001"
    )
    programme["status"] = (
        "bounded_reconstruction_extended_through_affine_packets_analytic_series_"
        "and_signed_fixed_content_counts_local_package_visual_pass_remote_resync_pending"
    )
    cert_record = next(
        item for item in programme["certificates"] if item.get("path") == certificate["path"]
    )
    cert_record.update(
        certificate,
        status="PASS_bounded_exact_signed_fixed_content_necklace_checks",
        execution_receipt=certificate_execution["path"],
        execution_receipt_sha256=certificate_execution["sha256"],
    )
    programme["signed_necklace_reconstruction"] = {
        **signed,
        "certificate": cert_record,
    }

    packet = read_json("state/affine_packet_current.json")
    packet.update(
        checkpoint="AFFINE-SIGNED-NECKLACE-LOCAL-CLOSURE-20260905",
        updated_utc=now,
        remote_sync_status="local_package_build_visual_and_validation_pass_remote_resync_pending",
        next_action="Stage and upload the exact nine-path signed-necklace delta to canonical Overleaf project 6a91f06e408dd545780c660f; compile research_companion.tex and main.tex; verify a fresh 66-file source download.",
        portable_apparatus_complete=True,
        formal_status="all-parameter proof, exact finite Python certificate, 18-source portable manifest, seven-certificate validator and page-level visual QA PASS; no Lean launch",
    )
    for relative in (
        chapter["path"],
        critical["path"],
        certificate_execution["path"],
        reconstruction["path"],
        package_visual["path"],
        portable_manifest["path"],
        companion_pdf["path"],
        critical_pdf["path"],
        validation_receipt["path"],
        validation_stdout["path"],
    ):
        put_file_record(packet["files"], relative)
    packet["signed_necklace_reconstruction"] = signed

    analytic = read_json("state/affine_analytic_current.json")
    analytic.update(
        updated_utc=now,
        status="signed_fixed_content_necklace_local_package_build_visual_and_validation_pass_remote_resync_pending",
        active_tex=chapter["path"],
        parallel_tex=critical["path"],
        remote_synced=False,
        next_action="Synchronize the exact nine-path signed-necklace delta to the one canonical Overleaf project, verify both affected builds and a fresh source download, then resume raw affine lines 1091-1208.",
    )
    analytic["signed_necklace_reconstruction"] = signed

    project = read_json("state/project_state.json")
    project.update(
        updated_utc=now,
        last_receipt_id=RECEIPT_ID,
        active_task="canonical_signed_necklace_nine_path_remote_sync",
        next_action="Synchronize the exact nine-path signed fixed-content necklace revision to canonical Overleaf project 6a91f06e408dd545780c660f, compile research_companion.tex and main.tex, and verify the fresh source download before resuming raw affine lines 1091-1208.",
    )
    request = project["current_request_state"]
    request.update(
        active_local_tex=chapter["path"],
        active_parallel_tex=critical["path"],
        active_tex_sha256=chapter["sha256"],
        active_parallel_tex_sha256=critical["sha256"],
        active_write_status="signed_fixed_content_necklace_local_build_portable_validation_and_visual_QA_pass_remote_sync_active",
        latest_immediate_request_status="Tao_preprint remains V7-only; signed affine-necklace local closure passed and exact canonical remote synchronization is active",
    )
    project["latest_local_admission"] = {
        "receipt_id": RECEIPT_ID,
        "claim": CLAIM_ID,
        "source": SOURCE_ID,
        "audit": reconstruction,
        "package_visual_receipt": package_visual,
        "portable_validation_receipt": validation_receipt,
        "remote_sync_complete": False,
        "sealed_remote_checkpoint_remains": project["current_checkpoint"],
    }

    coverage = read_json("state/coverage.json")
    coverage["coverage_status"] = (
        "active_signed_fixed_content_necklace_local_package_build_visual_and_"
        "validation_pass_remote_resync_pending_wider_raw_reconciliation_active"
    )
    coverage["post_ACT51_signed_fixed_content_necklace_local_closure"] = {
        "receipt_id": RECEIPT_ID,
        "claim": CLAIM_ID,
        "source": SOURCE_ID,
        "morphisms_used": ["MOR-COL-000064", "MOR-COL-000065"],
        "companion_chapter": chapter,
        "critical_chapter": critical,
        "certificate": certificate,
        "execution_receipt": certificate_execution,
        "content_audit": reconstruction,
        "package_visual_receipt": package_visual,
        "portable_manifest": portable_manifest,
        "portable_package_validation_complete": True,
        "visual_QA_complete": True,
        "remote_sync_complete": False,
        "full_raw_3021_line_reconciliation": False,
        "whole_corpus_complete": False,
    }

    overleaf = read_json("state/overleaf_current.json")
    overleaf.update(
        status="signed_fixed_content_necklace_local_package_build_visual_and_validation_pass_remote_resync_pending",
        updated_utc=now,
        pending_action="Upload the exact nine-path delta to this same canonical project, with MANIFEST.json last; compile research_companion.tex and main.tex; download and verify the exact 66-file closure.",
        pending_remote_delta=[
            "companion/bibliography.tex",
            "companion/chapters/04_affine_packets_parity_necklaces_and_residue_automata.tex",
            "companion/certificates/affine_signed_necklace_checks.py",
            "critical/chapters/06_affine_packet_source_audit.tex",
            "critical/chapters/99_source_register.tex",
            "SOURCE_MAP.json",
            "PACKAGE_STATUS.json",
            "README.md",
            "MANIFEST.json",
        ],
    )
    overleaf["local_signed_necklace_revision"] = {
        **signed,
        "canonical_project_unchanged": True,
        "new_project_created": False,
    }

    receipts = read_jsonl("state/action_receipts.jsonl")
    numbers = sorted(int(record["receipt_id"].rsplit("-", 1)[1]) for record in receipts)
    require(numbers == list(range(1, 51)), "action receipt IDs are not exactly 1-50")
    receipts.append(
        {
            "record_type": "action_receipt",
            "schema_version": "1.0",
            "receipt_id": RECEIPT_ID,
            "timestamp_utc": now,
            "action": "signed_fixed_content_necklace_local_build_portable_validation_page_level_visual_QA_and_layout_repair",
            "inputs": [
                "ACT-COL-000050",
                chapter["path"],
                critical["path"],
                certificate["path"],
            ],
            "outputs": [
                companion_pdf["path"],
                critical_pdf["path"],
                portable_manifest["path"],
                validation_receipt["path"],
                validation_stdout["path"],
                package_visual["path"],
                "state/source_registry.jsonl",
                "state/claims.jsonl",
                "state/programmes.jsonl",
                "state/affine_packet_current.json",
                "state/affine_analytic_current.json",
                "state/project_state.json",
                "state/coverage.json",
                "state/overleaf_current.json",
                "state/action_receipts.jsonl",
                "TODO.md",
            ],
            "result": "local_59_page_companion_and_185_page_critical_reader_build_log_font_parse_visual_and_portable_package_validation_pass_exact_nine_path_remote_delta_pending",
            "claim": CLAIM_ID,
            "source": SOURCE_ID,
            "portable_package": {
                "manifested_source_files": 18,
                "portable_certificates": 7,
                "isolated_reproducible_builds": 2,
                "validation_receipt": validation_receipt,
                "status": "PASS",
            },
            "builds": {
                "research_companion": {**companion_pdf, "pages": 59},
                "critical_reader": {**critical_pdf, "pages": 185},
            },
            "visual_QA": {
                "status": "PASS",
                "receipt": package_visual,
                "companion_pages": [2, 44, 45, 46, 57, 58],
                "critical_pages": [3, 171, 172, 174, 176, 177, 178],
                "repairs": [
                    "finite-strip table reading order",
                    "certificate locator directory-boundary wrap",
                ],
            },
            "remote_sync_complete": False,
            "whole_raw_affine_reconciliation_complete": False,
            "goal_complete": False,
            "Lean_started": False,
            "AGENTS_edits": False,
            "new_project": False,
            "tao_reader_baseline": "V7_only_zero_V5_references",
        }
    )

    outputs = {
        "state/source_registry.jsonl": jsonl_bytes(sources),
        "state/claims.jsonl": jsonl_bytes(claims),
        "state/programmes.jsonl": jsonl_bytes(programmes),
        "state/affine_packet_current.json": json_bytes(packet),
        "state/affine_analytic_current.json": json_bytes(analytic),
        "state/project_state.json": json_bytes(project),
        "state/coverage.json": json_bytes(coverage),
        "state/overleaf_current.json": json_bytes(overleaf),
        "state/action_receipts.jsonl": jsonl_bytes(receipts),
    }
    commit(outputs)
    print(
        json.dumps(
            {
                "status": "PASS",
                "receipt": RECEIPT_ID,
                "outputs": {
                    relative: {
                        "bytes": (ROOT / relative).stat().st_size,
                        "sha256": sha(ROOT / relative),
                    }
                    for relative in outputs
                },
                "portable_package_validation_complete": True,
                "visual_QA_complete": True,
                "remote_sync_complete": False,
                "Lean_launched": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
