"""Exact finite ND112 route comparisons; not an analytic/package certificate."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from functools import lru_cache
import hashlib,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SRC=ROOT/"external_literature/shaik_2026_v324/source/FirstPassageLinearTransport-ef3410843bf58d69f771f5ba2c0571d54b54da59/lean/FirstPassageLinearTransport"
def req(b,msg):
    if not b:raise AssertionError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def step(n):return n//2 if n%2==0 else (3*n+1)//2
def qrank(r,m):return (r*m).numerator//(r*m).denominator
@lru_cache(None)
def good(n):
    m=n.bit_length()-1;y=n
    # W_(1/8): positive inequalities raised to power 16, without logarithms.
    for k in range(m+1):
        z=pow(y,16)*pow(2,16*k)
        if not pow(3,8*k)*pow(n,14)<=z<=pow(3,8*k)*pow(n,18):return False
        y=step(y)
    return True
def passage(n,q,m):
    y=n
    for j in range(m+1):
        if y<=2**q:return j,y
        y=step(y)
    return None
L,S=64,72
HI,LO=F(31,32),F(127,128)
def run(n,certified):
    M=n.bit_length()-1;records=[]
    if not good(n):return False,records,"initial"
    q=qrank(HI,M);j,x=passage(n,q,M)
    h=j;records.append((M,q,j,h,x))
    while True:
        if certified:
            if q>=L and not good(x):return False,records,"certificate"
            if q<=L:return True,records,"terminal"
        else:
            if q<=L:return True,records,"terminal"
            if q>S:
                if not good(x):return False,records,"certificate"
            elif x==2**q:return True,records,"halving"
        m=x.bit_length()-1
        req(m==q-1,"departure rank")
        nq=qrank(HI if m>=S else LO,m)
        req(0<nq<m and nq<q and m>=L,"stage domain")
        p=passage(x,nq,m)
        if p is None:
            req(not certified,"certified timeout")
            return False,records,"timeout"
        j,x=p;h+=j;q=nq;records.append((m,q,j,h,x))
def body(p,name):
    s=p.read_text(encoding="utf-8").split("def "+name,1)[1].split("/--",1)[0]
    return s[s.index("{n : ℕ |"):].strip()
def main():
    counts=Counter()
    names=["TimeoutEndpointNaturalDensity.lean","Alternates/AllPrefix/NaturalDensity.lean"]
    req(body(SRC/names[0],"timeoutEndpointWitnessGood")==body(SRC/names[1],"movingEndpointWitnessGood"),
        "literal witness definitions")
    counts["literal_source_definition_identity"]=1
    req(3**5<2**8,"a0<4/5")
    for ratio in (HI,LO):
        for m in range(64,1000):
            q=qrank(ratio,m)
            req(F(4,5)*m+F(1,8)*m+F(9,8)<=q,"terminal scalar envelope")
            req(1<2**q<2**m and F(m,2*2**q)<=F(1,3),"target/horizon")
            counts["rational_stage_samples"]+=1
    for M in range(80,85):
        for i in range(129):
            n=2**M+(i*2654435761*2**(M-32))%(2**M)+i
            okA,ra,whyA=run(n,True);okT,rt,whyT=run(n,False)
            req(not okA or okT,"good set inclusion")
            counts["actual_source_samples"]+=1
            if okA:
                req(ra==rt and whyT=="terminal","same certified trace")
                counts["identical_successful_traces"]+=1
                h=ra[-1][3];x=n;raw_n=n;raw_h=0;odd=0
                for k in range(h):
                    if x%2:
                        odd+=1;raw_n=3*raw_n+1;raw_h+=1
                    raw_n//=2;raw_h+=1;x=step(x)
                    req(x==raw_n,"ordinary expansion")
                req(raw_h==h+odd and x==ra[-1][4],"clock/endpoint")
                counts["actual_clock_transfers"]+=1
            if okT and not okA:counts["extra_timeout_successes"]+=1
            if not okT and whyT=="timeout":
                counts["low_timeout_cases"]+=1
                req(whyA=="certificate" and ra==rt[:len(ra)],
                    "timeout to first missing certificate prefix")
                req(L<rt[-1][1]<=ra[-1][1]<=S,
                    "timeout/certificate rank direction")
                req(not good(ra[-1][4]),"missing certificate not missing")
                counts["first_missing_certificate_maps"]+=1
    req(counts["identical_successful_traces"]>0,"vacuous successful traces")
    req(counts["first_missing_certificate_maps"]>0,"vacuous timeout maps")
    for q in range(L+1,S+1):
        nq=qrank(LO,q-1)
        req(passage(2**q,nq,q-1)==(q-nq,2**nq),"dyadic upper endpoint")
        req(not good(2**q),"power unexpectedly certified")
        counts["dyadic_upper_endpoint_checks"]+=1
    labels=["prop:shaik-timeout-forgetting","eq:shaik-timeout-envelope-inclusion",
        "eq:shaik-timeout-certificate-defect","cor:shaik-identical-endpoint-witness",
        "eq:shaik-literal-witness-equality"]
    tex=(HERE/"audit.tex").read_text(encoding="utf-8")
    chapter=(ROOT/"tex/chapters/01n_shaik_reverse_transport.tex").read_text(encoding="utf-8")
    for lab in labels:
        req("\\label{"+lab+"}" in tex and "\\label{"+lab.replace("shaik-","Shaik-")+"}" in chapter,
            "written propagation "+lab)
    counts["written_propagation"]=1
    out=dict(status="passed",counts=dict(counts),new_formal_theorems=0,lean_started=False,
        whole_natural_density_package_verified=False,
        exact_sample_scope="Actual shortcut paths, integer-power W_(1/8), HI=31/32, LO=127/128, L=64, S=72, M=80..84. Generic valid-stage comparison, not asymptotic moving-low parameter samples.",
        scope="General inclusion has a written induction; finite samples do not prove that induction or the analytic/source package.",
        source_definition_hashes={n:sha(SRC/n) for n in names},
        artifact_hashes={n:sha(HERE/n) for n in ["check_shaik_route_comparison.py","audit.tex","CLAIMS.json"]})
    (HERE/"shaik_route_comparison_checks.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2))
if __name__=="__main__":main()
