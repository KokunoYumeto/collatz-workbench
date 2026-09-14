"""Admit the audited Krasikov--Lagarias 2003 source and exact crosswalk."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHELF = Path(r"C:\Users\LOCAL_USER\Documents\arxiv_latex\library\collatz_reconstruction")
NOW = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

EXPECTED = {
    ROOT / "qa" / "KRASIKOV-LAGARIAS-2003-F029-difference-inequality-audit.md": (
        18_261,
        "7bc00b095f99f55ae94f226a5b865223ecc2de030501536e1d26d2f71f01d187",
    ),
    ROOT / "certificates" / "krasikov_lagarias_2003_checks.py": (
        9_441,
        "3f4ccc7256f026fa65ce7660b47823969c6c605e2a4c45da5b4b6d48961315fa",
    ),
    SHELF / "latex" / "math.0205002v1" / "30apr02.tex": (
        69_729,
        "04fa4d484fe89256f6771f5651338891219385f6e049ffaf41035541016232cd",
    ),
    SHELF / "source" / "math.0205002v1.eprint": (
        26_236,
        "c35de018067ae838c17b647f0ce0354141a8bcfaa45b4966be2bb9a380252951",
    ),
    SHELF / "published" / "Krasikov-Lagarias-2003-Bounds-difference-inequalities.pdf": (
        217_588,
        "8433f68c6f04a008b7c1af4d2b11ee1007a74f987da56a658d8fa331b32eff9c",
    ),
    ROOT / "state" / "index_routes.jsonl": (
        274_170,
        "b05028694bf133b9b19f2b0c0a771323b7a47ae872c0712769267aaf1f1eff38",
    ),
    ROOT / "state" / "document_routes.jsonl": (
        324_776,
        "e439a5f9a70253b00824df5be791415e1c068d574c23f6f7f61851c19a88b2a5",
    ),
    ROOT / "state" / "index_snapshot.json": (
        799,
        "7d5a17440a3cb039f2bfbb4814567b5805117002136cc65687de738ee99af62f",
    ),
}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


for pinned_path, (pinned_bytes, pinned_hash) in EXPECTED.items():
    assert pinned_path.stat().st_size == pinned_bytes, pinned_path
    assert digest(pinned_path) == pinned_hash, pinned_path


def read_jsonl(name: str) -> list[dict]:
    return [
        json.loads(line)
        for line in (ROOT / name).read_text(encoding="utf-8").splitlines()
        if line
    ]


def write_jsonl(name: str, rows: list[dict]) -> None:
    data = "\n".join(
        json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in rows
    )
    (ROOT / name).write_text(data + "\n", encoding="utf-8")


def add_unique(values: list, *new_values) -> None:
    for value in new_values:
        if value not in values:
            values.append(value)


source_rows = read_jsonl("state/source_registry.jsonl")
claim_rows = read_jsonl("state/claims.jsonl")
morphism_rows = read_jsonl("state/morphisms.jsonl")
obligation_rows = read_jsonl("state/proof_obligations.jsonl")

assert source_rows[0]["next_id"] == "SRC-COL-000028"
assert claim_rows[0]["next_id"] == "CLM-COL-000123"
assert morphism_rows[0]["next_id"] == "MOR-COL-000032"
assert not any(row.get("source_id") == "SRC-COL-000028" for row in source_rows)
assert not any(
    row.get("claim_id")
    in {
        "CLM-COL-000123",
        "CLM-COL-000124",
        "CLM-COL-000125",
        "CLM-COL-000126",
    }
    for row in claim_rows
)
assert not any(row.get("morphism_id") == "MOR-COL-000032" for row in morphism_rows)

source_rows[0]["next_id"] = "SRC-COL-000029"
source_rows.append(
    {
        "record_type": "source_document",
        "schema_version": "1.0",
        "source_id": "SRC-COL-000028",
        "authors": ["Ilia Krasikov", "Jeffrey C. Lagarias"],
        "title": "Bounds for the 3x+1 problem using difference inequalities",
        "bibliographic_identity": {
            "journal": "Acta Arithmetica",
            "volume": "109",
            "issue": "3",
            "pages": "237-258",
            "publication_year": 2003,
            "doi": "10.4064/aa109-3-4",
            "received": "2002-05-07",
            "revised": "2002-09-12",
            "arxiv_version_id": "math/0205002v1",
            "arxiv_submitted": "2002-04-30",
        },
        "manifestations": [
            {
                "path": (SHELF / "published" / "Krasikov-Lagarias-2003-Bounds-difference-inequalities.pdf").as_posix(),
                "role": "controlling_published_IMPAN_article_PDF",
                "bytes": 217588,
                "pdf_pages": 22,
                "sha256": "8433f68c6f04a008b7c1af4d2b11ee1007a74f987da56a658d8fa331b32eff9c",
            },
            {
                "path": (SHELF / "source" / "math.0205002v1.eprint").as_posix(),
                "role": "version_pinned_arxiv_v1_source_archive",
                "bytes": 26236,
                "sha256": "c35de018067ae838c17b647f0ce0354141a8bcfaa45b4966be2bb9a380252951",
            },
            {
                "path": (SHELF / "latex" / "math.0205002v1" / "30apr02.tex").as_posix(),
                "role": "safely_extracted_arxiv_v1_source_TeX_comparison_manifestation",
                "bytes": 69729,
                "source_lines": 1900,
                "sha256": "04fa4d484fe89256f6771f5651338891219385f6e049ffaf41035541016232cd",
            },
        ],
        "route_ids": [],
        "route_integrity": {
            "status": "exact_title_author_and_citation_key_miss_in_both_frozen_route_ledgers_then_targeted_primary_source_acquisition",
            "queried": ["state/index_routes.jsonl", "state/document_routes.jsonl"],
            "frozen_ledgers_mutated": False,
            "acquisition_script": "scripts/acquire_arxiv_sources.py",
            "acquisition_note": "Legacy arXiv identifier support was added without restarting or rebuilding the frozen index.",
        },
        "reading": {
            "status": "complete_published_22_page_and_complete_arxiv_source_content_read_proof_chain_defects_computation_boundary_clock_and_Tao_crosswalk_typed",
            "locators": [
                "published pp. 237-239 and source lines 178-424: identity, map, pi_a, pi_a_star, phi, P1-P3, residue reduction, and two printed definition/index defects",
                "published pp. 239-242 and source lines 426-637: Proposition 2.1, D1-D3, L_k^NT(lambda), principal/auxiliary coordinates, and Theorem 2.2",
                "published pp. 242-248 and source lines 668-1069: advanced-variable back-substitution, rooted-tree coordinates, Theorems 3.1-3.2, termination sign defect, and solution preservation",
                "published pp. 248-251 and source lines 1072-1322: tree linear programs and Theorem 4.1 feasibility transport",
                "published pp. 251-254 and source lines 1325-1529: Theorem 5.1 retarded-time induction, Theorem 2.2 deduction, proof-text index defects, and Theorem 6.1",
                "published pp. 254-258 and source lines 1533-1900: rounded computation table, open optimality questions, k=2 appendix, and bibliography",
                "qa/KRASIKOV-LAGARIAS-2003-F029-difference-inequality-audit.md",
                "tex/chapters/01_literature_spine.tex labels prop:KL-Tao-clock-embedding, thm:KL-2003-predecessor-bound, prop:KL-target-handoff, and sourceissue:KL-2003-defects",
            ],
            "visual_checks": [
                "all 22 published pages content-read",
                "published pp. 239, 245, 252, 253, and 254 rendered at 220 dpi and inspected at original detail",
            ],
            "source_objects": {
                "map": "T(n)=n/2 for even n and (3n+1)/2 for odd n on positive integers",
                "counts": ["pi_a(x)", "pi_a_star(x)"],
                "auxiliary_functions": "phi_k^m(y) indexed by residue classes modulo 3^k and noncyclic targets",
                "inequality_system": "I_k with D1-D3 and three-lift minima",
                "linear_program": "L_k^NT(lambda) with principal c_k^m, auxiliary c_(k-1)^m, and C_k^max",
                "proof_chain": [
                    "Theorem 3.1",
                    "Theorem 3.2",
                    "Theorem 4.1",
                    "Theorem 5.1",
                    "Theorem 2.2",
                    "Theorem 6.1",
                ],
            },
        },
        "source_defects": [
            "Published p. 239 defines phi_k^m with an unbound modulus exponent j; the declared class, well-definedness sentence, and P3 force 3^k.",
            "Published p. 239 applies a congruence modulo 3 to real time y; equation (2.1) and [3^k] force the residue variable m.",
            "Published p. 245 prints delta=beta_2-beta_1>0 after beta_1>beta_2>...; termination requires delta<0.",
            "Published p. 253 closes the Theorem 5.1 induction with k in [3^m], where m in [3^k] is forced.",
            "Published p. 253 equation (5.7) prints c_m^k where the principal coordinate is c_k^m.",
            "Published p. 254 omits a closing parenthesis in T^(j).",
            "ArXiv source lines 532-534 use 3^k rather than 3^(k-1) in the L4 lifts; the journal corrects them and the source itself uses 3^(k-1) in the following minimum.",
            "ArXiv source line 1376 ends the initial interval at a tree-vertex macro rather than nu; the journal corrects it.",
        ],
        "dependency_boundaries": [
            "The published proof routes I_k through finite advanced-term elimination, preservation of positive nondecreasing solutions, feasibility transport at fixed lambda and principal coordinates, and retarded-time induction.",
            "Theorem 6.1 reports a computer-found positive feasible k=11 point at lambda=1.7922310; the paper prints no k=11 vector, code, or exact feasibility certificate.",
            "The exact integer comparison 1792231^25>2^21*10^150 certifies only log_2(1.7922310)>21/25, not feasibility.",
            "The definition of phi excludes cyclic targets; the edition supplies the exact b=2^r a cycle-target handoff without assuming or classifying unknown cycles.",
            "MOR-COL-000032 proves the exact variable-time embedding into Tao's unshortened map, including image, fibres, kernel, omitted states, and target-one preservation.",
        ],
        "certificate": {
            "path": "certificates/krasikov_lagarias_2003_checks.py",
            "status": "pass_finite_exact_source_exponent_clock_and_target_kernel_scope",
            "bytes": 9441,
            "sha256": "3f4ccc7256f026fa65ce7660b47823969c6c605e2a4c45da5b4b6d48961315fa",
            "metrics": {
                "pinned_artifacts": 7,
                "source_lines": 1900,
                "source_signature_checks": 40,
                "published_pdf_pages": 22,
                "clock_embedding_checks": 2010000,
                "omitted_intermediate_checks": 1005735,
                "bounded_target_one_equivalence_checks": 10000,
                "cycle_target_lift_checks": 40,
            },
            "explicitly_not_certified": [
                "the unprinted k=11 feasible coordinate vector",
                "feasibility of L_11^NT(1.7922310)",
                "Theorem 2.2 or Theorem 6.1 independently of publication",
                "any infinite-density theorem",
                "the Collatz conjecture",
            ],
        },
        "nonclaims": [
            "The exponent 0.84 does not imply positive density or density one.",
            "No target-uniform threshold is proved.",
            "Targets divisible by 3 are outside Theorem 6.1.",
            "The table does not prove exponent 0.8417560 as a theorem or certify an exact optimum.",
            "Strict growth of lambda_k, convergence lambda_k to 2, supremum attainment, and method optimality remain unproved.",
            "The source theorem does not prove the Collatz conjecture.",
        ],
    }
)

tao = next(row for row in source_rows if row.get("source_id") == "SRC-COL-000005")
inventory = tao["reading"]["citation_inventory"]
add_unique(
    tao["reading"]["locators"],
    "Krasikov-Lagarias 2003 complete published article and arXiv v1 source intake, qa/KRASIKOV-LAGARIAS-2003-F029-difference-inequality-audit.md",
    "tex/chapters/01_literature_spine.tex Proposition prop:KL-Tao-clock-embedding and exact set identity eq:KL-Tao-count-identity",
)
add_unique(inventory["already_content_read_keys"], "kl")
inventory["cited_but_not_in_source_registry_keys"] = [
    key for key in inventory["cited_but_not_in_source_registry_keys"] if key != "kl"
]
inventory["priority"] = [key for key in inventory["priority"] if key != "kl"]
inventory.setdefault("crosswalks", []).append(
    {
        "citation_key": "kl",
        "source_id": "SRC-COL-000028",
        "status": "complete_content_read_and_exact_clock_transport_proved",
        "audit": "qa/KRASIKOV-LAGARIAS-2003-F029-difference-inequality-audit.md",
        "source_theorem_claim": "CLM-COL-000123",
        "morphism": "MOR-COL-000032",
        "transported_claim": "CLM-COL-000126",
    }
)

claim_rows[0]["next_id"] = "CLM-COL-000127"
claim_rows.extend(
    [
        {
            "record_type": "claim",
            "schema_version": "1.0",
            "claim_id": "CLM-COL-000123",
            "claim_type": "sourced_published_computer_assisted_theorem",
            "status": "published_theorem_content_read_computational_feasibility_premise_not_independently_reproduced",
            "statement": "For every fixed positive integer a not divisible by 3, Krasikov-Lagarias Theorem 6.1 states that there is x_0(a) such that pi_a(x)>=x^(21/25) for all x>=x_0(a), where pi_a counts positive n<=x whose shortened T-orbit reaches a.",
            "source_ids": ["SRC-COL-000028"],
            "dependencies": [],
            "source_locators": [
                "Krasikov-Lagarias 2003 published p. 254, Theorem 6.1",
                "arXiv math/0205002v1 source lines 1516-1529",
                "qa/KRASIKOV-LAGARIAS-2003-F029-difference-inequality-audit.md",
            ],
            "proof_locator": {
                "path": "tex/chapters/01_literature_spine.tex",
                "label": "thm:KL-2003-predecessor-bound",
            },
            "formal_status": {
                "status": "published_computer_assisted_theorem_exact_exponent_margin_certified_unprinted_feasible_vector_open",
                "artifact": "certificates/krasikov_lagarias_2003_checks.py",
                "artifact_bytes": 9441,
                "artifact_sha256": "3f4ccc7256f026fa65ce7660b47823969c6c605e2a4c45da5b4b6d48961315fa",
                "verified_finite_metrics": {
                    "pinned_artifacts": 7,
                    "source_signature_checks": 40,
                    "exact_integer_exponent_margin_positive": True,
                },
                "explicitly_not_certified": [
                    "the k=11 feasible vector",
                    "L_11^NT(1.7922310) feasibility",
                    "Theorem 6.1 independently of its published status",
                ],
            },
            "open_obligation_ids": ["PO-COL-000001"],
            "nonclaims": [
                "No positive-density, density-one, target-uniform-threshold, target-divisible-by-3, or Collatz-conjecture conclusion follows.",
                "The theorem exponent is 21/25, not the rounded computational exponent 0.8417560.",
            ],
        },
        {
            "record_type": "claim",
            "schema_version": "1.0",
            "claim_id": "CLM-COL-000124",
            "claim_type": "independent_exact_clock_morphism",
            "status": "proved_with_domain_codomain_image_fibres_kernel_and_information_loss",
            "statement": "For each positive N, if n_j=T^j(N) and s_(j+1)-s_j is 1 for even n_j and 2 for odd n_j, then U^(s_j)(N)=T^j(N). The time embedding is strictly increasing with singleton image fibres and diagonal equality kernel. Its omitted times are exactly s_j+1 after odd n_j and carry 3n_j+1>=4, so shortened and unshortened orbits reach 1 on exactly the same starting values.",
            "source_ids": ["SRC-COL-000028", "SRC-COL-000005"],
            "dependencies": [],
            "source_locators": [
                "Krasikov-Lagarias 2003 published p. 237 shortcut map",
                "Tao arXiv:1909.03562v7 Section 1.1 unshortened map",
                "qa/KRASIKOV-LAGARIAS-2003-F029-difference-inequality-audit.md",
            ],
            "proof_locator": {
                "path": "tex/chapters/01_literature_spine.tex",
                "label": "prop:KL-Tao-clock-embedding",
            },
            "morphism_refs": ["MOR-COL-000032"],
            "formal_status": {
                "status": "proof_in_TeX_finite_exact_clock_kernel_pass",
                "artifact": "certificates/krasikov_lagarias_2003_checks.py",
                "artifact_bytes": 9441,
                "artifact_sha256": "3f4ccc7256f026fa65ce7660b47823969c6c605e2a4c45da5b4b6d48961315fa",
                "verified_finite_metrics": {
                    "clock_embedding_checks": 2010000,
                    "omitted_intermediate_checks": 1005735,
                    "bounded_target_one_equivalence_checks": 10000,
                },
                "explicitly_not_certified": [
                    "the infinite algebraic theorem independently of its TeX proof",
                    "the Collatz conjecture",
                ],
            },
            "open_obligation_ids": ["PO-COL-000001"],
            "nonclaims": [
                "The maps T and U are not identified one iterate at a time.",
                "The morphism loses each intermediate 3n+1 state after an odd shortened state; only target-one reachability is proved insensitive to that loss.",
                "No orbit-length, stopping-time, or density statement transfers without this variable clock.",
            ],
        },
        {
            "record_type": "claim",
            "schema_version": "1.0",
            "claim_id": "CLM-COL-000125",
            "claim_type": "independent_exact_source_proof_handoff_repair",
            "status": "proved_at_explicit_feasible_linear_program_hypothesis",
            "statement": "If L_k^NT(lambda) has a feasible solution for 1<lambda<=2, then for every 0<beta<log_2(lambda) and every positive a not divisible by 3 there is x_0(a) with pi_a(x)>=x^beta. The proof treats noncyclic residues 2 and 1 modulo 3 separately, then sends a cyclic target a to a noncyclic b=2^r a above the maximum of its cycle and uses pi_a>=pi_b.",
            "source_ids": ["SRC-COL-000028"],
            "dependencies": [],
            "source_locators": [
                "Krasikov-Lagarias 2003 Theorem 2.2, equation (2.1), and Theorem 6.1",
                "qa/KRASIKOV-LAGARIAS-2003-F029-difference-inequality-audit.md section Explicit transfer from phi to every permitted target",
            ],
            "proof_locator": {
                "path": "tex/chapters/01_literature_spine.tex",
                "label": "prop:KL-target-handoff",
            },
            "formal_status": {
                "status": "analytic_implication_proved_in_TeX_finite_cycle_lifts_and_exponent_margin_checked",
                "artifact": "certificates/krasikov_lagarias_2003_checks.py",
                "artifact_bytes": 9441,
                "artifact_sha256": "3f4ccc7256f026fa65ce7660b47823969c6c605e2a4c45da5b4b6d48961315fa",
                "verified_finite_metrics": {
                    "cycle_target_lift_checks": 40,
                    "exact_integer_exponent_margin_positive": True,
                },
                "explicitly_not_certified": [
                    "any unprinted feasible vector",
                    "Theorem 2.2 independently of the source proof",
                ],
            },
            "open_obligation_ids": ["PO-COL-000001"],
            "nonclaims": [
                "The proposition does not assert that a feasible solution exists.",
                "The cycle-target argument does not classify unknown cycles or assume the Collatz conjecture.",
            ],
        },
        {
            "record_type": "claim",
            "schema_version": "1.0",
            "claim_id": "CLM-COL-000126",
            "claim_type": "exact_sourced_theorem_transport_across_proved_morphism",
            "status": "proved_from_sourced_theorem_and_exact_clock_embedding",
            "statement": "For every x>=1, Tao's set {N<=x:Col_min(N)=1} is exactly the set counted by Krasikov-Lagarias pi_1(x). Hence their published Theorem 6.1 gives # {N<=x:Col_min(N)=1} >= x^(21/25) for all sufficiently large x, with the same published computer-assisted premise and no density upgrade.",
            "source_ids": ["SRC-COL-000028", "SRC-COL-000005"],
            "dependencies": ["CLM-COL-000123", "CLM-COL-000124"],
            "source_locators": [
                "Tao arXiv:1909.03562v7 lines 155-156",
                "Krasikov-Lagarias 2003 published p. 254",
                "qa/KRASIKOV-LAGARIAS-2003-F029-difference-inequality-audit.md",
            ],
            "proof_locator": {
                "path": "tex/chapters/01_literature_spine.tex",
                "label": "eq:KL-Tao-count-identity",
            },
            "morphism_refs": ["MOR-COL-000032"],
            "formal_status": {
                "status": "exact_set_transport_proved_finite_kernel_pass_source_theorem_not_recomputed",
                "artifact": "certificates/krasikov_lagarias_2003_checks.py",
                "artifact_sha256": "3f4ccc7256f026fa65ce7660b47823969c6c605e2a4c45da5b4b6d48961315fa",
            },
            "open_obligation_ids": ["PO-COL-000001"],
            "nonclaims": [
                "The transported exponent is not positive density, natural-density one, logarithmic-density one, or the Collatz conjecture.",
                "No clock identity stronger than MOR-COL-000032 is asserted.",
            ],
        },
    ]
)

morphism_rows[0]["next_id"] = "MOR-COL-000033"
morphism_rows.append(
    {
        "record_type": "morphism",
        "schema_version": "1.0",
        "morphism_id": "MOR-COL-000032",
        "name": "Krasikov_Lagarias_shortened_time_to_Tao_unshortened_time_embedding",
        "domain": "For each fixed positive starting value N, shortened time j in N_0 along n_j=T^j(N).",
        "codomain": "Unshortened time r in N_0 along U^r(N), with image {s_j:j in N_0}.",
        "formula": "iota_N(j)=s_j, s_0=0, s_(j+1)=s_j+1 when T^j(N) is even and s_j+2 when T^j(N) is odd; U^(s_j)(N)=T^j(N).",
        "well_definedness": "Every shortened state is positive and has a unique parity, so every increment is exactly 1 or 2. For even n, T(n)=U(n); for odd n, T(n)=U^2(n). Induction proves the intertwining identity.",
        "preserved_structure": "Starting value, chronological order, every shortened orbit state, and target-one reachability. The exact counted set for a=1 and every real cutoff x is preserved.",
        "fibres": "iota_N is strictly increasing, so each fibre on its image is a singleton and the equality kernel pair is diagonal.",
        "inverse_status": "There is a unique order-preserving inverse from the image {s_j} to N_0. No inverse is claimed on all unshortened times. The complement consists exactly of s_j+1 after odd shortened states.",
        "exceptions": [
            "At each omitted time the state is 3T^j(N)+1>=4, so omission cannot hide the target 1.",
            "The intermediate state after an odd input is genuine information loss; T and U are not identified stepwise.",
            "Stopping times and orbit lengths require the explicit variable clock and are not numerically preserved.",
        ],
        "claim_refs": ["CLM-COL-000124", "CLM-COL-000126"],
        "source_refs": ["SRC-COL-000028", "SRC-COL-000005"],
        "proof_locator": {
            "path": "tex/chapters/01_literature_spine.tex",
            "label": "prop:KL-Tao-clock-embedding",
        },
        "formal_status": {
            "status": "proof_in_TeX_finite_exact_embedding_fibre_omitted_state_and_target_one_checks_pass",
            "artifact": "certificates/krasikov_lagarias_2003_checks.py",
            "artifact_sha256": "3f4ccc7256f026fa65ce7660b47823969c6c605e2a4c45da5b4b6d48961315fa",
            "verified_metrics": {
                "clock_embedding_checks": 2010000,
                "omitted_intermediate_checks": 1005735,
                "bounded_target_one_equivalence_checks": 10000,
            },
        },
    }
)

po1 = next(row for row in obligation_rows if row.get("obligation_id") == "PO-COL-000001")
po1["status"] = "in_progress_after_complete_Tao_version_reconciliation_and_Krasikov_Lagarias_intake_remaining_Terras_Allouche_Korec_and_other_cited_literature_plus_release_gates_open"
add_unique(po1["source_refs"], "SRC-COL-000028")
add_unique(
    po1["claim_refs"],
    "CLM-COL-000123",
    "CLM-COL-000124",
    "CLM-COL-000125",
    "CLM-COL-000126",
)
po1["required_checks"][1] = "Content-read the remaining claim-driving cited literature absent from the local source registry, beginning with Terras 1976/1979, Allouche 1979, and Korec 1994; Krasikov-Lagarias 2003 is complete under SRC-COL-000028, CLM-COL-000123 through 000126, and MOR-COL-000032."
add_unique(
    po1["completed_checks"],
    "content-read all 22 published Krasikov-Lagarias pages and the complete arXiv v1 source, reconstructed the difference-inequality and LP proof chain, and typed six published plus two preprint-only defects",
    "proved the exact shortened-to-unshortened time embedding with image, singleton fibres, diagonal kernel, omitted intermediate states, target-one equivalence, and exact Tao counting-set identity",
    "supplied the exact noncyclic residue and cyclic-target handoffs, certified log_2(1.7922310)>21/25 by an integer inequality, and retained the unprinted k=11 feasibility vector as an open reproducibility boundary",
    "passed certificates/krasikov_lagarias_2003_checks.py at its finite source, exponent, clock, and target-kernel scope",
)
checkpoint = po1["local_checkpoint"]
checkpoint["status"] = "pass_complete_Tao_version_reconciliation_and_Krasikov_Lagarias_cited_source_crosswalk_remaining_Terras_Allouche_Korec_other_literature_and_release_gates_open"
add_unique(
    checkpoint["claim_refs"],
    "CLM-COL-000123",
    "CLM-COL-000124",
    "CLM-COL-000125",
    "CLM-COL-000126",
)
add_unique(checkpoint["morphism_refs"], "MOR-COL-000032")
checkpoint["certificates"].append(
    {
        "path": "certificates/krasikov_lagarias_2003_checks.py",
        "sha256": "3f4ccc7256f026fa65ce7660b47823969c6c605e2a4c45da5b4b6d48961315fa",
        "status": "pass_finite_exact_source_exponent_clock_and_target_kernel_scope",
    }
)
add_unique(
    checkpoint["proof_locators"],
    "tex/chapters/01_literature_spine.tex#prop:KL-Tao-clock-embedding",
    "tex/chapters/01_literature_spine.tex#thm:KL-2003-predecessor-bound",
    "tex/chapters/01_literature_spine.tex#prop:KL-target-handoff",
)
checkpoint["source_dependency_limit"] = "Tao v7 complete mathematical text and version reconciliation plus complete Krasikov-Lagarias 2003 content/proof/computation-boundary intake; Terras-Allouche-Korec and remaining cited-source intake and release gates remain open"
add_unique(
    po1["audit_records"],
    "qa/KRASIKOV-LAGARIAS-2003-F029-difference-inequality-audit.md",
)

coverage_path = ROOT / "state" / "coverage.json"
coverage = json.loads(coverage_path.read_text(encoding="utf-8"))
lit = next(layer for layer in coverage["layers"] if layer["layer_id"] == "LIT")
formal = next(layer for layer in coverage["layers"] if layer["layer_id"] == "FORMAL")
syn = next(layer for layer in coverage["layers"] if layer["layer_id"] == "SYN")
recovery = next(layer for layer in coverage["layers"] if layer["layer_id"] == "RECOVERY")
lit["documents_read"] = 28
lit["documents_admitted"] = 28
lit["status"] = "foundational_spine_in_progress_28_documents_Tao_whole_version_reconciliation_complete_Krasikov_Lagarias_2003_complete_with_exact_clock_and_computation_boundary_Terras_Allouche_Korec_other_cited_literature_and_release_gates_open"
formal["artifacts_verified"] = 18
formal["status"] += "_Krasikov_Lagarias_source_exponent_clock_target_finite_certificate_verified"
syn["live_tex_advanced_after_checkpoint"] = True
syn["fresh_ACT33_build_pending"] = True
syn["status"] = "ACT32_106_page_PDF_remains_prior_passing_checkpoint_live_TeX_advanced_with_Krasikov_Lagarias_source_theorem_repairs_and_clock_morphism_fresh_ACT33_build_and_visual_QA_pending"
recovery["status"] = "ACT32_checkpoint_passed_as_prior_boundary_ACT33_advanced_through_F028_and_Krasikov_Lagarias_F029_fresh_ACT33_literature_package_visual_and_release_recovery_gates_open"
coverage_path.write_text(json.dumps(coverage, indent=2) + "\n", encoding="utf-8")

project_path = ROOT / "state" / "project_state.json"
project = json.loads(project_path.read_text(encoding="utf-8"))
project["next_action"] = "Continue PO-COL-000001 by acquiring and content-admitting Terras 1976, Terras 1979, Allouche 1979, and Korec 1994, then propagate the exact Tao introductory threshold correction and 1979 density-clarification dependency. Krasikov-Lagarias 2003 is complete under SRC-COL-000028, CLM-COL-000123 through 000126, MOR-COL-000032, F029, and its passing finite certificate; its unprinted k=11 feasibility vector remains an explicit reproducibility obligation. Continue remaining cited literature before Chatnotes, Gemini, or archived tasks; keep all eight obligations and the durable goal active; do not contact the quarantined task; enforce the single bounded watched Lean-worker rule."
project["updated_utc"] = NOW
project_path.write_text(json.dumps(project, indent=2) + "\n", encoding="utf-8")

write_jsonl("state/source_registry.jsonl", source_rows)
write_jsonl("state/claims.jsonl", claim_rows)
write_jsonl("state/morphisms.jsonl", morphism_rows)
write_jsonl("state/proof_obligations.jsonl", obligation_rows)

print(
    json.dumps(
        {
            "status": "PASS",
            "timestamp_utc": NOW,
            "source_records": len(source_rows) - 1,
            "claim_records": len(claim_rows) - 1,
            "morphism_records": len(morphism_rows) - 1,
            "proof_obligations": len(obligation_rows) - 1,
            "admitted_source": "SRC-COL-000028",
            "admitted_claims": [
                "CLM-COL-000123",
                "CLM-COL-000124",
                "CLM-COL-000125",
                "CLM-COL-000126",
            ],
            "admitted_morphism": "MOR-COL-000032",
            "completion_claimed": False,
        },
        indent=2,
    )
)
