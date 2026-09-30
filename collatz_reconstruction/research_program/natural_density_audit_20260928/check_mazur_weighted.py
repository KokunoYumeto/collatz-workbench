"""Bounded exact checks of shifted supports, raw variation and phase padding.

Only the rationally enclosed log2(3) samples use the actual Collatz rotation.
Other rational rotations test algebraic identities, not Diophantine rates.
"""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
from math import ceil, floor, comb
from hashlib import sha256
import json
import re
from check_mazur_profile import log_bounds

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
SOURCE=ROOT/"external_literature/mazur_2026_v2/source/Erdos1135"
counts=Counter()

def require(ok,msg):
    if not ok:
        raise AssertionError(msg)

def mass(n,s):
    return Q(comb(s-1,n-1),2**s) if s>=n else Q(0)

def shift_checks():
    log2lo,log2hi=log_bounds(Q(2),60)
    log3lo,log3hi=log_bounds(Q(3),90)
    glo,ghi=log3lo/log2hi,log3hi/log2lo
    require(Q(1,3)<2-ghi<2-glo<1,"certified displacement slope")
    for A in (Q(12),Q(81,4),Q(45),Q(151,2),Q(200),Q(400)):
        for W in (Q(1),Q(3,2),Q(3),Q(11,2),Q(40),Q(64)):
            R=ceil(W)-1
            stop=ceil((A+ceil(W)+2)/(2-ghi))+3
            s={}; d={}
            for n in range(1,stop):
                low,high=A+n*glo,A+n*ghi
                require(floor(low)==floor(high),"ambiguous phase enclosure")
                s[n]=floor(low)+1; d[n]=s[n]-2*n
                require((abs(d[n])<W) == (-R<=d[n]<=R),"strict integer tube")
                counts["certified_floor_levels"]+=1
            require(d[stop-1]<-R-2,"tail of finite tube exhausted")
            I0={n for n in d if -R<=d[n]<=R}
            I1={n for n in d if -R<=d[n]+1<=R}
            common=I0&I1; lost=I0-I1; gained=I1-I0
            require(common=={n for n in d if -R<=d[n]<=R-1},"common support")
            require(lost=={n for n in d if d[n]==R},"lost support")
            require(gained=={n for n in d if d[n]==-R-1},"gained support")
            require(len(lost)<=3 and len(gained)<=3,"boundary fibre count")
            counts["strict_support_partitions"]+=1
            if not I0 or not I1 or min(I0|I1)<=R+1:
                continue
            ell=min(I0|I1)
            q0={n:mass(n,s[n]) if n in I0 else Q(0) for n in I0|I1}
            q1={n:mass(n,s[n]+1) if n in I1 else Q(0) for n in I0|I1}
            for n in common:
                require((q1[n]-q0[n])/q0[n]==-Q(d[n]+2,2*(n+d[n]+1)),"signed successor ratio")
                counts["signed_successor_ratios"]+=1
            E=sum((abs(q1[n]-q0[n]) for n in q0),Q(0))
            boundary=sum((q0[n] for n in lost),Q(0))+sum((q1[n] for n in gained),Q(0))
            direct=sum((q0[n]*Q(abs(d[n]+2),2*(n+d[n]+1)) for n in common),Q(0))+boundary
            require(E==direct,"exact L1 correction")
            coefficient=max(Q(max(R-2,0),2*(ell-R+1)),Q(R+1,2*(ell+R))) if R else Q(0)
            Z=sum(q0.values(),Q(0))
            require(E<=coefficient*Z+boundary,"finite endpoint coefficient")
            require(boundary**2*ell<=9,"six-atom square-root ceiling")
            for g in (lambda n:Q(1),lambda n:Q((-1)**n,n+1)):
                lhs=sum((g(n)*(q1[n]-q0[n]) for n in q0),Q(0))
                rhs=-sum((g(n)*q0[n]*Q(d[n]+2,2*(n+d[n]+1)) for n in common),Q(0))
                rhs-=sum((g(n)*q0[n] for n in lost),Q(0))
                rhs+=sum((g(n)*q1[n] for n in gained),Q(0))
                require(lhs==rhs,"signed test identity")
                counts["signed_shift_test_identities"]+=1
            counts["exact_shift_envelopes"]+=1
            l,h=min(I0),max(I0)
            require(I0==set(range(l,h+1)),"interval support without holes")
            eta=max(Q(R,2*l),Q(R*R+R+2*l,4*l*(l-R+1)))
            for n in range(l,h):
                step=s[n+1]-s[n]
                require(step in (1,2),"level increment")
                defect=Q(d[n],2*n) if step==1 else Q(d[n]**2+d[n]-2*n,4*n*(n+d[n]+1))
                require(q0[n+1]/q0[n]-1==defect,"cross-time exact recurrence")
                require(abs(defect)<=eta,"raw variation coefficient")
                counts["cross_time_recurrences"]+=1
            V=q0[l]+q0[h]+sum((abs(q0[n+1]-q0[n]) for n in range(l,h)),Q(0))
            require(V<=q0[l]+q0[h]+eta*Z,"full raw variation")
            if W>1 and W<=Q(l,8) and Z>=Q(1,32) and W*W>=Q(37,20)**2*l:
                require(V<=20*Z*W/l,"constant20 under actual scalar guards")
                counts["constant20_guarded_examples"]+=1
            counts["full_raw_variation_checks"]+=1
    require(counts["constant20_guarded_examples"]>0,"missing guarded examples")

def discrepancy(points):
    # Exact supremum of the weak empirical error: jump values and left limits.
    m=len(points)
    return max([Q(0)]+[
        abs(Q(sum(x<=t for x in points),m)-t) for t in set(points)] +[
        abs(Q(sum(x<t for x in points),m)-t) for t in set(points)])

def padding_checks():
    for u in [(Q(3,7),),(Q(1,3),Q(2,5)),(Q(0),Q(4),Q(0)),
              (Q(1,8),Q(3,16),Q(5,32),Q(7,64)),
              (Q(-1),Q(2),Q(-3),Q(4))]:
        length=len(u)
        for P in (1,2,length,length+3):
            V=abs(u[0])+abs(u[-1])+sum(abs(u[k]-u[k+1]) for k in range(length-1))
            B=P*abs(u[0])+(P+length)*abs(u[-1])+sum((P+k+1)*abs(u[k]-u[k+1]) for k in range(length-1))
            require(B<=(P+length)*V,"padded full variation")
            for gamma in (Q(3,2),Q(8,5)):
                for A in (Q(0),Q(1,4)):
                    l=2
                    phi=A+(l-P)*gamma
                    points=[(phi+j*gamma)%1 for j in range(P+length)]
                    require(all(points[P+k]==(A+(l+k)*gamma)%1 for k in range(length)),"circle anchor")
                    require(tuple(([Q(0)]*P+list(u))[P:])==u,"padding inverse")
                    for b in (Q(1,4),Q(1,2),Q(3,4)):
                        means=2-b
                        centered=[1+int(x>b)-means for x in points]
                        S=[Q(0)]
                        for x in centered:S.append(S[-1]+x)
                        lhs=sum((u[k]*centered[P+k] for k in range(length)),Q(0))
                        rhs=u[-1]*S[P+length]-u[0]*S[P]+sum((u[k]-u[k+1])*S[P+k+1] for k in range(length-1))
                        require(lhs==rhs,"signed Abel identity")
                        Dstar=max(discrepancy(points[:m]) for m in range(P,P+length+1))
                        require(abs(lhs)<=Dstar*B,"empirical padded discrepancy bound")
                        for m in range(P,P+length+1):
                            error=sum(x<=b for x in points[:m])-m*b
                            require(S[m]==-error,"strict gate uses weak endpoint count")
                        if b in points:counts["exact_gate_endpoint_hits"]+=1
                        counts["exact_padded_abel_and_discrepancy"]+=1
    for e in (Q(5,2),Q(3),Q(7,2)):
        require((2-e/2)+(3*e/2-3)+e==2*e-1,"flat total-variation coefficient")
        counts["flat_variation_coefficient_identities"]+=1

def main():
    audit=(HERE/"audit.tex").read_text(encoding="utf-8")
    begin=audit.index(r"\section{The shifted tube and the weighted phase sum}")
    end=audit.index("\n"+chr(92)+"section{",begin+10)
    sec=audit[begin:end].strip()
    target=sec.replace("mazur-","Mazur-").replace(r"\section{",r"\subsection{",1)
    cumulative=(ROOT/"tex/chapters/01m_mazur_terminal_rates.tex").read_text(encoding="utf-8")
    require(target in cumulative,"complete weighted proof propagation")
    labels=re.findall(r"\\label\{([^}]+)\}",audit)
    require(len(labels)==len(set(labels)),"duplicate labels")
    require(set(re.findall(r"\\(?:ref|eqref)\{([^}]+)\}",audit))<=set(labels),"unresolved proof reference")
    counts["complete_written_proof_propagation"]=1
    shift_checks(); padding_checks()
    files=["ND/Band/A5ShiftedRawComparison.lean","ND/Band/A5Regularity.lean",
           "ND/Discrepancy/A5Padding.lean","ND/Discrepancy/A5PaddedProfile.lean",
           "ND/Discrepancy/A5TwoProfileTail.lean","ND/Discrepancy/PhaseToDbar.lean"]
    output={"status":"passed","counts":dict(counts),
        "scope":"Bounded exact rational tests, with directed rational log enclosures for sampled actual Collatz levels. Rational phase orbits test the algebra, not Diophantine rates. All-size statements and the flat integration formula are written proofs, not certified by the samples.",
        "artifact_hashes":{p:sha256((HERE/p).read_bytes()).hexdigest() for p in ["audit.tex","CLAIMS.json","check_mazur_weighted.py"]},
        "source_hashes":{p:sha256((SOURCE/p).read_bytes()).hexdigest() for p in files},
        "source_package_commit":"ca3dd0d63920411213403092aecc6946619eb082",
        "lean_started":False,"public_mutations":False}
    (HERE/"mazur_weighted_checks.json").write_text(json.dumps(output,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(output,indent=2))

if __name__=="__main__":main()
