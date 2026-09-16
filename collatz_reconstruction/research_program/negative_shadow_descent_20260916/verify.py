#!/usr/bin/env python3
"""Rebuild exact arithmetic evidence; no asserts, floating-point or web access.

The finite certificate verifies the displayed specialization and all subsequent
arithmetic steps, not Matveev's external transcendence theorem. Output is
identical under python and python -O. Prior first-jet source is hash-pinned.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from fractions import Fraction as F
import gzip
import hashlib
import importlib.util
from itertools import product
import json
from math import comb, factorial, gcd
from pathlib import Path
import sys

import shadow_descent as sd

HERE = Path(__file__).resolve().parent
CHECKS: Counter[str] = Counter()
FIRSTJET_SHA = '97f9ef5ad535f7ec18259d41fab6a3557be17d98'


def check(condition: bool, group: str, message: str) -> None:
    if not condition:
        raise sd.CertificateError(group+': '+message)
    CHECKS[group] += 1


def canonical(value) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(',', ':'))+'\n').encode()


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_firstjet():
    path = HERE.parent/'intrinsic_zero_firstjet_20260915'/'firstjet.py'
    data = path.read_bytes()
    blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    check(blob == FIRSTJET_SHA, 'source_identity', 'first-jet file is not the authenticated predecessor')
    spec = importlib.util.spec_from_file_location('_pinned_intrinsic_firstjet', path)
    check(spec is not None and spec.loader is not None, 'source_identity', 'cannot load first-jet source')
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def divided_step(n: int) -> tuple[int, int]:
    value, count = 3*n+1, 0
    while value % 2 == 0:
        value //= 2
        count += 1
    return value, count


def log_bounds(x: int, terms: int = 128) -> tuple[F, F]:
    z = F(x-1, x+1)
    lower = sum((2*z**(2*j+1)/F(2*j+1) for j in range(terms)), F(0))
    tail = 2*z**(2*terms+1)/F(2*terms+1)/(1-z*z)
    return lower, lower+tail


def logarithm_certificate() -> dict:
    l2, u2 = log_bounds(2)
    l3, u3 = log_bounds(3)
    check(F(1,2) < l2 < u2 < F(7,10), 'logarithm', 'log 2 elementary bounds')
    check(F(1) < l3 < u3 < F(11,10), 'logarithm', 'log 3 elementary bounds')
    gamma_lo, gamma_hi = l3/u2, u3/l2
    lower = F(83130157078217, 52449289519716)
    upper = F(350861368503572, 221368876767703)
    check(lower < gamma_lo, 'logarithm', 'lower rational neighbour')
    check(gamma_hi+F(1,1 << 128) < upper, 'logarithm', 'upper rational neighbour with retained gap')
    determinant = upper.numerator*lower.denominator-lower.numerator*upper.denominator
    check(determinant == 1, 'logarithm', 'unimodular rational interval')
    denominator_sum = lower.denominator+upper.denominator
    check(denominator_sum > 9*10**12, 'logarithm', 'period denominator ceiling')
    coefficient = F(14,10)*30**5*24*F(7,10)*F(11,10)
    check(coefficient == 628689600 < 10**9, 'logarithm', 'safe Matveev coefficient')
    exp36 = sum((F(36**j, factorial(j)) for j in range(101)), F(0))
    exp5 = sum((F(5**j, factorial(j)) for j in range(7)), F(0))
    check(exp36 > 15*10**12, 'logarithm', 'finite proof log(15*10^12)<36')
    check(exp5 > 92, 'logarithm', 'finite proof log 92<5')
    check(10**12 > 10**9*37+5, 'logarithm', 'large-repetition exclusion endpoint')
    check(F(10**9,10**12) < 1, 'logarithm', 'monotonic derivative on excluded halfline')
    check(184*(1 << 128) < 8**128, 'logarithm', 'exponential gap at repetition 128')
    return {'terms': 128, 'log2_interval': [str(l2),str(u2)],
            'log3_interval': [str(l3),str(u3)], 'lower_neighbour': str(lower),
            'upper_neighbour': str(upper), 'neighbour_determinant': determinant,
            'neighbour_denominator_sum': denominator_sum,
            'retained_ratio_gap': '1/2^128', 'Matveev_safe_constant': 10**9,
            'external_theorem_is_not_proved_by_checker': True,
            'hypothetical_exception_repetition_upper_bound': 10**12,
            'exception_denominator_upper_bound': 9*10**12,
            'remaining_repetitions': [1,127]}


def base_certificate() -> tuple[dict, dict]:
    tables, trace = [], hashlib.sha256()
    smallest = {}
    for U,L,K in ((8,9,4),(2048,2187,46)):
        check(U >= 2*K and U < L, 'coarse_domain', 'anchor size bound')
        check(16*U-9*L > 7*K, 'coarse_domain', 'all r, s>=2r induction seed')
        check(16*U > 16 and 9*L > 9, 'coarse_domain', 'termwise power comparison')
        rows, margin_min = [], None
        for r in range(1,128):
            ur, lr = U**r,L**r
            for s in range(1,2*r+1):
                B = sd.least_contracting_tail_sum(U,L,r,s)
                check(2*s <= B <= 4*r, 'integer_gap_base', 'complete exponent interval')
                check(ur*(1 << B) > lr*3**s, 'integer_gap_base', 'positive original coefficient gap')
                check(B == 2*s or ur*(1 << (B-1)) <= lr*3**s,
                      'integer_gap_base', 'least exponent at fixed original r,s')
                margin = (ur-K)*(1 << B)-(lr-K)*3**s
                check(margin > 0, 'integer_gap_base', 'required strict gap margin')
                rows.append([r,s,B])
                trace.update(canonical([U,L,K,r,s,B,margin]))
                margin_min = margin if margin_min is None else min(margin_min,margin)
        check(len(rows) == 16256, 'integer_gap_base', 'all 127 complete repetition rows')
        tables.append({'U':U,'L':L,'K':K,'rows':rows})
        smallest[str(U)] = margin_min
    return {'format':'complete_gap_bases_v1','tables':tables}, {
        'complete_base_rows': sum(len(t['rows']) for t in tables),
        'exact_margin_trace_sha256': trace.hexdigest(),
        'smallest_positive_base_margin': smallest,
        'large_repetition_domain_proved_in_note': 'r >= 128',
        'large_tail_domain_proved_in_note': 's >= 2*r, all B >= 2*s',
    }


def check_anchors() -> list[dict]:
    records = []
    for h, word in sd.ANCHORS.items():
        p = sd.anchor_packet(h)
        n, values = -h, [-h]
        for a in word:
            n,b = divided_step(n)
            check(a == b and n < 0, 'signed_original_edges', 'signed original orbit')
            values.append(n)
        check(n == -h and len(set(values[:-1])) == len(word), 'signed_anchors', 'primitive signed cycle')
        check(p.C == (p.L-p.U)*h and p.C % p.D == 0, 'signed_anchors', 'supported integral forcing zero')
        check(gcd(p.L-p.U,2*p.U) == 1, 'signed_anchors', 'repeat congruence inverse')
        records.append({'h':h,'word':list(word),'values':values,'L':p.L,'U':p.U,'C':p.C,
                        'D':p.D,'integral_primitive':-h,'marked_forcing_class':0,
                        'positive_cycle':False})
        for r in (1,2,4):
            w = word*r
            for t in (1,2,7,19):
                sh = sd.shadow(h,r,t)
                n = sh['source']
                for a in w:
                    n, b = divided_step(n)
                    check(n > 0 and a == b,'positive_shadow_edges','original lifted valuation')
                check(n == sh['packet_endpoint'], 'positive_shadow_chart', 'exact endpoint')
                check((sh['source']+h)//(2*p.U**r) == t, 'positive_shadow_chart', 'source inverse')
                check((n+h)//(2*p.L**r) == t, 'positive_shadow_chart', 'target inverse')
            for start in range(1,256,2):
                x, actual = start, True
                for a in w:
                    x,b = divided_step(x)
                    if a != b:
                        actual = False; break
                check(actual == ((start+h) % (2*p.U**r) == 0), 'cylinder_converse', 'complete small original source domain')
    return records


def check_families(firstjet) -> dict:
    fixtures=accepted=retained=edges=0
    for h in sd.ANCHORS:
        p=sd.anchor_packet(h)
        for r in (1,2,3):
            for s in (1,2,3):
                for tail in product((2,3,4), repeat=s):
                    f=sd.family(h,r,tail)
                    sd.validate_family(f)
                    full=sd.packet(p.word*r+tail)
                    check((f['original_L'],f['original_U'],f['original_C']) == (full.L,full.U,full.C),
                          'affine_family','expanded original numerator')
                    q=sd.packet(tail)
                    check(q.C+q.L-q.U <= 0, 'affine_family','retained anchored tail forcing')
                    check((q.C+q.L-q.U == 0) == all(c==2 for c in tail),
                          'affine_family','supported zero tail does not erase its relations')
                    if f['strict_descent_for_whole_cylinder']:
                        accepted+=1
                        check(f['original_section_defect_at_shadow_min'] < 0,
                              'affine_family','original affine correction at lower source bound')
                        check(full.C % full.D != 0, 'cycle_fixture','no positive integral fixed point in accepted family')
                    else: retained+=1
                    for v in (0,1,7):
                        source=f['source_anchor']+f['source_step']*v
                        x=source; chain=Counter()
                        for a in full.word:
                            chain[x]+=1
                            x,b=divided_step(x); edges+=1
                            check(a==b,'positive_family_edges','independent source valuation')
                        check(x == f['target_anchor']+f['target_step']*v, 'affine_family','unchanged target progression')
                        if f['strict_descent_for_whole_cylinder']:
                            check(x < source,'affine_family','positive original descent')
                        const,lin=firstjet.jet_boundary({},dict(chain))
                        target=Counter({source:1}); target[x]-=1
                        check(const == {} and lin == firstjet.clean(target), 'jet_descent','untruncated first-jet boundary')
                    fixtures+=1
    # Very large individual fall exponents remain in the theorem domain.
    for h in (5,17,91):
        for r in (4,8):
            for tail in ((128,), (2,512), (3,2,257)):
                f=sd.family(h,r,tail)
                check(f['strict_descent_for_whole_cylinder'], 'large_valuation','unbounded valuation stratum')
                path=sd.original_path(f['source_anchor'], sd.ANCHORS[h]*r+tail)
                check(path['strict_descent'], 'large_valuation','large-valuation original replay')
    return {'family_fixtures':fixtures,'accepted_cylinders':accepted,'retained_cylinders':retained,
            'independently_divided_positive_family_edges':edges}


def check_residuals() -> list[dict]:
    out=[]
    for h in (5,17):
        p=sd.anchor_packet(h)
        for r in range(1,25):
            rec=sd.residual_counts(h,r)
            for row in rec['rows'][1:]:
                s,H=row['tail_length'],row['maximum_tail_sum']
                count=sum(comb(B-s-1,s-1) for B in range(2*s,H+1))
                check(count == row['words'], 'residual_language','complete composition count')
                check(p.U**r*(1 << H) < p.L**r*3**s,
                      'residual_language','retained top coefficient')
                check(p.U**r*(1 << (H+1)) > p.L**r*3**s,
                      'residual_language','next exponent crosses exactly')
            out.append(rec)
    # The previously unexcluded 1507-rise sector includes this exact ordering.
    r,s,B=1507,617,1234
    D=8**r*(1 << B)-9**r*3**s
    check(D > 0, 'retained_sector','original (m,A)=(3631,5755) coefficient crossing')
    check((2*r+s,3*r+B,r)==(3631,5755,1507), 'retained_sector','literal count/word crosswalk')
    check(sd.gap_value(8,9,4,r,s,B) > 0, 'retained_sector','large original gap margin')
    return out


def examples(firstjet) -> list[dict]:
    output=[]
    for h,r,t in ((5,2,1),(5,8,1),(17,1,1),(17,4,1)):
        rec=sd.falling_prefix_after_shadow(h,r,t)
        check(rec['status']=='CERTIFIED_DESCENT','example','new exact block accepted')
        endpoint=rec['path']['endpoint']
        continuation=firstjet.witness(endpoint,10000)
        check(continuation['status']=='verified_finite_first_order_boundary','example','finite endpoint certificate')
        chain=Counter({int(k):v for k,v in rec['path']['original_edge_chain'].items()})
        chain.update(continuation['linear_chain'])
        witness=firstjet.validate_witness(rec['path']['source'],continuation['constant_cycle'],dict(chain))
        check(witness['values'][-1] == 1,'example','actual path extracted from spliced integral boundary')
        output.append({'new_descent':rec,'finite_singleton_witness':witness})
    # A genuinely retained switch: never relabel this as an accepted block.
    retained=sd.falling_prefix_after_shadow(5,12,1)
    check(retained['status'] != 'CERTIFIED_DESCENT','retained_example','unproved switch retained')
    output.append({'retained_query':retained})
    return output



def elementary_cones() -> list[dict]:
    records=[]
    for U,L,K,d in ((8,9,4,2),(2048,2187,46,4)):
        mu=3*L**d
        check(4*U**d > mu > 7, 'elementary_cones','exact block-induction multipliers')
        seeds=[]
        for r in range(1,d+1):
            margin=sd.gap_value(U,L,K,r,1,2)
            check(margin>0,'elementary_cones','complete cone base')
            seeds.append([r,margin])
        for r in range(1,65):
            ss=(r+d-1)//d
            old=sd.gap_value(U,L,K,r,ss,2*ss)
            new=sd.gap_value(U,L,K,r+d,ss+1,2*ss+2)
            correction=(4*U**d-mu)*U**r*4**ss+K*((mu-4)*4**ss-(mu-3)*3**ss)
            check(new-mu*old == correction > 0,'elementary_cones','independent exact induction identity')
        records.append({'U':U,'L':L,'K':K,'denominator':d,'seeds':seeds,
                        'induction_multiplier':mu,'logarithm_dependency':False})
    return records


def reset_checks(firstjet) -> dict:
    count=0
    for r in range(1,257):
        check(sd.valuation2(9**r-1) == 3+sd.valuation2(r), 'reset','integer exponent-lifting identity')
        for t in (1,9,17,65):
            rec=sd.reset_after_three(r,t)
            x=rec['after_three']
            for j in range(rec['next_maximal_one_run']):
                x,a=divided_step(x)
                check(a==1,'reset_edges','original maximal rising-run exponent')
            check(x==rec['after_one_run'] and divided_step(x)[1]>=2,
                  'reset','rising-run endpoint and actual next fall')
            count+=1
    for r in range(1,9):
        for k in range(33):
            mod=1 << (k+4)
            t=(pow(9**r,-1,mod)*(1+(1 << (k+3))))%mod
            rec=sd.reset_after_three(r,t)
            check(rec['next_maximal_one_run']==k and t%8==1,'reset_strata','all declared exact reset residues')
    repair=sd.switched_repair_family()
    w=tuple(repair['word'])
    for v in (0,1,7):
        source=repair['source_anchor']+v*repair['source_step']
        x=source; chain=Counter()
        for j,expected in enumerate(w,1):
            chain[x]+=1; x,a=divided_step(x)
            check(a==expected,'repair_edges','original switched word')
            if j<len(w):check(x>=source,'repair_first_descent','no earlier descent')
        check(x==repair['target_anchor']+v*repair['target_step'] < source,
              'repair_first_descent','whole original cylinder endpoint')
        const,lin=firstjet.jet_boundary({},dict(chain))
        check(const=={} and lin=={source:1,x:-1},'repair_jet','original first-jet relation')
    end=firstjet.witness(repair['target_anchor'],10000)
    check(end['status']=='verified_finite_first_order_boundary','repair_jet','repaired endpoint has a finite witness')
    path=sd.original_path(repair['source_anchor'],w)
    chain=Counter({int(k):v for k,v in path['original_edge_chain'].items()});chain.update(end['linear_chain'])
    witness=firstjet.validate_witness(repair['source_anchor'],end['constant_cycle'],dict(chain))
    check(witness['values'][-1]==1,'repair_jet','full repaired singleton path extracted')
    return {'reset_parameter_fixtures':count,'exact_reset_strata':8*33,
            'repair':repair,'repair_extracted_returns_to_one':witness['returns'],
            'repair_source_witness':witness}


def reject_controls() -> int:
    count=0
    def reject(fn):
        nonlocal count
        try: fn()
        except (sd.CertificateError,TypeError): count+=1
        else: raise sd.CertificateError('malformed input was accepted')
    for h in (1,3,-5,True): reject(lambda h=h: sd.anchor_packet(h))
    for r in (0,-1,True): reject(lambda r=r: sd.family(5,r,(2,)))
    for tail in ((),(1,),(2,0),(2,True)):
        reject(lambda tail=tail: sd.family(5,2,tail))
    for t in (0,-1): reject(lambda t=t: sd.shadow(5,2,t))
    for t in (2,3,5,7): reject(lambda t=t: sd.reset_after_three(12,t))
    good=sd.family(17,4,(2,))
    for key in ('original_C','source_step','target_anchor','tail_anchored_forcing'):
        corrupt=deepcopy(good);corrupt[key]+=1
        reject(lambda corrupt=corrupt: sd.validate_family(corrupt))
    bad=sd.family(5,12,(2,))
    check(not bad['strict_descent_for_whole_cylinder'],'rejection_control','uncrossed domain is retained')
    bad['status']='CERTIFIED_DESCENT';bad['strict_descent_for_whole_cylinder']=True
    reject(lambda:sd.validate_family(bad))
    CHECKS['rejected_invalid_inputs']+=count
    return count


def build() -> tuple[dict,bytes,bytes]:
    firstjet=load_firstjet()
    log=logarithm_certificate()
    base,summary=base_certificate()
    cones=elementary_cones()
    anchors=check_anchors()
    families=check_families(firstjet)
    residuals=check_residuals()
    ex=examples(firstjet)
    resets=reset_checks(firstjet)
    rejects=reject_controls()
    base_bytes=canonical(base)
    example_bytes=canonical(ex)
    result={'status':'PASS','date':'2026-09-16','theorem':'positive_shadow_fall_descent',
            'coefficient_ring':'original integers; Matveev input explicit',
            'proof_domains': {'repetitions':'all integers >=1','tail_length':'all integers >=1',
                              'tail_exponents':'arbitrary integers >=2','acceptance':'original U_total > L_total'},
            'logarithm_certificate':log,'finite_gap_certificate':summary,
            'finite_gap_bases_sha256':sha(base_bytes),'examples_sha256':sha(example_bytes),
            'negative_anchor_records':anchors,'positive_family_scope':families,
            'elementary_cone_certificates':cones,'reset_and_repair':resets,
            'residual_count_fixtures':residuals,
            'example_summaries':[{'source':e['new_descent']['path']['source'],
                                  'endpoint':e['new_descent']['path']['endpoint'],
                                  'block_returns':len(e['new_descent']['path']['word']),
                                  'extracted_returns_to_one':e['finite_singleton_witness']['returns']}
                                 for e in ex if 'new_descent' in e],
            'rejected_inputs':rejects,'checks_by_group':dict(sorted(CHECKS.items())),
            'named_exact_checks':sum(CHECKS.values()),
            'global_Collatz_coverage_claim':False,'new_numerical_record_claim':False,
            'prior_large_atlas_is_a_proof_dependency':False}
    return result,base_bytes,example_bytes


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true',help='write deterministic results in this new directory')
    parser.add_argument('--check',action='store_true',help='require equality with all recorded evidence')
    args=parser.parse_args()
    result,base,examples_bytes=build()
    data=canonical(result)
    if args.write:
        (HERE/'verification.json').write_bytes(data)
        (HERE/'gap_bases.json.gz').write_bytes(gzip.compress(base,mtime=0))
        (HERE/'examples.json').write_bytes(examples_bytes)
    if args.check:
        check_bytes=[((HERE/'verification.json').read_bytes(),data,'verification'),
                     (gzip.decompress((HERE/'gap_bases.json.gz').read_bytes()),base,'complete base rows'),
                     ((HERE/'examples.json').read_bytes(),examples_bytes,'example witnesses')]
        for actual,expected,label in check_bytes:
            sd.require(actual==expected,label+' differs from exact reconstruction')
    print(json.dumps({'status':'PASS','named_exact_checks':result['named_exact_checks'],
                      'complete_gap_rows':result['finite_gap_certificate']['complete_base_rows'],
                      'positive_family_edges':result['positive_family_scope']['independently_divided_positive_family_edges'],
                      'verification_sha256':sha(data)},sort_keys=True))


if __name__ == '__main__':
    try: main()
    except (sd.CertificateError,OSError,ValueError) as exc: raise SystemExit(str(exc))
