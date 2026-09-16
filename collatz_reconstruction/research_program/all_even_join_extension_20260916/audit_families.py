#!/usr/bin/env python3
"""Independent original-affine-column audit; imports no workbench module."""
from pathlib import Path
import argparse,gzip,hashlib,json


def must(x,message):
    if not x:raise ValueError(message)

def order3(n):
    must(type(n) is int and n>0,'valuation source');r=0
    while n%3==0:n//=3;r+=1
    return r

def leg(c,s,word):
    rows=0
    for e in word:
        must(type(e) is int and e>=1,'exponent')
        c,s=3*c+1,3*s
        must(c%2**e==0 and s%2**e==0,'literal affine division')
        c,s=c//2**e,s//2**e
        must(c>0 and c%2 and s%2==0,'exact valuation or positivity')
        rows+=1
    return c,s,rows

def audit(path):
    seen=[];equations=0;digest=hashlib.sha256()
    opener=gzip.open if str(path).endswith('.gz') else open
    with opener(path,'rb') as f:
        for line in f:
            digest.update(line);z=json.loads(line);b,e,side=z['b'],z['e'],z['bilateral']
            must(type(b) is int and 1<=b<=16,'b-domain')
            must(type(e) is int and 2<=e<=32 and e%2==0,'e-domain')
            must(type(side) is bool,'selector')
            seen.append((b,e,side));h=(2**e+2)//3;t=order3(h)
            must(t==order3(e-1)==z['h_order'],'interior order')
            a=1
            while 2**(a+e+2*b-int(side))>=3**(a+b):a+=1
            must(a==z['a_min'],'minimal a')
            J,Q,K=2**(e+2*b-int(side)),3**(a+b),2**(a+e+2*b-int(side))
            dd,rr=(32,27) if side else (4,3)
            must(0<z['n0']<dd*Q and z['n0']%dd==rr,'canonical dyadic source')
            must((J*z['n0']+h*3**b)%Q==0,'original ternary source')
            must(z['nstep']==dd*Q and z['mstep']==dd*K,'unmodified lattice')
            must(z['m0']==(K*z['n0']+2**a*h*3**b)//Q-1,'original smaller source')
            must(order3(z['n0'])==b+t and z['nstep']%3**(b+t+1)==0,'exact original source layer')
            lw=[1,2,1] if side else [1]
            rw=[1]*a+[e]+[2]*(b-1)+([1,1,3] if side else [3])
            must(z['left_word']==lw and z['right_word']==rw,'original words')
            c,s,k=leg(z['n0'],z['nstep'],lw);equations+=k
            c2,s2,k=leg(z['m0'],z['mstep'],rw);equations+=k
            must((c,s)==(c2,s2)==(z['y0'],z['ystep']),'shared original future')
            must(0<z['m0']<z['n0'] and z['mstep']<z['nstep'],'whole-domain height')
    expected=[(b,e,side) for b in range(1,17) for e in range(2,33,2) for side in (False,True)]
    must(seen==expected,'complete ordered family domain')
    return {'status':'PASS','families':len(seen),'independently_audited_affine_equations':equations,'ledger_sha256':digest.hexdigest(),'imports_predecessor':False}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('ledger',type=Path);p.add_argument('--output',type=Path);a=p.parse_args()
    r=audit(a.ledger);text=json.dumps(r,indent=2,sort_keys=True)+'\n'
    if a.output:a.output.write_bytes(text.encode('utf-8'))
    print(text,end='')
