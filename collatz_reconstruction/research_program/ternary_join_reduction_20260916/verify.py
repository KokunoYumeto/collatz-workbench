#!/usr/bin/env python3
"""Complete finite catalogue, exact family regressions, original witness receiver."""
from __future__ import annotations
import argparse
from collections import Counter
from dataclasses import replace
import hashlib
import importlib.util
import json
from math import comb
from pathlib import Path
import sys
import join_control as j
ROOT=Path(__file__).resolve().parent
COUNTS=Counter()
def check(ok,name):
    if not ok:raise j.CertificateError(name)
    COUNTS[name]+=1
def encode(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def sha(x):return hashlib.sha256(encode(x)).hexdigest()
def affine_trace(x,s,w):
    for a in w:
        mod=1<<a;t=3*x+1;u=3*s
        check(t%mod==u%mod==0,'affine_divisibility');x=t//mod;s=u//mod
        check(x>0 and x%2==1 and s%2==0,'original_affine_oddness')
    return x,s

def run():
    COUNTS.clear();families=[]
    for b in range(1,65):
        for e in(2,6):
            f=j.layer(b,e);a=f['a'];n=f['source_anchor'];m=f['smaller_anchor']
            check(f['K']<f['Q'] and 3*f['K']>=2*f['Q'],'minimal_run')
            check(a<=b+2*e and f['h']*2**a<3**a,'finite_run_and_negative_intercept')
            check(j.v3(n)==b and (n//3**b)%3==f['source_ternary_unit'],'actual_ternary_layer')
            if b<64:check(j.layer(b+1,e)['a']-a in(0,1),'adjacent_layer')
            check(affine_trace(n,f['source_step'],[1])==affine_trace(m,f['smaller_step'],f['word'])==(f['target_anchor'],f['target_step']),'complete_layer_coefficient_identity')
            for t in(0,1,7,3**(b+2)):
                x=n+f['source_step']*t;z=m+f['smaller_step']*t
                check(j.layer_for_source(x)==f and z<x,'layer_source_inverse_and_height')
                v=j.path(z,f['word']);check(v[-1]==j.step(x)[0],'original_layer_target')
                check(max(v)<=64*x*x+21,'layer_quadratic_bound')
            families.append({k:f[k] for k in('b','e','a','source_anchor','source_step','smaller_anchor','smaller_step','signed_clock')})
    cand=j.candidates();wc=Counter();stream=hashlib.sha256()
    for f in cand:
        w=f['word'];k=len(w);wc[k]+=1
        check(sum(w)<=(3**(k-1)).bit_length() and w[-1]%2,'candidate_domain')
        check(0<f['smaller_anchor']<f['source_anchor']<f['source_step'] and f['source_step']>f['smaller_step'],'complete_residue_height')
        check(affine_trace(f['source_anchor'],f['source_step'],[1])==affine_trace(f['smaller_anchor'],f['smaller_step'],w)==(f['target_anchor'],f['target_step']),'complete_candidate_equations')
        stream.update(encode(f))
    counts={}
    for k in range(2,13):
        counts[k]=sum(comb(A-l-1,k-2) for A in range(k,(3**(k-1)).bit_length()+1) for l in range(1,A-k+2,2))
    check(dict(wc)==counts,'independent_word_count')
    cat=j.catalogue();P=cat['period'];R=set(cat['remaining']);cover=bytearray(P//4)
    for f in cand:
        for n in range(f['source_anchor'],P,f['source_step']):cover[(n-3)//4]=1
    rem=[n for n in range(3,P,4) if j.old_root_residue(n) and not cover[(n-3)//4]]
    check(rem==cat['remaining'],'independent_residue_union')
    check(sum(f['new_residues'] for f in cat['selected'])+len(R)==cat['old_root_count'],'exact_cover_conservation')
    check(177147 in R,'all_high_ternary_layers')
    for e in(2,6):
        for b in range(1,65):
            f=j.layer(b,e);p=f['source_step'];n=f['source_anchor']
            hit=n%P in R if p>=P else any(x in R for x in range(n,P,p))
            check(hit==((b>=5) if e==2 else (b>=2)),'catalogue_layer_comparison')
    old=j.Retraction('old');mid=j.Retraction('catalogue');new=j.Retraction('full')
    fixtures=list(range(1,128,2))+[f['source_anchor'] for f in cat['selected'][:8]]
    for n in dict.fromkeys(fixtures):
        v={n:(1,0)}
        for A in(old,mid,new):
            h=A.H(v);q=A.Q(v);ff=A.F(v)
            check(j.d(h)==j.add(v,j.negative(q)),'original_homotopy')
            check(A.Q(q)==q and A.H(q)=={},'vertex_retraction')
            check(A.F(ff)==ff and A.F(h)=={},'edge_retraction')
            check(j.d(ff)==A.Q(j.d(v)),'chain_map')
            check(not h or max(h)<=64*n*n+21,'global_support_bound')
            if n>=3:
                B=0;x=n
                while x>=3:x//=3;B+=1
                K=(n-1)//2*(2*B+14)
                check(sum(abs(z[0]) for z in h.values())<=K and sum(abs(z[1]) for z in h.values())<=K*K,'global_coefficient_bounds')
        for A,B in((old,mid),(mid,new),(old,new)):
            k=j.add(B.H(v),j.negative(A.H(v)))
            check(A.F(k)==k,'correction_in_original_image')
            check(B.F(A.F(v))==A.F(B.F(v))==B.F(v),'nested_edge_maps')
            check(B.Q(A.Q(v))==A.Q(B.Q(v))==B.Q(v),'nested_vertex_maps')
    src=ROOT.parent/'intrinsic_zero_firstjet_20260915'/'firstjet.py'
    check(hashlib.sha256(src.read_bytes()).hexdigest()=='a53cef65109285f377e2c1344ae662c4a74574a30c1c40dfffebc9ed6cca06b0','original_receiver_hash')
    spec=importlib.util.spec_from_file_location('original_firstjet',src);fj=importlib.util.module_from_spec(spec);sys.modules[spec.name]=fj;spec.loader.exec_module(fj)
    examples=[]
    for n in(91,6219,75195,1536975,13704327,734883):
        root,k,h=new.resolve(n);check(root<=6728241,'example_root_in_certified_window')
        base=fj.witness(root,cap=10000);check(base['status']=='verified_finite_first_order_boundary','root_witness')
        linear=Counter(base['linear_chain'])
        for x,z in h.items():linear[x]+=z[0]
        cert=fj.validate_witness(n,base['constant_cycle'],dict(linear));check(cert['values'][-1]==1,'original_extracted_path')
        examples.append({'source':n,'old_root':old.resolve(n)[0],'new_root':root,'signed_clock':k,'actual_odd_returns':cert['returns'],'original_values':cert['values'],'original_exponents':cert['exponents'],'constant_cycle':base['constant_cycle'],'linear_chain':{str(x):z for x,z in sorted(linear.items()) if z}})
    bad=[('zero_layer',lambda:j.layer(0,2)),('wrong_exponent',lambda:j.layer(1,4)),('boolean_layer',lambda:j.layer(True,2)),('even_source',lambda:j.layer_for_source(6)),('wrong_final_parity',lambda:j.original_family((1,2))),('wrong_expansion',lambda:j.original_family((3,3,3))),('wrong_mode',lambda:j.Retraction('gone'))]
    move=j.join_move(6219,j.layer(2,2))
    bad.extend([('lost_clock',lambda:j.check_move(replace(move,clock=0))),('lost_chain',lambda:j.check_move(replace(move,chain={}))),('wrong_height',lambda:j.check_move(replace(move,target=move.source))),('wrong_target',lambda:j.check_move(replace(move,right=move.right[:-1]+(1,)))),('outside_residue',lambda:j.join_move(6221,j.layer(2,2)))])
    rejected=[]
    for name,call in bad:
        try:call()
        except(ValueError,TypeError):rejected.append(name)
        else:raise j.CertificateError('invalid control accepted: '+name)
    check(len(rejected)==12,'negative_controls')
    return {'status':'PASS','counts':dict(sorted(COUNTS.items())),'total_exact_checks':sum(COUNTS.values()),'layer_objects':families,'candidate_counts':dict(wc),'candidate_count':len(cand),'candidate_stream_sha256':stream.hexdigest(),'catalogue_period':P,'old_root_count':cat['old_root_count'],'selected_families':cat['selected'],'remaining_root_count':len(R),'remaining_residue_sha256':sha(cat['remaining']),'all_masks_sha256':sha(cat['candidate_labels']),'examples':examples,'rejected_controls':rejected,'global_convergence_claim':False}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path);p.add_argument('--check',type=Path);a=p.parse_args()
    result=run();data=encode(result)
    if a.output:a.output.write_bytes(data)
    receipt={'status':'PASS','total_exact_checks':result['total_exact_checks'],'candidate_count':result['candidate_count'],'selected_families':len(result['selected_families']),'remaining_root_count':result['remaining_root_count'],'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}
    if a.check:j.need(receipt==json.loads(a.check.read_text()),'exact result differs from recorded receipt')
    print(json.dumps(receipt,sort_keys=True))
if __name__=='__main__':main()
