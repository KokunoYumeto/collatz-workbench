#!/usr/bin/env python3
"""Exact finite checks for the Collatz history-law continuation (stdlib only).

Run: python -B check_history_law.py > verification.json
Assertions are explicit, so python -O performs the same checks.
The Gaussian limit is proved in RESEARCH_NOTE.md, not certified by these tests.
"""
from __future__ import annotations

import json
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from math import comb
from typing import Iterator

Word = tuple[int, ...]


def require(ok: bool, message: str) -> None:
    if not ok:
        raise AssertionError(message)


def natural(value: int, name: str, positive: bool = False) -> None:
    if type(value) is not int or value < int(positive):
        raise ValueError(f"{name} must be an integer >= {int(positive)}")


def affine(word: Word) -> tuple[int, int]:
    if not word:
        raise ValueError("a nonempty exponent word is required")
    a_sum, numerator = 0, 0
    for a in word:
        natural(a, "exponent", True)
        numerator = 3 * numerator + (1 << a_sum)
        a_sum += a
    return a_sum, numerator


def cylinder(word: Word) -> tuple[int, int, int]:
    """Return (A, r, h), where n=r mod 2^(A+1), j=h mod 2^A, n=2j+1."""
    a_sum, numerator = affine(word)
    modulus = 1 << (a_sum + 1)
    r = (((1 << a_sum) - numerator) * pow(3 ** len(word), -1, modulus)) % modulus
    require(0 < r < modulus and r % 2 == 1, "invalid odd residue")
    return a_sum, r, (r - 1) // 2


def residue_count(h: int, modulus: int, lower: int, upper: int) -> int:
    if upper < lower:
        return 0
    return (upper - h) // modulus - (lower - 1 - h) // modulus


def word_count(word: Word, n_starts: int, offset: int = 0) -> int:
    natural(n_starts, "n_starts", True)
    natural(offset, "offset")
    a_sum, _, h = cylinder(word)
    return residue_count(h, 1 << a_sum, offset, offset + n_starts - 1)


def history(n: int, depth: int) -> tuple[Word, bool]:
    natural(n, "start", True)
    natural(depth, "depth", True)
    if n % 2 == 0:
        raise ValueError("start must be odd")
    x, exponents, descended = n, [], False
    for _ in range(depth):
        y = 3 * x + 1
        a = (y & -y).bit_length() - 1
        x = y >> a
        exponents.append(a)
        descended = descended or x < n
    return tuple(exponents), descended


def capped_words(depth: int, cap: int) -> Iterator[Word]:
    natural(depth, "depth", True)
    natural(cap, "cap")
    for total in range(depth, cap + 1):
        for cuts in combinations(range(1, total), depth - 1):
            ends = (0,) + cuts + (total,)
            yield tuple(ends[i + 1] - ends[i] for i in range(depth))


def tail(depth: int, cap: int) -> F:
    natural(depth, "depth", True)
    natural(cap, "cap")
    return F(sum(comb(cap, j) for j in range(min(depth - 1, cap) + 1)), 1 << cap)


def bounds(n_starts: int, depth: int, cap: int) -> tuple[F, F]:
    natural(n_starts, "n_starts", True)
    q = tail(depth, cap)
    k = comb(cap, depth) if cap >= depth else 0
    return max(F(0), q - F(n_starts, 1 << (cap + 1))), min(F(1), q + F(k, n_starts))


def rounding_upper(n_starts: int, depth: int, cap: int) -> F:
    correction = sum((F(comb(a - 1, depth - 1) * (n_starts % (1 << a)), n_starts * (1 << a))
                      for a in range(depth, cap + 1)), F(0))
    return min(F(1), tail(depth, cap) + correction)


def support_lower(n_starts: int, depth: int) -> F:
    # Locate the N largest geometric atoms without enumerating words.
    lo, hi = depth - 1, max(depth, 1)
    while comb(hi, depth) <= n_starts:
        hi *= 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if comb(mid, depth) <= n_starts:
            lo = mid
        else:
            hi = mid
    return tail(depth, lo) - F(n_starts - (comb(lo, depth) if lo >= depth else 0), 1 << (lo + 1))


def total_variation(counts: Counter[Word], n_starts: int) -> F:
    require(sum(counts.values()) == n_starts, "sample mass mismatch")
    return 1 - sum((min(F(c, n_starts), F(1, 1 << sum(w))) for w, c in counts.items()), F(0))


def no_descent_threshold(word: Word) -> int | None:
    """None means +infinity. All original affine offsets are retained."""
    a_sum, numerator, threshold = 0, 0, None
    for j, a in enumerate(word, 1):
        natural(a, "exponent", True)
        numerator = 3 * numerator + (1 << a_sum)
        a_sum += a
        d = (1 << a_sum) - 3 ** j
        if d > 0:
            t = numerator // d
            threshold = t if threshold is None else min(threshold, t)
    return threshold


def descent_certificate(n_starts: int, depth: int, cap: int, offset: int = 0) -> dict[str, int]:
    accounted, descended = 0, 0
    for word in capped_words(depth, cap):
        a_sum, _, h = cylinder(word)
        count = word_count(word, n_starts, offset)
        accounted += count
        threshold = no_descent_threshold(word)
        upper = offset + n_starts - 1
        if threshold is not None:
            upper = min(upper, (threshold - 1) // 2)
        no_descent = residue_count(h, 1 << a_sum, offset, upper)
        descended += count - no_descent
    require(0 <= descended <= accounted <= n_starts, "bad descent partition")
    return {"lower": descended, "upper": descended + n_starts - accounted,
            "accounted": accounted, "unresolved": n_starts - accounted}


def lagrange_value(nodes: list[int], values: list[F], moments: list[F]) -> F:
    require(len(nodes) == len(set(nodes)) == len(values) == len(moments), "bad interpolation inputs")
    answer = F(0)
    for i, node in enumerate(nodes):
        coefficients = [F(1)]
        for j, other in enumerate(nodes):
            if i == j:
                continue
            nxt = [F(0)] * (len(coefficients) + 1)
            for k, c in enumerate(coefficients):
                nxt[k] -= other * c / (node - other)
                nxt[k + 1] += c / (node - other)
            coefficients = nxt
        answer += values[i] * sum((c * moments[k] for k, c in enumerate(coefficients)), F(0))
    return answer


def fraction_record(value: F) -> dict[str, int | float]:
    return {"numerator": value.numerator, "denominator": value.denominator, "decimal": float(value)}


def run() -> dict:
    counters = Counter()
    for depth in range(1, 6):
        for cap in range(0, 11):
            words = list(capped_words(depth, cap))
            expected = comb(cap, depth) if cap >= depth else 0
            require(len(words) == expected, "hockey-stick cardinality failed")
            require(len({cylinder(w)[1] for w in words}) == len(words), "residue-node collision")
            require(sum((F(1, 1 << sum(w)) for w in words), F(0)) + tail(depth, cap) == 1,
                    "negative-binomial mass identity failed")
            counters["capped_families"] += 1
            for word in words:
                a_sum, r, _ = cylinder(word)
                for lift in (0, 1, 7):
                    require(history(r + (lift << (a_sum + 1)), depth)[0] == word, "cylinder realization failed")
                    counters["integer_lifts"] += 1
    for offset in (0, 17, 10**30 + 3):
        for n_starts in (1, 7, 31, 128):
            for depth in range(1, 7):
                counts = Counter()
                actual_descents = 0
                for j in range(offset, offset + n_starts):
                    word, descended = history(2 * j + 1, depth)
                    counts[word] += 1
                    actual_descents += descended
                    threshold = no_descent_threshold(word)
                    require(descended == (threshold is not None and 2 * j + 1 > threshold),
                            "offset-preserving descent test failed")
                    counters["descent_equivalences"] += 1
                tv = total_variation(counts, n_starts)
                require(support_lower(n_starts, depth) <= tv, "optimal support lower bound failed")
                for word, c in counts.items():
                    require(word_count(word, n_starts, offset) == c, "exact interval count failed")
                for cap in range(0, 17):
                    lo, hi = bounds(n_starts, depth, cap)
                    require(lo <= tv <= hi and tv <= rounding_upper(n_starts, depth, cap), "TV envelope failed")
                    counters["tv_envelopes"] += 1
                for cap in (depth, depth + 2, depth + 4):
                    cert = descent_certificate(n_starts, depth, cap, offset)
                    require(cert["lower"] <= actual_descents <= cert["upper"], "descent certificate failed")
                    for word in capped_words(depth, cap):
                        require(word_count(word, n_starts, offset) == counts[word], "zero/nonzero cylinder count failed")
                        counters["cylinder_counts"] += 1
                    counters["descent_certificates"] += 1
                counters["interval_laws"] += 1
    # The finite spectral predecessor uses moments; no numerical zeta zero is used here.
    words = list(capped_words(2, 4))
    nodes = [0] + [cylinder(w)[1] for w in words]
    for n_starts, offset in ((1, 0), (257, 0), (37, 100)):
        weights = [F(word_count(w, n_starts, offset), n_starts) for w in words]
        weights.insert(0, 1 - sum(weights, F(0)))
        moments = [sum((p * x**j for p, x in zip(weights, nodes)), F(0)) for j in range(len(nodes))]
        for i in range(len(nodes)):
            values = [F(int(i == j)) for j in range(len(nodes))]
            require(lagrange_value(nodes, values, moments) == weights[i], "censored weight recovery failed")
            counters["moment_weight_recoveries"] += 1
        # Simultaneous tests, evaluated on the same word; 9 and 15 are not coprime.
        values = [F(0)]
        for w in words:
            a_sum, numerator = affine(w)
            d = (1 << a_sum) - 3 ** len(w)
            values.append(F(int(numerator % 9 == 7 and numerator % 15 == 7 and d > 0 and numerator % d == 0)))
        require(lagrange_value(nodes, values, moments) == sum((p * v for p, v in zip(weights, values)), F(0)),
                "joint arithmetic predicate recovery failed")
        counters["joint_predicates"] += 1
    require(no_descent_threshold((2,)) == 1 and not history(1, 1)[1], "fixed point equality mishandled")
    negative_controls = []
    for label, action in (
        ("even starting integer", lambda: history(2, 1)),
        ("zero exponent", lambda: cylinder((0, 2))),
        ("negative interval offset", lambda: word_count((2,), 10, -1)),
        ("lost probability mass", lambda: total_variation(Counter({(2,): 1}), 2)),
        ("wrong fixed-point descent", lambda: require(history(1, 1)[1], "expected rejection")),
    ):
        try:
            action()
        except (ValueError, AssertionError):
            negative_controls.append(label)
        else:
            raise AssertionError(f"negative control unexpectedly accepted: {label}")
    profiles = []
    for power in (8, 12, 16, 18):
        n_starts = 1 << power
        depths = (power // 2 - 2, power // 2, power // 2 + 2)
        samples = {depth: Counter() for depth in depths}
        for j in range(n_starts):
            word, _ = history(2 * j + 1, max(depths))
            for depth in depths:
                samples[depth][word[:depth]] += 1
        counters["profile_starting_integers"] += n_starts
        for depth in depths:
            tv = total_variation(samples[depth], n_starts)
            envelopes = [bounds(n_starts, depth, cap) for cap in range(2 * power + 1)]
            lo = max(support_lower(n_starts, depth), max(v[0] for v in envelopes))
            hi = min(tail(depth, power), min(v[1] for v in envelopes))
            require(lo <= tv <= hi, "profile envelope failed")
            tail_overlap = sum((F(1, 1 << sum(w)) for w in samples[depth] if sum(w) > power), F(0))
            require(tv == tail(depth, power) - tail_overlap, "exact dyadic TV formula failed")
            profiles.append({"N": n_starts, "m": depth, "support": len(samples[depth]),
                             "tv": fraction_record(tv), "lower": fraction_record(lo), "upper": fraction_record(hi)})
    certificate = descent_certificate(4096, 5, 16)
    direct = sum(history(2 * j + 1, 5)[1] for j in range(4096))
    require(certificate["lower"] <= direct <= certificate["upper"], "displayed certificate failed")
    return {"status": "pass", "arithmetic": "exact integers and Fraction; decimals are display only",
            "tv_convention": "half-L1 / supremum over events", "checks": dict(sorted(counters.items())),
            "negative_controls_rejected": negative_controls, "profiles": profiles,
            "descent_example": {"N": 4096, "m": 5, "H": 16, **certificate, "direct_count": direct},
            "scope": "Finite checks only; no numerical zeta, Lean, Gaussian-limit numerical certification, or Collatz convergence claim."}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
