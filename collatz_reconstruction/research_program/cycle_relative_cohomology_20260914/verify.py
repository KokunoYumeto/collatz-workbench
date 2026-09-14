#!/usr/bin/env python3
"""Independent exact-matrix, graph, return-chart and predecessor-bridge replay."""
from __future__ import annotations
import argparse
from collections import Counter
from copy import deepcopy
from fractions import Fraction as F
import hashlib
import importlib.util
from itertools import product
import json
from math import gcd
from pathlib import Path
import sys

import cycle_detector as cd

COUNTS: Counter[str] = Counter()


def check(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)
    COUNTS[label] += 1


def mm(A,B):
    return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]


def eye(n):
    return [[F(int(i==j)) for j in range(n)] for i in range(n)]


def inv_det(A):
    n = len(A)
    R = [[F(x) for x in row]+eye(n)[i] for i,row in enumerate(A)]
    determinant = F(1)
    for j in range(n):
        k = next((k for k in range(j,n) if R[k][j]),None)
        check(k is not None,'nonzero rational pivot')
        if k != j:
            R[j],R[k]=R[k],R[j]
            determinant = -determinant
        p = R[j][j]
        determinant *= p
        R[j]=[v/p for v in R[j]]
        for i in range(n):
            if i != j:
                p = R[i][j]
                R[i]=[a-p*b for a,b in zip(R[i],R[j])]
    return [row[n:] for row in R],determinant


def rank(A):
    if not A or not A[0]: return 0
    R = [[F(v) for v in row] for row in A]
    i = 0
    for j in range(len(R[0])):
        k = next((k for k in range(i,len(R)) if R[k][j]),None)
        if k is None: continue
        R[i],R[k] = R[k],R[i]
        p=R[i][j]; R[i]=[v/p for v in R[i]]
        for k in range(len(R)):
            if k!=i:
                p=R[k][j]; R[k]=[a-p*b for a,b in zip(R[k],R[i])]
        i+=1
        if i==len(R): break
    return i


def egcd(a,b):
    oa,ob,x0,x1,y0,y1=a,b,1,0,0,1
    while b:
        q,a,b=a//b,b,a%b
        x0,x1=x1,x0-q*x1
        y0,y1=y1,y0-q*y1
    check(oa*x0+ob*y0==a,'Bezout identity')
    return a,x0,y0


def matrix_tests():
    fixtures = [w for m in range(1,5) for w in product(range(1,5),repeat=m)]
    fixtures += [(1,1,2,4,3),(1,1,3,2),(2,)*7,(1,2)*3]
    for w in fixtures:
        cert=cd.cycle_certificate(w)
        p=cd.packet(w); B=cd.cyclic_matrix(w); m=len(w)
        inverse,det=inv_det(B); I=eye(m); Fp=cd.functional(w)
        check(det==(-1)**(m-1)*p.D,'independent determinant')
        check(mm([list(Fp)],B)==[[p.D]+[0]*(m-1)],'original telescoping row')
        x=mm(inverse,[[1] for _ in w])
        check([str(row[0]) for row in x]==cert['rational_orbit'],'independent rational solve')
        if m==1: u=[1]
        else:
            g,a,b=egcd(Fp[0],Fp[-1]); check(g==1,'functional primitive')
            u=[a]+[0]*(m-2)+[b]
        s0=mm(inverse,[[p.D*t] for t in u])
        H=mm(inverse,[[I[i][j]-u[i]*Fp[j] for j in range(m)] for i in range(m)])
        check(all(v.denominator==1 for row in H+s0 for v in row),'integral chain comparison')
        check(sum(a*b for a,b in zip(Fp,u))==1 and s0[0][0]==1,'chain section retraction')
        check(mm(B,H)==[[I[i][j]-u[i]*Fp[j] for j in range(m)] for i in range(m)],
              'degree one chain homotopy')
        check(mm(H,B)==[[I[i][j]-s0[i][0]*int(j==0) for j in range(m)] for i in range(m)],
              'degree zero chain homotopy')
        # Compare weighted closure to ordinary circle incidence on the same vertices.
        R=[[F(int(j==(i+1)%m)) for j in range(m)] for i in range(m)]
        diagonal=[[x[i][0] if i==j else F(0) for j in range(m)] for i in range(m)]
        rhs=[[I[i][j]+(3*x[i][0]+1)*(R[i][j]-I[i][j]) for j in range(m)] for i in range(m)]
        check(mm(B,diagonal)==rhs,'weighted to ordinary cycle operator identity')
        anchored=mm(B,[[row[0]-1] for row in x])
        check([z[0] for z in anchored]==cert['anchored_forcing'],'anchored affine primitive')
        for v in (-2,0,1,3):
            n=cert['cylinder_source_anchor']+2*p.U*v
            y=cert['image_anchor']+2*p.L*v
            check(p.evaluate(n)==y,'original cylinder chart')
            check((n-y)//2==p.D*v-cert['return_mark'],'literal return displacement')
        # Span P -> image and return; Fpar = L*s-U*t is a primitive cokernel map.
        g,a,b=egcd(p.L,p.U)
        check(g==1,'parallel lattice primitive')
        s,t=a,-b
        check(p.L*s-p.U*t==1,'parallel cokernel section')
        check((p.L*(s-t)-1) % abs(p.D)==0,'parallel to return cohomology map')
        check((-p.U*t-1) % p.L==0,'parallel to image cohomology map')
        # Source-enriched incidence columns retain both endpoints.
        z0=(cert['cylinder_source_anchor']-1)//2
        z1=(cert['image_anchor']-1)//2
        for v in range(4):
            column=(1,z0+p.U*v,z1+p.L*v)
            check((column[1]-z0*column[0],column[2]-z1*column[0])==(p.U*v,p.L*v),
                  'joint incidence to parallel chain map')
        for r in (2,3,4):
            repeated=cd.packet(w*r)
            S=sum(p.U**(r-1-j)*p.L**j for j in range(r))
            check(repeated.D==S*p.D and repeated.C==S*p.C,'retained repetition map')
            check(F(repeated.C,repeated.D)==F(p.C,p.D),'same rational cycle under repetition')
    return len(fixtures)


def modular_tests():
    fixtures=0
    for m in (1,2,3):
        for w in product((1,2,3),repeat=m):
            B=cd.cyclic_matrix(w)
            for N in (2,3,4,5,7,9):
                for c in (1,-1):
                    observed=sum(all((sum(a*b for a,b in zip(row,x))-c)%N==0 for row in B)
                                 for x in product(range(N),repeat=m))
                    check(observed==cd.modular_solution_count(w,N,c),'exhaustive modular solution count')
                    fixtures+=1
    w=(1,1,2,4,3); B=cd.cyclic_matrix(w); x=(0,10,6,0,6)
    residual=[(sum(a*b for a,b in zip(row,x))-1)//19 for row in B]
    check(residual==[1,-1,-1,5,-1],'prime-power lifting residual')
    check(sum(a*b for a,b in zip(cd.functional(w),residual))==-25,'lifting obstruction pairing')
    check(cd.modular_solution_count(w,19)==19 and cd.modular_solution_count(w,361)==0,
          'prime versus prime-power obstruction')
    return fixtures


def graph_tests():
    out=[]
    fixtures=[(3,),(3,5),(5,7),(3,5,7,9),tuple(range(3,32,2)),tuple(range(3,64,2))]
    for c in (1,-1):
        for sources in fixtures:
            rec=cd.finite_graph_certificate(sources,c)
            vs=[v for v in rec['vertices'] if v!=1]
            B=[[int(v==n)-int(v==y) for n,y in rec['edges']] for v in vs]
            rk=rank(B)
            check(len(vs)-rk==rec['relative_H0_rank'],'independent graph H0 rank')
            check(len(sources)-rk==rec['relative_H1_rank'],'independent graph H1 rank')
            for comp in rec['cycle_components']:
                chain={int(k):v for k,v in comp['cycle_chain'].items()}
                check(cd.sparse_boundary(chain,c)=={},'actual relative cycle closed')
                check(chain[comp['detecting_cochain_edge']]==1,'actual cycle period pairing')
            out.append({'forcing_c':c,'source_count':len(sources),
                        'H0_rank':rec['relative_H0_rank'],'H1_rank':rec['relative_H1_rank'],
                        'frontier':rec['frontier']})
    check(cd.finite_graph_certificate((3,))['relative_H0_rank']==1,'retain unresolved frontier')
    check(cd.finite_graph_certificate((3,5))['relative_H0_rank']==0,'frontier killed by actual edge')
    control=cd.finite_graph_certificate((5,7),-1)
    check(control['relative_H1_rank']==1 and control['cycle_components'][0]['cycle_vertices']==[5,7],
          'positive control cycle detected')
    # Exact sign conjugacy, with the valuation retained on the original signed source.
    for n in range(1,256,2):
        y,a=cd.step(n,-1)
        signed=3*(-n)+1
        check(cd.v2(signed)==a and signed//(1<<a)==-y,'signed control conjugacy')
    return out,control


def predecessor_bridge():
    source=Path(__file__).resolve().parent.parent/'stopped_affine_transport_20260914'/'verify.py'
    spec=importlib.util.spec_from_file_location('stopped_predecessor',source)
    old=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=old
    spec.loader.exec_module(old)
    words=[(1,1,3,2),(3,),(1,2,2),(2,),(1,4)]
    for w in words:
        a=old.packet(w); b=cd.packet(w)
        check((a.A,a.L,a.C)==(b.A,b.L,b.C),'predecessor unchanged coefficient convention')
    fam=old.Family(1,1,1,1024)
    w=(1,1,3,2); ch=old.chart(fam,old.packet(w)); cert=cd.cycle_certificate(w)
    check((ch.u,ch.target_d)==(157,81),'predecessor actual image retained')
    check(cert['image_anchor']==157 and cert['image_step']==162,'cycle to predecessor chart')
    block=cd.path_from_word(247,w)
    check(block['terminal']==157 and block['strict_descent'],'actual block bridge')
    tail=cd.path_certificate(157)
    chain=Counter({int(k):v for k,v in block['relative_chain'].items()})
    chain.update({int(k):v for k,v in tail['chain'].items()})
    check(cd.sparse_boundary(dict(chain))=={247:1},'stopped block plus tail contraction')
    # H ∂ e_n = e_n on a finite forward-closed basin, using actual path chains.
    for n in range(3,257,2):
        y,_=cd.step(n)
        a=cd.path_certificate(n); b=cd.path_certificate(y)
        check(a['status']==b['status']=='reaches_basepoint','finite contraction source covered')
        diff=Counter({int(k):v for k,v in a['chain'].items()})
        diff.subtract({int(k):v for k,v in b['chain'].items()})
        check({k:v for k,v in diff.items() if v}=={n:1},'degree one actual path contraction')
    return {'predecessor_verify_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'block':block,'tail':tail}


def source_tests():
    max_ret,max_seed,peak=0,1,1
    digest=hashlib.sha256()
    for n in range(1,4096,2):
        cert=cd.path_certificate(n)
        check(cert['status']=='reaches_basepoint','finite positive source reaches basepoint')
        cd.validate_path_certificate(cert)
        check(cd.sparse_boundary({int(k):v for k,v in cert['chain'].items()})==({n:1} if n>1 else {}),
              'finite source column boundary')
        if cert['returns_recorded']>max_ret:
            max_ret,max_seed=cert['returns_recorded'],n
        peak=max([peak,cert['terminal']]+cert['values'])
        digest.update(json.dumps(cert,sort_keys=True,separators=(',',':')).encode()+b'\n')
    for n in (1,3,27,247,4095):
        path=cd.path_certificate(n)
        w=tuple(path['exponents'])+(2,)*12
        rec=cd.residue_tower(w)
        for row in rec['rows']:
            check(n % row['modulus']==row['residue'],'actual integer residue tower')
            if row['modulus']>n:
                check(row['residue']==n,'integer tower stabilization')
    for m in range(1,101):
        rec=cd.residue_tower((1,)*m)
        check(rec['rows'][-1]['residue']==(1<<(m+1))-1,'all-one noninteger tower')
        check(cd.residue_tower((2,)*m)['rows'][-1]['residue']==1,'trivial fixed tower')
        cd.one_spike_formula(m)
        check(True,'arbitrary length one-spike identity fixture')
    for n in range(1,1024,2):
        k=cd.v2(n+1); u=(n+1)//(1<<k); x=n
        for j in range(k-1):
            check(x==(3**j)*(1<<(k-j))*u-1,'maximal initial ascent original value')
            x,a=cd.step(x)
            check(a==1,'maximal initial ascent actual exponent')
        r=cd.v2(3**k*u-1)
        y,a=cd.step(x)
        check(a==r+1 and y==(3**k*u-1)//(1<<r),'completed ascent exact exit')
        check((y<n)==(((1<<(k+r))-3**k)*u>(1<<r)-1),'completed ascent affine descent')
    return {'positive_odd_starts_checked':2048,'largest_start':4095,
            'maximum_odd_returns':max_ret,'first_seed_at_maximum':max_seed,
            'maximum_observed_odd_value':peak,'canonical_path_records_sha256':digest.hexdigest()}


def compression_tests():
    # Actual first-descent words; vertices outside the supplied dictionary stay rooted.
    words={}
    for n in range(3,256,2):
        x=n; w=[]
        for _ in range(10000):
            x,a=cd.step(x); w.append(a)
            if x < n: break
        check(x<n,'compression input has actual descent')
        words[n]=tuple(w)
    comp=cd.DescentCompression(words)
    for n in range(3,512,2):
        vertices={n:1}; root,H=comp.resolve(n)
        check(root==1 if n<256 else root==n,'unlisted compression roots retained')
        Q=comp.project_vertices(vertices)
        bH=cd.sparse_boundary(H)
        expected=Counter(vertices); expected.subtract(Q)
        check(bH==cd.clean_counter(expected),'compression degree zero homotopy')
        check(comp.project_vertices(Q)==Q,'compression vertex idempotence')
        check(comp.homotopy(Q)=={},'compression homotopy vanishes on roots')
        edge={n:1}; Fedge=comp.project_edges(edge)
        check(comp.project_edges(Fedge)==Fedge,'compression edge idempotence')
        check(cd.sparse_boundary(Fedge)==comp.project_vertices(cd.sparse_boundary(edge)),
              'compression chain map')
        expected=Counter(edge); expected.subtract(Fedge)
        check(comp.homotopy(cd.sparse_boundary(edge))==cd.clean_counter(expected),
              'compression degree one homotopy')
    control=cd.DescentCompression({7:(2,)},-1)
    check(control.resolve(7)==(5,{7:1}),'control descends to surviving root')
    check(control.project_edges({5:1})=={5:1,7:1},'control edge exposes actual cycle')
    check(control.project_edges({7:1})=={},'control tree direction contracts')
    check(control.project_edges({5:1,7:1})=={5:1,7:1},'nontrivial cycle preserved literally')
    return {'original_descent_words':{str(n):list(w) for n,w in words.items()},
            'root_policy':'Every unlisted vertex remains itself, except basepoint 1 is relative zero.',
            'control_c':-1,'control_words':{'7':[2]},
            'control_vertex_7_root':5,'control_projected_edge_5':{'5':1,'7':1},
            'control_cycle_preserved':True}


def cutoff_compression_tests():
    cutoffs=(0,4,8,12,16,32,64,128)
    systems=[cd.StoppedDescentCompression(H) for H in cutoffs]
    summaries=[]
    for H,system in zip(cutoffs,systems):
        roots=Counter()
        for n in range(1,1024,2):
            cert=system.certificate(n)
            roots[cert['root']]+=1
            root,path=system.resolve(n)
            check(root<=n,'cutoff compression preserves positive order')
            check(system.project_vertices(system.project_vertices({n:1}))==system.project_vertices({n:1}),
                  'whole-source cutoff vertex projection')
            if n>1:
                edge={n:1}; Fedge=system.project_edges(edge)
                check(system.project_edges(Fedge)==Fedge,'whole-source cutoff edge projection')
                check(cd.sparse_boundary(Fedge)==system.project_vertices(cd.sparse_boundary(edge)),
                      'whole-source cutoff chain map')
        all_one=(1<<(H+1))-1
        # At H=0 use source 3; all_one=1 is the basepoint, not an unresolved source.
        witness=all_one if H else 3
        check(system.resolve(witness)==(witness,{}),'positive residual witness at every finite cutoff')
        summaries.append({'H':H,'source_count':512,'absorbed_at_1':roots.get(1,0),
                          'distinct_unresolved_roots':len([v for v in roots if v!=1]),
                          'retained_all_one_witness':witness})
    for small,big in zip(systems,systems[1:]):
        for n in range(1,256,2):
            r1,h1=small.resolve(n); r2,h2=big.resolve(n)
            check(big.resolve(r1)[0]==r2 and small.resolve(r2)[0]==r2,
                  'nested cutoff root maps commute')
            both=Counter(h1); both.update(big.resolve(r1)[1])
            check(cd.clean_counter(both)==h2,'nested cutoff path extension identity')
            if n>1:
                e={n:1}
                check(big.project_edges(small.project_edges(e))==big.project_edges(e),
                      'nested cutoff edge retractions first order')
                check(small.project_edges(big.project_edges(e))==big.project_edges(e),
                      'nested cutoff edge retractions reverse order')
    return {'cutoffs':summaries,
            'source_27_by_cutoff':[system.certificate(27) for system in systems]}


def negative_tests():
    cases=[]
    def reject(name,f):
        try: f()
        except (cd.CertificateError,ValueError,TypeError):
            cases.append(name); check(True,'deliberately corrupted input rejected')
        else: raise RuntimeError('negative control accepted: '+name)
    reject('empty cycle',lambda: cd.cycle_certificate(()))
    reject('zero exponent',lambda: cd.cycle_certificate((0,)))
    reject('even source',lambda: cd.path_certificate(4))
    reject('unlabelled forcing change',lambda: cd.cycle_certificate((2,),3))
    bad=cd.cycle_certificate((1,3)); bad['integral']=True
    reject('rational cycle labelled integral',lambda: cd.validate_cycle_certificate(bad))
    bad2=cd.cycle_certificate((2,2)); bad2['actual_relative_cycle_contribution']=True
    reject('trivial repetition labelled counterexample',lambda: cd.validate_cycle_certificate(bad2))
    bad3=cd.path_certificate(27,2); bad3['status']='reaches_basepoint'
    reject('open boundary labelled convergence',lambda: cd.validate_path_certificate(bad3))
    reject('wrong actual word',lambda: cd.path_from_word(247,(1,2)))
    reject('fixed point called strict descent',lambda: cd.DescentCompression({1:(2,)}))
    reject('increasing block called descent',lambda: cd.DescentCompression({3:(1,)}))
    return cases


def run(A_max=20):
    COUNTS.clear()
    nmat=matrix_tests(); nmod=modular_tests()
    graphs,control=graph_tests(); bridge=predecessor_bridge(); sources=source_tests()
    compression=compression_tests(); cutoff_compression=cutoff_compression_tests(); bad=negative_tests()
    scan=cd.enumerate_words(A_max)
    check(all(row['word']==[2]*len(row['word']) and row['fixed_value']==1
              for row in scan['positive_integral_words']),'bounded word search only trivial cycles')
    examples=[cd.cycle_certificate(w,c) for w,c in
              [((2,),1),((2,2),1),((1,3),1),((1,1,2,4,3),1),((1,2),1),((1,2),-1),
               ((1,1,3,2),1)]]
    return {'status':'PASS','exact_checks':sum(COUNTS.values()),'check_counts':dict(sorted(COUNTS.items())),
            'matrix_fixtures':nmat,'exhaustive_modular_fixtures':nmod,
            'graph_fixtures':graphs,'control_graph':control,'predecessor_bridge':bridge,
            'finite_source_scan':sources,'bounded_word_scan':scan,'cycle_examples':examples,
            'descent_compression':compression,'whole_source_cutoff_compression':cutoff_compression,
            'negative_controls_rejected':bad,'proof_scope':'Finite replay. Infinite claims have separate written proofs.',
            'remote_publication_verified_by_this_checker':False,'checker_does_not_attest_Lean_or_remote_CI':True}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,default=Path('verification.json'))
    ap.add_argument('--sum-bound',type=int,default=20)
    args=ap.parse_args()
    result=run(args.sum_bound)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({'status':'PASS','exact_checks':result['exact_checks'],
                      'words_visited':result['bounded_word_scan']['counts']['words'],
                      'output':str(args.output)},sort_keys=True))


if __name__=='__main__': main()
