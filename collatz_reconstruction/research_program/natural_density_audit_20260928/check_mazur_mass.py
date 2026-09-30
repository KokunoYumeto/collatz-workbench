"""Finite regressions for the written raw-mass and physical-interior proof.
Exact algebra and rational enclosures are separated from numerical diagnostics.
No finite sample certifies an asymptotic theorem or a Lean endpoint.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from hashlib import sha256
from math import ceil, floor, comb
import json
import re
import sympy as sp
import mpmath as mp
from check_mazur_profile import log_bounds

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
SOURCE=ROOT/"external_literature/mazur_2026_v2/source/Erdos1135"
counts=Counter()
mp.mp.dps=65

def require(test,message):
    if not test: raise AssertionError(message)

def log_interval(x):
    if x>=1:return log_bounds(x,65)
    lo,hi=log_bounds(1/x,65)
    return -hi,-lo

def exact_checks():
    t=sp.symbols("t",real=True)
    rate=(1+t)*sp.log(1+t)-(2+t)*sp.log(1+t/2)
    require(sp.simplify(sp.diff(rate,t,2)-1/((1+t)*(2+t)))==0,"rate second derivative")
    require(sp.simplify(sp.diff(rate,t,3)+(3+2*t)/((1+t)**2*(2+t)**2))==0,"rate third derivative")
    k,e=sp.symbols("k e")
    require(sp.expand(k*k-(k-e)**2-2*k*e+e*e)==0,"strict signed rounding")
    n=sp.symbols("n",positive=True)
    # Square of the prefactor equality after factorial cancellation.
    require(sp.simplify((n/(2*n+n*t))**2*(2*n+n*t)/(2*sp.pi*n*(n+n*t))
                       -1/(4*sp.pi*n*(1+t/2)*(1+t)))==0,"retained n/s prefactor")
    counts["symbolic_rate_prefactor_rounding"]=4
    for j in range(-50,51):
        x=F(j,100)
        lo1,hi1=log_interval(1+x);lo2,hi2=log_interval(1+x/2)
        lo=(1+x)*lo1-(2+x)*hi2-x*x/4
        hi=(1+x)*hi1-(2+x)*lo2-x*x/4
        bound=F(16,27)*abs(x)**3
        require(lo>=-bound and hi<=bound,"directed Taylor remainder sample")
        counts["directed_rate_remainders"]+=1
    lo2,hi2=log_bounds(F(2),12);lod,hid=log_bounds(F(4,3),6)
    require(F(6931,10000)<lo2<hi2<F(6932,10000),"log2 source interval")
    require(F(2876,10000)<lod<hid<F(2877,10000),"drift source interval")
    lower=10*F(6931,10000)*(F(1,1000)/F(2877,10000)-F(1,100000))
    upper=10*F(6932,10000)*(F(1001,1000)**3-1)/F(2876,10000)
    require(lower>F(1,43) and upper<F(1,13),"uniform center room")
    require((F(4,25)+F(6932,10000))/F(2876,10000)<3,"directional margin")
    counts["certified_physical_log_constants"]=4

def rational_transport():
    # These rational parameters test the exact map and endpoints, not log2(3).
    for delta in (F(5,12),F(4,9)):
        logtwo=F(7,10);drift=delta*logtwo
        for width in (F(71),F(143,2),F(142)):
            R=ceil(width)-1
            for xi in (F(400),F(400)+F(1,3),F(1000)):
                A=delta*xi;m0=25
                for tau in (-F(4,25)*width,F(0),F(4,25)*width):
                    require(abs(tau)/drift+(width+1)/delta<=3*width,"sample margin")
                    for beta in (logtwo*F(1001,1000),logtwo*F(3,2)):
                        t0=xi+m0+tau/drift
                        union=[]
                        for nu in range(1,ceil((A+R+2)/delta)+2):
                            dis=floor(A-delta*nu)+1
                            active=(abs(dis)<width or abs(dis+1)<width)
                            interval=(A-R)/delta<nu<=(A+R+2)/delta
                            require(active==interval,"exact union interval")
                            if active:
                                time=nu+m0
                                require(t0-3*width<=time<=t0+beta/drift+3*width,"carrier")
                                require(time-m0==nu and time>m0,"inverse without clipped subtraction")
                                union.append(nu)
                        counts["rational_support_transport"]+=len(union)
                        counts["rational_transport_cases"]+=1

def atom(n,k):
    return mp.mpf(comb(2*n+k-1,n-1))/mp.power(2,2*n+k)

def remainder(n):
    return mp.loggamma(n+1)-(mp.mpf(n)+mp.mpf(".5"))*mp.log(n)+n-mp.log(2*mp.pi)/2

def numerical_checks():
    # High-precision diagnostics; not interval-certified analytic proofs.
    tol=mp.mpf("1e-48")
    for n in (1,2,3,5,10,30,100):
        for k in range(ceil(-n/2),floor(n/2)+1):
            t=mp.mpf(k)/n
            I=(1+t)*mp.log(1+t)-(2+t)*mp.log(1+t/2)
            r=remainder(2*n+k)-remainder(n)-remainder(n+k)
            model=mp.exp(-n*I+r)/(2*mp.sqrt(mp.pi*n)*mp.sqrt((1+t/2)*(1+t)))
            p=atom(n,k)
            require(abs(p/model-1)<tol,"numerical exact atom identity")
            G=mp.exp(-mp.mpf(k)**2/(4*n))/(2*mp.sqrt(mp.pi*n))
            E=mp.mpf(4)*abs(k)/(3*n)+mp.mpf(16)*abs(k)**3/(27*n*n)+mp.mpf(1)/(4*n)
            require(abs(mp.log(p/G))<=E+tol,"numerical log error")
            counts["numerical_atom_identities_and_bounds"]+=1
    delta=2-mp.log(3,2)
    for xi in (mp.mpf(200),mp.mpf("400.3"),mp.mpf(800)):
        for W in (mp.mpf(5),mp.mpf("14.5"),mp.mpf(30)):
            R=int(mp.ceil(W)-1);A=delta*xi
            a=xi-R/delta;b=xi+(R+1)/delta
            ns=list(range(int(mp.floor(a))+1,int(mp.floor(b))+1));l=min(ns)
            require(W<=mp.mpf(l)/2,"finite mass domain")
            G=lambda u:mp.exp(-delta**2*(u-xi)**2/(4*u))/(2*mp.sqrt(mp.pi*u))
            eps=11*W/(6*l)+16*W**3/(27*l*l)+mp.mpf(1)/(2*l)
            vals=[]
            for nu in ns:
                k=int(mp.floor(A-delta*nu)+1)
                p=atom(nu,k);vals.append(p)
                ee=1-mp.frac(A-delta*nu)
                exact=mp.log(p/G(nu))
                loglocal=mp.log(p/(mp.exp(-mp.mpf(k)**2/(4*nu))/(2*mp.sqrt(mp.pi*nu))))
                require(abs(exact-loglocal+(2*k*ee-ee**2)/(4*nu))<tol,"rounding sign")
                require(abs(exact)<=eps+tol,"rounded envelope")
            peak=mp.sqrt(xi**2+delta**-4)-delta**-2
            M=G(peak);um=R/(delta*mp.sqrt(a));up=(R+1)/(delta*mp.sqrt(b))
            T=2/(delta**2*mp.sqrt(mp.pi))*(mp.exp(-delta**2*um**2/4)/um+mp.exp(-delta**2*up**2/4)/up)
            Q=2*M+T
            ZG=sum(G(nu) for nu in ns);Z=sum(vals)
            require(abs(ZG-1/delta)<=Q+tol,"finite Gaussian quadrature")
            require(abs(Z-1/delta)<=(mp.exp(eps)-1)*(1/delta+Q)+Q+tol,"finite original mass")
            variation=G(ns[0])+G(ns[-1])+sum(abs(G(n+1)-G(n)) for n in ns[:-1])
            require(variation<=2*M+tol,"smooth sampled variation")
            # Numerically integrate in transformed v coordinates with finite tails handled by mp.
            density=lambda v:mp.exp(-delta**2*v*v/4)/(2*mp.sqrt(mp.pi))*(1+v/mp.sqrt(v*v+4*xi))
            integral=mp.quad(density,[-mp.inf,0,mp.inf])
            tails=mp.quad(density,[-mp.inf,-um])+mp.quad(density,[up,mp.inf])
            require(abs(integral-1/delta)<tol and tails<=T+tol,"transformed integral/tails")
            counts["numerical_finite_mass_and_tails"]+=1
            counts["numerical_rounded_atoms"]+=len(ns)

def propagation_checks():
    audit=(HERE/"audit.tex").read_text(encoding="utf-8")
    start=audit.index(r"\section{Raw mass, Gaussian coordinates, and physical interior profiles}")
    end=audit.index("\n"+chr(92)+"section{",start+10)
    sec=audit[start:end].strip()
    mapped=sec.replace("mazur-","Mazur-").replace(r"\section{",r"\subsection{",1)
    mapped=mapped.replace(r"Lemma~\ref{lem:envelope-mass}",r"the Gaussian-envelope argument in Section~\ref{subsec:Allikvere-phase-average}")
    mapped=mapped.replace(r"Lemma~\ref{lem:abel-rotation}",r"the Abel estimate in Section~\ref{subsec:Allikvere-phase-average}")
    require(mapped in (ROOT/"tex/chapters/01m_mazur_terminal_rates.tex").read_text(encoding="utf-8"),"full mass proof propagation")
    labels=re.findall(r"\\label\{([^}]+)\}",audit)
    require(len(labels)==len(set(labels)),"duplicate label")
    require(set(re.findall(r"\\(?:ref|eqref)\{([^}]+)\}",audit))<=set(labels),"unresolved local label")
    chapters=[ROOT/"tex/chapters"/name for name in ("01l_allikvere_uniform_fibres.tex","01m_mazur_terminal_rates.tex","99_source_register.tex")]
    combined="\n".join(p.read_text(encoding="utf-8") for p in chapters)
    for key in re.findall(r"\\(?:ref|eqref)\{([^}]+)\}",mapped):
        require(r"\label{"+key+"}" in combined,"unresolved cumulative new reference "+key)
    require(r"\bibitem{Robbins1955}" in combined,"Robbins attribution")
    require(r"(\log N)^{1/2-1/17.232}" in sec,"sharper logarithmic power")
    counts["complete_written_propagation"]=1

def main():
    propagation_checks();exact_checks();rational_transport();numerical_checks()
    sources=["ND/Band/A6PhysicalRate.lean","ND/Band/A6PhysicalInteriorRate.lean",
             "ND/Band/A5Physical.lean","ND/Discrepancy/A5TwoProfilePhysicalA6.lean",
             "Tao/Section5/Schedule.lean","Tao/Section5/PassSchedule.lean",
             "Tao/Probability/LogWindowEndpoints.lean"]
    report={"status":"passed","counts":dict(counts),"lean_started":False,
        "scope":"Exact symbolic/rational finite regressions and separately labelled 65-digit numerical diagnostics. Complete written proofs establish the infinite estimates using Robbins, Rhin and discrepancy inputs; neither these samples nor source-file presence is a Lean replay.",
        "source_package_commit":"ca3dd0d63920411213403092aecc6946619eb082",
        "source_hashes":{p:sha256((SOURCE/p).read_bytes()).hexdigest() for p in sources},
        "robbins_sha256":sha256((ROOT/"external_literature/robbins_1955/paper.pdf").read_bytes()).hexdigest(),
        "artifact_hashes":{p:sha256((HERE/p).read_bytes()).hexdigest() for p in ("audit.tex","CLAIMS.json","check_mazur_mass.py")},
        "public_mutations":False}
    (HERE/"mazur_mass_checks.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2))

if __name__=="__main__":main()
