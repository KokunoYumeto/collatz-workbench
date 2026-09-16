#!/usr/bin/env python3
"""Independent, all-row audit of the original two-leg family catalogue.

No contribution or predecessor module is imported. Word-domain membership,
strict ordering, and exact binomial bucket counts establish completeness.
Every original affine constant and slope is replayed by repeated division.
Incompatible comparisons remain declared records, not missing rows.
"""
from __future__ import annotations
from collections import Counter
from math import comb, gcd
from pathlib import Path
import argparse
import gzip
import hashlib
import json

LEFTS=((1,1),(1,2),(1,1,1),(1,1,2),(1,2,1))
OLD_PERIOD=4*3**11
NEW_PERIOD=8*OLD_PERIOD

class AuditError(ValueError):
    pass

def require(ok, message):
    if not ok:
        raise AuditError(message)

def literal_packet(word):
    require(isinstance(word,(list,tuple)) and all(type(a) is int and a>0 for a in word),'invalid original word')
    m=len(word);A=sum(word);L=3**m;U=2**A;C=0;power2=1
    for i,a in enumerate(word):
        C+=3**(m-1-i)*power2
        power2*=2**a
    rho=((U-C)*pow(L,-1,2*U))%(2*U)
    require(0<rho<2*U and rho%2==1,'invalid original cylinder representative')
    numerator=L*rho+C
    require(numerator%U==0,'nonintegral image anchor')
    eta=numerator//U
    require(0<eta<2*L and eta%2==1,'original image anchor outside its stated interval')
    return L,U,C,rho,eta

def expected_family(lw,rw):
    l,r=literal_packet(lw),literal_packet(rw)
    g=gcd(l[0],r[0])
    out={'left_word':list(lw),'right_word':list(rw),'left_data':list(l),'right_data':list(r),
         'signed_clock':len(lw)-len(rw),'declared_comparison_retained':True}
    if (l[4]-r[4])%(2*g):
        return {**out,'compatible':False,'domain':None}
    # Actual image moduli are powers of three times two and hence nested.
    y=l[4] if l[0]>=r[0] else r[4]
    period=2*l[0]*r[0]//g
    require(y>=max(l[4],r[4]),'common image anchor is before an original image')
    ul=(y-l[4])//(2*l[0]);ur=(y-r[4])//(2*r[0])
    n=l[3]+2*l[1]*ul;m=r[3]+2*r[1]*ur
    ns=period*l[1]//l[0];ms=period*r[1]//r[0]
    c,d=n-m,ns-ms
    if d>0:domain=[max(0,(-c)//d+1),None]
    elif d==0:domain=[0,None] if c>0 else None
    else:domain=[0,(c-1)//(-d)] if c>0 else None
    return {**out,'compatible':True,'n0':n,'nstep':ns,'m0':m,'mstep':ms,'y0':y,'ystep':period,
            'left_parameter':[ul,r[0]//g],'right_parameter':[ur,l[0]//g],
            'height_constant':c,'height_slope':d,'domain':domain}

def replay_leg(c,s,word,y,ys):
    require(c>0 and c%2==1 and s>0 and s%2==0,'incorrect source coefficient columns')
    rows=divisions=0
    for a in word:
        c=3*c+1;s=3*s;actual=0
        while c%2==0:
            require(s%2==0,'variable-source coefficient not divisible with its original constant')
            c//=2;s//=2;actual+=1;divisions+=1
        require(actual==a and c>0 and s>0 and s%2==0,'incorrect exact family valuation')
        rows+=1
    require((c,s)==(y,ys),'false common original endpoint columns')
    return rows,divisions

def compositions(length,total):
    if length==0:
        yield ();return
    for a in range(1,total-length+2):
        for rest in compositions(length-1,total-a):
            yield (a,)+rest

def old_mask():
    mask=bytearray(OLD_PERIOD)
    for n in range(3,OLD_PERIOD,4):
        mask[n]=n%36 in(3,7,15,19,27) and n%8748!=8731 and n%2916!=1731
    initial=sum(mask);words=0
    for k in range(2,13):
        limit=1
        while 2**limit<2*3**(k-1):limit+=1
        limit-=1
        for w in compositions(k,limit):
            if w[-1]%2==0:continue
            f=expected_family((1,),w);words+=1
            require(f['compatible'] and f['domain']==[0,None],'prior full-family equation fails')
            require(0<f['n0']<f['nstep'],'prior family has an omitted canonical positive source')
            mask[f['n0']::f['nstep']]=bytes(len(mask[f['n0']::f['nstep']]))
    require(words==20397 and initial==98091 and sum(mask)==93025,'prior complete domain or root mask mismatch')
    return mask

def audit(ledger: Path):
    expected_counts={}
    for i,lw in enumerate(LEFTS):
        L,U,*_=literal_packet(lw)
        for k in range(1,13):
            cap=0
            while 2**(cap+1)*L<U*3**k:cap+=1
            if 2**cap*L<U*3**k and cap>=k:expected_counts[(i,k)]=comb(cap,k)
    mask=old_mask()*8
    old_digest=hashlib.sha256(mask[:OLD_PERIOD]).hexdigest()
    counts=Counter();previous=None;total=compatible=equations=divisions=0
    digest=hashlib.sha256()
    with gzip.open(ledger,'rb') as stream:
        for line in stream:
            digest.update(line)
            record=json.loads(line)
            require(isinstance(record,dict),'invalid comparison record')
            lw=tuple(record.get('left_word',[]));rw=tuple(record.get('right_word',[]))
            require(lw in LEFTS and 1<=len(rw)<=12,'word outside complete catalogue domain')
            literal_packet(rw)
            i,k=LEFTS.index(lw),len(rw)
            key=(i,k,rw)
            require(previous is None or previous<key,'duplicate, reordered or unexpected candidate')
            previous=key
            l=literal_packet(lw)
            require(2**sum(rw)*l[0]<l[1]*3**k,'candidate violates strict coefficient comparison')
            counts[(i,k)]+=1;total+=1
            require(record==expected_family(lw,rw),'changed original maps, support flag or arithmetic face')
            if not record['compatible']:
                continue
            compatible+=1
            require(record['domain']==[0,None] and 0<record['n0']<record['nstep'],
                    'compatible family is not a whole positive residue class')
            require(record['height_constant']>0 and record['height_slope']>0,'nonpositive original source-height difference')
            for prefix in ('n','m'):
                word=lw if prefix=='n' else rw
                r,d=replay_leg(record[prefix+'0'],record[prefix+'step'],word,record['y0'],record['ystep'])
                equations+=r;divisions+=d
            require(NEW_PERIOD%record['nstep']==0,'original source period does not divide common counting period')
            mask[record['n0']::record['nstep']]=bytes(len(mask[record['n0']::record['nstep']]))
    require(dict(counts)==expected_counts,'incomplete catalogue: a finite word-domain bucket is missing or truncated')
    require(total==112050 and compatible==24107 and sum(mask)==739770,'full-catalogue counts disagree')
    return {'status':'PASS','imports_main_or_predecessor':False,'all_rows_checked':True,
            'complete_pair_rows':total,'compatible_pair_rows':compatible,
            'incompatible_declared_faces':total-compatible,
            'original_affine_equations_replayed':equations,
            'individual_coefficient_divisions_replayed':divisions,
            'complete_pair_ledger_sha256':digest.hexdigest(),
            'old_mask_sha256':old_digest,'new_mask_sha256':hashlib.sha256(mask).hexdigest(),
            'original_root_count_before_two_leg_union':93025*8,'original_root_count_after_two_leg_union':sum(mask),
            'complete_domain_bucket_counts':{f'{i}:{k}':v for (i,k),v in sorted(counts.items())}}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ledger',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    try:
        result=audit(args.ledger)
        args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({k:result[k] for k in ('status','complete_pair_rows','compatible_pair_rows','original_affine_equations_replayed','new_mask_sha256')},sort_keys=True))
    except(AuditError,ValueError,TypeError,KeyError,EOFError,OSError) as exc:
        parser.error(str(exc))
if __name__=='__main__':main()
