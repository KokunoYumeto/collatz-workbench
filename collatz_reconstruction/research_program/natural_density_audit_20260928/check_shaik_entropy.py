"""ND101-102 finite checks. Real-variable results are proved in audit.tex."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D, localcontext
from collections import Counter
from functools import cache
import hashlib,json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
SRC=ROOT/"external_literature/shaik_2026_v324/source/FirstPassageLinearTransport-ef3410843bf58d69f771f5ba2c0571d54b54da59/lean/FirstPassageLinearTransport"
LABELS=("eq:shaik-full-entropy-constants","prop:shaik-full-entropy",
 "eq:shaik-full-entropy-shell","eq:shaik-entropy-quadratic-comparison",
 "lem:shaik-entropy-terminal","eq:shaik-entropy-terminal",
 "cor:shaik-entropy-propagation","eq:shaik-entropy-pullback",
 "eq:shaik-entropy-iterate","eq:shaik-entropy-fixed-failure",
 "eq:shaik-entropy-stretched")
def req(b,m):
 if not b:raise AssertionError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
@cache
def bad(M,a):
 states={0:1}
 for _ in range(M):
  nxt={}
  for y,c in states.items():
   for z in (y-1,y+1):
    if abs(z)<=a:nxt[z]=nxt.get(z,0)+c
  states=nxt
 return 2**M-sum(states.values())
def fr(z,r,L):
 return z**L*((1+3*F(L+2)/r)/(1-z)+3*z/r/(1-z)**2)
def main():
 req(__debug__,"optimized execution invalidates checks");counts=Counter()
 for M in range(15):
  for a in {0,1,M//3,M}:
   total=0
   for word in range(2**M):
    y=0;hit=False
    for i in range(M):
     y+=1 if (word>>i)&1 else -1
     hit|=abs(y)>a
    total+=hit
   req(total==bad(M,a),"open two-sided boundary/Boolean enumeration")
   counts["exhaustive_boolean_cases"]+=1
 for M in range(41):
  for a in range(M+1):
   for w in (F(3,2),F(2)):
    cosh=(w+1/w)/2;at_a=(w**a+w**(-a))/2
    req(bad(M,a)*at_a<=2**M*cosh**M,"exact rational cosh potential")
    counts["rational_cosh_potentials"]+=1
 for z in (F(1,2),F(2,3),F(3,4),F(7,8)):
  for r in (F(3,4),F(15,16),F(5,4)):
   for L in range(1,9):
    for U in range(L,L+9):
     exact=sum(((1+3*F(q+2)/r)*z**q for q in range(L,U+1)),F(0))
     req(exact==fr(z,r,L)-fr(z,r,U+1),"both endpoints in exact terminal sum")
     req(exact<=fr(z,r,L),"positive discarded tail")
     counts["exact_terminal_profiles"]+=1
 # eta=1/16: m_eta=16 is sufficient, by integer-cleared comparisons.
 for M in range(16,513):
  req(3**(8*M)>=2**(M+16),"affine-correction startup with constant<8")
  counts["integer_startup_comparisons"]+=1
 seed=109;regular=0
 for M in (64,96,128,192,256,512):
  for _ in range(60):
   seed=(6364136223846793005*seed+1442695040888963407)%(2**600)
   n=2**M+seed%2**M;x=n;s=0;ok=True;path=[]
   for j in range(M+1):
    path.append(x)
    if 3**(8*abs(2*s-j))>2**(M-16):ok=False;break
    s+=x%2;x=x//2 if x%2==0 else (3*x+1)//2
   counts["actual_barrier_samples"]+=1
   if not ok:continue
   for j,x in enumerate(path):
    req(3**(8*j)*n**15<=2**(16*j)*x**16<=3**(8*j)*n**17,
        "actual barrier implies unchanged full orbit envelope")
   regular+=1
 req(regular>10,"regular actual examples absent")
 counts["actual_regular_envelopes"]=regular
 plot=[]
 with localcontext() as ctx:
  ctx.prec=80;ell=D(2).ln();lam=D(3).ln()/ell
  eta=D(1)/16;u=eta/lam
  B=lambda x:ell+(D(".5")+x)*(D(".5")+x).ln()+(D(".5")-x)*(D(".5")-x).ln()
  b=B(u);J=((D(".5")+u)/(D(".5")-u)).ln()/lam
  c0=1/(2*lam*lam);old=c0*eta*eta
  C=max(2*J.exp(),(15*b).exp());oldC=2*(4*c0).exp()
  req(b>4*old,"entropy/quadratic strict comparison diagnostic")
  for den in (32,16,8,4):
   v=D(1)/den
   req(B(v)>2*v*v,"strict entropy comparison diagnostic")
   for M in (64,128,256,512,1024):
    shift=1/(lam*M);vM=v-shift
    req(vM>=0,"diagnostic domain")
    deriv=((D(".5")+v)/(D(".5")-v)).ln()
    req(M*B(vM)>=M*B(v)-deriv/lam,"derivative payment diagnostic")
    counts["decimal_entropy_diagnostics"]+=1
  for M in (16,32,64,128,192,256,384,512,768,1024,1536,2048):
   a=0
   while 3**(8*(a+1))<=2**(M-16):a+=1
   num=bad(M,a);fraction=D(num)/D(2**M)
   newbound=2*J.exp()*(-b*M).exp()
   req(fraction<=newbound,"exact tree count vs Decimal endpoint bound diagnostic")
   counts["decimal_exact_tree_comparisons"]+=1
   plot.append(dict(M=M,integer_barrier=a,bad_words=str(num),
       total_words=str(2**M),fraction=str(fraction),
       entropy_bound=str(newbound),quadratic_bound=str(oldC*(-old*M).exp())))
  constants=dict(eta="1/16",b_eta=str(b),old_quadratic=str(old),
      ratio=str(b/old),J_eta=str(J),C_eta=str(C),m_eta=16)
 tex=(HERE/"audit.tex").read_text(encoding="utf-8")
 for label in LABELS:req(tex.count("\\label{"+label+"}")==1,"unique proof locator")
 title=r"\section{Shaik's timeout tail, critical rate and drift clock}"
 sec=title+tex.split(title,1)[1].split(r"\section{",1)[0]
 mapped=sec.strip().replace(r"\section{",r"\subsection{",1).replace("shaik-","Shaik-")
 req((ROOT/"tex/chapters/01n_shaik_reverse_transport.tex").read_text(encoding="utf-8").strip().endswith(mapped),
     "complete cumulative propagation")
 cs=json.loads((HERE/"CLAIMS.json").read_text(encoding="utf-8"))["claims"]
 for nd,clm in (("ND-101","CLM-COL-000294"),("ND-102","CLM-COL-000295")):
  req(next(c for c in cs if c["id"]==nd)["canonical_claim_id"]==clm,"canonical claim mapping")
 for nd in ("ND-091","ND-092","ND-093","ND-096","ND-100"):
  req("ND-102" in next(c for c in cs if c["id"]==nd)["later_refinements"],"downstream claim crosslink")
 counts["complete_written_propagation"]+=1
 names=("ShrinkingBarrierRun.lean","AdjustableBarrierDensity.lean","EntropyBarrier.lean",
        "TerminalTail.lean","TerminalProfile.lean","AdjustableEnvelope.lean","Envelope.lean",
        "FirstBadEnvelope.lean")
 reading=[dict(name=n,sha256=sha(SRC/n),lines=len((SRC/n).read_text(encoding="utf-8").splitlines()),
               read="complete") for n in names]
 artifacts=("audit.tex","CLAIMS.json","check_shaik_entropy.py","draw_shaik_entropy.py")
 out=dict(status="passed",counts=dict(counts),reading=reading,plot_data=plot,constants=constants,
  scope="Exact Boolean enumeration, rational cosh potentials, exact finite terminal profiles and integer-cleared actual barrier/envelope samples. Decimal rate diagnostics and plotting are not certificates. Complete infinite statements are written in audit.tex.",
  lean_started=False,new_formal_theorems=0,whole_natural_density_package_verified=False,
  artifact_hashes={n:sha(HERE/n) for n in artifacts})
 if (HERE/"shaik_entropy_rate.png").exists():out["artifact_hashes"]["shaik_entropy_rate.png"]=sha(HERE/"shaik_entropy_rate.png")
 (HERE/"shaik_entropy_checks.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(dict(status="passed",counts=dict(counts),constants=constants),indent=2))
if __name__=="__main__":main()
