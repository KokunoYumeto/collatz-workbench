#!/usr/bin/env python3
"""Deterministically seal the ACT31 Proposition 1.11 working checkpoint."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "tmp" / "tao_prop111_act31_20260828"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json_if_changed(path: Path, value: dict) -> bool:
    rendered = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    if path.read_text(encoding="utf-8") == rendered:
        return False
    path.write_text(rendered, encoding="utf-8", newline="\n")
    return True


pdf = BUILD / "main.pdf"
log = BUILD / "main.log"
layout = BUILD / "main-layout.txt"
fonts = BUILD / "pdffonts.txt"
render_dir = BUILD / "rendered_final_root_200dpi"
contact_dir = BUILD / "contact_sheets_final_root"

assert pdf.stat().st_size == 1_089_943
assert sha256(pdf) == "a5bd834b97c760416e236ee35dbb048377788984ff6d51a732920028027f6c19"
assert log.stat().st_size == 31_632
assert sha256(log) == "6c3a053374c6a16ad7cfd3c27604bafe86c18481944ac9a5d1c56060ac3be9af"
assert layout.stat().st_size == 352_866
assert sha256(layout) == "4b82cbdaf24fa64dd99f0244fcc18879d2fa2d9e5b43a3f415c25d66e094e2c4"
assert fonts.stat().st_size == 2_565
assert sha256(fonts) == "fd3439fcad506e7c075b16a5e887a5f77ade1cbd20335bc7b000099c70cb58bb"

rendered = sorted(render_dir.glob("page-*.png"))
contacts = sorted(contact_dir.glob("contact-*.png"))
assert len(rendered) == 99
assert sum(path.stat().st_size for path in rendered) == 42_683_768
assert len(contacts) == 13
assert sum(path.stat().st_size for path in contacts) == 16_129_216

coverage_path = ROOT / "state" / "coverage.json"
coverage = load_json(coverage_path)
layers = {layer["layer_id"]: layer for layer in coverage["layers"]}

syn = layers["SYN"]
syn.update(
    {
        "status": "working_foundational_chapter_99_pages_Tao_v7_Proposition1_11_exact_first_passage_stabilisation_reconstruction_added_zero_actionable_diagnostics_all_fonts_embedded_subset_fresh_all_page_QA_pass_not_release_QA",
        "working_pdf_pages": 99,
        "working_pdf_bytes": 1_089_943,
        "working_pdf_sha256": "A5BD834B97C760416E236EE35DBB048377788984FF6D51A732920028027F6C19",
        "root_rendered_page_count": 99,
        "root_render_dpi": 200,
        "root_render_bytes": 42_683_768,
        "root_contact_sheet_count": 13,
        "root_contact_sheet_bytes": 16_129_216,
        "current_pages_visually_checked": 99,
        "root_all_pages_contact_sheet_checked": 99,
        "root_pages_checked_at_original_detail": [2, 88, 89, 90, 91, 92, 93, 94, 98, 99],
        "root_edge_min_px": {"left": 213, "top": 215, "right": 211, "bottom": 132},
        "checkpoint_visual_qa_passed": True,
        "visual_qa_complete": False,
        "fresh_render_policy": {
            "current_pdf_pages_freshly_rendered": 99,
            "current_render_dpi": 200,
            "current_all_contact_sheets_inspected": 13,
            "byte_identical_to_fully_inspected_ACT30_pages": 86,
            "byte_identical_page_set": "1 and 3-87",
            "changed_pages": [2, *range(88, 100)],
            "changed_pages_contact_sheet_checked": [2, *range(88, 100)],
            "changed_pages_checked_at_original_detail": [2, 88, 89, 90, 91, 92, 93, 94, 98, 99],
            "reason": "The current 99-page PDF was freshly rendered in full and all thirteen contact sheets were inspected. Current pages 1 and 3-87 are pixel-identical to the fully inspected ACT30 200-dpi render; every changed or new page was contact-sheet checked, and pages 2, 88-94, 98, and 99 were checked at original render detail.",
        },
        "root_contact_sheet_thumbnail_percent": 24,
        "final_build_directory": "tmp/tao_prop111_act31_20260828",
        "final_layout_sha256": "4B82CBDAF24FA64DD99F0244FCC18879D2FA2D9E5B43A3F415C25D66E094E2C4",
        "final_log_sha256": "6C3A053374C6A16AD7CFD3C27604BAFE86C18481944AC9A5D1C56060AC3BE9AF",
        "actionable_log_diagnostics": 0,
        "unresolved_placeholder_hits": 0,
        "literal_quad_leak_hits": 0,
        "embedded_subset_font_rows": 25,
        "unembedded_font_rows": 0,
        "final_root_render_directory": "tmp/tao_prop111_act31_20260828/rendered_final_root_200dpi",
        "final_independent_render_directory": None,
        "final_root_contact_sheet_directory": "tmp/tao_prop111_act31_20260828/contact_sheets_final_root",
        "final_independent_contact_sheet_directory": None,
        "build_correction": {
            "initial_failed_build_accepted": False,
            "defect": "The pre-seal draft contained a reversed floor direction in the descent estimate and raw control-byte/backslash corruption.",
            "action": "The floor-directed exponents and TeX bytes were repaired; a second independent read-only audit passed; then three clean TeX passes, complete font inspection, a fresh 99-page 200-dpi render, all-page contact-sheet inspection, and original-detail inspection of the changed proof and terminal pages were completed.",
            "final_build_accepted": True,
        },
    }
)
if "prior_checkpoint_independent_QA" in syn:
    syn["prior_checkpoint_independent_QA"]["note"] = (
        "Retained as prior-checkpoint evidence only; it is not represented as an independent render of the current 99-page PDF."
    )

recovery = layers["RECOVERY"]
recovery.update(
    {
        "status": "working_checkpoint_passed_state_advanced_through_Tao_v7_Proposition1_14_Proposition1_9_and_exact_Proposition1_11_ACT31_Theorem1_6_Theorem1_3_later_literature_Chatnotes_and_release_recovery_gates_open",
        "checkpoint_passed": True,
        "checkpoint_record": "qa/RECOVERY-CHECKPOINT-20260828-ACT31.md",
        "latest_receipt": "ACT-COL-000031",
        "passed": False,
    }
)

project_path = ROOT / "state" / "project_state.json"
project = load_json(project_path)
project["resource_policy"].update(
    {
        "last_enforcement_utc": "2026-08-28T09:41:50.6446005Z",
        "last_enforcement_result": "stopped_new_uncapped_R107DeficitProgression_Coordinates_Fibres_Complement_and_Transport_process_trees_as_they_appeared; transient_Exact_worker_ended_before_second_stop; verified_no_remaining_R107_Lean_Lake_process_tree; no_build_restarted_by_this_task",
        "enforcement_events": [
            {"module": "Coordinates", "action": "stopped_exact_process_tree", "pids": [47260, 24180, 35504, 50292]},
            {"module": "Fibres", "action": "stopped_exact_process_tree", "pids": [50800, 52108, 50296, 46952]},
            {"module": "Complement", "action": "stopped_exact_process_tree", "pids": [32844, 39604, 30832, 40480]},
            {"module": "Transport", "action": "stopped_exact_process_tree", "pids": [34208]},
            {"module": "Exact", "action": "ended_before_second_stop", "pids": [34716]},
        ],
    }
)
project["last_receipt_id"] = "ACT-COL-000031"
project["updated_utc"] = "2026-08-28T09:41:50.6446005Z"
project["current_checkpoint"] = {
    "receipt_id": "ACT-COL-000031",
    "path": "qa/RECOVERY-CHECKPOINT-20260828-ACT31.md",
    "scope": "Tao_v5_v7_journal_Proposition1_11_exact_first_passage_stabilisation_and_affine_path_endpoint_bijection",
    "global_completion": False,
}

changed = {
    "coverage": write_json_if_changed(coverage_path, coverage),
    "project_state": write_json_if_changed(project_path, project),
}
print(json.dumps({"status": "PASS", "changed": changed}, sort_keys=True))
