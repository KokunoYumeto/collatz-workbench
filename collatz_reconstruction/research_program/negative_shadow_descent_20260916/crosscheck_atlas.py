#!/usr/bin/env python3
"""Optional original-source crosswalk to the pending, unchanged descent atlas.

This is not a dependency of the all-length shadow theorem. It merely identifies
which previously recorded full cylinders instantiate the new rule.
"""
from __future__ import annotations
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import shadow_descent as sd

HERE=Path(__file__).resolve().parent


def canonical(value) -> bytes:
    return (json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode()


def compute(path: Path) -> dict:
    data=gzip.decompress(path.read_bytes())
    atlas=json.loads(data)
    sd.require(atlas['forcing']==1,'original +1 forcing required')
    low,high=atlas['odd_source_interval']
    sd.require((low,high)==(3,1166399),'unexpected prior source interval')
    found=[];by_anchor=Counter();points=mixed_points=mixed_cells=0
    for index,cell in enumerate(atlas['cells']):
        word=tuple(cell['word']);hits=[]
        for h,p in sd.ANCHORS.items():
            for r in range(1,(len(word)-1)//len(p)+1):
                if word[:r*len(p)]!=p*r:break
                tail=word[r*len(p):]
                if any(a<2 for a in tail):continue
                rec=sd.family(h,r,tail)
                sd.require(rec['strict_descent_for_whole_cylinder'],'prior first-descent word lacks the proved crossing')
                for old,new in [('L','original_L'),('U','original_U'),('C','original_C'),
                                ('source_anchor','source_anchor'),('source_step','source_step'),
                                ('target_anchor','target_anchor'),('target_step','target_step')]:
                    sd.require(cell[old]==rec[new],'original atlas/family coefficient differs: '+old)
                hits.append([h,r,list(tail)])
        if hits:
            h,r,_=hits[0];by_anchor[h]+=1
            left=max(cell['lower_parameter'],(low-cell['source_anchor']+cell['source_step']-1)//cell['source_step'])
            right=(high-cell['source_anchor'])//cell['source_step']
            if cell['upper_parameter'] is not None:right=min(right,cell['upper_parameter'])
            count=max(0,right-left+1);points+=count
            if h==17 or r>=2:mixed_cells+=1;mixed_points+=count
            found.append({'cell_index':index,'discovery_seed':cell['discovery_seed'],
                          'source_anchor':cell['source_anchor'],'word':list(word),
                          'matches':hits,'covered_interval_points':count})
    return {'status':'PASS','prior_atlas_raw_sha256':hashlib.sha256(data).hexdigest(),
            'source_interval':[low,high],'matching_cells':len(found),'by_anchor':dict(by_anchor),
            'covered_interval_points':points,'multiple_rise_run_cells':mixed_cells,
            'multiple_rise_run_interval_points':mixed_points,'matches':found,
            'new_starting_integers_discovered':0,'all_length_theorem_depends_on_this_atlas':False}


def main() -> None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--atlas',type=Path,default=HERE.parent/'defect_rank_descent_20260915'/'atlas.json.gz')
    ap.add_argument('--write',action='store_true')
    ap.add_argument('--check',action='store_true')
    args=ap.parse_args();result=compute(args.atlas);data=canonical(result)
    if args.write:(HERE/'atlas_crosscheck.json').write_bytes(data)
    if args.check:sd.require((HERE/'atlas_crosscheck.json').read_bytes()==data,'original atlas crosswalk changed')
    print(json.dumps({k:v for k,v in result.items() if k!='matches'},sort_keys=True))


if __name__=='__main__':
    try:main()
    except (OSError,ValueError) as exc:raise SystemExit(str(exc))
