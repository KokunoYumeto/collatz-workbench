#!/usr/bin/env python3
"""Fail-closed, idempotent ACT33 checkpoint seal.

This script admits no new source, claim, morphism, or proof-obligation row.
It verifies the already admitted F028--F030 state and artifacts, advances only
coverage/project checkpoint pointers, and appends ACT-COL-000033 atomically.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state"
BUILD = ROOT / "tmp" / "act33_f030_build_root"
RENDER = ROOT / "tmp" / "act33_f030_full_visual_root_200dpi"
CONTACTS = RENDER / "contact_sheets_4x4"
STAMP = "2026-08-28T16:09:58.2199617Z"
CHECKPOINT = "qa/RECOVERY-CHECKPOINT-20260828-ACT33.md"
RECOVERY_REPORT = "qa/ACT33-FRESH-CONTEXT-RECOVERY-TEST.md"
RECEIPT_ID = "ACT-COL-000033"


EXPECTED_LOCAL: dict[str, tuple[int, str]] = {
    "raw/USR-0001.txt": (5_156, "8ab3bd5f53338cc9fcb3494018763d29c89f67aa0623d26b1c39ee09f69cd442"),
    "raw/USR-0002.txt": (379, "4d09eabbaf85ef4351493c89afd9ffabc1d630283a92d1d6927f632158088729"),
    "raw/USR-0003.txt": (324, "675bc42a44356f579f63f6abd816b9c2cf36701f0d017ffd467eca033d5c7925"),
    "state/index_routes.jsonl": (274_170, "b05028694bf133b9b19f2b0c0a771323b7a47ae872c0712769267aaf1f1eff38"),
    "state/document_routes.jsonl": (324_776, "e439a5f9a70253b00824df5be791415e1c068d574c23f6f7f61851c19a88b2a5"),
    "state/index_snapshot.json": (799, "7d5a17440a3cb039f2bfbb4814567b5805117002136cc65687de738ee99af62f"),
    "state/source_registry.jsonl": (138_480, "4173625b117fb4d6aa234c9c58713260ab6de8ed4dc1d9f5e271e1e4875c2a56"),
    "state/claims.jsonl": (162_937, "c050c4d724bf07b89f10807ca945d196160edf6891017bac58accb69d9897536"),
    "state/morphisms.jsonl": (56_231, "3e4dfe7f45b27ab4190c210d9cc385178530a9729d494ecf8b4dbb9351de96e7"),
    "state/proof_obligations.jsonl": (50_862, "e807afdbf4a3f78df0c93c903a0ab6178da03b3d69aeaa6b28c99f96a83e1383"),
    "TODO.md": (21_888, "22b507464a0acbd88bace574310cba6302d793fa6546bec17ea6e32e893f5718"),
    "qa/ACT33-WORKLOG-TAO-POST1860.md": (18_524, "6542da621823c301ec9fd1851e82f7febb72611b9b75e3412fc924e374ae454e"),
    CHECKPOINT: (24_909, "613a1c5b6c2f5487c171e6b0e7e3688929062cc798d616bc34604fcb9fe87b41"),
    RECOVERY_REPORT: (6_097, "80f7553721f23088b097fa040393a6c8d85f2023a9c37a525f0618176707d63c"),
    "qa/R7R11CRTForcing-RESOURCE-SNAPSHOT-20260828T155746Z.json": (3_790, "6b02d63cff539499856ced4cde800e24ad43fef15ed14c6fa615b8686b32c49a"),
    "qa/TAO-V5-V7-JOURNAL-F028-whole-version-citation-audit.md": (17_255, "bf00a90d3acd819435a7ef2da0ebeae032d752b8c921c1f97ff23ddff2a0b095"),
    "qa/KRASIKOV-LAGARIAS-2003-F029-difference-inequality-audit.md": (18_261, "7bc00b095f99f55ae94f226a5b865223ecc2de030501536e1d26d2f71f01d187"),
    "qa/TERRAS-ALLOUCHE-KOREC-F030-density-lineage-audit.md": (28_949, "3765a2ef9a98ed101ad387f64e9f707fe714e0a64c8479ea012bc1ef846ec6ba"),
    "certificates/tao_whole_version_checks.py": (12_614, "c13f10f397c3abcd562a99702705b6e6a6d76731b78d2fe0aeb0a0a36f54d26f"),
    "certificates/krasikov_lagarias_2003_checks.py": (9_441, "3f4ccc7256f026fa65ce7660b47823969c6c605e2a4c45da5b4b6d48961315fa"),
    "certificates/terras_allouche_korec_checks.py": (23_451, "0c098c6a70073b5b8ddd4e460c35491c28db5363c910c9127c6644b513ec25aa"),
    "tex/main.tex": (2_275, "dad1321989bcb94c63d53329c69b0cd6ae4ba7980b970ce10b05d53e54d03c95"),
    "tex/chapters/01_literature_spine.tex": (110_569, "22bd06bf82d30debea6842d4249078e4dad5c468d2d5491d8bc20da1777bafc9"),
    "tex/chapters/99_source_register.tex": (25_289, "46d189221cf0d20bd1c60d52c0c1ef5badd1cd8b652e697e59b7b44943034fa2"),
    "tmp/act33_f030_build_root/main.pdf": (1_261_638, "509b415815623cd7a0c661a3cd01a66282edd339eb07888d184b9acf2ff17f72"),
    "tmp/act33_f030_build_root/main.log": (33_040, "4cbd48150e55307e693f6b77b632f117528e0026d6b49e29940890a861447f66"),
    "tmp/act33_f030_build_root/main-layout.txt": (443_606, "a05d2ade5023d39d25702886b94828a4ba6648cb800acffb651e4dbd9588b8b0"),
    "tmp/act33_f030_build_root/pdfinfo.txt": (808, "6a75f531b81581e9a32ccad5ef0eb3f86288c732436d1590c9e9ffee5ad9e042"),
    "tmp/act33_f030_build_root/pdffonts.txt": (2_660, "372d4689722d2920cb4cc9cee065bf0244c970dbba804e14920d232e52eba74d"),
    "tmp/act33_f030_full_visual_root_200dpi/contact_sheets_4x4/contact-113-124-4x3.png": (1_481_117, "4646899e6d990d10efc7c8ce9bcc1d09d96e6d1a6a25833d30ed81f9fc70ad06"),
    "tmp/act33_f030_full_visual_root_200dpi/contact_sheets_4x4/contact-113-124-4x3-view.jpg": (557_848, "c2afba6b809441c7060c9078064752adb4bca0b8c9066c692f6bdbc89d2daacc"),
}

EXPECTED_PRE_STATE: dict[str, tuple[int, str]] = {
    "state/coverage.json": (7_417, "efb0f05f74e7e224f815ed1591d02638909a76a6ea1161e89b33922fe40dca73"),
    "state/project_state.json": (11_072, "a50f534e413e86642748871e10a5c15f90a4dd1d4ce6c8d03bbb930092d4bf67"),
    "state/action_receipts.jsonl": (165_837, "9913e08c329f0b942791d0dea4b078a53a034633dafe411ac7c22c3641697b2a"),
}

EXPECTED_EXTERNAL: dict[str, tuple[int, str]] = {
    "C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/latex/1909.03562v7/collatz.tex": (164_932, "bfbc39432d4084a276416cb019a592003c868fa32f18e2f90028ac325ae5c19d"),
    "C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/latex/1909.03562v5/collatz.tex": (163_356, "c676b362b30807aa6690d0d4f16b8c8e84324732f5c0eb72ccfd875000276ae0"),
    "C:/Users/LOCAL_USER/Documents/arxiv_latex/library/_recovered_from_papers/by_title/Tao Almost all orbits of the Collatz map attain almost bounded values.pdf": (1_008_484, "55c817c73498f940ed1e70f10208105922f1f7c89e378dcb629040c534151a2b"),
    "C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/published/Krasikov-Lagarias-2003-Bounds-difference-inequalities.pdf": (217_588, "8433f68c6f04a008b7c1af4d2b11ee1007a74f987da56a658d8fa331b32eff9c"),
    "C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/source/math.0205002v1.eprint": (26_236, "c35de018067ae838c17b647f0ce0354141a8bcfaa45b4966be2bb9a380252951"),
    "C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/latex/math.0205002v1/30apr02.tex": (69_729, "04fa4d484fe89256f6771f5651338891219385f6e049ffaf41035541016232cd"),
    "C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/published/Terras-1976-A-stopping-time-problem.pdf": (646_395, "2b9c296a05541c5b52f63482a09982519546eba36f581bddd853af6ca014bf89"),
    "C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/published/Terras-1979-On-the-existence-of-a-density.pdf": (134_556, "6cb5efbda449752cc0e815f630680f4153aa3ee62a548307041f7968b5d0e47b"),
    "C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/published/Allouche-1979-Syracuse-Kakutani-Collatz.pdf": (1_160_082, "96f959368e5417dcc6d432e4831f3cf957e7b0db687b916a6aed0262102a01b6"),
    "C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/published/Korec-1994-A-density-estimate.pdf": (383_521, "3111bcc638a563fa4395d8a090a4b563116f1ffe30aee136f6e24a76d4d97c77"),
}

EXPECTED_HEADERS = {
    "source_registry.jsonl": "SRC-COL-000033",
    "claims.jsonl": "CLM-COL-000137",
    "morphisms.jsonl": "MOR-COL-000033",
    "proof_obligations.jsonl": "PO-COL-000009",
}

EXPECTED_COUNTS = {
    "source_registry.jsonl": ("source_document", 32),
    "claims.jsonl": ("claim", 136),
    "morphisms.jsonl": ("morphism", 32),
    "proof_obligations.jsonl": ("proof_obligation", 8),
}

REQUIRED_F030_LABELS = [
    "prop:Terras-parity-coordinate",
    "thm:Terras-1976-coefficient-tail",
    "thm:Terras-1979-density-identity",
    "cor:Terras-density-one-stopping",
    "thm:Allouche-affine-counting",
    "thm:Allouche-slope-obstruction",
    "prop:Allouche-threshold-extraction",
    "thm:Korec-density-estimate",
    "sourceissue:Tao-line165-threshold",
    "prop:Tao-Korec-threshold-crosswalk",
]


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def record(path: Path, label: str | None = None) -> dict[str, Any]:
    return {
        "path": label if label is not None else path.as_posix(),
        "bytes": path.stat().st_size,
        "sha256": digest(path),
    }


def assert_pin(path: Path, expected: tuple[int, str]) -> None:
    size, sha = expected
    assert path.is_file(), path
    assert path.stat().st_size == size, (path, size, path.stat().st_size)
    actual = digest(path)
    assert actual == sha, (path, sha, actual)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    ]


def json_bytes(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def append_unique(rows: list[dict[str, Any]], value: dict[str, Any]) -> None:
    if value not in rows:
        rows.append(value)


def verify_static_artifacts() -> None:
    for relative, expected in EXPECTED_LOCAL.items():
        assert_pin(ROOT / relative, expected)
    for absolute, expected in EXPECTED_EXTERNAL.items():
        assert_pin(Path(absolute), expected)

    rendered = sorted(RENDER.glob("page-*.png"))
    assert len(rendered) == 124
    assert sum(path.stat().st_size for path in rendered) == 52_989_982

    canonical_names = [
        "contact-001-016.png",
        "contact-017-032.png",
        "contact-033-048.png",
        "contact-049-064.png",
        "contact-065-080.png",
        "contact-081-096.png",
        "contact-097-112.png",
        "contact-113-124.png",
    ]
    canonical = [CONTACTS / name for name in canonical_names]
    assert all(path.is_file() for path in canonical)
    assert sum(path.stat().st_size for path in canonical) == 13_253_297

    log_text = (BUILD / "main.log").read_text(encoding="utf-8", errors="replace")
    assert len(re.findall(r"^Underfull \\hbox", log_text, flags=re.MULTILINE)) == 6
    assert "Overfull \\hbox" not in log_text
    assert "There were undefined references" not in log_text
    assert "Citation `" not in log_text
    assert "multiply defined" not in log_text
    assert "Rerun to get cross-references right" not in log_text

    font_lines = (BUILD / "pdffonts.txt").read_text(encoding="utf-8").splitlines()[2:]
    font_lines = [line for line in font_lines if line.strip()]
    assert len(font_lines) == 26
    assert all(re.search(r"\byes\s+yes\s+yes\s+\d+\s+\d+\s*$", line) for line in font_lines)
    assert re.search(r"^Pages:\s+124\s*$", (BUILD / "pdfinfo.txt").read_text(encoding="utf-8"), re.MULTILINE)

    spine = (ROOT / "tex/chapters/01_literature_spine.tex").read_text(encoding="utf-8")
    for label in REQUIRED_F030_LABELS:
        assert spine.count("\\label{" + label + "}") == 1, label


def verify_ledgers() -> dict[str, list[dict[str, Any]]]:
    ledgers: dict[str, list[dict[str, Any]]] = {}
    for filename, (record_type, expected_count) in EXPECTED_COUNTS.items():
        rows = load_jsonl(STATE / filename)
        ledgers[filename] = rows
        assert rows[0]["record_type"] == "ledger_header"
        assert rows[0]["next_id"] == EXPECTED_HEADERS[filename]
        records = [row for row in rows if row.get("record_type") == record_type]
        assert len(records) == expected_count, (filename, len(records), expected_count)

    obligations = ledgers["proof_obligations.jsonl"][1:]
    assert [row["obligation_id"] for row in obligations] == [
        f"PO-COL-{index:06d}" for index in range(1, 9)
    ]
    assert all(
        not row["status"].lower().startswith(("closed", "complete", "withdrawn"))
        for row in obligations
    )

    source_ids = {row.get("source_id") for row in ledgers["source_registry.jsonl"]}
    claim_ids = {row.get("claim_id") for row in ledgers["claims.jsonl"]}
    morphism_rows = ledgers["morphisms.jsonl"]
    assert {f"SRC-COL-{index:06d}" for index in range(28, 33)} <= source_ids
    assert {f"CLM-COL-{index:06d}" for index in range(123, 137)} <= claim_ids
    mor32 = next(row for row in morphism_rows if row.get("morphism_id") == "MOR-COL-000032")
    assert mor32["claim_refs"] == ["CLM-COL-000124", "CLM-COL-000126", "CLM-COL-000136"]
    for claim_number in range(127, 136):
        claim = next(row for row in ledgers["claims.jsonl"] if row.get("claim_id") == f"CLM-COL-{claim_number:06d}")
        text = json.dumps(claim, ensure_ascii=False)
        assert "MOR-COL-000001" not in text and "MOR-COL-000032" not in text
    clm136 = next(row for row in ledgers["claims.jsonl"] if row.get("claim_id") == "CLM-COL-000136")
    clm136_text = json.dumps(clm136, ensure_ascii=False)
    assert "MOR-COL-000001" in clm136_text and "MOR-COL-000032" in clm136_text
    return ledgers


def update_state(coverage: dict[str, Any], project: dict[str, Any]) -> None:
    layers = {layer["layer_id"]: layer for layer in coverage["layers"]}
    lit = layers["LIT"]
    assert lit["documents_read"] == 32 and lit["documents_admitted"] == 32
    formal = layers["FORMAL"]
    assert formal["artifacts_verified"] == 19

    syn = layers["SYN"]
    syn.update({
        "status": "ACT33_124_page_checkpoint_PDF_F028_whole_version_F029_Krasikov_Lagarias_and_F030_Terras_Allouche_Korec_density_lineage_propagated_zero_actionable_diagnostics_all_fonts_embedded_subset_fresh_all_page_QA_pass_not_release_QA",
        "working_pdf_pages": 124,
        "working_pdf_bytes": 1_261_638,
        "working_pdf_sha256": "509B415815623CD7A0C661A3CD01A66282EDD339EB07888D184B9ACF2FF17F72",
        "root_rendered_page_count": 124,
        "root_render_dpi": 200,
        "root_render_bytes": 52_989_982,
        "root_contact_sheet_count": 8,
        "root_contact_sheet_bytes": 13_253_297,
        "current_pages_visually_checked": 124,
        "root_all_pages_contact_sheet_checked": 124,
        "root_pages_checked_at_original_detail": [2, 3, 4, 5, 12, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 113, 118, 121, 122, 123, 124],
        "root_edge_min_px": {"left": 213, "top": 216, "right": 211, "bottom": 132},
        "checkpoint_visual_qa_passed": True,
        "visual_qa_complete": False,
        "fresh_render_policy": {
            "current_pdf_pages_freshly_rendered": 124,
            "current_render_dpi": 200,
            "current_all_contact_sheets_inspected": 8,
            "all_pages_contact_sheet_checked": 124,
            "original_detail_pages": [2, 3, 4, 5, 12, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 113, 118, 121, 122, 123, 124],
            "last_contact_view_surrogates": [
                "tmp/act33_f030_full_visual_root_200dpi/contact_sheets_4x4/contact-113-124-4x3.png",
                "tmp/act33_f030_full_visual_root_200dpi/contact_sheets_4x4/contact-113-124-4x3-view.jpg",
            ],
            "reason": "All 124 pages of the accepted ACT33 PDF were freshly rendered at 200 dpi. Every canonical contact sheet was inspected, the listed pages were inspected at original detail, and a JPEG surrogate was used only to bypass a viewer defect on the final grayscale contact. No clipping, overlap, blank insertion, malformed display, displaced folio, or terminal fault was found.",
        },
        "root_contact_sheet_thumbnail_percent": 28,
        "final_build_directory": "tmp/act33_f030_build_root",
        "final_layout_sha256": "A05D2ADE5023D39D25702886B94828A4BA6648CB800ACFFB651E4DBD9588B8B0",
        "final_log_sha256": "4CBD48150E55307E693F6B77B632F117528E0026D6B49E29940890A861447F66",
        "actionable_log_diagnostics": 0,
        "nonactionable_underfull_warnings": 6,
        "unresolved_placeholder_hits": 0,
        "literal_quad_leak_hits": 0,
        "embedded_subset_font_rows": 26,
        "unembedded_font_rows": 0,
        "final_root_render_directory": "tmp/act33_f030_full_visual_root_200dpi",
        "final_independent_render_directory": None,
        "final_root_contact_sheet_directory": "tmp/act33_f030_full_visual_root_200dpi/contact_sheets_4x4",
        "final_independent_contact_sheet_directory": None,
        "build_correction": {
            "initial_failed_build_accepted": False,
            "defects": [],
            "action": "F028--F030 were globally propagated before the fresh three-pass ACT33 build. The accepted 124-page build has zero actionable diagnostics, all 26 font rows embedded/subset, a complete fresh 200-dpi render, all-page contact-sheet inspection, targeted original-detail inspection, and a passing isolated recovery audit.",
            "final_build_accepted": True,
            "qpdf_available": False,
            "qpdf_nonavailability_is_not_a_passed_check": True,
        },
        "live_tex_advanced_after_checkpoint": False,
        "fresh_ACT33_build_pending": False,
    })

    recovery = layers["RECOVERY"]
    recovery.update({
        "status": "ACT33_checkpoint_passed_F028_F029_F030_124_page_build_and_isolated_fresh_context_recovery_verified_remaining_literature_formal_package_final_visual_and_release_gates_open",
        "checkpoint_passed": True,
        "checkpoint_record": CHECKPOINT,
        "latest_receipt": RECEIPT_ID,
        "passed": False,
        "act33_fresh_context_test": {
            "status": "PASS_no_discrepancy",
            "path": RECOVERY_REPORT,
            "bytes": 6_097,
            "sha256": "80f7553721f23088b097fa040393a6c8d85f2023a9c37a525f0618176707d63c",
            "checkpoint_bytes": 24_909,
            "checkpoint_sha256": "613a1c5b6c2f5487c171e6b0e7e3688929062cc798d616bc34604fcb9fe87b41",
            "validator_failures": 0,
            "expected_route_warnings": 8,
            "certificates_passed": ["F028", "F029", "F030"],
            "intentional_preseal_discrepancy_repaired_by": RECEIPT_ID,
        },
    })

    assert project["status"] == "active"
    assert project["completion_claimed"] is False
    assert project["codex_goal"]["status"] == "active"
    project["next_action"] = (
        "Continue PO-COL-000001 with the remaining claim-driving cited literature after the sealed F028 whole-version audit, F029 Krasikov-Lagarias reconstruction, and F030 Terras--Allouche--Korec density lineage. Query the immutable route ledgers first, read primary content, preserve exact objects and attribution, and propagate every consequence globally before use. Keep all eight obligations and the durable goal active; do not enter modern Chatnotes, residual Gemini, or archived tasks early; do not contact the quarantined task; do not publish; and start formal work only after a fresh serial release as one watched worker killed at 3 GiB."
    )
    project["last_receipt_id"] = RECEIPT_ID
    project["updated_utc"] = STAMP
    project["current_checkpoint"] = {
        "receipt_id": RECEIPT_ID,
        "path": CHECKPOINT,
        "scope": "Tao_F028_whole_version_Krasikov_Lagarias_F029_and_Terras_Allouche_Korec_F030_exact_literature_lineage_124_page_checkpoint",
        "global_completion": False,
    }

    resource = project["resource_policy"]
    assert resource["lean_worker_private_working_set_limit_bytes"] == 3_221_225_472
    assert resource["maximum_overlapping_lean_builds"] == 1
    append_unique(resource["enforcement_events"], {
        "module": "R7R11CRTForcing",
        "action": "serialization_release_then_correction_arrived_after_sole_bounded_watched_tree_started_Stacks_hold_notified_no_second_worker_started",
        "pids": [42596, 23744, 53084, 54504],
        "lean_worker_working_set_bytes_at_audit": 107_728_896,
        "memory_limit_bytes": 3_221_225_472,
        "poll_milliseconds": 200,
        "audit_utc": "2026-08-28T15:47:16.9582501Z",
        "delegation_source_thread_id": "01a03474-c8fb-7e73-b549-1420961dc8e4",
    })
    append_unique(resource["enforcement_events"], {
        "module": "R7R11CRTForcing",
        "action": "first_bounded_serial_attempt_ended_with_two_maximum_recursion_depth_diagnostics_memory_limit_not_triggered_then_single_bounded_serial_retry_authorized_by_already_started_rule",
        "pids": [23744, 53084, 54504],
        "peak_individual_worker_working_set_bytes": 1_143_291_904,
        "exit_code": 1,
        "started_utc": "2026-08-28T15:46:38.8966208Z",
        "finished_utc": "2026-08-28T15:47:28.4091958Z",
    })
    append_unique(resource["enforcement_events"], {
        "module": "R7R11CRTForcing",
        "action": "sole_bounded_watched_worker_passed_no_overlap_memory_limit_not_triggered",
        "pids": [55788, 39348, 53184],
        "receipt_path": "../Erdos-Straus-Foundation/runtime/R7_R11_CRT_FORCING_LEAN_BUILD.json",
        "receipt_bytes": 2_033,
        "receipt_sha256": "302a516b27c37455cdfd8ec9e7c90a969991f7829e48e74be9dacf5bff3358a1",
        "peak_individual_worker_working_set_bytes": 1_355_563_008,
        "peak_process_tree_working_set_bytes": 1_826_144_256,
        "memory_limit_bytes": 3_221_225_472,
        "poll_milliseconds": 200,
        "exit_code": 0,
        "started_utc": "2026-08-28T15:48:07.2064913Z",
        "finished_utc": "2026-08-28T15:48:24.5815219Z",
    })
    append_unique(resource["enforcement_events"], {
        "module": "all_Lean_Lake",
        "action": "post_R7R11CRTForcing_PASS_audit_no_active_Lean_or_Lake_worker_clear_signal_sent_fresh_release_required_before_any_future_formal_run",
        "pids": [],
        "audit_utc": "2026-08-28T15:48:51.0504363Z",
        "delegation_source_thread_id": "01a03474-c8fb-7e73-b549-1420961dc8e4",
    })
    append_unique(resource["enforcement_events"], {
        "module": "R7R11CRTForcing",
        "action": "later_bounded_attempt_overwrote_mutable_shared_receipt_and_ended_FAIL_exit_minus_1_empty_streams_no_memory_trigger_initiator_and_cause_not_inferred",
        "pids": [26712, 26484],
        "snapshot_path": "qa/R7R11CRTForcing-RESOURCE-SNAPSHOT-20260828T155746Z.json",
        "snapshot_bytes": 3_790,
        "snapshot_sha256": "6b02d63cff539499856ced4cde800e24ad43fef15ed14c6fa615b8686b32c49a",
        "source_receipt_bytes_at_snapshot": 2_615,
        "source_receipt_sha256_at_snapshot": "34eeb9aefef0d436fccbdd1db5f7433dbfdbdaff19754a6e2d9c2b5a5c352cef",
        "peak_individual_worker_working_set_bytes": 451_620_864,
        "peak_process_tree_working_set_bytes": 470_077_440,
        "memory_limit_bytes": 3_221_225_472,
        "poll_milliseconds": 100,
        "exit_code": -1,
        "started_utc": "2026-08-28T15:54:30.4967483Z",
        "finished_utc": "2026-08-28T15:57:46.9928416Z",
    })
    append_unique(resource["enforcement_events"], {
        "module": "all_Lean_Lake",
        "action": "post_later_R7R11CRTForcing_FAIL_audit_no_active_Lean_or_Lake_worker_changed_result_and_fresh_release_requirement_sent_to_coordinator",
        "pids": [],
        "audit_utc": "2026-08-28T16:00:44.7358266Z",
        "delegation_source_thread_id": "01a03474-c8fb-7e73-b549-1420961dc8e4",
    })
    resource["last_enforcement_utc"] = "2026-08-28T16:00:44.7358266Z"
    resource["last_enforcement_result"] = (
        "later_bounded_R7R11CRTForcing_attempt_ended_FAIL_exit_minus_1_under_3_GiB_100_ms_watcher_no_overlap_memory_limit_not_triggered_initiator_and_cause_not_inferred; final_process_table_clear_and_changed_result_sent; fresh_serial_release_required_before_any_future_formal_run"
    )
    resource["serial_coordination_status"] = "process_table_clear_latest_attempt_failed_historical_release_consumed_fresh_release_required"


def build_receipt(
    coverage_bytes: bytes,
    project_bytes: bytes,
    pre_state: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    static_records = {
        relative: record(ROOT / relative, relative)
        for relative in EXPECTED_LOCAL
    }
    external_records = {
        absolute: record(Path(absolute), absolute)
        for absolute in EXPECTED_EXTERNAL
    }
    seal_script = record(Path(__file__).resolve(), "scripts/seal_act33_f030_checkpoint.py")
    return {
        "record_type": "action_receipt",
        "schema_version": "1.0",
        "receipt_id": RECEIPT_ID,
        "timestamp_utc": STAMP,
        "action": "seal_F028_Tao_whole_version_F029_Krasikov_Lagarias_F030_Terras_Allouche_Korec_density_lineage_124_page_reader_visual_QA_bounded_resource_history_and_fresh_context_recovery",
        "inputs": [
            "ACT-COL-000032",
            "raw/USR-0001.txt",
            "raw/USR-0002.txt",
            "raw/USR-0003.txt",
            "state/index_routes.jsonl",
            "state/document_routes.jsonl",
            "state/index_snapshot.json",
            "SRC-COL-000005",
            "SRC-COL-000027",
            "SRC-COL-000028",
            "SRC-COL-000029",
            "SRC-COL-000030",
            "SRC-COL-000031",
            "SRC-COL-000032",
        ],
        "outputs": [
            CHECKPOINT,
            RECOVERY_REPORT,
            "state/coverage.json",
            "state/project_state.json",
            "state/action_receipts.jsonl",
            "tmp/act33_f030_build_root/main.pdf",
            "tmp/act33_f030_full_visual_root_200dpi",
        ],
        "result": "pass_working_checkpoint_goal_and_eight_obligations_active_remaining_literature_formal_package_final_visual_and_release_gates_open",
        "measurements": {
            "predecessor_receipt": "ACT-COL-000032",
            "pre_state": pre_state,
            "post_state": {
                "coverage": {"path": "state/coverage.json", "bytes": len(coverage_bytes), "sha256": sha256_bytes(coverage_bytes)},
                "project_state": {"path": "state/project_state.json", "bytes": len(project_bytes), "sha256": sha256_bytes(project_bytes)},
                "receipt_count_after_append": 33,
            },
            "static_artifacts": static_records,
            "external_artifacts": external_records,
            "seal_script": seal_script,
            "records": {"sources": 32, "claims": 136, "morphisms": 32, "proof_obligations": 8, "open_obligations": 8},
            "record_boundary": {
                "F028": ["CLM-COL-000122"],
                "F029": ["SRC-COL-000028", "CLM-COL-000123--000126", "MOR-COL-000032"],
                "F030": ["SRC-COL-000029--000032", "CLM-COL-000127--000136", "no_new_morphism"],
                "F030_morphism_references": "only_CLM-COL-000136_uses_MOR-COL-000001_and_MOR-COL-000032",
            },
            "finite_certificates": {
                "F028": {"status": "PASS", "raw_hunks": 124, "substantive_hunks": 28, "citation_calls": 25, "cited_keys": 23, "bibliography_items": 24},
                "F029": {"status": "PASS", "clock_checks": 2_010_000, "omitted_state_checks": 1_005_735, "target_one_checks": 10_000},
                "F030": {"status": "PASS", "classical_remainders": 16_392, "generalized_fibres": 64_165, "count_checks": 139, "parity_affine": 16_382, "terminal_words": 1_752, "repaired_coverage": 77, "agreement": 49, "weak_boundary": 36, "separating_k": 529_254},
            },
            "mathematical_nonclaims": [
                "no_Collatz_conjecture_proof",
                "no_endpoint_promotion",
                "no_clock_identity",
                "no_density_notions_identified",
                "no_Krasikov_Lagarias_k11_feasible_vector_reproduction",
                "no_infinite_density_theorem_certified_by_finite_scripts",
                "no_Tao_analytic_theorem_certified_by_finite_scripts",
                "Allouche_divisible_branch_completion_separately_attributed_to_edition",
            ],
            "pdf": {"pages": 124, "bytes": 1_261_638, "sha256": "509b415815623cd7a0c661a3cd01a66282edd339eb07888d184b9acf2ff17f72", "actionable_diagnostics": 0, "nonactionable_underfull_warnings": 6, "embedded_subset_font_rows": 26, "unembedded_font_rows": 0},
            "visual_QA": {"rendered_pages": 124, "dpi": 200, "render_bytes": 52_989_982, "canonical_contact_sheets": 8, "canonical_contact_bytes": 13_253_297, "all_pages_checked": 124, "original_detail_pages": [2, 3, 4, 5, 12, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 113, 118, 121, 122, 123, 124], "edge_min_px": {"left": 213, "top": 216, "right": 211, "bottom": 132}, "issues": 0, "release_visual_QA_complete": False},
            "fresh_context_recovery": {"status": "PASS_no_discrepancy", "checkpoint_pins": 42, "validator_failures": 0, "expected_route_warnings": 8, "intentional_preseal_discrepancy": "ACT32 pointers only; repaired by this receipt"},
            "resource_policy": {
                "historical_bounded_pass": {"status": "PASS", "receipt_bytes_when_observed": 2_033, "receipt_sha256_when_observed": "302a516b27c37455cdfd8ec9e7c90a969991f7829e48e74be9dacf5bff3358a1", "peak_individual_bytes": 1_355_563_008, "peak_tree_bytes": 1_826_144_256},
                "latest_snapshotted_attempt": {"status": "FAIL", "exit_code": -1, "single_worker": True, "memory_limit_bytes": 3_221_225_472, "peak_individual_bytes": 451_620_864, "peak_tree_bytes": 470_077_440, "memory_triggered": False, "initiator_inferred": False, "failure_cause_inferred": False},
                "final_workers": 0,
                "changed_result_and_clear_signal_sent": True,
                "fresh_release_required": True
            },
            "completion_claimed": False,
        },
        "notes": [
            "Frozen routing artifacts remained byte-identical and no indexing restart occurred.",
            "Every F028--F030 repair and nonclaim remains separately typed and attributed; no mathematical ledger row changed during the seal.",
            "The isolated fresh-context reviewer recovered the exact goal, restrictions, mathematical boundaries, finite-certificate scopes, build evidence, intentional pre-seal pointer discrepancy, and next action.",
            "The 124-page visual pass is checkpoint QA, not final release QA; visual_qa_complete remains false.",
            "No public record was mutated and quarantined task 019fe2cf-438a-7112-859c-119accee0e9e was not contacted or used.",
            "The durable goal and all eight proof obligations remain active. The next action is remaining claim-driving cited literature, not Chatnotes, Gemini, archives, or completion.",
        ],
    }


def atomic_replace(contents: dict[Path, bytes]) -> None:
    originals = {path: path.read_bytes() for path in contents}
    temporaries: dict[Path, Path] = {}
    try:
        for path, data in contents.items():
            fd, temp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
            temp = Path(temp_name)
            temporaries[path] = temp
            with os.fdopen(fd, "wb") as handle:
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
        replaced: list[Path] = []
        try:
            for path, temp in temporaries.items():
                os.replace(temp, path)
                replaced.append(path)
        except Exception:
            for path in replaced:
                path.write_bytes(originals[path])
            raise
    finally:
        for temp in temporaries.values():
            if temp.exists():
                temp.unlink()


def verify_idempotent_state(receipts: list[dict[str, Any]]) -> None:
    assert len(receipts) == 33
    assert [row["receipt_id"] for row in receipts] == [f"ACT-COL-{index:06d}" for index in range(1, 34)]
    receipt = receipts[-1]
    assert receipt["receipt_id"] == RECEIPT_ID
    project = load_json(STATE / "project_state.json")
    coverage = load_json(STATE / "coverage.json")
    layers = {layer["layer_id"]: layer for layer in coverage["layers"]}
    assert project["last_receipt_id"] == RECEIPT_ID
    assert project["current_checkpoint"]["receipt_id"] == RECEIPT_ID
    assert project["current_checkpoint"]["global_completion"] is False
    assert project["completion_claimed"] is False
    assert layers["SYN"]["working_pdf_pages"] == 124
    assert layers["SYN"]["fresh_ACT33_build_pending"] is False
    assert layers["SYN"]["visual_qa_complete"] is False
    assert layers["RECOVERY"]["latest_receipt"] == RECEIPT_ID
    assert layers["RECOVERY"]["passed"] is False
    post = receipt["measurements"]["post_state"]
    assert record(STATE / "coverage.json", "state/coverage.json") == post["coverage"]
    assert record(STATE / "project_state.json", "state/project_state.json") == post["project_state"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()

    verify_static_artifacts()
    verify_ledgers()

    receipts_path = STATE / "action_receipts.jsonl"
    receipts = load_jsonl(receipts_path)
    receipt_ids = [row.get("receipt_id") for row in receipts]
    if RECEIPT_ID in receipt_ids:
        verify_idempotent_state(receipts)
        print(json.dumps({"status": "PASS", "changed": False, "receipt_id": RECEIPT_ID, "global_completion": False}, sort_keys=True))
        return 0

    assert receipt_ids == [f"ACT-COL-{index:06d}" for index in range(1, 33)]
    assert receipts[-1]["receipt_id"] == "ACT-COL-000032"
    for relative, expected in EXPECTED_PRE_STATE.items():
        assert_pin(ROOT / relative, expected)

    coverage_path = STATE / "coverage.json"
    project_path = STATE / "project_state.json"
    coverage = load_json(coverage_path)
    project = load_json(project_path)
    assert project["last_receipt_id"] == "ACT-COL-000032"
    assert project["current_checkpoint"]["receipt_id"] == "ACT-COL-000032"
    pre_recovery = next(layer for layer in coverage["layers"] if layer["layer_id"] == "RECOVERY")
    pre_syn = next(layer for layer in coverage["layers"] if layer["layer_id"] == "SYN")
    assert pre_recovery["latest_receipt"] == "ACT-COL-000032"
    assert pre_syn["working_pdf_pages"] == 106
    assert pre_syn["fresh_ACT33_build_pending"] is True

    pre_state = {
        key.split("/")[-1].replace(".jsonl", "").replace(".json", ""): record(ROOT / key, key)
        for key in EXPECTED_PRE_STATE
    }
    update_state(coverage, project)
    coverage_bytes = json_bytes(coverage)
    project_bytes = json_bytes(project)
    receipt = build_receipt(coverage_bytes, project_bytes, pre_state)
    receipt_line = (json.dumps(receipt, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
    ledger_bytes = receipts_path.read_bytes()
    assert ledger_bytes.endswith(b"\n")
    final_receipts_bytes = ledger_bytes + receipt_line

    result = {
        "status": "PASS",
        "changed": not args.check_only,
        "check_only": args.check_only,
        "receipt_id": RECEIPT_ID,
        "records": {"sources": 32, "claims": 136, "morphisms": 32, "open_obligations": 8},
        "coverage_post": {"bytes": len(coverage_bytes), "sha256": sha256_bytes(coverage_bytes)},
        "project_state_post": {"bytes": len(project_bytes), "sha256": sha256_bytes(project_bytes)},
        "action_receipts_post": {"bytes": len(final_receipts_bytes), "sha256": sha256_bytes(final_receipts_bytes)},
        "global_completion": False,
    }
    if args.check_only:
        print(json.dumps(result, sort_keys=True))
        return 0

    atomic_replace({
        coverage_path: coverage_bytes,
        project_path: project_bytes,
        receipts_path: final_receipts_bytes,
    })
    verify_idempotent_state(load_jsonl(receipts_path))
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
