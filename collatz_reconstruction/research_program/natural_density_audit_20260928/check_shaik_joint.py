"""ND095 finite witnesses and ND096 schedule diagnostics.
General integer results have a separate Lean certificate; analytic rates are
proved in audit.tex. Decimal diagnostics are not interval proofs.
"""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D, localcontext, ROUND_CEILING, ROUND_FLOOR
from collections import Counter
import hashlib,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
SRC=ROOT/"external_literature/shaik_2026_v324/source/FirstPassageLinearTransport-ef3410843bf58d69f771f5ba2c0571d54b54da59/lean/FirstPassageLinearTransport"
LABELS=("prop:shaik-joint-certificate","eq:shaik-joint-count","eq:shaik-joint-startup",
 "prop:shaik-matched-schedule","eq:shaik-matched-depth","eq:shaik-matched-clock",
 "eq:shaik-matched-rate","eq:shaik-matched-floor","eq:shaik-matched-landing-cutoff",
 "eq:shaik-matched-shell","eq:shaik-matched-count-cutoff")
def req(b,m):
 if not b:raise AssertionError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def path(n,H,raw=False):
 xs=[n]
 for k in range(H):
  z=xs[-1];xs.append(z//2 if z%2==0 else (3*z+1 if raw else (3*z+1)//2))
 return xs
def main():
 req(__debug__,"optimized Python")
 c=Counter()
 for r in (F(3,4),F(7,8),F(15,16)):
  for a in range(401):
   t=F(a,8);R=t.numerator//t.denominator+1;b=t.denominator
   req(r**(t.numerator+b)<=r**(R*b)<=r**t.numerator,"two-sided cleared floor powers")
   c["exact_floor_power_pairs"]+=1
 for A in (F(1),F(7,3),F(10)):
  for delta in (F(1,100),F(1,5),F(2)):
   for sigma in (F(1,10),F(1,3),F(9,10)):
    v=max(F(1),48*A/(delta*sigma**3))
    req(4*A*v*v <= (delta/2)*(sigma*v)**3/6,"explicit absorption via cubic exp term")
    c["rational_absorption_cutoffs"]+=1
 for n in range(1,101):
  xs=path(n,24);odd=0
  for h in range(25):
   if h:odd+=xs[h-1]%2
   rx=path(n,h+odd,True)
   req(rx[-1]==xs[h] and max(rx)<=2*max(xs[:h+1]),"common raw witness")
   if all(z>xs[h] for z in xs[:h]):
    req(all(z>xs[h] for z in rx[:-1]),"first passage retained")
    c["actual_first_passages"]+=1
   c["actual_clock_height_witnesses"]+=1
 for pm in range(128):
  for qm in range(128):
   fails=[n for n in range(1,8) if pm>>(n-1)&1 and not qm>>(n-1)&1]
   N=1+max(fails,default=0)
   for X in range(8):
    bp=sum(not(pm>>(n-1)&1) for n in range(1,X+1))
    bq=sum(not(qm>>(n-1)&1) for n in range(1,X+1))
    req(bq<=bp+min(X,N-1),"positive-prefix startup count")
    c["exhaustive_predicate_prefixes"]+=1
 for H,S in ((8,4),(16,8),(24,12)):
  taggedbad=rawbad=0
  for n in range(1,201):
   Y=n//2+1;B=5*n;xs=path(n,H);rx=path(n,H+S,True);odd=0;tagged=False
   for h in range(H+1):
    if h:odd+=xs[h-1]%2
    tagged |= odd<=S and xs[h]<=Y and max(xs[:h+1])<=B
   raw=any(rx[h]<=Y and max(rx[:h+1])<=2*B for h in range(H+S+1))
   req(not tagged or raw,"same-start implication")
   taggedbad+=not tagged;rawbad+=not raw
   req(rawbad<=taggedbad,"literal prefix count")
   c["actual_predicate_prefixes"]+=1
 for prec in (60,80):
  with localcontext() as ctx:
   ctx.prec=prec;ell=D(2).ln();tol=D(10)**(-prec+8)
   power=lambda x,a:(a*D(x).ln()).exp()
   for r in (D(".85"),D(".9"),D(".95")):
    for a in (D(".2"),D(".5"),D(".8")):
     sigma=1-a;omega=a/(1/r).ln();eta=D(".01")
     lam=D(3).ln()/ell;c0=1/(2*lam**2);De=c0*eta**2/ell
     C0=2*(4*c0).exp();Ae=2*C0/(2*(-c0*eta**2).exp()-1)
     M0=D(64);E=power(2,r*De*M0)+C0;Fv=D("2.5")*power(2,De)
     Q=1/(1-power(2,r*De-1));L=1+Q*(E+Fv)
     A=(2*(Ae+1)).ln()+(omega+1)*L.ln()+(omega+1)*(omega+2)*(1/ell).ln()+2*(omega+1)
     for M in (D(4),D(64),D(1000),D(10)**8):
      x=M+4;u=x.ln();R=int((omega*u).to_integral_value(rounding=ROUND_FLOOR))+1;rR=r**R
      req(r*power(x,-a)<=rR+tol and rR<=power(x,-a)+tol,"floor signs")
      cost=(2*(Ae+1)).ln()+R*L.ln()+R*(R+1)*(1/ell).ln()+2*R*(1+(M+1)*ell).ln()
      req(cost<=A*u*u+tol,"full prefactor")
      c["decimal_schedule_diagnostics"]+=1
     cutoff=max(D(1),4/(power(ell,-a/sigma)-1),power(M0*ell,1/sigma)/ell)
     Mc=cutoff.to_integral_value(rounding=ROUND_CEILING)+1
     req(ell*power(Mc+4,sigma)<=power(ell*Mc,sigma)+tol,"unit landing coefficient")
     req(M0*ell<=power(ell*Mc,sigma)+tol,"startup target")
     c["decimal_landing_cutoffs"]+=1
 tex=(HERE/"audit.tex").read_text(encoding="utf-8")
 for lab in LABELS:req(tex.count(r"\label{"+lab+"}")==1,"unique label")
 title=r"\section{Shaik's timeout tail, critical rate and drift clock}"
 sec=title+tex.split(title,1)[1].split(r"\section{",1)[0]
 mapped=sec.strip().replace(r"\section{",r"\subsection{",1).replace("shaik-","Shaik-")
 req((ROOT/"tex/chapters/01n_shaik_reverse_transport.tex").read_text(encoding="utf-8").strip().endswith(mapped),"complete propagation")
 claims=json.loads((HERE/"CLAIMS.json").read_text(encoding="utf-8"))["claims"]
 for nd,clm in (("ND-095","CLM-COL-000288"),("ND-096","CLM-COL-000289")):
  req(next(x for x in claims if x["id"]==nd)["canonical_claim_id"]==clm,"claim mapping")
 c["complete_written_propagation"]+=1
 ver=json.loads((HERE/"formal_shaik_joint/verification.json").read_text(encoding="utf-8"))
 req(ver["status"]=="passed" and len(ver["theorem_axioms"])==9,"formal receipt")
 reads=[dict(name=name,sha256=sha(SRC/name),lines=len((SRC/name).read_text(encoding="utf-8").splitlines()),read="complete")
        for name in ("VaryingDensity.lean","BootstrapSchedule.lean","GlobalAssembly.lean","StretchedLogLanding.lean","Constants.lean","Scalar.lean")]
 for name,ranges in (("HeadlineParameters.lean",[[1,175]]),):
  lines=len((SRC/name).read_text(encoding="utf-8").splitlines())
  reads.append(dict(name=name,sha256=sha(SRC/name),lines=lines,read=[[a,min(b,lines)] for a,b in ranges]))
 out=dict(status="passed",counts=dict(c),reading=reads,new_formal_theorems=9,
  formal_verification_receipt="formal_shaik_joint/verification.json",
  analytic_claim_formalized=False,whole_natural_density_package_verified=False,
  scope="Finite rational/actual-orbit regressions, exhaustive finite prefixes, noncertifying decimal diagnostics. Nine general integer statements are kernel checked separately; ND096 remains written analytic proof.",
  artifact_hashes={f:sha(HERE/f) for f in ("audit.tex","CLAIMS.json","check_shaik_joint.py",
   "draw_shaik_joint.py","shaik_joint_schedule.png","formal_shaik_joint/verification.json")})
 (HERE/"shaik_joint_checks.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(dict(status="passed",counts=dict(c),new_formal_theorems=9),indent=2))
if __name__=="__main__":main()
