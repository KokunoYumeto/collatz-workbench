#!/usr/bin/env python3
"""Original-source bilateral Collatz joins and explicit support bounds.

Source formulas continue the integral first-jet and ternary-layer workbenches.
A join compares TWO original paths. It is not a forward iterate from the larger
source to the smaller source. All tests remain active under python -O.
"""
from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
from math import gcd
from pathlib import Path
from typing import Iterable, Mapping
import argparse
import hashlib
import json

class CertificateError(ValueError):
    pass

def need(ok: bool, message: str) -> None:
    if not ok:
        raise CertificateError(message)

def odd(n: int) -> None:
    need(type(n) is int and n > 0 and n % 2 == 1, 'positive original odd integer required')

def step(n: int) -> tuple[int, int]:
    odd(n)
    x = 3*n+1
    a = (x & -x).bit_length()-1
    return x >> a, a

def divided_step(n: int) -> tuple[int, int]:
    odd(n)
    x, a = 3*n+1, 0
    while x % 2 == 0:
        x //= 2
        a += 1
    return x, a

def v3(n: int) -> int:
    need(type(n) is int and n > 0, 'positive integer required for nu_3')
    b = 0
    while n % 3 == 0:
        n //= 3
        b += 1
    return b

def floor_log3(n: int) -> int:
    need(type(n) is int and n >= 1, 'positive height required')
    b, power = 0, 1
    while power*3 <= n:
        power *= 3
        b += 1
    return b

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
    def m(self) -> int:
        return len(self.word)
    @property
    def rho(self) -> int:
        return ((self.U-self.C)*pow(self.L, -1, 2*self.U)) % (2*self.U)
    @property
    def eta(self) -> int:
        return (self.L*self.rho+self.C)//self.U

def packet(word: Iterable[int]) -> Packet:
    w = tuple(word)
    A, L, C = 0, 1, 0
    for a in w:
        need(type(a) is int and a >= 1, 'positive integral original exponents required')
        C, L, A = 3*C+(1 << A), 3*L, A+a
    return Packet(w, A, L, C)

def path(n: int, word: Iterable[int]) -> list[int]:
    odd(n)
    values = [n]
    for a in word:
        x, b = divided_step(values[-1])
        need(a == b, 'word is not the original valuation word')
        values.append(x)
    return values

def crt_pair(a: int, q: int, b: int, r: int) -> tuple[int, int]:
    need(all(type(x) is int for x in (a,q,b,r)) and q > 0 and r > 0, 'integer congruences required')
    g = gcd(q, r)
    need((b-a) % g == 0, 'incompatible original congruences')
    modulus = q*(r//g)
    k = ((b-a)//g * pow(q//g, -1, r//g)) % (r//g) if r//g > 1 else 0
    value = (a+q*k) % modulus
    need((value-a) % q == 0 and (value-b) % r == 0, 'CRT image mismatch')
    return value, modulus

def join_family(left: Iterable[int], right: Iterable[int]) -> dict:
    """Complete original target intersection and exact positive-height interval."""
    l, r = packet(left), packet(right)
    g = gcd(l.L, r.L)
    out = {'left_word': list(l.word), 'right_word': list(r.word),
           'left_data': [l.L,l.U,l.C,l.rho,l.eta],
           'right_data': [r.L,r.U,r.C,r.rho,r.eta],
           'signed_clock': l.m-r.m, 'declared_comparison_retained': True}
    if (r.eta-l.eta) % (2*g):
        return {**out, 'compatible': False, 'domain': None}
    residue, period = crt_pair(l.eta, 2*l.L, r.eta, 2*r.L)
    lower = max(l.eta, r.eta)
    y0 = residue + ((lower-residue+period-1)//period)*period
    ul, ur = (y0-l.eta)//(2*l.L), (y0-r.eta)//(2*r.L)
    n0, m0 = l.rho+2*l.U*ul, r.rho+2*r.U*ur
    ns, ms = 2*l.U*(r.L//g), 2*r.U*(l.L//g)
    c, d = n0-m0, ns-ms
    if d > 0:
        domain = [max(0, (-c)//d+1), None]
    elif d == 0:
        domain = [0, None] if c > 0 else None
    else:
        domain = [0, (c-1)//(-d)] if c > 0 else None
    return {**out, 'compatible': True, 'n0':n0, 'nstep':ns,
            'm0':m0, 'mstep':ms, 'y0':y0, 'ystep':period,
            'left_parameter':[ul,r.L//g], 'right_parameter':[ur,l.L//g],
            'height_constant':c, 'height_slope':d, 'domain':domain}

# Integral dual-number vectors. No cycle period or odd integer is inverted.
Dual = tuple[int, int]
Vector = dict[int, Dual]
ZERO, ONE = (0,0), (1,0)

def addc(a: Dual, b: Dual) -> Dual:
    return a[0]+b[0], a[1]+b[1]

def mulc(a: Dual, b: Dual) -> Dual:
    return a[0]*b[0], a[0]*b[1]+a[1]*b[0]

def qpower(k: int) -> Dual:
    need(type(k) is int, 'signed integral clock required')
    return 1, k

def add_vectors(*vectors: Mapping[int,Dual]) -> Vector:
    out: Vector = {}
    for vector in vectors:
        for n,a in vector.items():
            odd(n)
            need(isinstance(a,tuple) and len(a)==2 and all(type(x) is int for x in a), 'integral dual coefficient required')
            out[n] = addc(out.get(n,ZERO), a)
    return {n:a for n,a in sorted(out.items()) if a != ZERO}

def scale(a: Dual, vector: Mapping[int,Dual]) -> Vector:
    return {n:c for n,b in sorted(vector.items()) if (c := mulc(a,b)) != ZERO}

def jet_d(vector: Mapping[int,Dual]) -> Vector:
    out: Vector = {}
    for n,a in vector.items():
        y,_ = step(n)
        b = mulc(qpower(1), a)
        out = add_vectors(out,{n:a},{y:(-b[0],-b[1])})
    return out

def weighted_path(values: list[int]) -> Vector:
    out: Vector = {}
    for j,n in enumerate(values[:-1]):
        need(step(n)[0] == values[j+1], 'false original path edge')
        out = add_vectors(out,{n:qpower(j)})
    return out

@dataclass(frozen=True)
class Move:
    source: int
    target: int
    clock: int
    chain: Vector
    left_word: tuple[int,...]
    right_word: tuple[int,...]
    left_values: tuple[int,...]
    right_values: tuple[int,...]
    rule: str

def make_move(n: int, m: int, left: Iterable[int], right: Iterable[int], rule: str) -> Move:
    odd(n); odd(m)
    need(m < n, 'original source height must strictly decrease')
    l, r = tuple(left), tuple(right)
    lv, rv = path(n,l), path(m,r)
    need(lv[-1] == rv[-1], 'original targets do not coincide')
    k = len(l)-len(r)
    chain = add_vectors(weighted_path(lv),scale((-1,-k),weighted_path(rv)))
    expected = add_vectors({n:ONE},{m:(-1,-k)})
    need(jet_d(chain) == expected, 'original first-jet boundary mismatch')
    return Move(n,m,k,chain,l,r,tuple(lv),tuple(rv),rule)

def family_move(family: dict, t: int, rule: str='bilateral_catalogue') -> Move:
    need(type(t) is int and t >= 0, 'nonnegative integral family parameter required')
    need(family == join_family(family['left_word'], family['right_word']), 'altered original family record')
    domain = family['domain']
    need(domain is not None and t >= domain[0] and (domain[1] is None or t <= domain[1]), 'parameter outside complete height domain')
    return make_move(family['n0']+family['nstep']*t,
                     family['m0']+family['mstep']*t,
                     family['left_word'],family['right_word'],rule)

@lru_cache(maxsize=None)
def layer_family(b: int, e: int, bilateral: bool) -> dict:
    """One FULL original congruence family, with no cap on the ternary layer."""
    need(type(b) is int and b >= 1 and type(e) is int and e in (2,6), 'layer b>=1 and original e=2 or 6 required')
    need(type(bilateral) is bool, 'explicit layer-map selector required')
    shift = 1 if bilateral else 0
    a = 1
    while (1 << (a+e+2*b-shift)) >= 3**(a+b):
        a += 1
    Q, J, h = 3**(a+b), 1 << (e+2*b-shift), (2**e+2)//3
    K = 1 << (a+e+2*b-shift)
    residue = (-h*3**b*pow(J,-1,Q)) % Q
    n0, ns = crt_pair(residue,Q,27 if bilateral else 3,32 if bilateral else 4)
    need(n0 > 0, 'canonical family source must be positive')
    numerator = K*n0+2**a*h*3**b
    need(numerator % Q == 0, 'original smaller-source integrality failed')
    m0, ms = numerator//Q-1, ns*K//Q
    left = (1,2,1) if bilateral else (1,)
    right = (1,)*a+(e,)+(2,)*(b-1)+((1,1,3) if bilateral else (3,))
    lp = packet(left)
    y0, ys = (lp.L*n0+lp.C)//lp.U, lp.L*ns//lp.U
    need(0 < m0 < n0 and ms < ns, 'layer height inequality failed')
    need(v3(n0)==b and ns % 3**(b+1)==0, 'actual ternary layer lost')
    return {'b':b,'e':e,'bilateral':bilateral,'a':a,'Q':Q,'J':J,'K':K,'h':h,
            'left_word':list(left),'right_word':list(right),'n0':n0,'nstep':ns,
            'm0':m0,'mstep':ms,'y0':y0,'ystep':ys,
            'ternary_unit':(n0//3**b)%3,'signed_clock':len(left)-len(right),
            'height_constant':n0-m0,'height_slope':ns-ms,
            'domain':[0,None],'parameter_inverse':'(n-n0)/nstep on the original source image'}

def layer_move(n: int, bilateral: bool) -> Move | None:
    odd(n)
    if n % 3 or (n % 32 != 27 if bilateral else n % 4 != 3):
        return None
    b = v3(n)
    unit = (n//3**b) % 3
    e = (2 if unit==2 else 6) if bilateral else (2 if unit==1 else 6)
    f = layer_family(b,e,bilateral)
    if (n-f['n0']) % f['nstep']:
        return None
    t = (n-f['n0'])//f['nstep']
    need(t >= 0, 'positive source before canonical representative')
    if bilateral:
        # All longer admitted leading runs are nested original-source strata.
        # Use the MAXIMAL one; its peak is unchanged and its source is smaller.
        Z = f['J']*(n//3**b)+f['h']
        a_max = v3(Z)
        need(a_max >= f['a'], 'admitted source lost its leading-run congruence')
        m = 2**a_max*(Z//3**a_max)-1
        right = (1,)*a_max+(e,)+(2,)*(b-1)+(1,1,3)
        return make_move(n,m,f['left_word'],right,'bilateral_layer_maximal')
    return make_move(n,f['m0']+f['mstep']*t,f['left_word'],f['right_word'],'published_layer')


def saturation_stratum(b: int, e: int, extra: int, unit: int) -> dict:
    """Exact all-depth partition of the original bilateral family parameter."""
    need(type(extra) is int and extra >= 0 and type(unit) is int and unit in (1,2),
         'nonnegative extra depth and ternary unit 1 or 2 required')
    f = layer_family(b,e,True)
    W0 = (f['J']*(f['n0']//3**b)+f['h'])//3**f['a']
    slope = 32*f['J']
    modulus = 3**(extra+1)
    t0 = ((3**extra*unit-W0)*pow(slope,-1,modulus)) % modulus
    n0 = f['n0']+f['nstep']*t0
    nstep = f['nstep']*modulus
    a = f['a']+extra
    w = (W0+slope*t0)//3**extra
    need(w % 3 == unit and w % 2 == 0 and w % 4 == 2,
         'original maximal-run unit or parity mismatch')
    m0 = 2**a*w-1
    mstep = 2**a*slope*3
    left = tuple(f['left_word'])
    right = (1,)*a+(e,)+(2,)*(b-1)+(1,1,3)
    lp=packet(left)
    need(m0 < n0 and mstep < nstep, 'saturated height inequality failed')
    return {'b':b,'e':e,'extra_depth':extra,'unit':unit,'a_min':f['a'],
            'a_max':a,'parent_parameter_anchor':t0,'parent_parameter_step':modulus,
            'W0':W0,'parent_defect_slope':slope,
            'n0':n0,'nstep':nstep,'m0':m0,'mstep':mstep,
            'y0':(lp.L*n0+lp.C)//lp.U,'ystep':lp.L*nstep//lp.U,
            'left_word':list(left),'right_word':list(right),'signed_clock':len(left)-len(right),
            'height_constant':n0-m0,'height_slope':nstep-mstep,
            'parameter_domain':'s is an integer >= 0',
            'maximality_equation':'nu_3(W0+32*J*t) = extra_depth'}


def words_length_sum_le(length: int, total: int):
    def visit(prefix: tuple[int,...], remaining: int, budget: int):
        if remaining == 0:
            yield prefix
            return
        for a in range(1,budget-remaining+2):
            yield from visit(prefix+(a,),remaining-1,budget-a)
    yield from visit((),length,total)

OLD_PERIOD = 4*3**11
NEW_PERIOD = 8*OLD_PERIOD
LEFTS = ((1,1),(1,2),(1,1,1),(1,1,2),(1,2,1))
INVERSES = ((1,),(1,2),(1,1,1,2,1,1,4))

def old_arithmetic_root(n: int) -> bool:
    return n==1 or (n%36 in (3,7,15,19,27) and n%8748!=8731 and n%2916!=1731)

def compact(obj: object) -> bytes:
    return (json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n').encode()

@lru_cache(maxsize=1)
def catalogues() -> dict:
    """Reconstruct both complete finite word domains; preserve all candidate masks."""
    roots = bytearray(OLD_PERIOD)
    for n in range(3,OLD_PERIOD,4):
        roots[n] = old_arithmetic_root(n)
    start_count = sum(roots)
    old_candidates = []
    for k in range(2,13):
        for w in words_length_sum_le(k,(3**(k-1)).bit_length()):
            if w[-1] % 2 == 0:
                continue
            f = join_family((1,),w)
            need(f['compatible'] and f['domain']==[0,None], 'published catalogue theorem failed')
            old_candidates.append(f)
    old_candidates.sort(key=lambda f:(f['nstep'],f['n0'],sum(f['right_word']),f['right_word']))
    old_selected = []
    old_digest = hashlib.sha256()
    for f in old_candidates:
        view = roots[f['n0']::f['nstep']]
        added = sum(view)
        old_digest.update(compact([f,added]))
        if added:
            roots[f['n0']::f['nstep']] = b'\0'*len(view)
            old_selected.append(f)
    old_mask = bytes(roots)
    roots *= 8
    before = sum(roots)
    pairs = 0
    compatible = []
    domain_digest = hashlib.sha256()
    for lw in LEFTS:
        l = packet(lw)
        for k in range(1,13):
            limit = l.A + (3**max(0,k-l.m)).bit_length()-1
            while limit >= 0 and (1<<limit)*l.L >= l.U*3**k:
                limit -= 1
            if limit < k:
                continue
            for rw in words_length_sum_le(k,limit):
                pairs += 1
                f = join_family(lw,rw)
                domain_digest.update(compact(f))
                if f['compatible'] and f['domain'] is not None:
                    need(f['domain'][1] is None, 'strict slope domain unexpectedly bounded')
                    compatible.append(f)
    compatible.sort(key=lambda f:(f['nstep'],f['n0']+f['nstep']*f['domain'][0],
                                   len(f['left_word'])+len(f['right_word']),f['left_word'],f['right_word']))
    selected, stage_records = [], []
    for f in compatible:
        nmin = f['n0']+f['nstep']*f['domain'][0]
        residue = nmin % f['nstep']
        view = roots[residue::f['nstep']]
        added = sum(view)
        stage_records.append([f['left_word'],f['right_word'],residue,f['nstep'],added])
        if added:
            need(f['domain']==[0,None] and 0 < f['n0'] < f['nstep'], 'selected family is not a full positive residue class')
            roots[residue::f['nstep']] = b'\0'*len(view)
            selected.append(f)
    return {'old_candidates':old_candidates,'old_selected':old_selected,
            'old_mask':old_mask,'new_mask':bytes(roots),'selected':selected,
            'compatible_candidates':compatible,'stage_records':stage_records,
            'summary':{'old_start_roots':start_count,'old_candidate_words':len(old_candidates),
                'old_selected_families':len(old_selected),'old_root_residues':sum(old_mask),
                'new_period':NEW_PERIOD,'old_lifted_roots':before,'new_root_residues':sum(roots),
                'new_removed_residues':before-sum(roots),'ordered_pairs':pairs,
                'compatible_pairs':len(compatible),'new_selected_families':len(selected),
                'old_mask_sha256':hashlib.sha256(old_mask).hexdigest(),
                'new_mask_sha256':hashlib.sha256(roots).hexdigest(),
                'old_candidate_status_sha256':old_digest.hexdigest(),
                'all_pair_records_sha256':domain_digest.hexdigest(),
                'all_compatible_selection_records_sha256':hashlib.sha256(b''.join(compact(x) for x in stage_records)).hexdigest()}}

@lru_cache(maxsize=1)
def lookup_tables() -> tuple[dict,dict]:
    c = catalogues()
    def table(families):
        result = {}
        for f in families:
            result.setdefault(f['nstep'],{})[f['n0']] = f
        return result
    return table(c['old_selected']), table(c['selected'])

def catalogue_move(n: int, new: bool) -> Move | None:
    table = lookup_tables()[1 if new else 0]
    for modulus, faces in table.items():
        f = faces.get(n % modulus)
        if f is not None:
            return family_move(f,(n-f['n0'])//modulus,
                               'bilateral_catalogue' if new else 'published_catalogue')
    return None

def choose_move(n: int, stage: int=2) -> Move | None:
    odd(n)
    need(type(stage) is int and stage in (0,1,2), 'stage 0=published, 1=bilateral finite, 2=both new constructions')
    if n == 1:
        return None
    y,a = step(n)
    if y < n:
        return make_move(n,y,(a,),(),'forward')
    for word in INVERSES:
        p = packet(word)
        numerator = p.U*n-p.C
        if numerator > 0 and numerator % p.L == 0:
            x = numerator//p.L
            if x > 0 and x % 2 and x < n:
                return make_move(n,x,(),word,'inverse')
    if n >= 1731 and (n-1731) % 2916 == 0:
        return layer_move(n,False)
    move = catalogue_move(n,False)
    if move is not None:
        return move
    move = layer_move(n,False)
    if move is not None or stage == 0:
        return move
    move = catalogue_move(n,True)
    if move is not None or stage == 1:
        return move
    return layer_move(n,True)

def root_test(n: int, stage: int=2) -> bool:
    odd(n)
    need(stage in (0,1,2), 'invalid root stage')
    if n == 1:
        return True
    c = catalogues()
    if not c['old_mask'][n % OLD_PERIOD]:
        return False
    if layer_move(n,False) is not None:
        return False
    if stage == 0:
        return True
    if not c['new_mask'][n % NEW_PERIOD]:
        return False
    return stage == 1 or layer_move(n,True) is None

def support_bound(n: int) -> int:
    need(type(n) is int and n >= 1, 'positive source height required')
    b = floor_log3(n)
    return max(130*(n+1),64*n*4**b//3**b+21)

def term_bound(n: int) -> int:
    need(type(n) is int and n >= 1, 'positive source height required')
    return ((n-1)//2)*(3*floor_log3(n)+14)

class Retraction:
    """Global finite-column retraction; every selected source height decreases."""
    def __init__(self, stage: int=2):
        need(type(stage) is int and stage in (0,1,2), 'invalid retraction stage')
        self.stage = stage
        self.cache = {1:(1,0,{},0,1)}
    def resolve(self,n: int):
        odd(n)
        trail, x = [], n
        while x not in self.cache:
            move = choose_move(x,self.stage)
            if move is None:
                self.cache[x]=(x,0,{},0,x)
                break
            trail.append(move)
            x = move.target
        for move in reversed(trail):
            root,k,chain,count,peak = self.cache[move.target]
            newchain = add_vectors(move.chain,scale(qpower(move.clock),chain))
            newcount = count+len(move.left_word)+len(move.right_word)
            newpeak = max(peak,*move.left_values,*move.right_values)
            self.cache[move.source]=(root,k+move.clock,newchain,newcount,newpeak)
        r,k,h,count,peak = self.cache[n]
        return r,k,dict(h),count,peak
    def H(self,v: Mapping[int,Dual]) -> Vector:
        out: Vector = {}
        for n,a in v.items():
            _,_,h,_,_ = self.resolve(n)
            out = add_vectors(out,scale(a,h))
        return out
    def Q(self,v: Mapping[int,Dual]) -> Vector:
        out: Vector = {}
        for n,a in v.items():
            r,k,_,_,_ = self.resolve(n)
            out = add_vectors(out,{r:mulc(a,qpower(k))})
        return out
    def F(self,v: Mapping[int,Dual]) -> Vector:
        return add_vectors(v,scale((-1,0),self.H(jet_d(v))))
    def certificate(self,n: int) -> dict:
        root,k,h,count,peak = self.resolve(n)
        need(jet_d(h)==add_vectors({n:ONE},{root:(-1,-k)}), 'retraction column boundary failed')
        need(count <= term_bound(n) and peak <= support_bound(n), 'global support/term bound failed')
        need(sum(abs(x[0]) for x in h.values())<=count, 'constant coefficient bound failed')
        need(sum(abs(x[1]) for x in h.values())<=count*count, 'first-order coefficient bound failed')
        moves=[];x=n
        while (mv:=choose_move(x,self.stage)) is not None:
            moves.append({'source':x,'smaller_source':mv.target,'signed_clock':mv.clock,
                          'rule':mv.rule,'left_word':list(mv.left_word),'right_word':list(mv.right_word),
                          'left_path':list(mv.left_values),'right_path':list(mv.right_values)})
            x=mv.target
        return {'source':n,'root':root,'stage':self.stage,'signed_clock':k,
                'moves':moves,'original_chain':{str(i):list(a) for i,a in h.items()},
                'uncollected_terms':count,'original_odd_vertex_peak':peak,
                'proved_term_bound':term_bound(n),'proved_support_bound':support_bound(n),
                'status':'reduced_to_basepoint' if root==1 else 'retained_original_root'}

# Same sharp word-domain envelope, derived again in the accompanying note.
def envelope(horizon: int) -> dict:
    need(type(horizon) is int and 1<=horizon<=1000000, 'horizon must be 1..1000000')
    L,C,maximum=1,0,0
    rows,records,floors=[],[],[0]
    digest=hashlib.sha256()
    for m in range(1,horizon+1):
        C=3*C+(1<<(L.bit_length()-1));L*=3
        exponent=L.bit_length();D=(1<<exponent)-L
        bound=C//D;row=[m,exponent,bound]
        rows.append(row);floors.append(exponent-1)
        for z in (m,exponent,C,D):
            data=z.to_bytes(max(1,(z.bit_length()+7)//8),'big')
            digest.update(len(data).to_bytes(8,'big'));digest.update(data)
        if bound>maximum:maximum=bound;records.append(row)
    return {'horizon':horizon,'maximum_integer_candidate':maximum,
            'maximum_odd_candidate':maximum if maximum%2 else maximum-1,
            'record_rows':records,'rows_m_crossing_sum_candidate_bound':rows,
            'critical_floor_prefix_sums':floors,'exact_big_integer_state_sha256':digest.hexdigest(),
            'uses_transcendence_or_logarithm_estimate':False}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    sub=ap.add_subparsers(dest='command',required=True)
    p=sub.add_parser('layer');p.add_argument('b',type=int);p.add_argument('e',type=int,choices=(2,6));p.add_argument('--old',action='store_true')
    p=sub.add_parser('reduce');p.add_argument('source',type=int);p.add_argument('--stage',type=int,choices=(0,1,2),default=2)
    sub.add_parser('catalogue')
    p=sub.add_parser('envelope');p.add_argument('--horizon',type=int,default=11610)
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    try:
        if args.command=='layer':result=layer_family(args.b,args.e,not args.old)
        elif args.command=='reduce':result=Retraction(args.stage).certificate(args.source)
        elif args.command=='catalogue':result=catalogues()['summary']
        else:result=envelope(args.horizon)
        text=json.dumps(result,sort_keys=True,indent=2)+'\n'
        if args.output:args.output.write_text(text,encoding='utf-8')
        else:print(text,end='')
    except CertificateError as exc:
        ap.error(str(exc))
if __name__=='__main__':
    main()
