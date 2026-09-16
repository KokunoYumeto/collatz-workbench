#!/usr/bin/env python3
"""A proof-carrying cover by complete original first-descent cylinders.

The search runs only the least uncovered original source. Acceptance checks
full symbolic cylinders and an exact disjoint counting identity. Search caps
produce failures, not convergence or divergence certificates.
"""
from __future__ import annotations
import argparse
from collections import Counter
from dataclasses import dataclass
import gzip
import hashlib
import json
from pathlib import Path
from typing import Iterable

import arithmetic as ar


@dataclass(frozen=True)
class Cell:
    word: tuple[int,...]
    seed: int
    r: int
    U: int
    L: int
    C: int
    lower: int
    upper: int | None

    def interval(self, bound: int) -> tuple[int,int]:
        lo = max(self.lower, (3-self.r+2*self.U-1)//(2*self.U))
        hi = (bound-self.r)//(2*self.U)
        if self.upper is not None:
            hi = min(hi,self.upper)
        return lo,hi

    def count(self,bound: int) -> int:
        lo,hi=self.interval(bound)
        return max(0,hi-lo+1)

    def parameter(self,n: int) -> int | None:
        t,rem=divmod(n-self.r,2*self.U)
        return t if (rem==0 and n>=3 and t>=self.lower
                     and (self.upper is None or t<=self.upper)) else None

    def endpoint(self,n: int) -> int:
        t=self.parameter(n)
        ar.require(t is not None, 'original source outside the declared descent cell')
        y,rem=divmod(self.L*n+self.C,self.U)
        ar.require(rem==0 and y>0 and y%2==1 and y<n,'cell endpoint is not an actual strict descent')
        return y

    def record(self) -> dict:
        return {'word':list(self.word),'discovery_seed':self.seed,
                'source_anchor':self.r,'source_step':2*self.U,
                'target_anchor':(self.L*self.r+self.C)//self.U,
                'target_step':2*self.L,'L':self.L,'U':self.U,'C':self.C,
                'lower_parameter':self.lower,'upper_parameter':self.upper}


def make_cell(word: Iterable[int], seed: int=0) -> Cell:
    p=ar.packet(word)
    ar.require(p.D>0,'a first-descent word has positive original affine difference')
    r=p.C*pow(p.D,-1,2*p.U)%(2*p.U)
    low=max(0,(p.C-p.D*r)//(2*p.U*p.D)+1)
    high=None
    A,L,U,C=0,1,1,0
    for a in p.word[:-1]:
        A,L,U,C=A+a,3*L,U*(1<<a),3*C+U
        D=U-L
        if D>0:
            h=(C-D*r)//(2*p.U*D)
            high=h if high is None else min(high,h)
    return Cell(p.word,seed,r,p.U,p.L,p.C,low,high)


def seek_first_descent(n: int, cap: int) -> tuple[int,...]:
    ar.positive_odd(n)
    ar.require(n>1 and type(cap) is int and cap>0,'nonbase source and positive search cap required')
    x=n; word=[]
    for _ in range(cap):
        x,a=ar.step(x);word.append(a)
        if x<n:return tuple(word)
        if x==n:raise ar.CertificateError('actual return without descent: '+str(n))
    raise ar.CertificateError('unresolved search cap at original source '+str(n))


def canonical_bytes(data: dict) -> bytes:
    return (json.dumps(data,sort_keys=True,separators=(',',':'))+'\n').encode()


def build(bound: int, cap: int=10000) -> dict:
    ar.require(type(bound) is int and bound>=3 and bound%2==1,'odd finite bound >=3 required')
    last=(bound-1)//2
    covered=bytearray(last+1);covered[0]=1
    cells=[]; discoveries=0; evaluated=0
    for i in range(1,last+1):
        if covered[i]:continue
        n=2*i+1
        word=seek_first_descent(n,cap)
        evaluated+=len(word);discoveries+=1
        cell=make_cell(word,n)
        ar.require(cell.parameter(n) is not None,'discovery source missing from symbolic cell')
        lo,hi=cell.interval(bound);count=max(0,hi-lo+1)
        first=(cell.r+2*cell.U*lo-1)//2
        stop=first+cell.U*count
        previous=covered[first:stop:cell.U]
        ar.require(len(previous)==count and not any(previous),'overlapping first-descent cells')
        covered[first:stop:cell.U]=b'\1'*count
        cells.append(cell.record())
    ar.require(all(covered),'source interval not covered')
    return {'schema':'collatz-original-descent-cover-v1','forcing':1,
            'odd_source_interval':[3,bound],'fixed_source':1,
            'declared_zero_labels':[{'word':[1],'reason':'no coefficient contraction'},
                                    {'word':[2,2],'reason':'first descent already occurs at prefix (2) or source is 1'}],
            'cells':cells,'search':{'original_sources_iterated':discoveries,
                                   'original_return_equations_during_search':evaluated,
                                   'return_cap_per_search_source':cap},
            'claim':'exact finite interval coverage by full original first-descent cells'}


def independent_cell(record: dict) -> Cell:
    """Reconstruct using prefix recurrences and the unreduced final parity equation.

    Anchor paths and their slopes verify *every* original equation for every
    integer parameter, rather than validating the cell by sampled lifts.
    """
    word=tuple(record['word'])
    ar.require(word and all(type(a) is int and a>=1 for a in word),'bad exponent word')
    L,U,C=1,1,0
    prefixes=[]
    for a in word:
        L,C,U=3*L,3*C+U,U*(2**a)
        prefixes.append((L,U,C,U-L))
    D=U-L
    ar.require(D>0,'positive final coefficient difference required')
    r=((U-C)*pow(L,-1,2*U))%(2*U)
    ar.require(0<r<2*U and r%2==1,'bad original cylinder representative')
    lower=max(0,(C-D*r)//(2*U*D)+1)
    upper=None
    for lj,uj,cj,dj in prefixes[:-1]:
        if dj>0:
            h=(cj-dj*r)//(2*U*dj)
            upper=h if upper is None else min(upper,h)
    cell=Cell(word,record['discovery_seed'],r,U,L,C,lower,upper)
    ar.require(record==cell.record(),'cell differs from independent exact reconstruction')
    x0,xstep=r,2*U
    equation_checks=0
    for a,(lj,uj,cj,_) in zip(word,prefixes):
        y0,rem=divmod(lj*r+cj,uj)
        ystep,rem2=divmod(lj*2*U,uj)
        ar.require(not rem and not rem2 and y0>0 and y0%2==1 and ystep%2==0,
                   'full cylinder failed integral/parity lift')
        ar.require(3*x0+1==(2**a)*y0 and 3*xstep==(2**a)*ystep,
                   'constant or slope of original equation failed')
        equation_checks+=2;x0,xstep=y0,ystep
    ar.require(cell.parameter(cell.seed) is not None,'discovery seed not in cell')
    return cell


def verify_cover(data: dict, enumerate_interval: bool=True) -> tuple[list[Cell],dict]:
    ar.require(data.get('schema')=='collatz-original-descent-cover-v1' and data.get('forcing')==1,
               'unexpected source schema or forcing')
    lower,bound=data['odd_source_interval']
    ar.require(lower==3 and type(bound) is int and bound>=3 and bound%2==1,'bad source interval')
    ar.require(data['fixed_source']==1,'actual basepoint changed')
    ar.require(data['declared_zero_labels']==[
        {'word':[1],'reason':'no coefficient contraction'},
        {'word':[2,2],'reason':'first descent already occurs at prefix (2) or source is 1'}],
        'declared supported-zero labels changed')
    cells=[independent_cell(r) for r in data['cells']]
    words=[c.word for c in cells]
    ar.require(len(set(words))==len(words),'repeated word label in cover')
    search=data['search']
    ar.require(search['original_sources_iterated']==len(cells) and
               search['original_return_equations_during_search']==sum(map(len,words)),
               'discovery receipt counts disagree with retained source words')
    ar.require(type(search['return_cap_per_search_source']) is int and
               search['return_cap_per_search_source']>=max(map(len,words)),
               'discovery cap is incompatible with a retained completed word')
    count=sum(c.count(bound) for c in cells)
    ar.require(count==(bound-1)//2,'exact disjoint cardinality does not exhaust the interval')
    # Determinism plus exact first-descent masks proves disjointness globally.
    # This second finite implementation independently checks all interval slots.
    if enumerate_interval:
        hits=bytearray((bound-1)//2+1);hits[0]=1
        for c in cells:
            lo,hi=c.interval(bound)
            for t in range(lo,hi+1):
                n=c.r+2*c.U*t;j=(n-1)//2
                ar.require(not hits[j],'duplicate original source in finite coverage replay')
                y=(c.L*n+c.C)//c.U
                ar.require(0<y<n and y%2==1,'induction endpoint is not a lower positive odd integer')
                hits[j]=1
        ar.require(all(hits),'finite coverage replay left a source hole')
    return cells,{'covered_original_sources':count,'bound':bound,
                  'symbolic_first_descent_cells':len(cells),
                  'infinite_parameter_cells':sum(c.upper is None for c in cells),
                  'finite_parameter_cells':sum(c.upper is not None for c in cells),
                  'declared_empty_labels':len(data['declared_zero_labels']),
                  'symbolic_original_equations':sum(len(c.word) for c in cells),
                  'constant_and_slope_equalities':2*sum(len(c.word) for c in cells),
                  'maximum_word_length':max(map(len,words)),
                  'maximum_exponent_sum':max(sum(w) for w in words),
                  'all_positive_endpoints_strictly_lower':True,
                  'full_parameter_proof':'original affine constants/slopes, parity, and exact floor interval'}


class Index:
    def __init__(self,cells: Iterable[Cell]):
        self.levels={}
        for c in cells:
            self.levels.setdefault(c.U,{})[c.r]=c
        self.ordered=sorted(self.levels)

    def find(self,n: int) -> Cell | None:
        for U in self.ordered:
            c=self.levels[U].get(n%(2*U))
            if c is not None and c.parameter(n) is not None:return c
        return None

    def witness(self,n: int) -> dict:
        ar.positive_odd(n)
        original=n;c=Counter();blocks=[];path=[n]
        while n!=1:
            cell=self.find(n)
            ar.require(cell is not None,'original singleton is outside the certified cover')
            values,chain=ar.actual_path(n,cell.word)
            y=cell.endpoint(n)
            ar.require(values[-1]==y and y<n,'compiled reduction did not strictly lower the source')
            blocks.append({'source':n,'target':y,'word':list(cell.word),
                           'source_parameter':cell.parameter(n)})
            c.update(chain);path.extend(values[1:]);n=y
        b={1:-1};cc=ar.clean(c)
        ar.require(ar.jet_boundary(b,cc)==({},{original:1}),'assembled first-jet witness failed')
        return {'source':original,'constant_chain':b,'linear_chain':cc,
                'blocks':blocks,'original_path':path,
                'original_returns':len(path)-1,
                'first_jet_boundary':[{}, {original:1}]}


def period_bound(s: int, period_limit: int=100000) -> dict:
    ar.require(type(s) is int and s>=3 and s%2==1,'odd source lower bound required')
    p3,sp,rp=1,1,1
    tests=hashlib.sha256()
    for m in range(1,period_limit+1):
        p3*=3;sp*=s;rp*=3*s+1
        A=p3.bit_length()
        if (sp<<A)<=rp:break
        tests.update(f'{m}:{A}:excluded\n'.encode())
    else:raise ar.CertificateError('period search limit unresolved')
    num=(4*s)**m;den=(3*s+1)**m
    K=(num//den).bit_length()-1
    if num==den<<K:K-=1
    ar.require(num>den<<K,'all-length rise inequality failed')
    lo,hi=s,2*s
    def admitted(x):return x**m*(1<<A)<=(3*x+1)**m
    while admitted(hi):hi*=2
    while hi-lo>1:
        mid=(lo+hi)//2
        if admitted(mid):lo=mid
        else:hi=mid
    return {'minimum_lower_bound':s,'excluded_periods':[1,m-1],
            'excluded_period_comparisons_sha256':tests.hexdigest(),
            'first_retained_period':m,'first_retained_exponent_sum':A,
            'excluded_exponent_one_count':K,
            'all_length_comparison_exponent':m,
            'next_minimum_ceiling':lo,
            'next_exponent_sum_unique':(sp<<(A+1))>rp,
            'next_one_count':2*m-A,
            'next_one_count_forces_period':(4*s)**(m+1)>((3*s+1)**(m+1)<<(2*m-A)),
            'claim_scope':'all primitive lengths and positive exponents within the stated one-count budget'}


def independent_period_check(record: dict) -> int:
    s=record['minimum_lower_bound'];m0=record['first_retained_period'];A0=record['first_retained_exponent_sum']
    power3=1;power2=1;exp=0;hs=hashlib.sha256()
    checks=0
    for m in range(1,m0+1):
        power3*=3
        while power2<=power3:power2*=2;exp+=1
        left=power2*pow(s,m);right=pow(3*s+1,m)
        if m<m0:
            ar.require(left>right,'earlier integer period window was not excluded')
            hs.update(f'{m}:{exp}:excluded\n'.encode())
        else:ar.require(left<=right and exp==A0,'next period window mismatch')
        checks+=1
    ar.require(hs.hexdigest()==record['excluded_period_comparisons_sha256'],'period comparison transcript mismatch')
    K=record['excluded_exponent_one_count']
    ar.require(pow(4*s,m0)>pow(2,K)*pow(3*s+1,m0),'rise-budget inequality failed')
    top=record['next_minimum_ceiling']
    ar.require(pow(2,A0)*pow(top,m0)<=pow(3*top+1,m0),'ceiling lower endpoint failed')
    ar.require(pow(2,A0)*pow(top+1,m0)>pow(3*(top+1)+1,m0),'ceiling upper endpoint failed')
    ar.require(record==period_bound(s,m0),'period record failed full reconstruction')
    return checks+5


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    sub=ap.add_subparsers(dest='command',required=True)
    p=sub.add_parser('build');p.add_argument('--bound',type=int,default=1166399);p.add_argument('--output',type=Path,required=True)
    p=sub.add_parser('verify');p.add_argument('atlas',type=Path)
    p=sub.add_parser('witness');p.add_argument('atlas',type=Path);p.add_argument('source',type=int);p.add_argument('--output',type=Path)
    a=ap.parse_args()
    try:
        if a.command=='build':
            data=build(a.bound);raw=canonical_bytes(data)
            cells,summary=verify_cover(data)
            a.output.write_bytes(gzip.compress(raw,mtime=0))
            print(json.dumps({'status':'PASS','atlas_uncompressed_sha256':hashlib.sha256(raw).hexdigest(),**summary},sort_keys=True))
        else:
            data=json.loads(gzip.decompress(a.atlas.read_bytes()));cells,summary=verify_cover(data)
            result=summary if a.command=='verify' else Index(cells).witness(a.source)
            text=json.dumps(result,sort_keys=True,indent=2)+'\n'
            if getattr(a,'output',None):a.output.write_text(text)
            else:print(text,end='')
    except ar.CertificateError as e:ap.error(str(e))

def finite_equation_support(cells: list[Cell], bound: int) -> tuple[set[int], dict[int,int], dict]:
    """Materialize the finite *equation* support implied by the symbolic cover.

    Each progression keeps its literal parameter. All outgoing edges are
    checked independently; a positive integral height on this SAME graph
    certifies that its first-jet reduction kernel is zero.
    """
    sources={1}; expanded=0
    for cell in cells:
        lo,hi=cell.interval(bound)
        if hi<lo:continue
        x0,dx=cell.r,2*cell.U
        for a in cell.word:
            sources.update(range(x0+dx*lo,x0+dx*hi+1,dx))
            expanded+=hi-lo+1
            x0,dx=(3*x0+1)//(1<<a),(3*dx)//(1<<a)
    ordered=sorted(sources)
    # Independent repeated division, not the bit extraction used in discovery.
    next_value={}; exponents={}
    for n in ordered:
        y=3*n+1;a=0
        while y%2==0:y//=2;a+=1
        ar.require(y in sources,'symbolic equation support is not forward closed')
        next_value[n]=y;exponents[n]=a
    height={1:0}
    for n in ordered:
        x=n;path=[];seen=set()
        while x not in height:
            ar.require(x not in seen,'nonbase cycle encountered in the finite original support')
            seen.add(x);path.append(x);x=next_value[x]
        h=height[x]
        for x in reversed(path):h+=1;height[x]=h
    sha=hashlib.sha256(); profile=Counter()
    for n in ordered:
        y=next_value[n]
        ar.require((n==1 and y==1) or height[n]==height[y]+1,'positive height certificate failed')
        sha.update(f'{n}:{y}:{exponents[n]}:{height[n]}\n'.encode())
        profile[height[n]]+=1
    summary={'original_equation_support_size':len(sources),
             'original_prefix_equations_before_deduplication':expanded,
             'independently_divided_original_edges':len(sources),
             'actual_component_count':1,'actual_cycle':[1],
             'maximum_source_label':max(sources),
             'maximum_positive_height':max(height.values()),
             'height_profile':{str(k):v for k,v in sorted(profile.items())},
             'edge_height_transcript_sha256':sha.hexdigest(),
             'first_jet_connecting_matrix':[[-1]],
             'first_jet_reduction_kernel':'zero_with_original_equation_support_retained'}
    return sources,height,summary


if __name__=='__main__':
    main()
