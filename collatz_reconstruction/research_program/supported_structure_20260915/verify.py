#!/usr/bin/env python3
"""Finite exact regression for the structural Split-Zero Collatz note.

No third-party dependencies. All comparisons remain active under python -O.
Formal circles and synthetic rays are explicitly not positive Collatz orbits.
A finite unresolved endpoint is never reported as an infinite survivor.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
from typing import Callable, Iterable

Monomial = tuple[int, int]
Poly = dict[Monomial, int]
Vector = dict[tuple[int, int, int], int]


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def clean(d: dict) -> dict:
    return {k: c for k, c in d.items() if c}


def plus(a: dict, b: dict, sign: int = 1) -> dict:
    out = dict(a)
    for k, c in b.items():
        out[k] = out.get(k, 0) + sign*c
    return clean(out)


def pmul(a: Poly, b: Poly) -> Poly:
    out: Poly = {}
    for (i, j), c in a.items():
        for (k, l), e in b.items():
            key = (i+k, j+l)
            out[key] = out.get(key, 0) + c*e
    return clean(out)


def times(p: Poly, x: Vector) -> Vector:
    out: Vector = {}
    for (i, j), c in p.items():
        for (n, k, l), e in x.items():
            key = (n, i+k, j+l)
            out[key] = out.get(key, 0) + c*e
    return clean(out)


def basis(n: int, coefficient: int = 1) -> Vector:
    return {(n, 0, 0): coefficient} if coefficient else {}


def v2(n: int) -> int:
    require(type(n) is int and n > 0, 'valuation requires a positive integer')
    return (n & -n).bit_length()-1


def step(n: int) -> tuple[int, int]:
    require(type(n) is int and n > 0 and n % 2 == 1, 'source must be a positive odd integer')
    b = 3*n+1
    a = v2(b)
    return b >> a, a


def independent_step(n: int) -> tuple[int, int]:
    require(type(n) is int and n > 0 and n % 2 == 1, 'independent source invalid')
    x, a = 3*n+1, 0
    while x % 2 == 0:
        x //= 2
        a += 1
    return x, a


def block(n: int) -> dict:
    step(n)
    r = v2(n+1)-1
    t = (n+1) >> (r+1)
    numerator = 3**(r+1)*t-1
    b = 1+v2(numerator)
    y = numerator >> (b-1)
    values = [3**j*2**(r+1-j)*t-1 for j in range(r+1)]
    return {'source': n, 'r': r, 't': t, 'last_exponent': b,
            'word': [1]*r+[b], 'path_sources': values, 'target': y,
            'clock': [r+1, b-1],
            'descent_left': (2**(b+r)-3**(r+1))*t,
            'descent_right': 2**(b-1)-1}


def original_boundary(chain: Vector, relative: bool = True) -> Vector:
    out: Vector = {}
    for (n, i, j), c in chain.items():
        y, a = step(n)
        if relative and n == 1:
            continue
        out = plus(out, {(n, i, j): c})
        if not relative or y != 1:
            out = plus(out, {(y, i+1, j+a-1): -c})
    return out


def original_path(n: int, word: Iterable[int], relative: bool = True) -> tuple[Vector, int, Monomial]:
    out: Vector = {}
    x, i, j = n, 0, 0
    for a in word:
        y, actual = step(x)
        require(type(a) is int and a == actual, 'word does not match the actual original valuation')
        if not relative or x != 1:
            out = plus(out, {(x, i, j): 1})
        x, i, j = y, i+1, j+a-1
    return out, x, (i, j)


def transport(q: Vector, N: int) -> Vector:
    require(type(N) is int and N >= 0, 'nonnegative return count required')
    out: Vector = {}
    for (n, i, j), c in q.items():
        step(n)
        x, e = n, j
        for _ in range(N):
            if x == 1:
                break
            x, a = step(x)
            e += a-1
        if x != 1:
            out = plus(out, {(x, i, e): c})
    return out


def packet(word: Iterable[int]) -> tuple[int, int, int]:
    A, L, C = 0, 1, 0
    for a in word:
        require(type(a) is int and a >= 1, 'positive exponent required')
        C, L, A = 3*C+2**A, 3*L, A+a
    return A, L, C


def word_mark(word: Iterable[int]) -> tuple[Monomial, Poly]:
    w = tuple(word)
    require(bool(w), 'nonempty word required')
    A, N = 0, {}
    for j, a in enumerate(w):
        require(type(a) is int and a >= 1, 'positive exponent required')
        N[(j, A-j)] = 1
        A += a
    return (len(w), A-len(w)), N


def word_inverse(W: Monomial, N: Poly) -> tuple[int, ...]:
    m, e = W
    require(type(m) is int and m >= 1 and type(e) is int and e >= 0, 'invalid terminal clocks')
    require(len(N) == m, 'forcing mark lacks one original position')
    b: list[int] = []
    for j in range(m):
        entries = [(v, c) for (u, v), c in N.items() if u == j]
        require(len(entries) == 1 and entries[0][1] == 1, 'forcing coefficient must be one monomial with coefficient one')
        b.append(entries[0][0])
    b.append(e)
    require(b[0] == 0 and all(type(x) is int and x >= 0 for x in b), 'invalid initial mark')
    require(all(x <= y for x, y in zip(b, b[1:])), 'nonmonotone prefix clocks')
    return tuple(1+b[j+1]-b[j] for j in range(m))


def evaluate(p: Poly) -> Fraction:
    return sum((Fraction(c)*Fraction(2, 3)**i*2**j for (i, j), c in p.items()), Fraction(0))


def compositions(total: int) -> Iterable[tuple[int, ...]]:
    if total == 0:
        yield ()
    else:
        for first in range(1, total+1):
            for tail in compositions(total-first):
                yield (first,)+tail


def circle_maps(word: tuple[int, ...]):
    """Original finite position-circle maps; no integer realization is assumed."""
    m = len(word)
    prefix: list[Monomial] = [(0, 0)]
    for a in word:
        i, j = prefix[-1]
        prefix.append((i+1, j+a-1))
    W = prefix[-1]
    annihilator = plus({(0, 0): 1}, {W: 1}, -1)
    period: Vector = {(i, *prefix[i]): 1 for i in range(m)}

    def d(x: Vector) -> Vector:
        out: Vector = {}
        for (n, i, j), c in x.items():
            require(0 <= n < m, 'circle position outside the original word')
            out = plus(out, {(n, i, j): c})
            out = plus(out, {((n+1) % m, i+1, j+word[n]-1): -c})
        return out

    def phi0(x: Vector) -> Poly:
        return clean({(i, j): c for (n, i, j), c in x.items() if n == 0})

    def phi1(x: Vector) -> Poly:
        out: Poly = {}
        for (n, i, j), c in x.items():
            a, b = (0, 0) if n == 0 else (W[0]-prefix[n][0], W[1]-prefix[n][1])
            out = plus(out, {(i+a, j+b): c})
        return out

    def psi0(p: Poly) -> Vector:
        return times(p, period)

    def psi1(p: Poly) -> Vector:
        return times(p, basis(0))

    def H(x: Vector) -> Vector:
        out: Vector = {}
        for (n, i, j), c in x.items():
            if n == 0:
                continue
            for k in range(n, m):
                key = (k, i+prefix[k][0]-prefix[n][0], j+prefix[k][1]-prefix[n][1])
                out = plus(out, {key: c})
        return out

    return W, annihilator, period, d, phi0, phi1, psi0, psi1, H


def coset_coordinates(a: int, b: int, m: int, e: int) -> tuple[int, int]:
    require(m >= 1 and e >= 0, 'invalid cycle clocks')
    q, r = divmod(a, m)
    return r, b-q*e


def run() -> dict:
    counts: Counter[str] = Counter()

    def check(condition: bool, group: str) -> None:
        counts[group] += 1
        require(condition, 'failed: '+group)

    examples = []
    for n in range(1, 4096, 2):
        z = block(n)
        r, t, b, y = z['r'], z['t'], z['last_exponent'], z['target']
        check(t > 0 and t % 2 == 1 and 2**(r+1)*t-1 == n, 'original_parameter_inverse')
        check(b >= 2 and z['clock'] == [len(z['word']), sum(z['word'])-len(z['word'])], 'original_two_clocks')
        x = n
        for i, a in enumerate(z['word']):
            check(x == z['path_sources'][i], 'original_intermediate_states')
            x, actual = independent_step(x)
            check(a == actual, 'independent_original_valuations')
        check(x == y, 'original_block_endpoint')
        check((y < n) == (z['descent_left'] > z['descent_right']), 'affine_descent_equivalence')
        chain, end, W = original_path(n, z['word'])
        rhs = {} if n == 1 else basis(n)
        if y != 1:
            rhs = plus(rhs, times({W: 1}, basis(y)), -1)
        check(original_boundary(chain) == rhs, 'original_block_boundary')
        Jv = {} if y == 1 else {(y, r+1, b-2): 1}
        identity = plus({} if n == 1 else basis(n), times({(0, 1): 1}, Jv), -1)
        check(original_boundary(chain) == identity, 'v_inverse_original_primitive')
        if n in (1, 3, 5, 7, 13, 27, 31, 247):
            examples.append(z)
    for r in range(65):
        for t in (1, 3, 7, 19):
            z = block(2**(r+1)*t-1)
            check((z['r'], z['t']) == (r, t), 'large_parameter_round_trip')
    for N in (1, 2, 8, 32, 128, 512):
        n = 2**(N+1)-1
        x = n
        for j in range(N):
            x, a = independent_step(x)
            check(a == 1 and x == 3**(j+1)*2**(N-j)-1, 'nonuniform_original_family')
        check(x > 1, 'nonuniform_residual_nonzero')

    word_count = 0
    for total in range(1, 9):
        for word in compositions(total):
            word_count += 1
            W, N = word_mark(word)
            check(word_inverse(W, N) == word, 'ordered_word_mark_inverse')
            A, L, C = packet(word)
            check(evaluate(N) == Fraction(C, 3**(len(word)-1)), 'original_forcing_specialization')
            check(evaluate({(0, 0): 1, W: -1}) == Fraction(-(2**A-L), L), 'original_determinant_specialization')
            W, ann, period, d, f0, f1, s0, s1, H = circle_maps(word)
            check(d(period) == s1(ann), 'full_circle_period_boundary')
            check(f0(s0({(0, 0): 1})) == {(0, 0): 1}, 'circle_source_section')
            check(f1(s1({(0, 0): 1})) == {(0, 0): 1}, 'circle_target_section')
            for j in range(len(word)):
                v = basis(j)
                check(f1(d(v)) == pmul(ann, f0(v)), 'circle_projection_chain_equation')
                check(d(H(v)) == plus(v, s1(f1(v)), -1), 'circle_target_homotopy')
                check(H(d(v)) == plus(v, s0(f0(v)), -1), 'circle_source_homotopy')
            for a, b in ((-13, 7), (0, 0), (16, -9)):
                for k in (-3, 0, 5):
                    check(coset_coordinates(a, b, *W) == coset_coordinates(a+k*W[0], b+k*W[1], *W),
                          'laurent_cycle_coset_inverse')
            if W[1] > 0:
                check(coset_coordinates(W[0], W[1], *W) == (0, 0), 'cycle_clock_inverses')
    check(word_count == 255, 'complete_finite_word_fixture_count')

    # A synthetic labelled ray with all exponent labels 2, not a Collatz orbit.
    for a in range(-12, 13):
        for b in range(-12, 13):
            j = max(0, -a, -b)
            check(a+j >= 0 and b+j >= 0, 'synthetic_ray_laurent_numerator')
            check((a+j-j, b+j-j) == (a, b), 'synthetic_ray_laurent_inverse')
            for later in (j, j+1, j+13):
                check((a+later-later, b+later-later) == (a, b), 'synthetic_ray_meeting_independence')

    sources = (3, 5, 7, 11, 13, 27)
    for N in range(10):
        endpoints = {}
        for n in sources:
            x = n
            for _ in range(N):
                if x == 1:
                    break
                x, _ = independent_step(x)
            endpoints[n] = x
        for coeff in product(range(3), repeat=len(sources)):
            q: Vector = {}
            for j, (n, c) in enumerate(zip(sources, coeff)):
                if c:
                    q[(n, 0, j % 3)] = c
            check((transport(q, N) == {}) == all(c == 0 or endpoints[n] == 1 for n, c in zip(sources, coeff)),
                  'positive_cone_absorption_equivalence')
    merger = {(3, 0, 2): 1, (13, 0, 0): -1}
    check(merger != {} and transport(merger, 1) == {}, 'signed_merger_supported_zero')
    check(transport(basis(3), 1) != {} and transport(basis(13), 1) != {}, 'merger_not_singleton_absorption')
    check(transport(basis(3), 2) == {} and transport(basis(13), 2) == {}, 'actual_later_absorption')

    # Original ordered-mark collision: no positive cycle is asserted for (1,3).
    W1, N1 = word_mark((1, 3))
    W2, N2 = word_mark((2, 2))
    check(W1 == W2 and N1 != N2, 'same_binomial_different_original_history')
    check(packet((1, 3))[2] == 5 and packet((2, 2))[2] == 7, 'same_determinant_different_integral_mark')

    # Genuine signed-forcing control: T_minus(n)=-T_plus(-n), not positive +1.
    control = []
    for n in (5, 7):
        b = 3*n-1
        a = v2(b)
        control.append((n, a, b >> a))
    check(control == [(5, 1, 7), (7, 2, 5)], 'signed_control_actual_cycle')
    check(word_mark((1, 2))[0] == (2, 1), 'signed_control_period_module')

    rejected = []
    def reject(label: str, fn: Callable[[], object]) -> None:
        try:
            fn()
        except (ValueError, TypeError):
            rejected.append(label)
        else:
            raise ValueError('false certificate accepted: '+label)
    reject('zero source', lambda: block(0))
    reject('even source', lambda: block(4))
    reject('negative source', lambda: block(-1))
    reject('boolean source', lambda: block(True))
    reject('zero exponent', lambda: word_mark((1, 0)))
    reject('erased forcing position', lambda: word_inverse((2, 2), {(0, 0): 1}))
    reject('nonmonotone clock mark', lambda: word_inverse((2, 0), {(0, 0): 1, (1, 1): 1}))
    reject('wrong forcing coefficient', lambda: word_inverse((2, 2), {(0, 0): 2, (1, 1): 1}))
    reject('false original valuation', lambda: original_path(3, (2,)))
    reject('negative kernel time', lambda: transport(basis(3), -1))
    reject('merger promoted to one-step arrival', lambda: require(transport(basis(3), 1) == {}, 'not absorbed'))
    return {
        'status': 'PASS', 'scope': 'finite regression; no global Collatz endpoint is asserted',
        'source_commit': '6b3ded8880946b2c3140a9d79f1aa1d658d36b8c',
        'counts': dict(sorted(counts.items())), 'total_exact_checks': sum(counts.values()),
        'original_block_sources': 2048, 'formal_circle_words': word_count,
        'formal_circle_warning': 'labelled position circles, not asserted positive integer cycles',
        'synthetic_ray_warning': 'all-2 forward test ray, not an original positive Collatz orbit',
        'block_examples': examples, 'signed_control': control,
        'rejected_inputs': rejected,
        'global_targets_unproved_here': ['periodic torsion exhaustion', 'generic ray-module exhaustion',
                                        'positive integer survivor-source exhaustion']
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    result = run()
    data = (json.dumps(result, sort_keys=True, indent=2)+'\n').encode('utf-8')
    if args.check:
        require(args.check.read_bytes() == data, 'recorded result bytes differ')
    if args.output:
        args.output.write_bytes(data)
    if args.output or args.check:
        print(json.dumps({'status': 'PASS', 'total_exact_checks': result['total_exact_checks'],
                          'recorded_bytes': len(data), 'check': bool(args.check)}, sort_keys=True))
    else:
        print(data.decode('utf-8'), end='')


if __name__ == '__main__':
    main()
