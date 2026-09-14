#!/usr/bin/env python3
"""Apply the audited ACT42 symbolic-boundary corrections to live JSONL state.

The transformation is deliberately ID-addressed and assertion-heavy.  It
repairs only the records named by the independent mathematical audit and the
three source-route omissions exposed by the hardened state validator.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLAIMS_PATH = ROOT / "state" / "claims.jsonl"
MORPHISMS_PATH = ROOT / "state" / "morphisms.jsonl"
SOURCES_PATH = ROOT / "state" / "source_registry.jsonl"

OLD_CERT = "6f43fa50d7d96feaa592a60e23927ecc30de626087000eaec2049b455f165dc8"
NEW_CERT = "07e736400ffa96b25119e215c444d5305569d0fde83179d71c1c7b33946cd0f7"
CERT_PATH = "certificates/chatnotes_symbolic_completion_checks.py"
CHAPTER = "tex/chapters/04_symbolic_completion_and_geometric_boundaries.tex"


def read_jsonl(path: Path) -> list[dict]:
    records = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            raise AssertionError(f"blank JSONL line at {path}:{line_number}")
        records.append(json.loads(line))
    return records


def write_jsonl(path: Path, records: list[dict]) -> None:
    payload = "\n".join(
        json.dumps(record, ensure_ascii=False, separators=(",", ":"))
        for record in records
    ) + "\n"
    path.write_text(payload, encoding="utf-8", newline="\n")


def index_by(records: list[dict], key: str) -> dict[str, dict]:
    indexed = {record[key]: record for record in records if key in record}
    if len(indexed) != sum(key in record for record in records):
        raise AssertionError(f"duplicate {key}")
    return indexed


def pin_certificate(record: dict, status: str, metrics: dict | None = None) -> None:
    formal = record["formal_status"]
    assert formal["artifact"] == CERT_PATH
    assert formal["artifact_sha256"] in {OLD_CERT, NEW_CERT}
    formal["artifact_sha256"] = NEW_CERT
    formal["status"] = status
    if metrics is not None:
        formal["verified_metrics"] = metrics


def locator(label: str, path: str = CHAPTER) -> dict[str, str]:
    return {"path": path, "label": label}


claims = read_jsonl(CLAIMS_PATH)
claim = index_by(claims, "claim_id")
expected_claims = {f"CLM-COL-{number:06d}" for number in range(151, 165)}
assert expected_claims <= set(claim)
modified_claims = {
    "CLM-COL-000151",
    "CLM-COL-000152",
    "CLM-COL-000153",
    "CLM-COL-000154",
    "CLM-COL-000155",
    "CLM-COL-000156",
    "CLM-COL-000157",
    "CLM-COL-000158",
    "CLM-COL-000159",
    "CLM-COL-000162",
}

pin_certificate(
    claim["CLM-COL-000151"],
    "certificate_pass_32_explicit_first_preimages_self_map_fibre_and_countability_proved_in_TeX_not_independently_certified",
    {"exceptional_preimage_checks": 32},
)

record = claim["CLM-COL-000152"]
record["additional_proof_locators"] = [locator("lem:symbolic-inverse-branch-homeomorphism")]
pin_certificate(
    record,
    "certificate_pass_bounded_word_lift_refinement_checks_inverse_homeomorphism_partition_and_density_proved_in_TeX_not_independently_certified",
    {
        "finite_word_residue_checks": 3905,
        "positive_word_lift_checks": 15620,
        "prefix_refinement_checks": 3900,
    },
)

pin_certificate(
    claim["CLM-COL-000153"],
    "certificate_pass_finite_prefix_kernel_infinite_nested_ball_conjugacy_proved_in_TeX_not_independently_certified",
)

pin_certificate(
    claim["CLM-COL-000154"],
    "certificate_pass_20_constant_one_prefix_witnesses_countability_density_and_exact_shift_image_proved_in_TeX_not_independently_certified",
    {"negative_fixed_point_prefix_checks": 20},
)

record = claim["CLM-COL-000155"]
record["additional_proof_locators"] = [
    locator("construction:symbolic-prefix-refinement-tree")
]
pin_certificate(
    record,
    "certificate_pass_3900_refinements_and_20_nonpositive_limit_witnesses_tree_and_stabilization_proved_in_TeX_not_independently_certified",
    {
        "prefix_refinement_checks": 3900,
        "negative_fixed_point_prefix_checks": 20,
    },
)

record = claim["CLM-COL-000156"]
record["additional_proof_locators"] = [
    locator("eq:symbolic-gurevich-partition"),
    locator("cor:symbolic-positive-image-null"),
]
pin_certificate(
    record,
    "certificate_pass_finite_exact_partition_checks_real_beta_domain_Gibbs_identity_and_nullity_proved_in_TeX_not_independently_certified",
    {
        "pressure_factorization_checks": 48,
        "Bernoulli_normalization_checks": 8,
        "one_symbol_geometric_decomposition_checks": 8,
        "gurevich_based_partition_checks": 192,
    },
)

pin_certificate(
    claim["CLM-COL-000157"],
    "certificate_pass_explicit_counterexample_and_3905_canonical_pair_checks_general_repair_proved_in_TeX",
    {
        "raw_transducer_counterexample_checks": 1,
        "canonical_pair_injectivity_checks": 3905,
    },
)

record = claim["CLM-COL-000158"]
record["statement"] = (
    "The path bidegree deg(p)=(ell(p),A(p)-ell(p)) is a functor from the odd "
    "path category to the one-object additive monoid category N_0^2. With "
    "Q=R_{>=0}^2, the translated-quadrant map j(r,s)=(r,s)+Q injects this "
    "monoid into the multiplicative monoid of Connes-Consani Conv(Z^2) under "
    "Minkowski sum. Over (r,s), r>=1, the word component of the degree fibre "
    "has binomial(r+s-1,r-1) exponent compositions, each with its exact "
    "infinite arithmetic source fibre; over (0,0) every object identity occurs, "
    "and every fibre over (0,s) with s>0 is empty."
)
record["nonclaims"] = [
    "The functor loses objects and exponent order and is not faithful.",
    "Its Newton-polygon image consists only of translated upper quadrants anchored in N_0^2, not all of Conv(Z^2).",
    "No arithmetic-site or Frobenius correspondence is identified with Collatz dynamics.",
]
pin_certificate(
    record,
    "certificate_pass_2_Connes_definition_locator_and_625_translated_quadrant_checks_general_functor_membership_and_fibres_proved_in_TeX",
    {
        "connes_consani_definition_locator_checks": 2,
        "translated_quadrant_monoid_checks": 625,
    },
)

record = claim["CLM-COL-000159"]
record["statement"] = (
    "For any nonzero commutative coefficient semiring, the raw linear assignment "
    "sending every path basis element only to its bidegree monomial is not "
    "multiplicative: distinct object identities multiply to zero in the category "
    "algebra but both map to the target unit. Composing with the translated upper "
    "quadrants j(r,s)=(r,s)+Q preserves the contradiction because the category "
    "zero maps to the empty polygon while both object identities map to Q and "
    "Q+_Mink Q=Q is not empty. The existing typed matrix representation, which "
    "retains object matrix units, is the exact algebraic repair."
)
record["additional_proof_locators"] = [
    locator(
        "prop:weighted-typed-representations",
        "tex/chapters/03_chatnotes_weighted_path_algebra.tex",
    )
]
pin_certificate(
    record,
    "certificate_pass_1_object_idempotent_and_625_translated_quadrant_checks_general_obstruction_proved_in_TeX",
    {
        "object_idempotent_obstruction_checks": 1,
        "translated_quadrant_monoid_checks": 625,
    },
)

record = claim["CLM-COL-000162"]
pin_certificate(
    record,
    "certificate_pass_32_zero_image_obstruction_checks_continuity_substitution_and_point_fibres_proved_in_TeX_not_independently_certified",
    {"formal_point_ring_map_obstruction_checks": 32},
)


morphisms = read_jsonl(MORPHISMS_PATH)
morphism = index_by(morphisms, "morphism_id")
expected_morphisms = {f"MOR-COL-{number:06d}" for number in range(45, 52)}
assert expected_morphisms <= set(morphism)

pin_certificate(
    morphism["MOR-COL-000045"],
    "certificate_pass_32_explicit_first_preimages_general_fibre_and_backward_preservation_proved_in_TeX_not_independently_certified",
    {"exceptional_preimage_checks": 32},
)

record = morphism["MOR-COL-000046"]
record["fibres"] = (
    "For each x in U_w, h_w^(-1)({x})={C_2^|w|(x)}. Equivalently, every "
    "codomain point has exactly one preimage in O_2 under h_w."
)
record["proof_locator"] = locator("lem:symbolic-inverse-branch-homeomorphism")
record["additional_proof_locators"] = [locator("lem:symbolic-Z2-prefix-cylinders")]
pin_certificate(
    record,
    "certificate_pass_3905_word_15620_lift_and_3900_refinement_checks_affine_homeomorphism_and_fibres_proved_in_TeX_not_independently_certified",
    {
        "finite_word_residue_checks": 3905,
        "positive_word_lift_checks": 15620,
        "prefix_refinement_checks": 3900,
    },
)

pin_certificate(
    morphism["MOR-COL-000047"],
    "certificate_pass_finite_prefix_kernel_infinite_nested_ball_homeomorphism_proved_in_TeX_not_independently_certified",
)

record = morphism["MOR-COL-000048"]
record["additional_proof_locators"] = [
    locator("construction:symbolic-prefix-refinement-tree"),
    locator("thm:symbolic-positive-stabilization"),
]
pin_certificate(
    record,
    "certificate_pass_3905_canonical_pairs_and_3900_refinements_tree_and_stabilization_proved_in_TeX_not_independently_certified",
    {
        "canonical_pair_injectivity_checks": 3905,
        "prefix_refinement_checks": 3900,
    },
)

record = morphism["MOR-COL-000049"]
record["fibres"] = (
    "For (r,s) with r>=1, the exponent-word component contains "
    "binomial(r+s-1,r-1) positive compositions of r+s into r parts; every "
    "such word has one infinite positive source class modulo 2^(r+s+1). "
    "Over (0,0) every object identity occurs, while every fibre over (0,s) "
    "with s>0 is empty."
)
pin_certificate(
    record,
    "general_constructive_proof_in_TeX_with_certificate_object_idempotent_countercheck",
    {"object_idempotent_obstruction_checks": 1},
)

record = morphism["MOR-COL-000050"]
record.update(
    {
        "name": "translated_quadrant_Newton_polygon_embedding",
        "domain": "The additive monoid N_0^2.",
        "codomain": "The multiplicative monoid of the Connes-Consani semiring Conv(Z^2), whose multiplication is Minkowski sum.",
        "formula": "With Q=R_{>=0}^2, j(r,s)=(r,s)+Q.",
        "well_definedness": "Every translated quadrant (r,s)+Q is closed, convex, Q-upper, bounded below by itself, and has the integral extreme point (r,s). Since Q+Q=Q, Minkowski sum adds anchors: j(r,s)+_Mink j(r',s')=j(r+r',s+s').",
        "preserved_structure": "The additive monoid law, identity j(0,0)=Q, and the two lattice anchor coordinates.",
        "fibres": "Every translated upper quadrant in the image has the singleton anchor fibre {(r,s)}; every other element of Conv(Z^2) has empty fibre.",
        "inverse_status": "The inverse on the image reads the unique extreme anchor. There is no surjection or semiring isomorphism onto Conv(Z^2).",
        "exceptions": [
            "This is a monoid embedding, not by itself an additive semiring map from the Collatz category algebra.",
            "It supplies no Frobenius correspondence or arithmetic-site identification.",
        ],
    }
)
pin_certificate(
    record,
    "certificate_pass_2_Connes_definition_locator_and_625_translated_quadrant_checks_general_membership_proved_in_TeX",
    {
        "connes_consani_definition_locator_checks": 2,
        "translated_quadrant_monoid_checks": 625,
    },
)

pin_certificate(
    morphism["MOR-COL-000051"],
    "certificate_pass_32_zero_image_obstruction_checks_formal_affine_substitution_continuity_and_point_fibres_proved_in_TeX_not_independently_certified",
    {"formal_point_ring_map_obstruction_checks": 32},
)


sources = read_jsonl(SOURCES_PATH)
source = index_by(sources, "source_id")
route_repairs = {
    "SRC-COL-000034": "PUBUNIT-A0F6B922149DFC4135A8024B",
    "SRC-COL-000035": "PUBUNIT-8187D07E235E5B37C62396CB",
    "SRC-COL-000036": "PUBUNIT-2567B15CF313BDDA475F900E",
}
for source_id, canonical_id in route_repairs.items():
    record = source[source_id]
    assert record["route_integrity"]["canonical_publication_unit_id"] == canonical_id
    assert record["route_ids"] in ([], [canonical_id])
    record["route_ids"] = [canonical_id]


write_jsonl(CLAIMS_PATH, claims)
write_jsonl(MORPHISMS_PATH, morphisms)
write_jsonl(SOURCES_PATH, sources)

print(
    json.dumps(
        {
            "status": "PASS",
            "claims_repaired": sorted(modified_claims),
            "morphisms_repaired": sorted(expected_morphisms),
            "source_routes_repaired": route_repairs,
            "certificate_sha256": NEW_CERT,
        },
        indent=2,
        sort_keys=True,
    )
)
