#!/usr/bin/env python3
"""Exact regressions plus a complete finite-source arithmetic certificate.

Named regression assertions and fully enumerated source/edge scopes are
reported separately. No timeout is interpreted as an orbit conclusion.
"""
from __future__ import annotations
import argparse
from collections import Counter
import copy
from fractions import Fraction
import gzip
import hashlib
import importlib.util
from itertools import product
import json
from pathlib import Path
import sys

import arithmetic as ar
import atlas
import logarithm_certificate as lc

HERE=Path(__file__).resolve().parent

class Checks:
    def __init__(self):self.counts=Counter()
    def check(self,ok,name):
        self.counts[name]+=1
        ar.require(bool(ok),name+' failed')


def div_step(n):
    z=3*n+1;a=0
    while z%2==0:z//=2;a+=1
    return z,a


def div_v2(n):
    if n==0:return None
    n=abs(n);a=0
    while n%2==0:n//=2;a+=1
    return a


def direct_copies(n,p,bound):
    x=n;copies=0
    for _ in range(bound):
        y=x;match=True
        for a in p:
            y,b=div_step(y)
            if a!=b:match=False;break
        if not match:return copies,x
        x=y;copies+=1
    return copies,x


def plus(a,b,sign=1):
    c=Counter(a)
    for k,v in b.items():c[k]+=sign*v
    return ar.clean(c)


def dual_plus(a,b,sign=1):return plus(a[0],b[0],sign),plus(a[1],b[1],sign)

def wmul(v,k):return dict(v[0]),plus(v[1],{n:k*c for n,c in v[0].items()})

def homotopy(n):
    t=ar.rising_tail(n);c0=Counter();c1=Counter()
    for j,x in enumerate(t['values'][:-1]):c0[x]+=1;c1[x]+=j
    return ar.clean(c0),ar.clean(c1)


def projection_vertex(n):
    t=ar.rising_tail(n)
    return {t['target']:1},({t['target']:t['r']} if t['r'] else {})


def regression(check):
    words=[p for m in range(1,5) for p in product(range(1,5),repeat=m)]
    return_zeros=0
    for p in words:
        pk=ar.packet(p)
        for n in range(1,256,2):
            rec=ar.repeat_record(n,p)
            count=rec['complete_initial_copies']
            test_depth=4 if count is None else min(4,count+1)
            k,y=direct_copies(n,p,test_depth)
            check.check(k==(test_depth if count is None else min(test_depth,count)), 'repetition_count')
            check.check(ar.repeat_endpoint(n,p,k)==y,'repetition_endpoint')
            check.check(div_v2(pk.defect(n))==rec['defect_valuation'],'independent_defect_valuation')
            if count is None:
                return_zeros+=1
                check.check(n==1 and all(a==2 for a in p),'retained_return_zero_fixture')
        for r in (1,2,5):
            pp=ar.packet(p*r)
            source=((pp.U-pp.C)*pow(pp.L,-1,2*pp.U))%(2*pp.U)
            for t in (0,1):
                n=source+2*pp.U*t
                observed,endpoint=direct_copies(n,p,r)
                check.check(observed==r,'full_repeated_cylinder')
                check.check(ar.repeat_endpoint(n,p,r)==endpoint,'full_repeated_cylinder_endpoint')
                factor=(pp.U-pp.L)//pk.D
                check.check(factor%2==1 and pp.C==factor*pk.C,'repetition_preserves_original_mark')
    small=[p for m in (1,2) for p in product((1,2,3),repeat=m)]
    switch_modes=Counter()
    for p in small:
        pk=ar.packet(p);r=((pk.U-pk.C)*pow(pk.L,-1,2*pk.U))%(2*pk.U)
        for q in small:
            for t in range(5):
                rec=ar.switch_record(r+2*pk.U*t,p,q)
                switch_modes[rec['mode']]+=1
                qk=ar.packet(q)
                check.check(pk.D*qk.defect(rec['target'])==qk.D*pk.defect(rec['target'])+rec['resultant'],
                            'exact_switch_resultant')
                check.check(div_v2(qk.defect(rec['target']))==rec['second_target_depth'],
                            'independent_switch_valuation')
    resonances=[]
    for r in list(range(2,33))+[64,128,512]:
        for v in (0,1,7):
            rec=ar.resonant_family(r,v)
            check.check(rec['strict_descent'] and rec['source']-rec['target']>0,
                        'resonant_family_actual_descent')
            check.check(rec['switch']['mode']=='resonant_layer','rank_reset_kept_in_resonance')
            if v==0 and r in (2,3,8,32,128,512):
                resonances.append({'r':r,'v':v,'source':rec['source'],'target':rec['target'],
                                    'before_first_depth':2,'after_second_depth':2*r+2,
                                    'source_step':rec['source_step'],'target_step':rec['target_step']})
    run_fixtures=0
    for a in range(1,25):
        for b in ((3*a+1)//2,(3*a+1)//2+1,(3*a+1)//2+3):
            tails=[(2,)*b,(3,)+(2,)*(b-1),(2,)*(b-1)+(3,),
                   (2,)*(b//2)+(4,)+(2,)*(b-b//2-1),
                   (3,)*b,(2,)*(b-1)+(20,),tuple(2+j%4 for j in range(b))]
            for tail in tails:
                p=ar.packet((1,)*a+tail)
                r=((p.U-p.C)*pow(p.L,-1,2*p.U))%(2*p.U)
                for t in (0,1,3):
                    n=r+2*p.U*t;rec=ar.run_witness(n,a,tail)
                    check.check(rec['strict_descent'],'unbounded_run_theorem')
                    x=n
                    for aa in (1,)*a+tail:
                        x,bb=div_step(x)
                        check.check(aa==bb,'independent_run_original_equation')
                    check.check(x==rec['target'],'independent_run_endpoint')
                    run_fixtures+=1
    weak_fixtures=0
    for a in range(1,65):
        b=1
        while (1 << (a+2*b))<=3**(a+b):b+=1
        for tail in [(2,)*b,(3,)+(2,)*(b-1),(2,)*(b-1)+(3,)]:
            p=ar.packet((1,)*a+tail);r=p.C*pow(p.D,-1,2*p.U)%(2*p.U)
            for t in (0,1,2):
                rec=ar.run_witness(r+2*p.U*t,a,tail)
                check.check(rec['target']<=rec['source'],'first_contracting_run_nonexpansion')
                weak_fixtures+=1
    # Both first-jet homotopy identities on the SAME absolute original graph.
    peak_count=0
    for n in range(1,4096,2):
        y,_=div_step(n)
        hn=homotopy(n);hy=homotopy(y)
        dH=ar.jet_boundary(*hn)
        expected=dual_plus(({n:1},{}),projection_vertex(n),-1)
        check.check(dH==expected,'firstjet_vertex_homotopy')
        Hd=dual_plus(hn,wmul(hy,1),-1)
        if n%4==1:
            block=ar.peak_block(n);peak_count+=1
            expansion=(block['jet_constant_chain'],block['jet_linear_chain'])
            rhs=dual_plus(({n:1},{}),expansion,-1)
            # Only the first source of a first-return block is in Y.
            projected0={x:c for x,c in expansion[0].items() if x%4==1}
            projected1={x:c for x,c in expansion[1].items() if x%4==1}
            check.check((projected0,projected1)==({n:1},{}),'firstjet_block_section_identity')
        else:rhs=({n:1},{})
        check.check(Hd==rhs,'firstjet_edge_homotopy')
        lhs=dual_plus(projection_vertex(n),wmul(projection_vertex(y),1),-1)
        if n%4==1:
            b=ar.peak_block(n)
            rhs=({n:1}, {})
            rhs=dual_plus(rhs,({b['target']:1},{b['target']:b['odd_return_length']}),-1)
        else:rhs=({}, {})
        check.check(lhs==rhs,'firstjet_projection_chain_map')
    block=ar.peak_block(9)
    check.check(block['values']==[9,7,11,17] and block['odd_return_length']==3,
                'retained_block_clock_control')
    residual=plus({17:-3},{17:-1},-1)
    check.check(residual=={17:-2},'incorrect_shortening_retains_nonzero_residual')
    slopes=[ar.slope_certificate(p,q) for p,q in [(3,2),(17,12),(179,127),(568,403),(2124,1507)]]
    for a in list(range(1,1508))+[1508,3014,10000]:
        p,q=2124,1507;b=(p*a+q-1)//q
        D=2**(a+2*b)-3**(a+b)
        check.check(D>3**a-2**a,'sharp_run_cone_base_and_induction_fixtures')
        r=(a-1)%q+1;h=(a-r)//q
        check.check(b==h*p+(p*r+q-1)//q,'sharp_run_cone_residue_decomposition')
    failed_packet=ar.packet((1,)*22+(2,)*31)
    failed_source=failed_packet.C*pow(failed_packet.D,-1,2*failed_packet.U)%(2*failed_packet.U)
    failed_target=failed_packet.apply(failed_source)
    vals,_=ar.actual_path(failed_source,failed_packet.word)
    check.check(failed_packet.D<0 and failed_target>failed_source and vals[-1]==failed_target,
                'overaggressive_run_slope_original_counterexample')
    return {'run_slope_certificates':slopes,
            'overaggressive_slope_control':{'numerator':31,'denominator':22,
                'source':failed_source,'target':failed_target,'D':failed_packet.D,
                'word':[1]*22+[2]*31},
            'repetition_words':len(words),'ordinary_sources_per_word':128,
            'actual_return_zero_fixtures':return_zeros,
            'switch_modes':dict(sorted(switch_modes.items())),
            'strict_run_fixtures':run_fixtures,'first_contracting_run_fixtures':weak_fixtures,
            'first_jet_original_vertex_fixtures':2048,
            'peak_block_fixtures':peak_count,'resonant_family_examples':resonances,
            'clock_control':block}


def load_predecessor():
    path=HERE.parent/'intrinsic_zero_firstjet_20260915'/'firstjet.py'
    spec=importlib.util.spec_from_file_location('original_integral_firstjet_for_descent',path)
    ar.require(spec is not None and spec.loader is not None,'first-jet predecessor unavailable')
    module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
    return module


def verify_all() -> dict:
    ch=Checks();r=regression(ch)
    raw=gzip.decompress((HERE/'atlas.json.gz').read_bytes());data=json.loads(raw)
    ch.check(raw==atlas.canonical_bytes(data),'canonical_atlas_encoding')
    cells,cover=atlas.verify_cover(data)
    index=atlas.Index(cells);old=load_predecessor()
    examples=[];jet_hash=hashlib.sha256();witness_returns=0
    sources=list(range(1,512,2))+[2*((i*7919)%583200)+1 for i in range(128)]
    sources+=list(range(1166371,1166400,2))
    for n in sources:
        w=index.witness(n)
        oldw=old.validate_witness(n,w['constant_chain'],w['linear_chain'])
        ch.check(oldw['values']==w['original_path'],'predecessor_extracts_new_atlas_witness')
        jet_hash.update(atlas.canonical_bytes(w));witness_returns+=w['original_returns']
        if n in (1,3,27,511,1166399):examples.append(w)
    E,h,graph=atlas.finite_equation_support(cells,cover['bound'])
    ch.check(len(E)==len(h),'original_equation_support_height_domain')
    ch.check(all(n in E for n in range(1,cover['bound']+1,2)),'all_initial_sources_retained_in_graph')
    period=atlas.period_bound(cover['bound']+2)
    period_checks=atlas.independent_period_check(period)
    log_record=lc.certificate()
    log_raw=atlas.canonical_bytes(log_record)
    ch.check(log_raw==(HERE/'logarithm_verification.json').read_bytes(), 'complete_exact_logarithm_certificate')
    ch.check(log_record['covered_source_minimum']==cover['bound']+2, 'logarithm_certificate_uses_certified_source_bound')
    retained=lc.validate_retained_minima()
    ch.check(retained['original_equation_support_sha256']==graph['edge_height_transcript_sha256'], 'reused_zero_original_equation_support')
    for row in retained['rows']:
        for item in row['retained_zero_sources']:
            ch.check(item['source'] in E and h[item['source']]==item['retained_height'] and all(x in E for x in item['original_values']), 'reused_zero_is_in_original_supported_fibre')
    failures=[]
    def reject(name,fn):
        try:fn()
        except (ar.CertificateError,ValueError,KeyError,TypeError):failures.append(name)
        else:raise ar.CertificateError('invalid input accepted: '+name)
    reject('negative_source',lambda:ar.repeat_record(-1,(1,)))
    reject('fractional_source',lambda:ar.repeat_record(Fraction(5,19),(1,1,2,4,3)))
    reject('boolean_source',lambda:ar.repeat_record(True,(2,)))
    reject('empty_word',lambda:ar.packet(()))
    reject('zero_exponent',lambda:ar.packet((0,)))
    reject('excess_repetitions',lambda:ar.repeat_endpoint(7,(1,),3))
    reject('false_switch_source',lambda:ar.switch_record(5,(1,),(2,)))
    reject('nonfall_letter',lambda:ar.run_witness(7,1,(1,2)))
    reject('uncontracted_run_domain',lambda:ar.run_witness(11,1,(2,)))
    reject('forged_run_word',lambda:ar.run_witness(3,1,(2,2)))
    reject('wrong_resonant_domain',lambda:ar.resonant_family(1,0))
    reject('wrong_peak_support',lambda:ar.peak_block(3))
    reject('overaggressive_universal_run_slope',lambda:ar.slope_certificate(31,22))
    bad=copy.deepcopy(data['cells'][0]);bad['C']+=1
    reject('changed_affine_offset',lambda:atlas.independent_cell(bad))
    bad_cover=dict(data);bad_cover['cells']=data['cells'][:-1]
    reject('missing_cover_cell',lambda:atlas.verify_cover(bad_cover,False))
    bad_cover2=dict(data);bad_cover2['cells']=data['cells']+[data['cells'][0]]
    reject('duplicate_cover_label',lambda:atlas.verify_cover(bad_cover2,False))
    bad_period=dict(period);bad_period['excluded_exponent_one_count']+=1
    reject('unsupported_cycle_budget',lambda:atlas.independent_period_check(bad_period))
    bad_log=copy.deepcopy(log_record);bad_log['farey']['upper'][0]+=1
    reject('changed_farey_endpoint',lambda:lc.validate_certificate(bad_log))
    bad_log_constant=copy.deepcopy(log_record);bad_log_constant['coarse_coefficient']=10
    reject('invalid_transcendence_constant',lambda:lc.validate_certificate(bad_log_constant))
    bad_retained=copy.deepcopy(retained)
    next(row for row in bad_retained['rows'] if row['retained_zero_sources'])['retained_zero_sources'][0]['original_values'][-1]=3
    reject('forged_reused_supported_zero',lambda:lc.validate_retained_minima(bad_retained))
    # A rational half of the -1 forcing control is not an integral witness.
    try:old.validate_witness(5,{5:Fraction(-1,2),7:Fraction(-1,2)},{7:Fraction(-1,2)},-1)
    except old.CertificateError:failures.append('rationalized_cycle_witness')
    else:raise ar.CertificateError('rationalized control accepted')
    return {'schema':'collatz-defect-rank-descent-verification-v1','status':'PASS',
            'base_commit':'d0c987b12c20be5978f496ab1ef2a60018caa5e5',
            'named_regression_checks':sum(ch.counts.values()),
            'regression_check_breakdown':dict(sorted(ch.counts.items())),
            'regression':r,'atlas_uncompressed_sha256':hashlib.sha256(raw).hexdigest(),
            'atlas_search':data['search'],'symbolic_cover':cover,
            'finite_original_firstjet_support':graph,'cycle_certificate':period,
            'independent_period_checks':period_checks,
            'logarithm_certificate':{'sha256':hashlib.sha256(log_raw).hexdigest(),
                'external_theorem':log_record['external_theorem'],
                'farey':log_record['farey'],
                'complete_positive_run_gap':True,
                'minimum_run_period_ratio':log_record['minimum_run_period_ratio'],
                'pure_run_finite_rows':len(log_record['pure_run_small_rows']),
                'minimum_run_finite_rows':len(log_record['small_cycle_rows']),
                'single_cyclic_one_run_excluded':True,
                'retained_zero_sources_reused':log_record['retained_zero_sources_reused'],
                'retained_zero_original_returns':log_record['retained_zero_original_returns'],
                'retained_zero_source_sha256':log_record['retained_zero_source_sha256']},
            'witness_sources':len(sources),'witness_original_returns':witness_returns,
            'witness_transcript_sha256':jet_hash.hexdigest(),
            'witness_examples':examples,'rejected_controls':failures,
            'global_collatz_resolution':False,'external_independent_review':False,
            'proof_assistant_run':False}


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path);ap.add_argument('--check',type=Path)
    args=ap.parse_args();data=verify_all();raw=atlas.canonical_bytes(data)
    if args.output:args.output.write_bytes(raw)
    if args.check:ar.require(raw==args.check.read_bytes(),'recorded verification bytes differ')
    print(json.dumps({'status':'PASS','named_regression_checks':data['named_regression_checks'],
                      'independently_divided_original_edges':data['finite_original_firstjet_support']['independently_divided_original_edges'],
                      'covered_original_sources':data['symbolic_cover']['covered_original_sources'],
                      'cycle_one_budget':data['cycle_certificate']['excluded_exponent_one_count'],
                      'sha256':hashlib.sha256(raw).hexdigest()},sort_keys=True))

if __name__=='__main__':main()
