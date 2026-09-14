# LAGARIAS-1990-F009 — rational cycles and primitive 3x+k audit

## Status and controlling witness

This is a full content-level audit of Jeffrey C. Lagarias, *The Set of
Rational Cycles for the 3x+1 Problem*, Acta Arithmetica **56** (1990),
33--53.  It resolves the exact rational-cycle dependency used by
Laarhoven--de Weger and records the rest of the article's theorem,
conjecture, heuristic, and source-defect boundaries.

- IMPAN publisher record:
  `https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/en/publishing-house/journals-and-series/acta-arithmetica/all/56/1/106574/the-set-of-rational-cycles-for-the-3x-1-problem`
- DOI: `10.4064/aa-56-1-33-53`
- official local witness:
  `external_literature/dependency_gate_2026-08-25/lagarias_1990_impan.pdf`
- PDF pages: `11` landscape two-up scan pages, containing printed pp. 33--53
- PDF bytes: `2559375`
- PDF SHA-256:
  `7dc39db8d59c141b19eebfbd76e48c4e7d3906f97d0c7187739d2a7561399005`

All printed pp. 33--53 were cropped into individual page images and read
visually.  The scan has no usable text layer.  The received and revised dates
printed at the end are 22 November 1988 and 20 April 1989.

## Exact domain, parity, and fixed-return theorem

Printed p. 36 defines \(\mathbb Q[(2)]\) as the rationals \(p/q\) with odd
reduced denominator \(q\), with parity given by the numerator \(p\).  This
ring is canonically embedded in \(\mathbb Z_2\).  The shortened map is

\[
 T(x)=
 \begin{cases}
 (3x+1)/2,&x\text{ odd},\\
 x/2,&x\text{ even}.
 \end{cases}
\]

For \(n\geq1\) and a word \(v=(v_0,\ldots,v_{n-1})\in\{0,1\}^n\), put

\[
 m(v)=\sum_{i=0}^{n-1}v_i,
 \qquad
 D(v)=2^n-3^{m(v)}\neq0,
\]

and

\[
 N(v)=\sum_{j=0}^{n-1}
 v_j2^j3^{v_{j+1}+\cdots+v_{n-1}}.
\]

The restriction $n\geq1$ is essential: then $2^n$ is even and
$3^{m(v)}$ is odd, so $D(v)\neq0$.  The empty word would instead give a
zero denominator and the tautological return $T^0(x)=x$.

Theorem 2.1, printed pp. 36--37, Eqs. (2.1)--(2.2), proves that

\[
 x(v)=\frac{N(v)}{D(v)}
\]

is the unique element of \(\mathbb Q[(2)]\) satisfying
\(T^n(x(v))=x(v)\) with initial parity word \(v\).  The proof first solves
the literal affine composition equation.  It then proves branch correctness:
for every \(y\in\mathbb Q[(2)]\), exactly one of the two forward branch
expressions \(U_0(y)=y/2\) and \(U_1(y)=(3y+1)/2\) remains in
\(\mathbb Q[(2)]\), with the choice determined by the numerator parity of
\(y\); if \(y\notin\mathbb Q[(2)]\), both expressions remain outside the
ring.  Because \(D(v)\) is odd, the formal fixed point lies in the ring.  If
the prescribed composition ever selected the other forward expression, it
would leave the ring and could not return, contradicting the fixed-return
equation.  Thus every prescribed branch is actual rather than extraneous.
This is not a predecessor uniqueness statement: both genuine
\(T\)-predecessors \(2y\) and \((2y-1)/3\) lie in \(\mathbb Q[(2)]\).

“Period \(n\)” in this statement means return after \(n\) displayed steps.
Printed p. 38 defines a reducible word as a proper repeated block and an
irreducible word otherwise.  The least dynamical period is \(n\) exactly for
an irreducible word; no displayed return length is silently replaced by least
period.

Printed p. 34, Eq. (1.3), is the same formula in decreasing one-position
coordinates.  Printed p. 38, Eqs. (2.4)--(2.6), gives the primitive-necklace
count

\[
 \sum_{d\mid n}dI(d)=2^n,
 \qquad
 I(n)=\frac1n\sum_{d\mid n}\mu(d)2^{n/d},
\]

whose values begin \(2,1,2,3,6,9\).  This independently confirms the
Laarhoven--de Weger sequence correction.

## Raw denominator, reduced denominator, and the all-even case

Printed p. 39, Eqs. (2.7a)--(2.7b), distinguishes the raw pair \(D(v),N(v)\)
from the common reduced cycle denominator.  With a positive-denominator
convention the latter is

\[
 \delta(v)=\frac{|D(v)|}{\gcd(|N(v)|,|D(v)|)}.
\]

Every phase has the same reduced denominator once that denominator is prime
to 3.  The exact coprimality proof has a required case split:

- if \(m(v)\geq1\), then
  \(D(v)=2^n-3^{m(v)}\not\equiv0\pmod3\), so every divisor
  \(\delta(v)\) is prime to 3;
- if \(m(v)=0\), the word is all even, the return equation is
  \(x=x/2^n\), hence \(x=0\) and \(\delta(v)=1\).

In every case \(\delta(v)\) is positive, odd, and prime to 3, hence
\(\delta(v)\equiv\pm1\pmod6\).  The all-even case cannot be skipped merely
because \(2^n-1\) may itself be divisible by 3.

## Exact primitive 3x+k correspondence

Printed pp. 34 and 39--40 define, for odd \(k\),

\[
 T_k(n)=
 \begin{cases}
 (3n+k)/2,&n\text{ odd},\\
 n/2,&n\text{ even}.
 \end{cases}
\]

A primitive \(T_k\)-cycle is a cycle all of whose entries are coprime to
\(k\).  Let \((x_j)\) be a rational \(T\)-cycle and let \(k>0\) be its
common reduced denominator.  Put \(n_j=kx_j\).  Then, phase by phase,

\[
 kT(x_j)=T_k(n_j).
\]

The integer tuple \((n_j)\) is primitive because the denominator was reduced.
Conversely, division by \(k\) sends every primitive integer \(T_k\)-cycle,
with \(k>0\) and \(k\equiv\pm1\pmod6\), to a rational \(T\)-cycle with
common reduced denominator \(k\).  Multiplication and division are literal
two-sided inverses and preserve cyclic phase, every parity, displayed return
length, and least period.

The source also retains the raw scaling strata.  Under its standing
\(\gcd(k,6)=1\) hypothesis, for \(d\mid k\) define

\[
 Z(d,k)=\{n\in\mathbb Z:\gcd(n,k)=d\}.
\]

Writing \(n=dm\) and \(k=db\) gives the exact intertwining identity

\[
 T_k(dm)=dT_b(m).
\]

Thus unscaled integer cycles at different parameters have common-scaling
fibres.  The paper does not silently identify these raw representatives: it
states the strata and then selects the primitive layer.  Laarhoven--de
Weger's later phrase “having denominator \(b\)” naturally refers to this
reduced-denominator layer.  Its earlier unqualified one-to-one sentence still
requires either the primitive condition or the explicit common-scaling
quotient.

## Source defects forced by exact coordinates

The following local printed statements require correction.  None invalidates
Theorem 2.1 or the primitive correspondence after the displayed repairs.

1. The itinerary sentence at the top of printed p. 34 defines
   \(v=(v_0,\ldots,v_{n-1})\) but prints
   \(T^i(x(v))\equiv v_i\pmod2\) for \(1\leq i\leq n\).  That range skips
   \(v_0\) and invokes the undefined \(v_n\); the exact corrected range is
   \(0\leq i\leq n-1\).
2. Printed p. 39 says that \(T\) never changes the denominator of any
   rational in \(\mathbb Q[(2)]\).  This is false:
   \(T(1/3)=1\).  A reduced odd denominator is preserved when it is also
   prime to 3.  Every periodic rational has that property by the case split
   above.
3. Printed p. 39 writes
   \(\delta(v)=D(v)/(N(v),D(v))\).  For the positive denominator used
   elsewhere, absolute values are required unless a signed-gcd convention is
   supplied.
4. Printed p. 40 writes \(T_k(n)=T_{-k}(-n)\).  The branch formulas give
   instead
   \[
   T_k(n)=-T_{-k}(-n),
   \]
   equivalently \(T_{-k}=J\circ T_k\circ J\) for \(J(n)=-n\).
5. The final correspondence sentence on printed p. 34 restricts to
   \(k\equiv1\pmod6\); the preceding sentence, printed p. 40, and the
   examples require \(k\equiv\pm1\pmod6\).
6. The invariant-stratum sentence on printed p. 40 needs the standing
   \(\gcd(k,3)=1\) hypothesis.  It is false for arbitrary odd \(k\), for
   example \(k=3\).

## Remaining theorem and conjecture boundaries

The remainder of the paper was read, including Theorems 3.1--3.5 and
4.1--4.3.  Their exact roles are retained for later integration:

- Theorem 3.1 proves infinitely many admissible \(k\) have no primitive cycle
  of period at most \((5/4)k^{1/3}\).
- Theorem 3.2 gives an either-no-cycle or large-cancellation alternative.
- Theorem 3.3 gives occasional large values of the short-cycle count.
- Theorem 3.4 propagates a positive integer already lying on one primitive
  \(T_k\)-cycle to infinitely many parameters.
- Theorem 3.5 bounds parameters for a fixed negative cycle member.
- Theorems 4.1--4.3 prove numerator-distribution and average short-cycle
  bounds at their displayed parameter ranges.
- Primitive-cycle existence, primitive-cycle finiteness, Conjecture P, and
  the Equidistribution Conjecture remain conjectures.
- The random-numerator discussion in Section 3.5 is expressly heuristic and
  is acknowledged by the source to be false in its literal independence
  form.

The paper does not prove that every admissible \(k\) has a primitive cycle,
that every \(T_k\) has finitely many cycles, or that every positive integer
reaches 1.
