#!/usr/bin/env python3
"""Propagate the independently audited ACT42 corrections through live state.

This is a bounded, ID-addressed mechanical rewrite.  It does not touch the
frozen corpus index, source files, TeX, project seal, or historical receipts.
"""

from __future__ import annotations

import json
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLAIMS = ROOT / "state" / "claims.jsonl"
MORPHISMS = ROOT / "state" / "morphisms.jsonl"
SOURCES = ROOT / "state" / "source_registry.jsonl"
TOPICS = ROOT / "state" / "topic_routes.jsonl"
INTAKE = ROOT / "state" / "chatnotes_intake.jsonl"

ROOT_CERT_PATH = "certificates/chatnotes_symbolic_completion_checks.py"
ROOT_CERT_HASH = "f6130edbabd04602a7d686943416d6adb715d94bb3d44c959a0d1c8f07d4cbd0"
CHAPTER = "tex/chapters/04_symbolic_completion_and_geometric_boundaries.tex"


def read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        assert line.strip(), f"blank JSONL line at {path}:{number}"
        rows.append(json.loads(line))
    return rows


def index(rows: list[dict], key: str) -> dict[str, dict]:
    result = {row[key]: row for row in rows if key in row}
    assert len(result) == sum(key in row for row in rows), f"duplicate {key}"
    return result


def encode(rows: list[dict]) -> str:
    return "\n".join(
        json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in rows
    ) + "\n"


def atomic_write(path: Path, payload: str) -> None:
    temporary = path.with_name(path.name + ".act42-audited.tmp")
    assert not temporary.exists(), temporary
    temporary.write_text(payload, encoding="utf-8", newline="\n")
    os.replace(temporary, path)


def locator(label: str) -> dict[str, str]:
    return {"path": CHAPTER, "label": label}


claims = read_jsonl(CLAIMS)
morphisms = read_jsonl(MORPHISMS)
sources = read_jsonl(SOURCES)
topics = read_jsonl(TOPICS)
intakes = read_jsonl(INTAKE)

claim = index(claims, "claim_id")
morphism = index(morphisms, "morphism_id")
source = index(sources, "source_id")
topic = index(topics, "topic_id")
intake = index(intakes, "intake_id")

assert claims[0]["next_id"] == "CLM-COL-000165"
assert morphisms[0]["next_id"] == "MOR-COL-000052"
assert sources[0]["next_id"] == "SRC-COL-000042"
assert "SRC-COL-000042" not in source
assert set(f"CLM-COL-{n:06d}" for n in range(151, 165)) <= set(claim)
assert set(f"MOR-COL-{n:06d}" for n in range(45, 52)) <= set(morphism)
assert "CHATINT-COL-000015" in intake


# Source identity and content-scope repairs.
source["SRC-COL-000037"]["bibliographic_identity"] = {
    "arxiv_version_id": "1502.05580",
    "arxiv_primary_class": "math.AG",
    "arxiv_record": "https://arxiv.org/abs/1502.05580",
    "journal": "Advances in Mathematics",
    "volume": 291,
    "pages": "274-329",
    "publication_year": 2016,
    "doi": "10.1016/j.aim.2015.11.045",
}
src37 = source["SRC-COL-000037"]
src37["reading"]["locators"] = [
    "source TeX lines 350-406: arithmetic site, tropical characteristic-one notation, and theorem context",
    "source TeX lines 1151-1214: unreduced square, Frobenius maps, diagonal/power distinction, and non-cancellativity caveat",
    "source TeX lines 1364-1400: Conv(Z x Z) semiring and quotient proposition",
    "source TeX lines 1470-1519: universal factorization, reduced square, and semiring scope",
    "source TeX lines 1522-1902, especially 1747-1755: Frobenius correspondences and the exact three-case composition theorem",
]
src37["reading"]["source_objects"]["frobenius_correspondence_composition"] = {
    "case_product_irrational": "if lambda lambda' is irrational, Psi(lambda) composed with Psi(lambda') equals Psi(lambda lambda')",
    "case_both_rational": "if lambda and lambda' are positive rational, the same equality holds",
    "case_both_irrational_product_rational": "if lambda and lambda' are irrational and their product is positive rational, the composition is id_epsilon composed with Psi(lambda lambda')",
}

src38 = source["SRC-COL-000038"]
src38["reading"]["locators"] = [
    "PDF p. 1: abstract and one-variable cyclotomic setup",
    "PDF printed pp. 50-53, section 7: Theorem 7.5 on complete modules with Delta-hyperstratification and Theorem 7.12 on finite-free weakly nilpotent Delta-modules/vector bundles",
    "PDF printed pp. 54-61, section 8: de Rham crystal comparison",
    "PDF printed pp. 62-66, section 9: Hodge-Tate crystal comparisons",
    "PDF printed pp. 67-69, section 10: prismatic F-crystals, crystalline representation lattices, and Wach modules",
]
src38["reading"]["source_objects"] = {
        "base": "W(k) with k a perfect field of characteristic p>0, a primitive pth root zeta, and the one-variable ring W[[q-1]]",
    "Theorem_7_5": "equivalence formulated using complete modules with Delta-hyperstratification",
    "Theorem_7_12": "equivalence between the stated finite-free weakly nilpotent Delta-modules and prismatic vector bundles",
    "F_crystal_equivalence": "with Frobenius, prismatic F-crystals correspond to crystalline representation lattices under the printed hypotheses",
}
src38["nonclaims"] = [
    "The source constructs no two-coordinate (2,3) toric or Collatz calculus and no pair of commuting Collatz connection operators.",
    "Its Delta-connections and Frobenius structures cannot be applied to the raw branch maps without a separately defined base ring, object, and map.",
    "No Collatz termination, KMS, or operator-algebra conclusion is sourced here.",
]

src41 = source["SRC-COL-000041"]
assert src41["manifestations"][0]["sha256"] == (
    "db08aa70c9676db5becd352ed4881b7b7ffd08c89e0d3db52c0f7f0a34720492"
)
src41.update(
    {
        "authors": ["Omri M. Sarig"],
        "title": "Thermodynamic formalism for countable Markov shifts",
        "bibliographic_identity": {
            "book_title": "Hyperbolic Dynamics, Fluctuations and Large Deviations",
            "series": "Proceedings of Symposia in Pure Mathematics",
            "volume": 89,
            "pages": "81-117",
            "publisher": "American Mathematical Society",
            "publication_year": 2015,
            "doi": "10.1090/pspum/089/01485",
        },
        "manifestations": [
            {
                "path": "C:/Users/LOCAL_USER/Documents/Papors/OS/arig O (1999) Thermodynamic formalism for countable.pdf",
                "role": "controlling_2015_PSPUM_overview_PDF_despite_misleading_local_filename",
                "bytes": 544513,
                "pdf_pages": 36,
                "published_pages": "81-117",
                "sha256": "db08aa70c9676db5becd352ed4881b7b7ffd08c89e0d3db52c0f7f0a34720492",
            }
        ],
        "route_ids": [],
        "route_integrity": {
            "status": "frozen_route_and_local_filename_misidentified_the_2015_overview_as_the_1999_article; content_and_bibliography_adjudicated_the_identity",
            "corrupted_routing_residue": "PUBUNIT-41ED65E25C5A2A660466C7AA",
            "canonical_publication_unit_id": None,
            "frozen_ledgers_mutated": False,
            "routing_metadata_used_as_theorem_evidence": False,
        },
        "reading": {
            "status": "complete_relevant_sections_read_for_current_pressure_recurrence_equilibrium_and_BIP_scope",
            "locators": [
                "physical PDF p. 1: title, author, overview abstract, and Section 1",
                "physical PDF p. 14: Theorem 4.3 and Definition 4.5",
                "physical PDF p. 16: Theorem 4.9; notes continue on physical p. 17",
                "physical PDF p. 18: Theorem 5.3",
                "physical PDF p. 19: Definition 5.8 and Theorem 5.9",
                "physical PDF pp. 35-36: bibliography, including [Sar99] as a distinct 1999 article",
            ],
            "source_objects": {
                "document_type": "2015 overview distinct from the 1999 ETDS article",
                "TMS": "one-sided shift on a finite or countable directed graph",
                "pressure_and_recurrence": "overview statements at Theorems 4.3 and 4.9",
                "variational_and_Gibbs_scope": "overview statements at Theorem 5.3, Definition 5.8, and Theorem 5.9",
            },
        },
        "audit": {
            "path": "intake/chatnotes/ZN-SYMMETRIES-TROPICAL-PRISMATIC-SYMBOLIC-DIRECT-LOCATOR-AUDIT-04.md",
            "status": "content_identity_adjudicated_as_2015_overview_and_exact_physical_locators_crosswalked",
        },
        "nonclaims": [
            "This 36-page file is not the 1999 ETDS article, irrespective of its local filename or frozen-route metadata.",
            "The overview does not turn the positive Collatz image or prefix tree into a topologically mixing BIP shift.",
            "No recurrence, equilibrium, or Collatz endpoint assertion is transferred without its hypotheses.",
        ],
    }
)

src42 = {
    "record_type": "source_document",
    "schema_version": "1.0",
    "source_id": "SRC-COL-000042",
    "authors": ["Omri M. Sarig"],
    "title": "Thermodynamic formalism for countable Markov shifts",
    "bibliographic_identity": {
        "journal": "Ergodic Theory and Dynamical Systems",
        "volume": 19,
        "issue": 6,
        "pages": "1565-1593",
        "publication_year": 1999,
        "doi": "10.1017/S0143385799146820",
        "publisher_record": "https://www.cambridge.org/core/journals/ergodic-theory-and-dynamical-systems/article/thermodynamic-formalism-for-countable-markov-shifts/0E7AE519009DE8E9163DF27EFCF539D6",
    },
    "manifestations": [
        {
            "path": "C:/Users/LOCAL_USER/Documents/Erdos Strauss and related/collatz_reconstruction/external_literature/act42_sarig_1999/sarig_1999_author_preprint_pr_4.pdf",
            "role": "official_author_preprint_corresponding_to_the_published_1999_article",
            "bytes": 347306,
            "pdf_pages": 33,
            "preprint_date": "February 1998",
            "sha256": "9e32047d0d605f22375a419ccda190ad9aff7c71a1a78aae0c142cb170618c47",
            "official_author_url": "https://www.weizmann.ac.il/math/sarigo/sites/math.sarigo/files/uploads/pr_4.pdf",
        }
    ],
    "route_ids": [],
    "route_integrity": {
        "status": "exact_frozen_query_exposed_a_corrupted_2015_route_then_official_author_preprint_acquired_and_content_read",
        "queried_corrupted_result_unit_id": "PUBUNIT-41ED65E25C5A2A660466C7AA",
        "frozen_ledgers_mutated": False,
        "nonexistence_inferred_from_bad_route": False,
    },
    "reading": {
        "status": "complete_33_page_author_preprint_visually_reviewed_with_exact_definition_theorem_and_Gibbs_pages_read",
        "locators": [
            "physical preprint p. 1: title, author, abstract, and February 1998 date",
            "physical preprint p. 3: countable topological Markov shift and topological mixing",
            "physical preprint pp. 5-6: fixed-base periodic partition Z_n(phi,a) and Definition 1 of Gurevich pressure",
            "physical preprint p. 7: finite-subshift pressure and variational route",
            "physical preprint p. 18: condition (13), the one-sided big-images condition, and Theorem 5",
            "physical preprint pp. 24-25: Gibbs definition and Theorem 8",
            "all 33 physical pages rendered and reviewed through six contact sheets; the cited pages were inspected at original detail",
        ],
        "source_objects": {
            "TMS": "one-sided topological Markov shift with countably many states",
            "Gurevich_pressure": "fixed-base periodic partition growth under the printed mixing and regularity hypotheses",
            "recurrence_and_RPF": "positive/null/transient recurrence framework and generalized Ruelle-Perron-Frobenius theorem",
            "condition_13": "one-sided big images: there are finitely many states b_1,...,b_n such that every state a has an edge a to some b_i; this is not BIP",
            "Theorem_5_scope": "for a topologically mixing shift and a locally Holder potential with finite Gurevich pressure, positive recurrence and an RPF eigenfunction uniformly bounded above and below are among the hypotheses for exponential RPF convergence, together with condition (13)",
            "Theorem_8_scope": "for a topologically mixing shift and a locally Holder potential with finite Gurevich pressure, a Gibbs measure exists exactly when the potential is positive recurrent, its RPF eigenfunction is uniformly bounded above and below, and condition (13) holds; then the Gibbs measure is the RPF measure h nu and its pressure parameter equals the Gurevich pressure",
        },
    },
    "audit": {
        "path": "intake/chatnotes/ZN-SYMMETRIES-TROPICAL-PRISMATIC-SYMBOLIC-DIRECT-LOCATOR-AUDIT-04.md",
        "status": "official_author_preprint_content_and_visual_crosswalk",
    },
    "nonclaims": [
        "The 1999 paper is distinct from Sarig's 2015 overview with the same title.",
        "The paper's pressure and recurrence theory is not transferred to the positive Collatz image or prefix tree without checking every hypothesis.",
        "No Collatz termination or endpoint theorem is supplied.",
    ],
}
sources.append(src42)
source[src42["source_id"]] = src42
sources[0]["next_id"] = "SRC-COL-000043"


# Claim propagation, including reciprocal morphism references and exact source locators.
claim["CLM-COL-000153"]["morphism_refs"] = [
    "MOR-COL-000045",
    "MOR-COL-000046",
    "MOR-COL-000047",
]
claim["CLM-COL-000153"]["nonclaims"] = [
    "There is no itinerary morphism on E, so there is no bijection on all of 1+2Z_2.",
    "The survivor domain D is an inverse-limit coding domain, not the metric completion of the positive odd integers; that completion is all of 1+2Z_2.",
    "The full-shift conjugacy on D is not a theorem about termination of positive orbits.",
]

claim["CLM-COL-000155"]["nonclaims"] = [
    "The criterion does not assert that a general exponent word stabilizes.",
    "It is not tail-invariant: (2,2,...) codes 1, while the tail-equivalent (1,2,2,...) codes 1/3.",
    "The rooted tree is acyclic and strictly graded; it does not by itself give a topologically mixing recurrent Markov presentation of the positive image.",
    "No finite forbidden-word criterion exists because the finite language is full.",
]

clm156 = claim["CLM-COL-000156"]
clm156["statement"] = (
    "For phi(a)=log 3-a_1 log 2 on the full countable shift, the n-block "
    "partition sum is finite exactly for beta>0 and then equals "
    "(((3/2)^beta)/(1-2^(-beta)))^n, with pressure "
    "beta log(3/2)-log(1-2^(-beta)) and exact Bernoulli weights "
    "(1-2^(-beta))2^(-beta(a-1)). At beta<=0 the one-symbol sum diverges. "
    "The full shift is the TMS of the complete countable graph, is topologically "
    "mixing and BIP, and beta phi is one-cylinder locally constant with zero "
    "higher variations and finite supremum for beta>0. For every beta>0 the "
    "countable positive itinerary image has measure zero under this full-shift "
    "Gibbs law."
)
clm156["source_ids"] = [
    "SRC-COL-000040",
    "SRC-COL-000041",
    "SRC-COL-000042",
]
clm156["source_locators"] = [
    "raw Z_n Symmetries physical lines 16282-16348 and 16799-16823",
    "Sarig 2003 printed pp. 1751-1757, especially Theorem 1",
    "Sarig 2015 overview physical PDF pp. 14, 16, 18, and 19",
    "Sarig 1999 author preprint physical pp. 3, 5-7, and 24-25",
]
clm156["nonclaims"] = [
    "This is thermodynamic formalism on the full survivor shift, not a distribution theorem for deterministic positive Collatz orbits.",
    "The equality p_1(a)=2^(-a) does not establish independence along positive integer trajectories.",
    "The theorem proves no termination or recurrence statement for positive Collatz dynamics.",
]

clm159 = claim["CLM-COL-000159"]
clm159["statement"] = (
    "For a nonzero commutative semiring K, the K-linear degree map from the "
    "finite-support category semialgebra K[E_C] to K[N_0^2] is not "
    "multiplicative: distinct object identities multiply to zero but both map "
    "to the target unit. Separately, on the path semigroup with absorbing zero, "
    "the zero-preserving set map theta(0)=empty and theta(p)=j(deg p) is "
    "multiplicative on composable pairs but not globally: theta(1_x1_y)=empty "
    "for x!=y whereas theta(1_x)theta(1_y)=Q+_Mink Q=Q. No coefficient-semiring "
    "map into Conv(Z^2) is asserted. The typed matrix representation retaining "
    "object units is the algebraic repair."
)
clm159["morphism_refs"] = ["MOR-COL-000049", "MOR-COL-000050"]
clm159["nonclaims"] = [
    "Failure of these exact object-erasing formulas does not rule out typed tropical representations.",
    "The translated-quadrant statement is a semigroup-with-zero obstruction, not an untyped composition of a monomial algebra map with j.",
    "No categorical nonidentity or unrelatedness conclusion is inferred from differing presentations.",
]

claim["CLM-COL-000160"]["statement"] = (
    "Connes and Consani construct the arithmetic-site tensor square, its "
    "reduction via Newton polygons in Conv(Z x Z), and Frobenius maps and "
    "correspondences. Their composition theorem has three exact cases: if "
    "lambda lambda' is irrational, Psi(lambda) composed with Psi(lambda') "
    "equals Psi(lambda lambda'); if both parameters are positive rational, "
    "the same equality holds; if both are irrational and their product is "
    "positive rational, the composition is id_epsilon composed with "
    "Psi(lambda lambda'). The source also distinguishes diagonal Frobenius "
    "from a power map and records noncancellativity before reduction."
)
claim["CLM-COL-000160"]["source_locators"] = [
    "Connes-Consani source TeX lines 1151-1214, 1364-1400, 1470-1519, 1522-1902, and especially 1747-1755",
]

clm162 = claim["CLM-COL-000162"]
clm162["statement"] = (
    "Every continuous unital endomorphism of Z_3 is the identity, so "
    "g_a(x)=(3x+1)/2^a is not an endomorphism of Spf(Z_3), already because "
    "g_a(0)=2^(-a) is nonzero. The coordinate substitution "
    "T->(3T+1)/2^a does define an endomorphism of the formal affine line "
    "Spf(Z_3<T>); on Z_3-points it is injective with image 2^(-a)+3Z_3 and "
    "the displayed inverse. For every a,k>=1 and every residue b mod 3^k, "
    "CRT constructs positive odd points in the same 3-adic ball with valuations "
    "a and a+1. Thus the integer a-stratum and its complement meet every "
    "finite 3-adic residue ball, and no clopen subset of Z_3 cuts out that "
    "stratum on the positive odd integers."
)
clm162["additional_proof_locators"] = [
    locator("prop:symbolic-formal-affine-line-repair"),
    locator("prop:symbolic-no-three-adic-valuation-selector"),
]
clm162["formal_status"] = {
    "status": "certificate_pass_32_formal_point_and_960_bounded_CRT_checks_with_general_continuity_substitution_point_fibre_and_density_proofs_in_TeX",
    "artifact": ROOT_CERT_PATH,
    "artifact_sha256": ROOT_CERT_HASH,
    "verified_metrics": {
        "formal_point_ring_map_obstruction_checks": 32,
        "three_adic_selector_CRT_checks": 960,
    },
}
clm162["nonclaims"] = [
    "No WCart(g_a) on the formal point is admitted.",
    "The formal-affine-line endomorphism does not assemble the Collatz piecewise map or supply its 2-adic exponent selector.",
    "The CRT theorem rules out a clopen finite-level 3-adic selector on positive odds; it does not assert that every richer mixed-adic construction is impossible.",
    "No prismatic or crystalline Collatz theorem follows.",
]

clm163 = claim["CLM-COL-000163"]
clm163["statement"] = (
    "For W the Witt vectors of a perfect field of characteristic p and a "
    "primitive pth root zeta, Gros, Le Stum, and Quiros work over the "
    "one-variable ring W[[q-1]]. Their Theorem 7.5 uses complete modules with "
    "Delta-hyperstratification, while Theorem 7.12 identifies the stated "
    "finite-free weakly nilpotent Delta-modules and prismatic vector bundles. "
    "Their later sections treat de Rham, Hodge-Tate, Frobenius, crystalline-"
    "representation, and Wach-module comparisons at their printed scopes."
)
clm163["nonclaims"] = [
    "The source contains no two-coordinate W[[q_2-1,q_3-1]] Collatz calculus and no pair of commuting Collatz connection operators.",
    "It supplies no pair of branch operators or drift-observable identity for the Collatz map.",
]

clm164 = claim["CLM-COL-000164"]
clm164["statement"] = (
    "Sarig's 1999 article defines the countable-shift Gurevich-pressure and "
    "recurrence/Ruelle-Perron-Frobenius framework. Its Theorem 8, for a "
    "topologically mixing shift and a locally Holder potential of finite "
    "Gurevich pressure, says that a Gibbs measure exists exactly when the "
    "potential is positive recurrent, its RPF eigenfunction is uniformly "
    "bounded above and below, and condition (13) holds; condition (13) is "
    "the one-sided big-images condition, not BIP. In that case the Gibbs "
    "measure is h nu and its pressure parameter equals the Gurevich pressure. "
    "His 2003 theorem treats a "
    "topologically mixing countable Markov shift with summable variations, "
    "finite first variation, and finite Gurevich pressure, and characterizes "
    "existence of an invariant Gibbs measure by BIP at that scope. His distinct "
    "2015 overview restates the pressure, recurrence, variational, equilibrium, "
    "Gibbs, and BIP boundaries at its separately cited theorem locators."
)
clm164["source_ids"] = [
    "SRC-COL-000040",
    "SRC-COL-000041",
    "SRC-COL-000042",
]
clm164["source_locators"] = [
    "Sarig 2003 printed pp. 1751-1757, especially Theorem 1",
    "Sarig 2015 overview physical PDF pp. 14, 16, 18, and 19",
    "Sarig 1999 author preprint physical pp. 3, 5-7, 18, and 24-25",
]
clm164["nonclaims"] = [
    "These hypotheses are checked here for the full survivor shift, not transferred to Sigma_C^+ or the acyclic strictly graded prefix tree.",
    "No recurrence or termination theorem for positive Collatz dynamics is supplied by the source crosswalk.",
]


# Morphism propagation.
morphism["MOR-COL-000047"]["inverse_status"] = (
    "The nested-ball map is a two-sided continuous inverse. It is not an "
    "integer-valued inverse: all but countably many full-shift words correspond "
    "to nonrational 2-adic points, while the positive-integer image is the "
    "countable dense proper subset Sigma_C^+."
)

mor50 = morphism["MOR-COL-000050"]
mor50["well_definedness"] = (
    "Every translated quadrant (r,s)+Q is closed and convex, satisfies "
    "C+Q=C, obeys the literal source condition C subset (r,s)+Q, and has the "
    "unique integral extreme point (r,s). Since Q+Q=Q, Minkowski sum adds "
    "anchors: j(r,s)+_Mink j(r',s')=j(r+r',s+s')."
)
mor50["claim_refs"] = [
    "CLM-COL-000158",
    "CLM-COL-000159",
    "CLM-COL-000160",
]

mor51 = morphism["MOR-COL-000051"]
mor51["exceptions"] = [
    "This is not a self-map of the base formal point Spf(Z_3).",
    "For every a, the positive integer valuation-a stratum and its complement meet every finite 3-adic residue ball; no clopen subset of Z_3 restricts to that selector on positive odds.",
    "The family does not assemble the piecewise Collatz map, a prismatic lift, or a crystalline comparison.",
]
mor51["additional_proof_locators"] = [
    locator("prop:symbolic-no-three-adic-valuation-selector")
]
mor51["formal_status"] = {
    "status": "certificate_pass_32_formal_point_and_960_bounded_CRT_checks_with_general_formal_affine_substitution_point_fibre_and_selector_density_proofs_in_TeX",
    "artifact": ROOT_CERT_PATH,
    "artifact_sha256": ROOT_CERT_HASH,
    "verified_metrics": {
        "formal_point_ring_map_obstruction_checks": 32,
        "three_adic_selector_CRT_checks": 960,
    },
}

# Every ACT42 root-certificate reference must pin the new audited artifact.
for record in claims + morphisms:
    formal = record.get("formal_status")
    if isinstance(formal, dict) and formal.get("artifact") == ROOT_CERT_PATH:
        formal["artifact_sha256"] = ROOT_CERT_HASH


# Topic-route repair, including explicit adjudication of the corrupted route.
route = topic["TOPIC-COL-SYMBOLIC-GEOMETRIC-BOUNDARIES-0002"]
route["updated_utc"] = "2026-08-29T21:07:40Z"
route["mathematical_objects"] = [
    item.replace(
        "path bidegree functor and Conv(Z x Z) singleton shadow",
        "path bidegree functor and Conv(Z x Z) translated-quadrant shadow/embedding",
    )
    for item in route["mathematical_objects"]
]
for query in route["queries"]:
    if query["query"] == "Sarig Thermodynamic Formalism countable Markov shifts":
        assert query["result_unit_ids"] == ["PUBUNIT-41ED65E25C5A2A660466C7AA"]
        query["adjudication"] = (
            "The frozen result and local filename misidentify a 36-page 2015 "
            "PSPUM overview as the 1999 ETDS article. The overview is SRC-COL-"
            "000041; the genuine 1999 author preprint was acquired separately "
            "as SRC-COL-000042. The frozen route remains unmodified."
        )

for item in route["sources"]:
    if item["publication_unit_or_source_id"] == "PUBUNIT-D3E19D3ED7DF512627055246":
        item["relevance_edge"] = (
            "supplies the exact one-variable cyclotomic prismatic and Delta-"
            "connection theorem scope against which the raw two-coordinate "
            "proposal is typed"
        )
        item["content_loci_read"][0] = (
            "Theorem 7.5 complete modules with Delta-hyperstratification and "
            "Theorem 7.12 finite-free weakly nilpotent Delta-modules/vector bundles"
        )
    if item["publication_unit_or_source_id"] == "PUBUNIT-41ED65E25C5A2A660466C7AA":
        item.update(
            {
                "publication_unit_or_source_id": "SRC-COL-000041",
                "exact_locators": [
                    "physical PDF pp. 1, 14, 16-19, and 35-36",
                    "SRC-COL-000041",
                ],
                "relevance_edge": "supplies the distinct 2015 overview of countable-shift pressure, recurrence, variational, equilibrium, Gibbs, and BIP boundaries",
                "toc_or_section_check": {
                    "status": "checked",
                    "checked_utc": "2026-08-29T21:07:40Z",
                    "relevant_sections": [
                        "countable Markov shifts and variations",
                        "pressure and recurrence overview",
                        "variational principle, Gibbs measures, and BIP",
                    ],
                },
                "reading_status": "complete_relevant_sections_read_for_current_dependency",
                "content_loci_read": [
                    "physical p. 14 Theorem 4.3 and Definition 4.5",
                    "physical p. 16 Theorem 4.9 with notes on p. 17",
                    "physical p. 18 Theorem 5.3",
                    "physical p. 19 Definition 5.8 and Theorem 5.9",
                    "physical pp. 35-36 bibliography proving [Sar99] is a distinct source",
                ],
                "dependencies": [],
                "claim_or_proof_crosswalk_ids": [
                    "CLM-COL-000156",
                    "CLM-COL-000164",
                ],
                "notes": "The frozen route identity is corrupted; this entry is controlled by the PDF content and SRC-COL-000041 adjudication.",
            }
        )

route["sources"].insert(
    -1,
    {
        "source_class": "research_literature",
        "publication_unit_or_source_id": "SRC-COL-000042",
        "exact_locators": [
            "official author preprint physical pp. 3, 5-7, and 24-25",
            "SRC-COL-000042",
        ],
        "relevance_edge": "supplies the genuine 1999 fixed-base Gurevich-pressure, recurrence, Ruelle-Perron-Frobenius, variational, and Gibbs framework",
        "toc_or_section_check": {
            "status": "checked",
            "checked_utc": "2026-08-29T21:07:40Z",
            "relevant_sections": [
                "countable Markov shifts and mixing",
                "Gurevich pressure",
                "recurrence and generalized Ruelle-Perron-Frobenius theory",
                "Gibbs measures",
            ],
        },
        "reading_status": "complete_33_page_author_preprint_visually_reviewed_and_exact_dependency_pages_read",
        "content_loci_read": [
            "physical p. 3 countable Markov shift and mixing",
            "physical pp. 5-6 fixed-base partition and Definition 1",
            "physical p. 7 finite-subshift pressure/variational route",
            "physical p. 18 condition (13), one-sided big images, and Theorem 5",
            "physical pp. 24-25 Gibbs definition and Theorem 8",
        ],
        "dependencies": [],
        "claim_or_proof_crosswalk_ids": [
            "CLM-COL-000156",
            "CLM-COL-000164",
        ],
    },
)
route["refresh_reason"] = (
    "direct reading of raw lines 14012-17437 and independent proof audit "
    "established the survivor coding, positive prefix-stabilization criterion, "
    "typed tropical semigroup obstruction, formal-affine-line map, CRT proof "
    "that each integer valuation stratum and its complement meet every 3-adic "
    "residue ball, and the corrected 1999/2015 Sarig source split"
)
route["anti_loop_note"] = (
    "This route uses the completed canonical corpus and direct Chatnotes intake. "
    "It does not rebuild indexing, use corrupted routing metadata as theorem "
    "evidence, transfer Sarig hypotheses to the positive image, or promote raw "
    "operator, KMS, BCM, motivic, two-coordinate prismatic, or crystalline "
    "proposals without separately typed maps and proofs."
)


# The direct-intake audit itself changed during the audited repair.  Keep the
# machine-readable intake pin and its mathematical summary tied to that exact
# live report rather than to its pre-repair bytes.
chatint15 = intake["CHATINT-COL-000015"]
assert chatint15["report_path"] == (
    "intake/chatnotes/"
    "ZN-SYMMETRIES-TROPICAL-PRISMATIC-SYMBOLIC-DIRECT-LOCATOR-AUDIT-04.md"
)
assert chatint15["report_bytes"] == 12492
assert chatint15["report_sha256"] == (
    "cfb5b4130ad65abddeb7aaa9e7175c63fcce0c80d2c392dfa6bb2e8a74e47580"
)
chatint15["report_bytes"] = 14364
chatint15["report_sha256"] = (
    "da9e24cc4e5fac820d2e9ad773a4bc14baf94237e2408ed95cb52c631fee2b6c"
)
chatint15["programme_status"] = (
    "survivor_coding_prefix_stabilization_and_prismatic_typing_boundary_reconstructed"
)
chatint15["verified_findings"] = [
    "finite_exponent_words_have_one_exact_odd_residue_class_modulo_2_power",
    "predecessor_integrality_is_one_parity_class_for_odd_targets_not_divisible_by_3",
    "rho_is_a_reversed_affine_offset_and_the_forward_intercept_is_beta",
    "rho_cocycle_and_twisted_Leibniz_require_explicit_product_convention",
    "category_algebra_to_object_erasing_degree_monomials_is_not_multiplicative_on_orthogonal_idempotents",
    "translated_quadrants_embed_the_degree_monoid_but_the_path_semigroup_with_zero_map_still_fails_on_distinct_object_identities",
    "Connes_Consani_reduced_square_uses_Conv_Z2_not_raw_Conv_N2_and_warns_about_non_cancellativity",
    "Bhatt_Lurie_WCart_functoriality_requires_formal_scheme_maps_and_g_a_is_not_a_self_map_of_Spf_Z3",
    "the_formal_affine_line_substitution_is_typed_but_CRT_proves_no_clopen_finite_level_3_adic_selector_for_the_integer_valuation_strata",
    "GLSQ_theorems_are_one_variable_cyclotomic_and_do_not_supply_two_independent_Collatz_coordinate_directions",
    "odd_2_adic_survivor_coding_requires_removing_the_backward_orbit_of_minus_one_third_and_is_not_the_metric_completion_of_positive_odds",
    "finite_language_is_full_and_positive_image_is_dense_but_infinite_positivity_is_prefix_lift_stabilization",
    "positive_realizability_is_not_tail_invariant",
    "canonical_prefix_lift_state_determines_the_successor_while_the_printed_congruence_alone_does_not",
    "the_full_shift_pressure_formula_has_finite_domain_exactly_beta_positive_and_Sarig_hypotheses_are_not_transferred_to_the_positive_image",
]


# Fail before writing if the resulting ID sets or critical statements are wrong.
assert sources[0]["next_id"] == "SRC-COL-000043"
assert set(source) >= {f"SRC-COL-{n:06d}" for n in range(1, 43)}
assert any(
    "translated-quadrant shadow/embedding" in item
    for item in route["mathematical_objects"]
)
assert clm159["morphism_refs"] == ["MOR-COL-000049", "MOR-COL-000050"]
assert "MOR-COL-000047" in claim["CLM-COL-000153"]["morphism_refs"]
assert "most" not in morphism["MOR-COL-000047"]["inverse_status"]
assert clm162["formal_status"]["verified_metrics"]["three_adic_selector_CRT_checks"] == 960

payloads = {
    CLAIMS: encode(claims),
    MORPHISMS: encode(morphisms),
    SOURCES: encode(sources),
    TOPICS: encode(topics),
    INTAKE: encode(intakes),
}
for path, payload in payloads.items():
    assert payload.endswith("\n") and "\n\n" not in payload
for path, payload in payloads.items():
    atomic_write(path, payload)

print(
    json.dumps(
        {
            "status": "PASS",
            "source_count": len(source),
            "new_source": "SRC-COL-000042",
            "repaired_source_ids": [
                "SRC-COL-000037",
                "SRC-COL-000038",
                "SRC-COL-000041",
                "SRC-COL-000042",
            ],
            "root_certificate_sha256": ROOT_CERT_HASH,
            "topic_route": route["topic_id"],
        },
        indent=2,
        sort_keys=True,
    )
)
