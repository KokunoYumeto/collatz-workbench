#!/usr/bin/env python3
"""Exact finite representatives for the Collatz completion-defect construction.

Coordinates are (u degree, v degree, original vertex); coefficients are integers.
Polynomial zero amplitudes are combined, but the declared source carrier and
original transition records are kept separately. No finite cutoff reports an
infinite Collatz orbit. The two control operators are explicitly named.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
from fractions import Fraction
from math import gcd
from typing import Iterable

Poly = dict[tuple[int, int, int], int]
MODES = ('collatz_plus', 'collatz_minus_control', 'ray_control')


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def transition(n: int, mode: str = 'collatz_plus') -> tuple[int, int]:
    require(mode in MODES, 'unknown operator')
    require(type(n) is int, 'integer vertex required')
    if mode == 'ray_control':
        require(n >= 2, 'ray vertices start at 2')
        return n + 1, 1
    require(n > 0 and n % 2 == 1, 'positive odd vertex required')
    value = 3*n + (1 if mode == 'collatz_plus' else -1)
    a = (value & -value).bit_length() - 1
    return value >> a, a


def combine(items: Iterable[tuple[tuple[int, int, int], int]]) -> Poly:
    out: dict[tuple[int, int, int], int] = defaultdict(int)
    for key, c in items:
        require(len(key) == 3 and all(type(t) is int for t in key), 'invalid coordinate')
        require(key[0] >= 0 and key[1] >= 0 and key[2] >= 2, 'invalid degree or relative vertex')
        require(type(c) is int, 'integer coefficient required')
        out[key] += c
    return {k: c for k, c in sorted(out.items()) if c}


def add(a: Poly, b: Poly, factor: int = 1) -> Poly:
    return combine(list(a.items()) + [(k, factor*c) for k, c in b.items()])


def shift(p: Poly, du: int = 0, dv: int = 0, factor: int = 1) -> Poly:
    return combine([((i+du, j+dv, n), factor*c) for (i, j, n), c in p.items()])


def S(p: Poly, mode: str = 'collatz_plus') -> Poly:
    require(mode in MODES, 'unknown operator')
    out = []
    for (i, j, n), c in p.items():
        y, a = transition(n, mode)
        if y != 1:
            out.append(((i, j+a-1, y), c))
    return combine(out)


def differential(p: Poly, mode: str = 'collatz_plus') -> Poly:
    return add(p, shift(S(p, mode), du=1), -1)


def rows(p: Poly) -> list[list[int]]:
    return [[i, j, n, c] for (i, j, n), c in sorted(p.items())]


def from_rows(data: list[list[int]]) -> Poly:
    require(isinstance(data, list), 'polynomial rows must be a list')
    items = []
    for row in data:
        require(isinstance(row, list) and len(row) == 4, 'row must be [u,v,vertex,coefficient]')
        items.append((tuple(row[:3]), row[3]))
    return combine(items)


def truncation(p: Poly, cap: int) -> Poly:
    return {key: c for key, c in p.items() if key[0] <= cap}


def trajectory(n: int, returns: int, mode: str = 'collatz_plus') -> dict:
    require(type(returns) is int and returns >= 0, 'nonnegative integer return count required')
    transition(n, mode)
    require(n != 1, 'basepoint has no relative source basis column')
    x, power, edges = n, 0, []
    for _ in range(returns):
        if x == 1:
            break
        y, a = transition(x, mode)
        edges.append([x, a, y])
        power += a-1
        x = y
    return {'source': n, 'returns_requested': returns, 'operator': mode,
            'original_edges': edges, 'endpoint': x, 'v_power': power,
            'absorbed_at_basepoint': x == 1,
            'source_carrier_retained': True}


def iterate(p: Poly, returns: int, mode: str = 'collatz_plus') -> Poly:
    require(type(returns) is int and returns >= 0, 'nonnegative integer return count required')
    out = p
    for _ in range(returns):
        out = S(out, mode)
    return out


def kernel_presentation(sources: Iterable[int], returns: int,
                        mode: str = 'collatz_plus') -> dict:
    """A complete free basis for ker(S^returns) on the declared finite source span.

    This map's codomain retains every original endpoint, including endpoints
    outside the source set. Images at 1 are zero in the specified relative
    module, not omitted source labels.
    """
    require(mode in MODES, 'unknown operator')
    require(type(returns) is int and returns >= 0, 'nonnegative return count required')
    src = sorted(set(sources))
    paths = [trajectory(n, returns, mode) for n in src]
    by_target: dict[int, list[dict]] = defaultdict(list)
    killed, basis, lifts = [], [], []
    for path in paths:
        n, y = path['source'], path['endpoint']
        if y == 1:
            killed.append(n)
            basis.append({'pivot_source': n, 'kind': 'arrives_at_basepoint',
                          'vector': [[0, 0, n, 1]]})
        else:
            by_target[y].append(path)
    for y, fibre in sorted(by_target.items()):
        pivot = min(fibre, key=lambda p: (p['v_power'], p['source']))
        n0, b0 = pivot['source'], pivot['v_power']
        lifts.append({'endpoint': y, 'selected_source': n0, 'v_power': b0,
                      'original_image_generator': [[0, b0, y, 1]]})
        for path in sorted(fibre, key=lambda p: p['source']):
            n = path['source']
            if n != n0:
                basis.append({'pivot_source': n, 'kind': 'synchronized_merge',
                              'vector': rows(add({(0, 0, n): 1},
                                                {(0, path['v_power']-b0, n0): 1}, -1))})
    return {'operator': mode, 'returns': returns, 'declared_sources': src,
            'ambient_support_label': {'basepoint': 1, 'forward_closure_generators': src},
            'paths': paths, 'arrivals_at_basepoint': killed,
            'kernel_basis': basis, 'kernel_rank': len(basis),
            'image_generators': lifts, 'image_rank': len(lifts),
            'rank_identity': len(basis)+len(lifts) == len(src)}


def decompose(vector: Poly, presentation: dict) -> tuple[Poly, Poly]:
    """Return its kernel component and the original selected-source complement."""
    require(all(i == 0 for i, _, _ in vector), 'use a vector over Z[v], not u-polynomials')
    require({n for _, _, n in vector} <= set(presentation['declared_sources']),
            'vector outside declared source carrier')
    kernel, residual = {}, dict(vector)
    # Each relation has one unique nonselected pivot with coefficient +1.
    for entry in presentation['kernel_basis']:
        n = entry['pivot_source']
        relation = from_rows(entry['vector'])
        for (i, j, v), c in list(residual.items()):
            if v == n:
                term = shift(relation, dv=j, factor=c)
                kernel = add(kernel, term)
                residual = add(residual, term, -1)
    return kernel, residual


def terminal_vector(q: Poly, mode: str = 'collatz_plus') -> tuple[int, Poly, Poly]:
    """q = d(prefix) + u^degree * terminal, on the original source coordinates."""
    d = max((i for i, _, _ in q), default=0)
    b, prefix = {}, {}
    for j in range(d+1):
        qj = {(0, e, n): c for (i, e, n), c in q.items() if i == j}
        b = add(qj, S(b, mode))
        if j < d:
            prefix = add(prefix, shift(b, du=j))
    require(add(differential(prefix, mode), shift(b, du=d)) == q,
            'original terminal comparison failed')
    return d, b, prefix


def completion_certificate(q: Poly, cap: int, sources: Iterable[int],
                           mode: str = 'collatz_plus') -> dict:
    """Finite inverse jet AND its exact original residual. No convergence guess."""
    q = combine(q.items())
    d = max((i for i, _, _ in q), default=0)
    require(type(cap) is int and cap >= d, 'cap must include the full forcing polynomial')
    src = sorted(set(sources))
    for n in src:
        transition(n, mode)
        require(n != 1, 'relative source carrier excludes the basepoint generator')
    require({n for _, _, n in q} <= set(src), 'forcing outside declared source carrier')
    b, primitive = {}, {}
    for j in range(cap+1):
        qj = {(0, e, n): c for (i, e, n), c in q.items() if i == j}
        b = add(qj, S(b, mode))
        primitive = add(primitive, shift(b, du=j))
    residual = shift(S(b, mode), du=cap+1)
    require(add(differential(primitive, mode), residual) == q,
            'truncated primitive/residual boundary identity failed')
    degree, terminal, prefix = terminal_vector(q, mode)
    return {'operator': mode, 'cap': cap, 'declared_sources': src,
            'ambient_support_label': {'basepoint': 1, 'forward_closure_generators': src},
            'forcing': rows(q), 'primitive_jet': rows(primitive),
            'original_residual': rows(residual),
            'status': 'finite_boundary_certificate' if not residual else 'unresolved_at_cutoff',
            'terminal_degree': degree, 'terminal_vector': rows(terminal),
            'terminal_prefix': rows(prefix),
            'source_paths': [trajectory(n, cap+1, mode) for n in src],
            'coefficient_zero_does_not_delete_carrier': True}


def validate_completion(cert: dict) -> None:
    require(isinstance(cert, dict), 'certificate must be an object')
    require({'forcing','cap','declared_sources','operator'} <= set(cert), 'missing input data')
    expected = completion_certificate(from_rows(cert['forcing']), cert['cap'],
                                      cert['declared_sources'], cert['operator'])
    require(expected == cert, 'certificate differs from exact original reconstruction')


def validate_kernel(cert: dict) -> None:
    require(isinstance(cert, dict), 'certificate must be an object')
    require({'declared_sources','returns','operator'} <= set(cert), 'missing kernel input data')
    expected = kernel_presentation(cert['declared_sources'], cert['returns'], cert['operator'])
    require(expected == cert, 'kernel certificate differs from exact reconstruction')


def arithmetic_return(word: Iterable[int]) -> dict:
    """Return the rational cyclic primitive through the specified coefficient map.

    This evaluates only R[(1-W)^-1], not arbitrary completed series.
    The original word, numerator, integral mark and prime-power data remain.
    """
    word = tuple(word)
    require(bool(word) and all(type(a) is int and a >= 1 for a in word),
            'nonempty positive exponent word required')
    A, C, L, monomials = 0, 0, 1, []
    for j, a in enumerate(word):
        monomials.append([j, A-j, 1])
        C, L, A = 3*C+(1 << A), 3*L, A+a
    U, m = 1 << A, len(word)
    D = U-L
    evaluated_N = sum((Fraction(2,3)**j * 2**e for j,e,_ in monomials), Fraction(0))
    evaluated_a = 1-Fraction(2,3)**m * 2**(A-m)
    require(evaluated_N == Fraction(C,3**(m-1)), 'forcing coefficient map failed')
    require(evaluated_a == Fraction(-D,3**m), 'differential coefficient map failed')
    returned = (-evaluated_N/evaluated_a)/3
    require(returned == Fraction(C,D), 'original primitive return failed')
    return {'word':list(word), 'm':m, 'A':A, 'C':C, 'D':D,
            'W_exponents':[m,A-m], 'N_monomials':monomials,
            'alpha_N':str(evaluated_N), 'alpha_1_minus_W':str(evaluated_a),
            'degree_zero_comparison_factor':'1/3',
            'degree_one_comparison_factor':-3**(m-1),
            'returned_primitive':str(returned),
            'integral_mark':C % abs(D),
            'integral_mark_order':abs(D)//gcd(abs(D),C),
            'full_word_retained':True, 'arbitrary_formal_series_evaluated':False}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('source'); p.add_argument('source', type=int)
    p.add_argument('--cap', type=int, default=32)
    p.add_argument('--operator', choices=MODES, default='collatz_plus')
    p = sub.add_parser('kernel'); p.add_argument('sources', nargs='+', type=int)
    p.add_argument('--returns', type=int, default=1)
    p.add_argument('--operator', choices=MODES, default='collatz_plus')
    args = parser.parse_args()
    try:
        if args.command == 'source':
            cert = completion_certificate({(0, 0, args.source): 1}, args.cap,
                                          [args.source], args.operator)
        else:
            cert = kernel_presentation(args.sources, args.returns, args.operator)
        print(json.dumps(cert, indent=2, sort_keys=True))
    except ValueError as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    main()
