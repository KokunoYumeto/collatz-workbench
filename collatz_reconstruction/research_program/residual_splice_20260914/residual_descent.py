#!/usr/bin/env python3
"""Exact first-descent cylinders, root-level splicing, and integral block maps.

Original forcing is +1 throughout. No density assumption or tail truncation
is used to accept a source. Imported files remain byte-for-byte unchanged.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from typing import Iterable

HERE = Path(__file__).resolve().parent
NAME = '_collatz_cycle_predecessor_for_residual_splice'
if NAME not in sys.modules:
    source = HERE.parent/'cycle_relative_cohomology_20260914'/'cycle_detector.py'
    spec = importlib.util.spec_from_file_location(NAME, source)
    if spec is None or spec.loader is None:
        raise RuntimeError('The preserved cycle continuation is required')
    module = importlib.util.module_from_spec(spec)
    sys.modules[NAME] = module
    spec.loader.exec_module(module)
cd = sys.modules[NAME]


def need(value: bool, message: str) -> None:
    if not value:
        raise ValueError(message)


def clean(values: Counter | dict[int, int]) -> dict[int, int]:
    return {n: k for n, k in sorted(values.items()) if k}


def add(*chains: dict[int, int]) -> dict[int, int]:
    total: Counter[int] = Counter()
    for chain in chains:
        total.update(chain)
    return clean(total)


@dataclass(frozen=True)
class DescentCell:
    word: tuple[int, ...]
    source_anchor: int
    source_step: int
    target_anchor: int
    target_step: int
    lower: int
    upper: int | None
    A: int
    L: int
    C: int
    D: int

    @property
    def occupied(self) -> bool:
        return self.upper is None or self.lower <= self.upper

    def parameter(self, n: int) -> int | None:
        need(type(n) is int and n > 0 and n % 2 == 1, 'positive odd source required')
        t, rem = divmod(n-self.source_anchor, self.source_step)
        if rem or not self.occupied or t < self.lower:
            return None
        if self.upper is not None and t > self.upper:
            return None
        return t

    def record(self) -> dict:
        return {'word': list(self.word), 'source_anchor': self.source_anchor,
                'source_step': self.source_step, 'target_anchor': self.target_anchor,
                'target_step': self.target_step, 'lower': self.lower, 'upper': self.upper,
                'occupied': self.occupied, 'A': self.A, 'L': self.L, 'C': self.C, 'D': self.D}


def first_descent_cell(word: Iterable[int]) -> DescentCell:
    """All positive odd sources whose *first* strict descent is this word.

    The full legal cylinder is retained even when its first-descent mask is
    empty. lower/upper apply to the original integer lift parameter t.
    """
    p = cd.packet(word)
    need(bool(p.word), 'nonempty word required')
    r = ((p.U-p.C)*pow(p.L, -1, 2*p.U)) % (2*p.U)
    u, rem = divmod(p.L*r+p.C, p.U)
    need(not rem and r > 0 and r % 2 and u % 2, 'invalid original cylinder')
    lo, hi = 0, None
    if p.D <= 0:
        hi = -1  # supported, empty first-descent interval
    else:
        lo = max(0, (p.C-p.D*r)//(2*p.U*p.D)+1)
        for j in range(1, len(p.word)):
            q = cd.packet(p.word[:j])
            if q.D > 0:
                upper = (q.C-q.D*r)//(2*p.U*q.D)
                hi = upper if hi is None else min(hi, upper)
    return DescentCell(p.word, r, 2*p.U, u, 2*p.L, lo, hi,
                       p.A, p.L, p.C, p.D)


def first_descent_word(n: int, cap: int = 10000) -> tuple[int, ...] | None:
    cd.step(n)
    need(type(cap) is int and cap >= 0, 'nonnegative return cap required')
    if n == 1:
        return None
    x, word = n, []
    for _ in range(cap):
        x, a = cd.step(x)
        word.append(a)
        if x < n:
            return tuple(word)
        if x == n:
            return None  # no descent; not relabelled as convergence
    return None  # unresolved at the stated cap


def build_atlas(seed_bound: int = 4095, cap: int = 10000) -> tuple[tuple[DescentCell, ...], dict]:
    need(type(seed_bound) is int and seed_bound >= 1 and seed_bound % 2 == 1,
         'positive odd seed bound required')
    cells: dict[tuple[int, ...], DescentCell] = {}
    unresolved, seed_rows = [], []
    for n in range(3, seed_bound+1, 2):
        w = first_descent_word(n, cap)
        if w is None:
            unresolved.append(n)
            continue
        cell = cells.setdefault(w, first_descent_cell(w))
        t = cell.parameter(n)
        need(t is not None, 'seed absent from its compiled first-descent cell')
        y = cell.target_anchor+cell.target_step*t
        need(0 < y < n, 'invalid seed descent endpoint')
        seed_rows.append([n, list(w), y])
    rows = tuple(cells[w] for w in sorted(cells, key=lambda w: (len(w), w)))
    encoded = json.dumps(seed_rows, separators=(',', ':')).encode()
    summary = {'seed_bound': seed_bound, 'return_cap': cap,
               'seeds_with_descent': len(seed_rows), 'unresolved_seeds': unresolved,
               'distinct_cells': len(rows), 'seed_rows_sha256': hashlib.sha256(encoded).hexdigest(),
               'max_word_length': max((len(c.word) for c in rows), default=0),
               'max_exponent_sum': max((c.A for c in rows), default=0),
               'infinite_cells': sum(c.upper is None and c.occupied for c in rows),
               'finite_cells': sum(c.upper is not None and c.occupied for c in rows)}
    return rows, summary


class RootSplice(cd.DescentCompression):
    """Extend an existing exact retraction only at its actual residual roots.

    A new block r -> d is followed by the old d -> Q(d) path. The endpoint
    is a strictly smaller old root; recursion cannot cycle. All new paths
    and all old paths remain chains on the original +1 Collatz edges.
    """
    def __init__(self, base: cd.DescentCompression, cells: Iterable[DescentCell], tails=()):
        need(base.c == 1, 'root splicing here uses the original +1 forcing only')
        self.base, self.cells, self.c = base, tuple(cells), 1
        self.tails = tuple(tails)
        if self.tails:
            from tail_descent import descent_tail
            for tail in self.tails:
                need(tail == descent_tail(tail.prefix), 'forged unbounded descent tail')
        # Reject a forged chart before using it to certify any source.
        for cell in self.cells:
            need(cell == first_descent_cell(cell.word), 'forged descent cell')
        self.cache = {1: (1, {})}
        self.records = {}
        self.added_roots: dict[int, dict] = {}

    def _old_root(self, root: int) -> tuple[int, dict[int, int]]:
        old_root, old_path = self.base.resolve(root)
        need(old_root == root and not old_path, 'new block must start at an old root')
        trail = []
        x = root
        while x not in self.cache:
            matches = [cell for cell in self.cells if cell.parameter(x) is not None]
            need(len(matches) <= 1, 'first-descent atlas has overlapping labelled cells')
            word = matches[0].word if matches else None
            kind = 'first-descent cell'
            if word is None:
                tail_words = [w for tail in self.tails if (w := tail.word_for(x)) is not None]
                need(len(tail_words) <= 1, 'overlapping labelled tail prefixes')
                if tail_words:
                    word, kind = tail_words[0], 'unbounded last-exponent tail'
            if word is None:
                self.cache[x] = (x, {})
                break
            rec = cd.path_from_word(x, word)
            y = rec['terminal']
            need(rec['strict_descent'], 'new word does not give actual strict descent')
            z, old_tail = self.base.resolve(y)
            need(z <= y < x, 'old-root endpoint did not strictly decrease')
            chain = add({int(k): v for k, v in rec['relative_chain'].items()}, old_tail)
            expected = Counter({x: 1})
            if z != 1:
                expected[z] -= 1
            need(cd.sparse_boundary(chain) == clean(expected), 'new root-block boundary failed')
            self.records[x] = (z, chain)
            self.added_roots[x] = {'word': list(word), 'rule_kind': kind, 'block_terminal': y,
                                   'old_root_endpoint': z}
            trail.append(x)
            x = z
        for v in reversed(trail):
            endpoint, block = self.records[v]
            final_root, tail = self.cache[endpoint]
            self.cache[v] = (final_root, add(block, tail))
        final_root, chain = self.cache[root]
        return final_root, dict(chain)

    def correction(self, n: int) -> dict[int, int]:
        root, _ = self.base.resolve(n)
        return self._old_root(root)[1]

    def resolve(self, n: int) -> tuple[int, dict[int, int]]:
        root, old_path = self.base.resolve(n)
        final_root, extra = self._old_root(root)
        return final_root, add(old_path, extra)


def mm(A, B):
    return [[sum(a*b for a, b in zip(row, col)) for col in zip(*B)] for row in A]


def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def minus(A, B):
    return [[a-b for a, b in zip(ar, br)] for ar, br in zip(A, B)]


def inverse(A):
    n = len(A)
    rows = [[Fraction(x) for x in row]+[Fraction(x) for x in eye(n)[i]]
            for i, row in enumerate(A)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if rows[i][j]), None)
        need(pivot is not None, 'singular matrix')
        rows[j], rows[pivot] = rows[pivot], rows[j]
        p = rows[j][j]
        rows[j] = [x/p for x in rows[j]]
        for i in range(n):
            if i != j:
                p = rows[i][j]
                rows[i] = [x-p*y for x, y in zip(rows[i], rows[j])]
    return [row[n:] for row in rows]


def bezout(a: int, b: int) -> tuple[int, int]:
    x, xx, y, yy, aa, bb = 1, 0, 0, 1, a, b
    while bb:
        q, rem = divmod(aa, bb)
        aa, bb, x, xx, y, yy = bb, rem, xx, x-q*xx, yy, y-q*yy
    need(aa == 1 and a*x+b*y == 1, 'nonprimitive block row')
    return x, y


def integral(A):
    need(all(Fraction(x).denominator == 1 for row in A for x in row), 'nonintegral comparison map')
    return [[int(x) for x in row] for row in A]


def block_comparison(word: Iterable[int], lengths: Iterable[int]) -> dict:
    """Integral chain equivalence with the full block dictionary retained."""
    p, lengths = cd.packet(word), tuple(lengths)
    need(bool(p.word) and bool(lengths) and all(type(s) is int and s > 0 for s in lengths)
         and sum(lengths) == len(p.word), 'block lengths must partition the original word')
    m, k = len(p.word), len(lengths)
    R, P0, S1, Bbar = [[0]*m for _ in lengths], [[0]*m for _ in lengths], [[0]*k for _ in p.word], [[0]*k for _ in lengths]
    blocks, start = [], 0
    for i, size in enumerate(lengths):
        q = cd.packet(p.word[start:start+size])
        row = cd.functional(q.word)
        R[i][start:start+size] = row
        P0[i][start] = 1
        if size == 1:
            S1[start][i] = 1
        else:
            a, b = bezout(row[0], row[-1])
            S1[start][i], S1[start+size-1][i] = a, b
        Bbar[i][i] -= q.L
        Bbar[i][(i+1) % k] += q.U
        blocks.append({'start': start, 'word': list(q.word), 'L': q.L, 'U': q.U,
                       'C': q.C, 'anchored_forcing': q.C-q.D})
        start += size
    B = cd.cyclic_matrix(p.word)
    Binv = inverse(B)
    S0 = integral(mm(mm(Binv, S1), Bbar))
    H = integral(mm(Binv, minus(eye(m), mm(S1, R))))
    need(mm(R, B) == mm(Bbar, P0), 'block chain equation failed')
    need(mm(R, S1) == eye(k) and mm(P0, S0) == eye(k), 'block inverse-on-image failed')
    need(mm(B, H) == minus(eye(m), mm(S1, R)), 'degree-one homotopy failed')
    need(mm(H, B) == minus(eye(m), mm(S0, P0)), 'degree-zero homotopy failed')
    return {'original_word': list(p.word), 'lengths': list(lengths), 'blocks': blocks,
            'B': B, 'Bbar': Bbar, 'P0': P0, 'R': R, 'S0': S0, 'S1': S1, 'H': H,
            'D': p.D, 'original_forcing': [1]*m,
            'compressed_forcing': [b['C'] for b in blocks]}


def rising_blocks(word: Iterable[int]) -> dict:
    p = cd.packet(word)
    positions = [i for i, a in enumerate(p.word) if a == 1]
    need(bool(positions), 'this blocking requires at least one exponent 1')
    offset = positions[0]
    rotated = p.word[offset:]+p.word[:offset]
    starts = [i for i, a in enumerate(rotated) if a == 1]
    lengths = [b-a for a, b in zip(starts, starts[1:]+[len(rotated)])]
    return {'original_word': list(p.word), 'rotation_offset': offset,
            'rotation_inverse': [(i+offset) % len(p.word) for i in range(len(p.word))],
            'rotated_word': list(rotated), 'lengths': lengths}


def period_sieve(minimum: int = 4097, rise_budget: int = 60, scan: int = 147) -> dict:
    """Exact necessary period windows, not a conjectural cycle oracle.

    The verifier separately proves the fixed minimum from the finite atlas.
    Every comparison below is on integers; no floating logarithms occur.
    """
    need(type(minimum) is int and minimum >= 3 and minimum % 2 == 1, 'odd minimum >= 3 required')
    need(type(rise_budget) is int and rise_budget >= 0 and type(scan) is int and scan >= 1,
         'invalid finite bounds')
    s, k = minimum, rise_budget
    m = 0
    while (4*s)**(m+1) <= 2**k*(3*s+1)**(m+1):
        m += 1
    ceiling = m
    rows, first = [], None
    for length in range(1, max(scan, ceiling)+1):
        odd_power = 3**length
        exponent = odd_power.bit_length()  # least A with 2**A > 3**length
        left = (1 << exponent)*s**length
        right = (3*s+1)**length
        allowed = left <= right
        rows.append([length, exponent, allowed])
        if allowed and first is None:
            first = [length, exponent, 2*length-exponent]
    excluded = all(not row[2] for row in rows if row[0] <= ceiling)
    return {'minimum': s, 'rise_budget': k, 'period_ceiling': ceiling,
            'cutoff_witness_length': ceiling+1,
            'cutoff_comparison': '(4*s)^(M+1) > 2^k*(3*s+1)^(M+1)',
            'period_windows': rows, 'budget_excluded': excluded,
            'first_unexcluded_window': first}


def coefficient_crossing_box(word: Iterable[int], minimum: int = 3) -> dict:
    """The exact remaining source interval at a first completed coefficient crossing."""
    p = cd.packet(word)
    need(p.word and p.D > 0 and all(cd.packet(p.word[:j]).D <= 0
                                  for j in range(1, len(p.word))),
         'word must end at its first completed coefficient crossing')
    need(type(minimum) is int and minimum >= 1, 'positive minimum required')
    r = ((p.U-p.C)*pow(p.L, -1, 2*p.U)) % (2*p.U)
    lo = max(0, -((r-minimum)//(2*p.U)))
    hi = (p.C-p.D*r)//(2*p.U*p.D)
    count = max(0, hi-lo+1)
    bound = (len(p.word)+6*p.D-1)//(6*p.D)
    need(3*p.C <= len(p.word)*p.L, 'first-crossing numerator bound failed')
    need(count <= bound, 'exception-count bound failed')
    return {'word': list(p.word), 'r': r, 'step': 2*p.U, 'minimum': minimum,
            'lower': lo, 'upper': hi, 'count': count,
            'universal_count_bound': bound, 'C': p.C, 'D': p.D,
            'original_label_retained': True}


def first_period_window(minimum: int, scan_limit: int = 10000) -> tuple[int, int] | None:
    need(type(minimum) is int and minimum >= 3 and type(scan_limit) is int and scan_limit > 0,
         'invalid period search domain')
    three, denominator, upper = 1, 1, 1
    for m in range(1, scan_limit+1):
        three *= 3; denominator *= minimum; upper *= 3*minimum+1
        A = three.bit_length()
        if (1 << A)*denominator <= upper:
            return m, A
    return None


def cycle_minimum_ceiling(m: int, A: int) -> int:
    need(type(m) is int and m >= 1 and type(A) is int and A >= 1 and 2**A > 3**m,
         'positive contracting period data required')
    def allowed(n):
        return 2**A*n**m <= (3*n+1)**m
    low, high = 0, 1
    while allowed(high):
        high *= 2
    while high-low > 1:
        mid = (high+low)//2
        if allowed(mid): low = mid
        else: high = mid
    need(allowed(low) and not allowed(low+1), 'minimum ceiling boundary check failed')
    return low


def bootstrap(seed_budget: int = 100000) -> tuple[tuple[DescentCell, ...], dict]:
    """Discharge successive period windows by proving their full minimum range.

    The budget caps finite execution only. The first unprocessed window and
    every source beyond the proved range remain explicitly unresolved.
    """
    need(type(seed_budget) is int and seed_budget >= 4095, 'budget must include the inherited range')
    bound, stages = 4095, []
    cells, summary = build_atlas(bound)
    need(not summary['unresolved_seeds'], 'initial source range not certified')
    while True:
        s = bound+2
        pair = first_period_window(s)
        need(pair is not None, 'period scan exhausted; no global conclusion supplied')
        m, A = pair
        ceiling = cycle_minimum_ceiling(m, A)
        target = ceiling if ceiling % 2 else ceiling-1
        pending = {'minimum': s, 'period': m, 'exponent_sum': A,
                   'least_possible_rise_count': 2*m-A,
                   'cycle_minimum_ceiling': ceiling, 'required_odd_seed_bound': target}
        if target > seed_budget:
            break
        need(target > bound, 'feedback did not extend the certified source')
        new_cells, new_summary = build_atlas(target)
        need(not new_summary['unresolved_seeds'], 'new minimum range retained: a seed is unresolved')
        stages.append(dict(pending, certified_odd_seed_bound=target,
                           new_seeds=(target-bound)//2, distinct_cells=new_summary['distinct_cells'],
                           seed_rows_sha256=new_summary['seed_rows_sha256']))
        bound, cells, summary = target, new_cells, new_summary
    return cells, {'seed_budget': seed_budget, 'initial_seed_bound': 4095,
                   'stages': stages, 'final_atlas': summary, 'pending_window': pending}
