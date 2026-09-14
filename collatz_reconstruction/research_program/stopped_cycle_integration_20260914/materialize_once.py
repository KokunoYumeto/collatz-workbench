#!/usr/bin/env python3
"""Rebuild only three absent deterministic result files, checking original bytes."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PREFIX = 'collatz_reconstruction/research_program/'
OLD = PREFIX + 'stopped_affine_transport_20260914/'
NEW = PREFIX + 'cycle_relative_cohomology_20260914/'
WORKFLOW = '.github/workflows/collatz-stopped-cycle-cohomology.yml'
JOBS = ((OLD+'verify.py', OLD+'verification.json'),
        (OLD+'make_certificate.py', OLD+'example_certificate.json'),
        (NEW+'verify.py', NEW+'verification.json'))


def require(ok: bool, text: str) -> None:
    if not ok:
        raise RuntimeError(text)


def check_file(row: dict) -> None:
    path = ROOT / row['path']
    require(path.is_file() and not path.is_symlink(), 'Missing or symlinked file: '+row['path'])
    data = path.read_bytes()
    require(len(data) == row['bytes'], 'Byte length mismatch: '+row['path'])
    require(hashlib.sha256(data).hexdigest() == row['sha256'], 'Hash mismatch: '+row['path'])


def main() -> None:
    rows = json.loads((HERE/'PAYLOAD_MANIFEST.json').read_text(encoding='utf-8'))['files']
    require(len(rows) == 21, 'Expected exactly 21 frozen payload entries')
    expected = {row['path']: row for row in rows}
    require(len(expected) == 21, 'Duplicate payload path')
    for name in expected:
        p = Path(name)
        require(not p.is_absolute() and '..' not in p.parts, 'Unsafe payload path')
    results = {target for _,target in JOBS}
    delayed = results | {WORKFLOW}
    for row in rows:
        path = ROOT/row['path']
        if row['path'] in delayed:
            require(not path.exists() and not path.is_symlink(), 'Refusing to replace: '+row['path'])
        else:
            check_file(row)
    for program,target in JOBS:
        subprocess.run([sys.executable, '-B', str(ROOT/program), '--output', str(ROOT/target)],
                       cwd=(ROOT/program).parent, check=True, timeout=600)
        check_file(expected[target])
    for row in rows:
        if row['path'] != WORKFLOW:
            check_file(row)
    subprocess.run([sys.executable, '-B', str(ROOT/NEW/'replay_all.py')],
                   cwd=ROOT, check=True, timeout=600)
    print(json.dumps({'status':'PASS', 'frozen_files_checked':20,
                      'generated_files':sorted(results),
                      'original_result_bytes_matched':True}, sort_keys=True))


if __name__ == '__main__':
    main()
