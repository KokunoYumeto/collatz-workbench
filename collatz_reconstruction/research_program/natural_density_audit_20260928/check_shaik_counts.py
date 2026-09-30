"""Finite regressions for ND086--087; general Lean proofs are separate evidence."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
from math import comb, factorial
import hashlib, json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
SRC=ROOT/"external_literature/shaik_2026_v324/source/FirstPassageLinearTransport-ef3410843bf58d69f771f5ba2c0571d54b54da59/lean/FirstPassageLinearTransport"

def require(b,msg):
    if not b: raise AssertionError(msg)
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def orbit_code(n,m):
    w=s=0
    for i in range(m):
        b=n%2
        w+=b*2**i
        s+=b
        n=n//2 if b==0 else (3*n+1)//2
    return w,s

def main():
    counts=Counter()
    row=[1]
    for m in range(11):
        hist=Counter(orbit_code(2**m+r,m)[1] for r in range(2**m))
        for s in range(m+4):
            b=row[s] if s<len(row) else 0
            require(hist[s]==b==comb(m,s),"literal shell/Pascal count")
            counts["pascal_shell_weights"]+=1
        for f in (lambda w:w*w+3*w+7,lambda w:2**w if w<8 else 0,
                  lambda w:int(w%3==1)):
            expected=sum(f(w) for w in range(2**m))
            require(sum(f(orbit_code(n,m)[0]) for n in range(2**m))==expected,
                    "residue weighted sum")
            require(sum(f(orbit_code(2**m+n,m)[0]) for n in range(2**m))==expected,
                    "positive shell weighted sum")
            counts["weighted_shells"]+=1
        row=[1]+[row[s-1]+(row[s] if s<len(row) else 0) for s in range(1,m+2)]
    for X in range(7):
        full=(1<<X)-1
        for N in range(9):
            E=max(N-1,0)
            start=(1<<min(X,E))-1
            tail=full^start
            for S in range(1<<X):
                for W in range(1<<X):
                    if S&tail&(~W): continue
                    bS=X-S.bit_count();bW=X-W.bit_count()
                    require(bW<=bS+min(X,E),"positive-set finite startup")
                    counts["finite_startup_set_pairs"]+=1
            require((full&~start).bit_count()==X-min(X,E),"sharp startup")
            counts["sharp_startup_examples"]+=1
    for eta in map(Fraction,("1/2","1","5/2","5","11")):
        k=eta.numerator//eta.denominator+1
        b=eta.denominator
        exponent=k*b-eta.numerator
        require(exponent>0,"positive power after exponential-series term")
        for E in (0,1,2,17,100):
            for eps in (Fraction(1,10),Fraction(1),Fraction(3,2)):
                q=Fraction(max(1,E)*factorial(k),1)/eps
                t=max(1,(q.numerator+q.denominator-1)//q.denominator)
                # y=t^b; y^(k-eta)=t^(kb-a), exact integer arithmetic.
                require(eps*t**exponent>=max(1,E)*factorial(k),"rate absorption coefficient")
                counts["rational_absorption_witnesses"]+=1
    tex=(HERE/"audit.tex").read_text(encoding="utf-8")
    title=r"\section{Shaik's timeout tail, critical rate and drift clock}"
    section=title+tex.split(title,1)[1].split(r"\section{",1)[0]
    mapped=section.strip().replace(r"\section{",r"\subsection{",1).replace("shaik-","Shaik-")
    cumulative=(ROOT/"tex/chapters/01n_shaik_reverse_transport.tex").read_text(encoding="utf-8")
    require(cumulative.strip().endswith(mapped),"complete proof propagation")
    for label in ("prop:shaik-weighted-count","prop:shaik-startup-rate",
                  "eq:shaik-startup-exact","eq:shaik-startup-rate"):
        require(tex.count(r"\label{"+label+"}")==1,"unique proof label "+label)
    counts["complete_written_propagation"]+=1
    v=json.loads((HERE/"formal_shaik_core/verification.json").read_text(encoding="utf-8"))
    required={"parity_weighted_sum","shell_parity_weighted_sum","weightCount_binomial",
              "shellOddCountCard_binomial","finite_startup_count_bound"}
    require(v["status"]=="passed" and len(v["theorem_axioms"])==36,"formal count")
    require(required<=set(v["theorem_axioms"]),"missing exact theorem")
    require(all(set(a)<={"propext","Quot.sound"} for a in v["theorem_axioms"].values()),
            "unexpected axioms")
    for name,h in v["artifact_hashes"].items():
        require(digest(HERE/"formal_shaik_core"/name)==h,"stale formal receipt")
    out={"status":"passed","counts":dict(counts),"lean_started":False,
         "general_formal_theorem_count":36,"whole_natural_density_package_verified":False,
         "scope":"Finite regression only. General counts and startup bound are independently kernel checked. Real exponential-series absorption is proved in the manuscript, not formalized here.",
         "source_hashes":{n:digest(SRC/n) for n in
          ("Main.lean","TimeoutCore.lean","TimeoutEndpointNaturalDensity.lean",
           "MovingEndpointAsymptotics.lean","FiniteStartup.lean")},
         "artifact_hashes":{n:digest(HERE/n) for n in
          ("audit.tex","CLAIMS.json","check_shaik_counts.py","formal_shaik_core/verification.json",
           "draw_shaik_startup.py","shaik_startup_count.png")}}
    (HERE/"shaik_count_checks.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":"passed","counts":dict(counts)},indent=2))
if __name__=="__main__": main()
