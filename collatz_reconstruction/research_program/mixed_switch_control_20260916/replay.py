#!/usr/bin/env python3
"""Verify source identities and regenerate the complete exact result in both modes."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parent
for line in (root/'MANIFEST.sha256').read_text(encoding='utf-8').splitlines():
    expected, name = line.split('  ', 1)
    actual = hashlib.sha256((root/name).read_bytes()).hexdigest()
    if actual != expected:
        raise RuntimeError('source identity mismatch: '+name)
receipt = json.loads((root/'verification.json').read_text(encoding='utf-8'))
with tempfile.TemporaryDirectory(prefix='collatz-mixed-switch-') as temp:
    previous = None
    for optimized in (False, True):
        out = Path(temp)/('optimized.json' if optimized else 'ordinary.json')
        cmd = [sys.executable, '-B']+(['-O'] if optimized else [])
        cmd += [str(root/'verify.py'), '--output', str(out)]
        subprocess.run(cmd, check=True, cwd=root, timeout=180)
        raw = out.read_bytes()
        if len(raw) != receipt['full_result_bytes'] or hashlib.sha256(raw).hexdigest() != receipt['full_result_sha256']:
            raise RuntimeError('complete result differs from recorded identity')
        if previous is not None and raw != previous:
            raise RuntimeError('ordinary/optimized result differs')
        previous = raw
print(json.dumps({'status':'PASS','ordinary_optimized_byte_identical':True,
                  'exact_checks_per_run':receipt['total_exact_checks'],
                  'gap_rows':receipt['gap_scan']['rows']},sort_keys=True))
