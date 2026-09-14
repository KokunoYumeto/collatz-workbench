#!/usr/bin/env python3
"""Rebuild the exact bounded checks; all checks also run with python -O."""
from __future__ import annotations
import copy
import itertools
from fractions import Fraction
from math import gcd
import hashlib
import json
import random
from collections import Counter
from pathlib import Path
import completion as C

counts = Counter()

def check(test: bool, kind: str) -> None:
    if not test:
        raise AssertionError(kind)
    counts[kind] += 1


def reject(fn, kind: str) -> None:
    try:
        fn()
    except (ValueError, TypeError):
        counts['rejected_'+kind] += 1
    else:
        raise AssertionError('accepted invalid '+kind)


def independent_path(n: int, N: int, sign: int = 1) -> tuple[int,int,list]:
    edges, exponent = [], 0
    for _ in range(N):
        if n == 1:
            break
        m, a = 3*n+sign, 0
        while m % 2 == 0:
            a += 1
            m //= 2
        edges.append([n,a,m]); exponent += a-1; n=m
    return n,exponent,edges


def main() -> dict:
    rng = random.Random(20260914)
    for n in range(3,260,2):
        for N in range(13):
            p=C.trajectory(n,N)
            y,b,edges=independent_path(n,N)
            check((p['endpoint'],p['v_power'],p['original_edges'])==(y,b,edges),
                  'independent_original_path')
    for _ in range(130):
        src=sorted(rng.sample(list(range(3,260,2)),14))
        N=rng.randrange(13)
        k=C.kernel_presentation(src,N)
        C.validate_kernel(k)
        check(k['rank_identity'],'kernel_rank_identity')
        for row in k['kernel_basis']:
            relation=C.from_rows(row['vector'])
            check(C.iterate(relation,N)=={},'exact_kernel_basis_vector')
            check(C.iterate(relation,N+1)=={},'kernel_filtration_inclusion')
        vector=C.combine([((0,rng.randrange(5),n),rng.randrange(-4,5))
                          for n in src for _ in range(2)])
        a,b=C.decompose(vector,k)
        check(C.add(a,b)==vector,'kernel_complement_inverse')
        check(C.iterate(a,N)=={},'kernel_component_zero')
        check(C.iterate(vector,N)==C.iterate(b,N),'unscaled_original_image')
        check({n for _,_,n in b}<=set(r['selected_source'] for r in k['image_generators']),
              'complement_original_carrier')
    for n in range(3,130,2):
        for cap in [0,1,2,4,8,16,32,48]:
            q={(0,0,n):1}
            cert=C.completion_certificate(q,cap,[n])
            C.validate_completion(cert)
            primitive=C.from_rows(cert['primitive_jet'])
            residual=C.from_rows(cert['original_residual'])
            check(C.add(C.differential(primitive),residual)==q,'jet_exact_boundary')
            check(C.truncation(C.differential(primitive),cap)==q,'truncated_complex_zero')
            y,b,_=independent_path(n,cap+1)
            expected={} if y==1 else {(cap+1,b,y):1}
            check(residual==expected,'independent_original_residual')
            check(cert['declared_sources']==[n],'zero_keeps_declared_source')
    for _ in range(180):
        src=sorted(rng.sample(list(range(3,90,2)),5))
        q=C.combine([((rng.randrange(5),rng.randrange(4),n),rng.randrange(-3,4))
                     for n in src for _ in range(3)])
        f=C.combine([((rng.randrange(4),rng.randrange(3),n),rng.randrange(-3,4))
                     for n in src for _ in range(2)])
        q2=C.add(q,C.differential(f)); cap=9
        # d(f) introduces actual one-step endpoints. Retain them in both carriers.
        src=sorted(set(src)|{n for _,_,n in q2})
        g=C.from_rows(C.completion_certificate(q,cap,src)['primitive_jet'])
        g2=C.from_rows(C.completion_certificate(q2,cap,src)['primitive_jet'])
        check(g2==C.add(g,f),'completion_quotient_representative_identity')
        d,b,p=C.terminal_vector(q)
        check(C.add(C.differential(p),C.shift(b,du=d))==q,'terminal_vector_chain_identity')
        # The original polynomial q and u*S(q) differ by d(q).
        check(C.add(q,C.shift(C.S(q),du=1),-1)==C.differential(q),'invertible_clock_class_relation')
        for N in [1,2,5]:
            term=q; witness={}
            for j in range(N):
                witness=C.add(witness,C.shift(term,du=j)); term=C.S(term)
            check(C.add(C.differential(witness),C.shift(term,du=N))==q,
                  'finite_telescoping_u_divisibility')
    arithmetic_fixtures=0
    for length in range(1,5):
        for word in itertools.product(range(1,5), repeat=length):
            r=C.arithmetic_return(word); arithmetic_fixtures+=1
            x=Fraction(r['C'],r['D']); start=x
            for a in word:
                x=(3*x+1)/2**a
            check(x==start,'independent_rational_cycle_closure')
            check(start.denominator==r['integral_mark_order'],'integral_defect_denominator_order')
            # Arbitrary polynomial forcing q = u^i v^j in the scalar comparison.
            i,j=length+1,sum(word)+1
            alpha_q=Fraction(2,3)**i * 2**j
            left=(alpha_q/Fraction(r['alpha_1_minus_W']))/3
            right=Fraction(-3**(length-1),r['D'])*alpha_q
            check(left==right,'quotient_connecting_square')
    prime=C.arithmetic_return((1,1,2,4,3))
    check(prime['returned_primitive']=='5/19','original_prime_power_primitive')
    check(gcd(1805,19)==19 and 475%19==0 and 475%361!=0,
          'original_prime_power_failed_lift')
    reject(lambda:C.arithmetic_return([]),'empty_cyclic_word')
    # Genuine cycle for the explicitly changed forcing, not a positive 3n+1 cycle.
    for cap in range(2,27):
        cert=C.completion_certificate({(0,0,5):1},cap,[5], 'collatz_minus_control')
        g=C.from_rows(cert['primitive_jet'])
        numerator=C.add(g,C.shift(g,du=2,dv=1),-1)
        check(C.truncation(numerator,cap)=={(0,0,5):1,(1,0,7):1},
              'cycle_geometric_primitive_coefficients')
        check(bool(cert['original_residual']),'cycle_never_erased_by_cutoff')
        k=C.kernel_presentation([5,7],cap,'collatz_minus_control')
        check(k['kernel_rank']==0,'cycle_constant_source_kernel')
    # Abstract ray control uses its own operator and vertex labels.
    for cap in range(27):
        cert=C.completion_certificate({(0,0,2):1},cap,[2],'ray_control')
        g=C.from_rows(cert['primitive_jet'])
        check(g=={(j,0,2+j):1 for j in range(cap+1)},'ray_original_support_growth')
        check(cert['original_residual']==[[cap+1,0,cap+3,1]],'ray_retained_endpoint')
    # Arbitrarily long genuine all-one prefixes; these are DIFFERENT sources.
    for N in list(range(1,51))+[64,128,256,512]:
        n=(1 << (N+1))-1
        p=C.trajectory(n,N)
        expected=2*3**N-1
        check(p['endpoint']==expected and p['v_power']==0,'unbounded_actual_prefix_formula')
        check(all(a==1 for _,a,_ in p['original_edges']),'all_one_actual_valuations')
        check(all(y>n for _,_,y in p['original_edges']),'all_one_no_descent_prefix')
    # Same-support linear cancellation is explicitly retained.
    merge=C.kernel_presentation([3,5,13],1)
    check(merge['kernel_rank']==2 and merge['image_rank']==1,'actual_kernel_example_ranks')
    vector={(0,2,3):1,(0,0,13):-1}
    cert=C.completion_certificate(vector,0,[3,13])
    check(cert['status']=='finite_boundary_certificate','synchronized_zero_certificate')
    check(cert['declared_sources']==[3,13] and cert['source_paths'][0]['endpoint']==5,
          'synchronized_zero_carrier_and_maps_retained')
    zero=C.completion_certificate({},0,[3,13])
    check(zero['ambient_support_label']==cert['ambient_support_label'],'supported_zero_same_fibre')
    check(zero['ambient_support_label']!=C.completion_certificate({},0,[])['ambient_support_label'],
          'supported_zero_distinct_from_absence')
    changed=copy.deepcopy(cert); changed['declared_sources']=[]
    reject(lambda:C.validate_completion(changed),'erased_source_carrier')
    changed=C.completion_certificate({(0,0,27):1},8,[27])
    changed['original_residual']=[]
    reject(lambda:C.validate_completion(changed),'erased_terminal_residual')
    changed=copy.deepcopy(merge); changed['kernel_basis'][0]['vector'][0][3]=2
    reject(lambda:C.validate_kernel(changed),'changed_kernel_generator')
    changed=copy.deepcopy(cert); changed['source_paths'][0]['original_edges'][0][1]=2
    reject(lambda:C.validate_completion(changed),'changed_original_exponent')
    reject(lambda:C.trajectory(4,1),'even_source')
    reject(lambda:C.trajectory(3,-1),'negative_return_count')
    reject(lambda:C.completion_certificate({(3,0,3):1},2,[3]),'incomplete_forcing_cap')
    reject(lambda:C.kernel_presentation([],0,'not_an_operator'),'unknown_empty_operator')
    reject(lambda:C.decompose({(1,0,3):1},merge),'wrong_coefficient_ring')
    reject(lambda:C.from_rows([[0,-1,3,1]]),'negative_clock_exponent')
    source27=C.completion_certificate({(0,0,27):1},40,[27])
    check(source27['status']=='finite_boundary_certificate','source27_polynomial_primitive')
    check(len(source27['primitive_jet'])==41,'source27_original_clock_degree')
    examples={
        'arithmetic_return_13':C.arithmetic_return((1,3)),
        'arithmetic_return_22':C.arithmetic_return((2,2)),
        'prime_power_return':prime,
        'actual_kernel_at_one_return':merge,
        'actual_supported_cancellation':cert,
        'source27_at_cutoff8':C.completion_certificate({(0,0,27):1},8,[27]),
        'source27_polynomial':{'returns':41, 'u_degree':40,
                            'primitive_sha256':hashlib.sha256(json.dumps(source27,sort_keys=True).encode()).hexdigest()},
        'control_cycle_at_cutoff4':C.completion_certificate({(0,0,5):1},4,[5],'collatz_minus_control'),
        'control_ray_at_cutoff4':C.completion_certificate({(0,0,2):1},4,[2],'ray_control'),
    }
    return {'schema':1,'scope':'Exact finite regressions; infinite statements have written proofs.',
            'operator':'original odd-return 3n+1, plus separately named controls',
            'checks':dict(sorted(counts.items())), 'total_checks':sum(counts.values()),
            'fixtures':{'kernel_presentations':130,'polynomial_forcings':180,
                        'source_jet_fixtures':512,'independent_path_fixtures':1677,
                        'max_all_one_prefix_length':512,'arithmetic_word_fixtures':arithmetic_fixtures},
            'examples':examples,'global_convergence_proved':False,
            'nontrivial_positive_cycle_found':False}

if __name__=='__main__':
    print(json.dumps(main(),sort_keys=True,separators=(',',':')))
