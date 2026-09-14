# LAGARIAS-1985-F008 — finite parity, positive image, and Periodicity audit

## Status and controlling witness

This is a content-level audit of Jeffrey C. Lagarias, *The 3x+1 Problem and
its Generalizations*, American Mathematical Monthly **92** (1985), no. 1,
3--23.  It resolves the exact 1985 scopes invoked by
Laarhoven--de Weger.  It does not treat a later web conversion as a
page-identical original and does not admit any conjecture as a theorem.

- publisher DOI: `10.1080/00029890.1985.11971528`
- JSTOR record: `https://www.jstor.org/stable/2322189`
- author bibliography: `https://websites.umich.edu/~lagarias/3x%2B1.html`
- exact published page-image witness:
  `external_literature/dependency_gate_2026-08-25/lagarias_1985_published_scan.pdf`
- PDF pages: `21`, exactly printed pp. 3--23
- PDF bytes: `2188527`
- PDF SHA-256:
  `f0030a27524cddd15dba19a7978798e4b0e1cd38e3ad69ba196a59b84534ee1a`
- creator: `JstorPdfGenerator v1.0`

All 21 printed pages were rendered and read visually.  The scan has no text
layer.  The author-linked CECM HTML conversion is dated 16 January 1996 and
is only an auxiliary searchable reprint; the 1985 page images control exact
locators and wording.

## Finite chronological parity maps

Printed p. 4, Eq. (2.1), defines the shortened map

\[
 T(n)=
 \begin{cases}
 (3n+1)/2,&n\equiv1\pmod2,\\
 n/2,&n\equiv0\pmod2.
 \end{cases}
\]

Printed p. 6, Eq. (2.2), defines
\(x_i(n)\equiv T^i(n)\pmod2\).  Printed p. 7, Eq. (2.3), calls
\((x_0(n),\ldots,x_{k-1}(n))\) the length-\(k\) parity vector.  Theorem B on
printed p. 7 defines

\[
 Q_k(n)=\sum_{i=0}^{k-1}x_i(n)2^i
\]

and asserts:

1. \(Q_k\) is periodic with period \(2^k\);
2. the induced
   \(\overline Q_k:\mathbb Z/2^k\mathbb Z\to\mathbb Z/2^k\mathbb Z\)
   is a permutation;
3. the order of that permutation is a power of two.

The printed proof is expressly a sketch and ends with “I omit the details.”
Its induction records Eq. (2.9), the periodicity of the parity coordinates
and affine-iterate coefficients, that the order divides \(2^k\), and

\[
 \overline Q_k(n+2^{k-1})
 \equiv \overline Q_k(n)+2^{k-1}\pmod{2^k}
 \tag{2.10}.
\]

The full bijectivity used in this edition is independently supplied by the
already proved 2-adic isometry of \(Q_3\), and Bernstein 1994 independently
supplies the finite permutation and lift statement.  No omitted source detail
is silently treated as printed proof.

Theorem B establishes a parity-label permutation.  It does not make the
shortened map \(T\) a deterministic endomap modulo \(2^k\), and it does not
state the finite De Bruijn graph isomorphism.  Division by two loses one input
bit; the modular Collatz object is a two-successor relation.

## Table 2: exact data and a forced omission

The sentence immediately before Table 2 on printed p. 7 says that one-cycles
are omitted.  Printed p. 8 carries the table, captioned “Cycle structure and
order of permutation \(\overline Q_k\).”  Its orders for
\(k=1,\ldots,6\) are

\[
 1,1,2,2,4,4.
\]

The nontrivial cycles printed for \(k=6\) omit

\[
 (14,46).
\]

This is not an omitted fixed point: direct evaluation from Eq. (2.1) and the
definition of \(Q_6\) gives

\[
 \overline Q_6(14)=46,
 \qquad
 \overline Q_6(46)=14.
\]

The omission does not change the printed order 4.  The deterministic
certificate `certificates/lagarias_dependency_checks.py` enumerates every
residue for \(k\leq6\), checks the displayed orders, and proves that the
nontrivial-cycle difference between the computed \(k=6\) row and the printed
row is exactly \(\{(14,46)\}\).

## The infinite encoder and its exact orientation

Printed p. 17, Eq. (2.33), defines

\[
 Q_\infty(\alpha)=\sum_{i\geq0}x_i2^i,
 \qquad T^i(\alpha)\equiv x_i\pmod2,
\]

as a map \(Q_\infty:\mathbb Z_2\to\mathbb Z_2\).  Its orientation is
state to chronological parity digits.  It is therefore Laarhoven--de Weger
\(\Phi\) and later Bernstein--Lagarias \(Q_3\), not the inverse map
\(\Phi_3\).

Printed p. 17, Theorem L, asserts that \(Q_\infty\) is continuous,
one-to-one, onto, and measure-preserving.  Its proof uses

\[
 Q_\infty(\alpha)\equiv\overline Q_n(\alpha)\pmod{2^n}
\]

and the finite permutations to prove prefix preservation, injectivity,
surjectivity, and inverse continuity.  Two details are not printed:

1. the inverse residue classes selected in the compactness argument are
   compatible because each \(\overline Q_n\) is the reduction of the same
   prefix map;
2. measure preservation follows because every residue cylinder modulo
   \(2^n\) is carried bijectively to one residue cylinder of the same Haar
   measure.

These are exact completions of the printed proof, not enlarged conclusions.

## Positive-integer image: conjectural third form

Immediately after Theorem L, printed p. 17 states the “3x+1 Conjecture
(Third form)” as

\[
 Q_\infty(\mathbb N^+)\subseteq\frac13\mathbb Z,
\]

and sharpens the target to

\[
 Q_\infty(\mathbb N^+)
 \subseteq\frac13\mathbb Z\setminus\mathbb Z.
\]

This is an inclusion, not equality.  The source presents it as equivalent to
the ordinary conjecture but does not write the bridge proof at this location.
The exact bridge uses Theorem L and the digit-shift relation: reaching the
\(1\leftrightarrow2\) cycle yields an eventually alternating parity tail;
conversely, a nonintegral element of \((1/3)\mathbb Z\) has that tail and the
inverse encoder returns the state to 1 or 2.  The endpoint remains
conjectural.

The examples on printed p. 18 are

\[
 Q_\infty(1)=-\frac13,
 \quad Q_\infty(2)=-\frac23,
 \quad Q_\infty(3)=-\frac{20}{3}.
\]

The first displayed series uses summation index \(i\) but exponent \(2n\);
the intended exponent is \(2i\).  The third displayed value is also false
under Eqs. (2.1), (2.2), and (2.33): the shortened trajectory

\[
 3\longmapsto5\longmapsto8\longmapsto4\longmapsto2
 \longmapsto1\longmapsto2
\]

has parity bits \(11000(10)^\infty\), so

\[
 Q_\infty(3)=1+2+\frac{2^5}{1-2^2}=-\frac{23}{3},
\]

not \(-20/3\).  The deterministic certificate recomputes this value from
the map.  The later web rendering repeats the printed series-index mismatch
and value.

## Exact Periodicity Conjecture

Printed p. 18 defines its symbol \(\mathbf Q_2\) to mean the rational
numbers with odd denominator, embedded in \(\mathbb Z_2\).  In modern field
notation this is

\[
 \mathcal R=\mathbb Q\cap\mathbb Z_2=\mathbb Z_{(2)},
\]

not the full 2-adic field.  The source characterizes these elements by finite
or eventually periodic 2-adic expansions.  Its exact unnumbered conjecture is

\[
 \boxed{Q_\infty(\mathcal R)=\mathcal R}.
\]

No proof is claimed.  Bernstein 1994 later proves only the inverse-oriented
half
\(\Phi_3(\mathcal R)\subseteq\mathcal R\), equivalently
\(\mathcal R\subseteq Q_\infty(\mathcal R)\).

The printed exploratory chain includes

\[
 Q_\infty(10)=-26/3,
 \quad Q_\infty(-26/3)=-54,
 \quad Q_\infty(-54)=-82/7,
 \quad Q_\infty(-82/7)=?/15.
\]

The question mark is literal source text.  Exact rational iteration gives a
prefix followed by parity block \(1100\), and hence

\[
 Q_\infty(-82/7)=\frac{18098}{5}=\frac{54294}{15}.
\]

This finite calculation is independently reproduced by
`certificates/lagarias_dependency_checks.py`; it is not attributed to the
1985 paper.

The source says that a divergent integer trajectory cannot have eventually
periodic parity and therefore Periodicity implies the Divergent Trajectories
Conjecture.  That conjecture, printed p. 15, excludes trajectories with
\(\lvert T^k(n_0)\rvert\to\infty\).  This is not the full positive-integer
Collatz conjecture: exclusion of nontrivial cycles remains separate.

## Remaining boundaries

- Theorem M constrains minimal periods of \(Q_\infty\)-orbits to powers of
  two; it does not prove Periodicity.
- The paper does not classify rational encoder orbits.
- The one-sided Bernstein inclusion does not imply equality.
- The third-form image assertion is not admitted as a theorem.
- No finite permutation statement is converted into deterministic modular
  Collatz dynamics.
