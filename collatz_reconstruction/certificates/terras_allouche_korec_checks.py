"""Finite checks for the Terras--Allouche--Korec density lineage.

This certificate pins the four primary scans, both Tao source manifestations
whose introductory formula is audited, and the immutable route artifacts.  It
checks exact finite residue coordinates and exact rational enclosures for the
elementary logarithmic comparisons used by F030.  Printed defective formulas
and their repairs are represented by different functions or expressions.

The checks below do not prove a central limit theorem, pass from finite blocks
to an infinite natural-density limit, prove Tao's analytic theorem, or prove
the Collatz conjecture.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import re
import subprocess
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHELF = Path(
    r"C:\Users\LOCAL_USER\Documents\arxiv_latex\library\collatz_reconstruction"
)
PUBLISHED = SHELF / "published"
TAO_V5 = SHELF / "latex" / "1909.03562v5" / "collatz.tex"
TAO_V7 = SHELF / "latex" / "1909.03562v7" / "collatz.tex"
F030 = ROOT / "qa" / "TERRAS-ALLOUCHE-KOREC-F030-density-lineage-audit.md"


PDF_PINS = {
    PUBLISHED / "Terras-1976-A-stopping-time-problem.pdf": (
        646_395,
        "2b9c296a05541c5b52f63482a09982519546eba36f581bddd853af6ca014bf89",
        7,
    ),
    PUBLISHED / "Terras-1979-On-the-existence-of-a-density.pdf": (
        134_556,
        "6cb5efbda449752cc0e815f630680f4153aa3ee62a548307041f7968b5d0e47b",
        2,
    ),
    PUBLISHED / "Allouche-1979-Syracuse-Kakutani-Collatz.pdf": (
        1_160_082,
        "96f959368e5417dcc6d432e4831f3cf957e7b0db687b916a6aed0262102a01b6",
        17,
    ),
    PUBLISHED / "Korec-1994-A-density-estimate.pdf": (
        383_521,
        "3111bcc638a563fa4395d8a090a4b563116f1ffe30aee136f6e24a76d4d97c77",
        6,
    ),
}

ROUTE_PINS = {
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

TAO_SOURCE_PINS = {
    TAO_V5: (
        163_356,
        "c676b362b30807aa6690d0d4f16b8c8e84324732f5c0eb72ccfd875000276ae0",
    ),
    TAO_V7: (
        164_932,
        "bfbc39432d4084a276416cb019a592003c868fa32f18e2f90028ac325ae5c19d",
    ),
}

F030_AUDIT_PIN: tuple[int, str] | None = (
    28_949,
    "3765a2ef9a98ed101ad387f64e9f707fe714e0a64c8479ea012bc1ef846ec6ba",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_pin(path: Path, expected_bytes: int, expected_hash: str) -> None:
    assert path.is_file(), path
    assert path.stat().st_size == expected_bytes, (
        path,
        path.stat().st_size,
        expected_bytes,
    )
    assert sha256(path) == expected_hash, path


def pdf_pages(path: Path) -> int:
    info = subprocess.run(
        ["pdfinfo", str(path)],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    ).stdout
    match = re.search(r"(?m)^Pages:\s+(\d+)\s*$", info)
    assert match is not None, path
    return int(match.group(1))


def log_bounds(value: Fraction, terms: int = 120) -> tuple[Fraction, Fraction]:
    """Return a rigorous rational enclosure for log(value).

    For value >= 1, use

        log(value) = 2 sum_{j>=0} z^(2j+1)/(2j+1),
        z = (value-1)/(value+1).

    The omitted positive tail is bounded by its first denominator times the
    geometric tail.  Every operation in this function is rational.
    """

    assert value >= 1
    z = (value - 1) / (value + 1)
    partial = sum(
        (z ** (2 * j + 1) / (2 * j + 1) for j in range(terms)),
        Fraction(),
    )
    lower = 2 * partial
    first_omitted = 2 * z ** (2 * terms + 1) / (2 * terms + 1)
    upper = lower + first_omitted / (1 - z * z)
    return lower, upper


def quotient_bounds(
    numerator: tuple[Fraction, Fraction],
    denominator: tuple[Fraction, Fraction],
) -> tuple[Fraction, Fraction]:
    n_lower, n_upper = numerator
    d_lower, d_upper = denominator
    assert 0 < n_lower <= n_upper
    assert 0 < d_lower <= d_upper
    return n_lower / d_upper, n_upper / d_lower


def logarithmic_threshold_checks() -> dict[str, str | bool]:
    ln2 = log_bounds(Fraction(2))
    ln3 = log_bounds(Fraction(3))
    log2_of_3 = quotient_bounds(ln3, ln2)
    log3_of_2 = quotient_bounds(ln2, ln3)

    bad_lower = Fraction(3, 2) - log2_of_3[1]
    bad_upper = Fraction(3, 2) - log2_of_3[0]
    allouche_lower = Fraction(3, 2) - log3_of_2[1]
    allouche_upper = Fraction(3, 2) - log3_of_2[0]
    korec_lower = log2_of_3[0] / 2
    korec_upper = log2_of_3[1] / 2
    error_lower = 1 - log3_of_2[1]
    error_upper = 1 - log3_of_2[0]

    # Tao's printed formula is negative, hence cannot equal its positive
    # decimal.  The enclosure also certifies the repaired decimal windows.
    assert bad_upper < 0
    assert Fraction(869, 1000) < allouche_lower
    assert allouche_upper < Fraction(87, 100)
    assert Fraction(792, 1000) < korec_lower
    assert korec_upper < Fraction(793, 1000)

    # Korec's strict threshold is strictly better than the repaired Allouche
    # threshold.  The affine-remainder error exponent is lower still.
    assert error_upper < korec_lower
    assert korec_upper < allouche_lower
    assert error_upper < allouche_lower
    assert Fraction(3, 2) - Fraction(7, 11) - (1 - Fraction(7, 11)) == Fraction(1, 2)

    lines_v5 = TAO_V5.read_text(encoding="utf-8").splitlines()
    lines_v7 = TAO_V7.read_text(encoding="utf-8").splitlines()
    assert len(lines_v5) == 1_945
    assert len(lines_v7) == 1_956
    printed = r"\frac{3}{2} - \frac{\log 3}{\log 2} \approx 0.869"
    korec = r"\frac{\log 3}{\log 4} \approx 0.7924"
    assert printed in lines_v5[164]
    assert printed in lines_v7[164]
    assert korec in lines_v5[164]
    assert korec in lines_v7[164]
    assert lines_v5[164].rstrip() == lines_v7[164].rstrip()

    return {
        "tao_printed_bad_formula_rigorously_negative": True,
        "correct_allouche_threshold_enclosure": "869/1000 < c_A < 87/100",
        "korec_threshold_enclosure": "792/1000 < c_K < 793/1000",
        "threshold_order": "error exponent < c_K < c_A",
        "allouche_minus_error_exponent": "1/2 exactly",
        "tao_v5_v7_line_165_exact_match": True,
    }


def terras_t(n: int) -> int:
    assert n >= 0
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def terras_parity_vector(n: int, length: int) -> tuple[int, ...]:
    bits: list[int] = []
    for _ in range(length):
        bits.append(n % 2)
        n = terras_t(n)
    return tuple(bits)


def terras_iterate(n: int, length: int) -> int:
    for _ in range(length):
        n = terras_t(n)
    return n


def floor_interval(lower: Fraction, upper: Fraction) -> int:
    assert lower <= upper
    floor_lower = lower.numerator // lower.denominator
    floor_upper = upper.numerator // upper.denominator
    assert floor_lower == floor_upper, (lower, upper)
    return floor_lower


def terminal_words(length: int) -> list[tuple[int, ...]]:
    result: list[tuple[int, ...]] = []
    for word in itertools.product((0, 1), repeat=length):
        ones = 0
        proper_prefixes_active = True
        for index, bit in enumerate(word, start=1):
            ones += bit
            if index < length and 3**ones <= 2**index:
                proper_prefixes_active = False
                break
        if proper_prefixes_active and 3**sum(word) < 2**length:
            result.append(word)
    return result


def terras_finite_checks() -> dict[str, int | bool | list[int]]:
    parity_max_length = 13
    parity_vectors_checked = 0
    affine_coordinates_checked = 0
    for length in range(1, parity_max_length + 1):
        vectors = {
            terras_parity_vector(residue, length)
            for residue in range(2**length)
        }
        expected = set(itertools.product((0, 1), repeat=length))
        assert vectors == expected
        parity_vectors_checked += 2**length

        for residue in range(2**length):
            word = terras_parity_vector(residue, length)
            coefficient = Fraction(3 ** sum(word), 2**length)
            remainder = Fraction(terras_iterate(residue, length)) - coefficient * residue
            assert remainder >= 0
            assert Fraction(terras_iterate(residue, length)) == coefficient * residue + remainder
            affine_coordinates_checked += 1

    # Proposition 1.7 is false without lambda_k < 1.
    n = 1
    image = terras_t(n)
    coefficient = Fraction(3, 2)
    remainder = Fraction(1, 2)
    assert not image < n
    assert remainder / (1 - coefficient) < n
    assert coefficient > 1

    gamma = quotient_bounds(log_bounds(Fraction(2)), log_bounds(Fraction(3)))
    terminal_max_length = 19
    terminal_counts: list[int] = []
    terminal_words_checked = 0
    for length in range(1, terminal_max_length + 1):
        words = terminal_words(length)
        terminal_counts.append(len(words))
        terminal_words_checked += len(words)

        x_lower = (length - 1) * (1 - gamma[1])
        x_upper = (length - 1) * (1 - gamma[0])
        repaired_cutoff = floor_interval(x_lower, x_upper) + 1

        for word in words:
            zeros = length - sum(word)
            assert word[-1] == 0
            if length > 1:
                assert 3 ** sum(word) > 2 ** (length - 1)
            assert zeros <= repaired_cutoff

    counterexample = (1, 0)
    assert counterexample in terminal_words(2)
    printed_x_lower = 2 * (1 - gamma[1])
    printed_x_upper = 2 * (1 - gamma[0])
    printed_cutoff = floor_interval(printed_x_lower, printed_x_upper)
    assert printed_cutoff == 0
    assert counterexample.count(0) == 1 > printed_cutoff

    return {
        "parity_bijection_max_length": parity_max_length,
        "parity_vectors_checked": parity_vectors_checked,
        "terras_affine_coordinates_checked": affine_coordinates_checked,
        "proposition_1_7_counterexample_n1_k1": True,
        "terminal_cutoff_max_length": terminal_max_length,
        "terminal_words_checked": terminal_words_checked,
        "terminal_counts_k1_through_k19": terminal_counts,
        "printed_terminal_cutoff_counterexample_10_at_k2": True,
    }


def representative_map(d: int, representatives: tuple[int, ...]) -> dict[int, int]:
    assert len(representatives) == d
    mapping = {representative % d: representative for representative in representatives}
    assert len(mapping) == d
    assert mapping[0] == 0
    return mapping


def allouche_g(
    ell: int,
    n: int,
    d: int,
    representatives: tuple[int, ...],
) -> int:
    if ell % d == 0:
        return ell // d
    phi = representative_map(d, representatives)
    numerator = n * ell - phi[(n * ell) % d]
    assert numerator % d == 0
    return numerator // d


def allouche_iterate_and_alpha(
    ell: int,
    length: int,
    n: int,
    d: int,
    representatives: tuple[int, ...],
) -> tuple[int, int]:
    alpha = 0
    for _ in range(length):
        alpha += int(ell % d != 0)
        ell = allouche_g(ell, n, d, representatives)
    return ell, alpha


def repaired_divisible_branch(ell: int, d: int, u: int) -> tuple[int, int]:
    """The explicit total repair of Allouche's printed divisible branch."""

    assert ell % d == 0
    retained_modulus = d ** (u - 1)
    rho = (-ell // d) % retained_modulus
    assert 0 <= rho < retained_modulus
    value = ell // d + rho
    assert value % retained_modulus == 0
    return value, rho


def printed_divisible_branch_on_displayed_class(
    ell: int,
    d: int,
    u: int,
    index: int,
) -> int:
    """Allouche's displayed value, only where its printed class applies."""

    assert 1 <= index <= u
    modulus = d**u
    assert ell % modulus == d**index % modulus
    if index == u:
        return ell // d
    return ell // d + d ** (u - 1) - d ** (index - 1)


def allouche_finite_checks() -> dict[str, int | bool | list[int]]:
    # Each tuple is (n, d, complete representatives, maximum k).
    cases = (
        (3, 2, (0, -1), 11),
        (4, 3, (0, 1, -1), 7),
        (5, 4, (0, 1, -2, -1), 6),
    )
    affine_checks = 0
    counting_checks = 0
    remainder_checks = 0

    for n, d, representatives, maximum_length in cases:
        assert n > d >= 2
        assert math.gcd(n, d) == 1
        representative_map(d, representatives)
        for length in range(1, maximum_length + 1):
            counts = [0] * (length + 1)
            for residue in range(d**length):
                base_image, alpha = allouche_iterate_and_alpha(
                    residue, length, n, d, representatives
                )
                counts[alpha] += 1
                for quotient in range(-2, 3):
                    lifted = d**length * quotient + residue
                    lifted_image, lifted_alpha = allouche_iterate_and_alpha(
                        lifted, length, n, d, representatives
                    )
                    assert lifted_alpha == alpha
                    assert lifted_image == n**alpha * quotient + base_image
                    affine_checks += 1

            expected = [
                math.comb(length, alpha) * (d - 1) ** alpha
                for alpha in range(length + 1)
            ]
            assert counts == expected
            assert sum(counts) == d**length
            counting_checks += length + 1

    # Classical Lemma 2 remainder inequality, on a symmetric finite window.
    n, d, representatives = 3, 2, (0, -1)
    for length in range(1, 13):
        for ell in range(-(2**length), 2**length + 1):
            image, alpha = allouche_iterate_and_alpha(
                ell, length, n, d, representatives
            )
            remainder = Fraction(image) - Fraction(n**alpha, d**length) * ell
            assert abs(remainder) <= Fraction(n**length, d**length)
            remainder_checks += 1

    # The printed classes do not cover all divisible residues.  For d=2,u=3,
    # residue 6 modulo 8 is the smallest explicit gap.
    d, u = 2, 3
    modulus = d**u
    displayed = {d**index % modulus for index in range(1, u + 1)}
    divisible = {residue for residue in range(modulus) if residue % d == 0}
    missing = sorted(divisible - displayed)
    assert displayed == {0, 2, 4}
    assert missing == [6]
    printed_domain = {
        residue for residue in range(modulus) if residue % d != 0
    } | displayed
    assert sorted(set(range(modulus)) - printed_domain) == [6]

    repair_coverage_checks = 0
    displayed_agreement_checks = 0
    for d, n, u in ((2, 3, 3), (3, 4, 2), (4, 5, 2)):
        assert d < n < d**u
        modulus = d**u
        retained_modulus = d ** (u - 1)
        repaired_residues = 0
        for residue in range(0, modulus, d):
            repaired_residues += 1
            for period in range(-3, 4):
                ell = residue + period * modulus
                value, rho = repaired_divisible_branch(ell, d, u)
                assert 0 <= rho < retained_modulus
                assert value % retained_modulus == 0
                assert value - ell // d == rho
                repair_coverage_checks += 1
        assert repaired_residues == d ** (u - 1)

        for index in range(1, u + 1):
            residue = d**index % modulus
            for period in range(-3, 4):
                ell = residue + period * modulus
                repaired, _ = repaired_divisible_branch(ell, d, u)
                printed = printed_divisible_branch_on_displayed_class(
                    ell, d, u, index
                )
                assert repaired == printed
                displayed_agreement_checks += 1

    return {
        "generalized_affine_fibre_checks": affine_checks,
        "generalized_binomial_count_checks": counting_checks,
        "classical_remainder_bound_checks": remainder_checks,
        "printed_theorem_2_missing_residues_d2_u3": missing,
        "repaired_divisible_branch_coverage_checks": repair_coverage_checks,
        "repair_agrees_on_printed_classes_checks": displayed_agreement_checks,
        "printed_theorem_2_function_total_as_written": False,
        "repaired_theorem_2_divisible_branch_total_on_tested_moduli": True,
    }


def korec_u_count(length: int, threshold: Fraction, weak: bool) -> int:
    result = 0
    for residue in range(2**length):
        branch_count = sum(terras_parity_vector(residue, length))
        relation = Fraction(branch_count, length) <= threshold
        if not weak:
            relation = Fraction(branch_count, length) < threshold
        result += int(relation)
    return result


def ceil_fraction(value: Fraction) -> int:
    return -((-value.numerator) // value.denominator)


def korec_finite_checks() -> dict[str, int | bool | str]:
    u_semantics_checks = 0
    for length in range(1, 13):
        for threshold in (Fraction(1, 2), Fraction(2, 3), Fraction(3, 4)):
            weak_count = korec_u_count(length, threshold, weak=True)
            strict_count = korec_u_count(length, threshold, weak=False)
            expected_weak = sum(
                math.comb(length, count)
                for count in range(length + 1)
                if Fraction(count, length) <= threshold
            )
            expected_strict = sum(
                math.comb(length, count)
                for count in range(length + 1)
                if Fraction(count, length) < threshold
            )
            assert weak_count == expected_weak
            assert strict_count == expected_strict
            assert weak_count - strict_count == sum(
                math.comb(length, count)
                for count in range(length + 1)
                if Fraction(count, length) == threshold
            )
            u_semantics_checks += 1

    # At m=2,d=1/2 the weak boundary includes the two words of weight one.
    assert korec_u_count(2, Fraction(1, 2), weak=True) == 3
    assert korec_u_count(2, Fraction(1, 2), weak=False) == 1

    # Write q=c/log_2(3).  The printed denominator log_4(3) makes
    # d_printed=q+1/4, so d_printed<q is impossible.  The repaired choice is
    # d_*=(q+1/2)/2, which lies strictly between 1/2 and q whenever q>1/2.
    d_parameter_checks = 0
    for q in (Fraction(51, 100), Fraction(3, 5), Fraction(4, 5)):
        printed_d = q + Fraction(1, 4)
        repaired_d = (q + Fraction(1, 2)) / 2
        assert printed_d - q == Fraction(1, 4)
        assert not printed_d < q
        assert Fraction(1, 2) < repaired_d < q
        assert q - repaired_d == (q - Fraction(1, 2)) / 2
        d_parameter_checks += 1

    ln2 = log_bounds(Fraction(2))
    ln3 = log_bounds(Fraction(3))
    log2_of_3 = quotient_bounds(ln3, ln2)
    assert log2_of_3[0] > 1

    # A concrete rigorous instance of Korec's asymptotic margin.  c=4/5 is
    # above log_4(3), while m=2^20 has log_2(m)=20 exactly.
    c = Fraction(4, 5)
    assert c > log2_of_3[1] / 2
    m = 2**20
    log2_m = 20
    correction_numerator = 1 + 2 * (1 - c) * log2_m
    assert correction_numerator > 0

    # The exact logarithmic rearrangement of
    #   (m^2 2^m)^(1-c) 3^k <= 2^(m-1)
    # is
    #   k/m <= c/L - A/(mL), L=log_2(3), A=1+2(1-c)log_2(m).
    # The printed equation (4) omits L in the second denominator.
    correct_lower = (c * m - correction_numerator) / (m * log2_of_3[1])
    correct_upper = (c * m - correction_numerator) / (m * log2_of_3[0])
    printed_lower = c / log2_of_3[1] - correction_numerator / m
    printed_upper = c / log2_of_3[0] - correction_numerator / m
    assert printed_upper < correct_lower

    # Exact algebra at both rational endpoints: multiplying the repaired RHS
    # by mL recovers mc-A, whereas the printed RHS gives mc-AL<mc-A because
    # L>1 and A>0.
    for ell in log2_of_3:
        assert m * ell * (c / ell - correction_numerator / (m * ell)) == (
            m * c - correction_numerator
        )
        assert m * ell * (c / ell - correction_numerator / m) == (
            m * c - correction_numerator * ell
        )
        assert m * c - correction_numerator * ell < m * c - correction_numerator

    # There is an integer grid point satisfying the correct condition but not
    # the printed stronger one; the enclosure makes both decisions rigorous.
    separating_k = ceil_fraction(m * printed_upper)
    assert Fraction(separating_k, m) > printed_upper
    assert Fraction(separating_k, m) <= correct_lower
    assert separating_k * log2_of_3[1] <= m * c - correction_numerator

    q_lower = c / log2_of_3[1]
    q_upper = c / log2_of_3[0]
    repaired_d_lower = (q_lower + Fraction(1, 2)) / 2
    repaired_d_upper = (q_upper + Fraction(1, 2)) / 2
    assert Fraction(1, 2) < repaired_d_lower
    assert repaired_d_upper < q_lower
    assert repaired_d_upper < correct_lower

    return {
        "weak_boundary_semantics_cases": u_semantics_checks,
        "m2_dhalf_weak_count": 3,
        "m2_dhalf_strict_count": 1,
        "printed_d_denominator_defect_checks": d_parameter_checks,
        "printed_d_is_q_plus_one_quarter": True,
        "repaired_d_interval": "1/2 < d_* < c/log_2(3)",
        "equation_4_missing_log2_3_denominator": True,
        "printed_equation_4_condition_is_stronger": True,
        "finite_integer_separating_k": separating_k,
        "weak_boundary_implication_has_positive_margin_at_test_scale": True,
    }


def main() -> None:
    for path, (expected_bytes, expected_hash, expected_pages) in PDF_PINS.items():
        check_pin(path, expected_bytes, expected_hash)
        assert pdf_pages(path) == expected_pages, path

    for path, (expected_bytes, expected_hash) in ROUTE_PINS.items():
        check_pin(path, expected_bytes, expected_hash)
    for path, (expected_bytes, expected_hash) in TAO_SOURCE_PINS.items():
        check_pin(path, expected_bytes, expected_hash)

    audit_pin_status = "DEFERRED: set F030_AUDIT_PIN after the audit is finalized"
    if F030_AUDIT_PIN is not None:
        check_pin(F030, *F030_AUDIT_PIN)
        audit_pin_status = "ENFORCED"
    else:
        assert F030.is_file(), F030

    report = {
        "status": "PASS",
        "scope": "finite exact Terras--Allouche--Korec density-lineage kernels",
        "pinned_primary_pdfs": len(PDF_PINS),
        "pinned_frozen_route_artifacts": len(ROUTE_PINS),
        "pinned_tao_source_manifestations": len(TAO_SOURCE_PINS),
        "f030_audit_pin": audit_pin_status,
        **logarithmic_threshold_checks(),
        **terras_finite_checks(),
        **allouche_finite_checks(),
        **korec_finite_checks(),
        "explicitly_not_certified": [
            "a central limit theorem",
            "any passage from finite residue blocks to an infinite natural-density limit",
            "the Terras, Allouche, or Korec density-one theorem in full",
            "Tao's analytic theorem",
            "the Collatz conjecture",
        ],
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
