"""Finite exact count/clock regressions and noncertifying scalar diagnostics for ND110."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from itertools import product
import hashlib,json,math
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
def req(b,msg):
    if not b: raise AssertionError(msg)
def floor(v): return v.numerator//v.denominator
def step(n): return n//2 if n%2==0 else (3*n+1)//2
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    counts=Counter()
    # Exact arbitrary shell budgets, with oscillations and every partial top shell.
    for M0 in range(4):
        for budgets in product(*(range(2**m+1) for m in range(M0,4))):
            bs=dict(zip(range(M0,4),budgets))
            bad=set(range(1,2**M0))
            for m,b in bs.items(): bad.update(range(2**m,2**m+b))
            for X in range(1,16):
                N=X.bit_length()-1
                actual=sum(n<=X for n in bad)
                if N<M0: bound=X
                else:
                    bound=2**M0-1+sum(bs[m] for m in range(M0,N))
                    bound+=min(X-2**N+1,bs[N])
                req(actual==bound,"sharp finite shell budget / partial endpoint")
                counts["exact_prefix_budget_extrema"]+=1
                for K in range(M0,N+1):
                    sup=max(F(bs[m],2**m) for m in range(K,N+1))
                    req(actual<=2**K-1+2*X*sup,"nonmonotone tail supremum")
                    counts["exact_tail_sup_bounds"]+=1
    # A top-shell-only bound fails on a nonmonotone profile.
    example_bad={2};X=8
    top_error=F(len(example_bad & set(range(8,16))),8)
    req(len(example_bad & set(range(1,X+1)))>X*top_error,
        "previous bad shell survives at zero top-shell error")
    counts["nonmonotone_counterexample"]+=1
    # Every possible subset through shell 2: no placement assumption in upper bound.
    for mask in range(1<<7):
        bad={i+1 for i in range(7) if mask>>i&1}
        b={m:len(bad & set(range(2**m,2**(m+1)))) for m in range(3)}
        for X in range(1,8):
            N=X.bit_length()-1
            cap=sum(b[m] for m in range(N))+min(X-2**N+1,b[N])
            req(len(bad & set(range(1,X+1)))<=cap,"arbitrary bad-point placement")
            counts["exhaustive_subset_prefixes"]+=1
    # Rational majorants retain floor and cardinality cap.
    for m in range(8):
        for den in range(1,8):
            for num in range(2*den+1):
                delta=F(num,den); b=min(2**m,floor(2**m*delta))
                req(0<=b<=2**m and F(b,2**m)<=delta,"integer density budget")
                counts["rational_density_budgets"]+=1
    # Actual finite Collatz prefixes: affine identity and expansion are integer exact.
    for n in range(1,513):
        x=n;s=0;B=0;raw=n;raw_steps=0;raw_peak=n;short_peak=n
        for k in range(1,33):
            old=x
            if old%2:
                s+=1;B=3*B+2**(k-1)
                raw=3*raw+1;raw_steps+=1;raw_peak=max(raw_peak,raw)
            raw//=2;raw_steps+=1;raw_peak=max(raw_peak,raw)
            x=step(old);short_peak=max(short_peak,x)
            req(2**k*x==3**s*n+B,"actual affine endpoint with nonnegative B")
            req(B>=0 and 3**s*n<=2**k*x,"parity-clock comparison")
            req(raw==x and raw_steps==k+s,"same endpoint raw expansion")
            req(raw_peak<=2*short_peak,"inserted peak bound")
            counts["actual_affine_raw_clock_prefixes"]+=1
    # Float diagnostics ONLY, separate from the exact checks and general written proof.
    diagnostics=Counter();ell=math.log(2)
    for b in (ell/100,ell/10,ell/2,9*ell/10):
        d=ell-b;Cd=2+1/math.sqrt(2*d*math.e)
        for L in range(1,201):
            ratio=(math.sqrt(L)+2/math.sqrt(L))*math.exp(-d*L)
            req(ratio<=Cd*(1+1e-14),"low prefactor scalar diagnostic")
            diagnostics["low_constant_samples"]+=1
    for mu in (.01,.1,.5,2.,10.):
        maximum=(3/(2*mu*math.e))**1.5
        for j in range(1,201):
            v=j/(10*mu)
            req(v**1.5*math.exp(-mu*v)<=maximum*(1+1e-14),"high absorption maximum")
            diagnostics["high_absorption_samples"]+=1
    for M in (8,31,127,1023):
        for L in (2,7,19,50):
            kappa=.13
            buffer=kappa*L-.5*math.log2(M+2)-math.log2(math.log(M+3))
            a=2**(-buffer)
            b=math.sqrt(M+2)*math.log(M+3)*math.exp(-kappa*ell*L)
            req(abs(a-b)<=1e-12*max(a,b),"buffer exact identity diagnostic")
            diagnostics["buffer_identity_samples"]+=1
    tex=(HERE/"audit.tex").read_text(encoding="utf-8")
    labs=["thm:shaik-refined-moving-endpoint","eq:shaik-refined-moving-domain",
          "eq:shaik-refined-moving-buffer","eq:shaik-refined-moving-profile",
          "eq:shaik-refined-moving-witness","eq:shaik-refined-moving-global-count",
          "eq:shaik-moving-tail-sup","cor:shaik-refined-moving-clocks"]
    for lab in labs:req(tex.count("\\label{"+lab+"}")==1,"unique proof locator")
    title=r"\section{Shaik's timeout tail, critical rate and drift clock}"
    section=title+tex.split(title,1)[1].split(r"\section{",1)[0]
    mapped=section.strip().replace(r"\section{",r"\subsection{",1).replace("shaik-","Shaik-")
    req((ROOT/"tex/chapters/01n_shaik_reverse_transport.tex").read_text(encoding="utf-8").strip().endswith(mapped),
        "complete cumulative propagation")
    claims=json.loads((HERE/"CLAIMS.json").read_text(encoding="utf-8"))["claims"]
    current=next(c for c in claims if c["id"]=="ND-110")
    req(current["canonical_claim_id"]=="CLM-COL-000303","canonical crosswalk")
    for old in ("ND-104","ND-106","ND-107","ND-108","ND-109"):
        req("ND-110" in next(c for c in claims if c["id"]==old)["later_refinements"],"upstream propagation")
    counts["complete_written_propagation"]+=1
    out=dict(status="passed",counts=dict(counts),noncertifying_diagnostics=dict(diagnostics),
        new_formal_theorems=0,lean_started=False,whole_natural_density_package_verified=False,
        scope="Exact finite dyadic counts and actual integer orbit-clock identities; floating scalar diagnostics are not proofs. Infinite analytic endpoint has the separate written proof, not a new Lean certificate.",
        artifact_hashes={n:sha(HERE/n) for n in ("audit.tex","CLAIMS.json","check_shaik_moving_endpoint.py",
              "draw_shaik_moving_endpoint.py","shaik_moving_endpoint_assembly.png")})
    (HERE/"shaik_moving_endpoint_checks.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:out[k] for k in ("status","counts","noncertifying_diagnostics")},indent=2))
if __name__=="__main__":main()
