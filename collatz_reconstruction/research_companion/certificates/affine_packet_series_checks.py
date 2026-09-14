"""Exact finite checks for packet series; analytic proofs are in the TeX.

No third-party dependency; no files read or written. Finite checks do not
replace the all-length convergence and meromorphic-continuation proofs.
"""
from fractions import Fraction as Q
from math import comb
import json


def compositions(total, length):
    if length == 1:
        yield (total,)
        return
    for first in range(1, total - length + 2):
        for tail in compositions(total - first, length - 1):
            yield (first,) + tail


def numerator(word):
    value, budget = 0, 0
    for a in word:
        value = 3 * value + 2 ** budget
        budget += a
    return value


def rational_F(m, q):
    u, v = q / (1 - q), q / (2 - q)
    return sum((3 ** (m - 1 - k) * u ** k * v ** (m - k)
                for k in range(m)), Q(0))


def main():
    if not __debug__:
        raise SystemExit('Optimized Python is not accepted.')
    limit = 13
    offsets, fixed = {}, {}
    word_count = coefficient_count = tail_checks = 0
    for m in range(1, 7):
        for A in range(m, limit + 1):
            words = list(compositions(A, m))
            assert len(words) == comb(A - 1, m - 1)
            C = [numerator(p) for p in words]
            D = 2 ** A - 3 ** m
            S = sum((Q(c, 2 ** A) for c in C), Q(0))
            X = sum((Q(c, D) for c in C), Q(0))
            offsets[m, A], fixed[m, A] = S, X
            assert (2 ** A - 3 ** m) * X == 2 ** A * S
            if m == 1:
                assert S == Q(1, 2 ** A)
            else:
                assert S == sum((Q(3 * offsets[m - 1, A - a]
                                      + comb(A - a - 1, m - 2), 2 ** a)
                                 for a in range(1, A - m + 2)), Q(0))
            if m == 2:
                assert X == Q(2 ** A + 3 * A - 5, D)
            if A >= 2 * m:
                assert 0 < X <= 2 * ((Q(3, 2) ** m) - 1) * len(words)
                if m >= 2:
                    assert X >= Q(1, 2)
                # Exact remainder of the geometric coefficient expansion.
                for R in range(6):
                    ratio = Q(3 ** m, 2 ** A)
                    partial = S * sum((ratio ** r for r in range(R + 1)), Q(0))
                    assert X - partial == S * ratio ** (R + 1) / (1 - ratio)
            for p, c in zip(words, C):
                for y in (-7, 0, 1, 11):
                    z = D * y - c
                    y_next = Q(3 ** m * y + c, 2 ** A)
                    assert D * y_next - c == Q(3 ** m * z, 2 ** A)
                    tail_checks += 1
            word_count += len(words)
            coefficient_count += 1
    rational_checks = 0
    explicit_tail_constants = []
    for m in range(1, 7):
        L = 2 * m
        eta = Q(3 ** m, 2 ** L)
        B = 2 ** L * (Q(m, 3) - sum((offsets[m, A] * Q(1, 2) ** A
                                     for A in range(m, L)), Q(0)))
        assert 0 < eta < 1 and B > 0
        assert rational_F(m, Q(1, 2)) == Q(m, 3)
        explicit_tail_constants.append({'m': m, 'L': L, 'B': str(B), 'eta': str(eta)})
    for m in range(1, 9):
        for q in (Q(-1, 2), Q(1, 4), Q(1, 2), Q(3, 4), Q(3, 2), Q(3)):
            u, v = q / (1 - q), q / (2 - q)
            assert rational_F(m + 1, q) == v * (3 * rational_F(m, q) + u ** m)
            f, g = v, u
            for _ in range(m - 1):
                f, g = 3 * v * f + v * g, u * g
            assert f == rational_F(m, q)
            rational_checks += 1
    # This assertion is the exact local counterexample to the source line.
    wrong = Q(3 * 1 * 1 + 3 * 1 - 4 * 1, 4)
    assert wrong == Q(1, 2) and wrong != 0
    # The terms at q=3/4 in X_2(2q) already exceed (3/2)^A for A>=4.
    divergence_terms = []
    for A in range(4, 14):
        term = fixed[2, A] * Q(3, 2) ** A
        assert term > Q(3, 2) ** A
        divergence_terms.append({'A': A, 'term': str(term)})
    print(json.dumps({
        'status': 'PASS', 'words': word_count, 'packet_coefficients': coefficient_count,
        'tail_affine_equalities': tail_checks, 'rational_recurrence_checks': rational_checks,
        'source_tail_wrong_value': str(wrong), 'm2_dilated_divergence_terms': divergence_terms,
        'explicit_tail_constants': explicit_tail_constants,
        'proof_scope': 'finite exact algebra only; general analytic statements proved in chapter05',
        'Lean_launched': False,
    }, indent=2))


if __name__ == '__main__':
    main()
