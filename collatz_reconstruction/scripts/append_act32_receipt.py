#!/usr/bin/env python3
"""Append the contiguous, idempotent ACT-COL-000032 receipt."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state"
BUILD = ROOT / "tmp" / "tao_main_reduction_act32_final_20260828"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def file_record(relative: str) -> dict:
    path = ROOT / relative
    return {"path": relative, "bytes": path.stat().st_size, "sha256": digest(path)}


def absolute_record(path_text: str) -> dict:
    path = Path(path_text)
    return {"path": path_text, "bytes": path.stat().st_size, "sha256": digest(path)}


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


frozen = {
    "index_routes": file_record("state/index_routes.jsonl"),
    "document_routes": file_record("state/document_routes.jsonl"),
    "snapshot": file_record("state/index_snapshot.json"),
}
assert frozen["index_routes"] == {
    "path": "state/index_routes.jsonl",
    "bytes": 274_170,
    "sha256": "b05028694bf133b9b19f2b0c0a771323b7a47ae872c0712769267aaf1f1eff38",
}
assert frozen["document_routes"] == {
    "path": "state/document_routes.jsonl",
    "bytes": 324_776,
    "sha256": "e439a5f9a70253b00824df5be791415e1c068d574c23f6f7f61851c19a88b2a5",
}
assert frozen["snapshot"] == {
    "path": "state/index_snapshot.json",
    "bytes": 799,
    "sha256": "7d5a17440a3cb039f2bfbb4814567b5805117002136cc65687de738ee99af62f",
}

sources = {
    "Tao_v7_TeX": absolute_record(
        "C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/latex/1909.03562v7/collatz.tex"
    ),
    "Tao_v7_eprint": absolute_record(
        "C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/source/1909.03562v7.eprint"
    ),
    "Tao_v5_TeX": absolute_record(
        "C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/latex/1909.03562v5/collatz.tex"
    ),
    "Tao_v5_eprint": absolute_record(
        "C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/source/1909.03562v5.eprint"
    ),
    "Tao_journal_PDF": absolute_record(
        "C:/Users/LOCAL_USER/Documents/arxiv_latex/library/_recovered_from_papers/by_title/Tao Almost all orbits of the Collatz map attain almost bounded values.pdf"
    ),
}
assert (sources["Tao_v7_TeX"]["bytes"], sources["Tao_v7_TeX"]["sha256"]) == (
    164_932,
    "bfbc39432d4084a276416cb019a592003c868fa32f18e2f90028ac325ae5c19d",
)
assert (sources["Tao_v7_eprint"]["bytes"], sources["Tao_v7_eprint"]["sha256"]) == (
    1_226_861,
    "ba81acd6254838251f1ee585256a6f9f223cdc9c73bed0a3c4fd25782d0124ad",
)
assert (sources["Tao_v5_TeX"]["bytes"], sources["Tao_v5_TeX"]["sha256"]) == (
    163_356,
    "c676b362b30807aa6690d0d4f16b8c8e84324732f5c0eb72ccfd875000276ae0",
)
assert (sources["Tao_v5_eprint"]["bytes"], sources["Tao_v5_eprint"]["sha256"]) == (
    1_226_298,
    "eb7a4668ebf27a3f795f72fcdc8d992ada365824359c734fa58813c750ff2ede",
)
assert (sources["Tao_journal_PDF"]["bytes"], sources["Tao_journal_PDF"]["sha256"]) == (
    1_008_484,
    "55c817c73498f940ed1e70f10208105922f1f7c89e378dcb629040c534151a2b",
)

artifacts = {
    "live_TeX_root": file_record("tex/main.tex"),
    "literature_spine": file_record("tex/chapters/01_literature_spine.tex"),
    "first_passage_chapter": file_record("tex/chapters/01i_tao_first_passage_stabilisation.tex"),
    "main_reduction_chapter": file_record("tex/chapters/01j_tao_main_theorem_reduction.tex"),
    "source_register": file_record("tex/chapters/99_source_register.tex"),
    "F026_audit": file_record("qa/TAO-V5-V7-JOURNAL-F026-prop111-first-passage-audit.md"),
    "F027_audit": file_record("qa/TAO-V5-V7-JOURNAL-F027-main-theorem-reduction-audit.md"),
    "recovery_checkpoint": file_record("qa/RECOVERY-CHECKPOINT-20260828-ACT32.md"),
    "main_reduction_certificate": file_record("certificates/tao_main_reduction_checks.py"),
    "source_registry": file_record("state/source_registry.jsonl"),
    "claims": file_record("state/claims.jsonl"),
    "morphisms": file_record("state/morphisms.jsonl"),
    "proof_obligations": file_record("state/proof_obligations.jsonl"),
    "coverage": file_record("state/coverage.json"),
    "project_state": file_record("state/project_state.json"),
    "todo": file_record("TODO.md"),
    "main_reduction_propagation_script": file_record("scripts/propagate_tao_main_reduction_act32.py"),
    "ACT32_seal_script": file_record("scripts/seal_tao_main_reduction_act32.py"),
    "ACT32_finalize_script": file_record("scripts/finalize_tao_main_reduction_act32.py"),
    "ACT32_first_passage_boundary_hash_repair_script": file_record(
        "scripts/repair_act32_first_passage_boundary_hash.py"
    ),
    "contact_sheet_script": file_record("scripts/make_pdf_contact_sheets.py"),
    "margin_measurement_script": file_record("scripts/measure_render_margins.py"),
    "ACT32_receipt_script": file_record("scripts/append_act32_receipt.py"),
}

expected_artifacts = {
    "live_TeX_root": (2_275, "dad1321989bcb94c63d53329c69b0cd6ae4ba7980b970ce10b05d53e54d03c95"),
    "literature_spine": (69_389, "cce8e24a7e31d1ed24633d2f71992f3b674f188225222bb0be50273b58aceb48"),
    "first_passage_chapter": (20_537, "4757ddcbd1ca4353b51f243c65fd8d0468f7b10700f1a091c881357a24edd647"),
    "main_reduction_chapter": (19_796, "53d97d24d201fe90f97fde3a4e3afbf4e21949f4fa40be559562cc995375cffa"),
    "source_register": (18_553, "2e7ee2a60d2e29e12670009487bb4793f3105963e3d1c4008157e8124c11021d"),
    "F026_audit": (15_068, "37334a91b9fee6cbcba5cb8c6d8d368981d1d96b254495af3f3454b8e828e320"),
    "F027_audit": (13_607, "7ab39a57a00e5c753fdd895ec07cab7f3c672a2b479c80b1369db6cd9ae3bd37"),
    "recovery_checkpoint": (16_037, "cb7e5e5e9c172f27ab15cacfc2459201cf06c19b4a793c98b16d048bc5bf0d8a"),
    "main_reduction_certificate": (17_676, "feab839198920b58469694605cc604b128bac78e0d032258e325b3d9b173c795"),
    "source_registry": (100_615, "26dd42562bd7044f0867ec64e0e7a98c79f575c308edf267d3b8abc8559481ed"),
    "claims": (137_614, "847078d7000f47aed5f381754ba032f6a1337038fd223927267f4c05070656ca"),
    "morphisms": (53_773, "95219ebde8e079f0c2c407166ce326d1b588163053e34bd03511948bdcaebd81"),
    "proof_obligations": (43_943, "3a217302bf01b0f6c5348395ca50604b1bfb408031875bb5d0bc0352babfb2bf"),
    "coverage": (7_583, "a79bb8b1e0f426484f9972ee9c8fa90e28c9eeaeba08e8b89530ac5008b50a95"),
    "project_state": (10_530, "bbe60a3574e09d2597db5c69b5946693a3397b01aaee75738b5022b26e9e8f50"),
    "todo": (18_947, "c93afd5c852dba3b96617ee30dfcc471c5284b88aae32d145bfb4cfe973ea5d2"),
    "main_reduction_propagation_script": (38_397, "309e94bb479b6b0de43094425061f048fe0eb470295edfad97f26b8e1eb8404f"),
    "ACT32_seal_script": (7_117, "958451cc0f90c7f11d505fb326c025bc38f52ab994246a0b2fd4af7656ede55f"),
    "ACT32_finalize_script": (3_739, "f9cd825cc2cbc982ad1c4569b60af01f46280b98bc3a20dab1bc804a2937ffa0"),
    "ACT32_first_passage_boundary_hash_repair_script": (3_808, "93b7bc189dabbffc8f50e0441daace84e8dd4a422e751be1f826e061f838cb4c"),
    "contact_sheet_script": (2_705, "20b576796beb628d48b80b8b96d6be671c8e820456d4185f69b86c2844bad9bc"),
    "margin_measurement_script": (1_734, "973bc17eb714cc29467e67e32278cca0f93c6d57ed14fc52d20942b6c4df268c"),
}
for name, (size, sha256) in expected_artifacts.items():
    assert artifacts[name]["bytes"] == size, (name, artifacts[name]["bytes"], size)
    assert artifacts[name]["sha256"] == sha256, (name, artifacts[name]["sha256"], sha256)

source_records = read_jsonl(STATE / "source_registry.jsonl")
claim_records = read_jsonl(STATE / "claims.jsonl")
morphism_records = read_jsonl(STATE / "morphisms.jsonl")
obligation_records = read_jsonl(STATE / "proof_obligations.jsonl")
counts = {
    "sources": sum(record.get("record_type") == "source_document" for record in source_records),
    "claims": sum(record.get("record_type") == "claim" for record in claim_records),
    "morphisms": sum(record.get("record_type") == "morphism" for record in morphism_records),
    "proof_obligations": sum(record.get("record_type") == "proof_obligation" for record in obligation_records),
}
assert counts == {"sources": 27, "claims": 121, "morphisms": 31, "proof_obligations": 8}
assert claim_records[0]["next_id"] == "CLM-COL-000122"
assert morphism_records[0]["next_id"] == "MOR-COL-000032"

coverage = json.loads((STATE / "coverage.json").read_text(encoding="utf-8"))
recovery = next(layer for layer in coverage["layers"] if layer["layer_id"] == "RECOVERY")
syn = next(layer for layer in coverage["layers"] if layer["layer_id"] == "SYN")
assert recovery["checkpoint_record"] == "qa/RECOVERY-CHECKPOINT-20260828-ACT32.md"
assert recovery["latest_receipt"] == "ACT-COL-000032"
assert recovery["checkpoint_passed"] is True and recovery["passed"] is False
assert syn["working_pdf_pages"] == 106
assert syn["checkpoint_visual_qa_passed"] is True
assert syn["visual_qa_complete"] is False
assert syn["independent_rendered_page_count"] == 0
assert "final fresh root three-pass build" in syn["build_correction"]["action"]

project = json.loads((STATE / "project_state.json").read_text(encoding="utf-8"))
assert project["status"] == "active"
assert project["completion_claimed"] is False
assert project["codex_goal"]["status"] == "active"
assert project["last_receipt_id"] == "ACT-COL-000032"
assert project["current_checkpoint"]["path"] == "qa/RECOVERY-CHECKPOINT-20260828-ACT32.md"
assert project["current_checkpoint"]["global_completion"] is False

pdf = BUILD / "main.pdf"
log = BUILD / "main.log"
layout = BUILD / "main-layout.txt"
fonts = BUILD / "pdffonts.txt"
info = BUILD / "pdfinfo.txt"
rendered = sorted((BUILD / "rendered_final_root_200dpi").glob("page-*.png"))
contacts = sorted((BUILD / "contact_sheets_final_root").glob("contact-*.png"))
assert (pdf.stat().st_size, digest(pdf)) == (
    1_133_714,
    "1aa6e7f37db0ae8c417651bfa1fa4a2634ebbe52191f69ef748a7a001148e2d8",
)
assert (log.stat().st_size, digest(log)) == (
    31_840,
    "711473b671a3b0308d7516ae16a2aac335d18e4eece4bd9db438ec9abe251075",
)
assert (layout.stat().st_size, digest(layout)) == (
    377_152,
    "333abb0f9f73fde103950492c0269b815cc0a7e60e4c2e17f111852ccabf7a79",
)
assert (fonts.stat().st_size, digest(fonts)) == (
    2_565,
    "6a195059941ab57bd82ff917fbebe499834b71877eec4cd0ca849f40bfc397cc",
)
assert (info.stat().st_size, digest(info)) == (
    808,
    "73a2d3f1c8b5c0aa24a506dbe1a901c43c11fdf163404cd3c7daadaf7f18bb75",
)
assert len(rendered) == 106 and sum(path.stat().st_size for path in rendered) == 45_406_236
assert len(contacts) == 14 and sum(path.stat().st_size for path in contacts) == 15_616_660

receipt = {
    "record_type": "action_receipt",
    "schema_version": "1.0",
    "receipt_id": "ACT-COL-000032",
    "timestamp_utc": "2026-08-28T12:46:29.9462086Z",
    "action": (
        "tao_v5_v7_journal_exact_Proposition1_11_to_Theorem3_1_Theorem1_6_"
        "Theorem1_3_main_reduction_eight_source_defects_fixed_threshold_"
        "indexed_tail_morphism_fixed_K_tail_repair_exact_dyadic_bijection_"
        "and_limit_order_adversarial_audit_finite_certificate_fresh_root_"
        "106_page_PDF_all_page_visual_QA_resource_enforcement_and_"
        "compaction_hardened_recovery_checkpoint"
    ),
    "inputs": [
        "ACT-COL-000031",
        "raw/USR-0001.txt",
        "raw/USR-0002.txt",
        "raw/USR-0003.txt",
        "state/index_routes.jsonl",
        "state/document_routes.jsonl",
        "state/index_snapshot.json",
        "SRC-COL-000005",
        "SRC-COL-000027",
        sources["Tao_v7_TeX"]["path"],
        sources["Tao_v7_eprint"]["path"],
        sources["Tao_v5_TeX"]["path"],
        sources["Tao_v5_eprint"]["path"],
        sources["Tao_journal_PDF"]["path"],
    ],
    "outputs": [record["path"] for record in artifacts.values()] + [
        "tmp/tao_main_reduction_act32_final_20260828/main.pdf",
        "tmp/tao_main_reduction_act32_final_20260828/main.log",
        "tmp/tao_main_reduction_act32_final_20260828/main-layout.txt",
        "tmp/tao_main_reduction_act32_final_20260828/pdffonts.txt",
        "tmp/tao_main_reduction_act32_final_20260828/pdfinfo.txt",
        "tmp/tao_main_reduction_act32_final_20260828/rendered_final_root_200dpi",
        "tmp/tao_main_reduction_act32_final_20260828/contact_sheets_final_root",
    ],
    "result": (
        "pass_working_checkpoint_repaired_Tao_main_theorem_chain_closed_at_"
        "exact_logarithmic_density_scope_post1860_versioned_whole_paper_"
        "formal_corpus_package_and_release_gates_open"
    ),
    "measurements": {
        "controlling_sources": {
            "records": sources,
            "Tao_v7_locators": {
                "logarithmic_law": "159-163",
                "Theorem_1_3": "169-170",
                "Syracuse_setup": "180-193",
                "Theorem_1_6": "199-206",
                "Proposition_1_11": "316-335",
                "main_reduction": "535-593",
            },
            "Tao_v5_locators": {
                "introduction": "159-206",
                "Proposition_1_11": "316-335",
                "main_reduction": "529-587",
            },
            "journal_physical_pages_read": [3, 4, 8, 15, 16, 17],
            "local_whitespace_deleted_v5_v7_reduction_equality": {
                "v5_lines": "529-587",
                "v7_lines": "535-593",
                "normalized_length_each": 4_748,
                "exactly_equal": True,
                "whole_documents_identified": False,
            },
        },
        "source_defects": [
            "reversed_tail_envelope_with_explicit_counterexample",
            "strict_greater_than_drops_equality_from_bad_complement",
            "silent_nonnegative_restriction_of_real_valued_f",
            "dyadic_density_factor_two_and_missing_g_a_rescaling",
            "J_equals_zero_omitted",
            "empty_small_odd_blocks_omitted",
            "finite_passage_false_redundancy_parenthetical",
            "recurrence_exponent_j_minus_2_shift",
        ],
        "mathematical_boundary": {
            "claims": ["CLM-COL-000119", "CLM-COL-000120", "CLM-COL-000121"],
            "morphisms": ["MOR-COL-000030", "MOR-COL-000031"],
            "dependency": "CLM-COL-000118_and_MOR-COL-000029",
            "closed": [
                "repaired_fixed_threshold_Theorem_3_1",
                "repaired_fixed_tail_Theorem_1_6",
                "repaired_dyadic_Theorem_1_3",
            ],
            "indexed_tail_map": "O_u_equals_O_v_composed_with_sigma_d",
            "indexed_shift_fibres": "singletons_on_image",
            "indexed_shift_kernel_pair": "diagonal",
            "orbit_value_injectivity_claimed": False,
            "dyadic_map": "iota_a_of_M_equals_2_power_a_times_M_with_inverse_pi_a",
            "dyadic_fibres": "singletons",
            "dyadic_kernel_pair": "diagonal",
            "dyadic_stratum_density": "2^(-(a+1))",
            "limit_orders": {
                "fixed_tail": "X_to_infinity_at_fixed_K_then_K_to_infinity",
                "dyadic_strata": "X_to_infinity_at_fixed_A_then_A_to_infinity",
            },
            "nonclaims": [
                "natural_density",
                "convergence_to_one",
                "individual_first_passage",
                "universal_orbit_bound",
                "coupling",
                "invariant_logarithmic_measure",
                "periodic_or_unbounded_orbit_exclusion",
                "Collatz_conjecture",
            ],
        },
        "certificate": {
            "path": "certificates/tao_main_reduction_checks.py",
            "status": "PASS",
            "pinned_hashes": 8,
            "route_identity_checks": 3,
            "v7_source_locator_checks": 25,
            "v5_source_locator_checks": 25,
            "reconstruction_locator_checks": 16,
            "normalized_version_checks": 2,
            "nested_indexed_tail_shift_checks": 1_100_000,
            "nested_event_transport_checks": 330_000,
            "geometric_recurrence_error_checks": 1_500,
            "constructive_log_cover_checks": 37_576,
            "dyadic_bijection_and_inverse_checks": 80_000,
            "dyadic_harmonic_weight_checks": 14_400,
            "dyadic_tail_identity_checks": 10_000,
            "collatz_syracuse_minimum_checks": 26_000,
            "fixed_K_tail_inclusion_checks": 27_920,
            "strict_complement_equality_counterexample_checks": 3,
            "printed_tail_envelope_counterexample_checks": 1,
            "explicitly_not_certified": [
                "analytic total-variation estimate",
                "infinite harmonic-density limits",
                "Proposition 1.11 independently of F026",
                "Theorem 3.1",
                "Theorem 1.6",
                "Theorem 1.3",
                "Collatz conjecture",
            ],
        },
        "adversarial_audit": {
            "status": "pass_after_independent_findings_and_root_recheck",
            "forced_repairs": [
                "truncated_nonnegative_dyadic_logarithmic_sum",
                "real_N_0_quantifier",
                "empty_terminal_cover_block",
                "s_at_least_2_harmonic_normalizer_qualifier",
                "deterministic_Collatz_time_recovery_from_odd_states",
                "unambiguous_bijection_language",
                "root_build_provenance_wording",
                "live_01i_hash_propagated_after_boundary_only_update_already_present_in_accepted_PDF",
                "ACT32_checkpoint_and_receipt_v5_SHA256_restored_to_exact_64_character_digest",
            ],
            "first_passage_boundary_update": {
                "f026_checkpoint_bytes": 20_386,
                "f026_checkpoint_sha256": "ec16f1047928073682df1085f055ef5582a756c3b2cd2f3bef3169b6ba138ffd",
                "act32_current_bytes": 20_537,
                "act32_current_sha256": "4757ddcbd1ca4353b51f243c65fd8d0468f7b10700f1a091c881357a24edd647",
                "locator": "tex/chapters/01i_tao_first_passage_stabilisation.tex lines 594-597",
                "proof_changed": False,
                "accepted_106_page_PDF_already_contains_update": True,
            },
        },
        "artifacts": artifacts,
        "records": counts,
        "pdf": {
            "pages": 106,
            "bytes": pdf.stat().st_size,
            "sha256": digest(pdf),
            "log_bytes": log.stat().st_size,
            "log_sha256": digest(log),
            "layout_bytes": layout.stat().st_size,
            "layout_sha256": digest(layout),
            "pdffonts_bytes": fonts.stat().st_size,
            "pdffonts_sha256": digest(fonts),
            "pdfinfo_bytes": info.stat().st_size,
            "pdfinfo_sha256": digest(info),
            "clean_TeX_passes": 3,
            "actionable_log_diagnostics": 0,
            "unresolved_placeholder_hits": 0,
            "literal_control_leak_hits": 0,
            "embedded_subset_font_rows": 25,
            "unembedded_font_rows": 0,
        },
        "root_visual_QA": {
            "rendered_pages": len(rendered),
            "dpi": 200,
            "render_bytes": sum(path.stat().st_size for path in rendered),
            "contact_sheets": len(contacts),
            "contact_sheet_bytes": sum(path.stat().st_size for path in contacts),
            "all_pages_checked": 106,
            "preliminary_and_final_pixel_identical_pages": 104,
            "pixel_identical_page_set": "1-104",
            "final_changed_pages_contact_sheet_checked": [105, 106],
            "final_changed_pages_original_detail": [105, 106],
            "proof_pages_original_detail": [94, 95, 96, 97, 98, 99, 100, 101],
            "additional_original_detail_pages": [2],
            "edge_min_px": {"left": 213, "top": 215, "right": 211, "bottom": 132},
            "issues": 0,
            "independent_current_render_claimed": False,
        },
        "resource_policy_enforcement": {
            "directive": "raw/USR-0003.txt",
            "directive_sha256": "675bc42a44356f579f63f6abd816b9c2cf36701f0d017ffd467eca033d5c7925",
            "worker_limit_bytes": 3_221_225_472,
            "maximum_overlapping_builds": 1,
            "uncapped_builds_forbidden": True,
            "R107_events_recorded_in_project_state": True,
            "unrelated_R11_observation": {
                "pids": [6256, 16360, 43608],
                "lean_worker_private_working_set_bytes": 1_126_707_200,
                "action": "left_untouched_below_cap_no_overlap_started_then_ended",
            },
            "final_audit_utc": "2026-08-28T12:46:29.9462086Z",
            "final_active_Lean_Lake_workers": 0,
            "build_started_by_this_task": False,
        },
        "frozen_routes": frozen,
        "expected_validator_warnings": 8,
        "expected_validator_failures": 0,
    },
    "notes": [
        "The reconstructed main-theorem chain is admitted only at its repaired logarithmic-density scope; all eight source defects and independent repairs remain separately attributed.",
        "The indexed-tail shift records its domain, codomain, image, fibres, and equality kernel; the dyadic morphism additionally records its two-sided inverse and exact harmonic-weight transport. Both retain their information-loss boundaries, and no presentation-level nonidentity inference is used.",
        "The finite certificate checks exact finite kernels and counterexamples and explicitly does not replace the analytic TeX proof or certify the named infinite theorems.",
        "The complete fresh root 106-page render and all fourteen contact sheets were inspected; all changed final pages and the complete new proof received original-detail inspection.",
        "The resource rule was enforced without killing the unrelated compliant R11 worker and without starting an overlapping build; no Lean/Lake process remained at the final audit.",
        "Frozen route artifacts remained byte-identical. No public record was mutated, and quarantined task 019fe2cf-438a-7112-859c-119accee0e9e was neither contacted nor steered.",
        "All eight proof obligations remain open. The next mathematical boundary is Tao v7 after line 1860 plus remaining v5/journal whole-paper reconciliation; Chatnotes and Gemini remain deferred.",
        "The durable goal remains active and this receipt is not a completion or release claim.",
    ],
}

ledger_path = STATE / "action_receipts.jsonl"
ledger = read_jsonl(ledger_path)
assert all(record.get("record_type") == "action_receipt" for record in ledger)
assert all("receipt_id" in record for record in ledger)
existing = [record for record in ledger if record.get("receipt_id") == "ACT-COL-000032"]
if existing:
    assert len(existing) == 1
    assert existing[0] == receipt
    assert ledger[-1]["receipt_id"] == "ACT-COL-000032"
    print(json.dumps({"status": "PASS", "changed": False, "receipt_id": "ACT-COL-000032"}, sort_keys=True))
else:
    assert len(ledger) == 31
    assert ledger[-1]["receipt_id"] == "ACT-COL-000031"
    assert [record["receipt_id"] for record in ledger] == [
        f"ACT-COL-{index:06d}" for index in range(1, 32)
    ]
    with ledger_path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(receipt, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(json.dumps({"status": "PASS", "changed": True, "receipt_id": "ACT-COL-000032"}, sort_keys=True))
