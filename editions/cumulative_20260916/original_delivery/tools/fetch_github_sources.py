#!/usr/bin/env python3
"""Restore companion files from three immutable, pinned GitHub directories.

The four complete mathematical notes are already included. This optional tool
fetches the remaining original scripts, manifests and receipts, checks their Git
blob IDs, and refuses to overwrite a different file. Default: preview only.
Network access is required. GITHUB_TOKEN or GH_TOKEN is optional and never saved.
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request
from safe_files import apply_additions

ROOT = Path(__file__).resolve().parents[1]
API = 'https://api.github.com/repos/KokunoYumeto/collatz-workbench/'
REF = '9453b5306b3a897389dece309f9c119dffbcc489'
PREFIX = 'collatz_reconstruction/research_program/'
DIRECTORIES = ('history_law_cutoff_20260914', 'anchored_defect_20260914',
               'ternary_join_reduction_20260916')
MAX_TOTAL_BYTES = 256 * 1024 * 1024


def get_json(endpoint: str):
    headers = {'Accept': 'application/vnd.github+json',
               'User-Agent': 'Collatz-pinned-source-restorer',
               'X-GitHub-Api-Version': '2022-11-28'}
    token = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
    if token:
        headers['Authorization'] = 'Bearer ' + token
    req = urllib.request.Request(API + endpoint, headers=headers, method='GET')
    with urllib.request.urlopen(req, timeout=60) as r:
        if urllib.parse.urlsplit(r.url).hostname != 'api.github.com':
            raise ValueError('Unexpected API redirect')
        return json.load(r)


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def collect_payload() -> tuple[dict[str, bytes], list[dict]]:
    payload, records = {}, []
    queue = [PREFIX + d for d in DIRECTORIES]
    total = 0
    while queue:
        directory = queue.pop(0)
        items = get_json('contents/' + urllib.parse.quote(directory, safe='/') + '?ref=' + REF)
        if not isinstance(items, list):
            raise ValueError('Expected a directory listing: ' + directory)
        for item in sorted(items, key=lambda i: i['path']):
            name = item['path']
            if not name.startswith(directory + '/'):
                raise ValueError('API path outside requested directory')
            if item['type'] == 'dir':
                queue.append(name)
                continue
            if item['type'] != 'file':
                raise ValueError('Only regular source files are accepted: ' + name)
            blob = get_json('git/blobs/' + item['sha'])
            if blob.get('encoding') != 'base64':
                raise ValueError('Unexpected blob encoding: ' + name)
            data = base64.b64decode(''.join(blob['content'].split()), validate=True)
            if git_blob(data) != item['sha'] or len(data) != item['size']:
                raise ValueError('Original blob identity mismatch: ' + name)
            total += len(data)
            if total > MAX_TOTAL_BYTES:
                raise ValueError('Restore exceeds the declared 256 MiB safety budget')
            payload[name] = data
            records.append({'path': name, 'git_blob': item['sha'], 'bytes': len(data),
                            'sha256': hashlib.sha256(data).hexdigest()})
    return payload, records


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--destination', type=Path, default=ROOT/'repository')
    ap.add_argument('--apply', action='store_true', help='Write checked missing files; otherwise preview only')
    a = ap.parse_args()
    try:
        payload, records = collect_payload()
        result = apply_additions(a.destination, payload, apply=a.apply)
    except (OSError, ValueError, urllib.error.URLError) as e:
        ap.exit(1, f'Original-source restore stopped: {e}\n')
    print(json.dumps({'ref': REF, 'repository': 'KokunoYumeto/collatz-workbench',
                      'result': result, 'files': records, 'git_refs_modified': False}, indent=2))


if __name__ == '__main__':
    main()
