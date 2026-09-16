#!/usr/bin/env python3
"""Original Collatz section defects, repetition ranks, and symbolic run descent.

All coordinates remain integers on their explicitly checked source domains.
A zero return defect is recorded as a supported return, never as absence.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from typing import Iterable, Mapping


RUN_SLOPE_NUMERATOR = 2124
RUN_SLOPE_DENOMINATOR = 1507


class CertificateError(ValueError):
    pass


def require(ok: bool, message: str) -> None:
    if not ok:
        raise CertificateError(message)


def positive_odd(n: int) -> None:
    require(type(n) is int and n > 0 and n % 2 == 1, 'positive odd integer required')


def valuation(n: int) -> int | None:
    require(type(n) is int, 'integer valuation input required')
    if n == 0:
        return None  # explicit infinite valuation of a supported zero
    n = abs(n)
    return (n & -n).bit_length() - 1


def step(n: int) -> tuple[int, int]:
    positive_odd(n)
    z = 3*n+1
    a = valuation(z)
    require(a is not None and a >= 1, 'invalid odd-return valuation')
    return z >> a, a


@dataclass(frozen=True)
class Packet:
    word: tuple[int, ...]
    A: int
    L: int
    U: int
    C: int

    @property
    def D(self) -> int:
        return self.U-self.L

    def defect(self, n: int) -> int:
        return self.C-self.D*n

    def apply(self, n: int) -> int:
        q, rem = divmod(self.L*n+self.C, self.U)
        require(rem == 0 and q > 0 and q % 2 == 1,
                'source not in the full exact-word cylinder')
        return q


def packet(word: Iterable[int]) -> Packet:
    w = tuple(word)
    require(bool(w), 'nonempty exponent word required')
    require(all(type(a) is int and a >= 1 for a in w), 'positive integral exponents required')
    A, L, U, C = 0, 1, 1, 0
    for a in w:
        A, L, U, C = A+a, 3*L, U*(1 << a), 3*C+U
    return Packet(w, A, L, U, C)


def legal_source(n: int, p: Packet) -> bool:
    positive_odd(n)
    return p.defect(n) % (2*p.U) == 0


def repeat_count(n: int, word: Iterable[int]) -> int | None:
    """Number of complete initial copies of word; None means actual return."""
    positive_odd(n)
    p = packet(word)
    h = p.defect(n)
    depth = valuation(h)
    if depth is None:
        return None
    require(depth >= 1, 'original odd source must have an even section defect')
    return (depth-1)//p.A


def repeat_endpoint(n: int, word: Iterable[int], copies: int) -> int:
    p = packet(word)
    positive_odd(n)
    require(type(copies) is int and copies >= 0, 'nonnegative integral copy count required')
    count = repeat_count(n, p.word)
    require(count is None or copies <= count, 'copies exceed the exact original repetition rank')
    if copies == 0:
        return n
    # h(F_p^r(n)) = L^r h(n)/U^r, and h(x)=C-D*x.
    hr, rem = divmod(p.L**copies*p.defect(n), p.U**copies)
    require(rem == 0, 'nonintegral transported section defect')
    y, rem = divmod(p.C-hr, p.D)
    require(rem == 0 and y > 0 and y % 2 == 1, 'nonintegral repeated endpoint')
    return y


def repeat_record(n: int, word: Iterable[int]) -> dict:
    p = packet(word)
    count = repeat_count(n, p.word)
    h = p.defect(n)
    result = {'source': n, 'word': list(p.word), 'A': p.A, 'L': p.L,
              'U': p.U, 'C': p.C, 'D': p.D, 'section_defect': h,
              'defect_valuation': valuation(h), 'complete_initial_copies': count,
              'supported_zero': h == 0, 'external_absence': False,
              'affine_fixed_point': str(Fraction(p.C, p.D))}
    if count is None:
        require(legal_source(n,p) and p.apply(n) == n, 'return-zero verification failed')
        result['status'] = 'actual_positive_return'
        result['terminal'] = n
    else:
        y = repeat_endpoint(n,p.word,count)
        require(not legal_source(y,p), 'maximal repetition endpoint still admits another full copy')
        result['status'] = 'finite_repetition_rank'
        result['terminal'] = y
        result['terminal_defect_valuation'] = valuation(p.defect(y))
    return result


def switch_record(n: int, first: Iterable[int], second: Iterable[int]) -> dict:
    p, q = packet(first), packet(second)
    require(legal_source(n,p), 'first packet must be the actual exponent word')
    y = p.apply(n)
    hp, hq = p.defect(n), q.defect(y)
    delta = p.D*q.C-q.D*p.C
    transported, rem = divmod(p.L*hp,p.U)
    require(rem == 0, 'first defect did not transport integrally')
    require(p.D*hq == q.D*transported+delta, 'packet-switch identity failed')
    t, r = valuation(transported), valuation(delta)
    exact = valuation(hq)
    if t == r:
        mode = 'resonant_layer' if t is not None else 'common_supported_return'
    else:
        predicted = r if t is None else t if r is None else min(t,r)
        require(exact == predicted, 'nonresonant valuation prediction failed')
        mode = 'nonresonant_exact_minimum'
    return {'source':n, 'target':y, 'first_word':list(p.word), 'second_word':list(q.word),
            'first_source_defect':hp, 'first_target_defect':transported,
            'second_target_defect':hq, 'resultant':delta,
            'first_target_depth':t, 'resultant_depth':r,
            'second_target_depth':exact, 'mode':mode}


def actual_path(n: int, word: Iterable[int]) -> tuple[list[int], dict[int,int]]:
    p = packet(word)
    x, values, chain = n, [n], Counter()
    for a in p.word:
        y, observed = step(x)
        require(a == observed, 'word is not the original actual valuation sequence')
        chain[x] += 1
        values.append(y)
        x = y
    require(x == p.apply(n), 'path and affine endpoint disagree')
    return values, dict(sorted(chain.items()))


def clean(c: Mapping[int,int]) -> dict[int,int]:
    return {k:v for k,v in sorted(c.items()) if v}


def boundary(c: Mapping[int,int]) -> dict[int,int]:
    out = Counter()
    for n,k in c.items():
        positive_odd(n)
        require(type(k) is int, 'integral edge coefficient required')
        out[n] += k
        out[step(n)[0]] -= k
    return clean(out)


def target(c: Mapping[int,int]) -> dict[int,int]:
    out = Counter()
    for n,k in c.items():
        positive_odd(n)
        require(type(k) is int, 'integral edge coefficient required')
        out[step(n)[0]] += k
    return clean(out)


def jet_boundary(b: Mapping[int,int], c: Mapping[int,int]) -> tuple[dict,dict]:
    out = Counter(boundary(c)); out.subtract(target(b))
    return boundary(b), clean(out)


def run_witness(n: int, rise_count: int, fall_word: Iterable[int]) -> dict:
    """Exact endpoint theorem for an original 1-run followed by a fall run.

    A pure-2 contracting run is nonincreasing, with equality retained as an
    actual return. A run with a >=3 letter is strictly decreasing whenever
    the pure-2 multiplier already contracts. The finite slope certificate
    proves b>=ceil(2124*a/1507) strictly decreasing, including the pure-2 case.
    """
    require(type(rise_count) is int and rise_count >= 1, 'positive rise count required')
    tail = tuple(fall_word)
    require(tail and all(type(c) is int and c >= 2 for c in tail), 'nonempty fall word with exponents >=2 required')
    a, b = rise_count, len(tail)
    p = packet((1,)*a+tail)
    values, chain = actual_path(n,p.word)
    y = values[-1]
    D2 = (1 << (a+2*b))-3**(a+b)
    threshold = (RUN_SLOPE_NUMERATOR*a+RUN_SLOPE_DENOMINATOR-1)//RUN_SLOPE_DENOMINATOR
    long_run = b >= threshold
    require(D2 > 0, 'the proved contracting-run domain is not satisfied')
    pure = all(c == 2 for c in tail)
    result = {'source':n, 'target':y, 'rise_count':a, 'fall_word':list(tail),
              'word':list(p.word), 'original_values':values,
              'original_edge_chain':chain, 'pure_two_defect':D2,
              'long_run_threshold':threshold,
              'elementary_long_run_threshold':(3*a+1)//2,
              'long_run_domain':long_run, 'pure_two_fall':pure,
              'strict_descent':y<n}
    if pure:
        z,rem = divmod(y-1, 2*3**b)
        require(rem == 0 and z >= 1, 'pure-two original integer parameter failed')
        k,rem = divmod(D2*z+(1 << a),3**a)
        require(rem == 0 and k >= 1, 'positive integral nonexpansion certificate failed')
        require(n-y == 2*(k-1), 'original displacement formula failed')
        result.update({'z':z, 'integral_displacement_index':k,
                       'supported_return_zero':k == 1})
        if long_run:
            require(D2 > 3**a-(1 << a), 'long-run integer power inequality failed')
            require(k >= 2 and y < n, 'long-run strict descent failed')
    else:
        require(y < n, 'higher-exponent strict descent failed')
    expected = Counter({n:1}); expected[y]-=1
    require(boundary(chain)==clean(expected), 'original run boundary failed')
    require(jet_boundary({},chain)==({},clean(expected)), 'infinitesimal run boundary failed')
    return result


def resonant_family(r: int, v: int) -> dict:
    require(type(r) is int and r >= 2 and type(v) is int and v >= 0,
            'family domain is r>=2, v>=0')
    s = 6*v+1
    n = ((1 << (2*r+3))*s+1)//3
    y = 4*3**r*s+1
    result = run_witness(n,1,(2,)*r)
    require(result['target']==y, 'resonant-family endpoint failed')
    sw = switch_record(n,(1,),(2,))
    require(valuation(n+1)==2 and sw['second_target_depth']==2*r+2,
            'unbounded rank reset formula failed')
    require(repeat_count(step(n)[0],(2,))==r, 'maximal two-run length failed')
    result.update({'family_r':r,'family_v':v,'family_s':s,
                   'source_anchor':((1 << (2*r+3))+1)//3,
                   'source_step':1 << (2*r+4),
                   'target_anchor':4*3**r+1,
                   'target_step':24*3**r,
                   'switch':sw})
    return result


def rising_tail(n: int) -> dict:
    positive_odd(n)
    r = valuation(n+1)-1
    t = (n+1) >> (r+1)
    y = 2*3**r*t-1
    require(t > 0 and t%2 == 1 and y%4==1, 'rising-tail coordinates failed')
    values = [3**j*(1 << (r+1-j))*t-1 for j in range(r+1)]
    for x,z in zip(values,values[1:]):
        require(step(x)==(z,1), 'rising-tail edge failed')
    return {'source':n,'target':y,'r':r,'t':t,'values':values,
            'source_inverse':(1 << (r+1))*t-1}


def peak_block(n: int) -> dict:
    positive_odd(n)
    require(n%4==1, 'peak-source set is the original class 1 modulo 4')
    x,a = step(n)
    tail = rising_tail(x)
    require(a>=2, 'peak-source exponent failed')
    values = [n]+tail['values']
    length = len(values)-1
    c0, c1 = Counter(), Counter()
    for j,x in enumerate(values[:-1]):
        c0[x]+=1; c1[x]+=j
    expected0 = Counter({n:1}); expected0[values[-1]]-=1
    expected1 = {values[-1]:-length}
    require(jet_boundary(c0,c1)==(clean(expected0),expected1),
            'block first-jet length was not retained')
    return {'source':n,'target':values[-1],'initial_exponent':a,
            'rising_run':tail['r'],'odd_return_length':length,
            'word':[a]+[1]*tail['r'],'values':values,
            'jet_constant_chain':clean(c0),'jet_linear_chain':clean(c1)}


def slope_certificate(numerator: int = RUN_SLOPE_NUMERATOR,
                      denominator: int = RUN_SLOPE_DENOMINATOR) -> dict:
    """Check a finite, sound certificate for an all-length descent cone.

    Each of the q residue cases is checked on integers. The documented
    induction (a,b)->(a+q,b+p) proves the unbounded family.
    """
    p,q=numerator,denominator
    require(type(p) is int and type(q) is int and p>=1 and q>=1,
            'positive integral slope coordinates required')
    block_U=1 << (q+2*p);block_L=3**(q+p)
    require(block_U>block_L, 'slope block does not contract')
    sha=hashlib.sha256();least=None
    for a in range(1,q+1):
        b=(p*a+q-1)//q
        D=(1 << (a+2*b))-3**(a+b)
        target=3**a-(1 << a)
        require(D>target,'slope base case does not give strict descent')
        ratio=Fraction(D,target)
        if least is None or ratio<least[0]:least=(ratio,a,b)
        sha.update(f'{a}:{b}:{D}:{target}\n'.encode())
    return {'numerator':p,'denominator':q,'base_cases':q,
            'base_inequalities_sha256':sha.hexdigest(),
            'block_A':q+2*p,'block_m':q+p,
            'block_difference_positive':True,
            'minimum_base_difference_ratio':str(least[0]),
            'minimum_ratio_at':[least[1],least[2]],
            'statement':'every original (1)^a followed by b>=ceil(p*a/q) exponents >=2 strictly descends'}
