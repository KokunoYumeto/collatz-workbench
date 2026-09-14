#!/usr/bin/env python3
"""Replay both unchanged/new contributions without writing into the source tree."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
OLD = HERE.parent/'stopped_affine_transport_20260914'


def verify_manifest(base: Path) -> int:
    count=0
    for line in (base/'MANIFEST.sha256').read_text(encoding='utf-8').splitlines():
        expected,name=line.split(maxsplit=1)
        name=name.lstrip('*')
        if Path(name).name != name:
            raise RuntimeError('Manifest must use local file names: '+name)
        target=base/name
        if target.is_symlink() or not target.is_file():
            raise RuntimeError('Missing or symlinked source: '+str(target))
        actual=hashlib.sha256(target.read_bytes()).hexdigest()
        if actual!=expected:
            raise RuntimeError('Source hash mismatch: '+str(target))
        count+=1
    return count


def main() -> None:
    hashes=verify_manifest(OLD)+verify_manifest(HERE)
    receipts=[]
    with tempfile.TemporaryDirectory(prefix='collatz-replay-') as td:
        for label,base,program,reference in (
            ('stopped',OLD,'verify.py','verification.json'),
            ('support',OLD,'make_certificate.py','example_certificate.json'),
            ('cycles',HERE,'verify.py','verification.json'),
        ):
            for optimized in (False,True):
                output=Path(td)/(label+('_O' if optimized else '')+'.json')
                command=[sys.executable]+(['-O'] if optimized else [])+[str(base/program),'--output',str(output)]
                run=subprocess.run(command,cwd=base,check=True,capture_output=True,text=True)
                if output.read_bytes()!=(base/reference).read_bytes():
                    raise RuntimeError('Replay differs from committed result: '+label)
                receipts.append({'suite':label,'optimized':optimized,'byte_identical':True,
                                 'stdout':run.stdout.strip()})
    print(json.dumps({'status':'PASS','manifest_entries':hashes,'replays':receipts},indent=2,sort_keys=True))


if __name__=='__main__': main()
