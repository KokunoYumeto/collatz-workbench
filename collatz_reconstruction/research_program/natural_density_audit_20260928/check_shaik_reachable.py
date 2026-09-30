"""Exact finite regressions for reachable-rank/time/profile algebra, not infinite-orbit certification."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import json,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
def req(b,m):
 if not b:raise AssertionError(m)
def floor(x):return x.numerator//x.denominator
def ceil(x):return -((-x.numerator)//x.denominator)
def ranks(M,S,L,r,lo):
 rows=[];m=M
 while True:
  ratio=r if m>=S else lo;q=floor(ratio*m)
  rows.append((m,q,m>=S))
  req(0<=q<m,"strict deterministic rank descent")
  if q<=L:break
  m=q-1
 return rows
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 c=Counter()
 for M in (32,64,127,256,511,1000):
  for S in (8,16,24):
   if S>=M:continue
   for L in (2,4,6):
    for r in (F(2,3),F(4,5),F(9,10)):
     for lo in (F(3,4),F(7,8),F(31,32)):
      rows=ranks(M,S,L,r,lo);qs=[q for m,q,h in rows]
      req(len(qs)==len(set(qs)),"unique rank coordinate")
      for (m,q,h),(mn,qn,hn) in zip(rows,rows[1:]):
       req(mn==q-1 and qn<q,"exact parent and phase")
      hi=[q for q in qs if q>S]
      req(sum(hi)<=r*M/(1-r),"high geometric weight")
      req(len(hi)*(S+1)<=sum(hi),"exact high rank count")
      for rs in (F(1,4),F(1,2)):
       w=lambda q:1+3*F(q+2,1)/rs
       coef=r/(1-r)*(3/rs+(1+6/rs)/(S+1))
       req(sum(map(w,hi),F(0))<=coef*M,"linear high transport coefficient")
       dyadic=sum((w(q)/2**q for q in hi),F(0))
       req(dyadic<=(1+3*F(S+4,1)/rs)/2**S,"exact dyadic endpoint tail")
       c["rational_high_profile_bounds"]+=1
      c["deterministic_rank_lists"]+=1
 # Necessary scalar duration corridors are sampled, not asserted actual Collatz runs.
 for M in range(8,33,4):
  for S in (4,6):
   for r in (F(2,3),F(4,5)):
    for lo in (F(3,4),F(7,8)):
     rows=ranks(M,S,2,r,lo);times={0};E=F(0)
     for j,(m,q,high) in enumerate(rows):
      g=F(1,5);t=F(1,20) if high else F(1,10)
      ds=[h for h in range(1,m+1) if abs(g*h-(m-q))<=t*(m+1)+2]
      times={h+k for h in times for k in ds}
      E+=t*(m+1)+3;center=M+1-q
      A=max(1,ceil((center-E)/g));B=floor((center+E)/g)
      req(all(A<=h<=B for h in times),"cumulative integer enclosure")
      req(len(times)<=max(0,B-A+1),"exact time cardinality")
      c["rational_duration_prefixes"]+=1
 for S in range(1,80):
  for rs in (F(1,4),F(1,2),F(3,4)):
   w=lambda q:1+3*F(q+2,1)/rs
   for N in (S+1,S+5,S+17):
    finite=sum((w(q)/2**q for q in range(S+1,N+1)),F(0))
    tail=(1+3*F(N+4,1)/rs)/2**N
    full=(1+3*F(S+4,1)/rs)/2**S
    req(finite+tail==full,"exact finite dyadic tail identity")
    c["rational_dyadic_tail_identities"]+=1
 # Preserve directed source bounds and round each block before summing.
 # These are exact scalar corridors, not asserted realized Collatz durations.
 for M in range(8,33,4):
  for S in (4,6):
   for r in (F(2,3),F(4,5)):
    for lo in (F(3,4),F(7,8)):
     rows=ranks(M,S,2,r,lo);g=F(1,5)
     times={0};amin=0;bmax=0;nonempty=True;U=T=F(0)
     for j,(m,q,high) in enumerate(rows):
      t=F(1,20) if high else F(1,10)
      low=(1-t)*m-q;up=(1+t)*(m+1)-q+1
      a=max(1,ceil(low/g));b=min(m,ceil(up/g)-1)
      ds=set(range(a,b+1))
      req(ds=={h for h in range(1,m+1) if low<=g*h<up},'directed strict endpoint')
      times={h+k for h in times for k in ds}
      amin+=a;bmax+=b;nonempty=nonempty and a<=b
      U+=t*m;T+=t*(m+1);p=j+1;center=M-q-j
      req(times==(set(range(amin,bmax+1)) if nonempty else set()),'exact scalar interval addition')
      Ad=max(1,ceil((center-U)/g));Bd=ceil((center+T+2*p)/g)-1
      As=max(1,ceil((M+1-q-(T+3*p))/g));Bs=floor((M+1-q+T+3*p)/g)
      req(Ad>=As and Bd<=Bs,'directed within symmetric enclosure')
      if nonempty:req(amin>=Ad and bmax<=Bd,'blockwise enclosure nesting')
      for cut in (0,5,17,50):
       clipped={h for h in times if h<=cut}
       count=max(0,min(cut,bmax)-amin+1) if nonempty else 0
       req(len(clipped)==count,'exact clipped interval cardinality')
       c['directed_clipped_profiles']+=1
      c['directed_blockwise_prefixes']+=1
 # Integer upper endpoints use ceil(u)-1, including exactly integral u.
 for n in range(-10,21):
  for d in range(1,8):
   u=F(n,d)
   req(all((h<u)==(h<=ceil(u)-1) for h in range(-15,25)),'strict ceiling identity')
   c['strict_ceiling_endpoints']+=1
 # At Q=e+3/2 the V prefactors cancel exactly. Generic positive V is enough here.
 for n in range(3,30):
  for s in range(1,8):
   for e in (1,2,3):
    x=n*n;V=s*s;H=F(n*s);Delta=F(1,s*n**(2*e+3))
    req(H*(x-2)*Delta==F(x-2,n**(2*e+2)),"closed margin exact cancellation")
    req(H*(x-2)*Delta<=F(1,x**e),"closed margin bound")
    c["closed_margin_rational_identities"]+=1
 tex=(HERE/"audit.tex").read_text(encoding="utf-8")
 labs=["eq:shaik-moving-reachable-ranks","prop:shaik-moving-reachable-support",
  "eq:shaik-moving-integer-time-support","eq:shaik-moving-retained-potential",
  "eq:shaik-moving-reachable-profile","cor:shaik-moving-linear-high",
  "eq:shaik-moving-linear-high","eq:shaik-moving-high-rate","eq:shaik-moving-high-closed-margin",
  "eq:shaik-moving-directed-corridor","eq:shaik-moving-blockwise-support"]
 for lab in labs:req(tex.count("\\label{"+lab+"}")==1,"unique proof label")
 title=r"\section{Shaik's timeout tail, critical rate and drift clock}"
 sec=title+tex.split(title,1)[1].split(r"\section{",1)[0]
 mapped=sec.strip().replace(r"\section{",r"\subsection{",1).replace("shaik-","Shaik-")
 req((ROOT/"tex/chapters/01n_shaik_reverse_transport.tex").read_text(encoding="utf-8").strip().endswith(mapped),
     "complete cumulative proof propagation")
 cls=json.loads((HERE/"CLAIMS.json").read_text(encoding="utf-8"))["claims"]
 req(next(x for x in cls if x["id"]=="ND-109")["canonical_claim_id"]=="CLM-COL-000302","canonical claim mapping")
 for old in ("ND-104","ND-106","ND-107","ND-108"):
  req("ND-109" in next(x for x in cls if x["id"]==old)["later_refinements"],"earlier consequence propagation")
 c["complete_written_propagation"]+=1
 out=dict(status="passed",counts=dict(c),new_formal_theorems=0,lean_started=False,
  whole_natural_density_package_verified=False,
  scope="Exact finite rank/transport/interval and cancellation checks; synthetic necessary duration corridors are not asserted realized Collatz runs. General claims have complete written proofs; no analytic or whole-package Lean certificate.",
  artifact_hashes={n:sha(HERE/n) for n in ("audit.tex","CLAIMS.json","check_shaik_reachable.py","draw_shaik_reachable.py","shaik_reachable_ranks.png")})
 (HERE/"shaik_reachable_checks.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(dict(status="passed",counts=dict(c)),indent=2))
if __name__=="__main__":main()
