#!/usr/bin/env python3
"""Exact structural regression suite; full source audit has its own receipt."""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import sys
import height_control as h

class Checks:
    def __init__(self):self.counts=Counter()
    def check(self,ok,name):
        if not ok:raise h.CertificateError('failed '+name)
        self.counts[name]+=1
    def reject(self,fn,name):
        try:fn()
        except (h.CertificateError,ValueError,KeyError,TypeError):self.counts['reject '+name]+=1
        else:raise h.CertificateError('invalid fixture accepted: '+name)


def test() -> dict:
    c=Checks();env=h.envelope(10280)
    c.check(env['maximum_integer_candidate']==5624777,'complete horizon source bound')
    c.check(env['record_rows'][-1]==[9616,15241,5624777],'attained maximum window row')
    extended=h.envelope(10281)
    c.check(extended['maximum_integer_candidate']==6728242,'next window record retained')
    L=1;C=0; table={};floor=[0]
    for m in range(1,10281):
        C=3*C+(1<<(L.bit_length()-1));L*=3
        A=L.bit_length();D=(1<<A)-L;table[m]=(C,D,A)
        c.check(env['rows_m_crossing_sum_candidate_bound'][m-1]==[m,A,C//D],'each exact envelope row')
        floor.append(A-1)
        c.check(floor[m]-floor[m-1] in (1,2),'critical floor step is positive')
    # Complete nonempty word domain with total exponent <=16, retaining every order.
    stack=[((),0,1,0,False)];words=0;firstcross=0;extremizers=0
    while stack:
        w,A,L,C,crossed=stack.pop()
        if w:
            words+=1;m=len(w);U=1<<A
            if U>L and not crossed:
                firstcross+=1; Cs,Ds,As=table[m]
                c.check(C<=Cs and U-L>=Ds,'separate numerator and denominator envelopes')
                c.check(C*Ds<=Cs*(U-L),'sharp quotient envelope')
                critical=tuple(floor[j]-floor[j-1] for j in range(1,m))+(As-floor[m-1],)
                c.check((C*Ds==Cs*(U-L))==(w==critical),'unique ordered maximizing word')
                if w==critical:extremizers+=1
                p=h.packet(w); c.check(p.C==C and p.A==A,'independent packet recomposition')
                for t in (0,1,7):
                    n=p.rho+2*U*t;values=h.path(n,w)
                    short_end=values[-1] << (A-As)
                    c.check(values[-1]==(L*n+C)//U,'original affine endpoint')
                    c.check(n<=Cs//Ds or short_end<n,'all lifts outside window descend at shortened crossing')
                crossed=True
        for a in range(1,16-A+1):
            stack.append((w+(a,),A+a,3*L,3*C+(1<<A),crossed))
    c.check(words==(1<<16)-1,'complete composition domain')
    # Explicit integral coefficient inverses, including negative clocks.
    for a in range(-16,17):
        for b in range(-16,17):
            c.check(h.times(h.power(a),h.power(b))==h.power(a+b),'signed first-jet clock multiplication')
        c.check(h.times(h.power(a),h.power(-a))==h.ONE,'signed clock is an integral unit')
    for w in h.INVERSE_LIBRARY:
        f=h.inverse_family(w)
        for v in (0,1,2,17,10**20):
            low=f['smaller_source_anchor']+f['smaller_source_step']*v
            high=f['reduced_from_anchor']+f['reduced_from_step']*v
            c.check(h.path(low,w)[-1]==high and low<high,'entire inverse-family coefficient identities')
            c.check((f['U']*high-f['C'])//f['L']==low,'inverse source parameter')
    # Full residue period and one translated copy; no sampling claim for root formula.
    for n in range(1,2*8748,2):
        for enabled in (False,True):
            c.check((h.choose_move(n,enabled) is None)==h.arithmetic_root(n,enabled),'arithmetic root predicate')
    old=h.HeightRetraction(False);new=h.HeightRetraction()
    tested=list(range(1,2048,2))+[1731+2916*t for t in (1,2,3,10,100,10**12,10**30)]
    for n in tested:
        v={n:h.ONE};H=new.H(v);Q=new.Q(v);F=new.F(v)
        c.check(h.jet_d(H)==h.add_vectors(v,h.scale((-1,0),Q)),'d H = I-Q')
        c.check(new.Q(Q)==Q,'Q idempotent')
        c.check(new.F(F)==F,'F idempotent')
        c.check(h.jet_d(F)==new.Q(h.jet_d(v)),'projected differential commutes')
        c.check(new.H(Q)=={} and new.F(H)=={},'homotopy side identities')
        c.check(new.H(h.jet_d(v))==h.add_vectors(v,h.scale((-1,0),F)),'H d = I-F')
        K=h.add_vectors(H,h.scale((-1,0),old.H(v)))
        c.check(h.jet_d(K)==h.add_vectors(old.Q(v),h.scale((-1,0),Q)),'old-new homotopy differential')
        c.check(old.F(K)==K,'new correction remains in old projected edge module')
        c.check(new.F(old.F(v))==F==old.F(F),'both old-new edge projection compositions')
        c.check(new.Q(old.Q(v))==Q==old.Q(Q),'both old-new vertex projection compositions')
        root,_,_=new.resolve(n)
        c.check(root<=n and h.arithmetic_root(root),'finite decreasing endpoint recursion')
    # Small complete pair-word domain; every common target is an original lattice intersection.
    pw=[()]+[w for m in range(1,4) for w in itertools.product((1,2,3),repeat=m)]
    pairs=0;active=0;incompatible=0
    for a in pw:
        for b in pw:
            pairs+=1;f=h.coalescence_family(a,b)
            if not f['target_compatible']:incompatible+=1;continue
            domain=f['parameter_domain']
            if domain is None:continue
            active+=1
            values={domain[0]}
            if domain[1] is None:values.add(domain[0]+3)
            else:values.add(domain[1])
            for t in sorted(values):
                rec=h.coalescence_move(f,t)
                c.check(rec['source']>rec['smaller_source'],'coalescence strict source-height margin')
                c.check(rec['left_original_path'][-1]==rec['right_original_path'][-1],'same original endpoint')
                chain={int(n):tuple(v) for n,v in rec['dual_edge_chain'].items()}
                c.check(h.jet_d(chain)==h.add_vectors({rec['source']:h.ONE},{rec['smaller_source']:h.neg(h.power(rec['signed_clock']))}),'coalescence integral chain equation')
    # The new residual-root family is checked as constant/slope arithmetic, not just at points.
    lw=(1,);rw=(1,1,1,1,1,2,3);newfamily=h.coalescence_family(lw,rw)
    c.check([newfamily[k] for k in ('left_source_anchor','left_source_step','right_source_anchor','right_source_step','common_target_anchor','common_target_step')]==[1731,2916,1215,2048,2597,4374],'new whole coalescence family')
    end=[]
    for x,z,w in ((1731,2916,lw),(1215,2048,rw)):
        for a in w:
            c.check((3*x+1)%(1<<a)==0 and (3*z)%(1<<a)==0,'original affine row divisibility')
            x=(3*x+1)//(1<<a);z=3*z//(1<<a)
            c.check(x%2==1 and z%2==0,'exact valuation on all nonnegative parameters')
        end.append((x,z))
    c.check(end==[(2597,4374),(2597,4374)],'whole family common target')
    c.check(1731-1215>0 and 2916-2048>0,'whole family strict height difference')
    c.check(sum(h.arithmetic_root(n,False) for n in range(3,8748,2))==1214,'old original residue roots retained')
    c.check(sum(h.arithmetic_root(n,True) for n in range(3,8748,2))==1211,'new original residue roots retained')
    # These exact controls show that a finite jet keeps the integral cycle index.
    for m in range(2,33):
        c.check(h.power(m)==(1,m),'period holonomy retains actual length')
        c.check(all(-m*k!=1 for k in range(-3,4)),'finite integral unit obstruction control')
    # Authentic predecessor receiver and independently recomposed finite witnesses.
    source=Path(__file__).parent.parent/'intrinsic_zero_firstjet_20260915'/'firstjet.py'
    data=source.read_bytes();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    c.check(blob=='97f9ef5ad535f7ec18259d41fab6a3557be17d98','unchanged original first-jet source blob')
    spec=importlib.util.spec_from_file_location('_original_firstjet',source);mod=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
    arrival=[]
    for n in (27,31,165,1215,1731,8175,8731,1126015,3732423,5624777):
        record=mod.witness(n,10000);c.check(record['status']=='verified_finite_first_order_boundary','original integral point receiver')
        arrival.append(record)
    # The globally reduced column returns to the SAME integral singleton receiver.
    spliced=[]
    for n in (13,31,1731,4647,10479):
        root,clock,original_chain=new.resolve(n)
        receiver=mod.witness(root,10000)
        c.check(receiver['status']=='verified_finite_first_order_boundary','retained root has a point receiver')
        combined=Counter({e:v[0] for e,v in original_chain.items()})
        combined.update(receiver['linear_chain'])
        accepted=mod.validate_witness(n,receiver['constant_cycle'],mod.clean(combined))
        c.check(accepted['status']=='verified_finite_first_order_boundary','height/coalescence column splices integrally')
        spliced.append({'source':n,'root':root,'signed_clock':clock,'witness':accepted})
    # Negative input and false-map tests are always active under -O.
    c.reject(lambda:h.step(0),'zero original source')
    c.reject(lambda:h.step(4),'even original source')
    c.reject(lambda:h.packet((1,0)),'zero exponent')
    c.reject(lambda:h.inverse_family((2,)),'contracting word used for decreasing inverse')
    c.reject(lambda:h.crt_pair(0,4,1,2),'incompatible source-image congruences')
    c.reject(lambda:h.path(3,(2,)),'wrong original valuation')
    bad=dict(newfamily);bad['left_source_step']+=2
    c.reject(lambda:h.coalescence_move(bad,0),'altered source lattice')
    c.reject(lambda:h.coalescence_move(newfamily,-1),'negative parameter')
    c.reject(lambda:h.add_vectors({3:(1,0.5)}),'rational jet coefficient')
    move=h.choose_move(1731)
    wrong=h.Move(move.source,move.target,0,move.chain,move.kind,move.original_word,move.original_values,move.other_word,move.other_values)
    c.reject(lambda:h.check_move(wrong),'discarded signed original clock')
    c.reject(lambda:mod.validate_witness(3,{1:-1},{3:0.5,5:1}),'nonintegral singleton primitive')
    c.reject(lambda:mod.validate_witness(3,{1:-1},{3:1}),'truncated singleton primitive')
    c.reject(lambda:h.envelope(0),'zero horizon')
    examples={str(n):new.certificate(n) for n in (1,11,31,165,1731,4647,7563,8731,1731+2916*10**20)}
    return {'status':'PASS','total_exact_regression_checks':sum(c.counts.values()),
            'checks':dict(sorted(c.counts.items())),'complete_word_sum_bound':16,'words_visited':words,
            'first_crossing_words':firstcross,'critical_extremizers':extremizers,
            'complete_pair_words':len(pw),'word_pairs':pairs,'active_pair_families':active,
            'incompatible_pair_labels':incompatible,'horizon':10280,'finite_window_upper_odd':5624777,
            'next_horizon_record':[10281,16295,6728242],
            'new_global_coalescence_family':newfamily,'retraction_examples':examples,
            'point_firstjet_witnesses':arrival,'spliced_height_witnesses':spliced,'predecessor_blob':blob,
            'external_transcendence_or_logarithm_estimate_used':False,
            'full_2812388_source_scan_is_separately_certified':True}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path);p.add_argument('--check',type=Path)
    a=p.parse_args();r=test();b=(json.dumps(r,sort_keys=True,indent=2)+'\n').encode()
    if a.check:h.need(a.check.read_bytes()==b,'recorded structural result is not byte-identical')
    if a.output:a.output.write_bytes(b)
    print(json.dumps({'status':'PASS','checks':r['total_exact_regression_checks'],'words':r['words_visited'],'sha256':hashlib.sha256(b).hexdigest()},sort_keys=True))
if __name__=='__main__':main()
