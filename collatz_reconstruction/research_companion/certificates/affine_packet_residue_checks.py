#!/usr/bin/env python3
"""Exact certificates for odd-step affine packets and modular exclusions.

The certificate uses exact integer and rational arithmetic.  It checks the
morphisms from positive exponent compositions to shortened and full parity
words, all intermediate cycle values and their three clocks, cyclic groupoid
arrows and stabilizers, residue multiplicities and formal-series coefficients,
the cyclic transport identity, the exact packet strip, the length-five and length-eight residue
calculations, and two independent streaming enumerations of every candidate
packet through odd-step period sixteen.  It makes no claim about periods not
listed in ``PACKET_EXPECTATIONS`` and no claim that these finite exclusions are
new in the literature.
"""

from __future__ import annotations

import hashlib
import csv
import itertools
import json
import math
import sys
from functools import lru_cache
from fractions import Fraction
from pathlib import Path


if not __debug__:
    raise RuntimeError(
        "affine_packet_residue_checks.py refuses optimized Python: "
        "fail-closed assertions require __debug__"
    )


PACKET_EXPECTATIONS = {
    (5, 8): {
        "word_count": 35,
        "denominator": 13,
        "minimum_C": 211,
        "maximum_C": 1121,
        "stream_sha256": "dfbff92e10eaea255370be2bbc5aab306b53a0909493eec1750da28f2845d56d",
    },
    (8, 13): {
        "word_count": 792,
        "denominator": 1631,
        "minimum_C": 6305,
        "maximum_C": 133963,
        "stream_sha256": "0b67f08b3c7d3804c740af3b958cb6a4e2e4b5976ec4d4b5e97df8d6b5dbec69",
    },
    (10, 16): {
        "word_count": 5005,
        "denominator": 6487,
        "minimum_C": 58025,
        "maximum_C": 2473571,
        "stream_sha256": "53555b5b8f67c8350e6e7bf61a062562b0a333b45984e2118377323139543378",
    },
    (11, 18): {
        "word_count": 19448,
        "denominator": 84997,
        "minimum_C": 175099,
        "maximum_C": 14913449,
        "stream_sha256": "d705445b90e445277590a6356440022cbd36f668fdcdd11bb236166fe41f2019",
    },
    (13, 21): {
        "word_count": 125970,
        "denominator": 502829,
        "minimum_C": 1586131,
        "maximum_C": 270532081,
        "stream_sha256": "4da62c00e26e5bf9916e721816bd5579758b7663872aa6cad3a98481f44b37be",
    },
    (14, 23): {
        "word_count": 497420,
        "denominator": 3605639,
        "minimum_C": 4766585,
        "maximum_C": 1625792467,
        "stream_sha256": "d8263e05c1e7478b5dca0df4167d3fb8e07d95c576f84fcd2687809d1bf4a543",
    },
    (15, 24): {
        "word_count": 817190,
        "denominator": 2428309,
        "minimum_C": 14316139,
        "maximum_C": 4885766009,
        "stream_sha256": "04dfc6af0b5928f64e4a274c505b6a9402833eba4c9214a5a05f8e1fd670079e",
    },
    (16, 26): {
        "word_count": 3268760,
        "denominator": 24062143,
        "minimum_C": 42981185,
        "maximum_C": 29333801579,
        "stream_sha256": "a228fd686384564476a29ba9bf868ff9e57f29f2b40cfc917d268e6813ffc633",
    },
}

EXPECTED_STRIP = {
    2: (),
    3: (),
    4: (),
    5: (8,),
    6: (),
    7: (),
    8: (13,),
    9: (),
    10: (16,),
    11: (18,),
    12: (),
    13: (21,),
    14: (23,),
    15: (24,),
    16: (26,),
    17: (27, 28),
}

EXPECTED_LENGTH_FIVE = {
    (1, 1, 1, 1, 4): (211, (3, 11, 10, 2, 3)),
    (1, 1, 1, 2, 3): (227, (6, 9, 7, 4, 3)),
    (1, 1, 1, 3, 2): (259, (12, 5, 1, 8, 3)),
    (1, 1, 2, 1, 3): (251, (4, 6, 9, 10, 2)),
    (1, 1, 2, 2, 2): (283, (10, 2, 3, 12, 9)),
    (1, 1, 3, 1, 2): (331, (6, 9, 7, 1, 8)),
    (1, 2, 1, 2, 2): (319, (7, 4, 3, 11, 5)),
}

ROOT = Path(__file__).resolve().parents[1]
PERIOD_EIGHT_TABLE = ROOT / "data/period_8_A_13_classes.csv"
PERIOD_EIGHT_TABLE_BYTES = 3_358
PERIOD_EIGHT_TABLE_SHA256 = (
    "13bd2d5451530fc7ab674720b5f142b489d0a1111161730a6d013f8fab69025b"
)


def file_sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def compositions(total: int, length: int):
    """Yield every positive composition in separator lexicographic order."""
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


def affine_C(word: tuple[int, ...]) -> int:
    """Return C(p)=sum 3^(m-1-k)2^(a_1+...+a_k), A_0=0."""
    if any(a < 1 for a in word):
        raise ValueError("exponents must be positive")
    # This auxiliary empty-tail value does not define a rational cycle point.
    if not word:
        return 0
    m = len(word)
    prefix = 0
    value = 0
    for k in range(m):
        value += (3 ** (m - 1 - k)) * (2**prefix)
        prefix += word[k]
    return value


def affine_C_recurrence(word: tuple[int, ...]) -> int:
    """Compute the same numerator by B_(j+1)=3B_j+2^S_j."""
    prefix = 0
    value = 0
    for exponent in word:
        value = 3 * value + 2**prefix
        prefix += exponent
    return value


def rotations(word: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(word[j:] + word[:j] for j in range(len(word)))


def canonical_rotation(word: tuple[int, ...]) -> tuple[int, ...]:
    return min(rotations(word))


def minimal_period(word: tuple[int, ...]) -> int:
    for period in range(1, len(word) + 1):
        if len(word) % period == 0 and word == word[:period] * (len(word) // period):
            return period
    raise AssertionError("every finite word has its full length as a period")


def shortened_parity_word(packet: tuple[int, ...]) -> tuple[int, ...]:
    """Encode a_i by the shortened-T block 1 followed by a_i-1 zeros."""
    if not packet or any(a < 1 for a in packet):
        raise ValueError("a cycle packet must be nonempty and positive")
    result: list[int] = []
    for exponent in packet:
        result.append(1)
        result.extend((0,) * (exponent - 1))
    return tuple(result)


def full_parity_word(packet: tuple[int, ...]) -> tuple[int, ...]:
    """Encode a_i by the full-C block 1 followed by a_i zeros."""
    if not packet or any(a < 1 for a in packet):
        raise ValueError("a cycle packet must be nonempty and positive")
    return tuple(bit for a in packet for bit in (1,) + (0,) * a)


def decode_parity_word(bits: tuple[int, ...], full: bool = False) -> tuple[int, ...]:
    """Read cyclic one-to-one gaps; remove one even step for the full clock."""
    if not bits or bits[0] != 1 or any(bit not in (0, 1) for bit in bits):
        raise ValueError("a pointed parity word must begin in one")
    ones = [j for j, bit in enumerate(bits) if bit]
    boundaries = ones + [len(bits)]
    packet = tuple(boundaries[j + 1] - boundaries[j] - int(full) for j in range(len(ones)))
    if any(a < 1 for a in packet):
        raise ValueError("full-map words cannot have cyclically adjacent ones")
    return packet


def rotate(word: tuple, amount: int) -> tuple:
    amount %= len(word)
    return word[amount:] + word[:amount]


def lagarias_numerator(bits: tuple[int, ...]) -> int:
    """Numerator in Lagarias's rational-cycle formula (2.1)."""
    remaining_ones = sum(bits)
    value = 0
    for position, bit in enumerate(bits):
        if bit:
            remaining_ones -= 1
            value += (2**position) * (3**remaining_ones)
    return value


def full_clock_numerator(bits: tuple[int, ...]) -> int:
    """Use the number of preceding divisions, not the full position index."""
    remaining_ones = sum(bits)
    divisions = 0
    value = 0
    for bit in bits:
        if bit:
            remaining_ones -= 1
            value += (2**divisions) * (3**remaining_ones)
        else:
            divisions += 1
    return value


def rational_parity(value: Fraction) -> int:
    if value.denominator % 2 == 0:
        raise AssertionError("the rational-cycle domain requires odd denominator")
    return value.numerator % 2


def shortened_T(value: Fraction) -> Fraction:
    """T on rationals with odd denominator: (3x+1)/2 odd, x/2 even."""
    if rational_parity(value):
        return (3 * value + 1) / 2
    return value / 2


def full_C(value: Fraction) -> Fraction:
    """Full map C on the same domain: 3x+1 odd, x/2 even."""
    if rational_parity(value):
        return 3 * value + 1
    return value / 2


def valuation_two(value: Fraction) -> int:
    if value == 0:
        raise ValueError("the finite valuation is undefined at zero")
    numerator = abs(value.numerator)
    denominator = value.denominator
    return (numerator & -numerator).bit_length() - (denominator & -denominator).bit_length()


def exact_strip() -> dict[int, tuple[int, ...]]:
    result: dict[int, tuple[int, ...]] = {}
    for m in range(2, 18):
        candidates = tuple(
            A
            for A in range(m, 2 * m)
            if 3**m < 2**A and (7**m) * (2**A) < 22**m
        )
        result[m] = candidates
    assert result == EXPECTED_STRIP
    return result


def check_packet_parity_morphism() -> dict[str, int]:
    counts = {
        "packet_words": 0,
        "shortened_rational_steps": 0,
        "full_rational_steps": 0,
        "exact_odd_returns": 0,
        "primitive_packets": 0,
        "imprimitive_packets": 0,
        "positive_rational_cycle_packets": 0,
        "negative_rational_cycle_packets": 0,
        "three_clock_minimal_period_checks": 0,
    }
    assert affine_C(()) == affine_C_recurrence(()) == 0
    for m in range(1, 9):
        for total in range(m, min(14, 2 * m + 4) + 1):
            for packet in compositions(total, m):
                bits = shortened_parity_word(packet)
                full_bits = full_parity_word(packet)
                denominator = 2**total - 3**m
                assert denominator != 0 and math.gcd(denominator, 6) == 1
                assert len(bits) == total
                assert sum(bits) == m
                assert len(full_bits) == total + m and sum(full_bits) == m
                assert all(not (full_bits[j] and full_bits[(j + 1) % len(full_bits)]) for j in range(len(full_bits)))
                assert decode_parity_word(bits) == decode_parity_word(full_bits, full=True) == packet
                assert lagarias_numerator(bits) == affine_C(packet)
                assert full_clock_numerator(full_bits) == affine_C(packet)
                assert affine_C_recurrence(packet) == affine_C(packet)
                primitive_length = minimal_period(packet)
                primitive_sum = sum(packet[:primitive_length])
                repetitions = m // primitive_length
                assert total == repetitions * primitive_sum
                primitive = packet[:primitive_length]
                assert affine_C(packet) == affine_C(primitive) * sum(
                    2 ** (primitive_sum * k) * 3 ** (primitive_length * (repetitions - 1 - k))
                    for k in range(repetitions)
                )
                assert Fraction(affine_C(packet), denominator) == Fraction(
                    affine_C(primitive), 2**primitive_sum - 3**primitive_length
                )
                assert minimal_period(bits) == primitive_sum
                assert minimal_period(full_bits) == primitive_sum + primitive_length
                shifted = packet[1:] + packet[:1]
                assert shortened_parity_word(shifted) == rotate(bits, packet[0])
                assert full_parity_word(shifted) == rotate(full_bits, packet[0] + 1)
                assert 3 * affine_C(packet) + denominator == 2 ** packet[0] * affine_C(shifted)
                odd_values = [Fraction(affine_C(rotate(packet, j)), denominator) for j in range(m)]
                odd_values.append(odd_values[0])
                shortened_values = [odd_values[0]]
                full_values = [odd_values[0]]
                prefixes = [0]
                for j, exponent in enumerate(packet):
                    left, right = odd_values[j : j + 2]
                    assert rational_parity(left) == rational_parity(right) == 1
                    assert left != Fraction(-1, 3)
                    assert 3 * left + 1 == 2**exponent * right
                    assert valuation_two(3 * left + 1) == exponent
                    assert shortened_values[prefixes[j]] == left
                    assert full_values[prefixes[j] + j] == left
                    for step in range(1, exponent + 1):
                        value = shortened_T(shortened_values[-1])
                        assert value == 2 ** (exponent - step) * right
                        shortened_values.append(value)
                    for step in range(1, exponent + 2):
                        value = full_C(full_values[-1])
                        assert value == 2 ** (exponent + 1 - step) * right
                        full_values.append(value)
                    prefixes.append(prefixes[-1] + exponent)
                assert len(shortened_values) == total + 1
                assert len(full_values) == total + m + 1
                assert tuple(map(rational_parity, shortened_values[:-1])) == bits
                assert tuple(map(rational_parity, full_values[:-1])) == full_bits
                assert [j for j, value in enumerate(shortened_values[:-1]) if rational_parity(value)] == prefixes[:-1]
                assert [j for j, value in enumerate(full_values[:-1]) if rational_parity(value)] == [prefixes[j] + j for j in range(m)]
                assert shortened_values[-1] == full_values[-1] == odd_values[0]
                assert next(j for j in range(1, m + 1) if odd_values[j] == odd_values[0]) == primitive_length
                assert next(j for j in range(1, total + 1) if shortened_values[j] == odd_values[0]) == primitive_sum
                assert next(j for j in range(1, total + m + 1) if full_values[j] == odd_values[0]) == primitive_sum + primitive_length
                assert [j for j in range(1, m + 1) if odd_values[j] == odd_values[0]] == list(range(primitive_length, m + 1, primitive_length))
                assert [j for j in range(1, total + 1) if shortened_values[j] == odd_values[0]] == list(range(primitive_sum, total + 1, primitive_sum))
                assert [j for j in range(1, total + m + 1) if full_values[j] == odd_values[0]] == list(range(primitive_sum + primitive_length, total + m + 1, primitive_sum + primitive_length))
                assert len(set(odd_values[:-1])) == primitive_length
                assert len(set(shortened_values[:-1])) == primitive_sum
                assert len(set(full_values[:-1])) == primitive_sum + primitive_length
                counts["packet_words"] += 1
                counts["shortened_rational_steps"] += total
                counts["full_rational_steps"] += total + m
                counts["exact_odd_returns"] += m
                counts["primitive_packets" if primitive_length == m else "imprimitive_packets"] += 1
                counts["positive_rational_cycle_packets" if denominator > 0 else "negative_rational_cycle_packets"] += 1
                counts["three_clock_minimal_period_checks"] += 3
    assert counts["packet_words"] == 12_089
    assert counts["shortened_rational_steps"] == 155_047
    return counts


def check_rotation_groupoids() -> dict[str, int]:
    counts = {"packets": 0, "packet_arrows": 0, "arrow_inverse_checks_both_clocks": 0,
              "composition_checks_both_clocks": 0, "stabilizer_checks_both_clocks": 0,
              "identity_checks_both_clocks": 0}
    for m in range(1, 6):
        for total in range(m, m + 6):
            for packet in compositions(total, m):
                d = minimal_period(packet)
                B = sum(packet[:d])
                repeats = m // d
                stabilizer = {j for j in range(m) if rotate(packet, j) == packet}
                assert stabilizer == {k * d for k in range(repeats)}
                for full in (False, True):
                    encode = full_parity_word if full else shortened_parity_word
                    bits = encode(packet)
                    size = len(bits)
                    offsets = [sum(packet[:j]) + int(full) * j for j in range(m)]
                    assert offsets == [j for j, bit in enumerate(bits) if bit]
                    assert len(set(offsets)) == m
                    assert offsets[0] == 0 and rotate(bits, offsets[0]) == bits
                    assert decode_parity_word(bits, full) == packet
                    counts["identity_checks_both_clocks"] += 1
                    binary_stabilizer = {t for t in range(size) if rotate(bits, t) == bits}
                    assert binary_stabilizer == {offsets[j] for j in stabilizer}
                    assert binary_stabilizer == {k * (B + int(full) * d) for k in range(repeats)}
                    counts["stabilizer_checks_both_clocks"] += 1
                    for j in range(m):
                        target = rotate(packet, j)
                        target_bits = encode(target)
                        assert target_bits == rotate(bits, offsets[j])
                        assert decode_parity_word(target_bits, full) == target
                        assert offsets.index(offsets[j]) == j
                        target_offsets = [sum(target[:k]) + int(full) * k for k in range(m)]
                        inverse = (-j) % m
                        assert rotate(target, inverse) == packet
                        assert (offsets[j] + target_offsets[inverse]) % size == 0
                        assert rotate(target_bits, target_offsets[inverse]) == bits
                        counts["arrow_inverse_checks_both_clocks"] += 1
                        for k in range(m):
                            composed = (j + k) % m
                            assert rotate(target, k) == rotate(packet, composed)
                            assert (offsets[j] + target_offsets[k]) % size == offsets[composed]
                            assert rotate(target_bits, target_offsets[k]) == encode(rotate(packet, composed))
                            counts["composition_checks_both_clocks"] += 1
                counts["packets"] += 1
                counts["packet_arrows"] += m
    assert counts["packets"] == 461 and counts["packet_arrows"] == 1_980
    return counts


@lru_cache(maxsize=4096)
def residue_set(m: int, total: int, modulus: int) -> frozenset[int]:
    if m < 1 or modulus < 1:
        raise ValueError("positive packet length and modulus required")
    if total < m:
        return frozenset()
    if m == 1:
        return frozenset((1 % modulus,)) if total >= 1 else frozenset()
    values: set[int] = set()
    for first in range(1, total - m + 2):
        offset = pow(3, m - 1, modulus)
        multiplier = pow(2, first, modulus)
        values.update(
            (offset + multiplier * residue) % modulus
            for residue in residue_set(m - 1, total - first, modulus)
        )
    return frozenset(values)


@lru_cache(maxsize=4096)
def residue_counts(m: int, total: int, modulus: int) -> tuple[int, ...]:
    """Multiplicity vector from unique first-part decomposition, as columns."""
    if m < 1 or modulus < 1:
        raise ValueError("positive packet length and modulus required")
    values = [0] * modulus
    if total < m:
        return tuple(values)
    if m == 1:
        values[1 % modulus] = 1
        return tuple(values)
    offset = pow(3, m - 1, modulus)
    for first in range(1, total - m + 2):
        multiplier = pow(2, first, modulus)
        for residue, count in enumerate(residue_counts(m - 1, total - first, modulus)):
            values[(offset + multiplier * residue) % modulus] += count
    return tuple(values)


def order_two(modulus: int) -> int:
    """Multiplicative order, with ord_1(2)=1 for the singleton residue ring."""
    if modulus < 1 or modulus % 2 == 0:
        raise ValueError("a positive odd modulus is required")
    if modulus == 1:
        return 1
    for period in range(1, modulus + 1):
        if pow(2, period, modulus) == 1:
            return period
    raise AssertionError("2 is a unit in the finite odd residue ring")


def apply_residue_matrix(m: int, exponent: int, vector: tuple[int, ...]) -> tuple[int, ...]:
    """M_(m,a) e_r = e_(3^(m-1)+2^a*r); valid column orientation."""
    modulus = len(vector)
    assert m >= 2 and exponent >= 1 and modulus >= 1 and modulus % 2 == 1
    result = [0] * modulus
    for residue, count in enumerate(vector):
        target = (pow(3, m - 1, modulus) + pow(2, exponent, modulus) * residue) % modulus
        result[target] += count
    return tuple(result)


def check_residue_multiplicities_and_series() -> dict[str, int]:
    counts = {"multiplicity_vectors": 0, "empty_A_less_than_m_vectors": 0,
              "matrix_basis_images_and_inverses": 0, "matrix_periodicity_checks": 0,
              "rational_series_coefficient_vectors": 0, "q_one_composition_coefficients": 0}
    max_m, max_total = 6, 12
    moduli = (1, 2, 3, 4, 5, 7, 9, 11, 13)
    for modulus in moduli:
        for m in range(1, max_m + 1):
            for total in range(max_total + 1):
                direct = [0] * modulus
                for packet in compositions(total, m):
                    direct[affine_C(packet) % modulus] += 1
                expected_count = math.comb(total - 1, m - 1) if total >= m else 0
                assert sum(direct) == expected_count
                assert tuple(direct) == residue_counts(m, total, modulus)
                assert {r for r, count in enumerate(direct) if count} == set(residue_set(m, total, modulus))
                counts["multiplicity_vectors"] += 1
                counts["empty_A_less_than_m_vectors"] += int(total < m)
        if modulus % 2 == 0:
            continue
        period = order_two(modulus)
        assert pow(2, period, modulus) == 1 % modulus
        if modulus == 1:
            assert period == 1
        zero = (0,) * modulus
        base = tuple(int(r == 1 % modulus) for r in range(modulus))
        # V_1(z)=z/(1-z)e_1, truncated only after coefficient max_total.
        previous = [zero] + [base] * max_total
        for total, vector in enumerate(previous):
            assert vector == residue_counts(1, total, modulus)
            counts["rational_series_coefficient_vectors"] += 1
            counts["q_one_composition_coefficients"] += int(modulus == 1)
        for m in range(2, max_m + 1):
            for exponent in range(1, period + 1):
                targets = set()
                for residue in range(modulus):
                    basis = tuple(int(r == residue) for r in range(modulus))
                    image = apply_residue_matrix(m, exponent, basis)
                    target = (pow(3, m - 1, modulus) + pow(2, exponent, modulus) * residue) % modulus
                    assert image == tuple(int(r == target) for r in range(modulus))
                    targets.add(target)
                    inverse = 0 if modulus == 1 else (pow(2, -exponent, modulus) * (target - pow(3, m - 1, modulus))) % modulus
                    assert inverse == residue
                    assert image == apply_residue_matrix(m, exponent + period, basis)
                    counts["matrix_basis_images_and_inverses"] += 1
                    counts["matrix_periodicity_checks"] += 1
                assert targets == set(range(modulus))
            # Multiply by P_m(z)/(1-z^period), in the stated noncommuting order.
            current = []
            for total in range(max_total + 1):
                coefficient = [0] * modulus
                for exponent in range(1, min(period, total) + 1):
                    image = apply_residue_matrix(m, exponent, previous[total - exponent])
                    for residue, value in enumerate(image):
                        coefficient[residue] += value
                if total >= period:
                    coefficient = [a + b for a, b in zip(coefficient, current[total - period], strict=True)]
                current.append(tuple(coefficient))
                assert current[-1] == residue_counts(m, total, modulus)
                counts["rational_series_coefficient_vectors"] += 1
                if modulus == 1:
                    assert current[-1] == (math.comb(total - 1, m - 1) if total >= m else 0,)
                    counts["q_one_composition_coefficients"] += 1
            previous = current
    residue_counts.cache_clear()
    return counts


def length_five_classes() -> list[dict[str, object]]:
    classes: dict[tuple[int, ...], set[tuple[int, ...]]] = {}
    for packet in compositions(8, 5):
        classes.setdefault(canonical_rotation(packet), set()).add(packet)
    assert len(classes) == 7
    assert all(len(members) == 5 for members in classes.values())

    rows = []
    for representative in sorted(classes):
        value = affine_C(representative)
        residues = tuple(affine_C(rotated) % 13 for rotated in rotations(representative))
        assert (value, residues) == EXPECTED_LENGTH_FIVE[representative]
        assert all(residue != 0 for residue in residues)
        rows.append(
            {
                "representative": list(representative),
                "C": value,
                "rotation_residues_mod_13": list(residues),
            }
        )
    return rows


def period_eight_classes() -> dict[str, object]:
    classes: dict[tuple[int, ...], int] = {}
    direct_residues: set[int] = set()
    for packet in compositions(13, 8):
        classes[canonical_rotation(packet)] = classes.get(canonical_rotation(packet), 0) + 1
        direct_residues.add(affine_C(packet) % 233)
    assert len(classes) == 99
    assert set(classes.values()) == {8}
    assert direct_residues == set(residue_set(8, 13, 233))
    missing = sorted(set(range(233)) - direct_residues)
    assert missing == [0, 138]

    representatives = sorted(classes)
    divisible_7 = sum(affine_C(rep) % 7 == 0 for rep in representatives)
    divisible_233 = sum(affine_C(rep) % 233 == 0 for rep in representatives)
    divisible_1631 = sum(affine_C(rep) % 1631 == 0 for rep in representatives)
    assert (divisible_7, divisible_233, divisible_1631) == (15, 0, 0)
    assert PERIOD_EIGHT_TABLE.is_file()
    assert PERIOD_EIGHT_TABLE.stat().st_size == PERIOD_EIGHT_TABLE_BYTES
    assert file_sha256(PERIOD_EIGHT_TABLE) == PERIOD_EIGHT_TABLE_SHA256
    with PERIOD_EIGHT_TABLE.open(encoding="utf-8", newline="") as stream:
        table_rows = list(csv.DictReader(stream))
    assert len(table_rows) == 99
    for representative, row in zip(representatives, table_rows, strict=True):
        value = affine_C(representative)
        assert row == {
            "representative": " ".join(map(str, representative)),
            "C": str(value),
            "C_mod_7": str(value % 7),
            "C_mod_233": str(value % 233),
            "C_mod_1631": str(value % 1631),
            "class_size": "8",
        }
    return {
        "word_count": 792,
        "class_count": 99,
        "class_size": 8,
        "residue_set_size_mod_233": len(direct_residues),
        "missing_residues_mod_233": missing,
        "representatives_divisible_by_7": divisible_7,
        "representatives_divisible_by_233": divisible_233,
        "representatives_divisible_by_1631": divisible_1631,
        "class_table_bytes": PERIOD_EIGHT_TABLE_BYTES,
        "class_table_sha256": PERIOD_EIGHT_TABLE_SHA256,
    }


def scan_separator(m: int, total: int) -> dict[str, object]:
    denominator = 2**total - 3**m
    count = 0
    integral = 0
    minimum = None
    maximum = None
    stream = hashlib.sha256()
    for packet in compositions(total, m):
        value = affine_C(packet)
        count += 1
        integral += int(value % denominator == 0)
        minimum = value if minimum is None else min(minimum, value)
        maximum = value if maximum is None else max(maximum, value)
        stream.update(bytes(packet))
        stream.update(value.to_bytes(16, "big"))
    return {
        "m": m,
        "A": total,
        "word_count": count,
        "denominator": denominator,
        "integral_word_count": integral,
        "minimum_C": minimum,
        "maximum_C": maximum,
        "stream_sha256": stream.hexdigest(),
    }


def scan_depth_first(m: int, total: int) -> dict[str, object]:
    denominator = 2**total - 3**m
    count = 0
    integral = 0
    minimum = None
    maximum = None
    stream = hashlib.sha256()
    packet = bytearray(m)

    def visit(position: int, remaining: int, prefix: int, numerator: int) -> None:
        nonlocal count, integral, minimum, maximum
        positions_left = m - position
        next_numerator = 3 * numerator + 2**prefix
        if positions_left == 1:
            packet[position] = remaining
            value = next_numerator
            count += 1
            integral += int(value % denominator == 0)
            minimum = value if minimum is None else min(minimum, value)
            maximum = value if maximum is None else max(maximum, value)
            stream.update(packet)
            stream.update(value.to_bytes(16, "big"))
            return
        for exponent in range(1, remaining - positions_left + 2):
            packet[position] = exponent
            visit(
                position + 1,
                remaining - exponent,
                prefix + exponent,
                next_numerator,
            )

    visit(0, total, 0, 0)
    return {
        "m": m,
        "A": total,
        "word_count": count,
        "denominator": denominator,
        "integral_word_count": integral,
        "minimum_C": minimum,
        "maximum_C": maximum,
        "stream_sha256": stream.hexdigest(),
    }


def check_scan(row: dict[str, object]) -> None:
    expected = PACKET_EXPECTATIONS[(int(row["m"]), int(row["A"]))]
    assert row["word_count"] == expected["word_count"]
    assert row["word_count"] == math.comb(int(row["A"]) - 1, int(row["m"]) - 1)
    assert row["denominator"] == expected["denominator"]
    assert row["integral_word_count"] == 0
    assert row["minimum_C"] == expected["minimum_C"]
    assert row["maximum_C"] == expected["maximum_C"]
    assert row["stream_sha256"] == expected["stream_sha256"]


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    for divisor in range(3, math.isqrt(value) + 1, 2):
        if value % divisor == 0:
            return False
    return True


def prime_obstructions() -> list[dict[str, int]]:
    rows = []
    for m, total, prime in ((5, 8, 13), (8, 13, 233), (11, 18, 7727), (13, 21, 502829)):
        denominator = 2**total - 3**m
        assert is_prime(prime)
        assert denominator % prime == 0
        residues = {affine_C(packet) % prime for packet in compositions(total, m)}
        assert 0 not in residues
        rows.append(
            {
                "m": m,
                "A": total,
                "prime": prime,
                "residue_count": len(residues),
            }
        )
    return rows


def main() -> int:
    strip = exact_strip()
    morphism_checks = check_packet_parity_morphism()
    groupoid_checks = check_rotation_groupoids()
    residue_series_checks = check_residue_multiplicities_and_series()
    length_five = length_five_classes()
    period_eight = period_eight_classes()

    scan_rows = []
    for m, total in PACKET_EXPECTATIONS:
        separator = scan_separator(m, total)
        depth_first = scan_depth_first(m, total)
        check_scan(separator)
        check_scan(depth_first)
        assert separator == depth_first
        scan_rows.append(separator)

    assert sum(int(row["word_count"]) for row in scan_rows) == 4_734_620
    assert sum(int(row["integral_word_count"]) for row in scan_rows) == 0
    obstruction_rows = prime_obstructions()

    metrics = {
        "strip_candidates_m_2_through_17": {str(k): list(v) for k, v in strip.items()},
        "packet_parity_morphism_checks": morphism_checks,
        "rotation_groupoid_checks": groupoid_checks,
        "residue_multiplicity_and_series_checks": residue_series_checks,
        "length_five_class_count": len(length_five),
        "period_eight": period_eight,
        "exhaustive_packet_scans": scan_rows,
        "total_words_scanned_by_each_method": 4_734_620,
        "independent_full_scan_methods": 2,
        "total_integral_words": 0,
        "prime_obstructions": obstruction_rows,
    }
    metrics_sha256 = hashlib.sha256(
        json.dumps(metrics, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    output = {
        "certificate": "exact affine-packet and modular-residue checks",
        "python": sys.version.split()[0],
        "arithmetic": "integer and fractions.Fraction only; no floating point",
        "checks": {
            "packet_to_shortened_and_full_parity_word_morphisms": "PASS",
            "all_intermediate_rational_values_and_odd_return_clocks": "PASS",
            "three_exact_minimal_periods_including_imprimitive_packets": "PASS",
            "cyclic_groupoid_composition_inverses_and_stabilizers": "PASS",
            "residue_multiplicities_and_empty_packet_ranges": "PASS",
            "rational_series_coefficients_and_singleton_modulus": "PASS",
            "cyclic_transport_identity": "PASS",
            "primitive_period_equivalence_bounded_instances": "PASS",
            "exact_strip": "PASS",
            "length_five_classes": "PASS",
            "period_eight_residue_recursion": "PASS",
            "period_eight_99_class_table": "PASS",
            "two_independent_full_packet_scans": "PASS",
            "single_prime_packet_obstructions": "PASS",
        },
        "metrics": metrics,
        "metrics_sha256": metrics_sha256,
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
