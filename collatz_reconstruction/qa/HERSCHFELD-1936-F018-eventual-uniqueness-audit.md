# Herschfeld 1936: eventual uniqueness of a fixed power difference

## Identity and controlling witness

- Author: Aaron Herschfeld.
- Title: “The equation \(2^x-3^y=d\).”
- Journal identity: *Bulletin of the American Mathematical Society* 42
  (1936), no. 4, 231–234.
- DOI: `10.1090/S0002-9904-1936-06275-0`.
- Controlling local witness:
  `external_literature/dependency_gate_2026-08-25/herschfeld_1936_equation_2x_minus_3y_equals_d_ams.pdf`.
- Witness size: 299,845 bytes; four PDF pages.
- SHA-256:
  `1259b633643db5d7e2468cbd578d72443a4bdc29a8ce0d85a57e0cbcb8ac2d3a`.
- Retrieval identity: official AMS article PDF at
  `https://www.ams.org/journals/bull/1936-42-04/S0002-9904-1936-06275-0/S0002-9904-1936-06275-0.pdf`.
- The first physical PDF page contains the tail of the preceding article
  above Herschfeld's title.  The Herschfeld article itself is complete at
  printed pp. 231–234.
- Crandall reference 10 misspells the surname “HERSCHEFELD.”  The primary
  title and byline read **HERSCHFELD**.
- Routing history: exact searches of the immutable route ledgers for both
  spellings, the title, journal, year, and pagination returned no route.  A
  targeted filename search in the authorized literature roots also missed.
  Only the identified primary article was then acquired; no frozen ledger
  was rebuilt or mutated.
- Reading control: all four pages were rendered at 300 dpi and read visually.
  The PDF raster controls formulas because its OCR corrupts exponents.

## Exact source programme

Herschfeld works with positive integral exponents.  Printed p. 232 first
recalls fixed-difference finiteness and then announces the main theorem:

\[
 \exists D>0\ \forall d\in\mathbb Z,
 \qquad |d|>D\Longrightarrow
 \#\{(x,y)\in\mathbb N_{>0}^2:2^x-3^y=d\}\leq1.
\]

The parameter is the two-sided quantity \(|d|\), not only large positive
\(d\).  The source also solves the six possible nonzero differences with
\(|d|\leq10\):

\[
\begin{array}{c|c}
d&(x,y)\\ \hline
-1&(1,1),(3,2)\\
-5&(2,2)\\
-7&(1,2)\\
1&(2,1)\\
5&(3,1),(5,3)\\
7&(4,2).
\end{array}
\]

The remaining values in that interval are excluded by parity.  The paper
then reports an unpublished computation for \(|d|\leq100\).  That report is
not used as a theorem or certificate here.

The final paragraph treats the separate general equation
\(a^x-b^y=d\).  It reports at most nine positive-integer solutions for
sufficiently large \(|d|\), reducing the nine exponent classes modulo three
to cubic equations and citing C. L. Siegel's 1929 paper.  This is a distinct
dependency.  It is not needed for the \((2,3)\) theorem and is not admitted
until the exact Siegel theorem and coefficient hypotheses have been read.

## Dependency substitution: repaired Pillai theorem

Printed p. 233 invokes the quantitative property that, for each
\(0<\delta<1/2\), there are thresholds \(x_1=x_1(\delta)\) and
\(y_1=y_1(\delta)\) such that

\[
 0<2^u-3^v\Longrightarrow
 2^u-3^v>2^{u(1-\delta)}\quad(u>x_1),
\]

and

\[
 0<3^v-2^u\Longrightarrow
 3^v-2^u>3^{v(1-\delta)}\quad(v>y_1).
\]

Herschfeld cites Pillai's 1931 theorem.  Pillai's literal derivation contains
the defects recorded in `qa/PILLAI-1931-F014-fixed-difference-audit.md`.
The edition has already proved the same quantitative statement without
those defects by applying Siegel's approximation theorem at the actual
algebraic degree, treating degree one by rational separation, retaining the
exact difference-of-powers factorization, and taking a finite minimum over
residue classes.  Herschfeld's proof is therefore admitted with that repaired
theorem as its dependency.  No effective value of either threshold follows.

For a selected \(0<\delta<1/2\), the printed proof permits

\[
 D=\max\{2^{x_1+5},3^{y_1+2}\}.
\]

This is an exact quantified threshold description, not a numerical bound.

## Exact order coordinates

For every \(r\geq1\),

\[
 \operatorname{ord}_{3^r}(2)=2\cdot3^{r-1}.
\]

An exponent giving one modulo \(3^r\) is even, say \(n=2m\), and LTE gives

\[
 v_3(2^{2m}-1)=v_3(4^m-1)=1+v_3(m).
\]

Thus \(3^r\mid2^n-1\) exactly when \(2\cdot3^{r-1}\mid n\).

For every \(r\geq3\),

\[
 \operatorname{ord}_{2^r}(3)=2^{r-2}.
\]

An odd exponent is not one modulo eight; for even \(n\), LTE gives

\[
 v_2(3^n-1)=v_2(3-1)+v_2(3+1)+v_2(n)-1=2+v_2(n).
\]

Hence \(2^r\mid3^n-1\) exactly when \(2^{r-2}\mid n\).  Herschfeld's older
phrase that “3 belongs to \(2^{r-2}\) modulo \(2^r\)” means this order
identity.

## Complete positive-exponent proof

Suppose two distinct solutions have the same \(d\).  Relabel so that
\(X>x\).  Then

\[
 2^X-2^x=3^Y-3^y>0,
\]

so necessarily \(Y>y\).  This simultaneous ordering is a lossless map on
the unordered two-element solution set.  Factoring gives

\[
 2^x(2^{X-x}-1)=3^y(3^{Y-y}-1),
\]

and coprimality gives the two exact congruences

\[
 2^{X-x}\equiv1\pmod{3^y},\qquad
 3^{Y-y}\equiv1\pmod{2^x}.
\]

Consequently

\[
 X-x\geq2\cdot3^{y-1},
 \qquad
 Y-y\geq2^{x-2}\quad(x>2).
\]

For \(d>2^{x_1+5}\), the smaller solution satisfies
\(d=2^x-3^y<2^x\), hence \(x>x_1+5>5\).  Therefore

\[
 2^X=3^Y+d>3^Y
 \geq3^{2^{x-2}}>2^{2^{x-2}},
 \qquad X>2^{x-2}>2x.
\]

Applying the repaired Pillai theorem to the larger solution gives

\[
 d=2^X-3^Y>2^{X(1-\delta)}>2^{X/2}>2^x>d,
\]

a contradiction.

For \(d<0\) and \(|d|>3^{y_1+2}\), the smaller solution satisfies
\(|d|=3^y-2^x<3^y\), hence \(y>y_1+2>2\).  Now

\[
 3^Y=2^X-d>2^X
 \geq2^{2\cdot3^{y-1}}>3^{3^{y-1}},
 \qquad Y>3^{y-1}>2y.
\]

The repaired theorem with the bases exchanged gives

\[
 |d|=3^Y-2^X>3^{Y(1-\delta)}>3^{Y/2}>3^y>|d|,
\]

again a contradiction.  The elementary comparisons used are exact:
\(2^{x-2}>2x\) for \(x>5\) and \(3^{y-1}>2y\) for \(y>2\).

## Constructive extension to Crandall's integer domain

The same proof works on \(\mathbb N_0^2\).  If \(d>0\), the smaller
solution still has \(d<2^x\), so \(x>5\); the proof uses only the order of
3 modulo \(2^x\).  It permits \(y=0\), and the larger pair has positive
coordinates when the repaired Pillai theorem is invoked.  If \(d<0\), the
smaller solution still has \(|d|<3^y\), so \(y>2\); the proof uses only the
order of 2 modulo \(3^y\).  It permits \(x=0\), and again the larger pair is
positive.  Thus the same \(D\) gives at most one nonnegative-exponent
solution.

For an integer value \(d\), every integer-exponent solution already has
nonnegative exponents.  If \(x=-a<0\) and \(y\geq0\), then

\[
 2^x-3^y=\frac{1-2^a3^y}{2^a}
\]

has odd numerator.  If \(x\geq0\) and \(y=-b<0\), then

\[
 2^x-3^y=\frac{3^b2^x-1}{3^b}
\]

has numerator congruent to \(-1\) modulo three.  If both exponents are
negative, the nonzero difference

\[
 \frac{3^b-2^a}{2^a3^b}
\]

has absolute value below one.  Therefore none is an integer.  Combining
this exponent-domain injection with the nonnegative proof gives the
separately attributed edition theorem

\[
 |d|>D\Longrightarrow
 \#\{(x,y)\in\mathbb Z^2:2^x-3^y=d\}\leq1.
\]

This is not silently attributed to Herschfeld.  It is the exact morphism from
his positive-exponent theorem to Crandall's all-integer wording, with the
zero-coordinate cases proved inside the extension.

## Source defects and nonclaims

1. Printed p. 232 says “equation (1)” at the end of a congruence argument
   that visibly concerns the specialized equation (2).  No mathematical
   ambiguity remains, but the label defect is not silently normalized.
2. The \(|d|\leq100\) calculation is only reported from an unpublished
   paper and supplies no checked certificate here.
3. The general \(a^x-b^y=d\) at-most-nine theorem has a separate Siegel-1929
   dependency and is not used in the specialized theorem.
4. Eventual uniqueness is ineffective and supplies no uniform formula for
   the sole solution, no fixed-\(d\) effective search bound, and no Collatz
   endpoint or cycle exclusion.
5. Fixed-difference finiteness and eventual uniqueness are distinct claims;
   neither was inferred from the other.

The deterministic finite kernel is
`certificates/herschfeld_1936_checks.py`; the infinite theorem is controlled
by the primary source, the repaired Pillai theorem, and the complete proof
above.
