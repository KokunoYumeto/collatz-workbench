#!/usr/bin/env python3
"""Preview or apply the verified additive research files to an existing checkout.

Default selects only this turn's all-even-exponent contribution and workflow.
--all-supplied additionally selects the archival research overlay (not a clone).
No commit, push, branch, merge, deletion, or differing-file overwrite is performed.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from safe_files import apply_additions

ROOT=Path(__file__).resolve().parents[1]
NEW='collatz_reconstruction/research_program/all_even_join_extension_20260916/'
FLOW='.github/workflows/collatz-all-even-join-extension.yml'


def load_payload(all_supplied: bool) -> dict[str,bytes]:
    manifest=json.loads((ROOT/'provenance/REPOSITORY_FILES.json').read_text())
    out={}
    for name,row in manifest['files'].items():
        if not all_supplied and not(name.startswith(NEW) or name==FLOW):
            continue
        p=ROOT/'repository'/name
        if p.is_symlink():raise ValueError('Source symlink: '+name)
        data=p.read_bytes()
        if hashlib.sha256(data).hexdigest()!=row['sha256'] or len(data)!=row['bytes']:
            raise ValueError('Archival source differs: '+name)
        out[name]=data
    if not out:raise ValueError('No selected files')
    return out


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('checkout',type=Path)
    ap.add_argument('--apply',action='store_true')
    ap.add_argument('--all-supplied',action='store_true')
    a=ap.parse_args()
    try:r=apply_additions(a.checkout,load_payload(a.all_supplied),apply=a.apply)
    except (OSError,ValueError) as e:ap.exit(1,f'No conflicting files were replaced: {e}\n')
    print(json.dumps({'selected':'all archival source' if a.all_supplied else 'new contribution only',
                      'result':r,'git_refs_modified':False},indent=2))

if __name__=='__main__':main()
