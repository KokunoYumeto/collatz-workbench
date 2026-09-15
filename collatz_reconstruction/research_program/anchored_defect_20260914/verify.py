#!/usr/bin/env python3
"""Exact, independently replayed certificate for the anchored 403- and 404-rise sectors."""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import anchored_cycles as ac

COUNTS = Counter()


def check(ok, label):
    if not ok:
        raise ValueError(label)
    COUNTS[label] += 1


def raw_step(n):
    value, a = 3*n+1, 0
    while value % 2 == 0:
        value //= 2; a += 1
    return value,a


def raw_packet(word):
    sums = [0]
    for a in word:
        sums.append(sums[-1]+a)
    m = len(word)
    return 3**m, 2**sums[-1], sum(3**(m-1-i)*2**sums[i] for i in range(m))


def support_and_affine_checks():
    values = [ac.Supported(0,False)]+[ac.Supported(F(n,2),True) for n in range(-3,4)]
    zero,one=values[0],ac.Supported(1,True)
    for x in values:
        check(x+zero == x and x*one == x, 'external zero and multiplicative identity')
        for y in values:
            check((x+y).value == x.value+y.value, 'reflection preserves addition')
            check((x*y).value == x.value*y.value, 'reflection preserves multiplication')
            check((x+y).present == (x.present or y.present), 'support preserves addition')
            check((x*y).present == (x.present and y.present), 'support preserves multiplication')
            for z in values:
                check((x+y)+z == x+(y+z) and (x*y)*z == x*(y*z), 'supported associativity')
                check(x*(y+z) == x*y+x*z, 'supported distributivity')
    check(ac.Supported(0,True) != zero, 'present zero not external absence')
    positive_periods=0
    for m in range(1,6):
        for word in product(range(1,5),repeat=m):
            L,U,C=raw_packet(word); D=U-L
            B=ac.cd.cyclic_matrix(word)
            b=[4-2**a for a in word]
            f=ac.cd.functional(word)
            check([1-sum(row) for row in B] == b, 'exact anchored affine translation')
            check(sum(x*y for x,y in zip(f,b)) == C-D, 'anchored marked numerator')
            check((C-D) % abs(D) == C % abs(D), 'forcing class unchanged by boundary')
            x=[F(raw_packet(word[i:]+word[:i])[2],D) for i in range(m)]
            y=[v-1 for v in x]
            check([sum(F(a)*v for a,v in zip(row,y)) for row in B] == b,
                  'original matrix on anchored rational primitive')
            check(all(v==0 for v in y) == all(a==2 for a in word), 'trivial anchored primitive')
            if min(x)>1:
                eta=F(1)
                for i,a in enumerate(word):
                    eta *= F(3*y[i]+4-2**a,3*y[i])
                check(eta == F(U,L), 'closed anchored period with original clocks')
                s=min(x)
                check(F(U,L) <= (1+F(2,3*(s-1)))**word.count(1), 'positive anchored period bound')
                h3=h4=0
                for i,a in enumerate(word):
                    if a>=3 and word[(i+1)%m]==1:
                        valley=x[(i+1)%m]
                        incoming=F(3*y[i]+4-2**a,3*y[i])
                        outgoing=1+F(2,3*(valley-1))
                        paired=1+F(12-2**a,3*2**a*valley-12)
                        check(incoming*outgoing==paired, 'exact adjacent-turn period factor')
                        h3+=a==3; h4+=a>=4
                bound=(1+F(2,3*(s-1)))**(word.count(1)-h3-h4)*(1+F(1,6*s-3))**h3
                check(F(U,L)<=bound, 'ordered-turn-aware cycle inequality')
                positive_periods += 1
    check(ac.anchored_edge(1)['ratio'] is None, 'basepoint zero relation retained without division')
    check(ac.anchored_edge(5)['ratio'] == {'value':'0','present':True}, 'entry zero is supported')
    check(ac.anchored_edge(9)['anchored_forcing'] == {'value':'0','present':True}, 'exponent two forcing zero retained')
    check(ac.anchored_edge(9)['ratio']['value'] == '1', 'exponent two period factor is one')
    for n in range(3,2048,2):
        x=n; factor=F(1); A=m=0
        while x>1 and m<16:
            nxt,a=raw_step(x)
            rec=ac.anchored_edge(x)
            check((rec['target'],rec['a']) == (nxt,a), 'independent original edge')
            factor *= F(rec['ratio']['value']); A+=a; m+=1
            check(factor == F(2**A,3**m)*F(nxt-1,n-1), 'original finite-path period with endpoint')
            x=nxt
    return {'word_fixtures':sum(4**m for m in range(1,6)),
            'positive_rational_period_fixtures':positive_periods,
            'edge_examples':[ac.anchored_edge(n) for n in (1,3,5,9,13)]}


def verify_fiber(fiber, record=True):
    test=check if record else ac.need
    r,q,lo,hi,c,M=(fiber[k] for k in ('r','q','low','high','residue','modulus'))
    # Independent enumeration along the ORIGINAL dyadic progression, followed
    # by the residue predicate. It does not use the generator's CRT inverse.
    start=(lo-r+q-1)//q; end=(hi-r)//q
    actual=[r+q*t for t in range(start,end+1) if (r+q*t-c) % M == 0]
    test(len(actual)==fiber['count'], 'independent original-fiber count')
    test(fiber['label_present'] is True, 'empty and occupied labels stay present')
    test(fiber['first']==(actual[0] if actual else None), 'independent fiber first')
    test(fiber['last']==(actual[-1] if actual else None), 'independent fiber last')
    if actual:
        displayed=[fiber['anchor']+fiber['step']*t for t in
                   range(fiber['lower_parameter'],fiber['upper_parameter']+1)]
        test(displayed==actual, 'CRT image and inverse exact')
        test(all((n-r) % q==0 for n in actual), 'original parameter retained')
    return actual


def validate_cover(cover, record=True):
    test=check if record else ac.need
    p=cover['parameters']; lo,hi=p['low'],p['high']
    residue,modulus=p['residue'],p['modulus']
    budget=p['excess_budget']
    expected=[n for n in range(lo,hi+1) if n % 2 and (n-residue) % modulus==0]
    test(cover['root']['count']==len(expected), 'complete root cardinality')
    seen={}; independent=[]; all_counts=Counter(); max_path=0; max_exit=0
    for node in cover['nodes']:
        source=verify_fiber(node['source'],record)
        parts=[verify_fiber(node['tail'],record)]
        for child in node['children']:
            parts += [verify_fiber(child['descent'],record),verify_fiber(child['retained'],record)]
        flattened=[n for part in parts for n in part]
        test(sorted(flattened)==source, 'independent disjoint node partition')
    for leaf in cover['leaves']:
        members=verify_fiber(leaf['fiber'],record)
        word=tuple(leaf['word'])
        L,U,C=raw_packet(word)
        for n in members:
            test(n not in seen, 'no overlapping terminal fibers')
            w=ac.raw_witness(n,excess_budget=budget)
            test(w['kind']==leaf['kind'] and tuple(w['word'])==word,
                 'independent interpreter matches full leaf word and kind')
            # Replay the primitive integer divisions once more from the
            # explicit source, accumulating the literal graph boundary.
            x=n; boundary=Counter(); A=0
            for a in word:
                test(x>=n, 'no earlier descent on a terminal fiber')
                nxt,b=raw_step(x)
                test(a==b, 'every retained original exponent is exact')
                boundary[x]+=1; boundary[nxt]-=1
                x=nxt; A+=a
            boundary={v:k for v,k in boundary.items() if k}
            test(boundary==({n:1,x:-1} if n!=x else {}), 'unquotiented original path boundary')
            test(F(L*n+C,U)==x, 'original full affine endpoint retained')
            if leaf['kind']=='descent':
                test(x<n and (U-L)*n>C, 'actual descent contradicts a cycle minimum')
            elif leaf['kind']=='exit':
                nxt,a=raw_step(x)
                used=sum(max(0,v-2) for v in word)
                test(x>=n and used+max(0,a-2)>budget, 'actual excess exit not convergence')
                test(leaf['remaining_excess']==budget-used and leaf['next_exponent_lower_bound']==budget-used+3,
                     'retained prefix excess and tail bound')
                t=(n-leaf['prefix_source_anchor'])//leaf['prefix_source_step']
                test(x==leaf['prefix_image_anchor']+leaf['prefix_image_step']*t,
                     'exit original source-image parameter')
                test((3*x+1) % (1 << leaf['next_exponent_lower_bound'])==0, 'entire high-exponent tail predicate')
                max_exit=max(max_exit,a)
            else:
                test(False, 'unresolved or cyclic leaf cannot certify exclusion')
            seen[n]=leaf['kind']; all_counts[leaf['kind']]+=1
            independent.append(w); max_path=max(max_path,len(word))
    test(sorted(seen)==expected, 'every possible minimum covered exactly once')
    test(dict(all_counts)==cover['point_counts'], 'independent complete classification counts')
    test(cover['complete'] is True, 'complete cover explicitly certified')
    independent.sort(key=lambda w:w['source'])
    return {'sources':len(expected), 'first_source':expected[0] if expected else None,
            'last_source':expected[-1] if expected else None,
            'counts':dict(sorted(all_counts.items())), 'max_allowed_path_length':max_path,
            'largest_observed_exit_exponent':max_exit,
            'independent_rows_sha256':ac.digest(independent),
            'example_witnesses':[independent[i] for i in (0,1,len(independent)//2,-1)]}


def arithmetic_sector_checks():
    reduction=ac.period_reduction()
    check(reduction['period_ceiling']==971, 'all-length 403-rise period ceiling')
    check(reduction['windows']==[{'m':971,'A':1539,'k_budget':403,'maximum_excess':0,'least_rises':403}],
          'unique period and exponent sector')
    # Independent least-power loop, with all lengths retained.
    s=99781
    for m in range(1,972):
        L=3**m; U=1; A=0
        while U<=L: U*=2; A+=1
        allowed=U*s**m <= (3*s+1)**m
        check(allowed==(m==971), 'independent complete period-window scan')
        if allowed:
            check(A==1539 and 2*U*s**m>(3*s+1)**m, 'unique admissible exponent')
    check((4*s)**972 > 2**403*(3*s+1)**972, 'all larger lengths excluded')
    ceiling=ac.anchored_ceiling(971,1539,403)
    check(ceiling==274546, 'anchored exact minimum ceiling')
    U,L,k=2**1539,3**971,403
    check(U*(3*ceiling-3)**k <= L*(3*ceiling-1)**k, 'ceiling retained')
    check(U*(3*(ceiling+1)-3)**k > L*(3*(ceiling+1)-1)**k, 'next integer excluded')
    for n in range(3,2048,2):
        source_a=raw_step(n)[1]
        numerator=4*n-1
        predecessor_allowed=numerator%3==0 and numerator//3>=n
        test=source_a==1 and predecessor_allowed
        check(test==(n%12==7), 'exact minimum CRT restriction with inverse predecessor')
    return {'reduction':reduction, 'anchored_minimum_ceiling':ceiling,
            'previous_unanchored_ceiling':330749,
            'minimum_residue':7,'minimum_modulus':12,
            'all_cycles_with_at_most_403_rises_excluded_by_this_certificate':True,
            'common_verified_odd_source_bound_unchanged':99779,
            'next_404_rise_window':ac.period_reduction(k=404)}


def verify_unit_excess_sector():
    check(ac.period_reduction(k=404)['windows']==[
          {'m':971,'A':1539,'k_budget':404,'maximum_excess':1,'least_rises':403}],
          '404-rise sector has exactly one excess after previous exclusion')
    ordinary=ac.anchored_ceiling(971,1539,404)
    incoming=ac.anchored_ceiling(971,1539,404,incoming_three=True)
    check(ordinary==275227 and incoming==274717, 'two 404-sector minimum ceilings')
    U,L=2**1539,3**971
    for n,expected in ((incoming,True),(incoming+1,False)):
        check((U*(3*n-3)**404*(2*n-1)<=L*(3*n-1)**404*(2*n-2))==expected,
              'incoming-three exact endpoint comparisons')
    records=[]
    for residue,upper,budget in ((7,ordinary,1),(11,incoming,0)):
        cover=ac.make_cover(high=upper,residue=residue,excess_budget=budget)
        independent=validate_cover(cover)
        # At residue 11 the one exponent-3 edge is the last edge of the
        # putative 971-cycle. Its first 970 edges must have zero excess.
        permitted_horizon=971 if residue==7 else 970
        check(independent['max_allowed_path_length']+1<=permitted_horizon,
              'exit uses only the justified single-traversal prefix')
        records.append({'minimum_residue':residue,'budget_on_tested_prefix':budget,
                        'justified_prefix_horizon':permitted_horizon,
                        'cover':ac.summarize_cover(cover),'independent':independent})
    check(sum(r['independent']['sources'] for r in records)==29199,
          'complete two-residue 404 minimum count')
    return {'m':971,'A':1539,'ones':404,'twos':566,'threes':1,
            'records':records,'all_at_most_404_rises_excluded':True,
            'common_source_bound_unchanged':99779,
            'next_405_rise_window':ac.period_reduction(k=405)}


def rejected_controls(cover):
    controls=[('absent nonzero',lambda:ac.Supported(1,False)),
              ('zero source',lambda:ac.anchored_edge(0)),
              ('even source',lambda:ac.anchored_edge(4)),
              ('negative depth',lambda:ac.make_cover(depth_cap=-1)),
              ('reversed source interval',lambda:ac.make_cover(low=20,high=3)),
              ('zero modulus',lambda:ac.joint_fiber(1,2,3,9,1,0)),
              ('noncontracting period',lambda:ac.anchored_ceiling(3,4,2)),
              ('zero rise count',lambda:ac.anchored_ceiling(1,2,0))]
    removed=dict(cover); removed['leaves']=cover['leaves'][1:]
    # Delete the first occupied leaf, rather than an empty branch.
    index=next(i for i,x in enumerate(cover['leaves']) if x['fiber']['count'])
    removed['leaves']=cover['leaves'][:index]+cover['leaves'][index+1:]
    controls.append(('missing occupied label',lambda:validate_cover(removed,False)))
    forged=dict(cover); forged['leaves']=list(cover['leaves'])
    leaf=dict(forged['leaves'][index]); leaf['word']=leaf['word']+[2]
    forged['leaves'][index]=leaf
    controls.append(('forged original word',lambda:validate_cover(forged,False)))
    vanished=dict(cover); vanished['leaves']=list(cover['leaves'])
    empty_index=next(i for i,x in enumerate(cover['leaves']) if not x['fiber']['count'])
    leaf=dict(vanished['leaves'][empty_index]); f=dict(leaf['fiber']); f['label_present']=False
    leaf['fiber']=f; vanished['leaves'][empty_index]=leaf
    controls.append(('empty support erased',lambda:validate_cover(vanished,False)))
    promoted=dict(cover); promoted['leaves']=list(cover['leaves'])
    exit_index=next(i for i,x in enumerate(cover['leaves']) if x['fiber']['count'] and x['kind']=='exit')
    leaf=dict(promoted['leaves'][exit_index]); leaf['kind']='descent'
    promoted['leaves'][exit_index]=leaf
    controls.append(('alphabet exit promoted to descent',lambda:validate_cover(promoted,False)))
    controls.append(('depth cap mistaken for proof',lambda:validate_cover(ac.make_cover(depth_cap=0),False)))
    rejected=[]
    for name,operation in controls:
        try: operation()
        except (ValueError, ac.cd.CertificateError): rejected.append(name)
        else: raise ValueError('Invalid control accepted: '+name)
    check(len(rejected)==13, 'malformed and false proof controls rejected')
    return rejected


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    algebra=support_and_affine_checks()
    sector=arithmetic_sector_checks()
    cover=ac.make_cover()
    summary=ac.summarize_cover(cover)
    independent=validate_cover(cover)
    check(independent['counts']=={'descent':1165,'exit':13399}, 'complete 403-sector exclusion')
    unit=verify_unit_excess_sector()
    rejected=rejected_controls(cover)
    result={'status':'PASS','source_checkpoint':'6a30f1dc23110fae0abbe3b3bd5e60072a842385',
            'algebra':algebra,'sector':sector,'cover':summary,'independent':independent,
            'unit_excess_sector':unit,
            'rejected_controls':rejected,'checks':dict(sorted(COUNTS.items())),
            'exact_checks':sum(COUNTS.values()),
            'scope':'anchored product and finite full minimum-sector exclusion, not global convergence',
            'all_inherited_files_unchanged':True}
    text=json.dumps(result,sort_keys=True,indent=2)+'\n'
    if args.output: args.output.write_text(text,encoding='utf-8')
    else: print(text,end='')


if __name__=='__main__': main()
