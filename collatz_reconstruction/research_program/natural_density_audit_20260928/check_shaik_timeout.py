"""Finite exact regressions and separately labelled analytic diagnostics.
Infinite/asymptotic claims are proved in audit.tex, not certified by samples.
No source-package code is executed and no Lean worker is launched.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from hashlib import sha256
import json, math, re
import mpmath as mp
mp.mp.dps=60
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
SRC=ROOT/"external_literature/shaik_2026_v324/source/FirstPassageLinearTransport-ef3410843bf58d69f771f5ba2c0571d54b54da59/lean/FirstPassageLinearTransport"
counts=Counter()
def req(b, label):
    if not b: raise AssertionError(label)
def T(x): return x//2 if x%2==0 else (3*x+1)//2
def U(m,s): return (3**s*(2**(m+1)-1+2**(m-s)))//2**m-1
def cut(q):
    s=0
    while 3**(s+1)<=2**q: s+=1
    return s
def W(xs,a=1,b=8):
    n=xs[0]
    return all(n**(2*(b-a))*3**(j*b)<=z**(2*b)*2**(2*j*b)
      <=3**(j*b)*n**(2*(b+a)) for j,z in enumerate(xs))
def paths():
    examples=[]
    lam=mp.log(3,2);g=1-lam/2
    for m in range(1,13):
        words=set();hist=Counter();timeout=Counter();corridor=0
        for n in range(2**m,2**(m+1)):
            xs=[n];word=[];offset=F(0)
            for j in range(m):
                odd=xs[-1]%2;word.append(odd)
                offset=(3*offset+1)/2 if odd else offset/2
                xs.append(T(xs[-1]))
            w=tuple(word);req(w not in words,"parity injection");words.add(w)
            s=sum(word);hist[s]+=1
            req(xs[-1]==F(3**s*n,2**m)+offset,"affine identity")
            req(offset<=F(3,2)**s-1,"odd-position offset bound")
            req(xs[-1]<=U(m,s)<3**(s+1),"integer affine envelope")
            rawtime=0;z=n
            for x,y in zip(xs,xs[1:]):
                req(z==x,"clock expansion at source")
                if x%2:
                    z=3*z+1;req(z==2*y,"inserted height");rawtime+=1
                z=z//2;rawtime+=1
            req(z==xs[-1] and rawtime==m+s,"clock bijection")
            P=F(3**s*n,2**m*xs[-1])
            req(0<P<=1,"reverse product sign")
            req(mp.mpf(s) <= (m+mp.log(mp.mpf(xs[-1])/n,2))/lam+mp.mpf("1e-55"),
                "raw odd-count logarithmic inequality")
            for q in range(m):
                if min(xs)>2**q: timeout[q]+=1
            if W(xs):
                q=9*m//10
                hits=[j for j,z in enumerate(xs) if z<=2**q]
                if hits:
                    h=hits[0];t=F(1,8)
                    req((1-mp.mpf(1)/8)*m-q<=g*h+mp.mpf("1e-55"),"one-sided lower")
                    req(g*h<(1+mp.mpf(1)/8)*(m+1)-q+1,"one-sided upper")
                    corridor+=1
            counts["actual_affine_paths"]+=1
        req(len(words)==2**m,"parity surjection")
        req(all(hist[s]==math.comb(m,s) for s in range(m+1)),"exact binomial law")
        req(all(U(m,s)<U(m,s+1) for s in range(m)),"strict integer envelope")
        for q in range(m):
            ks=next(s for s in range(m+1) if U(m,s)>2**q)
            k=cut(q)
            req(ks>=k,"cut refinement")
            sharp=sum(math.comb(m,s) for s in range(ks,m+1))
            old=sum(math.comb(m,s) for s in range(k,m+1))
            req(timeout[q]<=sharp<=old,"actual timeout subset and exact tail count")
            if ks>k and q>0:
                examples.append(dict(m=m,q=q,source_cut=k,integer_cut=ks,
                  timeouts=timeout[q],old_tail=old,refined_tail=sharp))
            counts["complete_timeout_shell_counts"]+=1
        counts["certified_one_block_corridors"]+=corridor
    return examples[:8]
def ranks():
    for M in (32,64,128,512,2048):
        for r in (F(4,5),F(7,8),F(9,10),F(19,20)):
            for S in (8,16,24):
                ms=[];qs=[];m=M
                while m>=S:
                    q=math.floor(r*m);ms.append(m);qs.append(q);m=q-1
                for j,q in enumerate(qs):
                    req(sum(a-b for a,b in zip(ms[:j+1],qs[:j+1]))==M-q-j,"telescoping center")
                    req(ms[j]<=r**j*M,"geometric decay")
                    req(sum(qs[:j+1])<=r*M/(1-r),"rank charge sum")
                    counts["exact_rank_prefixes"]+=1
                for L in range(1,S):
                    req(sum(range(L,S))==(S*(S-1)-L*(L-1))//2,"triangular low duration")
                    counts["exact_low_rank_sums"]+=1
def diagnostics():
    p=mp.log(2)/mp.log(3)
    D=lambda u:u*mp.log(2*u)+(1-u)*mp.log(2*(1-u))
    kap=D(p)/mp.log(2);u0=(p+mp.mpf(".5"))/2
    for K in (F(1,2),F(1),F(2),F(3)):
        for L in (32,64,128,256):
            for m in (L,2*L,3*L):
                q=math.floor((1-K/(2*L))*m);k=cut(q);u=mp.mpf(k)/m
                if u<u0: continue
                B=3*mp.mpf(K.numerator)/K.denominator*p/2+p+1
                req(0<=m*(D(p)-D(u))<=mp.log(p/(1-p))*B,"entropy constant multiplier")
                req(mp.mpf(q)*p-1<k<=mp.mpf(q)*p,"rounding")
                counts["60_digit_entropy_diagnostics"]+=1
    return dict(p_star=str(p),kappa=str(kap),A_FP=str(1/(2*kap)),
        source="Numerical diagnostics only; analytic bounds have written proofs.")
def propagation():
    tex=(HERE/"audit.tex").read_text(encoding="utf-8")
    title=r"\section{Shaik's timeout tail, critical rate and drift clock}"
    sec=title+tex.split(title,1)[1].split(r"\section{",1)[0]
    mapped=sec.strip().replace(r"\section{",r"\subsection{",1).replace("shaik-","Shaik-")
    cumulative=(ROOT/"tex/chapters/01n_shaik_reverse_transport.tex").read_text(encoding="utf-8")
    req(cumulative.strip().endswith(mapped),"complete timeout proof propagation")
    labels=re.findall(r"\\label\{([^}]+)\}",tex)
    req(len(labels)==len(set(labels)),"unique labels")
    req(set(re.findall(r"\\(?:ref|eqref)\{([^}]+)\}",tex))<=set(labels),"all refs")
    claims=json.loads((HERE/"CLAIMS.json").read_text(encoding="utf-8"))["claims"]
    for i,label in enumerate(("prop:shaik-prefix-uniform","prop:shaik-timeout-tail","prop:shaik-time-corridor","thm:shaik-shell-drift","cor:shaik-fixed-rate-clocks"),79):
        req(any(c["id"]==f"ND-{i:03d}" and c["tex_label"]==label for c in claims),"claim locator")
    counts["complete_written_proof_propagation"]=1
def main():
    propagation();examples=paths();ranks();diag=diagnostics()
    out=dict(status="passed",counts=dict(counts),integer_cut_examples=examples,diagnostics=diag,
      artifact_hashes={p:sha256((HERE/p).read_bytes()).hexdigest() for p in ("audit.tex","CLAIMS.json","check_shaik_timeout.py")},
      source_hashes={p:sha256((SRC/p).read_bytes()).hexdigest() for p in ("TimeoutDensity.lean","TimeoutEndpointProfile.lean")},
      formal_replay=False,public_mutations=False,
      scope="Exact complete finite-shell parity/timeout/affine/clock regressions; exact rank algebra; separately labelled 60-digit analytic diagnostics. Written proofs, not samples, establish infinite claims.")
    (HERE/"shaik_timeout_checks.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2))
if __name__=="__main__": main()
