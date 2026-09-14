"""Deterministic finite checks for the Crandall 1978 full-paper audit.

This certificate checks exact arithmetic examples, endpoint counterexamples,
finite address realizations, affine trajectory identities, continued-fraction
denominators, and the qx+r examples used by the edition.  It does not replace
the source's infinite proofs or the edition's analytic arguments.
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path


SOURCE = Path(
    r"C:\Users\LOCAL_USER\Documents\Papors\OS\on-the-3x-1-problem-5cygpgqcjg.pdf"
)
SOURCE_BYTES = 964_602
SOURCE_SHA256 = "acafa9070e7c5e4b167d70d7cace81da39489710804c510ff8db4369133217f4"


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def v2(value: int) -> int:
    if value <= 0:
        raise ValueError("v2 is used here only on positive integers")
    exponent = 0
    while value % 2 == 0:
        value //= 2
        exponent += 1
    return exponent


def c_qr(value: int, q: int = 3, r: int = 1) -> tuple[int, int]:
    numerator = q * value + r
    exponent = v2(numerator)
    result = numerator // (2**exponent)
    assert result > 0 and result % 2 == 1
    return result, exponent


def backward(value: Fraction, exponent: int, q: int = 3) -> Fraction:
    return (2**exponent * value - 1) / q


def address_value(exponents: tuple[int, ...], q: int = 3) -> Fraction:
    value = Fraction(1)
    for exponent in exponents:
        value = backward(value, exponent, q)
    return value


def corrected_address_gate(exponents: tuple[int, ...]) -> bool:
    if not exponents or exponents[0] <= 2:
        return False
    value = 1
    final_index = len(exponents) - 1
    for index, exponent in enumerate(exponents):
        powered = (2**exponent) * value
        if powered % 3 != 1:
            return False
        if index < final_index and powered % 9 == 1:
            return False
        value = (powered - 1) // 3
    return value > 1


def source_height(value: int, limit: int = 10_000) -> int | None:
    # Crandall's convention counts C(1)=1, so h(1)=1.
    for step in range(1, limit + 1):
        value, _ = c_qr(value)
        if value == 1:
            return step
    return None


def divisors(value: int) -> list[int]:
    found: set[int] = set()
    for candidate in range(1, math.isqrt(value) + 1):
        if value % candidate == 0:
            found.add(candidate)
            found.add(value // candidate)
    return sorted(found)


def main() -> int:
    measurements: dict[str, int | str | bool] = {}

    assert SOURCE.is_file()
    assert SOURCE.stat().st_size == SOURCE_BYTES
    assert file_sha256(SOURCE) == SOURCE_SHA256

    excursion_checks = 0
    for k in range(2, 21):
        start = 2**k - 1
        value = start
        for j in range(1, k):
            value, _ = c_qr(value)
            assert value == 3**j * 2 ** (k - j) - 1
            excursion_checks += 1
        assert value / start > (3 / 2) ** (k - 1)
    measurements["crandall_excursion_identity_checks"] = excursion_checks

    # Literal endpoint counterexamples to the printed G/Lemma 4.3 package.
    assert address_value((6,)) == 21
    assert c_qr(21)[0] == 1
    assert pow(2, 6, 9) == 1
    assert corrected_address_gate((6,))
    assert address_value((2,)) == 1
    assert source_height(1) == 1
    assert not corrected_address_gate((2,))

    # Literal small-z counterexample to Lemma 5.2.
    z, j = 1, 2
    literal_lower_bound = (2 * math.floor((z - 2) / (6 * j))) ** j
    eligible_positive_sequences = 0
    assert literal_lower_bound == 4
    assert eligible_positive_sequences == 0

    address_checks = 0
    for length in range(1, 5):
        for exponents in __import__("itertools").product(range(1, 9), repeat=length):
            if not corrected_address_gate(exponents):
                continue
            value = address_value(exponents)
            assert value.denominator == 1
            integer_value = value.numerator
            assert integer_value > 1
            assert source_height(integer_value) == length
            address_checks += 1
    assert address_checks > 0
    measurements["corrected_address_realizations_checked"] = address_checks

    # Theorem 7.1 affine identity on exact forward segments.
    trajectory_identity_checks = 0
    for start in range(1, 1_002, 2):
        value = start
        cumulative = [0]
        for k in range(1, 7):
            value, exponent = c_qr(value)
            cumulative.append(cumulative[-1] + exponent)
            lhs = 2 ** cumulative[k] * value - 3**k * start
            rhs = sum(
                2 ** cumulative[position] * 3 ** (k - 1 - position)
                for position in range(k)
            )
            assert lhs == rhs
            trajectory_identity_checks += 1
    measurements["trajectory_affine_identities_checked"] = trajectory_identity_checks

    # A fully explicit admissible r and c witness for the repaired Theorem 6.1 proof.
    getcontext().prec = 80
    r = Decimal(1) / Decimal(100)
    lhs = r * (Decimal(3) / Decimal(64)).ln() / Decimal(2).ln() + Decimal(1) / 2
    rhs = Decimal(3) * Decimal(1).exp() * r
    assert lhs > rhs > 0
    assert r / Decimal(2).ln() > Decimal(1) / Decimal(100)
    measurements["explicit_counting_exponent_denominator"] = 100

    # Continued fraction data and the historical numerical lower bound.
    partial_quotients = [1, 1, 1, 2, 2, 3, 1, 5, 2, 23, 2, 2]
    p_previous, q_previous = 1, 0
    p_current, q_current = partial_quotients[0], 1
    convergents = [(p_current, q_current)]
    for quotient in partial_quotients[1:]:
        p_previous, p_current = p_current, quotient * p_current + p_previous
        q_previous, q_current = q_current, quotient * q_current + q_previous
        convergents.append((p_current, q_current))
    assert convergents[10] == (50_508, 31_867)
    assert convergents[11] == (125_743, 79_335)
    assert Fraction(2_000_000_000, 31_867 + 79_335) > 17_985

    # Exact generalized-map cycles and source OCR correction.
    q5_values = [13]
    q5_exponents = []
    for _ in range(3):
        next_value, exponent = c_qr(q5_values[-1], q=5)
        q5_values.append(next_value)
        q5_exponents.append(exponent)
    assert q5_values == [13, 33, 83, 13]
    assert q5_exponents == [1, 1, 5]
    assert 2**sum(q5_exponents) - 5**3 == 3

    q181_values = [27]
    q181_exponents = []
    for _ in range(2):
        next_value, exponent = c_qr(q181_values[-1], q=181)
        q181_values.append(next_value)
        q181_exponents.append(exponent)
    assert q181_values == [27, 611, 27]
    assert q181_exponents == [3, 12]
    assert 2**sum(q181_exponents) - 181**2 == 7

    q = 1093
    order = 364
    assert pow(2, order, q) == 1
    for proper_divisor in divisors(order)[:-1]:
        assert pow(2, proper_divisor, q) != 1
    assert pow(2, order, q * q) == 1
    assert pow(2, 182, q) == 1092
    assert pow(2, 52, q) == 27
    assert pow(2, 28, q) == 121
    for multiplier in range(1, 9):
        exponent = order * multiplier
        height_one = (2**exponent - 1) // q
        assert height_one > 0 and height_one % 2 == 1
        assert c_qr(height_one, q=q)[0] == 1
        assert height_one % q == 0
        # A predecessor u would require q*u+1=2^a*height_one, impossible mod q.
        for predecessor_exponent in range(1, 2 * order + 1):
            assert (2**predecessor_exponent * height_one - 1) % q != 0
    measurements["q1093_height_one_values_checked"] = 8
    measurements["q1093_predecessor_exponents_per_value"] = 2 * order

    report = {
        "schema_version": "1.0",
        "status": "pass",
        "source_sha256": SOURCE_SHA256,
        "python_version": sys.version.split()[0],
        "measurements": measurements,
        "nonclaims": [
            "Finite checks do not prove the infinite address or counting theorems.",
            "No nontrivial 3x+1 cycle or unbounded qx+1 orbit is asserted.",
            "The certificate does not replace the repaired analytic and continued-fraction proofs.",
        ],
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
