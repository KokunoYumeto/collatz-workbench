#!/usr/bin/env python3
"""Check exact source identities, finite arithmetic proofs, and both replays."""
from __future__ import annotations
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent


def require(ok: bool, message: str) -> None:
    if not ok:raise RuntimeError(message)


def run(command: list[str]) -> dict:
    result=subprocess.run(command,cwd=HERE,text=True,capture_output=True,check=False)
    require(result.returncode==0,
            'Replay failed: '+' '.join(command)+'\n'+result.stdout+'\n'+result.stderr)
    print(result.stdout,end='',flush=True)
    return {'argv':command[1:],'stdout':result.stdout.strip(),'status':'PASS'}


def main() -> None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--predecessors',action='store_true',help='also run four unchanged predecessor executions')
    ap.add_argument('--rebuild-atlas',action='store_true',help='regenerate the complete symbolic atlas and compare raw bytes')
    args=ap.parse_args()
    manifest=HERE/'MANIFEST.sha256'
    entries=manifest.read_text().splitlines()
    for line in entries:
        digest,name=line.split('  ',1)
        path=Path(name)
        require(not path.is_absolute() and '..' not in path.parts,'unsafe manifest path')
        require(hashlib.sha256((HERE/path).read_bytes()).hexdigest()==digest,'source hash mismatch: '+name)
    intake=json.loads((HERE/'SOURCE_INTAKE.json').read_text())
    root=HERE.parents[2]
    for row in intake['required_predecessor_files']:
        path=root/row['repository_path']
        data=path.read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        require(actual==row['git_blob'],'predecessor blob mismatch: '+row['repository_path'])
    executions=[]
    if args.predecessors:
        firstjet=HERE.parent/'intrinsic_zero_firstjet_20260915'
        executions.append(run([sys.executable,'-B',str(firstjet/'replay.py')]))
        structural=HERE.parent/'supported_structure_20260915'
        for mode in ([],['-O']):
            executions.append(run([sys.executable,*mode,'-B',str(structural/'verify.py'),
                                   '--check',str(structural/'verification.json')]))
    if args.rebuild_atlas:
        with tempfile.TemporaryDirectory(prefix='collatz-atlas-rebuild-') as d:
            output=Path(d)/'atlas.json.gz'
            executions.append(run([sys.executable,'-B',str(HERE/'atlas.py'),'build',
                                   '--bound','1166399','--output',str(output)]))
            require(gzip.decompress(output.read_bytes())==gzip.decompress((HERE/'atlas.json.gz').read_bytes()),
                    'regenerated atlas differs in its original canonical data')
            print('PASS independently regenerated atlas bytes',flush=True)
    for mode in ([],['-O']):
        executions.append(run([sys.executable,*mode,'-B',str(HERE/'verify.py'),
                               '--check',str(HERE/'verification.json')]))
    print(json.dumps({'status':'PASS','manifested_files':len(entries),
                      'new_replays':2,'ordinary_optimized_byte_identical':True,
                      'predecessor_executions':4 if args.predecessors else 0,
                      'atlas_regenerated':args.rebuild_atlas,
                      'verification_sha256':hashlib.sha256((HERE/'verification.json').read_bytes()).hexdigest()},sort_keys=True))


if __name__=='__main__':
    try:main()
    except (RuntimeError,OSError,ValueError) as exc:raise SystemExit(str(exc))
