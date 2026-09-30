"""ND088 finite checks. Analytic proof is in audit.tex; this is not a formal certificate."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D, localcontext, ROUND_CEILING
from collections import Counter
import hashlib, json
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SRC = ROOT / "external_literature/shaik_2026_v324/source/FirstPassageLinearTransport-ef3410843bf58d69f771f5ba2c0571d54b54da59/lean/FirstPassageLinearTransport"
FULL = ("ShrinkingParameters.lean", "FixedPolylogParameters.lean",
        "ShrinkingNaturalDensityDescent.lean", "ShrinkingTailAsymptotics.lean",
        "ShrinkingPolylogProfile.lean", "ShrinkingOrbitCeiling.lean",
        "Parameters.lean", "PolylogTarget.lean", "AdjustableEntropyRate.lean",
        "TerminalTailAsymptotics.lean")
PARTIAL = {"Pullback.lean":[[1,72]], "ShrinkingBarrierRun.lean":[[1,65]],
           "AdjustableBarrierDensity.lean":[[21,38]], "EntropyBarrier.lean":[[23,38]],
           "BarrierDensity.lean":[[73,79],[160,167]],
           "TerminalTail.lean":[[1,45]], "TerminalProfile.lean":[[1,45]]}

def require(p, msg):
    if not p: raise AssertionError(msg)
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def ceil(x): return -(-x.numerator // x.denominator)
def dyadic(u,v):
    k=0
    while 2**k*(v-u)<=1: k+=1
    r=F((u*2**k).__floor__()+1,2**k)
    require(u<r<v,"dyadic interval")
    return r

def main():
    count=Counter()
    # Rational substitutions test the parameter algebra, not identities of real logs.
    for ell in (F(1,2),F(2,3),F(3,4)):
      for a in (F(2,3),F(3,4),F(4,5)):
       g=1-a; lam=2*a; c0=1/(2*lam**2)
       for A in (F(10),F(20),F(50)):
        delta=A/10-F(1,2); bstar=ell/10
        for f in (F(1,10),F(1,2),F(9,10),F(99,100)):
         gamma=delta*f; theta=(gamma+F(1,2))*ell/A
         bj=(theta+bstar)/2; b=(theta+bj)/2
         t=g*F(99,100)
         for beta in (F(1,100),F(1,10),F(2)):
          c=2/(g*ell)
          rh=dyadic(a,1-1/(c*ell)); rl=dyadic(a+t,F(1))
          tau=min(rh-a,beta,a)/2; K=gamma+4
          bigD=K/c0+1; switch=(bigD/tau)**2+K/ell+A/ell+3
          require(0<theta<b<bj<bstar<ell,"low order")
          require(gamma<A*b/ell-F(1,2),"low margin")
          require(0<tau<min(rh-a,beta,a),"tolerance")
          require(1/(1-rh)<c*ell,"clock pressure")
          require(switch>A/ell and switch*tau**2>bigD**2,"switch/cap")
          require(min(switch*ell,c0*bigD**2)>gamma+F(5,2),"high margin")
          count["rational_parameter_packages"]+=1
          for r,eta in ((rh,tau),(rl,t)):
           gap=r-a-eta
           M0=1+ceil(max(F(1),(2+eta)/gap,2/r,6/(r*ell)**2))
           for M in (M0,M0+1,M0+10):
            q=(r*M).__floor__()
            require(1<q<M,"stage target floors")
            require((a+eta)*M+1+eta<q,"stage terminal budget")
            require(2/((r*ell)**2*M)<=F(1,3),"stage horizon scalar bound")
            count["rational_stage_startups"]+=1
    # Tests of the exact explicit logarithmic absorption cutoff.
    for d in (F(1,100),F(1,10),F(1,2),F(1),F(10)):
     y=max(F(1),2/d**2)
     require((d*y)**2/2>=y and y>=1,"log absorption cutoff")
     count["rational_log_absorptions"]+=1
    rows=[]
    for precision in (60,80):
     with localcontext() as ctx:
      ctx.prec=precision
      ell=D(2).ln(); lam=D(3).ln()/ell
      a=lam/2; g=1-a; p=1/lam; ds=p-D("0.5")
      h=lambda x: -x*x.ln()-(1-x)*(1-x).ln()
      bs=ell-h(p); kap=bs/ell; lip=(p/(1-p)).ln()
      for Ai in (11,12,20,40,100):
       A=D(Ai); delta=kap*A-D("0.5")
       for fs in ("0.1","0.5","0.9","0.99","0.999"):
        gamma=delta*D(fs); theta=(gamma+D("0.5"))*ell/A
        e=bs-theta; j=int((2*lip*ds/e).to_integral_value(rounding=ROUND_CEILING))
        alpha=1-1/D(j+2); pj=D("0.5")+ds*alpha**2
        bj=ell-h(pj); b=(theta+bj)/2
        bound=lip*ds*(1-alpha**2)
        require(0<bs-bj<=bound<2*lip*ds/D(j+2)<e,"entropy Lipschitz sample")
        require(0<theta<b<bj<bs<ell,"numeric entropy order")
        require(A*b/ell-D("0.5")>gamma,"prescribed rate sample")
        count["decimal_entropy_samples"]+=1
        if precision==80:
         rows.append({"A":Ai,"rate_fraction":fs,"j":j,
                      "gamma":str(gamma),"low_margin":str(A*b/ell-D("0.5")-gamma)})
    tex=(HERE/"audit.tex").read_text(encoding="utf-8")
    title=r"\section{Shaik's timeout tail, critical rate and drift clock}"
    sec=title+tex.split(title,1)[1].split(r"\section{",1)[0]
    mapped=sec.strip().replace(r"\section{",r"\subsection{",1).replace("shaik-","Shaik-")
    require((ROOT/"tex/chapters/01n_shaik_reverse_transport.tex").read_text(encoding="utf-8").strip().endswith(mapped),"full proof propagation")
    for lab in ("prop:shaik-prescribed-rate","eq:shaik-effective-barrier",
                "eq:shaik-prescribed-high","eq:shaik-explicit-startup",
                "eq:shaik-barrier-gap","eq:shaik-prescribed-profile"):
     require(tex.count(r"\label{"+lab+"}")==1,"unique label")
    require(r"\max(1,2/d^2)" in tex,"explicit absorption cutoff")
    claims=json.loads((HERE/"CLAIMS.json").read_text(encoding="utf-8"))
    nd=next(x for x in claims["claims"] if x["id"]=="ND-088")
    require(nd["canonical_claim_id"]=="CLM-COL-000281","claim identity")
    count["complete_written_propagation"]+=1
    reading=[{"name":n,"sha256":sha(SRC/n),"lines":len((SRC/n).read_text(encoding="utf-8").splitlines()),
              "read":"complete" if n in FULL else PARTIAL[n]} for n in (*FULL,*PARTIAL)]
    out={"status":"passed","counts":dict(count),"scope":"Exact rational tests of parameter algebra and startup formulas; 60/80-digit entropy samples are numerical diagnostics, not interval certificates or proofs of infinite claims. Complete analytic argument is in the cited manuscript.",
         "lean_started":False,"new_formal_theorems":0,"whole_natural_density_package_verified":False,
         "reading":reading,"entropy_samples":rows,
         "artifact_hashes":{n:sha(HERE/n) for n in ("audit.tex","CLAIMS.json","check_shaik_parameters.py","draw_shaik_parameters.py","shaik_parameter_rates.png")}}
    (HERE/"shaik_parameter_checks.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":"passed","counts":dict(count)},indent=2))
if __name__=="__main__": main()

