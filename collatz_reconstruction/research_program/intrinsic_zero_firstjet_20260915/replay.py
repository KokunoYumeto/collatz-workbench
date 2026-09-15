#!/usr/bin/env python3
"""Check all declared source bytes and both first-jet regression executions."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile

root=Path(__file__).resolve().parent
for line in (root/'MANIFEST.sha256').read_text().splitlines():
    digest,name=line.split('  ',1)
    if hashlib.sha256((root/name).read_bytes()).hexdigest()!=digest:
        raise RuntimeError('source hash mismatch: '+name)
reference=(root/'verification.json').read_bytes()
with tempfile.TemporaryDirectory(prefix='collatz-firstjet-') as folder:
    for optimized in (False,True):
        out=Path(folder)/('optimized.json' if optimized else 'ordinary.json')
        cmd=[sys.executable,'-B']+(['-O'] if optimized else [])+[str(root/'verify.py'),'--output',str(out)]
        subprocess.run(cmd,check=True,cwd=root,timeout=180)
        if out.read_bytes()!=reference:
            raise RuntimeError('first-jet result mismatch')
print(json.dumps({'status':'PASS','ordinary_optimized_byte_identical':True,
                  'exact_checks_per_run':json.loads(reference)['total_checks']},sort_keys=True))
