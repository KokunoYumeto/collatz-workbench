#!/usr/bin/env python3
"""Exact regression and complete family-domain checks. No assert statements."""
from __future__ import annotations
from collections import Counter
from fractions import Fraction
from math import comb, gcd
from pathlib import Path
import argparse
import gzip
import hashlib
import importlib.util
import json
import sys
import bilateral_control as b

COUNTS=Counter()
def check(ok: bool, category: str) -> None:
    if not ok:
        raise b.CertificateError('verification failed: '+category)
    COUNTS[category]+=1

def independent_packet(word):
    # Explicit sum, then a step-by-step lift of the ORIGINAL source congruence.
    A=0;C=0;m=len(word)
    for j,a in enumerate(word):
        C+=3**(m-1-j)*2**A;A+=a
    rho,eta,previous_A,L=1,1,0,1
    for a in word:
        residue=((2**(a-1)-(3*eta+1)//2)*pow(3*L,-1,2**a))%(2**a)
        rho+=2**(previous_A+1)*residue
        eta=(3*eta+1+6*L*residue)//2**a
        L*=3;previous_A+=a
    return L,2**A,C,rho,eta

def affine_leg(c: int, slope: int, word, target: int, target_slope: int, category: str):
    check(c>0 and c%2==1 and slope>0 and slope%2==0,category+'_input')
    peak_c,peak_s=c,slope
    for a in word:
        z,ss=3*c+1,3*slope
        check(z%(2**a)==0 and ss%(2**a)==0,category+'_divisibility')
        c,slope=z//2**a,ss//2**a
        check(c>0 and c%2==1 and slope>0 and slope%2==0,category+'_odd_endpoint')
        peak_c=max(peak_c,c);peak_s=max(peak_s,slope)
    check((c,slope)==(target,target_slope),category+'_terminal')
    return peak_c,peak_s

def family_columns(f,category):
    affine_leg(f['n0'],f['nstep'],f['left_word'],f['y0'],f['ystep'],category+'_left')
    affine_leg(f['m0'],f['mstep'],f['right_word'],f['y0'],f['ystep'],category+'_right')
    check(f['height_constant']==f['n0']-f['m0'] and f['height_slope']==f['nstep']-f['mstep'],category+'_height_equation')
    check(f['height_constant']>0 and f['height_slope']>0,category+'_complete_positive_height')

def firstjet_module():
    source=Path(__file__).resolve().parent.parent/'intrinsic_zero_firstjet_20260915'/'firstjet.py'
    data=source.read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    check(blob=='97f9ef5ad535f7ec18259d41fab6a3557be17d98','unchanged_firstjet_source')
    spec=importlib.util.spec_from_file_location('_retained_firstjet_bilateral',source)
    module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
    return module,blob

def run(ledger: Path | None=None) -> dict:
    COUNTS.clear()
    catalogue=b.catalogues();summary=catalogue['summary']
    check(summary['old_candidate_words']==20397 and summary['old_selected_families']==370,'published_catalogue_counts')
    check(summary['old_root_residues']==93025,'published_root_count')
    check(summary['ordered_pairs']==112050 and summary['compatible_pairs']==24107,'complete_pair_domain_counts')
    check(summary['new_selected_families']==67 and summary['new_root_residues']==739770,'new_cover_counts')
    # Count the complete domain independently by the positive-composition identity.
    composition_count=0
    all_rows_digest=hashlib.sha256();all_rows=0
    stream=None;raw=None
    if ledger:
        raw=ledger.open('wb');stream=gzip.GzipFile(filename='',fileobj=raw,mode='wb',mtime=0,compresslevel=5)
    try:
        for lw in b.LEFTS:
            l=independent_packet(lw);Al=sum(lw);ml=len(lw)
            for k in range(1,13):
                cap=0
                while 2**(cap+1)*l[0]<l[1]*3**k:cap+=1
                # cap=0 includes no positive word if the inequality already fails.
                if not 2**cap*l[0]<l[1]*3**k or cap<k:continue
                composition_count+=comb(cap,k)
                for rw in b.words_length_sum_le(k,cap):
                    f=b.join_family(lw,rw)
                    row=b.compact(f);all_rows_digest.update(row);all_rows+=1
                    if stream:stream.write(row)
                    r=independent_packet(rw)
                    check(f['left_data']==list(l) and f['right_data']==list(r),'independent_packet_and_lift')
                    g=gcd(l[0],r[0]);compatible=(l[4]-r[4])%(2*g)==0
                    check(f['compatible']==compatible,'independent_target_compatibility')
                    if not compatible:
                        check(f['domain'] is None and f['declared_comparison_retained'],'empty_comparison_face_retained')
                        continue
                    y0=l[4] if ml>=k else r[4]
                    target_step=2*l[0]*r[0]//g
                    nl=(l[1]*y0-l[2])//l[0];nr=(r[1]*y0-r[2])//r[0]
                    ns=l[1]*target_step//l[0];ms=r[1]*target_step//r[0]
                    check((nl,nr,ns,ms,y0,target_step)==(f['n0'],f['m0'],f['nstep'],f['mstep'],f['y0'],f['ystep']),'independent_original_join_parameters')
                    check(0<nl<ns and 0<nr<ms and f['domain']==[0,None],'entire_canonical_positive_family')
                    family_columns(f,'finite_pair')
    finally:
        if stream:stream.close()
        if raw:raw.close()
    check(composition_count==all_rows==112050,'independent_complete_composition_count')
    check(all_rows_digest.hexdigest()==summary['all_pair_records_sha256'],'all_candidate_faces_digest')
    # Independently union every compatible family, not only the selected cover.
    union=bytearray(catalogue['old_mask']*8)
    for f in reversed(catalogue['compatible_candidates']):
        view=union[f['n0']::f['nstep']]
        union[f['n0']::f['nstep']]=b'\0'*len(view)
    check(bytes(union)==catalogue['new_mask'],'all_pairs_union_equals_selected_cover')
    # Every old candidate has its complete source/target affine columns replayed.
    for f in catalogue['old_candidates']:
        family_columns(f,'published_pair')
    layer_hash=hashlib.sha256();layer_count=0;new_points=0;saturation_points=0
    minimum_a=[]
    for layer in range(1,129):
        for e in (2,6):
            f=b.layer_family(layer,e,True);a=f['a'];Q=f['Q'];K=f['K'];J=f['J'];h=f['h']
            check(K<Q and (a==1 or 2**(a-1+e+2*layer-1)>=3**(a-1+layer)),'minimal_leading_run')
            check(a<=layer+2*e-2,'all_layer_explicit_length_bound')
            if layer>1:check(a-b.layer_family(layer-1,e,True)['a'] in(0,1),'adjacent_minimal_run_increment')
            check(f['nstep']==32*Q and f['mstep']==32*K,'layer_original_lattices')
            check(b.v3(f['n0'])==layer and f['ternary_unit']==(2 if e==2 else 1),'exact_layer_and_unit')
            check((J*f['n0']+h*3**layer)%Q==0 and f['n0']%32==27,'layer_original_congruences')
            check(Fraction(h*2**a,3**a)<1,'negative_height_translation')
            family_columns(f,'all_layer')
            layer_hash.update(b.compact(f));layer_count+=1
            old=b.layer_family(layer,6 if e==2 else 2,False)
            check(min(a,old['a'])>=2,'overlap_precision_at_least_two')
            if e==2:
                check(old['J']==32*J and 32*h-old['h']==42 and b.v3(42)==1,'exact_old_new_overlap_obstruction')
            else:
                check(J==8*old['J'] and h-8*old['h']==6 and b.v3(6)==1,'exact_old_new_overlap_obstruction')
            for t in (0,1,7):
                n=f['n0']+f['nstep']*t
                move=b.layer_move(n,True)
                check(move is not None and move.target<n,'maximal_layer_move')
                check(b.layer_move(n,False) is None,'old_new_layer_disjoint_original_points')
                Z=J*(n//3**layer)+h;amax=b.v3(Z)
                check(amax>=a and len(move.right_word)==amax+layer+3,'maximal_original_word_recovery')
                k=b.floor_log3(n)
                check(amax<=k+layer+e-1,'maximal_run_logarithmic_length_bound')
                check(max(move.left_values+move.right_values)<=b.support_bound(n),'all_layer_subquadratic_support')
                # Exact chain comparison to the minimal run followed by incoming ones.
                mmin=f['m0']+f['mstep']*t
                minmove=b.make_move(n,mmin,f['left_word'],f['right_word'],'minimal_layer')
                extra=amax-a
                incoming=b.path(move.target,(1,)*extra)
                check(incoming[-1]==mmin,'maximal_to_minimal_original_path')
                correction=b.scale((-1,-(minmove.clock-extra)),b.weighted_path(incoming))
                check(b.add_vectors(minmove.chain,correction)==move.chain,'maximal_minimal_chain_identity')
                new_points+=1
            if layer<=10:
                mask=catalogue['new_mask'];P=len(mask)
                values=[mask[f['n0']%P]] if f['nstep']>=P else mask[f['n0']::f['nstep']]
                expected=layer>=5 if e==2 else layer>=2
                check(all(bool(x)==expected for x in values),'complete_low_layer_residue_cover')
                minimum_a.append([layer,e,a,sum(values),len(values)])
    check(catalogue['new_mask'][177147]==1 and 177147%32==27 and 177147%3**11==0,'all_high_layers_single_retained_residue')
    for layer in (1,2,3,5,11,32):
        for e in (2,6):
            for depth in range(13):
                for unit in (1,2):
                    f=b.saturation_stratum(layer,e,depth,unit)
                    family_columns(f,'saturation')
                    for t in (0,1,4):
                        n=f['n0']+f['nstep']*t
                        move=b.layer_move(n,True)
                        check(move.target==f['m0']+f['mstep']*t and list(move.right_word)==f['right_word'],'all_depth_stratum_inverse')
                        check(b.v3(f['W0']+f['parent_defect_slope']*(f['parent_parameter_anchor']+f['parent_parameter_step']*t))==depth,'exact_saturation_depth')
                        saturation_points+=1
    # Nested integral maps on original source columns, including active new faces.
    retractions=[b.Retraction(stage) for stage in range(3)]
    active=[f['n0'] for f in catalogue['selected'][:20]]
    active += [b.layer_family(j,e,True)['n0'] for j,e in ((2,6),(3,6),(5,2),(6,2))]
    sample=sorted(set(range(1,256,2))|set(active)|{1731,27,8808219})
    certificates=[]
    for n in sample:
        v={n:b.ONE};dv=b.jet_d(v)
        for stage,R in enumerate(retractions):
            h=R.H(v);q=R.Q(v);f=R.F(v)
            check(b.jet_d(h)==b.add_vectors(v,b.scale((-1,0),q)),'global_dH_identity')
            check(R.Q(q)==q and R.H(q)=={},'global_Q_projection_and_HQ')
            check(R.F(f)==f and b.jet_d(f)==R.Q(dv),'global_F_projection_and_chain_map')
            check(R.F(h)=={},'global_FH_identity')
            cert=R.certificate(n)
            check((cert['root']==n)==b.root_test(n,stage),'root_formula_equals_original_rule')
        for old,new in ((0,1),(1,2),(0,2)):
            R0,R1=retractions[old],retractions[new]
            K=b.add_vectors(R1.H(v),b.scale((-1,0),R0.H(v)))
            check(R0.F(K)==K,'new_correction_in_old_image')
            check(R0.F(R1.F(v))==R1.F(v) and R1.F(R0.F(v))==R1.F(v),'two_projection_compositions')
            check(R0.Q(R1.Q(v))==R1.Q(v) and R1.Q(R0.Q(v))==R1.Q(v),'two_root_projection_compositions')
        if n in (1275,27,8808219,4313979):certificates.append(retractions[-1].certificate(n))
    for n in range(1,2048,2):
        check((b.choose_move(n,2) is None)==b.root_test(n,2),'whole_original_root_membership')
    for n in range(27,5000):
        k=b.floor_log3(n)
        check(64*n*4**k//3**k+21>=130*(n+1),'large_height_bound_exact_form')
    firstjet,firstjet_blob=firstjet_module();points=[]
    for n in (1275,8808219,4313979,118607355):
        root,clock,h,_,_=retractions[-1].resolve(n)
        lower=firstjet.witness(root,1000)
        check(lower['status']=='verified_finite_first_order_boundary','original_lower_point_certificate')
        c=Counter({int(i):int(v) for i,v in lower['linear_chain'].items()})
        c.update({i:a[0] for i,a in h.items()})
        b0={int(i):int(v) for i,v in lower['constant_cycle'].items()}
        witness=firstjet.validate_witness(n,b0,{i:v for i,v in c.items() if v})
        check(witness['values'][0]==n and witness['values'][-1]==1,'integral_join_witness_path_extraction')
        points.append(witness)
    failures=[]
    controls=[('zero source',lambda:b.step(0)),('even source',lambda:b.step(4)),
        ('zero exponent',lambda:b.packet((1,0))),('boolean exponent',lambda:b.packet((True,))),
        ('invalid layer',lambda:b.layer_family(0,2,True)),('unsupported middle exponent',lambda:b.layer_family(1,4,True)),
        ('invalid depth',lambda:b.saturation_stratum(1,2,-1,1)),('zero ternary unit',lambda:b.saturation_stratum(1,2,0,0)),
        ('incompatible CRT',lambda:b.crt_pair(0,3,1,3)),('false original path',lambda:b.path(27,(2,))),
        ('nondecreasing move',lambda:b.make_move(3,5,(1,),(),'false')),
        ('false joined endpoints',lambda:b.make_move(7,3,(1,),(1,),'false')),
        ('rational original witness',lambda:firstjet.validate_witness(3,{1:Fraction(-1,2)},{3:1,5:1})),
        ('false singleton boundary',lambda:firstjet.validate_witness(3,{1:-1},{3:1})),
        ('bad stage',lambda:b.Retraction(3)),('invalid height',lambda:b.support_bound(0))]
    altered=dict(catalogue['selected'][0]);altered['nstep']+=2
    controls.append(('altered source lattice',lambda:b.family_move(altered,0)))
    for name,fn in controls:
        try:fn()
        except (b.CertificateError,firstjet.CertificateError):failures.append(name)
        else:raise b.CertificateError('invalid control accepted: '+name)
    check(len(failures)==17,'rejected_invalid_controls')
    env=b.envelope(11611)
    check(env['record_rows'][-2:]==[[10946,17349,8129266],[11611,18403,9966964]],'next_crossing_record')
    return {'status':'PASS','counts':dict(sorted(COUNTS.items())),
            'total_exact_checks':sum(COUNTS.values()),'complete_catalogue':summary,
            'complete_pair_rows':all_rows,'complete_pair_ledger_sha256':all_rows_digest.hexdigest(),
            'all_layer_fixtures':layer_count,'all_layer_fixture_sha256':layer_hash.hexdigest(),
            'original_maximal_layer_point_checks':new_points,
            'original_saturation_point_checks':saturation_points,
            'low_layer_cover_rows':minimum_a,'new_selected_families':catalogue['selected'],
            'retraction_certificates':certificates,'independently_extracted_point_witnesses':points,
            'firstjet_source_git_blob':firstjet_blob,'rejected_controls':failures,
            'next_record':[11611,18403,9966964],
            'scope':'general proofs in note.md; complete finite pair domain; bounded regression; no universal Collatz claim'}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path);ap.add_argument('--ledger',type=Path);ap.add_argument('--check',type=Path)
    args=ap.parse_args()
    result=run(args.ledger);data=json.dumps(result,sort_keys=True,indent=2).encode()+b'\n'
    if args.check:
        check_bytes=args.check.read_bytes()
        if data!=check_bytes:raise b.CertificateError('recorded verification bytes changed')
    if args.output:args.output.write_bytes(data)
    print(json.dumps({'status':'PASS','total_exact_checks':result['total_exact_checks'],
                      'pair_rows':result['complete_pair_rows'],'sha256':hashlib.sha256(data).hexdigest()},sort_keys=True))
if __name__=='__main__':main()
