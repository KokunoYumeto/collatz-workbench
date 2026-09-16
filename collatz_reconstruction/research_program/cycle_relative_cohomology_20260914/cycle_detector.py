#!/usr/bin/env python3
"""Exact Collatz return obstruction and relative graph certificates.

Default c=1 is the original map. c=-1 is an explicitly labelled detector
control, related to signed 3x+1 by x -> -x. Standard library only.
No finite overflow is reported as a proof of divergence.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as F
from math import gcd
import json
from pathlib import Path
from typing import Iterable


class CertificateError(ValueError):
    pass


def need(condition: bool, message: str) -> None:
    if not condition:
        raise CertificateError(message)


def v2(n: int) -> int:
    need(type(n) is int and n != 0, 'valuation requires a nonzero integer')
    n = abs(n)
    return (n & -n).bit_length() - 1


def step(n: int, c: int = 1) -> tuple[int, int]:
    need(c in (1, -1), 'supported forcing constants are +1 and control -1')
    need(type(n) is int and n > 0 and n % 2 == 1, 'positive odd source required')
    b = 3*n+c
    a = v2(b)
    need(a >= 1, 'odd-return parity failed')
    return b >> a, a


@dataclass(frozen=True)
class Packet:
    word: tuple[int, ...]
    A: int
    L: int
    C: int

    @property
    def U(self) -> int:
        return 1 << self.A

    @property
    def D(self) -> int:
        return self.U-self.L

    def evaluate(self, n: int | F, c: int = 1) -> F:
        return (self.L*F(n)+c*self.C)/self.U


def packet(word: Iterable[int]) -> Packet:
    w = tuple(word)
    need(all(type(a) is int and a >= 1 for a in w), 'exponents must be positive integers')
    A, L, C = 0, 1, 0
    for a in w:
        C, L, A = 3*C+(1 << A), 3*L, A+a
    return Packet(w,A,L,C)


def primitive(word: tuple[int, ...]) -> tuple[tuple[int, ...], int]:
    need(bool(word), 'nonempty word required')
    for d in range(1,len(word)+1):
        if len(word) % d == 0 and word[:d]*(len(word)//d) == word:
            return word[:d], len(word)//d
    raise CertificateError('primitive-period search failed')


def cyclic_matrix(word: tuple[int, ...]) -> list[list[int]]:
    need(bool(word), 'nonempty word required')
    m = len(word)
    B = [[0]*m for _ in range(m)]
    for i,a in enumerate(word):
        B[i][i] -= 3
        B[i][(i+1) % m] += 1 << a  # additive, including the m=1 case
    return B


def functional(word: tuple[int, ...]) -> tuple[int, ...]:
    A, m, out = 0,len(word),[]
    for i,a in enumerate(word):
        out.append(3**(m-1-i)*(1 << A))
        A += a
    return tuple(out)


def cycle_certificate(word: Iterable[int], c: int = 1) -> dict:
    need(c in (1,-1), 'supported forcing constants are +1 and control -1')
    p = packet(word)
    need(bool(p.word), 'cycle certificate requires a nonempty word')
    m, D = len(p.word),p.D
    need(D != 0 and gcd(D,6) == 1, 'invalid packet determinant')
    r = ((p.U-c*p.C)*pow(p.L,-1,2*p.U)) % (2*p.U)
    need(r > 0 and r % 2 == 1, 'invalid cylinder representative')
    u = p.evaluate(r,c)
    need(u.denominator == 1 and u.numerator % 2 == 1, 'invalid target anchor')
    u = int(u)
    k = (u-r)//2
    need(c*p.C == D*r+2*p.U*k, 'return-mark transport failed')
    orbit = tuple(F(c*packet(p.word[i:]+p.word[:i]).C,D) for i in range(m))
    for i,a in enumerate(p.word):
        need((3*orbit[i]+c)/(1 << a) == orbit[(i+1)%m], 'cyclic transport failed')
    q = abs(D)//gcd(abs(D),c*p.C)
    need(all(x.denominator == q for x in orbit), 'denominator transport failed')
    integral = q == 1
    positive = all(x > 0 for x in orbit)
    if integral:
        need(all(x.numerator % 2 == 1 for x in orbit), 'integer cycle parity failed')
    root, repeats = primitive(p.word)
    rp = packet(root)
    repetition_factor = sum(rp.U**(repeats-1-j)*rp.L**j for j in range(repeats))
    need(p.D == rp.D*repetition_factor and p.C == rp.C*repetition_factor,
         'repetition comparison failed')
    original_cycle = c == 1 and integral and positive
    trivial = original_cycle and all(x == 1 for x in orbit)
    if original_cycle:
        need(trivial == all(a == 2 for a in p.word), 'trivial orbit/word equivalence failed')
    if not integral:
        status = 'rational_cycle_not_integral'
    elif not positive:
        status = 'integral_cycle_outside_positive_source'
    elif c == -1:
        status = 'positive_control_cycle'
    elif trivial:
        status = 'trivial_positive_collatz_cycle'
    else:
        status = 'NONTRIVIAL_POSITIVE_COLLATZ_CYCLE'
    return {
        'forcing_c':c,'word':list(p.word),'A':p.A,'L':p.L,'U':p.U,'C':p.C,'D':D,
        'status':status,'integral':integral,'positive':positive,
        'cycle_matrix':cyclic_matrix(p.word), 'telescoping_row':list(functional(p.word)),
        'H1_cycle_group_modulus':abs(D),'forcing_class':(c*p.C) % abs(D),
        'forcing_class_order':q,'rational_orbit':[str(x) for x in orbit],
        'anchored_displacement':[str(x-1) for x in orbit],
        'anchored_forcing':[c+3-(1 << a) for a in p.word],
        'cylinder_source_anchor':r,'cylinder_source_step':2*p.U,
        'image_anchor':u,'image_step':2*p.L,'image_complex_modulus':p.L,
        'return_mark':k,'return_mark_class':k % abs(D),
        'return_parameter':str(F(k,D)),
        'primitive_word':list(root),'repetitions':repeats,'repetition_factor':repetition_factor,
        'actual_relative_cycle_contribution':bool(original_cycle and not trivial),
        'original_word_retained':True,
    }


def modular_solution_count(word: Iterable[int], modulus: int, c: int = 1) -> int:
    p = packet(word)
    need(p.word and type(modulus) is int and modulus >= 1, 'invalid modular problem')
    g = gcd(abs(p.D),modulus)
    return g if c*p.C % g == 0 else 0


def sparse_boundary(chain: dict[int,int], c: int = 1) -> dict[int,int]:
    out: Counter[int] = Counter()
    for n,k in chain.items():
        need(n != 1, 'relative edge at the basepoint is zero, not a declared edge')
        y,_ = step(n,c)
        out[n] += k
        if y != 1:
            out[y] -= k
    return {n:k for n,k in sorted(out.items()) if k}


def path_certificate(n: int, max_returns: int = 100000, c: int = 1) -> dict:
    need(type(max_returns) is int and max_returns >= 0, 'nonnegative return cap required')
    step(n,c)
    start,seen,values,exponents = n,{},[],[]
    while n != 1 and n not in seen and len(values) < max_returns:
        seen[n] = len(values)
        values.append(n)
        n,a = step(n,c)
        exponents.append(a)
    if n == 1:
        status = 'reaches_basepoint'
        cycle = []
    elif n in seen:
        status = 'actual_cycle_away_from_basepoint'
        cycle = values[seen[n]:]
    else:
        status = 'OPEN_BOUNDARY'
        cycle = []
    chain = dict(Counter(values))
    expected = Counter({start:1}) if start != 1 else Counter()
    if n != 1:
        expected[n] -= 1
    expected = {v:k for v,k in sorted(expected.items()) if k}
    boundary = sparse_boundary(chain,c)
    need(boundary == expected, 'path boundary mismatch')
    if cycle:
        need(sparse_boundary(dict(Counter(cycle)),c) == {}, 'cycle boundary mismatch')
    return {'start':start,'forcing_c':c,'status':status,'values':values,'exponents':exponents,
            'terminal':n,'cycle_vertices':cycle,'chain':{str(v):k for v,k in sorted(chain.items())},
            'boundary':{str(v):k for v,k in boundary.items()},'returns_recorded':len(values)}


class DSU:
    def __init__(self,values: Iterable[int]):
        self.parent = {v:v for v in values}
    def find(self,a: int) -> int:
        b = a
        while self.parent[b] != b:
            b = self.parent[b]
        while self.parent[a] != a:
            old_parent = self.parent[a]
            self.parent[a] = b
            a = old_parent
        return b
    def union(self,a: int,b: int) -> None:
        a,b = self.find(a),self.find(b)
        if a != b:
            self.parent[max(a,b)] = min(a,b)


def finite_graph_certificate(sources: Iterable[int], c: int = 1) -> dict:
    """Keep all actual targets, including distinct open frontier vertices."""
    src = sorted(set(sources)-{1})
    edges = [(n,step(n,c)[0]) for n in src]
    vertices = sorted({1}|set(src)|{y for _,y in edges})
    dsu = DSU(vertices)
    for n,y in edges:
        dsu.union(n,y)
    groups: dict[int,list[int]] = {}
    for v in vertices:
        groups.setdefault(dsu.find(v),[]).append(v)
    frontier = sorted(set(vertices)-set(src)-{1})
    base = dsu.find(1)
    cyclic,open_components = [],[]
    for root,vs in sorted(groups.items()):
        if root == base:
            continue
        tips = sorted(set(vs) & set(frontier))
        if tips:
            need(len(tips) == 1, 'a finite functional tree must have one frontier root')
            open_components.append({'vertices':vs,'frontier':tips[0]})
        else:
            rec = path_certificate(min(vs),len(vs)+1,c)
            need(rec['status'] == 'actual_cycle_away_from_basepoint', 'closed component cycle missing')
            cyc = rec['cycle_vertices']
            j = cyc.index(min(cyc))
            cyc = cyc[j:]+cyc[:j]
            cyclic.append({'vertices':vs,'cycle_vertices':cyc,
                           'cycle_chain':{str(v):1 for v in sorted(cyc)},
                           'detecting_cochain_edge':min(cyc),'pairing':1})
    h0 = len(groups)-1
    h1 = len(edges)-(len(vertices)-1)+h0
    need(h1 == len(cyclic), 'relative graph Euler/rank mismatch')
    return {'forcing_c':c,'sources':src,'vertices':vertices,'edges':[list(e) for e in edges],
            'frontier':frontier,'relative_H0_rank':h0,'relative_H1_rank':h1,
            'cycle_components':cyclic,'open_components':open_components,
            'basepoint':1,'unobserved_edges_added':False,'frontier_collapsed':False}


def path_from_word(n: int, word: Iterable[int]) -> dict:
    p = packet(word)
    values,x = [],n
    for a in p.word:
        y,b = step(x)
        need(a == b,'word is not the actual exponent word of this source')
        if x != 1:
            values.append(x)
        x = y
    boundary = sparse_boundary(dict(Counter(values)))
    expected = Counter()
    if n != 1: expected[n] += 1
    if x != 1: expected[x] -= 1
    need(boundary == {v:k for v,k in sorted(expected.items()) if k}, 'block path boundary failed')
    return {'source':n,'word':list(p.word),'terminal':x,
            'relative_chain':{str(v):k for v,k in sorted(Counter(values).items())},
            'boundary':{str(v):k for v,k in boundary.items()},
            'strict_descent':x<n}


def residue_tower(word: Iterable[int]) -> dict:
    w = tuple(word)
    rows,prev,prev_mod = [],1,2
    for j in range(1,len(w)+1):
        p = packet(w[:j])
        modulus = 2*p.U
        r = ((p.U-p.C)*pow(p.L,-1,modulus)) % modulus
        need(r % prev_mod == prev and r >= prev,'residue tower transition failed')
        rows.append({'prefix_length':j,'A':p.A,'modulus':modulus,'residue':r,
                     'digit_increment':(r-prev)//prev_mod})
        prev,prev_mod = r,modulus
    return {'word':list(w),'rows':rows,'finite_only':True}


def one_spike_formula(m: int) -> dict:
    need(type(m) is int and m >= 1,'positive length required')
    p = packet((1,)+(2,)*(m-1))
    need(p.C-p.D == 2*3**(m-1),'one-spike anchored identity failed')
    need((p.D == -1) if m <= 2 else p.D >= 5,'one-spike determinant bound failed')
    need(not (p.D > 0 and p.C % p.D == 0),'one-spike positive integer exclusion failed')
    return {'m':m,'D':p.D,'C_minus_D':p.C-p.D,
            'gcd_D_C_minus_D':gcd(abs(p.D),p.C-p.D)}


def enumerate_words(A_max: int) -> dict:
    """Exhaust every nonempty exponent word with total sum <= A_max."""
    need(type(A_max) is int and 1 <= A_max <= 24,'choose an exact sum bound from 1 to 24')
    stack = [((),0,1,0)]
    counts = Counter()
    positives = []
    negative_integral = []
    # Never prune on conjectural cycle properties. Every word is visited.
    while stack:
        w,A,L,C = stack.pop()
        if w:
            D = (1 << A)-L
            counts['words'] += 1
            counts['positive_rational_words' if D>0 else 'negative_rational_words'] += 1
            if C % D == 0:
                counts['integral_words'] += 1
                if D > 0:
                    positives.append({'word':list(w),'fixed_value':C//D})
                elif len(negative_integral) < 30:
                    negative_integral.append({'word':list(w),'fixed_value':C//D})
        for a in range(1,A_max-A+1):
            stack.append((w+(a,),A+a,3*L,3*C+(1 << A)))
    need(counts['words'] == (1 << A_max)-1,'complete composition count failed')
    return {'sum_bound':A_max,'counts':dict(sorted(counts.items())),
            'positive_integral_words':sorted(positives,key=lambda z:(len(z['word']),z['word'])),
            'negative_integral_sample':negative_integral,
            'all_words_visited':True,'asymptotic_claim':False}


def clean_counter(c: Counter) -> dict[int,int]:
    return {n:k for n,k in sorted(c.items()) if k}


class DescentCompression:
    """A literal chain-homotopy retraction from checked finite descent paths.

    Unlisted vertices remain individual roots. No overflow is collapsed.
    H(n) is an actual edge chain from n to root(n); P1=I-H*boundary.
    """
    def __init__(self, words: dict[int,tuple[int,...]], c: int = 1):
        need(c in (1,-1), 'unsupported forcing')
        self.c = c
        self.records: dict[int,tuple[int,dict[int,int]]] = {}
        self.cache: dict[int,tuple[int,dict[int,int]]] = {1:(1,{})}
        for n,word in sorted(words.items()):
            need(n > 1 and n % 2 == 1 and bool(word), 'nontrivial positive source and word required')
            x,chain = n,Counter()
            for a in word:
                need(x != 1, 'descent path must end when it reaches the basepoint')
                y,b = step(x,c)
                need(a == b, 'descent path uses a false exponent')
                chain[x] += 1
                x = y
            need(x < n, 'path is not a strict descent')
            self.records[n] = (x,clean_counter(chain))
        # Since every endpoint is smaller, sorted evaluation is an exact finite recursion.
        for n,(y,path) in sorted(self.records.items()):
            root,tail = self.resolve(y)
            chain = Counter(path); chain.update(tail)
            self.cache[n] = (root,clean_counter(chain))

    def resolve(self,n: int) -> tuple[int,dict[int,int]]:
        step(n,self.c)
        if n in self.cache:
            root,chain = self.cache[n]
            return root,dict(chain)
        need(n not in self.records, 'certificate recursion was not evaluated in order')
        return n,{}

    def project_vertices(self,vertices: dict[int,int]) -> dict[int,int]:
        out = Counter()
        for n,k in vertices.items():
            root,_ = self.resolve(n)
            if root != 1:
                out[root] += k
        return clean_counter(out)

    def homotopy(self,vertices: dict[int,int]) -> dict[int,int]:
        out = Counter()
        for n,k in vertices.items():
            _,path = self.resolve(n)
            for v,m in path.items(): out[v] += k*m
        return clean_counter(out)

    def project_edges(self,chain: dict[int,int]) -> dict[int,int]:
        boundary = sparse_boundary(chain,self.c)
        out = Counter(chain)
        out.subtract(self.homotopy(boundary))
        return clean_counter(out)


class StoppedDescentCompression(DescentCompression):
    """Apply the preserved predecessor observer to its whole infinite source.

    Evaluation is lazy and finite for every queried positive integer. A root
    beyond this exponent-sum cutoff remains an actual unresolved source.
    """
    def __init__(self, cutoff: int):
        need(type(cutoff) is int and cutoff >= 0, 'nonnegative integer cutoff required')
        import importlib.util
        import sys
        name = '_preserved_stopped_affine_observer'
        if name not in sys.modules:
            source = Path(__file__).resolve().parent.parent/'stopped_affine_transport_20260914'/'verify.py'
            need(source.is_file(), 'preserved stopped-affine predecessor is required')
            spec = importlib.util.spec_from_file_location(name,source)
            need(spec is not None and spec.loader is not None, 'predecessor module unavailable')
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            spec.loader.exec_module(module)
        self.observer = sys.modules[name].observe
        self.c,self.cutoff = 1,cutoff
        self.records = {}
        self.cache = {1:(1,{})}

    def resolve(self,n: int) -> tuple[int,dict[int,int]]:
        step(n)
        trail=[]; x=n
        while x not in self.cache:
            observed=self.observer(x,self.cutoff)
            if observed is None:
                self.cache[x]=(x,{})
                break
            p,_=observed
            block=path_from_word(x,p.word)
            need(block['strict_descent'], 'predecessor block does not strictly descend')
            y=block['terminal']
            chain={int(k):v for k,v in block['relative_chain'].items()}
            self.records[x]=(y,chain)
            trail.append(x)
            x=y
        for v in reversed(trail):
            y,chain=self.records[v]
            root,tail=self.cache[y]
            combined=Counter(chain); combined.update(tail)
            self.cache[v]=(root,clean_counter(combined))
        root,chain=self.cache[n]
        return root,dict(chain)

    def certificate(self,n: int) -> dict:
        root,chain=self.resolve(n)
        boundary=sparse_boundary(chain)
        expected=Counter()
        if n != 1: expected[n]+=1
        if root != 1: expected[root]-=1
        need(boundary==clean_counter(expected), 'stopped compression boundary failed')
        return {'source':n,'exponent_cutoff':self.cutoff,'root':root,
                'root_status':'basepoint' if root==1 else 'unresolved_at_exponent_cutoff',
                'chain':{str(k):v for k,v in chain.items()},
                'boundary':{str(k):v for k,v in boundary.items()},
                'retained_predecessor_observer':True}


def validate_cycle_certificate(cert: dict) -> None:
    need(isinstance(cert,dict), 'certificate must be a dictionary')
    expected = cycle_certificate(cert.get('word',()),cert.get('forcing_c',0))
    need(cert == expected, 'cycle certificate differs from exact reconstruction')


def validate_path_certificate(cert: dict) -> None:
    need(isinstance(cert,dict), 'certificate must be a dictionary')
    expected = path_certificate(cert.get('start',0),cert.get('returns_recorded',-1),
                                cert.get('forcing_c',0))
    need(cert == expected, 'path certificate differs from exact reconstruction')


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest='mode',required=True)
    cp = sub.add_parser('cycle')
    cp.add_argument('word',type=int,nargs='+')
    cp.add_argument('--forcing',type=int,choices=[1,-1],default=1)
    cp.add_argument('--output',type=Path)
    pp = sub.add_parser('path')
    pp.add_argument('start',type=int)
    pp.add_argument('--cap',type=int,default=100000)
    pp.add_argument('--forcing',type=int,choices=[1,-1],default=1)
    pp.add_argument('--output',type=Path)
    gp = sub.add_parser('graph')
    gp.add_argument('sources',type=int,nargs='+')
    gp.add_argument('--forcing',type=int,choices=[1,-1],default=1)
    gp.add_argument('--output',type=Path)
    hp = sub.add_parser('compress')
    hp.add_argument('start',type=int)
    hp.add_argument('--cutoff',type=int,default=16)
    hp.add_argument('--output',type=Path)
    ep = sub.add_parser('enumerate')
    ep.add_argument('--sum-bound',type=int,default=18)
    ep.add_argument('--output',type=Path)
    args = ap.parse_args()
    try:
        if args.mode == 'cycle': result=cycle_certificate(args.word,args.forcing)
        elif args.mode == 'path': result=path_certificate(args.start,args.cap,args.forcing)
        elif args.mode == 'graph': result=finite_graph_certificate(args.sources,args.forcing)
        elif args.mode == 'compress': result=StoppedDescentCompression(args.cutoff).certificate(args.start)
        else: result=enumerate_words(args.sum_bound)
    except CertificateError as exc:
        ap.error(str(exc))
    text = json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output:
        args.output.write_text(text,encoding='utf-8')
    else:
        print(text,end='')


if __name__ == '__main__':
    main()
