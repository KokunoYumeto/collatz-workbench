# Tao arXiv v7 proof-text audit

Audit ID: `TAO-V7-F001`  
Status: open; exact source statement registered; Proposition 5.2 and Lemma 5.3 repaired and independently certified; the Section 5 reduction is checked through source line 925 conditional on fine-scale mixing; complete proof certification not yet granted  
Audited manifestation: `SRC-COL-000005`  
Version: `arXiv:1909.03562v7`  
Source TeX: `C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/latex/1909.03562v7/collatz.tex`  
Source TeX SHA-256: `bfbc39432d4084a276416cb019a592003c868fa32f18e2f90028ac325ae5c19d`  
Source archive SHA-256: `ba81acd6254838251f1ee585256a6f9f223cdc9c73bed0a3c4fd25782d0124ad`

## Audit boundary

This record distinguishes four things:

1. the exact statement of Theorem 1.3 in the current v7 source;
2. local typographical or indexing defects whose intended correction is forced by the surrounding typed expressions;
3. malformed proof text for which a local reconstruction is visible but must still be checked through every dependent line;
4. two genuine gaps in Section 5: the endpoint buffer in Proposition 5.2 and the non-uniform final summation in Lemma 5.3, together with independently proved repairs and a dependency check through the end of the section at source line 925.

Nothing below is a claim that Theorem 1.3 is false. The theorem remains registered as a sourced theorem with its proof-dependency certification open. No downstream local claim may enlarge its displayed conclusion.

## Exact theorem boundary

At source Section 1.1, Theorem 1.3 states: for every function (f:\mathbb N\to\mathbb R) with (f(N)\to+\infty), the minimum of the unshortened Collatz orbit is less than (f(N)) for a set of positive integers of logarithmic density one.

It does not assert natural density one, a universal constant bound, eventual arrival at (1), boundedness of every orbit, or exclusion of an unbounded orbit.

## Version-level corrections present in v7

- Lines 795--797 correctly type the first-passage time as (T_x) and the first-passage location as \(\operatorname{Pass}_x\). The time decomposition is
  \[
  T_x(\mathbf N_y)=n-m_0+T_x(\operatorname{Syr}^{n-m_0}(\mathbf N_y))=n,
  \]
  followed by the location identity
  \[
  \operatorname{Pass}_x(\mathbf N_y)
  =\operatorname{Pass}_x(\operatorname{Syr}^{n-m_0}(\mathbf N_y))\in E.
  \]
- The Section 6 Fourier transform and its high-frequency estimate use the same event (E_k\wedge B_k\wedge C_{k,l}); the older complement mismatch is absent in v7.
- Lemma 7.9 now states its exponential estimate with (1_{R\leq\mathbf r}) and (+\varepsilon R). This is a substantive revision, although malformed expressions persist in its proof and application.

## Persistent forced local corrections

These corrections are fixed by the surrounding definitions or dimensions. They are not new mathematical hypotheses.

| v7 locator | printed expression | forced correction | reason |
|---|---|---|---|
| line 460, Lemma 2.1 | `Aff_{a^(n)(N)} in 2N+1` | `Aff_{a^(n)(N)}(N) in 2N+1` | The affine map itself is not an odd integer; its value at (N) is. |
| line 469, Lemma 2.1 | `Syr^{N-1}(N)` | `Syr^{n-1}(N)` | The induction index is (n); line 467 has the correct iterate. |
| line 505, Lemma 2.2 | scalar (lambda) in the shifted Fourier exponent | vector (\vec\lambda) | The contour shift was defined as a vector and is paired with (\vec L). |
| line 516, Lemma 2.2 | Gaussian factor (n^{-1/2}) | (n^{-d/2}) | The integral is (d)-dimensional and the claimed bound at line 486 has exponent (d/2). |
| lines 633, 638, Proposition 1.9 | cutoff \(|\vec a|<m\) | \(|\vec a|<n'\) | No operative (m) occurs; lines 645--646 use (n'). |
| lines 651--652 | `Pass_x` described and compared as a time | (T_x(\mathbf N_y)\) | The right side is a real-valued time approximation; `Pass_x` is a location. |
| line 670, figure caption | `Syr^{n-m}` | `Syr^{n-m_0}` | The section's fixed backward step is (m_0). |
| line 689 | (1.9n) | (1.9n_0) | Lines 684, 690, and 693 use the (n_0)-step valuation. |
| line 805, Proposition 5.2 | tuple length (n-m) | tuple length (n-m_0) | The iterate and the set \(\mathcal A\) have length (n-m_0). |
| line 805, fixed (M) event | \(\operatorname{Aff}_{\vec a}(\mathbf N_y)\in E'\) | \(\operatorname{Aff}_{\vec a}(\mathbf N_y)=M\) | (M\in E') is fixed inside the inner sum; membership does not identify that summand. |
| line 868, Lemma 5.3 | coefficient \(3^{m_0}\) in the \((m_0-1)\)-st iterate | \(3^{m_0-1}\) | The exact iterate formula at time \(m_0-1\) has this coefficient; the following coarse \(\ll\)-bound remains valid. |
| line 899, Lemma 5.3 | coefficient \(3^{m_0}\) inside the last-step valuation | \(3^{m_0-1}\) | The valuation is taken after the \((m_0-1)\)-st iterate, so the same exact coefficient correction is forced. |
| line 889, Lemma 5.3 | `q^{-1} log O(M_1/M_0)` | \(q^{-1}(1+\log(M_1/M_0))\) | Lines 882--885 give this exact upper bound once (q\leq M_0); the printed expression is malformed. |
| line 1093 | tuple \((a_1,\ldots,a_m)\), mass (2^{-a_{[1,m]}}) | \((a_1,\ldots,a_{k+1})\), mass (2^{-a_{[1,k+1]}}=2^{-l}) | Lines 1065 and 1088 fix the prefix length and define (l). |

At lines 1311 and 1313, the comparison signs and the typed argument of \(\theta\) are missing. The intended Case 1 chain is
\[
 \varepsilon
 <\varepsilon e^{-s_*+(j'-j_*)\log 9+(l_*-l')\log 2}
 \leq \varepsilon^{1-(\log 9+\log 2)/10}<\tfrac12,
\]
and then
\[
 |\theta(j',l')|
 =\varepsilon e^{-s_*+(j'-j_*)\log 9+(l_*-l')\log 2}
 >\varepsilon.
\]
The inequalities follow directly from line 1309 after exponentiating and multiplying by \(\varepsilon\).

## Proposition 5.2 endpoint-buffer repair

Let
\[
 \lambda=\log(4/3),\qquad L=\log x,
\]
and retain the interval printed at lines 716--719,
\[
 I_y=
 \left[
 \frac{\log(y/x)}{\lambda}+L^{0.8},
 \frac{\log(y^\alpha/x)}{\lambda}-L^{0.8}
 \right].
\]
On the good valuation event, lines 754--757 establish
\[
 T_x(\mathbf N_y)
 =\frac{\log(\mathbf N_y/x)}{\lambda}+O(L^{0.6}).
\]
Line 759 instead restricts the scalar \(\mathbf N_y\) by an additive buffer
\[
 [y+2L^{0.8},\ y^\alpha-2L^{0.8}],
\]
and even types scalar membership as `\subset`. The additive displacement changes \(\log(\mathbf N_y/y)\) by only (O(L^{0.8}/y)), not by the required order (L^{0.8}). It therefore does not imply (T_x(\mathbf N_y)\in I_y).

### Exact local repair

Let (G_x) be the source event
\[
 G_x=\{\vec a^{(n_0)}(\mathbf N_y)\in\mathcal A^{(n_0)}\}.
\]
The constants implicit in lines 741--756 are absolute and uniform for the two allowed values (y=x^\alpha,x^{\alpha^2}).  Hence there is a fixed (K>0) such that, for all sufficiently large (x),
\[
 \left|T_x(\mathbf N_y)-\frac{\log(\mathbf N_y/x)}{\lambda}\right|
 \leq K L^{0.6}
 \quad\hbox{on }G_x.
\]
Here the first-passage time is finite on (G_x): at time (n_0), the upper bound (\mathbf N_y\leq x^{\alpha^3}) and line 750 give
\[
 \log\frac{\operatorname{Syr}^{n_0}(\mathbf N_y)}x
 \leq (\alpha^3-1)L-\lambda n_0+O(L^{0.6})<0
\]
for large (x).  The last strict inequality is quantitative: (\alpha^3-1<1/300), while
(\lambda/(10\log2)>1/40), using (\log(4/3)>1/4) and (\log2<1).  Applying line 750 at the first passage time and at the preceding time gives the displayed two-sided time bound, with the one-step error absorbed into (K L^{0.6}).

Take the fixed constant (C=1).  Since (\lambda=\log(4/3)<1), one has
(C/\lambda-1>0).  For all sufficiently large (x), the multiplicative restriction
\[
 \mathbf N_y\in
 \left[
 y\exp(L^{0.8}),
 y^\alpha\exp(-L^{0.8})
 \right]
\]
implies
\[
 \frac{\log(\mathbf N_y/x)}{\lambda}-K L^{0.6}
 \geq \frac{\log(y/x)}{\lambda}+L^{0.8}
\]
and
\[
 \frac{\log(\mathbf N_y/x)}{\lambda}+K L^{0.6}
 \leq \frac{\log(y^\alpha/x)}{\lambda}-L^{0.8}.
\]
Indeed, each endpoint gains the positive margin
((1/\lambda-1)L^{0.8}), which dominates (K L^{0.6}) because
(L^{0.8}/L^{0.6}=L^{0.2}\to\infty).

Under the logarithmic distribution on odd integers in \([y,y^\alpha]\), the discarded logarithmic length is at most (2CL^{0.8}+O(1/y)), while the total logarithmic length is
\[
 \log(y^\alpha/y)=(\alpha-1)\log y\asymp L.
\]
The retained interval is nonempty for large (x), because its logarithmic width is
((\alpha-1)\log y-2L^{0.8}) and (\log y\asymp L).  Applying the odd-integer harmonic-sum integral estimate separately to the two discarded intervals gives excluded probability (O(L^{-0.2})).  Together with line 737, this proves
\[
 \mathbb P(T_x(\mathbf N_y)\in I_y)=1-O(L^{-1/5})
\]
uniformly for (y=x^\alpha,x^{\alpha^2}).  Thus line 762 holds with the explicit local choice (c=1/5).

### Downstream dependency check through line 925

The replacement is used only to prove line 762.  Lines 766--805 use the unchanged interval (I_y) and the high-probability statement at line 762; they never use either the printed additive restriction or the replacement multiplicative restriction.  Lines 808--840 reconstruct the unique possible input from (n,\vec a,M).  Their use of (n\in I_y) at lines 816--820 has a margin (L^{0.8}) against an (O(L^{0.7})) reconstruction error and is unchanged.  The count of integer times in (I_y) at lines 841--845 is likewise unchanged.  Lines 847--925 depend on (I_y), (\mathcal A^{(n-m_0)}), and the assumed fine-scale-mixing proposition, not on the discarded input endpoints.

One separate lower-bound line in this same dependency path requires reconstruction.  Lines 790--793 use an unsigned factor (\exp(O(L^{0.6}))) as though it supplied a lower bound.  On (G_x), line 750 instead gives, for (0\leq n'\leq n-m_0),
\[
 \operatorname{Syr}^{n'}(\mathbf N_y)
 \geq e^{-2K_1L^{0.6}}(4/3)^{n-m_0-n'}
       \operatorname{Syr}^{n-m_0}(\mathbf N_y)
 \geq e^{-2K_1L^{0.6}-L^{0.7}}(4/3)^{m_0}x>x
\]
for a fixed absolute (K_1) and all sufficiently large (x), using the lower endpoint in line 722 and (m_0=\lfloor(\alpha-1)L/100\rfloor).  This is the exact lower bound needed at line 793.  At line 889, lines 882--885 give
\[
 \sum_{\substack{M_0\leq M\leq M_1\\M\equiv a\pmod q}}\frac1M
 \leq \frac1q\left(1+\log\frac{M_1}{M_0}\right)
 \qquad(q\leq M_0),
\]
which replaces the malformed printed expression and gives the bound used at lines 894--897.

These checks close the endpoint-buffer branch.  The next subsection audits the
remaining event and uniformity steps before assigning a status to Proposition
5.2 or Lemma 5.3.  The fine-scale-mixing, Fourier-decay, renewal, and main
theorem branches remain separate obligations throughout.

## Proposition 5.2 event chain and Lemma 5.3 uniformity repair

The event chain at source lines 766--803 is valid after the endpoint and
signed-lower-bound repairs above.  Put \(L=\log x\), let
\(G_x=\{\vec a^{(n_0)}(\mathbf N_y)\in\mathcal A^{(n_0)}\}\), and fix
\(n\in I_y\).  If
\(T_x(\operatorname{Syr}^{n-m_0}(\mathbf N_y))=m_0\), then time \(n\)
is a crossing:
\[
 \operatorname{Syr}^n(\mathbf N_y)\leq x
 <\operatorname{Syr}^{n-1}(\mathbf N_y).
\]
The same good-orbit estimate that proves the first-passage approximation
places both this crossing time and the actual first-passage time within
\(O(L^{0.6})\) of
\(\log(\mathbf N_y/x)/\log(4/3)\).  Since
\(m_0=\lfloor L/100000\rfloor\), one has
\(T_x(\mathbf N_y)\geq n-m_0\) for large \(x\).  The semigroup identity
then gives
\[
 T_x(\mathbf N_y)=n-m_0+
 T_x(\operatorname{Syr}^{n-m_0}(\mathbf N_y))=n.
\]

Conversely, if
\(M=\operatorname{Syr}^{n-m_0}(\mathbf N_y)\in E'\) and \(G_x\) holds,
the signed comparison already displayed gives, for every
\(0\leq j\leq n-m_0\),
\[
 \operatorname{Syr}^j(\mathbf N_y)
 \geq e^{-2K L^{0.6}}(4/3)^{n-m_0-j}M.
\]
Using the lower endpoint
\(M\geq e^{-L^{0.7}}(4/3)^{m_0}x\), even the \(j=n-m_0\) bound is
strictly larger than \(x\) for large \(x\).  Hence there was no earlier
passage, and the event equality at line 800 follows.  Replacing
\(G_x\) by its prefix event of length \(n-m_0\) changes each probability by
at most \(O(L^{-10})\); since \(\#(I_y\cap\mathbb Z)=O(L)\), the summed
change is still negligible.  At line 805, for fixed \(\vec a,M\), the exact
equivalence is with \(\operatorname{Aff}_{\vec a}(\mathbf N_y)=M\), not
membership in \(E'\).  This closes Proposition 5.2 after the forced
\(n-m_0\) index corrections.

The printed proof of Lemma 5.3 has a separate genuine gap.  Write
\[
 m=m_0,\qquad A=a_1+\cdots+a_m,\qquad b=a_m.
\]
The final displayed majorant at lines 913--914 is not uniformly bounded:
over positive valuation coordinates it equals
\[
 \sum_{a_1,\ldots,a_m\geq1}2^{-A/2}
 =\left(\sum_{a\geq1}2^{-a/2}\right)^m
 =(1+\sqrt2)^m.
\]
Because \(m=\lfloor L/100000\rfloor\), this grows as a positive power of
\(x\), however small; it is not an absolute implied constant and cannot be
absorbed by the later polylogarithmic mixing estimate.

The estimates immediately before the invalid weakening contain the repair.
After restricting lines 862 and 865 to the actual positive valuation domain
\((\mathbb N+1)^m\), they give uniformly in \(X\)
\[
 c_{n,\vec a}(X)\ll b2^{-A}
 \quad(2^A\leq x^{1/2})
\]
and
\[
 c_{n,\vec a}(X)\ll3^n2^{-A}+b2^{-A}
 \quad(2^A>x^{1/2}).
\]
The exact \((m-1)\)-st iterate in line 868 has coefficient
\(3^{m-1}\), not \(3^m\); its lower bound on \(M\) is stronger than the
coarse bound used next, so the displayed estimates survive this correction.
Summing the \(b\)-term gives exactly
\[
 \sum_{a_1,\ldots,a_m\geq1}b2^{-A}
 =\left(\sum_{a\geq1}2^{-a}\right)^{m-1}
   \sum_{b\geq1}b2^{-b}=2.
\]
On the high-\(A\) branch, \(2^A>x^{1/2}\) implies
\[
 \sum_{2^A>x^{1/2}}2^{-A}
 \leq x^{-1/4}
      \sum_{a_1,\ldots,a_m\geq1}2^{-A/2}
 =x^{-1/4}(1+\sqrt2)^m.
\]
Now \(n\leq n_0\), \(3^5<2^8\), and \(1+\sqrt2<e\), so
\[
 3^n x^{-1/4}(1+\sqrt2)^m
 \leq x^{4/25-1/4+1/100000}
 =x^{-8999/100000}.
\]
Consequently \(c_n(X)\ll2+O(x^{-8999/100000})\ll1\) with an absolute
constant, proving the source lemma at its stated uniform scope.

At line 917, the citation to line 737 alone is not typed for the iid
\(\operatorname{Geom}(2)\) tuple in line 852: line 737 concerns the actual
valuation tuple.  The required estimate follows either directly from the
same Chernoff bound or by combining the total-variation estimate at line 680
with line 737.  With this correction and the repaired uniform bound, source
lines 921--924 apply Proposition 1.14 at levels \(n-m_0\) and \(m_0\)
correctly.  Projection consistency changes the distribution to
\[
 3^{2m_0-n}\,
 \mathbb P(\operatorname{Syrac}(\mathbb Z/3^{m_0}\mathbb Z)
              =X\bmod3^{m_0}),
\]
because source line 355 gives
\(\operatorname{Syrac}(\mathbb Z/3^{n-m_0}\mathbb Z)\bmod3^{m_0}
\equiv\operatorname{Syrac}(\mathbb Z/3^{m_0}\mathbb Z)\) in law.
Substitution of the definition of \(c_n\) then collapses the sum exactly to
the displayed \(Z\).  Thus the internal Section 5 deduction is certified
through line 925 conditional on the still-open fine-scale-mixing proposition.

One separate defect occurs in the nonperiodicity remark: line 699 writes a
period minus the random time, which can be negative.  If \(p(M)\) is the
least positive period, the correct nonnegative exponent is the representative
of \(-\mathbf m\pmod{p(M)}\), or equivalently one may first choose a positive
multiple of \(p(M)\) at least \(\mathbf m\).  The counting conclusion is
unchanged because \((M,\mathbf m)\) still determines \(\mathbf N_y\).

The deterministic certificate
`certificates/tao_v7_prop52_cn_checks.py` pins the source and frozen routes,
checks twelve source locators, verifies the exact exponent
\(-8999/100000\), the one-coordinate masses \(1\) and \(2\), and 228 bounded
positive-composition identities.

## Lemma 7.9 malformed proof text and restricted Markov event

- Line 1676 contains a malformed recursive call. The typed recursive factor is
  \[
  Z\bigl((j',l')+\mathbf v_{[1,\mathbf k_1]},R-1\bigr),
  \]
  not a call with (1_W) inside the spatial argument.
- Lines 1829, 1832, and 1836 omit the closing parenthesis in the (1_W)-sum.
- Lines 1830--1834 define (F_*) without the event \(\{R\leq\mathbf r\}\), but the expectation at line 1829 is indicator-weighted. Markov's inequality directly bounds only
  \[
  F_*^{\mathrm{typed}}
  =\{R\leq\mathbf r\}\cap
  \left\{
  \exp\left(
  -\sum_{p=1}^{\mathbf t_R}
   1_W((j,l)+\mathbf v_{[1,\mathbf k+p]})
  +\varepsilon R
  \right)>10^{A+2}e^\varepsilon
  \right\}.
  \]
  This restricted event is sufficient for the immediately following argument because line 1835 assumes \(\mathbf r\geq R\). A full certification must nevertheless recheck the induction defining (Z) and every dependent use.

## Numbering and dependency corrections

- The main result is Theorem 1.3.
- The approximate formula is Proposition 5.2.
- Prefix-offset injectivity is Lemma 6.2 and its separation consequence is Corollary 6.3.
- Lemma 7.7 is the first-passage-location distribution lemma and is syntactically intact in the inspected passage.
- The malformed recursive expression is in Lemma 7.9.
- The environment with internal label `77` compiles as Lemma 7.10.

## Open closure checks

`PO-COL-000001` remains open until all of the following have been completed and propagated:

- retain the proved endpoint-buffer replacement, the event-chain corrections, and the repaired uniform \(c_n\) estimate; Proposition 5.2 and Lemma 5.3 are closed at this scope, while the Section 5 conclusion remains conditional on fine-scale mixing;
- reconstruct Lemma 7.9's recursion and Markov event as fully typed formulas and verify every downstream use;
- audit the Fourier-decay and renewal dependency chain at content level, not by labels or summaries;
- rebuild the source or a faithful patched audit copy and confirm that no malformed expression has been silently interpreted by TeX in a different way;
- keep the theorem's exact sourced conclusion separate from the status of this independent proof certification.

## Closure-status addendum through F025

The list immediately above records the state at the original F001 pass.  It is
not the current gate.  F024 subsequently reconstructed and adversarially
audited the exact Fourier, black-triangle, first-passage Green, weaker-v7
Lemma~7.9, parameterized large-triangle, renewal, and Proposition~1.14 branch;
the stronger v5/journal Lemma~7.9 remains separately uncertified.  F025 then
reconstructed Proposition~1.9 with the corrected \(2^{n'}\) residue space,
first-crossing endpoints, \(n'\) truncation, empty-prefix and \(n=0\)
endpoints, exact residue fibres, explicit split-surjection map, both tail
bounds, and accumulated interior error.  Its finite certificate and
independent adversarial audit pass at their declared scopes.

Accordingly `PO-COL-000001` remains open at the next, narrower boundary: the
exact use of Propositions~1.14 and~1.9 in Proposition~1.11, followed by the
dependency chain through Theorems~1.6 and~1.3, remaining-source/version audit,
whole-paper adversarial audit, package validation, and final recovery.  F024
and F025 must not be reopened absent contrary mathematical evidence.
