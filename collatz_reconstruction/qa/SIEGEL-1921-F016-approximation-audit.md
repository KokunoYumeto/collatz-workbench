# C. L. Siegel 1921: approximation of algebraic numbers

## Identity and controlling extract

- Carl Ludwig Siegel, “Approximation algebraischer Zahlen,”
  *Mathematische Zeitschrift* 10 (1921), no. 3–4, 173–213.
- DOI: `10.1007/BF01211608`.
- Official GDZ full-volume scan:
  `https://gdz.sub.uni-goettingen.de/download/pdf/PPN266833020_0010/PPN266833020_0010.pdf`.
- The article occupies full-volume PDF pp. 184–224, corresponding to printed
  pp. 173–213.
- Controlling exact article extract:
  `external_literature/dependency_gate_2026-08-25/siegel_1921_approximation_algebraischer_zahlen_gdz_extract.pdf`.
- Extract size: 3,334,564 bytes; 41 pages.
- Extract SHA-256:
  `309cd862fa24f173c7e17fb86db5f082f0c8ad8b89762dd4ddf8d0d4c0dcdc4f`.
- Full-volume acquisition hash:
  `cb8f6738638627da89e24d07812632ecc5699aed3a3f335851e85e7de90b75e9`
  for 20,773,778 bytes and 333 PDF pages.
- Exact-title, DOI, Carl-Siegel, and Thue–Siegel searches missed the frozen
  ledgers; targeted authorized-root filename searches also missed.  No
  frozen ledger was changed.
- The complete article was inspected for the proof route.  The exact theorem
  pages were independently rerendered at 300 dpi and checked at original
  detail.

## Exact rational-approximation statement

Printed p. 174 / full PDF p. 185 / extract p. 2 states that for an algebraic
number \(\xi\) of degree \(n\geq2\) and \(\epsilon>0\), there is a positive
constant \(a_3=a_3(\xi,\epsilon)\) such that

\[
 \left|\xi-\frac{x}{y}\right|
 >\frac{a_3}{y^{\kappa_n+\epsilon}},
 \qquad
 \kappa_n=\min_{1\leq\lambda\leq n}
 \left(\frac n{\lambda+1}+\lambda\right),
\]

for rational integers \(x,y\) with \(y>0\).  The constant is positive; it
is not asserted to be an integer and is not made numerically effective.

The Hauptsatz, Satz 1, begins on printed p. 178 / extract p. 6 in height
language.  For an algebraic integer \(\xi\) of degree \(n\), natural numbers
\(h,s\) with \(s<n\), and \(\Theta>0\), the second part gives only finitely
many degree-\(h\) algebraic \(\eta\) satisfying the corresponding
\(H(\eta)^{-h(n/(s+1)+s)-\Theta}\) approximation.  Auxiliary height,
Wronskian, polynomial, and norm lemmas occupy printed pp. 175–188; the final
Hauptsatz proof runs from printed p. 188 through p. 191.  Zusätze 1–3 on
printed p. 191 / extract p. 19 turn finiteness into a uniform positive
constant and extend the theorem from integral to arbitrary algebraic
\(\xi\).

The apparent range difference \(1\leq s<n\) versus the introductory minimum
through \(n\) is harmless: the endpoint \(s=n\) cannot minimize, since
\(n+n/(n+1)>n\), while the value at \(s=1\) is \(n/2+1\leq n\).

For a reduced rational \(p/q\), Siegel's height is
\(H(p/q)=\max(|p|,q)\).  If \(|\xi-p/q|<1\), then
\(H(p/q)\leq Cq\) for \(C=\max(1,|\xi|+1)\); if the error is at least one,
a smaller fixed constant handles it.  Thus the height theorem yields the
displayed denominator theorem.  For an unreduced \(x/y\), reduction gives
\(q\leq y\), preserving the lower bound after replacing \(q\) by \(y\).

## Exact use in the Pillai repair

For integer \(t\geq1\), define

\[
 m(t)=\min_{1\leq\lambda\leq t}
 \left(\frac t{\lambda+1}+\lambda\right).
\]

This function is nondecreasing.  For every old candidate
\(1\leq\lambda\leq t\), increasing \(t\) to \(t+1\) raises its value by
\(1/(\lambda+1)\); the new candidate \(\lambda=t+1\) is larger than the old
value at \(\lambda=1\).  Consequently an algebraic number of actual degree
\(d\leq r\) receives the at-least-as-strong exponent
\(m(d)\leq m(r)\).  Degree one is handled by exact rational separation.

This proves that Pillai's false full-degree assertion is repairable without
enlarging Siegel's theorem.  The repaired factorization and residue argument
is separately attributed to this edition in the Pillai audit and TeX text.

## Nonclaims

- The source does not state a positive integer approximation constant.
- No effective numerical value for the constant or Pillai threshold is
  extracted.
- Siegel's theorem alone does not prove Pillai's residue-class reduction;
  the actual-degree, rational, and constant-absorption steps remain separate.
- The theorem does not by itself prove Herschfeld's uniqueness statement or any
  Collatz endpoint.
