"""Exact finite regressions for the independently proved parity coordinates.
General integer identities have the separate Lean certificate; sampled
counts/graphs do not certify infinite analytic statements. No Lean launch.
"""
from pathlib import Path
from functools import lru_cache
from collections import Counter
from hashlib import sha256
from math import comb
from fractions import Fraction
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
SRC=ROOT/"external_literature/shaik_2026_v324/source/FirstPassageLinearTransport-ef3410843bf58d69f771f5ba2c0571d54b54da59/lean/FirstPassageLinearTransport"
LDW=ROOT/"external_literature/1209.3495v1/main.tex"
counts=Counter()
def require(b,label):
    if not b: raise AssertionError(label)
def T(n): return n//2 if n%2==0 else (3*n+1)//2
def orbit(n,k):
    xs=[n]
    for _ in range(k): xs.append(T(xs[-1]))
    return xs
def code(n,k):
    ans=0
    for i in range(k):
        ans+=2**i*(n%2); n=T(n)
    return ans
@lru_cache(None)
def decode(k,w):
    if k==0: return 0
    r=decode(k-1,w%2**(k-1))
    return r if code(r,k)==w else r+2**(k-1)
@lru_cache(None)
def barrier_count(a,r,y):
    if abs(y)>a:return 2**r
    if r==0:return 0
    return barrier_count(a,r-1,y-1)+barrier_count(a,r-1,y+1)
def word_hits(a,r,y,w):
    hit=abs(y)>a
    for i in range(r):
        y+=2*((w>>i)&1)-1
        hit=hit or abs(y)>a
    return hit
def cosh_log_integer(z,k):
    return (z**abs(k)+z**(-abs(k)))/2
def main():
    for length in range(8):
        for a in range(5):
            for y in range(-3,4):
                B=barrier_count(a,length,y)
                require(B==sum(word_hits(a,length,y,w) for w in range(2**length)),
                        "exact open-barrier recursive count")
                counts["exact_barrier_recursions"]+=1
                for z in (Fraction(1),Fraction(3,2),Fraction(2)):
                    require(B*cosh_log_integer(z,a)<=
                            2**length*cosh_log_integer(z,y)*cosh_log_integer(z,1)**length,
                            "exact rational cosh potential")
                    counts["rational_cosh_potentials"]+=1
    for m in range(11):
        N=2**m
        for w in range(N):
            r=decode(m,w); n=N+r
            require(0<=r<N and code(r,m)==w,"right inverse")
            require(decode(m,code(w,m))==w,"left inverse")
            require(N<=n<2*N and code(n,m)==w,"positive shell inverse")
            require(sum(x%2 for x in orbit(n,m)[:-1])==w.bit_count(),"weight")
            counts["decoder_and_weight"]+=1
        for j in range(m+1):
            for u in range(2**j):
                r=decode(j,u); a=u.bit_count()
                ds=range(2**(m-j),2**(m+1-j))
                ns=[r+2**j*d for d in ds]
                ys=[Tj for Tj in (orbit(n,j)[-1] for n in ns)]
                require(all(N<=n<2*N and code(n,j)==u for n in ns),"prefix fibre")
                require(ys==[orbit(r,j)[-1]+3**a*d for d in ds],"actual image progression")
                suffix=[code(y,m-j) for y in ys]
                require(sorted(suffix)==list(range(2**(m-j))),"uniform suffix codes")
                weights=Counter(w.bit_count() for w in suffix)
                require(all(weights[b]==comb(m-j,b) for b in range(m-j+1)),"conditional binomial")
                counts["prefix_fibres"]+=1
                counts["actual_image_points"]+=len(ys)
        hist=Counter(code(n,m).bit_count() for n in range(N,2*N))
        require(all(hist[s]==comb(m,s) for s in range(m+1)),"shell binomial")
        counts["complete_binomial_shells"]+=1
        for n in range(min(512,4*N)):
            w=code(n,m)
            require(n==decode(m,w)+N*(n//N),"full fibre quotient")
            require(code(n%N,m)==w,"residue invariance")
            counts["natural_fibres"]+=1
        if m:
            for r in range(N):
                targets={T(r)%N,T(r+N)%N}
                w=code(r,m)
                require(len(targets)==2,"distinct state successors")
                require({code(y,m) for y in targets}=={w//2,w//2+N//2},"directed graph map")
                require({decode(m,v) for v in (w//2,w//2+N//2)}==targets,"inverse edge map")
                require({T(r+N*d)%N for d in range(-3,4)}==targets,"all signed lift classes")
                counts["graph_vertices"]+=1
    for m in range(8):
        for n in range(64):
            xs=orbit(n,m)
            for d in range(4):
                ys=orbit(n+2**m*d,m)
                for i in range(m+1):
                    s=sum(x%2 for x in xs[:i])
                    require(s==sum(y%2 for y in ys[:i]),"lift odd count")
                    require(ys[i]==xs[i]+2**(m-i)*3**s*d,"lift exact integer")
                    counts["lift_coordinates"]+=1
    require([decode(3,w) for w in range(8)]==[0,5,2,3,4,1,6,7],"figure table")
    require([T(n) for n in (9,11,13,15)]==[14,17,20,23],"figure progression")
    tex=(HERE/"audit.tex").read_text(encoding="utf-8")
    title=r"\section{Shaik's timeout tail, critical rate and drift clock}"
    section=title+tex.split(title,1)[1].split(r"\section{",1)[0]
    mapped=section.strip().replace(r"\section{",r"\subsection{",1).replace("shaik-","Shaik-")
    cumulative=(ROOT/"tex/chapters/01n_shaik_reverse_transport.tex").read_text(encoding="utf-8")
    require(cumulative.strip().endswith(mapped),"full written proof propagation")
    counts["complete_written_propagation"]+=1
    v=json.loads((HERE/"formal_shaik_core/verification.json").read_text(encoding="utf-8"))
    require(v["status"]=="passed" and len(v["theorem_axioms"])==36,"formal certificate scope")
    for name,digest in v["artifact_hashes"].items():
        require(sha256((HERE/"formal_shaik_core"/name).read_bytes()).hexdigest()==digest,"formal receipt stale")
    out={"status":"passed","counts":dict(counts),"lean_started":False,
      "formal_scope":"36 separately compiled all-input exact statements, including complete-shell binomial cardinality and the finite-startup count bound. Prefix-conditioned cardinality and graph packaging remain written proofs; real-variable absorption and analytic density are not formalized here.",
      "test_scope":"Complete shells 0<=m<=10; full prefix disintegration; lifts m<=7,n<64,d<4; signed-lift graph checks; exact barrier counts r<=7,a<=4,abs(y)<=3 and rational cosh potentials at exp(theta)=1,3/2,2.",
      "source_hashes":{name:sha256((SRC/name).read_bytes()).hexdigest() for name in ("Parity.lean","Barrier.lean")},
      "laarhoven_source":{"path":str(LDW),"sha256":sha256(LDW.read_bytes()).hexdigest(),"read_lines":[63,175]},
      "artifact_hashes":{name:sha256((HERE/name).read_bytes()).hexdigest() for name in
        ("audit.tex","CLAIMS.json","check_shaik_parity.py","draw_shaik_parity.py",
         "shaik_parity_coordinates.png","formal_shaik_core/verification.json")},
      "whole_natural_density_package_verified":False}
    (HERE/"shaik_parity_checks.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":"passed","counts":dict(counts)},indent=2))
if __name__=="__main__":main()
