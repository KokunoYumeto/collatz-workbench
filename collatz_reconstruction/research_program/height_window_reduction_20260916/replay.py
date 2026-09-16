#!/usr/bin/env python3
"""Replay source identities, structural checks, and the complete proof window.

Default execution reruns the two structural checks. --full adds both complete
source scans plus an independently implemented streaming audit. --predecessor
also replays the published first-jet pair. No network or optional package is used.
The ledger is regenerated in a temporary directory unless --keep-ledger is set.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent

def need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)

def run(script: Path, *arguments: str, optimized: bool=False) -> None:
    command=[sys.executable]
    if optimized:
        command.append('-O')
    command.extend(['-B', str(script), *arguments])
    subprocess.run(command, check=True, cwd=HERE)

def identical(a: Path, b: Path) -> None:
    need(a.read_bytes()==b.read_bytes(), f'nonidentical replay: {a.name}, {b.name}')

def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--full',action='store_true')
    parser.add_argument('--predecessor',action='store_true')
    parser.add_argument('--keep-ledger',type=Path)
    args=parser.parse_args()
    try:
        entries=0
        for line in (HERE/'MANIFEST.sha256').read_text(encoding='utf-8').splitlines():
            digest,name=line.split('  ',1)
            relative=Path(name)
            need(not relative.is_absolute() and '..' not in relative.parts, 'unsafe manifest path')
            target=HERE/relative
            need(target.is_file(), f'missing manifested source: {name}')
            need(hashlib.sha256(target.read_bytes()).hexdigest()==digest, f'source identity mismatch: {name}')
            entries+=1
        if args.predecessor:
            run(HERE.parent/'intrinsic_zero_firstjet_20260915'/'replay.py')
        for optimized in (False,True):
            run(HERE/'verify.py','--check',str(HERE/'verification.json'),optimized=optimized)
        if args.full:
            with tempfile.TemporaryDirectory(prefix='collatz-height-window-') as tmp:
                temp=Path(tmp)
                ledger=args.keep_ledger.resolve() if args.keep_ledger else temp/'sources.jsonl.gz'
                ordinary=temp/'scan.json'; optimized_output=temp/'scan_O.json'
                independent=temp/'audit.json'; envelope=temp/'envelope.json'
                run(HERE/'scan_sources.py','--horizon','10280','--ledger',str(ledger),
                    '--output',str(ordinary),'--envelope-output',str(envelope))
                run(HERE/'scan_sources.py','--horizon','10280','--output',str(optimized_output),optimized=True)
                identical(ordinary,optimized_output)
                identical(ordinary,HERE/'source_scan.json')
                identical(envelope,HERE/'envelope.json')
                run(HERE/'audit_sources.py','--horizon','10280','--ledger',str(ledger),'--output',str(independent))
                identical(independent,HERE/'independent_source_audit.json')
        print(json.dumps({'status':'PASS','source_manifest_entries':entries,
            'structural_replays':2,'full_source_scans':2 if args.full else 0,
            'independent_all_source_audits':1 if args.full else 0,
            'predecessor_pair_replayed':args.predecessor},sort_keys=True))
    except (ValueError,OSError,subprocess.CalledProcessError) as exc:
        parser.error(str(exc))

if __name__=='__main__':
    main()
