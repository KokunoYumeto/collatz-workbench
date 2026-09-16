#!/usr/bin/env python3
"""Independent streaming audit; imports NO contribution or predecessor module.

Reconstructs the sharp envelope through exact integer powers; then reads EVERY
original-source row and replays each valuation by repeated divisions. Checks
both the odd endpoint and the earlier shortened-map first crossing. The
integer-valued source-height table supplies a separate finite induction.
"""
from __future__ import annotations
import argparse
from array import array
import gzip
import hashlib
import json
from pathlib import Path

class AuditError(ValueError):pass

def require(ok: bool,message: str) -> None:
    if not ok:raise AuditError(message)

def audit(horizon: int, ledger: Path) -> dict:
    require(type(horizon) is int and horizon>=1,'positive horizon required')
    # A critical floor-prefix path, evaluated with original rational affine
    # numerator/denominator, provides the same sharp source ceiling.
    power3=1;power2=1;critical_num=0;critical_den=1;last_floor=0
    bounds=[]; maximum=0
    for m in range(1,horizon+1):
        power3*=3
        while 2*power2<power3:power2*=2
        # The last floor step has 1 or 2 divisions. It is NOT the crossing
        # step; its numerator is unchanged on replacing that step by the
        # first crossing exponent.
        floor=power2.bit_length()-1
        critical_num=3*critical_num+critical_den
        critical_den<<=(floor-last_floor);last_floor=floor
        require(critical_den==power2,'critical floor-prefix image mismatch')
        gap=2*power2-power3;require(gap>0,'first crossing power is not above original 3-power')
        b=critical_num//gap
        bounds.append((m,floor+1,b));maximum=max(maximum,b)
    bound=maximum if maximum%2 else maximum-1
    expected=3;rows=0;edges=0;halvings=0;histogram={};shorthist={};sha=hashlib.sha256()
    heights=array('I',[0])*((bound+1)//2);max_height=0;max_height_source=1
    longest=0;longest_source=1;peak=1;peak_source=1
    with gzip.open(ledger,'rb') as f:
        for line in f:
            sha.update(line);entry=json.loads(line)
            require(isinstance(entry,list) and len(entry)==3,'invalid ledger row')
            n,terminal,word=entry
            require(type(n) is int and n==expected and n<=bound,'missing, duplicated, out-of-order or extra source')
            require(type(terminal) is int and isinstance(word,list) and bool(word),'invalid source endpoint or word')
            x=n;coeff_num=1;coeff_den=1;A=0;short_cross=None;short_steps=0;odd_count=0
            for j,a in enumerate(word,1):
                require(type(a) is int and a>=1,'nonpositive or nonintegral exponent')
                require(x%2==1 and x>0,'odd original endpoint required')
                # First division is the original shortened odd map. Remaining
                # divisions are original shortened even maps.
                x=3*x+1;coeff_num*=3;odd_count+=1
                b=0
                while x%2==0:
                    x//=2;coeff_den*=2;b+=1;halvings+=1;short_steps+=1
                    if short_cross is None and coeff_num<coeff_den:
                        short_cross=(short_steps,x,odd_count)
                require(a==b,'declared exponent differs from repeated-division valuation')
                A+=a;edges+=1
                if x>peak:peak=x;peak_source=n
                if j<len(word):
                    require(coeff_num>coeff_den and x>n,'word crossed or descended before its declared last return')
            require(x==terminal and x<n and coeff_num<coeff_den,'false original terminal or descent')
            require(len(word)<=horizon and short_cross is not None,'no certified crossing in the horizon')
            require(short_cross[1]<n and short_cross[2]==len(word),'shortened-map crossing was not a descent')
            require(short_cross[0]==coeff_num.bit_length(),'wrong shortened first-crossing clock')
            h=len(word)+heights[x//2];require(h<2**32,'height overflow');heights[n//2]=h
            if h>max_height:max_height=h;max_height_source=n
            if len(word)>longest:longest=len(word);longest_source=n
            histogram[len(word)]=histogram.get(len(word),0)+1
            shorthist[short_cross[0]]=shorthist.get(short_cross[0],0)+1
            rows+=1;expected+=2
    require(expected==bound+2,'truncated source ledger')
    hsha=hashlib.sha256()
    for h in heights:hsha.update(int(h).to_bytes(4,'little'))
    return {'status':'PASS','horizon':horizon,'source_upper_odd':bound,'source_rows':rows,
            'original_return_equations_replayed':edges,'original_divisions_replayed':halvings,
            'source_ledger_uncompressed_sha256':sha.hexdigest(),
            'maximum_first_crossing_returns':longest,'maximum_first_crossing_source':longest_source,
            'maximum_odd_vertex_in_first_crossing_paths':peak,'peak_path_source':peak_source,
            'maximum_inductive_total_odd_returns':max_height,'maximum_total_source':max_height_source,
            'crossing_length_histogram':{str(k):v for k,v in sorted(histogram.items())},
            'shortened_first_crossing_step_histogram':{str(k):v for k,v in sorted(shorthist.items())},
            'height_table_little_endian_sha256':hsha.hexdigest(),
            'imports_main_or_predecessor':False,'all_rows_checked':True,
            'external_logarithm_theorem_used':False,'maximum_candidate_record':max(bounds,key=lambda row:row[2])}

def main() -> None:
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--horizon',type=int,default=10280)
    ap.add_argument('--ledger',type=Path,required=True);ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args()
    try:
        result=audit(a.horizon,a.ledger);a.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
        print(json.dumps({k:result[k] for k in ('status','horizon','source_rows','original_return_equations_replayed','original_divisions_replayed','source_ledger_uncompressed_sha256')},sort_keys=True))
    except AuditError as exc:ap.error(str(exc))
if __name__=='__main__':main()
