"""Exact completed-block height regressions; not an infinite-claim certificate."""
from pathlib import Path
from collections import Counter
import hashlib,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SRC=ROOT/"external_literature/shaik_2026_v324/source/FirstPassageLinearTransport-ef3410843bf58d69f771f5ba2c0571d54b54da59/lean/FirstPassageLinearTransport"
def req(b,msg):
    if not b: raise AssertionError(msg)
def step(n): return n//2 if n%2==0 else (3*n+1)//2
def aa(m,v): return 3**v*2**(m+1-v)-1
def dd(m,q,v): return 2**(m+q-v)
def crossing(m,q):
    lo,hi=0,m
    while hi-lo>1:
        v=(lo+hi)//2
        if 2**(m+1)*3**v-2**v<=2**(m+q):lo=v
        else:hi=v
    return lo
def budget(m,q):
    a=crossing(m,q)
    return max(aa(m,a),dd(m,q,a+1))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    counts=Counter(); example=None; best=0
    for m in range(2,121):
        for q in range(1,m):
            b=budget(m,q);a=crossing(m,q)
            req(b==max(min(aa(m,v),dd(m,q,v)) for v in range(m+1)),
                "two-candidate equality")
            req(0<=a<m and aa(m,a)<=dd(m,q,a) and aa(m,a+1)>dd(m,q,a+1),
                "crossing boundary")
            req(b<=budget(m,m-1) and b<2*3**m,"uniform scalar budgets")
            counts["integer_crossing_budgets"]+=1
    for m in range(2,11):
        for x in range(2**m,2**(m+1)):
            path=[x]
            for _ in range(m):path.append(step(path[-1]))
            for v,z in enumerate(path):
                req(2**v*(z+1)<=3**v*(x+1),"forward affine growth")
                counts["forward_prefixes"]+=1
            for q in range(1,m):
                hh=next((h for h,z in enumerate(path) if z<=2**q),None)
                if hh is None:continue
                h=hh;y=path[h];b=budget(m,q);counts["actual_completed_blocks"]+=1
                for v,z in enumerate(path[:h+1]):
                    f=3**v*(x+1)//2**v-1
                    g=2**(h-v)*y
                    req(z<=min(f,g)<=b,"actual two-sided block height")
                    req(z<=min(aa(m,v),dd(m,q,v)),"shell/target height")
                    counts["two_sided_prefixes"]+=1
                raw=[x];odd=0
                for z in path[:h]:
                    if z%2:raw.append(3*raw[-1]+1);odd+=1
                    raw.append(raw[-1]//2)
                req(len(raw)-1==h+odd and raw[-1]==y and max(raw)<=2*b,
                    "raw clock and height")
                counts["ordinary_expansions"]+=1
                rise=max(path[:h+1])-x
                if rise>best:
                    best=rise;example=dict(x=x,m=m,q=q,h=h,y=y,path=path[:h+1],budget=b,
                        forward=[3**v*(x+1)//2**v-1 for v in range(h+1)],
                        backward=[2**(h-v)*y for v in range(h+1)],raw=raw,odd=odd)
    req(example is not None and best>0,"nonvacuous rising completed block")
    tex=(HERE/"audit.tex").read_text(encoding="utf-8")
    chapter=(ROOT/"tex/chapters/01n_shaik_reverse_transport.tex").read_text(encoding="utf-8")
    labels=["prop:shaik-completed-block-height","eq:shaik-two-sided-block-height",
        "eq:shaik-height-crossing","eq:shaik-height-two-candidates","eq:shaik-height-exponent",
        "cor:shaik-timeout-height-refinement","eq:shaik-timeout-low-height","eq:shaik-timeout-height-max"]
    for lab in labels:
        req("\\label{"+lab+"}" in tex and "\\label{"+lab.replace("shaik-","Shaik-")+"}" in chapter,
            "proof propagation")
    counts["proof_locators"]=len(labels)
    out=dict(status="passed",counts=dict(counts),example=example,
        scope="All integer crossing budgets for 2<=m<=120; all positive shell sources 2<=m<=10, all positive smaller target ranks, and their completed first passages by m. Finite exact regression, not proof of the general theorem or analytic package.",
        new_formal_theorems=0,lean_started=False,whole_natural_density_package_verified=False,
        source_hashes={n:sha(SRC/n) for n in ["TimeoutOrbitCeiling.lean","TimeoutEndpointWitness.lean","TimeoutRun.lean","OrbitCeiling.lean"]},
        artifact_hashes={n:sha(HERE/n) for n in ["audit.tex","CLAIMS.json","check_shaik_completed_height.py"]})
    (HERE/"shaik_completed_height_checks.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2))
if __name__=="__main__":main()
