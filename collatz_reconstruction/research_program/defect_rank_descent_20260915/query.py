#!/usr/bin/env python3
"""Inspect original arithmetic certificates without replacing source labels."""
from __future__ import annotations
import argparse
import gzip
import json
from pathlib import Path
import arithmetic as ar
import atlas
import logarithm_certificate as lc

HERE=Path(__file__).resolve().parent


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('repeat',help='exact complete-copy rank of an original word')
    p.add_argument('source',type=int);p.add_argument('--word',type=int,nargs='+',required=True)
    p=sub.add_parser('switch',help='retain the exact resultant and the resonant residual')
    p.add_argument('source',type=int);p.add_argument('--first',type=int,nargs='+',required=True)
    p.add_argument('--second',type=int,nargs='+',required=True)
    p=sub.add_parser('resonance',help='the proved unbounded rank-reset descent family')
    p.add_argument('r',type=int);p.add_argument('v',type=int)
    p=sub.add_parser('run',help='strict descent on the exact contracting pure-two comparison domain')
    p.add_argument('source',type=int);p.add_argument('--ones',type=int,required=True)
    p.add_argument('--falls',type=int,nargs='+',required=True)
    p=sub.add_parser('peak',help='original first-return block to n=1 modulo 4')
    p.add_argument('source',type=int)
    p=sub.add_parser('witness',help='construct the original finite integral first-jet witness')
    p.add_argument('source',type=int);p.add_argument('--atlas',type=Path,default=HERE/'atlas.json.gz')
    p=sub.add_parser('logarithm',help='verify the complete finite rational logarithm certificate')
    p.add_argument('--full',action='store_true')
    for p in sub.choices.values():p.add_argument('--output',type=Path)
    args=parser.parse_args()
    try:
        if args.command=='repeat':result=ar.repeat_record(args.source,args.word)
        elif args.command=='switch':result=ar.switch_record(args.source,args.first,args.second)
        elif args.command=='resonance':result=ar.resonant_family(args.r,args.v)
        elif args.command=='peak':result=ar.peak_block(args.source)
        elif args.command=='run':
            result=ar.run_witness(args.source,args.ones,args.falls)
            ar.require(result['pure_two_defect']>3**args.ones-2**args.ones,
                       'the exact positive-gap theorem failed on this input')
            ar.require(result['strict_descent'],'original strict descent failed')
            result['proof_route']='Corollary E1; original congruence plus certified all-length positive gap'
        elif args.command=='witness':
            data=json.loads(gzip.decompress(args.atlas.read_bytes()))
            cells,_=atlas.verify_cover(data)
            result=atlas.Index(cells).witness(args.source)
        else:
            data=lc.certificate()
            result=data if args.full else {
                'status':data['status'],'external_theorem':data['external_theorem'],
                'farey':data['farey'],
                'pure_run_finite_rows':len(data['pure_run_small_rows']),
                'minimum_run_finite_rows':len(data['small_cycle_rows']),
                'minimum_run_period_ratio':data['minimum_run_period_ratio'],
                'certified_results':data['certified_results']}
        text=json.dumps(result,sort_keys=True,indent=2)+'\n'
        if args.output:args.output.write_text(text,encoding='utf-8')
        else:print(text,end='')
    except (ar.CertificateError,OSError,ValueError,KeyError) as exc:
        parser.error(str(exc))


if __name__=='__main__':main()
