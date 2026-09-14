#!/usr/bin/env python3
"""Deterministic finite checks for the Herschfeld 1936 audit.

The arbitrary-parameter proofs and the scope of Herschfeld's theorem remain
in TeX.  This certificate pins the primary source and frozen routing state,
computes the exact orders used in the two-solution argument, checks its
sorting/factorization/congruence kernel on bounded fibres, checks the printed
small-d table, and exercises the exponent-boundary and elementary comparison
lemmas.  Finite exhaustion is not presented as a proof of eventual
uniqueness.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from math import gcd
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

EXPECTED_HASHES = {
    "external_literature/dependency_gate_2026-08-25/"
    "herschfeld_1936_equation_2x_minus_3y_equals_d_ams.pdf":
        "1259b633643db5d7e2468cbd578d72443a4bdc29a8ce0d85a57e0cbcb8ac2d3a",
    "state/index_routes.jsonl":
        "b05028694bf133b9b19f2b0c0a771323b7a47ae872c0712769267aaf1f1eff38",
    "state/document_routes.jsonl":
        "e439a5f9a70253b00824df5be791415e1c068d574c23f6f7f61851c19a88b2a5",
    "state/index_snapshot.json":
        "7d5a17440a3cb039f2bfbb4814567b5805117002136cc65687de738ee99af62f",
}

PRINTED_SMALL_FIBRES = {
    -7: {(1, 2)},
    -5: {(2, 2)},
    -1: {(1, 1), (3, 2)},
    1: {(2, 1)},
    5: {(3, 1), (5, 3)},
    7: {(4, 2)},
}


def digest(path: Path) -> str:
    h = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def prime_factors(value: int) -> tuple[int, ...]:
    """Return the distinct prime divisors of a positive integer."""
    assert value >= 1
    remainder = value
    factors: list[int] = []
    candidate = 2
    while candidate * candidate <= remainder:
        if remainder % candidate == 0:
            factors.append(candidate)
            while remainder % candidate == 0:
                remainder //= candidate
        candidate = 3 if candidate == 2 else candidate + 2
    if remainder > 1:
        factors.append(remainder)
    return tuple(factors)


def euler_phi(value: int) -> int:
    assert value >= 1
    result = value
    for prime in prime_factors(value):
        result = result // prime * (prime - 1)
    return result


def multiplicative_order(base: int, modulus: int) -> int:
    """Compute the exact order by prime-factor descent from Euler's phi."""
    assert modulus > 1 and gcd(base, modulus) == 1
    order = euler_phi(modulus)
    for prime in prime_factors(order):
        while order % prime == 0 and pow(base, order // prime, modulus) == 1:
            order //= prime
    assert pow(base, order, modulus) == 1
    # These tests certify minimality: every proper divisor of ``order`` omits
    # at least one prime factor, and hence divides one of order/prime.
    for prime in prime_factors(order):
        assert pow(base, order // prime, modulus) != 1
    return order


def main() -> None:
    for relative, expected in EXPECTED_HASHES.items():
        actual = digest(ROOT / relative)
        assert actual == expected, (relative, actual, expected)

    order_mod_3_checks = 0
    for exponent in range(1, 17):
        modulus = 3**exponent
        assert multiplicative_order(2, modulus) == 2 * 3 ** (exponent - 1)
        order_mod_3_checks += 1

    order_mod_2_checks = 0
    for exponent in range(3, 29):
        modulus = 2**exponent
        assert multiplicative_order(3, modulus) == 2 ** (exponent - 2)
        order_mod_2_checks += 1

    # Enumerate a bounded nonnegative coordinate square.  Whenever two
    # distinct coordinates have the same difference, strict monotonicity
    # lets us sort them simultaneously as X>x and Y>y.  The factorization and
    # both order congruences are then checked literally.
    exponent_bound = 256
    seen: dict[int, list[tuple[int, int]]] = defaultdict(list)
    repeated_pairs: list[tuple[int, tuple[int, int], tuple[int, int]]] = []
    for x in range(exponent_bound + 1):
        power_2 = 2**x
        for y in range(exponent_bound + 1):
            difference = power_2 - 3**y
            for previous in seen[difference]:
                repeated_pairs.append((difference, previous, (x, y)))
            seen[difference].append((x, y))

    expected_repeated_pairs = {
        (1, (1, 0), (2, 1)),
        (-1, (1, 1), (3, 2)),
        (7, (3, 0), (4, 2)),
        (5, (3, 1), (5, 3)),
        (13, (4, 1), (8, 5)),
    }
    assert set(repeated_pairs) == expected_repeated_pairs

    sorting_factorization_checks = 0
    congruence_checks = 0
    for difference, first, second in repeated_pairs:
        (x, y), (X, Y) = sorted((first, second), key=lambda pair: pair[0])
        assert X > x
        assert Y > y
        assert 2**x - 3**y == difference == 2**X - 3**Y
        assert 2**X - 2**x == 3**Y - 3**y
        assert (
            2**x * (2 ** (X - x) - 1)
            == 3**y * (3 ** (Y - y) - 1)
        )
        sorting_factorization_checks += 1

        if y > 0:
            modulus_3 = 3**y
            assert pow(2, X - x, modulus_3) == 1
            assert (X - x) % multiplicative_order(2, modulus_3) == 0
            congruence_checks += 1
        if x > 0:
            modulus_2 = 2**x
            assert pow(3, Y - y, modulus_2) == 1
            # Herschfeld's displayed order formula is used only for x>2;
            # the exact order computation also covers the two small moduli.
            assert (Y - y) % multiplicative_order(3, modulus_2) == 0
            congruence_checks += 1

    # The six nonempty positive-exponent fibres printed for |d|<=10 are
    # checked over the same explicit coordinate bound, including absence of
    # any other nonempty fibre in that interval within the bounded kernel.
    bounded_small_fibres: dict[int, set[tuple[int, int]]] = {}
    for difference in range(-10, 11):
        fibre = {
            (x, y)
            for x in range(1, exponent_bound + 1)
            for y in range(1, exponent_bound + 1)
            if 2**x - 3**y == difference
        }
        if fibre:
            bounded_small_fibres[difference] = fibre
    assert bounded_small_fibres == PRINTED_SMALL_FIBRES
    printed_fibre_points = sum(map(len, bounded_small_fibres.values()))

    # Exact rational arithmetic checks the negative-exponent obstruction on
    # a symmetric sample box: if either exponent is negative, the difference
    # is not an integer.
    negative_exponent_checks = 0
    for x in range(-32, 33):
        for y in range(-32, 33):
            if x >= 0 and y >= 0:
                continue
            difference = Fraction(2) ** x - Fraction(3) ** y
            assert difference.denominator != 1
            negative_exponent_checks += 1

    # Exercise the exact elementary thresholds and the two exponential
    # comparisons used after the order bounds.  Boundary failures certify
    # that the strict starting indices have not been shifted silently.
    assert 2 ** (5 - 2) <= 2 * 5
    assert 3 ** (2 - 1) <= 2 * 2
    threshold_checks = 0
    for x in range(6, 257):
        assert 2 ** (x - 2) > 2 * x
        threshold_checks += 1
    for y in range(3, 257):
        assert 3 ** (y - 1) > 2 * y
        threshold_checks += 1

    exponential_comparison_checks = 0
    for x in range(3, 21):
        exponent = 2 ** (x - 2)
        assert 3**exponent > 2**exponent
        exponential_comparison_checks += 1
    for y in range(1, 13):
        exponent = 3 ** (y - 1)
        assert 2 ** (2 * exponent) > 3**exponent
        exponential_comparison_checks += 1

    print("PASS herschfeld_1936_checks")
    print(f"source_and_frozen_hashes={len(EXPECTED_HASHES)}")
    print(f"order_mod_3_power_checks={order_mod_3_checks}")
    print(f"order_mod_2_power_checks={order_mod_2_checks}")
    print(f"bounded_exponent_max={exponent_bound}")
    print(f"same_difference_pair_checks={sorting_factorization_checks}")
    print(f"same_difference_congruence_checks={congruence_checks}")
    print(f"printed_small_fibres={len(bounded_small_fibres)}")
    print(f"printed_small_fibre_points={printed_fibre_points}")
    print(f"negative_exponent_obstruction_checks={negative_exponent_checks}")
    print(f"elementary_threshold_checks={threshold_checks}")
    print(f"exponential_comparison_checks={exponential_comparison_checks}")


if __name__ == "__main__":
    main()
