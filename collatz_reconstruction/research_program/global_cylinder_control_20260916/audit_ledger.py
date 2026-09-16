#!/usr/bin/env python3
"""Independent elementary checker of every original first-crossing ledger row.

This file imports neither global_control nor the predecessor. It checks
both the original arithmetic and the complete depth-first prefix domain.
The all-length Matveev theorem is not used by this bounded-return audit.
"""
from __future__ import annotations
import argparse
import gzip
import hashlib
import json
from pathlib import Path


def require(ok: bool, why: str) -> None:
    if not ok:raise ValueError(why)


def verify(path: Path, max_return: int) -> dict:
    require(type(max_return) is int and max_return>=1,'positive return bound')
    stack=[()];count=0;levels=[0]*max_return;exceptions=[];digest=hashlib.sha256()
    with gzip.open(path,'rb') as fh:
        for line in fh:
            digest.update(line);row=json.loads(line)
            require(len(row)==10,'row format')
            word,A,L,C,rho,y,a,x,cross,bad=row
            require(stack and tuple(word)==stack.pop(),'prefix domain missing, duplicated or out of order')
            j=len(word);levels[j]+=1;count+=1
            total=0;force=0
            for i,b in enumerate(word):
                require(type(b) is int and b>=1,'positive exponent')
                force+=3**(j-1-i)*2**total;total+=b
                require(2**total<3**(i+1),'prefix already crossed')
            require(A==total and L==3**j and C==force,'original closed coefficients')
            U=2**A
            require(rho==((U-C)*pow(L,-1,2*U))%(2*U),'original congruence')
            require(U*y==L*rho+C and y%2==1,'original odd endpoint')
            nextvalue=3*y+1; exponent=0
            while nextvalue%2==0:nextvalue//=2;exponent+=1
            require((a,x)==(exponent,nextvalue),'actual next exponent')
            threshold=(3*L).bit_length()-A
            require(threshold>=2 and U*2**(threshold-1)<3*L<U*2**threshold,'threshold')
            require(cross==int(U*2**a>3*L) and bad==int(cross and x>=rho),'canonical status')
            M=2**(threshold-1)
            t0=(-(3*y+1)//2*pow(3*L,-1,M))%M
            n0=rho+2*U*t0
            numerator=3*y+1+6*L*t0
            require(numerator%2**threshold==0,'complete crossing congruence')
            b0=numerator//2**threshold
            stride=U*2**threshold
            require(stride>3*L and n0+stride>b0+3*L,'whole positive tail does not descend')
            endpoint=b0
            while endpoint%2==0:endpoint//=2
            require((endpoint>=n0)==bool(bad),'whole-tail first point')
            if bad:exceptions.append({'word':word+[a],'source':rho,'endpoint':x})
            if j+1<max_return:
                for b in range(threshold-1,0,-1):stack.append(tuple(word)+(b,))
    require(not stack,'ledger ended before domain completed')
    require(exceptions==[{'word':[2],'source':1,'endpoint':1}],'additional crossing exception in claimed domain')
    return {'status':'PASS','max_first_crossing_return':max_return,'original_prefixes':count,
            'prefix_counts':levels,'exceptions':exceptions,'uncompressed_sha256':digest.hexdigest(),
            'uses_global_control_module':False,'uses_matveev_as_premise':False,
            'positive_start_bound':None,'last_exponent_bound':None}


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('ledger',type=Path)
    ap.add_argument('--max-return',type=int,default=18);ap.add_argument('--output',type=Path)
    args=ap.parse_args();result=verify(args.ledger,args.max_return)
    text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output:args.output.write_text(text,encoding='utf-8')
    print(text,end='')

if __name__=='__main__':main()
