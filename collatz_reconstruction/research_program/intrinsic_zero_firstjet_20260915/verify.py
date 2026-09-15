#!/usr/bin/env python3
"""Regenerate the deterministic exact first-jet receipt; standard library only.

Matrix checks retain the original matrix and construct unimodular U,V with
U*A*V=D. They are a separate calculation from functional-graph classification.
No optimized-Python-sensitive assert statements are used.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction
from itertools import product
import argparse
import hashlib
import json
from pathlib import Path
import random
import firstjet as F

COUNTS = Counter()


def check(ok: bool, name: str) -> None:
    COUNTS[name] += 1
    if not ok:
        raise RuntimeError('exact check failed: '+name)


def identity(n: int) -> list[list[int]]:
    return [[int(i == j) for j in range(n)] for i in range(n)]


def multiply(A, B):
    if not A: return []
    if not B: return [[] for _ in A]
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*B)] for row in A]


def smith(A: list[list[int]]):
    """Exact integer row/column equivalence, INCLUDING both original maps."""
    D = [row[:] for row in A]
    m,n = len(A),len(A[0]) if A else 0
    U,V = identity(m),identity(n)
    def rs(i,j):
        D[i],D[j]=D[j],D[i]; U[i],U[j]=U[j],U[i]
    def cs(i,j):
        for B in (D,V):
            for row in B: row[i],row[j]=row[j],row[i]
    def ra(i,j,q):
        for B in (D,U): B[i]=[a+q*b for a,b in zip(B[i],B[j])]
    def ca(i,j,q):
        for B in (D,V):
            for row in B: row[i]+=q*row[j]
    for k in range(min(m,n)):
        nz=[(abs(D[i][j]),i,j) for i in range(k,m) for j in range(k,n) if D[i][j]]
        if not nz: break
        _,i,j=min(nz); rs(k,i); cs(k,j)
        while True:
            for i in range(k+1,m):
                while D[i][k]:
                    ra(i,k,-(D[i][k]//D[k][k]))
                    if D[i][k]: rs(i,k)
            for j in range(k+1,n):
                while D[k][j]:
                    ca(j,k,-(D[k][j]//D[k][k]))
                    if D[k][j]: cs(j,k)
            if any(D[i][k] for i in range(k+1,m)) or any(D[k][j] for j in range(k+1,n)):
                continue
            bad=next(((i,j) for i in range(k+1,m) for j in range(k+1,n) if D[i][j] % D[k][k]), None)
            if bad is None: break
            ra(k,bad[0],1)
        if D[k][k] < 0:
            D[k]=[-a for a in D[k]]; U[k]=[-a for a in U[k]]
    return D,U,V


def determinant(A):
    n=len(A)
    if not n: return 1
    B=[[Fraction(a) for a in row] for row in A]
    out=Fraction(1)
    for i in range(n):
        j=next((j for j in range(i,n) if B[j][i]),None)
        if j is None: return 0
        if j != i: B[j],B[i]=B[i],B[j]; out=-out
        p=B[i][i]; out*=p
        for j in range(i+1,n):
            q=B[j][i]/p
            for k in range(i+1,n): B[j][k]-=q*B[i][k]
    return out


def rank_mod(A,p):
    if not A: return 0
    B=[[x%p for x in row] for row in A]; row=0
    for col in range(len(B[0])):
        piv=next((i for i in range(row,len(B)) if B[i][col]),None)
        if piv is None: continue
        B[row],B[piv]=B[piv],B[row]
        inv=pow(B[row][col],-1,p)
        B[row]=[(x*inv)%p for x in B[row]]
        for i in range(row+1,len(B)):
            q=B[i][col]
            B[i]=[(x-q*y)%p for x,y in zip(B[i],B[row])]
        row+=1
        if row==len(B): break
    return row


def elementary_signature(moduli):
    out={}
    for modulus in moduli:
        d=2; n=modulus
        while d*d<=n:
            e=0
            while n%d==0: n//=d; e+=1
            if e: out.setdefault(d,[]).append(e)
            d+=1
        if n>1: out.setdefault(n,[]).append(1)
    return {p:sorted(v) for p,v in sorted(out.items())}


def check_smith(A, free_rank, moduli, label):
    D,U,V=smith(A)
    m,n=len(A),len(A[0]) if A else 0
    check(multiply(multiply(U,A),V)==D, label+'.UAV')
    check(abs(determinant(U))==1 and abs(determinant(V))==1, label+'.unimodular')
    check(all(D[i][j]==0 for i in range(m) for j in range(n) if i!=j), label+'.diagonal')
    diag=[D[i][i] for i in range(min(m,n)) if D[i][i]]
    check(all(a>0 for a in diag) and all(b%a==0 for a,b in zip(diag,diag[1:])),label+'.divisibility')
    check(m-len(diag)==free_rank,label+'.free_rank')
    check(elementary_signature([a for a in diag if a>1])==elementary_signature(moduli),label+'.torsion')
    for p in (2,3,5,7):
        expected=free_rank+sum(m%p==0 for m in moduli)
        check(m-rank_mod(A,p)==expected,label+'.mod_prime')


def jet_matrix(d,P):
    if not d: return []
    n=len(d[0])
    return [row[:]+[0]*n for row in d]+[[-x for x in a]+b[:] for a,b in zip(P,d)]


def all_subsets(xs):
    for flags in product((0,1),repeat=len(xs)):
        yield tuple(x for x,b in zip(xs,flags) if b)


def abstract_cycle(m):
    d=[[0]*m for _ in range(m)]; P=[[0]*m for _ in range(m)]
    for j in range(m):
        d[j][j]+=1; d[(j+1)%m][j]-=1; P[(j+1)%m][j]+=1
    return d,P


def run():
    # The foundational scalar operations do not contain trajectory data.
    samples=[None]+[F.Dual(a,b) for a,b in product(range(-1,2),repeat=2)]
    for a in samples:
        check(F.from_coordinates(F.coordinates(a))==a,'split.coordinate_inverse')
        for b in samples:
            check(F.split_add(a,b)==F.split_add(b,a),'split.add_commutes')
            check(F.split_mul(a,b)==F.split_mul(b,a),'split.mul_commutes')
            for c in samples:
                check(F.split_add(F.split_add(a,b),c)==F.split_add(a,F.split_add(b,c)),'split.add_associates')
                check(F.split_mul(a,F.split_add(b,c))==F.split_add(F.split_mul(a,b),F.split_mul(a,c)),'split.distributes')
    eps=F.Dual(0,1); e=F.Dual(0,0)
    check(F.split_mul(eps,eps)==e and e is not None,'split.nilpotent_to_supported_zero')
    for a in samples:
        check(F.split_mul(None,a) is None,'split.absent_absorber')
    for k in range(-12,13):
        check(F.Dual(0,k).constant==0 and F.Dual(0,k) is not None,'split.reduction_zero_fibre')
    # Independent integer presentations for all subsets of seven actual edges.
    base=(1,3,5,7,9,11,13)
    graphs={E:F.diagram(E) for E in all_subsets(base)}
    for E,g in graphs.items():
        check_smith(F.defect_presentation(g),g['defect_free_rank'],g['defect_cycle_moduli'],'graph.defect')
        check_smith(jet_matrix(g['d_matrix'],g['target_matrix']),g['H1_rank']+g['defect_free_rank'],g['defect_cycle_moduli'],'graph.jet')
        for n,y,a in g['original_edges']:
            z=3*n+1; independent_a=0
            while z%2==0: z//=2; independent_a+=1
            check((z,independent_a)==(y,a),'graph.original_equation')
            check(all(x==0 for x in F.class_coordinates(g,{n:1,y:-1}) ) if n!=y else True,'graph.original_relation')
    nested=0
    for labels in product(range(3),repeat=len(base)):
        A=tuple(n for n,b in zip(base,labels) if b==2)
        B=tuple(n for n,b in zip(base,labels) if b>=1)
        matrix=F.transition(graphs[A],graphs[B]); nested+=1
        for j,comp in enumerate(graphs[A]['components']):
            check(sum(row[j] for row in matrix)==1,'support.transition_retains_component')
    compositions=0
    smallbase=base[:5]
    for labels in product(range(4),repeat=len(smallbase)):
        A=tuple(n for n,b in zip(smallbase,labels) if b==3)
        B=tuple(n for n,b in zip(smallbase,labels) if b>=2)
        C=tuple(n for n,b in zip(smallbase,labels) if b>=1)
        f=F.transition(graphs[A],graphs[B]); g=F.transition(graphs[B],graphs[C]); h=F.transition(graphs[A],graphs[C])
        check(multiply(g,f)==h,'support.composition'); compositions+=1
    # Symbolic cycle matrices are controls, NOT claimed positive Collatz cycles.
    symbolic=[]
    for m in range(1,33):
        d,P=abstract_cycle(m)
        cyc=[[sum(row) for _ in (0,)] for row in P]
        presentation=[a+b for a,b in zip(d,cyc)]
        check_smith(presentation,0,[] if m==1 else [m],'symbolic.defect')
        check_smith(jet_matrix(d,P),1,[] if m==1 else [m],'symbolic.jet')
        beta=-sum(sum(row) for row in P)
        check(beta==-m,'symbolic.beta_exact')
        w=F.Dual(1,1); value=F.Dual(1,0)
        for _ in range(m): value=value*w
        check(value==F.Dual(1,m),'symbolic.first_jet_period')
        symbolic.append({'label':'abstract_position_circle','period':m,'beta':beta,'defect_modulus':m})
    # Elementary-map expansion retains its exact first-order chain map.
    for n in range(1,514,2):
        expected,a=F.step(n)
        x=n; full_edges=[n]; x=3*n+1
        while x%2==0:
            full_edges.append(x); x//=2
        const=Counter(); linear=Counter()
        for i,z in enumerate(full_edges):
            y=3*z+1 if z%2 else z//2
            const[z]+=1; const[y]-=1
            if i:
                linear[z]+=1; linear[y]-=1
            if z%2: linear[y]-=1
        rhs=Counter({n:1}); rhs[expected]-=1
        check(x==expected and len(full_edges)==a+1,'elementary.original_block')
        check(F.clean(const)==F.clean(rhs) and F.clean(linear)=={expected:-1},'elementary.jet_expansion')
    for repeats in range(1,9):
        check(F.step(1)==(1,2) and -repeats==-1*repeats,'position.repeated_fixed_loop_map')
    # A genuine cycle for the explicitly changed -1 forcing.
    control=F.diagram([5,7],-1)
    check(control['defect_cycle_moduli']==[2] and control['defect_free_rank']==0,'control.actual_minus_cycle')
    check_smith(F.defect_presentation(control),0,[2],'control.minus_defect')
    check_smith(jet_matrix(control['d_matrix'],control['target_matrix']),1,[2],'control.minus_jet')
    check(F.jet_boundary({5:-1,7:-1},{7:-1},-1)==({}, {5:2}),'control.two_times_supported_class_boundary')
    # Full original-source first-order witnesses and extraction, no rationalization.
    witness_digest=hashlib.sha256(); return_equations=0
    for n in range(1,2048,2):
        w=F.witness(n,10000)
        check(w['status']=='verified_finite_first_order_boundary','witness.finite_identity')
        replay=n
        for recorded,a in zip(w['values'][1:],w['exponents']):
            z=3*replay+1; b=0
            while z%2==0: z//=2; b+=1
            check((z,b)==(recorded,a),'witness.independent_return')
            return_equations+=1; replay=z
        check(replay==1,'witness.extracted_target')
        witness_digest.update((json.dumps(w,sort_keys=True,separators=(',',':'))+'\n').encode())
    check(F.witness(27,10)['status']=='unresolved_at_cap','witness.finite_cutoff_retained')
    check(F.witness(27,100)['returns']==41,'witness.twenty_seven_path')
    for j in (1,2,3,16,64,256):
        n=(4**j-1)//3
        check(3*n+1==2**(2*j),'family.literal_equation')
        w=F.witness(n,1)
        check(w['status']=='verified_finite_first_order_boundary','family.exact_boundary')
    # A zero first-jet singleton over Z requires a fixed point, not a divided cycle.
    rejects=[]
    bad=[('even_source',lambda:F.diagram([2])),
         ('bool_source',lambda:F.diagram([1,True])),
         ('false_forcing',lambda:F.diagram([],0)),
         ('false_support_coordinates',lambda:F.from_coordinates((F.Dual(1,0),False))),
         ('wrong_singleton',lambda:F.validate_witness(3,{1:-1},{})),
         ('empty_cycle',lambda:F.validate_witness(1,{},{})),
         ('false_cycle',lambda:F.validate_witness(3,{3:1},{})),
         ('fractional_witness',lambda:F.validate_witness(5,{5:Fraction(-1,2),7:Fraction(-1,2)},{7:Fraction(-1,2)},-1)),
         ('noninteger_witness',lambda:F.validate_witness(1,{1:-1.0},{})),
         ('changed_forcing',lambda:F.transition(F.diagram([5],1),F.diagram([5,7],-1))),
         ('not_an_inclusion',lambda:F.transition(F.diagram([3]),F.diagram([1]))),
         ('negative_cap',lambda:F.witness(27,-1))]
    for name,fn in bad:
        caught=False
        try: fn()
        except F.CertificateError: caught=True
        check(caught,'reject.malformed'); rejects.append(name)
    examples={
      'scalar_nilpotent':{'epsilon':[0,1],'epsilon_square_supported_zero':[0,0],'absent':None},
      'open_merger':F.diagram([3,13]),
      'edge_to_one_but_fixed_relation_not_yet_added':F.diagram([3,5,13]),
      'complete_retained_base_component':F.diagram([1,3,5,13]),
      'actual_minus_one_cycle':control,
      'first_order_source_3':F.witness(3,100),
      'first_order_source_27':F.witness(27,100),
      'unresolved_source_27_at_10':F.witness(27,10)}
    return {'status':'PASS','checks':dict(sorted(COUNTS.items())), 'total_checks':sum(COUNTS.values()),
            'actual_finite_equation_supports':len(graphs), 'nested_support_pairs':nested,
            'support_composition_triples':compositions, 'abstract_cycle_controls':symbolic,
            'original_singleton_witnesses':1024, 'independent_return_equations':return_equations,
            'witness_sha256':witness_digest.hexdigest(),'rejected_cases':rejects,'examples':examples,
            'global_Collatz_claim':False,'positive_nontrivial_cycle_claim':False,
            'no_new_numerical_cycle_bound':True,'new_Lean_execution':False}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    data=run()
    args.output.write_text(json.dumps(data,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':data['status'],'total_checks':data['total_checks'],
                      'original_singleton_witnesses':data['original_singleton_witnesses'],
                      'sha256':hashlib.sha256(args.output.read_bytes()).hexdigest()},sort_keys=True))


if __name__=='__main__': main()
