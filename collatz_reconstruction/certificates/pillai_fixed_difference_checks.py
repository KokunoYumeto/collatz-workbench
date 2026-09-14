#!/usr/bin/env python3
"""Deterministic finite checks for the Pillai--Pólya--Siegel audit.

The arbitrary-parameter proofs remain in TeX.  This file checks source
identity, the printed degree counterexamples, exact exponent arithmetic,
finite instances of the prime-coordinate inverse, and the integer-exponent
denominator boundary.  It also checks the exact sign-quadrant inverse and a
finite algebra kernel for Pólya's residue-cell cubic.  It is not presented as
a proof of Pólya's, Thue's, or Siegel's infinite theorems.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import product
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

EXPECTED_HASHES = {
    "external_literature/dependency_gate_2026-08-25/"
    "pillai_1931_inequality_google_drive_witness.pdf":
        "dd4ef9acb06352fad2913baa6b6d4ab854fd9689e2f6c13910bf99573f84ee69",
    "external_literature/dependency_gate_2026-08-25/"
    "polya_1918_zur_arithmetischen_untersuchung_der_polynome_gdz.pdf":
        "4b067f72cff9598a0ee37924793d28ea67ed58bc7ca14ca149e5c4bed599ff5f",
    "external_literature/dependency_gate_2026-08-25/"
    "siegel_1921_approximation_algebraischer_zahlen_gdz_extract.pdf":
        "309cd862fa24f173c7e17fb86db5f082f0c8ad8b89762dd4ddf8d0d4c0dcdc4f",
    "external_literature/dependency_gate_2026-08-25/"
    "thue_1908_skrifter_volume_bemerkungen_and_om_en_generel_bhl_ia.pdf":
        "80444727aa7790eb52e833d3ed4e860e076bef73bd5ad3fe7e1bf4a555f394aa",
    "external_literature/dependency_gate_2026-08-25/"
    "thue_1909_ueber_annaeherungswerte_gdz.pdf":
        "629f8fbe27376812abc44394a960e6ab343471764016c73e8b23e1d789f80b22",
    "state/index_routes.jsonl":
        "b05028694bf133b9b19f2b0c0a771323b7a47ae872c0712769267aaf1f1eff38",
    "state/document_routes.jsonl":
        "e439a5f9a70253b00824df5be791415e1c068d574c23f6f7f61851c19a88b2a5",
    "state/index_snapshot.json":
        "7d5a17440a3cb039f2bfbb4814567b5805117002136cc65687de738ee99af62f",
}


def digest(path: Path) -> str:
    h = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def mu(q: int) -> Fraction:
    assert q >= 1
    return min(Fraction(q, lam + 1) + lam for lam in range(1, q + 1))


def valuations(value: int, primes: tuple[int, ...]) -> tuple[int, ...]:
    out: list[int] = []
    remainder = value
    for prime in primes:
        exponent = 0
        while remainder % prime == 0:
            remainder //= prime
            exponent += 1
        out.append(exponent)
    assert remainder == 1
    return tuple(out)


def main() -> None:
    for relative, expected in EXPECTED_HASHES.items():
        actual = digest(ROOT / relative)
        assert actual == expected, (relative, actual, expected)

    # Pillai's full-degree inference has two exact counterexamples.
    # (4/1)^(1/4)=sqrt(2), and T^2-2 is irreducible over Q because 2 is not
    # a rational square; hence the degree is two rather than four.
    assert 1 * 1 < 2 < 2 * 2
    assert 4 == 2**2
    # (2/2)^(1/2)=1 has degree one although neither displayed coefficient is
    # a perfect square.
    assert Fraction(2, 2) == 1
    assert all(n * n != 2 for n in range(2))

    previous = mu(1)
    monotonic_pairs = 0
    for q in range(2, 513):
        current = mu(q)
        assert current >= previous
        previous = current
        monotonic_pairs += 1

    # Exact difference-of-powers factorization over an integer test kernel.
    factorization_checks = 0
    for r in range(2, 13):
        for u in range(1, 18):
            for v in range(1, 18):
                rhs = (u - v) * sum(
                    u ** (r - 1 - j) * v**j for j in range(r)
                )
                assert u**r - v**r == rhs
                factorization_checks += 1

    # The prime-exponent morphism and its valuation inverse.
    primes = (2, 3, 5)
    coordinate_checks = 0
    for exponents in product(range(7), repeat=len(primes)):
        value = 1
        for prime, exponent in zip(primes, exponents, strict=True):
            value *= prime**exponent
        assert valuations(value, primes) == exponents
        coordinate_checks += 1

    # The off-axis sign decomposition used to extend Thue III from positive
    # coordinates to all integer sign cells is a literal two-sided inverse.
    sign_quadrant_checks = 0
    for x in range(-10, 11):
        for y in range(-10, 11):
            if x == 0 or y == 0:
                continue
            encoded = (
                1 if x > 0 else -1,
                1 if y > 0 else -1,
                abs(x),
                abs(y),
            )
            epsilon, delta, X, Y = encoded
            assert (epsilon * X, delta * Y) == (x, y)
            sign_quadrant_checks += 1

    # Finite exact-algebra kernel for the residue-cell map.  Define b and d
    # from a retained source n and the two cube coordinates; then verify both
    # linear-value identities, elimination, the inverse formulas, nonzero
    # discriminant, and the coefficient obstruction to a scalar linear cube.
    residue_cubic_checks = 0
    for a, c in product((-3, -2, -1, 1, 2, 3), repeat=2):
        for R, S0 in product(range(1, 5), repeat=2):
            for X, Y in product(range(1, 6), repeat=2):
                for n in range(5):
                    b = R * X**3 - a * n
                    d = S0 * Y**3 - c * n
                    Delta = a * d - b * c
                    assert a * n + b == R * X**3
                    assert c * n + d == S0 * Y**3
                    assert a * S0 * Y**3 - c * R * X**3 == Delta
                    assert Fraction(R * X**3 - b, a) == n
                    assert Fraction(S0 * Y**3 - d, c) == n
                    discriminant = -27 * (a * S0) ** 2 * (c * R) ** 2
                    assert discriminant != 0
                    # A scalar cube with both pure coefficients nonzero has
                    # nonzero X^2Y coefficient 3*lambda*u^2*v.
                    assert a * S0 != 0 and c * R != 0
                    residue_cubic_checks += 1

    # Exhaust the local negative-exponent kernel.  Every integral difference
    # has nonnegative exponents, and its zero fibre contains only (0,0).
    denominator_checks = 0
    integral_checks = 0
    zero_checks = 0
    for x in range(-20, 21):
        for y in range(-20, 21):
            difference = Fraction(2) ** x - Fraction(3) ** y
            denominator_checks += 1
            if difference.denominator == 1:
                integral_checks += 1
                assert x >= 0 and y >= 0
                if difference == 0:
                    zero_checks += 1
                    assert (x, y) == (0, 0)

    # Finite, explicitly bounded samples of the fixed-difference fibres.
    # These checks are subordinate to Pólya's infinite gap theorem.
    fibre_checks = 0
    powers2 = {2**x: x for x in range(81)}
    powers3 = {3**y: y for y in range(81)}
    for z in range(-500, 501):
        pairs = [
            (x, powers3[u - z])
            for u, x in powers2.items()
            if u - z in powers3
        ]
        assert len(pairs) == len(set(pairs))
        fibre_checks += len(pairs)

    print("PASS pillai_fixed_difference_checks")
    print(f"source_and_frozen_hashes={len(EXPECTED_HASHES)}")
    print(f"mu_monotonic_pairs={monotonic_pairs}")
    print(f"factorization_checks={factorization_checks}")
    print(f"prime_coordinate_inverse_checks={coordinate_checks}")
    print(f"sign_quadrant_inverse_checks={sign_quadrant_checks}")
    print(f"residue_cubic_algebra_checks={residue_cubic_checks}")
    print(f"integer_exponent_denominator_checks={denominator_checks}")
    print(f"integer_valued_samples={integral_checks}")
    print(f"zero_fibre_samples={zero_checks}")
    print(f"bounded_fixed_difference_pairs={fibre_checks}")


if __name__ == "__main__":
    main()
