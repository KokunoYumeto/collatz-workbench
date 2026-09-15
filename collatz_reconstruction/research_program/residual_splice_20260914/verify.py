#!/usr/bin/env python3
"""Exact regressions and the finite certificate for the all-length 402-rise exclusion."""
from __future__ import annotations
import argparse
from collections import Counter
from dataclasses import replace
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import residual_descent as rd
import tail_descent as td

COUNTS: Counter[str] = Counter()


def check(value, label):
    if not value:
        raise RuntimeError(label)
    COUNTS[label] += 1


def raw_step(n):
    if type(n) is not int or n < 1 or n % 2 == 0:
        raise ValueError('positive odd source required')
    y, a = 3*n+1, 0
    while y % 2 == 0:
        y //= 2
        a += 1
    return y, a


def raw_path(n, word):
    x, first, chain = n, None, Counter()
    for i, expected in enumerate(word, 1):
        if x != 1:
            chain[x] += 1
        x, a = raw_step(x)
        check(a == expected, 'independent exact valuation')
        if first is None and x < n:
            first = i
    return x, first, rd.clean(chain)


def vertex(n):
    return {} if n == 1 else {n: 1}


def difference(n, r):
    x = Counter(vertex(n)); x.subtract(vertex(r))
    return rd.clean(x)


def cell_checks(cells):
    fixtures = 0
    for length in range(1, 5):
        for word in product(range(1, 5), repeat=length):
            cell = rd.first_descent_cell(word)
            for t in (0, 1, 2, 7):
                n = cell.source_anchor+cell.source_step*t
                y, first, chain = raw_path(n, word)
                check(y == cell.target_anchor+cell.target_step*t, 'unreduced target progression')
                check((cell.parameter(n) is not None) == (first == length), 'complete first-descent interval')
                check(rd.cd.sparse_boundary(chain) == difference(n, y), 'original cylinder boundary')
            fixtures += 1
    for cell in cells:
        for t in (cell.lower, cell.lower+1, cell.lower+17, 2**32+cell.lower):
            n = cell.source_anchor+cell.source_step*t
            y, first, chain = raw_path(n, cell.word)
            check(first == len(cell.word) and y < n, 'atlas lift first descent')
            check(y == cell.target_anchor+cell.target_step*t, 'atlas lift affine endpoint')
            check(rd.cd.sparse_boundary(chain) == difference(n, y), 'atlas lift boundary')
        check(cell.parameter(cell.source_anchor+cell.source_step*cell.lower+2) is None,
              'wrong residue remains absent')
    zero = rd.first_descent_cell((2, 2))
    check(not zero.occupied and zero.word == (2, 2), 'empty first-descent label retained')
    ordinary = rd.first_descent_cell((2,))
    check(ordinary.lower == 1 and ordinary.parameter(1) is None, 'fixed point not strict descent')
    return fixtures


def splicing_checks(cells):
    base = rd.cd.StoppedDescentCompression(64)
    extended = rd.RootSplice(base, cells)
    example_sources = [27+2**60*t for t in (0, 1, 2, 7)]
    sample = list(range(1, 1024, 2))+[703, 4095]+example_sources
    for n in sorted(set(sample)):
        r0, h0 = base.resolve(n)
        r1, h1 = extended.resolve(n)
        correction = extended.correction(n)
        check(h1 == rd.add(h0, correction), 'old path retained with root correction')
        check(extended.resolve(r1) == (r1, {}), 'new root idempotent and homotopy zero')
        check(base.resolve(r1) == (r1, {}), 'new root remains an old root')
        check(extended.resolve(r0)[0] == r1, 'Qnew Qold equals Qnew')
        check(rd.cd.sparse_boundary(h1) == difference(n, r1), 'full splice boundary')
        check(base.project_edges(correction) == correction, 'correction lies in old projected edges')
        if n == 1:
            continue
        e = {n: 1}; f = extended.project_edges(e)
        check(rd.cd.sparse_boundary(f) == extended.project_vertices(rd.cd.sparse_boundary(e)),
              'new chain equation')
        check(extended.project_edges(f) == f, 'Fnew idempotent')
        check(extended.project_edges(base.project_edges(e)) == f, 'Fnew Fold equals Fnew')
        check(base.project_edges(f) == f, 'Fold Fnew equals Fnew')
    # Compare nested additions without changing any earlier accepted path.
    small_base = rd.cd.StoppedDescentCompression(8)
    first = rd.RootSplice(small_base, cells[:100])
    second = rd.RootSplice(first, cells[100:])
    union = rd.RootSplice(small_base, cells)
    for n in range(3, 512, 2):
        check(second.resolve(n) == union.resolve(n), 'disjoint-atlas staged splicing')
    profile = []
    for H in (8, 16, 32, 64):
        old = rd.cd.StoppedDescentCompression(H)
        new = rd.RootSplice(old, cells)
        old_roots, new_roots = set(), set()
        for n in range(1, 4096, 2):
            a, _ = old.resolve(n); b, chain = new.resolve(n)
            old_roots.add(a); new_roots.add(b)
            check(b == 1 and rd.cd.sparse_boundary(chain) == vertex(n), 'finite whole-source boundary certificate')
        profile.append({'cutoff': H, 'sources': 2048,
                        'old_nonbase_roots': len(old_roots-{1}),
                        'new_nonbase_roots': len(new_roots-{1})})
    check(base.resolve(27)[0] == 27 and extended.resolve(27)[0] == 1,
          '27 discharged without raising old cutoff')
    return {'profile': profile, 'new_block_at_27': extended.added_roots[27],
            'path_edges_27': len(extended.resolve(27)[1])}


def tail_checks(cells):
    tails = td.tails_from_cells(cells)
    for tail in tails:
        p = rd.cd.packet(tail.prefix)
        r,u,B = tail.prefix_source_anchor,tail.prefix_target_anchor,tail.threshold
        check(2**B*r > 3*u+1 and 2**B*p.U >= 3*p.L, 'unbounded-tail raw coefficient inequalities')
        for v in (0,1,13):
            n = tail.source_anchor+tail.source_step*v
            word = tail.word_for(n)
            check(word is not None, 'tail source retained')
            y, first, chain = raw_path(n, word)
            check(first == len(word) and y < n, 'unbounded-tail actual first descent')
            check(rd.cd.sparse_boundary(chain) == difference(n,y), 'unbounded-tail original boundary')
        for a in (B, B+1, B+17):
            cell = rd.first_descent_cell(tail.prefix+(a,))
            check(cell.lower == 0 and cell.upper is None and cell.occupied, 'entire exact tail stratum retained')
            check(tail.word_for(cell.source_anchor) == cell.word, 'tail-stratum inverse word map')
    for tail in tails[:80]:
        split = td.split_prefix(tail.prefix)
        rows = {row['exponent']:row for row in split['finite_children']}
        for t in range(16):
            n=tail.prefix_source_anchor+tail.prefix_source_step*t
            x,first,_=raw_path(n,tail.prefix)
            check(first is None, 'frontier prefix has no earlier descent')
            y,a=raw_step(x)
            if a >= tail.threshold:
                check(tail.word_for(n) == tail.prefix+(a,) and y<n,
                      'complete prefix partition unbounded tail')
            else:
                row=rows[a];cell=rd.first_descent_cell(tail.prefix+(a,))
                if cell.D <= 0:
                    check(y>=n and cell.parameter(n) is None,
                          'complete prefix partition noncontracting child')
                else:
                    box=row['exception_box'];v=(n-box['r'])//box['step']
                    check((box['lower']<=v<=box['upper']) == (y>=n),
                          'complete prefix partition finite exception')
                    check((cell.parameter(n) is not None) == (y<n),
                          'complete prefix partition descent interval')
    deep = td.descent_tail(())
    old = rd.cd.StoppedDescentCompression(64)
    new = rd.RootSplice(old,cells,tails)
    examples=[]
    for j in (33,64,128,512):
        n=(4**j-1)//3
        check(old.resolve(n) == (n,{}), 'arbitrarily deep tested source remains an old cutoff root')
        root,chain=new.resolve(n)
        check(root == 1 and chain == {n:1}, 'unbounded tail discharges deep root on its original edge')
        check(new.added_roots[n]['word'] == [2*j], 'large actual exponent not discarded')
        examples.append({'j':j,'source_formula':'(4^j-1)/3','actual_exponent':2*j,'new_root':root})
    check(td.descent_tail((1,2)).source_anchor == 11 and td.descent_tail((1,2)).source_step == 32,
          '11 mod 32 unbounded last-exponent family')
    return {'tail_families': len(tails), 'empty_prefix_tail': deep.record(),
            'one_two_prefix_tail': td.descent_tail((1,2)).record(), 'deep_root_examples':examples,
            'one_two_complete_partition': td.split_prefix((1,2))}


def block_checks():
    count = 0
    for length in range(1, 5):
        for word in product((1, 2, 3), repeat=length):
            for cuts in ((), tuple(range(1, length)), tuple(range(1, length, 2))):
                endpoints = (0,)+cuts+(length,)
                lengths = tuple(b-a for a, b in zip(endpoints, endpoints[1:]))
                maps = rd.block_comparison(word, lengths)
                R, B, G, S0, S1, H = (maps[k] for k in ('R', 'B', 'Bbar', 'S0', 'S1', 'H'))
                P0 = maps['P0']; k = len(lengths)
                row, U_before = [], 1
                for i, block in enumerate(maps['blocks']):
                    L_after = 1
                    for later in maps['blocks'][i+1:]: L_after *= later['L']
                    row.append(L_after*U_before)
                    U_before *= block['U']
                check(rd.mm([row], R) == [list(rd.cd.functional(word))], 'marked cokernel identity')
                check(rd.mm(R, [[1] for _ in word]) == [[v] for v in maps['compressed_forcing']],
                      'original forcing transported')
                anchored = [[4-2**a] for a in word]
                check(rd.mm(R, anchored) == [[b['anchored_forcing']] for b in maps['blocks']],
                      'anchored forcing transported')
                z = rd.mm(rd.inverse(G), [[v] for v in maps['compressed_forcing']])
                lift = rd.mm(S0, z)
                Hb = rd.mm(H, [[1] for _ in word])
                lift = [[x[0]+y[0]] for x, y in zip(lift, Hb)]
                direct = rd.mm(rd.inverse(B), [[1] for _ in word])
                check(lift == direct and rd.mm(P0, lift) == z, 'full affine inverse with homotopy correction')
                for modulus in (2, 3, 9, 19):
                    check(all((a-b) % modulus == 0 for ar, br in zip(rd.mm(R, B), rd.mm(G, P0))
                              for a, b in zip(ar, br)), 'finite coefficient block chain map')
                count += 1
    special = (1, 1, 2, 4, 3)
    maps = rd.block_comparison(special, (1, 4))
    z = rd.mm(rd.inverse(maps['Bbar']), [[v] for v in maps['compressed_forcing']])
    check(z == [[F(5, 19)], [F(17, 19)]], 'prime-power obstruction survives compression')
    for N, expected in ((19,19),(361,0)):
        observed = sum((1024*x-81*((1+3*x)*pow(2,-1,N) % N)-197) % N == 0
                       for x in range(N))
        check(observed == expected, 'compressed full prime-power solution count')
    for word in ((2,1,2,2,1), (1,), (2,3,1,2,1,3)):
        rec = rd.rising_blocks(word)
        rotated = tuple(rec['rotated_word'])
        recovered = [None]*len(word)
        for i, j in enumerate(rec['rotation_inverse']): recovered[j] = rotated[i]
        check(tuple(recovered) == word, 'retained rotation dictionary has exact inverse')
        maps2 = rd.block_comparison(rotated, rec['lengths'])
        check(tuple(a for block in maps2['blocks'] for a in block['word']) == rotated,
              'original block dictionary reconstructs every ordered letter')
    for r in range(16):
        p = rd.cd.packet((1,)+(2,)*r)
        check(p.U == 2*4**r and p.L == 3**(r+1) and p.C == 2*4**r-3**r,
              'arbitrary homogeneous gap formula')
        check(p.C-p.D == 2*3**r, 'gap anchored forcing')
    return count, maps


def crossing_checks(sum_bound=18):
    stack = [((), 0, 1, 0)]
    leaves, empty, support_one, max_count = 0, 0, 0, 0
    while stack:
        word, A, L, C = stack.pop()
        for a in range(1, sum_bound-A+1):
            w, AA, LL, CC = word+(a,), A+a, 3*L, 3*C+2**A
            D = 2**AA-LL
            if D <= 0:
                stack.append((w, AA, LL, CC))
                continue
            box = rd.coefficient_crossing_box(w, 1)
            leaves += 1; max_count = max(max_count, box['count'])
            check(box['count'] <= box['universal_count_bound'], 'finite exception count bound')
            if not box['count']: empty += 1
            for t in range(box['lower'], box['upper']+1):
                n = box['r']+box['step']*t
                y, first, _ = raw_path(n, w)
                check(y >= n and first is None, 'exact retained coefficient exception')
                if n == 1: support_one += 1
                else: raise RuntimeError('New nontrivial first-crossing exception: '+str((n, w)))
    return {'exponent_sum_bound': sum_bound, 'first_crossing_words': leaves,
            'empty_source_boxes': empty, 'supported_basepoint_occurrences': support_one,
            'maximum_box_occupancy': max_count,
            'nonbase_exceptions_found': 0, 'only_a_bounded_crossing_scan': True}


def exclusion_checks(cells, atlas, feedback):
    # Induction uses only actual first-descent edges below the seed, not an
    # assumption that a finite batch of trajectories is representative.
    known = {1}
    by_word = {c.word: c for c in cells}
    seed_bound = atlas['seed_bound']
    for n in range(3, seed_bound+1, 2):
        w = rd.first_descent_word(n)
        check(w in by_word, 'seed certificate in retained atlas')
        y, first, _ = raw_path(n, w)
        check(y in known and first == len(w), 'strong-induction base-range certificate')
        known.add(n)
    check(len(known) == (seed_bound+1)//2 and not atlas['unresolved_seeds'],
          'full minimum range established by actual descent')
    sieve = rd.period_sieve()
    check(sieve['period_ceiling'] == 144 and sieve['budget_excluded'], 'complete sixty-rise exclusion')
    s = 4097
    # Independent selection of the least power of 2; no bit_length helper.
    for m in range(1, 147):
        A, power = 0, 1
        while power <= 3**m:
            power *= 2; A += 1
        check(power*s**m > (3*s+1)**m, 'all periods below 147 rejected')
    check((4*s)**145 > 2**60*(3*s+1)**145, 'all larger sixty-rise periods rejected')
    check(3**147 < 2**233 and 2**233*s**147 <= (3*s+1)**147,
          'first remaining arithmetic window retained')
    check(2*147-61 == 233, '61-rise first-window exponents restricted to one and two')
    expected_stages = [(147,233,6724,6723), (200,317,12824,12823),
                       (253,401,27113,27113), (306,485,99780,99779)]
    check([(r['period'],r['exponent_sum'],r['cycle_minimum_ceiling'],
            r['certified_odd_seed_bound']) for r in feedback['stages']] == expected_stages,
          'four period windows discharged on their complete minimum ranges')
    for row in feedback['stages']+[feedback['pending_window']]:
        m,A,u = row['period'],row['exponent_sum'],row['cycle_minimum_ceiling']
        check(2**A*u**m <= (3*u+1)**m and 2**A*(u+1)**m > (3*(u+1)+1)**m,
              'exact cycle-minimum ceiling endpoints')
    final = rd.period_sieve(seed_bound+2, 402, 971)
    check(final['period_ceiling'] == 968 and final['budget_excluded'], 'all-length 402-rise exclusion')
    check(final['first_unexcluded_window'] == [971,1539,403], 'next 403-rise window retained')
    for m in range(1,971):
        A,power = 0,1
        while power <= 3**m: power *= 2; A += 1
        check(power*(seed_bound+2)**m > (3*(seed_bound+2)+1)**m,
              'independent final period-window rejection')
    check((4*(seed_bound+2))**969 > 2**402*(3*(seed_bound+2)+1)**969,
          'all larger 402-rise periods rejected')
    check(2*971-403 == 1539, 'next sector retains 403 ones and 568 twos')
    s = seed_bound+2
    check(2**1540*s**971 > (3*s+1)**971, 'next power of two excluded in retained 971 window')
    check((4*s)**971 <= 2**403*(3*s+1)**971 and
          (4*s)**972 > 2**403*(3*s+1)**972, 'exact 403-rise period ceiling')
    import hashlib
    final_rows = json.dumps(final.pop('period_windows'), separators=(',', ':')).encode()
    final['all_period_rows_sha256'] = hashlib.sha256(final_rows).hexdigest()
    final['all_period_rows_regenerate_with'] = 'period_sieve(99781, 402, 971)'
    return {'initial_sieve': sieve, 'final_sieve': final}


def negative_checks(cells):
    bad = replace(cells[0], target_anchor=cells[0].target_anchor+2)
    tests = [lambda: rd.first_descent_cell(()), lambda: rd.first_descent_cell((0,)),
             lambda: rd.first_descent_cell((True,)), lambda: cells[0].parameter(2),
             lambda: rd.RootSplice(rd.cd.DescentCompression({}), [bad]),
             lambda: rd.RootSplice(rd.cd.DescentCompression({}, -1), []),
             lambda: rd.block_comparison((1, 2), (1,)),
             lambda: rd.block_comparison((1, 2), (0, 2)),
             lambda: rd.rising_blocks((2, 2)), lambda: rd.inverse([[0]]),
             lambda: rd.coefficient_crossing_box((1,)),
             lambda: rd.coefficient_crossing_box((2, 2)), lambda: td.descent_tail((2,)),
             lambda: rd.RootSplice(rd.cd.DescentCompression({}), [],
                [replace(td.descent_tail(()), threshold=1)])]
    for run in tests:
        try:
            run()
        except (ValueError, rd.cd.CertificateError):
            COUNTS['rejected invalid input'] += 1
        else:
            raise RuntimeError('invalid input accepted')
    return len(tests)


def run():
    cells, feedback = rd.bootstrap()
    atlas = feedback['final_atlas']
    small = cell_checks(cells)
    splice = splicing_checks(cells)
    tails = tail_checks(cells)
    blocks, prime_control = block_checks()
    crossings = crossing_checks()
    sieve = exclusion_checks(cells, atlas, feedback)
    invalid = negative_checks(cells)
    examples = {str(n): rd.first_descent_cell(rd.first_descent_word(n)).record()
                for n in (27, 43, 703)}
    return {'status': 'PASS', 'exact_checks': sum(COUNTS.values()), 'checks': dict(sorted(COUNTS.items())),
            'atlas': atlas, 'small_cell_fixtures': small, 'block_fixtures': blocks,
            'invalid_inputs_rejected': invalid, 'splice': splice, 'examples': examples, 'unbounded_tails': tails,
            'crossing_scan': crossings, 'period_sieve': sieve, 'period_feedback': feedback,
            'compressed_prime_power_control': {'word': prime_control['original_word'],
                 'Bbar': prime_control['Bbar'], 'forcing': prime_control['compressed_forcing'],
                 'D': prime_control['D'], 'forcing_order': 19},
            'global_collatz_proof_claimed': False, 'independent_external_review_claimed': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = run()
    text = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.output:
        args.output.write_text(text, encoding='utf-8')
    else:
        print(text, end='')
