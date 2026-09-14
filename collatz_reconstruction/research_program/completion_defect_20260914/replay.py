#!/usr/bin/env python3
"""Check the exact local manifest and replay the new ordinary/optimized pair."""
from pathlib import Path
import hashlib
import subprocess
import sys

HERE=Path(__file__).resolve().parent

def main() -> None:
    for line in (HERE/'MANIFEST.sha256').read_text().splitlines():
        expected,name=line.split('  ',1)
        if Path(name).name!=name:
            raise RuntimeError('Manifest path must be a local basename')
        actual=hashlib.sha256((HERE/name).read_bytes()).hexdigest()
        if actual!=expected:
            raise RuntimeError('Source mismatch: '+name)
    reference=(HERE/'verification.json').read_bytes()
    for flags in [[],['-O']]:
        command=[sys.executable,*flags,'-B',str(HERE/'verify.py')]
        run=subprocess.run(command,cwd=HERE,capture_output=True,timeout=120,check=True)
        if run.stdout!=reference:
            raise RuntimeError('Verification output mismatch: '+' '.join(flags))
        if run.stderr:
            raise RuntimeError('Unexpected stderr: '+run.stderr.decode())
        print('PASS', 'optimized' if flags else 'ordinary',
              hashlib.sha256(run.stdout).hexdigest())
    print('PASS source manifest and both completion-defect executions')

if __name__=='__main__':
    main()
