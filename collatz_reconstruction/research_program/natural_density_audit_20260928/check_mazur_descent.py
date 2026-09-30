"""Exact finite regressions for fixed-total descent; not an analytic or Lean certificate."""
from collections import Counter
from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
from itertools import product
from math import comb, factorial
from pathlib import Path
import json
import re
import random

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SOURCE = ROOT / "external_literature/mazur_2026_v2/source/Erdos1135"
COUNT = Counter()

def require(condition, message):
    if not condition:
        raise AssertionError(message)

def dot(p, c):
    return sum((a*b for a,b in zip(p,c)), Q(0))

def project(p, m):
    out = [Q(0)] * (3**m)
    for y,v in enumerate(p):
        out[y % len(out)] += v
    return out

def average(c, m):
    return [v / (len(c)//(3**m)) for v in project(c,m)]

def lift(q,n):
    return [q[y % len(q)]/(3**n//len(q)) for y in range(3**n)]

def projection_tests():
    rng = random.Random(20260929)
    for n in range(1,5):
        for m in range(n+1):
            for _ in range(8):
                raw = [rng.randrange(1,17) for _ in range(3**n)]
                p = [Q(v,sum(raw)) for v in raw]
                c = [Q(rng.randrange(-12,19),7) for _ in p]
                q = project(p,m)
                u = lift(q,n)
                r = [v-w for v,w in zip(p,u)]
                ac = average(c,m)
                require(project(u,m)==q, "projection/lift right inverse")
                require(dot(u,c)==dot(q,ac), "mass/test adjoint")
                require(sum(abs(v) for v in u)==sum(abs(v) for v in q), "lift isometry")
                require(average([q[y % len(q)] for y in range(len(p))],m)==q,
                        "average/pullback right inverse")
                bound = Q(0)
                for x in range(len(q)):
                    vals = c[x::len(q)]
                    rs = r[x::len(q)]
                    require(sum(rs)==0, "zero mass on a fibre")
                    bound += (max(vals)-min(vals))*sum(abs(v) for v in rs)/2
                require(abs(dot(r,c))<=bound, "fibre oscillation estimate")
                addresses = [rng.randrange(len(p)) for _ in range(11)]
                weights = [Q(rng.randrange(1,9),5) for _ in addresses]
                fine = [sum((d for a,d in zip(addresses,weights) if a==y),Q(0))
                        for y in range(len(p))]
                require(dot(p,fine)==sum(p[a]*d for a,d in zip(addresses,weights)),
                        "collision-resolved fine pairing")
                coarse = average(fine,m)
                require(coarse==[sum((d for a,d in zip(addresses,weights)
                                      if a % len(q)==x),Q(0))/(len(p)//len(q))
                                 for x in range(len(q))], "collision-resolved coarsening")
                COUNT["projection_and_cancellation_fixtures"] += 1
    p=[Q(1),Q(0),Q(0)]
    c=p
    u=[Q(1,3)]*3
    require(abs(dot(p,c)-dot(u,c))==sum(abs(a-b) for a,b in zip(p,u))/2,
            "sharp factor one half")
    COUNT["sharp_half_witnesses"] += 1

@lru_cache(None)
def compositions(n,total):
    if n==1:
        return ((total,),) if total>=1 else ()
    if total<n:
        return ()
    return tuple((a,)+tail for a in range(1,total-n+2)
                 for tail in compositions(n-1,total-a))

def offset(a):
    modulus=3**len(a)
    total=0
    x=0
    for i,v in enumerate(a):
        total+=v
        x=(x+3**i*pow(pow(2,total,modulus),-1,modulus)) % modulus
    return x

def affine(a):
    modulus=3**len(a)
    total=0
    x=0
    for i in range(len(a)-1,-1,-1):
        total+=a[i]
        x=(x+3**(len(a)-1-i)*pow(pow(2,total,modulus),-1,modulus)) % modulus
    return x

@lru_cache(None)
def law(n,total):
    words=compositions(n,total)
    h=Counter(offset(a) for a in words)
    return tuple(Q(h[y],len(words)) for y in range(3**n))

def b(n,total):
    return Q(comb(total-1,n-1),2**total) if total>=n else Q(0)

def mixture_tests():
    for n in range(2,7):
        for total in range(n,n+7):
            words=compositions(n,total)
            require(len(words)==comb(total-1,n-1), "positive-composition count")
            for a in words:
                require(affine(a[::-1])==offset(a), "word reversal orientation")
                COUNT["reversal_words"]+=1
            for m in range(1,n):
                p={u:b(m,u)*b(n-m,total-u)/b(n,total)
                   for u in range(m,total-(n-m)+1)}
                require(sum(p.values())==1, "conditioned total mass")
                actual=project(law(n,total),m)
                mixture=[sum((v*law(m,u)[x] for u,v in p.items()),Q(0))
                         for x in range(3**m)]
                require(actual==mixture, "exact conditioned prefix mixture")
                for u in range(m,total-(n-m)):
                    r=b(n-m,total-u)/b(n,total)
                    nxt=b(n-m,total-u-1)/b(n,total)
                    step=Q(2*(total-u-(n-m)),total-u-1)
                    require(nxt/r==step, "adjacent likelihood")
                    require(step-1==Q((total-2*n)-(u-2*m)+1,total-u-1),
                            "adjacent signed numerator plus one")
                    COUNT["adjacent_ratios"]+=1
                COUNT["conditioned_mixtures"]+=1

def likelihood_tests():
    rng=random.Random(731)
    for _ in range(300):
        rawp=[rng.randrange(1,30) for _ in range(7)]
        rawq=[rng.randrange(1,30) for _ in range(7)]
        p=[Q(v,sum(rawp)) for v in rawp]
        q=[Q(v,sum(rawq)) for v in rawq]
        good=range(4)
        ratios=[p[i]/q[i] for i in good]
        kappa=max(ratios)/min(ratios)
        pt=sum(p[4:]); qt=sum(q[4:])
        mean=(1-pt)/(1-qt)
        require(all(mean/kappa<=v<=kappa*mean for v in ratios),
                "exact central mass ratio")
        a=max(kappa/(1-qt)-1,1-(1-pt)/kappa)
        phi=[Q(rng.randrange(0,21),10) for _ in range(7)]
        H=Q(2)
        tail=sum((p[i]-q[i])*phi[i] for i in range(4,7))
        require(-H*qt<=tail<=H*pt, "oriented outside interval")
        require(abs(dot([u-v for u,v in zip(p,q)],phi))<=a*dot(q,phi)+H*max(pt,qt),
                "weighted likelihood and maximum-tail bound")
        COUNT["exact_likelihood_fixtures"]+=1
    p=[Q(4,5),Q(1,5),Q(0)]
    q=[Q(4,5),Q(0),Q(1,5)]
    require(abs(dot([u-v for u,v in zip(p,q)],[Q(0),Q(1),Q(0)]))==Q(1,5),
            "outside bound equality")
    COUNT["signed_tail_equality_witnesses"]+=1

def exp_interval(x,N=24):
    require(Q(0)<=x<=1,"exponential input guard")
    low=sum((x**j/factorial(j) for j in range(N+1)),Q(0))
    first=x**(N+1)/factorial(N+1)
    high=low+first/(1-x/Q(N+2))
    return low,high

def terminal_tests():
    require(exp_interval(Q(1),6)[1]<Q(68,25), "exponential chord rational certificate")
    COUNT["exp_chord_certificates"]+=1
    for E,theta in product([Q(0),Q(1,10000),Q(1,100),Q(1,20),Q(1,10)],
                           [Q(1,1000000),Q(1,10000),Q(1,1000),Q(1,100)]):
        eta=E+4*theta
        lam=Q(43,25)*eta
        if lam>Q(1,2):
            continue
        el,eh=exp_interval(E)
        gl,gh=el/(1-theta)-1,eh/(1-theta)-1
        require(0<=gl<=gh<=lam, "exponential coefficient below linear coefficient")
        for M,e in product([Q(1),Q(101,100)], [Q(0),Q(1,1000),Q(1,3)]):
            newhi=(gh*M+e/2)/(1-gh)
            sharp=(lam*M+e)/(1-lam)
            old=2*(lam*M+e)
            require(newhi<=sharp<=old,"nested terminal comparison")
            COUNT["directed_terminal_comparisons"]+=1

def main():
    audit=(HERE/'audit.tex').read_text(encoding='utf-8')
    begin=audit.index(r'\section{Fixed-total descent with fibre cancellation}')
    end=audit.index('\n'+chr(92)+'section{',begin+10)
    section=audit[begin:end].strip()
    cumulative=(ROOT/'tex/chapters/01m_mazur_terminal_rates.tex').read_text(encoding='utf-8')
    expected=section.replace('mazur-','Mazur-').replace(
        r'Corollary~\ref{cor:fixed-total}',r'Proposition~\ref{prop:Tao-joint-total-mixing}').replace(
        r'\section{',r'\subsection{',1)
    require(expected in cumulative,'complete proof propagation to cumulative chapter')
    labels=re.findall(r'\\label\{([^}]+)\}',audit)
    require(len(labels)==len(set(labels)),'duplicate audit labels')
    refs=re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',audit)
    require(set(refs)<=set(labels),'unresolved audit references')
    stack=[]
    for match in re.finditer(r'\\(begin|end)\{([^}]+)\}',audit):
        kind,env=match.groups()
        if kind=='begin':
            stack.append(env)
        else:
            require(bool(stack) and stack.pop()==env,'TeX environment mismatch')
    require(not stack,'unclosed TeX environment')
    COUNT['written_proof_propagation_checks']+=1
    projection_tests()
    mixture_tests()
    likelihood_tests()
    terminal_tests()
    names=["ND/Fourier/FixedTotalFiniteResolvedDescent.lean",
           "ND/Fourier/FixedTotalSourceLaw.lean",
           "ND/Fourier/FixedTotalRatioWindow.lean",
           "ND/Fourier/FixedTotalRatioTelescope.lean",
           "ND/Fourier/FixedTotalRatioTails.lean",
           "ND/Fourier/FixedTotalRatioNormalization.lean",
           "ND/Band/A5FixedCellTerminalDescent.lean"]
    report={"status":"passed","counts":dict(COUNT),
            "scope":"Finite exact rational and directed exponential regressions; not proof of concentration, Fourier estimates, first-passage coverage, or formal certification.",
            "source_package_commit":"ca3dd0d63920411213403092aecc6946619eb082",
            "source_hashes":{p:sha256((SOURCE/p).read_bytes()).hexdigest() for p in names},
            "artifact_hashes":{p:sha256((HERE/p).read_bytes()).hexdigest()
                               for p in ("audit.tex","CLAIMS.json","check_mazur_descent.py")},
            "lean_started":False,"public_mutations":False}
    (HERE/"mazur_descent_checks.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2))

if __name__=="__main__":
    main()
