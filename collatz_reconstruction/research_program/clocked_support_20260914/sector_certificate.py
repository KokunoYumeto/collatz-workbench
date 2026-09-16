#!/usr/bin/env python3
"""Lossless source/word dictionary and direct proof certificate for the 403-rise sector.

An original source n is recovered from its row index. The original word is
recovered from its dictionary ID, and the unchanged affine chart recovers its
source parameter and target. All integers in the affine charts are decimal
strings so non-Python readers cannot silently round a large coefficient.
"""
from __future__ import annotations

from collections import Counter
import argparse
import gzip
import hashlib
import json
from pathlib import Path

from clock_module import need, original_step

BASE = '6a30f1dc23110fae0abbe3b3bd5e60072a842385'
BOUND = 330749


def compile_cell(word: tuple[int, ...]) -> dict:
    need(bool(word) and all(type(a) is int and a >= 1 for a in word), 'invalid word')
    L, U, C, prefixes = 1, 1, 0, []
    for a in word:
        L, U, C = 3*L, U*(1 << a), 3*C+U
        prefixes.append((L, U, C))
    D = U-L
    r = ((U-C)*pow(L, -1, 2*U)) % (2*U)
    target, rem = divmod(L*r+C, U)
    need(rem == 0 and r % 2 == 1 and target % 2 == 1, 'legal cylinder mismatch')
    lo, hi = 0, None
    if D <= 0:
        hi = -1
    else:
        lo = max(0, (C-D*r)//(2*U*D)+1)
        for lj, uj, cj in prefixes[:-1]:
            dj = uj-lj
            if dj > 0:
                h = (cj-dj*r)//(2*U*dj)
                hi = h if hi is None else min(hi, h)
    return {'A': sum(word), 'L': str(L), 'U': str(U), 'C': str(C), 'D': str(D),
            'source_anchor': str(r), 'source_step': str(2*U),
            'target_anchor': str(target), 'target_step': str(2*L),
            'lower': str(lo), 'upper': None if hi is None else str(hi),
            'present': True, 'occupied': hi is None or hi >= lo}


def cell_row(n: int, cell: dict) -> tuple[int, int]:
    r, step = int(cell['source_anchor']), int(cell['source_step'])
    t, rem = divmod(n-r, step)
    lo, hi = int(cell['lower']), cell['upper']
    need(rem == 0 and cell['present'] is True and cell['occupied'] is True and t >= lo,
         'source absent from its declared first-descent cell')
    need(hi is None or t <= int(hi), 'source above cell interval')
    target = int(cell['target_anchor'])+int(cell['target_step'])*t
    need(0 < target < n and target % 2 == 1, 'cell did not give a lower original odd integer')
    return t, target


def generate(bound: int = BOUND, cap: int = 10000) -> dict:
    need(type(bound) is int and bound >= 3 and bound % 2 == 1, 'odd source bound required')
    need(type(cap) is int and cap > 0, 'positive return cap required')
    words, seed_words = {}, []
    for n in range(3, bound+1, 2):
        x, w = n, []
        for _ in range(cap):
            x, a = original_step(x)
            w.append(a)
            if x < n:
                break
            need(x != n, 'an actual return to this source was found; retain it, do not certify descent')
        need(x < n, 'source remained unresolved at the cap; no complete interval certificate exists')
        word = tuple(w)
        if word not in words:
            words[word] = compile_cell(word)
        t, y = cell_row(n, words[word])
        need(y == x, 'source and original affine image disagree')
        seed_words.append(word)
    # These supported zero first-descent labels are intentionally present.
    for word in ((1,), (2, 2)):
        words.setdefault(word, compile_cell(word))
    order = sorted(words, key=lambda w: (len(w), w))
    index = {word: i for i, word in enumerate(order)}
    return {'schema': 'collatz-source-word-certificate-v1', 'source_commit': BASE,
            'map': 'T(n)=(3n+1)/2^v2(3n+1)', 'forcing': 1,
            'source_interval': {'first': 3, 'last': bound, 'step': 2}, 'generation_cap': cap,
            'dictionary': [{'word': list(w), 'cell': words[w]} for w in order],
            'source_word_ids': [index[w] for w in seed_words],
            'supported_zero_word_ids': [index[(1,)], index[(2, 2)]],
            'unresolved_sources': []}


def serialize(data: dict) -> bytes:
    return (json.dumps(data, sort_keys=True, separators=(',', ':'))+'\n').encode('utf-8')


def pack(data: dict) -> bytes:
    return gzip.compress(serialize(data), compresslevel=9, mtime=0)


def independently_verify(data: dict) -> dict:
    need(data['schema'] == 'collatz-source-word-certificate-v1' and data['forcing'] == 1,
         'wrong source schema or forcing')
    need(data['source_commit'] == BASE and data['unresolved_sources'] == [], 'source provenance or coverage changed')
    interval = data['source_interval']
    need(interval['first'] == 3 and interval['step'] == 2, 'original source enumeration changed')
    bound = interval['last']
    need(type(bound) is int and bound >= 3 and bound % 2 == 1, 'invalid upper bound')
    ids, table = data['source_word_ids'], data['dictionary']
    need(len(ids) == (bound-1)//2, 'a source row has been dropped or added')
    words = [tuple(entry['word']) for entry in table]
    need(words == sorted(set(words), key=lambda w: (len(w), w)), 'word dictionary not injective')
    for entry, word in zip(table, words):
        need(entry['cell'] == compile_cell(word), 'original affine chart or first-descent interval was altered')
    need([words[i] for i in data['supported_zero_word_ids']] == [(1,), (2, 2)],
         'supported zero labels have been erased or relabelled')
    counts, rank, edge, orbit_checks = Counter(), {1: 0}, {}, 0
    max_first = max_A = 0
    for offset, word_id in enumerate(ids):
        n = 3+2*offset
        need(type(word_id) is int and 0 <= word_id < len(table), 'invalid word reference')
        counts[word_id] += 1
        word, cell = words[word_id], table[word_id]['cell']
        t, chart_target = cell_row(n, cell)
        need(int(cell['source_anchor'])+int(cell['source_step'])*t == n,
             'source parameter inverse failed')
        x, path = n, []
        for j, exponent in enumerate(word):
            value, a = 3*x+1, 0
            while value % 2 == 0:
                value //= 2
                a += 1
            need(a == exponent, 'word is not the original exact valuation sequence')
            need(j == len(word)-1 or value >= n, 'a claimed first-descent word descends earlier')
            path.append(x)
            if x in edge:
                need(edge[x] == (value, a), 'inconsistent original transition')
            edge[x] = (value, a)
            x = value
            orbit_checks += 1
        need(x == chart_target and x < n and x in rank, 'strong-induction endpoint is missing')
        height = rank[x]
        for vertex in reversed(path):
            height += 1
            if vertex in rank:
                need(rank[vertex] == height, 'overlapping actual path heights disagree')
            rank[vertex] = height
        max_first, max_A = max(max_first, len(word)), max(max_A, sum(word))
    for word_id, entry in enumerate(table):
        c = entry['cell']
        lo = max(int(c['lower']), (3-int(c['source_anchor'])+int(c['source_step'])-1)//int(c['source_step']))
        hi = (bound-int(c['source_anchor']))//int(c['source_step'])
        if c['upper'] is not None:
            hi = min(hi, int(c['upper']))
        expected_count = max(0, hi-lo+1) if c['occupied'] else 0
        need(counts[word_id] == expected_count, 'a complete original cell fiber was not accounted for')
    need(set(edge) == set(rank)-{1}, 'the witnessed graph has an unaccounted boundary')
    for n, (target, exponent) in edge.items():
        need(target in rank and rank[n]-rank[target] == 1, 'unit cochain primitive failed')
    return {'status': 'PASS', 'seed_bound': bound, 'seed_count': len(ids),
            'new_seed_count_above_99779': (bound-99779)//2,
            'declared_word_count': len(table), 'occupied_word_count': sum(c > 0 for c in counts.values()),
            'supported_zero_labels': [[1], [2, 2]],
            'actual_return_equations_replayed': orbit_checks,
            'witnessed_nonbase_vertices': len(edge),
            'maximum_witnessed_vertex': max(rank),
            'maximum_unit_primitive': max(rank.values()),
            'maximum_first_descent_returns': max_first, 'maximum_first_descent_exponent_sum': max_A,
            'original_graph_closed_at_basepoint': True,
            'clocked_column_degree_bound': max(rank.values())-1,
            'canonical_database_sha256': hashlib.sha256(serialize(data)).hexdigest()}


def period_feedback(minimum: int = BOUND+2, limit: int = 1636, rise_budget: int = 678) -> dict:
    need(minimum == 330751 and limit == 1636 and rise_budget == 678,
         'this certificate records the specified proved source bound and exact target')
    # Repeated multiplication by two supplies an independent least-power test.
    three = s_power = upper = 1
    rejected, first, allowed_exponent = [], None, None
    for m in range(1, limit+1):
        three *= 3
        s_power *= minimum
        upper *= 3*minimum+1
        A, power = 0, 1
        while power <= three:
            A, power = A+1, 2*power
        if power*s_power <= upper:
            if first is None:
                first, allowed_exponent = m, A
        else:
            rejected.append(m)
    need(first == 1636 and allowed_exponent == 2593 and rejected == list(range(1, 1636)),
         'period window certificate failed')
    witness_m = 1634
    need((4*minimum)**witness_m > (1 << rise_budget)*(3*minimum+1)**witness_m,
         'all-length 678-rise obstruction failed')
    # Exactly locate the remaining minimum interval for m=1636, A=2593.
    m, A, ceiling = 1636, 2593, 583287
    allowed = lambda n: (1 << A)*n**m <= (3*n+1)**m
    need(allowed(ceiling) and not allowed(ceiling+1), 'next minimum ceiling failed')
    need((1 << (A+1))*minimum**m > (3*minimum+1)**m, 'second exponent in next period window')
    next_k = 679
    need((4*minimum)**(m+1) > (1 << next_k)*(3*minimum+1)**(m+1),
         'next rise-sector length ceiling failed')
    need(2*m-A == next_k, 'exponent-1 bookkeeping failed')
    # Close the old (971,1539) sector by its complete minimum interval.
    old_m, old_A = 971, 1539
    need((1 << old_A)*330749**old_m <= (3*330749+1)**old_m,
         'old sector lower endpoint calculation changed')
    need((1 << old_A)*330750**old_m > (3*330750+1)**old_m,
         'old sector upper endpoint calculation changed')
    return {'status': 'PASS', 'proved_minimum_lower_bound': minimum,
            'closed_sector': {'rises': 403, 'm': 971, 'A': 1539, 'minimum_ceiling': 330749},
            'all_lengths_excluded_rise_budget': rise_budget,
            'period_lengths_rejected': [1, 1635], 'period_comparisons': 1636,
            'rise_witness_length': witness_m,
            'next_retained_sector': {'rises': 679, 'm': m, 'A': A,
                                     'ones': 679, 'twos': 957,
                                     'minimum_interval': [minimum, ceiling]},
            'published_record_claim': False}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--generate', type=Path)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    need((args.generate is None) != (args.check is None), 'choose --generate or --check')
    if args.generate:
        data = generate()
        receipt = independently_verify(data)
        args.generate.write_bytes(pack(data))
    else:
        raw = gzip.decompress(args.check.read_bytes())
        data = json.loads(raw)
        need(raw == serialize(data), 'database encoding changed')
        receipt = independently_verify(data)
    receipt['period_feedback'] = period_feedback()
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
