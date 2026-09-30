"""Exact finite regressions for the written real/timed proof, not asymptotic certification."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import Counter
from hashlib import sha256
import json, re
import mpmath as mp
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
SOURCE=ROOT/"external_literature/mazur_2026_v2/source/Erdos1135"
counts=Counter()
def req(x,msg):
    if not x: raise AssertionError(msg)
def tv(p,q):
    return sum((abs(p.get(k,F(0))-q.get(k,F(0))) for k in p.keys()|q.keys()),F(0))/2
def push(p,f):
    out={}
    for k,v in p.items():out[f(k)]=out.get(f(k),F(0))+v
    return out
def comp(n,k):
    if k==1:yield (n,);return
    for j in range(n+1):
        for tail in comp(n-j,k-1):yield (j,)+tail
def totalizer():
    laws=[dict(enumerate(map(lambda x:F(x,4),v))) for v in comp(4,4)]
    r=lambda k:0 if k==3 else k # coordinate0=1, coordinate3=partial
    for p in laws:
        for q in laws:
            u=p[0]-q[0];v=p[3]-q[3]
            loss=2*(tv(p,q)-tv(push(p,r),push(q,r)))
            req(loss==abs(u)+abs(v)-abs(u+v),"exact loss")
            req(loss==(2*min(abs(u),abs(v)) if u*v<0 else 0),"sign cases")
            event=max(abs(sum((p[i]-q[i] for i in range(4) if mask>>i&1),F(0))) for mask in range(16))
            req(event==tv(p,q),"event/full-L1 convention")
            pp=push(p,r); recovered={k:pp.get(k,F(0)) for k in range(3)}
            recovered[3]=p[3];recovered[0]-=p[3]
            req(recovered==p,"recovery with failure mass")
            counts["exact_totalizer_law_pairs"]+=1
def overlaps():
    ambient=(1,3,5,7)
    sets=[{ambient[i] for i in range(4) if mask>>i&1} for mask in range(1,16)]
    for S,T in product(sets,repeat=2):
        for weighted in (False,True):
            w={n:1/F(n) if weighted else F(1) for n in S|T}
            mass=lambda A:sum((w[n] for n in A),F(0))
            p={n:w[n]/mass(S) for n in S};q={n:w[n]/mass(T) for n in T}
            exact=max(mass(S-T),mass(T-S))/max(mass(S),mass(T))
            req(tv(p,q)==exact==1-mass(S&T)/max(mass(S),mass(T)),"overlap")
            for f in (lambda n:n,lambda n:n%3,lambda n:1):
                req(tv(push(p,f),push(q,f))<=exact,"fibre contraction")
            counts["exact_weighted_overlap_pairs"]+=1
    # Rational intervals test both closed endpoints and the exclusive half-open shells.
    for aa in range(2,20):
        for ba in range(aa+4,aa+13):
            a=F(aa,2);b=F(ba,2)
            for shift in (F(0),F(1,3),F(5,4)):
                c=a+shift;d=b+2*shift
                universe=range(1,int(d)+2,2)
                S={n for n in universe if a<=n<=b};T={n for n in universe if c<=n<=d}
                req(S-T=={n for n in universe if a<=n<c},"lower exclusive shell")
                req(T-S=={n for n in universe if b<n<=d},"upper exclusive shell")
                req(abs(F(len(S))-(b-a)/2)<=1,"closed count discrepancy")
                counts["exact_endpoint_shell_cases"]+=1
def dynamics():
    def syr(n):
        k=3*n+1
        while k%2==0:k//=2
        return k
    def tau(n,B,limit=300):
        for j in range(limit+1):
            if n<=B:return j,n
            n=syr(n)
        raise AssertionError("bounded sample failed to finish; not classify as nonpassage")
    for n in range(1,301,2):
        for B,q in product((1,3,7,20),(1,4,11,31)):
            t,r=tau(n,q);s,_=tau(n,B);u,_=tau(r,B)
            for K,N in product((0,1,3,12),(0,2,5,20)):
                req((u>K)<=(s>K),"first deterministic inequality")
                req((s>K+N)<=((u>K)+(t>N)),"time concatenation")
                counts["actual_timed_implications"]+=1
            for theta in (F(0),F(1,4),F(3,4)):
                req(tau(n,F(q)+theta)==(t,r),"exact real/floor dynamics")
                counts["actual_floor_hit_equalities"]+=1
    # Abstract dynamics, including cycles that avoid the threshold forever:
    # this checks totalizer branches that finite Collatz samples cannot decide.
    states=(1,3,5,7)
    for images in product(states,repeat=4):
        mapping=dict(zip(states,images))
        def first(n,B):
            seen=set();j=0
            while n not in seen:
                if n<=B:return j,n
                seen.add(n);n=mapping[n];j+=1
            return None,1
        for n,B,q in product(states,(1,3,5),(1,3,5)):
            t,r=first(n,q);s,_=first(n,B);u,_=first(r,B)
            for K,N in product((0,1,4),(0,2)):
                bad=lambda t,k:t is None or t>k
                req(bad(u,K)<=bad(s,K),"abstract totalizer inequality")
                req(bad(s,K+N)<=(bad(u,K)+bad(t,N)),"abstract timed inequality")
                counts["finite_system_timed_implications"]+=1
            if t is None:counts["abstract_nonpassage_cases"]+=1
    for n in range(1,501):
        u=n;v=0
        while u%2==0:u//=2;v+=1
        t=0;S=0;x=u
        while x>1:
            z=3*x+1;k=0
            while z%2==0:z//=2;k+=1
            S+=k;t+=1;x=z
        x=n;raw=0
        while x>1:
            x=x//2 if x%2==0 else 3*x+1
            raw+=1
        req(raw==v+t+S,"raw expansion length")
        req(2**S<=4**t*u,"valuation telescoping integer inequality")
        counts["actual_raw_clock_paths"]+=1
    for X in range(1,100):
        for B in (1,3,7):
            # Arbitrary finite odd event, not a theorem about asymptotic bad sets.
            A={u for u in range(1,X+1,2) if u%(B+2)==1 and u>1}
            direct=sum(next((n//2**v for v in range(n.bit_length()) if (n//2**v)%2),0) in A for n in range(1,X+1))
            lifted=sum(sum(u<=F(X,2**v) for u in A) for v in range(X.bit_length()+1))
            req(direct==lifted,"odd-part count identity")
            counts["exact_odd_part_count_identities"]+=1
def clocks():
    alpha=F(1001,1000);b=1/F("17.232")
    req(F(1,16)>b and 0<F(1,2)-b<1,"rate ordering")
    req(1/(10*(alpha-1))==100,"odd clock")
    req(3*100+1==301,"raw clock")
    req(F(501501,5000)-100==F(1501,5000),"original odd margin")
    req(F(1509503,5000)-301==F(4503,5000),"original raw margin")
    counts["exact_rate_clock_guards"]=5
    for J in range(41):
        s=sum((alpha**j for j in range(J)),F(0))
        req(s==(alpha**J-1)/(alpha-1),"finite clock geometric sum")
        # final source y=X^(1/alpha): complete schedule algebra before log_n conversion
        req(1/(10*alpha**2*(alpha-1))+1/(10*alpha**2)==1/(10*alpha*(alpha-1)),"top passage coefficient")
        counts["exact_geometric_clock_identities"]+=1
def diagnostics():
    mp.mp.dps=60
    alpha=mp.mpf(1001)/1000;b=1/mp.mpf("17.232");a=mp.mpf(".5")-b
    h=mp.log(alpha);r=alpha**(-b)
    rows=[]
    for L in (mp.mpf(10),mp.mpf(10)**5,mp.mpf(10)**20):
        upper=1/(1-r)+a*h/(1+mp.log(L))*r/(1-r)**2
        partial=mp.fsum(r**j*(1+j*h/(1+mp.log(L)))**a for j in range(2000))
        req(partial<=upper,"numerical geometric diagnostic")
        rows.append({"L":str(L),"first_2000_terms_ratio":str(partial),"proved_upper_envelope":str(upper)})
    counts["noncertifying_geometric_diagnostics"]=len(rows)
    return {"precision":60,"rows":rows,"infinite_ratio_limit":str(1/(1-r))}
def propagation():
    tex=(HERE/"audit.tex").read_text(encoding="utf-8")
    sec=tex.split(r"\section{Real thresholds and the timed density conclusion}",1)[1].split(r"\section{",1)[0]
    sec=r"\section{Real thresholds and the timed density conclusion}"+sec
    mapped=sec.strip().replace("mazur-","Mazur-").replace(r"\section{",r"\subsection{",1).replace(r"\cite{Tao7}",r"\cite{Tao2026v7}")
    req(mapped in (ROOT/"tex/chapters/01m_mazur_terminal_rates.tex").read_text(encoding="utf-8"),"full proof propagation")
    labels=re.findall(r"\\label\{([^}]+)\}",tex)
    req(len(labels)==len(set(labels)),"unique labels")
    req(set(re.findall(r"\\(?:ref|eqref)\{([^}]+)\}",tex))<=set(labels),"resolved references")
    claims=json.loads((HERE/"CLAIMS.json").read_text(encoding="utf-8"))["claims"]
    for i,label in enumerate(("prop:mazur-totalizer-exact","prop:mazur-source-overlap","prop:mazur-real-overlap","thm:mazur-real-passage","prop:mazur-critical-iteration","thm:mazur-critical-density"),69):
        req(any(c["id"]==f"ND-{i:03d}" and c["tex_label"]==label for c in claims),"claim locator")
    req("uniformly in the trace length" in sec and "including nonpassage" in sec,"uniformity/no-hit retained")
    counts["complete_written_propagation"]=1
def main():
    propagation();totalizer();overlaps();dynamics();clocks()
    diag=diagnostics()
    sources=["ND/Probability/PassTotalizer.lean","ND/Probability/UniformFloorPerturbation.lean",
      "ND/Discrepancy/A5ReferenceTotalizedSourceRate.lean","ND/Discrepancy/A5ReferenceRealFloorPass.lean",
      "ND/Discrepancy/A5ReferenceRealLogBlock.lean","ND/Discrepancy/A5ReferenceSection3GeometricBudget.lean",
      "ND/LogTime/Clock.lean","Tao/Section3/TimeBudget.lean","Tao/Section3/AmbientPartialTrace.lean"]
    out={"status":"passed","counts":dict(counts),"diagnostics":diag,"lean_started":False,"public_mutations":False,
      "scope":"Finite exact measures, map loss, endpoints, actual and abstract dynamical implications, raw path lengths, and geometric algebra. Abstract finite cycles test nonpassage branches; no infinite Collatz claim is decided by a simulation. Critical-rate diagnostics are noncertifying. Analytic conclusions rest on written proofs.",
      "source_package_commit":"ca3dd0d63920411213403092aecc6946619eb082",
      "source_hashes":{p:sha256((SOURCE/p).read_bytes()).hexdigest() for p in sources},
      "artifact_hashes":{p:sha256((HERE/p).read_bytes()).hexdigest() for p in ("audit.tex","CLAIMS.json","check_mazur_real_timed.py")}}
    (HERE/"mazur_real_timed_checks.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2))
if __name__=="__main__":main()
