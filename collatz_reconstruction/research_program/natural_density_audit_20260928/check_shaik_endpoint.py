"""ND093-094 exact finite regressions; general proofs are in audit.tex."""
from pathlib import Path
from fractions import Fraction as F
from functools import cache
from collections import Counter
import hashlib,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
SRC=ROOT/"external_literature/shaik_2026_v324/source/FirstPassageLinearTransport-ef3410843bf58d69f771f5ba2c0571d54b54da59/lean/FirstPassageLinearTransport"
LABELS=("eq:shaik-log-stage","prop:shaik-log-pullback","eq:shaik-log-pullback",
 "eq:shaik-log-recursion","eq:shaik-log-iterate","eq:shaik-log-prefactor",
 "prop:shaik-absorbing-startup","eq:shaik-absorbing-witness","eq:shaik-absorbing-odd")
def req(b,m):
 if not b: raise AssertionError(m)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def shortcut(n): return n//2 if n%2==0 else (3*n+1)//2
K=2**64
@cache
def window(n):
 if n<K:return True
 # eta=1/16, rho=sqrt(3)/2: clearing the 16th powers is exact.
 x=n
 for j in range(n.bit_length()):
  q=(2**(16*j))*x**16
  if not 3**(8*j)*n**15<=q<=3**(8*j)*n**17:return False
  x=shortcut(x)
 return True
@cache
def block(n):
 M=n.bit_length()-1
 if M<64:return (n,0,0,n,n)
 Y=2**((15*M)//16); x=n; odd=0; height=n; rawheight=n
 for h in range(M+1):
  if x<=Y:return (x,h,odd,height,rawheight)
  if h==M:break
  if x%2:
   odd+=1;rawheight=max(rawheight,3*x+1)
  x=shortcut(x);height=max(height,x);rawheight=max(rawheight,x)
 # Literal source failed bounded-passage totalization.
 return (n,0,0,n,n)
@cache
def good(n,R):
 return window(n) and (R==0 or good(block(n)[0],R-1))
def main():
 req(__debug__,"optimized Python invalidates assertions")
 c=Counter()
 for t in (F(5,4),F(4,3),F(3,2),F(7,4)):
  for p in range(9):
   for J in range(31):
    lhs=sum((1+m)**p*t**m for m in range(J+1))
    rhs=(1+J)**p*t**J/(1-1/t)
    req(lhs<=rhs,"weighted final-shell sum")
    c["rational_shell_sums"]+=1
 for ell in (F(1,2),F(2,3),F(3,4)):
  for E in (F(1),F(7,3)):
   for Fv in (F(2),F(5)):
    for Q in (F(1),F(5,2)):
     A0=F(3,2);A=A0;L=1+Q*(E+Fv)
     for j in range(12):
      req(A+1<=(A0+1)*L**j*ell**(-j*(j+1)),"uniform prefactor")
      A=Q*ell**(-2*j-2)*(E+Fv*A)
      c["rational_prefactor_stages"]+=1
 # Exact scalar setup diagnostics, not an infinite-parameter certificate.
 req(3**8<2**13,"rational bound for log_2(3)")
 for M in range(64,513):
  q=15*M//16;Y=2**q
  req(1<Y<2**M and 3*M<=2*Y,"stage size and horizon")
  req(3**(8*M)*2**(M+17)<=2**(16*q),"raised terminal envelope")
  c["integer_stage_setup_samples"]+=1
 # Exact original good-set membership, not random/independent resampling.
 starts=list(range(1,100))+[K-1,K,K+1]
 seed=37
 for M in (64,65,72,90,128,192):
  for j in range(16):
   seed=(6364136223846793005*seed+1442695040888963407)%(2**256)
   starts.append(2**M+(seed%(2**M)))
 examples=[]
 for n in starts:
  for R in range(4):
   z=n;h=0;s=0;height=n;rh=n;marked=[n];retained=True
   for i in range(R+1):
    retained=retained and window(z)
    if i==R:break
    z1,hh,ss,bb,rr=block(z)
    h+=hh;s+=ss;height=max(height,bb);rh=max(rh,rr)
    if retained:
     req((z<K and z1==z and hh==0) or
         (z>=K and 0<hh<=z.bit_length()-1 and z1**16<=z**15),
         "actual retained stage branch")
    z=z1;marked.append(z)
   req(retained==good(n,R),"inverse-image/marked-chain equality")
   c["exact_set_memberships"]+=1
   if not retained:continue
   g=sum((F(15,16)**j for j in range(R)),F(0))
   req(2**(h*g.denominator)<=n**g.numerator,"no startup clock loss")
   req(z<=K or z**(16**R)<=n**(15**R),"absorbing endpoint")
   req(height**16<=n**17 and rh<=2*height,"common height and raw expansion")
   req(n*3**s<=2**h*z,"actual odd-count bound")
   raw=n
   for j in range(h+s):raw=raw//2 if raw%2==0 else 3*raw+1
   req(raw==z,"exact raw endpoint and clock")
   c["exact_retained_witnesses"]+=1
   if h>0 and R==3 and len(examples)<3:
    examples.append(dict(n=str(n),depth=R,marked_vertices=list(map(str,marked)),
                         shortcut_steps=h,odd_inputs=s,raw_steps=h+s,
                         startup_rank=64,r="15/16",eta="1/16"))
 req(examples,"no nonzero retained paths tested")
 tex=(HERE/"audit.tex").read_text(encoding="utf-8")
 for lab in LABELS:req(tex.count(r"\label{"+lab+"}")==1,"unique proof locator")
 title=r"\section{Shaik's timeout tail, critical rate and drift clock}"
 sec=title+tex.split(title,1)[1].split(r"\section{",1)[0]
 mapped=sec.strip().replace(r"\section{",r"\subsection{",1).replace("shaik-","Shaik-")
 req((ROOT/"tex/chapters/01n_shaik_reverse_transport.tex").read_text(encoding="utf-8").strip().endswith(mapped),"complete propagation")
 claims=json.loads((HERE/"CLAIMS.json").read_text(encoding="utf-8"))["claims"]
 for nd,clm in (("ND-093","CLM-COL-000286"),("ND-094","CLM-COL-000287")):
  req(next(x for x in claims if x["id"]==nd)["canonical_claim_id"]==clm,"claim mapping")
 c["complete_written_propagation"]+=1
 reading=[dict(name=name,sha256=sha(SRC/name),lines=len((SRC/name).read_text(encoding="utf-8").splitlines()),read="complete")
          for name in ("Pullback.lean","BarrierDensity.lean","Bootstrap.lean")]
 out=dict(status="passed",counts=dict(c),reading=reading,examples=examples,
  scope="Exact rational scalar sums and prefactor recurrence; integer-cleared window, actual first passages, set recursion, endpoint/clock/height tests. Finite regressions do not prove infinite density estimates, which have complete written proofs.",
  lean_started=False,new_formal_theorems=0,whole_natural_density_package_verified=False,
  artifact_hashes={name:sha(HERE/name) for name in ("audit.tex","CLAIMS.json","check_shaik_endpoint.py","draw_shaik_endpoint.py","shaik_endpoint_transport.png")})
 (HERE/"shaik_endpoint_checks.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({"status":"passed","counts":dict(c)},indent=2))
if __name__=="__main__":main()
