# Pólya 1918: gaps between integers supported on fixed primes

## Identity and witness

- Georg Pólya, “Zur arithmetischen Untersuchung der Polynome,”
  *Mathematische Zeitschrift* 1 (1918), no. 2–3, 143–148.
- DOI: `10.1007/BF01203608`.
- Received 4 August 1917.
- Official SUB Göttingen/GDZ witness:
  `external_literature/dependency_gate_2026-08-25/polya_1918_zur_arithmetischen_untersuchung_der_polynome_gdz.pdf`.
- PDF size: 428,068 bytes; seven pages, comprising the repository cover and
  journal pp. 143–148.
- SHA-256:
  `4b067f72cff9598a0ee37924793d28ea67ed58bc7ca14ca149e5c4bed599ff5f`.
- Official direct PDF:
  `https://gdz.sub.uni-goettingen.de/download/pdf/PPN266833020_0001/LOG_0020.pdf`.
- Exact-title, author, journal, and Pólya searches missed the frozen route
  ledgers; targeted searches of the authorized literature roots also missed.
  The ledgers remained immutable.
- Every article page was rendered at 300 dpi and read visually.

## Exact theorem and proof route

Satz I, printed p. 144 / PDF p. 3, says that if a rational polynomial is the
product of two rational linear factors that are not scalar multiples, the
largest prime divisor of its value at \(n\) tends to infinity with \(n\).
Printed pp. 144–145 prove this using Thue's finiteness theorem for binary
forms.  Assuming an infinite sequence of values supported on finitely many
primes, Pólya reduces both exponent vectors modulo three, fixes a residue
vector by pigeonhole, writes the two linear values as fixed coefficients
times cubes, eliminates \(n\), and obtains a fixed nonzero binary cubic
equation.  The cubic is not the cube of a linear form, contradicting the
quoted Thue theorem.  Pólya gives the exact dependency locators Thue III,
Theorem IV, p. 303; Thue II, p. 3; and Thue I, Satz 12, p. 30.  The primary
dependency audit is now recorded in
`qa/THUE-1908-1909-F017-binary-form-audit.md`.  Thue III alone would not
cover every residue cell because the cubic can be reducible; Thue II's
exceptional-form classification is the controlling route.  The exact
coefficient comparison proves that Pólya's cubic is not a scalar linear cube.

Section 4, printed pp. 147–148 / PDF pp. 6–7, equations (12)–(14), is the
form quoted by Pillai.  Fix distinct primes \(p_1,\ldots,p_r\), \(r\geq2\),
and order every

\[
 p_1^{x_1}\cdots p_r^{x_r},
 \qquad x_i\in\mathbb Z_{\geq0},
\]

as \(a_0<a_1<a_2<\cdots\).  Then

\[
 \lim_{n\to\infty}(a_{n+1}-a_n)=\infty.
\]

Pólya proves this equivalent to Satz I: a bounded liminf gap \(k\) would
contradict Satz I for \(x(x+k)\), while proving Satz I for those polynomials
suffices for the gap assertion.

## Exact fixed-difference consequence

Let \(S\) be a finite set of at least two primes and enumerate the positive
\(S\)-smooth integers increasingly.  For each fixed nonzero integer \(c\),
only finitely many ordered pairs of \(S\)-smooth integers differ by \(c\).
Indeed, beyond the index where every adjacent gap exceeds \(|c|\), two
distinct terms cannot have difference \(|c|\), since their difference is a
sum of one or more adjacent positive gaps.  If \(|S|=1\), the same conclusion
is elementary from \(p^{j+1}-p^j\to\infty\).

Taking \(S\) to contain the prime divisors of fixed \(M,N>1\) proves that
\(M^x-N^y=c\), \(x,y\geq0\), has finitely many solutions for fixed
\(c\neq0\).  In particular \(S=\{2,3\}\) supplies the qualitative result
Crandall needs independently of Pillai's defective quantitative derivation.

## Boundaries

- The gap theorem is qualitative and supplies no effective threshold here.
- It does not cover \(c=0\); multiplicatively dependent bases can have
  infinitely many zero-difference solutions.  The \(2,3\) case is handled
  separately by unique factorization.
- It is stated for nonnegative prime exponents.  Arbitrary negative exponents
  require the separate denominator obstruction proved in the edition.
- It proves fixed-difference finiteness, not Pillai's quantitative lower bound
  and not Herschfeld's eventual uniqueness.
- The published gap theorem is admitted at its printed scope.  Its explicit
  Thue dependency has now been read and reconstructed at the exact
  irreducible/reducible-form boundary.  No effective Thue bound is claimed.
- Both located primary scans of Thue II omit printed pp. 2--3.  Pólya's p. 3
  locator is not represented as visually verified; the equivalent Thue II
  p. 1 theorem, Pólya's exact quotation, and the supplementary faithful
  translation control that manifestation gap.
