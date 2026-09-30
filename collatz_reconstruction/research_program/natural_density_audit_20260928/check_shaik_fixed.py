"""ND091-092 finite regressions. Infinite estimates are proved in audit.tex."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D, localcontext, ROUND_CEILING, ROUND_FLOOR
from collections import Counter
import hashlib,json,re
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
SRC=ROOT/"external_literature/shaik_2026_v324/source/FirstPassageLinearTransport-ef3410843bf58d69f771f5ba2c0571d54b54da59/lean/FirstPassageLinearTransport"
READS={"HeightSensitiveClock.lean":"complete","GradedPowerDescent.lean":"complete",
       "Bootstrap.lean":[[1,160]],"GradedClock.lean":[[206,342]],
       "StretchedExceptionalCount.lean":[[1,90]],
       "QuantitativeNaturalDensityDescent.lean":[[146,316]],"Main.lean":[[161,393]]}
LABELS=("lem:shaik-fixed-barrier","eq:shaik-fixed-failure","eq:shaik-fixed-witness",
"eq:shaik-fixed-clock","lem:shaik-final-shell","eq:shaik-final-shell",
"eq:shaik-final-shell-natural","prop:shaik-stretched-fixed","eq:shaik-stretched-rate",
"eq:shaik-fixed-odd-budget","prop:shaik-graded-quantitative","eq:shaik-graded-clocks",
"eq:shaik-graded-rate","eq:shaik-graded-parameters")
def req(b,msg):
    if not b: raise AssertionError(msg)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 c=Counter()
 # Rational substitutions test algebra, not the values of real logarithms.
 for lam in (F(3,2),F(8,5),F(7,4)):
  g=1-lam/2
  for ell in (F(1,2),F(2,3),F(3,4)):
   for alpha in (F(1,100),F(1,4),F(1,2),F(3,4),F(99,100)):
    for eps in (F(1,100),F(1,2),F(1),F(10)):
     for beta in (F(1,100),F(1,10),F(1),F(10)):
      budget=eps*g*ell/(2*(1+1/lam))
      r=1-min(g/2,budget/(4*alpha))
      eta=min((r-lam/2)/2,beta/2,(1-r)*budget/4,F(1,2))
      mu=alpha*(1-r)+eta/(1-r)
      req(lam/2<r<1 and 0<eta<r-lam/2,"strict fixed parameters")
      req(eta<=beta/2 and mu<=budget/2,"clock and height margins")
      req((1/g-1)/lam==1/(2*g),"exact odd coefficient")
      req((1+1/lam)/g-1/lam==3/(2*g),"exact raw coefficient")
      req((1+1/lam)*mu/(g*ell)<=eps/4,"all-clock slack")
      c["rational_parameter_packages"]+=1
 # Floor/rank telescope on all generated abstract certified rank chains.
 # These are scalar chains, not asserted to be actual Collatz trajectories.
 for r in (F(4,5),F(7,8),F(19,20)):
  for M in range(10,201):
   for alpha in (F(1,4),F(1,2),F(3,4)):
    L=max(3,int(alpha*M)); m=M; ms=[]; qs=[]
    while m>=L:
     q=int(r*m); ms.append(m); qs.append(q); m=q-1
    j=len(ms)-1
    req(sum(a-b for a,b in zip(ms,qs))==M-qs[-1]-j,"rank telescope")
    req(qs[-1]>=r*L-1 and sum(ms)<F(M)/(1-r),"rank/floor bounds")
    req(F(L)<=r**j*M,"last-parent rank")
    eta=(r-F(3,4))/4
    direct=sum((1+eta)*(v+1)-q+1 for v,q in zip(ms,qs))
    telescoped=M-qs[-1]+eta*sum(ms)+(1+eta)*j+2+eta
    req(direct==telescoped,"complete clock payment")
    c["rational_rank_chains"]+=1
 # Exact geometric tails, including their finite truncation remainder.
 for z in (F(1,2),F(2,3),F(3,4)):
  for L in range(1,21):
   total=z**L*((L+1)/(1-z)+z/(1-z)**2)
   for N in (L,L+3,L+20):
    partial=sum((q+1)*z**q for q in range(L,N+1))
    tail=z**(N+1)*((N+2)/(1-z)+z/(1-z)**2)
    req(total==partial+tail,"exact first-failure tail")
    c["exact_geometric_tails"]+=1
 # Every subset of [1,7], every prefix, rational profile f(m)=t^-m.
 for mask in range(1<<7):
  for t in (F(4,3),F(3,2),F(7,4)):
   shell=[sum((mask>>(n-1))&1 for n in range(1<<m,1<<(m+1))) for m in range(3)]
   A=max(F(shell[m],1<<m)*t**m for m in range(1,3))
   bad=0
   for X in range(1,8):
    bad+=(mask>>(X-1))&1
    J=X.bit_length()-1
    if J>=1:
     bound=1+A*(1<<J)*t**(-J)/(1-t/2)
     req(bad<=bound,"last-shell prefix with incomplete top")
     c["exhaustive_subset_prefixes"]+=1
 # Decimal evaluations diagnose the logarithmic formula implementation;
 # they are not rigorous interval bounds or infinite-claim certificates.
 samples=[]
 for prec in (60,80):
  with localcontext() as ctx:
   ctx.prec=prec; ell=D(2).ln()
   powr=lambda x,a:(a*x.ln()).exp()
   tol=D(10)**(-prec+10)
   for sigma in (D(".1"),D(".3"),D(".5"),D(".9")):
    for d in (D(".1"),D(1),D(3)):
     N0=max(2,int(powr(2*d*sigma/ell,1/(1-sigma)).to_integral_value(rounding=ROUND_CEILING))+1)
     for p in (D(0),D(".5"),D(2)):
      for base in (N0,2*N0,10*N0):
       J=D(base+12); M=D(base)
       req(d*sigma*powr(M,sigma-1)<=ell/2+tol,"derivative cutoff")
       logratio=p*(M/J).ln()+d*(powr(J,sigma)-powr(M,sigma))
       req(logratio<=(ell/2)*(J-M)+tol,"last-shell profile inequality")
       nu=powr(ell,sigma-1)
       H=nu*powr(M,sigma); L=H.to_integral_value(rounding=ROUND_FLOOR)
       req(0<=H-L<1 and ell*L<=powr(M*ell,sigma)+tol,"exact target-rank floor")
       req(abs(d/powr(ell,sigma)-(d/nu)/ell)<tol,"coefficient conversion")
       c["decimal_profile_diagnostics"]+=1
       if prec==80 and p==2 and base==N0:
        samples.append({"sigma":str(sigma),"d":str(d),"N0":N0,"L":str(L)})
 tex=(HERE/"audit.tex").read_text(encoding="utf-8")
 for label in LABELS: req(tex.count(r"\label{"+label+"}")==1,"unique proof label")
 title=r"\section{Shaik's timeout tail, critical rate and drift clock}"
 sec=title+tex.split(title,1)[1].split(r"\section{",1)[0]
 mapped=sec.strip().replace(r"\section{",r"\subsection{",1).replace("shaik-","Shaik-")
 req((ROOT/"tex/chapters/01n_shaik_reverse_transport.tex").read_text(encoding="utf-8").strip().endswith(mapped),"complete proof propagation")
 claims=json.loads((HERE/"CLAIMS.json").read_text(encoding="utf-8"))["claims"]
 for nd,clm in (("ND-091","CLM-COL-000284"),("ND-092","CLM-COL-000285")):
  req(next(x for x in claims if x["id"]==nd)["canonical_claim_id"]==clm,"canonical claim mapping")
 c["complete_written_propagation"]+=1
 reading=[]
 for name,ranges in READS.items():
  lines=len((SRC/name).read_text(encoding="utf-8").splitlines())
  if ranges!="complete":
   ranges=[[a,min(b,lines)] for a,b in ranges]
  reading.append({"name":name,"sha256":sha(SRC/name),"lines":lines,"read":ranges})
 out={"status":"passed","counts":dict(c),"reading":reading,"decimal_samples":samples,
 "scope":"Exact rational parameter, rank and geometric-tail tests; exhaustive finite subset/prefix tests. Decimal real-log/profile samples are numerical diagnostics, not interval certificates. The general analytic and actual-orbit proofs are in audit.tex.",
 "lean_started":False,"new_formal_theorems":0,"whole_natural_density_package_verified":False,
 "artifact_hashes":{name:sha(HERE/name) for name in ("audit.tex","CLAIMS.json","check_shaik_fixed.py","draw_shaik_fixed.py","shaik_fixed_clocks.png")}}
 (HERE/"shaik_fixed_checks.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({"status":"passed","counts":dict(c)},indent=2))
if __name__=="__main__": main()

