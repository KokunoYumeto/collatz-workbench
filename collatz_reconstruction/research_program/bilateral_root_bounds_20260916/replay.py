#!/usr/bin/env python3
"""Rebuild the exact original-source evidence and compare recorded bytes."""
from __future__ import annotations
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]

def need(ok,message):
    if not ok:raise RuntimeError(message)

def execute(script,args,optimized=False):
    command=[sys.executable]+(['-O'] if optimized else [])+['-B',str(HERE/script)]+[str(x) for x in args]
    subprocess.run(command,check=True,cwd=ROOT)

def check_manifest():
    manifest=json.loads((HERE/'MANIFEST.json').read_text())
    for name,expected in manifest['local_files'].items():
        need(Path(name).name==name,'manifest local file must have one component')
        need(hashlib.sha256((HERE/name).read_bytes()).hexdigest()==expected,'source hash mismatch: '+name)
    workflow=manifest['workflow']
    need(hashlib.sha256((ROOT/workflow['path']).read_bytes()).hexdigest()==workflow['sha256'],'workflow identity mismatch')
    source=HERE.parent/'intrinsic_zero_firstjet_20260915'/'firstjet.py'
    data=source.read_bytes()
    need(hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==manifest['firstjet_git_blob'],'original first-jet dependency differs')

def run(args,folder):
    check_manifest();folder.mkdir(parents=True,exist_ok=True)
    if args.predecessor:
        subprocess.run([sys.executable,'-B',str(HERE.parent/'intrinsic_zero_firstjet_20260915'/'replay.py')],check=True,cwd=ROOT)
    structural=folder/'structural.json';optimized=folder/'structural_optimized.json';pairs=folder/'all_join_pairs.jsonl.gz'
    execute('verify.py',['--output',structural,'--ledger',pairs])
    execute('verify.py',['--output',optimized],True)
    expected=(HERE/'verification.json').read_bytes()
    need(structural.read_bytes()==optimized.read_bytes()==expected,'structural ordinary/optimized/recorded bytes differ')
    af=folder/'independent_family_audit.json'
    execute('audit_families.py',['--ledger',pairs,'--output',af])
    need(af.read_bytes()==(HERE/'family_audit.json').read_bytes(),'independent family audit differs')
    subprocess.run([sys.executable,'-B',str(HERE/'test_audits.py')],check=True,cwd=ROOT)
    if args.full:
        ledger=folder/'sources11610.jsonl.gz';ordinary=folder/'source_scan.json';opt=folder/'source_scan_optimized.json';audit=folder/'independent_source_audit.json'
        execute('scan_sources.py',['--horizon',11610,'--ledger',ledger,'--output',ordinary,'--envelope-output',folder/'envelope11610.json'])
        execute('scan_sources.py',['--horizon',11610,'--output',opt],True)
        need(ordinary.read_bytes()==opt.read_bytes(),'source ordinary/optimized bytes differ')
        execute('audit_sources.py',['--horizon',11610,'--ledger',ledger,'--output',audit])
        window=json.loads((HERE/'window_certificate.json').read_text())
        need(json.loads(ordinary.read_text())==window['producer'],'complete source scan differs from receipt')
        need(json.loads(audit.read_text())==window['independent_audit'],'complete independent source audit differs')
        for key in ('source_rows','source_upper_odd','source_ledger_uncompressed_sha256','height_table_little_endian_sha256'):
            need(window['producer'][key]==window['independent_audit'][key],'producer/auditor mismatch: '+key)
    print(json.dumps({'status':'PASS','full_source_scan':args.full,'predecessor_pair':args.predecessor,
                      'ordinary_optimized_byte_identical':True,'complete_pair_rows':112050,
                      'structural_exact_checks_per_run':1905007,'source_rows_when_full':4064632 if args.full else None},sort_keys=True),flush=True)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--full',action='store_true');parser.add_argument('--predecessor',action='store_true')
    parser.add_argument('--emit-dir',type=Path)
    args=parser.parse_args()
    if args.emit_dir:run(args,args.emit_dir.resolve())
    else:
        with tempfile.TemporaryDirectory(prefix='collatz-bilateral-replay-') as folder:run(args,Path(folder))
if __name__=='__main__':main()
