"""Exact finite checks for the written Shaik transport reconstruction.
No finite sample certifies a natural-density or infinite-orbit theorem.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter, defaultdict
from hashlib import sha256
import json, re, math
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
SHELF=ROOT/"external_literature/shaik_2026_v324"
SRC=SHELF/"source/FirstPassageLinearTransport-ef3410843bf58d69f771f5ba2c0571d54b54da59/lean"
counts=Counter()
def req(x,msg):
    if not x: raise AssertionError(msg)
def T(n):return n//2 if n%2==0 else (3*n+1)//2
def raw(n):return n//2 if n%2==0 else 3*n+1
def v2(n):
    a=0
    while n%2==0:n//=2;a+=1
    return a
def passage(n,Y,cap=200):
    xs=[n]
    for h in range(cap+1):
        if xs[-1]<=Y:return xs
        if h<cap:xs.append(T(xs[-1]))
    return None
def data(xs):
    L=F(0);P=F(1);b=F(0);s=0
    for x,z in zip(xs,xs[1:]):
        req(T(x)==z,"actual edge")
        odd=x%2
        u=F(odd,2*z)
        L+=u;P*=1-u
        b=(3*b+1)/2 if odd else b/2
        s+=odd
    return L,P,b,s
def cceil(x):return -((-x.numerator)//x.denominator)
def interval_count(N,A,e):
    lo=max(N,cceil((1-e)*A));hi=min(2*N-1,math.floor(A))
    return max(0,hi-lo+1)
def finite_paths():
    fibres=defaultdict(list);examples=[]
    for n in range(3,1025):
        M=n.bit_length()-1;N=2**M
        for Y in (F(3,2),F(2),F(7,2),F(7),F(15),F(31)):
            if not (1<Y<N):continue
            xs=passage(n,Y)
            if xs is None:
                counts["bounded_paths_not_decided"]+=1;continue
            h=len(xs)-1;y=xs[-1];L,P,b,s=data(xs)
            req(Y/2<y<=Y,"landing band")
            req(n==F(2**h*y,3**s)*P,"reverse identity")
            req(y==F(3**s*n,2**h)+b,"forward identity")
            req(1-P==b/y and 0<=1-P<=L,"defect map")
            o=math.floor(Y)+1
            if o%2==0:o+=1
            req(Y*L<=F(Y*s,3*o+1)<=F(Y*(h-1),3*o+1)<F(h,3),"odd denominator")
            for k in {0,h//2,h}:
                L1,P1,b1,s1=data(xs[:k+1]);L2,P2,b2,s2=data(xs[k:])
                Y1=Y+3;G1=Y1*(1-P1);G2=Y*(1-P2)
                req(L==L1+L2 and P==P1*P2,"sum/product concatenation")
                req(Y*(1-P)==Y/Y1*G1+G2-G1*G2/Y1,"nonlinear defect composition")
                counts["exact_concatenations"]+=1
            for e in (F(0),F(1,12),F(1,6),F(1,3)):
                if 1-P<=e:fibres[(M,Y,h,y,e)].append((n,s))
            if not examples and 1-P<L and 1-P<F(1,3):
                e=(1-P+min(L,F(1,3)))/2
                req(1-P<=e<L,"strictly weaker exact defect filter")
                examples.append(dict(n=n,Y=str(Y),h=h,y=y,product_defect=str(1-P),additive_loss=str(L),epsilon=str(e)))
            if n%2:
                d=v2(y);u=y//2**d;z=n;vals=[];oddpath=[n]
                while z>Y and len(vals)<=h:
                    a=v2(3*z+1);z=(3*z+1)//2**a;vals.append(a);oddpath.append(z)
                req(len(vals)==s and z==u and sum(vals)==h+d,"Syracuse clocks")
                dd=0
                while 2**(dd+1)*u<=Y:dd+=1
                req(dd==d,"inverse terminal tail")
                rr=n
                for t in range(h+s):
                    req(rr>Y,"raw first passage has no earlier hit");rr=raw(rr)
                req(rr==y,"raw first passage index")
                LL=sum((F(1,3*z+1) for z in oddpath[:-1]),F(0))
                PP=math.prod((F(3*z,3*z+1) for z in oddpath[:-1]),start=F(1))
                req(LL==L and PP==P,"return loss coordinates")
                counts["exact_clock_correspondences"]+=1
            counts["actual_first_passage_paths"]+=1
    for (M,Y,h,y,e),rows in fibres.items():
        req(len({s for n,s in rows})==1,"odd count rigidity")
        N=2**M;s=rows[0][1];A=F(2**h*y,3**s)
        bound=1+math.floor(e*(2*N-1))
        req(len(rows)<=interval_count(N,A,e)<=bound,"clipped fibre count")
        req(bound<=1+2*e*N<=1+3*e*N,"source coefficient comparison")
        counts["exact_tagged_fibres"]+=1
    # Disjointness of tags means aggregation retains actual support, not a horizon.
    groups=defaultdict(list)
    for tag,rows in fibres.items():
        M,Y,h,y,e=tag;groups[(M,Y,e)].append((h,y,rows))
    for (M,Y,e),rows in groups.items():
        selected=[(h,y,rr) for h,y,rr in rows if h%3!=0 and y%2==1]
        S={h for h,y,rr in selected};B={y for h,y,rr in selected}
        starts=[n for h,y,rr in selected for n,s in rr]
        req(len(starts)==len(set(starts)),"unique first-passage tags")
        req(len(starts)<=len(S)*len(B)*(1+math.floor(e*(2**(M+1)-1))),"support-sensitive transport")
        counts["exact_transport_unions"]+=1
    return examples
def intervals():
    for N in (2,4,8,16,32):
        for e in (F(0),F(1,48),F(1,12),F(1,6),F(1,3)):
            bound=1+math.floor(e*(2*N-1))
            req(interval_count(N,F(2*N-1),e)==bound,"sharp interval envelope")
            for j in range(1,12*N):
                A=F(j,3)
                req(interval_count(N,A,e)<=bound,"all tested interval positions")
                counts["rational_shell_intervals"]+=1
def chains():
    r=F(7,8)
    for n in range(16,1025):
        x=n;t=0;full=[n];parts=[]
        while x.bit_length()-1>=3:
            m=x.bit_length()-1;q=math.floor(r*m);Y=2**q
            xs=passage(x,Y,cap=m)
            if xs is None:break
            h=len(xs)-1;L,P,b,s=data(xs)
            if parts:req(q<parts[-1][0],"decreasing ranks")
            parts.append((q,m,h,s));t+=h;full+=xs[1:];x=xs[-1]
            req(passage(n,Y,cap=t)==full,"direct first passage")
            LL,PP,bb,ss=data(full)
            B=sum((F(2**q*sj,3*2**qj+4) for qj,mj,hj,sj in parts),F(0))
            C=sum((F(mj)*F(2)**(q-qj)/3 for qj,mj,hj,sj in parts),F(0))
            D=F(2*(q+2),3)/r
            req(Y*LL<=B<C<D,"exact and two-thirds chain budgets")
            req(D==F(2,3)*F(q+2)/r,"source budget comparison")
            if D/Y<=F(1,3):
                req(2*D/(3*F(q+2)/r)==F(4,9),"combined coefficient ratio")
                counts["admissible_chain_transport_budgets"]+=1
            counts["actual_chain_prefixes"]+=1
def propagation():
    tex=(HERE/"audit.tex").read_text(encoding="utf-8")
    title=r"\section{Shaik's reverse loss and exact first-passage transport}"
    sec=title+tex.split(title,1)[1].split(r"\section{",1)[0]
    mapped=sec.strip().replace(r"\section{",r"\subsection{",1).replace("shaik-","Shaik-").replace("sec:mazur-real-timed","sec:Mazur-real-timed")
    cumulative=(ROOT/"tex/chapters/01n_shaik_reverse_transport.tex").read_text(encoding="utf-8")
    first=cumulative.split(r"\subsection{",2)
    reverse=r"\subsection{"+first[1] if len(first)>2 else cumulative
    req(mapped==reverse.strip(),"entire reverse proof propagation")
    labels=re.findall(r"\\label\{([^}]+)\}",tex)
    req(len(labels)==len(set(labels)),"unique audit labels")
    req(set(re.findall(r"\\(?:ref|eqref)\{([^}]+)\}",tex))<=set(labels),"resolved audit references")
    claims=json.loads((HERE/"CLAIMS.json").read_text(encoding="utf-8"))["claims"]
    for i,label in enumerate(("prop:shaik-defect","prop:shaik-clipped-fibre","prop:shaik-chain-transport","prop:shaik-clock-map"),75):
        req(any(c["id"]==f"ND-{i:03d}" and c["tex_label"]==label for c in claims),"claim/proof locator")
    spine=(ROOT/"tex/chapters/01_literature_spine.tex").read_text(encoding="utf-8")
    req(r"\input{chapters/01n_shaik_reverse_transport}" in spine,"cumulative inclusion")
    counts["complete_written_proof_propagation"]=1
def main():
    propagation();examples=finite_paths();intervals();chains()
    sourcefiles=("FirstPassage.lean","LossTransport.lean","NestedRecertification.lean","RankScaledLoss.lean","Main.lean")
    out={"status":"passed","counts":dict(counts),"strict_defect_example":examples,
      "source_commit":"ef3410843bf58d69f771f5ba2c0571d54b54da59",
      "source_hashes":{p:sha256((SRC/"FirstPassageLinearTransport"/p).read_bytes()).hexdigest() for p in sourcefiles},
      "artifact_hashes":{p:sha256((HERE/p).read_bytes()).hexdigest() for p in ("audit.tex","CLAIMS.json","check_shaik_reverse.py")},
      "scope":"Exact rational checks of finite actual paths, products, affine defects, shell-clipped fibres, disjoint tag aggregation, rank-chain budgets and clock inverses. Sharpness is for interval containment, not actual Collatz occupancy. All-size assertions have separate written proofs; no density theorem is certified by enumeration.",
      "formal_replay":False,"public_mutations":False}
    (HERE/"shaik_reverse_checks.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2))
if __name__=="__main__":main()
