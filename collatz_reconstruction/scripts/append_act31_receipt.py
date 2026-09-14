#!/usr/bin/env python3
"""Append the contiguous, idempotent ACT-COL-000031 receipt."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state"
BUILD = ROOT / "tmp" / "tao_prop111_act31_20260828"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def file_record(relative: str) -> dict:
    path = ROOT / relative
    return {"path": relative, "bytes": path.stat().st_size, "sha256": digest(path)}


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


frozen = {
    "index_routes": file_record("state/index_routes.jsonl"),
    "document_routes": file_record("state/document_routes.jsonl"),
    "snapshot": file_record("state/index_snapshot.json"),
}
assert frozen["index_routes"]["bytes"] == 274_170
assert frozen["index_routes"]["sha256"] == "b05028694bf133b9b19f2b0c0a771323b7a47ae872c0712769267aaf1f1eff38"
assert frozen["document_routes"]["bytes"] == 324_776
assert frozen["document_routes"]["sha256"] == "e439a5f9a70253b00824df5be791415e1c068d574c23f6f7f61851c19a88b2a5"
assert frozen["snapshot"]["bytes"] == 799
assert frozen["snapshot"]["sha256"] == "7d5a17440a3cb039f2bfbb4814567b5805117002136cc65687de738ee99af62f"

artifacts = {
    "literature_spine": file_record("tex/chapters/01_literature_spine.tex"),
    "Fourier_renewal_chapter": file_record("tex/chapters/01g_tao_fourier_renewal.tex"),
    "valuation_chapter": file_record("tex/chapters/01h_tao_valuation_law.tex"),
    "first_passage_chapter": file_record("tex/chapters/01i_tao_first_passage_stabilisation.tex"),
    "source_register": file_record("tex/chapters/99_source_register.tex"),
    "F024_audit": file_record("qa/TAO-V5-V7-JOURNAL-F024-fourier-renewal-audit.md"),
    "F025_audit": file_record("qa/TAO-V5-V7-JOURNAL-F025-prop19-valuation-audit.md"),
    "F026_audit": file_record("qa/TAO-V5-V7-JOURNAL-F026-prop111-first-passage-audit.md"),
    "recovery_checkpoint": file_record("qa/RECOVERY-CHECKPOINT-20260828-ACT31.md"),
    "Proposition1_11_certificate": file_record("certificates/tao_prop111_transport_checks.py"),
    "Proposition1_9_certificate": file_record("certificates/tao_prop19_valuation_checks.py"),
    "endpoint_certificate": file_record("certificates/tao_v7_endpoint_buffer_checks.py"),
    "Proposition5_2_certificate": file_record("certificates/tao_v7_prop52_cn_checks.py"),
    "Fourier_renewal_certificate": file_record("certificates/tao_v7_fourier_renewal_checks.py"),
    "source_registry": file_record("state/source_registry.jsonl"),
    "claims": file_record("state/claims.jsonl"),
    "morphisms": file_record("state/morphisms.jsonl"),
    "proof_obligations": file_record("state/proof_obligations.jsonl"),
    "coverage": file_record("state/coverage.json"),
    "project_state": file_record("state/project_state.json"),
    "todo": file_record("TODO.md"),
    "Proposition1_11_propagation_script": file_record("scripts/propagate_prop111_checkpoint.py"),
    "stale_boundary_repair_script": file_record("scripts/repair_act31_stale_boundaries.py"),
    "ACT31_seal_script": file_record("scripts/seal_prop111_act31.py"),
    "ACT31_receipt_script": file_record("scripts/append_act31_receipt.py"),
}

expected_artifacts = {
    "first_passage_chapter": (20_386, "ec16f1047928073682df1085f055ef5582a756c3b2cd2f3bef3169b6ba138ffd"),
    "F026_audit": (15_068, "37334a91b9fee6cbcba5cb8c6d8d368981d1d96b254495af3f3454b8e828e320"),
    "recovery_checkpoint": (12_656, "c5cf784eddc284bb2167e30a5dd757f81958132feb8edb1bee7502010efb0968"),
    "Proposition1_11_certificate": (39_424, "70ca21065cb5af036044617250f5682d90ca223299918a32379feaef0f9dfc31"),
    "source_registry": (95_492, "74e66617393d86ee7d40499cdee2572f34006edb85d997030b8e3bb9305fbdc7"),
    "claims": (128_609, "efc8ad2131f957888591269a272b92d271929911c620abe60aaa938310de0ed4"),
    "morphisms": (49_312, "59c888b138ec2bf035bf9006698bf0b4ba1f861186e0131a6bf7065488166fdc"),
    "proof_obligations": (42_217, "16818e3ff1f9ae6daf0d8fb9652c1d3f45b7c3641a98f59d0ae1924488df096e"),
    "coverage": (6_977, "11afa0af0b5d81683a7cf8ed8a34ffe1b005bd4c5585ae6b06acd0019bc135b4"),
    "project_state": (8_184, "e3dc22d59d90eceb125b668628f14f8b9cbe7a932cf797ce2bdf727e4de516f4"),
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
assert counts == {"sources": 27, "claims": 118, "morphisms": 29, "proof_obligations": 8}

pdf = BUILD / "main.pdf"
log = BUILD / "main.log"
layout = BUILD / "main-layout.txt"
fonts = BUILD / "pdffonts.txt"
info = BUILD / "pdfinfo.txt"
rendered = sorted((BUILD / "rendered_final_root_200dpi").glob("page-*.png"))
contacts = sorted((BUILD / "contact_sheets_final_root").glob("contact-*.png"))

receipt = {
    "record_type": "action_receipt",
    "schema_version": "1.0",
    "receipt_id": "ACT-COL-000031",
    "timestamp_utc": "2026-08-28T09:43:09.2717666Z",
    "action": "tao_v5_v7_journal_Proposition1_11_exact_statement_and_version_boundary_real_endpoint_modular_law_floor_correct_descent_affine_path_endpoint_bijection_integer_window_normalization_uniform_lift_collapse_arbitrary_event_total_variation_two_stage_adversarial_audit_stale_global_gate_repair_complete_certificate_metrics_fresh_99_page_PDF_all_page_visual_QA_resource_policy_enforcement_and_compaction_hardened_recovery_checkpoint",
    "inputs": [
        "ACT-COL-000030",
        "raw/USR-0003.txt",
        "state/index_routes.jsonl",
        "state/document_routes.jsonl",
        "state/index_snapshot.json",
        "SRC-COL-000005",
        "SRC-COL-000027",
        "C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/latex/1909.03562v7/collatz.tex",
        "C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/source/1909.03562v7.eprint",
        "C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/latex/1909.03562v5/collatz.tex",
        "C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/source/1909.03562v5.eprint",
        "C:/Users/LOCAL_USER/Documents/arxiv_latex/library/_recovered_from_papers/by_title/Tao Almost all orbits of the Collatz map attain almost bounded values.pdf",
    ],
    "outputs": [
        "tex/chapters/01_literature_spine.tex",
        "tex/chapters/01g_tao_fourier_renewal.tex",
        "tex/chapters/01h_tao_valuation_law.tex",
        "tex/chapters/01i_tao_first_passage_stabilisation.tex",
        "tex/chapters/99_source_register.tex",
        "qa/TAO-V5-V7-JOURNAL-F024-fourier-renewal-audit.md",
        "qa/TAO-V5-V7-JOURNAL-F025-prop19-valuation-audit.md",
        "qa/TAO-V5-V7-JOURNAL-F026-prop111-first-passage-audit.md",
        "qa/RECOVERY-CHECKPOINT-20260828-ACT31.md",
        "certificates/tao_prop111_transport_checks.py",
        "state/source_registry.jsonl",
        "state/claims.jsonl",
        "state/morphisms.jsonl",
        "state/proof_obligations.jsonl",
        "state/coverage.json",
        "state/project_state.json",
        "TODO.md",
        "scripts/propagate_prop111_checkpoint.py",
        "scripts/repair_act31_stale_boundaries.py",
        "scripts/seal_prop111_act31.py",
        "scripts/append_act31_receipt.py",
        "tmp/tao_prop111_act31_20260828/main.pdf",
        "tmp/tao_prop111_act31_20260828/main.log",
        "tmp/tao_prop111_act31_20260828/main-layout.txt",
        "tmp/tao_prop111_act31_20260828/pdffonts.txt",
        "tmp/tao_prop111_act31_20260828/pdfinfo.txt",
        "tmp/tao_prop111_act31_20260828/rendered_final_root_200dpi",
        "tmp/tao_prop111_act31_20260828/contact_sheets_final_root",
    ],
    "result": "pass_working_checkpoint_Tao_v7_Proposition1_11_closed_at_exact_source_scope_Theorem1_6_Theorem1_3_and_all_global_release_gates_open",
    "measurements": {
        "controlling_sources": {
            "Tao_v7": {
                "source_tex_bytes": 164_932,
                "source_tex_sha256": "bfbc39432d4084a276416cb019a592003c868fa32f18e2f90028ac325ae5c19d",
                "source_archive_bytes": 1_226_861,
                "source_archive_sha256": "ba81acd6254838251f1ee585256a6f9f223cdc9c73bed0a3c4fd25782d0124ad",
                "statement_lines": "316-335",
                "proof_lines": "649-925",
            },
            "Tao_v5": {
                "source_tex_bytes": 163_356,
                "source_tex_sha256": "c676b362b30807aa6690d0d4f16b8c8e84324732f5c0eb72ccfd875000276ae0",
                "source_archive_bytes": 1_226_298,
                "source_archive_sha256": "eb7a4668ebf27a3f795f72fcdc8d992ada365824359c734fa58813c750ff2ede",
                "statement_lines": "316-335",
                "proof_lines": "643-919",
            },
            "journal_pdf": {
                "bytes": 1_008_484,
                "sha256": "55c817c73498f940ed1e70f10208105922f1f7c89e378dcb629040c534151a2b",
                "physical_pages": [7, *range(18, 28)],
                "status": "separate_manifestation_exact_comparison",
            },
        },
        "mathematical_boundary": {
            "claim": "CLM-COL-000118",
            "morphism": "MOR-COL-000029",
            "closed": "Proposition_1.11_first_passage_stabilisation",
            "exact_map": "Theta_(r,y,E,x)_with_two_sided_inverse_Phi_r",
            "fibres": "singletons",
            "kernel_pair": "diagonal",
            "information_loss": "none_on_the_displayed_typed_domain",
            "version_difference": "v5_and_journal_interchange_passage_time_and_location; v7_lines_795_797_correct",
            "downstream_open": ["Proposition_1.11_to_Theorem_1.6", "Theorem_1.6_to_Theorem_1.3"],
            "nonclaims": [
                "natural_density",
                "convergence_to_one",
                "coupling_of_passage_locations",
                "fixed_universal_orbit_bound",
                "exclusion_of_unbounded_or_periodic_orbits",
            ],
        },
        "certificate": {
            "path": "certificates/tao_prop111_transport_checks.py",
            "status": "PASS",
            "pinned_hashes": 8,
            "route_identity_checks": 3,
            "v7_source_locator_checks": 44,
            "v5_source_locator_checks": 44,
            "reconstruction_locator_checks": 13,
            "version_boundary_checks": 5,
            "affine_recurrence_and_offset_checks": 6_820,
            "affine_inverse_congruence_checks": 1_628_712,
            "positive_odd_inverse_and_valuation_checks": 12_276,
            "affine_singleton_checks": 24_522,
            "printed_fixed_M_membership_counterexample_checks": 3,
            "constructive_CRT_checks": 120_444,
            "uniform_lift_projection_checks": 182,
            "ternary_reduction_fibre_checks": 1_086,
            "offset_suffix_projective_checks": 36_408,
            "cn_uniform_lift_weighted_collapse_checks": 72,
            "lift_exponent_factor_checks": 24,
            "cn_valuation_partition_checks": 3_381,
            "truncated_one_coordinate_mass_checks": 66,
            "truncated_tuple_weighted_mass_checks": 60,
            "nonuniform_square_root_majorant_checks": 37,
            "exact_parameter_and_log_range_checks": 128,
            "explicitly_not_certified": [
                "analytic logarithmic progression law",
                "Chernoff and endpoint estimates",
                "uniform analytic c_n bound",
                "first-passage event chain",
                "Proposition 1.9",
                "Proposition 1.14",
                "Proposition 1.11",
                "Theorem 1.6",
                "Theorem 1.3",
            ],
        },
        "prerequisite_certificates": {
            "tao_prop19_valuation_checks.py": "PASS",
            "tao_v7_endpoint_buffer_checks.py": "PASS",
            "tao_v7_prop52_cn_checks.py": "PASS",
            "tao_v7_fourier_renewal_checks.py": "PASS",
        },
        "adversarial_and_state_audit": {
            "first_pass_repairs": ["floor_direction", "raw_control_bytes_and_lost_backslashes"],
            "second_independent_mathematics_reaudit": "PASS_no_substantive_issue",
            "stale_gate_records_repaired": ["CLM-COL-000116", "CLM-COL-000117", "F024", "F025"],
            "nested_artifact_hash_repaired": "SRC-COL-000005.reading.adversarial_audit",
            "complete_certificate_metrics_propagated": True,
        },
        "artifacts": artifacts,
        "records": counts,
        "pdf": {
            "pages": 99,
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
            "all_pages_checked": 99,
            "original_detail_pages": [2, 88, 89, 90, 91, 92, 93, 94, 98, 99],
            "pixel_identical_pages_to_ACT30": 86,
            "pixel_identical_page_set": "1_and_3_through_87",
            "edge_min_px": {"left": 213, "top": 215, "right": 211, "bottom": 132},
            "issues": 0,
        },
        "resource_policy_enforcement": {
            "directive": "raw/USR-0003.txt",
            "directive_sha256": "675bc42a44356f579f63f6abd816b9c2cf36701f0d017ffd467eca033d5c7925",
            "worker_limit_bytes": 3_221_225_472,
            "maximum_overlapping_builds": 1,
            "uncapped_builds_forbidden": True,
            "events": [
                {"module": "Coordinates", "action": "stopped_exact_tree", "pids": [47260, 24180, 35504, 50292]},
                {"module": "Fibres", "action": "stopped_exact_tree", "pids": [50800, 52108, 50296, 46952]},
                {"module": "Complement", "action": "stopped_exact_tree", "pids": [32844, 39604, 30832, 40480]},
                {"module": "Transport", "action": "stopped_exact_tree", "pids": [34208]},
                {"module": "Exact", "action": "ended_before_second_stop", "pids": [34716]},
            ],
            "final_audit_utc": "2026-08-28T09:41:50.6446005Z",
            "final_active_R107_Lean_Lake_trees": 0,
            "restarted_by_this_task": False,
        },
        "frozen_routes": frozen,
        "expected_validator_warnings": 8,
        "expected_validator_failures": 0,
    },
    "notes": [
        "Proposition 1.11 is admitted only at its printed v7 logarithmic first-passage-stabilisation scope; Theorem 1.6 and Theorem 1.3 remain open.",
        "The exact affine path-endpoint morphism has a displayed two-sided inverse, singleton fibres, diagonal kernel pair, and no information loss on its typed domain.",
        "The finite certificate verifies exact algebraic and combinatorial kernels and explicitly does not replace the analytic TeX proof.",
        "A final state audit repaired stale historical gate wording and a nested chapter hash before the receipt; no contradictory current Prop1.11 gate text remains in the audited records.",
        "The complete current 99-page render and all thirteen contact sheets were inspected; the changed proof and terminal pages received original-detail inspection.",
        "Multiple unauthorized uncapped R107DeficitProgression process trees appeared during sealing and were stopped under USR-0003; no such tree remained at the final resource audit, and this task restarted none.",
        "Frozen route artifacts remained byte-identical. No public record was mutated, and quarantined task 019fe2cf-438a-7112-859c-119accee0e9e was neither contacted nor steered.",
        "All eight proof obligations remain open at their recorded boundaries; the durable goal remains active and this is not a completion claim.",
    ],
}

ledger_path = STATE / "action_receipts.jsonl"
ledger = read_jsonl(ledger_path)
existing = [record for record in ledger if record.get("receipt_id") == "ACT-COL-000031"]
if existing:
    assert len(existing) == 1
    assert existing[0] == receipt
    assert ledger[-1]["receipt_id"] == "ACT-COL-000031"
    print(json.dumps({"status": "PASS", "changed": False, "receipt_id": "ACT-COL-000031"}, sort_keys=True))
else:
    assert ledger[-1]["receipt_id"] == "ACT-COL-000030"
    with ledger_path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(receipt, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(json.dumps({"status": "PASS", "changed": True, "receipt_id": "ACT-COL-000031"}, sort_keys=True))
