# BERNSTEIN-1994-F007 — inverse parity map and rational-image audit

## Status and controlling witnesses

This is a content-level audit of Daniel J. Bernstein, *A Non-Iterative
2-Adic Statement of the 3N+1 Conjecture*, Proceedings of the American
Mathematical Society **121** (1994), no. 2, 405--408.  It resolves the exact
Bernstein dependency cited by Laarhoven--de Weger; it does not enlarge the
Collatz conjecture.

- official AMS record:
  `https://www.ams.org/journals/proc/1994-121-02/S0002-9939-1994-1186982-9/`
- official AMS DOI: `10.1090/S0002-9939-1994-1186982-9`
- official local witness:
  `external_literature/dependency_gate_2026-08-25/bernstein_1994_ams_official.pdf`
- AMS PDF pages: `4`
- AMS PDF bytes: `338805`
- AMS PDF SHA-256:
  `6b17ddffb41416fb04dc0cba487a9c042a1186f40ae1a5d330b83f96770a3562`
- author record: `https://cr.yp.to/papers.html#231`
- author witness:
  `external_literature/dependency_gate_2026-08-25/bernstein_1994_author.pdf`
- author PDF bytes: `137610`
- author PDF SHA-256:
  `c0b063872fc36411218831742adedecdec0b6e84a047dc083abf0ff68ae6c2f8`

All four printed pages of the official AMS witness were visually read.  The
author witness independently agrees at every formula used here.  The AMS PDF
text extraction is not allowed to control formulas because its embedded font
mapping corrupts symbols.

The official identity is received 13 July 1992, revised 30 September 1992,
communicated by William Adams, and published in June 1994.  The correct AMS
article identifier is `1186982-9`; `1185247-1` is not this article.

## Exact inverse orientation and clock

On printed pp. 405--406, Eqs. (1)--(2), Bernstein writes a 2-adic integer as

\[
 Q=\sum_{i\geq0}2^{d_i},
 \qquad 0\leq d_0<d_1<\cdots,
\]

and defines

\[
 \Phi_B(Q)
 =-\sum_{i\geq0}\frac{2^{d_i}}{3^{i+1}}=N.
\]

The finite and infinite one-position expansions give bijections on
\(\mathbb Z_2\).  Printed p. 407 explicitly identifies

\[
 \Phi_B=Q_\infty^{-1}.
\]

Thus Bernstein's \(\Phi_B\) has the same orientation as the later
Bernstein--Lagarias \(\Phi_3\), and the opposite orientation to
Laarhoven--de Weger's \(\Phi\), which is the chronological parity encoder
\(Q_\infty=Q_3\).

Printed p. 406, Theorem 1, uses the unshortened maps

\[
 C(N)=
 \begin{cases}
 N/2,&N\equiv0\pmod2,\\
 3N+1,&N\equiv1\pmod2,
 \end{cases}
 \qquad
 H(Q)=
 \begin{cases}
 Q/2,&Q\equiv0\pmod2,\\
 Q-1,&Q\equiv1\pmod2,
 \end{cases}
\]

and proves \(C\Phi_B=\Phi_BH\).  This is not literally the shortened
\(T/S\) conjugacy equation: after an odd \(C\)-step the forced even step must
first be compressed.  No inference below crosses that clock boundary without
performing this compression.

## Positive-integer conjecture: exact equivalence, still conjectural

Printed p. 406, Theorems 2--3, prove the two directions of the equivalence
between the ordinary \(3N+1\) conjecture and

\[
 \mathbb Z^+\subseteq \Phi_B\!\left(\frac13\mathbb Z\right).
\]

Theorems 2--3 establish the equivalence, not either endpoint assertion.  The
display remains a conjecture.

## Corollary 1 and the Periodicity boundary

Let

\[
 \mathcal R=\mathbb Q\cap\mathbb Z_2,
\]

the rationals with odd reduced denominator.  Printed p. 407, Corollary 1, is
exactly

\[
 \Phi_B(\mathcal R)\subseteq\mathcal R.
\]

If \(Q\in\mathcal R\), its binary one-position sequence is finite or
eventually periodic: for some \(\mu,\lambda,X\),
\(d_{m+\lambda}=d_m+X\) for all \(m\geq\mu\).  Bernstein substitutes this
relation into Eq. (2) and obtains an explicit nonzero integer multiple of
\(N=\Phi_B(Q)\); hence \(N\) is rational.  This proves the inclusion.

Applying the inverse bijection gives the exact Laarhoven--de Weger
orientation

\[
 \mathcal R\subseteq Q_\infty(\mathcal R).
\]

The source immediately states that equality is Lagarias's Periodicity
Conjecture and says that Corollary 1 proves one half.  The admitted conclusion
is therefore only that every finite or eventually periodic parity address has
a rational state preimage.  It does not prove the reverse rational-image
inclusion, equality, classification of rational components, or a
positive-integer endpoint.

## Finite parity permutations

The unnumbered third application on printed p. 407 defines

\[
 Q_k(N)=\Phi_B^{-1}(N)\pmod{2^k}.
\]

It proves that this value depends only on \(N\bmod2^k\), so it induces a
permutation \(\overline Q_k\) of \(\mathbb Z/2^k\mathbb Z\).  Every
permutation-cycle length divides \(2^k\).  An \(r\)-cycle at level \(k\)
lifts at level \(k+1\) either to one \(2r\)-cycle or to two \(r\)-cycles.

This \(\overline Q_k\) is exactly the finite chronological parity labeling
called \(\Phi_k\) by Laarhoven--de Weger.  Bernstein proves the finite
permutation and lift statements.  He does not state the finite De Bruijn
graph-isomorphism theorem.  In particular, cycles of \(\overline Q_k\) are
cycles of the labeling permutation, not dynamical cycles of the two-successor
modular Collatz relation.

## Defects and nonclaims

No mathematical defect was found in Corollary 1 or in the finite permutation
paragraph.  The controlling boundaries are:

1. \(\Phi_B\) is the inverse parity orientation; Laarhoven--de Weger \(\Phi\)
   is the forward orientation.
2. Theorem 1 uses the unshortened clock.
3. Theorems 2--3 prove an equivalence to a conjectural image assertion, not
   the assertion itself.
4. Corollary 1 is one inclusion only.
5. Finite permutation cycles are not modular Collatz-relation cycles.
6. OCR text is not an attribution witness for the displayed formulas.

