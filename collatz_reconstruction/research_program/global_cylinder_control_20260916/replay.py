#!/usr/bin/env python3
"""Source identities, original receiver, and ordinary/optimized exact replays."""
from __future__ import annotations
import argparse
import hashlib
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--predecessor',action='store_true',help='also replay the unchanged first-jet pair')
    ap.add_argument('--mode',choices=['both','ordinary','optimized'],default='both')
    args=ap.parse_args()
    for line in (HERE/'MANIFEST.sha256').read_text().splitlines():
        digest,name=line.split('  ',1)
        path=(HERE/name).resolve()
        if path.parent!=HERE:raise ValueError('manifest path outside contribution')
        if hashlib.sha256(path.read_bytes()).hexdigest()!=digest:raise ValueError('source identity mismatch: '+name)
    if args.predecessor:
        subprocess.run([sys.executable,'-B',str(HERE.parent/'intrinsic_zero_firstjet_20260915'/'replay.py')],check=True)
    for optimized in (False,True):
        if args.mode=='ordinary' and optimized:continue
        if args.mode=='optimized' and not optimized:continue
        command=[sys.executable]+(['-O'] if optimized else [])+['-B',str(HERE/'verify.py'),'--check',str(HERE/'verification.json')]
        subprocess.run(command,check=True)
    print('PASS source manifest and requested global-cylinder replays')

if __name__=='__main__':main()
