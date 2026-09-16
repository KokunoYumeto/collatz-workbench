#!/usr/bin/env python3
"""Original Collatz joins; integral first-jet reduction to retained roots."""
from __future__ import annotations
import argparse
from dataclasses import dataclass
from functools import lru_cache
import hashlib
import json
from pathlib import Path

class CertificateError(ValueError): pass

def need(ok, text):
    if not ok: raise CertificateError(text)
def odd(n): need(type(n) is int and n>0 and n%2==1,'positive odd original source required')
def step(n):
    odd(n);x=3*n+1;a=(x&-x).bit_length()-1
    return x>>a,a
def v3(n):
    need(type(n) is int and n>0,'positive valuation source required');b=0
    while n%3==0:n//=3;b+=1
    return b
@dataclass(frozen=True)
class Packet:
    word:tuple
    A:int
    L:int
    C:int
    @property
    def U(self):return 1<<self.A
    @property
    def rho(self):return ((self.U-self.C)*pow(self.L,-1,2*self.U))%(2*self.U)
    @property
    def eta(self):return (self.L*self.rho+self.C)//self.U

def packet(word):
    w=tuple(word);A=0;L=1;C=0
    for a in w:
        need(type(a) is int and a>=1,'positive integral exponent required')
        C=3*C+(1<<A);L*=3;A+=a
    return Packet(w,A,L,C)
def path(n,word):
    odd(n);v=[n]
    for a in word:
        x,b=step(v[-1]);need(a==b,'false original valuation');v.append(x)
    return v

def envelope(horizon):
    need(type(horizon) is int and 1<=horizon<=1000000,'horizon must be 1..1000000')
    L=1;C=0;maximum=0;floor_sums=[0];rows=[];records=[];sha=hashlib.sha256()
    for m in range(1,horizon+1):
        C=3*C+(1<<(L.bit_length()-1));L*=3
        cross=L.bit_length();D=(1<<cross)-L;bound=C//D
        row=[m,cross,bound];rows.append(row);floor_sums.append(cross-1)
        for n in(m,cross,C,D):
            data=n.to_bytes(max(1,(n.bit_length()+7)//8),'big')
            sha.update(len(data).to_bytes(8,'big'));sha.update(data)
        if bound>maximum:maximum=bound;records.append(row)
    return {'horizon':horizon,'original_forcing':1,'maximum_integer_candidate':maximum,
        'maximum_odd_candidate':maximum if maximum%2 else maximum-1,
        'rows_m_crossing_sum_candidate_bound':rows,'record_rows':records,
        'critical_floor_prefix_sums':floor_sums,'exact_big_integer_state_sha256':sha.hexdigest(),
        'maximizer_word_rule':'successive floor-prefix differences, then crossing_sum minus previous floor',
        'uses_transcendence_or_logarithm_estimate':False}

@lru_cache(maxsize=None,typed=True)
def layer(b,e):
    need(type(b) is int and b>=1 and type(e) is int and e in(2,6),'b>=1 and e in {2,6} required')
    a=1
    while 2**(a+e+2*b)>=3**(a+b):a+=1
    h=(2**e+2)//3;Q=3**(a+b);J=2**(e+2*b);K=2**(a+e+2*b)
    r=(-h*3**b*pow(J,-1,Q))%Q
    n=r+Q*(((3-r)*pow(Q,-1,4))%4)
    m=(K*n+2**a*h*3**b)//Q-1
    return {'b':b,'e':e,'a':a,'h':h,'Q':Q,'J':J,'K':K,'word':[1]*a+[e]+[2]*(b-1)+[3],
        'source_anchor':n,'source_step':4*Q,'smaller_anchor':m,'smaller_step':4*K,
        'target_anchor':(3*n+1)//2,'target_step':6*Q,'signed_clock':-(a+b),
        'source_ternary_unit':1 if e==2 else 2}

def layer_for_source(n):
    odd(n)
    if n%4!=3 or n%3:return None
    b=v3(n);e=2 if (n//3**b)%3==1 else 6;f=layer(b,e)
    return dict(f) if n>=f['source_anchor'] and (n-f['source_anchor'])%f['source_step']==0 else None

def original_family(word):
    p=packet(word);k=len(p.word)
    need(k>=2 and p.word[-1]%2==1 and 2**(p.A-1)<3**(k-1),'outside right-word domain')
    y=p.eta;need(y%6==5 and y>=5,'incompatible original target')
    n=(2*y-1)//3;period=4*3**(k-1);m=p.rho
    need(n%4==3 and 0<m<n<period,'original full residue domain failed')
    return {'word':list(p.word),'source_anchor':n,'source_step':period,'smaller_anchor':m,
        'smaller_step':2*p.U,'target_anchor':y,'target_step':2*p.L,'signed_clock':1-k,
        'L':p.L,'U':p.U,'C':p.C}

def candidates(max_length=12):
    need(type(max_length) is int and 2<=max_length<=14,'catalogue length must be 2..14');out=[]
    for k in range(2,max_length+1):
        cap=(3**(k-1)).bit_length()
        def visit(w,total):
            if len(w)==k:
                if w[-1]%2:out.append(original_family(w))
                return
            for a in range(1,cap-total-(k-len(w)-1)+1):visit(w+(a,),total+a)
        visit((),0)
    return sorted(out,key=lambda f:(f['source_step'],f['source_anchor'],sum(f['word']),f['word']))

def old_root_residue(n):
    return n%36 in(3,7,15,19,27) and n%8748!=8731 and n%2916!=1731

@lru_cache(maxsize=1)
def catalogue():
    P=4*3**11;remaining={n for n in range(3,P,4) if old_root_residue(n)}
    old=len(remaining);selected=[];labels=[];rows=candidates()
    for i,f in enumerate(rows):
        hit=[n for n in range(f['source_anchor'],P,f['source_step']) if n in remaining]
        labels.append([i,bool(hit),len(hit)])
        if hit:
            selected.append({**f,'new_residues':len(hit),'candidate_index':i});remaining.difference_update(hit)
    return {'period':P,'candidate_count':len(rows),'old_root_count':old,
        'selected':selected,'remaining':sorted(remaining),'candidate_labels':labels}

def catalogue_for_source(n):
    for f in catalogue()['selected']:
        if n>=f['source_anchor'] and (n-f['source_anchor'])%f['source_step']==0:return f
    return None

def power(k):return 1,k
def mul(a,b):return a[0]*b[0],a[0]*b[1]+a[1]*b[0]
def add(*vs):
    out={}
    for v in vs:
        for n,z in v.items():
            odd(n);need(isinstance(z,tuple) and len(z)==2 and all(type(t) is int for t in z),'integral dual pair required')
            w=out.get(n,(0,0));out[n]=(w[0]+z[0],w[1]+z[1])
    return {n:z for n,z in sorted(out.items()) if z!=(0,0)}
def scale(a,v):return {n:z for n,w in sorted(v.items()) if(z:=mul(a,w))!=(0,0)}
def negative(v):return scale((-1,0),v)
def d(v):
    out={}
    for n,z in v.items():out=add(out,{n:z},scale((-1,-1),{step(n)[0]:z}))
    return out
def weighted(values):
    out={}
    for i,n in enumerate(values[:-1]):
        need(step(n)[0]==values[i+1],'false original edge');out=add(out,{n:power(i)})
    return out
@dataclass(frozen=True)
class Move:
    source:int
    target:int
    clock:int
    chain:dict
    kind:str
    left:tuple
    right:tuple

def check_move(t):
    odd(t.source);odd(t.target);need(t.target<t.source,'height must strictly decrease')
    need(t.left and t.right and t.left[0]==t.source and t.right[0]==t.target,'wrong source legs')
    need(t.left[-1]==t.right[-1] and t.clock==len(t.left)-len(t.right),'wrong common target or clock')
    need(t.chain==add(weighted(t.left),negative(scale(power(t.clock),weighted(t.right)))),'changed original chain')
    need(d(t.chain)==add({t.source:(1,0)},negative({t.target:power(t.clock)})),'false boundary')
def join_move(n,f):
    need(n>=f['source_anchor'] and(n-f['source_anchor'])%f['source_step']==0,'outside source fibre')
    t=(n-f['source_anchor'])//f['source_step'];m=f['smaller_anchor']+f['smaller_step']*t
    l=(n,step(n)[0]);r=tuple(path(m,f['word']));k=1-len(f['word'])
    z=Move(n,m,k,add(weighted(l),negative(scale(power(k),weighted(r)))),'join',l,r)
    check_move(z);return z
INVERSES=((1,),(1,2),(1,1,1,2,1,1,4))
def choose_move(n,mode='full'):
    odd(n);need(mode in('old','catalogue','full'),'invalid mode')
    if n==1:return None
    y,_=step(n)
    if y<n:
        z=Move(n,y,1,{n:(1,0)},'forward',(n,y),(y,));check_move(z);return z
    for w in INVERSES:
        p=packet(w);num=p.U*n-p.C
        if num>0 and num%p.L==0:
            m=num//p.L;r=tuple(path(m,w));k=-len(w)
            z=Move(n,m,k,negative(scale(power(k),weighted(r))),'inverse',(n,),r);check_move(z);return z
    f=layer(1,2)
    if n>=f['source_anchor'] and(n-f['source_anchor'])%f['source_step']==0:return join_move(n,f)
    if mode=='old':return None
    f=catalogue_for_source(n)
    if f is not None:return join_move(n,f)
    if mode=='full':
        f=layer_for_source(n)
        if f is not None:return join_move(n,f)
    return None

class Retraction:
    def __init__(self,mode='full'):
        need(mode in('old','catalogue','full'),'invalid mode');self.mode=mode;self.cache={1:(1,0,{})}
    def resolve(self,n):
        odd(n);trail=[];x=n
        while x not in self.cache:
            move=choose_move(x,self.mode)
            if move is None:self.cache[x]=(x,0,{});break
            trail.append(move);x=move.target
        for move in reversed(trail):
            root,k,h=self.cache[move.target]
            self.cache[move.source]=(root,move.clock+k,add(move.chain,scale(power(move.clock),h)))
        root,k,h=self.cache[n];return root,k,dict(h)
    def Q(self,v):
        out={}
        for n,z in v.items():
            r,k,_=self.resolve(n);out=add(out,{r:mul(z,power(k))})
        return out
    def H(self,v):
        out={}
        for n,z in v.items():out=add(out,scale(z,self.resolve(n)[2]))
        return out
    def F(self,v):return add(v,negative(self.H(d(v))))
    def certificate(self,n):
        r,k,h=self.resolve(n);need(d(h)==add({n:(1,0)},negative({r:power(k)})),'retraction boundary')
        return {'source':n,'root':r,'signed_clock':k,'chain':{str(x):list(z) for x,z in h.items()},
            'status':'basepoint_reduction' if r==1 else 'retained_root','mode':self.mode,'forward_orbit_claim':False}

def main():
    ap=argparse.ArgumentParser(description=__doc__);sub=ap.add_subparsers(dest='command',required=True)
    p=sub.add_parser('layer');p.add_argument('b',type=int);p.add_argument('e',type=int,choices=[2,6])
    p=sub.add_parser('reduce');p.add_argument('source',type=int);p.add_argument('--mode',choices=['old','catalogue','full'],default='full')
    p=sub.add_parser('envelope');p.add_argument('horizon',type=int)
    a=ap.parse_args()
    try:r=layer(a.b,a.e) if a.command=='layer' else envelope(a.horizon) if a.command=='envelope' else Retraction(a.mode).certificate(a.source)
    except CertificateError as e:ap.error(str(e))
    print(json.dumps(r,sort_keys=True,indent=2))
if __name__=='__main__':main()
