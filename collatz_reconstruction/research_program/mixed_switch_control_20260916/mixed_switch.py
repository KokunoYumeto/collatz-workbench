#!/usr/bin/env python3
"""Exact mixed packet control on the original +1 Collatz source.

P=(1,2), Q=(1,1,1,2,1,1,4). A retained core is any ordered word
in P and Q containing both letters; every exponent-level phase is allowed.
The all-length theorem is proved in note.md. No finite timeout is a
nonconvergence certificate. No fractional fixed point is called an integer orbit.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from math import gcd
from collections import Counter
from typing import Iterable
import argparse
import json


class CertificateError(ValueError):
    pass


def need(test: bool, message: str) -> None:
    if not test:
        raise CertificateError(message)


def nat(x: int, minimum: int, name: str) -> None:
    need(type(x) is int and x >= minimum, f'{name} must be an integer >= {minimum}')


P = (1, 2)
Q = (1, 1, 1, 2, 1, 1, 4)
LETTERS = {'P': P, 'Q': Q}


@dataclass(frozen=True)
class Packet:
    word: tuple[int, ...]
    A: int
    L: int
    U: int
    C: int


def packet(word: Iterable[int]) -> Packet:
    w = tuple(word)
    need(all(type(a) is int and a >= 1 for a in w), 'positive integer exponents required')
    A, L, U, C = 0, 1, 1, 0
    for a in w:
        L, U, C, A = 3*L, U*(1 << a), 3*C+U, A+a
    return Packet(w, A, L, U, C)


def recover_word(m: int, A: int, C: int) -> tuple[int, ...]:
    """Inverse on the exact affine-packet image; no quotient of word order."""
    nat(m, 1, 'length'); nat(A, m, 'exponent sum'); nat(C, 1, 'numerator')
    original = (m, A, C)
    out = []
    while m > 1:
        rest = C-3**(m-1)
        need(rest > 0, 'not in the positive-word numerator image')
        a = v2(rest)
        need(1 <= a <= A-(m-1), 'invalid recovered exponent')
        out.append(a)
        C, A, m = rest//(1 << a), A-a, m-1
    need(C == 1, 'last affine numerator must be one')
    out.append(A)
    p = packet(out)
    need((len(out), p.A, p.C) == original, 'affine inverse failed')
    return tuple(out)


def v2(n: int) -> int:
    need(type(n) is int and n != 0, 'nonzero integer required')
    n = abs(n)
    return (n & -n).bit_length()-1


def step(n: int) -> tuple[int, int]:
    need(type(n) is int and n > 0 and n % 2 == 1, 'positive odd source required')
    b = 3*n+1
    a = v2(b)
    return b//(1 << a), a


def core(symbols: str, phase: int = 0) -> dict:
    need(type(symbols) is str and symbols and set(symbols) <= set(LETTERS), 'P/Q word required')
    need('P' in symbols and 'Q' in symbols, 'both packet types are required by this theorem')
    raw = tuple(a for symbol in symbols for a in LETTERS[symbol])
    nat(phase, 0, 'phase'); need(phase < len(raw), 'phase outside original word')
    p = packet(raw[phase:]+raw[:phase])
    delta = p.L-p.U
    need(delta > 0, 'core must be expanding')
    g = gcd(p.C, delta)
    c, d = p.C//g, delta//g
    need(0 < c <= 91*d and gcd(d, 6) == 1, 'original rational anchor bound failed')
    need(2*p.U*p.U > c, 'positive-source parameter threshold failed')
    return {'symbols': symbols, 'phase': phase, 'word': list(p.word),
            'P_count': symbols.count('P'), 'Q_count': symbols.count('Q'),
            'm': len(p.word), 'A': p.A, 'L': p.L, 'U': p.U, 'C': p.C,
            'delta': delta, 'anchor_numerator': c, 'anchor_denominator': d,
            'raw_forcing_class': p.C % delta, 'forcing_class_order': d,
            'anchor_is_integer': d == 1,
            'original_affine_inverse_word': list(recover_word(len(p.word), p.A, p.C))}


def power_data(c: dict, repetitions: int) -> tuple[int, int, int]:
    nat(repetitions, 2, 'repetitions')
    L, U = c['L']**repetitions, c['U']**repetitions
    num = c['anchor_numerator']*(L-U)
    den = c['anchor_denominator']
    need(num % den == 0, 'original power numerator failed integrality')
    return L, U, num//den


def source_chart(symbols: str, phase: int, repetitions: int) -> dict:
    c = core(symbols, phase)
    L, U, C = power_data(c, repetitions)
    d, h = c['anchor_denominator'], c['anchor_numerator']
    t0 = (h*pow(2*U, -1, d)) % d if d > 1 else 0
    tmin = t0 if t0 else d
    n_num, y_num = 2*U*tmin-h, 2*L*tmin-h
    need(n_num > 0 and n_num % d == 0 and y_num % d == 0, 'source lattice failed')
    n, y = n_num//d, y_num//d
    rho = ((U-C)*pow(L, -1, 2*U)) % (2*U)
    need(n == rho and n % 2 == y % 2 == 1, 'canonical source cylinder failed')
    return {'core': c, 'repetitions': repetitions, 'parameter_residue': t0,
            'parameter_modulus': d, 'parameter_minimum': tmin,
            'source_anchor': n, 'source_step': 2*U,
            'target_anchor': y, 'target_step': 2*L,
            'L': L, 'U': U, 'C': C,
            'domain': 'z>=0 integral; t=tmin+d*z; n=(2*U*t-c)/d'}


def gap_margin(P_count: int, Q_count: int, r: int, s: int, B: int) -> int:
    nat(P_count, 1, 'P count'); nat(Q_count, 1, 'Q count')
    nat(r, 2, 'repetitions'); nat(s, 1, 'tail length'); nat(B, 2*s, 'tail sum')
    m, A = 2*P_count+7*Q_count, 3*P_count+11*Q_count
    L, U = 3**m, 1 << A
    return (U**r-46*L)*(1 << B)-(L**r-46*L)*3**s


def family(symbols: str, phase: int, repetitions: int, tail: Iterable[int]) -> dict:
    c = core(symbols, phase)
    tail = tuple(tail)
    need(tail and all(type(a) is int and a >= 2 for a in tail), 'nonempty falling tail required')
    Lp, Up, Cp = power_data(c, repetitions)
    q = packet(tail)
    L, U, C = q.L*Lp, q.U*Up, q.L*Cp+Up*q.C
    D = U-L
    rho = ((U-C)*pow(L, -1, 2*U)) % (2*U)
    numerator = L*rho+C
    need(rho > 0 and numerator % U == 0, 'full source cylinder failed')
    y = numerator//U
    d, h = c['anchor_denominator'], c['anchor_numerator']
    t_num = d*rho+h
    need(t_num % (2*Up) == 0, 'mixed denominator source map failed')
    t = t_num//(2*Up)
    E = q.C+q.L-q.U
    need(E <= 0, 'falling affine correction sign failed')
    displacement = 2*D*t-(h+d)*(q.U-q.L)-d*E
    need(displacement == d*q.U*(rho-y), 'raw mixed displacement identity failed')
    margin = gap_margin(c['P_count'], c['Q_count'], repetitions, len(tail), q.A)
    accepted = D > 0
    if accepted:
        need(margin > 0 and rho > y > 0, 'proved mixed gap/descent failed')
    return {'core': c, 'repetitions': repetitions, 'tail': list(tail),
            'length': c['m']*repetitions+len(tail),
            'A': c['A']*repetitions+q.A, 'L': L, 'U': U, 'C': C, 'D': D,
            'source_anchor': rho, 'source_step': 2*U,
            'target_anchor': y, 'target_step': 2*L,
            'anchor_parameter': t, 'tail_anchored_forcing': E,
            'mixed_displacement_numerator': displacement,
            'count_uniform_gap_margin': margin,
            'status': 'PROVED_WHOLE_CYLINDER_DESCENT' if accepted else 'RETAINED_BEFORE_CROSSING',
            'source_domain': 'original n=source_anchor+source_step*z, integer z>=0',
            'parameter_at_z': f't={t}+{d*q.U}*z',
            'forcing': 1}


def validate_family(record: dict) -> None:
    need(type(record) is dict and type(record.get('core')) is dict, 'family object required')
    c = record['core']
    need(record == family(c.get('symbols'), c.get('phase'), record.get('repetitions'), record.get('tail', ())),
         'certificate differs from exact original reconstruction')


def path(n: int, word: Iterable[int]) -> dict:
    values, actual, x = [n], [], n
    for a in word:
        y, k = step(x)
        need(a == k, 'not the original valuation word')
        values.append(y); actual.append(k); x = y
    ch = Counter(values[:-1])
    return {'values': values, 'exponents': actual,
            'chain': {str(k): v for k, v in sorted(ch.items())},
            'boundary': {str(n): 1, str(x): -1} if n != x else {}}


def switch_chart(h: int, k: int, L: int, U: int, repetitions: int, depth: int) -> dict:
    """Exact synchronized fibres at a packet endpoint; depths are NOT truncated.

    x+h=2*U**r*t, y+h=2*L**r*t, y+k=2*(L**r*t+(k-h)/2).
    Here h,k are declared odd integral anchors and U a positive power of two.
    """
    need(type(h) is int and type(k) is int and h > 0 and k > 0 and h % 2 == k % 2 == 1,
         'positive odd anchors required')
    nat(L, 1, 'L'); nat(U, 2, 'U'); nat(repetitions, 1, 'repetitions'); nat(depth, 0, 'depth')
    need(L % 2 == 1 and U & (U-1) == 0, 'odd multiplier/power-of-two denominator required')
    b = (k-h)//2
    modulus = 1 << (depth+1)
    residue = (((1 << depth)-b)*pow(L**repetitions, -1, modulus)) % modulus
    return {'h': h, 'k': k, 'L': L, 'U': U, 'r': repetitions,
            'cross_term': b, 'exact_next_coordinate_depth': depth+1,
            'parameter_residue': residue, 'parameter_modulus': modulus,
            'source_formula': f'{2*U**repetitions}*t-{h}',
            'target_formula': f'{2*L**repetitions}*t-{h}'}


def interpolate_two(h: int, k: int, left: int, right: int) -> tuple[int, int]:
    """Inverse onto the image of f -> (f(-h),f(-k)), for degree<2."""
    need(all(type(x) is int for x in (h,k,left,right)) and h != k, 'distinct integer anchors required')
    need((right-left) % (h-k) == 0, 'pair violates the retained conductor congruence')
    slope = (right-left)//(h-k)
    return left+h*slope, slope



def two_packet_chart(first: str, r: int, second: str, s: int) -> dict:
    """All original sources of P**r Q**s or Q**r P**s, with exact seam."""
    need(first in LETTERS and second in LETTERS and first != second, 'distinct packet types required')
    nat(r, 1, 'first repetition'); nat(s, 1, 'second repetition')
    a, b = packet(LETTERS[first]), packet(LETTERS[second])
    h, k = (5 if first == 'P' else 17), (5 if second == 'P' else 17)
    cross = (k-h)//2
    modulus = b.U**s
    t0 = (-cross*pow(a.L**r, -1, modulus)) % modulus
    need(t0 > 0, 'nonzero mixed seam residue required')
    znum = a.L**r*t0+cross
    need(znum > 0 and znum % modulus == 0, 'seam inverse failed')
    z0 = znum//modulus
    n = 2*a.U**r*t0-h
    mid = 2*a.L**r*t0-h
    y = 2*b.L**s*z0-k
    total = packet(LETTERS[first]*r+LETTERS[second]*s)
    rho = ((total.U-total.C)*pow(total.L, -1, 2*total.U)) % (2*total.U)
    need(n == rho and mid == 2*b.U**s*z0-k, 'seam source cylinder mismatch')
    need(v2(n+h) == a.A*r+2 and v2(mid+h) == 2, 'induced dyadic filtration mismatch')
    return {'first': first, 'first_repetitions': r, 'second': second,
            'second_repetitions': s, 'cross_term': cross,
            't_minimum': t0, 't_step': modulus, 'z_minimum': z0, 'z_step': a.L**r,
            'source_anchor': n, 'source_step': 2*total.U,
            'intermediate_anchor': mid, 'intermediate_step': 2*a.L**r*modulus,
            'target_anchor': y, 'target_step': 2*total.L,
            'original_n_plus_h_depth': a.A*r+2,
            'intermediate_plus_h_depth': 2,
            'full_word': list(total.word), 'L': total.L, 'U': total.U, 'C': total.C}



def induced_filtration(depth: int) -> dict:
    """I_k/2^k Lambda for Lambda={(a,b):12 divides b-a}."""
    nat(depth, 0, 'filtration depth')
    scale = 1 << depth
    order = gcd(12, scale)
    return {'depth': depth, 'scale': scale, 'defect_order': order,
            'induced_basis': [[scale,scale],[0,scale*(12//order)]],
            'source_image_basis': [[scale,scale],[0,scale*12]],
            'quotient_generator': [0,scale*(12//order)],
            'quotient_map': '(b/2^k-a/2^k)/(12/g) modulo g, g=gcd(12,2^k)'}

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('symbols', help='ordered P/Q string containing both types')
    ap.add_argument('--phase', type=int, default=0)
    ap.add_argument('--repeat', type=int, default=2)
    ap.add_argument('--tail', type=int, nargs='+', default=[2])
    ap.add_argument('--output')
    args = ap.parse_args()
    try:
        result = family(args.symbols, args.phase, args.repeat, args.tail)
    except CertificateError as exc:
        ap.error(str(exc))
    text = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.output:
        from pathlib import Path
        Path(args.output).write_text(text, encoding='utf-8')
    else:
        print(text, end='')


if __name__ == '__main__':
    main()
