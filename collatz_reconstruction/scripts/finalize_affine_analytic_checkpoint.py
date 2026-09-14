"""Seal the checked affine-analytic checkpoint without remote mutation.

This script is intentionally specific to the 2026-09-04 build.  It verifies
the certificate, watched TeX runs, rendered-page hashes, and canonical staging
delta before updating the durable ledgers.  It performs no browser, Git, Lean,
archive, or publication action.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN_ROOT = ROOT / "overleaf/sync_20260904/audit/affine_analytic"
INSPECTED_RUN = RUN_ROOT / "run_20260904T165754Z"
FINAL_RUN = RUN_ROOT / "run_20260904T170410Z"
RECEIPT = FINAL_RUN / "local_receipt.json"
STAGE = ROOT / "overleaf/sync_20260904/canonical_project"
QA_REL = "qa/ACT47-AFFINE-ANALYTIC-CHECKPOINT.json"
QA = ROOT / QA_REL
RECEIPT_REL = RECEIPT.relative_to(ROOT).as_posix()
ACT_ID = "ACT-COL-000047"
CLAIM_IDS = {f"CLM-COL-{n:06d}" for n in range(196, 200)}
MORPHISM_ID = "MOR-COL-000071"


def sha_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_jsonl(path: Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows) -> None:
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in rows) + "\n", encoding="utf-8")


def inventory(root: Path):
    return {
        p.relative_to(root).as_posix(): sha_file(p)
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }


def render_hashes(run: Path, case: str):
    folder = run / case / "renders"
    return {p.name: sha_file(p) for p in sorted(folder.glob("page-*.png"))}


def build_by_name(receipt, name: str):
    matches = [row for row in receipt["builds"] if row["name"] == name]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one build {name}, found {len(matches)}")
    return matches[0]


def live_tao_tex_files():
    base = ROOT / "preprints/tao_clock_audit"
    return [base / "main.tex", base / "bibliography.tex", *sorted((base / "sections").glob("*.tex"))]


def canonical_tao_tex_files():
    return [STAGE / "tao_preprint.tex", *sorted((STAGE / "tao").rglob("*.tex"))]


def assert_v7_only_reader_sources():
    pattern = re.compile(r"(?:\bV5\b|Tao5|1909\.03562v5)", re.IGNORECASE)
    hits = []
    files = live_tao_tex_files() + canonical_tao_tex_files()
    for path in files:
        text = path.read_text(encoding="utf-8")
        for number, line in enumerate(text.splitlines(), 1):
            if pattern.search(line):
                hits.append({"path": str(path), "line": number, "text": line})
    if hits:
        raise RuntimeError(f"Reader-facing Tao V5 hits: {hits}")
    return {
        "baseline": "arXiv:1909.03562v7",
        "live_and_canonical_tex_files_scanned": len(files),
        "reader_facing_v5_hits": 0,
        "historical_v5_material": "retained only in local provenance audits",
    }


def validate_and_annotate_receipt():
    receipt = read_json(RECEIPT)
    if receipt.get("status") != "compiled_visual_review_pending":
        raise RuntimeError(f"Unexpected receipt status: {receipt.get('status')}")
    if receipt.get("certificate_result", {}).get("status") != "PASS":
        raise RuntimeError("Affine analytic certificate did not report PASS")
    if receipt["certificate_result"].get("Lean_launched") is not False:
        raise RuntimeError("Unexpected Lean launch in certificate result")

    expected_cases = {"live_companion", "live_critical", "canonical_companion", "canonical_critical"}
    if {row["name"] for row in receipt["builds"]} != expected_cases:
        raise RuntimeError("Build case set mismatch")

    for build in receipt["builds"]:
        pdf = Path(build["pdf"])
        if not pdf.is_file() or sha_file(pdf) != build["pdf_sha256"]:
            raise RuntimeError(f"PDF identity mismatch: {pdf}")
        if build.get("undefined_reference_errors"):
            raise RuntimeError(f"Unresolved TeX diagnostic: {build['name']}")
        if any("Overfull" in warning for warning in build.get("warnings", [])):
            raise RuntimeError(f"Overfull box in {build['name']}")
        if len(build.get("passes", [])) != 3:
            raise RuntimeError(f"Expected three passes in {build['name']}")
        for run in build["passes"]:
            if run["returncode"] != 0 or run["termination_reason"] is not None or not run["process_tree_clear"]:
                raise RuntimeError(f"Watched pass failed: {build['name']}")
            if run["cap_bytes"] != 5_000_000_000:
                raise RuntimeError(f"Wrong process-tree cap: {build['name']}")

    # The final bookmark-only repair changed no rendered page.  Every final PNG
    # must exactly match the run directly inspected by root.
    final_rasters = {}
    for case in sorted(expected_cases):
        old = render_hashes(INSPECTED_RUN, case)
        new = render_hashes(FINAL_RUN, case)
        if old != new:
            differing = sorted(set(old) | set(new))
            differing = [name for name in differing if old.get(name) != new.get(name)]
            raise RuntimeError(f"Final raster changed after inspection in {case}: {differing}")
        final_rasters[case] = {"rendered_pages": len(new), "all_equal_to_directly_inspected_run": True}

    companion_live = render_hashes(FINAL_RUN, "live_companion")
    companion_stage = render_hashes(FINAL_RUN, "canonical_companion")
    critical_live = render_hashes(FINAL_RUN, "live_critical")
    critical_stage = render_hashes(FINAL_RUN, "canonical_critical")
    companion_different = sorted(int(name[5:8]) for name in companion_live if companion_live[name] != companion_stage[name])
    critical_different = sorted(int(name[5:8]) for name in critical_live if critical_live[name] != critical_stage[name])
    if companion_different != [15, 23, 33, 50, 51]:
        raise RuntimeError(f"Unexpected companion remap pages: {companion_different}")
    if critical_different != [7, 167, *range(173, 185)]:
        raise RuntimeError(f"Unexpected critical remap pages: {critical_different}")

    visual = {
        "status": "PASS",
        "reviewer": "/root",
        "directly_inspected_run": INSPECTED_RUN.relative_to(ROOT).as_posix(),
        "final_run": FINAL_RUN.relative_to(ROOT).as_posix(),
        "final_raster_identity_to_inspected_run": final_rasters,
        "live_companion": {
            "pages": 57,
            "inspected_pages": list(range(1, 58)),
            "original_detail_pages": [1, 51, 52, 53, 54],
        },
        "live_critical": {
            "pages": 184,
            "inspected_pages": [*range(1, 8), *range(167, 185)],
            "original_detail_pages": [168, 169, 170, 171, 172, 173],
        },
        "canonical_companion": {
            "pages": 57,
            "live_raster_different_pages": companion_different,
            "all_different_pages_directly_inspected": True,
            "other_pages_exactly_raster_identical_to_inspected_live_pages": True,
        },
        "canonical_critical": {
            "pages": 184,
            "rendered_and_inspected_pages": [*range(1, 8), *range(167, 185)],
            "live_raster_different_pages": critical_different,
            "all_different_pages_directly_inspected": True,
        },
        "material_visual_defects": [],
        "checks": [
            "no clipping",
            "no overlap",
            "no broken glyphs",
            "no black boxes",
            "page numbers and section transitions intact",
            "canonical path remapping legible",
        ],
    }
    for build in receipt["builds"]:
        build["visual_review"] = visual[build["name"]]
    receipt["visual_review"] = visual
    receipt["status"] = "compiled_visual_review_pass"
    return receipt


def update_package_status(receipt):
    status_path = STAGE / "PACKAGE_STATUS.json"
    status = read_json(status_path)
    builds = {row["name"]: {"pages": row["pages"], "pdf_sha256": row["pdf_sha256"]} for row in receipt["builds"]}
    status["affine_analytic_revision"] = {
        "status": "compiled_visual_review_pass_remote_sync_pending",
        "scope": "Periodic-tail repair, packet offset family, exact formal dilation inverse, Taylor domains, and meromorphic continuation with complete finite-pole data.",
        "scope_caveat": receipt["scope_caveat"],
        "certificate_status": "PASS finite exact algebra; general analytic proof is in companion chapter 5 and independently reviewed",
        "local_build_receipt": RECEIPT_REL,
        "builds": builds,
        "visual_review": receipt["visual_review"],
        "tao_sources_unchanged": True,
        "new_archive": False,
        "remote_action": False,
    }
    write_json(status_path, status)
    manifest = {
        "schema_version": 1,
        "hash": "sha256",
        "files": [
            {"path": p.relative_to(STAGE).as_posix(), "bytes": p.stat().st_size, "sha256": sha_file(p)}
            for p in sorted(STAGE.rglob("*"))
            if p.is_file() and p.name != "MANIFEST.json"
        ],
    }
    write_json(STAGE / "MANIFEST.json", manifest)


def update_claim_and_morphism_ledgers(receipt_hash: str, certificate_info):
    execution = {
        "status": "PASS_watched_finite_exact_algebra",
        "local_build_receipt": RECEIPT_REL,
        "local_build_receipt_sha256": receipt_hash,
        "certificate_stdout_sha256": certificate_info["stdout_sha256"],
        "cap_bytes": 5_000_000_000,
        "Lean_launched": False,
        "metrics": certificate_info["metrics"],
    }
    claims_path = ROOT / "state/claims.jsonl"
    claims = read_jsonl(claims_path)
    found = set()
    for row in claims:
        if row.get("claim_id") in CLAIM_IDS:
            row["formal_status"]["certificate_execution"] = execution
            row["formal_status"]["certificate_sha256"] = sha_file(ROOT / "research_companion/certificates/affine_packet_series_checks.py")
            found.add(row["claim_id"])
    if found != CLAIM_IDS:
        raise RuntimeError(f"Claim ledger mismatch: {found}")
    write_jsonl(claims_path, claims)

    morphisms_path = ROOT / "state/morphisms.jsonl"
    morphisms = read_jsonl(morphisms_path)
    found_morphism = False
    for row in morphisms:
        if row.get("morphism_id") == MORPHISM_ID:
            row["formal_status"]["certificate_execution"] = execution
            row["formal_status"]["certificate_sha256"] = sha_file(ROOT / "research_companion/certificates/affine_packet_series_checks.py")
            found_morphism = True
    if not found_morphism:
        raise RuntimeError("Morphism record missing")
    write_jsonl(morphisms_path, morphisms)


def update_programme(receipt_hash: str, qa_hash: str):
    path = ROOT / "state/programmes.jsonl"
    rows = read_jsonl(path)
    matches = [row for row in rows if row.get("programme_id") == "PRG-COL-0001"]
    if len(matches) != 1:
        raise RuntimeError("Programme record mismatch")
    matches[0]["analytic_reconstruction"].update({
        "status": "proved_independently_reviewed_certificate_pass_four_serial_builds_and_visual_QA_pass_remote_sync_pending",
        "local_build_receipt": RECEIPT_REL,
        "local_build_receipt_sha256": receipt_hash,
        "checkpoint": QA_REL,
        "checkpoint_sha256": qa_hash,
    })
    write_jsonl(path, rows)


def main():
    if QA.exists():
        raise RuntimeError(f"Checkpoint already exists: {QA}")
    if any(row.get("receipt_id") == ACT_ID for row in read_jsonl(ROOT / "state/action_receipts.jsonl")):
        raise RuntimeError(f"Action receipt already exists: {ACT_ID}")

    v7_boundary = assert_v7_only_reader_sources()
    receipt = validate_and_annotate_receipt()
    update_package_status(receipt)
    receipt["canonical_after_visual_finalization"] = inventory(STAGE)
    write_json(RECEIPT, receipt)
    receipt_hash = sha_file(RECEIPT)

    prior_remote = read_json(ROOT / "overleaf/sync_20260904/audit/affine_crt/run_20260904T152745Z/local_receipt.json")["canonical_after"]
    current_stage = inventory(STAGE)
    remote_delta = sorted(path for path, digest in current_stage.items() if prior_remote.get(path) != digest)
    removed_remote = sorted(set(prior_remote) - set(current_stage))
    if removed_remote:
        raise RuntimeError(f"Unexpected canonical removals: {removed_remote}")

    certificate_info = {
        "path": "research_companion/certificates/affine_packet_series_checks.py",
        "sha256": sha_file(ROOT / "research_companion/certificates/affine_packet_series_checks.py"),
        "stdout_sha256": receipt["certificate_stdout_sha256"],
        "watcher": receipt["certificate_watcher"],
        "metrics": receipt["certificate_result"],
    }
    qa_record = {
        "schema_version": 1,
        "checkpoint_id": ACT_ID,
        "status": "PASS_bounded_affine_analytic_local_checkpoint",
        "recorded_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "Periodic-tail repair and packet fixed-point analytic family only; this is not full raw-Chatnotes or whole-corpus completion.",
        "source_hashes": receipt["source_hashes"],
        "proof_review": {
            "path": "research_companion/audit/affine_mahler_analytic_reconstruction_20260904.md",
            "sha256": sha_file(ROOT / "research_companion/audit/affine_mahler_analytic_reconstruction_20260904.md"),
        },
        "source_witness_review": {
            "path": "research_companion/audit/affine_tail_mahler_witness_collation_20260904.json",
            "sha256": sha_file(ROOT / "research_companion/audit/affine_tail_mahler_witness_collation_20260904.json"),
        },
        "certificate": certificate_info,
        "claims": sorted(CLAIM_IDS),
        "morphism": MORPHISM_ID,
        "local_build_receipt": {"path": RECEIPT_REL, "sha256": receipt_hash},
        "builds": {row["name"]: {"pages": row["pages"], "pdf_sha256": row["pdf_sha256"]} for row in receipt["builds"]},
        "visual_review": receipt["visual_review"],
        "tao_reader_boundary": v7_boundary,
        "canonical_remote_delta_pending": remote_delta,
        "remote_sync_complete": False,
        "Lean_launched": False,
        "whole_raw_affine_coverage_reconciled": False,
        "whole_corpus_complete": False,
    }
    write_json(QA, qa_record)
    qa_hash = sha_file(QA)

    update_claim_and_morphism_ledgers(receipt_hash, certificate_info)
    update_programme(receipt_hash, qa_hash)

    current = read_json(ROOT / "state/affine_analytic_current.json")
    current.update({
        "updated_utc": qa_record["recorded_utc"],
        "status": "local_proofs_review_certificate_build_and_visual_QA_pass_remote_sync_pending",
        "claims": sorted(CLAIM_IDS),
        "morphism": MORPHISM_ID,
        "certificate": certificate_info,
        "local_build_receipt": {"path": RECEIPT_REL, "sha256": receipt_hash},
        "checkpoint": {"path": QA_REL, "sha256": qa_hash},
        "remote_synced": False,
        "whole_raw_audit_complete": False,
        "full_goal_complete": False,
        "Lean_launched": False,
        "next_action": "Synchronize the exact canonical delta to the existing Overleaf project, verify both affected roots there, then continue direct raw affine content reading beyond the recorded 1-900 audit without inferring coverage from summaries.",
    })
    write_json(ROOT / "state/affine_analytic_current.json", current)

    overleaf = read_json(ROOT / "state/overleaf_current.json")
    overleaf.update({
        "updated_utc": qa_record["recorded_utc"],
        "status": "affine_analytic_delta_staged_and_locally_verified_remote_sync_pending",
        "last_local_receipt": RECEIPT_REL,
        "pending_remote_delta": remote_delta,
        "pending_action": "Upload only the listed canonical delta to project 6a91f06e408dd545780c660f and verify main.tex and research_companion.tex after explicit recompilation; do not create a project.",
        "tao_unchanged_by_current_sync": True,
    })
    write_json(ROOT / "state/overleaf_current.json", overleaf)

    tao = read_json(ROOT / "state/tao_preprint_current.json")
    tao.update({
        "updated_utc": qa_record["recorded_utc"],
        "reader_facing_version_boundary": v7_boundary,
        "next_action": "Retain the preprint as a V7-based first-entry-law draft; historical V5 evidence remains outside its reader-facing TeX.",
    })
    write_json(ROOT / "state/tao_preprint_current.json", tao)

    coverage = read_json(ROOT / "state/coverage.json")
    coverage["coverage_status"] = "active_affine_analytic_local_checkpoint_pass_remote_sync_and_full_raw_reconciliation_pending"
    coverage["post_ACT47_affine_analytic_checkpoint"] = {
        "path": QA_REL,
        "sha256": qa_hash,
        "claims": sorted(CLAIM_IDS),
        "morphism": MORPHISM_ID,
        "working_pdf_pages": 184,
        "research_companion_pdf_pages": 57,
        "certificate_status": "PASS",
        "visual_QA_status": "PASS",
        "remote_sync_complete": False,
        "full_raw_3021_line_reconciliation": False,
        "whole_corpus_complete": False,
    }
    write_json(ROOT / "state/coverage.json", coverage)

    project = read_json(ROOT / "state/project_state.json")
    project.update({
        "updated_utc": qa_record["recorded_utc"],
        "active_task": "affine_analytic_remote_sync_then_direct_raw_affine_reconciliation",
        "next_action": "Synchronize the ACT47 canonical delta to the existing Overleaf project and verify both affected roots; then continue direct content-level audit of raw affine lines beyond the saved 1-900 record.",
        "current_checkpoint": {
            "receipt_id": ACT_ID,
            "path": QA_REL,
            "sha256": qa_hash,
            "scope": qa_record["scope"],
            "global_completion": False,
            "fresh_context_full_recovery_pass_claimed": False,
            "remote_sync_complete": False,
        },
    })
    write_json(ROOT / "state/project_state.json", project)

    action = {
        "record_type": "action_receipt",
        "schema_version": "1.0",
        "receipt_id": ACT_ID,
        "timestamp_utc": qa_record["recorded_utc"],
        "action": "affine_periodic_tail_repair_packet_fixed_point_dilation_series_exact_domains_meromorphic_continuation_and_local_package_QA",
        "inputs": ["raw/USR-0017-tao-v7-baseline.txt", "state/affine_analytic_topic_route.json", "CHATINT-COL-000002"],
        "outputs": [QA_REL, RECEIPT_REL, "state/affine_analytic_current.json", "state/overleaf_current.json", "research_companion/chapters/05_packet_fixed_point_series.tex"],
        "result": "bounded_local_proof_review_certificate_build_and_visual_QA_pass_remote_sync_pending",
        "claims": sorted(CLAIM_IDS),
        "morphisms": [MORPHISM_ID],
        "certificate": certificate_info,
        "build_receipt": {"path": RECEIPT_REL, "sha256": receipt_hash},
        "checkpoint": {"path": QA_REL, "sha256": qa_hash},
        "tao_reader_baseline": "V7_only",
        "remote_sync_complete": False,
        "whole_raw_affine_coverage_reconciled": False,
        "goal_complete": False,
        "new_project": False,
        "Lean_started": False,
        "AGENTS_edits": False,
    }
    actions_path = ROOT / "state/action_receipts.jsonl"
    actions = read_jsonl(actions_path)
    actions.append(action)
    write_jsonl(actions_path, actions)

    print(json.dumps({
        "status": "PASS",
        "checkpoint": QA_REL,
        "checkpoint_sha256": qa_hash,
        "receipt": RECEIPT_REL,
        "receipt_sha256": receipt_hash,
        "remote_delta": remote_delta,
        "tao_reader_facing_v5_hits": 0,
    }))


if __name__ == "__main__":
    main()
