#!/usr/bin/env python3
"""Check the added manifest, six preserved replays, and two new exact replays."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def main() -> None:
    seen = set()
    for line in (HERE/'MANIFEST.sha256').read_text(encoding='utf-8').splitlines():
        digest, name = line.split('  ', 1)
        relative = Path(name)
        if relative.is_absolute() or '..' in relative.parts or name in seen:
            raise RuntimeError('Invalid or duplicate manifest path')
        seen.add(name)
        path = HERE/relative
        if path.is_symlink() or not path.is_file():
            raise RuntimeError('Missing or symlinked source: '+name)
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise RuntimeError('Source hash differs: '+name)
    if len(seen) != 9:
        raise RuntimeError('Expected exactly nine manifested continuation files')
    predecessor = HERE.parent/'stopped_cycle_integration_20260914'/'verify_import.py'
    subprocess.run([sys.executable, '-B', str(predecessor)], cwd=ROOT, check=True, timeout=600)
    expected = (HERE/'verification.json').read_bytes()
    with tempfile.TemporaryDirectory(prefix='collatz-residual-replay-') as temporary:
        for optimized in (False, True):
            target = Path(temporary)/('optimized.json' if optimized else 'ordinary.json')
            command = [sys.executable]+(['-O'] if optimized else [])
            command += ['-B', str(HERE/'verify.py'), '--output', str(target)]
            subprocess.run(command, cwd=ROOT, check=True, timeout=600)
            if target.read_bytes() != expected:
                raise RuntimeError('New replay differs from the committed result')
    result = json.loads(expected)
    print(json.dumps({'status': 'PASS', 'manifested_new_files': len(seen),
                      'new_checks_per_run': result['exact_checks'],
                      'preserved_replays': 6, 'new_replays': 2,
                      'ordinary_optimized_byte_identical': True}, sort_keys=True))


if __name__ == '__main__':
    main()
