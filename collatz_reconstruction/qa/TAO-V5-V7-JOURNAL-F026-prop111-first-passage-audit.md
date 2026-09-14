# Tao v5/v7/journal F026 — Proposition 1.11 first-passage audit

## Scope and routing receipt

This audit closes only the exact dependency edge

\[
\text{Tao Proposition 1.9}+\text{Tao Proposition 1.14}
\Longrightarrow \text{Tao Proposition 1.11}.
\]

It does not close the later deductions to Theorem 1.6 or Theorem 1.3.
Before the edge was admitted, the immutable route ledgers were queried and
the three exact Tao records were recovered:

- `ROUTE-COL-77768C71C4B3C049A8B8`;
- `ROUTE-COL-F8A670E4F671DDE694CB`;
- `DOCROUTE-COL-8F0EDA4DC27DA85735AB`.

The route metadata was used only to locate manifestations. The mathematical
content was read in the source TeX and the separately retained journal PDF.
The frozen routing artifacts remain:

- `state/index_routes.jsonl`: 274170 bytes, SHA-256
  `b05028694bf133b9b19f2b0c0a771323b7a47ae872c0712769267aaf1f1eff38`;
- `state/document_routes.jsonl`: 324776 bytes, SHA-256
  `e439a5f9a70253b00824df5be791415e1c068d574c23f6f7f61851c19a88b2a5`;
- `state/index_snapshot.json`: 799 bytes, SHA-256
  `7d5a17440a3cb039f2bfbb4814567b5805117002136cc65687de738ee99af62f`.

The quarantined task `019fe2cf-438a-7112-859c-119accee0e9e` was not
contacted, messaged, steered, or used as evidence.

## Exact manifestations and locators

### Controlling v7 source

- TeX:
  `C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/latex/1909.03562v7/collatz.tex`;
  164932 bytes; SHA-256
  `bfbc39432d4084a276416cb019a592003c868fa32f18e2f90028ac325ae5c19d`.
- E-print archive: 1226861 bytes; SHA-256
  `ba81acd6254838251f1ee585256a6f9f223cdc9c73bed0a3c4fd25782d0124ad`.
- Proposition 1.11 statement: source lines 316–335.
- Deduction from Propositions 1.9 and 1.14: source lines 649–925.

### Version-pinned v5 comparison

- TeX:
  `C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/latex/1909.03562v5/collatz.tex`;
  163356 bytes; SHA-256
  `c676b362b30807aa6690d0d4f16b8c8e84324732f5c0eb72ccfd875000276ae0`.
- E-print archive: 1226298 bytes; SHA-256
  `eb7a4668ebf27a3f795f72fcdc8d992ada365824359c734fa58813c750ff2ede`.
- Proposition 1.11 statement: source lines 316–335.
- Corresponding deduction: source lines 643–919.

### Published journal comparison

- PDF:
  `C:/Users/LOCAL_USER/Documents/arxiv_latex/library/_recovered_from_papers/by_title/Tao Almost all orbits of the Collatz map attain almost bounded values.pdf`;
  1008484 bytes; 56 pages; SHA-256
  `55c817c73498f940ed1e70f10208105922f1f7c89e378dcb629040c534151a2b`.
- Proposition 1.11 statement: physical page 7.
- Corresponding Section 5 deduction: physical pages 18–27.

The source manifestations are not declared text-identical. V7 broadens a
harmless statement-level quantifier from sufficiently large \(y\) to every
\(y\) with nonempty support; only the two sufficiently large values used in
the proof occur here. More importantly, v5 lines 789–791 and journal physical
page 23 interchange passage time and passage location in the converse
implication. V7 lines 795–797 restore the typed identities: first the equality
of times, then the equality of locations. The modular estimate, affine
calculation, integer-window count, and mixing collapse otherwise agree at the
comparison loci used here.

## Exact theorem boundary

Let \(\alpha=1001/1000\). For odd \(N\), let \(T_x(N)\) be the first
accelerated Syracuse time at which the orbit is at most \(x\), and let
\(\operatorname{Pass}_x(N)\) be that location, with the source convention
that the location is \(1\) if the time is infinite. Let \(\mathbf N_y\) have
the logarithmic law on the odd integers in \([y,y^\alpha]\). Proposition
1.11 asserts, for an absolute \(c>0\),

\[
 \mathbb P(T_x(\mathbf N_y)=+\infty)\ll x^{-c}
 \quad(y=x^\alpha,x^{\alpha^2})
\]

and

\[
 d_{\rm TV}(\operatorname{Pass}_x(\mathbf N_{x^\alpha}),
             \operatorname{Pass}_x(\mathbf N_{x^{\alpha^2}})
 \ll (\log x)^{-c}.
\]

Here \(d_{\rm TV}\) is Tao's unhalved \(\ell^1\) distance. The proposition
does not assert a coupling, natural-density transport, convergence to one,
or any universal orbit bound.

## Source defects at this edge

The reconstruction preserves and repairs the following local defects instead
of silently attributing the repaired text to Tao:

1. V7 lines 651–652 display \(\operatorname{Pass}_x\) where a time is being
   estimated and require \(\log(\mathbf N_y/x)\), not the printed numerator.
2. Line 689 requires \(1.9n_0\), not \(1.9n\).
3. The periodic aside at line 699 requires the representative of
   \(-\mathbf m\) modulo the least positive period, or a period multiple at
   least \(\mathbf m\). It is not used in Proposition 1.11.
4. The additive deletion at lines 759–762 cannot provide the asserted
   logarithmic time margin. F001 replaces it by
   \([y e^{L^{4/5}},y^\alpha e^{-L^{4/5}}]\), whose excluded logarithmic
   mass is \(O(L^{-1/5})\).
5. The unsigned lower comparison at lines 790–793 is replaced by an explicit
   negative error exponent; this proves that no passage occurred before the
   candidate split time.
6. Line 805 requires tuple length \(n-m_0\), and a fixed \(M\) requires the
   equality \(\operatorname{Aff}_{\vec a}(\mathbf N_y)=M\), not membership
   in \(E'\).
7. The two previous-iterate coefficients, the line 889 progression estimate,
   the nonuniform line 913 majorant, and the line 917 probability-space
   mismatch are repaired in the already sealed Proposition 5.2/\(c_n\)
   reconstruction.

During the first adversarial pass over the new chapter, the draft itself was
found to have the floor direction reversed in the descent exponent: the
coefficient \(\log3-1.9\log2\) is negative. It also contained four raw
carriage-return bytes and three lost TeX backslashes. Those defects were
repaired before admission. The correct floor estimate is recorded below.

## Exact modular input to Proposition 1.9

Put

\[
 L=\log x,\qquad
 n_0=\left\lfloor\frac{L}{10\log2}\right\rfloor,
 \qquad q=2^{3n_0},\qquad y_j=x^{\alpha^j}\quad(j=1,2).
\]

For real \(1\le A<B\), \(J=\log(B/A)\), and an odd residue \(r\pmod q\),
the direct progression estimate is

\[
 \left|\sum_{\substack{A\le N\le B\\N\equiv r\pmod q}}\frac1N
       -\frac Jq\right|\le\frac1A.
\]

This includes empty fibres and arbitrary real endpoints. Summing over the
\(q/2\) odd residues gives

\[
 \sum_{r\ {m odd}}|W_r-J/q|\le q/(2A),\qquad
 |H-J/2|\le q/(2A).
\]

The target uniform mass is \(2/q\), not \(1/q\). If \(AJ\ge2q\), Tao's
unhalved distance is therefore at most

\[
 \frac{2q}{AJ-q}\le\frac{4q}{AJ}.
\]

For \(A=y_j\), \(B=y_j^\alpha\), the retained floor gives

\[
 x^{3/10}/8\le q\le x^{3/10},
\]

and hence the last display is \(o(q^{-1})\), uniformly in \(j\). Proposition
1.9 applies with the exact parameters \(n=n_0\), \(n'=3n_0\), and
\(c_0=1\), yielding

\[
 d_{\rm TV}(\vec a^{(n_0)}(\mathbf N_{y_j}),
             \operatorname{Geom}(2)^{n_0})\ll x^{-c_2}.
\]

## Finite-time descent with the floor sign exposed

For iid \(G_i\sim\operatorname{Geom}(2)\), choosing
\(e^{-t}=18/19\) makes the Chernoff base
\(0.9(19/18)^{1.9}<1\). Thus the event
\(|\vec a^{(n_0)}|\le1.9n_0\) has probability \(O(x^{-c_3})\).
Outside it,

\[
 \operatorname{Syr}^{n_0}(\mathbf N_{y_j})
 \le3^{n_0}2^{-1.9n_0}x^{\alpha^3}+3^{n_0}.
\]

Set

\[
 \beta_1=\alpha^3+
   \frac{\log3-1.9\log2}{10\log2},\qquad
 \beta_2=\frac{\log3}{10\log2}.
\]

Exact rational atanh-series enclosures with indices \(0,\ldots,20\) prove
\(\beta_1<0.972\) and \(\beta_2<0.159\). Because the first coefficient is
negative, its floor estimate uses
\(n_0\ge L/(10\log2)-1\), giving the factor
\(e^{1.9\log2-\log3}x^{\beta_1}\). The positive second coefficient uses
\(n_0\le L/(10\log2)\), giving \(x^{\beta_2}\). Their sum is less than
\(x\) for sufficiently large \(x\), proving \(T_x\le n_0\) outside the
declared exceptional event.

## Exact affine inverse and morphism

Fix \(E\subseteq(2\mathbb N+1)\cap[1,x]\), let \(E'\) be the repaired
source set, take \(n\in I_y\cap\mathbb Z\), and put \(r=n-m_0\). For a
positive path-tube tuple \(\vec a=(a_1,\ldots,a_r)\), define

\[
 A_k=\sum_{i\le k}a_i,\quad A=A_r,\quad
 C_r(\vec a)=\sum_{i=1}^r3^{r-i}2^{A_{i-1}},\quad
 F_r(\vec a)=2^{-A}C_r(\vec a).
\]

The equation \(\operatorname{Aff}_{\vec a}(N)=M\) has the unique rational
solution

\[
 \Phi_r(\vec a,M)=\frac{2^AM-C_r(\vec a)}{3^r}
                  =2^A\frac{M-F_r(\vec a)}{3^r}.
\]

It is integral exactly when
\(M\equiv F_r(\vec a)\pmod{3^r}\) in
\(\mathbb Z[1/2]/3^r\mathbb Z[1/2]\). The numerator is odd; division by
the odd integer \(3^r\) preserves oddness. The path-tube and \(E'\) bounds
give

\[
 \log\Phi_r=L+n\log(4/3)+(A-2r)\log2+\eta+
              \log(1-F_r/M),
\]

where \(|A-2r|<L^{3/5}\), \(|\eta|\le L^{7/10}\), and
\(0\le F_r/M\le x^{-7/10}\). The \(L^{4/5}\) margins in \(I_y\) dominate
these errors, proving positivity and membership in \([y,y^\alpha]\).
The prefix lemma then recovers exactly \(\vec a\) and endpoint \(M\).

With every ambient parameter fixed, define

\[
 \mathcal X_{r,y,E,x}=\{N\in\mathcal R_y:
   \vec a^{(r)}(N)\in\mathcal A^{(r)},\ 
   \operatorname{Syr}^r(N)\in E'\}
\]

and

\[
 \mathcal D_{r,y,E,x}=\{(\vec a,M)\in\mathcal A^{(r)}\times E':
   M\equiv F_r(\vec a)\pmod{3^r}\}.
\]

Then

\[
 \Theta_{r,y,E,x}(N)=
 (\vec a^{(r)}(N),\operatorname{Syr}^r(N))
\]

is a bijection with inverse \(\Phi_r\). Both composites are identities,
every fibre is a singleton, the kernel pair is the diagonal, and no higher
binary coordinate is discarded. Its point mass is

\[
 \mathbb P(\operatorname{Aff}_{\vec a}(\mathbf N_y)=M)
 =\frac{1+O(x^{-c_4})}{((\alpha-1)/2)\log y}
   \frac{2^{-A}3^r}{M}.
\]

## Integer window, mixing, and exact collapse

For \(y_j=x^{\alpha^j}\), the closed real interval has the exact integer
count

\[
 \#(I_{y_j}\cap\mathbb Z)
 =\frac{\alpha-1}{\log(4/3)}\log y_j-2L^{4/5}+\varepsilon_j,
 \qquad -1<\varepsilon_j\le1.
\]

Consequently

\[
 \frac{\#(I_{y_j}\cap\mathbb Z)}{((\alpha-1)/2)\log y_j}
 =\frac2{\log(4/3)}-
   \frac4{(\alpha-1)\alpha^j}L^{-1/5}+O(L^{-1}).
\]

The leading term is independent of \(j\); the finite buffer correction is
not. Exact coefficient bounds, with floors retained, give
\(I_y\subseteq[2m_0,n_0]\), so \(r=n-m_0\ge m_0\) and Proposition 1.14
applies at levels \(m_0\le r\).

For fixed \(n,E\), the repaired event chain and affine bijection give

\[
 A_{n,E}=3^r\sum_{\vec a\in\mathcal A^{(r)}}2^{-|\vec a|}
  \sum_{\substack{M\in E'\\M\equiv F_r(\vec a)\ (3^r)}}\frac1M.
\]

The uniform \(c_n\) bound deletes the bad iid path tube. Proposition 1.14
then replaces the level-\(r\) offset law by the exact uniform lift of its
level-\(m_0\) projection. The finite pairing collapses exactly:

\[
 \sum_{X\bmod3^r}
 \left(3^r\sum_{\substack{M\in E'\\M\equiv X\ (3^r)}}\frac1M\right)
 3^{m_0-r}\mathbb P(\operatorname{Syrac}_{m_0}\equiv X\ (3^{m_0}))
 =Z_E,
\]

where

\[
 Z_E=\sum_{M\in E'}\frac{3^{m_0}}M
      \mathbb P(\operatorname{Syrac}_{m_0}\equiv M\pmod{3^{m_0}}).
\]

Thus \(A_{n,E}=Z_E+O(L^{-c_6})\), uniformly in the event, time, and both
choices of \(y\). The uniform \(c_n\) bound gives \(A_{n,E}=O(1)\), and
therefore \(Z_E=O(1)\) noncircularly. After the time sum and harmonic
normalization,

\[
 \mathbb P(\operatorname{Pass}_x(\mathbf N_y)\in E)
 =\frac2{\log(4/3)}Z_E+O(L^{-c}).
\]

This holds uniformly for every subset of the common state space. Taking the
difference, the supremum over events, and finally the source inequality
\(d_{\rm TV}\le2\sup_E|P(E)-Q(E)|\) proves the unhalved total-variation
claim.

## Reproducible finite certificate

`certificates/tao_prop111_transport_checks.py` is 39424 bytes with SHA-256
`70ca21065cb5af036044617250f5682d90ca223299918a32379feaef0f9dfc31`.
It passes and pins all five Tao manifestations plus all three frozen routing
artifacts. Its checked finite kernels include:

- 3 route-identity checks, 44 v7 source locators, 44 v5 source locators, 13
  reconstruction locators, and 5 explicit version-boundary checks;
- 6820 affine recurrence/offset identities;
- 1628712 affine inverse/congruence checks;
- 12276 positive odd inverse and valuation-prefix checks;
- 24522 singleton checks and 3 explicit fixed-\(M\) membership
  counterexample checks;
- 120444 constructive CRT checks;
- 182 uniform-lift/projection checks and 1086 ternary-fibre checks;
- 36408 suffix/projective offset checks;
- 72 exact weighted-collapse checks and 24 source lift-factor checks;
- 3381 valuation-partition checks;
- 66 one-coordinate and 60 tuple truncated-mass checks;
- 37 checks exposing the nonuniform square-root majorant;
- 128 exact parameter, logarithm, exponent, and interval-range checks.

The script explicitly does not certify the infinite harmonic-progression
estimate, Chernoff/path-tube estimate, endpoint asymptotics, analytic uniform
\(c_n\) bound, first-passage event chain, Proposition 1.9, Proposition 1.14,
Proposition 1.11, Theorem 1.6, or Theorem 1.3. Those analytic claims are
controlled by the primary sources and the displayed TeX proofs at their
separately recorded scopes.

## Adversarial audit and admission boundary

The first independent adversarial pass caught the reversed floor inequality
and the TeX control-character/backslash defects described above. After those
repairs, a second independent read-only audit checked the progression lemma,
TV convention, all floors and exponents, affine inverse, localized
integrality, positivity, range, bijection, count, event chain, uniform lift,
finite collapse, error summation, and arbitrary-event conversion. It reported
no remaining substantive mathematical issue. The final chapter is
`tex/chapters/01i_tao_first_passage_stabilisation.tex`, 20386 bytes, SHA-256
`ec16f1047928073682df1085f055ef5582a756c3b2cd2f3bef3169b6ba138ffd`,
with no embedded control bytes.

Proposition 1.11 is therefore admitted at exactly its printed v7 scope. The
next Tao gate is the separate implication from Proposition 1.11 to Theorem
1.6, followed by the implication from Theorem 1.6 to Theorem 1.3 and the
remaining whole-paper/version audit. No downstream theorem or global corpus
completion is claimed here.

## ACT31 reader seal

After the mathematical and adversarial audits, three fresh clean TeX passes
produced `tmp/tao_prop111_act31_20260828/main.pdf`: 99 pages, 1089943 bytes,
SHA-256
`a5bd834b97c760416e236ee35dbb048377788984ff6d51a732920028027f6c19`.
The final log has zero actionable diagnostics, all 25 reported font rows are
embedded and subset, and the placeholder and literal-control-leak scans are
empty.

All 99 pages were freshly rendered at 200 dpi and every one of the 13 contact
sheets was inspected. Pages 2, 88--94, 98, and 99 were additionally checked
at original render detail. Pages 1 and 3--87 are pixel-identical to the fully
inspected ACT30 render. The minimum detected content margins are 213, 215,
211, and 132 pixels at the left, top, right, and bottom respectively. No
clipping, overlap, malformed display, blank insertion, displaced folio, or
terminal-page fault was found. This is working-checkpoint QA, not final
release QA.
