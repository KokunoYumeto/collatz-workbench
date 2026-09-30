"""Exact finite checks of band transport, strict decoding and maximal moments."""
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from math import ceil, comb
from pathlib import Path
import json
import random
import re
from check_mazur_descent import compositions
from check_mazur_coverage import orbit

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
SOURCE=ROOT/"external_literature/mazur_2026_v2/source/Erdos1135"
COUNT=Counter()

def require(ok,message):
    if not ok:
        raise AssertionError(message)

def theta(n,M):
    return Q(sum(comb(M-1,j) for j in range(min(n,M))),2**(M-1))

def full_distance(actual,n):
    # Ideal law is infinite. Its mass outside the actual finite support is retained.
    ideal={a:Q(1,2**sum(a)) for a in actual}
    return sum(abs(p-ideal[a]) for a,p in actual.items())+1-sum(ideal.values())

def rate_bound(n,w):
    # exp(-n I(+-w/n)) is rational when n,w are integral.
    require(0<w<n,"rate domain")
    return sum((Q(2*n+s*w,2*n)**(2*n+s*w)/
                Q(n+s*w,n)**(n+s*w) for s in (1,-1)),Q(0))

def maximal_mass(n,w):
    # Exact survival in -w<X_k<w; all outside mass is retained as failure.
    states={0:Q(1)}
    for k in range(1,n+1):
        nxt=Counter()
        for x,p in states.items():
            for y in range(-w+1,w):
                a=y-x+2
                if a>=1:
                    nxt[y]+=p*Q(1,2**a)
        states=dict(nxt)
    return 1-sum(states.values())

def decoder_tests():
    for M in range(1,10):
        residues=range(1,2**M,2)
        for n in range(1,6):
            decoded={}
            for r in residues:
                a=tuple(orbit(r,n)[1])
                decoded[r]=a if sum(a)<M else None
                for lift in (1,3):
                    b=tuple(orbit(r+lift*2**M,n)[1])
                    require(decoded[r]==(b if sum(b)<M else None),"decoder independent of lift")
                    COUNT["strict_decoder_lift_checks"]+=1
            hist=Counter(decoded.values())
            for total in range(n,M):
                for a in compositions(n,total):
                    require(hist[a]==2**(M-total-1),"accepted decoder fibre size")
                    COUNT["accepted_decoder_fibres"]+=1
            require(Q(hist[None],2**(M-1))==theta(n,M),"exact binomial overflow")
            COUNT["exact_overflow_identities"]+=1
    for n in range(1,101):
        require(theta(n,3*n)<=Q(27,32)**n,"optimized overflow bound")
        COUNT["overflow_rate_checks"]+=1
    # The sharp two-min remainder cannot be removed.
    p,q=[Q(1),Q(0)],[Q(0),Q(1)]
    require(sum(abs(a-b) for a,b in zip(p,q))==2 and abs(sum(p)-sum(q))==0,
            "two different overflow atoms collapse to the same symbol")
    COUNT["sharp_overflow_and_half_event_witnesses"]+=1

def band_tests():
    for z,U in [(Q(1),Q(15)),(Q(6),Q(40)),(Q(17,2),Q(91,2)),
                (Q(20),Q(91)),(Q(101),Q(301)),(Q(201,2),Q(603,2))]:
        values=[N for N in range(1,ceil(U)) if N%2 and z<=N<U]
        D=len(values)
        H=sum((Q(1,N) for N in values),Q(0))
        laws={"F":[Q(1,D)]*D,"H":[Q(1,N)/H for N in values]}
        for i,N in enumerate(values):
            require(laws["F"][i]/laws["H"][i]==N*H/D,"exact density ratio")
            COUNT["band_density_ratio_identities"]+=1
        for M in (1,2,3,5,7,9):
            q=2**M
            for sigma,weights in laws.items():
                hist=Counter()
                for N,p in zip(values,weights):
                    hist[N%q]+=p
                delta=sum(abs(hist[b]-Q(2,q)) for b in range(1,q,2))
                bound=Q(q,2*D) if sigma=="F" else Q(q,2*ceil(z))/H
                require(delta<=bound,"finite band residue discrepancy")
                COUNT["band_residue_bounds"]+=1
                for n in (1,2,4):
                    wordlaw=Counter()
                    for N,p in zip(values,weights):
                        wordlaw[tuple(orbit(N,n)[1])]+=p
                    distance=full_distance(wordlaw,n)
                    require(distance<=delta+2*theta(n,M),"strict-truncation full L1 transfer")
                    COUNT["full_valuation_distance_bounds"]+=1
                    for w in range(1,n):
                        actual=sum((p for a,p in wordlaw.items()
                                    if any(abs(sum(a[:k])-2*k)>=w for k in range(1,n+1))),Q(0))
                        ideal=maximal_mass(n,w)
                        require(abs(actual-ideal)<=distance/2,"event half full-L1 bound")
                        require(actual<=rate_bound(n,w)+bound/2+theta(n,M),"actual maximal-event bound")
                        COUNT["actual_band_event_transfers"]+=1
        for W in (Q(1),Q(3,2),Q(6),Q(13,2)):
            w=ceil(W); R=w-1
            for v in range(-9,10):
                require((abs(v)<W)==(abs(v)<=R),"strict source radius")
                require((abs(v)>=W)==(abs(v)>=w),"inclusive ceiling crossing")
                COUNT["strict_radius_endpoint_checks"]+=1

def stopped_moment(n,w,c):
    """Exact E[Z_tau] for two-sided stopping, with the infinite upper tail summed."""
    moment=1/(c*(2-c))
    states={0:Q(1)}
    stopped=Q(0)
    for k in range(1,n+1):
        nxt=Counter()
        for x,p in states.items():
            upper=max(1,w-x+2)
            # Sum_a>=upper 2^-a c^(x+a-2)/moment^k exactly.
            stopped+=p*c**(x-2)*(c/2)**upper/(1-c/2)/moment**k
            for a in range(1,upper):
                y=x+a-2
                mass=p*Q(1,2**a)
                if y<=-w:
                    stopped+=mass*c**y/moment**k
                else:
                    nxt[y]+=mass
        states=dict(nxt)
    return stopped+sum((p*c**x/moment**n for x,p in states.items()),Q(0))

def maximal_tests():
    for n in (2,3,4,6,8,12,20,40):
        for w in sorted({1,max(1,n//3),n//2,n-1}):
            require(maximal_mass(n,w)<=rate_bound(n,w),"exact maximal rate bound")
            COUNT["exact_maximal_tail_checks"]+=1
    for n in (2,4,7):
        for w in (1,2,3):
            for c in (Q(3,4),Q(1),Q(4,3),Q(3,2)):
                require(stopped_moment(n,w,c)==1,"bounded stopped exponential expectation")
                COUNT["exact_stopped_exponential_identities"]+=1
    for v in (Q(-1,2),Q(-1,10),Q(0),Q(1,10),Q(1,2),Q(1)):
        c=2*(1+v)/(2+v)
        require(2*(c-1)/(2-c)==v,"exact optimizing parameter")
        require(1/(1+v)-1/(2+v)==1/((1+v)*(2+v)),"rate second derivative")
        COUNT["rate_derivative_and_optimizer_checks"]+=1

def main():
    audit=(HERE/"audit.tex").read_text(encoding="utf-8")
    start=audit.index(r"\section{Actual band laws and a maximal prefix bound}")
    end=audit.index("\n"+chr(92)+"section{",start+10)
    section=audit[start:end].strip()
    expected=section.replace("mazur-","Mazur-").replace(
        r"Proposition~\ref{prop:fibre}",r"Lemma~\ref{lem:Tao-Prop19-residue-fibre}").replace(
        r"\cite{Tao7}",r"\cite{Tao2026v7}").replace(r"\section{",r"\subsection{",1)
    cumulative=(ROOT/"tex/chapters/01m_mazur_terminal_rates.tex").read_text(encoding="utf-8")
    require(expected in cumulative,"complete band proof propagation")
    labels=re.findall(r"\\label\{([^}]+)\}",audit)
    require(len(labels)==len(set(labels)),"duplicate audit label")
    require(set(re.findall(r"\\(?:ref|eqref)\{([^}]+)\}",audit))<=set(labels),"unresolved audit label")
    other=(ROOT/"tex/chapters/01l_allikvere_uniform_fibres.tex").read_text(encoding="utf-8")
    require(r"\ref{cor:Mazur-allikvere-prefix}" in other,"Allikvere prefix consequence not propagated")
    COUNT["written_proof_and_cross_source_propagation_checks"]+=1
    decoder_tests()
    band_tests()
    maximal_tests()
    files=["ND/Band/A5HarmonicFullGood.lean","ND/Band/A5BandCoverageFullGood.lean",
           "ND/Band/A5BandCoverageProbability.lean","ND/Band/A5PrefixGood.lean",
           "ND/Band/A5HarmonicProp19.lean","ND/Band/A5HarmonicResidue.lean",
           "Tao/Probability/Geom2PrefixTypical.lean","Tao/Probability/LogWindowResidue.lean",
           "Tao/Syracuse/Prop19.lean","Tao/Syracuse/Prop19Laws.lean",
           "Tao/Syracuse/Prop19Truncation.lean","Tao/Syracuse/TruncatedValuationTV.lean"]
    report={"status":"passed","counts":dict(COUNT),
            "scope":"Exact rational finite regressions, including full infinite ideal-law residual mass and summed geometric overshoots. Written proofs establish the asymptotic bounds; these tests are not a Lean or analytic certificate.",
            "source_package_commit":"ca3dd0d63920411213403092aecc6946619eb082",
            "source_hashes":{p:sha256((SOURCE/p).read_bytes()).hexdigest() for p in files},
            "artifact_hashes":{p:sha256((HERE/p).read_bytes()).hexdigest()
                               for p in ("audit.tex","CLAIMS.json","check_mazur_band.py")},
            "lean_started":False,"public_mutations":False}
    (HERE/"mazur_band_checks.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2))

if __name__=="__main__":
    main()
