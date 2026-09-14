# Belaga-Mignotte 2000/018: packet coordinates and the 6487 example

Audit ID: AUD-COL-BM2000-PACKET-20260904-0001  
Recorded: 2026-09-04T15:16:12Z  
Scope: bounded primary-source reading and exact coordinate verification. No TeX, source ledger, index, Lean, build, or remote changes.

## Witness and coverage

The witness read is the author-uploaded full text of E. G. Belaga and M. Mignotte, *Cyclic Structure of Dynamical Systems Associated with 3x+d Extensions of Collatz Problem*, available at [ResearchGate](https://www.researchgate.net/publication/2459588_Cyclic_Structure_of_Dynamical_Systems_Associated_with_3xd_Extensions_of_Collatz_Problem). The page identifies an upload by Edouard Belaga on 2014-11-16. The designation “preprint 2000/018, Univ. Louis Pasteur, Strasbourg” is independently corroborated by the author's reference list on printed p. 206 of [his 2003 Acta Arithmetica paper](https://www.impan.pl/shop/publication/transaction/download/product/82606); that citation does not establish byte identity between editions.

The displayed PDF download link returned HTTP 404 on one attempt. No repeated download attempts or broad source search followed. One targeted bibliographic search returned a CiteSeer PDF route, which was not retrieved. The mathematical reading therefore uses the actual full-text transcription, not a visually checked PDF. No primary-PDF SHA256 or physical-PDF-page identity is claimed. Printed pages below follow the page markers in that transcription. Its web-extraction line numbers are supplemental retrieval locators, not permanent publication identifiers.

Read loci:

| Locus | Printed pages | Web-extraction lines | Use |
|---|---:|---:|---|
| Contents | 1-2 | 103-140 | Section routing |
| Section 2, (2:1)-(2:3) | 7-8 | 529-678 | Map, minimal period, parameter domain |
| Lemma-Definition 4.2, Definition 4.3 | 12-13 | 985-1237 | Odd returns, scaling, primitive cycles |
| Definition 6.1 and Lemma 6.2 | 23-24 | 1958-2173 | Pointed memberships versus cycles |
| Definition 7.1 | 27-28 | 2330-2438 | Configurations and five coordinates |
| Lemma 7.2 and proof | 28-31 | 2440-2694 | Rotation identities, counts, injectivity assertions |
| Theorems 8.1, 8.3; Definition 8.2 | 31-33 | 2696-3132 | Forward and inverse constructions |
| Corollary 8.4 and proof | 33-35 | 3134-3274 | Exact integer-coordinate criteria |
| Example 8.5 | 35-36 | 3276-3336 | The 6487 count |

Other material that appeared in overlapping tool output is not claimed as systematically audited. In particular, the full cycle census and Sections 9-12 were not audited.

The current directives and affine topic route were read. The route identifies the canonical index entry point as `C:/Users/LOCAL_USER/Documents/Papors/Chatnotes/Zeta-Function-Foundation/config/literature_index_entrypoint.json`, whose SHA256 at this read was `0992419e4490901d1651194f63cccbecd6fdef42366160620faadcb1f3bf67c1`. The dispatch reported that the exact combined query `Belaga 6487` had no hits; that query was not rerun and no new indexing was performed. An initial attempted workspace-local entry-point path was absent; the existing topic route supplied the correct path.

## Source identification in packet coordinates

The source uses the shortened map

\[
T_d(n)=\begin{cases}n/2&n\text{ even},\\(3n+d)/2&n\text{ odd},\end{cases}
\qquad d\ge1,\quad\gcd(d,6)=1.
\]

Its configurations are aperiodic pointed positive tuples; its primitive integer cycles have coprime member and parameter. Theorems 8.1 and 8.3 identify configurations with pointed primitive memberships. Cycles themselves are represented with their minimum first. [Primary full text, Definitions 4.3, 6.1, 7.1 and Theorems 8.1, 8.3](https://www.researchgate.net/publication/2459588_Cyclic_Structure_of_Dynamical_Systems_Associated_with_3xd_Extensions_of_Collatz_Problem).

To avoid the source's capital A colliding with our exponent sum, write our packet as \(p=(a_1,\ldots,a_m)\), set \(S_0=0\), \(S_j=a_1+\cdots+a_j\), and set \(A=S_m\). The exact crosswalk is:

| Source notation | Packet notation |
|---|---|
| \(k,\ell,P=(p_1,\ldots,p_k)\) | \(m,A,p=(a_1,\ldots,a_m)\) |
| \(a(P)\), capital \(A\) in (7:6) | \(C(p)=\sum_{j=0}^{m-1}3^{m-1-j}2^{S_j}\) |
| \(B=b(P)\) | \(D=2^A-3^m>0\) |
| \(H=h(P)\) | \(H=\gcd(C(p),D)\) |
| \(F=f(P)\) | \(n=C(p)/H\) |
| \(G=g(P)\) | \(d=D/H\) |
| \(\sigma P\) | \((a_2,\ldots,a_m,a_1)\) |
| \(\gamma(P)\) | Pointed membership \((n,d)\) |

The formulas are (7:6), (7:19), (7:21)-(7:23), and (8:13). In particular, the scaling parameter is the **reduced denominator**, not the reduced numerator. The source's positive configuration domain is \(2^A>3^m\), with no repeated exponent word. It does not cover the negative-rational packet branch under these positive-parameter definitions.

## Independent coordinate verification

The following calculations rederive the comparison directly. They are not claims of new mathematics and do not rely on the source's blanket injectivity assertions.

Put \(C_j=C(\sigma^j p)\). Expanding the finite sums and cancelling common terms gives

\[
2^{a_{j+1}}C_{j+1}=3C_j+D,\qquad j\pmod m.
\]

Every \(C_j\) is positive and odd: its first summand is odd and the remaining summands are even. Modulo 3, its final summand is a power of 2, so \(3\nmid C_j\). Also \(D\) is odd and prime to 3. Consequently

\[
\gcd(C_{j+1},D)
=\gcd(2^{a_{j+1}}C_{j+1},D)
=\gcd(3C_j+D,D)
=\gcd(C_j,D)=H.
\]

Thus \(n_j=C_j/H\) are positive odd integers, \(d=D/H\) is fixed, and

\[
3n_j+d=2^{a_{j+1}}n_{j+1},\qquad
v_2(3n_j+d)=a_{j+1},\qquad \gcd(n_j,d)=1.
\]

This is an actual integer orbit, with the stated exponents, not just a congruence. Under \(T_d\), the next odd value occurs after \(a_{j+1}\) steps. Under the full map \(\mathcal C_d(n)=3n+d\) for odd \(n\) and \(n/2\) for even \(n\), it occurs after \(a_{j+1}+1\) steps. For an aperiodic packet the exact periods are therefore respectively \(A\) and \(A+m\), with odd-return period \(m\).

For completeness, exactness does not follow merely from closing the displayed orbit. If an odd value repeated before \(m\) odd steps, determinism would repeat the valuation sequence at that earlier index, making the cyclic tuple periodic. Equivalently, if \(p=q^r\), the affine block map has the form \(L(x)=ux+v\), with \(u=3^{|q|}/2^{\sum q}>0\). Since

\[
L^r(x)-x=(1+u+\cdots+u^{r-1})(L(x)-x),
\]

closing a repeated block already closes one block. Hence a cycle written with its true least period yields an aperiodic tuple. A shorter shortened/full return from an odd starting point would also be an earlier odd return, so neither clock can have a hidden shorter period.

Conversely, start from a pointed primitive integer \(T_d\)-cycle at an odd member \(n\). Record the actual valuations of \(3n_j+d\) until the first odd return. The resulting tuple satisfies \(D n=dC(p)\), so \(D>0\). From \(\gcd(n,d)=1\), there is a positive integer \(t\) such that \(C(p)=tn\) and \(D=td\); necessarily \(t=\gcd(C(p),D)\). This recovers exactly \(F=n\) and \(G=d\). The valuation record is unique. This establishes both inverse identities for the pointed correspondence without assuming that \((m,A)\mapsto D\) is injective.

Finally, division by \(d\) gives the rational Collatz coordinate \(x=n/d=C(p)/D\). On odd-denominator rationals parity is the numerator's parity after reducing to an odd denominator. Since \(d\) is odd,

\[
T_1(n/d)=T_d(n)/d
\]

on both branches. Multiplication by \(d\) is the inverse on this cycle. No values, valuations, return indices, or cycle points are discarded by this comparison. Quotienting by packet rotation, unlike this coordinate change, deliberately forgets the chosen odd base point; an aperiodic \(m\)-packet has exactly \(m\) such pointings.

### The two meanings of primitive

These are distinct tests with an exact relation, not disconnected notions:

- Word primitivity means the recorded exponent tuple is not a power of a shorter tuple; it makes the recorded periods minimal.
- Integer-cycle primitivity means \(\gcd(n,d)=1\); it removes a common scaling factor from the orbit and its parameter.

For example, \(p=(2)\) gives the primitive \(T_1\)-cycle \(1,2\). Multiplying by 5 gives the \(T_5\)-cycle \(5,10\): the same primitive exponent word, but a nonprimitive integer cycle. Conversely, recording \(p=(2,2)\) yields reduced \((n,d)=(1,1)\), a primitive integer cycle described twice by a nonprimitive word. The source excludes that repeated word from its configuration domain.

## Example 8.5: exactly what 456 counts

Here \(m=10\), \(A=16\), and \(D=65536-59049=6487=13\cdot499\). The source says 456 solutions and associates them with cycles of shortened length 16 and oddlength 10. Its immediately displayed tuple condition does not explicitly quotient pointings. [Example 8.5, printed pp. 35-36](https://www.researchgate.net/publication/2459588_Cyclic_Structure_of_Dynamical_Systems_Associated_with_3xd_Extensions_of_Collatz_Problem).

An exact enumeration of all \(\binom{15}{9}=5005\) positive tuples gives:

| \(\gcd(C,6487)\) | Pointed tuples | Primitive words | Repeated words | Rotation classes | Class size |
|---:|---:|---:|---:|---:|---:|
| 1 | 4560 | 4560 | 0 | 456 | 10 |
| 13 | 410 | 410 | 0 | 41 | 10 |
| 499 | 35 | 0 | 35 | 7 | 5 |
| 6487 | 0 | 0 | 0 | 0 | - |
| Total | 5005 | 4970 | 35 | 504 | - |

The gcd-one tuples therefore give exactly **456 primitive \(T_{6487}\)-cycle classes**, not 456 pointed configurations. They give 4560 pointed odd memberships. Their full-map period is 26, not 16. This checks precisely the \((m,A)=(10,16)\) part of the example; it does not validate any total cycle census at other lengths.

The 35 repeated tuples have the form \(q^2\), where \(q\) has length 5 and sum 8. The factor \(2^8+3^5=499\) divides both repeated-word numerator and denominator. Their reduced parameter is 13 and their minimal shortened period is 8. This explains why word repetition must not be confused with a nonprimitive integer-cycle scaling.

The enumeration was run independently by a delegated arithmetic checker and then rerun by this reviewer. Both used exact integers and obtained the same counts. No Lean proof or general census was run. The reviewer's executable command was an inline `python -c` invocation of the following code, which printed
`5005 {1: 4560, 13: 410, 499: 35} {(1, 10): 4560, (13, 10): 410, (499, 5): 35} 456` and exited 0:

```python
from itertools import combinations
from math import gcd
from collections import Counter

counts, periods, orbits, N = Counter(), Counter(), set(), 0
for q in combinations(range(1, 16), 9):
    s = (0,) + q + (16,)
    p = tuple(s[i + 1] - s[i] for i in range(10))
    c = sum(3**(9-j) * 2**s[j] for j in range(10))
    h = gcd(c, 6487)
    d = next(d for d in (1, 2, 5, 10) if p == p[:d] * (10 // d))
    counts[h] += 1
    periods[h, d] += 1
    N += 1
    if h == 1:
        orbits.add(min(p[j:] + p[:j] for j in range(10)))
assert N == 5005
assert counts == {1: 4560, 13: 410, 499: 35}
assert len(orbits) == 456
print(N, dict(counts), dict(periods), len(orbits))
```

## Local defects and qualifications

These are defects in assertions visible in the full-text witness. A PDF image is still needed before identifying any transcription-sensitive mark as a printed typographical error. The counterexamples themselves are exact and do not depend on typography.

1. **False injectivity of the denominator alone.** Lemma 7.2(5), (7:14), printed pp. 29-30, web lines 2544-2572, includes \(b:\Lambda\to\mathcal D\) among injective maps. But \(b(1,3)=8-3=5=32-27=b(3,5)\), with both pairs in \(\Lambda\). Keep \((m,A)\) as coordinates; the value \(D\) alone cannot recover them. The pointed membership correspondence remains valid by the independent inverse construction above.

2. **Corona inclusion loses aperiodicity.** Lemma 7.2(3), (7:10), printed p. 29, web lines 2498-2504, asserts inclusion as total length increases. The aperiodic tuple \((3,2)\) has length 5 and numerator 11. At length 6, the only 2-tuple with that numerator is \((3,3)\), which is periodic and excluded. Thus \(11\) is in the \((2,5)\)-corona but not the \((2,6)\)-corona. This assertion is unnecessary for the rotation/scaling correspondence.

3. **The 456 wording must distinguish pointings from classes.** Example 8.5, printed p. 35, web lines 3276-3291, uses a solutions count without making that quotient explicit. The literal ordered tuple condition has 4560 solutions. Division by its free ten-element rotation action gives 456 cycles.

4. **Overbroad nondivisibility statement.** Lemma-Definition 4.2(1), (4:2), printed p. 12, web lines 998-1011, quantifies over all positive starting values and all positive iterates. With \(m=6,d=1\), \(T_1(6)=3\), contradicting that formulation. Once an odd step has occurred, subsequent iterates are prime to 3; positive cycles are also prime to 3. Only those valid restrictions are used above.

5. **Prime-parameter sufficiency needs qualification.** Corollary 8.4(3), printed p. 34, web lines 3160-3175, presents the second congruence \(B\mid dC\) as sufficient in the prime-\(d\) case. Read as a standalone condition for a primitive cycle at the stated lengths, it fails: take \(d=5\), \((m,A)=(1,2)\), so \(C=B=1\). The congruence holds but the resulting \(T_5\)-cycle is \(5,10\), nonprimitive, and the sole tuple \((2)\) has reduced parameter 1. The exact sufficient criterion is \(d=D/\gcd(C,D)\), as in (8:9), not this congruence alone. If the text intends additional simultaneous conditions, that intention should not be silently supplied.

No source-wide verdict or erratum-publication claim is made. In particular, the essential packet-to-membership construction is mathematically usable on the exact stated positive, aperiodic domain, with the explicit verification above. Its existing literature attribution must be retained; it is not a new theorem of this reconstruction.
