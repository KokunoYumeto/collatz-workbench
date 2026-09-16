#!/usr/bin/env python3
"""Read-only source validation and ordinary/optimized exact replay."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent


def require(ok: bool, message: str) -> None:
    if not ok:raise RuntimeError(message)


def main() -> None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--predecessor',action='store_true')
    ap.add_argument('--atlas',action='store_true',help='also check optional earlier atlas crosswalk')
    args=ap.parse_args()
    entries=(HERE/'MANIFEST.sha256').read_text().splitlines()
    for line in entries:
        digest,name=line.split('  ',1);path=Path(name)
        require(not path.is_absolute() and '..' not in path.parts,'unsafe manifest path')
        require(hashlib.sha256((HERE/path).read_bytes()).hexdigest()==digest,'changed new source: '+name)
    commands=[]
    if args.predecessor:
        commands.append([sys.executable,'-B',str(HERE.parent/'intrinsic_zero_firstjet_20260915'/'replay.py')])
    for mode in ([],['-O']):commands.append([sys.executable,*mode,'-B',str(HERE/'verify.py'),'--check'])
    if args.atlas:commands.append([sys.executable,'-B',str(HERE/'crosscheck_atlas.py'),'--check'])
    for command in commands:
        result=subprocess.run(command,cwd=HERE,capture_output=True,text=True,check=False)
        print(result.stdout,end='',flush=True)
        require(result.returncode==0,'failed replay: '+' '.join(command)+'\n'+result.stderr)
    record=json.loads((HERE/'verification.json').read_text())
    print(json.dumps({'status':'PASS','manifest_entries':len(entries),'new_replays':2,
                      'ordinary_optimized_byte_identical':True,'named_checks_per_run':record['named_exact_checks'],
                      'predecessor_replayed':args.predecessor,'optional_atlas_crosswalk':args.atlas},sort_keys=True))


if __name__=='__main__':
    try:main()
    except (OSError,RuntimeError,ValueError) as exc:raise SystemExit(str(exc))
