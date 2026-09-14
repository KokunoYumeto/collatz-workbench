#!/usr/bin/env python3
"""Finite exact checks for signed fixed-content Collatz packet necklaces.

The general formulas are proved in the TeX.  This certificate independently
enumerates a bounded parameter rectangle using integers and Fraction only.  It
does not infer an all-length theorem or make a historical priority claim.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import sys
from fractions import Fraction


if not __debug__:
    raise RuntimeError(
        "affine_signed_necklace_checks.py refuses optimized Python: "
        "fail-closed assertions require __debug__"
    )


MAX_LENGTH = 8
MAX_BUDGET = 16


def compositions(total: int, length: int):
    if total < length or length < 1:
        return
    if length == 1:
        yield (total,)
        return
    for cuts in itertools.combinations(range(1, total), length - 1):
        prior = 0
        parts = []
        for cut in cuts:
            parts.append(cut - prior)
            prior = cut
        parts.append(total - prior)
        yield tuple(parts)


def rotations(word: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(word[j:] + word[:j] for j in range(len(word)))


def canonical_rotation(word: tuple[int, ...]) -> tuple[int, ...]:
    return min(rotations(word))


def minimal_period(word: tuple[int, ...]) -> int:
    for period in range(1, len(word) + 1):
        if len(word) % period == 0 and word == word[:period] * (len(word) // period):
            return period
    raise AssertionError("every nonempty finite word has a period")


def divisors(value: int) -> tuple[int, ...]:
    return tuple(d for d in range(1, value + 1) if value % d == 0)


def moebius(value: int) -> int:
    if value < 1:
        raise ValueError("Moebius is used only on positive divisors")
    remaining = value
    prime_factors = 0
    prime = 2
    while prime * prime <= remaining:
        if remaining % prime == 0:
            remaining //= prime
            prime_factors += 1
            if remaining % prime == 0:
                return 0
        prime += 1
    if remaining > 1:
        prime_factors += 1
    return -1 if prime_factors % 2 else 1


def affine_numerator(word: tuple[int, ...]) -> int:
    length = len(word)
    prefix = 0
    value = 0
    for index, exponent in enumerate(word):
        value += 3 ** (length - 1 - index) * 2**prefix
        prefix += exponent
    return value


def shortened_word(packet: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(bit for exponent in packet for bit in (1,) + (0,) * (exponent - 1))


def binary_words(length: int, weight: int):
    for positions in itertools.combinations(range(length), weight):
        position_set = set(positions)
        yield tuple(int(index in position_set) for index in range(length))


def main() -> int:
    metrics = {
        "parameter_pairs": 0,
        "composition_words": 0,
        "primitive_composition_words": 0,
        "primitive_orbits": 0,
        "positive_primitive_points": 0,
        "negative_primitive_points": 0,
        "packet_binary_necklace_bijections": 0,
        "coprime_parameter_pairs": 0,
        "unrestricted_moreau_sums": 0,
    }

    orbit_counts_by_budget: dict[int, int] = {}
    for length in range(1, MAX_LENGTH + 1):
        for budget in range(length, MAX_BUDGET + 1):
            words = tuple(compositions(budget, length))
            primitive = tuple(word for word in words if minimal_period(word) == length)
            common = math.gcd(length, budget)

            primitive_formula = sum(
                moebius(d) * math.comb(budget // d - 1, length // d - 1)
                for d in divisors(common)
            )
            fixed_weight_numerator = sum(
                moebius(d) * math.comb(budget // d, length // d)
                for d in divisors(common)
            )
            assert len(words) == math.comb(budget - 1, length - 1)
            assert len(primitive) == primitive_formula
            assert primitive_formula % length == 0
            assert fixed_weight_numerator % budget == 0
            orbit_count = primitive_formula // length
            assert orbit_count == fixed_weight_numerator // budget

            packet_classes = {canonical_rotation(word) for word in primitive}
            assert len(packet_classes) == orbit_count
            assert all(len(set(rotations(word))) == length for word in primitive)

            encoded_classes = {
                canonical_rotation(shortened_word(word)) for word in packet_classes
            }
            binary_classes = {
                canonical_rotation(word)
                for word in binary_words(budget, length)
                if minimal_period(word) == budget
            }
            assert encoded_classes == binary_classes

            denominator = 2**budget - 3**length
            assert denominator != 0
            for word in primitive:
                points = tuple(
                    Fraction(affine_numerator(rotated), denominator)
                    for rotated in rotations(word)
                )
                assert len(set(points)) == length
                assert all((point > 0) == (denominator > 0) for point in points)
                assert all((point < 0) == (denominator < 0) for point in points)

            if common == 1:
                assert len(primitive) == len(words)
                assert orbit_count * length == math.comb(budget - 1, length - 1)
                metrics["coprime_parameter_pairs"] += 1

            metrics["parameter_pairs"] += 1
            metrics["composition_words"] += len(words)
            metrics["primitive_composition_words"] += len(primitive)
            metrics["primitive_orbits"] += orbit_count
            metrics["packet_binary_necklace_bijections"] += len(packet_classes)
            sign_key = (
                "positive_primitive_points"
                if denominator > 0
                else "negative_primitive_points"
            )
            metrics[sign_key] += len(primitive)
            orbit_counts_by_budget[budget] = orbit_counts_by_budget.get(budget, 0) + orbit_count

    # The length bound above includes every possible positive weight only for
    # budgets at most MAX_LENGTH.  On that complete triangle, summing the
    # fixed-weight counts recovers Moreau's unrestricted primitive count.  For
    # budget one the excluded all-zero word is the second primitive necklace.
    for budget in range(2, MAX_LENGTH + 1):
        moreau_numerator = sum(
            moebius(d) * 2 ** (budget // d) for d in divisors(budget)
        )
        assert moreau_numerator % budget == 0
        assert orbit_counts_by_budget[budget] == moreau_numerator // budget
        metrics["unrestricted_moreau_sums"] += 1
    assert orbit_counts_by_budget[1] == 1

    checks = {
        "positive_composition_count": "PASS",
        "primitive_root_moebius_inversion": "PASS",
        "free_cyclic_orbit_division": "PASS",
        "fixed_weight_binary_formula": "PASS",
        "packet_to_binary_necklace_bijection": "PASS",
        "packet_denominator_sign_split": "PASS",
        "distinct_points_per_primitive_orbit": "PASS",
        "coprime_specialization": "PASS",
        "unrestricted_moreau_recovery": "PASS",
    }
    payload = {
        "certificate": "signed fixed-content affine-packet necklace checks",
        "status": "PASS",
        "python": sys.version.split()[0],
        "arithmetic": "integer and fractions.Fraction only; no floating point",
        "bounds": {"max_packet_length": MAX_LENGTH, "max_exponent_budget": MAX_BUDGET},
        "checks": checks,
        "metrics": metrics,
        "proof_scope": (
            "bounded exact enumeration only; the all-parameter proof is in "
            "Theorem signed-fixed-content-necklace-count"
        ),
        "Lean_launched": False,
    }
    payload["metrics_sha256"] = hashlib.sha256(
        json.dumps(metrics, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
