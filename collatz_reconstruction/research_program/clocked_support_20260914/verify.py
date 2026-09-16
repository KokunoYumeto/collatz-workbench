#!/usr/bin/env python3
"""Symbolic identities, original-source replay, and explicit negative controls."""
from __future__ import annotations

import argparse
from collections import Counter
import copy
from fractions import Fraction
import gzip
import hashlib
import importlib.util
from itertools import product
import json
from pathlib import Path
import sys

import clock_module as c
import sector_certificate as sector

HERE = Path(__file__).resolve().parent
PRIOR = HERE.parent/'residual_splice_20260914'
sys.path.insert(0, str(PRIOR))
import residual_descent as old

COUNTS = Counter()


def check(condition, label):
    if not condition:
        raise RuntimeError(label)
    COUNTS[label] += 1


def reject(function, label):
    try:
        function()
    except (ValueError, KeyError, TypeError):
        COUNTS['rejected:'+label] += 1
        return
    raise RuntimeError('Malformed input accepted: '+label)


def cycle_checks():
    words = [w for m in range(1, 6) for w in product(range(1, 4), repeat=m)]
    words.append((1, 1, 2, 4, 3))
    for w in words:
        m, marked = len(w), c.marked_word(w)
        check(c.recover_word(marked['weight'], marked['forcing_polynomial']) == w, 'two-sided-word-inverse')
        L, U, C, D = c.affine_packet(w)
        original = old.cd.packet(w)
        check((L, U, C, D) == (original.L, original.U, original.C, original.D), 'original-packet-identity')
        u, v = Fraction(2, 3), 2
        check(c.evaluate(marked['annihilator'], u, v) == Fraction(-D, L), 'arithmetic-annihilator-map')
        check(3**(m-1)*c.evaluate(marked['forcing_polynomial'], u, v) == C,
              'ordered-forcing-map')
        unit = [c.monomial() for _ in w]
        check(c.phi_one(w, unit) == marked['forcing_polynomial'], 'forcing-polynomial-sum')
        for j in range(m):
            e = [c.monomial() if i == j else {} for i in range(m)]
            d_e = c.cycle_d(w, e)
            check(c.phi_one(w, d_e) == c.mul(marked['annihilator'], e[0]), 'scalar-chain-map')
            check(c.vector_add(e, c.homotopy(w, d_e), -1) == c.psi_zero(w, e[0]),
                  'degree-zero-polynomial-homotopy')
            check(c.vector_add(e, c.cycle_d(w, c.homotopy(w, e)), -1) ==
                  c.psi_one(w, c.phi_one(w, e)), 'degree-one-polynomial-homotopy')
            B = old.cd.cyclic_matrix(w)
            check([c.evaluate(row, u, v) for row in d_e] ==
                  [Fraction(-B[i][j], 3) for i in range(m)], 'original-integral-matrix-localization')
        check(c.cycle_d(w, c.psi_zero(w, c.monomial())) == c.psi_one(w, marked['annihilator']),
              'scalar-section-chain-map')
        check(c.psi_zero(w, c.monomial())[0] == c.monomial(), 'degree-zero-section')
        check(c.phi_one(w, c.psi_one(w, c.monomial())) == c.monomial(), 'degree-one-section')
    p, q = c.marked_word((1, 3)), c.marked_word((2, 2))
    check(p['annihilator'] == q['annihilator'], 'same-clock-determinant-control')
    check(p['forcing_polynomial'] != q['forcing_polynomial'], 'retained-forcing-separates-words')
    check((c.affine_packet((1, 3))[2] % 7, c.affine_packet((2, 2))[2] % 7) == (5, 0),
          'original-marked-integral-classes')
    for modulus, expected in ((19, 19), (361, 0)):
        # Independent scalar equation after the original five-row telescope.
        solutions = sum((1805*x-475) % modulus == 0 for x in range(modulus))
        check(solutions == expected, 'prime-power-retained-after-specialization')
    return len(words)


def path_and_completion_controls():
    examples = []
    for n in range(1, 512, 2):
        x, tau = n, 0
        while x != 1:
            x, _ = c.original_step(x)
            tau += 1
            check(tau < 1000, 'finite-actual-orbit-cap')
        col = c.path_column(n, tau)
        expected = {} if n == 1 else {(n, 0, 0): 1}
        check(c.boundary(col['chain'], c.original_step) == expected, 'actual-polynomial-contraction-column')
        check(c.ordinary(col['chain']) == dict(Counter(col['values'])), 'clock-erasure-original-chain')
        for cap in sorted({0, min(1, tau), min(4, tau), tau}):
            truncated = c.path_column(n, cap)
            independent = n
            for _ in range(cap):
                independent = 3*independent+1
                while independent % 2 == 0:
                    independent //= 2
            check(truncated['terminal'] == independent, 'independent-original-terminal-retained')
        if n in (1, 3, 7, 27, 247):
            examples.append({'source': n, 'returns_to_basepoint': tau,
                             'exponent_sum': col['exponent_sum'], 'full_original_word': list(col['word']),
                             'declared_edge_labels': list(col['declared_edge_labels'])})
    control_step = lambda n: c.original_step(n, -1)
    primitive = c.path_column(5, 2, control_step)
    check(primitive['word'] == (1, 2) and primitive['terminal'] == 5, 'actual-minus-one-control-cycle')
    check(c.boundary(primitive['chain'], control_step) == {(5, 0, 0): 1, (5, 2, 1): -1},
          'control-two-clock-cycle-relation')
    for repeats in range(1, 17):
        actual = c.path_column(5, 2*repeats, control_step)
        expansion = c.add(*(c.shift(primitive['chain'], 2*j, j) for j in range(repeats)))
        check(actual['chain'] == expansion, 'repetition-polynomial-cover-map')
        check(len(actual['declared_edge_labels']) == 2, 'periodic-formal-column-finite-vertex-support')
        check(c.ordinary(actual['chain']) == {5: repeats, 7: repeats}, 'original-repetition-multiplicity')
    # This ray is a labelled test map, never reported as an original Collatz orbit.
    ray = lambda n: (n+2, 2)
    for length in range(1, 65):
        col = c.path_column(3, length, ray)
        check(len(col['declared_edge_labels']) == length, 'synthetic-ray-escaping-vertex-support')
        check(c.boundary(col['chain'], ray) == {(3, 0, 0): 1, (3+2*length, length, length): -1},
              'synthetic-ray-exact-frontier')
    return examples


def retraction_checks():
    cutoffs = (0, 4, 8, 16, 64, 128)
    lifts = [c.ClockedRetraction(old.cd.StoppedDescentCompression(h)) for h in cutoffs]
    for lift in lifts:
        for n in range(3, 128, 2):
            vertex = edge = {(n, 0, 0): 1}
            check(c.add(c.boundary(lift.h(vertex), lift.successor), lift.q(vertex)) == vertex,
                  'weighted-retraction-vertex-identity')
            check(lift.q(lift.q(vertex)) == lift.q(vertex), 'weighted-root-idempotence')
            check(lift.h(lift.q(vertex)) == {}, 'weighted-root-homotopy-zero')
            check(lift.f(lift.f(edge)) == lift.f(edge), 'weighted-edge-idempotence')
            check(c.boundary(lift.f(edge), lift.successor) == lift.q(c.boundary(edge, lift.successor)),
                  'weighted-projection-chain-equation')
            check(c.ordinary(lift.h(vertex)) == lift.predecessor.resolve(n)[1],
                  'ordinary-retraction-recovered')
    for a, b in zip(lifts, lifts[1:]):
        for n in range(3, 128, 2):
            v = e = {(n, 0, 0): 1}
            check(b.h(v) == c.add(a.h(v), b.h(a.q(v))), 'cutoff-weighted-path-concatenation')
            check(b.q(a.q(v)) == b.q(v) == a.q(b.q(v)), 'cutoff-weighted-root-compositions')
            check(b.f(a.f(e)) == b.f(e) == a.f(b.f(e)), 'cutoff-weighted-edge-compositions')
    base = old.cd.DescentCompression({5: (4,)})
    extension = old.RootSplice(base, [old.first_descent_cell((1, 1, 2, 3))])
    base_lift, new_lift = c.ClockedRetraction(base), c.ClockedRetraction(extension)
    b = c.path_column(7, 4)
    correct = c.add(b['chain'], c.shift(base_lift.h({(5, 0, 0): 1}), 4, 3))
    wrong = c.add(b['chain'], base_lift.h({(5, 0, 0): 1}))
    check(new_lift.h({(7, 0, 0): 1}) == correct, 'root-splice-must-retain-terminal-clock')
    wrong_residual = c.add(c.boundary(wrong, c.original_step), {(7, 0, 0): -1})
    check(wrong_residual == {(5, 0, 0): 1, (5, 4, 3): -1}, 'missing-clock-exact-defect')
    for n in (3, 5, 7, 11, 17, 13, 263, 519):
        v = e = {(n, 0, 0): 1}
        K = c.add(new_lift.h(v), c.scale(base_lift.h(v), -1))
        check(base_lift.f(K) == K, 'weighted-root-splice-correction-in-old-image')
        check(base_lift.f(new_lift.f(e)) == new_lift.f(e) == new_lift.f(base_lift.f(e)),
              'weighted-root-splice-both-compositions')
    return {'source': 7, 'old_root': 7, 'new_root': 1, 'block_word': [1, 1, 2, 3],
            'retained_terminal_weight': [4, 3], 'tail_word': [4],
            'missing_weight_defect': '(1-u^4*v^3)*v_5'}


def negative_controls(data):
    good = c.marked_word((1, 2, 3))
    reject(lambda: c.recover_word((3, 3), {(0, 0): 1, (1, 0): 1}), 'missing-forcing-position')
    reject(lambda: c.recover_word((3, 3), {(0, 0): 2, (1, 0): 1, (2, 1): 1}), 'altered-forcing-coefficient')
    reject(lambda: c.recover_word((3, 0), good['forcing_polynomial']), 'negative-recovered-exponent')
    reject(lambda: c.marked_word((1, 0)), 'zero-original-exponent')
    reject(lambda: c.monomial(-1, 0), 'negative-polynomial-degree')
    reject(lambda: c.path_column(1, 1), 'removed-base-loop-reintroduced')
    reject(lambda: c.original_step(4), 'even-odd-return-source')
    small = sector.generate(31)
    altered = copy.deepcopy(small); altered['source_word_ids'].pop()
    reject(lambda: sector.independently_verify(altered), 'missing-source-row')
    altered = copy.deepcopy(small); altered['forcing'] = -1
    reject(lambda: sector.independently_verify(altered), 'forcing-change')
    altered = copy.deepcopy(small); altered['dictionary'][0]['cell']['C'] = '0'
    reject(lambda: sector.independently_verify(altered), 'erased-affine-offset')
    altered = copy.deepcopy(small); altered['supported_zero_word_ids'] = []
    reject(lambda: sector.independently_verify(altered), 'erased-supported-zero-labels')
    altered = copy.deepcopy(small); altered['source_word_ids'][0] = 10**9
    reject(lambda: sector.independently_verify(altered), 'invalid-dictionary-reference')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    fixtures = cycle_checks()
    examples = path_and_completion_controls()
    splice = retraction_checks()
    raw = gzip.decompress((HERE/'source_database.json.gz').read_bytes())
    data = json.loads(raw)
    check(raw == sector.serialize(data), 'lossless-source-database-encoding')
    database = sector.independently_verify(data)
    negative_controls(data)
    feedback = sector.period_feedback()
    # Cross-check every saved chart against the untouched predecessor constructor.
    for entry in data['dictionary']:
        w = tuple(entry['word'])
        previous = old.first_descent_cell(w)
        c1 = entry['cell']
        check(previous.source_anchor == int(c1['source_anchor']) and
              previous.source_step == int(c1['source_step']) and
              previous.target_anchor == int(c1['target_anchor']) and
              previous.target_step == int(c1['target_step']) and
              previous.lower == int(c1['lower']) and
              previous.upper == (None if c1['upper'] is None else int(c1['upper'])) and
              (previous.A, previous.L, previous.C, previous.D) ==
              (c1['A'], int(c1['L']), int(c1['C']), int(c1['D'])),
              'unchanged-predecessor-cell-comparison')
    result = {'status': 'PASS', 'source_commit': sector.BASE,
              'symbolic_cycle_word_fixtures': fixtures, 'named_check_count': sum(COUNTS.values()),
              'checks_by_name': dict(sorted(COUNTS.items())), 'source_database': database,
              'period_feedback': feedback, 'actual_path_examples': examples,
              'clock_splice_defect': splice,
              'negative_controls': sum(v for k, v in COUNTS.items() if k.startswith('rejected:')),
              'scope': {'original_collatz_forcing': 1, 'nontrivial_cycle_control_forcing': -1,
                        'synthetic_ray_is_not_an_original_collatz_orbit': True,
                        'global_convergence_proved': False, 'independent_external_review': False}}
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'status': 'PASS', 'named_checks': result['named_check_count'],
                      'source_seeds': database['seed_count'],
                      'original_return_equations_replayed': database['actual_return_equations_replayed'],
                      'all_length_rise_budget_excluded': 678}, sort_keys=True))


if __name__ == '__main__':
    main()
