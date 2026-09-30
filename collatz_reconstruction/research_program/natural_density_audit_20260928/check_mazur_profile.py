"""Finite checks of the original two-cell profile, denominators and kernel transport."""
from pathlib import Path
from fractions import Fraction as Q
from math import comb, floor, ceil
from collections import Counter
from hashlib import sha256
import json
import re
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
SOURCE=ROOT/"external_literature/mazur_2026_v2/source/Erdos1135"
counts=Counter()

def require(ok,msg):
    if not ok: raise AssertionError(msg)

def log_bounds(x,terms=100):
    require(x>=1,"log domain")
    t=(x-1)/(x+1)
    total=Q(0); power=t
    for k in range(terms):
        total+=2*power/(2*k+1)
        power*=t*t
    tail=2*power/((2*terms+1)*(1-t*t))
    return total,total+tail

def mass(n,s):
    return Q(comb(s-1,n-1),2**s) if s>=n else Q(0)

def denominator_checks():
    for z,U in [(Q(1),Q(9)),(Q(6),Q(17)),(Q(13,2),Q(19)),
                (Q(17),Q(35)),(Q(101,2),Q(317,2)),(Q(99),Q(301))]:
        values=[N for N in range(1,ceil(U)) if N%2 and z<=N<U]
        D=len(values); H=sum((Q(1,N) for N in values),Q(0))
        epsD=D-(U-z)/2
        require(abs(epsD)<1,"strict count error")
        for t in [z,U]+[Q(N) for N in values]+[Q(N)+Q(1,7) for N in values if N+Q(1,7)<=U]:
            C=sum(z<=N<t for N in values)
            require(abs(C-(t-z)/2)<1,"every half-open counting discrepancy")
            counts["exact_counting_discrepancies"]+=1
        # Exact finite integration by parts: sum over each endpoint jump.
        integral=sum((Q(1,N)-1/U for N in values),Q(0))
        require(D/U+integral==H,"harmonic sum from counting integral")
        lo,hi=log_bounds(U/z)
        require(H-hi/2>=-1/z and H-lo/2<=1/z,"directed rational harmonic error")
        counts["directed_logarithmic_band_tests"]+=1
        # Signed denominator identities hold algebraically for beta and d.
        for beta in (Q(1),Q(6,5),Q(13,10)):
            for d in (Q(1,4),Q(3,10)):
                for R in (Q(-2),Q(0),Q(3,7),Q(8)):
                    eH=H-beta/2
                    require(R/H-2/d==(R-beta/d)/H-2*eH/(d*H),"harmonic exact identity")
                    # Here e^beta is represented by U/z: only the algebra is tested.
                    require(z*R/D-2/d==z/D*(R-(U/z-1)/d)-2*epsD/(d*D),"flat exact identity")
                    counts["signed_denominator_identities"]+=2

def profile_checks():
    # The cell membership and tube test are rational in lambda=beta/log2
    # and phase Lo; therefore strict boundary cases need no numerical logs.
    for n in range(1,10):
        for lo in (Q(2*n-3),Q(2*n-2,1)+Q(1,3),Q(2*n),Q(2*n)+Q(2,3)):
            theta=lo-floor(lo); s=floor(lo)+1
            for lam in (Q(4,3),Q(3,2),Q(5,3)):
                b=2-lam
                active=[L for L in range(floor(lo)-1,floor(lo)+5) if 0<L-lo<lam]
                target=[s]+([s+1] if theta>b else [])
                require(active==target,"strict base/successor enumeration")
                counts["strict_two_cell_enumerations"]+=1
                for W in (Q(1),Q(3,2),Q(3),Q(4)):
                    q0=mass(n,s) if abs(s-2*n)<W else Q(0)
                    q1=mass(n,s+1) if abs(s+1-2*n)<W else Q(0)
                    g=int(theta>b)
                    require(q0+g*q1==q0*(1+g)+g*(q1-q0),"harmonic residual")
                    # c=2^(1-theta) is symbolic: upper weight equals2c.
                    for c in (Q(1),Q(5,4),Q(2)):
                        require(c*q0+2*c*g*q1==q0*(c+2*c*g)+2*c*g*(q1-q0),"flat residual")
                        counts["signed_neighbour_identities"]+=1
                    if (q0==0)!=(q1==0): counts["distinct_tube_supports"]+=1
    for k in range(80):
        central=Q(comb(2*k,k),4**k)
        require(central*central*(k+1)<=1,"central-binomial ceiling")
        require(4*(k+1)**3-(2*k+1)**2*(k+2)==3*k+2,"induction polynomial")
        counts["central_atom_ceiling_checks"]+=1
    for n in range(1,31):
        peak=Q(comb(2*n-2,n-1),2**(2*n-1))
        for s in range(n,5*n+1):
            require(mass(n,s)<=peak,"global mass maximum")
            require(mass(n,s+1)/mass(n,s)==Q(s,2*(s+1-n)),"exact adjacent ratio")
            counts["adjacent_mass_and_peak_checks"]+=1
    for b in (Q(1,4),Q(1,2),Q(3,4)):
        require(1+1-b==2-b,"harmonic phase mean in dyadic units")
        # Integral flat pieces are1/log2 and(2^(2-b)-2)/log2:
        # retaining symbolic E=2^(2-b) gives E-1.
        for E in (Q(5,2),Q(3),Q(7,2)):
            require(1+(E-2)==E-1,"flat mean numerator")
            counts["phase_mean_coefficient_identities"]+=1

def kernel_checks():
    weights=[Q(0),Q(1,9),Q(2,7),Q(1,3)]
    for H,D,z,d,beta in [(Q(2,3),Q(5),Q(7),Q(2,7),Q(6,5)),
                         (Q(5,7),Q(11),Q(13),Q(1,3),Q(1))]:
        raw=[Q(1,5),Q(2),Q(3,4),Q(7,3)]
        for mask in range(16):
            selected=[i for i in range(4) if mask>>i&1]
            Z=sum((weights[i] for i in selected),Q(0))
            eH=H-beta/2; growth=Q(7,4); eD=D-z*growth/2
            ph=sum((weights[i]*raw[i]/H for i in selected),Q(0))
            pf=sum((weights[i]*z*raw[i]/D for i in selected),Q(0))
            require(ph-2*Z/d==sum((weights[i]*(raw[i]-beta/d) for i in selected),Q(0))/H-2*eH*Z/(d*H),"signed kernel harmonic")
            require(pf-2*Z/d==z/D*sum((weights[i]*(raw[i]-growth/d) for i in selected),Q(0))-2*eD*Z/(d*D),"signed kernel flat")
            counts["signed_kernel_transport"]+=2
        landing=[1,1,3,3]
        for targets in (set(),{1},{3},{1,3}):
            direct=sum((w for w,t in zip(weights,landing) if t in targets),Q(0))
            push={y:sum((w for w,t in zip(weights,landing) if t==y),Q(0)) for y in (1,3)}
            require(direct==sum((push[y] for y in targets),Q(0)),"landing pushforward")
            counts["landing_fibre_sums"]+=1
    for L in (Q(0),Q(1,2),Q(2),Q(7)):
        for a in (Q(1),Q(3)):
            factor=max(a,L-a)
            for j in range(11):
                x=L*Q(j,10)
                require(abs(x-a)<=factor,"sharp positive interval coefficient")
                counts["sharp_exterior_tests"]+=1
            require(max(abs(a),abs(L-a))==factor,"sharp endpoints")
            require(factor<=L+a,"source sum coefficient retained as weaker bound")
            counts["sharp_exterior_witnesses"]+=1

def main():
    audit=(HERE/"audit.tex").read_text(encoding="utf-8")
    start=audit.index(r"\section{The common endpoint profile with exact band corrections}")
    end=audit.index("\n"+chr(92)+"section{",start+10)
    section=audit[start:end].strip()
    expected=section.replace("mazur-","Mazur-").replace(r"\section{",r"\subsection{",1)
    cumulative=(ROOT/"tex/chapters/01m_mazur_terminal_rates.tex").read_text(encoding="utf-8")
    require(expected in cumulative,"complete profile proof propagation")
    labels=re.findall(r"\\label\{([^}]+)\}",audit)
    require(len(labels)==len(set(labels)),"duplicate labels")
    require(set(re.findall(r"\\(?:ref|eqref)\{([^}]+)\}",audit))<=set(labels),"missing reference")
    counts["written_proof_propagation"]=1
    denominator_checks(); profile_checks(); kernel_checks()
    files=["ND/Band/A5BandNormalizerRatios.lean","ND/Band/A5TwoProfileRawQ.lean",
           "ND/Band/A5RawMass.lean","ND/Band/A5ReferencePhysicalSplit.lean",
           "ND/Discrepancy/A5TwoProfileNormalizedA6.lean",
           "ND/Discrepancy/A5ReferenceInteriorAggregate.lean",
           "ND/Discrepancy/A5ReferenceFullCenterRate.lean",
           "Tao/Section5/CommonZ.lean"]
    out={"status":"passed","counts":dict(counts),"scope":"Finite exact rational identities, bounded log enclosures and proof-text propagation. Phase integrals and all-size assertions are proved in the written text, not certified by these samples. No Lean replay.",
         "artifact_hashes":{p:sha256((HERE/p).read_bytes()).hexdigest() for p in ["audit.tex","CLAIMS.json","check_mazur_profile.py"]},
         "source_hashes":{p:sha256((SOURCE/p).read_bytes()).hexdigest() for p in files},
         "source_package_commit":"ca3dd0d63920411213403092aecc6946619eb082","lean_started":False,"public_mutations":False}
    (HERE/"mazur_profile_checks.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2))

if __name__=="__main__": main()
