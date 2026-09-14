"""Exact checks for the private-tail and Haar-covariance chapter.

This certificate does not establish that 63,728,127 is a delay record; that
status is supplied by the separate exhaustive C++ scan through every smaller
start.  It independently replays both displayed orbits and verifies every
rational identity in the Haar comparison theorem.
"""

from __future__ import annotations

from fractions import Fraction


def collatz(n: int) -> int:
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def v2(n: int) -> int:
    if n == 0:
        raise ValueError("v2(0) is not finite")
    return (n & -n).bit_length() - 1


def orbit_to_cycle(n: int) -> list[int]:
    orbit = [n]
    while n not in (1, 2):
        n = collatz(n)
        orbit.append(n)
    return orbit


def private_tail_variation(orbit: list[int], previous_record: int) -> Fraction:
    tau = len(orbit) - 1
    total = Fraction(0)
    for k in range(previous_record, tau - 1):
        x = orbit[k]
        if x % 2 == 0:
            total += Fraction(1, 3 * (1 << v2(x)))
    return total + Fraction(1, 6)


def check_finite_records() -> None:
    small_taus = [len(orbit_to_cycle(n)) - 1 for n in range(1, 27)]
    assert max(small_taus) == 15

    orbit_27 = orbit_to_cycle(27)
    assert len(orbit_27) - 1 == 69
    assert orbit_27[-2] == 4
    w_27 = private_tail_variation(orbit_27, 15)
    assert w_27 == Fraction(137, 48)
    assert w_27 / 54 == Fraction(137, 2592)
    assert w_27 / 54 == Fraction(1, 18) - Fraction(7, 2592)

    orbit_large = orbit_to_cycle(63_728_127)
    assert len(orbit_large) - 1 == 591
    assert orbit_large[-2] == 4
    w_large = private_tail_variation(orbit_large, 465)
    assert w_large == Fraction(445, 64)
    assert w_large / 126 == Fraction(1, 18) - Fraction(1, 2688)


def joint_moment(h: int) -> Fraction:
    if h < 1:
        raise ValueError("h must be positive")
    before = sum(
        (Fraction(1, 6) * Fraction(1, 2 ** (2 * j + 1)) for j in range(1, h)),
        Fraction(0),
    )
    after = Fraction(1, 2 ** (2 * h + 4)) / (1 - Fraction(1, 8))
    return before + after


def finite_variance(g: int) -> Fraction:
    variance_one = Fraction(11, 252)
    covariances = sum(
        ((g - h) * Fraction(-5, 126 * 4**h) for h in range(1, g)),
        Fraction(0),
    )
    return g * variance_one + 2 * covariances


def closed_variance(g: int) -> Fraction:
    return Fraction(39 * g + 80, 2268) - Fraction(20, 2268 * 4 ** (g - 1))


def check_haar_identities() -> None:
    mean = sum((Fraction(1, 2 ** (2 * j + 1)) for j in range(1, 200)), Fraction(0))
    mean += Fraction(1, 6) * Fraction(1, 4**199)
    assert mean == Fraction(1, 6)

    second = sum((Fraction(1, 2 ** (3 * j + 1)) for j in range(1, 200)), Fraction(0))
    second += Fraction(1, 14) * Fraction(1, 8**199)
    assert second == Fraction(1, 14)
    assert second - mean * mean == Fraction(11, 252)

    for h in range(1, 200):
        expected = Fraction(1, 36) - Fraction(5, 126 * 4**h)
        assert joint_moment(h) == expected

    for g in range(1, 1001):
        assert finite_variance(g) == closed_variance(g)


def main() -> None:
    check_finite_records()
    check_haar_identities()
    print("PASS private-tail examples r=27 and r=63728127")
    print("PASS exact Haar moments and covariances for h=1..199")
    print("PASS exact finite-variance identity for g=1..1000")


if __name__ == "__main__":
    main()
