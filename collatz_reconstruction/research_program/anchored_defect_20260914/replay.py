#!/usr/bin/env python3
"""Verify this source, all eight inherited replays, and both new outputs."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]


def main():
    seen=set()
    for line in (HERE/'MANIFEST.sha256').read_text(encoding='utf-8').splitlines():
        digest,name=line.split('  ',1)
        relative=Path(name)
        if relative.is_absolute() or '..' in relative.parts or name in seen:
            raise RuntimeError('Invalid or repeated manifest path')
        seen.add(name); source=HERE/relative
        if source.is_symlink() or not source.is_file():
            raise RuntimeError('Missing or symlinked source: '+name)
        if hashlib.sha256(source.read_bytes()).hexdigest()!=digest:
            raise RuntimeError('Changed source: '+name)
    if len(seen)!=9:
        raise RuntimeError('Expected nine manifested source/result files')
    previous=HERE.parent/'residual_splice_20260914'/'replay.py'
    subprocess.run([sys.executable,'-B',str(previous)],cwd=ROOT,check=True,timeout=600)
    expected=(HERE/'verification.json').read_bytes()
    with tempfile.TemporaryDirectory(prefix='collatz-anchored-') as tmp:
        for optimized in (False,True):
            target=Path(tmp)/('optimized.json' if optimized else 'ordinary.json')
            command=[sys.executable]+(['-O'] if optimized else [])
            command+=['-B',str(HERE/'verify.py'),'--output',str(target)]
            subprocess.run(command,cwd=ROOT,check=True,timeout=600)
            if target.read_bytes()!=expected:
                raise RuntimeError('New replay differs from the recorded exact output')
    result=json.loads(expected)
    print(json.dumps({'status':'PASS','new_exact_checks_per_run':result['exact_checks'],
                      'new_replays':2,'inherited_replays':8,
                      'ordinary_optimized_byte_identical':True,
                      'excluded_rise_budget':404},sort_keys=True))


if __name__=='__main__': main()
