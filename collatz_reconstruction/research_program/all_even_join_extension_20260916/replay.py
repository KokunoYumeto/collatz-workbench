#!/usr/bin/env python3
"""Exact replay of this addition; no network or write to any Git reference."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,tempfile
root=Path(__file__).resolve().parent
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--predecessor',action='store_true',help='Also run the unchanged original first-jet pair')
args=ap.parse_args()
manifest=json.loads((root/'MANIFEST.json').read_text())
for name,digest in manifest['files'].items():
    p=root/name
    if hashlib.sha256(p.read_bytes()).hexdigest()!=digest:
        raise RuntimeError('Source identity mismatch: '+name)
base=root.parent/'bilateral_root_bounds_20260916'/'bilateral_control.py'
if hashlib.sha256(base.read_bytes()).hexdigest()!=manifest['bilateral_sha256']:
    raise RuntimeError('Original bilateral dependency differs')
if args.predecessor:
    subprocess.run([sys.executable,'-B',str(root.parent/'intrinsic_zero_firstjet_20260915'/'replay.py')],check=True)
for options in ([],['-O']):
    subprocess.run([sys.executable,*options,'-B',str(root/'verify.py'),'--check',str(root/'verification.json')],check=True)
with tempfile.TemporaryDirectory() as t:
    target=Path(t)/'audit.json'
    subprocess.run([sys.executable,'-B',str(root/'audit_families.py'),str(root/'family_cases.jsonl.gz'),'--output',str(target)],check=True)
    if target.read_bytes()!=(root/'family_audit.json').read_bytes():
        raise RuntimeError('Independent all-row audit differs from its recorded result')
print(json.dumps({'status':'PASS','original_source_files_checked':len(manifest['files']),
                  'ordinary_optimized_identical':True,'independent_all_row_audit_matched':True,
                  'original_firstjet_pair_run':args.predecessor,
                  'full_historical_repository_replay':False}))
