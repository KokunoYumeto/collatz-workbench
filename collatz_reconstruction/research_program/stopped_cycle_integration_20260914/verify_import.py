#!/usr/bin/env python3
"""Verify every frozen import byte, then replay the original six executions."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--hashes-only', action='store_true')
    args = parser.parse_args()
    manifest = json.loads((HERE/'PAYLOAD_MANIFEST.json').read_text(encoding='utf-8'))
    rows = manifest['files']
    if manifest['file_count'] != 21 or len(rows) != 21:
        raise RuntimeError('Expected exactly 21 frozen payload files')
    seen = set()
    size = 0
    for row in rows:
        relative = Path(row['path'])
        if relative.is_absolute() or '..' in relative.parts or row['path'] in seen:
            raise RuntimeError('Invalid or duplicate manifest path')
        seen.add(row['path'])
        path = ROOT/relative
        if path.is_symlink() or not path.is_file():
            raise RuntimeError('Missing or symlinked import: '+row['path'])
        data = path.read_bytes()
        if len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256']:
            raise RuntimeError('Frozen import differs: '+row['path'])
        size += len(data)
    print(json.dumps({'status':'PASS', 'frozen_payload_files':len(seen),
                      'frozen_payload_bytes':size}, sort_keys=True), flush=True)
    if not args.hashes_only:
        replay = HERE.parent/'cycle_relative_cohomology_20260914'/'replay_all.py'
        subprocess.run([sys.executable, '-B', str(replay)], cwd=ROOT, check=True, timeout=600)


if __name__ == '__main__':
    main()
