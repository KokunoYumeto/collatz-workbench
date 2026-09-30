"""Exact rational regressions for ND107-108; general results have written proofs."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import json,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
def req(b,m):
 if not b:raise AssertionError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ceil(x):return -(-x.numerator//x.denominator)
def floor(x):return x.numerator//x.denominator
def budget(g,K,L,M):
 eta=g-K/L;r=1-K/(2*L);t=K*M/(2*L)
 left=(1-g+eta)*M+1+eta;right=floor(r*M)
 req(right==M-ceil(t),"exact integer floor complement")
 req(right-left==2*t-ceil(t)-1-eta,"exact terminal-budget defect")
 return left<=right
def main():
 c=Counter();examples=[]
 for g in (F(1,10),F(1,5),F(1,4),F(1,2),F(9,10)):
  for K in (4+g,4+g+F(1,100),F(5),F(6),F(7),F(21,2)):
   Lst=max(8,ceil(2*K/g))
   for L in (Lst,Lst+1,2*Lst,10*Lst):
    eta=g-K/L;r=1-K/(2*L)
    req(0<eta<=1 and F(1,2)<r<1,"stage parameter ranges")
    for M in range(L,4*L+1):
     req(budget(g,K,L,M),"exact closed-threshold terminal budget")
     q=floor(r*M);Y=2**q
     req(1<Y<2**M and 3*M<=2*Y,"remaining target/horizon fields")
     c["rational_full_stage_samples"]+=1
  for K in (F(1,2),F(2),F(3),F(4),4+g/2,4+g-F(1,1000)):
   lower=K/g
   if K<=2:
    L= floor(lower)+2;M=L;case="K<=2"
   elif K<=4:
    L=floor(2*K/g)+2;M=floor(4*L/K)+1;case="2<K<=4"
   else:
    L=floor(max(lower,K/(4+g-K)))+2;M=L;case="4<K<4+g"
   req(M>=L and not budget(g,K,L,M),"explicit obstruction")
   c["explicit_counterparents"]+=1
   examples.append(dict(g=str(g),K0=str(K),L=L,M=M,case=case,
      initial_parent_passes=budget(g,K,L,L),witness_parent_fails=True))
  for rs in (F(1,10),F(1,2),F(9,10)):
   K=4+g;L=max(8,ceil(2*K/g),ceil(K/(2*(1-rs))),ceil(F(9,2)/rs))
   req(rs<=1-K/(2*L),"common lower ratio")
   for q in range(L,L+150):
    req(F(q+2,1)/(rs*2**q)<=F(1,3),"uniform small transport condition")
    c["rational_common_startups"]+=1
 for g in (F(1,10),F(1,5),F(1,4),F(1,2),F(9,10)):
  for K in (F(1,2),F(1),F(2),F(3),F(4),4+g,F(6),F(21,2)):
   Lmin=floor(2*K/g)+1
   for L in (Lmin,Lmin+1,2*Lmin,10*Lmin):
    rho=(4+g)/K;B=rho*L-1;Z=ceil(B)
    req(Z>=10 and not budget(g,K,L,Z-1),"least startup last failed parent")
    req(rho*L-1<=Z<rho*L,"exact one-rank rounding")
    req((Z<=L)==(K>=(4+g)*L/(L+1)),"finite necessary/sufficient threshold")
    c["exact_minimum_and_finite_threshold"]+=1
    for M in range(Z,Z+150):
     req(budget(g,K,L,M),"least startup full suffix")
     q=floor((1-K/(2*L))*M);Y=2**q
     req(1<Y<2**M and 3*M<=2*Y,"least startup remaining fields")
     c["least_startup_suffix_fields"]+=1
 for a in range(1,6):
  for b in range(a,7):
   U=set(range(1,2**(b+1)))
   for wmod in (2,3,5):
    W={n for n in U if n%wmod!=0}
    for smod in (2,3,5,7):
     S={n for n in U if n%smod==0}
     def image(n):
      m=n.bit_length()-1;Y=2**floor(F(3,4)*m);v=n
      for k in range(m+1):
       if v<=Y:return v
       v=v//2 if v%2==0 else (3*v+1)//2
      return n
     def pull(s):
      return {n for n in U if (n in W or n<2**s)
              and (n if n<2**s else image(n)) in S}
     pa,pb=pull(a),pull(b)
     expected={n for n in U if 2**a<=n<2**b
        and ((n in S)!=(n in W and image(n) in S))}
     req(pa^pb==expected,"exact annular xor identity")
     for X in (1,2**a-1,2**a,2**b-1,2**b,2**(b+1)-1):
      count=abs(sum(n<=X for n in pa)-sum(n<=X for n in pb))
      req(count<=max(0,min(X+1,2**b)-2**a),"exact clipped annular count")
     c["finite_annulus_set_identities"]+=1
 for n in range(4,2000):
  req(3*(2*n+1)<=2**(n+1),"explicit half-ratio horizon")
  c["integer_horizon_bounds"]+=1
 tex=(HERE/"audit.tex").read_text(encoding="utf-8")
 labels=["prop:shaik-exact-moving-startup","eq:shaik-exact-moving-threshold",
   "eq:shaik-exact-moving-budget","eq:shaik-sawtooth-budget","eq:shaik-common-moving-startup"]
 labels += ["prop:shaik-least-moving-startup","eq:shaik-least-moving-startup",
   "eq:shaik-least-moving-rounding","eq:shaik-finite-moving-threshold",
   "eq:shaik-startup-map-comparison","eq:shaik-startup-pullback-difference"]
 for lab in labels:req(tex.count("\\label{"+lab+"}")==1,"unique proof locator")
 title=r"\section{Shaik's timeout tail, critical rate and drift clock}"
 sec=title+tex.split(title,1)[1].split(r"\section{",1)[0]
 mapped=sec.strip().replace(r"\section{",r"\subsection{",1).replace("shaik-","Shaik-")
 req((ROOT/"tex/chapters/01n_shaik_reverse_transport.tex").read_text(encoding="utf-8").strip().endswith(mapped),
     "complete cumulative propagation")
 claims=json.loads((HERE/"CLAIMS.json").read_text(encoding="utf-8"))["claims"]
 req(next(x for x in claims if x["id"]=="ND-107")["canonical_claim_id"]=="CLM-COL-000300","claim mapping")
 req("ND-107" in next(x for x in claims if x["id"]=="ND-106")["later_refinements"],"density propagation")
 req(next(x for x in claims if x["id"]=="ND-108")["canonical_claim_id"]=="CLM-COL-000301","least startup claim mapping")
 req("ND-108" in next(x for x in claims if x["id"]=="ND-107")["later_refinements"],"sharp threshold propagation")
 c["complete_written_propagation"]+=1
 out=dict(status="passed",counts=dict(c),counterexamples=examples,
  scope="Exact Fraction/integer samples check all original scalar fields, floor defects, counterparent constructions, common finite startup, the exact least startup and finite threshold. The universal results are established by their written proofs, not these samples.",
  new_formal_theorems=0,lean_started=False,whole_natural_density_package_verified=False,
  artifact_hashes={n:sha(HERE/n) for n in ["audit.tex","CLAIMS.json","check_shaik_startup.py","draw_shaik_startup_floor.py","shaik_startup_floor.png","draw_shaik_least_startup.py","shaik_least_startup.png"]})
 (HERE/"shaik_startup_checks.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(dict(status="passed",counts=dict(c),noninitial_counterexample=next(x for x in examples if x["initial_parent_passes"])),indent=2))
if __name__=="__main__":main()
