"""Admit the exact coefficient-algebra core after direct source verification."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

EXPECTED = {
    "state/chatnotes_intake.jsonl": "16ee9e20235e90038033e18ed38b083abe3ccda016f61e7c05b28be8e3bf5f56",
    "state/source_registry.jsonl": "4173625b117fb4d6aa234c9c58713260ab6de8ed4dc1d9f5e271e1e4875c2a56",
    "state/claims.jsonl": "d474bdb20217cb007b1a4d3618a6d602f4c6b09aecad1a2b2c57daa8c069e9a0",
    "state/morphisms.jsonl": "3e4dfe7f45b27ab4190c210d9cc385178530a9729d494ecf8b4dbb9351de96e7",
    "intake/chatnotes/ZN-SYMMETRIES-DIRECT-LOCATOR-AUDIT-02.md": "f5dbc9bbef2f1573b82c0dcb7691151f6912776a2baf2f0ef47f43e9f43b9d8a",
    "qa/AIZAWA-ISAAC-SEGAR-2018-F032-color-coefficient-crosswalk.md": "bcdd724d3b5a0210671b6a8792adf04d79f3954c399cc1c38c6778daa237115a",
    "certificates/chatnotes_color_coefficient_checks.py": "f273138b2ae71f3ad86738f5abd8bb01fba5a4eac7a3e4d2a222581aceea008e",
}

RAW_CHAT = Path(
    r"C:\Users\LOCAL_USER\Documents\Obsidian notes\ChatGPT-Branch · Z_n Symmetries of Collatz.md"
)
ARXIV_ARCHIVE = Path(
    r"C:\Users\LOCAL_USER\Documents\arxiv_latex\library\collatz_reconstruction\source\1808.09112v1.eprint"
)
ARXIV_TEX = Path(
    r"C:\Users\LOCAL_USER\Documents\arxiv_latex\library\collatz_reconstruction\latex\1808.09112v1\Z2-N1-ellv5.tex"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text(
        "\n".join(
            json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in rows
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> None:
    for relative, expected in EXPECTED.items():
        path = ROOT / relative
        assert path.is_file(), path
        assert sha256(path) == expected, path

    assert sha256(RAW_CHAT) == "9a80f53764a9da42c0f8e0b6d19ce61f978980a448a683b9c45f04038716160d"
    assert RAW_CHAT.stat().st_size == 538005
    assert len(RAW_CHAT.read_text(encoding="utf-8").splitlines()) == 17437
    assert sha256(ARXIV_ARCHIVE) == "d5361e762a6f8f0983aabe62fa9256c9a9adf0531dc3cefccd2f187324dd76b0"
    assert ARXIV_ARCHIVE.stat().st_size == 14499
    assert sha256(ARXIV_TEX) == "168e9e0b3c524c0813c795b357c87fbacabf9d4d013f430330b63fc4a46562ab"
    assert ARXIV_TEX.stat().st_size == 48693
    assert len(ARXIV_TEX.read_text(encoding="utf-8").splitlines()) == 1127

    intake_path = ROOT / "state" / "chatnotes_intake.jsonl"
    intake = read_jsonl(intake_path)
    assert intake[0]["next_id"] == "CHATINT-COL-000012"
    assert intake[-1]["intake_id"] == "CHATINT-COL-000011"
    intake[0]["next_id"] = "CHATINT-COL-000013"
    intake[1]["content_status"] = (
        "all_physical_lines_have_chronological_intake_reports_lines_1_12000_"
        "agent_derived_unadmitted_lines_12001_17437_main_report_unadmitted_"
        "direct_locator_audits_01_and_02_complete_through_raw_line_6220_"
        "bounded_coefficient_results_admitted_separately_weighted_path_continuation_pending"
    )
    intake.append(
        {
            "record_type": "chatnotes_locator_audit",
            "schema_version": "1.0",
            "intake_id": "CHATINT-COL-000012",
            "source_intake_id": "CHATINT-COL-000001",
            "audit_scope": "raw_lines_5712_6220_complete_direct_read",
            "primary_source_id": "SRC-COL-000033",
            "admission_status": "bounded_independently_proved_claims_admitted_separately_programme_boundary_not_frozen",
            "report_path": "intake/chatnotes/ZN-SYMMETRIES-DIRECT-LOCATOR-AUDIT-02.md",
            "report_bytes": 10242,
            "report_sha256": "f5dbc9bbef2f1573b82c0dcb7691151f6912776a2baf2f0ef47f43e9f43b9d8a",
            "certificate_path": "certificates/chatnotes_color_coefficient_checks.py",
            "certificate_sha256": "f273138b2ae71f3ad86738f5abd8bb01fba5a4eac7a3e4d2a222581aceea008e",
            "verified_findings": [
                "four_affine_labels_are_an_injective_set_map_not_an_additive_group_action",
                "F_ab_of_n_is_integral_exactly_when_n_mod_2_equals_b",
                "Delta_is_kernel_of_a_plus_b_and_pointwise_H_requires_state_dependent_iota_evaluation",
                "raw_orthogonal_idempotent_rules_are_function_algebra_or_Fourier_basis_not_group_element_basis",
                "Fourier_primitive_idempotents_give_an_exact_unital_algebra_isomorphism_but_not_the_natural_V_grading",
                "diagonal_projection_retains_two_components_and_is_not_the_scalar_H_without_evaluation",
                "Aizawa_Isaac_Segar_supports_its_color_definition_and_enveloping_construction_not_a_Collatz_action",
                "coordinate_swap_fixes_Delta_while_diagonal_exchange_is_translation_by_11",
                "chosen_S_and_J_satisfy_O2_relations_but_J_is_additional_structure",
                "Spin_SU2_quotient_and_Delta_kernel_remain_unmapped_distinct_operations",
            ],
        }
    )
    write_jsonl(intake_path, intake)

    source_path = ROOT / "state" / "source_registry.jsonl"
    sources = read_jsonl(source_path)
    assert sources[0]["next_id"] == "SRC-COL-000033"
    assert sources[-1]["source_id"] == "SRC-COL-000032"
    sources[0]["next_id"] = "SRC-COL-000034"
    sources.append(
        {
            "record_type": "source_document",
            "schema_version": "1.0",
            "source_id": "SRC-COL-000033",
            "authors": ["Naruhiko Aizawa", "Peter S. Isaac", "J. Segar"],
            "title": "Z2 x Z2 generalizations of N=1 superconformal Galilei algebras and their representations",
            "bibliographic_identity": {
                "arxiv_version_id": "1808.09112v1",
                "arxiv_submitted": "2018-08-28T04:34:54Z",
                "arxiv_primary_class": "math-ph",
                "arxiv_record": "https://arxiv.org/abs/1808.09112",
                "journal": "Journal of Mathematical Physics",
                "volume": "60",
                "publication_year": 2019,
                "article_number": "023507",
                "doi": "10.1063/1.5054699",
                "version_count_on_official_record": 1,
            },
            "manifestations": [
                {
                    "path": "C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/source/1808.09112v1.eprint",
                    "role": "official_arxiv_v1_gzip_single_TeX_source_archive",
                    "bytes": 14499,
                    "sha256": "d5361e762a6f8f0983aabe62fa9256c9a9adf0531dc3cefccd2f187324dd76b0",
                },
                {
                    "path": "C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/latex/1808.09112v1/Z2-N1-ellv5.tex",
                    "role": "decompressed_complete_arxiv_v1_source_TeX",
                    "bytes": 48693,
                    "source_lines": 1127,
                    "sha256": "168e9e0b3c524c0813c795b357c87fbacabf9d4d013f430330b63fc4a46562ab",
                },
            ],
            "route_ids": [],
            "route_integrity": {
                "status": "exact_author_title_and_arxiv_ID_miss_then_bounded_local_filename_miss_and_official_arxiv_acquisition",
                "queried": [
                    "state/index_routes.jsonl",
                    "state/document_routes.jsonl",
                    "authorized_Papors_and_arxiv_latex_filename_roots",
                    "authorized_Obsidian_and_Downloads_filename_roots",
                ],
                "frozen_ledgers_mutated": False,
            },
            "reading": {
                "status": "complete_substantive_source_TeX_content_read_and_Collatz_boundary_crosswalked",
                "locators": [
                    "source lines 69-118: title, authors, and abstract",
                    "source lines 130-193: introduction, results, and paper plan",
                    "source lines 203-251: V grading, bilinear form, color bracket, and enveloping-algebra realization",
                    "source lines 256-296: N=1 superconformal Galilei algebra and central extension",
                    "source lines 308-501: quadratic composites, four degree assignments, both complete relation systems, and Jacobi closure statements",
                    "source lines 505-653: triangular decomposition, adjoint, and superadjoint",
                    "source lines 665-984: boson-fermion and color-supergroup vector-field representations",
                    "source lines 995-1024: conclusions and future-work boundary",
                    "qa/AIZAWA-ISAAC-SEGAR-2018-F032-color-coefficient-crosswalk.md",
                ],
                "certificate": {
                    "path": "certificates/chatnotes_color_coefficient_checks.py",
                    "status": "pass_finite_exact_source_signatures_and_coefficient_algebra",
                    "sha256": "f273138b2ae71f3ad86738f5abd8bb01fba5a4eac7a3e4d2a222581aceea008e",
                },
            },
            "exact_results_used": [
                "definition of a V-graded color superalgebra with dot-product sign rule",
                "enveloping-algebra formula for the color bracket",
                "quadratic composites P_nm Lambda_nm X_nm and their four degree assignments",
                "closure of the paper's two explicit color-superalgebra constructions",
            ],
            "nonclaims": [
                "The paper contains no Collatz map, parity evaluator, affine branch action, weighted path, or arithmetic transfer operator.",
                "The paper supplies no morphism from the local coefficient algebra to either of its color superalgebras.",
                "Its closure statements do not imply a color-superalgebra action on Collatz states or observables.",
                "It does not address or reformulate the Collatz conjecture.",
            ],
        }
    )
    write_jsonl(source_path, sources)

    claims_path = ROOT / "state" / "claims.jsonl"
    claims = read_jsonl(claims_path)
    assert claims[0]["next_id"] == "CLM-COL-000137"
    assert claims[-1]["claim_id"] == "CLM-COL-000136"
    claims[0]["next_id"] = "CLM-COL-000142"
    claims.extend(
        [
            {
                "record_type": "claim",
                "schema_version": "1.0",
                "claim_id": "CLM-COL-000137",
                "claim_type": "sourced_color_superalgebra_definition_and_enveloping_construction",
                "status": "primary_source_content_read_at_exact_scope",
                "statement": "For V=F_2^2 with B(u,v)=u_1v_1+u_2v_2, Aizawa--Isaac--Segar define a V-graded color superalgebra and its enveloping color bracket. From an N=1 superconformal Galilei algebra they construct quadratic composites P_nm, Lambda_nm, X_nm, assign the exact degrees 00,01,10,11 displayed in the source, and verify closure and graded Jacobi compatibility for their two explicit constructions.",
                "source_ids": ["SRC-COL-000033"],
                "dependencies": [],
                "source_locators": [
                    "Aizawa--Isaac--Segar source lines 203-251",
                    "Aizawa--Isaac--Segar source lines 308-501",
                    "qa/AIZAWA-ISAAC-SEGAR-2018-F032-color-coefficient-crosswalk.md",
                ],
                "proof_locator": {
                    "path": "tex/chapters/02_chatnotes_coefficient_algebra.tex",
                    "label": "sec:chatnotes-coefficient-algebra",
                },
                "nonclaims": [
                    "No Collatz object occurs in the source.",
                    "The sourced closure theorem is not transferred to local coefficient labels without a new morphism.",
                ],
            },
            {
                "record_type": "claim",
                "schema_version": "1.0",
                "claim_id": "CLM-COL-000138",
                "claim_type": "independent_exact_affine_label_and_parity_evaluator_theorem",
                "status": "proved",
                "statement": "The map lambda(a,b)=((1+2a)/2,b/2) injects V into the underlying set of invertible rational affine maps but is not a group homomorphism under composition. F_(a,b)(n) is integral exactly when n mod 2=b. With Delta=ker(a+b) and iota(n)=(n mod 2,n mod 2), the graph map eta(n)=(n,iota(n)) is a bijection onto its typed graph and the shortened Collatz map factors exactly as H=E o eta, E(n,v)=F_v(n).",
                "source_ids": [],
                "dependencies": [],
                "local_source_refs": ["CHATINT-COL-000012"],
                "source_locators": ["raw Z_n Symmetries physical lines 5744-5833"],
                "proof_locator": {
                    "path": "tex/chapters/02_chatnotes_coefficient_algebra.tex",
                    "label": "prop:chatnotes-diagonal-evaluator",
                },
                "morphism_refs": ["MOR-COL-000034", "MOR-COL-000035"],
                "formal_status": {
                    "status": "pass_finite_exact_certificate",
                    "artifact": "certificates/chatnotes_color_coefficient_checks.py",
                    "artifact_sha256": "f273138b2ae71f3ad86738f5abd8bb01fba5a4eac7a3e4d2a222581aceea008e",
                    "verified_metrics": {
                        "affine_labels": 4,
                        "affine_composition_equalities_out_of_16": 0,
                        "integrality_checks": 8004,
                        "parity_evaluation_checks": 2001,
                    },
                },
                "lineage_status": "raw_Chatnotes_result_independently_proved_programme_and_authorship_boundary_not_yet_frozen",
                "nonclaims": [
                    "The four labels do not act on states by the additive group law.",
                    "The factorization does not identify iteration with addition in V.",
                ],
            },
            {
                "record_type": "claim",
                "schema_version": "1.0",
                "claim_id": "CLM-COL-000139",
                "claim_type": "independent_coefficient_algebra_type_and_grading_obstruction",
                "status": "proved",
                "statement": "The raw orthogonal idempotent multiplication e_u e_w=delta_(u,w)e_u is the point-mass basis of Map(V,C), not the group-element basis of C[V]. In the natural V-grading of C[V], every nonzero Fourier primitive idempotent is nonhomogeneous; more generally a nonzero idempotent cannot be homogeneous of nonzero degree u because u+u=0.",
                "source_ids": ["SRC-COL-000033"],
                "dependencies": ["CLM-COL-000137"],
                "local_source_refs": ["CHATINT-COL-000012"],
                "source_locators": ["raw Z_n Symmetries physical lines 5967-6003"],
                "proof_locator": {
                    "path": "tex/chapters/02_chatnotes_coefficient_algebra.tex",
                    "label": "thm:chatnotes-fourier-algebra-isomorphism",
                },
                "formal_status": {
                    "status": "pass_finite_exact_certificate",
                    "artifact": "certificates/chatnotes_color_coefficient_checks.py",
                    "artifact_sha256": "f273138b2ae71f3ad86738f5abd8bb01fba5a4eac7a3e4d2a222581aceea008e",
                    "verified_metrics": {
                        "function_basis_product_checks": 16,
                        "group_basis_product_checks": 16,
                        "naive_homogeneous_idempotent_obstructions": 3,
                    },
                },
                "nonclaims": [
                    "An algebra isomorphism does not identify the natural bases or preserve the natural V-grading.",
                ],
            },
            {
                "record_type": "claim",
                "schema_version": "1.0",
                "claim_id": "CLM-COL-000140",
                "claim_type": "independent_exact_Fourier_repair_and_diagonal_evaluation_theorem",
                "status": "proved",
                "statement": "The map delta_u -> p_u=(1/4)sum_v(-1)^(B(u,v))g_v is a unital algebra isomorphism Map(V,C)->C[V], with inverse g_v -> sum_u(-1)^(B(u,v))delta_u. Diagonal projection gives the two-component family delta_00 X/2+delta_11(3X+1)/2; the scalar shortened Collatz value is recovered only after evaluation at the state-dependent label iota(n). Under Fourier transform the projector is (g_00+g_11)/2.",
                "source_ids": ["SRC-COL-000033"],
                "dependencies": ["CLM-COL-000138", "CLM-COL-000139"],
                "local_source_refs": ["CHATINT-COL-000012"],
                "source_locators": ["raw Z_n Symmetries physical lines 5967-6003 and 6171-6187"],
                "proof_locator": {
                    "path": "tex/chapters/02_chatnotes_coefficient_algebra.tex",
                    "label": "thm:chatnotes-fourier-algebra-isomorphism",
                },
                "morphism_refs": ["MOR-COL-000033", "MOR-COL-000034"],
                "formal_status": {
                    "status": "pass_finite_exact_certificate",
                    "artifact": "certificates/chatnotes_color_coefficient_checks.py",
                    "artifact_sha256": "f273138b2ae71f3ad86738f5abd8bb01fba5a4eac7a3e4d2a222581aceea008e",
                    "verified_metrics": {"fourier_idempotent_product_checks": 16},
                },
                "nonclaims": [
                    "Projection alone is not the scalar map H.",
                    "The Fourier repair supplies no color-superalgebra action or iteration law.",
                ],
            },
            {
                "record_type": "claim",
                "schema_version": "1.0",
                "claim_id": "CLM-COL-000141",
                "claim_type": "independent_isotropic_diagonal_and_involution_separation_theorem",
                "status": "proved_at_exact_algebra_and_matrix_scope",
                "statement": "For every associative V-graded algebra with the Aizawa--Isaac--Segar sign pairing, A_00 direct-sum A_11 is closed and its color commutator is the ordinary commutator because Delta is totally isotropic. Coordinate swap fixes Delta pointwise, whereas exchange of its two labels is translation by 11 and is not a group automorphism. After independently choosing the displayed matrices S and J, they satisfy the O(2) relations; J and the resulting O(2) block are not intrinsic to the Collatz coefficient datum.",
                "source_ids": ["SRC-COL-000033"],
                "dependencies": ["CLM-COL-000137", "CLM-COL-000138", "CLM-COL-000139", "CLM-COL-000140"],
                "local_source_refs": ["CHATINT-COL-000012"],
                "source_locators": ["raw Z_n Symmetries physical lines 5838-5959 and 6008-6217"],
                "proof_locator": {
                    "path": "tex/chapters/02_chatnotes_coefficient_algebra.tex",
                    "label": "lem:chatnotes-isotropic-diagonal",
                },
                "related_gap_ids": ["GAP-COL-000003"],
                "formal_status": {
                    "status": "pass_finite_exact_certificate",
                    "artifact": "certificates/chatnotes_color_coefficient_checks.py",
                    "artifact_sha256": "f273138b2ae71f3ad86738f5abd8bb01fba5a4eac7a3e4d2a222581aceea008e",
                },
                "nonclaims": [
                    "No graded Collatz algebra, bracket morphism, representation, or color action has been constructed.",
                    "No intrinsic O(2) action, determinant anomaly, or Spin--SU(2) quotient for Collatz follows.",
                    "A quotient by a diagonal central subgroup is not identified with taking the kernel Delta.",
                ],
            },
        ]
    )
    write_jsonl(claims_path, claims)

    morphisms_path = ROOT / "state" / "morphisms.jsonl"
    morphisms = read_jsonl(morphisms_path)
    assert morphisms[0]["next_id"] == "MOR-COL-000033"
    assert morphisms[-1]["morphism_id"] == "MOR-COL-000032"
    morphisms[0]["next_id"] = "MOR-COL-000036"
    morphisms.extend(
        [
            {
                "record_type": "morphism",
                "schema_version": "1.0",
                "morphism_id": "MOR-COL-000033",
                "name": "finite_coefficient_Fourier_algebra_isomorphism",
                "domain": "A=Map(V,C) for V=F_2^2, with pointwise multiplication and point-mass basis delta_u.",
                "codomain": "B=C[V], with convolution/group multiplication in the group-element basis g_v.",
                "formula": "F(delta_u)=p_u=(1/4) sum_(v in V)(-1)^(u dot v) g_v; F^(-1)(g_v)=sum_(u in V)(-1)^(u dot v) delta_u.",
                "well_definedness": "The delta_u and g_v are bases. Character orthogonality proves p_u p_w=delta_(u,w)p_u, sum_u p_u=g_00, and g_v=sum_u(-1)^(u dot v)p_u.",
                "preserved_structure": "Complex linear combinations, multiplication, unit, orthogonal-idempotent decomposition, and all algebra information are preserved.",
                "fibres": "Every fibre is a singleton; the equality kernel pair is the diagonal on A.",
                "inverse_status": "The displayed formula on g_v is a two-sided inverse, proved by the four-character orthogonality identities.",
                "exceptions": [
                    "The isomorphism does not send the point-mass labels to the group-element basis.",
                    "It does not preserve the natural V-grading of C[V]; each p_u has four nonzero homogeneous components.",
                    "It supplies no iteration law or color-superalgebra action on Collatz states.",
                ],
                "claim_refs": ["CLM-COL-000139", "CLM-COL-000140"],
                "source_refs": ["SRC-COL-000033"],
                "proof_locator": {
                    "path": "tex/chapters/02_chatnotes_coefficient_algebra.tex",
                    "label": "thm:chatnotes-fourier-algebra-isomorphism",
                },
                "formal_status": {
                    "status": "pass_finite_exact_certificate",
                    "artifact": "certificates/chatnotes_color_coefficient_checks.py",
                    "artifact_sha256": "f273138b2ae71f3ad86738f5abd8bb01fba5a4eac7a3e4d2a222581aceea008e",
                },
            },
            {
                "record_type": "morphism",
                "schema_version": "1.0",
                "morphism_id": "MOR-COL-000034",
                "name": "integer_state_to_parity_label_graph_bijection_and_branch_evaluator_factorization",
                "domain": "The additive group Z, carrying the shortened Collatz branch evaluator H as additional displayed data.",
                "codomain": "D={(n,v) in Z x Delta : v=(n mod 2,n mod 2)}, with Delta={00,11}.",
                "formula": "eta(n)=(n,iota(n)), iota(n)=(n mod 2,n mod 2); E(n,v)=F_v(n); H=E o eta.",
                "well_definedness": "iota(n) lies in Delta. On D the second coordinate b equals n mod 2, so F_v(n) is integral. Direct substitution gives H on both parity fibres.",
                "preserved_structure": "eta retains the integer state exactly and appends its unique admissible coefficient label. iota is a surjective group homomorphism Z->Delta with kernel 2Z; eta preserves equality and the complete state coordinate.",
                "fibres": "eta has singleton fibres and diagonal equality kernel. iota has fibres 2Z and 2Z+1 over 00 and 11 respectively.",
                "inverse_status": "First projection D->Z is the two-sided inverse of eta. E is an evaluator, not asserted to be invertible.",
                "exceptions": [
                    "H itself is not asserted to be a group homomorphism.",
                    "The factorization is pointwise and does not identify H iteration with addition in Delta or V.",
                    "No orbit, period, density, or endpoint theorem follows from the label graph alone.",
                ],
                "claim_refs": ["CLM-COL-000138", "CLM-COL-000140"],
                "source_refs": [],
                "proof_locator": {
                    "path": "tex/chapters/02_chatnotes_coefficient_algebra.tex",
                    "label": "prop:chatnotes-diagonal-evaluator",
                },
                "formal_status": {
                    "status": "pass_finite_exact_certificate",
                    "artifact": "certificates/chatnotes_color_coefficient_checks.py",
                    "artifact_sha256": "f273138b2ae71f3ad86738f5abd8bb01fba5a4eac7a3e4d2a222581aceea008e",
                },
            },
            {
                "record_type": "morphism",
                "schema_version": "1.0",
                "morphism_id": "MOR-COL-000035",
                "name": "four_label_affine_set_embedding",
                "domain": "The underlying four-element set of V=F_2^2.",
                "codomain": "The underlying set of Aff_Q^x={X->mX+c:m in Q^x,c in Q}.",
                "formula": "lambda(a,b)=F_(a,b), with affine coordinates ((1+2a)/2,b/2).",
                "well_definedness": "Both possible slopes are nonzero rational numbers, so all four formulas are invertible affine maps. Equality of slopes and intercepts separately recovers a and b.",
                "preserved_structure": "Equality, the slope bit, the intercept/integrality-selector bit, and the four distinct affine formulas are preserved.",
                "fibres": "Every fibre on the image is a singleton; the equality kernel pair is the diagonal on V.",
                "inverse_status": "On the image, an affine coordinate (m,c) returns a=(2m-1)/2 and b=2c, which are in {0,1}. There is no inverse outside the four-point image.",
                "exceptions": [
                    "This is a set embedding, not a homomorphism from additive V to affine composition: lambda(00)=X/2 is not the affine identity.",
                    "The certificate finds zero composition equalities lambda(v) o lambda(w)=lambda(v+w) among all sixteen ordered pairs.",
                    "No action, semiconjugacy, or iteration morphism is asserted.",
                ],
                "claim_refs": ["CLM-COL-000138"],
                "source_refs": [],
                "proof_locator": {
                    "path": "tex/chapters/02_chatnotes_coefficient_algebra.tex",
                    "label": "prop:chatnotes-affine-label-map",
                },
                "formal_status": {
                    "status": "pass_finite_exact_certificate",
                    "artifact": "certificates/chatnotes_color_coefficient_checks.py",
                    "artifact_sha256": "f273138b2ae71f3ad86738f5abd8bb01fba5a4eac7a3e4d2a222581aceea008e",
                },
            },
        ]
    )
    write_jsonl(morphisms_path, morphisms)

    print(
        json.dumps(
            {
                "status": "PASS",
                "chatnotes_intake_records": len(intake) - 1,
                "source_records": len(sources) - 1,
                "claim_records": len(claims) - 1,
                "morphism_records": len(morphisms) - 1,
                "post_hashes": {
                    "chatnotes_intake": sha256(intake_path),
                    "source_registry": sha256(source_path),
                    "claims": sha256(claims_path),
                    "morphisms": sha256(morphisms_path),
                },
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
