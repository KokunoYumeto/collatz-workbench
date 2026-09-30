"""Exact finite regressions for exterior weights and common-profile assembly.
No sample certifies the asymptotic bounds. See the complete written proofs.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter, defaultdict
from hashlib import sha256
from math import comb
import json, re
import sympy as sp
import mpmath as mp

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
SOURCE=ROOT/"external_literature/mazur_2026_v2/source/Erdos1135"
counts=Counter()
mp.mp.dps=70

def require(test,msg):
    if not test: raise AssertionError(msg)

def tail(n,k):
    """Exact Pr[sum of n positive Geom(2) >= k]."""
    if k<=n:return F(1)
    return F(sum(comb(k-1,j) for j in range(n)),2**(k-1))

def pmass(n,s):
    return F(comb(s-1,n-1),2**s) if s>=n>=1 else F(0)

def terminal_tail(k):
    require(k>=1,"terminal tail domain")
    return F(k+3,2**k)

def weighted_events(h,u,v):
    """Integers u,v; strict upper/lower endpoints; exact infinite masses."""
    K=2*h+u+1
    upper=tail(h,K)+tail(h+1,K+1)
    k=h-1
    lower=2*sum((pmass(k,s) for s in range(k,2*k-v)),F(0))
    lower_only=sum((pmass(k,s)*(2-terminal_tail(K-s))
                    for s in range(k,min(2*k-v,K-1))),F(0))
    return upper,lower,upper+lower_only

def symbolic_checks():
    y=sp.symbols("y",positive=True)
    a=sp.symbols("a",positive=True)
    z=sp.symbols("z",positive=True)
    g=1/(y*(2-y))
    # Weighted derivative of the uncentered series y/(2-y), then y^-2.
    wg=(y/(2-y)+y*sp.diff(y/(2-y),y)/2)/y**2
    require(sp.factor(wg-g*(1+1/(2-y)))==0,"exact weighted MGF")
    opt=2*(1+a)/(2+a)
    require(sp.simplify((1+1/(2-y)).subs(y,opt)-(2+a/2))==0,"upper factor")
    require(sp.simplify((y*sp.diff(g,y)/g-a).subs(y,opt))==0,"rate stationarity")
    # Geometric tail derivative: sum_{r>=k} (1+r/2)z^r.
    k=sp.symbols("k",integer=True,positive=True)
    t=z**k/(1-z)
    require(sp.simplify((t+z*sp.diff(t,z)/2).subs(z,sp.Rational(1,2))
                        -(k+3)*2**(-k))==0,"terminal weighted tail")
    counts["symbolic_mgf_and_terminal_series"]=4
    require(F(1,6)-F(34999,200000)==-F(4997,600000),"high exponent")
    require(F(16,1)/(F(6932,10000)**3)>48,"A_half>48")
    require(F(16)*100000/F(625*40)==64,"leading exponent constant")
    counts["exact_exponent_constants"]=3

def event_checks():
    for h in range(3,13):
        for u in range(1,11):
            for v in range(1,h-1):
                up,low,union=weighted_events(h,u,v)
                y=F(2)*(1+F(u,h))/(2+F(u,h))
                gu=1/(y*(2-y))
                bu=y**(-u)*gu**h*(1+1/(2-y))
                k=h-1
                yl=F(2)*(1-F(v,k))/(2-F(v,k))
                bl=2*yl**v*(1/(yl*(2-yl)))**k
                require(up<=bu and low<=bl and union<=bu+bl,"exact rational optimized bound")
                require(0<=union<=2 and max(up,low)<=union<=up+low,"exact union")
                counts["exact_infinite_tail_comparisons"]+=1
    # Independent finite total-word enumeration checks the symmetry factor.
    from itertools import product
    for h in range(2,5):
        sums=defaultdict(F)
        for word in product(range(1,10),repeat=h):
            if sum(word)<=10:
                sums[sum(word)]+=F(1)+F(word[-1],2)
        for s,val in sums.items():
            require(val==comb(s-1,h-1)*(1+F(s,2*h)),"terminal symmetry at fixed total")
            counts["exact_word_symmetry"]=counts["exact_word_symmetry"]+1

def endpoint_checks():
    for B in (10,40,150,500):
        groups=defaultdict(list)
        for M in range(B+1 if B%2==0 else B+2,B+4000,2):
            x=M;word=[]
            for h in range(1,7):
                t=3*x+1;a=0
                while t%2==0:t//=2;a+=1
                word.append(a);x=t
                if x<=B:
                    if 2*3**(h-1)<=B:
                        s=sum(word);pre=s-a
                        A0=B*2**pre//(2*3**(h-1))+1
                        A1=max(A0,2**s//(8*3**(h-1))+1)
                        U=B*2**s//3**h
                        require(A0<=A1<=M<=U,"inclusive rounded first-passage interval")
                        require(U<2**a*A0,"terminal ratio")
                        groups[(h,tuple(word))].append(M)
                        counts["actual_first_passage_intervals"]+=1
                    break
        for (h,word),Ms in groups.items():
            s=sum(word);a=word[-1];pre=s-a
            A0=B*2**pre//(2*3**(h-1))+1
            U=B*2**s//3**h
            A1=max(A0,2**s//(8*3**(h-1))+1)
            native=(1+F(a,2))*F(1,2**s)
            for q in range(3):
                Q=2**(s+1)*3**q
                fibres=defaultdict(list)
                for M in Ms:fibres[M%3**q].append(M)
                for xs in fibres.values():
                    require(all((M-xs[0])%Q==0 for M in xs),"CRT progression")
                    weight=3**q*sum((F(1,M) for M in xs),F(0))
                    if Q<=A0:
                        require(weight<=native,"low native bound")
                        counts["actual_low_fibre_envelopes"]+=1
                    require(weight<=native+F(3*3**(h+q),2**s),"high native bound")
                    counts["actual_high_fibre_envelopes"]+=1
                    counts["actual_fibre_crt"]=counts["actual_fibre_crt"]+1

def assembly_checks():
    for q in range(3):
        residues=3**q
        p=[F(2*(j+1),residues*(residues+1)) for j in range(residues)]
        require(sum(p)==1,"probability source only")
        S=list(range(5,38,2))
        coeff=[3**q*sum((F(1,M) for M in S if M%residues==j),F(0))
               for j in range(residues)]
        weights={M:F(3**q,M)*p[M%residues] for M in S}
        require(sum(weights.values())==sum((p[j]*coeff[j] for j in range(residues)),F(0)),
                "original kernel regrouping")
        counts["exact_kernel_mass_regrouping"]+=1
        for a in (F(2,3),F(3),F(7)):
            for L in (F(1),F(4),F(12)):
                for split in (15,25):
                    inner=[M for M in S if M<=split]
                    outer=[M for M in S if M>split]
                    e=F(1,9)
                    point={M:a+(-1)**M*e for M in inner}
                    point.update({M:L*F(M%5,4) for M in outer})
                    Zi=sum((weights[M] for M in inner),F(0))
                    Zo=sum((weights[M] for M in outer),F(0))
                    err=abs(sum((weights[M]*(point[M]-a) for M in S),F(0)))
                    require(err<=e*Zi+max(a,L-a)*Zo,"finite centered assembly")
                    counts["exact_centered_kernel_bounds"]+=1

def numerical_checks():
    # These are diagnostics for a proved limiting formula, not certified bounds.
    for C in (mp.mpf("0.5"),mp.mpf("1")):
        A=64*C*C/mp.log(2)**3
        ratios=[]
        for L in (mp.mpf(10)**k for k in (14,18,24,32)):
            h=mp.floor(L/100000);N=mp.floor(L/(10*mp.log(2)))
            W=C*mp.sqrt(N*mp.log(N));u=4*W/(25*mp.log(2))
            v=u-mp.log(mp.mpf(8)/3)/mp.log(2)
            rate=lambda t:(1+t)*mp.log1p(t)-(2+t)*mp.log1p(t/2)
            val=(2+u/(2*h))*mp.exp(-h*rate(u/h))+2*mp.exp(-(h-1)*rate(-v/(h-1)))
            ratios.append(val*mp.exp(A*mp.log(N))/4)
            counts["numerical_asymptotic_diagnostics"]+=1
        require(abs(ratios[-1]-1)<mp.mpf("1e-7"),"limiting scale diagnostic")
    return {"A_at_C_half":str(16/mp.log(2)**3),"precision_digits":mp.mp.dps}

def propagation_checks():
    audit=(HERE/"audit.tex").read_text(encoding="utf-8")
    start=audit.index(r"\section{Exterior endpoint weights and the full reference profile}")
    end=audit.index("\n"+chr(92)+"section{",start+10)
    sec=audit[start:end].strip()
    mapped=sec.replace("mazur-","Mazur-").replace(r"\section{",r"\subsection{",1)
    mapped=mapped.replace(r"\cite{Tao7}",r"\cite{Tao2026v7}")
    require(mapped in (ROOT/"tex/chapters/01m_mazur_terminal_rates.tex").read_text(encoding="utf-8"),
            "complete written propagation")
    labels=re.findall(r"\\label\{([^}]+)\}",audit)
    require(len(labels)==len(set(labels)),"duplicate local labels")
    require(set(re.findall(r"\\(?:ref|eqref)\{([^}]+)\}",audit))<=set(labels),"unresolved local labels")
    require("Definition 1.7" not in sec and r"\texttt{loam}" in sec,"source attribution")
    counts["complete_written_propagation"]=1

def main():
    propagation_checks();symbolic_checks();event_checks();endpoint_checks();assembly_checks()
    diagnostics=numerical_checks()
    sources=["ND/Band/A5ReferenceFilteredCoefficient.lean","ND/Band/A5ReferenceExteriorTupleTail.lean",
        "ND/Band/A5ReferenceTerminalCap.lean","ND/Probability/Geom2FiniteTwoEventTail.lean",
        "Tao/Section5/EndpointCoefficientBound.lean","Tao/Section5/EndpointFiberEnvelope.lean",
        "Tao/Section5/EndpointLowRoom.lean","Tao/Section5/EndpointRatio.lean",
        "Tao/Section5/Geom2HighWeightScalar.lean","Tao/Probability/Geom2HighWeight.lean",
        "Tao/Section5/EndpointValuationFiber.lean","Tao/Section5/EndpointFiberProgression.lean",
        "ND/Discrepancy/A5ReferenceFullCenterRate.lean","ND/Band/A5ReferenceSchedule.lean"]
    report={"status":"passed","counts":dict(counts),"numerical_diagnostics":diagnostics,
      "lean_started":False,"public_mutations":False,
      "scope":"Exact rational infinite-tail formula evaluations, finite word/orbit/CRT/kernel tests and symbolic MGF identities; separate 70-digit diagnostics. The complete written proof establishes the universal and asymptotic claims, not these samples. No Lean replay.",
      "source_package_commit":"ca3dd0d63920411213403092aecc6946619eb082",
      "source_hashes":{p:sha256((SOURCE/p).read_bytes()).hexdigest() for p in sources},
      "artifact_hashes":{p:sha256((HERE/p).read_bytes()).hexdigest() for p in ("audit.tex","CLAIMS.json","check_mazur_exterior.py")}}
    (HERE/"mazur_exterior_checks.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2))
if __name__=="__main__":main()
