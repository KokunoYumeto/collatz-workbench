"""ND089-090 finite checks; the general analytic proofs are in audit.tex."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D, localcontext, ROUND_CEILING
from collections import Counter
import hashlib, json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
SRC=ROOT/"external_literature/shaik_2026_v324/source/FirstPassageLinearTransport-ef3410843bf58d69f771f5ba2c0571d54b54da59/lean/FirstPassageLinearTransport"
FULL=("MovingEndpointScalars.lean","MovingEndpointParameters.lean",
      "MovingEndpointAssembly.lean","TimeoutEndpointAsymptotics.lean",
      "TimeoutEndpointNaturalDensity.lean","PolylogExceptionalCount.lean")
PARTIAL={"Main.lean":[[1,160]]}
LABELS=("lem:shaik-antitone-assembly","eq:shaik-antitone-prefix",
        "cor:shaik-critical-rates","eq:shaik-critical-B-rate",
        "eq:shaik-critical-D-rate","eq:shaik-critical-cancellation",
        "prop:shaik-slow-factor","eq:shaik-slow-target",
        "eq:shaik-slow-prefix","eq:shaik-slow-cancellation")
def require(p,m):
    if not p: raise AssertionError(m)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    counts=Counter()
    # Exact cancellation as a polynomial identity tested at rational arguments.
    # u,v,w below substitute logarithmic coordinates, not approximate real logs.
    for k in (F(1,20),F(1,10),F(2,7)):
      a=1/(2*k)
      for u in (F(2),F(7,3),F(100)):
       for v in (F(1,3),F(3),F(50)):
        for w in (F(1,7),F(1),F(12)):
         for rem in (F(0),F(1,2),F(99,100)):
          B=2/k; dp=F(3,7)
          HB=a*u+B*v; HD=a*u+v/k+dp*w; HF=a*u+v/k+w
          for H,want in ((HB,(k*B-1)*v+k*rem),
                         (HD,k*dp*w+k*rem),(HF,k*w+k*rem)):
           require(k*(H+rem)-u/2-v==want,"exact buffer cancellation")
           counts["rational_cancellations"]+=1
    # Exhaust every subset of [1,15], every prefix. Build its decreasing
    # shell-density majorant; this tests incomplete final shells and jumps.
    for mask in range(1<<15):
      shell=[sum((mask>>(n-1))&1 for n in range(1<<m,1<<(m+1))) for m in range(4)]
      q=[F(v,1<<m) for m,v in enumerate(shell)]
      for m in range(2,-1,-1): q[m]=max(q[m],q[m+1])
      bad=0
      for X in range(1,16):
       bad+=(mask>>(X-1))&1
       J=X.bit_length()-1; K=J//2
       sharp=(1<<K)-1+q[K]*((1<<(J+1))-(1<<K))
       loose=(1<<K)+2*X*q[K]
       require(bad<=sharp<=loose,"antitone shell/prefix count")
       counts["exhaustive_subset_prefixes"]+=1
    samples=[]
    for precision in (60,80):
     with localcontext() as ctx:
      ctx.prec=precision
      ell=D(2).ln(); p=ell/D(3).ln()
      h=-p*p.ln()-(1-p)*(1-p).ln()
      k=1-h/ell; a=1/(2*k)
      K1=1/ell+2; K2=1+(1/ell+3).ln()
      K3=1+(1+(1/ell+4).ln()).ln()
      for Mi in (2,4,16,100,1000,10**6,10**12):
       M=D(Mi); x=M+2; v=(M+3).ln(); w=(M+4).ln().ln()
       log2=lambda z:z.ln()/ell
       for multiplier in ("1.01","1.5","3"):
        B=D(multiplier)/k
        for exponent in ("0.1","1","3"):
         dp=D(exponent)
         for kind,H,core in (
            ("B",a*log2(x)+B*log2(v),(k*B-1)*log2(v)),
            ("D",a*log2(x)+log2(v)/k+dp*log2(w),k*dp*log2(w))):
          L=H.to_integral_value(rounding=ROUND_CEILING); rem=L-H
          delta=k*L-log2(x)/2-log2(v)
          require(0<=rem<1,"actual ceiling range")
          require(abs(delta-(core+k*rem))<D(10)**(-precision+8),"decimal cancellation")
          factor=(-ell*k*rem).exp()
          require((-ell*k).exp()<factor<=1,"ceiling multiplier")
          counts["decimal_shifted_schedules"]+=1
          if precision==80 and Mi in (16,10**6) and multiplier=="1.5" and exponent=="1":
           samples.append({"M":Mi,"type":kind,"L":str(L),"delta":str(delta),"rounding_factor":str(factor)})
       u=M*ell
       if u.ln()>1 and u.ln().ln()>1:
        require(x<=K1*u and v<=K2*u.ln() and w<=K3*u.ln().ln(),"target conversion shifts")
        counts["decimal_target_conversions"]+=1
    tex=(HERE/"audit.tex").read_text(encoding="utf-8")
    for lab in LABELS: require(tex.count(r"\label{"+lab+"}")==1,"unique new label")
    title=r"\section{Shaik's timeout tail, critical rate and drift clock}"
    sec=title+tex.split(title,1)[1].split(r"\section{",1)[0]
    mapped=sec.strip().replace(r"\section{",r"\subsection{",1).replace("shaik-","Shaik-")
    require((ROOT/"tex/chapters/01n_shaik_reverse_transport.tex").read_text(encoding="utf-8").strip().endswith(mapped),"complete proof propagation")
    claims=json.loads((HERE/"CLAIMS.json").read_text(encoding="utf-8"))["claims"]
    for nd,clm in (("ND-089","CLM-COL-000282"),("ND-090","CLM-COL-000283")):
       require(next(c for c in claims if c["id"]==nd)["canonical_claim_id"]==clm,"claim identity")
    counts["complete_written_propagation"]+=1
    reading=[{"name":n,"sha256":sha(SRC/n),"lines":len((SRC/n).read_text(encoding="utf-8").splitlines()),
              "read":"complete" if n in FULL else PARTIAL[n]} for n in (*FULL,*PARTIAL)]
    out={"status":"passed","counts":dict(counts),
         "scope":"Exact rational cancellation tests and exhaustive finite shell-prefix counts. 60/80-digit real-log calculations are numerical diagnostics, not interval certificates. No finite test certifies an infinite orbit or analytic theorem.",
         "lean_started":False,"new_formal_theorems":0,"whole_natural_density_package_verified":False,
         "reading":reading,"decimal_samples":samples,
         "artifact_hashes":{n:sha(HERE/n) for n in ("audit.tex","CLAIMS.json","check_shaik_critical.py","draw_shaik_critical.py","shaik_critical_scales.png")}}
    (HERE/"shaik_critical_checks.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":"passed","counts":dict(counts)},indent=2))
if __name__=="__main__": main()
