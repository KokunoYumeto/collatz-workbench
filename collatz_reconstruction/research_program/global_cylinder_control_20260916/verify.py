#!/usr/bin/env python3
"""Replay exact finite proof certificates and bounded global-control regressions."""
from __future__ import annotations
import argparse
from collections import Counter
import copy
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

from global_control import (CertificateError, Packet, crossing_audit, crossing_value,
    cylinder_certificate, divided_step, first_crossing_partition, gap_certificate,
    need, packet, path_certificate, step)

HERE=Path(__file__).resolve().parent
COUNT=Counter()

def check(name,ok):
    need(bool(ok),name)
    COUNT[name]+=1


def load_firstjet():
    p=HERE.parent/'intrinsic_zero_firstjet_20260915'/'firstjet.py'
    need(p.is_file(),'preserved firstjet.py is required')
    data=p.read_bytes()
    git=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    need(git=='97f9ef5ad535f7ec18259d41fab6a3557be17d98','first-jet source differs from pinned Git blob')
    spec=importlib.util.spec_from_file_location('original_firstjet',p)
    need(spec is not None and spec.loader is not None,'cannot import original validator')
    module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
    return module


def all_words():
    h=hashlib.sha256();stack=[Packet()];counts=Counter();exceptions=[]
    while stack:
        p=stack.pop()
        if p.m:
            counts['words']+=1
            # Original numerator from the independent explicit sum.
            A=0;C=0
            for j,a in enumerate(p.word):
                C+=3**(p.m-j-1)*(1<<A);A+=a
            check('word_original_coefficients',C==p.C and A==p.A and p.L==3**p.m)
            check('word_canonical_residue',p.rho==((p.U-p.C)*pow(p.L,-1,2*p.U))%(2*p.U))
            check('word_original_endpoint',p.U*p.image==p.L*p.rho+p.C)
            if p.D>0:
                counts['contracting']+=1
                check('word_power_gap',(p.D+1)*(1<<p.m)>p.L)
                bound=1<<(p.A-p.word[-1]+1)
                check('word_threshold_bound',p.C<p.D*bound)
                tmin=1 if p.image>=p.rho else 0
                check('word_tail_descent',p.rho+2*p.U*tmin>p.image+2*p.L*tmin)
                if tmin:
                    counts['canonical_exceptions']+=1;exceptions.append([list(p.word),p.rho,p.image])
            else:counts['expanding']+=1
            h.update((json.dumps([list(p.word),p.rho,p.image,p.D],separators=(',',':'))+'\n').encode())
        for a in range(18-p.A,0,-1):stack.append(p.append(a))
    check('composition_count',counts['words']==2**18-1)
    check('small_word_exceptions',exceptions==[[[2]*j,1,1] for j in range(1,10)])
    return {'exponent_sum_bound':18,'counts':dict(counts),'exceptions':exceptions,'row_sha256':h.hexdigest()}


def binary_words():
    # Generate each original parity cylinder by literally iterating its canonical source.
    # U=2^length. These are the shortened elementary map (odd step includes one division).
    count=0;exceptions=0
    for length in range(1,15):
        U=1<<length
        for rho in range(U):
            x=rho;L=1;C=0;two=1;odd=0;bits=[]
            for j in range(length):
                b=x%2;bits.append(b)
                if b:
                    x=(3*x+1)//2;C=3*C+two;L*=3;odd+=1
                else:x//=2
                two*=2
            check('binary_affine',U*x==L*rho+C)
            if U>L:
                check('binary_threshold',C<(U-L)*U)
                check('binary_noncanonical_descent',x+L<rho+U)
                if rho>0 and x>=rho:exceptions+=1
            count+=1
    return {'length_bound':14,'parity_cylinders':count,'canonical_positive_exceptions':exceptions}


def fixture_checks(firstjet):
    out=[];prefixes=[(),(1,),(1,2),(1,1),(1,2,1,1,1,2,1,1,4)]
    P=(1,2);Q=(1,1,1,2,1,1,4)
    prefixes += [P+Q+Q+P,Q+P+Q,P*12,Q*4,(1,)*32]
    for prefix in prefixes:
        part=first_crossing_partition(prefix)
        # Whole high-exponent family is one progression, every low child remains explicit.
        p=packet(prefix);h=part['crossing_next_exponents']['minimum']
        check('next_threshold',(p.U<<(h-1))<3*p.L<(p.U<<h))
        for t in range(25):
            value=crossing_value(part,t);n=value['source'];word=value['full_word']
            c=path_certificate(n,word);check('crossing_actual_endpoint',c['endpoint']==value['endpoint'])
            check('crossing_last_exponent',value['last_exponent']>=h)
            bad=part['exception_source']==n
            check('crossing_descent_scope',c['strict_descent']==(not bad))
            check('crossing_proper_prefixes',all(x>=n for x in c['values'][:-1]))
            b={int(k):v for k,v in c['original_chain'].items()}
            const,linear=firstjet.jet_boundary({},b)
            check('firstjet_original_boundary',const=={} and linear=={int(k):v for k,v in c['firstjet_linear_boundary'].items()})
        # Test actual arbitrary-depth exponent strata by constructing their original digits.
        for a in [h,h+1,h+17,h+64,h+129]:
            full=p.append(a)
            for lift in [0,1,3]:
                n=full.rho+2*full.U*lift
                need((n-part['crossing_source_anchor'])%part['crossing_source_step']==0,'child misses whole crossing progression')
                c=path_certificate(n,full.word)
                check('deep_crossing_valuation',c['word'][-1]==a)
                check('deep_crossing_descent',c['strict_descent'] or n==part['exception_source'])
        part['sample']=crossing_value(part,0)
        out.append(part)
    return out


def explicit_examples(firstjet):
    # A true coefficient contraction can fail to give endpoint descent at its CANONICAL point.
    w=(4,1,1,1,1,2,2,1,2,1,1,2,1,1,1,2,3)
    cert=cylinder_certificate(w);check('paradoxical_source',cert['source_anchor']==165 and cert['target_anchor']==167)
    check('paradoxical_exception',cert['nondescending_source_points']==[165])
    a=path_certificate(165,w);b=path_certificate(165+cert['source_step'],w)
    check('paradoxical_not_first_crossing',a['values'][1]<165)
    check('translated_repair',b['strict_descent'])
    cert['canonical_path']=a;cert['first_translated_path']=b
    cert['canonical_arrival_witness']=firstjet.witness(165,1000)
    check('canonical_arrival',cert['canonical_arrival_witness']['status']=='verified_finite_first_order_boundary')
    # A long genuine first crossing beyond the exhaustive certificate bound.
    n=27;x=n;A=0;L=1;word=[]
    while 1<<A<=L:
        x,a=divided_step(x);word.append(a);A+=a;L*=3
    c=cylinder_certificate(word)
    check('27_first_crossing',len(word)==37 and x==23 and c['source_anchor']==27)
    c['path']=path_certificate(27,word)
    c['firstjet_arrival_witness']=firstjet.witness(27,1000)
    # Matveev input boundary and hypothetical corruption controls are separate below.
    return {'canonical_nondescending_example':cert,'long_first_crossing':c,
            'fixed_loop':cylinder_certificate((2,)),
            'strict_cylinder':cylinder_certificate((1,3))}


def negative_controls(firstjet):
    rejected=[]
    tests=[('zero_exponent',lambda:packet((0,))),('negative_exponent',lambda:packet((-1,))),
      ('boolean_exponent',lambda:packet((True,))),('empty_cylinder',lambda:cylinder_certificate(())),
      ('crossed_prefix',lambda:first_crossing_partition((2,))),
      ('even_source',lambda:path_certificate(2,(1,))),
      ('false_valuation_word',lambda:path_certificate(3,(2,))),
      ('negative_parameter',lambda:crossing_value(first_crossing_partition((1,)),-1)),
      ('unsupported_audit_bound',lambda:crossing_audit(0)),
      ('false_fixed_descent',lambda:need(cylinder_certificate((2,))['strict_descent_parameter_min']==0,'fixed point does not descend')),
      ('false_multiplier_inference',lambda:need(cylinder_certificate((4,1,1,1,1,2,2,1,2,1,1,2,1,1,1,2,3))['nondescending_source_points']==[],'retained exception was erased')),
      ('false_arrival_boundary',lambda:firstjet.validate_witness(3,{1:-1},{3:1})),
      ('nonintegral_firstjet',lambda:firstjet.validate_witness(3,{1:F(-1,2)},{3:1,5:1}))]
    damaged=first_crossing_partition((1,2));damaged['crossing_source_step']+=2
    tests.append(('corrupt_crossing_lattice',lambda:crossing_value(damaged,0)))
    for name,fn in tests:
        try:fn()
        except (CertificateError,firstjet.CertificateError):rejected.append(name)
        else:raise CertificateError('false control accepted: '+name)
    return rejected


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path);ap.add_argument('--check',type=Path)
    ap.add_argument('--ledger',type=Path)
    args=ap.parse_args();firstjet=load_firstjet()
    gap=gap_certificate();gap_bytes=(json.dumps(gap,sort_keys=True,indent=2)+'\n').encode()
    check('gap_certificate_bytes',gap_bytes==(HERE/'power_gap_certificate.json').read_bytes())
    result={'scope':'all-length arithmetic proof has written argument plus explicit external theorem; bounded regressions are separate',
      'gap_certificate_sha256':hashlib.sha256(gap_bytes).hexdigest(),
      'word_regressions':all_words(),'binary_regressions':binary_words(),
      'source_partitions':fixture_checks(firstjet),'examples':explicit_examples(firstjet),
      'rejected_controls':negative_controls(firstjet)}
    result['complete_first_crossing_audit']=crossing_audit(18,args.ledger)
    result['named_checks']=dict(sorted(COUNT.items()));result['total_named_checks']=sum(COUNT.values())
    result['status']='PASS';result['global_collatz_proof_claim']=False
    text=json.dumps(result,sort_keys=True,indent=2)+'\n';data=text.encode()
    if args.output:args.output.write_bytes(data)
    if args.check:need(data==args.check.read_bytes(),'regenerated verification is not byte-identical')
    print(json.dumps({'status':'PASS','checks':result['total_named_checks'],'prefixes':result['complete_first_crossing_audit']['total_prefixes'],
      'sha256':hashlib.sha256(data).hexdigest(),'check':args.check is not None},sort_keys=True))

if __name__=='__main__':main()
