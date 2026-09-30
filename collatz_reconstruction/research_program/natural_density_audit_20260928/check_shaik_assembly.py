"""Sharp shell assembly: exact finite regression, not an infinite proof."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D, localcontext
from collections import Counter
from math import isqrt
import hashlib,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
SRC=ROOT/"external_literature/shaik_2026_v324/source/FirstPassageLinearTransport-ef3410843bf58d69f771f5ba2c0571d54b54da59/lean/FirstPassageLinearTransport"
LABELS=("prop:shaik-sharp-shell","eq:shaik-shifted-shell-input",
 "eq:shaik-sharp-shell-finite","eq:shaik-sharp-shell-asymptotic",
 "prop:shaik-linear-shell","cor:shaik-unclipped-source-count",
 "eq:shaik-unclipped-source-count")
def req(b,m):
 if not b:raise AssertionError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def iroot(n,k):
 if k==2:return isqrt(n)
 lo,hi=0,n+1
 while hi-lo>1:
  m=(lo+hi)//2
  if m**k<=n:lo=m
  else:hi=m
 return lo
def floor_cap(gamma,slope,M):
 # q=floor(gamma*2^(slope*M)), proved by exact cleared powers.
 e=slope*M
 power=gamma**e.denominator * F(2)**e.numerator
 q=iroot(power.numerator//power.denominator,e.denominator)
 req(F(q)**e.denominator<=power<F(q+1)**e.denominator,"integer floor cap")
 return q
def main():
 req(__debug__,"optimized Python")
 c=Counter()
 for A in (F(1,4),F(1),F(2),F(10)):
  for eps in (F(1,100),F(1,3),F(2)):
   t=1+eps/(4*A+eps)
   req(1<t<2 and A/(1-t/2)==2*A+eps/2,"exact theta coefficient")
   c["rational_prefactor_choices"]+=1
 for t in (F(11,10),F(5,4),F(3,2),F(7,4)):
  for J in range(31):
   for N0 in range(J+1):
    # Worst admissible relative shell weights t^(J-M).
    total=sum(F(2)**M*t**(J-M) for M in range(N0,J+1))
    req(total<=F(2)**J/(1-t/2),"geometric terminal majorant")
    c["exact_terminal_sums"]+=1
 for mask in range(1<<10):
  points=[n for n in range(1,11) if mask>>(n-1)&1]
  shell=[sum(2**m<=n<2**(m+1) for n in points) for m in range(4)]
  for X in range(1,11):
   J=X.bit_length()-1
   actual=sum(n<=X for n in points)
   req(actual<=sum(shell[:J+1]),"literal prefix to full shells")
   for N0 in range(J+1):
    early=sum(n<2**N0 for n in points)
    partial=sum(2**J<=n<=X for n in points)
    req(actual==early+sum(shell[N0:J])+partial,"disjoint positive-prefix identity")
    c["exhaustive_prefix_partitions"]+=1
 for gamma in (F(1,4),F(1),F(4),F(17,3)):
  for q in (F(1,4),F(1,2),F(3,4),F(1),F(5,4),F(3,2),F(2)):
   slope=1-q
   caps=[floor_cap(gamma,slope,M) for M in range(49)]
   for M,cap in enumerate(caps):
    if q==1:req(cap==gamma.numerator//gamma.denominator,"critical integer cap")
    if q>1 and cap==0:req(all(x==0 for x in caps[M:]),"supercritical integer extinction")
    c["exact_linear_shell_caps"]+=1
   if q>1:
    req(caps[-1]==0,"finite exact extinction sample")
 # Exact illustrative sets: first q_M points in each shell, gamma=1.
 prefixes={}
 for q in (F(1,2),F(1),F(3,2)):
  sums=[];total=0
  for M in range(21):
   cap=floor_cap(F(1),1-q,M)
   req(0<=cap<=2**M,"illustration fits actual integer shell")
   total+=cap;sums.append(total)
   if q==1:req(total==M+1,"one point per shell")
   if q>1:req(total==1,"only initial point")
   c["exact_illustrated_prefixes"]+=1
  prefixes[str(q)]=sums
 for prec in (60,80):
  with localcontext() as ctx:
   ctx.prec=prec;ell=D(2).ln();tol=D(10)**(-prec+8)
   power=lambda x,a:(a*D(x).ln()).exp()
   for alpha in (D(".2"),D(".5"),D(".8")):
    for cc in (D(".1"),D(".7"),D("2")):
     A=D(2);theta=D(".3")
     N0=max(D(0),power(cc*alpha/theta,1/(1-alpha))-4)
     n0=int(N0)+1
     for gap in (0,1,3,9):
      J=n0+gap
      total=sum(power(2,M)*(-cc*power(M+4,alpha)).exp() for M in range(n0,J+1))
      bound=power(2,J)*(-cc*power(J+4,alpha)).exp()/(1-theta.exp()/2)
      req(total<=bound+tol*max(D(1),bound),"shifted sum diagnostic")
      c["decimal_shifted_sums"]+=1
     Dc=D(".1");kappa=ell*Dc/20
     revised=kappa/power(ell,alpha);old=kappa/8
     req(abs(revised/old-8/power(ell,alpha))<=tol,"source rate factor")
     c["decimal_rate_factors"]+=1
 tex=(HERE/"audit.tex").read_text(encoding="utf-8")
 for lab in LABELS:req(tex.count(r"\label{"+lab+"}")==1,"unique proof label")
 title=r"\section{Shaik's timeout tail, critical rate and drift clock}"
 sec=title+tex.split(title,1)[1].split(r"\section{",1)[0]
 mapped=sec.strip().replace(r"\section{",r"\subsection{",1).replace("shaik-","Shaik-")
 req((ROOT/"tex/chapters/01n_shaik_reverse_transport.tex").read_text(encoding="utf-8").strip().endswith(mapped),"full proof propagation")
 claims=json.loads((HERE/"CLAIMS.json").read_text(encoding="utf-8"))["claims"]
 for nd,clm in (("ND-097","CLM-COL-000290"),("ND-098","CLM-COL-000291")):
  req(next(x for x in claims if x["id"]==nd)["canonical_claim_id"]==clm,"claim mapping")
 c["complete_written_propagation"]+=1
 names=("HeadlineParameters.lean","QuantitativeNaturalDensityDescent.lean",
        "StretchedExceptionalCount.lean","Density.lean","ClockBudget.lean","NaturalDensityDescent.lean")
 reading=[dict(name=n,sha256=sha(SRC/n),lines=len((SRC/n).read_text(encoding="utf-8").splitlines()),read="complete") for n in names]
 report=dict(status="passed",counts=dict(c),reading=reading,illustrated_prefixes=prefixes,
  new_formal_theorems=0,lean_started=False,whole_natural_density_package_verified=False,
  scope="Exact rational/integer finite checks and noncertifying Decimal diagnostics. Complete analytic and sharpness proofs are in TeX; no new Lean theorem.",
  artifact_hashes={n:sha(HERE/n) for n in ("audit.tex","CLAIMS.json","check_shaik_assembly.py","draw_shaik_assembly.py","shaik_linear_shells.png")})
 (HERE/"shaik_assembly_checks.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(dict(status="passed",counts=dict(c)),indent=2))
if __name__=="__main__":main()
