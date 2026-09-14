"""Exact finite checks for Steuding, Exercise 5.22.

This certificate checks the quadratic-field algebra in the reconstructed
Markoff-constant calculation and the literal 4 -> 2 -> 1 -> 4 orbit.  It is
not a proof of the Collatz conjecture, Serret's theorem, or the limiting
continued-fraction formula.
"""

from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path


RADICAND = 229
SOURCE = Path(
    r"C:\Users\LOCAL_USER\Documents\Papors\OS\Mason-Stothers theorem"
    r"\Diophantine Analysis (Jorn Steuding).pdf"
)
EXPECTED_SOURCE_SHA256 = (
    "ea31b76c5c400f91b23038885c3576224496457633be84bcc22d335e3e323b88"
)


@dataclass(frozen=True)
class Quad:
    """The exact element a + b*sqrt(229) of Q(sqrt(229))."""

    a: Fraction
    b: Fraction = Fraction(0)

    @classmethod
    def rational(cls, numerator: int, denominator: int = 1) -> "Quad":
        return cls(Fraction(numerator, denominator))

    def __add__(self, other: "Quad") -> "Quad":
        return Quad(self.a + other.a, self.b + other.b)

    def __sub__(self, other: "Quad") -> "Quad":
        return Quad(self.a - other.a, self.b - other.b)

    def __mul__(self, other: "Quad") -> "Quad":
        return Quad(
            self.a * other.a + RADICAND * self.b * other.b,
            self.a * other.b + self.b * other.a,
        )

    def inverse(self) -> "Quad":
        norm = self.a * self.a - RADICAND * self.b * self.b
        if norm == 0:
            raise ZeroDivisionError("zero norm")
        return Quad(self.a / norm, -self.b / norm)

    def __truediv__(self, other: "Quad") -> "Quad":
        return self * other.inverse()


ZERO = Quad.rational(0)
ONE = Quad.rational(1)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def collatz_unshortened(n: int) -> int:
    if n <= 0:
        raise ValueError("the Steuding exercise has positive-integer domain")
    return n // 2 if n % 2 == 0 else 3 * n + 1


def main() -> int:
    if sha256(SOURCE) != EXPECTED_SOURCE_SHA256:
        raise AssertionError("controlling Steuding PDF hash mismatch")

    root = Quad(Fraction(0), Fraction(1))
    beta = Quad(Fraction(11, 6), Fraction(1, 6))
    forward = (
        beta,
        Quad(Fraction(13, 10), Fraction(1, 10)),
        Quad(Fraction(7, 18), Fraction(1, 18)),
    )
    backward = (
        Quad(Fraction(-13, 10), Fraction(1, 10)),
        Quad(Fraction(-7, 18), Fraction(1, 18)),
        Quad(Fraction(-11, 6), Fraction(1, 6)),
    )

    assert Quad.rational(3) * beta * beta - Quad.rational(11) * beta - Quad.rational(9) == ZERO

    digits = (4, 2, 1)
    for i, digit in enumerate(digits):
        assert forward[i] == Quad.rational(digit) + ONE / forward[(i + 1) % 3]

    # B_i=[0;a_i,a_(i-1),...] and indices are read modulo three.
    for i, digit in enumerate(digits):
        assert backward[i] == ONE / (
            Quad.rational(digit) + backward[(i - 1) % 3]
        )

    phase_sums = tuple(
        forward[(i + 1) % 3] + backward[i] for i in range(3)
    )
    expected_sums = (root / Quad.rational(5), root / Quad.rational(9), root / Quad.rational(3))
    assert phase_sums == expected_sums

    phase_reciprocals = tuple(ONE / value for value in phase_sums)
    expected_reciprocals = (
        Quad(Fraction(0), Fraction(5, 229)),
        Quad(Fraction(0), Fraction(9, 229)),
        Quad(Fraction(0), Fraction(3, 229)),
    )
    assert phase_reciprocals == expected_reciprocals
    assert expected_reciprocals[2].b < expected_reciprocals[0].b < expected_reciprocals[1].b

    orbit = [4]
    for _ in range(3):
        orbit.append(collatz_unshortened(orbit[-1]))
    assert orbit == [4, 2, 1, 4]

    report = {
        "schema_version": "1.0",
        "status": "pass",
        "python_version": sys.version.split()[0],
        "source_sha256": EXPECTED_SOURCE_SHA256,
        "quadratic_radicand": RADICAND,
        "pure_period_polynomial": "3*X^2-11*X-9",
        "forward_phase_identities_checked": 3,
        "backward_phase_identities_checked": 3,
        "perron_phase_sums": ["sqrt(229)/5", "sqrt(229)/9", "sqrt(229)/3"],
        "phase_reciprocals": ["5/sqrt(229)", "9/sqrt(229)", "3/sqrt(229)"],
        "markoff_constant": "3/sqrt(229)",
        "unshortened_cycle_checked": orbit,
        "nonclaims": [
            "The exact finite algebra does not prove the Collatz conjecture.",
            "The certificate does not replace Serret's theorem or the limiting formula (5.11).",
            "Equality of Markoff constants is not treated as equality of equivalence classes.",
        ],
    }
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
