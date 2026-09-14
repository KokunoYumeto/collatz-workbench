from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state"


if not __debug__:
    raise RuntimeError("state propagation refuses optimized Python")


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def pinned(path: Path, *, size: int, digest: str) -> None:
    assert path.is_file(), path
    assert path.stat().st_size == size, (path, path.stat().st_size, size)
    assert sha256(path) == digest, (path, sha256(path), digest)


def load_lines(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    assert lines, path
    for line in lines:
        json.loads(line)
    return lines


def dump(record: dict) -> str:
    return json.dumps(record, ensure_ascii=False, separators=(",", ":"))


def body_ids(lines: list[str], key: str) -> list[str]:
    return [row[key] for row in map(json.loads, lines) if key in row]


def set_header(lines: list[str], *, expected: str, replacement: str) -> None:
    header = json.loads(lines[0])
    assert header["record_type"] == "ledger_header"
    assert header["next_id"] == expected, (header["next_id"], expected)
    header["next_id"] = replacement
    lines[0] = dump(header)


def insert_after(lines: list[str], *, key: str, marker: str, records: list[dict]) -> None:
    positions = [index for index, line in enumerate(lines) if json.loads(line).get(key) == marker]
    assert positions == [positions[0]] and len(positions) == 1, (key, marker, positions)
    position = positions[0] + 1
    lines[position:position] = [dump(record) for record in records]


def append_jsonl(path: Path, lines: list[str]) -> None:
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


raw_source = Path("C:/Users/LOCAL_USER/Documents/Obsidian notes/ChatGPT-Branch · Z_n Symmetries of Collatz.md")
audit_path = ROOT / "intake/chatnotes/ZN-SYMMETRIES-ARCTANGENT-DIRECT-LOCATOR-AUDIT-05.md"
certificate_path = ROOT / "research_companion/certificates/arctangent_relation_lattice_checks.py"
directive_path = ROOT / "raw/USR-0012.txt"
reference_path = Path(
    "C:/Users/LOCAL_USER/.codex/attachments/dbad1702-848d-4a03-a3de-e8232f9465fe/pasted-text.txt"
)

pinned(
    raw_source,
    size=538005,
    digest="9a80f53764a9da42c0f8e0b6d19ce61f978980a448a683b9c45f04038716160d",
)
pinned(
    audit_path,
    size=7241,
    digest="3243d452e4d8e71ecddcec19112d11747120d58bf7b577e4233907042ed38517",
)
pinned(
    certificate_path,
    size=19204,
    digest="3b324c5ff1862bdef17d5cc2ab413e85d4a3dd011012fcdde9797dccab08df26",
)
pinned(
    directive_path,
    size=817,
    digest="cd726fce3faa5fead6897fab54816a63c5851ac822b886287920b4f6e159ff29",
)
pinned(
    reference_path,
    size=9837,
    digest="2f4c77618d0c35fd9edc5a8798fc67d4e708cf0e28b67d00c7d91b3175228f5e",
)
assert sum(1 for _ in reference_path.open("r", encoding="utf-8")) == 261


intake_file = STATE / "chatnotes_intake.jsonl"
intake_lines = load_lines(intake_file)
assert body_ids(intake_lines, "intake_id") == [
    f"CHATINT-COL-{number:06d}" for number in range(1, 16)
]
set_header(
    intake_lines,
    expected="CHATINT-COL-000016",
    replacement="CHATINT-COL-000017",
)
source_identity = json.loads(intake_lines[1])
assert source_identity["intake_id"] == "CHATINT-COL-000001"
source_identity["content_status"] = (
    "all_physical_lines_have_chronological_intake_reports; direct_locator_audits_cover_"
    "lines_1_11087_and_14012_17437; only_lines_11088_14011_remain_without_a_direct_"
    "locator_audit; bounded_results_are_admitted_only_in_separate_claim_morphism_and_"
    "source_records"
)
intake_lines[1] = dump(source_identity)
intake_record = {
    "record_type": "chatnotes_locator_audit",
    "schema_version": "1.0",
    "intake_id": "CHATINT-COL-000016",
    "source_intake_id": "CHATINT-COL-000001",
    "audit_scope": "raw_lines_9597_11087_complete_direct_read_arctangent_gaussian_torsion_programme",
    "primary_source_ids": [
        "SRC-COL-000043",
        "SRC-COL-000044",
        "SRC-COL-000045",
    ],
    "admission_status": "no_mathematical_admission",
    "separate_ledger_status": "definitions_sourced_boundaries_independent_theorems_and_conjecture_recorded_separately",
    "programme_status": "arctangent_gaussian_relation_lattice_programme_reconstructed",
    "report_path": "intake/chatnotes/ZN-SYMMETRIES-ARCTANGENT-DIRECT-LOCATOR-AUDIT-05.md",
    "report_bytes": 7241,
    "report_sha256": "3243d452e4d8e71ecddcec19112d11747120d58bf7b577e4233907042ed38517",
    "certificate_path": "research_companion/certificates/arctangent_relation_lattice_checks.py",
    "certificate_bytes": 19204,
    "certificate_sha256": "3b324c5ff1862bdef17d5cc2ab413e85d4a3dd011012fcdde9797dccab08df26",
    "source_bytes": 538005,
    "source_physical_lines": 17437,
    "source_sha256": "9a80f53764a9da42c0f8e0b6d19ce61f978980a448a683b9c45f04038716160d",
    "verified_findings": [
        "the_prefix_ratios_are_3_to_the_k_minus_1_over_2_to_the_A_k_and_are_summands_of_the_existing_prefix_coordinate_not_an_Euler_product",
        "principal_arctangent_relations_are_exactly_multiplicative_torsion_relations_in_Q_i_modulo_mu_4",
        "the_raw_chronology_retracts_its_classical_unit_equation_wording_and_supplies_no_universal_nonvanishing_theorem",
        "the_legal_word_1_1_has_the_exact_identity_2_arctan_1_over_2_plus_arctan_3_over_4_equals_pi_over_2",
        "fixed_instances_have_exact_Gaussian_prime_coordinates_but_the_uniform_prefix_rank_classification_is_a_separate_question",
    ],
    "nonclaims": [
        "The raw chronology proves neither universal relation-lattice rigidity nor any Collatz endpoint.",
        "Its exploratory zeta, Heegner, modular, CM, operator, and period vocabulary supplies no typed map to this lattice.",
        "The finite certificate proves only the displayed 795-column grid and makes no priority claim.",
    ],
}
intake_lines.append(dump(intake_record))


source_file = STATE / "source_registry.jsonl"
source_lines = load_lines(source_file)
assert set(body_ids(source_lines, "source_id")) == {
    f"SRC-COL-{number:06d}" for number in range(1, 43)
}
set_header(source_lines, expected="SRC-COL-000043", replacement="SRC-COL-000046")
sources = [
    {
        "record_type": "source_document",
        "schema_version": "1.0",
        "source_id": "SRC-COL-000043",
        "authors": ["John H. Conway", "Charles Radin", "Lorenzo Sadun"],
        "title": "On Angles Whose Squared Trigonometric Functions are Rational",
        "bibliographic_identity": {
            "arxiv_version_id": "math-ph/9812019v1",
            "arxiv_record": "https://arxiv.org/abs/math-ph/9812019",
            "submitted": "1998-12-18",
            "journal": "Discrete & Computational Geometry",
            "volume": "22",
            "issue": "3",
            "pages": "321-332",
            "publication_year": 1999,
            "doi": "10.1007/PL00009463",
        },
        "manifestations": [
            {
                "path": "C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/latex/math-ph.9812019v1/text16.tex",
                "role": "controlling_versioned_arXiv_Plain_TeX_source",
                "bytes": 42239,
                "source_lines": 619,
                "sha256": "0b37130b7e958c58c1e9f70f855f9181699b0f42d78ac5d04c29329aae0db21d",
            },
            {
                "path": "C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/source/math-ph.9812019v1.eprint",
                "role": "versioned_arXiv_source_archive",
                "bytes": 37959,
                "sha256": "12395ea06721c1306923f40b5966eb4bd39f16d5734c996b1e60d85fe5e8b034",
            },
            {
                "path": "C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/latex/math-ph.9812019v1/extraction_manifest.json",
                "role": "source_extraction_manifest",
                "bytes": 1175,
                "sha256": "ed099d19eb55af4d7c6e551ca10876f43a81467795bfadc4e2671e2389b6d0bd",
            },
        ],
        "route_ids": [],
        "route_integrity": {
            "status": "exact_title_and_author_miss_in_frozen_publication_units_then_official_arXiv_source_acquired_and_read",
            "frozen_ledgers_mutated": False,
            "nonexistence_inferred_from_route_miss": False,
        },
        "reading": {
            "status": "complete_relevant_source_sections_read_for_fixed_Gaussian_angle_coordinates",
            "locators": [
                "source lines 151-168: Theorems 1 and 2",
                "source lines 251-306: d=1 Stormer theory, oriented Gaussian primes, basis, and independence",
            ],
            "source_objects": {
                "fixed_instance_coordinates": "one oriented Gaussian prime angle over each split rational prime together with pi/4",
                "structural_input": "unique factorization in Z[i]",
                "scope": "fixed rational-angle relations, not a uniform Collatz prefix family",
            },
        },
        "audit": {
            "path": "intake/chatnotes/ZN-SYMMETRIES-ARCTANGENT-DIRECT-LOCATOR-AUDIT-05.md",
            "status": "source_TeX_content_and_exact_scope_crosswalk",
        },
        "nonclaims": [
            "The source states no Collatz-prefix rank theorem.",
            "The fixed Gaussian coordinate machinery does not by itself prove the all-length conjecture.",
        ],
    },
    {
        "record_type": "source_document",
        "schema_version": "1.0",
        "source_id": "SRC-COL-000044",
        "authors": ["Jack S. Calcut"],
        "title": "Gaussian Integers and Arctangent Identities for pi",
        "bibliographic_identity": {
            "journal": "The American Mathematical Monthly",
            "volume": "116",
            "issue": "6",
            "pages": "515-530",
            "publication_year": 2009,
            "doi": "10.1080/00029890.2009.11920967",
        },
        "manifestations": [
            {
                "path": "C:/Users/LOCAL_USER/Documents/arxiv_latex/library/_recovered_from_papers/by_title/Gaussian Integers and Arctangent Identities for π.pdf",
                "role": "controlling_published_article_PDF",
                "bytes": 169888,
                "pdf_pages": 16,
                "printed_pages": "515-530",
                "sha256": "d650da61527c78c67caca06758363280bac7303cb2b553fc786914ddf3a4886f",
            }
        ],
        "route_ids": ["PUBUNIT-0F37C9695BAA49C4C5EE414D"],
        "route_integrity": {
            "status": "canonical_publication_unit_title_is_embedded_calcut_dvi_but_controlling_PDF_content_and_bibliography_fix_exact_identity",
            "canonical_publication_unit_id": "PUBUNIT-0F37C9695BAA49C4C5EE414D",
            "frozen_ledgers_mutated": False,
        },
        "reading": {
            "status": "complete_relevant_Main_Lemma_and_corollaries_read",
            "locators": [
                "physical PDF p. 5 / printed p. 519: Main Lemma",
                "physical PDF p. 6 / printed p. 520: Corollaries 1-3",
                "physical PDF p. 7: continuation of the Gaussian-integer argument",
            ],
            "source_objects": {
                "root_of_unity_restriction": "rational arctangent sums that are rational multiples of pi lie in (pi/4)Z",
                "single_angle_scope": "a rational tangent gives a rational multiple of pi only at tangent 0 or plus/minus 1",
            },
        },
        "audit": {
            "path": "intake/chatnotes/ZN-SYMMETRIES-ARCTANGENT-DIRECT-LOCATOR-AUDIT-05.md",
            "status": "published_PDF_content_and_scope_crosswalk",
        },
        "nonclaims": [
            "The source does not classify the Collatz prefix family uniformly.",
            "The companion's exceptional-pair lattice is proved independently by a Gaussian valuation.",
        ],
    },
    {
        "record_type": "source_document",
        "schema_version": "1.0",
        "source_id": "SRC-COL-000045",
        "authors": ["Armengol Gasull", "Florian Luca", "Juan L. Varona"],
        "title": "Three Essays on Machin's Type Formulas",
        "bibliographic_identity": {
            "arxiv_version_id": "2302.00154v2",
            "arxiv_record": "https://arxiv.org/abs/2302.00154",
            "journal": "Indagationes Mathematicae",
            "volume": "34",
            "issue": "6",
            "pages": "1373-1396",
            "publication_year": 2023,
            "doi": "10.1016/j.indag.2023.07.002",
        },
        "manifestations": [
            {
                "path": "C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/latex/2302.00154v2/Machin-three-issues-final.tex",
                "role": "controlling_versioned_arXiv_source_TeX",
                "bytes": 82898,
                "sha256": "53f19ec4bf58c9e64ec51a2397401cb51fc450c7d9eb5ec61d2cf0372c162baf",
            },
            {
                "path": "C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/source/2302.00154v2.eprint",
                "role": "versioned_arXiv_source_archive",
                "bytes": 53371,
                "sha256": "9b49cb3c182eb86aa5c94b5ae3ddfb7a201676b78a74a9e9c6519146432f2e32",
            },
            {
                "path": "C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/latex/2302.00154v2/extraction_manifest.json",
                "role": "source_extraction_manifest",
                "bytes": 1359,
                "sha256": "f2a17d9539cdc9d38ec9e58b3a04271a0b5525e07e7869ea2657556bb03ee601",
            },
            {
                "path": "C:/Users/LOCAL_USER/Documents/arxiv_latex/library/_recovered_from_papers/by_title/Three essays on Machin’s type formulas∗.pdf",
                "role": "published_article_PDF_crosswalk",
                "bytes": 465212,
                "pdf_pages": 24,
                "sha256": "e2b2fd89ea5668bc657d2a182dbc2d90b9f20e297a9f85e7338d5b459b7f75c1",
            },
        ],
        "route_ids": ["PUBUNIT-DACD031AA11CEAFCEC3782A5"],
        "route_integrity": {
            "status": "canonical_unit_title_and_PDF_match_but_frozen_arxiv_id_is_corrupt; exact_2302_00154v2_source_independently_acquired_and_controls",
            "canonical_publication_unit_id": "PUBUNIT-DACD031AA11CEAFCEC3782A5",
            "corrupted_frozen_arxiv_id": "1706.08835",
            "controlling_arxiv_version_id": "2302.00154v2",
            "frozen_ledgers_mutated": False,
            "corrupted_metadata_used_as_bibliographic_identity": False,
        },
        "reading": {
            "status": "complete_relevant_two_term_classification_and_Gaussian_reformulation_read",
            "locators": [
                "source lines 230-267: Section 2 and Theorem 1",
                "source lines 258-267: exceptional tuple including tangent arguments 1/2 and 3/4",
                "source lines 278-312: Gaussian root-of-unity reformulation",
                "source lines 341-352: zero double-angle family",
            ],
            "source_objects": {
                "Theorem_1_scope": "stated two-term nonzero-right-hand-side Machin formulas with 2-integer arguments",
                "exceptional_identity": "arctan(1/2)+(1/2)arctan(3/4)=pi/4",
            },
        },
        "audit": {
            "path": "intake/chatnotes/ZN-SYMMETRIES-ARCTANGENT-DIRECT-LOCATOR-AUDIT-05.md",
            "status": "versioned_source_TeX_and_published_PDF_scope_crosswalk",
        },
        "nonclaims": [
            "The theorem does not classify arbitrary-length or all zero-right-hand-side prefix relations.",
            "The source does not establish the 795-column lattice theorem or all-length conjecture.",
        ],
    },
]
assert body_ids(source_lines, "source_id")[-1] == "SRC-COL-000042"
source_lines.extend(dump(record) for record in sources)


claim_file = STATE / "claims.jsonl"
claim_lines = load_lines(claim_file)
assert set(body_ids(claim_lines, "claim_id")) == {
    f"CLM-COL-{number:06d}" for number in range(1, 165)
}
set_header(claim_lines, expected="CLM-COL-000165", replacement="CLM-COL-000174")
claims = [
    {
        "record_type": "claim",
        "schema_version": "1.0",
        "claim_id": "CLM-COL-000165",
        "claim_type": "verified_local_definition_and_problem_lineage",
        "status": "source_faithful_definition_and_question_reconstructed",
        "statement": "For a positive exponent word w=(a_1,...,a_n), with A_k=sum_(j<=k)a_j, the raw arctangent programme defines theta_k=arctan(3^(k-1)/2^A_k), z_k=2^A_k+i3^(k-1), u_k=z_k/conj(z_k), and Rel_pi(w)={m in Z^n:sum m_k theta_k in pi Q}. Chronologically, its corrected endpoint is the exact multiplicative torsion test product u_k^(m_k) in mu_4, not an additive unit equation or a universal nonvanishing theorem.",
        "source_ids": [],
        "dependencies": [],
        "local_source_refs": ["CHATINT-COL-000016"],
        "source_locators": [
            "raw Z_n Symmetries physical lines 9597-9602, 9611-9621, 9649-9685, 10013-10026, 10181-10246, and 10866-10936"
        ],
        "proof_locator": {
            "path": "tex/chapters/03a_chatnotes_arctangent_relations.tex",
            "label": "prop:chatnotes-arctangent-torsion-criterion",
        },
        "nonclaims": [
            "The raw chronology does not prove that the relation lattice is zero.",
            "No zeta, Heegner, modular, CM, operator, or endpoint implication is admitted from exploratory rhetoric.",
        ],
    },
    {
        "record_type": "claim",
        "schema_version": "1.0",
        "claim_id": "CLM-COL-000166",
        "claim_type": "sourced_Gaussian_prime_coordinate_theorem_scope",
        "status": "primary_source_content_read_at_exact_scope",
        "statement": "Conway, Radin, and Sadun's d=1 Stormer reconstruction uses unique factorization in Z[i], one oriented Gaussian prime above each split rational prime, and pi/4 to give exact fixed-instance coordinates and rational independence for rational-tangent angles at their stated scope.",
        "source_ids": ["SRC-COL-000043"],
        "dependencies": [],
        "source_locators": ["source TeX lines 151-168 and 251-306"],
        "audit_locator": "intake/chatnotes/ZN-SYMMETRIES-ARCTANGENT-DIRECT-LOCATOR-AUDIT-05.md",
        "nonclaims": ["The source does not state a uniform Collatz-prefix rank theorem."],
    },
    {
        "record_type": "claim",
        "schema_version": "1.0",
        "claim_id": "CLM-COL-000167",
        "claim_type": "sourced_rational_arctangent_mu4_and_single_angle_scope",
        "status": "primary_source_content_read_at_exact_scope",
        "statement": "Calcut's Main Lemma and Corollaries 1-3 give the Gaussian root-of-unity restriction for rational arctangent identities and show that a single rational tangent can be a rational multiple of pi only for tangent 0 or plus/minus 1.",
        "source_ids": ["SRC-COL-000044"],
        "dependencies": [],
        "source_locators": ["physical PDF p. 5 / printed p. 519 and physical PDF p. 6 / printed p. 520"],
        "audit_locator": "intake/chatnotes/ZN-SYMMETRIES-ARCTANGENT-DIRECT-LOCATOR-AUDIT-05.md",
        "nonclaims": ["The source does not classify the full Collatz-prefix family."],
    },
    {
        "record_type": "claim",
        "schema_version": "1.0",
        "claim_id": "CLM-COL-000168",
        "claim_type": "sourced_two_term_Machin_classification_and_exceptional_identity",
        "status": "primary_source_content_read_at_exact_scope",
        "statement": "Gasull, Luca, and Varona classify their stated two-term nonzero-right-hand-side Machin formulas with 2-integer arguments; their Theorem 1 contains arctan(1/2)+(1/2)arctan(3/4)=pi/4, and their Section 2 supplies the corresponding Gaussian root-of-unity reformulation.",
        "source_ids": ["SRC-COL-000045"],
        "dependencies": [],
        "source_locators": ["source TeX lines 230-312 and 341-352"],
        "audit_locator": "intake/chatnotes/ZN-SYMMETRIES-ARCTANGENT-DIRECT-LOCATOR-AUDIT-05.md",
        "nonclaims": ["The stated source theorem does not cover arbitrary-length zero relations or the uniform prefix classification."],
    },
    {
        "record_type": "claim",
        "schema_version": "1.0",
        "claim_id": "CLM-COL-000169",
        "claim_type": "independent_fixed_word_Gaussian_coordinate_kernel_theorem",
        "status": "proved",
        "statement": "For every fixed positive exponent word w, the homomorphism Gamma_bar_w:Z^n->U_1(Q(i))/mu_4 followed by the oriented split-prime valuation isomorphism nu_G gives the exact signed-valuation map E_w. Its kernel is Rel_pi(w); each nonempty fibre is one coset of Rel_pi(w), every point outside im(E_w) has empty fibre, and Z^n/Rel_pi(w)->im(E_w) has the displayed inverse on cosets. Reorienting one split prime negates only that coordinate.",
        "source_ids": ["SRC-COL-000043"],
        "dependencies": ["CLM-COL-000165", "CLM-COL-000166"],
        "local_source_refs": ["CHATINT-COL-000016"],
        "source_locators": ["Conway-Radin-Sadun source lines 251-306; independent exact morphism reconstruction"],
        "proof_locator": {
            "path": "research_companion/chapters/01_weighted_path_and_finite_residue_actions.tex",
            "label": "thm:collatz-machin-fixed-word-kernel",
        },
        "morphism_refs": ["MOR-COL-000052", "MOR-COL-000053", "MOR-COL-000054"],
        "formal_status": {"status": "general_constructive_Gaussian_UFD_proof_in_TeX"},
        "nonclaims": [
            "Fixed-word decidability after exact factorization is not a uniform rank classification.",
            "No Collatz endpoint follows from this kernel theorem.",
        ],
    },
    {
        "record_type": "claim",
        "schema_version": "1.0",
        "claim_id": "CLM-COL-000170",
        "claim_type": "independent_all_word_unweighted_arctangent_non_torsion_theorem",
        "status": "proved",
        "statement": "For every nonempty positive exponent word w, sum_k arctan(3^(k-1)/2^A_k) is not in pi Q, equivalently the all-ones coefficient vector is not in Rel_pi(w). The exact proof multiplies z_k=2^A_k+i3^(k-1): modulo 3 both real and imaginary parts are nonzero, and modulo 2 they have opposite parity, excluding all four values of Z/conj(Z) in mu_4.",
        "source_ids": [],
        "dependencies": ["CLM-COL-000165"],
        "local_source_refs": ["CHATINT-COL-000016"],
        "source_locators": ["independent consequence of the exact torsion criterion"],
        "proof_locator": {
            "path": "research_companion/chapters/01_weighted_path_and_finite_residue_actions.tex",
            "label": "thm:collatz-machin-unweighted-nontorsion",
        },
        "formal_status": {"status": "general_exact_mod_2_and_mod_3_proof_in_TeX"},
        "nonclaims": [
            "The theorem concerns only the coefficient vector (1,...,1), not all integer relations.",
            "It proves no Collatz orbit endpoint.",
        ],
    },
    {
        "record_type": "claim",
        "schema_version": "1.0",
        "claim_id": "CLM-COL-000171",
        "claim_type": "independent_exact_exceptional_two_letter_relation_lattice_theorem",
        "status": "proved",
        "statement": "For w=(1,1), Rel_pi(w)=Z(2,1) and 2 arctan(1/2)+arctan(3/4)=pi/2. The Gaussian identity (2+i)^2(4+3i)=25i gives the relation, while v_(2+i)((2+i)/(2-i))=1 proves that no additional independent power can lie in mu_4.",
        "source_ids": ["SRC-COL-000045"],
        "dependencies": ["CLM-COL-000165", "CLM-COL-000169"],
        "local_source_refs": ["CHATINT-COL-000016"],
        "source_locators": ["Gasull-Luca-Varona Theorem 1 for the identity crosswalk; independent full-lattice proof"],
        "proof_locator": {
            "path": "research_companion/chapters/01_weighted_path_and_finite_residue_actions.tex",
            "label": "thm:collatz-machin-exceptional-seed",
        },
        "formal_status": {"status": "exact_Gaussian_product_and_valuation_proof_in_TeX"},
        "nonclaims": ["The published two-term identity is not represented as a published classification of all prefix relations."],
    },
    {
        "record_type": "claim",
        "schema_version": "1.0",
        "claim_id": "CLM-COL-000172",
        "claim_type": "independent_exact_full_grid_Gaussian_relation_lattice_theorem",
        "status": "proved",
        "statement": "On G_(15,60)={(k,A):1<=k<=15,k<=A<=60}, the complete coefficient-unbounded integer relation lattice for arctan(3^(k-1)/2^A) is Z r_1 direct-sum Z r_2, where r_1=2e_(1,1)+e_(2,2) and r_2=2e_(1,1)+e_(1,2)+e_(1,3)+e_(3,5). Therefore every word with n<=15 and A_n<=60 has relation lattice Z(2,1,0,...,0) exactly when its first two exponents are (1,1), and zero otherwise.",
        "source_ids": [],
        "dependencies": ["CLM-COL-000169", "CLM-COL-000171"],
        "local_source_refs": ["CHATINT-COL-000016"],
        "source_locators": ["independent exact cubic-character rank and saturated integral lift"],
        "proof_locator": {
            "path": "research_companion/chapters/01_weighted_path_and_finite_residue_actions.tex",
            "label": "thm:collatz-machin-finite-census",
        },
        "formal_status": {
            "status": "PASS_exact_full_grid_integer_lattice_certificate",
            "artifact": "research_companion/certificates/arctangent_relation_lattice_checks.py",
            "artifact_sha256": "3b324c5ff1862bdef17d5cc2ab413e85d4a3dd011012fcdde9797dccab08df26",
            "verified_metrics": {
                "columns": 795,
                "candidate_primes": 1008,
                "good_rows": 794,
                "bad_rows": 214,
                "rank_F3": 793,
                "nullity_F3": 2,
                "character_entry_checks": 631230,
                "first_full_rank_prime": 38821,
                "character_matrix_trits_sha256": "15071896fda6f1d4e75b42c91db02a2155777baa4a7eb7bdb79c6959959e1ab6",
            },
        },
        "nonclaims": [
            "The certificate proves no relation-lattice assertion outside the declared grid.",
            "There is no bound on relation coefficients inside the certified grid.",
            "The theorem makes no novelty, priority, termination, or endpoint claim.",
        ],
    },
    {
        "record_type": "claim",
        "schema_version": "1.0",
        "claim_id": "CLM-COL-000173",
        "claim_type": "mathematically_justified_conjecture",
        "status": "conjecture_registered_not_proved",
        "statement": "Collatz-Machin rigidity conjecture: for every nonempty positive exponent word w=(a_1,...,a_n), Rel_pi(w)=Z(2,1,0,...,0) when n>=2 and (a_1,a_2)=(1,1), and Rel_pi(w)={0} otherwise.",
        "source_ids": ["SRC-COL-000043", "SRC-COL-000044", "SRC-COL-000045"],
        "dependencies": [
            "CLM-COL-000166",
            "CLM-COL-000167",
            "CLM-COL-000168",
            "CLM-COL-000169",
            "CLM-COL-000170",
            "CLM-COL-000171",
            "CLM-COL-000172",
        ],
        "local_source_refs": ["CHATINT-COL-000016"],
        "source_locators": [
            "fixed-word Gaussian-coordinate theorem",
            "two all-length proved boundaries",
            "complete coefficient-unbounded grid n<=15 and A_n<=60",
            "published fixed-instance and two-term source crosswalk",
        ],
        "statement_locator": {
            "path": "research_companion/chapters/01_weighted_path_and_finite_residue_actions.tex",
            "label": "conj:collatz-machin-rigidity",
        },
        "formal_status": {
            "status": "proved_only_for_n_at_most_15_and_A_n_at_most_60_plus_two_all_length_boundaries",
            "finite_artifact": "research_companion/certificates/arctangent_relation_lattice_checks.py",
            "finite_artifact_sha256": "3b324c5ff1862bdef17d5cc2ab413e85d4a3dd011012fcdde9797dccab08df26",
        },
        "nonclaims": [
            "The conjecture is not a theorem outside the certified grid.",
            "It is not the Collatz conjecture and implies no stated orbit endpoint.",
            "The literature search is not a novelty or priority certificate.",
        ],
    },
]
insert_after(
    claim_lines,
    key="claim_id",
    marker="CLM-COL-000164",
    records=claims,
)


morphism_file = STATE / "morphisms.jsonl"
morphism_lines = load_lines(morphism_file)
assert set(body_ids(morphism_lines, "morphism_id")) == {
    f"MOR-COL-{number:06d}" for number in range(1, 52)
}
set_header(morphism_lines, expected="MOR-COL-000052", replacement="MOR-COL-000055")
morphisms = [
    {
        "record_type": "morphism",
        "schema_version": "1.0",
        "morphism_id": "MOR-COL-000052",
        "name": "fixed_word_Collatz_Machin_unit_product_modulo_mu4",
        "domain": "The additive group Z^n for a fixed positive exponent word w of length n.",
        "codomain": "U_1(Q(i))/mu_4, where U_1(Q(i))={x in Q(i)^x:x conjugate(x)=1}.",
        "formula": "Gamma_bar_w(m)=[product_(k=1)^n u_k(w)^(m_k)], with u_k=(2^A_k+i3^(k-1))/(2^A_k-i3^(k-1)).",
        "well_definedness": "Each u_k is a nonzero norm-one element of Q(i); integer powers and multiplication define a homomorphism, and quotienting by mu_4 is compatible with multiplication.",
        "preserved_structure": "The additive law on exponent vectors, multiplication of unit products, the exact prefix angles, and rational-pi torsion modulo mu_4.",
        "fibres": "The kernel is exactly Rel_pi(w). Every nonempty fibre is a coset of Rel_pi(w); points outside the image have empty fibre.",
        "inverse_status": "The induced map Z^n/Rel_pi(w)->im(Gamma_bar_w) is an isomorphism with inverse sending an image point to its unique source coset.",
        "exceptions": [
            "No surjectivity onto all U_1(Q(i))/mu_4 is claimed.",
            "This fixed-word map alone does not give a uniform rank theorem.",
        ],
        "claim_refs": ["CLM-COL-000165", "CLM-COL-000169"],
        "source_refs": ["SRC-COL-000043"],
        "proof_locator": {
            "path": "research_companion/chapters/01_weighted_path_and_finite_residue_actions.tex",
            "label": "thm:collatz-machin-fixed-word-kernel",
        },
        "formal_status": {"status": "general_constructive_proof_in_TeX"},
    },
    {
        "record_type": "morphism",
        "schema_version": "1.0",
        "morphism_id": "MOR-COL-000053",
        "name": "oriented_split_Gaussian_prime_valuation_isomorphism",
        "domain": "U_1(Q(i))/mu_4.",
        "codomain": "The finite-support direct sum over rational primes p congruent to 1 mod 4 of Z.",
        "formula": "After choosing one Gaussian prime varpi_p above each split p, nu_G([x])=(v_(varpi_p)(x))_p.",
        "well_definedness": "Unique factorization in Z[i] makes split-prime valuations finite. Norm one forces conjugate valuations to be opposite and kills inert and ramified valuations; changing x by a Gaussian unit changes none.",
        "preserved_structure": "Multiplication becomes coordinate addition, conjugation reverses all split-prime exponents, and finite support is preserved.",
        "fibres": "Every fibre is a singleton because the map is an isomorphism; its kernel is the identity class mu_4.",
        "inverse_status": "The exact inverse sends (e_p)_p to [product_p (varpi_p/conjugate(varpi_p))^(e_p)].",
        "exceptions": [
            "Changing the chosen orientation over p negates only the p-coordinate.",
            "The construction is a coordinate choice, not a canonical ordering of split primes.",
        ],
        "claim_refs": ["CLM-COL-000166", "CLM-COL-000169"],
        "source_refs": ["SRC-COL-000043"],
        "proof_locator": {
            "path": "research_companion/chapters/01_weighted_path_and_finite_residue_actions.tex",
            "label": "thm:collatz-machin-fixed-word-kernel",
        },
        "formal_status": {"status": "general_Gaussian_UFD_isomorphism_proof_in_TeX"},
    },
    {
        "record_type": "morphism",
        "schema_version": "1.0",
        "morphism_id": "MOR-COL-000054",
        "name": "fixed_word_signed_Gaussian_valuation_map",
        "domain": "The additive group Z^n for a fixed positive exponent word w.",
        "codomain": "The finite-support direct sum over rational primes p congruent to 1 mod 4 of Z.",
        "formula": "E_w=nu_G composed with Gamma_bar_w, with matrix entry (E_w)_(p,k)=v_(varpi_p)(z_k(w))-v_(conjugate(varpi_p))(z_k(w)).",
        "well_definedness": "Each column is the finite signed split-prime valuation vector of z_k/conjugate(z_k), so matrix multiplication agrees exactly with the composite homomorphism.",
        "preserved_structure": "Integer linear combinations, multiplication of the associated Gaussian unit products, all split-prime exponent differences, and the exact relation kernel.",
        "fibres": "The kernel is Rel_pi(w); each nonempty fibre is a coset, and fibres outside im(E_w) are empty.",
        "inverse_status": "The induced quotient map Z^n/Rel_pi(w)->im(E_w) has the exact inverse y->m+Rel_pi(w) for any m with E_w(m)=y.",
        "exceptions": [
            "A fixed matrix is computable after factoring the finitely many norms, but no uniform factorization or rank bound is inferred.",
            "Reorienting a split prime negates a row without changing the kernel.",
        ],
        "claim_refs": ["CLM-COL-000169", "CLM-COL-000172"],
        "source_refs": ["SRC-COL-000043"],
        "component_morphism_refs": ["MOR-COL-000052", "MOR-COL-000053"],
        "proof_locator": {
            "path": "research_companion/chapters/01_weighted_path_and_finite_residue_actions.tex",
            "label": "thm:collatz-machin-fixed-word-kernel",
        },
        "formal_status": {
            "status": "general_constructive_proof_plus_exact_795_column_certificate",
            "artifact": "research_companion/certificates/arctangent_relation_lattice_checks.py",
            "artifact_sha256": "3b324c5ff1862bdef17d5cc2ab413e85d4a3dd011012fcdde9797dccab08df26",
        },
    },
]
insert_after(
    morphism_lines,
    key="morphism_id",
    marker="MOR-COL-000051",
    records=morphisms,
)


programme_file = STATE / "programmes.jsonl"
programme_lines = load_lines(programme_file)
assert body_ids(programme_lines, "programme_id") == ["PRG-COL-0001"]
set_header(programme_lines, expected="PRG-COL-0002", replacement="PRG-COL-0003")
programme = {
    "record_type": "programme",
    "schema_version": "1.0",
    "programme_id": "PRG-COL-0002",
    "name": "Collatz_prefix_arctangent_Gaussian_relation_lattices",
    "status": "reconstructed_with_exact_fixed_word_all_word_and_finite_grid_theorems_plus_explicit_all_length_conjecture",
    "natural_boundary": "raw Z_n Symmetries physical lines 9597-11087: the ratios 3^(k-1)/2^A_k, their principal arctangents, Cayley units in Q(i), exact multiplicative torsion relations, the chronology's correction of additive-unit-equation language, and the surviving classification question form one programme; exploratory zeta, Heegner, modular, CM, operator, and period rhetoric remains outside absent typed maps",
    "lineage": ["CHATINT-COL-000016 controlling directly read raw chronological passage"],
    "literature_sources": ["SRC-COL-000043", "SRC-COL-000044", "SRC-COL-000045"],
    "definitions": [
        "positive exponent word and cumulative exponents A_k",
        "prefix ratios and principal arctangent angles",
        "Gaussian numerators z_k and norm-one Cayley units u_k",
        "integer relation lattice Rel_pi(w)",
        "fixed-word product map Gamma_bar_w, Gaussian valuation isomorphism nu_G, and signed valuation map E_w",
        "full finite grid G_(15,60) and its exact relation lattice",
    ],
    "sourced_scope_results": ["CLM-COL-000166", "CLM-COL-000167", "CLM-COL-000168"],
    "proved_results": ["CLM-COL-000169", "CLM-COL-000170", "CLM-COL-000171", "CLM-COL-000172"],
    "conjectures": ["CLM-COL-000173"],
    "morphisms": ["MOR-COL-000052", "MOR-COL-000053", "MOR-COL-000054"],
    "repairs": [
        "replaced mu_infinity by the exact torsion group mu_4 inside Q(i)",
        "replaced additive unit-equation language by the exact multiplicative torsion kernel",
        "separated fixed-instance Gaussian decidability from uniform prefix-family rigidity",
        "rejected blanket independence using the exact legal-word 1_1 counterexample",
        "proved the exceptional pair's complete lattice by a Gaussian valuation rather than a literature-dependent shortcut",
        "lifted the finite mod-three kernel to the complete integer grid lattice using torsion-freeness and a primitive unit minor",
    ],
    "contradictions_and_retractions": [
        "the strongest blanket independence assertion is false for w=(1,1)",
        "the raw chronology itself retracts its classical-unit-equation terminology",
        "no universal Baker nonvanishing statement is supplied by the raw notes",
    ],
    "certificates": [
        {
            "path": "research_companion/certificates/arctangent_relation_lattice_checks.py",
            "bytes": 19204,
            "sha256": "3b324c5ff1862bdef17d5cc2ab413e85d4a3dd011012fcdde9797dccab08df26",
            "status": "PASS_exact_795_column_integer_relation_lattice",
        }
    ],
    "live_proof_path": "tex/chapters/03a_chatnotes_arctangent_relations.tex",
    "research_companion_path": "research_companion/chapters/01_weighted_path_and_finite_residue_actions.tex",
    "exact_nonclaims": [
        "no proof of the all-length Collatz-Machin rigidity conjecture",
        "no result outside the certified grid from the finite certificate",
        "no Collatz termination or endpoint theorem",
        "no novelty or priority claim",
        "no zeta, modular, CM, operator, BCM, KMS, or period bridge without an exact typed map",
    ],
    "programme_questions": [],
}
programme_lines.append(dump(programme))


topic_file = STATE / "topic_routes.jsonl"
topic_lines = load_lines(topic_file)
assert len(topic_lines) == 2
assert {json.loads(line)["topic_id"] for line in topic_lines} == {
    "TOPIC-COL-WEIGHTED-PATH-0001",
    "TOPIC-COL-SYMBOLIC-GEOMETRIC-BOUNDARIES-0002",
}
topic = {
    "schema_version": 1,
    "topic_id": "TOPIC-COL-ARCTANGENT-GAUSSIAN-0003",
    "topic": "Collatz prefix arctangent relations, Gaussian prime coordinates, Machin identities, and exact relation lattices",
    "workspace": "C:/Users/LOCAL_USER/Documents/Erdos Strauss and related/collatz_reconstruction",
    "corpus_entrypoint": "C:/Users/LOCAL_USER/Documents/Papors/Chatnotes/Zeta-Function-Foundation/config/literature_index_entrypoint.json",
    "updated_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    "mathematical_objects": [
        "positive Collatz exponent words and cumulative prefix exponents",
        "rational prefix tangents and principal arctangent angles",
        "norm-one Gaussian Cayley units modulo mu_4",
        "oriented split-prime valuation coordinates",
        "fixed-word signed valuation matrices and exact kernels",
        "795-column finite relation lattice",
        "all-length Collatz-Machin rigidity conjecture",
    ],
    "queries": [
        {
            "query": "Gaussian Integers and Arctangent Identities for pi Calcut",
            "layer": "research_literature",
            "index_level": "canonical",
            "executed_utc": "2026-08-29T23:05:00Z",
            "reason": "route the exact rational-arctangent root-of-unity and single-angle source boundary",
            "result_unit_ids": ["PUBUNIT-0F37C9695BAA49C4C5EE414D"],
        },
        {
            "query": "Three essays on Machin's type formulas",
            "layer": "research_literature",
            "index_level": "canonical",
            "executed_utc": "2026-08-29T23:05:00Z",
            "reason": "route the two-term classification and exceptional 1/2,3/4 identity while independently adjudicating corrupted frozen arXiv metadata",
            "result_unit_ids": ["PUBUNIT-DACD031AA11CEAFCEC3782A5"],
        },
    ],
    "sources": [
        {
            "source_class": "research_literature",
            "publication_unit_or_source_id": "SRC-COL-000043",
            "exact_locators": ["source TeX lines 151-168 and 251-306", "SRC-COL-000043"],
            "relevance_edge": "supplies the exact Gaussian-UFD and oriented split-prime coordinate machinery for fixed rational angles",
            "toc_or_section_check": {"status": "checked", "checked_utc": "2026-08-30T00:30:00Z", "relevant_sections": ["Theorems 1-2", "Section 2 d=1 Stormer theory"]},
            "reading_status": "fully_content_read_for_current_dependency",
            "dependencies": [],
            "claim_or_proof_crosswalk_ids": ["CLM-COL-000166", "CLM-COL-000169"],
        },
        {
            "source_class": "research_literature",
            "publication_unit_or_source_id": "PUBUNIT-0F37C9695BAA49C4C5EE414D",
            "exact_locators": ["SRC-COL-000044", "physical PDF pp. 5-7, especially printed pp. 519-520"],
            "relevance_edge": "supplies the exact rational-arctangent mu_4 and single-angle boundary",
            "toc_or_section_check": {"status": "checked", "checked_utc": "2026-08-30T00:30:00Z", "relevant_sections": ["Main Lemma", "Corollaries 1-3"]},
            "reading_status": "fully_content_read_for_current_dependency",
            "dependencies": [],
            "claim_or_proof_crosswalk_ids": ["CLM-COL-000167"],
        },
        {
            "source_class": "research_literature",
            "publication_unit_or_source_id": "PUBUNIT-DACD031AA11CEAFCEC3782A5",
            "exact_locators": ["SRC-COL-000045", "source TeX lines 230-312 and 341-352"],
            "relevance_edge": "supplies the stated two-term classification, Gaussian reformulation, and exceptional 1/2,3/4 identity; the frozen arXiv ID is separately rejected",
            "toc_or_section_check": {"status": "checked", "checked_utc": "2026-08-30T00:30:00Z", "relevant_sections": ["Section 2", "Theorem 1"]},
            "reading_status": "fully_content_read_for_current_dependency",
            "dependencies": [],
            "claim_or_proof_crosswalk_ids": ["CLM-COL-000168", "CLM-COL-000171"],
        },
        {
            "source_class": "local_unpublished_work",
            "publication_unit_or_source_id": "CHATINT-COL-000016",
            "exact_locators": ["raw Z_n Symmetries physical lines 9597-11087", "intake/chatnotes/ZN-SYMMETRIES-ARCTANGENT-DIRECT-LOCATOR-AUDIT-05.md"],
            "relevance_edge": "controlling chronological witness for the local arctangent torsion programme and its internal correction",
            "toc_or_section_check": {"status": "not_available", "checked_utc": "2026-08-30T00:30:00Z", "relevant_sections": [], "reason": "raw chronological export has no controlling table of contents"},
            "reading_status": "fully_content_read_for_current_dependency",
            "dependencies": [],
            "claim_or_proof_crosswalk_ids": ["CLM-COL-000165", "CLM-COL-000170", "CLM-COL-000173"],
        },
    ],
    "unresolved_dependencies": [],
    "refresh_reason": "direct reading of the raw arctangent chronology, content-level reading of three primary literature sources, exact fixed-word morphism reconstruction, two all-length theorems, and a coefficient-unbounded 795-column certificate produced a precise uniform classification conjecture",
    "anti_loop_note": "The completed canonical index was used continuously and not rebuilt. Exact negative searches are recorded only as a bounded source-scope comparison, never as proof of novelty, priority, or nonexistence. The conjecture is not encoded as an obligation or unresolved dependency.",
}
topic_lines.append(dump(topic))


project_state_file = STATE / "project_state.json"
project_state = json.loads(project_state_file.read_text(encoding="utf-8"))
directive_ids = [row["directive_id"] for row in project_state["raw_directives"]]
assert directive_ids[-2:] == ["REF-0001", "REF-0002"]
assert "USR-0012" not in directive_ids and "REF-0003" not in directive_ids
reference_records = project_state["raw_directives"]
reference_records.insert(
    len(reference_records) - 2,
    {
        "directive_id": "USR-0012",
        "path": "raw/USR-0012.txt",
        "bytes": 817,
        "sha256": "cd726fce3faa5fead6897fab54816a63c5851ac822b886287920b4f6e159ff29",
        "role": "controlling_2_GiB_per_Lean_session_resource_ceiling_and_current_hold",
    },
)
reference_records.append(
    {
        "directive_id": "REF-0003",
        "path": "C:/Users/LOCAL_USER/.codex/attachments/dbad1702-848d-4a03-a3de-e8232f9465fe/pasted-text.txt",
        "bytes": 9837,
        "physical_lines": 261,
        "sha256": "2f4c77618d0c35fd9edc5a8798fc67d4e708cf0e28b67d00c7d91b3175228f5e",
        "role": "uncompacted_recent_work_reference_not_independent_mathematical_authority",
    }
)
resource_policy = project_state["resource_policy"]
resource_policy["lean_worker_private_working_set_limit_bytes"] = 2147483648
resource_policy["current_cap_directive"] = "raw/USR-0012.txt"
resource_policy["maximum_overlapping_lean_builds"] = 1
resource_policy["required_resume_mode"] = (
    "current_hold_no_launch; after_verified_release_single_bounded_worker_with_"
    "process_tree_watcher_killing_at_2_GiB"
)
resource_policy["last_enforcement_utc"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
resource_policy["last_enforcement_result"] = (
    "direct_process_check_found_no_task_owned_Lean_or_Lake_worker; clear_signal_sent_to_"
    "Noether_coordinator; current_hold_retained; 2_GiB_cap_recorded"
)
resource_policy["enforcement_events"].append(
    {
        "module": "all_task_owned_Lean_Lake",
        "action": "no_active_worker_clear_signal_sent_then_current_hold_retained_under_new_2_GiB_cap",
        "pids": [],
        "audit_utc": resource_policy["last_enforcement_utc"],
        "delegation_source_thread_id": "01a03474-c8fb-7e73-b549-1420961dc8e4",
        "memory_limit_bytes": 2147483648,
    }
)
resource_policy["serial_coordination_status"] = (
    "no_task_owned_worker_current_hold_active_Noether_guarded_P11_retry_has_priority"
)
project_state["artifact_architecture"]["separately_authored_research_companion"] = (
    "research_companion/main.tex (unsealed ACT42 symbolic and Gaussian-relation additions; final rebuild and package validation pending)"
)
project_state["next_action"] = (
    "Finish ACT42 by rebuilding and validating both independent TeX/PDF artifacts, visually checking every page, sealing the exact arctangent source/claim/morphism/programme crosswalk and fresh-context recovery, then continue the remaining direct modern Chatnotes intake at lines 11088-14011. Keep Gemini and archived-task intake deferred, do not contact the quarantined zeta task, do not publish or upload, and keep Lean/Lake idle under the 2 GiB-per-session ceiling until a verified release."
)
project_state["updated_utc"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
checkpoint = project_state["current_checkpoint"]
assert checkpoint["receipt_id"] == "ACT-COL-000041"
checkpoint["post_checkpoint_state_changed"] = True
checkpoint["post_checkpoint_change"] = (
    "unsealed_ACT42_symbolic_completion_and_arctangent_Gaussian_relation_layer_awaiting_final_build_QA_and_receipt"
)
checkpoint["fresh_context_recovery_required_after_current_intake"] = True


append_jsonl(intake_file, intake_lines)
append_jsonl(source_file, source_lines)
append_jsonl(claim_file, claim_lines)
append_jsonl(morphism_file, morphism_lines)
append_jsonl(programme_file, programme_lines)
append_jsonl(topic_file, topic_lines)
project_state_file.write_text(
    json.dumps(project_state, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)


assert body_ids(load_lines(intake_file), "intake_id") == [
    f"CHATINT-COL-{number:06d}" for number in range(1, 17)
]
assert set(body_ids(load_lines(source_file), "source_id")) == {
    f"SRC-COL-{number:06d}" for number in range(1, 46)
}
assert set(body_ids(load_lines(claim_file), "claim_id")) == {
    f"CLM-COL-{number:06d}" for number in range(1, 174)
}
assert set(body_ids(load_lines(morphism_file), "morphism_id")) == {
    f"MOR-COL-{number:06d}" for number in range(1, 55)
}
assert body_ids(load_lines(programme_file), "programme_id") == [
    "PRG-COL-0001",
    "PRG-COL-0002",
]
assert len(load_lines(topic_file)) == 3

print(
    json.dumps(
        {
            "status": "PASS",
            "chatnotes_records": 16,
            "sources": 45,
            "claims": 173,
            "morphisms": 54,
            "programmes": 2,
            "topic_routes": 3,
            "new_resource_ceiling_bytes": 2147483648,
        },
        indent=2,
        sort_keys=True,
    )
)
