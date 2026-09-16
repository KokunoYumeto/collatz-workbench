#!/usr/bin/env python3
"""Verify the delivered files and original ZIP members; no mathematics is inferred."""
from pathlib import Path
import argparse,hashlib,json,zipfile

ROOT=Path(__file__).resolve().parents[1]

def sha256_file(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--skip-zip-crc',action='store_true')
    a=ap.parse_args()
    data=json.loads((ROOT/'MANIFEST.json').read_text());count=0
    for name,row in data['files'].items():
        p=ROOT/name
        if p.is_symlink() or not p.is_file() or p.stat().st_size!=row['bytes'] or sha256_file(p)!=row['sha256']:
            raise RuntimeError('Archive identity mismatch: '+name)
        count+=1
    zcount=0
    if not a.skip_zip_crc:
        for p in sorted((ROOT/'source_archives').glob('*.zip')):
            with zipfile.ZipFile(p) as z:
                failed=z.testzip()
                if failed:raise RuntimeError('ZIP CRC failure: '+str(p)+'!'+failed)
                zcount+=1
    print(json.dumps({'status':'PASS','checked_files':count,'original_zip_crc_checks':zcount,
                      'mathematical_proof_audit':False},indent=2))
if __name__=='__main__':main()
