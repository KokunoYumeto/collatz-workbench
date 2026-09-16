#!/usr/bin/env python3
"""Global, all-word Collatz cylinder and first-crossing certificates.

Only the original +1 forcing is used. The all-length power gap is proved
in note.md using the stated Matveev input plus exact rational certificates.
Every reported point or family also checks its own literal integer margins.
No finite search or unmatched pattern is a divergence certificate.
"""
from __future__ import annotations
import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
from typing import Iterable

class CertificateError(ValueError):
    pass

def need(ok: bool, message: str) -> None:
    if not ok:
        raise CertificateError(message)

def v2(n: int) -> int:
    need(type(n) is int and n != 0, 'a nonzero integer is required')
    n = abs(n)
    return (n & -n).bit_length()-1

def step(n: int) -> tuple[int,int]:
    need(type(n) is int and n > 0 and n % 2 == 1, 'positive odd source required')
    a = v2(3*n+1)
    return (3*n+1) >> a, a

def divided_step(n: int) -> tuple[int,int]:
    """Independent valuation by repeated division, not bit extraction."""
    need(type(n) is int and n > 0 and n % 2 == 1, 'positive odd source required')
    x,a = 3*n+1,0
    while x % 2 == 0:
        x //= 2; a += 1
    return x,a

@dataclass(frozen=True)
class Packet:
    word: tuple[int,...] = ()
    A: int = 0
    L: int = 1
    C: int = 0
    rho: int = 1
    image: int = 1

    @property
    def U(self) -> int:
        return 1 << self.A

    @property
    def D(self) -> int:
        return self.U-self.L

    @property
    def m(self) -> int:
        return len(self.word)

    def append(self,a: int) -> Packet:
        need(type(a) is int and a >= 1, 'positive integer exponent required')
        mod = 1 << a
        digit = (((1 << (a-1))-(3*self.image+1)//2)
                 *pow(3*self.L,-1,mod)) % mod
        rho = self.rho+2*self.U*digit
        image = (3*self.image+1+6*self.L*digit) >> a
        return Packet(self.word+(a,),self.A+a,3*self.L,3*self.C+self.U,rho,image)

    def evaluate(self,n: int) -> F:
        return F(self.L*n+self.C,self.U)

    def check(self) -> None:
        need(self.L == 3**self.m and self.A == sum(self.word), 'packet clock mismatch')
        A,C = 0,0
        for a in self.word:
            C = 3*C+(1 << A); A += a
        need(C == self.C, 'original forcing mismatch')
        need(0 < self.rho < 2*self.U and self.rho % 2 == 1, 'noncanonical cylinder anchor')
        need(self.evaluate(self.rho) == self.image and self.image % 2 == 1, 'image mismatch')
        need((self.L*self.rho+self.C-self.U) % (2*self.U) == 0, 'terminal odd congruence failed')


def packet(word: Iterable[int]) -> Packet:
    p=Packet()
    for a in word:
        p=p.append(a)
    return p


def cylinder_certificate(word: Iterable[int]) -> dict:
    p=packet(word); p.check()
    need(p.m > 0, 'nonempty word required')
    if p.D <= 0:
        label='every_positive_source_strictly_increases'
        threshold=None; exception=[]
    else:
        # This instance checks the global theorem's exact integer comparison.
        need((p.D+1)*(1 << p.m)>p.L, 'power gap contradicts the proved domain')
        bound=1 << (p.A-p.word[-1]+1)
        need(p.C < p.D*bound, 'all-word affine threshold bound failed')
        exception=[p.rho] if p.image >= p.rho else []
        threshold=1 if exception else 0
        label='one_canonical_exception' if exception else 'complete_cylinder_strict_descent'
        need(not exception or p.rho < bound, 'exception lies outside the proved source window')
        need((p.rho+2*p.U)>(p.image+2*p.L), 'first translated lift does not descend')
    return {'word':list(p.word),'A':p.A,'L':p.L,'U':p.U,'C':p.C,'D':p.D,
            'source_anchor':p.rho,'source_step':2*p.U,'target_anchor':p.image,'target_step':2*p.L,
            'source_parameter_domain':'integers t>=0','strict_descent_parameter_min':threshold,
            'nondescending_source_points':exception if p.D>0 else 'entire_original_cylinder',
            'canonical_label_retained':True,'status':label,
            'affine_difference_constant':p.rho-p.image,'affine_difference_slope':2*p.D,
            'arrival_at_1_claim':False}


def first_crossing_partition(prefix: Iterable[int]) -> dict:
    p=Packet()
    for a in prefix:
        p=p.append(a)
        need(p.U < p.L, 'prefix has already crossed the coefficient threshold')
    h=(3*p.L).bit_length()-p.A
    need(h >= 2, 'first crossing must have last exponent at least two')
    modulus=1 << (h-1)
    digit=(-(3*p.image+1)//2 * pow(3*p.L,-1,modulus)) % modulus
    # -(3*y+1)//2 is exact since its numerator is even.
    next_y,next_a=step(p.image)
    candidate=(next_a>=h and next_y>=p.rho)
    source_anchor=p.rho+2*p.U*digit
    b0=(3*p.image+1+6*p.L*digit)//(1<<h)
    source_step=2*p.U*modulus
    need(source_step>3*p.L and source_anchor+source_step>b0+3*p.L, 'crossing upper-line margin failed')
    need(candidate is False or digit==0, 'candidate outside crossing support')
    anchor_endpoint=b0>>v2(b0)
    need((anchor_endpoint>=source_anchor)==candidate, 'crossing anchor disagrees with complete singleton test')
    return {'prefix':list(p.word),'prefix_length':p.m,'prefix_A':p.A,
            'prefix_L':p.L,'prefix_C':p.C,'prefix_anchor':p.rho,'prefix_image':p.image,
            'noncrossing_next_exponents':list(range(1,h)),
            'crossing_next_exponents':{'minimum':h,'maximum':None},
            'crossing_source_anchor':source_anchor,'crossing_source_step':source_step,
            'target_before_extra_divisions_anchor':b0,'target_before_extra_divisions_step':3*p.L,
            'translated_upper_margin_at_one':source_anchor+source_step-b0-3*p.L,
            'crossing_anchor_endpoint':anchor_endpoint,
            'old_parameter_anchor':digit,'old_parameter_step':modulus,
            'canonical_source_test':{'source':p.rho,'next_exponent':next_a,
              'endpoint':next_y,'belongs_to_crossing_family':next_a>=h,
              'is_nondescending_exception':candidate},
            'exception_source':p.rho if candidate else None,
            'first_descent_parameter_min':1 if candidate else 0,
            'crossing_zero_label_retained':True,
            'unbounded_exponent_tail_retained':True}


def crossing_value(part: dict,parameter: int) -> dict:
    need(type(parameter) is int and parameter >= 0,'nonnegative source parameter required')
    p=packet(part['prefix'])
    need(part==first_crossing_partition(p.word),'corrupt crossing partition')
    n=part['crossing_source_anchor']+part['crossing_source_step']*parameter
    x=p.evaluate(n)
    need(x.denominator==1,'prefix evaluation not integral')
    y,a=step(x.numerator)
    return {'source':n,'parameter':parameter,'full_word':list(p.word+(a,)),
            'endpoint':y,'last_exponent':a,'strict_descent':y<n}


def path_certificate(n: int,word: Iterable[int]) -> dict:
    p=packet(word)
    need(type(n) is int and n > 0 and n%2==1,'positive odd source required')
    need((n-p.rho)%(2*p.U)==0,'source is outside original cylinder')
    values=[n]; chain=Counter(); x=n
    for a in p.word:
        y,b=divided_step(x)
        need(a==b,'exponent differs from original valuation')
        chain[x]+=1; values.append(y); x=y
    need(F(x)==p.evaluate(n),'independent path/affine discrepancy')
    boundary=Counter()
    for source,k in chain.items():
        target,_=divided_step(source)
        boundary[source]+=k; boundary[target]-=k
    boundary={k:v for k,v in sorted(boundary.items()) if v}
    expected=Counter({n:1});expected[x]-=1
    need(boundary=={k:v for k,v in sorted(expected.items()) if v},'original path boundary failed')
    return {'source':n,'endpoint':x,'word':list(p.word),'values':values,
            'original_chain':{str(k):v for k,v in sorted(chain.items())},
            'firstjet_constant_chain':{},'firstjet_linear_boundary':{str(k):v for k,v in boundary.items()},
            'strict_descent':x<n,'returns':p.m,'finite_path_only':True}


def log_interval(n: int, terms: int=160) -> tuple[F,F]:
    need(type(n) is int and n>=2 and type(terms) is int and terms>=1,'invalid logarithm interval')
    z=F(n-1,n+1); z2=z*z; power=z; total=F(0)
    for j in range(terms):
        total+=2*power/(2*j+1); power*=z2
    tail=2*power/((2*terms+1)*(1-z2))
    return total,total+tail


def rational_record(x: F) -> list[int]:
    return [x.numerator,x.denominator]


def gap_certificate() -> dict:
    l2,u2=log_interval(2);l3,u3=log_interval(3)
    low=F(83130157078217,52449289519716)
    high=F(350861368503572,221368876767703)
    need(F(2,3)<l2 and u2<F(7,10),'log 2 bounds failed')
    need(u3<F(11,10),'log 3 bound failed')
    need(low<l3/u2 and u3/l2+F(1,2**128)<high,'rational separating interval failed')
    need(high.numerator*low.denominator-low.numerator*high.denominator==1,'determinant not one')
    need(low.denominator+high.denominator>10**12,'denominator threshold failed')
    safe=F(7,5)*30**5*23*F(7,10)*F(11,10)
    need(23**2>2**9 and safe<10**9,'Matveev coefficient domination failed')
    need(2*10**12<2**41,'large-exponent log enclosure failed')
    need(F(2,3)*10**12>10**9*(1+41*F(7,10)),'large-exponent exclusion failed')
    need(F(2,3)-F(10**9,10**12)>0,'large-exponent derivative bound failed')
    need(F(3,2*128)<1,'small approximation comparison failed')
    rows=[]
    for m in range(1,128):
        L=3**m;A=L.bit_length();U=1<<A;D=U-L
        margin=(D+1)*(1<<m)-L
        need(U>L and U//2<L and margin>0,'finite power-gap row failed')
        rows.append({'m':m,'A_first':A,'D':D,'integer_margin':margin})
    return {'status':'exact_finite_part_passed','external_theorem':'Matveev rational-number bound; see note.md',
            'formal_proof_execution':False,'log_terms':160,
            'log2_interval':[rational_record(l2),rational_record(u2)],
            'log3_interval':[rational_record(l3),rational_record(u3)],
            'ratio_lower':rational_record(low),'ratio_upper':rational_record(high),
            'separation':rational_record(F(1,2**128)),
            'safe_matveev_coefficient':rational_record(safe),'finite_rows':rows}


def independent_prefix_counts(depth: int) -> list[int]:
    counts={0:1};out=[1]
    for j in range(1,depth+1):
        ceiling=(3**j).bit_length()-1
        nxt={A:sum(value for B,value in counts.items() if B<A) for A in range(j,ceiling+1)}
        counts=nxt;out.append(sum(counts.values()))
    return out


def crossing_audit(max_return: int=18, ledger: Path|None=None) -> dict:
    """Complete pre-crossing-prefix tree, not a bounded start sample.

    At every prefix the WHOLE unbounded next-exponent crossing tail has
    at most the single canonical-prefix source as a possible exception.
    All low-exponent noncrossing children are generated. The infinite-depth
    frontier is retained and no global coverage is claimed.
    """
    need(type(max_return) is int and 1<=max_return<=20,'audit bound must be 1..20')
    import gzip
    sink=gzip.open(ledger,'wt',encoding='utf-8',newline='\n',compresslevel=1) if ledger else None
    levels=[0]*max_return; crossings=[0]*max_return;exceptions=[]
    canonical_crossing_descents=[0]*max_return
    h=hashlib.sha256();stack=[Packet()]
    while stack:
        p=stack.pop();j=p.m;levels[j]+=1
        # Independent residue computation and original affine identity at EVERY node.
        direct_rho=((p.U-p.C)*pow(p.L,-1,2*p.U)) % (2*p.U)
        need(direct_rho==p.rho, 'lift recursion disagrees with original cylinder')
        need(p.L*p.rho+p.C==p.U*p.image, 'original affine equation fails')
        hnext=(3*p.L).bit_length()-p.A;modulus=1<<(hnext-1)
        digit=(-(3*p.image+1)//2*pow(3*p.L,-1,modulus))%modulus
        n0=p.rho+2*p.U*digit
        b0=(3*p.image+1+6*p.L*digit)//(1<<hnext)
        stride=2*p.U*modulus
        need(stride>3*p.L and n0+stride>b0+3*p.L, 'whole unbounded crossing tail fails')
        y,a=divided_step(p.image)
        crossing=(p.A+a >= (3*p.L).bit_length())
        bad=crossing and y>=p.rho
        anchor_endpoint=b0
        while anchor_endpoint%2==0:anchor_endpoint//=2
        need((anchor_endpoint>=n0)==bad,'unbounded family anchor discrepancy')
        if crossing:
            crossings[j]+=1
            if bad:
                rec={'prefix':list(p.word),'source':p.rho,'last_exponent':a,'endpoint':y,
                     'm':j+1,'A':p.A+a,'C':3*p.C+p.U,'D':(p.U<<a)-3*p.L}
                exceptions.append(rec)
            else:canonical_crossing_descents[j]+=1
        row=[list(p.word),p.A,p.L,p.C,p.rho,p.image,a,y,int(crossing),int(bad)]
        text=json.dumps(row,separators=(',',':'))+'\n';h.update(text.encode())
        if sink:sink.write(text)
        if j+1<max_return:
            ceiling=(3*p.L).bit_length()-1-p.A
            for b in range(ceiling,0,-1):
                stack.append(p.append(b))
    if sink:sink.close()
    need(levels==independent_prefix_counts(max_return-1),'prefix tree is not complete')
    return {'max_first_crossing_return':max_return,'prefix_counts':levels,
            'total_prefixes':sum(levels),'independent_node_equations':2*sum(levels),'whole_tail_margin_tests':sum(levels),'whole_tail_anchor_tests':sum(levels),'canonical_crossing_counts':crossings,
            'canonical_crossing_descents':canonical_crossing_descents,
            'exceptions':exceptions,'ledger_sha256':h.hexdigest(),
            'last_exponent_unbounded':True,'positive_source_unbounded':True,
            'infinite_depth_frontier_retained':True,'global_conjecture_claim':False}


def main() -> None:
    ap=argparse.ArgumentParser(description=__doc__)
    sub=ap.add_subparsers(dest='mode',required=True)
    p=sub.add_parser('cylinder');p.add_argument('word',nargs='+',type=int)
    p=sub.add_parser('crossing');p.add_argument('prefix',nargs='*',type=int)
    p.add_argument('--parameter',type=int)
    p=sub.add_parser('audit');p.add_argument('--max-return',type=int,default=18);p.add_argument('--ledger',type=Path)
    sub.add_parser('gap')
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    try:
        if args.mode=='cylinder':result=cylinder_certificate(args.word)
        elif args.mode=='crossing':
            result=first_crossing_partition(args.prefix)
            if args.parameter is not None:result['point']=crossing_value(result,args.parameter)
        elif args.mode=='audit':result=crossing_audit(args.max_return,args.ledger)
        else:result=gap_certificate()
    except CertificateError as e:ap.error(str(e))
    text=json.dumps(result,sort_keys=True,indent=2)+'\n'
    if args.output:args.output.write_text(text,encoding='utf-8')
    else:print(text,end='')

if __name__=='__main__':main()
