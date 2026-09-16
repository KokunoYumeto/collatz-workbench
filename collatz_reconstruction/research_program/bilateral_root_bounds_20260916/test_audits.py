#!/usr/bin/env python3
"""Reject malformed and incomplete ledgers using the independent auditors."""
from pathlib import Path
import gzip
import json
import tempfile
import audit_families as af
import audit_sources as aus


def write_rows(path,rows):
    with path.open('wb') as raw:
        with gzip.GzipFile(filename='',fileobj=raw,mode='wb',mtime=0) as stream:
            for row in rows:
                stream.write((json.dumps(row,sort_keys=True,separators=(',',':'))+'\n').encode())


def run():
    rejected=[]
    with tempfile.TemporaryDirectory(prefix='collatz-ledger-rejections-') as folder:
        p=Path(folder)/'bad.jsonl.gz'
        original=af.expected_family((1,1),(1,1,1))
        # This candidate is in the complete declared coefficient domain.
        changed=json.loads(json.dumps(original));changed['declared_comparison_retained']=False
        endpoint=json.loads(json.dumps(original));endpoint['left_data'][2]+=1
        wrongword=json.loads(json.dumps(original));wrongword['right_word']=[0,1,1]
        family_cases=[('missing_all_families',[]),('duplicated_family',[original,original]),
                      ('lost_declared_support',[changed]),('altered_affine_numerator',[endpoint]),
                      ('invalid_original_word',[wrongword])]
        for name,rows in family_cases:
            write_rows(p,rows)
            try:af.audit(p)
            except(af.AuditError,ValueError,TypeError,KeyError):rejected.append(name)
            else:raise RuntimeError('independent family audit accepted '+name)
        valid=[3,1,[1,4]]
        write_rows(p,[valid])
        if aus.audit(3,p)['source_rows']!=1:raise RuntimeError('small valid source control failed')
        source_cases=[('missing_source',[]),('duplicate_source',[valid,valid]),
                      ('false_endpoint',[[3,3,[1,4]]]),('false_valuation',[[3,1,[2,3]]])]
        for name,rows in source_cases:
            write_rows(p,rows)
            try:aus.audit(3,p)
            except(aus.AuditError,ValueError,TypeError,KeyError):rejected.append(name)
            else:raise RuntimeError('independent source audit accepted '+name)
    return {'status':'PASS','rejected_ledger_controls':rejected,'count':len(rejected),
            'small_valid_source_control_passed':True}

if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True))
