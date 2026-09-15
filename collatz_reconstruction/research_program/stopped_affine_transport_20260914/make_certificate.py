#!/usr/bin/env python3
"""Emit small, fully enumerated support/coset/chain-map certificates.

Run beside verify.py: python make_certificate.py --output example_certificate.json
Standard library only. These are finite certificates, not an infinite coverage claim.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
from fractions import Fraction
from math import gcd
from pathlib import Path
import json

from verify import (Family, VerificationError, actual_label, chart,
                    descent_intervals, marked_cells, odd_steps, packet, stop_leaves)


def build() -> dict:
    checks = 0

    def check(ok: bool, message: str) -> None:
        nonlocal checks
        if not ok:
            raise VerificationError(message)
        checks += 1

    fixtures = []
    for f in (Family(1, 1, 1, 17), Family(1, 4, 1, 17)):
        H, M = 4, 3
        source = [f.value(t) for t in range(f.b, f.b + f.N)]
        direct = [actual_label(f, t, H, M) for t in range(f.b, f.b + f.N)]
        rows, keys = [], []
        reference_total = Fraction(0)
        actual_total = 0
        for p in stop_leaves(H):
            ch = chart(f, p)
            cells = descent_intervals(f, p)
            if ch is not None:
                reference_total += Fraction(1, ch.P)
            for key, count, q in marked_cells(f, p, M):
                _, r, j = key
                ix = [i for i, k in enumerate(direct) if k == key]
                check(len(ix) == count, "certificate count does not match original fiber")
                check(abs(Fraction(count, f.N) - q) <= Fraction(1, f.N),
                      "certificate original cell discrepancy")
                prefixes = [list(odd_steps(source[i], p.m)[1]) for i in ix]
                interval = cells[j-1]
                image = None if ch is None else {
                    "original_target_step": 2*ch.target_d,
                    "differential": ch.target_d,
                    "coset_original_integer": (ch.u-1)//2,
                    "coset_mod_differential": ((ch.u-1)//2) % ch.target_d,
                    "coset_order": ch.target_d // gcd(ch.target_d, (ch.u-1)//2),
                }
                enriched = None
                if ch is not None:
                    ell = [((f.b+i-ch.s)//ch.P-r)//M for i in ix]
                    D = M*ch.target_d
                    zbase = (ch.u+2*ch.target_d*r-1)//2
                    zvals = [(vals[-1]-1)//2 for vals in prefixes]
                    check(all(z == zbase+D*v for z,v in zip(zvals,ell)),
                          "enriched certificate comparison chain equation")
                    check(all(v == ell[0]+i for i,v in enumerate(ell)),
                          "enriched certificate consecutive source lifts")
                    enriched = {
                        "actual_columns": [[1,z] for z in zvals],
                        "source_lift_parameters": ell,
                        "to_support_degree_one_row": [1,0],
                        "to_support_degree_zero": "identity on the original source basis",
                        "to_image_degree_zero_row": ell,
                        "to_image_degree_one_row": [-zbase,1],
                        "target_image_differential": D,
                        "H0_rank": max(len(ix)-2,0),
                        "H1_free_rank": 2 if not ix else 1 if len(ix)==1 else 0,
                        "H1_torsion_order": D if len(ix)>=2 else None,
                    }
                rows.append({
                    "enriched_affine_incidence_comparison": enriched,
                    "label": {"word": list(p.word), "lift_mark": r, "first_descent": j},
                    "declared_label_present": True,
                    "congruence_compatible": ch is not None,
                    "original_first_descent_interval": None if interval is None else {
                        "lower_open": str(interval[0]), "upper_closed": str(interval[1]),
                        "upper_already_clipped_to_sample_end": True,
                    },
                    "finite_sample_occupied": count > 0,
                    "count": count,
                    "actual_probability": str(Fraction(count, f.N)),
                    "reference_probability": str(q),
                    "source_positions_zero_based": ix,
                    "source_parameters": [f.b+i for i in ix],
                    "source_values": [source[i] for i in ix],
                    "actual_prefix_values": prefixes,
                    "synchronized_residues": [[v % M for v in vals] for vals in prefixes],
                    "chart": None if ch is None else asdict(ch),
                    "image_complex_and_coset": image,
                })
                keys.append(key)
                actual_total += count
        ix = [i for i,k in enumerate(direct) if k == ("overflow",)]
        overflow_count = f.N-actual_total
        check(overflow_count == len(ix), "explicit certificate overflow")
        rows.append({"label": {"cutoff_overflow": True},
                     "declared_label_present": True,
                     "finite_sample_occupied": overflow_count > 0,
                     "count": overflow_count,
                     "actual_probability": str(Fraction(overflow_count, f.N)),
                     "reference_probability": str(1-reference_total),
                     "source_positions_zero_based": ix,
                     "source_parameters": [f.b+i for i in ix],
                     "source_values": [source[i] for i in ix]})
        keys.append(("overflow",))
        target_lookup = {key: i for i,key in enumerate(keys)}
        delta = [target_lookup[k] for k in direct]
        h = [row['source_positions_zero_based'][0] if row['source_positions_zero_based'] else None
             for row in rows]
        H0 = []
        for label, row in enumerate(rows):
            if h[label] is not None:
                H0.extend({"plus_source_position": i, "minus_source_position": h[label]}
                          for i in row['source_positions_zero_based'] if i != h[label])
        H1 = [i for i,x in enumerate(h) if x is None]
        for source_position, target_label in enumerate(delta):
            check(delta[h[target_label]] == target_label, "certificate source homotopy")
        check(len(H0) == f.N-len(rows)+len(H1), "certificate H0 rank")
        check(all(rows[i]['count'] == 0 for i in H1), "certificate present-zero basis")
        check(sum(Fraction(row['actual_probability']) for row in rows) == 1,
              "certificate actual mass")
        check(sum(Fraction(row['reference_probability']) for row in rows) == 1,
              "certificate reference mass")
        fixtures.append({"family": asdict(f), "H": H, "M": M,
                         "original_source_values": source,
                         "declared_label_dictionary": rows,
                         "delta_column_target_indices_zero_based": delta,
                         "h1_column_source_indices_zero_based_or_null": h,
                         "H0_difference_basis": H0, "H1_present_zero_basis_indices": H1})
    images = []
    for word in ((2,), (1,1,3,2)):
        p = packet(word)
        u = int(p.evaluate(p.residue))
        z0 = (u-1)//2
        check((p.L*p.residue+p.C) == (1 << p.A)*u, "worked integral matrix constant")
        images.append({"word": list(word), "A": p.A, "L": p.L, "C": p.C,
                       "source_residue": p.residue, "source_step": p.modulus,
                       "source_minimum_parameter_for_n_at_least_3": 1 if p.residue == 1 else 0,
                       "terminal_base": u, "terminal_step": 2*p.L,
                       "image_complex_differential": p.L,
                       "distinguished_coset": z0,
                       "distinguished_coset_order": p.L//gcd(p.L,z0),
                       "dyadic_inverse_finite_residues": {
                           str(1 << r): pow(p.L,-1,1 << r) for r in range(1,9)}})
    return {"status": "PASS", "validation_checks": checks,
            "scope": "Fully enumerated finite examples; infinite claims are proved in note.md.",
            "label_indices": "zero-based; dictionary order retained literally",
            "finite_observation_certificates": fixtures,
            "image_complex_examples_including_a_supported_zero_coset": images}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = build()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n', encoding='utf-8')
    print(json.dumps({"status": result['status'], "validation_checks": result['validation_checks'],
                      "output": str(args.output)}, sort_keys=True))


if __name__ == '__main__':
    main()
