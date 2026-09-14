"""Finite, reproducible checks for the repaired Crandall CF dependency.

The infinite continued-fraction identities are proved in the TeX edition and
supported by the content-read Steuding source.  This script checks the pinned
source/route hashes, the printed partial-quotient prefix, exact convergent
recurrences and determinants, the historical q_10/q_11 values, and the
strict numerical boundary used in the cycle estimate.  It is not a proof of
the Collatz conjecture or of the historical 10^9 computation.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CRANDALL = Path(r"C:\Users\LOCAL_USER\Documents\Papors\OS\on-the-3x-1-problem-5cygpgqcjg.pdf")
STEUDING = Path(
    r"C:\Users\LOCAL_USER\Documents\Papors\OS\Mason-Stothers theorem\Diophantine Analysis (Jorn Steuding).pdf"
)
PINNED = {
    CRANDALL: (964602, "acafa9070e7c5e4b167d70d7cace81da39489710804c510ff8db4369133217f4"),
    STEUDING: (2257201, "ea31b76c5c400f91b23038885c3576224496457633be84bcc22d335e3e323b88"),
    ROOT / "state" / "index_routes.jsonl": (
        274170,
        "b05028694bf133b9b19f2b0c0a771323b7a47ae872c0712769267aaf1f1eff38",
    ),
    ROOT / "state" / "document_routes.jsonl": (
        324776,
        "e439a5f9a70253b00824df5be791415e1c068d574c23f6f7f61851c19a88b2a5",
    ),
    ROOT / "state" / "index_snapshot.json": (
        799,
        "7d5a17440a3cb039f2bfbb4814567b5805117002136cc65687de738ee99af62f",
    ),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def convergents(partial_quotients: list[int]) -> list[tuple[int, int]]:
    p_prev, q_prev = 1, 0
    p_cur, q_cur = partial_quotients[0], 1
    result = [(p_cur, q_cur)]
    for a in partial_quotients[1:]:
        p_prev, p_cur = p_cur, a * p_cur + p_prev
        q_prev, q_cur = q_cur, a * q_cur + q_prev
        result.append((p_cur, q_cur))
    return result


def log_bounds(integer: int, terms: int = 140) -> tuple[Fraction, Fraction]:
    """Exact rational enclosure from log x = 2*atanh((x-1)/(x+1))."""

    z = Fraction(integer - 1, integer + 1)
    partial = 2 * sum(
        (z ** (2 * j + 1) / (2 * j + 1) for j in range(terms + 1)),
        Fraction(0),
    )
    # Every omitted denominator is at least 2*terms+3.
    remainder_upper = (
        2
        * z ** (2 * terms + 3)
        / ((2 * terms + 3) * (1 - z * z))
    )
    return partial, partial + remainder_upper


def absolute_linear_interval(
    x: int, y: int, t_lower_num: int, t_upper_num: int, scale: int
) -> tuple[int, int]:
    """Integer-scaled enclosure of |x-y*t| for t in the pinned interval."""

    left = x * scale - y * t_upper_num
    right = x * scale - y * t_lower_num
    assert left <= right
    if left > 0:
        return left, right
    if right < 0:
        return -right, -left
    return 0, max(-left, right)


def main() -> int:
    for path, (size, digest) in PINNED.items():
        assert path.is_file(), path
        assert path.stat().st_size == size, (path, path.stat().st_size)
        assert sha256(path) == digest, path

    partial_quotients = [1, 1, 1, 2, 2, 3, 1, 5, 2, 23, 2, 2]
    conv = convergents(partial_quotients)
    assert conv[10] == (50508, 31867)
    assert conv[11] == (125743, 79335)

    determinant_checks = 0
    for n in range(1, len(conv)):
        p_n, q_n = conv[n]
        p_prev, q_prev = conv[n - 1]
        assert p_n * q_prev - p_prev * q_n == (-1) ** (n - 1)
        determinant_checks += 1

    # The exact rational boundary used in the historical corollary.
    assert Fraction(2_000_000_000, 31867 + 79335) > 17985
    assert Fraction(56, 81) > Fraction(20, 29)

    log_two_lower, log_two_upper = log_bounds(2)
    log_three_lower, log_three_upper = log_bounds(3)
    assert log_two_lower > Fraction(56, 81)
    t_exact_lower = log_three_lower / log_two_upper
    t_exact_upper = log_three_upper / log_two_lower
    assert 1 < t_exact_lower < t_exact_upper < 2

    # Coarsen the proved enclosure to a fixed-denominator interval.  All
    # subsequent comparisons are integer arithmetic; no floating point or
    # unproved decimal value of log_2(3) is used.
    scale = 10**60
    t_lower_num = (t_exact_lower.numerator * scale) // t_exact_lower.denominator
    t_upper_num = (
        t_exact_upper.numerator * scale + t_exact_upper.denominator - 1
    ) // t_exact_upper.denominator
    t_lower = Fraction(t_lower_num, scale)
    t_upper = Fraction(t_upper_num, scale)
    assert t_lower <= t_exact_lower < t_exact_upper <= t_upper

    # Verify that the rigorous interval has exactly the printed prefix.
    cf_lower, cf_upper = t_lower, t_upper
    for index, expected in enumerate(partial_quotients):
        lower_digit = cf_lower.numerator // cf_lower.denominator
        upper_digit = cf_upper.numerator // cf_upper.denominator
        assert lower_digit == upper_digit == expected
        if index + 1 < len(partial_quotients):
            cf_lower, cf_upper = (
                1 / (cf_upper - expected),
                1 / (cf_lower - expected),
            )
    # Crandall's state space is the positive odd integers.  Therefore the
    # open verification range m<10^9 excludes equality at its even endpoint.
    assert 1_000_000_000 % 2 == 0

    # The first admissible denominator pair already controls all later ones:
    # q_n is increasing after q_1 for positive partial quotients.
    assert conv[4][1] == 12 and conv[5][1] == 41
    assert conv[4][1] + conv[5][1] > 20
    for n in range(4, len(conv) - 1):
        assert conv[n][1] + conv[n + 1][1] >= conv[4][1] + conv[5][1]

    # Finite exact checks of every closest-integer competitor for t through
    # the printed prefix.  Checking floor(y*t) and floor(y*t)+1 controls all
    # integer x at that y; x=0 separately exercises the nonpositive branch.
    # The infinite law remains controlled by Steuding and the TeX proof.
    two_sided_error_checks = 0
    closest_integer_best_checks = 0
    nonpositive_boundary_checks = 0
    equal_denominator_checks = 0
    for n, (p_n, q_n) in enumerate(conv[2:], start=2):
        error_lower, error_upper = absolute_linear_interval(
            p_n, q_n, t_lower_num, t_upper_num, scale
        )
        assert error_lower > 0
        if n + 1 < len(conv):
            q_next = conv[n + 1][1]
            assert error_lower * (q_n + q_next) > scale
            assert error_upper * q_next < scale
            two_sided_error_checks += 1
        for y in range(1, q_n):
            target_lower = y * t_lower_num
            target_upper = y * t_upper_num
            floor_x = target_lower // scale
            assert target_upper // scale == floor_x
            for x in (floor_x, floor_x + 1):
                if x * q_n == p_n * y:
                    continue
                competitor_lower, _ = absolute_linear_interval(
                    x, y, t_lower_num, t_upper_num, scale
                )
                assert error_upper < competitor_lower
                closest_integer_best_checks += 1
            zero_lower, _ = absolute_linear_interval(
                0, y, t_lower_num, t_upper_num, scale
            )
            assert error_upper < zero_lower
            nonpositive_boundary_checks += 1
        if n >= 4:
            for x in (p_n - 1, p_n + 1):
                competitor_lower, _ = absolute_linear_interval(
                    x, q_n, t_lower_num, t_upper_num, scale
                )
                assert error_upper < competitor_lower
                equal_denominator_checks += 1

    measurements = {
        "status": "pass",
        "pinned_hashes": len(PINNED),
        "convergent_prefix_length": len(conv),
        "determinant_checks": determinant_checks,
        "two_sided_error_checks": two_sided_error_checks,
        "closest_integer_best_checks": closest_integer_best_checks,
        "nonpositive_boundary_checks": nonpositive_boundary_checks,
        "equal_denominator_checks": equal_denominator_checks,
        "q4": conv[4][1],
        "q5": conv[5][1],
        "q10": conv[10][1],
        "q11": conv[11][1],
        "historical_bound_strict": True,
        "historical_parity_endpoint_strict": True,
        "rigorous_log_series_terms": 141,
        "rational_t_interval_decimal_places": 60,
    }
    print(json.dumps(measurements, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
