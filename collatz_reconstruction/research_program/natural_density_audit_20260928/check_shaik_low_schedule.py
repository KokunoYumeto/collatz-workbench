"""ND115 exact scalar and actual-path regressions, not an infinite-claim certificate."""
from pathlib import Path
from fractions import Fraction as Q
from functools import lru_cache
from collections import Counter
import hashlib, json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SRC=ROOT/"external_literature/shaik_2026_v324/source/FirstPassageLinearTransport-ef3410843bf58d69f771f5ba2c0571d54b54da59/lean/FirstPassageLinearTransport"
LABELS=["prop:shaik-low-schedule","eq:shaik-low-duration-set","eq:shaik-low-budget",
 "prop:shaik-low-timeout-support","eq:shaik-low-refined-count",
 "cor:shaik-low-schedule-clocks","eq:shaik-low-integer-clock"]
def req(x,msg):
    if not x: raise AssertionError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def step(x):return x//2 if x%2==0 else (3*x+1)//2
def target(r,p):return (r*(p-1)).numerator//(r*(p-1)).denominator
def schedule(L,r,p):
    out=[]
    while p>L:
        q=target(r,p)
        req(1<=q<p-1,"admissible low target")
        out.append((p,q));p=q
    return out
@lru_cache(None)
def duration_set(L,r,p):
    if p<=L:return frozenset([0])
    q=target(r,p)
    return frozenset([p-L])|frozenset(h+d for h in range(p-q,p)
                                              for d in duration_set(L,r,q))
def budget(L,r,p):return sum(a-1 for a,b in schedule(L,r,p))
def section(intervals,total):
    rest=total-sum(a for a,b in intervals); out=[]
    req(0<=rest<=sum(b-a for a,b in intervals),"sum domain")
    for a,b in intervals:
        extra=min(rest,b-a);out.append(a+extra);rest-=extra
    req(rest==0 and sum(out)==total,"sum section")
    req(all(a<=x<=b for (a,b),x in zip(intervals,out)),"section coordinates")
    return out
def low_run(x,L,r,p):
    elapsed=0; path=[x];records=[]
    while p>L:
        if x==2**p:
            for _ in range(p-L):x=step(x);path.append(x);elapsed+=1
            return True,elapsed,path,records,"dyadic"
        req(2**(p-1)<x<2**p,"non-dyadic checkpoint")
        q=target(r,p); y=x;block=[x]
        for h in range(1,p):
            y=step(y);block.append(y)
            if y<=2**q:break
        else:return False,elapsed,path,records,"timeout"
        req(p-q<=h<=p-1,"directed duration")
        records.append((p,q,h));path.extend(block[1:]);elapsed+=h;x=y;p=q
    return True,elapsed,path,records,"terminal"
def main():
    counts=Counter()
    ratios=(Q(3,5),Q(2,3),Q(3,4),Q(7,8),Q(15,16))
    for L in range(3,13):
        for r in ratios:
            for p in range(L+1,65):
                sc=schedule(L,r,p);d=duration_set(L,r,p);f=budget(L,r,p)
                req(min(d)==p-L and max(d)==f,"scalar extrema")
                req(f<=((p*(p-1)-L*(L-1))//2),"triangle bound")
                req(f<(p-1)/(1-r),"strict geometric bound")
                counts["scalar_schedules"]+=1
                a,b=4,11
                for j,(pj,qj) in enumerate(sc):
                    ints=[(a,b)]+[(u-v,u-1) for u,v in sc[:j]]
                    lo=a+p-pj;hi=b+sum(u-1 for u,v in sc[:j])
                    width=b-a+1+sum(v-1 for u,v in sc[:j])
                    req(hi-lo+1==width and lo<=hi,"directed support width")
                    for t in sorted({lo,hi,(lo+hi)//2}):
                        section(ints,t);counts["constructive_interval_sections"]+=1
    for p in range(4,11):
        for L in range(3,p):
            for r in ratios:
                sc=schedule(L,r,p);f=budget(L,r,p);ds=duration_set(L,r,p)
                for x in range(2**(p-1)+1,2**p+1):
                    ok,d,path,rec,why=low_run(x,L,r,p)
                    counts["actual_low_starts"]+=1
                    req([(a,b) for a,b,h in rec]==sc[:len(rec)],"same actual rank list")
                    if not ok:
                        j=len(rec);pj=sc[j][0]
                        req(p-pj<=d<=sum(a-1 for a,b in sc[:j]),"actual timeout support")
                        req(pj>L and path[-1]!=2**pj,"non-dyadic failure target")
                        counts["actual_first_timeouts"]+=1
                        continue
                    counts["actual_completed_continuations"]+=1
                    req(d in ds and p-L<=d<=f and path[-1]<=2**L,"actual total budget")
                    raw=[x];odd=0
                    for z in path[:-1]:
                        if z%2:raw.append(3*raw[-1]+1);odd+=1
                        raw.append(raw[-1]//2)
                    M=x.bit_length()-1
                    valid=[s for s in range(f+1) if 3**s*2**M<=2**(f+L)]
                    req(valid and odd<=max(valid),"integer odd clock")
                    req(len(raw)-1==d+odd<=f+max(valid),"ordinary clock")
                    req(raw[-1]==path[-1] and max(raw)<=2*max(path),"ordinary path and height")
                    counts["exact_clock_transfers"]+=1
                    if why=="dyadic":counts["dyadic_completions"]+=1
    # Non-vacuous concrete duration gap and actual rising path.
    req(duration_set(5,Q(3,5),6)=={1,3,4,5},"scalar gap")
    req(budget(20,Q(9,10),64)==323 and (64*63-20*19)//2==1826,
        "finite reserve comparison")
    ok,d,path,rec,why=low_run(37,5,Q(3,5),6)
    req(ok and d==4 and path==[37,56,28,14,7],"illustrated actual path")
    # Reuse the exact integer-power high-certificate sampler, not floating tolerances.
    import check_shaik_route_comparison as routes
    for M in range(80,85):
        p=routes.qrank(routes.HI,M)
        while p>routes.S:p=routes.qrank(routes.HI,p-1)
        sc=schedule(routes.L,routes.LO,p)
        for i in range(129):
            n=2**M+(i*2654435761*2**(M-32))%(2**M)+i
            ok,records,why=routes.run(n,False)
            if why!="timeout":continue
            low=[rec for rec in records if rec[0]<routes.S]
            entry=next(rec for rec in records if rec[1]<=routes.S)
            elapsed=records[-1][3]-entry[3];pj=records[-1][1];j=len(low)
            req(pj==sc[j][0],"full source timeout rank")
            req(p-pj<=elapsed<=sum(a-1 for a,b in sc[:j]),"full source low time")
            counts["full_source_first_timeout_records"]+=1
    req(counts["actual_first_timeouts"] and counts["full_source_first_timeout_records"],"vacuous timeout sample")
    tex=(HERE/"audit.tex").read_text(encoding="utf-8")
    chapter=(ROOT/"tex/chapters/01n_shaik_reverse_transport.tex").read_text(encoding="utf-8")
    for lab in LABELS:
        req("\\label{"+lab+"}" in tex and "\\label{"+lab.replace("shaik-","Shaik-")+"}" in chapter,
            "proof propagation")
    example=dict(L=5,K0=4,r="3/5",p=6,q=3,scalar_durations=[1,3,4,5],
                 actual_path=path,actual_duration=4)
    counts["proof_locators"]=len(LABELS)
    out=dict(status="passed",counts=dict(counts),example=example,
        exact_scope="Scalar schedules L=3..12, p=L+1..64, five rational ratios; all x in (2^(p-1),2^p] for 4<=p<=10, 3<=L<p, same ratios; sampled full high/low sources from ND112.",
        scope="Complete general arguments are written in the manuscripts. These exact finite regressions do not prove general recursion, transport or analytic density; no Lean was launched.",
        new_formal_theorems=0,lean_started=False,whole_natural_density_package_verified=False,
        artifact_hashes={n:sha(HERE/n) for n in ["audit.tex","CLAIMS.json","check_shaik_low_schedule.py",
                                              "check_shaik_route_comparison.py"]},
        source_hashes={n:sha(SRC/n) for n in ["TimeoutRun.lean","TimeoutTimeSupport.lean",
                      "TimeoutFirstBad.lean","TimeoutEndpointWitness.lean","MovingLowParameters.lean",
                      "TimeSupportTransport.lean"]})
    (HERE/"shaik_low_schedule_checks.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2))
if __name__=="__main__":main()
