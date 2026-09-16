#!/usr/bin/env python3
"""Entire last-exponent tails with a proved original-source descent inequality."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable
import residual_descent as rd


def noncontracting_prefix(word: Iterable[int]) -> bool:
    p = rd.cd.packet(word)
    A, L = 0, 1
    for a in p.word:
        A += a; L *= 3
        if 2**A > L:
            return False
    return True


@dataclass(frozen=True)
class DescentTail:
    prefix: tuple[int, ...]
    threshold: int
    prefix_source_anchor: int
    prefix_source_step: int
    prefix_target_anchor: int
    prefix_target_step: int
    source_anchor: int
    source_step: int
    parameter_residue: int
    parameter_modulus: int

    def word_for(self, n: int) -> tuple[int, ...] | None:
        rd.need(type(n) is int and n > 0 and n % 2 == 1, 'positive odd source required')
        v, rem = divmod(n-self.source_anchor, self.source_step)
        if rem or v < 0:
            return None
        t = self.parameter_residue+self.parameter_modulus*v
        x = self.prefix_target_anchor+self.prefix_target_step*t
        a = rd.cd.v2(3*x+1)
        rd.need(a >= self.threshold, 'tail valuation below its exact threshold')
        return self.prefix+(a,)

    def record(self) -> dict:
        return {'prefix': list(self.prefix), 'threshold': self.threshold,
                'prefix_source_anchor': self.prefix_source_anchor,
                'prefix_source_step': self.prefix_source_step,
                'prefix_target_anchor': self.prefix_target_anchor,
                'prefix_target_step': self.prefix_target_step,
                'source_anchor': self.source_anchor, 'source_step': self.source_step,
                'parameter_residue': self.parameter_residue,
                'parameter_modulus': self.parameter_modulus,
                'last_exponent_upper_bound': None, 'all_original_exponent_labels_retained': True}


def descent_tail(prefix: Iterable[int]) -> DescentTail:
    p = rd.cd.packet(prefix)
    rd.need(noncontracting_prefix(p.word), 'every prefix coefficient must be at least one')
    r = ((p.U-p.C)*pow(p.L, -1, 2*p.U)) % (2*p.U)
    u, rem = divmod(p.L*r+p.C, p.U)
    rd.need(not rem and r > 0 and r % 2 and u % 2, 'invalid prefix chart')
    B = 1
    while 2**B*r <= 3*u+1 or 2**B*p.U < 3*p.L:
        B += 1
    modulus = 2**(B-1)
    t0 = (-(3*u+1)//2*pow(3*p.L, -1, modulus)) % modulus
    return DescentTail(p.word, B, r, 2*p.U, u, 2*p.L,
                       r+2*p.U*t0, 2*p.U*modulus, t0, modulus)


def tails_from_cells(cells: Iterable[rd.DescentCell]) -> tuple[DescentTail, ...]:
    prefixes = {c.word[:-1] for c in cells if noncontracting_prefix(c.word[:-1])}
    return tuple(descent_tail(p) for p in sorted(prefixes, key=lambda w: (len(w), w)))


def split_prefix(prefix: Iterable[int]) -> dict:
    """Exact finite frontier plus an entire closed last-exponent tail.

    The finite children and the tail partition the *full* positive prefix
    cylinder. Crossing children retain both their descent interval and their
    finite no-descent source box. There is no exponent-overflow atom.
    """
    tail = descent_tail(prefix)
    children = []
    for a in range(1, tail.threshold):
        cell = rd.first_descent_cell(tail.prefix+(a,))
        row = {'exponent': a, 'cell': cell.record()}
        if cell.D <= 0:
            row['status'] = 'noncontracting prefix frontier'
        else:
            row['status'] = 'first crossing with retained finite exception box'
            row['exception_box'] = rd.coefficient_crossing_box(cell.word, 1)
        children.append(row)
    return {'prefix': list(tail.prefix), 'finite_children': children,
            'entire_last_exponent_tail': tail.record(), 'exponent_overflow': False}


if __name__ == '__main__':
    import argparse
    import json
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('prefix', type=int, nargs='*')
    args = parser.parse_args()
    print(json.dumps(split_prefix(args.prefix), indent=2, sort_keys=True))
