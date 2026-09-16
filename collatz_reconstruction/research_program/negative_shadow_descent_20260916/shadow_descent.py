#!/usr/bin/env python3
"""Exact positive-source descent for two explicitly verified negative orbit packets.

The arithmetic forcing is ALWAYS 3*x+1. Negative integers are used to verify
specified integral packet anchors, not to replace the positive source. Every
returned positive family retains its original full word and affine lattice.
The all-length theorem depends on the separately documented logarithm input
and the finite integer certificate checked by verify.py.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from math import comb, gcd
import json
from typing import Iterable


class CertificateError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CertificateError(message)


def integer(value: int, lower: int, name: str) -> None:
    require(type(value) is int and value >= lower, f'{name} must be an integer >= {lower}')


def valuation2(n: int) -> int:
    require(type(n) is int and n != 0, 'nonzero integer required for valuation')
    n = abs(n)
    return (n & -n).bit_length()-1


def step(n: int) -> tuple[int, int]:
    require(type(n) is int and n % 2 == 1, 'nonzero odd integer required')
    numerator = 3*n+1
    a = valuation2(numerator)
    require(a >= 1, 'odd-return parity failed')
    return numerator // (1 << a), a


@dataclass(frozen=True)
class Packet:
    word: tuple[int, ...]
    A: int
    L: int
    C: int

    @property
    def U(self) -> int:
        return 1 << self.A

    @property
    def D(self) -> int:
        return self.U-self.L


def packet(word: Iterable[int]) -> Packet:
    w = tuple(word)
    require(all(type(a) is int and a >= 1 for a in w), 'positive integer exponents required')
    A, L, C = 0, 1, 0
    for a in w:
        C = 3*C+(1 << A)
        L *= 3
        A += a
    return Packet(w, A, L, C)


def concatenate(p: Packet, q: Packet) -> Packet:
    return Packet(p.word+q.word, p.A+q.A, q.L*p.L, q.L*p.C+p.U*q.C)


# The declared signed cycles are independently replayed by the verifier.
# Each dictionary value is the word STARTING AT -h; no rotation is discarded.
ANCHORS = {
    5: (1, 2),
    7: (2, 1),
    17: (1, 1, 1, 2, 1, 1, 4),
    25: (1, 1, 2, 1, 1, 4, 1),
    37: (1, 2, 1, 1, 4, 1, 1),
    55: (2, 1, 1, 4, 1, 1, 1),
    41: (1, 1, 4, 1, 1, 1, 2),
    61: (1, 4, 1, 1, 1, 2, 1),
    91: (4, 1, 1, 1, 2, 1, 1),
}


def anchor_packet(h: int) -> Packet:
    require(type(h) is int and h in ANCHORS, 'anchor must be one of the nine certified values')
    p = packet(ANCHORS[h])
    require(p.C == h*(p.L-p.U) and p.L > p.U, 'original negative anchor identity failed')
    return p


def shadow(h: int, repetitions: int, t: int) -> dict:
    p = anchor_packet(h)
    integer(repetitions, 1, 'repetitions')
    integer(t, 1, 'source parameter')
    U, L = p.U**repetitions, p.L**repetitions
    n, y = 2*U*t-h, 2*L*t-h
    require(n > 0 and y > 0, 'positive shadow source required')
    return {
        'anchor_magnitude': h, 'original_forcing': 1,
        'packet_word': list(p.word), 'repetitions': repetitions, 'parameter': t,
        'source': n, 'packet_endpoint': y,
        'source_step': 2*U, 'packet_target_step': 2*L,
        'section_defect': p.C-p.D*n,
        'supported_anchor_forcing_class': 0,
        'anchor_is_positive_cycle': False,
    }


def original_path(n: int, word: Iterable[int]) -> dict:
    w = tuple(word)
    require(type(n) is int and n > 0 and n % 2 == 1, 'positive odd path source required')
    values, exponents, current = [n], [], n
    for expected in w:
        nxt, actual = step(current)
        require(actual == expected, 'prescribed word differs from the actual valuation')
        require(nxt > 0, 'positive source left its original domain')
        exponents.append(actual)
        values.append(nxt)
        current = nxt
    chain = Counter(values[:-1])
    return {'source': n, 'endpoint': current, 'values': values, 'word': exponents,
            'original_edge_chain': {str(k): v for k, v in sorted(chain.items())},
            'strict_descent': current < n}


def gap_value(U: int, L: int, K: int, r: int, s: int, B: int) -> int:
    """Positive value proves D > K*(2**B-3**s), with no division."""
    return (U**r-K)*(1 << B)-(L**r-K)*3**s


def least_contracting_tail_sum(U: int, L: int, r: int, s: int) -> int:
    require(U > 0 and L > U, 'expanding packet required')
    integer(r, 1, 'repetitions'); integer(s, 1, 'tail length')
    B = 2*s
    lhs, rhs = U**r*(1 << B), L**r*3**s
    while lhs <= rhs:
        lhs *= 2
        B += 1
    return B


def family(h: int, repetitions: int, tail: Iterable[int]) -> dict:
    """Complete original cylinder for p_h**r followed by this fall word.

    The original parameter v is >=0. Status RETAINED means that the theorem's
    coefficient-crossing domain was not reached, never a divergence verdict.
    """
    p = anchor_packet(h)
    integer(repetitions, 1, 'repetitions')
    tail = tuple(tail)
    require(tail and all(type(c) is int and c >= 2 for c in tail), 'nonempty tail of exponents >=2 required')
    q = packet(tail)
    U, L = p.U**repetitions, p.L**repetitions
    # Full packet power is computed by its exact integer section, not expanded.
    Cpower = h*(L-U)
    total_U, total_L = U*q.U, L*q.L
    total_C = q.L*Cpower+U*q.C
    D = total_U-total_L
    q_residue = ((q.U-q.C)*pow(q.L, -1, 2*q.U)) % (2*q.U)
    t0 = (((q_residue+h)//2)*pow(L, -1, q.U)) % q.U
    tmin = t0 if t0 > 0 else q.U
    n0 = 2*U*tmin-h
    numerator = total_L*n0+total_C
    require(n0 > 0 and numerator % total_U == 0, 'affine cylinder anchor failed')
    y0 = numerator//total_U
    canonical = ((total_U-total_C)*pow(total_L, -1, 2*total_U)) % (2*total_U)
    require(n0 == canonical and n0 % 2 == 1 and y0 % 2 == 1, 'original cylinder comparison failed')
    margin = gap_value(p.U, p.L, (h+1)//2, repetitions, len(tail), q.A)
    accepted = D > 0
    if accepted:
        require(margin > 0 and y0 < n0, 'certified gap/descent inequality failed')
    return {
        'anchor_magnitude': h, 'original_forcing': 1,
        'packet_word': list(p.word), 'repetitions': repetitions, 'tail_word': list(tail),
        'word_length': len(p.word)*repetitions+len(tail), 'total_exponent': p.A*repetitions+q.A,
        'original_L': total_L, 'original_U': total_U, 'original_C': total_C, 'original_D': D,
        'tail_anchored_forcing': q.C+q.L-q.U,
        'original_section_defect_at_shadow_min': total_C-D*(2*U-h),
        'shadow_parameter_residue': t0, 'shadow_parameter_modulus': q.U,
        'shadow_parameter_least_positive': tmin,
        'source_anchor': n0, 'source_step': 2*total_U,
        'target_anchor': y0, 'target_step': 2*total_L,
        'parameter_domain': 'v >= 0, integer; t=tmin+2^B*v',
        'gap_margin_for_original_anchor': margin,
        'strict_descent_for_whole_cylinder': accepted,
        'status': 'CERTIFIED_DESCENT' if accepted else 'RETAINED_OUTSIDE_CROSSING_DOMAIN',
        'positive_cycle_realization_of_full_word': False if accepted else None,
    }


def validate_family(record: dict) -> None:
    require(isinstance(record, dict), 'family certificate must be an object')
    expected = family(record.get('anchor_magnitude'), record.get('repetitions'), record.get('tail_word', ()))
    require(record == expected, 'family certificate differs from original reconstruction')


def residual_counts(h: int, repetitions: int) -> dict:
    """Exact finite language before the fall-tail coefficient crossing.

    For a fixed shadow p**r, enumerate the counts of tails with c_i>=2 and
    D<=0. Their next exponent 1 exits the current theorem's language. All
    other sufficiently large tail exponents are certified, never overflow.
    Counts do not assert that every residual label is a nonconvergent source.
    """
    p = anchor_packet(h)
    integer(repetitions, 1, 'repetitions')
    rows = [{'tail_length': 0, 'maximum_tail_sum': 0, 'words': 1}]
    for s in range(1, 2*repetitions+1):
        H = (p.L**repetitions*3**s).bit_length()-1-p.A*repetitions
        if H < 2*s:
            break
        rows.append({'tail_length': s, 'maximum_tail_sum': H, 'words': comb(H-s, s)})
    require(rows[-1]['tail_length'] < 2*repetitions, 'coarse finite-tail bound failed')
    return {'anchor_magnitude': h, 'repetitions': repetitions,
            'rows': rows, 'total_retained_tail_words': sum(row['words'] for row in rows),
            'status': 'FINITE_WORD_FIBRES_RETAINED_NOT_DIVERGENCE'}


def falling_prefix_after_shadow(h: int, repetitions: int, t: int, tail_cap: int = 10000) -> dict:
    """Query original values. Finite budget is explicit; no global search implied."""
    integer(tail_cap, 1, 'tail cap')
    sh = shadow(h, repetitions, t)
    p = anchor_packet(h)
    current, tail = sh['packet_endpoint'], []
    while len(tail) < tail_cap:
        nxt, c = step(current)
        if c == 1:
            return {'shadow': sh, 'tail_word': tail, 'terminal': current,
                    'status': 'RETAINED_SWITCH_TO_EXPONENT_ONE'}
        tail.append(c)
        current = nxt
        U = p.U**repetitions*(1 << sum(tail))
        L = p.L**repetitions*3**len(tail)
        if U > L:
            rec = family(h, repetitions, tail)
            v, rem = divmod(sh['source']-rec['source_anchor'], rec['source_step'])
            require(rem == 0 and v >= 0, 'source not in its original family')
            path = original_path(sh['source'], p.word*repetitions+tuple(tail))
            require(path['strict_descent'], 'queried source does not descend')
            return {'shadow': sh, 'family': rec, 'family_parameter': v, 'path': path,
                    'status': 'CERTIFIED_DESCENT'}
    return {'shadow': sh, 'tail_word': tail, 'terminal': current, 'status': 'RETAINED_AT_FINITE_CAP'}



def reset_after_three(repetitions: int, t: int = 1) -> dict:
    """Exact next exponent-one run after p_5**r and the actual exponent 3.

    This is the entire t == 1 (mod 8) stratum, with its original parameter.
    A return count is not a global rank: the t-dependence remains visible.
    """
    integer(repetitions, 1, 'repetitions'); integer(t, 1, 'parameter')
    require(t % 8 == 1, 'the exponent-three stratum requires t == 1 modulo 8')
    sh = shadow(5, repetitions, t)
    x, a = step(sh['packet_endpoint'])
    require(a == 3 and x == (3*9**repetitions*t-7)//4, 'retained exponent-three formula failed')
    k = valuation2(9**repetitions*t-1)-3
    require(k >= 0, 'next maximal rising-run length must be nonnegative')
    numerator = 3**(k+1)*(9**repetitions*t-1)
    require(numerator % (1 << (k+2)) == 0, 'rising endpoint must be integral')
    endpoint = numerator//(1 << (k+2))-1
    residue = (pow(9**repetitions, -1, 1 << (k+4))*(1+(1 << (k+3)))) % (1 << (k+4))
    require(t % (1 << (k+4)) == residue, 'full exact reset stratum failed')
    if t == 1:
        require(k == valuation2(repetitions), 'exact exponent-lifting identity failed')
    return {'source':sh['source'], 'packet_endpoint':sh['packet_endpoint'],
            'repetitions':repetitions, 'parameter':t, 'next_exponent':3,
            'after_three':x, 'next_maximal_one_run':k, 'after_one_run':endpoint,
            'exact_parameter_residue':residue, 'exact_parameter_modulus':1 << (k+4),
            'old_packet_depth':valuation2(sh['source']+5),
            'global_decreasing_rank_claim':False}


def switched_repair_family() -> dict:
    """Fully specified residual switch, returned as a whole original cylinder."""
    word = (1,2)*12 + (3,1,1,2,1,2,1,2,1,7)
    p = packet(word)
    n0 = ((p.U-p.C)*pow(p.L,-1,2*p.U)) % (2*p.U)
    y0, rem = divmod(p.L*n0+p.C, p.U)
    require(rem == 0 and n0 == 137438953467 and y0 == 15904599857,
            'original switched-repair anchors failed')
    require(p.D > 0 and p.D*n0 > p.C, 'whole switched-repair cylinder does not descend')
    require(all(packet(word[:j]).D <= 0 for j in range(1,len(word))),
            'earlier first-descent coefficient crossing retained')
    return {'word':list(word), 'source_anchor':n0,'source_step':2*p.U,
            'target_anchor':y0,'target_step':2*p.L,'parameter_domain':'v>=0 integer',
            'L':p.L,'U':p.U,'C':p.C,'D':p.D,'all_proper_prefix_D_nonpositive':True,
            'whole_cylinder_first_descent':True,
            'theorem_dependency':'direct original affine identities only'}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    f = sub.add_parser('family'); f.add_argument('anchor', type=int); f.add_argument('repetitions', type=int)
    f.add_argument('tail', type=int, nargs='+')
    q = sub.add_parser('query'); q.add_argument('anchor', type=int); q.add_argument('repetitions', type=int)
    q.add_argument('parameter', type=int); q.add_argument('--tail-cap', type=int, default=10000)
    c = sub.add_parser('residual'); c.add_argument('anchor', type=int); c.add_argument('repetitions', type=int)
    z = sub.add_parser('reset'); z.add_argument('repetitions',type=int); z.add_argument('parameter',type=int,nargs='?',default=1)
    sub.add_parser('repair')
    args = parser.parse_args()
    try:
        if args.command == 'family': result = family(args.anchor, args.repetitions, args.tail)
        elif args.command == 'query': result = falling_prefix_after_shadow(args.anchor, args.repetitions, args.parameter, args.tail_cap)
        elif args.command == 'residual': result = residual_counts(args.anchor, args.repetitions)
        elif args.command == 'reset': result = reset_after_three(args.repetitions,args.parameter)
        else: result = switched_repair_family()
    except (CertificateError, TypeError, OverflowError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
