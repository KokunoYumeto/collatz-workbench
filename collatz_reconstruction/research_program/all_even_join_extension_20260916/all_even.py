#!/usr/bin/env python3
"""All even interior exponents in the ORIGINAL common-future templates.

An accepted comparison n -> y <- m proves equality of original first-jet
classes, with m<n. It is not a forward Collatz step from n to m.
Only integer arithmetic is used; all checks survive python -O.
"""
from __future__ import annotations
from functools import lru_cache
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import sys
from typing import Any

BASE = Path(__file__).resolve().parent.parent
dependency = BASE/'bilateral_root_bounds_20260916'/'bilateral_control.py'
if hashlib.sha256(dependency.read_bytes()).hexdigest() != '83288427125083f723d011915db9456843072eff10c15c0b71f3e56c31975358':
    raise RuntimeError('The original bilateral source identity differs')
spec = importlib.util.spec_from_file_location('retained_bilateral', dependency)
if spec is None or spec.loader is None:
    raise ImportError('Missing retained bilateral_control.py')
old = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = old
spec.loader.exec_module(old)
need, odd = old.need, old.odd


def interior_data(e: int) -> tuple[int,int,int]:
    need(type(e) is int and e >= 2 and e % 2 == 0, 'positive EVEN exponent >=2 required')
    h=((1 << e)+2)//3
    t=old.v3(h)
    # Independent exact lifting formula, proved in the note.
    expected=old.v3(e-1)
    need(t == expected, 'interior ternary-order identity failed')
    return h,t,h//3**t


@lru_cache(maxsize=None, typed=True)
def family(b: int,e: int,bilateral: bool) -> dict[str,Any]:
    need(type(b) is int and b>=1, 'positive tail-layer parameter b required')
    need(type(bilateral) is bool, 'explicit comparison selector required')
    h,t,unit=interior_data(e)
    shift=int(bilateral)
    a=1
    while (1 << (a+e+2*b-shift)) >= 3**(a+b):
        a+=1
    need(a >= e and a>t, 'leading run does not dominate interior ternary order')
    J=1 << (e+2*b-shift)
    Q=3**(a+b); K=(1 << a)*J
    residue=(-h*3**b*pow(J,-1,Q)) % Q
    dyad,dyad_res=(32,27) if bilateral else (4,3)
    n0,ns=old.crt_pair(residue,Q,dyad_res,dyad)
    m0=(K*n0+(1 << a)*h*3**b)//Q-1
    ms=dyad*K
    left=(1,2,1) if bilateral else (1,)
    right=(1,)*a+(e,)+(2,)*(b-1)+((1,1,3) if bilateral else (3,))
    lp=old.packet(left)
    y0=(lp.L*n0+lp.C)//lp.U; ys=lp.L*ns//lp.U
    need(n0>m0>0 and ns>ms, 'complete height domain failed')
    need(old.v3(n0)==b+t and ns%3**(b+t+1)==0, 'actual source ternary layer changed')
    return {'b':b,'e':e,'bilateral':bilateral,'h':h,'h_order':t,'h_unit':unit,
            'a_min':a,'J':J,'Q':Q,'K':K,'actual_layer':b+t,
            'n0':n0,'nstep':ns,'m0':m0,'mstep':ms,'y0':y0,'ystep':ys,
            'left_word':list(left),'right_word':list(right),'clock':len(left)-len(right),
            'height_constant':n0-m0,'height_slope':ns-ms,
            'parameter_domain':[0,None],'source_inverse':'(n-n0)/nstep',
            'complete_coefficient_contracting_template':True}


def candidates(n: int) -> list[dict[str,Any]]:
    """All admitted coefficient-contracting even-e templates at THIS source.

    No cutoff is guessed: e<=k(n) is proved from m<n and nu_2(W)=1.
    A maximal leading run gives the least endpoint for each template.
    """
    odd(n)
    if n==1 or n%3 or n%4!=3:
        return []
    B=old.v3(n)
    k=(n-1).bit_length()-2  # floor(log_2(n-1))-1
    out=[]
    for e in range(2,k+1,2):
        h,t,_=interior_data(e)
        b=B-t
        if b<1:
            continue
        for bilateral in (False,True):
            if bilateral and n%32!=27:
                continue
            f=family(b,e,bilateral)
            if f['a_min']>k or (n-f['n0'])%f['nstep']:
                continue
            parameter=(n-f['n0'])//f['nstep']
            need(parameter>=0, 'source before canonical positive residue')
            Z=f['J']*(n//3**b)+h
            a=old.v3(Z)
            need(f['a_min']<=a<=k, 'maximal leading-run range failed')
            W=Z//3**a
            m=(1 << a)*W-1
            right=(1,)*a+(e,)+(2,)*(b-1)+((1,1,3) if bilateral else (3,))
            need(0<m<n and W%4==2, 'exact positive smaller source failed')
            out.append({'source':n,'target':m,'b':b,'e':e,'actual_layer':B,
                        'bilateral':bilateral,'parameter':parameter,'a_min':f['a_min'],
                        'a_max':a,'W':W,'rise_peak':Z-1,
                        'left_word':f['left_word'],'right_word':list(right),
                        'clock':len(f['left_word'])-len(right)})
    return sorted(out,key=lambda z:(z['target'],len(z['right_word']),z['e'],z['bilateral']))


def move(n: int, budgeted: bool = True) -> Any:
    need(type(budgeted) is bool, "budget mode must be explicit Boolean")
    for z in candidates(n):
        mv=old.make_move(n,z['target'],z['left_word'],z['right_word'],'all_even_template')
        if not budgeted or max(mv.left_values+mv.right_values)<=old.support_bound(n):
            return mv
    return None


def support_bound(n: int) -> int:
    odd(n)
    if n==1:return 1
    k=(n-1).bit_length()-2
    return max(130*(n+1),(n-1)*3**k//(1 << k)-1)


def term_bound(n: int) -> int:
    odd(n)
    if n==1:return 0
    k=(n-1).bit_length()-2
    return ((n-1)//2)*max(24,k+old.floor_log3(n)+6)


class Retraction:
    """The prior stage is tried first; new rules apply only at retained roots."""
    def __init__(self, budgeted: bool = True):
        need(type(budgeted) is bool, "budget mode must be explicit Boolean")
        self.budgeted=budgeted
        self.cache={1:(1,0,{})}
    def resolve(self,n: int):
        odd(n);trail=[];x=n
        while x not in self.cache:
            edge=old.choose_move(x,2)
            if edge is None:
                edge=move(x,self.budgeted)
            if edge is None:
                self.cache[x]=(x,0,{});break
            trail.append(edge);x=edge.target
        for edge in reversed(trail):
            root,k,h=self.cache[edge.target]
            hh=old.add_vectors(edge.chain,old.scale(old.qpower(edge.clock),h))
            self.cache[edge.source]=(root,edge.clock+k,hh)
        r,k,h=self.cache[n]
        need(all(x<=(old.support_bound(n) if self.budgeted else support_bound(n)) for x in h), 'original support exceeded bound')
        need(old.jet_d(h)==old.add_vectors({n:old.ONE},{r:(-1,-k)}), 'global column boundary')
        return r,k,dict(h)
    def Q(self,v):
        out={}
        for n,a in v.items():
            r,k,_=self.resolve(n)
            out=old.add_vectors(out,{r:old.mulc(a,old.qpower(k))})
        return out
    def H(self,v):
        out={}
        for n,a in v.items():out=old.add_vectors(out,old.scale(a,self.resolve(n)[2]))
        return out
    def F(self,v):
        return old.add_vectors(v,old.scale((-1,0),self.H(old.jet_d(v))))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='cmd',required=True)
    f=sub.add_parser('family');f.add_argument('b',type=int);f.add_argument('e',type=int);f.add_argument('--bilateral',action='store_true')
    s=sub.add_parser('source');s.add_argument('n',type=int)
    a=p.parse_args()
    print(json.dumps(family(a.b,a.e,a.bilateral) if a.cmd=='family' else candidates(a.n),indent=2,sort_keys=True))
if __name__=='__main__':main()
