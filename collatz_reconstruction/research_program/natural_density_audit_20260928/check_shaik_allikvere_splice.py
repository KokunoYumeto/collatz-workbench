"""Exact finite regressions for the same-orbit splice; not an analytic proof."""
from pathlib import Path
from fractions import Fraction
from collections import Counter
import hashlib,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
LABELS=["lem:shaik-high-two-sided","eq:shaik-high-three-clocks",
"lem:shaik-same-orbit-tail","eq:shaik-exact-tail",
"thm:shaik-allikvere-drift-target","eq:shaik-allikvere-count"]
def req(x,msg):
    if not x: raise AssertionError(msg)
def step(n):return (3*n+1)//2 if n%2 else n//2
def oddpart(n):
    a=0
    while n%2==0:n//=2;a+=1
    return n,a
def syr(n):return oddpart(3*n+1)[0]
def passage(n,B):
    out=[n]
    while out[-1]>B:
        out.append(step(out[-1]))
        req(len(out)<2000,"finite regression cap")
    return out
def oddpass(n,B):
    out=[n]
    while out[-1]>B:
        out.append(syr(out[-1]))
        req(len(out)<2000,"finite regression cap")
    return out
def expand(path):
    out=[path[0]]
    for x,y in zip(path,path[1:]):
        if x%2:out.append(3*x+1)
        out.append(out[-1]//2)
        req(out[-1]==y,"expanded endpoint")
    return out
def main():
    counts=Counter()
    for n in range(3,10002,2):
        for Y in (2,4,8,16,32,64,128):
            if n<=Y:continue
            path=passage(n,Y);H=len(path)-1;y=path[-1]
            s=sum(x%2 for x in path[:-1])
            P=Fraction(1)
            for x,v in zip(path,path[1:]):
                if x%2:P*=1-Fraction(1,2*v)
            req(n==Fraction(2**H*y,3**s)*P,"reverse product sign")
            req(0<=1-P<Fraction(H,3*Y),"direct first-passage defect")
            req(Y<2*y<=2*Y,"closed upper landing")
            z,a=oddpart(y);op=oddpass(n,Y)
            req(len(op)-1==s and op[-1]==z,"first odd passage")
            tail=[y]
            while tail[-1]!=z:tail.append(tail[-1]//2)
            high=path+tail[1:];rawhigh=expand(high)
            req(len(rawhigh)-1==H+s+a,"completed high raw clock")
            req(max(rawhigh)<=2*max(path),"high expansion height")
            counts["high_passage_records"]+=1
            for B in sorted({2,3,5,16,max(1,Y-1),Y,Y+1,2*Y}):
                target=oddpass(n,B);sigma=len(target)-1
                if B>=Y:
                    req(sigma<=s and target==op[:sigma+1],"earlier target truncation")
                    counts["truncated_prefixes"]+=1
                    continue
                r=sigma-s
                req(r>=0 and target[:s+1]==op,"same deterministic prefix")
                short=[z]
                for u,v in zip(target[s:],target[s+1:]):
                    cur=step(u);short.append(cur)
                    while cur!=v:cur//=2;short.append(cur)
                raw=expand(short)
                v=len(short)-1
                req(len(raw)-1==r+v,"tail clock identity")
                req(2**v*target[-1]<=4**r*z,"valuation telescope")
                req(2**v<=4**r*z,"shortcut tail budget")
                req(2**(len(raw)-1)<=2**(3*r)*z,"ordinary tail budget")
                req(max(raw)<=2**(r+1)*Y,"tail ordinary height")
                complete=rawhigh+raw[1:]
                req(complete[-1]==target[-1],"common endpoint")
                counts["continued_prefixes"]+=1
                if r==0:counts["zero_return_tails"]+=1
    # Exact valuation fibres, including cutoffs below two.
    for X in range(2,100):
        for B in range(2,20):
            bad={u for u in range(1,X+1,2) if u>B and u%3==1}
            left={n for n in range(1,X+1) if oddpart(n)[0] in bad}
            right=sum(sum(u<=X//(2**a) for u in bad) for a in range(X.bit_length()))
            req(len(left)==right,"odd-part fibre count")
            counts["valuation_fibre_counts"]+=1
    tex=(HERE/"audit.tex").read_text(encoding="utf-8")
    chapter=(ROOT/"tex/chapters/01n_shaik_reverse_transport.tex").read_text(encoding="utf-8")
    start=tex.index(r"\subsection{Joining the drift prefix")
    end=tex.index(r"\section{What has been checked",start)
    proof=tex[start:end].strip()
    req(chapter.rstrip().endswith(proof.replace("shaik-","Shaik-")),"complete proof mirror")
    for lab in LABELS:req("\\label{"+lab+"}" in tex,"proof label")
    counts["proof_locators"]=len(LABELS)
    exn,exY,exB=27,16,2
    hp=passage(exn,exY);z,a=oddpart(hp[-1]);op=oddpass(exn,exY);tp=oddpass(exn,exB)
    out=dict(status="passed",counts=dict(counts),
        example=dict(n=exn,Y=exY,B=exB,H=len(hp)-1,y=hp[-1],z=z,
                     terminal_halvings=a,s=len(op)-1,sigma=len(tp)-1,
                     r=len(tp)-len(op),odd_tail=tp[len(op)-1:]),
        scope="Exact finite arithmetic and actual path regressions; no verification of infinite density, analytic inputs or asymptotic constants.",
        new_formal_theorems=0,lean_started=False,whole_natural_density_package_verified=False,
        artifact_hashes={p:hashlib.sha256((HERE/p).read_bytes()).hexdigest()
                         for p in ["audit.tex","CLAIMS.json","check_shaik_allikvere_splice.py"]})
    (HERE/"shaik_allikvere_splice_checks.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2))
if __name__=="__main__":main()

