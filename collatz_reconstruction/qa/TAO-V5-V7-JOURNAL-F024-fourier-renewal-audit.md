# Tao fine-scale Fourier and renewal audit (F024)

## Scope and controlling manifestations

This record audits the content of Tao's fine-scale-mixing, Fourier, and
renewal argument rather than its labels or later summaries.  The controlling
working source is

- Terence Tao, *Almost all orbits of the Collatz map attain almost bounded
  values*, arXiv:1909.03562v7, source `collatz.tex`, 1,956 lines, 164,932
  bytes, SHA-256
  `bfbc39432d4084a276416cb019a592003c868fa32f18e2f90028ac325ae5c19d`.

Two separately versioned comparison witnesses were also read:

- arXiv:1909.03562v5, safely acquired to the topical shelf as source archive
  `1909.03562v5.eprint`, 1,226,298 bytes, SHA-256
  `eb7a4668ebf27a3f795f72fcdc8d992ada365824359c734fa58813c750ff2ede`,
  and extracted `collatz.tex`, 163,356 bytes, SHA-256
  `c676b362b30807aa6690d0d4f16b8c8e84324732f5c0eb72ccfd875000276ae0`;
- the published Forum of Mathematics, Pi 10 (2022), e12 PDF, 56 physical
  pages, 1,008,484 bytes, SHA-256
  `55c817c73498f940ed1e70f10208105922f1f7c89e378dcb629040c534151a2b`.

The v5 topical-shelf archive is byte-identical to the previously routed local
archive.  The version boundary is substantive: no theorem or proof text is
transferred between v5, v7, and the journal unless this record states and
checks the transfer.

Content-read intervals for this pass are v7 lines 449--519 and 926--1860,
v5 lines 1638--1682 and 1800--1846, and journal physical pages 49--55.  The
earlier theorem, probability-space, and Section 5 passages are covered by
`qa/TAO-V7-F001-proof-text-audit.md`.

## Exact dependency graph and numbering

Remark 7.5 consumes the shared theorem counter.  The correct published
numbering is therefore:

1. Proposition 1.17, characteristic-function decay;
2. Proposition 1.14, fine-scale mixing;
3. Proposition 7.1, key Fourier decay;
4. Lemma 7.2, cancellation at a white point;
5. Proposition 7.3, the renewal process encounters many white points;
6. Lemma 7.4, black-set triangle structure;
7. Remark 7.5, the unused Baker interface;
8. Lemma 7.6, holding-time properties;
9. Lemma 7.7, first-passage location;
10. Proposition 7.8, monotonicity of the maximal quantity;
11. Lemma 7.9, many triangles imply many white points;
12. Lemma 7.10, large triangles are rarely encountered.

The exact proof DAG is

```
Lemma 2.2 (d=2 local bound)
  -> Lemma 7.7
Lemma 7.4 + Lemma 7.7
  -> repaired Case 2 of Proposition 7.8
Lemma 7.4 + Lemma 7.7
  -> repaired Lemma 7.9
Lemma 7.4 + Lemma 7.7 + post-p convolution
  -> parameterized Lemma 7.10
repaired Lemmas 7.9 and 7.10
  -> repaired Case 3 of Proposition 7.8
Proposition 7.8
  -> Proposition 7.3
  -> Proposition 7.1
  -> Proposition 1.17
  -> Proposition 1.14.
```

At the F024 checkpoint, the then-open downstream chain was Proposition 1.14
plus Proposition 1.9 to Proposition 1.11, then Theorem 1.6 and Theorem 1.3.
F025 subsequently supplied the independent Proposition 1.9 proof, and F026
subsequently closed its exact use with Proposition 1.14 to obtain Proposition
1.11. This record certifies the fine-scale branch only; Theorem 1.6, Theorem
1.3, and the durable release gate remain separate.

Sections 6--7 import no external research theorem.  Section 6 has no
bibliographic citation.  Section 7 cites Baker only in v7 line 1366 and says
explicitly that Baker's theorem is not used.  Marek Biskup is credited for
the renewal formulation, not cited as a proof dependency.

## Forced source corrections before the proof can be read literally

### Lemma 2.2

- v7 line 505 requires the vector `\vec\lambda` in the contour-shift
  exponential.
- v7 line 516 evaluates a (d)-dimensional Gaussian integral as
  (n^{-1/2}).  The exact value needed by the stated lemma is
  
  \[
  \int_{\mathbb R^d}e^{-cn|t|^2}\,dt
  =n^{-d/2}\int_{\mathbb R^d}e^{-c|u|^2}\,du
  =O_d(n^{-d/2}).
  \]
  
  The (d=2) instance supplies the (k^{-1}) factor used at v7 line 1462.

### Section 6

- v7 line 1051 has (3^n); the coefficient in the offset recursion is
  (3^{n-1}).
- v7 line 1093 must use the tuple
  ((a_1,\ldots,a_{k+1})) and total (a_{[1,k+1]}=l), not an (m)-tuple.
- The collision estimate is made exact below; it does not require counting
  the number of admissible tuples.

### Pairing and black triangles

- At v7 lines 1130--1131, for odd (n=2q+1), the random (g)-factor must
  remain inside the expectation:
  
  \[
  S_\chi(2q+1)=\mathbb E_{\mathbf b}\left[
    \prod_{r=1}^{q}f(3^{2r-2}2^{-B_r},b_r)\,
    g(3^{2q}2^{-B_q})\right],\qquad B_0=0.
  \]
  
  For even (n=2q), the (g)-factor is absent.  The prose at line 1131
  also drops its (3^{n-1}) argument.
- v7 line 1129 must read (j\in[n/2]), not (j\le[n/2]).
- v7 line 1174 requires (\theta(j,l)), not
  (\theta(j,\mathbf b_{[1,j]})).
- v7 line 1272 needs an absolute value around (\theta(j,l')).
- v7 line 1285 is valid for (j'\ge j_*) and (l'\le l_*), not
  (l'\ge l_*).
- Put
  (X=-s_*+(j'-j_*)\log9+(l_*-l')\log2).  V7 lines 1311--1313 must be
  
  \[
  \varepsilon<\varepsilon e^X
  \le \varepsilon^{1-(\log9+\log2)/10}<\tfrac12,
  \qquad |\theta(j',l')|=\varepsilon e^X>\varepsilon.
  \]
- In the boundary case (j'=j) at lines 1330--1334, the already obtained
  weak blackness of ((j,l_*+1)) gives the contradiction directly.  The
  iteration through (j'-1) is used only for (j'>j); this avoids an
  out-of-domain (j=0) point.

All these black-triangle defects persist in v5.  V5 is not a corrective
authority for them.

### Holding, stopping, and renewal text

- v7 line 1408 is not normalized: at (k=0) it gives (4/3).  Its exact
  replacement is recorded below.
- v7 line 1503 has an unmatched prose parenthesis; line 1514 needs `ref`,
  not `eqref`.
- v7 line 1556 extracts a white factor at a time not contained in the
  stopped product.  This is a genuine proof gap, repaired by stopping one
  step later.
- v7 line 1656 substitutes ((j,l)) for the declared initial point
  ((j',l')) twice.
- v7 line 1676 has a malformed recursive call.  The typed call is
  (Z((j',l')+\mathbf v_{[1,\mathbf k_1]},R-1)).
- v7 line 1700 has malformed (\mathbf v_{[1,\mathbf k]}) notation;
  lines 1716 and 1719 use a deterministic (k) where the stopping time is
  (\mathbf k).
- v7 lines 1829, 1832, and 1836 omit parentheses and thereby place
  (+\varepsilon R) inside an indicator.
- v7 line 1851 names (4^A(1+p^3)), inconsistent with the actual event
  (4^A(1+p)^3); line 1859 uses the old (p) where the new time is (p').

The real-tip estimate at v7 line 1607 needs no additional (+1) after the
smallness choice below.  Lemma 7.4 confines every lattice point of a triangle
to (j\le\lfloor n/2-\delta\rfloor), with
\(\delta=\frac1{10}\log(1/\varepsilon)\ge1\).  Hence
\(j_\Delta+s_\Delta/\log9<\lfloor n/2-\delta\rfloor+1
\le\lfloor n/2\rfloor\), which is stronger than the source's needed bound.

## Section 6 reconstructed at map level

For (0\le r\le N), define the uniform lifting map

\[
(L_{r\to N}\mu)(y)=3^{r-N}\mu(y\bmod3^r),
\qquad y\in\mathbb Z/3^N\mathbb Z.
\]

Its domain is the signed measures on \(\mathbb Z/3^r\mathbb Z\), its
codomain is the signed measures on \(\mathbb Z/3^N\mathbb Z\), and it
preserves total mass and the \(\ell^1\)-norm.  The fibre belongs to the
reduction map
\(\pi_{N,r}:\mathbb Z/3^N\mathbb Z\to\mathbb Z/3^r\mathbb Z\), and is
\(x+3^r\mathbb Z/3^N\mathbb Z\).  Define the typed fibre projection by

\[
(P_{r,N}\nu)(y)=3^{r-N}
\sum_{z\equiv y\;({\rm mod}\;3^r)}\nu(z).
\]

Projective consistency at v7 lines 353--357 gives

\[
P_{r,N}\mu_N=L_{r\to N}\mu_r,
\]

where \(\mu_r\) is the law of the \(r\)-Syracuse random variable.

For \(10\le m\le N\), choose the strictly decreasing chain
\(N=n_0>n_1>\cdots>n_t=m\) by repeatedly taking the larger of (m) and
\(\lceil0.9n_i\rceil\).  The lower bound ten is essential: below ten the
ceiling need not decrease.  Then

\[
\begin{aligned}
\|\mu_N-L_{m\to N}\mu_m\|_1
&\le\sum_{i=0}^{t-1}
 \|L_{n_i\to N}\mu_{n_i}-L_{n_{i+1}\to N}\mu_{n_{i+1}}\|_1\\
&=\sum_{i=0}^{t-1}
 \|\mu_{n_i}-L_{n_{i+1}\to n_i}\mu_{n_{i+1}}\|_1.
\end{aligned}
\]

The restricted (0.9n\le m\le n) estimate applies to every summand.
Because the (n_i) decrease geometrically until the final level, the sum of
(n_{i+1}^{-A-1}) is (O_A(m^{-A-1})), and a harmless exponent reserve
gives the source's (O_A(m^{-A})) bound.  This is the explicit telescoping
map implicit in v7 lines 932--936.  The cases \(1\le m<10\) follow
separately from the triangle inequality after enlarging the
(A\)-dependent constant, and the finitely many small (N) excluded in
the restricted proof are absorbed into the same constant.

For the restricted range, define

\[
F_r(a_1,\ldots,a_r)=
\sum_{q=1}^r3^{r-q}2^{-a_{[q,r]}}.
\]

The term with the uniquely least 2-adic valuation is
(3^{r-1}2^{-a_{[1,r]}}).  Thus equality of two offsets first forces
equality of the total valuation sums, after which subtraction gives

\[
F_{r-1}(a_2,\ldots,a_r)=F_{r-1}(a'_2,\ldots,a'_r).
\]

Induction proves rational injectivity, including its domain, codomain, and
singleton fibres.  Under the concentration conditions and fixed total (l),
multiplication by (2^l) turns a congruence modulo (3^n) into a congruence
between two positive integers.  The source estimates at lines 1076--1084
put each strictly below (3^n); the congruence is therefore equality, and
rational injectivity proves the residue-level separation.

For fixed stopping index (k), first replace the all-interval event (E) by
the prefix event (E_k), which retains only the concentration inequalities
in (a_1,\ldots,a_{k+1}).  The inclusion (E\subseteq E_k) and the source's
concentration estimate give
\(\mathbb P(E_k\setminus E)=O_{A,C_A}(N^{-A-1})\).  This error is paid by
the triangle inequality before factorisation; only then are
\(E_k,B_k,C_{k,l}\) and the prefix offset independent of the suffix
variables.  For fixed total (l), let

\[
p_y=\mathbb P(F_{k+1}\equiv y\pmod{3^N},
E_k\cap B_k\cap C_{k,l}).
\]

This is the unnormalised restricted joint mass, not a normalized conditional
probability.  Separation and the exact geometric product law give

\[
0\le p_y\le2^{-l},\qquad \sum_y p_y\le1.
\]

Consequently the collision term is bounded without an implicit tuple count:

\[
3^n\sum_y p_y^2
\le3^n(\max_y p_y)\sum_y p_y
\le3^n2^{-l}=n^{O(C_A^2)}.
\]

For every surviving frequency
\(\eta\notin3^{N-m}\mathbb Z/3^N\mathbb Z\), let
\(v=\nu_3(\eta)<N-m\).  Division by (3^v) and inversion of (2^l) give a
unique unit in the correct quotient ring,

\[
\bar\eta'\in(\mathbb Z/3^{N-v}\mathbb Z)^\times,
\qquad
\eta/3^v=2^l\bar\eta'\pmod{3^{N-v}}.
\]

The quotient is not unique modulo (3^N): it has (3^v) lifts there.  Put
\(q=N-k-v-1\), and let
\(\eta'_q\in(\mathbb Z/3^q\mathbb Z)^\times\) be the reduction of
\(\bar\eta'\).  Since (m\ge0.9N) and
\(k=N\log3/(2\log2)+O(C_A\sqrt{N\log N})\), one has (q\gg N\).  Exact
cancellation in the suffix character gives

\[
\mathbb E e^{-2\pi i\eta3^{k+1}2^{-l}F_{N-k-1}/3^N}
=\mathbb E e^{-2\pi i\eta'_q
\operatorname{Syrac}(\mathbb Z/3^q\mathbb Z)/3^q}.
\]

Proposition 1.17 with a sufficiently enlarged exponent absorbs the collision
polynomial uniformly.  The fixed-((k,l)) estimate is then summed over
(O_A(N)) stopping indices and (O_A(\log N)) totals using two reserved
powers of (N); the discarded concentration event has the independent
(O_A(N^{-A-1})) reserve.  This closes the reduction from Proposition 1.17
to Proposition 1.14 after the two forced source corrections above.

## Exact pairing and renewal coordinates

For (q=\lfloor n/2\rfloor), put
(b_r=a_{2r-1}+a_{2r}) and (B_r=\sum_{u=1}^r b_u), with (B_0=0).
Then

\[
\mathbb P(b_r=b)=\frac{b-1}{2^b},\qquad b\ge2.
\]

Conditioning on the (b_r) gives the corrected even and odd pairing
identities recorded above.  For (b=3), the two conditional fibres are
((1,2)) and ((2,1)), each of mass (1/2), so

\[
f(x,3)=\frac{\chi(5x)+\chi(7x)}2
=\frac{\chi(5x)}2(1+\chi(2x)).
\]

With (x=3^{2j-2}2^{-l}),
(chi(2x)=e^{-2\pi i\theta(j,l)}), hence

\[
|f(x,3)|=|\cos(\pi\theta(j,l))|=\cos(\pi\theta(j,l)).
\]

The last equality uses $\theta\in(-1/2,1/2]$.  At a white point,
$|\theta|>\varepsilon$, and for the fixed sufficiently small
$\varepsilon$, Taylor's inequality gives
$|f(x,3)|\le e^{-\varepsilon^3}$.  This produces exactly the nonnegative
exponential moment in Proposition 7.3; the terminal (g)-factor has modulus
at most one and is discarded only after it has been kept inside the odd-(n)
expectation.

The success event (b_r=3) has probability (1/4).  Let (Q) have the
Pascal law conditioned on (b\ne3), let
(R=\mathbf j-1\) be the number of failures before the first success, and
let (Q_i) be iid copies of (Q).  The holding vector is

\[
\mathbf H=(1,3)+\sum_{i=1}^{R}(1,Q_i),\qquad
\mathbb P(R=r)=\frac14\left(\frac34\right)^r.
\]

Writing (M_Q(k)=\mathbb E e^{(1,Q)\cdot k}), its normalized moment
generating function is

\[
\mathbb E e^{\mathbf H\cdot k}
=\sum_{r=0}^{\infty}\frac14\left(\frac34\right)^r
e^{(1,3)\cdot k}M_Q(k)^r
=\frac{e^{(1,3)\cdot k}}{4-3M_Q(k)}
\]

whenever (3M_Q(k)<4).  This equals one at (k=0) and is finite in a
neighbourhood of zero, proving an exponential tail.  The support contains
((1,3),(2,5),(2,7),(2,8)); its differences generate ((0,1)) and
((1,0)), hence all of (mathbb Z^2).  Finally

\[
\mathbb E Q=13/3,\qquad \mathbb ER=3,
\qquad \mathbb E\mathbf H=(4,16).
\]

Thus the renewal path has exact mean vector ((4,16)), not merely a slope
analogy.

## Black triangles after the source corrections

Fix once and for all (0<\varepsilon\le e^{-10}), small enough also for
the white-point cancellation and the exit estimate below, and put
(delta=\frac1{10}\log(1/\varepsilon)\).  The phase recurrences are

\[
\theta(j+1,l)\equiv9\theta(j,l),\qquad
\theta(j,l-1)\equiv2\theta(j,l)\pmod{\mathbb Z}.
\]

The source's three weak-black propagation rules follow without wraparound.
For example, the up-left relation first gives (5/100), and the doubling
relation then sharpens it to (1/200).  The primitive-frequency condition
(3\nmid\xi) gives the exact right-strip obstruction at v7 lines 1255--1265.

For a reconstructed anchor ((j_*,l_*)), write
(|\theta(j_*,l_*)|=\varepsilon e^{-s_*}).  On the corrected domain
(j'\ge j_*,l'\le l_*), multiplication is by the integer
(9^{j'-j_*}2^{l_*-l'}), so

\[
|\theta(j',l')|\le
\varepsilon e^{-s_*+(j'-j_*)\log9+(l_*-l')\log2},
\]

with equality below the (1/2) wraparound threshold.  Every lattice point
of the resulting triangle is black.  The three corrected collar cases show
that every exterior lattice point within distance (delta) is white.  The
choice $\varepsilon\le e^{-10}$ ensures simultaneously
(delta\ge1), all weak-black bounds are below (1/100), and the Case 1
upper bound is below (1/2).  Therefore the black set is a disjoint union of
these triangles, distinct triangles are at least (delta) apart, and every
triangle is confined (delta) to the left of (n/2).

## First-passage Green kernel and the omitted convolution

Let (mathbf V_q=\sum_{i=1}^q\mathbf H_i), with
(mathbf V_0=(0,0)), and define the renewal Green kernel

\[
U(x,t)=\sum_{q\ge0}\mathbb P(\mathbf V_q=(x,t)).
\]

The corrected (d=2) instance of Lemma 2.2 gives

\[
\mathbb P(\mathbf V_q=(x,t))
\ll(q+1)^{-1}G_q(c((x,t)-q(4,16))).
\]

Put (z=x-t/4).  The coordinate identity

\[
(x-4q,t-16q)=\left(z+\frac{t-16q}{4},t-16q\right)
\]

is an invertible linear change with two-sided norm bounds.  Split the
(q)-sum into (16q\in[t/2,2t]), (16q<t/2), and (16q>2t).  In the
central range (q\asymp1+t); summing the vertical discrete Gaussian costs
(O(\sqrt{1+t})) against the prefactor (O((1+t)^{-1})).  In the two
outer ranges, the vertical deviation is comparable to (t+q), and the
remaining horizontal deviation retains either Gaussian or exponential decay
in (z).  Thus

\[
U(x,t)\ll(1+t)^{-1/2}
G_{1+t}(c'(x-t/4)).
\]

For (t=0), positivity of the increments leaves only
(mathbf V_0=(0,0)), so the same bound holds after enlarging the constant.

Let (kappa_s=\inf\{q\ge1:(\mathbf V_q)_2>s\}).  If (l>s), the final
increment must have vertical component at least (l-s).  Independence and
the exponential tail give

\[
\begin{aligned}
\mathbb P(\mathbf V_{\kappa_s}=(j,l))
&\ll e^{-c(l-s)}
\sum_{r=0}^{s}\sum_{u\ge1}e^{-c(r+u)}U(j-u,s-r).
\end{aligned}
\]

For
(K_s(x)=(1+s)^{-1/2}(e^{-cx^2/(1+s)}+e^{-c|x|})), the two stable
convolution inequalities

\[
\sum_{r=0}^s e^{-ar}K_{s-r}(x+r/4)\ll K_s(c_1x),
\qquad
\sum_{u\ge1}e^{-au}K_s(x-u)\ll K_s(c_2x)
\]

follow by splitting at (r=s/2) and (u=|x|/2), respectively, and
shrinking the decay constants.  Applying them yields the fully typed
first-passage estimate

\[
\mathbb P(\mathbf V_{\kappa_s}=(j,l))
\ll\frac{e^{-c(l-s)}}{\sqrt{1+s}}
G_{1+s}(c(j-s/4)).
\]

This fills v7 lines 1457--1463 rather than treating “routine calculation” as
a proof.

There is also a sharper post-passage consequence which does not require a
tail cutoff for the later horizontal increments.  Let
\(m\) be sufficiently large, let \(s,p\in\mathbb N_0\), let
\(r_0\ge1\), and let \(\Sigma\subset\mathbb Z\) be \(h\)-separated.  If
\[
s>m/\log^2m,\qquad p\le m^{0.1},\qquad
4r_0\le h\le m^{0.4},
\]
then

\[
\mathbb P\bigl(\operatorname{dist}((\mathbf V_{\kappa_s+p})_1,
\Sigma)\le r_0\bigr)
\ll \frac {r_0} h.
\]

Indeed, summing the first-passage display over the vertical coordinate gives
the horizontal kernel \(K_s\).  Direct summation over the disjoint
radius-\(r_0\) intervals gives
\[
\sum_{\operatorname{dist}(x,\Sigma)\le r_0}K_s(x-s/4)
\ll \frac{r_0}{\sqrt{1+s}}+\frac{r_0}{h}.
\]
The smoothing-scale hypothesis makes the first term at most the second.
Conditioning on the sum of the \(p\) later horizontal increments merely
translates \(\Sigma\), preserving its spacing.  This is the exact post-
\(p\) estimate needed at v7 lines 1805--1812.  The condition
\(h\le m^{0.4}=o(\sqrt s)\) is essential; without it a singleton at the
kernel peak disproves a bare \(O(r_0/h)\) estimate.

## Repaired monotonicity: Cases 1 and 2

Extend (1_W) by zero outside
([n/2]\times\mathbb Z), and set

\[
Q(x)=\mathbb E_x\prod_{q\ge0}e^{-\varepsilon^3 1_W(X_q)},
\qquad X_q=x+\mathbf V_q.
\]

Then
(Q(x)=e^{-\varepsilon^3 1_W(x)}\mathbb E Q(x+\mathbf H)).
For (m\ge1), let

\[
Q_m=\sup_{\substack{j\in\mathbb N_+,\ j\ge\lfloor n/2\rfloor-m\\
l\in\mathbb Z}}
\max(\lfloor n/2\rfloor-j,1)^A Q(j,l).
\]

At (m=\lfloor n/2\rfloor), this domain is identical to the domain for
(Q_{m-1}), because both impose (j\in\mathbb N_+\); the endpoint inequality
is therefore equality.  For smaller (m), the genuine boundary row is
(j=\lfloor n/2\rfloor-m\in\mathbb N_+\).  No (j=0) row is admitted.

At a white starting point, the immediate factor
(e^{-\varepsilon^3}) absorbs the exponential moment of the horizontal
coordinate in

\[
\max(m-r,1)^{-1}\le m^{-1}
\exp\!\left(Cr\frac{\log m}{m}\right).
\]

This is source Case 1.

For source Case 2, let (x=(j,l)) lie in a triangle at vertical depth
(0\le s\le m/\log^2m), and stop at (kappa_s).  Iterating the recursion
one further step than the printed proof gives the exact identity

\[
Q(x)=\mathbb E\left[
e^{-\varepsilon^3\sum_{q=0}^{\kappa_s}1_W(X_q)}
Q(X_{\kappa_s+1})\right].
\]

The terminal horizontal coordinate is at least (j+1), so the definition
of (Q_{m-1}) applies.  With
(lambda=C A\log m/m),

\[
Q(x)\le m^{-A}Q_{m-1}
\mathbb E\left[e^{-\varepsilon^31_W(X_{\kappa_s})}
e^{\lambda(\mathbf V_{\kappa_s+1})_1}\right].
\]

The first-passage estimate gives
\(\mathbb E e^{\lambda(\mathbf V_{\kappa_s})_1}
=1+O_A(1/\log m)\).  To obtain the exit-white constant, first choose
absolute integers \(M_v,M_h\) so that summing the first-passage kernel outside
\[
1\le(\mathbf V_{\kappa_s})_2-s\le M_v,qquad
| (\mathbf V_{\kappa_s})_1-s/4|\le M_h\sqrt{1+s}
\]
leaves probability at most \(1/2\).  The strict slope inequality
\((\log9)/4<\log2\) places every supported point in this rectangle outside
the entered triangle but within an absolute distance
\(C_{\rm exit}=C(M_v,M_h)\).  The global smallness threshold is then fixed
so that
\[
\varepsilon_0\le e^{-10},\qquad
\tfrac1{10}\log(1/\varepsilon_0)>C_{\rm exit}+1.
\]
For \(0<\varepsilon\le\varepsilon_0\), the white collar gives the uniform
bound \(\mathbb P(X_{\kappa_s}\in W)\ge1/2\).  Strong Markov at
\(\kappa_s\) factors the extra holding increment and contributes
\(1+O_A(\log m/m)\).  Therefore

\[
\mathbb E\left[e^{\lambda(\mathbf V_{\kappa_s})_1}
e^{-\varepsilon^31_W(X_{\kappa_s})}\right]
\le1+O_A(1/\log m)-\tfrac12(1-e^{-\varepsilon^3}).
\]

For (m\ge C_{A,\varepsilon}), multiplication by the extra-increment
factor is at most one.  Hence (Q(x)\le m^{-A}Q_{m-1}).  This repairs the
genuine gap at v7 line 1556 without changing the source conclusion.

## Lemma 7.9: exact version boundary and v7 repair

V5 lines 1654--1659 and journal equation (7.57) state the stronger
unconditional estimate

\[
\mathbb E\exp\left(-\sum_{p=1}^{t_{\min(r,R)}}1_W(X_p)
+\varepsilon\min(r,R)\right)\le e^\varepsilon.
\]

V7 lines 1660--1665 instead state only

\[
\mathbb E1_{\{r\ge R\}}
\exp\left(-\sum_{p=1}^{t_R}1_W(X_p)+\varepsilon R\right)
\le e^\varepsilon.
\]

The latter is a genuine weakening, not a reindexing.  On (r\ge R), the
integrands agree; the v7 statement supplies no control on (r<R).  The
displayed v5/journal induction is not a proof of its stronger statement: on
(r=1<R), the quantity stops at (t_1), whereas the induction replaces it
by a product continuing through the later top-exit time.  The stronger
statement is therefore recorded as printed but uncertified here.

The weaker v7 statement has the following exact proof.  Define triangle
entry times allowing time zero.  After the (i)-th entry, let (sigma_i)
be the first later time whose vertical coordinate is above that triangle's
top, and let (t_{i+1}) be the first black time at or after (sigma_i).
On (r\ge R), every (sigma_i), (1\le i<R), occurs no later than
(t_R).  The first-passage exit argument supplies a uniform (c_0>0) with

\[
\mathbb P(X_{\sigma_i}\in W\mid\mathcal F_{t_i})\ge c_0.
\]

Put \(\rho=1-(1-e^{-1})c_0<1\), and choose the already fixed
\(\varepsilon\) still smaller if necessary so that
\(e^\varepsilon\rho\le1\).  The marginal exit bound is converted to a
product bound by the following uniform induction.  For \(q\in\mathbb N_0\),
set
\[
H_q(x)=\mathbb E_x\left[
1_{\{r\ge q+1\}}\prod_{i=1}^{q}e^{-1_W(X_{\sigma_i})}
\right].
\]
Then \(H_0\le1\), and strong Markov at the first top exit gives
\[
H_q(x)=\mathbb E_x\left[
1_{\{r\ge1\}}e^{-1_W(X_{\sigma_1})}
H_{q-1}(X_{\sigma_1})\right]\le\rho^q.
\]
The complete white count through \(t_R\) dominates the \(R-1\) distinct
exit indicators, so

\[
\begin{aligned}
&\mathbb E1_{\{r\ge R\}}
e^{-\sum_{p=1}^{t_R}1_W(X_p)+\varepsilon R}\\
&\qquad\le e^{\varepsilon R}\rho^{R-1}
\le e^\varepsilon.
\end{aligned}
\]

This displayed induction, rather than the marginal estimate alone, proves the
factor \(\rho^{R-1}\).  It also fixes the source's missing time-zero entry
atom.

For v7, Markov's inequality applies only to the restricted event

\[
F_*=
\left\{r\ge R,
e^{-\sum_{p=1}^{t_R}1_W(X_p)+\varepsilon R}>T\right\}.
\]

The unqualified (F_*) at v7 lines 1830--1834 is not controlled by the
weaker lemma.  The restriction is sufficient because the downstream argument
uses (F_*) only while assuming (r\ge R).

## Parameterized Lemma 7.10 and the quantitative repair (preliminary record)

The coordinate and finite-range details in this preliminary record are
superseded by the exact addendum at the end of F024.  It is retained to make
the audit chronology visible, not as an independently citable proof state.

The conclusion printed in every manifestation is

\[
\mathbb P(E_{p,s'})\ll
A^2\frac{1+p}{s'}+e^{-cA^2(1+p)}.
\]

Its proof is stable under replacing every cutoff (A^2(1+p)) by
(D(1+p)).  More precisely, there are absolute constants
(C_0,c_0,C_1>0) such that, for (D\ge1),
(C_1D(1+p)\le s'\le m^{0.4}), and sufficiently large (m),

\[
\mathbb P(E_{p,s'})\le
C_0\left(\frac{D(1+p)}{s'}+e^{-c_0D(1+p)}\right).
\]

The vertical overshoot and (p)-increment tails give the exponential term.
The horizontal deviations (s^{0.6}) have exponentially smaller tails
because (s>m/\log^2m) and (s'\le m^{0.4}).  On the regular event, the
triangle inequalities force an encountered triangle's lower tip to lie
within (O(D(1+p))) of the old top and its top-left horizontal coordinate
within the same tolerance of the renewal location.  Two eligible triangles
of size at least (s') have top-left coordinates separated by
(\gg s').  The post-(p) Green-kernel convolution above then gives the
first term.  This fills rather than assumes v7 lines 1805--1812.

The source's subsequent choice (s'_p=4^A(1+p)^3) yields only
(O(A^2 4^{-A})).  It cannot imply the required (10^{-A-2}) probability,
because

\[
\frac{A^2 4^{-A}}{10^{-A-2}}=100A^2(10/4)^A\longrightarrow\infty.
\]

Put (delta_A=10^{-A-2}).  Choose

\[
D_A\ge\max\left(1,
\frac1{c_0}\log\frac{6C_0}{\delta_A(1-e^{-c_0})}\right)
\]

and then

\[
K_A\ge\max\left(C_1D_A,
\frac{6C_0D_A\zeta(2)}{\delta_A}\right).
\]

For (s'_p=K_A(1+p)^3), summing the parameterized bound over any finite
set of (p\)'s gives

\[
\mathbb P(E_*)\le\delta_A/3.
\]

Now put (H=10A/\varepsilon^3) and define

\[
R=\left\lceil
\frac{H+\log3+(A+2)\log10+\varepsilon+1}{\varepsilon}
\right\rceil.
\]

With

\[
F_*=\left\{r\ge R,
e^{-S_R+\varepsilon R}>3\delta_A^{-1}e^\varepsilon\right\},
\qquad S_R=\sum_{p=1}^{t_R}1_W(X_p),
\]

the repaired v7 Lemma 7.9 gives
(mathbb P(F_*)\le\delta_A/3).  Outside (F_*), (r\ge R) forces
(S_R>H).

Let (h=\lceil H\rceil), (u_1=h), and recursively set

\[
u_{i+1}=u_i+\left\lceil10K_A(1+u_i)^3\right\rceil+h+1,
\qquad P=u_R+2.
\]

This is a finite, explicit (P=P(A,\varepsilon)).  Enlarge the lower
threshold for (m) until

\[
P\le m^{0.1},\qquad K_A(1+P)^3\le m^{0.4}
\]

and until the already established tail event

\[
G=\{(\mathbf V_{\kappa_s+P})_1\ge0.9m\}
\]

has probability at most \(\delta_A/3\), with the separately required weighted
budget \(m^A\mathbb P(G)\le1/2\).  The event (G) must be retained:
(B\uplus W) partitions only the strip, not the whole plane.

If at most (H) of the times (0,\ldots,P-1) are white, the actual first
triangle-entry time obeys (t_1\le h=u_1\).  Inductively, if
(t_i\le u_i), then outside (E_*\) its triangle has size
(<K_A(1+t_i)^3\le K_A(1+u_i)^3\).  At

\[
b_i=t_i+\lceil10K_A(1+u_i)^3\rceil+1
\]

the path is above that triangle's top, so (b_i\ge\sigma_i\).  The next
(h+1) times contain a black point, and the defining minimality of the actual
next entry gives (t_{i+1}\le b_i+h\le u_{i+1}\).  Thus the recursion proves
the existence of (R) actual distinct triangle entries with
(t_R\le u_R\le P-2\).  Outside (F_*\), this
forces more than (H) white times by (t_R\), a contradiction.  Hence the
bad event is contained in (E_*\cup F_*\cup G) and has probability at most
(delta_A).  This is the exact replacement for v7 lines 1823--1859.

## Consequence and nonclaims

The three cases now prove (Q_m\le Q_{m-1}) for
(m\ge C_{A,\varepsilon}).  The finite base range and the exponential tail
of the first holding coordinate give

\[
Q(j,l)\ll_A\max(\lfloor n/2\rfloor-j,1)^{-A},
\qquad \mathbb E Q(\mathbf H)\ll_A n^{-A}.
\]

Thus Proposition 7.3, Proposition 7.1, and Proposition 1.17 follow at their
stated uniform scope.  The Section 6 map and collision argument then give
Proposition 1.14.  Every implication here is versioned to v7 plus the
separately attributed repairs in this edition.

This does **not** prove convergence of Collatz or a fixed absolute orbit
bound.  It does not upgrade logarithmic density to natural density.  It does
not prove the stronger v5/journal form of Lemma 7.9.  It does not use Baker's
theorem.  It does not identify any Siegel Fourier claim with Tao's Fourier
proof.  It does not erase the source defects: each corrected formula remains
typed as an editorial repair rather than silently attributed to Tao's raw
v7 text.

## Exact post-exit and Case 3 addendum (controlling F024 record)

This addendum supersedes the preliminary Case 3 coordinate record above.
Let (x=(j,l)) lie at depth

\[
\frac m{\log^2m}<s\le\frac{\log9}{\log2}m
\]

in the initial triangle, let (kappa_s) be the first top-passage time, and
define the shifted process

\[
\widetilde X_p=X_{\kappa_s+p},\qquad
\widetilde{\mathbf V}_p
=\mathbf V_{\kappa_s+p}-\mathbf V_{\kappa_s}quad(p\in\mathbb N_0).
\]

Conditionally on (mathcal F_{\kappa_s}), the increments of
(widetilde{\mathbf V}) are iid holding vectors and are independent of
(widetilde X_0).  Every triangle statistic below is computed from this
shifted process.  This reset is essential: an unshifted (S_R) can count
white points before (kappa_s) and cannot contradict a post-exit low-white
event.

For (p\in\mathbb N_0) and (s'>0), put

\[
E_{p,s'}=\{\widetilde X_p\in\Delta'
\text{ for some }\Delta'\in\mathcal T
\text{ with }s_{\Delta'}\ge s'\}.
\]

There are absolute constants (C_0,c_0,C_1,D_0>0) such that

\[
\mathbb P(E_{p,s'})\le
C_0\left(\frac{D(1+p)}{s'}+e^{-c_0D(1+p)}\right)
\]

whenever

\[
D\ge D_0,qquad 0\le p\le m^{0.1},qquad
C_1D(1+p)\le s'\le m^{0.4}.
\]

The vertical overshoot and the next (p) vertical increments give the
exponential term.  The first-passage kernel and the next (p) horizontal
increments bound the event
(lvert(\mathbf V_{\kappa_s+p})_1-s/4\rvert>2s^{0.6}) by the rational
term.  On the complementary event, an eligible encountered triangle obeys
the exact lower-tip localization

\[
l_\Delta-10<l_{\Delta'}-\frac{s_{\Delta'}}{\log2}
\le l_\Delta+2D(1+p)
\]

and

\[
\lvert(\widetilde X_p)_1-j_{\Delta'}\rvert\le CD(1+p).
\]

If the left lower-tip inequality failed, moving by (O(D(1+p))) on the
row (l_\Delta) would give a lattice point in (Delta'); the horizontal
first-passage bound and the strict inequality
((\log9)/4<\log2) put the same point in the initial (Delta), contrary
to disjointness.  The right inequality follows from
(widetilde X_p\in\Delta').  Intersecting two eligible triangles with the
row (l_\Delta+\lfloor s'/2\rfloor) gives disjoint integer intervals, so
their top-left horizontal coordinates are (c_1s')-separated once
(s'\ge C_1D(1+p)).  The post-passage estimate, with neighbourhood radius
(CD(1+p)) and spacing (c_1s'), supplies the rational term.  This is the
complete geometry before the summation at v7 lines 1805--1812.

Put (delta_A=10^{-A-2}), and choose

\[
D_A\ge\max\left(D_0,
\frac1{c_0}\log\frac{6C_0}{\delta_A(1-e^{-c_0})}\right),
\qquad
K_A\ge\max\left(C_1D_A,
\frac{6C_0D_A\zeta(2)}{\delta_A}\right).
\]

Next set (H=10A/\varepsilon^3),

\[
R=\left\lceil
\frac{H+\log3+(A+2)\log10+\varepsilon+1}{\varepsilon}
\right\rceil,
\]

let (h=\lceil H\rceil), (u_1=h), and define

\[
u_{i+1}=u_i+\left\lceil10K_A(1+u_i)^3\right\rceil+h+1,
\qquad P=u_R+2.
\]

Only after this finite (P=P(A,\varepsilon)) is fixed is (m) enlarged
until

\[
P\le m^{0.1},\qquad K_A(1+P)^3\le m^{0.4}.
\]

The valid finite exceptional event is

\[
E_*^{(P)}=\bigcup_{p=0}^{P-1}E_{p,K_A(1+p)^3}.
\]

Every term is now in the domain of the parameterized estimate, and

\[
\begin{aligned}
\mathbb P(E_*^{(P)})
&\le\frac{C_0D_A}{K_A}
\sum_{p=0}^{P-1}\frac1{(1+p)^2}
+C_0\sum_{p=0}^{P-1}e^{-c_0D_A(1+p)}\\
&\le\delta_A/6+\delta_A/6=\delta_A/3.
\end{aligned}
\]

Condition on (widetilde X_0).  Let (r,t_i,sigma_i) be the triangle
statistics of (widetilde X), and define

\[
S_R=\sum_{p=1}^{t_R}1_W(\widetilde X_p),\qquad
F_*=\{r\ge R:e^{-S_R+\varepsilon R}>
3\delta_A^{-1}e^\varepsilon\}.
\]

The uniform v7 Lemma 7.9 estimate and Markov's inequality give
(mathbb P(F_*)\le\delta_A/3).  Outside (F_*), (r\ge R) forces

\[
S_R\ge\varepsilon R-\log3-\log(\delta_A^{-1})-\varepsilon>H.
\]

The depth upper bound and first-passage kernel give

\[
\mathbb P((\mathbf V_{\kappa_s})_1\ge0.8m)\le Ce^{-cm},
\]

because (0.8>(\log9)/(4\log2)).  Strong Markov gives the same type of
tail after the fixed additional time (P).  Thus, for

\[
G=\{(\mathbf V_{\kappa_s+P})_1\ge0.9m\},
\]

the threshold for (m) can be enlarged until both

\[
\mathbb P(G)\le\delta_A/3,qquad m^A\mathbb P(G)\le1/2.
\]

Outside (G), every inspected shifted point remains in the strip where
(B\uplus W) is the full partition.  Define

\[
N_W=\sum_{p=0}^{P-1}1_W(\widetilde X_p).
\]

If (N_W\le H\), the actual first entry obeys (t_1\le h=u_1\).
Inductively, outside (E_*^{(P)}\), the triangle entered at
(t_i\le u_i) has size below (K_A(1+t_i)^3\le K_A(1+u_i)^3\).  At

\[
b_i=t_i+\lceil10K_A(1+u_i)^3\rceil+1
\]

the path is above its top, so (b_i\ge\sigma_i\).  The next (h+1) times
contain a black point, and minimality of the recursively defined next entry
gives (t_{i+1}\le b_i+h\le u_{i+1}\).  Hence (R) actual distinct entries
exist and (t_R\le u_R\le P-2\).  Outside (F_*\), this yields (S_R>H\),
contradicting (S_R\le N_W\).  Therefore

\[
\mathbb P(N_W\le H)\le
\mathbb P(E_*^{(P)})+\mathbb P(F_*)+\mathbb P(G)\le\delta_A.
\]

The exact bridge from this estimate back to the renewal recursion is

\[
Q(j,l)\le m^{-A}Q_{m-1}\mathbb E\left[
e^{-\varepsilon^3N_W}
\max\left(1-\frac{(\mathbf V_{\kappa_s+P})_1}{m},\frac1m\right)^{-A}
\right].
\]

On (G) the weight is at most (m^A); on (G^c) it is at most (10^A).
Moreover,

\[
\mathbb E e^{-\varepsilon^3N_W}
\le\delta_A+e^{-10A}\le10^{-A-1}.
\]

The weighted expectation is consequently at most

\[
m^A\mathbb P(G)+10^A(\delta_A+e^{-10A})\le1.
\]

This closes the repaired Case 3 at its typed scope.  It does not remove the
separate whole-paper gate: the exact downstream source dependency is

\[
\text{Proposition 1.14}+\text{Proposition 1.9}
\Rightarrow\text{Proposition 1.11}
\Rightarrow\text{Theorem 1.6}
\Rightarrow\text{Theorem 1.3},
\]

and at the F024 checkpoint the edition had not yet supplied a complete typed
reconstruction of Proposition 1.9. F025 subsequently supplied that independent
proof and F026 closed the displayed first edge. Thus this addendum certifies
the fine-scale branch only,
not the main theorem or the whole-paper release.

## Final adversarial closure and certificate boundary

The Fourier adversarial read of the intermediate
`cf3d2abde4ecc5296046b859bc20990b2e9520c6f87b93cf845efcfae2a3e977`
snapshot found five definite typing defects: failure to replace (E) by
(E_k) before suffix independence, false uniqueness of the divided frequency
modulo (3^N), punctuation in the suffix product, omitted domains of (f,g),
and an unqualified MGF convergence formula.  Each is corrected in the final
chapter.  In particular, the quotient is unique in
(mathbb Z/3^{N-v}mathbb Z), then reduced to a unit modulo (3^q).

Independent geometry/first-passage and renewal adversarial reads passed the
`9abb995a2f5be118b43c31a673bb371c0b66f4ba773bc317134f8b7b7e8249b6`
snapshot.  The renewal read first found and then verified repairs for the
(j\in\mathbb N_+) endpoint and the induction on the actual entry times
(t_i).  After those passes, the only mathematical-text changes were to make
the local-factor domains and constants explicit and to normalize the harmless
separation constant to (0<c_1\le1); the (f,g) display was then line-broken
without altering its content. At the F024 checkpoint the chapter was 42,867
bytes with SHA-256
`39984da61e281ec83b1767800e5473c66bb434d165dbdb612b85925b96e8c924`.
Later dependency-boundary propagation changed only its closing nonclaim text;
the current chapter is 42,957 bytes with SHA-256
`23dea1dc9f414a86ac2cfa54ffde6ba884fb96e720ed33c9cf7407cc3070e2cc`.

`certificates/tao_v7_fourier_renewal_checks.py` is 18,278 bytes with SHA-256
`de0f78477d44e744ab22aee0feaaeb2507da8333e216307c5299b9741927f8de`
and reports `PASS`.  It pins eight source/route hashes and eighteen exact
source locators, and checks 182 lift/projection identities, 5,460 bounded
offset injectivity/recurrence instances, 30,948 finite projective reductions,
32,352 quotient-frequency morphisms, 1,720 quotient fibres, 39 holding masses,
three exact holding PGFs, 1,240 deterministic entry-budget instances, and 49
positive-row endpoint instances.  The report explicitly leaves analytic
characteristic decay, black-triangle geometry, the first-passage Green bound,
infinite renewal monotonicity, Proposition 1.9, and Tao's main theorem outside
the finite script's certification scope; those analytic results are controlled
by the proofs and audits above, with Proposition 1.9 and the downstream main
theorem chain still open.

The final three-pass working build has 88 pages, 1,010,550 bytes, and SHA-256
`7391714ee7d06de7fe4511a0f0ebcf2bee0e87ba2a53e2343a2fd801cf6141bb`.
Its log contains zero actionable warnings, overfull/underfull boxes, undefined
controls, or errors; all 25 font rows are embedded and subset.  All 88 pages
were freshly rendered at 200 dpi and all eleven complete contact sheets were
inspected.  Pages 1 and 3--68 are byte-identical to the fully inspected ACT28
200-dpi render; the changed table-of-contents page 2 and pages 72, 73, 81, 83,
87, and 88 were inspected at original render detail.  No
clipping, overlap, malformed display, or margin failure was found.  This is a
working-checkpoint QA result, not release QA or a completion claim.

## F025 dependency-status addendum

The statements above that the present edition had not yet reconstructed
Proposition 1.9 are historical to F024.  They must not be read as current
state.  F025 separately content-read the v5, v7, and journal manifestations,
repaired their exact statement and proof defects, reconstructed the complete
residue-fibre and tail argument, proved the split-surjection valuation map and
its noninjective-fibre obstruction, and passed an independent adversarial
audit plus `certificates/tao_prop19_valuation_checks.py`.

The F024 finite script still correctly reports that it does not itself
certify Proposition 1.9; F025 supplies that independent certification. F026
separately closes the exact use of Propositions 1.14 and 1.9 in Proposition
1.11. The current open gates are the deductions to Theorems 1.6 and 1.3. The
stronger v5/journal Lemma 7.9, natural density, convergence to one, and a fixed
universal orbit bound remain unclaimed.
