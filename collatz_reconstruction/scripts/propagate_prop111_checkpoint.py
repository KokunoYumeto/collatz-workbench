"""Idempotently propagate the admitted Proposition 1.11 checkpoint.

This is a mechanical state migration.  It does not alter the frozen route
artifacts and it does not close the downstream Theorem 1.6/1.3 obligation.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state"


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def write_jsonl(path: Path, records: list[dict]) -> None:
    text = "\n".join(
        json.dumps(record, ensure_ascii=False, separators=(",", ":"))
        for record in records
    ) + "\n"
    path.write_text(text, encoding="utf-8")


def append_unique(values: list, value) -> None:
    if value not in values:
        values.append(value)


def replace_exact(values: list[str], old: str, new: str) -> None:
    if old in values:
        values[values.index(old)] = new
    elif new not in values:
        values.append(new)


def update_sources() -> None:
    path = STATE / "source_registry.jsonl"
    records = read_jsonl(path)
    by_id = {record.get("source_id"): record for record in records}
    v7 = by_id["SRC-COL-000005"]
    v5 = by_id["SRC-COL-000027"]

    v7["reading"]["status"] = (
        "v7_lines_143_1860_content_read_Proposition5_2_uniform_cn_"
        "fine_scale_Fourier_black_triangle_first_passage_renewal_"
        "Proposition1_14_Proposition1_9_and_Proposition1_11_repaired_"
        "and_certified_at_declared_scopes_Theorem1_6_Theorem1_3_and_"
        "remaining_whole_paper_gate_open"
    )
    for locator in (
        "source lines 316-335, Proposition 1.11 statement",
        "source lines 649-925, exact Proposition 1.14 plus Proposition 1.9 deduction to Proposition 1.11",
        "v5 source lines 643-919 and journal physical pages 18-27, exact Proposition 1.11 comparison",
        "qa/TAO-V5-V7-JOURNAL-F026-prop111-first-passage-audit.md",
        "certificates/tao_prop111_transport_checks.py",
    ):
        append_unique(v7["reading"]["locators"], locator)

    replace_exact(
        v7["reading"]["nonclaims"],
        "The repaired fine-scale/Fourier/renewal branch certifies Proposition 1.14 at its printed uniform scope but does not itself certify Proposition 1.9; F025 independently proves Proposition 1.9, while Proposition 1.11, Theorem 1.6, and Theorem 1.3 remain open.",
        "The repaired fine-scale/Fourier/renewal branch certifies Proposition 1.14, F025 independently proves Proposition 1.9, and F026 closes their exact edge to Proposition 1.11; neither branch nor F026 certifies Theorem 1.6 or Theorem 1.3.",
    )
    replace_exact(
        v7["reading"]["dependency_boundaries"],
        "Proposition 1.9 is independently closed under CLM-COL-000117 and MOR-COL-000028. The current downstream gate is the exact use of Proposition 1.14 plus Proposition 1.9 to prove Proposition 1.11, followed by Theorem 1.6 and Theorem 1.3.",
        "Proposition 1.9 is independently closed under CLM-COL-000117 and MOR-COL-000028; the exact edge from Propositions 1.14 and 1.9 to Proposition 1.11 is closed under CLM-COL-000118 and MOR-COL-000029. The current downstream gates are Proposition 1.11 to Theorem 1.6 and Theorem 1.6 to Theorem 1.3.",
    )
    v7["reading"]["first_passage_certificate"] = {
        "path": "certificates/tao_prop111_transport_checks.py",
        "status": "pass_finite_exact_integration_kernel",
        "bytes": 39424,
        "sha256": "70ca21065cb5af036044617250f5682d90ca223299918a32379feaef0f9dfc31",
        "metrics": {
            "pinned_hashes": 8,
            "route_identity_checks": 3,
            "v7_source_locator_checks": 44,
            "v5_source_locator_checks": 44,
            "reconstruction_locator_checks": 13,
            "affine_recurrence_and_offset_checks": 6820,
            "affine_inverse_congruence_checks": 1628712,
            "positive_odd_inverse_and_valuation_checks": 12276,
            "affine_singleton_checks": 24522,
            "constructive_CRT_checks": 120444,
            "uniform_lift_projection_checks": 182,
            "ternary_reduction_fibre_checks": 1086,
            "offset_suffix_projective_checks": 36408,
            "cn_uniform_lift_weighted_collapse_checks": 72,
            "cn_valuation_partition_checks": 3381,
            "exact_parameter_and_log_range_checks": 128,
        },
        "noncertified_by_finite_script": [
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
    }
    v7["reading"]["first_passage_adversarial_audit"] = {
        "status": "pass_after_first_pass_floor_and_TeX_repairs_then_second_independent_reaudit",
        "final_tex_path": "tex/chapters/01i_tao_first_passage_stabilisation.tex",
        "final_tex_bytes": 20386,
        "final_tex_sha256": "ec16f1047928073682df1085f055ef5582a756c3b2cd2f3bef3169b6ba138ffd",
        "audit_record": "qa/TAO-V5-V7-JOURNAL-F026-prop111-first-passage-audit.md",
    }

    v5["reading"]["status"] = (
        "targeted_version_comparison_content_read_Proposition1_9_"
        "Proposition1_11_and_Lemma7_9_dependent_induction_boundaries"
    )
    for locator in (
        "v5 source lines 643-919, Proposition 1.11 deduction",
        "journal physical pages 7 and 18-27, Proposition 1.11 statement and deduction comparison",
        "qa/TAO-V5-V7-JOURNAL-F026-prop111-first-passage-audit.md",
        "certificates/tao_prop111_transport_checks.py",
    ):
        append_unique(v5["reading"]["locators"], locator)
    v5["reading"]["proposition_1_11_version_difference"] = {
        "v5_and_journal": "the converse implication interchanges passage location and passage time",
        "v7": "lines 795-797 give the typed time identity followed by the location identity",
        "status": "substantive_local_typing_correction_used_by_the_edition",
    }
    append_unique(
        v5["reading"]["dependency_boundaries"],
        "F026 compares the exact Proposition 1.11 loci and closes the v7 edge through an independently authored proof; it does not declare the manifestations text-identical or certify Theorem 1.6 or Theorem 1.3.",
    )
    replace_exact(
        v5["reading"]["nonclaims"],
        "This targeted v5 comparison does not itself prove Proposition 1.11 or Tao's main theorem; Proposition 1.9 is independently reconstructed under CLM-COL-000117.",
        "This targeted v5 comparison does not itself prove Proposition 1.11 or Tao's main theorem; Proposition 1.9 is independently reconstructed under CLM-COL-000117 and the v7 Proposition 1.11 edge under CLM-COL-000118.",
    )
    v5["reading"]["proposition_1_11_manifestation_defects"] = [
        "passage-time/location interchange in the converse implication",
        "Pass_x printed where T_x is the estimated time and malformed logarithmic numerator",
        "undefined n in the 1.9n_0 descent threshold",
        "invalid additive endpoint deletion",
        "unsigned asymptotic lower bound",
        "n-m in place of n-m_0 and fixed-M membership in place of equality",
        "previous-iterate coefficient, progression estimate, c_n majorant, and probability-space defects shared with the v7 comparison locus",
    ]

    write_jsonl(path, records)


def update_obligation() -> None:
    path = STATE / "proof_obligations.jsonl"
    records = read_jsonl(path)
    obligation = next(
        record for record in records if record.get("obligation_id") == "PO-COL-000001"
    )
    obligation["status"] = (
        "in_progress_after_v7_Proposition1_11_checkpoint_Theorem1_6_"
        "Theorem1_3_remaining_source_version_and_release_gates_open"
    )
    obligation["statement"] = (
        "Complete an independent proof-dependency certification of Tao arXiv v7. "
        "Source lines 143-1860 have been content-read. Proposition 5.2, the endpoint/event chain, "
        "uniform c_n, the exact Fourier-to-mixing map, black-triangle geometry, holding law, "
        "first-passage Green bounds, the weaker v7 Lemma 7.9, the parameterized large-triangle "
        "estimate, renewal monotonicity, Proposition 1.14, Proposition 1.9, and their exact edge "
        "to Proposition 1.11 are repaired and proved at their declared scopes. The separate "
        "Proposition 1.11 to Theorem 1.6 and Theorem 1.6 to Theorem 1.3 deductions, remaining "
        "source/version text, whole-paper adversarial audit, and release gates remain open."
    )
    append_unique(obligation["claim_refs"], "CLM-COL-000118")
    obligation["required_checks"] = [
        "Retain the complete Proposition 1.9 and Proposition 1.11 reconstructions, exact residue spaces, affine maps, fibres, inverse statuses, endpoint dispatches, manifestation defects, adversarial audits, and finite certificates; do not reopen F025 or F026 absent contrary mathematical evidence.",
        "Recheck the complete Proposition 1.11 to Theorem 1.6 and Theorem 1.6 to Theorem 1.3 dependency chain without replacing logarithmic density by natural density or endpoint descent by convergence to one.",
        "Content-read and classify any remaining mathematical text after source line 1860 and reconcile every theorem/proof difference with the separately versioned v5 and published manifestations.",
        "Run the whole-paper adversarial audit, deterministic certificates or formal proofs at their honest scopes, clean rebuild, page-level visual QA, package validation, and fresh-context recovery before closing PO-COL-000001.",
        "Preserve all nonclaims: no convergence to one, no fixed absolute bound, no natural-density upgrade, and no certification of the stronger v5/journal Lemma 7.9.",
    ]
    obligation["closure_rule"] = (
        "Close only after every surviving source defect has exact source and audit locators, the "
        "downstream Proposition 1.11 to Theorem 1.6 and Theorem 1.6 to Theorem 1.3 chain and "
        "remaining source/version text are audited, version provenance is explicit, all "
        "consequences are propagated, and deterministic rebuilds, certificates, package "
        "validation, final visual QA, and fresh-context recovery pass. The F024, F025, and F026 "
        "branches are closed at their declared scopes and must not be reopened absent contrary evidence."
    )
    for item in (
        "content-read and compared Proposition 1.11 in v7 lines 316-335 and 649-925, v5 lines 316-335 and 643-919, and journal physical pages 7 and 18-27",
        "proved the exact real-endpoint odd-residue modular estimate with target mass 2/q and applied Proposition 1.9 at n=n_0, n'=3n_0, c_0=1",
        "proved the floor-correct finite descent exponents beta_1<0.972 and beta_2<0.159 by exact rational logarithm enclosures",
        "constructed the localized affine inverse Phi_r, exact path-endpoint bijection Theta, singleton fibres, diagonal kernel pair, positivity, parity, range, and point mass",
        "proved the exact integer-window count including epsilon in (-1,1], the y-dependent finite correction, and the y-independent leading normalization",
        "combined the repaired event chain and uniform c_n bound with Proposition 1.14's uniform lift and proved the exact finite collapse to Z_E and arbitrary-event-to-unhalved-TV conversion",
        "passed the two-stage Proposition 1.11 adversarial audit after repairing a floor-direction error and TeX corruption in the draft",
        "passed certificates/tao_prop111_transport_checks.py at its finite exact integration-kernel scope with explicit analytic noncertification boundaries",
    ):
        append_unique(obligation["completed_checks"], item)

    obligation["local_checkpoint"] = {
        "status": "pass_v7_Proposition1_14_Proposition1_9_and_exact_Proposition1_11_edge_downstream_Theorem1_6_gate_open",
        "claim_refs": [
            "CLM-COL-000111",
            "CLM-COL-000113",
            "CLM-COL-000114",
            "CLM-COL-000115",
            "CLM-COL-000116",
            "CLM-COL-000117",
            "CLM-COL-000118",
        ],
        "morphism_refs": [
            "MOR-COL-000026",
            "MOR-COL-000027",
            "MOR-COL-000028",
            "MOR-COL-000029",
        ],
        "certificates": [
            *[
                certificate
                for certificate in obligation["local_checkpoint"]["certificates"]
                if certificate.get("path")
                != "certificates/tao_prop111_transport_checks.py"
            ],
            {
                "path": "certificates/tao_prop111_transport_checks.py",
                "sha256": "70ca21065cb5af036044617250f5682d90ca223299918a32379feaef0f9dfc31",
                "status": "pass_finite_exact_integration_kernel",
            },
        ],
        "proof_locators": [
            *[
                locator
                for locator in obligation["local_checkpoint"]["proof_locators"]
                if locator
                != "tex/chapters/01i_tao_first_passage_stabilisation.tex#thm:Tao-v7-Prop111-first-passage"
            ],
            "tex/chapters/01i_tao_first_passage_stabilisation.tex#thm:Tao-v7-Prop111-first-passage",
        ],
        "source_dependency_limit": (
            "arXiv:1909.03562v7 source line 1860; Proposition 1.11 is closed at its source scope "
            "and the exact Proposition 1.11 to Theorem 1.6 edge remains open"
        ),
        "full_obligation_closed": False,
    }
    append_unique(
        obligation["audit_records"],
        "qa/TAO-V5-V7-JOURNAL-F026-prop111-first-passage-audit.md",
    )
    write_jsonl(path, records)


def update_coverage_and_project() -> None:
    coverage_path = STATE / "coverage.json"
    coverage = json.loads(coverage_path.read_text(encoding="utf-8"))
    layers = {layer["layer_id"]: layer for layer in coverage["layers"]}
    layers["LIT"]["status"] = (
        "foundational_spine_in_progress_27_documents_Tao_v7_lines_143_1860_"
        "content_read_Proposition5_2_uniform_cn_fine_scale_Fourier_black_"
        "triangle_first_passage_renewal_Proposition1_14_Proposition1_9_and_"
        "Proposition1_11_closed_at_declared_scopes_Theorem1_6_Theorem1_3_"
        "remaining_source_and_release_gates_open_Crandall_Conway_chain_closed_"
        "underlying_historical_computation_unlocated_Siegel1929_full_text_pending"
    )
    layers["FORMAL"]["status"] = (
        "finite_generalized_residue_itinerary_lean_kernel_Lagarias_Crandall_"
        "Steuding_Everett_Pillai_fixed_difference_Herschfeld_primitive_root_"
        "continued_fraction_Tao_v7_endpoint_Tao_Proposition5_2_uniform_cn_"
        "Siegel_Tao_coordinate_Tao_v7_Fourier_renewal_Tao_Proposition1_9_and_"
        "Tao_Proposition1_11_finite_exact_certificates_verified_analytic_and_"
        "remaining_obligations_typed_open"
    )
    layers["FORMAL"]["artifacts_verified"] = 15
    coverage_path.write_text(
        json.dumps(coverage, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    project_path = STATE / "project_state.json"
    project = json.loads(project_path.read_text(encoding="utf-8"))
    project["next_action"] = (
        "Continue PO-COL-000001 at the exact Proposition 1.11 to Theorem 1.6 "
        "edge in Tao arXiv:1909.03562v7, then Theorem 1.6 to Theorem 1.3, with "
        "the version-pinned v5 and journal manifestations retained as separate "
        "comparison witnesses. Proposition 1.14, Proposition 1.9, and their exact "
        "edge to Proposition 1.11 are closed under CLM-COL-000114 through "
        "CLM-COL-000118 and MOR-COL-000026 through MOR-COL-000029. Preserve the "
        "F026 modular law, floor-directed descent bounds, affine inverse/bijection, "
        "integer-window count, uniform-lift collapse, certificate scope, adversarial "
        "repairs, and every nonclaim. Query the immutable frozen index before every "
        "consequential ambiguous or external-dependency step; read actual source "
        "content rather than route summaries; propagate every consequence globally "
        "before reliance. Do not enter Chatnotes/Gemini/archived tasks yet, do not "
        "contact the quarantined task, do not restart an uncapped R107DeficitProgression "
        "Lean build, and keep all eight proof obligations and the durable Codex goal active."
    )
    project["updated_utc"] = "2026-08-28T09:20:23.8884283Z"
    project_path.write_text(
        json.dumps(project, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> int:
    update_sources()
    update_obligation()
    update_coverage_and_project()
    print(
        json.dumps(
            {
                "status": "PASS",
                "updated": [
                    "state/source_registry.jsonl",
                    "state/proof_obligations.jsonl",
                    "state/coverage.json",
                    "state/project_state.json",
                ],
                "frozen_routes_mutated": False,
                "downstream_theorems_closed": False,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
