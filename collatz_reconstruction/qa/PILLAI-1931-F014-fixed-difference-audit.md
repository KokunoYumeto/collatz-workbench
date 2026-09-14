# Pillai 1931: fixed differences of powers

## Identity and controlling witness

- Author: S. Sivasankaranarayana Pillai.
- Title: “On the Inequality \(0<a^x-b^y\leq n\).”
- Journal identity: *Journal of the Indian Mathematical Society* 19
  (1931), 1–11.
- Controlling local witness:
  `external_literature/dependency_gate_2026-08-25/pillai_1931_inequality_google_drive_witness.pdf`.
- Witness size: 228,119 bytes.
- SHA-256:
  `dd4ef9acb06352fad2913baa6b6d4ab854fd9689e2f6c13910bf99573f84ee69`.
- Manifestation boundary: this is an eleven-page scan, not a publisher-hosted
  download.  Its title, author, journal pagination, and complete page sequence
  agree with the exact entries in authoritative Pillai and journal
  bibliographies.  That agreement authenticates the article content but is
  not represented as a publisher-download provenance claim.
- Routing history: exact searches of the completed frozen route ledgers for
  Pillai, the journal identity, the page range, and the displayed equation
  returned no matching route.  A targeted filename repair in the authorized
  literature roots also missed.  No frozen ledger was rescanned or mutated.
- Reading control: all eleven printed pages were rendered at 300 dpi and read
  visually.  OCR was used only as a search aid because it corrupts symbols.

## Exact source programme

Printed p. 1 states three results.  Theorem I fixes positive integers
\(m,n,a,b,c\) and a positive number \(\delta\), although \(c\) is unused in
the theorem.  Subject to \(\log m/\log n\) being irrational, it asserts a
threshold \(x(\delta)\) such that

\[
 a m^x-b n^y>m^{x(1-\delta)}
\]

whenever \(x>x(\delta)\) and \(a m^x>b n^y\).  The surrounding introduction
and later corollaries work with positive integral exponents; the isolated
phrase “all integral values” is not silently enlarged here to arbitrary
negative exponents.

Theorem II gives a power-versus-\(r\)-th-power lower bound.  Theorem III
counts solutions, including zero exponents, of
\(0<n^x-m^y\leq a\).  Printed pp. 6–11 prove the counting result and its
Pólya-number analogue.  Those later asymptotics are recorded as part of the
paper's programme but are not needed for Crandall's citation.

Printed p. 2 explains that the motivating equation
\(m^x-n^y=a\) has finitely many positive integral solutions and identifies
that qualitative fact as a special case of Pólya's 1918 fixed-prime gap
theorem.  The page then quotes Siegel's rational-approximation exponent

\[
 m(d)=\min_{1\leq\lambda\leq d}
 \left(\frac d{\lambda+1}+\lambda\right).
\]

Printed pp. 3–4 derive Lemma 1 and Theorem I.  Corollary 1 on printed p. 4
states that, for \(c>0\),

\[
 a m^x-b n^y=c
\]

has only finitely many solutions.  This is the positive-exponent,
nonzero-difference source statement behind Crandall reference 9; swapping the
bases handles the negative sign, while zero exponents, negative exponents,
and (z=0) require the separate crosswalk below.

## Source defects and omitted cases

1. Printed p. 2 calls Siegel's constant a “positive integer.”  Siegel states
   only a positive real constant.  An integer lower-bound constant is
   generally impossible; for example \(\xi=\sqrt2\) and \(x=y=1\) already
   give an error less than one.
2. Printed p. 3 puts \(\alpha=(a/b)^{1/n}\) and asserts that \(\alpha\) has
   degree \(n\) because \(a,b\) are not both perfect \(n\)-th powers.  This
   is false.  For \(a=4,b=1,n=4\), \(\alpha=\sqrt2\) has degree two; for
   \(a=b=2,n=2\), \(\alpha=1\) has degree one although neither coefficient
   is a square.
3. The next paragraph writes \(y=\ell x\) with only an upper bound on
   \(\ell\), then treats \(y^{n-1}\) as uniformly comparable with
   \(x^{n-1}\).  The missing lower bound requires a case split.
4. Printed p. 4 applies Lemma 1 to every residue pair
   \(x=rs+h,y=rt+\ell\) without checking the lemma's “not both perfect
   \(r\)-th powers” hypothesis.  When the outer coefficients are one and
   \(h=\ell=0\), both resulting coefficients are one.
5. The letters \(\epsilon\) and \(\delta\) are interchanged in Lemma 1, and
   the last displayed exponent introduces both losses without an explicit
   allocation.  Fixed constants are absorbed without a quantified threshold.
6. Theorem I lists an unused positive integer \(c\).
7. Printed p. 6 says an equation has “only infinite number of solutions” in
   the proof of Corollary 5.  Corollary 4 and the surrounding deduction
   require “only finite number”; the printed word is retained as a source
   defect, not silently quoted as mathematics.

These defects invalidate the literal displayed derivation.  They do not
invalidate the qualitative fixed-difference result: Pólya supplies an
independent primary proof route, and the quantitative argument admits the
separately attributed repair below.  Pólya's explicit Thue dependency has now
been read at its exact irreducible/reducible binary-cubic boundary; see
`qa/THUE-1908-1909-F017-binary-form-audit.md`.

## Exact repair boundary

Let \(r\geq2\), \(A,B\in\mathbb N_{>0}\),
\(\alpha=(A/B)^{1/r}\), and
\(d=[\mathbb Q(\alpha):\mathbb Q]\leq r\).  For positive integers \(X,Y\)
with \(AX^r>BY^r\), factor exactly:

\[
 AX^r-BY^r
 =B(\alpha X-Y)
   \sum_{j=0}^{r-1}(\alpha X)^{r-1-j}Y^j.
\]

If \(d\geq2\), Siegel at the actual degree gives, for every \(\eta>0\),
\(|\alpha-Y/X|>cX^{-m(d)-\eta}\).  The function \(m(q)\) is nondecreasing
in the integer degree \(q\), so \(m(d)\leq m(r)\).  Retaining the first
positive summand in the factorization gives

\[
 AX^r-BY^r>C X^{r-m(r)-\eta}.
\]

If \(d=1\), write \(\alpha=P/Q\) in lowest terms.  Strict positivity gives
\(PX-QY\geq1\), hence \(\alpha X-Y\geq1/Q\); the same factorization gives
the stronger order \(X^{r-1}\).  Thus neither the full-degree assertion nor
the “not both powers” hypothesis is needed.

Applying this repaired lemma to the finitely many residue pairs
\(x=rs+h,y=rt+\ell\), taking the minimum of their positive constants and
the maximum of their thresholds, and then absorbing the bounded residues and
constant into a strictly reserved exponent margin proves Pillai's Theorem I.
For example, first replace the requested \(\delta\) by
\(\delta_0=\min(\delta,1/2)\); choose \(r\) with
\(m(r)/r<\delta_0/2\).  This choice is explicit: for
\(k=\lceil\sqrt r\rceil\) and \(\lambda=k-1\),
\(m(r)\leq r/k+k-1<2\sqrt r\), so any integer
\(r>(4/\delta_0)^2\) suffices.  Run the lemma with
\(\eta/r<\delta_0/4\); and reserve the remaining
\(\delta_0/4\) to absorb every fixed coefficient and residue.  This is an
edition proof, not text attributed to Pillai.

## Crandall crosswalk

For \(z\in\mathbb Z\), any solution in arbitrary integer exponents of
\(2^x-3^y=z\) actually has \(x,y\geq0\): a negative exponent in only one
coordinate leaves an uncancelled denominator divisible by two or three; if
both are negative, the absolute value is strictly less than one and cannot
be an integer, while equality to zero is excluded by unique factorization.

For \(z\neq0\), Pólya's theorem for the ordered \(\{2,3\}\)-smooth integers
implies finiteness: two such integers at fixed distance \(|z|\) cannot both
lie beyond the point where every adjacent smooth-number gap exceeds
\(|z|\).  For \(z=0\), unique factorization gives only
\((x,y)=(0,0)\).  This proves exactly Crandall's unrestricted-integer wording.

## Nonclaims

- Pillai's theorem alone does not prove Herschfeld's eventual uniqueness;
  the latter additionally requires the two order coordinates and the
  two-solution growth argument audited in
  `qa/HERSCHFELD-1936-F018-eventual-uniqueness-audit.md`.
- Neither Pillai nor the repaired argument supplies an effective numerical
  threshold from Siegel's qualitative constant.
- Fixed-difference finiteness gives no bound uniform in \(z\).
- The result does not prove the Collatz conjecture, exclude nontrivial
  Collatz cycles, or turn Crandall's conditional primitive-root paragraph
  into an unconditional theorem.
