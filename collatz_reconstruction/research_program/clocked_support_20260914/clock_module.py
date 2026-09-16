#!/usr/bin/env python3
"""Original two-clock path weights, polynomial boundary and exact cycle maps.

The source convention is the workbench companion's u**m*v**(A-m).
Sparse zero coefficients do not remove any declared source label.
All computation is over Z[u,v], except explicit Fraction-valued evaluations.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction
from typing import Callable, Iterable

Poly = dict[tuple[int, int], int]
Chain = dict[tuple[int, int, int], int]  # (original vertex/edge label, u degree, v degree)
Step = Callable[[int], tuple[int, int]]


def need(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def positive_word(word: Iterable[int]) -> tuple[int, ...]:
    w = tuple(word)
    need(bool(w) and all(type(a) is int and a >= 1 for a in w),
         'a nonempty original positive-exponent word is required')
    return w


def add(*polys):
    result = Counter()
    for p in polys:
        result.update(p)
    return {k: v for k, v in sorted(result.items()) if v}


def scale(p, k: int):
    return {j: k*v for j, v in p.items() if k*v}


def monomial(u: int = 0, v: int = 0, coefficient: int = 1) -> Poly:
    need(type(u) is int and type(v) is int and u >= 0 and v >= 0,
         'polynomial clock degrees must be nonnegative integers')
    need(type(coefficient) is int, 'integral coefficient required')
    return {(u, v): coefficient} if coefficient else {}


def mul(p: Poly, q: Poly) -> Poly:
    out = Counter()
    for (i, j), a in p.items():
        for (k, l), b in q.items():
            out[i+k, j+l] += a*b
    return {key: value for key, value in sorted(out.items()) if value}


def shift(p, u: int = 0, v: int = 0):
    need(u >= 0 and v >= 0, 'negative clock shift')
    return {(*key[:-2], key[-2]+u, key[-1]+v): c for key, c in p.items()}


def evaluate(p: Poly, u=1, v=1) -> Fraction:
    u, v = Fraction(u), Fraction(v)
    return sum((c*u**i*v**j for (i, j), c in p.items()), Fraction())


def record_poly(p: Poly) -> list[list[int]]:
    return [[i, j, c] for (i, j), c in sorted(p.items())]


def boundary(chain: Chain, successor: Step) -> Chain:
    out = Counter()
    for (n, i, j), c in chain.items():
        need(n != 1, 'the base loop is removed only by the specified relative quotient')
        y, a = successor(n)
        need(type(a) is int and a >= 1, 'positive actual exponent required')
        out[n, i, j] += c
        if y != 1:
            out[y, i+1, j+a-1] -= c
    return {key: c for key, c in sorted(out.items()) if c}


def original_step(n: int, forcing: int = 1) -> tuple[int, int]:
    need(type(n) is int and n > 0 and n % 2 == 1, 'positive odd source required')
    need(type(forcing) is int and forcing in (1, -1), 'forcing +1 or explicitly labelled -1 control required')
    value = 3*n+forcing
    a = (value & -value).bit_length()-1
    return value >> a, a


def path_column(n: int, returns: int, successor: Step = original_step) -> dict:
    need(type(returns) is int and returns >= 0, 'nonnegative finite path length required')
    start, A, values, exponents, coefficients = n, 0, [], [], {}
    for i in range(returns):
        need(n != 1, 'a relative path stops on first reaching the basepoint')
        values.append(n)
        coefficients[n, i, A-i] = 1
        n, a = successor(n)
        exponents.append(a)
        A += a
    expected = {} if start == 1 else {(start, 0, 0): 1}
    if n != 1:
        expected = add(expected, {(n, returns, A-returns): -1})
    need(boundary(coefficients, successor) == expected, 'clocked path boundary failed')
    return {'source': start, 'terminal': n, 'returns': returns, 'exponent_sum': A,
            'word': tuple(exponents), 'values': tuple(values), 'chain': coefficients,
            'terminal_weight': (returns, A-returns),
            'declared_edge_labels': tuple(sorted(set(values)))}


def ordinary(chain: Chain) -> dict[int, int]:
    out = Counter()
    for (n, i, j), c in chain.items():
        out[n] += c
    return {n: c for n, c in sorted(out.items()) if c}


def marked_word(word: Iterable[int]) -> dict:
    w = positive_word(word)
    b, numerator = 0, {}
    for i, a in enumerate(w):
        numerator[i, b] = 1
        b += a-1
    return {'word': w, 'weight': (len(w), b), 'forcing_polynomial': numerator,
            'annihilator': add(monomial(), monomial(len(w), b, -1))}


def recover_word(weight: tuple[int, int], forcing_polynomial: Poly) -> tuple[int, ...]:
    need(isinstance(weight, tuple) and len(weight) == 2, 'two exact clock degrees required')
    m, total = weight
    need(type(m) is int and m >= 1 and type(total) is int and total >= 0,
         'invalid total clock data')
    need(len(forcing_polynomial) == m, 'one forcing monomial per original position required')
    by_position = {}
    for (i, j), coefficient in forcing_polynomial.items():
        need(type(i) is int and type(j) is int and 0 <= i < m and j >= 0,
             'invalid forcing monomial degree')
        need(coefficient == 1 and i not in by_position, 'forcing coefficients or positions changed')
        by_position[i] = j
    heights = [by_position[i] for i in range(m)] + [total]
    need(heights[0] == 0 and all(a <= b for a, b in zip(heights, heights[1:])),
         'forcing polynomial is outside the positive-word image')
    result = tuple(1+heights[i+1]-heights[i] for i in range(m))
    need(marked_word(result)['forcing_polynomial'] == forcing_polynomial,
         'word reconstruction identity failed')
    return result


def cycle_d(word: tuple[int, ...], vector: list[Poly]) -> list[Poly]:
    w = positive_word(word)
    need(len(vector) == len(w), 'cycle source dimension mismatch')
    return [add(vector[i], scale(shift(vector[(i+1) % len(w)], 1, a-1), -1))
            for i, a in enumerate(w)]


def phi_one(word: tuple[int, ...], vector: list[Poly]) -> Poly:
    need(len(vector) == len(word), 'cycle target dimension mismatch')
    out, b = {}, 0
    for i, a in enumerate(word):
        out = add(out, shift(vector[i], i, b))
        b += a-1
    return out


def psi_zero(word: tuple[int, ...], scalar: Poly) -> list[Poly]:
    w = positive_word(word)
    return [dict(scalar)] + [shift(scalar, len(w)-i, sum(w[i:])-(len(w)-i))
                            for i in range(1, len(w))]


def psi_one(word: tuple[int, ...], scalar: Poly) -> list[Poly]:
    return [dict(scalar)] + [{} for _ in word[1:]]


def homotopy(word: tuple[int, ...], vector: list[Poly]) -> list[Poly]:
    w = positive_word(word)
    need(len(vector) == len(w), 'homotopy source dimension mismatch')
    out = [{} for _ in w]
    for i in range(1, len(w)):
        B = 0
        for j in range(i, len(w)):
            out[i] = add(out[i], shift(vector[j], j-i, B))
            B += w[j]-1
    return out


def vector_add(a, b, b_coefficient=1):
    need(len(a) == len(b), 'polynomial vector dimension mismatch')
    return [add(x, scale(y, b_coefficient)) for x, y in zip(a, b)]


def affine_packet(word: tuple[int, ...]) -> tuple[int, int, int, int]:
    L, U, C = 1, 1, 0
    for a in positive_word(word):
        L, U, C = 3*L, U*(1 << a), 3*C+U
    return L, U, C, U-L


class ClockedRetraction:
    """Lift a retained actual path retraction; do not change its root choice.

    The deterministic source and the original edge multiplicities reconstruct
    chronological order. The original record is checked before weighting it.
    """
    def __init__(self, predecessor, successor: Step | None = None):
        self.predecessor = predecessor
        self.successor = successor or (lambda n: original_step(n, predecessor.c))
        self.cache = {}

    def resolve(self, n: int) -> dict:
        if n not in self.cache:
            root, old_chain = self.predecessor.resolve(n)
            need(all(type(c) is int and c > 0 for c in old_chain.values()),
                 'retained path needs positive original traversal multiplicities')
            col = path_column(n, sum(old_chain.values()), self.successor)
            need(col['terminal'] == root and ordinary(col['chain']) == old_chain,
                 'chronological lift does not recover the retained path')
            self.cache[n] = col
        return self.cache[n]

    def h(self, vertices: Chain) -> Chain:
        return add(*(scale(shift(self.resolve(n)['chain'], i, j), c)
                     for (n, i, j), c in vertices.items()))

    def q(self, vertices: Chain) -> Chain:
        pieces = []
        for (n, i, j), c in vertices.items():
            col = self.resolve(n)
            root = col['terminal']
            if root != 1:
                a, b = col['terminal_weight']
                pieces.append({(root, i+a, j+b): c})
        return add(*pieces)

    def f(self, edges: Chain) -> Chain:
        return add(edges, scale(self.h(boundary(edges, self.successor)), -1))
