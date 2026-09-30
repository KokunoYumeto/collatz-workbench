"""Finite checks for genuine-passage assembly; not analytic certification."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from hashlib import sha256
from itertools import product
import json, re
import mpmath as mp

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
SOURCE=ROOT/"external_literature/mazur_2026_v2/source/Erdos1135"
counts=Counter()
mp.mp.dps=70

def req(p,msg):
    if not p: raise AssertionError(msg)

def ceil(q): return -((-q.numerator)//q.denominator)
def odds(a,b): return [n for n in range(max(1,ceil(a)),ceil(b)) if n%2]
def syr(n):
    q=3*n+1
    while q%2==0:q//=2
    return q
def hit(n,B,max_steps=200):
    for k in range(max_steps+1):
        if n<=B:return k,n
        n=syr(n)
    return None
def comp(s,n):
    if n==1:
        if s>=1:yield (s,)
        return
    for a in range(1,s-n+2):
        for rest in comp(s-a,n-1):yield (a,)+rest
def offset(a):
    c=0;s=0
    for i,v in enumerate(a):
        c+=3**(len(a)-1-i)*2**s
        s+=v
    return c,s

def rational_guards():
    lo=F(2876,10000);hi=F(2877,10000);alpha=F(1001,1000)
    req(F(340,100000)<F(1,1000)/hi-F(1,100000),"lower time")
    req((alpha**3-1)/lo<F(105,10000),"upper time")
    req(F(105,10000)*F(11,10)==F(231,20000),"offset power")
    req(F(999,1000)-F(231,20000)==F(19749,20000),"ratio power")
    req(F(19749,20000)-F(9,10)==F(1749,20000),"boundary gap")
    req(F(1,16)>1/F("17.232"),"half width beats phase")
    counts["exact_scale_guards"]=6

def shell_and_record_checks():
    B=10;h=2;J=(3,4,5)
    endpoints=[M for M in range(11,160,2) if (hit(M,B) or (-1,))[0]==h]
    records=[]
    for t in J:
        nu=t-h
        for s in range(nu,2*nu+3):
            for a in comp(s,nu):
                c,l=offset(a)
                for M in endpoints:
                    numerator=2**l*M-c
                    if numerator>0 and numerator%3**nu==0:
                        N=numerator//3**nu
                        req(N%2==1,"odd inverse")
                        x=N
                        observed=[]
                        for _ in a:
                            q=3*x+1;v=0
                            while q%2==0:q//=2;v+=1
                            observed.append(v);x=q
                        req(tuple(observed)==a and x==M,"word inverse")
                        records.append((N,F(2**l*M,3**nu),F(c,2**l*M)))
    req(len({a[0] for a in records})==len(records),"cross-time injectivity")
    req(records,"nonempty records")
    counts["actual_affine_records"]=len(records)
    rho=max(x[2] for x in records);r=1-rho
    lower_cases=upper_cases=0
    bands=[(z,U) for z in (F(21),F(63,2),F(77),F(129,2)) for U in (z+F(57),z*3)]
    for n,n0,al in records[::max(1,len(records)//8)]:
        if n>5:
            mid=(n+n0)/2
            bands.extend(((mid,mid+60),(max(F(1),F(n-60)),mid)))
    for z,U in bands:
            band=odds(z,U);D=len(band);H=sum((1/F(n) for n in band),F(0))
            lower=set(odds(z*r,z));upper=set(odds(U*r,U));shell=lower|upper
            UH=UF=IH=IF=F(0)
            for n,n0,al in records:
                P=int(z<=n<U);Q=int(z<n0<U)
                UH+=F(P,n)/H;UF+=F(P,D)
                IH+=F(Q)/n0/H;IF+=F(Q,D)
                if Q and not P:
                    req(n in lower,"nominal-only lower shell");lower_cases+=1
                if P and not Q:
                    req(n in upper,"physical-only upper shell");upper_cases+=1
            hminus=sum((1/F(n) for n in lower),F(0))/H
            hboth=sum((1/F(n) for n in shell),F(0))/H
            req(abs(UH-IH)<=rho*UH+hboth,"harmonic signed support bound")
            req(abs(UF-IF)<=F(len(shell),D),"flat signed support bound")
            req(IH<=UH+hminus and IF<=UF+F(len(lower),D),"one-sided cap")
            req(UH<=1 and UF<=1,"actual union mass")
            for x in (z,U):
                req(len(odds(x*r,x))<x*(1-r)/2+1,"strict shell count")
                counts["exact_shell_counts"]+=1
            counts["actual_boundary_comparisons"]+=1
    req(lower_cases and upper_cases,"both support directions exercised")
    counts["actual_lower_mismatches"]=lower_cases
    counts["actual_upper_mismatches"]=upper_cases

def test_maps():
    # A finite actual-first-passage carrier; arbitrary finite depth checks the
    # algebra. This small example does not satisfy the asymptotic B schedule.
    endpoints=[M for M in range(11,220,2) if (hit(M,10) or (-1,))[0]==2]
    for nu in (2,3,4):
        modulus=3**nu
        for ell in range(nu,3*nu+1):
            z=F(13);U=F(103);band=odds(z,U)
            D=len(band);H=sum((1/F(n) for n in band),F(0))
            S=[M for M in endpoints if z<F(2**ell*M,3**nu)<U]
            cH=[sum((F(modulus,M)/H for M in S if M%modulus==x),F(0)) for x in range(modulus)]
            cF=[sum((F(2**ell,D) for M in S if M%modulus==x),F(0)) for x in range(modulus)]
            native=max([sum((F(modulus,M) for M in S if M%modulus==x),F(0)) for x in range(modulus)])
            req(max(cH)<=native/H and max(cF)<=native*U/D,"exact coefficient-to-cap algebra")
            counts["exact_assembled_caps"]+=1
            for m in range(1,nu):
                for x in range(3**m):
                    aH=sum((cH[v] for v in range(x,modulus,3**m)),F(0))/3**(nu-m)
                    aF=sum((cF[v] for v in range(x,modulus,3**m)),F(0))/3**(nu-m)
                    eH=sum((F(3**m,M)/H for M in S if M%3**m==x),F(0))
                    eF=sum((F(3**m,M)*F(2**ell*M,3**nu)/D for M in S if M%3**m==x),F(0))
                    req(aH==eH and aF==eF,"fibre average with collisions")
                    counts["exact_fibre_averages"]+=1

def assembly():
    for gamma in (F(0),F(1,7),F(2,5)):
        for Y in (F(0),F(1,3),F(5,4)):
            for e in (F(0),F(1,5)):
                Z=(Y+e)/(1-gamma)
                req(Z-Y==(gamma*Y+e)/(1-gamma),"sharp absorption witness")
                counts["exact_absorption_witnesses"]+=1
    for w in ((F(1,4),F(1,2)),(F(1,3),F(2,3)),(F(0),F(0))):
        p=1-sum(w)
        for f in product((F(0),F(1,3),F(1)),repeat=2):
            for Z in (F(0),F(1,4),F(1),F(3)):
                for t in (F(0),p/2,p):
                    whole=sum((a*b for a,b in zip(w,f)),F(0))+t
                    rhs=sum((a*abs(b-Z) for a,b in zip(w,f)),F(0))+p*max(Z,abs(1-Z))
                    req(abs(whole-Z)<=rhs,"exact weighted mixture incl top")
                    counts["exact_whole_source_mixtures"]+=1
    # Exhaust every event in a four-point space, the last point nonpassage.
    laws=[]
    for a in range(5):
        for b in range(5-a):
            for c in range(5-a-b):
                laws.append(tuple(F(k,4) for k in (a,b,c,4-a-b-c)))
    for mu in laws:
        for nu in laws:
            full=max(abs(sum((mu[i]-nu[i] for i in range(4) if mask>>i&1),F(0))) for mask in range(16))
            finite=max(abs(sum((mu[i]-nu[i] for i in range(3) if mask>>i&1),F(0))) for mask in range(8))
            req(full==finite,"completion has identical event supremum")
            for f in ((-3,1,0,4),(1,1,1,1)):
                req(abs(sum((F(f[i])*(mu[i]-nu[i]) for i in range(4)),F(0)))<=F(max(f)-min(f))*full,"oscillation inequality")
            counts["exact_completed_law_pairs"]+=1

def diagnostics():
    rows=[]
    for Li in (10**k for k in (4,5,6)):
        L=mp.mpf(Li)
        eps=mp.exp(-mp.mpf("0.9")*L);z=mp.exp(mp.mpf("1.001")*L)
        by=F(1001,1000000)*Li
        beta_r=by/(by.numerator//by.denominator)
        beta=mp.mpf(beta_r.numerator)/beta_r.denominator;U=z*mp.exp(beta)
        # Continuous denominators used only for limiting diagnostics; actual
        # discrepancy is controlled in the written proof, not erased there.
        H=beta/2;D=(U-z)/2
        factor=-mp.expm1(-eps)/eps
        rows.append({"L":str(L),"boundary_H_ratio":str((1+mp.exp(eps)*(1/z+1/U)/eps)/H),
                     "boundary_F_ratio":str(((z+U)*factor/2+2/eps)/D),
                     "cap_H":str(2/H),"cap_F":str(2*U/D)})
        counts["numerical_limit_diagnostics"]+=1
    return {"precision":70,"continuous_denominator_diagnostics_only":rows,
            "flat_cap_limit":str(4*mp.e/(mp.e-1))}

def propagation():
    a=(HERE/"audit.tex").read_text(encoding="utf-8")
    start=a.index(r"\section{From reference profiles to genuine passage laws}")
    end=a.index("\n"+chr(92)+"section{",start+10)
    sec=a[start:end].strip()
    mapped=sec.replace("mazur-","Mazur-").replace(r"\section{",r"\subsection{",1)
    mapped=mapped.replace(r"\cite{Tao7}",r"\cite{Tao2026v7}")
    req(mapped in (ROOT/"tex/chapters/01m_mazur_terminal_rates.tex").read_text(encoding="utf-8"),"whole proof propagation")
    labels=re.findall(r"\\label\{([^}]+)\}",a)
    req(len(labels)==len(set(labels)),"unique labels")
    req(set(re.findall(r"\\(?:ref|eqref)\{([^}]+)\}",a))<=set(labels),"resolved labels")
    req(r"Be^{-L^{7/10}}" in sec,"literal lost window exponent")
    req(r"\newtheorem{theorem}[proposition]{Theorem}" in a,"declared theorem environment")
    claims=json.loads((HERE/"CLAIMS.json").read_text(encoding="utf-8"))["claims"]
    ids={c["tex_label"]:c["id"] for c in claims if "tex_label" in c}
    expected={"prop:mazur-genuine-caps":("cor:fixed-total","cor:mazur-two-tails"),
              "thm:mazur-genuine-rate":("cor:mazur-band-fullgood","prop:mazur-genuine-coverage"),
              "cor:mazur-genuine-source":("cor:mazur-band-fullgood",)}
    for label,deps in expected.items():
        claim=next(c for c in claims if c.get("tex_label")==label)
        req({ids[d] for d in deps}<=set(claim["dependencies"]),"dependency locator alignment")
    counts["complete_written_propagation"]=1

def main():
    propagation();rational_guards();shell_and_record_checks();test_maps();assembly()
    diag=diagnostics()
    sources=["ND/Band/A5ExactAffineCorrection.lean","ND/Band/A5TerminalBoundaryShell.lean",
      "ND/Band/A5FixedCellTerminalDescent.lean","ND/Band/A5SourceMixture.lean",
      "ND/Band/A5ReferenceFixedTimeAbsorption.lean",
      "ND/Discrepancy/A5ReferenceGenuineBandRate.lean",
      "ND/Discrepancy/A5ReferenceGenuineSourceRate.lean"]
    out={"status":"passed","counts":dict(counts),"diagnostics":diag,
      "lean_started":False,"public_mutations":False,
      "scope":"Exact finite arithmetic, original affine records, fibre averages, mixture/completion identities, and separately labelled numerical diagnostics. The written proofs, not finite tests, establish the analytic rates. No Lean replay.",
      "source_package_commit":"ca3dd0d63920411213403092aecc6946619eb082",
      "source_hashes":{p:sha256((SOURCE/p).read_bytes()).hexdigest() for p in sources},
      "artifact_hashes":{p:sha256((HERE/p).read_bytes()).hexdigest() for p in ("audit.tex","CLAIMS.json","check_mazur_genuine.py")}}
    (HERE/"mazur_genuine_checks.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2))
if __name__=="__main__":main()
