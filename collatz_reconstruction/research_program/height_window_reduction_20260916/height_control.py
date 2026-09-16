#!/usr/bin/env python3
"""Exact first-crossing envelopes and integral bidirectional source reduction.

All numerical sources use the original +1 odd-return Collatz map. A reverse
reduction is certified by an ORIGINAL forward path from a smaller source;
it is not claimed to be a forward iterate of its target. Dual coefficients
live in Z[epsilon]/epsilon^2, with (1+epsilon)^k = 1+k*epsilon for any integer k.
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from typing import Iterable, Mapping

class CertificateError(ValueError):
    pass

def need(condition: bool, message: str) -> None:
    if not condition:
        raise CertificateError(message)

def odd(n: int) -> None:
    need(type(n) is int and n > 0 and n % 2 == 1, 'original positive odd integer required')

def step(n: int) -> tuple[int,int]:
    odd(n)
    z=3*n+1
    a=(z & -z).bit_length()-1
    return z >> a,a

def divided_step(n: int) -> tuple[int,int]:
    odd(n)
    z=3*n+1; a=0
    while z%2==0:
        z//=2; a+=1
    return z,a

@dataclass(frozen=True)
class Packet:
    word: tuple[int,...]
    A: int
    L: int
    C: int
    @property
    def U(self) -> int: return 1 << self.A
    @property
    def m(self) -> int: return len(self.word)
    @property
    def rho(self) -> int:
        return ((self.U-self.C)*pow(self.L,-1,2*self.U))%(2*self.U)
    @property
    def eta(self) -> int:
        return (self.L*self.rho+self.C)//self.U

def packet(word: Iterable[int]) -> Packet:
    w=tuple(word); A=0;L=1;C=0
    for a in w:
        need(type(a) is int and a>=1, 'positive integer exponents required')
        C=3*C+(1<<A); L*=3; A+=a
    return Packet(w,A,L,C)

def path(n: int, word: Iterable[int]) -> list[int]:
    odd(n); values=[n]
    for a in word:
        y,b=divided_step(values[-1]); need(a==b,'not the original valuation word')
        values.append(y)
    return values


def first_crossing(n: int, cap: int=10000) -> dict:
    odd(n);need(type(cap) is int and cap>=1,'positive cap required')
    x=n; A=0;L=1; w=[]; peak=n
    for j in range(1,cap+1):
        x,a=step(x); w.append(a); A+=a;L*=3;peak=max(peak,x)
        if (1<<A)>L:
            return {'source':n,'endpoint':x,'word':w,'returns':j,'A':A,
                    'strict_descent':x<n,'peak':peak,'status':'first_coefficient_crossing'}
        need(x>n,'positive affine forcing violated before coefficient crossing')
    return {'source':n,'endpoint':x,'word':w,'returns':cap,'A':A,
            'strict_descent':False,'peak':peak,'status':'unresolved_at_cap'}


def envelope(horizon: int) -> dict:
    """Sharp maximum C/(2^A-3^m) over FIRST-crossing words of each length.

    The maximizing proper prefix sums are floor(log_2 3^j), computed as
    bit_length(3^j)-1. No floating-point logarithm or large-gap theorem.
    Every row retains its explicit critical exponent word by the common
    prefix-sum dictionary and a last crossing exponent.
    """
    need(type(horizon) is int and 1<=horizon<=1000000,'horizon must be 1..1000000')
    L=1;C=0; maximum=0; floor_sums=[0];rows=[];records=[]
    state_hash=hashlib.sha256()
    def record_int(n: int) -> None:
        b=n.to_bytes(max(1,(n.bit_length()+7)//8),'big')
        state_hash.update(len(b).to_bytes(8,'big'));state_hash.update(b)
    for m in range(1,horizon+1):
        previous_floor=L.bit_length()-1
        C=3*C+(1<<previous_floor); L*=3
        crossing_sum=L.bit_length(); D=(1<<crossing_sum)-L
        bound=C//D
        row=[m,crossing_sum,bound]
        rows.append(row);floor_sums.append(crossing_sum-1)
        for z in (m,crossing_sum,C,D):record_int(z)
        if bound>maximum:
            maximum=bound; records.append(row)
    return {'horizon':horizon,'original_forcing':1,'maximum_integer_candidate':maximum,
            'maximum_odd_candidate':maximum if maximum%2 else maximum-1,
            'rows_m_crossing_sum_candidate_bound':rows,'record_rows':records,
            'critical_floor_prefix_sums':floor_sums,'exact_big_integer_state_sha256':state_hash.hexdigest(),
            'maximizer_word_rule':'successive floor-prefix differences, then crossing_sum minus previous floor',
            'uses_transcendence_or_logarithm_estimate':False}


def crt_pair(a: int, q: int, b: int, r: int) -> tuple[int,int]:
    """Exact pullback of two congruences; no independence assumption."""
    from math import gcd
    need(all(type(x) is int for x in (a,q,b,r)) and q>0 and r>0,'positive integral moduli required')
    g=gcd(q,r);need((b-a)%g==0,'incompatible source congruences')
    modulus=q*(r//g)
    k=((b-a)//g*pow(q//g,-1,r//g))%(r//g) if r//g>1 else 0
    x=(a+q*k)%modulus
    need((x-a)%q==0 and (x-b)%r==0,'CRT pullback equation failed')
    return x,modulus


def inverse_family(word: Iterable[int]) -> dict:
    p=packet(word);need(p.m>0 and p.L>p.U,'expanding original word required')
    rho=p.rho;eta=p.eta
    need(rho>0 and eta>rho,'expanding affine source must strictly increase')
    return {'word':list(p.word),'A':p.A,'L':p.L,'U':p.U,'C':p.C,
            'smaller_source_anchor':rho,'smaller_source_step':2*p.U,
            'reduced_from_anchor':eta,'reduced_from_step':2*p.L,
            'inverse_formula':'(U*n-C)/L','parameter_domain':'v is an integer >= 0',
            'comparison_direction':'original forward path runs from smaller source to reduced-from target',
            'net_firstjet_clock':-p.m}

# Coefficients are (constant, epsilon coefficient); each basis stays original.
Dual=tuple[int,int]
Vector=dict[int,Dual]
ZERO=(0,0);ONE=(1,0)

def plus(a: Dual,b: Dual) -> Dual:return a[0]+b[0],a[1]+b[1]
def times(a: Dual,b: Dual) -> Dual:return a[0]*b[0],a[0]*b[1]+a[1]*b[0]
def neg(a: Dual) -> Dual:return -a[0],-a[1]
def power(k: int) -> Dual:return 1,k

def add_vectors(*vectors: Mapping[int,Dual]) -> Vector:
    out: Vector={}
    for v in vectors:
        for n,a in v.items():
            odd(n);need(isinstance(a,tuple) and len(a)==2 and all(type(k) is int for k in a),'integral dual coefficient required')
            out[n]=plus(out.get(n,ZERO),a)
    return {n:a for n,a in sorted(out.items()) if a!=ZERO}

def scale(a: Dual,v: Mapping[int,Dual]) -> Vector:
    return {n:z for n,b in sorted(v.items()) if (z:=times(a,b))!=ZERO}

def jet_d(v: Mapping[int,Dual]) -> Vector:
    out: Vector={}
    for n,a in v.items():
        y,_=step(n)
        out=add_vectors(out,{n:a},{y:neg(times(power(1),a))})
    return out

def weighted_path(values: list[int]) -> Vector:
    need(bool(values),'nonempty vertex list required')
    out: Vector={}
    for j,n in enumerate(values[:-1]):
        need(step(n)[0]==values[j+1],'path edge is not original Collatz')
        out=add_vectors(out,{n:power(j)})
    return out

@dataclass(frozen=True)
class Move:
    source: int
    target: int
    clock: int
    chain: Vector
    kind: str
    original_word: tuple[int,...]
    original_values: tuple[int,...]
    other_word: tuple[int,...]=()
    other_values: tuple[int,...]=()


def check_move(move: Move) -> None:
    odd(move.source);odd(move.target);need(move.target<move.source,'height must strictly decrease')
    expected=add_vectors({move.source:ONE},{move.target:neg(power(move.clock))})
    need(jet_d(move.chain)==expected,'original first-jet move boundary failed')
    if move.kind=='forward':
        need(move.original_values[0]==move.source and move.original_values[-1]==move.target,'wrong forward endpoints')
    elif move.kind=='inverse':
        need(move.original_values[0]==move.target and move.original_values[-1]==move.source,'wrong inverse endpoints')
    else:
        need(move.kind=='coalescence' and move.original_values[0]==move.source and move.other_values[0]==move.target,'wrong coalescence sources')
        need(move.original_values[-1]==move.other_values[-1],'different coalescence endpoints')
        need(path(move.target,move.other_word)==list(move.other_values),'false second original path')
    need(path(move.original_values[0],move.original_word)==list(move.original_values),'word/edge correspondence failed')

INVERSE_LIBRARY=((1,),(1,2),(1,1,1,2,1,1,4))

def choose_move(n: int, use_coalescence: bool=True) -> Move | None:
    odd(n)
    if n==1:return None
    y,a=step(n)
    if y<n:
        result=Move(n,y,1,{n:ONE},'forward',(a,),(n,y));check_move(result);return result
    for word in INVERSE_LIBRARY:
        p=packet(word);z=p.U*n-p.C
        if z<=0 or z%p.L:continue
        x=z//p.L; values=path(x,word)
        need(values[-1]==n and x<n,'inverse arithmetic image failed')
        result=Move(n,x,-p.m,scale(neg(power(-p.m)),weighted_path(values)),
                    'inverse',word,tuple(values))
        check_move(result);return result
    if use_coalescence and n>=1731 and (n-1731)%2916==0:
        t=(n-1731)//2916; m=1215+2048*t
        left=(1,);right=(1,1,1,1,1,2,3)
        lv=path(n,left);rv=path(m,right)
        chain=add_vectors(weighted_path(lv),scale(neg(power(-6)),weighted_path(rv)))
        result=Move(n,m,-6,chain,'coalescence',left,tuple(lv),right,tuple(rv))
        check_move(result);return result
    return None


class HeightRetraction:
    """Global finite-column retraction, stopping at DECLARED arithmetic roots.

    All recursions decrease the actual queried positive integer. Intermediate
    original path vertices need not decrease. Roots are not declared convergent.
    """
    def __init__(self, use_coalescence: bool=True) -> None:
        self.use_coalescence=use_coalescence
        self.cache: dict[int,tuple[int,int,Vector]]={1:(1,0,{})}
    def resolve(self,n: int) -> tuple[int,int,Vector]:
        odd(n); trail=[];x=n
        while x not in self.cache:
            move=choose_move(x,self.use_coalescence)
            if move is None:
                self.cache[x]=(x,0,{})
                break
            trail.append(move);x=move.target
        for move in reversed(trail):
            root,clock,chain=self.cache[move.target]
            self.cache[move.source]=(root,move.clock+clock,
                add_vectors(move.chain,scale(power(move.clock),chain)))
        root,clock,chain=self.cache[n]
        return root,clock,dict(chain)
    def H(self,v: Mapping[int,Dual]) -> Vector:
        out: Vector={}
        for n,a in v.items():
            _,_,chain=self.resolve(n);out=add_vectors(out,scale(a,chain))
        return out
    def Q(self,v: Mapping[int,Dual]) -> Vector:
        out: Vector={}
        for n,a in v.items():
            root,clock,_=self.resolve(n);out=add_vectors(out,{root:times(a,power(clock))})
        return out
    def F(self,v: Mapping[int,Dual]) -> Vector:
        return add_vectors(v,scale((-1,0),self.H(jet_d(v))))
    def certificate(self,n: int) -> dict:
        root,clock,h=self.resolve(n)
        need(jet_d(h)==add_vectors({n:ONE},{root:neg(power(clock))}),'height-column boundary failed')
        x=n; moves=[]
        while (move:=choose_move(x,self.use_coalescence)) is not None:
            moves.append({'source':move.source,'smaller_target':move.target,'kind':move.kind,
                          'signed_clock':move.clock,'original_word':list(move.original_word),
                          'original_path':list(move.original_values),
                          'other_word':list(move.other_word),'other_path':list(move.other_values)})
            x=move.target
        return {'source':n,'root':root,'signed_clock':clock,'moves':moves,
                'original_dual_edge_chain':{str(k):list(v) for k,v in h.items()},
                'status':'reduced_to_basepoint' if root==1 else 'retained_arithmetic_root',
                'root_convergence_claim':root==1,'original_fixed_loop_retained':True}


def arithmetic_root(n: int, use_coalescence: bool=True) -> bool:
    odd(n)
    return n==1 or (n%36 in (3,7,15,19,27) and n%8748!=8731 and (not use_coalescence or n%2916!=1731))


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__);s=p.add_subparsers(dest='command',required=True)
    e=s.add_parser('envelope');e.add_argument('--horizon',type=int,default=10280)
    c=s.add_parser('crossing');c.add_argument('source',type=int);c.add_argument('--cap',type=int,default=10280)
    r=s.add_parser('reduce');r.add_argument('source',type=int)
    i=s.add_parser('inverse');i.add_argument('word',nargs='+',type=int)
    f=s.add_parser('coalescence')
    f.add_argument('--left',nargs='*',type=int,required=True)
    f.add_argument('--right',nargs='*',type=int,required=True)
    f.add_argument('--parameter',type=int)
    for q in (e,c,r,i,f):q.add_argument('--output',type=Path)
    a=p.parse_args()
    try:
        if a.command=='envelope':result=envelope(a.horizon)
        elif a.command=='crossing':result=first_crossing(a.source,a.cap)
        elif a.command=='reduce':result=HeightRetraction().certificate(a.source)
        elif a.command=='inverse':result=inverse_family(a.word)
        else:
            result=coalescence_family(a.left,a.right)
            if a.parameter is not None:result=coalescence_move(result,a.parameter)
    except CertificateError as exc:p.error(str(exc))
    text=json.dumps(result,sort_keys=True,indent=2)+'\n'
    if a.output:a.output.write_text(text)
    else:print(text,end='')



def coalescence_family(left_word: Iterable[int],right_word: Iterable[int]) -> dict:
    """Exact pair of ORIGINAL source cylinders with a common ORIGINAL endpoint.

    All compatible pairs are a single target-image intersection progression.
    The strict-left-source-larger subdomain is an exact integer interval.
    The comparison label is retained even when that arithmetic domain is empty.
    """
    a=packet(left_word);b=packet(right_word)
    from math import gcd
    g=gcd(a.L,b.L)
    out={'left_word':list(a.word),'right_word':list(b.word),
         'left_original_data':[a.L,a.U,a.C,a.rho,a.eta],
         'right_original_data':[b.L,b.U,b.C,b.rho,b.eta],
         'declared_comparison_retained':True,'signed_clock':a.m-b.m}
    if (b.eta-a.eta)%(2*g):
        return {**out,'target_compatible':False,'parameter_domain':None,
                'status':'empty_arithmetic_intersection_with_declared_label'}
    residue,period=crt_pair(a.eta,2*a.L,b.eta,2*b.L)
    threshold=max(a.eta,b.eta)
    y0=residue+((threshold-residue+period-1)//period)*period
    u0=(y0-a.eta)//(2*a.L);v0=(y0-b.eta)//(2*b.L)
    n0=a.rho+2*a.U*u0; m0=b.rho+2*b.U*v0
    ns=2*a.U*(b.L//g);ms=2*b.U*(a.L//g)
    constant=n0-m0;slope=ns-ms
    if slope>0:domain=[max(0,(-constant)//slope+1),None]
    elif slope==0:domain=[0,None] if constant>0 else None
    else:domain=[0,(constant-1)//(-slope)] if constant>0 else None
    return {**out,'target_compatible':True,'common_target_anchor':y0,'common_target_step':period,
            'left_source_anchor':n0,'left_source_step':ns,'right_source_anchor':m0,'right_source_step':ms,
            'original_left_parameter_anchor':u0,'original_left_parameter_step':b.L//g,
            'original_right_parameter_anchor':v0,'original_right_parameter_step':a.L//g,
            'source_difference_constant':constant,'source_difference_slope':slope,
            'parameter_domain':domain,'status':'strict_height_reduction_family' if domain is not None else 'compatible_without_strict_height_reduction'}


def coalescence_move(family: dict,t: int) -> dict:
    need(type(t) is int and t>=0,'nonnegative integer parameter required')
    expected=coalescence_family(family['left_word'],family['right_word'])
    need(family==expected,'altered coalescence family')
    domain=family['parameter_domain']
    need(domain is not None and t>=domain[0] and (domain[1] is None or t<=domain[1]),'outside exact reduction domain')
    n=family['left_source_anchor']+family['left_source_step']*t
    m=family['right_source_anchor']+family['right_source_step']*t
    left=path(n,family['left_word']);right=path(m,family['right_word'])
    need(left[-1]==right[-1],'original endpoints did not synchronize')
    ell=len(family['left_word'])-len(family['right_word'])
    chain=add_vectors(weighted_path(left),scale(neg(power(ell)),weighted_path(right)))
    need(m<n and jet_d(chain)==add_vectors({n:ONE},{m:neg(power(ell))}),'coalescence boundary or height failure')
    # This move records both paths separately, not as one forward path n -> m.
    return {'source':n,'smaller_source':m,'common_endpoint':left[-1],'signed_clock':ell,
            'left_original_path':left,'right_original_path':right,
            'dual_edge_chain':{str(k):list(v) for k,v in chain.items()},
            'claimed_forward_descent':False,'status':'verified_original_coalescence_reduction'}


if __name__=='__main__':main()
