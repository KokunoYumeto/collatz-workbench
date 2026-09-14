"""Seal the verified ACT32 PDF/visual-QA measurements into live state."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "tmp" / "tao_main_reduction_act32_final_20260828"
STAMP = "2026-08-28T12:26:36.0751565Z"

EXPECTED = {
    "main.pdf": (1_133_714, "1aa6e7f37db0ae8c417651bfa1fa4a2634ebbe52191f69ef748a7a001148e2d8"),
    "main.log": (31_840, "711473b671a3b0308d7516ae16a2aac335d18e4eece4bd9db438ec9abe251075"),
    "main-layout.txt": (377_152, "333abb0f9f73fde103950492c0269b815cc0a7e60e4c2e17f111852ccabf7a79"),
    "pdffonts.txt": (2_565, "6a195059941ab57bd82ff917fbebe499834b71877eec4cd0ca849f40bfc397cc"),
    "pdfinfo.txt": (808, "73a2d3f1c8b5c0aa24a506dbe1a901c43c11fdf163404cd3c7daadaf7f18bb75"),
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    for name, (size, sha256) in EXPECTED.items():
        path = BUILD / name
        assert path.stat().st_size == size, (name, size, path.stat().st_size)
        assert digest(path) == sha256, (name, sha256, digest(path))

    rendered = sorted((BUILD / "rendered_final_root_200dpi").glob("page-*.png"))
    contacts = sorted((BUILD / "contact_sheets_final_root").glob("contact-*.png"))
    assert len(rendered) == 106
    assert sum(path.stat().st_size for path in rendered) == 45_406_236
    assert len(contacts) == 14
    assert sum(path.stat().st_size for path in contacts) == 15_616_660

    coverage_path = ROOT / "state" / "coverage.json"
    coverage = load(coverage_path)
    layers = {layer["layer_id"]: layer for layer in coverage["layers"]}
    syn = layers["SYN"]
    syn.update({
        "status": "working_foundational_chapter_106_pages_exact_Tao_Proposition1_11_Theorem3_1_Theorem1_6_Theorem1_3_reduction_added_zero_actionable_diagnostics_all_fonts_embedded_subset_fresh_all_page_QA_pass_not_release_QA",
        "working_pdf_pages": 106,
        "working_pdf_bytes": 1_133_714,
        "working_pdf_sha256": EXPECTED["main.pdf"][1].upper(),
        "root_rendered_page_count": 106,
        "root_render_dpi": 200,
        "root_render_bytes": 45_406_236,
        "root_contact_sheet_count": 14,
        "root_contact_sheet_bytes": 15_616_660,
        "current_pages_visually_checked": 106,
        "root_all_pages_contact_sheet_checked": 106,
        "root_pages_checked_at_original_detail": [2, 94, 95, 96, 97, 98, 99, 100, 101, 105, 106],
        "root_edge_min_px": {"left": 213, "top": 215, "right": 211, "bottom": 132},
        "checkpoint_visual_qa_passed": True,
        "visual_qa_complete": False,
        "fresh_render_policy": {
            "current_pdf_pages_freshly_rendered": 106,
            "current_render_dpi": 200,
            "current_all_contact_sheets_inspected": 14,
            "preliminary_render_all_pages_and_contact_sheets_inspected": 106,
            "pixel_identical_to_preliminary_final_pages": 104,
            "pixel_identical_page_set": "1-104",
            "final_changed_pages": [105, 106],
            "final_changed_pages_contact_sheet_checked": [105, 106],
            "final_changed_pages_checked_at_original_detail": [105, 106],
            "proof_pages_checked_at_original_detail": [94, 95, 96, 97, 98, 99, 100, 101],
            "reason": "All 106 preliminary pages and all fourteen preliminary contact sheets were inspected. After the source-register propagation, a fresh final 106-page render was produced: pages 1-104 are pixel-identical to the inspected preliminary render, while changed pages 105-106 were inspected on the final contact sheet and at original render detail. Page 2 and the complete new proof on pages 94-101 also received original-detail inspection.",
        },
        "root_contact_sheet_thumbnail_percent": 28,
        "final_build_directory": "tmp/tao_main_reduction_act32_final_20260828",
        "final_layout_sha256": EXPECTED["main-layout.txt"][1].upper(),
        "final_log_sha256": EXPECTED["main.log"][1].upper(),
        "actionable_log_diagnostics": 0,
        "unresolved_placeholder_hits": 0,
        "literal_quad_leak_hits": 0,
        "embedded_subset_font_rows": 25,
        "unembedded_font_rows": 0,
        "final_root_render_directory": "tmp/tao_main_reduction_act32_final_20260828/rendered_final_root_200dpi",
        "final_independent_render_directory": None,
        "final_root_contact_sheet_directory": "tmp/tao_main_reduction_act32_final_20260828/contact_sheets_final_root",
        "final_independent_contact_sheet_directory": None,
        "build_correction": {
            "initial_failed_build_accepted": False,
            "defects": [
                "The draft used an untruncated signed dyadic logarithmic sum where only the nonnegative strata were admissible.",
                "The draft threshold and small-block wording required real-N_0 and empty-terminal-block repairs.",
                "The draft overstated information loss in Collatz-time recovery.",
                "The first clean render exposed a stale downstream-gate sentence in the source register.",
            ],
            "action": "All adversarial findings and the stale source-register boundary were repaired and globally propagated. The final fresh root three-pass build then had zero actionable diagnostics, 25 embedded/subset font rows, a fresh 106-page 200-dpi render, complete contact-sheet inspection with pixel identity recorded for inherited final pages, and original-detail inspection of every changed final page and the complete new proof.",
            "final_build_accepted": True,
        },
    })
    if "prior_checkpoint_independent_QA" in syn:
        syn["prior_checkpoint_independent_QA"]["note"] = (
            "Retained as prior-checkpoint evidence only; it is not represented as an independent render of the current 106-page PDF."
        )
    write(coverage_path, coverage)

    project_path = ROOT / "state" / "project_state.json"
    project = load(project_path)
    project["resource_policy"]["last_enforcement_utc"] = STAMP
    project["resource_policy"]["last_enforcement_result"] = (
        "all_observed_uncapped_R107DeficitProgression_trees_stopped; compliant_single_"
        "bounded_watched_worker_was_left_untouched; final_post_QA_audit_found_no_active_"
        "R107_Lean_or_Lake_worker; no_build_started_by_this_task"
    )
    project["updated_utc"] = STAMP
    write(project_path, project)

    print(json.dumps({
        "status": "PASS",
        "pdf_pages": 106,
        "rendered_pages": 106,
        "contact_sheets": 14,
        "all_pages_checked": 106,
        "final_changed_pages_original_detail": [105, 106],
        "actionable_diagnostics": 0,
        "unembedded_fonts": 0,
        "proof_obligation_closed": False,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
