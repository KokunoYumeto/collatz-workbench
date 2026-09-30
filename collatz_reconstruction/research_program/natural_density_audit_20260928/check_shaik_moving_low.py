"""ND105-106: finite structural checks; real estimates are written proofs."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
from collections import Counter
import json,hashlib,importlib.util
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def req(b,m):
    if not b:raise AssertionError(m)
def main():
    c=Counter()
    # Abstract rational parameters test the exact stated startup, not log(3).
    for g in (F(1,5),F(3,16),F(1,4)):
      for K in (F(1,2),F(1),F(7)):
       for Ng in (1,13,57):
        ceil=lambda x:-(-x.numerator//x.denominator)
        L0=max(2,ceil(2*K/g),Ng+1,ceil(4/g)+1)
        for L in range(L0,L0+12):
         eta=g-K/L
         for q in (L,L+1,2*L,3*L):
          m=q-1
          req(g/2<=eta<g and m>=Ng and eta*m>=2,"finite uniform region")
          alpha=1-1/(eta*m)
          req(0<=alpha<=1 and (1-alpha)*eta*m==1,"exact one-bit reserve")
          c["rational_startup_and_one_bit"]+=1
    for L in range(2,90):
      for j in range(100):
       q=L+j
       req((q+1)**2<=9*L*(q-1)*(j+1)**2,"squared series weight inequality")
       c["integer_series_weights"]+=1
      for S in (L,L+1,L+20):
       actual=sum((F(q+1,2**q) for q in range(L,S+1)),F(0))
       req(actual==F(2*(L+2),2**L)-F(2*(S+3),2**(S+1)),"finite dyadic endpoint")
       for z in (F(1,2),F(3,4),F(7,8)):
        seq=sum((F(j+1)*z**j for j in range(S-L+1)),F(0))
        req(seq<=1/(1-z)**2,"rational series bound")
        c["rational_geometric_series"]+=1
       c["exact_dyadic_tails"]+=1
    diagnostics=[]
    with localcontext() as ctx:
      ctx.prec=65
      ell=D(2).ln();lam=D(3).ln()/ell;g=1-lam/2;u=g/lam
      B=lambda t:ell+(D("0.5")+t)*(D("0.5")+t).ln()+(D("0.5")-t)*(D("0.5")-t).ln()
      deriv=((D("0.5")+u)/(D("0.5")-u)).ln()
      for K in (D("0.5"),D(1),D(7)):
       for L in (100,200,1000,10000):
        eta=g-K/L;D0=K*deriv/lam;loss=B(u)-B(eta/lam)
        req(eta>0 and 0<loss<D0/L,"Decimal endpoint derivative diagnostic")
        diagnostics.append(dict(K0=str(K),L=L,actual_rate_loss=str(loss),upper=str(D0/L)))
        c["decimal_rate_diagnostics"]+=1
    tex=(HERE/"audit.tex").read_text(encoding="utf-8")
    labels=["prop:shaik-reflection-certificate","prop:shaik-moving-low-reserve",
            "eq:shaik-moving-low-reserve","eq:shaik-moving-low-finite-profile",
            "eq:shaik-moving-low-explicit-profile"]
    for lab in labels:req(tex.count("\\label{"+lab+"}")==1,"unique proof label")
    title=r"\section{Shaik's timeout tail, critical rate and drift clock}"
    sec=title+tex.split(title,1)[1].split(r"\section{",1)[0]
    mapped=sec.strip().replace(r"\section{",r"\subsection{",1).replace("shaik-","Shaik-")
    req((ROOT/"tex/chapters/01n_shaik_reverse_transport.tex").read_text(encoding="utf-8").strip().endswith(mapped),
        "whole cumulative argument propagation")
    claims=json.loads((HERE/"CLAIMS.json").read_text(encoding="utf-8"))["claims"]
    for n,cid in (("ND-105","CLM-COL-000298"),("ND-106","CLM-COL-000299")):
      req(next(x for x in claims if x["id"]==n)["canonical_claim_id"]==cid,"claim mapping")
    spec=importlib.util.spec_from_file_location("reflection_verify",HERE/"formal_shaik_reflection/verify_certificate.py")
    v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);v.main()
    vr=json.loads((HERE/"formal_shaik_reflection/verification.json").read_text(encoding="utf-8"))
    req(vr["status"]=="passed" and vr["named_theorems"]==31 and not vr["shaik_package_replayed"],"formal scope")
    c["complete_written_propagation"]+=1
    names=["audit.tex","CLAIMS.json","check_shaik_moving_low.py","draw_shaik_moving_low.py",
           "shaik_moving_low.png","formal_shaik_reflection/verification.json"]
    out=dict(status="passed",counts=dict(c),decimal_diagnostics=diagnostics,
        formal_named_statements=31,lean_launched_by_this_check=False,whole_natural_density_package_verified=False,
        scope="Exact rational startup/reserve checks, squared integer series factors and exact finite dyadic tails. Decimal entropy evaluations are diagnostics only. General finite reflection proof is separately kernel-checked; analytic density refinements are written proofs.",
        artifact_hashes={n:sha(HERE/n) for n in names})
    (HERE/"shaik_moving_low_checks.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(dict(status="passed",counts=dict(c)),indent=2))
if __name__=="__main__":main()
