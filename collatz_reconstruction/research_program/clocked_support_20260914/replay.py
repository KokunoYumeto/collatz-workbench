#!/usr/bin/env python3
"""Verify preserved sources, the original eight runs, the database and two new runs."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def digest(path: Path) -> str:
    if path.is_symlink() or not path.is_file():
        raise RuntimeError('Missing or symlinked input: '+str(path))
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_relative(text: str) -> Path:
    p = Path(text)
    if p.is_absolute() or '..' in p.parts:
        raise RuntimeError('Invalid relative path: '+text)
    return p


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--new-only', action='store_true',
                        help='Verify all source hashes and replay only the two new executions')
    args = parser.parse_args()
    seen = set()
    for line in (HERE/'MANIFEST.sha256').read_text(encoding='utf-8').splitlines():
        expected, name = line.split('  ', 1)
        if name in seen or digest(HERE/safe_relative(name)) != expected:
            raise RuntimeError('New source hash differs or path repeats: '+name)
        seen.add(name)
    if len(seen) != 11:
        raise RuntimeError('Expected exactly eleven manifested continuation files')
    base = json.loads((HERE/'BASE_FILES.json').read_text())
    if base['source_commit'] != '6a30f1dc23110fae0abbe3b3bd5e60072a842385':
        raise RuntimeError('Inherited commit identity changed')
    for row in base['preserved_files']:
        path = ROOT/safe_relative(row['path'])
        if digest(path) != row['sha256'] or path.stat().st_size != row['bytes']:
            raise RuntimeError('Inherited source differs: '+row['path'])
    if len(base['preserved_files']) != 36:
        raise RuntimeError('Expected the complete 36-file inherited payload')
    if not args.new_only:
        subprocess.run([sys.executable, '-B', str(HERE.parent/'residual_splice_20260914'/'replay.py')],
                       cwd=ROOT, check=True, timeout=600)
    expected = (HERE/'verification.json').read_bytes()
    with tempfile.TemporaryDirectory(prefix='collatz-clocked-replay-') as temp:
        folder = Path(temp)
        generated = folder/'database.json.gz'
        subprocess.run([sys.executable, '-B', str(HERE/'sector_certificate.py'), '--generate', str(generated)],
                       cwd=ROOT, check=True, timeout=600, stdout=subprocess.PIPE)
        if gzip.decompress(generated.read_bytes()) != gzip.decompress((HERE/'source_database.json.gz').read_bytes()):
            raise RuntimeError('Canonical original-source database regeneration differs')
        for optimized in (False, True):
            result = folder/('optimized.json' if optimized else 'ordinary.json')
            command = [sys.executable]+(['-O'] if optimized else [])
            command += ['-B', str(HERE/'verify.py'), '--output', str(result)]
            subprocess.run(command, cwd=ROOT, check=True, timeout=600)
            if result.read_bytes() != expected:
                raise RuntimeError('New verification output differs from its recorded bytes')
    data = json.loads(expected)
    print(json.dumps({'status': 'PASS', 'preserved_files': 36, 'manifested_new_files': len(seen),
                      'inherited_executions': 0 if args.new_only else 8, 'new_executions': 2,
                      'canonical_database_regeneration_byte_identical': True,
                      'ordinary_optimized_byte_identical': True,
                      'new_named_checks': data['named_check_count'],
                      'original_return_equations_replayed': data['source_database']['actual_return_equations_replayed'],
                      'excluded_all_length_rise_budget': 678}, sort_keys=True))


if __name__ == '__main__':
    main()
