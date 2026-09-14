from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_jsonl(relative: str) -> list[dict]:
    return [
        json.loads(line)
        for line in (ROOT / relative).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def write_jsonl(relative: str, rows: list[dict]) -> None:
    text = "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in rows)
    (ROOT / relative).write_text(text + "\n", encoding="utf-8")


def pin(path: Path, *, role: str, pdf_pages: int | None = None) -> dict:
    if not path.is_file():
        raise FileNotFoundError(path)
    record: dict[str, object] = {
        "path": path.as_posix(),
        "role": role,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }
    if pdf_pages is not None:
        record["pdf_pages"] = pdf_pages
    return record


def append_numbered(
    relative: str,
    *,
    id_key: str,
    expected_next: str,
    new_next: str,
    records: list[dict],
) -> None:
    rows = load_jsonl(relative)
    headers = [row for row in rows if row.get("record_type") == "ledger_header"]
    if len(headers) != 1 or headers[0].get("next_id") != expected_next:
        raise RuntimeError(f"{relative}: expected unique header next_id {expected_next}")
    existing = {row.get(id_key) for row in rows if row.get(id_key)}
    new_ids = [row[id_key] for row in records]
    if existing.intersection(new_ids):
        raise RuntimeError(f"{relative}: proposed IDs already exist: {sorted(existing.intersection(new_ids))}")
    headers[0]["next_id"] = new_next
    rows.extend(records)
    write_jsonl(relative, rows)


def extend_unique(row: dict, field: str, values: list[object]) -> None:
    existing = list(row.get(field, []))
    for value in values:
        if value not in existing:
            existing.append(value)
    row[field] = existing


def main() -> int:
    raw_note = Path(r"C:\Users\LOCAL_USER\Documents\Obsidian notes\ChatGPT-Branch · Z_n Symmetries of Collatz.md")
    deaconu = Path(r"C:\Users\LOCAL_USER\Documents\arxiv_latex\library\other\Groupoids Associated with Endomorphisms (Valentin Deaconu).pdf")
    huber_wustholz = Path(r"C:\Users\LOCAL_USER\Documents\Papors\OS\Diophantine shimura varieties\Transcendence and Linear Relations of 1-Periods (Annette Huber, Gisbert Wüstholz) (.pdf")
    huber_muller_stach = Path(r"C:\Users\LOCAL_USER\Documents\arxiv_latex\library\other\Periods and Nori Motives (Annette Hube, Stefan Müller-Stach et al.).pdf")
    bvk_tex = Path(r"C:\Users\LOCAL_USER\Documents\arxiv_latex\library\collatz_reconstruction\latex\1009.1900v2\der1motast-pbl.tex")
    bvk_archive = Path(r"C:\Users\LOCAL_USER\Documents\arxiv_latex\library\collatz_reconstruction\source\1009.1900v2.eprint")
    bvk_manifest = Path(r"C:\Users\LOCAL_USER\Documents\arxiv_latex\library\collatz_reconstruction\latex\1009.1900v2\extraction_manifest.json")
    audit = ROOT / "intake/chatnotes/ZN-SYMMETRIES-GROUPOID-MOTIVIC-DIRECT-LOCATOR-AUDIT-06.md"
    certificate = ROOT / "research_companion/certificates/groupoid_motivic_interface_checks.py"

    expected_pins = {
        raw_note: (538005, "9a80f53764a9da42c0f8e0b6d19ce61f978980a448a683b9c45f04038716160d"),
        deaconu: (742789, "63a34e76b5404328d6eb5e7516660af357511d824a6de4b4a6286112e77cfdae"),
        huber_wustholz: (5175455, "1743c141fd0078e7ac19805a5174078a26551d978bf6d1cb623bf3b237da3d17"),
        huber_muller_stach: (1855231, "6d08014f21a616abb4ba7e177effad4d15e4a215b0f234ce3a4605c20a02b731"),
        bvk_tex: (564248, "f884b90f3760ac666c1047a975e6788dfc02a1eb7f047e8eae8b57df6f013c18"),
        bvk_archive: (171937, "dace798cce0445edae8ed871d9633c6aab87dacf2182e8dcc8fe726ca2b59aa5"),
        bvk_manifest: (1180, "38fdbdf2d62fe1d43dfb2d76ac4c32a37bfb2a0b2e9f155b97b4c8aef4caabb8"),
    }
    for path, expected in expected_pins.items():
        actual = (path.stat().st_size, sha256(path)) if path.is_file() else None
        if actual != expected:
            raise RuntimeError(f"source identity mismatch: {path}: {actual} != {expected}")

    sources = [
        {
            "record_type": "source_document",
            "schema_version": "1.0",
            "source_id": "SRC-COL-000046",
            "authors": ["Valentin Deaconu"],
            "title": "Groupoids Associated with Endomorphisms",
            "bibliographic_identity": {
                "journal": "Transactions of the American Mathematical Society",
                "volume": "347",
                "issue": "5",
                "pages": "1779-1786",
                "publication_year": 1995,
            },
            "manifestations": [pin(deaconu, role="controlling_PDF", pdf_pages=9)],
            "route_ids": ["PUBUNIT-EF51A30466D25AFE9C75C974"],
            "route_integrity": {
                "status": "canonical_title_and_manifestation_match",
                "canonical_publication_unit_id": "PUBUNIT-EF51A30466D25AFE9C75C974",
            },
            "reading": {
                "status": "complete_for_triple_groupoid_and_topological_hypothesis_boundary",
                "locators": [
                    "physical PDF pp. 2-4, printed pp. 1779-1781",
                    "Proposition on the r-discrete locally compact Hausdorff groupoid and counting Haar system",
                    "Definition requiring a compact Hausdorff space and a covering self-map",
                ],
                "source_objects": {
                    "set_theoretic_prototype": "triples (x,k,y) represented by equal forward iterates",
                    "topological_hypotheses": "compact Hausdorff unit space and covering self-map",
                },
            },
            "audit": {
                "path": "intake/chatnotes/ZN-SYMMETRIES-GROUPOID-MOTIVIC-DIRECT-LOCATOR-AUDIT-06.md",
                "status": "content_read_and_hypothesis_crosswalked",
            },
            "nonclaims": [
                "Deaconu's compact-covering theorem is not applied to the noncompact discrete positive-odd set.",
                "The source does not supply the Collatz arithmetic cocycles or the path embedding constructed here.",
            ],
        },
        {
            "record_type": "source_document",
            "schema_version": "1.0",
            "source_id": "SRC-COL-000047",
            "authors": ["Annette Huber", "Gisbert Wüstholz"],
            "title": "Transcendence and Linear Relations of 1-Periods",
            "bibliographic_identity": {
                "series": "Cambridge Tracts in Mathematics",
                "volume": "227",
                "publisher": "Cambridge University Press",
                "publication_year": 2022,
            },
            "manifestations": [pin(huber_wustholz, role="controlling_book_PDF", pdf_pages=265)],
            "route_ids": ["PUBUNIT-738F0D16B49618236C67D652"],
            "route_integrity": {
                "status": "canonical_title_and_manifestation_match",
                "canonical_publication_unit_id": "PUBUNIT-738F0D16B49618236C67D652",
            },
            "reading": {
                "status": "complete_for_1_motive_morphism_Kummer_character_and_1_period_dependencies",
                "locators": [
                    "physical PDF p. 90: Definition 8.1",
                    "physical PDF pp. 116-117: Section 10.2 and the Kummer motive",
                    "physical PDF pp. 119-120: Theorem 10.4 and the torus character (x,y)->x^n y^m",
                    "physical PDF p. 137: Proposition 12.10",
                ],
                "source_objects": {
                    "one_motive": "complex [L->G] with morphisms of complexes",
                    "Kummer_motive": "[Z -> G_m], 1 maps to alpha, with path-selected logarithm",
                    "period_scope": "the 1-periods are exactly periods of 1-motives",
                },
            },
            "audit": {
                "path": "intake/chatnotes/ZN-SYMMETRIES-GROUPOID-MOTIVIC-DIRECT-LOCATOR-AUDIT-06.md",
                "status": "content_read_and_concrete_square_scope_crosswalked",
            },
            "nonclaims": [
                "The source does not define the Collatz-specific torus point, characters, or path-indexed Kummer squares.",
                "Its general period theorems do not create a Collatz endpoint theorem.",
            ],
        },
        {
            "record_type": "source_document",
            "schema_version": "1.0",
            "source_id": "SRC-COL-000048",
            "authors": ["Annette Huber", "Stefan Müller-Stach"],
            "title": "Periods and Nori Motives",
            "bibliographic_identity": {
                "edition": "annotated version of 1 July 2025",
                "publisher": "Springer",
                "publication_year": 2025,
            },
            "manifestations": [pin(huber_muller_stach, role="controlling_annotated_book_PDF", pdf_pages=402)],
            "route_ids": ["PUBUNIT-499097DAF18CF6AEE1056A50"],
            "route_integrity": {
                "status": "canonical_title_and_manifestation_match",
                "canonical_publication_unit_id": "PUBUNIT-499097DAF18CF6AEE1056A50",
            },
            "reading": {
                "status": "complete_for_effective_Nori_pair_vertex_and_edge_types",
                "locators": [
                    "physical PDF p. 231: Definition 9.1.1",
                    "functoriality edge f*: (X',Y',i)->(X,Y,i)",
                    "coboundary edge (Y,Z,i)->(X,Y,i+1)",
                ],
                "source_objects": {
                    "vertices": "triples (X,Y,i)",
                    "primitive_edges": "contravariant functoriality for a map of pairs and coboundary for a nested triple",
                },
            },
            "audit": {
                "path": "intake/chatnotes/ZN-SYMMETRIES-GROUPOID-MOTIVIC-DIRECT-LOCATOR-AUDIT-06.md",
                "status": "content_read_and_edge_direction_crosswalked",
            },
            "nonclaims": [
                "Concatenation of singular paths is not a third primitive edge in Definition 9.1.1.",
                "The source does not construct a universal Collatz path-indexed Nori category.",
            ],
        },
        {
            "record_type": "source_document",
            "schema_version": "1.0",
            "source_id": "SRC-COL-000049",
            "authors": ["Luca Barbieri-Viale", "Bruno Kahn"],
            "title": "On the Derived Category of 1-Motives",
            "bibliographic_identity": {
                "arxiv_version_id": "1009.1900v2",
                "arxiv_record": "https://arxiv.org/abs/1009.1900",
                "journal": "Astérisque",
                "volume": "381",
                "publication_year": 2016,
            },
            "manifestations": [
                pin(bvk_tex, role="controlling_versioned_arXiv_source_TeX"),
                pin(bvk_archive, role="versioned_arXiv_source_archive"),
                pin(bvk_manifest, role="source_extraction_manifest"),
            ],
            "route_ids": ["PUBUNIT-663759AB2A92FA11265DB7BC"],
            "route_integrity": {
                "status": "canonical_publication_unit_routed_and_exact_v2_source_TeX_acquired",
                "canonical_publication_unit_id": "PUBUNIT-663759AB2A92FA11265DB7BC",
                "controlling_arxiv_version_id": "1009.1900v2",
                "frozen_ledgers_mutated": False,
            },
            "reading": {
                "status": "complete_for_Deligne_1_motive_morphism_embedding_and_LAlb_dependencies",
                "locators": [
                    "source TeX lines 728-750: Deligne 1-motives and commutative-square morphisms",
                    "source TeX lines 1736-1751: fully faithful triangulated functor and curve-generated image",
                    "source TeX lines 3796-3800: definition of LAlb",
                ],
                "source_objects": {
                    "morphism": "commutative square between [L->G] and [L'->G']",
                    "derived_embedding": "D^b of 1-motives into effective étale motives with dimension-at-most-one image",
                },
            },
            "audit": {
                "path": "intake/chatnotes/ZN-SYMMETRIES-GROUPOID-MOTIVIC-DIRECT-LOCATOR-AUDIT-06.md",
                "status": "versioned_source_TeX_content_read_and_concrete_scope_crosswalked",
            },
            "nonclaims": [
                "The source supplies general 1-motive machinery, not the point (2,3), the Collatz characters, or a curve realizing them.",
                "No LAlb computation for a Collatz-specific object is inferred.",
            ],
        },
    ]
    append_numbered(
        "state/source_registry.jsonl",
        id_key="source_id",
        expected_next="SRC-COL-000046",
        new_next="SRC-COL-000050",
        records=sources,
    )

    claims = [
        {
            "record_type": "claim",
            "schema_version": "1.0",
            "claim_id": "CLM-COL-000174",
            "claim_type": "sourced_theorem_and_hypothesis_boundary",
            "status": "verified_from_primary_PDF",
            "statement": "Deaconu's triple construction is an r-discrete locally compact Hausdorff groupoid with counting Haar system under the stated compact-Hausdorff self-covering hypotheses. Those hypotheses do not hold for the discrete positive-odd Collatz map, so the source theorem is not transferred to that space.",
            "source_ids": ["SRC-COL-000046"],
            "dependencies": [],
            "source_locators": ["physical PDF pp. 2-4, printed pp. 1779-1781"],
            "statement_locator": {
                "path": "tex/chapters/05_chatnotes_groupoid_and_motivic_interfaces.tex",
                "label": "sec:chatnotes-groupoid-motivic",
            },
            "nonclaims": ["This record does not assert that Deaconu's theorem applies to the positive-odd map."],
        },
        {
            "record_type": "claim",
            "schema_version": "1.0",
            "claim_id": "CLM-COL-000175",
            "claim_type": "sourced_definition_and_theorem_scope",
            "status": "verified_from_primary_book_and_versioned_source_TeX",
            "statement": "A Deligne 1-motive is a complex [L->G], its morphisms are commutative squares, Kummer logarithms arise from [Z->G_m], and every 1-period is a period of a 1-motive. The cited sources supply this framework but not the Collatz-specific torus point or characters.",
            "source_ids": ["SRC-COL-000047", "SRC-COL-000049"],
            "dependencies": [],
            "source_locators": [
                "Huber-Wüstholz physical PDF pp. 90, 116-120, 137",
                "Barbieri-Viale-Kahn source TeX lines 728-750, 1736-1751, 3796-3800",
            ],
            "statement_locator": {
                "path": "research_companion/chapters/03_arithmetic_groupoids_and_toric_period_morphisms.tex",
                "label": "thm:kummer-character-morphisms",
            },
            "nonclaims": ["The general framework does not itself construct any Collatz-specific 1-motive morphism."],
        },
        {
            "record_type": "claim",
            "schema_version": "1.0",
            "claim_id": "CLM-COL-000176",
            "claim_type": "sourced_definition_and_direction_boundary",
            "status": "verified_from_primary_PDF",
            "statement": "In the effective Nori diagram a vertex is (X,Y,i); a map of pairs produces the contravariant edge f*:(X',Y',i)->(X,Y,i), and a nested triple produces the coboundary edge (Y,Z,i)->(X,Y,i+1). Path concatenation without such data is not an edge of either type.",
            "source_ids": ["SRC-COL-000048"],
            "dependencies": [],
            "source_locators": ["physical PDF p. 231, Definition 9.1.1"],
            "statement_locator": {
                "path": "research_companion/chapters/03_arithmetic_groupoids_and_toric_period_morphisms.tex",
                "label": "thm:cayley-pair-isomorphism",
            },
            "nonclaims": ["This is not a universal Collatz path-indexed Nori category."],
        },
        {
            "record_type": "claim",
            "schema_version": "1.0",
            "claim_id": "CLM-COL-000177",
            "claim_type": "independent_constructive_theorem",
            "status": "proved",
            "statement": "The discrete arithmetic orbit triples form a countable Hausdorff locally compact étale groupoid with counting Haar system. The representative-independent exponent-sum difference yields exact Z^2 and real cocycles; the path functor J is injective, recovers the path bidegree and logarithmic weight, embeds the path algebra by point masses, and induces full and reduced gauge and time actions.",
            "source_ids": ["SRC-COL-000046"],
            "dependencies": ["CLM-COL-000142", "CLM-COL-000143", "CLM-COL-000174"],
            "local_source_refs": ["CHATINT-COL-000017"],
            "proof_locator": {
                "path": "research_companion/chapters/03_arithmetic_groupoids_and_toric_period_morphisms.tex",
                "label": "thm:path-to-arithmetic-groupoid",
            },
            "additional_proof_locators": [
                {
                    "path": "research_companion/chapters/03_arithmetic_groupoids_and_toric_period_morphisms.tex",
                    "label": "thm:arithmetic-groupoid-cocycles",
                }
            ],
            "formal_status": {
                "status": "general_proof_plus_bounded_exact_certificate",
                "artifact": "research_companion/certificates/groupoid_motivic_interface_checks.py",
                "artifact_sha256": sha256(certificate),
            },
            "nonclaims": ["No amenability or equality of full and reduced completions is asserted."],
        },
        {
            "record_type": "claim",
            "schema_version": "1.0",
            "claim_id": "CLM-COL-000178",
            "claim_type": "independent_constructive_theorem_and_explicit_obstructions",
            "status": "proved",
            "statement": "The displayed 3-adic branches are clopen-domain homeomorphisms and generate a Hausdorff second-countable locally compact étale germ groupoid with compact unit space. The actual orbit-prefix formula defines an injective cocycle-preserving functor Xi from the arithmetic groupoid. The raw l2(O) isometry fails at g_1(1)=2, and left prefixing by a nonempty word is not an algebra endomorphism.",
            "source_ids": [],
            "dependencies": ["CLM-COL-000177"],
            "local_source_refs": ["CHATINT-COL-000017"],
            "proof_locator": {
                "path": "research_companion/chapters/03_arithmetic_groupoids_and_toric_period_morphisms.tex",
                "label": "thm:three-adic-germ-functor",
            },
            "additional_proof_locators": [
                {
                    "path": "research_companion/chapters/03_arithmetic_groupoids_and_toric_period_morphisms.tex",
                    "label": "prop:three-adic-l2-restriction-failure",
                }
            ],
            "formal_status": {
                "status": "general_proof_plus_bounded_exact_certificate",
                "artifact": "research_companion/certificates/groupoid_motivic_interface_checks.py",
                "artifact_sha256": sha256(certificate),
            },
            "nonclaims": [
                "Xi is not promoted to a point-mass convolution-algebra embedding into the nondiscrete germ groupoid.",
                "No unspecified crossed-product identification is asserted.",
            ],
        },
        {
            "record_type": "claim",
            "schema_version": "1.0",
            "claim_id": "CLM-COL-000179",
            "claim_type": "independent_constructive_theorem",
            "status": "proved",
            "statement": "The arithmetic and degree tori are related by the explicit unimodular isomorphism Phi(x,y)=(x/y,x) with displayed inverse and inverse lattice matrices. It intertwines the two path characters, gives an isomorphism of the two rank-one-to-rank-two 1-motives, and each path character gives a commutative Kummer-motive square and the exact path-selected logarithmic period. The Cartier dual map is (r,s)->2^r3^s.",
            "source_ids": ["SRC-COL-000047", "SRC-COL-000049"],
            "dependencies": ["CLM-COL-000143", "CLM-COL-000175"],
            "local_source_refs": ["CHATINT-COL-000017"],
            "proof_locator": {
                "path": "research_companion/chapters/03_arithmetic_groupoids_and_toric_period_morphisms.tex",
                "label": "thm:torus-coordinate-isomorphism",
            },
            "additional_proof_locators": [
                {
                    "path": "research_companion/chapters/03_arithmetic_groupoids_and_toric_period_morphisms.tex",
                    "label": "thm:kummer-character-morphisms",
                }
            ],
            "formal_status": {
                "status": "general_proof_plus_bounded_exact_certificate",
                "artifact": "research_companion/certificates/groupoid_motivic_interface_checks.py",
                "artifact_sha256": sha256(certificate),
            },
            "nonclaims": ["No curve realization or LAlb computation is claimed for these concrete 1-motives."],
        },
        {
            "record_type": "claim",
            "schema_version": "1.0",
            "claim_id": "CLM-COL-000180",
            "claim_type": "independent_constructive_theorem",
            "status": "proved",
            "statement": "Over Q(i), the Cayley transform is an explicit isomorphism of the arctangent pair with a G_m Kummer pair and pulls dlog back to 2i dz/(1+z^2), producing the Nori edge in the exact contravariant direction. Over Q the arctangent differential is regular at infinity. For composable paths, torus-character multiplication gives a factorization of 1-motives and an actual multiplication map of pairs whose dlog pullback proves period additivity.",
            "source_ids": ["SRC-COL-000047", "SRC-COL-000048", "SRC-COL-000049"],
            "dependencies": ["CLM-COL-000169", "CLM-COL-000176", "CLM-COL-000179"],
            "local_source_refs": ["CHATINT-COL-000017"],
            "proof_locator": {
                "path": "research_companion/chapters/03_arithmetic_groupoids_and_toric_period_morphisms.tex",
                "label": "thm:cayley-pair-isomorphism",
            },
            "additional_proof_locators": [
                {
                    "path": "research_companion/chapters/03_arithmetic_groupoids_and_toric_period_morphisms.tex",
                    "label": "prop:kummer-character-multiplication",
                }
            ],
            "formal_status": {
                "status": "general_proof_plus_bounded_exact_certificate",
                "artifact": "research_companion/certificates/groupoid_motivic_interface_checks.py",
                "artifact_sha256": sha256(certificate),
            },
            "nonclaims": [
                "The Cayley marked point is not identified with the positive rational Collatz Kummer point.",
                "No universal path-indexed Nori category or motivic Galois action is asserted.",
            ],
        },
        {
            "record_type": "claim",
            "schema_version": "1.0",
            "claim_id": "CLM-COL-000181",
            "claim_type": "verified_raw_chronology_audit_and_retraction_boundary",
            "status": "verified_and_propagated",
            "statement": "Physical lines 11088-14011 contain exact bidegrees, characters, arctangent integrals, and 3-adic branch maps, but do not prove the printed unnamed groupoid arrows, path-concatenation Nori arrows, l2(O) isometries, prefix endomorphism, crossed-product equality, equilibrium package, or wider motivic and arithmetic identifications. The surviving mathematics is reconstructed by CLM-COL-000177 through CLM-COL-000180.",
            "source_ids": ["SRC-COL-000046", "SRC-COL-000047", "SRC-COL-000048", "SRC-COL-000049"],
            "dependencies": ["CLM-COL-000177", "CLM-COL-000178", "CLM-COL-000179", "CLM-COL-000180"],
            "local_source_refs": ["CHATINT-COL-000017"],
            "source_locators": [
                "raw Z_n Symmetries physical lines 11088-14011",
                "intake/chatnotes/ZN-SYMMETRIES-GROUPOID-MOTIVIC-DIRECT-LOCATOR-AUDIT-06.md",
            ],
            "statement_locator": {
                "path": "tex/chapters/05_chatnotes_groupoid_and_motivic_interfaces.tex",
                "label": "sec:chatnotes-groupoid-motivic",
            },
            "nonclaims": ["The absence of maps in this interval is not a claim that such constructions are impossible elsewhere."],
        },
    ]
    append_numbered(
        "state/claims.jsonl",
        id_key="claim_id",
        expected_next="CLM-COL-000174",
        new_next="CLM-COL-000182",
        records=claims,
    )

    morphisms = [
        {
            "record_type": "morphism",
            "schema_version": "1.0",
            "morphism_id": "MOR-COL-000055",
            "name": "arithmetic_groupoid_bidegree_cocycle",
            "domain": "The discrete arithmetic orbit groupoid G_arith with arrows (x,k,y).",
            "codomain": "The one-object additive groupoid Z^2.",
            "formula": "D(x,k,y)=(-k,-c_a(x,k,y)+k), where c_a=S_m a(x)-S_n a(y) for any representative k=m-n with C^m x=C^n y.",
            "well_definedness": "Common-future extension adds the same Birkhoff sum to both terms of c_a; common-middle alignment proves additivity.",
            "preserved_structure": "Units, inverses, groupoid products, and the path bidegree under J.",
            "fibres": "D^{-1}(r,s) consists exactly of arrows with k=-r and c_a=-r-s.",
            "inverse_status": "No inverse is claimed; the displayed fibre equations are exact.",
            "exceptions": ["The map does not determine source and range units."],
            "claim_refs": ["CLM-COL-000177"],
            "source_refs": [],
            "proof_locator": {
                "path": "research_companion/chapters/03_arithmetic_groupoids_and_toric_period_morphisms.tex",
                "label": "thm:arithmetic-groupoid-cocycles",
            },
            "formal_status": {"status": "general_proof_plus_bounded_certificate", "artifact": "research_companion/certificates/groupoid_motivic_interface_checks.py"},
        },
        {
            "record_type": "morphism",
            "schema_version": "1.0",
            "morphism_id": "MOR-COL-000056",
            "name": "arithmetic_groupoid_real_weight_cocycle",
            "domain": "The discrete arithmetic orbit groupoid G_arith.",
            "codomain": "The one-object additive groupoid R.",
            "formula": "delta_G(x,k,y)=-c_a(x,k,y) log 2+k log 3.",
            "well_definedness": "It is a real linear combination of the independently proved additive cocycles c_a and k.",
            "preserved_structure": "Units, inverses, groupoid products, and logarithmic path weights under J.",
            "fibres": "The fibre at t is the exact set of arrows satisfying -c_a log 2+k log 3=t.",
            "inverse_status": "No inverse is claimed; multiplicative independence of 2 and 3 makes (k,c_a) recoverable from delta only on its discrete image after both integer coordinates are known to exist.",
            "exceptions": ["The real value alone does not record source and range."],
            "claim_refs": ["CLM-COL-000177"],
            "source_refs": [],
            "proof_locator": {
                "path": "research_companion/chapters/03_arithmetic_groupoids_and_toric_period_morphisms.tex",
                "label": "thm:arithmetic-groupoid-cocycles",
            },
            "formal_status": {"status": "general_proof_plus_bounded_certificate", "artifact": "research_companion/certificates/groupoid_motivic_interface_checks.py"},
        },
        {
            "record_type": "morphism",
            "schema_version": "1.0",
            "morphism_id": "MOR-COL-000057",
            "name": "positive_odd_path_to_arithmetic_groupoid_embedding",
            "domain": "The positive-odd first-return path category E_C in target-left composition convention.",
            "codomain": "The groupoid category underlying G_arith.",
            "formula": "J(p)=(target(p),-ell(p),source(p)).",
            "well_definedness": "The representative (0,ell(p)) satisfies C^0(target)=C^ell(source); target-left composition maps to groupoid multiplication.",
            "preserved_structure": "Sources, targets, identities, composition, bidegree, logarithmic weight, and category-algebra multiplication by point masses.",
            "fibres": "Every nonempty fibre is a singleton because source and length determine a deterministic path.",
            "inverse_status": "On the image, recover the path from source s(J(p)) and length -k; arrows outside the image have no path preimage.",
            "exceptions": ["J is not asserted to be essentially surjective onto G_arith."],
            "claim_refs": ["CLM-COL-000177"],
            "source_refs": [],
            "component_morphism_refs": ["MOR-COL-000055", "MOR-COL-000056"],
            "proof_locator": {
                "path": "research_companion/chapters/03_arithmetic_groupoids_and_toric_period_morphisms.tex",
                "label": "thm:path-to-arithmetic-groupoid",
            },
            "formal_status": {"status": "general_proof_plus_bounded_certificate", "artifact": "research_companion/certificates/groupoid_motivic_interface_checks.py"},
        },
        {
            "record_type": "morphism",
            "schema_version": "1.0",
            "morphism_id": "MOR-COL-000058",
            "name": "arithmetic_groupoid_to_three_adic_germ_functor",
            "domain": "The discrete arithmetic orbit groupoid G_arith.",
            "codomain": "The germ groupoid H_3 of the pseudogroup generated by the clopen 3-adic branch homeomorphisms.",
            "formula": "Xi(x,m-n,y)=[h_{p_m(x)}^{-1} composed with h_{p_n(y)},y].",
            "well_definedness": "Common-future affine factors cancel; common-middle alignment proves functoriality; actual orbit words ensure the germ is defined at y.",
            "preserved_structure": "Object inclusion, source, range, identities, products, inverses, bidegree valuations, and the real logarithmic cocycle.",
            "fibres": "Every fibre is empty or a singleton: source, range, and minus the 3-adic valuation of the affine slope recover (x,m-n,y).",
            "inverse_status": "The inverse on the image reads source and range from the germ and k=-nu_3(slope); no inverse is claimed outside the image.",
            "exceptions": ["A singleton germ is generally not open, so Xi does not give a point-mass map into C_c(H_3)."],
            "claim_refs": ["CLM-COL-000178"],
            "source_refs": [],
            "component_morphism_refs": ["MOR-COL-000055", "MOR-COL-000056"],
            "proof_locator": {
                "path": "research_companion/chapters/03_arithmetic_groupoids_and_toric_period_morphisms.tex",
                "label": "thm:three-adic-germ-functor",
            },
            "formal_status": {"status": "general_proof_plus_bounded_certificate", "artifact": "research_companion/certificates/groupoid_motivic_interface_checks.py"},
        },
        {
            "record_type": "morphism",
            "schema_version": "1.0",
            "morphism_id": "MOR-COL-000059",
            "name": "arithmetic_to_degree_torus_isomorphism",
            "domain": "T_ar=(G_m)^2 with coordinates (x,y).",
            "codomain": "T_deg=(G_m)^2 with coordinates (lambda,mu).",
            "formula": "Phi(x,y)=(x/y,x).",
            "well_definedness": "Both coordinates are regular units on the torus and direct substitution gives Phi^{-1}(lambda,mu)=(mu,mu/lambda).",
            "preserved_structure": "Torus multiplication, the lattice isomorphism, the base point (2,3)->(2/3,2), and psi_p composed with Phi=chi_p.",
            "fibres": "Every fibre is the singleton {(mu,mu/lambda)}.",
            "inverse_status": "Global inverse Phi^{-1}(lambda,mu)=(mu,mu/lambda); the two displayed integer exponent matrices multiply to the identity.",
            "exceptions": [],
            "claim_refs": ["CLM-COL-000179"],
            "source_refs": ["SRC-COL-000047", "SRC-COL-000049"],
            "proof_locator": {
                "path": "research_companion/chapters/03_arithmetic_groupoids_and_toric_period_morphisms.tex",
                "label": "thm:torus-coordinate-isomorphism",
            },
            "formal_status": {"status": "general_proof_plus_bounded_certificate", "artifact": "research_companion/certificates/groupoid_motivic_interface_checks.py"},
        },
        {
            "record_type": "morphism",
            "schema_version": "1.0",
            "morphism_id": "MOR-COL-000060",
            "name": "path_character_Kummer_one_motive_morphism",
            "domain": "M_ar=[Z->(G_m)^2], n maps to (2^n,3^n).",
            "codomain": "K(alpha_p)=[Z->G_m], n maps to alpha_p^n with alpha_p=2^A 3^{-ell}.",
            "formula": "(id_Z,chi_p), with chi_p(x,y)=x^A y^{-ell}.",
            "well_definedness": "The square commutes because chi_p(2^n,3^n)=alpha_p^n for every n in Z.",
            "preserved_structure": "Lattice maps, torus group law, the selected positive-real path, and the logarithmic period A log 2-ell log 3.",
            "fibres": "On the torus, chi_p^{-1}(z) is the character fibre x^A y^{-ell}=z; on the lattice the map is the identity.",
            "inverse_status": "No inverse is claimed unless the character exponent is a primitive rank-one direct factor; the exact kernel subtorus is retained.",
            "exceptions": ["The logarithm branch is fixed by the displayed positive-real path."],
            "claim_refs": ["CLM-COL-000179"],
            "source_refs": ["SRC-COL-000047", "SRC-COL-000049"],
            "component_morphism_refs": ["MOR-COL-000059"],
            "proof_locator": {
                "path": "research_companion/chapters/03_arithmetic_groupoids_and_toric_period_morphisms.tex",
                "label": "thm:kummer-character-morphisms",
            },
            "formal_status": {"status": "general_proof_plus_bounded_certificate", "artifact": "research_companion/certificates/groupoid_motivic_interface_checks.py"},
        },
        {
            "record_type": "morphism",
            "schema_version": "1.0",
            "morphism_id": "MOR-COL-000061",
            "name": "Cayley_isomorphism_of_arctangent_and_Kummer_pairs",
            "domain": "(P^1_{Q(i)} minus {i,-i},{0,r}).",
            "codomain": "(G_{m,Q(i)},{1,(1+ir)/(1-ir)}).",
            "formula": "kappa(z)=(1+iz)/(1-iz).",
            "well_definedness": "The deleted points map to 0 and infinity, the marked points map as displayed, and solving for z gives (w-1)/(i(w+1)).",
            "preserved_structure": "Algebraic-pair structure and logarithmic differential: kappa^*(dw/w)=2i dz/(1+z^2).",
            "fibres": "Every fibre is a singleton on the declared open curves.",
            "inverse_status": "Global inverse kappa^{-1}(w)=(w-1)/(i(w+1)).",
            "exceptions": ["The isomorphism is over Q(i); the rational arctangent period is separately represented over Q."],
            "claim_refs": ["CLM-COL-000180"],
            "source_refs": ["SRC-COL-000048"],
            "proof_locator": {
                "path": "research_companion/chapters/03_arithmetic_groupoids_and_toric_period_morphisms.tex",
                "label": "thm:cayley-pair-isomorphism",
            },
            "formal_status": {"status": "general_proof_plus_bounded_certificate", "artifact": "research_companion/certificates/groupoid_motivic_interface_checks.py"},
        },
        {
            "record_type": "morphism",
            "schema_version": "1.0",
            "morphism_id": "MOR-COL-000062",
            "name": "multiplication_map_for_composable_Kummer_characters",
            "domain": "N_{p,q}=[Z->G_m^2], n maps to (alpha_p^n,alpha_q^n), together with the marked pair (G_m^2,{(1,1),(alpha_p,alpha_q)}).",
            "codomain": "K(alpha_p alpha_q)=[Z->G_m] and the marked pair (G_m,{1,alpha_p alpha_q}).",
            "formula": "(id_Z,m) with m(z_1,z_2)=z_1 z_2.",
            "well_definedness": "Multiplication maps both marked points correctly and m(alpha_p^n,alpha_q^n)=(alpha_p alpha_q)^n for every n.",
            "preserved_structure": "Group law, lattice map, character composition, marked pairs, contravariant Nori functoriality, and dlog additivity.",
            "fibres": "The torus fibre over z is {(z_1,z_2):z_1 z_2=z}; the marked-point images are exact.",
            "inverse_status": "No global inverse is claimed; sections z->(z,1) and z->(1,z) do not invert multiplication on all of G_m^2.",
            "exceptions": ["The induced Nori edge points from the codomain pair to the domain pair because cohomology is contravariant."],
            "claim_refs": ["CLM-COL-000180"],
            "source_refs": ["SRC-COL-000048"],
            "component_morphism_refs": ["MOR-COL-000060"],
            "proof_locator": {
                "path": "research_companion/chapters/03_arithmetic_groupoids_and_toric_period_morphisms.tex",
                "label": "prop:kummer-character-multiplication",
            },
            "formal_status": {"status": "general_proof_plus_bounded_certificate", "artifact": "research_companion/certificates/groupoid_motivic_interface_checks.py"},
        },
    ]
    append_numbered(
        "state/morphisms.jsonl",
        id_key="morphism_id",
        expected_next="MOR-COL-000055",
        new_next="MOR-COL-000063",
        records=morphisms,
    )

    intake = {
        "record_type": "chatnotes_locator_audit",
        "schema_version": "1.0",
        "intake_id": "CHATINT-COL-000017",
        "source_intake_id": "CHATINT-COL-000001",
        "audit_scope": "raw_lines_11088_14011_complete_direct_read_groupoid_three_adic_one_motive_and_Nori_interfaces",
        "primary_source_ids": ["SRC-COL-000046", "SRC-COL-000047", "SRC-COL-000048", "SRC-COL-000049"],
        "admission_status": "no_mathematical_admission",
        "separate_ledger_status": "sourced_boundaries_independent_theorems_explicit_obstructions_and_nonclaims_recorded_separately",
        "programme_status": "extends_PRG_COL_0001_and_PRG_COL_0002_without_creating_a_folder_based_programme",
        "report_path": "intake/chatnotes/ZN-SYMMETRIES-GROUPOID-MOTIVIC-DIRECT-LOCATOR-AUDIT-06.md",
        "report_bytes": audit.stat().st_size,
        "report_sha256": sha256(audit),
        "certificate_path": "research_companion/certificates/groupoid_motivic_interface_checks.py",
        "certificate_bytes": certificate.stat().st_size,
        "certificate_sha256": sha256(certificate),
        "source_bytes": raw_note.stat().st_size,
        "source_physical_lines": 17437,
        "source_sha256": sha256(raw_note),
        "verified_findings": [
            "the_raw_bidegree_characters_arctangent_integral_and_three_adic_branch_maps_survive_at_their_displayed_scope",
            "the_discrete_arithmetic_groupoid_and_its_two_cocycles_require_and_receive_independent_proofs",
            "the_exact_arithmetic_to_three_adic_germ_functor_is_injective_and_recovers_both_cocycles_from_affine_slope_valuations",
            "the_printed_l2_positive_odd_isometry_fails_on_delta_1_and_left_prefixing_is_not_an_algebra_endomorphism",
            "the_two_torus_coordinates_are_related_by_a_proved_unimodular_isomorphism_and_actual_one_motive_squares",
            "Cayley_and_multiplication_maps_of_pairs_supply_the_exact_contravariant_Nori_edges_missing_from_the_raw_chronology",
        ],
        "nonclaims": [
            "The raw chronology does not prove a crossed-product equality, equilibrium classification, motivic Galois action, local-factor package, or Collatz endpoint.",
            "The absence of the required maps in this interval is not a proof that such constructions are impossible elsewhere.",
        ],
    }
    append_numbered(
        "state/chatnotes_intake.jsonl",
        id_key="intake_id",
        expected_next="CHATINT-COL-000017",
        new_next="CHATINT-COL-000018",
        records=[intake],
    )

    topic_rows = load_jsonl("state/topic_routes.jsonl")
    if any(row.get("topic_id") == "TOPIC-COL-GROUPOID-MOTIVIC-0004" for row in topic_rows):
        raise RuntimeError("topic route TOPIC-COL-GROUPOID-MOTIVIC-0004 already exists")
    topic_rows.append(
        {
            "schema_version": 1,
            "topic_id": "TOPIC-COL-GROUPOID-MOTIVIC-0004",
            "topic": "Collatz arithmetic orbit groupoids, 3-adic germ maps, torus characters, 1-motives, Cayley pairs, and exact Nori arrows",
            "workspace": ROOT.as_posix(),
            "corpus_entrypoint": "C:/Users/LOCAL_USER/Documents/Papors/Chatnotes/Zeta-Function-Foundation/config/literature_index_entrypoint.json",
            "updated_utc": "2026-08-30T13:30:00Z",
            "mathematical_objects": [
                "positive-odd first-return paths and exponent Birkhoff sums",
                "discrete arithmetic orbit groupoid and two exact cocycles",
                "clopen 3-adic affine branch pseudogroup and germ groupoid",
                "injective arithmetic-to-germ functor and rational slope valuations",
                "unimodular arithmetic-degree torus coordinate change",
                "Kummer 1-motive character squares and Cartier dual",
                "Cayley isomorphism of pairs and multiplication-induced Nori edges",
            ],
            "queries": [
                {
                    "query": "Groupoids Associated with Endomorphisms",
                    "layer": "research_literature",
                    "index_level": "canonical",
                    "executed_utc": "2026-08-30T13:10:00Z",
                    "reason": "route the exact triple-groupoid prototype and compact-covering hypothesis boundary",
                    "result_unit_ids": ["PUBUNIT-EF51A30466D25AFE9C75C974"],
                },
                {
                    "query": "Transcendence Linear Relations 1-Periods",
                    "layer": "research_literature",
                    "index_level": "canonical",
                    "executed_utc": "2026-08-30T13:10:00Z",
                    "reason": "route the 1-motive morphism, Kummer logarithm, character, and 1-period framework",
                    "result_unit_ids": ["PUBUNIT-738F0D16B49618236C67D652"],
                },
                {
                    "query": "Periods Nori Motives",
                    "layer": "research_literature",
                    "index_level": "canonical",
                    "executed_utc": "2026-08-30T13:10:00Z",
                    "reason": "route the exact Nori pair vertices and primitive edge directions",
                    "result_unit_ids": ["PUBUNIT-499097DAF18CF6AEE1056A50"],
                },
                {
                    "query": "Derived Categories 1-Motives",
                    "layer": "research_literature",
                    "index_level": "canonical",
                    "executed_utc": "2026-08-30T13:10:00Z",
                    "reason": "route the Deligne 1-motive square and curve-generated derived framework",
                    "result_unit_ids": ["PUBUNIT-663759AB2A92FA11265DB7BC"],
                },
            ],
            "sources": [
                {
                    "source_class": "research_literature",
                    "publication_unit_or_source_id": "SRC-COL-000046",
                    "exact_locators": ["physical PDF pp. 2-4, printed pp. 1779-1781", "SRC-COL-000046"],
                    "relevance_edge": "supplies the triple-groupoid prototype and the exact topological hypotheses that are not silently transferred",
                    "toc_or_section_check": {"status": "checked", "checked_utc": "2026-08-30T13:20:00Z", "relevant_sections": ["opening construction and proposition", "compact-covering definition"]},
                    "reading_status": "fully_content_read_for_current_dependency",
                    "dependencies": [],
                    "claim_or_proof_crosswalk_ids": ["CLM-COL-000174", "CLM-COL-000177"],
                },
                {
                    "source_class": "research_literature",
                    "publication_unit_or_source_id": "SRC-COL-000047",
                    "exact_locators": ["physical PDF pp. 90, 116-120, 137", "SRC-COL-000047"],
                    "relevance_edge": "supplies 1-motive morphisms, Kummer logarithms, torus characters, and the 1-period comparison",
                    "toc_or_section_check": {"status": "checked", "checked_utc": "2026-08-30T13:20:00Z", "relevant_sections": ["8.1", "10.2-10.4", "12.10"]},
                    "reading_status": "fully_content_read_for_current_dependency",
                    "dependencies": [],
                    "claim_or_proof_crosswalk_ids": ["CLM-COL-000175", "CLM-COL-000179", "CLM-COL-000180"],
                },
                {
                    "source_class": "research_literature",
                    "publication_unit_or_source_id": "SRC-COL-000048",
                    "exact_locators": ["physical PDF p. 231, Definition 9.1.1", "SRC-COL-000048"],
                    "relevance_edge": "fixes the exact primitive Nori edge types and contravariant direction",
                    "toc_or_section_check": {"status": "checked", "checked_utc": "2026-08-30T13:20:00Z", "relevant_sections": ["9.1, effective pairs"]},
                    "reading_status": "fully_content_read_for_current_dependency",
                    "dependencies": [],
                    "claim_or_proof_crosswalk_ids": ["CLM-COL-000176", "CLM-COL-000180"],
                },
                {
                    "source_class": "research_literature",
                    "publication_unit_or_source_id": "SRC-COL-000049",
                    "exact_locators": ["source TeX lines 728-750, 1736-1751, 3796-3800", "SRC-COL-000049"],
                    "relevance_edge": "supplies the commutative-square definition and the exact wider 1-motive framework without supplying the concrete Collatz maps",
                    "toc_or_section_check": {"status": "checked", "checked_utc": "2026-08-30T13:20:00Z", "relevant_sections": ["Deligne 1-motives", "the fully faithful functor", "Motivic Albanese"]},
                    "reading_status": "fully_content_read_for_current_dependency",
                    "dependencies": [],
                    "claim_or_proof_crosswalk_ids": ["CLM-COL-000175", "CLM-COL-000179"],
                },
                {
                    "source_class": "local_unpublished_work",
                    "publication_unit_or_source_id": "CHATINT-COL-000017",
                    "exact_locators": ["raw Z_n Symmetries physical lines 11088-14011", "intake/chatnotes/ZN-SYMMETRIES-GROUPOID-MOTIVIC-DIRECT-LOCATOR-AUDIT-06.md"],
                    "relevance_edge": "controlling chronological witness for the local groupoid and motivic interface proposals, their corrections, and their exact surviving formulas",
                    "toc_or_section_check": {"status": "not_available", "checked_utc": "2026-08-30T13:20:00Z", "relevant_sections": [], "reason": "raw chronological export has no controlling table of contents"},
                    "reading_status": "fully_content_read_for_current_dependency",
                    "dependencies": [],
                    "claim_or_proof_crosswalk_ids": ["CLM-COL-000177", "CLM-COL-000178", "CLM-COL-000179", "CLM-COL-000180", "CLM-COL-000181"],
                },
            ],
            "unresolved_dependencies": [],
            "refresh_reason": "direct reading of the complete raw interval, canonical-index routing of four exact dependencies, content-level source reading, explicit construction of every admitted map, two elementary operator obstructions, and a bounded independent certificate",
            "anti_loop_note": "The completed canonical index was queried and not rebuilt. Broader operator, equilibrium, cyclic, and motivic vocabulary remains outside this route because the raw interval supplies no typed comparison maps.",
        }
    )
    write_jsonl("state/topic_routes.jsonl", topic_rows)

    programme_rows = load_jsonl("state/programmes.jsonl")
    programmes = {row.get("programme_id"): row for row in programme_rows if row.get("programme_id")}
    if set(programmes) != {"PRG-COL-0001", "PRG-COL-0002"}:
        raise RuntimeError(f"unexpected programme IDs: {sorted(programmes)}")

    p1 = programmes["PRG-COL-0001"]
    p1["status"] = "reconstructed_at_bounded_proved_scope_with_exact_arithmetic_groupoid_and_three_adic_germ_interface"
    p1["natural_boundary"] = "raw Z_n Symmetries physical lines 6221-9596 and the exact path/groupoid extension in 11088-14011: exponent paths, legal blocks, weights, predecessor transfer, prefix cocycles, finite residue transformations, the discrete arithmetic orbit groupoid, and the 3-adic germ functor form one programme because every construction uses the same chronological exponent word and composition law; unsupported crossed-product, equilibrium, cyclic, BCM, adelic, and motivic-Galois packages remain outside"
    extend_unique(p1, "lineage", ["CHATINT-COL-000017 controlling raw groupoid and three-adic extension"])
    extend_unique(p1, "literature_sources", ["SRC-COL-000046"])
    extend_unique(p1, "definitions", [
        "discrete arithmetic orbit groupoid G_arith",
        "representative-independent exponent-sum cocycle, bidegree D, and real cocycle delta_G",
        "clopen 3-adic branches, their pseudogroup, and germ groupoid H_3",
        "actual-orbit-word germ functor Xi",
    ])
    extend_unique(p1, "sourced_scope_results", ["CLM-COL-000174"])
    extend_unique(p1, "proved_results", ["CLM-COL-000177", "CLM-COL-000178"])
    extend_unique(p1, "morphisms", ["MOR-COL-000055", "MOR-COL-000056", "MOR-COL-000057", "MOR-COL-000058"])
    extend_unique(p1, "repairs", [
        "constructed the arithmetic groupoid, its topology, Haar system, and exact path-algebra embedding instead of naming an unspecified groupoid completion",
        "constructed the faithful arithmetic-to-three-adic germ functor and recovered both cocycles from its rational affine slope",
        "rejected the printed positive-odd l2 isometry by the exact basis-vector calculation V_1 delta_1=0",
        "rejected left prefixing as an algebra endomorphism by comparing L_q(1) with L_q(1)L_q(1)",
    ])
    extend_unique(p1, "contradictions_and_retractions", [
        "raw V_a*V_a=1 is false on l2(O), already for a=1 and delta_1",
        "raw left-prefix endomorphism is not multiplicative for any nonempty prefix",
        "raw crossed-product and groupoid equalities have no declared comparison homomorphism or universal-property proof",
    ])
    extend_unique(p1, "certificates", [{
        "path": "research_companion/certificates/groupoid_motivic_interface_checks.py",
        "bytes": certificate.stat().st_size,
        "sha256": sha256(certificate),
        "status": "PASS_exact_groupoid_germ_cocycle_and_obstruction_checks",
    }])
    p1["additional_live_proof_paths"] = ["tex/chapters/05_chatnotes_groupoid_and_motivic_interfaces.tex"]
    p1["additional_research_companion_paths"] = ["research_companion/chapters/03_arithmetic_groupoids_and_toric_period_morphisms.tex"]
    p1["exact_nonclaims"] = [
        "no Collatz termination theorem",
        "no amenability or equality of full and reduced groupoid completions",
        "no unspecified semigroup crossed-product identification",
        "no equilibrium-state or phase-transition classification",
        "no QGr, Leavitt, Hopf, bialgebra, BCM, adelic, cyclic, or motivic-Galois package",
        "no uniqueness, canonicity, priority, or novelty claim",
    ]

    p2 = programmes["PRG-COL-0002"]
    p2["status"] = "reconstructed_with_exact_Gaussian_relation_results_and_exact_torus_Kummer_Cayley_Nori_interface_maps"
    p2["natural_boundary"] = "raw Z_n Symmetries physical lines 9597-11087 and the period-interface extension in 11088-14011: prefix ratios, principal arctangents, Gaussian Cayley units, exact relation lattices, arithmetic and degree torus characters, Kummer 1-motive squares, Cayley pairs, and multiplication-induced Nori edges form one programme through explicit maps; wider modular, CM, equilibrium, operator, and motivic-Galois rhetoric remains outside absent typed maps"
    extend_unique(p2, "lineage", ["CHATINT-COL-000017 controlling raw torus, Kummer, Cayley, and Nori extension"])
    extend_unique(p2, "literature_sources", ["SRC-COL-000047", "SRC-COL-000048", "SRC-COL-000049"])
    extend_unique(p2, "definitions", [
        "arithmetic and degree tori with the unimodular coordinate map Phi",
        "rank-one-to-rank-two 1-motives M_ar and M_deg and path Kummer motives",
        "Cartier dual character map (r,s)->2^r3^s",
        "Cayley algebraic pairs and multiplication maps of Kummer pairs",
        "contravariant Nori functoriality edges induced by actual maps of pairs",
    ])
    extend_unique(p2, "sourced_scope_results", ["CLM-COL-000175", "CLM-COL-000176"])
    extend_unique(p2, "proved_results", ["CLM-COL-000179", "CLM-COL-000180"])
    extend_unique(p2, "morphisms", ["MOR-COL-000059", "MOR-COL-000060", "MOR-COL-000061", "MOR-COL-000062"])
    extend_unique(p2, "repairs", [
        "proved the exact unimodular map between degree and arithmetic torus coordinates without replacing either presentation",
        "replaced unnamed path periods by commutative Kummer 1-motive squares with a displayed logarithm path",
        "replaced path concatenation as a supposed Nori edge by the Cayley pair map and the multiplication map of marked pairs",
        "proved regularity of dz/(1+z^2) at infinity and kept the rational and Q(i) pair presentations distinct but explicitly related",
    ])
    extend_unique(p2, "contradictions_and_retractions", [
        "raw concatenation and prefix extension do not define Nori edges without a map of pairs or nested triple",
        "the positive rational Collatz Kummer point is not equal to the nonreal Cayley marked point for r>0",
    ])
    extend_unique(p2, "certificates", [{
        "path": "research_companion/certificates/groupoid_motivic_interface_checks.py",
        "bytes": certificate.stat().st_size,
        "sha256": sha256(certificate),
        "status": "PASS_exact_torus_character_motive_square_and_Cayley_checks",
    }])
    p2["additional_live_proof_paths"] = ["tex/chapters/05_chatnotes_groupoid_and_motivic_interfaces.tex"]
    p2["additional_research_companion_paths"] = ["research_companion/chapters/03_arithmetic_groupoids_and_toric_period_morphisms.tex"]
    p2["exact_nonclaims"] = [
        "no proof of the all-length Collatz-Machin rigidity conjecture",
        "no result outside the certified arctangent grid from the finite lattice certificate",
        "no Collatz termination or endpoint theorem",
        "no universal path-indexed Nori category, motivic Galois action, or LAlb computation",
        "no equilibrium, modular, CM, operator, BCM, KMS, or local-factor theorem beyond the displayed exact maps",
        "no novelty or priority claim",
    ]
    write_jsonl("state/programmes.jsonl", programme_rows)

    print(
        json.dumps(
            {
                "status": "PASS",
                "sources_added": [row["source_id"] for row in sources],
                "claims_added": [row["claim_id"] for row in claims],
                "morphisms_added": [row["morphism_id"] for row in morphisms],
                "intake_added": intake["intake_id"],
                "topic_added": "TOPIC-COL-GROUPOID-MOTIVIC-0004",
                "programmes_extended": ["PRG-COL-0001", "PRG-COL-0002"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
