"""Seal the reproducible research-companion package checkpoint.

The script verifies the completed bounded validator, the portable manifest,
the declared PDF, page-level text/raster identity to the already reviewed
ACT47 build, and the reader-facing Tao V7 boundary.  It then records ACT48 and
refreshes only durable state and canonical-project metadata.  It performs no
browser, Git, Lean, archive, publication, or source-mathematics action.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "research_companion"
STAGE = ROOT / "overleaf/sync_20260904/canonical_project"
VALIDATION_RUN = PACKAGE / "audit/package_validation/run_20260904T221258Z"
WATCH_RECEIPT = VALIDATION_RUN / "watch_receipt.json"
VALIDATOR_STDOUT = VALIDATION_RUN / "validator_stdout.json"
DECLARED_PDF = PACKAGE / "output/pdf/collatz_research_companion.pdf"
REVIEWED_PDF = (
    ROOT
    / "overleaf/sync_20260904/audit/affine_analytic/"
    "run_20260904T170410Z/live_companion/main.pdf"
)
PORTABLE_MANIFEST = PACKAGE / "MANIFEST.json"
QA_REL = "qa/ACT48-RESEARCH-COMPANION-PACKAGE.json"
QA = ROOT / QA_REL
ACT_ID = "ACT-COL-000048"
ACT47 = ROOT / "qa/ACT47-AFFINE-ANALYTIC-CHECKPOINT.json"
ACT46_LOCAL = (
    ROOT
    / "overleaf/sync_20260904/audit/affine_crt/"
    "run_20260904T152745Z/local_receipt.json"
)
EXPECTED_PDF_SHA = "cb3ddd8e4ad4dd6ca5802762da92f40a1b98f6e4e5302e58dd445dee236336c7"
EXPECTED_STDOUT_SHA = "a784affdc60740f970db9b3d13ac282e6f7e62f1dd538ed50ee5134a9440fc5a"


def sha_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def read_jsonl(path: Path):
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def write_jsonl(path: Path, rows) -> None:
    path.write_text(
        "\n".join(
            json.dumps(row, ensure_ascii=False, separators=(",", ":"))
            for row in rows
        )
        + "\n",
        encoding="utf-8",
    )


def inventory(root: Path):
    return {
        path.relative_to(root).as_posix(): sha_file(path)
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def validate_portable_manifest() -> dict:
    manifest = read_json(PORTABLE_MANIFEST)
    if manifest.get("schema_version") != "1.0":
        raise RuntimeError("portable manifest schema mismatch")
    files = manifest.get("files")
    if not isinstance(files, dict) or len(files) != 17:
        raise RuntimeError(f"expected 17 portable source files, found {len(files)}")
    for relative, identity in files.items():
        path = PACKAGE / relative
        if not path.is_file():
            raise RuntimeError(f"portable source missing: {relative}")
        if path.stat().st_size != identity.get("bytes"):
            raise RuntimeError(f"portable source byte count mismatch: {relative}")
        if sha_file(path) != identity.get("sha256"):
            raise RuntimeError(f"portable source hash mismatch: {relative}")
    output = manifest.get("output_pdf", {})
    if output.get("path") != "output/pdf/collatz_research_companion.pdf":
        raise RuntimeError("declared output path mismatch")
    if output.get("bytes") != DECLARED_PDF.stat().st_size:
        raise RuntimeError("declared output byte count mismatch")
    if output.get("sha256") != sha_file(DECLARED_PDF):
        raise RuntimeError("declared output hash mismatch")
    return manifest


def validate_bounded_run() -> dict:
    receipt = read_json(WATCH_RECEIPT)
    stdout_result = read_json(VALIDATOR_STDOUT)
    required = {
        "returncode": 0,
        "termination_reason": None,
        "process_tree_clear": True,
        "cap_bytes": 5_000_000_000,
    }
    for key, expected in required.items():
        if receipt.get(key) != expected:
            raise RuntimeError(f"bounded validator receipt mismatch: {key}")
    if receipt.get("peak_aggregate_rss_bytes", 5_000_000_000) >= 5_000_000_000:
        raise RuntimeError("validator RSS reached cap")
    if receipt.get("peak_aggregate_private_bytes", 5_000_000_000) >= 5_000_000_000:
        raise RuntimeError("validator private memory reached cap")
    if sha_file(VALIDATOR_STDOUT) != EXPECTED_STDOUT_SHA:
        raise RuntimeError("validator stdout identity mismatch")
    if receipt.get("stdout_sha256") != EXPECTED_STDOUT_SHA:
        raise RuntimeError("receipt stdout identity mismatch")
    if receipt.get("validator_result") != stdout_result:
        raise RuntimeError("receipt/result payload mismatch")
    if stdout_result.get("status") != "PASS":
        raise RuntimeError("portable validator did not pass")
    if stdout_result.get("manifested_source_files") != 17:
        raise RuntimeError("portable validator source-count mismatch")
    if stdout_result.get("tex") != {
        "citations": 22,
        "labels": 170,
        "references": 88,
        "tex_files": 7,
    }:
        raise RuntimeError("portable TeX closure metrics mismatch")
    if stdout_result.get("affine_series_certificate_metrics") != {
        "packet_coefficients": 63,
        "rational_recurrence_checks": 48,
        "tail_affine_equalities": 16380,
        "words": 4095,
    }:
        raise RuntimeError("affine-series certificate metrics mismatch")
    if (
        stdout_result.get("affine_packet_certificate_metrics", {}).get(
            "total_words_scanned_by_each_method"
        )
        != 4_734_620
    ):
        raise RuntimeError("affine packet scan total mismatch")
    if (
        stdout_result.get("affine_packet_certificate_metrics", {}).get(
            "total_integral_words"
        )
        != 0
    ):
        raise RuntimeError("affine packet finite exclusion mismatch")
    if stdout_result.get("output_pdf", {}).get("sha256") != EXPECTED_PDF_SHA:
        raise RuntimeError("validator output-PDF identity mismatch")
    return receipt


def validate_pdf_identity() -> dict:
    if sha_file(DECLARED_PDF) != EXPECTED_PDF_SHA:
        raise RuntimeError("declared companion PDF hash mismatch")
    if not REVIEWED_PDF.is_file():
        raise RuntimeError("reviewed ACT47 PDF is missing")
    raster_mismatches = []
    text_mismatches = []
    with fitz.open(DECLARED_PDF) as declared, fitz.open(REVIEWED_PDF) as reviewed:
        if len(declared) != 57 or len(reviewed) != 57:
            raise RuntimeError(
                f"unexpected PDF page counts: declared={len(declared)}, reviewed={len(reviewed)}"
            )
        matrix = fitz.Matrix(1.5, 1.5)
        for index in range(57):
            declared_page = declared[index]
            reviewed_page = reviewed[index]
            if declared_page.get_text() != reviewed_page.get_text():
                text_mismatches.append(index + 1)
            declared_pixels = declared_page.get_pixmap(matrix=matrix, alpha=False)
            reviewed_pixels = reviewed_page.get_pixmap(matrix=matrix, alpha=False)
            if (
                declared_pixels.width != reviewed_pixels.width
                or declared_pixels.height != reviewed_pixels.height
                or declared_pixels.samples != reviewed_pixels.samples
            ):
                raster_mismatches.append(index + 1)
    if text_mismatches or raster_mismatches:
        raise RuntimeError(
            f"declared/reviewed PDF mismatch: {text_mismatches=}, {raster_mismatches=}"
        )
    return {
        "declared_pdf": DECLARED_PDF.relative_to(ROOT).as_posix(),
        "declared_pdf_sha256": EXPECTED_PDF_SHA,
        "pages": 57,
        "text_identity_pages": 57,
        "raster_identity_pages": 57,
        "raster_matrix": [1.5, 1.5],
        "directly_reinspected_pages": [1, 51, 52, 53, 54, 57],
        "material_visual_defects": [],
    }


def assert_tao_v7_reader_boundary() -> dict:
    files = [
        ROOT / "preprints/tao_clock_audit/main.tex",
        ROOT / "preprints/tao_clock_audit/bibliography.tex",
        *sorted((ROOT / "preprints/tao_clock_audit/sections").glob("*.tex")),
        STAGE / "tao_preprint.tex",
        *sorted((STAGE / "tao").rglob("*.tex")),
    ]
    pattern = re.compile(r"(?:\bV5\b|Tao5|1909\.03562v5)", re.IGNORECASE)
    hits = []
    for path in files:
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if pattern.search(line):
                hits.append({"path": str(path), "line": number})
    if hits:
        raise RuntimeError(f"reader-facing Tao V5 references found: {hits}")
    return {
        "baseline": "arXiv:1909.03562v7",
        "files_scanned": len(files),
        "reader_facing_v5_hits": 0,
        "historical_version_comparison_location": "local provenance only",
    }


def refresh_canonical_metadata(validation, pdf_check) -> None:
    status_path = STAGE / "PACKAGE_STATUS.json"
    status = read_json(status_path)
    status["local_workbench_unchanged"] = False
    status["certificates_executed_for_sync"] = True
    status["status"] = (
        "Affine analytic delta and portable companion package locally verified; "
        "remote upload to the existing canonical project is pending."
    )
    status["portable_research_companion_validation"] = {
        "status": "PASS",
        "scope": (
            "All 17 manifested portable sources, seven-file TeX closure, six "
            "certificates, two deterministic rebuilds, declared PDF identity, "
            "and 57-page visual equivalence."
        ),
        "watch_receipt": WATCH_RECEIPT.relative_to(ROOT).as_posix(),
        "watch_receipt_sha256": sha_file(WATCH_RECEIPT),
        "validator_stdout": VALIDATOR_STDOUT.relative_to(ROOT).as_posix(),
        "validator_stdout_sha256": EXPECTED_STDOUT_SHA,
        "cap_bytes": validation["cap_bytes"],
        "peak_aggregate_rss_bytes": validation["peak_aggregate_rss_bytes"],
        "peak_aggregate_private_bytes": validation[
            "peak_aggregate_private_bytes"
        ],
        "process_tree_clear": validation["process_tree_clear"],
        "output_pdf": pdf_check,
        "remote_action": False,
    }
    status["affine_analytic_revision"]["status"] = (
        "compiled_visual_and_portable_package_validation_pass_remote_sync_pending"
    )
    status["affine_analytic_revision"]["reproducible_output_pdf"] = {
        "path": pdf_check["declared_pdf"],
        "pages": 57,
        "sha256": EXPECTED_PDF_SHA,
    }
    status["affine_analytic_revision"]["remote_action"] = False
    write_json(status_path, status)
    manifest = {
        "schema_version": 1,
        "hash": "sha256",
        "files": [
            {
                "path": path.relative_to(STAGE).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha_file(path),
            }
            for path in sorted(STAGE.rglob("*"))
            if path.is_file() and path.name != "MANIFEST.json"
        ],
    }
    write_json(STAGE / "MANIFEST.json", manifest)


def main() -> None:
    if QA.exists():
        raise RuntimeError(f"checkpoint already exists: {QA}")
    actions_path = ROOT / "state/action_receipts.jsonl"
    actions = read_jsonl(actions_path)
    if any(row.get("receipt_id") == ACT_ID for row in actions):
        raise RuntimeError(f"action receipt already exists: {ACT_ID}")
    if not ACT47.is_file() or not ACT46_LOCAL.is_file():
        raise RuntimeError("required prior checkpoint evidence is missing")

    portable_manifest = validate_portable_manifest()
    validation = validate_bounded_run()
    pdf_check = validate_pdf_identity()
    tao_boundary = assert_tao_v7_reader_boundary()
    refresh_canonical_metadata(validation, pdf_check)

    prior_remote = read_json(ACT46_LOCAL)["canonical_after"]
    current_stage = inventory(STAGE)
    removed = sorted(set(prior_remote) - set(current_stage))
    if removed:
        raise RuntimeError(f"unexpected canonical removals: {removed}")
    remote_delta = sorted(
        path
        for path, digest in current_stage.items()
        if prior_remote.get(path) != digest
    )
    expected_delta = sorted(
        [
            "MANIFEST.json",
            "PACKAGE_STATUS.json",
            "SOURCE_MAP.json",
            "companion/certificates/affine_packet_series_checks.py",
            "companion/chapters/04_affine_packets_parity_necklaces_and_residue_automata.tex",
            "companion/chapters/05_packet_fixed_point_series.tex",
            "critical/chapters/06_affine_packet_source_audit.tex",
            "research_companion.tex",
        ]
    )
    if remote_delta != expected_delta:
        raise RuntimeError(
            f"canonical remote delta mismatch: expected={expected_delta}, actual={remote_delta}"
        )

    recorded_utc = datetime.now(timezone.utc).isoformat()
    qa_record = {
        "schema_version": 1,
        "checkpoint_id": ACT_ID,
        "status": "PASS_reproducible_research_companion_package",
        "recorded_utc": recorded_utc,
        "scope": (
            "Portable research-companion packaging and reproducibility only; "
            "the wider corpus and raw-Chatnotes audit remain active."
        ),
        "portable_manifest": {
            "path": PORTABLE_MANIFEST.relative_to(ROOT).as_posix(),
            "sha256": sha_file(PORTABLE_MANIFEST),
            "manifested_source_files": len(portable_manifest["files"]),
        },
        "package_sources": {
            "README.md": sha_file(PACKAGE / "README.md"),
            "provenance.json": sha_file(PACKAGE / "provenance.json"),
            "validate_package.py": sha_file(PACKAGE / "validate_package.py"),
            "scripts/run_bounded_companion_validation.py": sha_file(
                ROOT / "scripts/run_bounded_companion_validation.py"
            ),
        },
        "bounded_validation": {
            "watch_receipt": WATCH_RECEIPT.relative_to(ROOT).as_posix(),
            "watch_receipt_sha256": sha_file(WATCH_RECEIPT),
            "validator_stdout": VALIDATOR_STDOUT.relative_to(ROOT).as_posix(),
            "validator_stdout_sha256": EXPECTED_STDOUT_SHA,
            "returncode": validation["returncode"],
            "cap_bytes": validation["cap_bytes"],
            "peak_aggregate_rss_bytes": validation["peak_aggregate_rss_bytes"],
            "peak_aggregate_private_bytes": validation[
                "peak_aggregate_private_bytes"
            ],
            "process_tree_clear": validation["process_tree_clear"],
            "certificate_families": 6,
            "deterministic_rebuilds": 2,
        },
        "pdf_visual_identity": pdf_check,
        "tao_reader_boundary": tao_boundary,
        "canonical_remote_delta_pending": remote_delta,
        "remote_sync_complete": False,
        "whole_raw_affine_coverage_reconciled": False,
        "whole_corpus_complete": False,
        "Lean_launched": False,
        "new_project": False,
        "AGENTS_edits": False,
    }
    write_json(QA, qa_record)
    qa_hash = sha_file(QA)

    overleaf = read_json(ROOT / "state/overleaf_current.json")
    overleaf.update(
        {
            "updated_utc": recorded_utc,
            "status": "affine_analytic_and_companion_package_pass_remote_sync_pending",
            "last_package_checkpoint": {
                "path": QA_REL,
                "sha256": qa_hash,
            },
            "pending_remote_delta": remote_delta,
            "pending_action": (
                "Upload only the listed canonical delta to project "
                "6a91f06e408dd545780c660f and verify main.tex and "
                "research_companion.tex after explicit recompilation; do not "
                "create another project."
            ),
            "tao_unchanged_by_current_sync": True,
        }
    )
    write_json(ROOT / "state/overleaf_current.json", overleaf)

    affine = read_json(ROOT / "state/affine_analytic_current.json")
    affine.update(
        {
            "updated_utc": recorded_utc,
            "status": (
                "local_proofs_visual_QA_and_reproducible_companion_package_pass_"
                "remote_sync_pending"
            ),
            "portable_package_checkpoint": {
                "path": QA_REL,
                "sha256": qa_hash,
            },
            "remote_synced": False,
            "whole_raw_audit_complete": False,
            "full_goal_complete": False,
            "Lean_launched": False,
            "next_action": (
                "Synchronize the exact eight-file canonical delta to the existing "
                "Overleaf project, verify main.tex and research_companion.tex "
                "there, then reconcile the saved affine raw-line audits against "
                "the primary raw text."
            ),
        }
    )
    write_json(ROOT / "state/affine_analytic_current.json", affine)

    coverage = read_json(ROOT / "state/coverage.json")
    coverage["coverage_status"] = (
        "active_affine_analytic_reproducible_package_pass_remote_sync_and_"
        "full_raw_reconciliation_pending"
    )
    coverage["post_ACT48_research_companion_package"] = {
        "path": QA_REL,
        "sha256": qa_hash,
        "portable_source_files": 17,
        "certificate_families": 6,
        "deterministic_rebuilds": 2,
        "pdf_pages": 57,
        "visual_identity_pages": 57,
        "remote_sync_complete": False,
        "full_raw_3021_line_reconciliation": False,
        "whole_corpus_complete": False,
    }
    write_json(ROOT / "state/coverage.json", coverage)

    project = read_json(ROOT / "state/project_state.json")
    project.update(
        {
            "updated_utc": recorded_utc,
            "last_receipt_id": ACT_ID,
            "active_task": (
                "affine_analytic_remote_sync_then_primary_raw_affine_reconciliation"
            ),
            "next_action": (
                "Synchronize the ACT48 eight-file delta to the existing canonical "
                "Overleaf project and verify both affected roots; then reconcile "
                "the two saved affine raw-line audits against the primary raw text."
            ),
            "current_checkpoint": {
                "receipt_id": ACT_ID,
                "path": QA_REL,
                "sha256": qa_hash,
                "scope": qa_record["scope"],
                "global_completion": False,
                "fresh_context_full_recovery_pass_claimed": False,
                "remote_sync_complete": False,
            },
        }
    )
    write_json(ROOT / "state/project_state.json", project)

    programmes_path = ROOT / "state/programmes.jsonl"
    programmes = read_jsonl(programmes_path)
    matches = [row for row in programmes if row.get("programme_id") == "PRG-COL-0001"]
    if len(matches) != 1:
        raise RuntimeError("programme record mismatch")
    matches[0]["analytic_reconstruction"].update(
        {
            "status": (
                "proved_reviewed_certificate_build_visual_and_portable_package_"
                "validation_pass_remote_sync_pending"
            ),
            "portable_package_checkpoint": QA_REL,
            "portable_package_checkpoint_sha256": qa_hash,
        }
    )
    write_jsonl(programmes_path, programmes)

    action = {
        "record_type": "action_receipt",
        "schema_version": "1.0",
        "receipt_id": ACT_ID,
        "timestamp_utc": recorded_utc,
        "action": (
            "research_companion_portable_manifest_six_certificate_"
            "deterministic_build_and_page_identity_validation"
        ),
        "inputs": [
            "qa/ACT47-AFFINE-ANALYTIC-CHECKPOINT.json",
            "research_companion/MANIFEST.json",
            "research_companion/validate_package.py",
        ],
        "outputs": [
            QA_REL,
            WATCH_RECEIPT.relative_to(ROOT).as_posix(),
            VALIDATOR_STDOUT.relative_to(ROOT).as_posix(),
            "state/affine_analytic_current.json",
            "state/overleaf_current.json",
        ],
        "result": (
            "reproducible_portable_companion_package_pass_remote_sync_pending"
        ),
        "checkpoint": {"path": QA_REL, "sha256": qa_hash},
        "output_pdf": {
            "path": DECLARED_PDF.relative_to(ROOT).as_posix(),
            "sha256": EXPECTED_PDF_SHA,
            "pages": 57,
        },
        "remote_sync_complete": False,
        "whole_raw_affine_coverage_reconciled": False,
        "goal_complete": False,
        "new_project": False,
        "Lean_started": False,
        "AGENTS_edits": False,
        "tao_reader_baseline": "V7_only",
    }
    actions.append(action)
    write_jsonl(actions_path, actions)

    print(
        json.dumps(
            {
                "status": "PASS",
                "checkpoint": QA_REL,
                "checkpoint_sha256": qa_hash,
                "portable_pdf_sha256": EXPECTED_PDF_SHA,
                "remote_delta": remote_delta,
                "tao_reader_facing_v5_hits": 0,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
