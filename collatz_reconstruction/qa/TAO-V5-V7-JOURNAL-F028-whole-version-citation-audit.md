# Tao v5/v7/journal F028 — whole-version and citation audit

## Scope, authority, and nonclaims

This record closes the source-to-source comparison of the complete arXiv v5
and v7 TeX files, classifies every non-whitespace source hunk against the
published journal manifestation, proves the finite numerical margin used in
Section 6, and inventories the active bibliography and citation calls.  It
does not prove Tao's analytic characteristic-function estimate, reprove the
main theorem from first principles, validate any cited work not yet read, or
close the whole-corpus, formal-release, Chatnotes, Gemini, or publication
gates.

The controlling proof manifestation is:

- arXiv v7 TeX:
  C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/latex/1909.03562v7/collatz.tex;
  164932 bytes; SHA-256
  bfbc39432d4084a276416cb019a592003c868fa32f18e2f90028ac325ae5c19d.

The comparison manifestations are:

- arXiv v5 TeX:
  C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/latex/1909.03562v5/collatz.tex;
  163356 bytes; SHA-256
  c676b362b30807aa6690d0d4f16b8c8e84324732f5c0eb72ccfd875000276ae0;
- journal PDF:
  C:/Users/LOCAL_USER/Documents/arxiv_latex/library/_recovered_from_papers/by_title/Tao Almost all orbits of the Collatz map attain almost bounded values.pdf;
  1008484 bytes; 56 physical pages; SHA-256
  55c817c73498f940ed1e70f10208105922f1f7c89e378dcb629040c534151a2b.

The immutable route artifacts were queried before the cited-source routing
audit and remain byte-identical:

- state/index_routes.jsonl: 274170 bytes; SHA-256
  b05028694bf133b9b19f2b0c0a771323b7a47ae872c0712769267aaf1f1eff38;
- state/document_routes.jsonl: 324776 bytes; SHA-256
  e439a5f9a70253b00824df5be791415e1c068d574c23f6f7f61851c19a88b2a5;
- state/index_snapshot.json: 799 bytes; SHA-256
  7d5a17440a3cb039f2bfbb4814567b5805117002136cc65687de738ee99af62f.

The quarantined task 019fe2cf-438a-7112-859c-119accee0e9e was not contacted,
steered, or used as evidence.  No Lean or Lake process was started.  The
global single-worker, watched, sub-3-GiB rule therefore remained satisfied.

## Exact terminal boundary

V7 has 1956 source lines.  Its proof ends at line 1859; line 1860 is blank;
the bibliography begins at line 1863, ends at line 1952, and the document
ends at line 1956.  V5 has 1945 lines.  Its proof ends at line 1848; its
bibliography occupies lines 1852--1941; the document ends at line 1945.
Journal pp. 55--56 contain the last proof implication, publisher paratext,
and references only.  There is consequently no mathematical content after
the former v7 line-1860 intake boundary.

The two exact bibliography blocks have 90 lines each.  After trailing-space
deletion they agree line by line; after deletion of all whitespace they are
the same 3600-character string.  This exact local identity does not identify
the complete source files.

## Complete source-diff census

A zero-context whole-file comparison gives 124 raw hunks, 147 added lines,
and 136 deleted lines.  Repeating with all whitespace ignored gives exactly
28 substantive hunks, 49 added lines, and 38 deleted lines.  Thus 96 raw
hunks are whitespace-only.  After deleting all whitespace from each complete
file, v5 has length 138900 and SHA-256
9f5d7629cc54e2f8660df82d2787ca256dacae145c905cad705e1dacbbb1375f,
whereas v7 has length 140369 and SHA-256
ca759f46014aaafab75e643e8ba13ee3befd5decb3e2f095c4ee712ab9193693.
The complete versions are therefore not text-identical even after whitespace
deletion.

The 28 substantive hunks are:

| Hunk | v5 locator | v7 locator | Exact distinguishing change |
|---:|---:|---:|---|
| 014 | 326 | 326 | Proposition 1.11 changes the opening domain from sufficiently large \(y\) to every \(y\) for which the defining set is nonempty. |
| 015 | 334 | 334 | The implied constants in Proposition 1.11 are stated to be absolute. |
| 017 | 344 | 344--346 | The forward Syracuse identity receives label syr-forward. |
| 019 | 364--365 | 366--369 | Reversal is explicitly relabelled and the recurrence receives label fn-recurse. |
| 021 | 381 | 385--387 | The \(3\)-adic projection receives label syr3. |
| 022 | 387 | 393 | Distributional equivalence is tied to reversal and (1.24); the ancient-iteration footnote is added. |
| 025 | 422 | 428 | The uniform domain \(n\ge1\), \(\xi\bmod3^n\), \(3\nmid\xi\) is made explicit. |
| 026 | 430 | 436 | The reverse-order statement cites fn-recurse. |
| 027 | 434 | 440 | The derivation from syr3 and the full random-variable name are supplied. |
| 028 | 440 | 446 | Lech Mazur is added to the acknowledgments. |
| 043 | 789 | 795 | A passage-location symbol is replaced by the required passage-time symbol. |
| 044 | 791 | 797 | The reciprocal passage-time/location interchange is corrected. |
| 057 | 983 | 989 | The Section 6 reserve changes from \(\frac12 C_A^2\log n\) to \(0.99C_A^2\log n\). |
| 058 | 991 | 997 | The same reserve change is propagated to the \(l\)-window. |
| 063 | 1029 | 1035 | The invalid \(1_{\overline E_k}\) is replaced by \(1_{E_k}\). |
| 064 | 1070 | 1076 | “Sufficiently small \(\varepsilon\)” becomes a suitable-choice statement. |
| 066 | 1074--1076 | 1080--1082 | The half/quarter exponent chain is replaced by the strengthened reserve and its resulting exponent. |
| 067 | 1078 | 1084 | The numerical comparison \(0.4175<0.6862\) is supplied. |
| 094 | 1656 | 1662 | Lemma 7.9 is weakened to the event \(R\le\mathbf r\), which is the event used downstream. |
| 095 | 1661 | 1667 | A missing closing parenthesis is repaired. |
| 096 | 1668--1670 | 1674--1675 | The separate \(r=0\) argument is removed after the indicator restriction. |
| 097 | 1676 | 1681 | The now-unneeded additive probability of \(r=0\) is removed. |
| 104 | 1753 | 1758--1760 | The triangle inequality receives label jjd. |
| 105 | 1772 | 1779 | Exact equation references are supplied. |
| 106 | after 1774 | 1782 | A missing algebraic substitution line is inserted. |
| 110 | 1821--1827 | 1829--1838 | The weakened Lemma 7.9 is propagated and \(F_*\) is explicitly defined. |
| 112 | 1838 | 1849 | The contradiction hypothesis is stated explicitly. |
| 113 | 1840 | 1851 | The final event is changed to \(E_{p,4^A(1+p^3)}\); this conflicts with the earlier definition using \(4^A(1+p)^3\). |

## Journal manifestation matrix

Every substantive hunk is visible in the journal.  “V5” and “v7” below
mean only that the journal agrees with that hunk's distinguishing content.
The journal is not silently identified with either arXiv manifestation.

| Hunk | Exact journal locator | Manifestation |
|---:|---|---|
| 014 | p. 8, Proposition 1.11 opening | v7 |
| 015 | p. 8, after (1.20) | v7 |
| 017 | p. 9, numbered equation (1.21) | v7 |
| 019 | p. 9, Lemma 1.12 proof and (1.24) | v7 |
| 021 | p. 10, Remark 1.13 and (1.25) | v7 |
| 022 | p. 10, below (1.25), including footnote 4 | v7 |
| 025 | p. 11, after Proposition 1.17/(1.28) | v7 |
| 026 | p. 12, before (1.29) | v7 |
| 027 | p. 12, after (1.29) | v7 |
| 028 | p. 55, acknowledgments/funding split | v5 |
| 043 | p. 23, converse bullet, first concluding display | v5 |
| 044 | p. 23, immediately following display | v5 |
| 057 | p. 28, equation (6.7) | v5 |
| 058 | p. 29, equation (6.8) | v5 |
| 063 | p. 30, equation (6.11) | v7 |
| 064 | p. 31, Corollary 6.3 proof after (6.14) | v5 |
| 066 | p. 31, three-line bound before (6.15) | v5 |
| 067 | p. 31, sentence before (6.15) | v5 |
| 094 | p. 49, Lemma 7.9 and (7.57) | v5 |
| 095 | p. 49, paragraph after (7.57) | v5 |
| 096 | p. 49, proof after (7.58) | v5 |
| 097 | p. 49, displayed \(Z((j',l'),R)\) estimate | v5 |
| 104 | p. 51, equation (7.65) | v7 |
| 105 | p. 52, paragraph below (7.66) | v7 |
| 106 | p. 52, middle line of the following display | v7 |
| 110 | p. 54, Lemma 7.9 application through (7.67) | hybrid |
| 112 | p. 54, immediately below (7.68) | v7 |
| 113 | p. 54, final paragraph | v7 |

The totals are 15 v7-like hunks, 12 v5-like hunks, and one hybrid hunk.
The hybrid at hunk 110 begins with v5's unconditional expectation and
\(\varepsilon\min(r,R)\), inserts v7's explicit definition of \(F_*\), and
returns to v5's unconditional conclusion.  The journal is therefore not a
uniform intermediate source version.

The four new source labels are recoverable as journal equation numbers:
syr-forward is (1.21), fn-recurse is (1.24), syr3 is (1.25), and jjd is
(7.65).

## Section 6: exact reserve computation and repair

Put
\[
 a=\log(4/3),\qquad b=\log2,\qquad
 q=\frac{b^2}{4a}.
\]
The square-root fluctuation term is bounded by Young's inequality in its
optimized form:
\[
 bC_A\sqrt{m\log n}
 \le am+\frac{b^2}{4a}C_A^2\log n
 =am+qC_A^2\log n.
\]
Numerically,
\[
 q=0.4175208154\ldots,\quad
 \tfrac12b=0.3465735903\ldots,\quad
 0.99b=0.6862157088\ldots.
\]
Consequently the v5 half-window leaves
\[
 \left(q-\tfrac12b\right)C_A^2\log n
 =0.0709472252\ldots\,C_A^2\log n
\]
with the wrong sign, even before the additional \(bC_A\log n\) tolerance.
The v5 conversion also drops the factor \(\log2\) when \(2^l\) is converted
to an exponential.  Thus the printed v5 Section 6 estimate does not close.
This is a statement about that printed proof, not a proof that its corollary
is false or cannot be proved another way.

The v7 reserve leaves the positive gap
\[
 (0.99b-q)C_A^2\log n
 =0.2686948933\ldots\,C_A^2\log n,
\]
which absorbs the \(O(C_A\log n)\) stopping overshoot after \(C_A\) is
enlarged.  Put
\[
 T=\frac{n\log3}{\log2}-C_A^2\log n.
\]
On \(B_k\), \(a_{[1,k]}\le T<a_{[1,k+1]}\).  On \(E_k\), the
\(i=k,j=k+1\) concentration inequality and \(a_k\ge1\) give
\[
 a_{k+1}\le1+C_A(\sqrt{\log n}+\log n).
\]
Thus the exact first-crossing estimate is
\[
 a_{[1,k+1]}\le T+1+C_A(\sqrt{\log n}+\log n).
\]
For \(n\ge2\), \(\sqrt{\log n}\le2\log n\) and \(2\le3\log n\); hence the
overshoot is, conservatively, at most \(6C_A\log n\).  For \(C_A\ge600\),
this is at most \(0.01C_A^2\log n\), yielding the printed
\(0.99\)-window.

The number \(0.99\) is convenient, not canonical.  If the retained fraction
of the unit \(C_A^2\log n\) window is denoted by \(\rho\), the asymptotic
closure condition is exactly
\[
 \rho>\frac{\log2}{4\log(4/3)}
 =0.6023552099\ldots.
\]
Any fixed \(\rho<1\) above this threshold is available after enlarging
\(C_A\) to absorb the linear overshoot.  No claim is made for
\(\rho\) at or below the threshold by this calculation.

Finally, the v5 factor \(1_{\overline E_k}\) cannot be substituted into the
restricted mass used in the collision estimate: the definitions and factor
carried through the proof require \(E_k\).  V7 and journal equation (6.11)
make the exact repair \(1_{E_k}\).

### The v5 size assertion has admissible counterexamples

The failure is not an artefact of a nonoptimal Young inequality.  Put
\[
 \lambda=\frac{2\log(4/3)}{\log2},
 \qquad
 \gamma=\lambda^{-2}.
\]
For fixed sufficiently large \(C_A\) and \(n\to\infty\), let
\[
 J=\lfloor\gamma C_A^2\log n\rfloor,\qquad
 d_i=\lfloor\lambda i\rfloor-\lfloor\lambda(i-1)\rfloor
 \quad(1\le i\le J),
\]
put \(d_i=0\) for \(i>J\), and set \(a_i=2-d_i\).  Every \(a_i\) is one or
two.  Every interval of length \(r\) has deficit at most
\(\lambda r+1\).  For \(r\le J\), this is within
\(C_A\sqrt{r\log n}+1\); for \(r>J\), the total deficit is within
\(C_A\sqrt{r\log n}+1\).  Thus, after the printed \(C_A\log n\)
tolerance, these coordinates satisfy the v5 concentration domain.

Let \(D=\lfloor\lambda J\rfloor\).  Choose \(l\), with parity matching
\(D\), within two of
\[
 \frac{n\log3}{\log2}-\frac12C_A^2\log n,
\]
and put \(K=(l+D)/2\).  For all sufficiently large \(n\), \(K\ge J\) and
\[
 a_{[1,K]}=2K-D=l.
\]
The \(j=J\) summand in the v5 natural-number size estimate then obeys
\[
 \log\frac{3^{J-1}2^{\,l-a_{[1,J]}}}{3^n}
 =
 \left(
 \frac{\log^22}{4\log(4/3)}-\frac12\log2
 \right)C_A^2\log n+O(1)>0.
\]
That single summand eventually exceeds \(3^n\).  This explicitly refutes
the universal v5 Archimedean size assertion used to lift a congruence to
integer equality.  It does not exhibit two colliding tuples and therefore
does not independently refute the separation corollary.  The actual v7
stopping event supplies the tighter window that excludes this construction.

### Prefix domain and two shared local formula defects

Corollary 6.3 does not need an unprinted \(i=0\) hypothesis.  For \(j\ge2\),
the printed \(i=1\) inequality bounds \(a_{[2,j]}\), and \(a_1\ge1\)
supplies the full prefix; \(j=1\) is direct.  There is nevertheless a literal
handoff mismatch: \(E_k\) is phrased with \(a_{[i,j]}\), whereas the
standalone corollary uses \(a_{[i+1,j]}\).  The needed prefix estimate follows
directly from \(E_k\); alternatively the shifted form follows after an
additive constant enlargement.  This is an indexing defect, not a false
standalone corollary.

Two defects shared by v5 and v7 were already repaired constructively in
F024 and remain part of the whole-version record.  The offset recurrence is
\[
 F_n(a_1,\ldots,a_n)
 =3^{n-1}2^{-a_{[1,n]}}+F_{n-1}(a_2,\ldots,a_n),
\]
not the printed expression with \(3^n\).  Also, the residue-fibre assertion
must concern \((a_1,\ldots,a_{k+1})\) with
\(a_{[1,k+1]}=l\), not a free \(m\)-tuple with
\(a_{[1,m]}=l\).  With those types corrected, injectivity gives
\(\max_y p_y\le2^{-l}\), and hence
\[
 \sum_y p_y^2\le2^{-l}\sum_y p_y\le2^{-l}.
\]

## Final-event mismatch

V7 line 1851 and journal p. 54 invoke
\(E_{p,4^A(1+p^3)}\).  Earlier, the same source and journal p. 53 define
\(E_*\) using the events \(E_{p,4^A(1+p)^3}\).  These parameters are not
equal in general.  The proof's following inequality uses
\(4^A(1+p)^3\), so the definition and downstream bound force the latter
event.  The occurrence with \(1+p^3\) is retained as a source defect and is
not used as a new event identity.

## Active bibliography and dependency boundary

V7 contains 25 active citation calls, 23 distinct cited keys, and 24 active
bibliography items.  Every cited key resolves within the bibliography.
The sole active uncited item is terras2.  Exact bibliography equality means
the same counts hold for v5.  No citation call occurs inside a proof as a
logical dependency: the calls serve introduction, provenance, nomenclature,
heuristic, computation-report, analogy, or “see also” roles.

Crandall, Everett, and Lagarias have already been read in the present corpus.
The following cited identities were not found in either frozen route ledger
and had no exact-title/author filename hit in the configured Library, OS,
used often, or arxiv_latex roots:

allouche, baker, barina, bourgain, carletti, chamber, korec, kont, km, ks,
kl, ls, lw, olive, eric, sinai, tao:chowla, terras, thomas, wirsch, and the
uncited terras2.

This is a bounded route and exact-filename miss, not a nonexistence claim and
not a claim that no opaque filename contains a source.

Claim-driven intake order is:

1. terras, allouche, korec for the almost-all descent lineage and exact
   exponent thresholds;
2. kl for the stated \(\gg x^{0.84}\) convergent-orbit count;
3. barina, eric, olive for the exact computational bounds and chronology;
4. sinai for the valuation/path construction;
5. carletti for the triple-iterate acceleration attribution;
6. wirsch and thomas for the explicitly tentative \(3\)-adic interfaces;
7. lw, kont, km, and ls for stochastic and Benford heuristics;
8. ks for “n-path” terminology;
9. chamber for survey navigation;
10. tao:chowla and bourgain for analogies;
11. baker, whose theorem Tao explicitly says is not exploited;
12. terras2 only if the Terras lineage or the uncited-entry discrepancy
    makes it consequential.

Nearby Baker and Bugeaud books and the local annotated bibliography are
finding aids or nonidentical works; they are not silently registered as the
cited articles.

## Deterministic certificate and exact certification boundary

The script certificates/tao_whole_version_checks.py pins all three
manifestations and all three frozen routing artifacts.  It deterministically
checks line counts and terminal boundaries, raw and whitespace-insensitive
diff metrics, the 32 distinguishing source signatures, exact bibliography
equality, citation-key closure, journal page count, and rational enclosures
for the Section 6 logarithmic inequalities.

The script does not certify the page-read journal matrix, the analytic
Fourier-decay estimate, an implicit constant not made explicit by the source,
Tao's main theorem, or the Collatz conjecture.  Those exclusions are emitted
in the certificate result rather than left implicit.

## Consequence boundary

The whole v5/v7 textual comparison and journal hunk classification are now
complete.  V7 remains the controlling proof manifestation.  The exact
Section 6 reserve repair and the corrected \(E_k\) event may be used
downstream; the v5/journal half-window may not.  The final
\((1+p^3)\)-event occurrence may not be treated as definitionally equal to
the earlier \((1+p)^3\)-event.  The bibliography inventory is complete, but
the substantive cited-source intake listed above remains open, as do
whole-paper adversarial release, formal/certificate coverage beyond the
finite kernels, package validation, visual QA, recovery, and the larger
corpus programme.
