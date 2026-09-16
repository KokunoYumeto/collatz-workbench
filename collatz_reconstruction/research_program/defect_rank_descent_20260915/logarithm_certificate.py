#!/usr/bin/env python3
"""Exact rational certificate for two all-length run exclusions.

The transcendence input is the published rational-number specialization of
Matveev's theorem cited in logarithmic_run_exclusion.md. This file verifies
all subsequent finite rational/ integer inequalities, not that external
transcendence theorem. No floating-point logarithm is used.
"""
from __future__ import annotations
from fractions import Fraction as F
import hashlib
import json
from math import factorial
from pathlib import Path

from arithmetic import CertificateError, require


def log_bounds(x: int, terms: int = 128) -> tuple[F,F]:
    """2*atanh((x-1)/(x+1)), with a proved positive geometric tail bound."""
    require(type(x) is int and x >= 2, 'integer logarithm base at least two required')
    require(type(terms) is int and terms >= 1, 'positive series length required')
    z=F(x-1,x+1);z2=z*z;power=z;s=F(0)
    for j in range(terms):
        s += 2*power/(2*j+1)
        power *= z2
    tail = 2*power/((2*terms+1)*(1-z2))
    require(tail > 0, 'positive logarithmic remainder required')
    return s,s+tail


def fraction_record(x: F) -> list[int]:
    return [x.numerator,x.denominator]


def farey_bracket(lo: F, hi: F, denominator_bound: int) -> dict:
    """A determinant-one bracket, not a floating-point continued fraction.

    Every reduced fraction strictly between the two final endpoints has
    denominator at least the sum of their denominators. This conclusion
    uses their final determinant and needs no trust in the search order.
    """
    require(F(1)<lo<hi<F(2), 'ratio interval must lie strictly between one and two')
    require(type(denominator_bound) is int and denominator_bound>=2, 'invalid denominator bound')
    lp,lq,hp,hq=1,1,2,1
    trace=hashlib.sha256();steps=0
    while lq+hq<=denominator_bound:
        mp,mq=lp+hp,lq+hq
        mid=F(mp,mq)
        if mid<lo:
            lp,lq=mp,mq;side='lower'
        elif mid>hi:
            hp,hq=mp,mq;side='upper'
        else:
            raise CertificateError('logarithm interval does not separate the rational mediant')
        trace.update(f'{mp}:{mq}:{side}\n'.encode());steps+=1
        require(steps<=100000, 'Farey search budget exhausted without a certificate')
    require(hp*lq-lp*hq==1, 'Farey determinant must be one')
    require(F(lp,lq)<lo<hi<F(hp,hq), 'final bracket does not strictly contain the interval')
    require(lq+hq>denominator_bound, 'denominator exclusion is incomplete')
    require(lq<=denominator_bound and hq<=denominator_bound, 'invalid bracket endpoint denominator')
    return {'lower':[lp,lq], 'upper':[hp,hq], 'determinant':1,
            'denominator_sum':lq+hq, 'denominator_bound':denominator_bound,
            'mediant_steps':steps,'mediant_transcript_sha256':trace.hexdigest()}


def validate_retained_minima(data: dict | None = None) -> dict:
    """Replay already-supported singleton zeros before using their source exclusion."""
    if data is None:
        data=json.loads((Path(__file__).resolve().parent/'retained_zero_minima.json').read_text())
    require(data.get('schema')=='collatz-retained-zero-minimum-support-v1', 'unknown retained-zero schema')
    require(data['covered_interval_upper']==1166399, 'retained support interval changed')
    require(len(data['rows'])==127, 'incomplete minimum-run rows')
    count=returns=0
    for a,row in enumerate(data['rows'],1):
        step=2**(a+1);t=(1166402+step-1)//step;t+=1-t%2
        require(row['initial_one_run']==a and row['initial_parameter']==t, 'minimum source start failed')
        for item in row['retained_zero_sources']:
            n=step*t-1
            require(item['source']==n and item['source_parameter']==t, 'retained zero skipped a source parameter')
            values=item['original_values'];word=item['original_word']
            require(values[0]==n and values[-1]==1 and len(values)==len(word)+1,
                    'retained zero path endpoints failed')
            require(len(word)==item['retained_height'], 'retained height mismatch')
            for x,y,aa in zip(values,values[1:],word):
                require(type(x) is int and x>1 and x%2==1 and type(aa) is int and aa>=1,
                        'non-original retained zero input')
                target=3*x+1;exponent=0
                while target%2==0:target//=2;exponent+=1
                require(y==target and aa==exponent, 'retained zero original equation failed')
            t+=2;count+=1;returns+=len(word)
        require(row['remaining_parameter']==t and row['remaining_minimum']==step*t-1,
                'retained minimum interval has an unjustified omission')
    require(count==data['retained_sources'] and returns==data['original_returns_replayed'],
            'retained zero receipt counts failed')
    require(data['search_extension'] is False, 'retained support is not a new discovery claim')
    return data


def certificate() -> dict:
    l2,u2=log_bounds(2);l3,u3=log_bounds(3)
    require(F(1,2)<l2<u2<F(7,10), 'log(2) elementary bounds failed')
    require(F(1)<l3<u3<F(11,10), 'log(3) elementary bounds failed')
    # 2^(4.5)=16*sqrt(2)<24; theorem coefficient is bounded by this rational.
    matveev_upper=F(14,10)*30**5*24*F(7,10)*F(11,10)
    C=10**9
    require(matveev_upper<C, 'coarse Matveev coefficient failed')
    a_bound=10**12
    cycle_ratio=226
    exp36_lower=sum((F(36**j,factorial(j)) for j in range(101)),F(0))
    require(exp36_lower>2*cycle_ratio*a_bound, 'log(452*a_bound)<36 certificate failed')
    require(F(a_bound,2)>37*C+36, 'all-length cycle cutoff comparison failed')
    require(a_bound>2*(C+1), 'cutoff monotonicity comparison failed')
    require(2*cycle_ratio*128<3*(2**129-1), 'small exponential argument failed')
    # This also implies a_bound > C*(1+log(4*a_bound)) for the pure-run case.
    gamma_lo,gamma_hi=l3/u2,u3/l2
    denominator_bound=cycle_ratio*a_bound
    bracket=farey_bracket(gamma_lo,gamma_hi,denominator_bound)
    upper=F(*bracket['upper']);lower=F(*bracket['lower'])
    tolerance=F(1,2**128)
    require(gamma_hi+tolerance<upper, 'upper Farey margin does not exclude the required approximation')
    require(lower<gamma_lo, 'lower Farey margin failed')
    require(2*F(1,3**128)<tolerance, 'pure-run approximation tolerance failed')
    small=[]
    for a in range(1,128):
        b=1
        while 2**(a+2*b)<=3**(a+b):b+=1
        D=2**(a+2*b)-3**(a+b)
        require(D>3**a-2**a, 'small pure-run gap inequality failed')
        small.append([a,b,D,3**a-2**a])
    # Small minimum-run lengths use the complete certified source bound.
    # Each row excludes EVERY rational exponent ratio with denominator <=226*a.
    s=1166401
    retained=validate_retained_minima()
    small_cycle_rows=[]
    plain_trace=hashlib.sha256()
    for a in range(1,128):
        initial_parameter=retained['rows'][a-1]['initial_parameter']
        initial_minimum=2**(a+1)*initial_parameter-1
        plain=farey_bracket(gamma_lo,gamma_hi,213*a)
        require(gamma_hi+F(1,3*initial_minimum)/l2<F(*plain['upper']), 'plain progression baseline failed')
        plain_trace.update(json.dumps([a,initial_minimum,plain['lower'],plain['upper']],separators=(',',':')).encode())
        source_parameter=retained['rows'][a-1]['remaining_parameter']
        minimum=retained['rows'][a-1]['remaining_minimum']
        require(minimum>=s and source_parameter%2==1, 'minimum-run source parameter failed')
        row=farey_bracket(gamma_lo,gamma_hi,cycle_ratio*a)
        ratio_tail_bound=F(1,3*minimum)/l2
        margin=F(*row['upper'])-gamma_hi
        require(ratio_tail_bound<margin, 'short minimum-run cycle ratio is not excluded')
        small_cycle_rows.append({'minimum_run_length':a,'source_minimum':minimum,'least_odd_source_parameter':source_parameter,
            'period_upper_bound':cycle_ratio*a,'farey':row,
            'ratio_tail_upper_bound':fraction_record(ratio_tail_bound),
            'upper_margin_lower_bound':fraction_record(margin)})
    result={'schema':'collatz-exact-logarithm-run-certificate-v1','status':'PASS',
            'external_theorem':'Matveev rational-number specialization; cited theorem, not re-proved by this checker',
            'coefficient_safe_upper':fraction_record(matveev_upper),'coarse_coefficient':C,
            'log_series_terms':128,'log_2_interval':[fraction_record(l2),fraction_record(u2)],
            'log_3_interval':[fraction_record(l3),fraction_record(u3)],
            'ratio_interval':[fraction_record(gamma_lo),fraction_record(gamma_hi)],
            'rise_length_strict_upper_bound':a_bound,'farey':bracket,
            'approximation_tolerance':fraction_record(tolerance),
            'upper_farey_margin_lower_bound':fraction_record(upper-gamma_hi),
            'exp36_positive_terms':101,'exp36_lower_bound':fraction_record(exp36_lower),
            'pure_run_small_rows':small,
            'covered_source_minimum':s,'minimum_run_period_ratio':cycle_ratio,
            'plain_progression_run_ratio':213,
            'plain_progression_small_table_sha256':plain_trace.hexdigest(),
            'retained_zero_sources_reused':retained['retained_sources'],
            'retained_zero_original_returns':retained['original_returns_replayed'],
            'retained_zero_source_sha256':hashlib.sha256((Path(__file__).resolve().parent/'retained_zero_minima.json').read_bytes()).hexdigest(),
            'small_cycle_rows':small_cycle_rows,
            'certified_results':['strict gap D_2(a,b)>3^a-2^a on its entire positive-D domain',
                                 'every nontrivial positive cycle has period greater than 226 times the initial exponent-1 run at its actual minimum',
                                 'no nontrivial positive cycle with exactly one cyclic run of exponent-1 letters'],
            'remaining_cycle_run_counts':'two or more; not excluded by this argument'}
    return result


def validate_certificate(record: dict) -> None:
    require(type(record) is dict and record==certificate(),
            'rational logarithm certificate differs from exact reconstruction')


if __name__=='__main__':
    print(json.dumps(certificate(),sort_keys=True,separators=(',',':')))
