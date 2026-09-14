#!/usr/bin/env python3
"""Deterministic finite checks for the Everett 1977 reconstruction.

This certificate checks the fixed source witness, the exact four-case fibre
induction, all finite parity residues through a declared level, the affine
word formula and inverse residue, the positive-representative corollary, the
source contraction count, and the shortened/accelerated first-descent bridge
on a large finite test range.  The arbitrary-length proofs remain in TeX.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT
    / "external_literature"
    / "dependency_gate_2026-08-25"
    / "everett_1977_paperzz_witness.pdf"
)
EXPECTED_SOURCE_BYTES = 165_514
EXPECTED_SOURCE_SHA256 = (
    "668bd5b548136b2f8183eb932af4f39a28965a1b54f676cbe8e949043d4ff160"
)

MAX_PREFIX_LEVEL = 12
AFFINE_QUOTIENT_SAMPLES = 5
MAX_DENSITY_LEVEL = 20
MAX_EXHAUSTIVE_INTERPOLATION_LEVEL = 3
MAX_CROSSWALK_START = 20_001
MAX_CROSSWALK_SHORTENED_STEPS = 512


def t(n: int) -> int:
    assert n >= 0
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def c_cr(n: int) -> int:
    assert n > 0 and n % 2 == 1
    y = 3 * n + 1
    while y % 2 == 0:
        y //= 2
    return y


def parity_prefix(n: int, length: int) -> tuple[int, ...]:
    out: list[int] = []
    for _ in range(length):
        out.append(n & 1)
        n = t(n)
    return tuple(out)


def iterate_t(n: int, length: int) -> int:
    for _ in range(length):
        n = t(n)
    return n


def source_coordinates(word: tuple[int, ...]) -> tuple[int, int, int]:
    """Return Everett's (a,b,X) by the literal four-case induction."""

    assert word and all(bit in (0, 1) for bit in word)
    if word[0] == 0:
        a, b, x = 0, 0, 0
    else:
        a, b, x = 1, 2, 1

    for n, bit in enumerate(word[1:], start=1):
        old_b, old_x = b, x
        if old_b % 2 == 0 and bit == 0:
            b = old_b // 2
        elif old_b % 2 == 0 and bit == 1:
            a += 1 << n
            b = (3 * old_b + 3 ** (old_x + 1) + 1) // 2
            x += 1
        elif old_b % 2 == 1 and bit == 0:
            a += 1 << n
            b = (old_b + 3**old_x) // 2
        else:
            b = (3 * old_b + 1) // 2
            x += 1

        assert 0 <= a < 1 << (n + 1)
        assert 0 <= b < 3**x

    return a, b, x


def affine_constant(word: tuple[int, ...]) -> int:
    total = 0
    for j, bit in enumerate(word):
        if bit:
            later_ones = sum(word[j + 1 :])
            total += (1 << j) * 3**later_ones
    return total


def inverse_residue(word: tuple[int, ...]) -> int:
    modulus = 1 << len(word)
    x = sum(word)
    return (-affine_constant(word) * pow(3**x, -1, modulus)) % modulus


def exact_below_L(x: int, n: int) -> bool:
    """Check x/n < log(2)/log(10/3) without floating point."""

    return 10**x < (1 << n) * 3**x


def exact_above_one_minus_L(x: int, n: int) -> bool:
    """Check x/n > 1-L by applying the exact L test to n-x."""

    return exact_below_L(n - x, n)


def first_t_descent(n: int, step_limit: int) -> tuple[bool, int | None]:
    start = n
    for k in range(1, step_limit + 1):
        n = t(n)
        if n < start:
            return True, k
    return False, None


def first_c_descent(n: int, accelerated_limit: int) -> tuple[bool, int | None]:
    assert n > 0 and n % 2 == 1
    start = n
    for j in range(1, accelerated_limit + 1):
        n = c_cr(n)
        if n < start:
            return True, j
    return False, None


def check_source() -> None:
    data = SOURCE.read_bytes()
    assert len(data) == EXPECTED_SOURCE_BYTES
    assert sha256(data).hexdigest() == EXPECTED_SOURCE_SHA256


def check_finite_fibres() -> tuple[int, int, int]:
    residue_checks = 0
    affine_checks = 0
    positive_representative_checks = 0

    for n in range(1, MAX_PREFIX_LEVEL + 1):
        modulus = 1 << n
        observed: dict[tuple[int, ...], int] = {}
        positive_words: list[tuple[int, ...]] = []

        for residue in range(modulus):
            word = parity_prefix(residue, n)
            assert word not in observed
            observed[word] = residue
            a, b, x = source_coordinates(word)
            assert a == residue
            assert x == sum(word)
            assert inverse_residue(word) == residue
            assert (3**x * residue + affine_constant(word)) % modulus == 0
            assert iterate_t(residue, n) == b
            residue_checks += 1

            for q in range(AFFINE_QUOTIENT_SAMPLES):
                start = a + modulus * q
                assert parity_prefix(start, n) == word
                assert iterate_t(start, n) == b + 3**x * q
                assert (
                    modulus * iterate_t(start, n)
                    == 3**x * start + affine_constant(word)
                )
                affine_checks += 1

        assert len(observed) == modulus

        for representative in range(1, modulus + 1):
            positive_words.append(parity_prefix(representative, n))
            positive_representative_checks += 1
        assert len(set(positive_words)) == modulus

    return residue_checks, affine_checks, positive_representative_checks


def check_density_count() -> tuple[int, int, int]:
    binomial_levels = 0
    word_classes_checked = 0
    dyadic_starts_checked = 0

    rational_gap = (1 << 40) * 3**23 - 10**23
    assert rational_gap == 3_511_519_796_081_828_298_752
    assert rational_gap > 0
    assert t(1) == 2
    assert 3 * t(3) == 5 * 3  # equality in the source's 5/3 odd-step bound

    for n in range(1, MAX_DENSITY_LEVEL + 1):
        modulus = 1 << n
        h_count = 0
        d_count = 0
        for x in range(n + 1):
            multiplicity = comb(n, x)
            below_l = exact_below_L(x, n)
            above_one_minus_l = exact_above_one_minus_L(x, n)
            if below_l:
                d_count += multiplicity
            if below_l and above_one_minus_l:
                h_count += multiplicity
            word_classes_checked += 1

        assert h_count <= d_count <= modulus

        # Exact binomial variance identity: Var(X)=N/4.
        assert sum(
            comb(n, x) * (2 * x - n) ** 2 for x in range(n + 1)
        ) == n * modulus

        # The rational window delta=3/40 lies inside Everett's epsilon window.
        rational_h_count = sum(
            comb(n, x)
            for x in range(n + 1)
            if abs(40 * (2 * x - n)) < 6 * n
        )
        assert rational_h_count <= h_count

        # Exact rational form of Chebyshev's weaker delta=3/40 bound.
        assert 9 * n * rational_h_count >= (9 * n - 400) * modulus

        # Every D_N representative except possibly m=1 descends by time N.
        witnessed = 0
        for start in range(1, modulus + 1):
            word = parity_prefix(start, n)
            x = sum(word)
            if exact_below_L(x, n):
                if start == 1:
                    continue
                value = start
                descended = False
                for _ in range(n):
                    value = t(value)
                    if value < start:
                        descended = True
                        break
                assert descended
                witnessed += 1
            dyadic_starts_checked += 1
        assert witnessed >= d_count - 1
        binomial_levels += 1

    return binomial_levels, word_classes_checked, dyadic_starts_checked


def check_interpolation_shells() -> int:
    """Exhaust the Boolean shell argument behind Everett Eqs. (10)-(12)."""

    checks = 0
    for n in range(1, MAX_EXHAUSTIVE_INTERPOLATION_LEVEL + 1):
        left = 1 << n
        shell_size = left
        for mask in range(1 << shell_size):
            shell = [(mask >> j) & 1 for j in range(shell_size)]
            shell_successes = sum(shell)
            shell_failures = shell_size - shell_successes
            n_n = left + shell_failures
            assert left <= n_n <= 2 * left
            for a_n in range(left + 1):
                a_next = a_n + shell_successes
                assert n_n == a_n + (2 * left - a_next)
                prefix_successes = 0
                for offset, success in enumerate(shell, start=1):
                    prefix_successes += success
                    m = left + offset
                    a_m = a_n + prefix_successes
                    if m <= n_n:
                        assert a_m * n_n >= a_n * m
                    else:
                        k = m - n_n
                        assert prefix_successes >= k
                        assert a_m * (n_n + k) >= (a_n + k) * m
                        assert (a_n + k) * n_n >= a_n * (n_n + k)
                    checks += 1
    return checks


def check_crosswalk() -> tuple[int, int]:
    odd_starts_checked = 0
    matched_descents = 0
    for start in range(1, MAX_CROSSWALK_START + 1, 2):
        raw = 3 * start + 1
        block: list[int] = []
        while raw % 2 == 0:
            raw //= 2
            block.append(raw)
        assert block
        assert block[-1] == c_cr(start)
        assert block[-1] == min(block)
        t_found, _ = first_t_descent(start, MAX_CROSSWALK_SHORTENED_STEPS)
        c_found, _ = first_c_descent(start, MAX_CROSSWALK_SHORTENED_STEPS)
        assert t_found == c_found
        odd_starts_checked += 1
        matched_descents += int(t_found)
    return odd_starts_checked, matched_descents


def main() -> None:
    check_source()
    residues, affine, positive = check_finite_fibres()
    levels, word_classes, starts = check_density_count()
    interpolation_checks = check_interpolation_shells()
    odd_starts, matched = check_crosswalk()
    print("Everett 1977 deterministic checks: PASS")
    print(f"source_sha256={EXPECTED_SOURCE_SHA256}")
    print(f"prefix_levels=1..{MAX_PREFIX_LEVEL}")
    print(f"residue_bijection_checks={residues}")
    print(f"affine_fibre_checks={affine}")
    print(f"positive_representative_checks={positive}")
    print(f"density_levels=1..{MAX_DENSITY_LEVEL}")
    print(f"binomial_word_classes_checked={word_classes}")
    print(f"dyadic_starts_checked={starts}")
    print(f"interpolation_shell_checks={interpolation_checks}")
    print(f"odd_crosswalk_starts_checked={odd_starts}")
    print(f"matched_finite_descents={matched}")


if __name__ == "__main__":
    main()
