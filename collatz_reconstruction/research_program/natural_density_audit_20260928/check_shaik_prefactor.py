"""ND103-104: exact finite tests; analytic claims are written proofs."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D, localcontext
from math import comb
from collections import Counter
import hashlib,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
SRC=ROOT/"external_literature/shaik_2026_v324/source/FirstPassageLinearTransport-ef3410843bf58d69f771f5ba2c0571d54b54da59/lean/FirstPassageLinearTransport"
LABELS=("lem:shaik-exact-reflection","eq:shaik-reflection-tail","eq:shaik-explicit-stirling",
"prop:shaik-uniform-prefactor","eq:shaik-uniform-prefactor","eq:shaik-fixed-prefactor",
"cor:shaik-prefactor-propagation","eq:shaik-prefactor-pullback","eq:shaik-prefactor-iterate",
"eq:shaik-prefactor-terminal","eq:shaik-prefactor-fixed-failure","eq:shaik-prefactor-stretched",
"eq:shaik-prefactor-graded","cor:shaik-shrinking-prefactor","eq:shaik-shrinking-prefactor",
"eq:shaik-shrinking-high-charge")
def req(b,s):
 if not b:raise AssertionError(s)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def heights(w):
 y=0;ys=[0]
 for bit in w:y+=bit;ys.append(y)
 return ys
def reflection(w,a):
 ys=heights(w);t=ys.index(a)
 return w[:t]+tuple(-v for v in w[t:])
def tail(M,k):return sum(comb(M,j) for j in range(k,M+1))
def main():
 req(__debug__,"checks require assertions enabled")
 counts=Counter()
 for M in range(13):
  ws=[tuple(1 if (w>>j)&1 else -1 for j in range(M)) for w in range(2**M)]
  pairs=[(w,heights(w)) for w in ws]
  for a in range(1,M+2):
   left={w for w,y in pairs if max(y)>=a and y[-1]<a}
   right={w for w,y in pairs if y[-1]>a}
   req({reflection(w,a) for w in left}==right,"reflection onto exact strict endpoint")
   for w in left|right:
    req(reflection(reflection(w,a),a)==w,"coordinate inverse")
    counts["inverse_word_checks"]+=1
   k=(M+a+1)//2;kp=(M+a)//2+1
   hit=sum(max(y)>=a for _,y in pairs)
   both=sum(max(map(abs,y))>=a for _,y in pairs)
   req(hit==tail(M,k)+tail(M,kp),"parity-aware exact one-sided identity")
   req(both<=2*hit<=4*tail(M,k),"two-sided union")
   counts["exhaustive_reflection_cases"]+=1
 for M in range(1,201):
  for k in range(M//2+1,M+1):
   req(sum((2*j-M)*comb(M,j) for j in range(k,M+1))==k*comb(M,k),
       "weighted telescoping identity")
   req((2*k-M)*tail(M,k)<=k*comb(M,k),"exact tail inequality")
   counts["integer_binomial_tails"]+=1
 for n in range(1,1001):
  z=F(1,2*n+1)**2
  req(z/(1-z)==F(1,4*n*(n+1)),"Stirling geometric remainder")
  req(sum((F(1,4*j*(j+1)) for j in range(1,n)),F(0))==F(n-1,4*n),
      "finite Stirling telescoping")
  counts["rational_stirling_telescopes"]+=1
 for r in (F(3,4),F(7,8),F(15,16)):
  for M in range(2,301):
   x=r*M;q=x.numerator//x.denominator
   req(q>=x/2 and q<=M,"negative-log-power floor comparison")
   ms=M;qs=[]
   while ms>=1:
    q=(r*ms).numerator//(r*ms).denominator
    if q<1:break
    qs.append(q);ms=q-1
   req(len(qs)==len(set(qs)) and sum(qs)<=r*M/(1-r),"actual deterministic ranks")
   for S in (1,5,17):
    actual=sum(( (F(2)**(q-M)+4*F(q+2)/(3*r))*F(2)**(-q)
                for q in qs if q>S),F(0))
    cr=1+4/(3*r)
    # Sum_{q>S}(q+2)2^-q = (S+4)2^-S.
    req(actual<=cr*(S+4)*F(2)**(-S),"upper-endpoint rank sum")
    counts["rational_high_endpoint_sums"]+=1
 for J in range(101):
  for M in range(J+1):
   req(F(J+1,M+1)<=J-M+1,"reverse-index square-root weight")
   counts["integer_weight_comparisons"]+=1
 # Decimal diagnostics only: explicit constants and rounded entropy region.
 diagnostics=[]
 with localcontext() as ctx:
  ctx.prec=65;ell=D(2).ln();lam=D(3).ln()/ell;a0=lam/2
  cstar=(D(2)/D(1).exp()).sqrt()
  for tau in (D(1)/16,D(1)/4,D(3)/4):
   ut=tau/lam;delta=(D("0.5")-ut)/2
   J=((D("0.5")+ut)/(D("0.5")-ut)).ln()/lam
   ncap=int(max(D(1),( (2*(2+D(3).sqrt())).ln()/ell-2)/(a0-tau),
                    2/(D("0.5")-ut)).to_integral_value(rounding="ROUND_CEILING"))
   K=4*lam*cstar*J.exp()/delta.sqrt()
   for eta in (tau,tau/2,tau/16):
    for factor in (1,2,8):
     M=max(ncap,int((2/eta).to_integral_value(rounding="ROUND_CEILING")))*factor
     u=eta/lam;v=u-1/(lam*M);a=int(2*v*M)+1;k=(M+a+1)//2;p=D(k)/M
     req(eta*M>=2 and v<p-D("0.5")<=v+D(1)/M and 1-p>=delta,
         f"Decimal-only rounding diagnostic: tau={tau}, eta={eta}, M={M}, v={v}, p={p}")
     B=lambda t:ell+(D("0.5")+t)*(D("0.5")+t).ln()+(D("0.5")-t)*(D("0.5")-t).ln()
     bound=K/(eta*D(M).sqrt())*(-D(M)*B(u)).exp()
     # Rational exact tail computed as integers; real comparison is diagnostic.
     frac=D(4*tail(M,k))/D(2**M)
     req(frac<=bound,"Decimal-only binomial vs proved envelope-bound diagnostic")
     diagnostics.append(dict(tau=str(tau),eta=str(eta),M=M,k=k,
          four_tail_fraction=str(frac),bound=str(bound),K=str(K)))
     counts["decimal_diagnostics"]+=1
 tex=(HERE/"audit.tex").read_text(encoding="utf-8")
 for label in LABELS:req(tex.count("\\label{"+label+"}")==1,"unique proof label")
 title=r"\section{Shaik's timeout tail, critical rate and drift clock}"
 sec=title+tex.split(title,1)[1].split(r"\section{",1)[0]
 mapped=sec.strip().replace(r"\section{",r"\subsection{",1).replace("shaik-","Shaik-")
 req((ROOT/"tex/chapters/01n_shaik_reverse_transport.tex").read_text(encoding="utf-8").strip().endswith(mapped),
     "complete cumulative argument propagation")
 cs=json.loads((HERE/"CLAIMS.json").read_text(encoding="utf-8"))["claims"]
 for n,c in (("ND-103","CLM-COL-000296"),("ND-104","CLM-COL-000297")):
  req(next(x for x in cs if x["id"]==n)["canonical_claim_id"]==c,"claim mapping")
 for n in (82,88,91,92,93,96,100,101,102):
  req("ND-104" in next(x for x in cs if x["id"]==f"ND-{n:03d}")["later_refinements"],
      "affected prior result crosslink")
 counts["complete_written_propagation"]+=1
 names=("SharpEntropyBarrier.lean","ShrinkingBarrierCore.lean","ShrinkingHighDensity.lean","ShrinkingTimeSupport.lean","Extras/Unreachable/SharpEntropyBarrier.lean")
 reading=[dict(name=n,sha256=sha(SRC/n),lines=len((SRC/n).read_text(encoding="utf-8").splitlines()),read="complete") for n in names]
 artifacts=("audit.tex","CLAIMS.json","check_shaik_prefactor.py","draw_shaik_prefactor.py","mathlib_stirling_9837ca9.lean")
 out=dict(status="passed",counts=dict(counts),reading=reading,decimal_diagnostics=diagnostics,
 scope="Exact reflection domains/inverses, parity endpoints, binomial telescoping, rational Stirling telescopes, rank sums and weighted comparisons. Decimal real-number evaluations are diagnostics only. No infinite theorem follows from enumeration.",
 lean_started=False,new_formal_theorems=0,whole_natural_density_package_verified=False,
 artifact_hashes={n:sha(HERE/n) for n in artifacts})
 if (HERE/"shaik_prefactor_reflection.png").exists():
  out["artifact_hashes"]["shaik_prefactor_reflection.png"]=sha(HERE/"shaik_prefactor_reflection.png")
 (HERE/"shaik_prefactor_checks.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(dict(status="passed",counts=dict(counts)),indent=2))
if __name__=="__main__":main()
