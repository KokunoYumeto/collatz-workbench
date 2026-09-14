#!/usr/bin/env python3
"""Supported anchored defects and exact alphabet-exit/descent partitions.

Original positive 3x+1 odd-return map. No external packages. A finite cap
produces explicit OPEN leaves; it is never interpreted as nonexistence.
"""
from __future__ import annotations
import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from math import gcd
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
NAME = '_anchored_original_cycle_source'
if NAME not in sys.modules:
    path = HERE.parent/'cycle_relative_cohomology_20260914'/'cycle_detector.py'
    spec = importlib.util.spec_from_file_location(NAME, path)
    if spec is None or spec.loader is None:
        raise RuntimeError('The preserved original cycle source is required')
    module = importlib.util.module_from_spec(spec)
    sys.modules[NAME] = module
    spec.loader.exec_module(module)
cd = sys.modules[NAME]


def need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


@dataclass(frozen=True)
class Supported:
    """Faithful G(Q) coordinate: absent=(0,False), present zero=(0,True)."""
    value: F
    present: bool

    def __post_init__(self):
        need(type(self.present) is bool, 'presence must be Boolean')
        object.__setattr__(self, 'value', F(self.value))
        need(self.present or self.value == 0, 'an absent value must reflect to zero')

    def __add__(self, other: Supported) -> Supported:
        return Supported(self.value+other.value, self.present or other.present)

    def __mul__(self, other: Supported) -> Supported:
        return Supported(self.value*other.value, self.present and other.present)

    def record(self) -> dict:
        return {'value': str(self.value), 'present': self.present}


def anchored_edge(n: int) -> dict:
    target, a = cd.step(n)
    forcing = Supported(4-(1 << a), True)
    out = {'source': n, 'target': target, 'a': a,
           'source_displacement': n-1, 'target_displacement': target-1,
           'anchored_forcing': forcing.record()}
    need((1 << a)*(target-1) == 3*(n-1)+forcing.value, 'anchored edge equation')
    if n == 1:
        out.update(ratio=None, ratio_domain='basepoint_relation_0_equals_0')
    else:
        eta = F((1 << a)*(target-1), 3*(n-1))
        need(eta == 1+F(forcing.value, 3*(n-1)), 'defect factor identity')
        out.update(ratio=Supported(eta, True).record(),
                   ratio_domain='positive' if target > 1 else 'present_zero_at_entry')
    return out


def anchored_ceiling(m: int, A: int, k: int, incoming_three: bool = False) -> int:
    """Largest integer s>=2 allowed by 2^A/3^m <= ((3s-1)/(3s-3))^k."""
    need(all(type(x) is int for x in (m,A,k)) and m >= 1 and A >= 1 and 1 <= k <= m,
         'invalid period/count data')
    U, L = 1 << A, 3**m
    need(U > L, 'positive contracting period required')
    def allowed(s):
        left, right = U*(3*s-3)**k, L*(3*s-1)**k
        if incoming_three:
            left *= 2*s-1; right *= 2*s-2
        return left <= right
    if not allowed(2):
        return 1
    low, high = 2, 4
    while allowed(high):
        high *= 2
    while high-low > 1:
        mid = (high+low)//2
        if allowed(mid): low = mid
        else: high = mid
    need(allowed(low) and not allowed(low+1), 'anchored ceiling boundary')
    return low


def joint_fiber(r: int, q: int, low: int, high: int, residue: int, modulus: int) -> dict:
    """The exact intersection of two retained progressions and an interval."""
    need(all(type(x) is int for x in (r,q,low,high,residue,modulus)) and q > 0 and modulus > 0,
         'integer progressions with positive moduli required')
    g = gcd(q, modulus)
    out = {'r': r, 'q': q, 'low': low, 'high': high,
           'residue': residue, 'modulus': modulus, 'gcd': g, 'label_present': True}
    if (residue-r) % g:
        out.update(compatible=False, residue_defect=(residue-r) % g,
                   parameter_offset=None, anchor=None, step=None,
                   lower_parameter=None, upper_parameter=None, first=None, last=None, count=0)
        return out
    reduced_modulus = modulus//g
    t0 = ((residue-r)//g*pow(q//g, -1, reduced_modulus)) % reduced_modulus
    anchor, step = r+q*t0, q*reduced_modulus
    lower = -((anchor-low)//step)
    upper = (high-anchor)//step
    count = max(0, upper-lower+1)
    out.update(compatible=True, residue_defect=0, parameter_offset=t0,
               anchor=anchor, step=step, lower_parameter=lower, upper_parameter=upper,
               first=anchor+step*lower if count else None,
               last=anchor+step*upper if count else None, count=count)
    return out


def chart(word: tuple[int, ...]) -> tuple:
    p = cd.packet(word)
    if not word:
        return p, 1, 1
    r = ((p.U-p.C)*pow(p.L, -1, 2*p.U)) % (2*p.U)
    u, rem = divmod(p.L*r+p.C, p.U)
    need(rem == 0 and r % 2 == u % 2 == 1, 'original chart membership')
    return p,r,u


def make_cover(low: int = 99781, high: int = 274546, residue: int = 7,
               modulus: int = 12, depth_cap: int = 64, excess_budget: int = 0) -> dict:
    """Partition candidate minima into descent, actual alphabet exit, or OPEN.

    Every node retains empty and incompatible branch labels. An exit at q
    means its next exponent would exceed the retained excess budget; it is recovered
    from the original target chart, not replaced by a fixed value 3.
    """
    need(type(low) is int and type(high) is int and 3 <= low <= high, 'invalid positive interval')
    need(type(depth_cap) is int and 0 <= depth_cap <= 1000, 'invalid finite depth cap')
    need(type(excess_budget) is int and 0 <= excess_budget <= 8, 'supported excess budget is 0 through 8')
    root = joint_fiber(1,2,low,high,residue,modulus)
    stack = [((),low,high)] if root['count'] else []
    nodes, leaves = [], []
    while stack:
        word,lo,hi = stack.pop()
        p,r,u = chart(word)
        source = joint_fiber(r,2*p.U,lo,hi,residue,modulus)
        need(source['count'] > 0, 'empty pending source')
        if len(word) >= depth_cap:
            leaves.append({'kind':'OPEN', 'word':list(word), 'fiber':source})
            continue
        remaining = excess_budget-sum(max(0,a-2) for a in word)
        need(remaining >= 0, 'prefix already exceeded its retained excess budget')
        B = remaining+3
        modulus_t = 1 << (B-1)
        t0 = (-(3*u+1)//2*pow(3*p.L,-1,modulus_t)) % modulus_t
        tail = joint_fiber(r+2*p.U*t0,2*p.U*modulus_t,lo,hi,residue,modulus)
        leaves.append({'kind':'exit', 'word':list(word), 'fiber':tail,
                       'next_exponent_lower_bound':B, 'remaining_excess':remaining,
                       'prefix_source_anchor':r, 'prefix_source_step':2*p.U,
                       'prefix_image_anchor':u, 'prefix_image_step':2*p.L,
                       'tail_parameter_offset':t0})
        children = []
        total = tail['count']
        for a in range(1,remaining+3):
            child = word+(a,)
            pp,rr,uu = chart(child)
            cutoff = pp.C//pp.D if pp.D > 0 else None
            descending_low = max(lo,cutoff+1) if cutoff is not None else hi+1
            surviving_high = min(hi,cutoff) if cutoff is not None else hi
            desc = joint_fiber(rr,2*pp.U,descending_low,hi,residue,modulus)
            alive = joint_fiber(rr,2*pp.U,lo,surviving_high,residue,modulus)
            leaves.append({'kind':'descent', 'word':list(child), 'fiber':desc,
                           'L':pp.L, 'U':pp.U, 'C':pp.C, 'D':pp.D,
                           'image_anchor':uu, 'image_step':2*pp.L})
            children.append({'a':a, 'descent':desc, 'retained':alive,
                             'descent_integer_threshold':cutoff})
            total += desc['count']+alive['count']
            if alive['count']:
                stack.append((child,lo,surviving_high))
        need(total == source['count'], 'next-exponent partition does not conserve source count')
        nodes.append({'word':list(word), 'remaining_excess':remaining, 'source':source, 'tail':tail, 'children':children})
    counts = Counter()
    for leaf in leaves:
        counts[leaf['kind']] += leaf['fiber']['count']
    need(sum(counts.values()) == root['count'], 'whole partition does not conserve source count')
    return {'parameters':{'low':low,'high':high,'residue':residue,'modulus':modulus,
                          'depth_cap':depth_cap, 'excess_budget':excess_budget}, 'root':root, 'nodes':nodes, 'leaves':leaves,
            'point_counts':dict(sorted(counts.items())),
            'complete':counts.get('OPEN',0) == 0}


def digest(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',',':')).encode()).hexdigest()


def summarize_cover(cover: dict) -> dict:
    leaves = cover['leaves']
    occupied = [x for x in leaves if x['fiber']['count']]
    return {'parameters':cover['parameters'], 'root':cover['root'],
            'node_count':len(cover['nodes']), 'leaf_labels':len(leaves),
            'occupied_leaf_labels':len(occupied),
            'present_empty_leaf_labels':sum(x['fiber']['count']==0 for x in leaves),
            'incompatible_leaf_labels':sum(not x['fiber']['compatible'] for x in leaves),
            'occupied_leaf_kinds':dict(sorted(Counter(x['kind'] for x in occupied).items())),
            'point_counts':cover['point_counts'], 'complete':cover['complete'],
            'max_nonempty_prefix':max((len(x['word']) for x in occupied),default=0),
            'full_tree_sha256':digest(cover),
            'example_leaves':[next(x for x in occupied if x['kind']==kind)
                              for kind in ('exit','descent') if any(x['kind']==kind for x in occupied)]}


def raw_witness(n: int, cap: int = 1000, excess_budget: int = 0) -> dict:
    """Independent repeated-division interpreter for a retained excess budget."""
    need(type(n) is int and n >= 3 and n % 2 == 1, 'positive odd n>=3 required')
    need(type(cap) is int and cap >= 0, 'invalid cap')
    start,x,word,chain,used = n,n,[],[],0
    for _ in range(cap):
        if x < start:
            return {'source':start,'kind':'descent','word':word,'terminal':x,'chain':chain}
        value,a = 3*x+1,0
        while value % 2 == 0:
            value //= 2; a += 1
        if used+max(0,a-2) > excess_budget:
            return {'source':start,'kind':'exit','word':word,'terminal':x,
                    'next_exponent':a,'excess_used':used,'chain':chain}
        chain.append(x); word.append(a); x=value; used+=max(0,a-2)
        if x == start:
            return {'source':start,'kind':'CYCLE','word':word,'terminal':x,'chain':chain}
    return {'source':start,'kind':'OPEN','word':word,'terminal':x,'chain':chain}


def period_reduction(s: int = 99781, k: int = 403) -> dict:
    """Exact period constraints used with the separately replayed source bound."""
    need(type(s) is int and s >= 3 and type(k) is int and k >= 1, 'invalid bounds')
    left,right,m = 1,1,0
    while left*(4*s) <= (1 << k)*right*(3*s+1):
        m += 1; left *= 4*s; right *= 3*s+1
    ceiling=m
    three,denom,upper=1,1,1
    windows=[]
    for length in range(1,ceiling+1):
        three*=3; denom*=s; upper*=3*s+1
        A=three.bit_length()
        while (1 << A)*denom <= upper:
            E=A-2*length+k
            if E >= 0:
                windows.append({'m':length,'A':A,'k_budget':k,'maximum_excess':E,
                                'least_rises':max(0,2*length-A)})
            A += 1
    return {'minimum_lower_bound':s,'rise_budget':k,'period_ceiling':ceiling,
            'cutoff_witness_length':ceiling+1,'windows':windows,
            'inequalities_checked_over_integers':True}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--full-cover',action='store_true')
    parser.add_argument('--output',type=Path)
    parser.add_argument('--excess-budget',type=int,default=0)
    parser.add_argument('--residue',type=int,default=7)
    parser.add_argument('--upper',type=int,default=274546)
    args=parser.parse_args()
    c=make_cover(high=args.upper,residue=args.residue,excess_budget=args.excess_budget)
    result=c if args.full_cover else summarize_cover(c)
    text=json.dumps(result,sort_keys=True,indent=2)+'\n'
    if args.output: args.output.write_text(text,encoding='utf-8')
    else: print(text,end='')


if __name__ == '__main__':
    main()
