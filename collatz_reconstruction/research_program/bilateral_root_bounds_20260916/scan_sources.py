#!/usr/bin/env python3
"""Produce a complete original-source proof ledger for the sharp envelope window.

Every [n, terminal, ordered_exponents] row retains an actual first-crossing
path. A row is accepted only after strict descent. A timeout or missed
crossing fails the whole-window claim. No external logarithm theorem is used.
"""
from __future__ import annotations
import argparse
from array import array
import gzip
import hashlib
import json
from pathlib import Path
from bilateral_control import envelope, CertificateError, need

def encode(x: object) -> bytes:return (json.dumps(x,separators=(',',':'),sort_keys=True)+'\n').encode()

def scan(horizon: int, ledger: Path | None=None) -> dict:
    env=envelope(horizon);bound=env['maximum_odd_candidate'];count=(bound-1)//2
    sink=None;raw=None
    if ledger:
        ledger.parent.mkdir(parents=True,exist_ok=True);raw=ledger.open('wb')
        sink=gzip.GzipFile(filename='',mode='wb',compresslevel=5,fileobj=raw,mtime=0)
    h=hashlib.sha256();returns=0;max_length=0;max_length_source=1;peak=1;peak_source=1
    lengths=array('I',[0])*((bound+1)//2)
    histogram={};short_histogram={};max_short=0;max_total=0;max_total_source=1;maximum_first_source=None
    try:
        for n in range(3,bound+1,2):
            x=n;A=0;L=1;word=[]
            for j in range(1,horizon+1):
                value=3*x+1;a=(value & -value).bit_length()-1;x=value>>a
                if x>peak:peak=x;peak_source=n
                A+=a;L*=3;word.append(a);returns+=1
                if (1<<A)>L:break
                need(x>n,'pre-crossing positive source did not increase')
            else:raise CertificateError(f'original source {n} retained at cap; no whole-window claim')
            need(x<n,f'first-crossing exception: source {n}, endpoint {x}, word {word}')
            crossing_divisions=L.bit_length()
            first_shortened=x << (A-crossing_divisions)
            need(first_shortened<n,f'shortened-map first-crossing exception at original source {n}')
            short_histogram[crossing_divisions]=short_histogram.get(crossing_divisions,0)+1
            max_short=max(max_short,crossing_divisions)
            need(x>0 and x%2==1,'original endpoint must be positive odd')
            histogram[j]=histogram.get(j,0)+1
            if j>max_length:max_length=j;max_length_source=n;maximum_first_source=[n,x,word[:]]
            total=j+lengths[x//2];need(total<2**32,'height table overflow');lengths[n//2]=total
            if total>max_total:max_total=total;max_total_source=n
            row=encode([n,x,word]);h.update(row)
            if sink:sink.write(row)
    finally:
        if sink:sink.close()
        if raw:raw.close()
    ht=hashlib.sha256()
    for value in lengths:ht.update(int(value).to_bytes(4,'little'))
    return {'status':'PASS','horizon':horizon,'source_lower_odd':3,'source_upper_odd':bound,
            'source_rows':count,'independently_replayable_original_edges':returns,
            'source_ledger_uncompressed_sha256':h.hexdigest(),
            'maximum_first_crossing_returns':max_length,'maximum_first_crossing_source':max_length_source,
            'maximum_first_crossing_witness':maximum_first_source,
            'maximum_odd_vertex_in_first_crossing_paths':peak,'peak_path_source':peak_source,
            'maximum_inductive_total_odd_returns':max_total,'maximum_total_source':max_total_source,
            'crossing_length_histogram':{str(k):v for k,v in sorted(histogram.items())},
            'shortened_first_crossing_step_histogram':{str(k):v for k,v in sorted(short_histogram.items())},
            'maximum_shortened_first_crossing_steps':max_short,
            'shortened_first_crossing_checked_before_remaining_divisions':True,
            'height_table_little_endian_sha256':ht.hexdigest(),
            'envelope_sha256':hashlib.sha256(encode(env)).hexdigest(),
            'envelope_integer_state_sha256':env['exact_big_integer_state_sha256'],
            'logarithm_estimate_used':False,'scan_results_extrapolated_without_envelope':False}

def main() -> None:
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--horizon',type=int,default=11610)
    ap.add_argument('--ledger',type=Path);ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--envelope-output',type=Path);a=ap.parse_args()
    try:
        result=scan(a.horizon,a.ledger)
        if a.envelope_output:a.envelope_output.write_bytes(encode(envelope(a.horizon)))
        a.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
        print(json.dumps({k:result[k] for k in ('status','horizon','source_rows','source_upper_odd','independently_replayable_original_edges','maximum_first_crossing_returns','source_ledger_uncompressed_sha256')},sort_keys=True))
    except CertificateError as exc:ap.error(str(exc))
if __name__=='__main__':main()
