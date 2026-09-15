#!/usr/bin/env python3
"""Integral first-jet defects on finite sets of ORIGINAL Collatz equations.

Support is the declared set of equations, not a trajectory word. All endpoints,
including frontier vertices and the fixed loop at 1, remain in the complex.
For d=J-P, the dual-number deformation is d_epsilon=d-epsilon*P.
The connecting map is beta(c)=-[P*c], c in ker d. Its cokernel has one Z/m
summand per retained cycle and one Z per open frontier component. An open
component of a finite graph is not a certified nonperiodic infinite component.
"""
from __future__ import annotations
import argparse
from collections import Counter
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Iterable, Mapping


class CertificateError(ValueError):
    """An input does not satisfy its exact stated certificate equations."""


def require(ok: bool, message: str) -> None:
    if not ok:
        raise CertificateError(message)


def step(n: int, forcing: int = 1) -> tuple[int, int]:
    require(type(n) is int and n > 0 and n % 2 == 1, 'source must be a positive odd integer')
    require(type(forcing) is int and forcing in (1, -1), 'forcing must be +1 or the labelled -1 control')
    value = 3*n+forcing
    a = (value & -value).bit_length()-1
    require(a >= 1, 'odd-return exponent must be positive')
    return value >> a, a


def clean(values: Mapping[int, int]) -> dict[int, int]:
    return {n: k for n, k in sorted(values.items()) if k}


def checked_chain(values: Mapping[int, int]) -> dict[int, int]:
    require(isinstance(values, dict), 'chain must be a dictionary')
    for n, k in values.items():
        require(type(n) is int and n > 0 and n % 2 == 1, 'invalid original edge label')
        require(type(k) is int, 'integral edge coefficients required')
    return clean(values)


def boundary(chain: Mapping[int, int], forcing: int = 1) -> dict[int, int]:
    result: Counter[int] = Counter()
    for n, k in checked_chain(dict(chain)).items():
        y, _ = step(n, forcing)
        result[n] += k
        result[y] -= k
    return clean(result)


def target(chain: Mapping[int, int], forcing: int = 1) -> dict[int, int]:
    result: Counter[int] = Counter()
    for n, k in checked_chain(dict(chain)).items():
        result[step(n, forcing)[0]] += k
    return clean(result)


def jet_boundary(b: Mapping[int, int], c: Mapping[int, int], forcing: int = 1) -> tuple[dict[int, int], dict[int, int]]:
    """d_epsilon(b+epsilon*c)=(d*b)+epsilon*(d*c-P*b)."""
    linear = Counter(boundary(c, forcing))
    linear.subtract(target(b, forcing))
    return boundary(b, forcing), clean(linear)


@dataclass(frozen=True)
class Dual:
    """The original ring Z[epsilon]/epsilon^2 in two integer coordinates."""
    constant: int
    linear: int

    def __post_init__(self) -> None:
        require(type(self.constant) is int and type(self.linear) is int, 'dual coordinates must be integers')

    def __add__(self, other: Dual) -> Dual:
        return Dual(self.constant+other.constant, self.linear+other.linear)

    def __mul__(self, other: Dual) -> Dual:
        return Dual(self.constant*other.constant, self.constant*other.linear+self.linear*other.constant)

    def __neg__(self) -> Dual:
        return Dual(-self.constant, -self.linear)


def split_add(a: Dual | None, b: Dual | None) -> Dual | None:
    return b if a is None else a if b is None else a+b


def split_mul(a: Dual | None, b: Dual | None) -> Dual | None:
    return None if a is None or b is None else a*b


def coordinates(a: Dual | None) -> tuple[Dual, bool]:
    return (Dual(0,0), False) if a is None else (a, True)


def from_coordinates(value: tuple[Dual, bool]) -> Dual | None:
    a, occupied = value
    require(type(occupied) is bool, 'Boolean support required')
    require(occupied or a == Dual(0,0), 'outside the split-zero coordinate image')
    return a if occupied else None


def diagram(sources: Iterable[int], forcing: int = 1) -> dict:
    """Full finite component presentation; a modulus 1 is RETAINED as a label."""
    require(type(forcing) is int and forcing in (1,-1), 'invalid forcing')
    declared = list(sources)
    for n in declared:
        step(n, forcing)
    src = sorted(set(declared))
    nxt, exponents = {}, {}
    for n in src:
        nxt[n], exponents[n] = step(n, forcing)
    vertices = sorted(set(src) | set(nxt.values()))
    parent = {n:n for n in vertices}
    def find(n: int) -> int:
        while parent[n] != n:
            parent[n] = parent[parent[n]]
            n = parent[n]
        return n
    for n,y in nxt.items():
        a,b = find(n),find(y)
        if a != b:
            parent[max(a,b)] = min(a,b)
    groups: dict[int, list[int]] = {}
    for n in vertices:
        groups.setdefault(find(n), []).append(n)
    comps, component_of = [], {}
    for key, vs in sorted(groups.items()):
        seen, path, x = {}, [], min(vs)
        while x in nxt and x not in seen:
            seen[x] = len(path)
            path.append(x)
            x = nxt[x]
        if x in seen:
            cyc = path[seen[x]:]
            cut = cyc.index(min(cyc))
            cyc = cyc[cut:]+cyc[:cut]
            m = len(cyc)
            require(boundary({v:1 for v in cyc}, forcing) == {}, 'cycle boundary failed')
            kind = 'fixed_cycle' if m == 1 else 'retained_cycle'
            frontier = []
        else:
            cyc, m, kind = [], 0, 'open_frontier'
            frontier = sorted(set(vs)-set(src))
            require(frontier == [x], 'finite functional component must have one frontier or one cycle')
        for n in vs:
            component_of[n] = len(comps)
        comps.append({'root_label':min(vs), 'vertices':vs, 'cycle':cyc,
                      'period':m, 'modulus':m, 'kind':kind, 'frontier':frontier,
                      'beta_coordinate':-m if cyc else None,
                      'even_clock':sum(exponents[n]-1 for n in cyc) if cyc else None,
                      'zero_defect_with_retained_support':m == 1})
    E,V = src,vertices
    rows = {n:i for i,n in enumerate(V)}
    d = [[0 for _ in E] for _ in V]
    P = [[0 for _ in E] for _ in V]
    for j,n in enumerate(E):
        d[rows[n]][j] += 1
        d[rows[nxt[n]]][j] -= 1
        P[rows[nxt[n]]][j] += 1
    return {'forcing':forcing, 'source_label':E, 'vertex_labels':V,
            'original_edges':[[n,nxt[n],exponents[n]] for n in E],
            'd_matrix':d, 'target_matrix':P, 'components':comps,
            'component_of':component_of,
            'H0_rank':sum(bool(c['cycle']) for c in comps), 'H1_rank':len(comps),
            'defect_free_rank':sum(c['period'] == 0 for c in comps),
            'defect_cycle_moduli':[c['period'] for c in comps if c['period'] > 1],
            'frontier_is_infinite_orbit_certificate':False,
            'fixed_loop_removed':False}


def class_coordinates(graph: dict, vector: Mapping[int, int]) -> list[int]:
    out = [0]*len(graph['components'])
    for n,k in vector.items():
        require(n in graph['component_of'], 'vertex outside declared graph')
        require(type(k) is int, 'integral coefficients required')
        out[graph['component_of'][n]] += k
    for i,comp in enumerate(graph['components']):
        if comp['modulus']:
            out[i] %= comp['modulus']
    return out


def transition(small: dict, large: dict) -> list[list[int]]:
    require(small['forcing'] == large['forcing'], 'cannot change the arithmetic forcing in an inclusion')
    require(set(small['source_label']) <= set(large['source_label']), 'support inclusion required')
    result = [[0]*len(small['components']) for _ in large['components']]
    for j,comp in enumerate(small['components']):
        i = large['component_of'][comp['root_label']]
        result[i][j] = 1
        old,new = comp['modulus'],large['components'][i]['modulus']
        require(not old or (new and old % new == 0), 'old cycle relation lost under source inclusion')
    return result


def defect_presentation(graph: dict) -> list[list[int]]:
    """Integer presentation [d | P*c_C] of coker beta, with original rows."""
    V = graph['vertex_labels']
    result = [row[:] for row in graph['d_matrix']]
    for comp in graph['components']:
        if comp['cycle']:
            col = target({n:1 for n in comp['cycle']}, graph['forcing'])
            for i,n in enumerate(V):
                result[i].append(col.get(n,0))
    return result


def validate_witness(n: int, b: Mapping[int, int], c: Mapping[int, int], forcing: int = 1) -> dict:
    """Check finite integral first-order boundary, then EXTRACT the actual path.

    No stopping-time conclusion is inferred from a rational witness.
    Both supported maps +/- have only the positive fixed point 1; -1 is a control.
    """
    step(n, forcing)
    b,c = checked_chain(dict(b)),checked_chain(dict(c))
    constant,linear = jet_boundary(b,c,forcing)
    require(constant == {}, 'nonzero constant boundary: b is not a cycle')
    require(linear == {n:1}, 'first-order boundary must be exactly the original singleton')
    graph = diagram(set(b)|set(c), forcing)
    require(n in graph['component_of'], 'source missing from certificate graph')
    comp = graph['components'][graph['component_of'][n]]
    require(comp['cycle'] == [1], 'integral singleton witness must contain the actual fixed loop')
    nxt = {x:y for x,y,_ in graph['original_edges']}
    x, values, exponents, seen = n,[n],[],set()
    while x != 1:
        require(x not in seen and x in nxt, 'certificate does not contain a finite route to 1')
        seen.add(x)
        y,a = step(x,forcing)
        require(nxt[x] == y, 'original edge mismatch')
        exponents.append(a); values.append(y); x=y
    return {'source':n, 'forcing':forcing, 'values':values, 'exponents':exponents,
            'returns':len(exponents), 'constant_cycle':b, 'linear_chain':c,
            'boundary_constant':constant, 'boundary_linear':linear,
            'status':'verified_finite_first_order_boundary'}


def witness(n: int, cap: int = 10000, forcing: int = 1) -> dict:
    require(type(cap) is int and cap >= 0, 'nonnegative finite cap required')
    step(n,forcing)
    x, seen, chain, count = n,set(),Counter(),0
    while x != 1 and x not in seen and count < cap:
        seen.add(x); chain[x] += 1
        x,_ = step(x,forcing)
        count += 1
    if x != 1:
        return {'source':n, 'forcing':forcing, 'status':'retained_cycle' if x in seen else 'unresolved_at_cap',
                'terminal':x, 'returns':count, 'finite_boundary_claim':False}
    return validate_witness(n, {1:-1}, clean(chain), forcing)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('diagram'); p.add_argument('sources',type=int,nargs='*')
    p.add_argument('--forcing',type=int,choices=[1,-1],default=1)
    w = sub.add_parser('witness'); w.add_argument('source',type=int)
    w.add_argument('--cap',type=int,default=10000)
    w.add_argument('--forcing',type=int,choices=[1,-1],default=1)
    for s in (p,w): s.add_argument('--output',type=Path)
    args = parser.parse_args()
    try:
        result = diagram(args.sources,args.forcing) if args.command == 'diagram' else witness(args.source,args.cap,args.forcing)
    except CertificateError as exc:
        parser.error(str(exc))
    text = json.dumps(result,sort_keys=True,indent=2)+'\n'
    if args.output: args.output.write_text(text,encoding='utf-8')
    else: print(text,end='')


if __name__ == '__main__':
    main()
