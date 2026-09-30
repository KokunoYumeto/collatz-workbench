"""Exact finite tests for ND099-100. Infinite statements are proved in audit.tex."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from decimal import Decimal as D, localcontext
import hashlib, json
from check_shaik_endpoint import window, block, good, shortcut, K

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
SRC=ROOT/"external_literature/shaik_2026_v324/source/FirstPassageLinearTransport-ef3410843bf58d69f771f5ba2c0571d54b54da59/lean/FirstPassageLinearTransport"
LABELS=("prop:shaik-clipped-horizon","eq:shaik-clipped-block",
 "eq:shaik-clipped-sum","eq:shaik-clipped-odd","cor:shaik-closed-graded",
 "eq:shaik-closed-coefficients","eq:shaik-closed-shortcut",
 "eq:shaik-closed-three","eq:shaik-closed-cutoff","eq:shaik-closed-count")
def req(b,m):
 if not b: raise AssertionError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def horizon(n):
 if n<K:return 0
 M=n.bit_length()-1;q=15*M//16
 # Exact 16th-power clearance of rho^h*n^(17/16)<=2^q.
 for h in range(M+1):
  if 3**(8*h)*n**17<=2**(16*(h+q)):return h
 raise AssertionError("the stage terminal hypothesis failed")
def coarse_horizon(M):
 h=0
 while 3**(8*h)*2**(2*M+33)>2**(16*h):h+=1
 return h
def main():
 req(__debug__,"optimized execution is not a check")
 c=Counter();req(3**8<2**13,"exact rational bound on logarithm")
 starts=list(range(1,40))+[K-1,K,K+1]
 seed=83
 for M in (64,65,80,96,128,192,256):
  for _ in range(10):
   seed=(6364136223846793005*seed+1442695040888963407)%(2**300)
   starts.append(2**M+seed%(2**M))
 chains=[]
 for n in starts:
  for R in range(4):
   z=n;h=s=nu=cap=0;rows=[]
   for i in range(R):
    m=z.bit_length()-1;y,l,t,_,_=block(z)
    if z>=K and window(z):
     H=horizon(z);HS=coarse_horizon(m)
     req(0<l<=H<=min(m,HS),"original passage/exact/source clipped horizons")
     x=z
     for _ in range(H):x=shortcut(x)
     req(x<=2**(15*m//16),"actual horizon witness")
     req(3**(8*(H-1))*z**17>2**(16*(H-1+15*m//16)),
         "exact horizon minimality")
     if 16*t-8*l>=0:req(3**(16*t-8*l)<=z,"block odd-count envelope")
     c["exact_active_block_horizons"]+=1
    else:H=0
    if z>=K:nu+=1
    rows.append(dict(start=str(z),rank=m,actual=l,horizon=H,
                     full=m if z>=K else 0))
    h+=l;s+=t;cap+=H;z=y
   if not good(n,R):continue
   g=sum((F(15,16)**i for i in range(nu)),F(0))
   req(h<=cap,"summed original clocks")
   req(2**(h*g.denominator)<=n**g.numerator,"absorbing geometric clock")
   e=(3*cap-34*nu)*g.denominator
   if e>=0:req(2**e<=n**(2*g.numerator),"rational bound for exact horizon sum")
   e=(16*s-8*h)*g.denominator
   if e>=0:req(3**e<=n**g.numerator,"accumulated odd-count envelope")
   req(n*3**s<=2**h*z,"whole-path affine bound")
   if R and n**(15**R)>=K**(16**R):
    req(z**(16**R)<=n**(15**R),"closed exponent without startup multiplier")
    c["exact_closed_exponent_witnesses"]+=1
   c["exact_retained_chains"]+=1
   if R==3 and nu==3:chains.append(dict(n=str(n),rows=rows,h=h,s=s))
 # Rational model test of the exact carry/ceiling algebra, including boundaries.
 for r in (F(13,16),F(7,8),F(15,16)):
  for eta in (F(1,32),F(1,16)):
   gap=F(1,5);a=(1+eta-r)/gap;cr=(1+r)/gap+1
   for M in range(1,41):
    for u in (F(0),F(1,4),F(999,1000)):
     q=(r*M).__floor__();x=M+u
     v=r*M-q;num=(1+eta)*x-q;H=(num/gap).__ceil__()
     req(num==(1+eta-r)*x+r*u+v,"literal floor carry")
     req(H<a*x+cr,"strict ceiling intercept")
     c["rational_floor_carry_cases"]+=1
 with localcontext() as ctx:
  ctx.prec=65;ell=D(2).ln();lam=D(3).ln()/ell;gap=1-lam/2
  r=D(15)/16;eta=D(1)/16;a=(1+eta-r)/gap;cr=(1+r)/gap+1
  threshold=((2+eta)/(r-lam/2-eta)).to_integral_value(rounding="ROUND_CEILING")
  E=max(D(64),threshold)+(2+eta)/gap+1
  for R in range(1,21):
   alpha=r**R;geom=(1-alpha)/(1-r);ct=a*geom/ell
   cs=ct/2+eta*geom/D(3).ln()
   req(abs(cs-(ct-(1-alpha)/ell)/lam)<D("1e-60"),"same leading odd coefficient")
   req(E-cr==D(64)+a or abs(E-cr-D(64)-a)<D("1e-60"),"intercept comparison")
   c["decimal_coefficient_diagnostics"]+=1
  constants=dict(a=str(a),c_r=str(cr),source_E=str(E),M0=64)
 req(chains,"no retained three-active-block illustration")
 example=chains[-1]
 tex=(HERE/"audit.tex").read_text(encoding="utf-8")
 for label in LABELS:req(tex.count("\\label{"+label+"}")==1,"proof locator")
 title=r"\section{Shaik's timeout tail, critical rate and drift clock}"
 sec=title+tex.split(title,1)[1].split(r"\section{",1)[0]
 mapped=sec.strip().replace(r"\section{",r"\subsection{",1).replace("shaik-","Shaik-")
 req((ROOT/"tex/chapters/01n_shaik_reverse_transport.tex").read_text(encoding="utf-8").strip().endswith(mapped),
     "complete cumulative propagation")
 claims=json.loads((HERE/"CLAIMS.json").read_text(encoding="utf-8"))["claims"]
 for nd,clm in (("ND-099","CLM-COL-000292"),("ND-100","CLM-COL-000293")):
  req(next(x for x in claims if x["id"]==nd)["canonical_claim_id"]==clm,"claim map")
 c["complete_written_propagation"]+=1
 names=("HeightSensitiveClock.lean","GradedClock.lean","RawClockBudget.lean",
        "PowerDescent.lean","RawNaturalDensityDescent.lean")
 reading=[dict(name=name,sha256=sha(SRC/name),
               lines=len((SRC/name).read_text(encoding="utf-8").splitlines()),read="complete") for name in names]
 out=dict(status="passed",counts=dict(c),reading=reading,example=example,constants=constants,
  scope="Exact integer actual-envelope, first-passage, accumulated odd and closed-exponent tests, rational floor/ceiling checks; Decimal diagnostics are noncertifying. Infinite analytic claims have written proofs, not finite certificates.",
  lean_started=False,new_formal_theorems=0,whole_natural_density_package_verified=False,
  artifact_hashes={name:sha(HERE/name) for name in ("audit.tex","CLAIMS.json","check_shaik_clipped.py","draw_shaik_clipped.py")})
 if (HERE/"shaik_clipped_horizons.png").exists():
  out["artifact_hashes"]["shaik_clipped_horizons.png"]=sha(HERE/"shaik_clipped_horizons.png")
 (HERE/"shaik_clipped_checks.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(dict(status="passed",counts=dict(c)),indent=2))
if __name__=="__main__":main()
