"""Deterministic finite checks for the Lagarias 1985/1990 dependency gate.

This is a calculation certificate, not a proof of an infinite theorem.  It
checks the published finite parity-permutation data through k=6, isolates the
missing (14,46) transposition, evaluates Lagarias's unevaluated rational
Q_infinity example, and exhaustively checks the rational fixed-return formula,
its prescribed branches, and its least-period/proper-power criterion for all
binary words of lengths 1 through 8.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from functools import reduce
from itertools import product


def shortened_t(x: Fraction) -> Fraction:
    """The shortened 3x+1 map on rationals with odd reduced denominator."""

    if x.denominator % 2 != 1:
        raise ValueError("input is not in Q intersect Z_2")
    if x.numerator % 2 == 0:
        return x / 2
    return (3 * x + 1) / 2


def qbar(k: int, n: int) -> int:
    """First k chronological parity bits, least significant bit first."""

    value = Fraction(n)
    result = 0
    for i in range(k):
        bit = value.numerator % 2
        result |= bit << i
        value = shortened_t(value)
    return result


def canonical_cycle(cycle: list[int]) -> tuple[int, ...]:
    """Rotate a directed permutation cycle to its least entry."""

    start = min(range(len(cycle)), key=cycle.__getitem__)
    return tuple(cycle[start:] + cycle[:start])


def nontrivial_cycles(k: int) -> set[tuple[int, ...]]:
    modulus = 1 << k
    image = [qbar(k, n) for n in range(modulus)]
    assert sorted(image) == list(range(modulus))
    seen: set[int] = set()
    cycles: set[tuple[int, ...]] = set()
    for start in range(modulus):
        if start in seen:
            continue
        cycle: list[int] = []
        current = start
        while current not in seen:
            seen.add(current)
            cycle.append(current)
            current = image[current]
        assert current == start
        if len(cycle) > 1:
            cycles.add(canonical_cycle(cycle))
    return cycles


def permutation_order(k: int) -> int:
    lengths = [len(cycle) for cycle in nontrivial_cycles(k)] or [1]
    return reduce(math.lcm, lengths, 1)


PRINTED_K6 = {
    (1, 21),
    (2, 42),
    (3, 35),
    (4, 20),
    (5, 17, 37, 49),
    (7, 23),
    (8, 40),
    (9, 29, 25, 13),
    (10, 34),
    (18, 58, 50, 26),
    (19, 51),
    (27, 59),
    (33, 53),
    (36, 52),
    (39, 55),
    (41, 61, 57, 45),
}


def eventually_periodic_q_infinity(x: Fraction) -> tuple[Fraction, int, int]:
    """Evaluate the rational represented by the eventually periodic bits."""

    seen: dict[Fraction, int] = {}
    bits: list[int] = []
    current = x
    while current not in seen:
        seen[current] = len(bits)
        bits.append(current.numerator % 2)
        current = shortened_t(current)
    preperiod = seen[current]
    period = len(bits) - preperiod
    prefix = sum(Fraction(bit * (1 << i)) for i, bit in enumerate(bits[:preperiod]))
    block = sum(
        Fraction(bit * (1 << (preperiod + offset)))
        for offset, bit in enumerate(bits[preperiod:])
    )
    value = prefix + block / (1 - (1 << period))
    return value, preperiod, period


def fixed_return_fraction(word: tuple[int, ...]) -> tuple[Fraction, int, int]:
    n = len(word)
    m = sum(word)
    numerator = sum(
        word[j] * (1 << j) * (3 ** sum(word[j + 1 :]))
        for j in range(n)
    )
    denominator = (1 << n) - (3**m)
    return Fraction(numerator, denominator), numerator, denominator


def t_k(k: int, n: int) -> int:
    if n % 2 == 0:
        return n // 2
    return (3 * n + k) // 2


def is_proper_repeated_block(word: tuple[int, ...]) -> bool:
    """Whether a nonempty word is a repetition of a strictly shorter block."""

    length = len(word)
    return any(
        length % block_length == 0
        and word == word[:block_length] * (length // block_length)
        for block_length in range(1, length)
    )


def check_fixed_returns(max_length: int = 8) -> int:
    checked = 0
    for length in range(1, max_length + 1):
        for word in product((0, 1), repeat=length):
            x, raw_numerator, raw_denominator = fixed_return_fraction(word)
            current = x
            orbit: list[Fraction] = []
            observed: list[int] = []
            for _ in range(length):
                orbit.append(current)
                observed.append(current.numerator % 2)
                current = shortened_t(current)
            assert tuple(observed) == word
            assert current == x

            least_return = next(
                (step for step in range(1, length) if orbit[step] == x),
                length,
            )
            assert (least_return == length) == (not is_proper_repeated_block(word))

            reduced_denominator = x.denominator
            assert reduced_denominator % 2 == 1
            assert math.gcd(reduced_denominator, 3) == 1
            assert raw_denominator % reduced_denominator == 0
            if sum(word) == 0:
                assert x == 0 and reduced_denominator == 1
            else:
                assert math.gcd(raw_denominator, 3) == 1

            scaled = [int(reduced_denominator * state) for state in orbit]
            assert all(Fraction(integer, reduced_denominator) == state for integer, state in zip(scaled, orbit))
            assert math.gcd(reduced_denominator, *scaled) == 1
            for j, integer in enumerate(scaled):
                assert t_k(reduced_denominator, integer) == scaled[(j + 1) % length]

            # Keep the raw affine numerator visible: no raw/reduced pair is
            # silently identified by the certificate.
            assert Fraction(raw_numerator, raw_denominator) == x
            checked += 1
    return checked


def main() -> None:
    expected_orders = {1: 1, 2: 1, 3: 2, 4: 2, 5: 4, 6: 4}
    computed_orders = {k: permutation_order(k) for k in expected_orders}
    assert computed_orders == expected_orders

    computed_k6 = nontrivial_cycles(6)
    printed_k6 = {canonical_cycle(list(cycle)) for cycle in PRINTED_K6}
    missing_from_print = computed_k6 - printed_k6
    extra_in_print = printed_k6 - computed_k6
    assert missing_from_print == {(14, 46)}
    assert not extra_in_print
    assert qbar(6, 14) == 46 and qbar(6, 46) == 14

    exact_examples = {
        Fraction(1): Fraction(-1, 3),
        Fraction(2): Fraction(-2, 3),
        Fraction(3): Fraction(-23, 3),
        Fraction(10): Fraction(-26, 3),
        Fraction(-26, 3): Fraction(-54),
        Fraction(-54): Fraction(-82, 7),
        Fraction(-82, 7): Fraction(18098, 5),
    }
    evaluated_examples: dict[str, str] = {}
    last_preperiod = last_period = 0
    for state, expected in exact_examples.items():
        value, preperiod, period = eventually_periodic_q_infinity(state)
        assert value == expected
        evaluated_examples[str(state)] = str(value)
        if state == Fraction(-82, 7):
            last_preperiod, last_period = preperiod, period
    assert last_preperiod == 13 and last_period == 4

    fixed_return_word_count = check_fixed_returns()
    assert fixed_return_word_count == sum(1 << length for length in range(1, 9))

    print(
        json.dumps(
            {
                "status": "pass",
                "finite_permutation_orders": computed_orders,
                "lagarias_1985_table2_k6_missing_nontrivial_cycles": [
                    list(cycle) for cycle in sorted(missing_from_print)
                ],
                "lagarias_1985_table2_k6_extra_nontrivial_cycles": [],
                "q_infinity_examples": evaluated_examples,
                "minus_82_over_7_preperiod": last_preperiod,
                "minus_82_over_7_period": last_period,
                "fixed_return_words_checked": fixed_return_word_count,
                "fixed_return_max_word_length": 8,
                "least_period_proper_power_equivalences_checked": fixed_return_word_count,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
