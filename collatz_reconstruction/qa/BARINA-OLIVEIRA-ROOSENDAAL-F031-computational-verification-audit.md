# Barina--Oliveira e Silva--Roosendaal F031 — computational verification and exact sieve-coordinate audit

## Scope and evidentiary status

This audit reconstructs the computational-verification lineage used by David
Barina's 2020/2021 and 2025 articles, Tomás Oliveira e Silva's 2010 chapter and
author status page, Eric Roosendaal's continuously revised computational page,
and the pinned public program lineages used by Barina's project.  It records
four kinds of statement separately:

1. exact arithmetic identities and morphisms proved in this edition;
2. finite computations reported by a named source;
3. finite checks reproduced by the F031 certificate;
4. implementation or historical claims for which the actual completed-work
   ledger was not acquired.

A published statement that a bound was checked is retained as a published
computational result.  It is not relabelled as an independently reproduced
exhaustive computation merely because source code is public.  Conversely, a
defect in prose, pseudocode, or server validation is not used to negate a
reported computation without an exact dependency argument.  No result in this
audit proves the Collatz conjecture for all positive integers.

The map convention is never inferred from the word “Collatz.”  The shortened
map \(T\), the unshortened map \(U\), Barina's auxiliary map \(T_1\), the
variable-length block map \(B\), and Oliveira e Silva's generalized maps are
defined separately below, with their clocks and bridges exposed.

## Frozen-route gate

Before external acquisition, the exact strings

- David Barina;
- Convergence verification of the Collatz problem;
- Improved verification limit for the convergence of the Collatz conjecture;
- DOI 10.1007/s11227-020-03368-x;
- DOI 10.1007/s11227-025-07337-0;
- Tomás Oliveira e Silva;
- Empirical Verification of the 3x+1 and Related Conjectures;
- Eric Roosendaal;
- ericr.nl/wondrous; and
- xbarin02/collatz-sieve

were queried in both immutable routing ledgers.  None produced a matching
source row.  These are bounded route misses, not source-nonexistence claims.
The three frozen route artifacts remain at their ACT33 hashes and were not
reindexed or modified.

## Controlling manifestations

### Barina 2020/2021 article

The institutional FIT record and publisher manifestation identify:

David Barina, “Convergence verification of the Collatz problem,”
*The Journal of Supercomputing* **77** (2021), no. 3, 2681--2688,
DOI 10.1007/s11227-020-03368-x.  The copyright line and online publication
belong to 2020; the journal coordinates belong to 2021.

The two retained eight-page manifestations are:

- publisher PDF:
  C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/published/Barina-2021-Convergence-verification-publisher.pdf,
  630022 bytes, SHA-256
  737a225fbc291cc182e940cc7ca31da4d2eb99b64e51a33e380213d8ed6b33a3;
- author postprint:
  C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/source/Barina-2020-Convergence-verification-postprint.pdf,
  205829 bytes, SHA-256
  6df53d8f2a41d032f215209f06a021d35e447f6bdf222f1d557be730b64409dc.

The FIT result-page snapshot is:

C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/source/Barina-FIT-result-c168171-20260828.html,
86108 bytes, SHA-256
4552fef8ff8e4df696128fc9acf92e52a26bacb57f754cce13b9271f36d1ad16.

Both article manifestations were content-read.  The publisher PDF is the
controlling journal manifestation; the postprint is retained as a distinct
author manifestation, not merged into it.

### Barina 2025 article

The controlling publisher manifestation is:

David Barina, “Improved verification limit for the convergence of the Collatz
conjecture,” *The Journal of Supercomputing* **81**, article 810 (2025),
accepted 21 April 2025, published online 2 May 2025,
DOI 10.1007/s11227-025-07337-0.

Local path:

C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/published/Barina-2025-Improved-verification-limit-publisher.pdf,
862781 bytes, fourteen pages, SHA-256
764fd732ad79545e71440f74bf738bf315b479eb404f68bae2c3b109785a5d06.

All fourteen physical pages were rendered at 180 dpi and inspected.  The
separate FIT record snapshot is:

C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/source/Barina-FIT-result-c197809-20260828.html,
86250 bytes, SHA-256
f568ef3f8d675493c4993458e94f912abf6f3386ecc397f815433615f5270161.

The FIT record says volume 81, no. 1, pp. 1--14.  The publisher PDF uses volume
81 and article number 810.  The publisher coordinate is controlling; the
metadata discrepancy is preserved.

### Barina program and sieve lineages

The public xbarin02/collatz repository is a changing code lineage.  It was
cloned locally at HEAD
326638d25c11f5849e9a7dc029f68fcf65afef79, tree
21f47c3cec5b3afa1a05816495f6eb0b7bd5e3b4.  Complete history is retained in

C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/source/xbarin02-collatz-all-20260828.bundle,
1083308 bytes, SHA-256
e7b655972c628f060ecbc7aaffaa381eeebe6868567d14c4f4524c18559cc3dd.

The bundle verifies as complete.  Two historical boundaries are used:

- 0fabf721434b20f00af820564e3b3781dcabe768, tree
  f8597ec3867e5734cd6a9fb57379aef2c670f857, dated 16 June 2020, for the
  earlier article's contemporary code boundary;
- 53c2a0608075d6fe3f10cc6eeeaf50e400c86338, tree
  82b9731dcd5108298a2fb2085ba1d76c837de6f5, dated 16 January 2025, resolving
  the abbreviated commit 53c2a06 printed in the 2025 article.

The 2025 bootstrap does not contain the sieve maps.  It clones the separate
xbarin02/collatz-sieve repository.  That dependency is pinned at
e5f0c264ba1f5f9c0a7d32a10c3aa61b225c70d1, tree
4b5a3b5afdf35596409c91da7f226e338c7c763a, dated 14 March 2024, with complete
history in

C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/source/xbarin02-collatz-sieve-all-20260828.bundle,
787146017 bytes, SHA-256
687f00faba696d2a3dc8b0a6f556c9cc6da56756bdb36535ac8f3ed49575983f.

This is the audit's acquisition pin, not a pin printed by the article.  The
2025 footnote fixes only the xbarin02/collatz commit.  At that commit,
scripts/bootstrap.sh:41--58 performs a clone or unpinned git pull of both
repositories.  Consequently the article and repository do not by themselves
fix the exact collatz-sieve tree that generated every production map.  The
2024 dependency pin above is therefore a separately attributed reconstruction
boundary, and no later code is back-projected into the 2025 run.

The exact generated-map dependencies selected by the pinned bootstrap include:

- esieve-34.lut50.gz, 87843031 bytes, SHA-256
  450596d8222a30724b732238de69b7fc13779795a52a93528941076a59e200ef;
- h2esieve-24.gz, 150110 bytes, SHA-256
  b0222a680a7f65a59efd413829cc56668dd5734c099bfc32c356b285a1867fa4.

The compressed map is an implementation artifact, not a proof by itself.  Its
generator and every elimination branch used below must still have an exact
arithmetic justification.

### Oliveira e Silva 2010 chapter and author records

The author's bibliography and the AMS volume identity fix:

Tomás Oliveira e Silva, “Empirical Verification of the 3x+1 and Related
Conjectures,” in Jeffrey C. Lagarias (ed.), *The Ultimate Challenge: The 3x+1
Problem*, American Mathematical Society, 2010, pp. 189--207.

The durable author snapshots are:

- C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/source/Oliveira-e-Silva-bibliography-3.5-20260828.html,
  3303 bytes, SHA-256
  ad4e9677811b3d3a82822f4938e924d199c5d34bd2ff42bac02c10746fe756c9;
- C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/source/Oliveira-e-Silva-3x-plus-1-20260828.html,
  11526 bytes, SHA-256
  46aba9a800d4fd9e0c08419e02ad4ec7ea2141b68ed0b9781987f7a309c8eeff.

The complete chapter was content-read against a third-party scan page by
page, including every printed page 189--207.  Those temporary images are
visual witnesses only.  They are not copied into the topical shelf or reader,
and the protected chapter is paraphrased and cited rather than reproduced in
bulk.

### Roosendaal page and dynamic Barina status

The Roosendaal page was captured over plain HTTP because the HTTPS endpoint
presented a certificate-name failure to the command-line client:

C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/source/Roosendaal-wondrous-20260828.html,
35449 bytes, SHA-256
e3ff21c62b1fe108ecaa9086a2c8679207339b3e086289a159b56099515f157d.

It identifies itself as last modified 30 June 2026.  The unauthenticated
transport is retained as a provenance limitation.  Its mathematical text is
audited on its own terms; it is not used as an authenticated project ledger.

The Barina project status API snapshot is:

C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/source/Barina-project-status-20260828.json,
198 bytes, SHA-256
daf454223878d578dc7a87dc0677aa1925eba602ae295f8547ce25927ce5c5ab.

It was generated 28 August 2026 at 19:24:59 +0200 and reports
verified_up_to_times_2_60 = 2075, work_unit_exp = 40, and both the lowest
incomplete and lowest unassigned unit as 2175975546.  This is a dated dynamic
status assertion, not part of the 2025 article and not an independently
acquired database ledger.

## Exact maps and clocks

Let

\[
 U(n)=
 \begin{cases}
  3n+1,&n\ \hbox{odd},\\
  n/2,&n\ \hbox{even},
 \end{cases}
\qquad
 T(n)=
 \begin{cases}
  (3n+1)/2,&n\ \hbox{odd},\\
  n/2,&n\ \hbox{even}.
 \end{cases}
\]

Thus one odd \(T\)-step is two \(U\)-steps and one even \(T\)-step is one
\(U\)-step.  The exact variable-time embedding is MOR-COL-000032.  No
one-step equality between \(T\) and \(U\) is asserted.

Barina defines

\[
 T_1(n)=
 \begin{cases}
  (n+1)/2,&n\ \hbox{odd},\\
  3n/2,&n\ \hbox{even}.
 \end{cases}
\]

The two printed bridges are exact branchwise identities:

\[
 T(n)=
 \begin{cases}
  T_1(n+1)-1,&n\ \hbox{odd},\\
  n/2,&n\ \hbox{even},
 \end{cases}
\]

and

\[
 T_1(n)=
 \begin{cases}
  T(n-1)+1,&n\ \hbox{odd},\\
  3n/2,&n\ \hbox{even}.
 \end{cases}
\]

They move the additive term between the two coordinate charts.  They do not
make \(T\) and \(T_1\) identical maps.

This distinction resolves the 2025 page-4 example.  Its displayed
``trajectory on \(n+1\)'',

\[
 (7,4,6,9,5,3,2),
\]

is the shifted-coordinate representation associated with the trajectory
starting at 12; it is not the shortened \(T\)-orbit of 13.  The phrase is
retained in its stated chart and is not normalized into a different orbit.

## Barina's variable-length block map

For \(x>0\), put

\[
 \alpha=\nu_2(x+1),\qquad
 u=\frac{x+1}{2^\alpha},\qquad
 y=3^\alpha u-1,\qquad
 \beta=\nu_2(y),
\]

and define

\[
 B(x)=\frac{y}{2^\beta}.
\]

Here \(u\) is odd.  If \(x\) is odd then \(\alpha\geq1\), \(y\) is positive
even, and \(\beta\geq1\).  If \(x\) is even then \(\alpha=0\), \(y=x\), and
again \(\beta\geq1\).  Hence \(B(x)\) is always a positive odd integer.

For \(0\leq j\leq\alpha\),

\[
 T^j(x)=3^j\frac{x+1}{2^j}-1.
\]

The proof is induction: the right side is odd before the next step because
\((x+1)/2^\alpha=u\) is odd and the preceding quotients still contain a
factor of two.  After the \(\alpha\) odd steps the state is \(y\), and for
\(0\leq r\leq\beta\),

\[
 T^{\alpha+r}(x)=\frac{y}{2^r}.
\]

Therefore

\[
 B(x)=T^{\alpha+\beta}(x).
\]

This is an exact variable-clock acceleration, not a fixed iterate.

The fibres are explicit.  For odd \(z>0\), every point in \(B^{-1}(z)\) is
uniquely described by integers \(\alpha\geq0\), \(\beta\geq1\) satisfying

\[
 3^\alpha\mid 2^\beta z+1,
\qquad
 x=2^\alpha\frac{2^\beta z+1}{3^\alpha}-1.
\]

Conversely this formula gives
\(\nu_2(x+1)=\alpha\), \(\nu_2(3^\alpha u-1)=\beta\), and \(B(x)=z\).
The section \(s(z)=2z\) has \(B(s(z))=z\), so \(B\) is surjective.  It is
not injective: for every \(\beta\geq1\), \(2^\beta z\) lies in the fibre
with \(\alpha=0\).  Thus no left or two-sided inverse exists after the
block boundaries and elapsed time have been discarded.

The special point is not omitted:

\[
 B(1)=1,
\]

representing the shortened cycle \(1\mapsto2\mapsto1\).  The printed endpoint
conditions are version- and algorithm-specific:

- 2021 Algorithm 1, page 4, uses strict ``until \(n<n_0\)'' and therefore
  loops at \(n_0=1\);
- 2021 Algorithm 2, page 5, uses ``until \(n=1\)''.  From \(n_0=1\) it
  performs one full \(1\mapsto1\) block and terminates, but a literal delay
  accumulator returns two shortened steps instead of the conventional total
  stopping time zero;
- both 2025 Algorithms 1 and 2, pages 4--5, use strict ``until \(n<n_0\)''
  and loop at \(n_0=1\).

For each strict version the exact repair is either the domain \(n_0>1\) or a
separate \(n_0=1\) base case; for the 2021 delay algorithm the base case is
needed to preserve the conventional value zero.  The production worker tests
starts congruent to \(3\bmod4\), so this endpoint does not occur in its
intended inner loop.

### The phrase “average four iterates”

The articles' average can be stated exactly only after a measure is named.
Give the odd 2-adic integers normalized Haar measure.  Then

\[
 \Pr(\alpha=a)=2^{-a}\quad(a\geq1).
\]

Conditional on \(\alpha=a\), multiplication of the odd quotient \(u\) by
the odd unit \(3^a\) preserves Haar measure, and

\[
 \Pr(\beta=b\mid\alpha=a)=2^{-b}\quad(b\geq1).
\]

Consequently \(\alpha\) and \(\beta\) are independent geometric variables
with means two, and

\[
 \mathbb E(\alpha+\beta)=4.
\]

This does not assert that every finite interval has raw arithmetic mean
exactly four.

## Fixed dyadic prefix coordinates

Fix \(k\geq0\), \(h\geq0\), and \(0\leq r<2^k\).  Let

\[
 a_j(r)=\#\{0\leq i<j:T^i(r)\ \hbox{is odd}\}.
\]

For every \(0\leq j\leq k\),

\[
 T^j(2^k h+r)
 =
 3^{a_j(r)}2^{k-j}h+T^j(r).
\tag{F031.1}
\]

For \(j<k\), the high term is even.  Hence the parity of the full state is
exactly the parity of \(T^j(r)\), which proves by induction that the same
branch is taken and establishes (F031.1).  At \(j=k\),

\[
 T^k(2^k h+r)=3^{a_k(r)}h+T^k(r).
\tag{F031.2}
\]

This is Oliveira e Silva's Proposition 1 and Barina's equation (6) in the
same exact coordinate, with no identification of their surrounding
algorithms.

Write \(a=a_k(r)\), \(d=T^k(r)\).  Uniform descent of every positive high
coordinate is

\[
 3^a h+d<2^k h+r\qquad\hbox{for every integer }h>0.
\]

With \(L=3^a-2^k\) and \(R=r-d\), its exact necessary-and-sufficient
criterion is

\[
 (L<0\ \hbox{and}\ L<R)
 \quad\hbox{or}\quad
 (L=0\ \hbox{and}\ R>0).
\tag{F031.3}
\]

The generator function is_convergent returns only the first disjunct,
lhs < rhs && lhs < 0.  It is therefore conservative at the coefficient
equality case; it does not falsely certify that case.

The 2025 Section 3.4 description contains a separate cardinality reversal.
Inside a work unit of width \(2^{40}\), one fixed residue class modulo
\(2^k\) contains exactly

\[
 2^{40-k}
\]

starts for \(0\leq k\leq40\), while there are \(2^k\) such residue classes.
The section twice assigns \(2^k\) starts to one class.  The 2021 page-6 CPU
example gives the correct \(2^{40-34}\), and the loop bounds in
src/worker/worker.c:336--369 implement the correct count.  This is a prose
defect, not an inferred change to the executable iteration domain.

If \(r'<r\) and the endpoint coordinates agree,

\[
 a_k(r')=a_k(r),\qquad T^k(r')=T^k(r),
\]

then for every fixed \(h\),

\[
 T^k(2^k h+r')=T^k(2^k h+r),
\qquad
 2^k h+r'<2^k h+r.
\]

This proves the lower-trajectory coalescence certificate represented by the
sorted \((a,d,r)\) table.  Equal endpoint coordinates are sufficient;
different-looking formulae are never treated as evidence of noncoalescence.

The generator's terminology must be repaired accordingly.  A dead residue
has a finite descent, lower-path, coalescence, inherited-prefix, or
predecessor certificate.  A live residue is only the complement of the
implemented finite certificates.  It is not a residue class of numbers
proved not to converge.  The 2025 phrase that the sieve tests numbers that
“do not converge” is too strong if read globally.

The generator history also has a bounded, dated implementation defect.
Commit 49c5524d8d42867c866e863030a8e5d86237bf17 (10 April 2020) introduced
the SAVE_MEMORY call

\[
 \texttt{is\_convergent(k,b,c\_,c\_)}
\]

where the fourth argument had to be the endpoint \(d_\), not the odd-step
count \(c_\).  Commit b3d2f61d89eec55008d61c32577a9e8c8b3874ab
(6 April 2023) changed it to \(d_\).  The committed baseline maps date
11 January 2020 and predate the faulty source interval; the hesieve and
h2esieve maps were added in March 2024 after the repair.  Thus the defect
matters for regeneration from intermediate history but is not attributed to
those committed blobs without evidence.

## Exact elementary reductions

The following reductions are finite orbit identities for the shortened map.

1. Every even \(n>0\) has \(T(n)=n/2<n\).
2. If \(n=4q+1\) with \(q\geq1\), then
   \(T^2(n)=3q+1<4q+1=n\); \(n=1\) is the base cycle.
   Hence an ascending stopping-time computation need test only starts
   \(n\equiv3\bmod4\).
3. For \(q\geq0\),

\[
 T(2q+1)=3q+2,
\]

so the target \(3q+2\) joins the path of the lower start \(2q+1\).
4. The further exact transports are

\[
 T^3(8q+3)=9q+4,\qquad
 T^6(64q+7)=81q+10,\qquad
 T^7(128q+95)=243q+182.
\tag{F031.4}
\]

Their odd-step counts are respectively \(2,4,5\); the first transport has
one odd step.  Each source is strictly below its target.

The first two initial-residue reductions give the omitted classes
\(\{2,4,5,8\}\bmod9\).  Their lifts modulo 27 are

\[
\{2,4,5,8,11,13,14,17,20,22,23,26\}.
\]

The \(81q+10\) family is disjoint from the first two initial families and
raises their combined eliminated fraction to

\[
\frac13+\frac19+\frac1{81}=\frac{37}{81}=45.679\ldots\%.
\]

The \(243q+182\) target is already \(2\bmod3\) as an initial residue; its
use inside the recursive predecessor search is nevertheless not redundant,
because the target can occur as an intermediate low-coordinate state.

Oliveira e Silva's Roosendaal coalescence example is also exact:

\[
 T^6(64q+15)=T^6(64q+14)=T^5(32q+7)=81q+20.
\tag{F031.5}
\]

## Hercher coalescence branch

Let \(x\) be an odd positive state, put

\[
 \alpha=\nu_2(x+1),\quad
 u=(x+1)/2^\alpha,\quad
 y=3^\alpha u-1,\quad
 \beta=\nu_2(y),
\]

and suppose \(\beta\geq2\).  Set \(m=(x-1)/2\).  Since
\(y\equiv0\bmod4\), the state \(3^{\alpha-1}u-1\) is \(2\bmod4\), and direct
iteration gives

\[
 T^{\alpha+\beta-1}(m)=T^{\alpha+\beta}(x)=y/2^\beta.
\tag{F031.6}
\]

Now suppose \(x=T^s(r)\) is the low state in a dyadic prefix, with \(c\)
odd steps among the first \(s\).  If \(m<r\), then \(x<2r\).  The affine
remainder in \(T^s(r)\) is nonnegative, and is positive when \(c>0\), so

\[
 \frac{3^c}{2^s}<2.
\]

For a full start \(N=2^k h+r\), the lifted lower coordinate is

\[
 Q=3^c2^{k-s-1}h+m<N.
\]

Equation (F031.1) and (F031.6) show that the trajectories of \(Q\) and \(N\)
coalesce after the displayed unequal clocks.  This proves the elimination
implemented by is_live_in_sieve_2_34v2 on the intended odd low-coordinate
classes.

## Recursive smallest-predecessor branch

The 2024 function smallest_predecessor composes the four transports in
(F031.4).  Its name is broader than its operation: it finds the minimum only
inside this restricted recursive closure, not among all Collatz predecessors.
For the four primitive inverse maps, the odd-step count \(d\), total-step
count \(t\), and affine loss \(H\) are

\[
 (d,t,H)=(1,1,1),(2,3,5),(4,6,73),(5,7,211),
\]

and each eligible target \(L\) is sent to

\[
 \phi(L)=\frac{2^tL-H}{3^d}
         =\left\lfloor\frac{2^tL}{3^d}\right\rfloor.
\]

A recursion word with total counts \((d,t)\) produces a positive integer
\(P\) satisfying

\[
 T^t(P)=L.
\tag{F031.7}
\]

and has the form

\[
 P=\frac{2^tL-H_w}{3^d}
   =\frac{2^t}{3^d}L-h_w,
 \qquad h_w=H_w/3^d.
\]

Each primitive multiplier \(2^t/3^d\) lies strictly between zero and one and
each primitive normalized loss lies strictly between zero and one.  Induction
under composition therefore gives

\[
 0<h_w<\ell(w)\leq d
\tag{F031.7a}
\]

for every nonempty word \(w\).

If the current low state is

\[
 L=T^s(r)
\]

after \(c\) odd steps, the only coefficient-correct lift to a full
\(N=2^k h+r\) is

\[
 Q=3^{c-d}2^{k-s+t}h+P.
\tag{F031.8}
\]

Substitution into the affine-prefix formula proves
\(T^t(Q)=T^s(N)\).  The necessary comparison is

\[
 3^{c-d}2^{t-s}\leq1
\tag{F031.9}
\]

together with \(P<r\).  There is a distinct comparison in the
\(\beta\geq2\) coalescence branch.  If the preceding prefix has length
\(s_0\), odd-step count \(c_0\), and low state \(x\), put
\(m=(x-1)/2\).  For a restricted word with \(T^t(P)=m\), its full lift has
coefficient

\[
 3^{c_0-d}2^{k-s_0-1+t},
\]

so the exact required inequality is

\[
 2^t3^{c_0-d}\leq2^{s_0+1}.
\tag{F031.9b}
\]

The C function returns only the numerical minimum \(P\).  It stores neither
\((d,t)\) nor a proof of (F031.9) or (F031.9b), and tests only \(P<r\).
This is a genuine missing source-level check.  F031 nevertheless closes it
for the generator's finite implementation domain \(k\leq34\) as follows.

If either lifted coefficient is greater than one, the least possible exact
ratio in the relevant exponent boxes is

\[
 C_{\min}=\frac{3^{12}}{2^{19}}
 =\frac{531441}{524288},
 \qquad C_{\min}-1=\frac{7153}{524288}.
\tag{F031.9c}
\]

In the current-state branch, (F031.7a), the affine prefix, and \(P<r\) imply

\[
 P(C-1)<h_w<34,
 \qquad r-P\leq33.
\]

Hence any unsafe witness has \(P\leq2492\).  In the coalescence branch the
extra division contributes \(a/2<1/2\), where
\(a=2^t/3^d<1\), so an unsafe witness must satisfy

\[
 P(C-1)<h_w+a/2<34\tfrac12,
 \qquad r-P\leq34,
\]

and therefore \(P\leq2528\).  These bounds reduce the apparently
\(2^{34}\)-sized question to a deterministic finite enumeration of every
restricted word of odd budget at most 34 and every nearby shortened-map
prefix of length at most 34.

The certificate finds, in the current-state branch, 7105 restricted word
states, 1557 identity endpoint pairs with their coefficient proved safe,
2983 nonidentity common-endpoint pairs, and 2585 budget-admissible pairs; all
2585 satisfy (F031.9).  In the coalescence branch it finds 7216 word states,
1003 common-endpoint pairs, of which 480 are identity pairs proved safe by
the Hercher argument and 523 are nonidentity; all 487 budget-admissible
nonidentity pairs satisfy (F031.9b).

Thus the omitted coefficient test has been proved safe for the pinned
\(k\leq34\) implementation domain.  No unbounded recursive coefficient
invariant follows: the proof uses the finite exponent box and its exact
minimum gap (F031.9c).  The unbounded statement remains an explicit proof
obligation and is not silently used as a theorem.  This distinction neither
authenticates nor contradicts the reported distributed computation.

Four further implementation boundaries remain visible.  First, residue zero
evaluates the unsigned expression \((L_{\rm last}-1)/2\); wraparound prevents
that branch from clearing zero, but the wrapped value has no meaning as a
positive-integer predecessor.  Second, the functions have no explicit
\(k\leq34\) precondition: the effective bound comes from the packed-coordinate
assertion \(b<2^{34}\) in fsieve.c:184.  If assertions are disabled beyond
that domain, the 34-bit \(b\)-field can alias rather than reject the input.
Third, compat.h:15--24 implements ctzu64 through unsigned long and traps when
unsigned long is not 64 bits; this is an LP64 assumption and fails on LLP64.
Fourth, a generated dead-map bit records no predecessor word, \((d,t)\), or
elimination-reason witness.  The bit artifact therefore cannot by itself
reconstruct which v3 certificate killed each residue.

## From strict descent to a finite convergence statement

Suppose a computation processes positive starts in increasing order.  If for
each \(2\leq n\leq X\) it exhibits an iterate \(T^{j(n)}(n)<n\), then all
starts through \(X\) reach 1.  The proof is strong induction: the displayed
iterate is a smaller positive start, which reaches 1 by the induction
hypothesis; composing the two finite orbit segments proves the assertion for
\(n\).  The base \(n=1\) is immediate.

This argument explains why a stopping-time computation can report
convergence throughout a finite range without calculating every trajectory
all the way to 1.  It does not turn a reported machine run into an
independently reproduced run.

## Oliveira e Silva's finite 3x+1 computation

Printed Theorem 1 says unambiguously

\[
 n\leq20\cdot2^{58}.
\]

The chapter reports that no counterexample in this range was found.  The
twenty processed intervals each contain \(2^{58}\) integers, so the direct
work is naturally half-open at \(20\cdot2^{58}\).  The inclusive printed
endpoint is nevertheless valid from the same finite result because
\(20\cdot2^{58}\) is even and its first \(T\)-iterate is the already covered
\(10\cdot2^{58}\).

The exact decimal value is

\[
 20\cdot2^{58}=5764607523034234880.
\]

The chapter reports a summer-2004 start, termination in January 2009, about
four CPU-years per interval, and approximately 81 CPU-years overall.  The
author status page gives the dated progression from \(2^{58}\) on
21 September 2004 through \(20\cdot2^{58}\) on 18 January 2009.

The verification algorithm used:

- a pruned parity tree to depth 46;
- \(269949796982\) surviving residue leaves at depth 46;
- blocks of \(2^{12}\) starts beneath each surviving leaf;
- the exact initial reductions \(2\bmod3\), \(4\bmod9\), and
  \(10\bmod81\);
- variable-step tables with \(\Delta=14\) and tolerance \(\tau=10\);
- separate exact recomputation for rare maximum-excursion or stopping-time
  candidates.

Every work item was assigned to two different workers.  The returned
candidate data and a cyclic-redundancy checksum depending on the entire
computation had to match exactly.  The chapter reports one mismatch in
81 CPU-years; the incompatible results were invalidated and recomputed.
This is a materially stronger protocol than a single unchecked run, but the
worker source, completed-work ledger, and raw duplicate outputs were not
acquired here.  The finite bound remains a sourced computational result, not
an F031 reproduction.

The author page deliberately says the conjecture is “probably” true through
the bound to reserve machine or algorithm error.  This rhetoric is not
rewritten as either a proof of universal convergence or a denial of the
finite reported result.

## Barina's reported bounds and exact chronology

The 2020/2021 article reports that the distributed project verified all
starts below \(2^{68}\) between September 2019 and May 2020.  Its performance
figures are measurements on named hardware and configurations, not
mathematical speed theorems.

The 2025 article's Section 6 and Table 10 report:

\[
 n<2^{71}
\]

verified on 15 January 2025.  Surrounding prose and the abstract also say
“up to” \(2^{71}\); the table's strict endpoint is retained as the published
computational coordinate.  The boundary \(2^{71}\) itself is a power of two
and trivially reaches 1, but that independent observation does not alter the
source wording.

The server space has \(2^{32}\) work units, each representing the half-open
interval

\[
 [j2^{40},(j+1)2^{40}),
\]

so its representable range is \(2^{72}\).  The production worker actually
iterates the \(3\bmod4\) starts; the even and \(1\bmod4\) cases are removed by
the exact reductions above.

The article reports 12395 CPU-years and 159 GPU-years, including very slow
machines.  Those totals and all throughput/speedup tables are reported
measurements.  They do not establish hardware-independent optimality.

The 2025 page-2 throughput convention explicitly counts starts eliminated by
sieve certificates although their trajectories are not individually run to
one; “numbers per second” is therefore not an orbit-evaluation count.  Its
cycle-length lower bound is imported from Hercher rather than proved by this
finite run.  Likewise, the 2021 statement that its record data “confirm” the
Lagarias--Weiss prediction records finite consistency, not an asymptotic
proof.  The 2021 \(O(N)\) memory statement concerns the iterate lookup table;
it is not a bound for the total worker state or the logical \(2^k\)-bit
convergence sieve.

The later API snapshot reports \(2075\cdot2^{60}\), namely

\[
 2392312122059207475200
 \approx2^{71.0188956211}.
\]

Its first incomplete unit begins at

\[
 2175975546\cdot2^{40}
 =2392510414583230365696.
\]

The status snapshot is later than the paper and cannot be used to rewrite
the paper's 15 January 2025 result.

## Pinned-code execution and validation boundary

At the 2025 code boundary, the CPU worker uses unsigned 128-bit arithmetic
and enters its GMP continuation only when compiled with \texttt{\_USE\_GMP}
(src/worker/worker.c:176--248).  The GPU kernel has no GMP arithmetic.  On its
overflow path it zeroes a lane checksum; gpuworker.c:652--656 translates that
zero into \texttt{ABORTED\_DUE\_TO\_OVERFLOW}, and mclient.c:427--436 retries
the complete assignment using the CPU worker.  Therefore the possible chain
is

\[
 \text{GPU}\longrightarrow\text{CPU}\longrightarrow\text{GMP},
\]

not in-kernel GPU multiprecision, and even that chain is deployment-
conditional.  scripts/bootstrap.sh:75--84 builds a GMP-enabled CPU worker,
but scripts/lumi_submit_gpu.sh:56--66 and scripts/meta_submit_gpu.sh:76--82
build only gpuworker and mclient.  In those GPU-only layouts a GPU overflow
does not by itself establish that a usable local CPU/GMP fallback exists.

The Git object src/gpuworker/kernel.cl has mode 120000 and points to
kernel32.cl; this is the default kernel used when the production scripts do
not pass an alternate kernel.  The optional/test kernel
kernel32-precalc.cl:187--192 executes a sieve-dependent \texttt{continue}
immediately before a work-group barrier.  If a multi-lane work group contains
both live and dead sieve lanes, not all work-items encounter the barrier, so
that optional kernel violates the OpenCL barrier-convergence requirement.
This defect bounds claims about that precalculation variant; it is not
silently transferred to the default kernel32.cl or to the published run.

The transmitted checksum is the accumulated \(\alpha\)-sum.  mclient.c:
374--381 parses but discards the \(\beta\)-sum before transmission.  The
remaining value is an informal proof-of-work consistency signal, not a
collision-resistant commitment to every orbit state.

server.c:512--515 first rejects a result whose stored current client ID does
not equal the returning client ID, so stale duplicate returns are normally
discarded.  It then rejects zero or non-whitelisted checksum prefixes at
lines 522--551.  For a result that passes those gates, however, it calls
set_complete at line 557 before comparing a previously stored checksum at
lines 563--565; it merely logs a mismatch and overwrites the value at line
567.  Lines 573--577 do the same for maximum offsets.  This is not Oliveira e
Silva's independent two-worker agreement-and-invalidation protocol.  The
server's verify-result utility reads the stored checksum and recomputes only
the trajectory maximum at the stored offset, not the entire work unit.
Accordingly, neither a completion bit nor that utility authenticates the
published range independently.

No complete server database, assignment bitmap, checksum ledger, overflow
ledger, or immutable result export was acquired.  The code audit proves what
the pinned programs do; it does not independently prove that every reported
work unit was executed correctly.

The deployment scripts select differing esieve, hesieve, and h2esieve maps
and options.  The acquired tests exercise selected work-unit identifiers
across configurations, but no exhaustive h/h2-specific regression suite was
located.  Nor does an immutable ledger bind each accepted unit to an exact
code tree, generated-map hash, binary, compiler, OpenCL implementation, and
returned checksum.  Those missing arrows are retained rather than replaced
by repository identity alone.

## Shortened and unshortened maximum excursions

Let

\[
 M_T(n)=\max_{j\geq0}T^j(n),\qquad
 M_U(n)=\max_{j\geq0}U^j(n)
\]

when the finite maxima exist.  For odd \(n>1\),

\[
 M_U(n)=2M_T(n).
\tag{F031.10}
\]

Indeed an odd shortened state \(x>1\) cannot be the shortened maximum because
\((3x+1)/2>x\).  A maximal shortened state cannot have an even predecessor,
since that predecessor would be twice as large.  Hence the maximal shortened
state is the output \(y=(3x+1)/2\) of an odd predecessor, and the unshortened
orbit contains the intermediate state \(2y\).  Every other omitted
unshortened state is twice some shortened state, so no value exceeds
\(2M_T(n)\).

No even \(n>2\) can be a new unshortened path record: the lower odd start
\(n-1\) has first image \(3n-2>n\).  Therefore the nontrivial record starts
are odd, and multiplication of all their maxima by the same factor two shows
that the shortened and unshortened conventions select the same record-start
sequence.  Their maximum values are not numerically identified.

The 2025 abstract says four new path records.  Section 6 calls five records
new and prints:

\[
\begin{split}
&274133054632352106267,\\
&1378299700343633691495,\\
&1735519168865914451271,\\
&1765856170146672440559,\\
&2358909599867980429759.
\end{split}
\]

The first value, \(274133054632352106267\), was already reported in the 2021
article on page 7.  The precise reconciliation is therefore four records new
since the earlier article and five cumulative project records in the 2025
list.  Section 6's phrase “five new” is imprecise; it is not an unexplained
five-versus-four mathematical contradiction, and neither wording is silently
rewritten.

The prediction that record maxima grow like \(n^2\) is heuristic.  Oliveira
e Silva explicitly says his data cannot distinguish \(O(n^2)\) from
\(O(n^2\log\log n)\).  Neither article's record plot proves a universal
quadratic bound.

## Roosendaal's modular maximum theorem

Roosendaal uses the unshortened map and calls the orbit maximum \(Mx(N)\).
His Theorem 4 has a valid bounded arithmetic proof:

> If \(N>2\) is odd, \(Mx(N)\) is finite, and
> \(Mx(N)>3N+1\), then \(Mx(N)\equiv16\bmod36\).

Let \(q=Mx(N)\).  It is even.  It cannot be \(2\bmod4\), because then
\(q/2\) is odd and its next unshortened image \(3q/2+1\) exceeds \(q\).
Since \(q>3N+1\), it is neither the initial state nor the first odd output,
and a maximum cannot be created by halving; hence \(q=3p+1\) for an odd
predecessor and \(q\equiv1\bmod3\).  The remaining residues modulo 36 are
4, 16, and 28.

If \(q=36a+4\), its forced preceding states are

\[
 12a+1,\quad24a+2,\quad48a+4,
\]

and the last exceeds \(q\).  If \(q=36a+28\), the forced preceding states
are

\[
 12a+9,\quad24a+18,\quad48a+36,
\]

again contradicting maximality.  Only \(16\bmod36\) remains.

Immediately afterwards the page says that all \(P_i\) are \(16\bmod36\).
That is a variable-name defect: the theorem and its proof concern
\(Mx(P_i)\), not the starting values \(P_i\).  The correction is proved,
not silently normalized.

The same page prints “for all \(N<1\)” in Conjecture 3 although the surrounding
definitions use \(N>1\).  It is retained as a source typo and is not used.
Theorems 2 and 3 on that page are expressly conditional on a residue bound;
they are not imported into the unconditional computational chronology.

## Oliveira e Silva's generalized maps

The chapter also defines

\[
 C_{5,\{2,3\}}(n)=
 \begin{cases}
  n/2,&n\equiv0\bmod2,\\
  n/3,&n\not\equiv0\bmod2,\ n\equiv0\bmod3,\\
  5n+1,&\gcd(n,6)=1,
 \end{cases}
\]

and analogously \(C_{7,\{2,3,5\}}\), dividing by the first applicable member
of \(\{2,3,5\}\) and otherwise applying \(7n+1\).  These are one-branch-per-
iterate maps.  Their clocks are not the shortened or unshortened 3x+1 clock.

For the 5x+1 map, the printed Proposition 2 asks
\(k_2(i,m_i)\), \(k_3(i,m_i)\), and \(k_5(i,m_i)\) to count the three
branch types in the first \(i\) iterates of \(m_i\), and then puts

\[
 r_i=2^{k_2(i,m_i)}3^{k_3(i,m_i)},\qquad
 n_0=r_i n_i+m_i,\qquad0\leq m_i<r_i.
\]

It prints \(m_i=n_0\bmod r_i\) and \(n_i=[n_0/r_i]\).  This circular
Euclidean coordinate is not merely awkward; it can fail to exist.  Already
for \(i=1,n_0=1\):

- if \(r_i=1\), its canonical remainder is \(m_i=0\), whose active branch is
  division by two and therefore demands \(r_i=2\);
- if \(r_i=2\), its canonical remainder is \(m_i=1\), whose active branch is
  \(5m_i+1\) and therefore demands \(r_i=1\);
- \(r_i=3\) also gives \(m_i=1\) and demands \(r_i=1\).

Thus no printed fixed point exists.  If one instead takes the branch counts
from \(n_0\), then \(r_i=1,m_i=0,n_i=1\), and the displayed identity would
read \(6=5\).  Proposition 2 is false as a literal Euclidean statement.

The following exact branch-cylinder coordinate repairs what the subsequent
implementation paragraph actually uses.  Set

\[
 a_i=n_0\bmod6^i,\qquad
 Q_i=\left\lfloor\frac{n_0}{6^i}\right\rfloor,\qquad
 (k_2,k_3,k_5)=\text{the first-\(i\) branch counts of }a_i,
\qquad
 R_i=2^{k_2}3^{k_3},
\]

and

\[
 N_i=\frac{n_0-a_i}{R_i}
 =\frac{6^i}{R_i}Q_i.
\]

Because \(R_i\mid6^i\), \(N_i\) is an integer.  Congruence modulo \(6^i\)
forces the same first \(i\) branch word for \(n_0\) and \(a_i\).  Here is the
exact induction.  If \(x\equiv y\pmod {6^j}\) with \(j\geq1\), then \(x\)
and \(y\) choose the same branch.  After a division by two their difference
is divisible by \(2^{j-1}3^j\), after a division by three it is divisible by
\(2^j3^{j-1}\), and after the \(5x+1\) branch it remains divisible by
\(6^j\).  In every case the images are congruent modulo \(6^{j-1}\).
Induction therefore gives the common length-\(i\) branch word.

For any fixed word \(w\) of length \(i\), with these counts, there is an
integer \(B_w\) such that every point in its branch cylinder satisfies

\[
 C_{5,\{2,3\}}^i(x)=\frac{5^{k_5}x+B_w}{R_i}.
\]

This follows recursively: a division branch multiplies the denominator by
two or three, while a \(5x+1\) branch replaces \(B_w\) by \(5B_w+R_i\).
Subtracting this formula for \(n_0\) and \(a_i\) now proves

\[
 C_{5,\{2,3\}}^i(n_0)
 =
 5^{k_5}N_i+C_{5,\{2,3\}}^i(a_i)
 =
 5^{k_5}\frac{6^i}{R_i}Q_i+C_{5,\{2,3\}}^i(a_i).
\tag{F031.11}
\]

The source itself notes the circularity and says that a finite table indexed
by \(n_0\bmod6^i\) is used.  Equation (F031.11) is the independently proved
coordinate forced by that implementation description.  The representative
\(a_i\) is a branch-cylinder representative, not in general the canonical
Euclidean remainder modulo \(R_i\); reducing it modulo \(R_i\) is legitimate
only after independently proving that the reduced representative retains the
same branch word.  Correspondingly, \(N_i\) is not silently identified with
\(\lfloor n_0/R_i\rfloor\).

The chapter defines \([x]\) as the “largest integer not smaller than \(x\),”
which is ceiling language.  Proposition 1 requires

\[
 n_i=\left\lfloor n_0/2^i\right\rfloor
\]

in its unique dyadic Euclidean decomposition.  The printed definition is
therefore a source defect there.  Replacing the bracket by a floor does not
repair Proposition 2; that proposition requires the distinct branch-cylinder
repair above.

For \(48n+17\), the chapter sorts the eight coefficient/intercept/iterate
columns as

\[
\begin{array}{c|rrrrrrrr}
 &1&2&3&4&5&6&7&8\\ \hline
\text{coefficient}&25&48&75&120&150&240&300&600\\
\text{intercept}&9&17&27&43&54&86&108&216\\
\text{iterate}&7&0&6&2&5&1&4&3.
\end{array}
\]

The fact that both numerical rows sort together was empirically checked only
for \(k_2\leq16\), \(k_3\leq8\).  It is not generalized without proof.

The 5x+1 pruning examined

\[
 2^{15}3^6=23887872
\]

residue classes and retained 92242.  The 7x+1 pruning retained 63507 of

\[
 2^8 3^4 5^3=2592000.
\]

Printed Theorems 2 and 3 report the finite inclusive ranges

\[
 n\leq10^{16}
\quad\hbox{and}\quad
 n\leq10^{14},
\]

respectively.  The source reports about five and two CPU-months on one
450 MHz Pentium III.  It does not say that the 3x+1 duplicate-worker
protocol was used for these two runs, so that protocol is not inferred.

Section 4 explicitly calls its Markov argument non-rigorous.  For the 5x+1
map it prints

\[
 P=\frac16
\begin{pmatrix}
3&0&0&3&0&0\\
6&0&0&0&0&0\\
0&3&0&0&3&0\\
0&2&0&2&0&2\\
0&0&3&0&0&3\\
0&0&6&0&0&0
\end{pmatrix},
\qquad
\pi=\frac1{27}(8,4,4,6,2,3),
\]

and expansion factors

\[
 (1/2,5,1/2,1/3,1/2,5).
\]

The passage from a Chernoff upper bound to the asymptotic equality in its
equation (21) is conjectural.  Therefore

\[
 \rho_5\approx1.442762198279,\qquad
 \rho_7\approx2.215508001593
\]

remain conjectured record-growth exponents supported by finite data.

## Defect and repair ledger

1. **Oliveira floor sentence and Proposition 2.**  The print says largest
   integer not smaller; Proposition 1 forces the floor.  Proposition 2's
   circular Euclidean coordinate has no solution already at \(i=1,n_0=1\);
   it is replaced by the independently proved \(6^i\)-branch-cylinder
   coordinate (F031.11), not by silent floor substitution.
2. **Barina pseudocode at one.**  The 2021 Algorithm 1 and both 2025
   algorithms have the strict-loop defect.  The 2021 Algorithm 2 terminates
   but gives the wrong conventional delay without a base case.  The cases are
   not collapsed.
3. **Barina live-sieve wording.**  Live means no implemented finite
   certificate, not mathematical nonconvergence.
4. **Uniform coefficient equality.**  The code's is_convergent omits the
   safe \(L=0,R>0\) case.  This is conservative.
5. **Recursive v3 lift.**  The source tests only the low predecessor and does
   not expose the coefficient invariants (F031.9)--(F031.9b).  F031 proves
   them for every candidate in the finite \(k\leq34\) implementation domain;
   the unbounded invariant remains open.
6. **Zero predecessor expression.**  Unsigned \((L_{\rm last}-1)/2\) wraps at
   residue zero.  It does not clear zero, but it has no integer-predecessor
   interpretation.
7. **Packed domain.**  The effective \(k\leq34\) limit is an assertion on the
   packed 34-bit residue field, not a function precondition; disabling the
   assertion outside the domain permits aliasing.
8. **LP64 portability.**  ctzu64 traps when unsigned long is not 64 bits.
9. **Congruence-class cardinality.**  The 2025 prose exchanges the number of
   classes \(2^k\) with the starts per class \(2^{40-k}\); the older paper and
   code use the latter.
10. **Generator historical argument.**  The faulty fourth argument in the
   2020--2023 SAVE_MEMORY source interval is recorded with its fixing commit
   and is not assigned to blobs outside that interval.
11. **Four versus five records.**  The first of the five was already in 2021;
   the exact reading is five cumulative and four post-2021 records.
12. **Publisher versus FIT coordinate.**  Article number 810 controls over
   FIT's no. 1, pp. 1--14 rendering.
13. **Server duplicate order.**  A stale client-ID mismatch is rejected, but
    an accepted result is marked complete before checksum comparison and a
    mismatch is logged and overwritten rather than invalidated.
14. **GPU multiprecision wording.**  GPU-to-CPU-to-GMP is possible only when
    a GMP-enabled CPU worker was actually built; GPU-only scripts do not
    establish that fallback.
15. **Optional GPU barrier.**  kernel32-precalc.cl can diverge immediately
    before a work-group barrier.  This bounds that optional/test variant, not
    the default kernel32.cl symlink target.
16. **Roosendaal maximum variable.**  The congruence is for \(Mx(P_i)\), not
    for \(P_i\).
17. **Roosendaal Conjecture 3 domain.**  The printed \(N<1\) is incompatible
    with the surrounding \(N>1\) definitions and is not used.
18. **Dynamic status.**  The 28 August 2026 API snapshot is not backdated
    into the 2025 article.

## Dependency graph and nonclaims

The exact dependency order is:

\[
\begin{gathered}
\text{map definitions and clock bridges}\\
\Downarrow\\
\text{block map and dyadic affine-prefix identity}\\
\Downarrow\\
\text{finite descent/coalescence/predecessor certificates}\\
\Downarrow\\
\text{ascending-order induction}\\
\Downarrow\\
\text{a finite convergence conclusion, if the reported work ledger and
implementation execution are accepted}.
\end{gathered}
\]

The final implication is not reversible.  Source code without the completed
ledger does not prove that the run occurred; a status page without the code
does not prove the algorithm; and a finite bound does not prove universal
convergence.

In particular:

- \(20\cdot2^{58}\), \(2^{68}\), \(87\cdot2^{60}\), \(2^{71}\), and
  \(2075\cdot2^{60}\) are distinct dated coordinates;
- shortened and unshortened clocks are not numerically identified;
- shortened and unshortened maximum values differ by the proved factor two
  on odd starts even though record-start order agrees;
- checksum equality is not a cryptographic certificate;
- measured speed is not asymptotic complexity or universal optimality;
- a live sieve bit is not a counterexample;
- the generalized 5x+1 and 7x+1 computations do not prove their universal
  conjectures;
- conjectured record-growth exponents are not endpoint theorems; and
- none of the finite verification results proves the Collatz conjecture.

## Formal and certificate boundary

F031's deterministic certificate pins the manifestations, repository
commits, tree identities, bundles, selected compressed maps, and frozen route
artifacts.  It checks the \(T/T_1\) bridges, the block map and its fibres, the
dyadic affine-prefix identity, the exact uniform-descent criterion, all four
lower-predecessor transports, the Oliveira coalescence identity, the
complete finite \(k\leq34\) recursive-coefficient reduction, the printed
Proposition 2 counterexample and corrected \(6^i\) branch-cylinder coordinate,
the shortened/unshortened maximum bridge on a finite domain, exact bound
arithmetic, finite sieve-generation kernels, and the pinned code-order and
deployment distinctions recorded above.

Those checks are finite certificates of the specified algebra and source
pins.  They do not certify:

- any completed historical distributed run;
- the full \(2^{34}\) or \(2^{24}\) generated map independently of its pinned
  compressed artifact;
- any recursive v3 coefficient invariant beyond the certified \(k\leq34\)
  exponent domain;
- the reliability of hardware, compilers, networks, or the live server;
- the non-rigorous Markov asymptotics;
- any universal convergence statement.

All global proof obligations remain open.  F031 advances the literature spine
and supplies exact computational coordinates; it is not a completion claim.
