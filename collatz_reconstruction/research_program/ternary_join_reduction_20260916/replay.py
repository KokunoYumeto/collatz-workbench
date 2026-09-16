#!/usr/bin/env python3
"""Replay exact source identities, both structural modes, and the optional full window."""
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
    if not ok:raise ValueError(message)

def digest(path: Path, kind: str='sha256') -> str:
    data=path.read_bytes()
    if kind=='git-blob-sha1':
        return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    need(kind=='sha256','unknown source digest')
    return hashlib.sha256(data).hexdigest()

def run(script: Path, arguments: list[str], optimized: bool=False) -> None:
    cmd=[sys.executable]+(['-O'] if optimized else [])+['-B',str(script)]+arguments
    subprocess.run(cmd,check=True)

def replay(full: bool, predecessor: bool, work: Path) -> None:
    manifest=json.loads((HERE/'MANIFEST.json').read_text())
    for name,item in manifest['files'].items():
        p=HERE/name
        need(p.is_file() and digest(p,item['algorithm'])==item['digest'],f'changed source: {name}')
    print(json.dumps({'status':'PASS','source_identities_checked':len(manifest['files'])}),flush=True)
    if predecessor:
        run(HERE.parent/'intrinsic_zero_firstjet_20260915'/'replay.py',[])
    for opt,label in [(False,'ordinary'),(True,'optimized')]:
        run(HERE/'verify.py',['--check',str(HERE/'verification.json'),'--output',str(work/(label+'.json'))],opt)
    need((work/'ordinary.json').read_bytes()==(work/'optimized.json').read_bytes(),'structural modes differ')
    if full:
        receipt=json.loads((HERE/'window_certificate.json').read_text())
        ledger=work/'original-sources.jsonl.gz'
        ordinary=work/'source-ordinary.json';optimized=work/'source-optimized.json';audit=work/'source-audit.json'
        run(HERE/'scan_sources.py',['--horizon',str(receipt['horizon']),'--ledger',str(ledger),'--output',str(ordinary)])
        run(HERE/'scan_sources.py',['--horizon',str(receipt['horizon']),'--output',str(optimized)],True)
        need(ordinary.read_bytes()==optimized.read_bytes(),'source scan modes differ')
        need(digest(ordinary)==receipt['scan_receipt_sha256'],'source scan receipt changed')
        run(HERE/'audit_sources.py',['--horizon',str(receipt['horizon']),'--ledger',str(ledger),'--output',str(audit)])
        need(digest(audit)==receipt['audit_receipt_sha256'],'independent audit receipt changed')
        obs=json.loads(audit.read_text())
        need(obs['source_ledger_uncompressed_sha256']==receipt['source_ledger_uncompressed_sha256'],'ledger changed')
        print(json.dumps({'status':'PASS','full_source_rows':obs['source_rows'],'independent_divisions':obs['original_divisions_replayed'],'ledger_sha256':obs['source_ledger_uncompressed_sha256']}),flush=True)
    print(json.dumps({'status':'PASS','ordinary_optimized_byte_identical':True,'full_window_replayed':full,'predecessor_replayed':predecessor}),flush=True)

def main() -> None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--full',action='store_true');ap.add_argument('--predecessor',action='store_true')
    ap.add_argument('--work-dir',type=Path)
    a=ap.parse_args()
    if a.work_dir:
        a.work_dir.mkdir(parents=True,exist_ok=True);replay(a.full,a.predecessor,a.work_dir)
    else:
        with tempfile.TemporaryDirectory(prefix='collatz-ternary-') as td:replay(a.full,a.predecessor,Path(td))
if __name__=='__main__':main()
