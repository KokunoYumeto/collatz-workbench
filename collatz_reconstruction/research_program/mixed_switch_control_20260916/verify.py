#!/usr/bin/env python3
"""Rebuild exact mixed-switch certificates. No floating point or assert checks.

The full finite gap domain is regenerated and hashed in canonical row order.
--ledger PATH writes every original integer comparison to a gzip JSON-lines file.
External linear-forms input is stated in note.md, not proved by these tests.
"""
from __future__ import annotations
import argparse
import copy
from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import gzip
import hashlib
import importlib.util
import json
import sys
import mixed_switch as m

ROOT = Path(__file__).resolve().parent
COUNT = Counter()


def check(ok: bool, label: str) -> None:
    COUNT[label] += 1
    m.need(ok, label)


def canonical(obj) -> bytes:
    return (json.dumps(obj, sort_keys=True, separators=(',', ':'))+'\n').encode()


def log_interval(x: int, terms: int = 160) -> tuple[F, F]:
    z = F(x-1, x+1)
    lo = 2*sum((z**(2*j+1)/F(2*j+1) for j in range(terms)), F(0))
    tail = 2*z**(2*terms+1)/(F(2*terms+1)*(1-z*z))
    return lo, lo+tail


def logarithm_certificate() -> dict:
    l2, h2 = log_interval(2); l3, h3 = log_interval(3)
    lo, hi = l3/h2, h3/l2
    left, right = F(83130157078217, 52449289519716), F(350861368503572, 221368876767703)
    check(F(2,3) < l2 < h2 < F(7,10), 'log_two_rational_enclosure')
    check(F(1) < l3 < h3 < F(11,10), 'log_three_rational_enclosure')
    check(left < lo and hi+F(1,2**128) < right, 'farey_full_interval')
    determinant = right.numerator*left.denominator-left.numerator*right.denominator
    check(determinant == 1, 'farey_determinant')
    denominator_sum = left.denominator+right.denominator
    check(denominator_sum > 2*10**12, 'farey_denominator_budget')
    # A safe rational majorant for the inspected two-log Matveev coefficient.
    matveev = F(7,5)*30**5*24*F(7,10)*F(11,10)
    check(matveev < 10**9, 'matveev_constant_majorant')
    check(4*10**12 < 2**42, 'large_size_log_bound')
    check(F(9,20)*10**12 > 5+10**9*(1+42*F(7,10)), 'large_size_contradiction')
    check(6-F(9,20)*256 < -128*F(7,10), 'narrow_gap_cutoff')
    check(sum(F(5)**j/F(__import__('math').factorial(j)) for j in range(12)) > 92,
          'log_ninety_two_less_than_five')
    check(F(81,128)**9+46*F(3,8)**9 < 1, 'long_fall_positive_margin')
    check(46*F(3,8)**9 < F(1,2), 'gap_denominator_positive')
    report = {'log_terms': 160, 'left': str(left), 'right': str(right),
              'farey_determinant': determinant, 'denominator_sum': denominator_sum,
              'gap_width': '1/2^128', 'size_cutoff': 256,
              'large_size_bound': 10**12, 'matveev_majorant': str(matveev),
              'exact_interval_sha256': hashlib.sha256(canonical([str(l2), str(h2), str(l3), str(h3)])).hexdigest()}
    return report


def gap_scan(ledger: Path | None = None) -> dict:
    digest = hashlib.sha256()
    out = None
    if ledger:
        ledger.parent.mkdir(parents=True, exist_ok=True)
        out = gzip.GzipFile(filename=str(ledger), mode='wb', mtime=0)
    rows, triples, minimum = 0, 0, None
    try:
        # alpha=P count; beta=Q count. M=r*(2*alpha+7*beta)<256.
        for alpha in range(1, 125):
            for beta in range(1, 36):
                base_m = 2*alpha+7*beta
                if 2*base_m >= 256:
                    break
                base_A = 3*alpha+11*beta
                base_L, base_U = 3**base_m, 1 << base_A
                for r in range(2, 256//base_m+1):
                    M = r*base_m
                    if M >= 256:
                        continue
                    triples += 1
                    for s in range(1, M):
                        B = 2*s
                        rhs, lhs = 3**(M+s), 1 << (r*base_A+B)
                        # Independent literal first-crossing loop.
                        while lhs <= rhs:
                            B += 1; lhs *= 2
                        check(B <= 2*M, 'first_crossing_sum_bound')
                        D = lhs-rhs
                        margin = D-46*base_L*((1 << B)-3**s)
                        check(margin > 0, 'complete_integer_gap_comparison')
                        check(margin == m.gap_margin(alpha,beta,r,s,B), 'independent_gap_formula')
                        row = [alpha,beta,r,M,s,B,D,margin]
                        data = canonical(row); digest.update(data)
                        if out: out.write(data)
                        rows += 1
                        if minimum is None or margin < minimum[-1]: minimum = row
    finally:
        if out: out.close()
    check((triples, rows) == (1197, 210527), 'complete_gap_domain_count')
    return {'triples': triples, 'rows': rows, 'minimum_margin_row': minimum,
            'canonical_rows_sha256': digest.hexdigest(),
            'domain': 'alpha,beta>=1; r>=2; 18<=M=r*(2alpha+7beta)<256; 1<=s<M; B first crossing >=2s'}


def independent_path(n: int, word: list[int]) -> tuple[list[int], list[int]]:
    x, values, actual = n, [n], []
    for a in word:
        y, k = 3*x+1, 0
        while y % 2 == 0:
            y //= 2; k += 1
        check(k == a and y > 0, 'independent_original_return')
        values.append(y); actual.append(k); x=y
    return values, actual


def conductor_and_order() -> dict:
    a,b = m.packet(m.P),m.packet(m.Q)
    pq,qp = m.packet(m.P+m.Q),m.packet(m.Q+m.P)
    check(pq.C-qp.C == -1668, 'mixed_commutator')
    for h,k in [(5,17),(17,5),(7,91)]:
        for constant in range(-3,4):
            for slope in range(-3,4):
                x,y=constant-h*slope,constant-k*slope
                check(m.interpolate_two(h,k,x,y)==(constant,slope), 'conductor_inverse')
    for n in range(1,200,2):
        check(m.interpolate_two(5,17,n+5,n+17)==(n,-1), 'original_anchor_diagonal')
        check(min(m.v2(n+5),m.v2(n+17))<=2, 'induced_depth_compatibility')
    filtration_rows=[]
    for depth in range(17):
        f=m.induced_filtration(depth);scale=f['scale'];order=f['defect_order']
        check(order==2**min(depth,2), 'induced_filtration_defect_order')
        for a in range(-2,3):
            for b in range(-2,3):
                x=scale*a;y=scale*(a+(12//order)*b)
                check((y-x)%12==0,'induced_filtration_image')
                check(((y//scale-x//scale)//(12//order))%order==b%order,'filtration_quotient_inverse')
                check(((y-x)//scale)%12==0 if b%order==0 else ((y-x)//scale)%12!=0,
                      'filtration_exact_kernel')
        filtration_rows.append(f)
    # Independent coefficient masks; a present zero remains in its declared slot.
    face_rows=[]
    for mask in [(),('P',),('Q',),('P','Q')]:
        for vals in product(range(-2,3),repeat=len(mask)):
            amplitudes=dict(zip(mask,vals));left=amplitudes.get('P',0);right=amplitudes.get('Q',0)
            residue=(right-left)%12
            check(set(amplitudes)==set(mask),'mixed_support_mask_retained')
            if residue==0:
                const,slope=m.interpolate_two(5,17,left,right)
                check((const-5*slope,const-17*slope)==(left,right),'mixed_face_kernel_inverse')
        face_rows.append({'mask':list(mask),'present_zero_slots':list(mask)})
    seam_rows=[]
    for first,second in [('P','Q'),('Q','P')]:
        for r in range(1,9):
            for s in range(1,9):
                z=m.two_packet_chart(first,r,second,s)
                for t in (0,1):
                    values,_=independent_path(z['source_anchor']+z['source_step']*t,z['full_word'])
                    check(values[-1]==z['target_anchor']+z['target_step']*t,'two_packet_chart_target')
                if (r,s) in [(1,1),(2,3)]:seam_rows.append(z)
    for r in range(1,5):
        for depth in range(20):
            z=m.switch_chart(5,17,9,8,r,depth)
            t=z['parameter_residue']+z['parameter_modulus']
            check(m.v2(9**r*t+6)==depth,'exact_reset_stratum')
    order_tests=0
    for length in range(2,8):
        for symbols in map(''.join,product('PQ',repeat=length)):
            w=tuple(a for x in symbols for a in m.LETTERS[x])
            orig=m.packet(w)
            check(m.recover_word(len(w),orig.A,orig.C)==w,'ordered_affine_inverse')
            for j in range(length-1):
                if symbols[j:j+2] != 'PQ':continue
                other=symbols[:j]+'QP'+symbols[j+2:]
                new=m.packet(tuple(a for x in other for a in m.LETTERS[x]))
                prefix=m.packet(tuple(a for x in symbols[:j] for a in m.LETTERS[x]))
                suffix=m.packet(tuple(a for x in symbols[j+2:] for a in m.LETTERS[x]))
                check(orig.C-new.C==-1668*prefix.U*suffix.L,'adjacent_swap_full_cross_term')
                order_tests+=1
    # Universal extension sections: c+(l-u)*n, without diagonal replacement.
    for l,u,c,n in product(range(-2,3),repeat=4):
        check((l*n+c)-u*n==c+(l-u)*n,'universal_extension_section')
    return {'PQ': {'L':pq.L,'U':pq.U,'C':pq.C},'QP_C':qp.C,
            'commutator_numerator':-1668,'anchor_conductor_modulus':12,
            'order_swap_tests':order_tests,'seam_examples':seam_rows,
            'induced_filtration':filtration_rows,'coefficient_faces':face_rows}


def families() -> dict:
    fixtures=accepted=0
    tails=[(2,),(3,),(4,),(2,2),(2,3),(3,2),(2,2,2)]
    anchor_rows=[]
    for length in range(2,5):
        for symbols in map(''.join,product('PQ',repeat=length)):
            if len(set(symbols))<2:continue
            size=sum(len(m.LETTERS[x]) for x in symbols)
            for phase in range(size):
                c=m.core(symbols,phase)
                check(c['anchor_numerator'] <= 91*c['anchor_denominator'],'all_phase_anchor_bound')
                if symbols=='PQ':anchor_rows.append(c)
                for r in (2,3):
                    chart=m.source_chart(symbols,phase,r)
                    n=chart['source_anchor'];h=c['anchor_numerator'];d=c['anchor_denominator']
                    check(d*n+h==2*chart['U']*chart['parameter_minimum'],'rational_lattice_inverse')
                    for tail in tails:
                        f=m.family(symbols,phase,r,tail);fixtures+=1
                        accepted += f['status']=='PROVED_WHOLE_CYLINDER_DESCENT'
                        full=c['word']*r+list(tail)
                        # An independent packet calculation, from the original word.
                        C=0;A=0;L=1
                        for a in full:C=3*C+2**A;A+=a;L*=3
                        check((L,2**A,C)==(f['L'],f['U'],f['C']),'independent_full_affine_packet')
                        # Original anchor and a nonzero source lift, with unchanged targets.
                        for z in (0,1):
                            values,_=independent_path(f['source_anchor']+f['source_step']*z,full)
                            check(values[-1]==f['target_anchor']+f['target_step']*z,'full_source_target_lift')
                            if f['D']>0:check(values[-1]<values[0],'actual_whole_family_descent')
    return {'fixtures':fixtures,'accepted':accepted,'retained':fixtures-accepted,'PQ_phase_records':anchor_rows}


def examples_and_firstjet() -> list[dict]:
    previous=ROOT.parent/'intrinsic_zero_firstjet_20260915'/'firstjet.py'
    need_hash='97f9ef5ad535f7ec18259d41fab6a3557be17d98'
    raw=previous.read_bytes()
    check(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==need_hash,'original_firstjet_blob')
    spec=importlib.util.spec_from_file_location('original_firstjet',previous)
    mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
    output=[]
    for symbols,phase,r,tail in [('PQ',0,2,[3]),('PQ',0,3,[3]),('PPQQPQ',0,2,[2,2,2,2])]:
        f=m.family(symbols,phase,r,tail)
        full=f['core']['word']*r+tail
        record=m.path(f['source_anchor'],full)
        chain={int(k):v for k,v in record['chain'].items()}
        const,linear=mod.jet_boundary({},chain)
        check(const=={} and linear=={f['source_anchor']:1,f['target_anchor']:-1},'original_firstjet_descent_relation')
        # The endpoint witness is separately evaluated and remains a POINT certificate.
        end=mod.witness(f['target_anchor'],cap=10000)
        check(end['status']=='verified_finite_first_order_boundary','example_endpoint_witness')
        combined=Counter(chain);combined.update(end['linear_chain'])
        witness=mod.validate_witness(f['source_anchor'],end['constant_cycle'],dict(combined))
        vals,_=independent_path(f['source_anchor'],witness['exponents'])
        check(vals[-1]==1,'independent_example_arrival')
        output.append({'family':f,'point_witness_returns':witness['returns'],
                       'point_witness_sha256':hashlib.sha256(canonical(witness)).hexdigest(),
                       'point_witness':witness})
    return output


def rejected_controls() -> list[str]:
    tests=[('missing_Q',lambda:m.core('PP')),('missing_P',lambda:m.core('QQ')),
           ('unknown_packet',lambda:m.core('PR')),('negative_phase',lambda:m.core('PQ',-1)),
           ('outside_phase',lambda:m.core('PQ',9)),('single_repeat',lambda:m.family('PQ',0,1,[2])),
           ('nonfalling_tail',lambda:m.family('PQ',0,2,[1])),('empty_tail',lambda:m.family('PQ',0,2,[])),
           ('fractional_repeat',lambda:m.family('PQ',0,F(5,2),[2])),
           ('conductor_false_pair',lambda:m.interpolate_two(5,17,0,1)),
           ('fake_affine_word',lambda:m.recover_word(2,3,6))]
    valid=m.family('PQ',0,2,[3])
    for key in ['C','source_anchor','target_step','mixed_displacement_numerator','count_uniform_gap_margin']:
        bad=copy.deepcopy(valid);bad[key]+=1
        tests.append(('mutated_'+key,lambda b=bad:m.validate_family(b)))
    rejected=[]
    for name,run in tests:
        try:run()
        except (m.CertificateError,TypeError):rejected.append(name)
        else:raise m.CertificateError('false control accepted: '+name)
    check(len(rejected)==len(tests),'all_false_controls_rejected')
    return rejected


def main() -> None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path);ap.add_argument('--check',type=Path)
    ap.add_argument('--ledger',type=Path)
    args=ap.parse_args()
    result={'status':'PASS','logarithm':logarithm_certificate(),'gap_scan':gap_scan(args.ledger),
            'mixed_maps':conductor_and_order(),'families':families(),
            'examples':examples_and_firstjet(),'rejected':rejected_controls(),
            'external_proof_dependency':'Matveev rational two-log bound, as specified in note.md',
            'global_convergence_claim':False}
    result['check_counts']=dict(sorted(COUNT.items()));result['total_exact_checks']=sum(COUNT.values())
    data=canonical(result)
    if args.check:m.need(args.check.read_bytes()==data,'recorded result differs byte-for-byte')
    if args.output:args.output.write_bytes(data)
    print(json.dumps({'status':'PASS','total_exact_checks':result['total_exact_checks'],
                      'gap_rows':result['gap_scan']['rows'],'family_fixtures':result['families']['fixtures'],
                      'sha256':hashlib.sha256(data).hexdigest()},sort_keys=True))


if __name__=='__main__':main()
