# Krasikov--Lagarias 2003 F029 — difference-inequality and clock audit

## Scope and authority

This record reconstructs the objects, hypotheses, proof dependency chain,
computer-assisted premise, theorem scope, source defects, and exact clock
transport in Ilia Krasikov and Jeffrey C. Lagarias, “Bounds for the \(3x+1\)
problem using difference inequalities,” *Acta Arithmetica* 109 (2003), no. 3,
237--258, DOI 10.4064/aa109-3-4.  The published paper is the controlling
mathematical manifestation.  The arXiv v1 source is used for exact source-line
locators and for identifying differences that the journal corrected; it is
not silently identified with the journal.

The admitted local manifestations are:

- published PDF:
  C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/published/Krasikov-Lagarias-2003-Bounds-difference-inequalities.pdf,
  217588 bytes, 22 physical pages, SHA-256
  8433f68c6f04a008b7c1af4d2b11ee1007a74f987da56a658d8fa331b32eff9c;
- arXiv source archive math/0205002v1:
  C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/source/math.0205002v1.eprint,
  26236 bytes, SHA-256
  c35de018067ae838c17b647f0ce0354141a8bcfaa45b4966be2bb9a380252951;
- extracted arXiv TeX:
  C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/latex/math.0205002v1/30apr02.tex,
  69729 bytes, 1900 lines, SHA-256
  04fa4d484fe89256f6771f5651338891219385f6e049ffaf41035541016232cd.

The source is dated 30 April 2002.  The journal record gives receipt on 7 May
2002 and revision on 12 September 2002.  The paper's entire 22-page published
manifestation and the complete source TeX were read.  Rendered original-detail
checks included journal pp. 239, 245, 252, 253, and 254, where the decisive
definitions, sign defect, inductive close, main-theorem deduction, and
computer-assisted theorem occur.

This audit does **not** reconstruct the unprinted \(k=11\) feasible vector,
certify its feasibility, prove the Collatz conjecture, prove density one,
or promote the displayed numerical optimum to a theorem stronger than the
paper's stated exponent.  It preserves the published theorem as a sourced
result while recording the exact reproducibility boundary.

No Lean or Lake command was started.  The global single-worker, watched,
sub-3-GiB rule remained satisfied.

## The source map and counting functions

Krasikov--Lagarias use the shortened map

\[
 T(n)=
 \begin{cases}
  n/2,&2\mid n,\\
  (3n+1)/2,&2\nmid n,
 \end{cases}
 \qquad T:\mathbb Z_{>0}\longrightarrow\mathbb Z_{>0}.
\]

This is exactly the map already denoted \(T\) in the reconstruction; no
normalization or change of state space is being made.  For a fixed positive
target \(a\not\equiv0\pmod3\), journal p. 239 and source lines 368--378 define

\[
 \pi_a(x)=\#\{n\in\mathbb Z_{>0}:1\le n\le x,
                  \ \exists j\in\mathbb Z_{\ge0},\ T^j(n)=a\},
\]

and the path-restricted count

\[
 \pi_a^*(x)=\#\{n\in\mathbb Z_{>0}:n\le x,
   \ \exists j\ge0,\ T^j(n)=a,
   \ T^i(n)\le x\text{ for every }0\le i\le j\}.
\]

The inclusion of the second set in the first proves
\(\pi_a^*(x)\le\pi_a(x)\).  The index \(j=0\) is allowed: \(n=a\) is counted
when \(a\le x\).  This supplies the positivity used below.

For \(k\ge2\), a residue \(m\bmod3^k\) not divisible by \(3\), and \(y\ge0\),
the intended auxiliary function is

\[
 \phi_k^m(y)=
 \inf_{\substack{a\equiv m\pmod{3^k}\\
                  a\text{ is not contained in a finite }T\text{-cycle}}}
       \pi_a^*(2^y a).
\]

The journal and arXiv source print \(3^j\) in the congruence inside this
infimum, but \(j\) is unbound there.  The preceding declaration fixes a
class modulo \(3^k\), the following well-definedness sentence again uses
\(3^k\), and property (P3) requires the three lifts modulo \(3^k\).  Thus
\(3^k\) is the uniquely typed repair; the printed \(3^j\) is not retained as
an alternative definition.

The paper records three properties:

1. positivity: \(\phi_k^m(y)\ge1\) for \(y\ge0\);
2. monotonicity: \(y\mapsto\phi_k^m(y)\) is nondecreasing;
3. three-lift minimization:
   \[
    \phi_{k-1}^m(y)=\min\bigl(
      \phi_k^m(y),
      \phi_k^{m+3^{k-1}}(y),
      \phi_k^{m+2\cdot3^{k-1}}(y)\bigr).
   \]

It also gives, for \(m\equiv1\pmod3\) and real \(y\ge1\),

\[
 \phi_k^m(y)=\phi_k^{2m}(y-1).
\]

The displayed conclusion immediately afterward says it suffices to study
\(\phi_k^m(y)\) for **\(y\equiv2\pmod3\)**.  The congruence is ill-typed:
\(y\) is a real time parameter.  Equation (2.1) and the next definition force
the repair **\(m\equiv2\pmod3\)**.  The paper then sets

\[
 [3^k]=\{m\bmod3^k:m\equiv2\pmod3\}.
\]

This second printed defect is independent of the unbound-\(j\) defect.

## Krasikov inequalities and the nonlinear linear-program family

Put \(\alpha=\log_2 3\).  Proposition 2.1, journal pp. 239--240 and source
lines 426--453, states that for \(y\ge2\) the functions indexed by
\([3^k]\) satisfy

\[
\begin{array}{ll}
\text{(D1)}&
 \phi_k^m(y)\ge \phi_k^{4m}(y-2)
 +\phi_{k-1}^{(4m-2)/3}(y+\alpha-2),
 \quad m\equiv2\pmod9,\\[3pt]
\text{(D2)}&
 \phi_k^m(y)\ge \phi_k^{4m}(y-2),
 \quad m\equiv5\pmod9,\\[3pt]
\text{(D3)}&
 \phi_k^m(y)\ge \phi_k^{4m}(y-2)
 +\phi_{k-1}^{(2m-1)/3}(y+\alpha-1),
 \quad m\equiv8\pmod9.
\end{array}
\]

Here \(4m\) is read modulo \(3^k\) and each lower-level function is expanded
by the three-lift minimum above.  A term \(\phi_k^{m'}(y+\beta)\) is called
advanced when \(\beta\ge0\) and retarded when \(\beta<0\).

For \(1\le\lambda\le2\), the paper's family
\(L_k^{NT}(\lambda)\) has principal variables
\(c_k^m\) for \(m\in[3^k]\), auxiliary variables
\(c_{k-1}^m\) for \(m\in[3^{k-1}]\), and objective variable
\(C_k^{\max}\).  Its constraints are

\[
 1\le c_k^m\le C_k^{\max},
\]

\[
\begin{array}{ll}
 c_k^m\le c_k^{4m}\lambda^{-2}
  +c_{k-1}^{(4m-2)/3}\lambda^{\alpha-2},
   &m\equiv2\pmod9,\\[2pt]
 c_k^m\le c_k^{4m}\lambda^{-2},
   &m\equiv5\pmod9,\\[2pt]
 c_k^m\le c_k^{4m}\lambda^{-2}
  +c_{k-1}^{(2m-1)/3}\lambda^{\alpha-1},
   &m\equiv8\pmod9,
\end{array}
\]

and, for \(m\in[3^{k-1}]\),

\[
 c_{k-1}^m\le c_k^m,
 \qquad
 c_{k-1}^m\le c_k^{m+3^{k-1}},
 \qquad
 c_{k-1}^m\le c_k^{m+2\cdot3^{k-1}}.
\]

The journal prints these last two lifts correctly.  ArXiv source lines
532--534 instead print \(m+3^k\) and \(m+2\cdot3^k\); source lines 559--560
return to the correctly typed \(3^{k-1}\).  This is a preprint-only
manifestation defect corrected in publication, not an ambiguity in the
admitted system.  The source's following reference to “(D4)” is likewise
printed as “(L4)” in the journal.

## Exact proof dependency chain

The paper's proof does not infer the theorem directly from the advanced
system.  Its dependency chain is:

1. **Finite elimination.**  Theorem 3.1 (journal pp. 244--245; source
   lines 794--858) recursively substitutes advanced leaves, deletes a leaf
   when an earlier node on the same root path has the same residue and no
   larger shift, and proves that the procedure halts at a unique retarded
   inequality \(I_k^m(EL)\), independently of splitting order.

2. **Preservation of positive monotone solutions.**  Theorem 3.2 (journal
   pp. 245--248; source lines 860 onward) forms the system
   \(\mathcal I_k(EL)\) and proves that every strictly positive,
   nondecreasing solution of the original Krasikov inequalities is still a
   solution after the substitutions and deletion steps.

3. **Transport of feasibility.**  Theorem 4.1 (journal p. 250; source
   lines 1201--1208 and proof thereafter) proves that a feasible solution of
   \(L_k^{NT}(\lambda)\) induces a positive feasible solution of the linear
   program \(L_k^{EL}(\lambda)\) attached to the retarded system, with the
   same \(\lambda\) and the same principal variables.

4. **Retarded-system induction.**  Theorem 5.1 (journal pp. 251--253;
   source lines 1335--1438) considers any positive, nondecreasing family
   satisfying a retarded tree system.  If its associated linear program has
   a positive feasible solution, then
   \[
    \phi_k^m(y)\ge \Delta c_k^m\lambda^y\qquad(y\ge0),
   \]
   where
   \[
    \Delta=\lambda^{-\nu}
       \frac{\min_m\phi_k^m(0)}{\max_m c_k^m}
   \]
   and \(\nu\) is the largest backward time shift.  The proof first covers
   \([0,\nu]\), then advances through intervals of width
   \(\mu\), the smallest positive backward shift.  Addition and minimum are
   monotone in every argument, so the induction hypotheses may be
   substituted leaf by leaf; the feasible linear-program inequalities are
   then applied from innermost minima outward to the root.

5. **Theorem 2.2.**  Combining the preceding steps, using
   \(\phi_k^m(0)\ge1\), \(\lambda\le2\), and \(\nu\le2\), gives
   \[
    \phi_k^m(y)\ge
    \frac{c_k^m}{4\max_r c_k^r}\lambda^y
    \qquad(m\in[3^k],\ y\ge0).
   \]
   Theorem 5.1 is stated for \(\lambda>1\), while Theorem 2.2 includes
   \(\lambda=1\).  At that endpoint the displayed conclusion follows
   directly from \(\phi_k^m(y)\ge1\) and
   \(c_k^m/(4\max_r c_k^r)\le1/4\).  This supplies the endpoint case without
   enlarging the theorem.

The dependency is therefore

\[
 \mathcal I_k
 \xrightarrow{\text{finite substitution/deletion}}
 \mathcal I_k(EL)
 \xrightarrow{\text{LP feasibility transport}}
 L_k^{EL}(\lambda)
 \xrightarrow{\text{retarded-time induction}}
 \phi_k^m(y)\gg\lambda^y.
\]

The arrows are proof dependencies, not identities of the systems.  The first
changes the displayed inequalities while preserving the relevant solution
class; the second preserves \(\lambda\) and the principal coordinates but
adds auxiliary coordinates; the last evaluates a feasible coordinate vector
as an exponential subsolution.

## Proof-text defects in the dependency chain

The controlling published manifestation contains the following local defects.
Each repair is forced by the immediately adjacent typed statement and proof;
none is used to enlarge the theorem.

| Published locator | Printed text | Forced repair | Reason |
|---|---|---|---|
| p. 239, definition of \(\phi_k^m\) | \(a\equiv m\pmod{3^j}\) | \(a\equiv m\pmod{3^k}\) | \(j\) is unbound; the declared residue class, well-definedness sentence, and three-lift formula all use \(k\). |
| p. 239, after (2.1) | study the functions for \(y\equiv2\pmod3\) | study residues \(m\equiv2\pmod3\) | \(y\in\mathbb R_{\ge0}\); the next line defines \([3^k]\) by the congruence on \(m\). |
| p. 245, proof of Theorem 3.1 | \(\delta=\beta_2-\beta_1>0\) | \(\delta<0\) | (3.2) has \(\beta_1>\beta_2>\cdots\); only a negative common difference implies eventual negativity and the printed contradiction. |
| p. 253, close of Theorem 5.1 | “for all \(k\in[3^m]\)” | “for all \(m\in[3^k]\)” | the induction fixes \(k\) and proves (5.1) for every residue \(m\) in its index set. |
| p. 253, equation (5.7) | \(\Delta c_m^k\lambda^y\) | \(\Delta c_k^m\lambda^y\) | the paper's principal variables and (5.1), (5.2), and (5.8) all use lower level \(k\), upper residue \(m\). |
| p. 254, Theorem 6.1 set | \(T^{(j}(n)\) | \(T^{(j)}(n)\), equivalently \(T^j(n)\) | missing closing parenthesis only. |

The arXiv source has two additional defects corrected in the journal: its
(L4) lift exponents are \(3^k\) rather than \(3^{k-1}\), and its initial
interval in the proof of Theorem 5.1 ends at an unrelated tree-vertex macro
instead of \(\nu\).  Conversely, the five journal defects in the table are
not silently excused merely because the intended formulas are recoverable.

## The published \(0.84\) theorem and its computational premise

Theorem 6.1, journal p. 254, states:

> For every fixed positive integer \(a\not\equiv0\pmod3\), there is a
> threshold \(x_0(a)\) such that
> \(\pi_a(x)\ge x^{0.84}\) for every \(x\ge x_0(a)\).

The exponent in the theorem is exactly

\[
 0.84=\frac{21}{25}.
\]

The proof cites a computer-found positive feasible solution to
\(L_{11}^{NT}(\lambda)\) at

\[
 \lambda=1.7922310.
\]

The journal table displays fewer decimals, but the paragraph immediately
above it says that every listed value is rounded downward in its last shown
decimal and that the computation used greater precision.  The arXiv table
records the \(k=11\) row

\[
 \gamma_{11}=0.8417560,
 \quad \lambda_{11}=1.7922310,
 \quad C_{11}^{\max}=98.4009647,
\]

whereas the published proof itself retains the seven-decimal value of
\(\lambda\).  No equality between the rounded table row and an exact optimum
is asserted.

The numerical sacrifice from the reported \(\lambda\) to the theorem's
\(21/25\) exponent has an exact integer certificate:

\[
 1.7922310^{25}>2^{21}
 \quad\Longleftrightarrow\quad
 1792231^{25}>2^{21}10^{150}.
\]

The difference is

\[
\begin{split}
1792231^{25}-2^{21}10^{150}
={}&64817808301881841171464200817066393781435854267877028218361650186559810536587510128279494684120172553258022825617035667743037735765387257538455190506275751,
\end{split}
\]

which is positive.  Therefore
\(\log_2(1.7922310)>21/25\).  This exact comparison does **not** certify that
the reported \(k=11\) coordinate vector exists or is feasible.

The paper prints neither the \(k=11\) vector nor executable code, an exact
rational certificate, or enough coordinates to reconstruct one.  Its
appendix writes the system only for \(k=2\).  Accordingly:

- Theorem 6.1 is recorded as a published computer-assisted theorem.
- The comparison \(\log_2(1.7922310)>0.84\) is independently certified.
- Reproducibility of the \(k=11\) feasibility premise remains open.
- The corpus does not claim an independent reproof of Theorem 6.1.

## Explicit transfer from \(\phi\) to every permitted target

The printed proof of Theorem 6.1 says only that the result follows from
Theorem 2.2 and the \(k=11\) feasible solution.  Two target cases are hidden
by that compression.

For a noncyclic target \(a\equiv2\pmod3\), choose the residue
\(m=a\pmod{3^{11}}\).  For \(x\ge a\), put \(y=\log_2(x/a)\).  Then

\[
 \pi_a(x)\ge\pi_a^*(x)
 \ge\phi_{11}^{m}(y)
 \ge \Delta_1c_{11}^{m}\lambda^y
 =\Delta_1c_{11}^{m}a^{-\gamma}x^\gamma,
 \qquad\gamma=\log_2\lambda.
\]

For a noncyclic target \(a\equiv1\pmod3\), equation (2.1) moves to the
typed residue \(2a\equiv2\pmod3\) and shifts the real time by one.  Thus the
same calculation has a further fixed factor \(\lambda^{-1}\).  In both cases
the positive \(a\)-dependent prefactor is absorbed by increasing \(x_0(a)\),
because \(\gamma>21/25\).

The definition of \(\phi_k^m\) excludes targets lying on a finite cycle,
whereas Theorem 6.1 quantifies over every positive \(a\not\equiv0\pmod3\).
For such a cyclic target, let \(M\) be the maximum value on its finite
\(T\)-cycle and choose \(r\ge1\) with \(b=2^ra>M\).  Then

\[
 T^r(b)=a.
\]

If \(b\) were on a finite \(T\)-cycle, its forward orbit would contain \(a\),
so \(b\) would lie on the same cycle as \(a\), contradicting \(b>M\).
Therefore \(b\) is an admissible noncyclic target.  Every \(n\) counted by
\(\pi_b(x)\) is counted by \(\pi_a(x)\), since an orbit reaching \(b\) reaches
\(a\) after \(r\) additional steps.  Hence

\[
 \pi_a(x)\ge\pi_b(x)\ge x^{0.84}
\]

for \(x\ge x_0(b)\).  This supplies the omitted cycle-target handoff at its
exact scope.  It does not assume the Collatz conjecture or classify any
unknown cycle.

## Exact shortened/unshortened clock morphism

Let \(U\) denote Tao's unshortened Collatz map:

\[
 U(n)=
 \begin{cases}
  n/2,&2\mid n,\\
  3n+1,&2\nmid n.
 \end{cases}
\]

For every positive \(n\),

\[
 T(n)=
 \begin{cases}
  U(n),&2\mid n,\\
  U^2(n),&2\nmid n.
 \end{cases}
\]

Fix \(N\in\mathbb Z_{>0}\), put \(n_j=T^j(N)\), and define the clock
embedding \(\iota_N:\mathbb Z_{\ge0}\to\mathbb Z_{\ge0}\) by

\[
 s_0=0,
 \qquad
 s_{j+1}=s_j+
 \begin{cases}
  1,&2\mid n_j,\\
  2,&2\nmid n_j,
 \end{cases}
 \qquad
 \iota_N(j)=s_j.
\]

Induction on \(j\) gives

\[
 U^{\iota_N(j)}(N)=T^j(N).
\]

Every increment is positive, so \(\iota_N\) is strictly increasing and
injective.  Its image consists of the unshortened times at which a shortened
state is observed.  The complement of its image consists exactly of the
single intermediate time \(s_j+1\) for each odd \(n_j\), and

\[
 U^{s_j+1}(N)=3n_j+1\ge4.
\]

Thus the morphism has singleton fibres on its image, diagonal kernel pair,
and no ambiguity in reconstructing \(j\) from an image time.  It does lose
the displayed intermediate state after an odd input; that information loss
is explicit.  Because every omitted value is at least \(4\), it cannot lose
an occurrence of the target \(1\).  Consequently

\[
 (\exists j\ge0,\ T^j(N)=1)
 \quad\Longleftrightarrow\quad
 (\exists r\ge0,\ U^r(N)=1).
\]

All unshortened orbit values are positive integers, so Tao's orbit minimum
\(\operatorname{Col}_{\min}(N)=\min_{r\ge0}U^r(N)\) equals \(1\) exactly when
the unshortened orbit reaches \(1\).  Therefore, for every real \(x\ge1\),

\[
 \{N\in\mathbb Z_{>0}:N\le x,
   \operatorname{Col}_{\min}(N)=1\}
 =
 \{N\in\mathbb Z_{>0}:N\le x,
   \exists j\ge0,\ T^j(N)=1\},
\]

and the cardinality of either set is exactly \(\pi_1(x)\).  Tao's use of the
Krasikov--Lagarias exponent is therefore an exact transport, not a heuristic
comparison of two differently clocked maps.

## Nonclaims and remaining obligations

The paper and this reconstruction do not establish any of the following:

- the Collatz conjecture;
- positive natural density, density one, or “almost all” convergence from the
  exponent \(0.84\), since \(x^{0.84}/x\to0\);
- a threshold uniform in the target \(a\);
- the theorem for targets divisible by \(3\);
- independent feasibility of the unprinted \(k=11\) coordinate vector;
- a theorem with exponent \(0.8417560\) or with the rounded table value as an
  exact optimum;
- strict increase of the optimal \(\lambda_k\), convergence
  \(\lambda_k\to2\), attainment of every supremum, or optimality of the
  extracted exponential bound.

The exact next reproducibility obligation is to locate an original Applegate
coordinate vector, code, or later exact certificate for the \(k=11\) system,
or else reconstruct the finite linear program and generate a separately
attributed exact feasible witness.  Until that is done, the paper's theorem
retains its published status and the corpus's finite certificate retains its
strictly smaller scope.
