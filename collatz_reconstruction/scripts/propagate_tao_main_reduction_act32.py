"""Idempotently propagate the ACT32 Tao main-reduction checkpoint.

This is a deterministic machine-state migration.  It leaves the frozen route
artifacts byte-identical, keeps PO-COL-000001 open for the remaining
whole-paper/version/release work, and does not launch Lean.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state"
STAMP = "2026-08-28T12:17:17.0296934Z"

PINNED = {
    "state/index_routes.jsonl": "b05028694bf133b9b19f2b0c0a771323b7a47ae872c0712769267aaf1f1eff38",
    "state/document_routes.jsonl": "e439a5f9a70253b00824df5be791415e1c068d574c23f6f7f61851c19a88b2a5",
    "state/index_snapshot.json": "7d5a17440a3cb039f2bfbb4814567b5805117002136cc65687de738ee99af62f",
    "tex/chapters/01j_tao_main_theorem_reduction.tex": "53d97d24d201fe90f97fde3a4e3afbf4e21949f4fa40be559562cc995375cffa",
    "qa/TAO-V5-V7-JOURNAL-F027-main-theorem-reduction-audit.md": "7ab39a57a00e5c753fdd895ec07cab7f3c672a2b479c80b1369db6cd9ae3bd37",
    "certificates/tao_main_reduction_checks.py": "feab839198920b58469694605cc604b128bac78e0d032258e325b3d9b173c795",
}

CERTIFICATE_METRICS = {
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
}

SCRIPT_NONCERTIFICATION = [
    "analytic total-variation estimate in Proposition 1.11",
    "infinite harmonic-density limits",
    "Tao Theorem 3.1",
    "Tao Theorem 1.6",
    "Tao Theorem 1.3",
    "the Collatz conjecture",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def write_jsonl(path: Path, records: list[dict]) -> None:
    rendered = "\n".join(
        json.dumps(record, ensure_ascii=False, separators=(",", ":"))
        for record in records
    ) + "\n"
    path.write_text(rendered, encoding="utf-8")


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def append_unique(values: list, value) -> None:
    if value not in values:
        values.append(value)


def replace_exact(values: list[str], old: str, new: str) -> None:
    if old in values:
        values[values.index(old)] = new
    elif new not in values:
        values.append(new)


def upsert(records: list[dict], key: str, value: str, record: dict) -> None:
    for index, current in enumerate(records):
        if current.get(key) == value:
            records[index] = record
            return
    records.append(record)


def certificate_record() -> dict:
    return {
        "path": "certificates/tao_main_reduction_checks.py",
        "status": "pass_finite_exact_reduction_kernels",
        "bytes": 17_676,
        "sha256": PINNED["certificates/tao_main_reduction_checks.py"],
        "metrics": CERTIFICATE_METRICS,
        "explicitly_not_certified_by_script": SCRIPT_NONCERTIFICATION,
    }


def update_sources() -> None:
    path = STATE / "source_registry.jsonl"
    records = read_jsonl(path)
    by_id = {record.get("source_id"): record for record in records}
    v7 = by_id["SRC-COL-000005"]
    v5 = by_id["SRC-COL-000027"]

    v7_reading = v7["reading"]
    v7_reading["status"] = (
        "v7_lines_143_1860_content_read_Proposition5_2_uniform_cn_fine_scale_"
        "Fourier_black_triangle_first_passage_renewal_Proposition1_14_"
        "Proposition1_9_Proposition1_11_Theorem3_1_Theorem1_6_and_Theorem1_3_"
        "repaired_and_closed_at_declared_scopes_remaining_post1860_versioned_"
        "whole_paper_and_release_gates_open"
    )
    for locator in (
        "source lines 159-206, logarithmic-density definitions and Theorems 1.3 and 1.6",
        "source lines 535-593, Section 3 Proposition 1.11 to Theorem 3.1 to Theorem 1.6 reduction",
        "v5 source lines 529-587, whitespace-identical local reduction comparison",
        "published journal physical pages 3-4, 8, and 15-17, main-theorem manifestation comparison",
        "qa/TAO-V5-V7-JOURNAL-F027-main-theorem-reduction-audit.md",
        "certificates/tao_main_reduction_checks.py",
    ):
        append_unique(v7_reading["locators"], locator)

    for defect in (
        "Lines 591-593 apply the lower tail envelope inf_{N>=x} f(N) to N<=x; the displayed inequality is false, for example for f(1)=0 and f(N)=exp(N) on odd N>=3.",
        "The complement of Syr_min(N)<f(N) is Syr_min(N)>=f(N), whereas the source sums only the strict set Syr_min(N)>f(N), omitting equality.",
        "Line 591 silently restricts the real-valued function f to [0,infinity); the exact repair retains arbitrary real f and discards only a finite prefix.",
        "Line 206 assigns dyadic stratum nu_2(N)=a the factor 2^(-a); its logarithmic density is 2^(-(a+1)), the union through a_0 has density 1-2^(-(a_0+1)), and the odd threshold is g_a(M)=f(2^a M).",
        "Lines 569-580 omit J=0; if the block scale s<=N_0^(1/alpha), the bad block event is exactly empty.",
        "The narrow odd logarithmic blocks may be empty at small scales; probabilistic recurrence is restricted to sufficiently large nonempty blocks and empty cover blocks contribute zero.",
        "The line 552 parenthetical incorrectly calls finite passage redundant for x>=N_0 under the artificial Pass_x=1 convention; the displayed proof retains the finite-passage condition.",
        "The recurrence substitution at lines 569-574 has exact error O((alpha^(j-2) log y)^(-c)), not O((alpha^j log y)^(-c)); the fixed factor alpha^(2c) is explicitly absorbed.",
    ):
        append_unique(v7_reading["source_defects"], defect)

    replace_exact(
        v7_reading["nonclaims"],
        "The repaired fine-scale/Fourier/renewal branch certifies Proposition 1.14, F025 independently proves Proposition 1.9, and F026 closes their exact edge to Proposition 1.11; neither branch nor F026 certifies Theorem 1.6 or Theorem 1.3.",
        "F024, F025, and F026 do not individually certify the main theorem; F027 separately closes the exact Proposition 1.11 to Theorem 3.1 to Theorem 1.6 to Theorem 1.3 reduction under CLM-COL-000119 through CLM-COL-000121.",
    )
    replace_exact(
        v7_reading["nonclaims"],
        "The localized v7 source defects do not by themselves prove Theorem 1.3 false; the named downstream proof gate remains open.",
        "The localized source defects are repaired in the independently authored F027 proof; their presence neither enlarges nor refutes the theorem beyond its exact logarithmic-density scope.",
    )
    replace_exact(
        v7_reading["dependency_boundaries"],
        "Proposition 1.9 is independently closed under CLM-COL-000117 and MOR-COL-000028; the exact edge from Propositions 1.14 and 1.9 to Proposition 1.11 is closed under CLM-COL-000118 and MOR-COL-000029. The current downstream gates are Proposition 1.11 to Theorem 1.6 and Theorem 1.6 to Theorem 1.3.",
        "The exact Proposition 1.11 to Theorem 3.1 to Theorem 1.6 to Theorem 1.3 reduction is closed under CLM-COL-000119 through CLM-COL-000121 and MOR-COL-000030 through MOR-COL-000031. The remaining Tao gates are post-line-1860 content, complete version reconciliation, whole-paper adversarial audit, package validation, final QA, and recovery.",
    )
    v7_reading["main_reduction_certificate"] = certificate_record()
    v7_reading["main_reduction_adversarial_audit"] = {
        "status": "pass_after_independent_adversarial_findings_and_root_recheck",
        "final_tex_path": "tex/chapters/01j_tao_main_theorem_reduction.tex",
        "final_tex_bytes": 19_796,
        "final_tex_sha256": PINNED["tex/chapters/01j_tao_main_theorem_reduction.tex"],
        "audit_record": "qa/TAO-V5-V7-JOURNAL-F027-main-theorem-reduction-audit.md",
        "repairs_forced_by_audit": [
            "truncated nonnegative dyadic logarithmic sum",
            "real N_0 quantifier",
            "empty terminal cover block",
            "s>=2 harmonic-normalizer qualifier",
            "deterministic recovery of Collatz time from odd states",
        ],
    }

    v5_reading = v5["reading"]
    v5_reading["status"] = (
        "targeted_version_comparison_content_read_Proposition1_9_Proposition1_11_"
        "Lemma7_9_and_main_theorem_reduction_with_exact_local_v5_v7_comparison"
    )
    for locator in (
        "v5 source lines 159-206, logarithmic-density definitions and main statements",
        "v5 source lines 529-587, main-theorem reduction",
        "v7 source lines 535-593, exact whitespace-deleted comparison locus",
        "journal physical pages 3-4, 8, and 15-17, published comparison manifestation",
        "qa/TAO-V5-V7-JOURNAL-F027-main-theorem-reduction-audit.md",
        "certificates/tao_main_reduction_checks.py",
    ):
        append_unique(v5_reading["locators"], locator)
    replace_exact(
        v5_reading["dependency_boundaries"],
        "F026 compares the exact Proposition 1.11 loci and closes the v7 edge through an independently authored proof; it does not declare the manifestations text-identical or certify Theorem 1.6 or Theorem 1.3.",
        "F026 compares the exact Proposition 1.11 loci. F027 proves the later main reduction independently, records the exact local whitespace equality of v5 lines 529-587 and v7 lines 535-593, and does not declare the complete manifestations text-identical.",
    )
    replace_exact(
        v5_reading["nonclaims"],
        "This targeted v5 comparison does not itself prove Proposition 1.11 or Tao's main theorem; Proposition 1.9 is independently reconstructed under CLM-COL-000117 and the v7 Proposition 1.11 edge under CLM-COL-000118.",
        "The v5 text is a comparison manifestation, not the proof authority for the repaired theorem; the independently authored chain is CLM-COL-000118 through CLM-COL-000121.",
    )
    v5_reading["main_reduction_version_comparison"] = {
        "v5_lines": "529-587",
        "v7_lines": "535-593",
        "normalization": "delete_all_whitespace",
        "normalized_length_each": 4_748,
        "exactly_equal": True,
        "whole_files_identified": False,
        "audit_record": "qa/TAO-V5-V7-JOURNAL-F027-main-theorem-reduction-audit.md",
    }
    write_jsonl(path, records)


def update_claims() -> None:
    path = STATE / "claims.jsonl"
    records = read_jsonl(path)
    by_id = {record.get("claim_id"): record for record in records}

    clm116 = by_id["CLM-COL-000116"]
    clm116["status"] = "proved_at_v7_branch_scope_main_reduction_closed_separately_under_CLM119_through_CLM121"
    replace_exact(
        clm116["nonclaims"],
        "The Fourier/renewal branch and its finite script do not themselves certify Proposition 1.9 or Proposition 1.11; F025 independently certifies Proposition 1.9, and F026 separately closes its exact use with Proposition 1.14 to obtain Proposition 1.11. Theorem 1.6 and Theorem 1.3 remain behind separate gates.",
        "The Fourier/renewal branch and its finite script do not themselves certify the main theorem; F025, F026, and F027 separately close the valuation, first-passage, and main-reduction edges.",
    )
    clm117 = by_id["CLM-COL-000117"]
    clm117["status"] = "proved_at_Tao_Proposition_1_9_scope_main_reduction_closed_separately_under_CLM118_through_CLM121"
    replace_exact(
        clm117["nonclaims"],
        "It does not certify Theorem 1.6 or Theorem 1.3 and does not upgrade logarithmic density to natural density.",
        "This valuation-law claim alone does not certify Theorem 1.6 or Theorem 1.3; F027 closes those later edges separately and does not upgrade logarithmic density to natural density.",
    )
    clm118 = by_id["CLM-COL-000118"]
    clm118["status"] = "proved_at_Tao_v7_Proposition_1_11_scope_main_reduction_closed_separately_under_CLM119_through_CLM121"
    replace_exact(
        clm118["nonclaims"],
        "Theorem 1.6 and Theorem 1.3 remain behind separate proof-audit gates.",
        "This Proposition 1.11 claim alone does not certify Theorems 1.6 and 1.3; F027 closes those later edges separately under CLM-COL-000119 through CLM-COL-000121.",
    )

    formal = {
        "status": "finite_exact_kernel_pass_analytic_proof_controlled_by_TeX_and_adversarial_audit",
        "artifact": "certificates/tao_main_reduction_checks.py",
        "artifact_bytes": 17_676,
        "artifact_sha256": PINNED["certificates/tao_main_reduction_checks.py"],
        "verified_finite_metrics": CERTIFICATE_METRICS,
        "explicitly_not_certified_by_script": SCRIPT_NONCERTIFICATION,
    }
    common_locators = [
        "Tao arXiv:1909.03562v7 source lines 159-206 and 535-593",
        "Tao arXiv:1909.03562v5 source lines 159-206 and 529-587",
        "published journal physical pages 3-4, 8, and 15-17",
        "qa/TAO-V5-V7-JOURNAL-F027-main-theorem-reduction-audit.md",
    ]

    claim119 = {
        "record_type": "claim",
        "schema_version": "1.0",
        "claim_id": "CLM-COL-000119",
        "claim_type": "independent_exact_block_recurrence_and_fixed_threshold_logarithmic_descent_reconstruction",
        "status": "proved_at_repaired_Tao_Theorem_3_1_scope",
        "statement": "Assume Tao's Proposition 1.11 at alpha=1001/1000. For every real N_0>=2 and X>=2, the harmonic mass below X of odd M with Syr_min(M)>N_0 is O(log X/(log N_0)^c), and the harmonic mass of all N with Col_min(N)>N_0 obeys the same bound. The proof constructs b_(N_0)(s), proves b(s^alpha)>=b(s)-C(log s)^(-c) using the indexed nested-threshold tail inclusion and marginal total variation without a coupling, dispatches J=0 and empty blocks, retains the exact alpha^(j-2) error, and covers [1,X] with z_k=X^(alpha^(-k)) while summing log z_k<=log X/(alpha-1).",
        "source_ids": ["SRC-COL-000005", "SRC-COL-000027"],
        "dependencies": ["CLM-COL-000118"],
        "source_locators": common_locators,
        "proof_locator": {"path": "tex/chapters/01j_tao_main_theorem_reduction.tex", "label": "thm:Tao-main-alt-repaired"},
        "supporting_proof_labels": ["lem:Tao-nested-passage-tail", "prop:Tao-main-block-recurrence"],
        "audit_locator": "qa/TAO-V5-V7-JOURNAL-F027-main-theorem-reduction-audit.md",
        "morphism_refs": ["MOR-COL-000030", "MOR-COL-000031"],
        "formal_status": formal,
        "open_obligation_ids": ["PO-COL-000001"],
        "nonclaims": [
            "The estimate is harmonic/logarithmic, not a natural-density theorem.",
            "The recurrence uses two marginal laws and failure bounds; no coupling is constructed.",
            "It proves no finite first passage for every individual input and no convergence to one.",
            "The finite script checks exact kernels and counterexamples but does not certify the analytic theorem.",
        ],
    }
    claim120 = {
        "record_type": "claim",
        "schema_version": "1.0",
        "claim_id": "CLM-COL-000120",
        "claim_type": "independent_fixed_tail_repair_of_sourced_odd_almost_bounded_orbit_theorem",
        "status": "proved_at_repaired_Tao_Theorem_1_6_scope",
        "statement": "For every real-valued f on the odd positive integers with f(M)->+infinity, Syr_min(M)<f(M) for a set of relative odd logarithmic density one. For each fixed integer K>=2, choose Y_K so that f(M)>K beyond the finite prefix; then {Syr_min>=f} on that tail is contained in {Syr_min>K}. Apply CLM-COL-000119, divide by H_odd(X), send X to infinity at fixed K, and only then send K to infinity. This retains equality in the bad complement, arbitrary nonmonotone real f, and the finite prefix, without a tail envelope.",
        "source_ids": ["SRC-COL-000005", "SRC-COL-000027"],
        "dependencies": ["CLM-COL-000119"],
        "source_locators": common_locators,
        "proof_locator": {"path": "tex/chapters/01j_tao_main_theorem_reduction.tex", "label": "thm:Tao-main-syr-repaired"},
        "audit_locator": "qa/TAO-V5-V7-JOURNAL-F027-main-theorem-reduction-audit.md",
        "formal_status": formal,
        "open_obligation_ids": ["PO-COL-000001"],
        "nonclaims": [
            "No monotonicity or nonnegativity of f is assumed.",
            "The theorem is relative odd logarithmic density one, not natural density.",
            "The limit order X then K is essential and is not interchanged.",
            "No fixed universal bound or convergence-to-one conclusion follows.",
        ],
    }
    claim121 = {
        "record_type": "claim",
        "schema_version": "1.0",
        "claim_id": "CLM-COL-000121",
        "claim_type": "independent_exact_dyadic_transport_and_repair_of_sourced_main_theorem",
        "status": "proved_at_repaired_Tao_Theorem_1_3_scope_remaining_whole_paper_release_gate_open",
        "statement": "For every real-valued f on the positive integers with f(N)->+infinity, Col_min(N)<f(N) for a set of logarithmic density one. On each fixed stratum nu_2(N)=a, the exact bijection M->2^aM transports harmonic weight by 2^(-a), has stratum density 2^(-(a+1)), and satisfies Col_min(2^aM)=Syr_min(M). Applying CLM-COL-000120 to g_a(M)=f(2^aM), taking X->infinity at fixed finite A, and only then A->infinity controls the exact dyadic tail 2^(-(A+1))H(X/2^(A+1)). The fixed-threshold Collatz estimate plus the same fixed-K argument supplies an independent cross-check.",
        "source_ids": ["SRC-COL-000005", "SRC-COL-000027"],
        "dependencies": ["CLM-COL-000119", "CLM-COL-000120"],
        "source_locators": common_locators,
        "proof_locator": {"path": "tex/chapters/01j_tao_main_theorem_reduction.tex", "label": "thm:Tao-main-repaired"},
        "supporting_proof_label": "prop:Tao-main-dyadic-morphism",
        "audit_locator": "qa/TAO-V5-V7-JOURNAL-F027-main-theorem-reduction-audit.md",
        "morphism_refs": ["MOR-COL-000031"],
        "formal_status": formal,
        "open_obligation_ids": ["PO-COL-000001"],
        "nonclaims": [
            "The theorem is logarithmic density one and is not upgraded to natural density.",
            "Almost-bounded descent does not assert convergence to one or exclude divergent or periodic exceptional orbits.",
            "No uniformity in the dyadic stratum index and no interchange of the X and A limits is used.",
            "The main theorem chain is closed at its displayed scope, but the whole-paper/version, formalization, corpus, packaging, and release gates remain open.",
        ],
    }
    upsert(records, "claim_id", "CLM-COL-000119", claim119)
    upsert(records, "claim_id", "CLM-COL-000120", claim120)
    upsert(records, "claim_id", "CLM-COL-000121", claim121)
    records[0]["next_id"] = "CLM-COL-000122"
    write_jsonl(path, records)


def update_morphisms() -> None:
    path = STATE / "morphisms.jsonl"
    records = read_jsonl(path)
    morphism30 = {
        "record_type": "morphism",
        "schema_version": "1.0",
        "morphism_id": "MOR-COL-000030",
        "name": "indexed_nested_first_passage_tail_shift",
        "domain": "Triples (N,u,v) with N odd positive, 1<=u<=v, and finite first-passage time T_u(N), together with the indexed v-tail O_v^N:N->odd positives.",
        "codomain": "The indexed u-tail O_u^N:N->odd positives and the translated index subset d+N, where d=T_u(N)-T_v(N).",
        "formula": "d_(u,v)(N)=T_u(N)-T_v(N), sigma_d(k)=k+d, Pass_u(N)=Syr^d(Pass_v(N)), and O_u^N=O_v^N o sigma_d.",
        "well_definedness": "Every iterate at most u is at most v, so T_v(N)<=T_u(N)<infinity and d is a natural number. The Syracuse semigroup identity then proves both displayed formulas.",
        "preserved_structure": "The complete ordered later orbit tail, every value and its relative order after the exact index translation, threshold-event reachability, and the numerical starting path from Pass_u as a literal sub-tail of the path from Pass_v.",
        "fibres": "sigma_d has singleton fibres over d+N and empty fibres outside its image; its equality kernel is the diagonal on N. No injectivity of the orbit-value function O_v^N is asserted because periodic orbits may repeat values.",
        "inverse_status": "sigma_d is a bijection N->d+N with inverse ell->ell-d on that image; it is not onto all N when d>0. The orbit tail O_v itself need not admit an inverse.",
        "exceptions": [
            "T_u(N)<infinity is part of the domain; the artificial Pass_u=1 branch is not used to infer passage.",
            "The shift depends on N,u,v and is not a single global time conjugacy.",
            "The morphism transports reachability and value sets, not passage-time laws or a coupling.",
        ],
        "claim_refs": ["CLM-COL-000119"],
        "source_refs": ["SRC-COL-000005", "SRC-COL-000027"],
        "proof_locator": {"path": "tex/chapters/01j_tao_main_theorem_reduction.tex", "label": "lem:Tao-nested-passage-tail"},
        "formal_status": {
            "status": "pass_finite_exact_indexed_tail_kernel",
            "artifact": "certificates/tao_main_reduction_checks.py",
            "artifact_sha256": PINNED["certificates/tao_main_reduction_checks.py"],
            "verified_metrics": {
                "nested_indexed_tail_shift_checks": 1_100_000,
                "nested_event_transport_checks": 330_000,
            },
        },
    }
    morphism31 = {
        "record_type": "morphism",
        "schema_version": "1.0",
        "morphism_id": "MOR-COL-000031",
        "name": "odd_coordinate_to_fixed_dyadic_stratum_bijection_and_harmonic_transport",
        "domain": "For fixed a in N, the odd positive integers O=2N+1; globally, the disjoint coordinate union over a of {a}xO.",
        "codomain": "The exact dyadic stratum S_a={N positive:nu_2(N)=a}; globally, all positive integers.",
        "formula": "iota_a(M)=2^aM, pi_a(N)=N/2^a on S_a; globally N maps to (nu_2(N),N/2^nu_2(N)) with inverse (a,M)->2^aM.",
        "well_definedness": "An odd M gives nu_2(2^aM)=a, and N in S_a has odd quotient N/2^a. Direct substitution proves both inverse identities and the unique global factorization.",
        "preserved_structure": "All starting-number information, singleton coordinates, exact cutoffs, harmonic weights sum_(N in iota_a(A),N<=X)1/N=2^(-a)sum_(M in A,M<=X/2^a)1/M, stratum logarithmic density 2^(-(a+1)), and orbit minimum Col_min(2^aM)=Syr_min(M).",
        "fibres": "Every iota_a and pi_a fibre is a singleton; both equality kernels are diagonal. The global coordinate map is bijective and loses no starting-number information.",
        "inverse_status": "iota_a and pi_a are two-sided inverses. The map is not time-preserving; full Collatz time is reconstructed by expanding each Syracuse step with q_j=nu_2(3M_j+1), deterministically computed from its odd source state.",
        "exceptions": [
            "The stratum density is 2^(-(a+1)), not 2^(-a).",
            "For a variable threshold f one must use g_a(M)=f(2^aM).",
            "The global proof takes X->infinity at fixed finite A and only then A->infinity; no uniformity in a is asserted.",
            "Minimum preservation is proved from every explicit Collatz segment and is not inferred from notation.",
        ],
        "claim_refs": ["CLM-COL-000119", "CLM-COL-000121"],
        "source_refs": ["SRC-COL-000005", "SRC-COL-000027"],
        "proof_locator": {"path": "tex/chapters/01j_tao_main_theorem_reduction.tex", "label": "prop:Tao-main-dyadic-morphism"},
        "formal_status": {
            "status": "pass_finite_exact_bijection_weight_tail_and_minimum_kernels",
            "artifact": "certificates/tao_main_reduction_checks.py",
            "artifact_sha256": PINNED["certificates/tao_main_reduction_checks.py"],
            "verified_metrics": {
                "dyadic_bijection_and_inverse_checks": 80_000,
                "dyadic_harmonic_weight_checks": 14_400,
                "dyadic_tail_identity_checks": 10_000,
                "collatz_syracuse_minimum_checks": 26_000,
            },
        },
    }
    upsert(records, "morphism_id", "MOR-COL-000030", morphism30)
    upsert(records, "morphism_id", "MOR-COL-000031", morphism31)
    records[0]["next_id"] = "MOR-COL-000032"
    write_jsonl(path, records)


def update_obligation() -> None:
    path = STATE / "proof_obligations.jsonl"
    records = read_jsonl(path)
    obligation = next(record for record in records if record.get("obligation_id") == "PO-COL-000001")
    obligation["status"] = "in_progress_after_exact_main_theorem_reduction_remaining_post1860_versioned_whole_paper_and_release_gates_open"
    obligation["statement"] = (
        "Complete the remaining whole-paper and versioned proof-dependency certification of Tao arXiv v7. "
        "Source lines 143-1860 and the introduction/main reduction have been content-read. Proposition 5.2, "
        "Propositions 1.14, 1.9, 1.11, the repaired fixed-threshold Theorem 3.1, fixed-tail Theorem 1.6, "
        "and dyadically transported Theorem 1.3 are proved at their declared scopes. Remaining mathematical "
        "content after line 1860, complete v5/journal reconciliation, whole-paper adversarial audit, formal and "
        "certificate coverage, package validation, final visual QA, and release recovery remain open."
    )
    for claim_id in ("CLM-COL-000119", "CLM-COL-000120", "CLM-COL-000121"):
        append_unique(obligation["claim_refs"], claim_id)
    obligation["required_checks"] = [
        "Retain the complete Proposition 1.9, Proposition 1.11, Theorem 3.1, Theorem 1.6, and Theorem 1.3 reconstructions, exact morphisms, manifestation defects, adversarial audits, and finite certificates; do not reopen F025-F027 absent contrary mathematical evidence.",
        "Content-read and classify every remaining mathematical passage after v7 source line 1860 and reconcile every theorem/proof difference with the separately versioned v5 and published manifestations.",
        "Run the whole-paper adversarial audit, deterministic certificates or formal proofs at their honest scopes, clean portable package rebuild, final page-level visual QA, and fresh-context recovery before closing PO-COL-000001.",
        "Preserve all nonclaims: no convergence to one, no fixed absolute bound, no natural-density upgrade, no individual threshold-passage theorem, and no certification of the stronger v5/journal Lemma 7.9.",
    ]
    obligation["closure_rule"] = (
        "Close only after every surviving source defect has exact source and audit locators, all remaining "
        "post-line-1860 and versioned mathematical text is audited, version provenance is explicit, every "
        "consequence is propagated, and deterministic rebuilds, certificates/formal proofs, package validation, "
        "final visual QA, and fresh-context recovery pass. F024 through F027 are closed at their declared scopes."
    )
    for item in (
        "content-read and compared the main reduction in v7 lines 535-593, v5 lines 529-587, and journal physical pages 15-17, with introduction definitions/statements on physical pages 3-4 and Proposition 1.11 on page 8",
        "proved the exact indexed nested-threshold tail shift with translated indices, singleton shift fibres, diagonal equality kernel, and no orbit-value injectivity claim",
        "proved the marginal-law block recurrence, J=0 dispatch, exact alpha^(j-2) error sum, nonempty-block qualifier, and constructive z_k=X^(alpha^(-k)) cover",
        "proved repaired Theorem 3.1 for every real N_0>=2, including the truncated nonnegative dyadic logarithmic sum",
        "replaced the false tail envelope by the fixed-K finite-prefix argument, retaining equality in the bad complement and arbitrary nonmonotone real f, thereby proving repaired Theorem 1.6",
        "proved the dyadic stratum bijection, inverse, singleton fibres, diagonal kernels, exact weights, density 2^(-(a+1)), deterministic Collatz-time expansion, and orbit-minimum identity",
        "proved repaired Theorem 1.3 by fixed finite dyadic strata followed by the exact tail limit, and independently cross-checked it from the fixed-threshold Collatz estimate",
        "passed certificates/tao_main_reduction_checks.py at its finite exact scope and retained every theorem-level analytic noncertification flag",
        "applied all independent adversarial findings, including the real threshold, truncated dyadic sum, empty terminal block, harmonic-scale qualifier, and deterministic time-coordinate repair",
    ):
        append_unique(obligation["completed_checks"], item)
    checkpoint = obligation["local_checkpoint"]
    checkpoint["status"] = "pass_exact_Proposition1_11_Theorem3_1_Theorem1_6_Theorem1_3_reduction_remaining_whole_paper_release_gate_open"
    for claim_id in ("CLM-COL-000119", "CLM-COL-000120", "CLM-COL-000121"):
        append_unique(checkpoint["claim_refs"], claim_id)
    for morphism_id in ("MOR-COL-000030", "MOR-COL-000031"):
        append_unique(checkpoint["morphism_refs"], morphism_id)
    checkpoint["certificates"] = [
        item for item in checkpoint["certificates"]
        if item.get("path") != "certificates/tao_main_reduction_checks.py"
    ]
    checkpoint["certificates"].append({
        "path": "certificates/tao_main_reduction_checks.py",
        "sha256": PINNED["certificates/tao_main_reduction_checks.py"],
        "status": "pass_finite_exact_reduction_kernels",
    })
    append_unique(checkpoint["proof_locators"], "tex/chapters/01j_tao_main_theorem_reduction.tex#thm:Tao-main-alt-repaired")
    append_unique(checkpoint["proof_locators"], "tex/chapters/01j_tao_main_theorem_reduction.tex#thm:Tao-main-syr-repaired")
    append_unique(checkpoint["proof_locators"], "tex/chapters/01j_tao_main_theorem_reduction.tex#thm:Tao-main-repaired")
    checkpoint["source_dependency_limit"] = "arXiv:1909.03562v7 source line 1860 plus exact introduction/main-reduction loci; remaining post-1860 and whole-version audit open"
    checkpoint["full_obligation_closed"] = False
    append_unique(obligation["audit_records"], "qa/TAO-V5-V7-JOURNAL-F027-main-theorem-reduction-audit.md")
    write_jsonl(path, records)


def update_coverage_project_and_todo() -> None:
    coverage_path = STATE / "coverage.json"
    coverage = json.loads(coverage_path.read_text(encoding="utf-8"))
    layers = {layer["layer_id"]: layer for layer in coverage["layers"]}
    layers["LIT"]["status"] = (
        "foundational_spine_in_progress_27_documents_Tao_v7_lines_143_1860_and_"
        "main_reduction_content_read_Proposition5_2_Proposition1_14_Proposition1_9_"
        "Proposition1_11_Theorem3_1_Theorem1_6_and_Theorem1_3_closed_at_declared_"
        "scopes_remaining_post1860_versioned_whole_paper_and_release_gates_open_"
        "Crandall_Conway_chain_closed_underlying_historical_computation_unlocated_"
        "Siegel1929_full_text_pending"
    )
    layers["FORMAL"]["status"] = (
        "finite_generalized_residue_itinerary_lean_kernel_Lagarias_Crandall_"
        "Steuding_Everett_Pillai_fixed_difference_Herschfeld_primitive_root_"
        "continued_fraction_Tao_endpoint_Proposition5_2_Siegel_Tao_coordinate_"
        "Fourier_renewal_Proposition1_9_Proposition1_11_and_main_reduction_finite_"
        "exact_certificates_verified_analytic_and_remaining_obligations_typed_open"
    )
    layers["FORMAL"]["artifacts_verified"] = 16
    write_json(coverage_path, coverage)

    project_path = STATE / "project_state.json"
    project = json.loads(project_path.read_text(encoding="utf-8"))
    project["next_action"] = (
        "Continue PO-COL-000001 by content-reading and classifying Tao v7 mathematical text after line 1860, "
        "then reconcile the remaining v5 and journal manifestations and perform the whole-paper adversarial "
        "audit. The exact Proposition 1.11 to Theorem 3.1 to Theorem 1.6 to Theorem 1.3 reduction is closed "
        "under CLM-COL-000119 through CLM-COL-000121 and MOR-COL-000030 through MOR-COL-000031; preserve "
        "its fixed-K repair, strict complements, real thresholds, exact maps, fibres, weights, limit order, "
        "certificate boundary, and nonclaims. Query the immutable frozen index before consequential ambiguous "
        "dependencies and read content, not routing summaries. Do not enter Chatnotes/Gemini/archived tasks yet, "
        "do not contact the quarantined task, and enforce the single bounded watched Lean-worker rule. Keep all "
        "eight proof obligations and the durable Codex goal active."
    )
    policy = project["resource_policy"]
    policy["last_enforcement_utc"] = STAMP
    policy["last_enforcement_result"] = (
        "stopped_all_observed_uncapped_R107DeficitProgression_trees; later_observed_one_"
        "single_bounded_watched_Coordinates_worker_under_cap_and_left_it_untouched; final_"
        "audit_found_no_active_R107_Lean_Lake_worker; no_build_started_by_this_task"
    )
    policy["enforcement_events"] = [
        {"module": "Coordinates", "action": "stopped_exact_process_tree", "pids": [47260, 24180, 35504, 50292]},
        {"module": "Fibres", "action": "stopped_exact_process_tree", "pids": [50800, 52108, 50296, 46952]},
        {"module": "Complement", "action": "stopped_exact_process_tree", "pids": [32844, 39604, 30832, 40480]},
        {"module": "Transport", "action": "stopped_exact_process_tree", "pids": [34208]},
        {"module": "Exact", "action": "ended_before_second_stop", "pids": [34716]},
        {"module": "Coordinates", "action": "stopped_uncapped_exact_tree", "pids": [8316, 32080, 36992, 34112]},
        {"module": "FullSupport", "action": "stopped_uncapped_exact_tree", "pids": [8316, 56864, 24540, 58352]},
        {"module": "Coordinates", "action": "stopped_uncapped_exact_tree", "pids": [38088, 18848, 35064, 36672]},
        {"module": "DifferenceExact", "action": "stopped_uncapped_exact_tree", "pids": [32360, 22516, 22912, 48388]},
        {"module": "Fibres", "action": "stopped_uncapped_exact_tree", "pids": [18832, 32944, 49288, 36468]},
        {"module": "Complement", "action": "stopped_uncapped_exact_tree", "pids": [38044, 17548, 25260, 12756]},
        {"module": "aggregate_R107DeficitProgression", "action": "stopped_uncapped_exact_tree", "pids": [35876, 55088, 25044]},
        {"module": "Coordinates", "action": "observed_compliant_single_bounded_watched_worker_and_did_not_interfere", "pids": [48548, 2996, 29852, 52756]},
        {"module": "R107DeficitProgression", "action": "final_audit_no_active_Lean_or_Lake_worker", "pids": []},
    ]
    project["updated_utc"] = STAMP
    write_json(project_path, project)

    todo_path = ROOT / "TODO.md"
    todo = todo_path.read_text(encoding="utf-8")
    old = (
        "  - [ ] Recheck Proposition 1.11 to Theorem 1.6 and then Theorem 1.6 to\n"
        "    Theorem 1.3.  Do not change the whole-paper theorem status before those\n"
        "    proof audits, remaining-version comparison, deterministic checks, reader\n"
        "    QA, and fresh recovery all pass."
    )
    new = (
        "  - [x] Recheck Proposition 1.11 through Theorem 3.1 and Theorem 1.6 to\n"
        "    Theorem 1.3: prove the indexed tail shift, exact recurrence and cover,\n"
        "    fixed-K strict-tail repair, dyadic bijection/weights/minimum identity,\n"
        "    limit order, deterministic certificate, adversarial audit, and reader QA.\n"
        "  - [ ] Complete the remaining post-line-1860 content audit, full v5/journal\n"
        "    reconciliation, whole-paper adversarial audit, formal/certificate status,\n"
        "    portable package QA, final all-page QA, and release recovery."
    )
    if old in todo:
        todo = todo.replace(old, new, 1)
    elif new not in todo:
        raise AssertionError("TODO main-reduction checkpoint text not found")
    anchor = (
        "    uniform-`c_n`, Proposition 1.9, Proposition 1.14, or Proposition 1.11\n"
        "    proofs in the TeX and primary sources."
    )
    addition = (
        anchor
        + "\n  - [x] `certificates/tao_main_reduction_checks.py` pins eight source, route,\n"
        "    and reconstruction artifacts; checks 1,100,000 indexed-tail shifts,\n"
        "    330,000 transported reachability events, exact recurrence-error and cover\n"
        "    arithmetic, 80,000 dyadic inverse coordinates, 14,400 harmonic weights,\n"
        "    10,000 exact dyadic tails, 26,000 Collatz/Syracuse minima, 27,920 fixed-K\n"
        "    inclusions, and explicit counterexamples. It does not certify the analytic\n"
        "    total-variation or infinite-density theorems proved in TeX."
    )
    if "`certificates/tao_main_reduction_checks.py`" not in todo:
        if anchor not in todo:
            raise AssertionError("TODO certificate anchor not found")
        todo = todo.replace(anchor, addition, 1)
    todo_path.write_text(todo, encoding="utf-8")


def main() -> int:
    for relative, expected in PINNED.items():
        actual = digest(ROOT / relative)
        assert actual == expected, (relative, expected, actual)
    update_sources()
    update_claims()
    update_morphisms()
    update_obligation()
    update_coverage_project_and_todo()
    for relative in (
        "state/index_routes.jsonl",
        "state/document_routes.jsonl",
        "state/index_snapshot.json",
    ):
        assert digest(ROOT / relative) == PINNED[relative]
    print(json.dumps({
        "status": "PASS",
        "claims_added": ["CLM-COL-000119", "CLM-COL-000120", "CLM-COL-000121"],
        "morphisms_added": ["MOR-COL-000030", "MOR-COL-000031"],
        "proof_obligation_closed": False,
        "frozen_routes_mutated": False,
        "lean_launched": False,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
