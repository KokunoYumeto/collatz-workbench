# Siegel 2007.15936 v1/v3 -- Tao Syracuse coordinate crosswalk

Audit ID: `SIEGEL-2007-V1-V3-F023`  
Status: exact Syracuse-coordinate morphism proved; targeted source sections read; neither version audited as a whole  
Controlling source records: `SRC-COL-000025`, `SRC-COL-000026`  
Related Tao source: `SRC-COL-000005`

## Versioned manifestations

The frozen index routes this logical arXiv work in materially different
versions.  They are not text-identical and are not collapsed.

- Historical v1: Maxwell C. Siegel, *Syracuse Random Variables and the
  Periodic Points of Collatz-type maps*, `arXiv:2007.15936v1`.
  - route `DOCROUTE-COL-3E40D11654F4089C8795`;
  - e-print SHA-256
    `ff849b016bf3530f23cf9f921e5e9fcefbd90e2274440d26a138ef3b32ae1eb7`;
  - extracted source TeX `Collatz_Numen_Integral.tex`, 263079 bytes,
    SHA-256
    `bbb6add6f9d113ce66ef68cd42dc0ffab234233a69e558f99615df7fef8a842b`;
  - the source is byte-faithful legacy Latin-1 rather than UTF-8.
- Current routed v3: Maxwell Charles Siegel, *The Collatz Conjecture &
  Non-Archimedean Spectral Theory: Part I -- Arithmetic Dynamical Systems
  and Non-Archimedean Value Distribution Theory*, `arXiv:2007.15936v3`,
  revised 24 April 2023.
  - route `DOCROUTE-COL-97610F92D74267B0D443`;
  - e-print SHA-256
    `2cd43f78e4b6035ba339398cfb2d520f98362fd84847d48d676c5345656346f5`;
  - extracted source TeX `main.tex`, 211321 bytes, SHA-256
    `7f66c3e4a7e49600a3848a51fb53e310edafd116d69856499b0010a24e39bfdb`;
  - the source declares `latin9` input encoding.

Both e-prints and both extracted source trees were copied byte-for-byte to
the Collatz topical shelf after they became used sources.  Source-side and
shelf-side hashes agree.  No public record was changed.

## Content read and exact source claims

The following source passages were read, not inferred from route metadata.

### Historical v1

- lines 100--178: branch strings, affine composition, definition of the
  numen, and the claimed relationship to Tao's Syracuse variables;
- lines 405--568: definition of \(\chi_p\), binary one-position formula
  \[
    \chi_p\!\left(\sum_{k\geq1}2^{n_k}\right)
      =\sum_{k\geq1}\frac{p^{k-1}}{2^{n_k+1}},
  \]
  first for finite strings and then in \(\mathbb Z_p\);
- lines 3441--3501: Haar characteristic function, the statement that
  Tao's finite Syracuse variable is the reduction of \(\chi_3\), and the
  separately presented Fourier recursion.

### Current v3

- lines 1524--1582: finite numen definition and descent from strings to
  nonnegative integers;
- lines 1851--2000: explicit bit-string formula and the \(2\)-adic to
  \(q\)-adic continuation;
- lines 3083--3184: current-version Syracuse discussion, characteristic
  function convention, finite reductions, and the displayed equality of
  laws.

Neither inspected passage contains Tao's first-passage interval \(I_y\), the
event manipulations of Proposition 5.2, the function called \(c_n\) in Tao's
Section 5, or a repair of Tao's Lemma 5.3.  The occurrence of `c_n` later in
Siegel v3 denotes a binary digit and is unrelated.

## Exact coordinate morphism

Let
\[
 \Omega=(\mathbb N_{>0})^{\mathbb N},\qquad
 A_k=a_1+\cdots+a_k,
\]
and give \(\Omega\) the product law
\(\mathbb P(a_k=r)=2^{-r}\).  Define
\[
 \mathcal R(a_1,a_2,\ldots)
   =\sum_{k\geq1}2^{A_k-1}\in\mathbb Z_2.
\]
The image is exactly the set \(\mathbb Z_2^{\infty 1}\) of binary
sequences with infinitely many one digits.  If their positions are
\(0\leq n_1<n_2<\cdots\), the inverse is
\[
 a_1=n_1+1,\qquad a_k=n_k-n_{k-1}\quad(k\geq2).
\]
Thus every fibre is a singleton and no coordinate is discarded.

The cylinder determined by \((a_1,\ldots,a_k)\) fixes every binary digit
through position \(A_k-1\).  Its product-geometric mass and its Haar mass are
both exactly
\[
 \prod_{j=1}^k2^{-a_j}=2^{-A_k}.
\]
Therefore \(\mathcal R\) pushes the geometric product law to Haar measure.
The omitted set of binary sequences with finitely many ones is countable and
Haar-null; this is a measure-space statement, not a pointwise bijection onto
all of \(\mathbb Z_2\).

Applying either Siegel v1's one-position formula or v3's explicit string
formula at \(p=q=3\) gives the pointwise identity in \(\mathbb Z_3\)
\[
 \chi_3(\mathcal R(a_1,a_2,\ldots))
   =\sum_{k\geq1}3^{k-1}2^{-A_k}.
\]
Tao defines the finite Syracuse variable by its law.  On the present sample
space define the deterministic realization
\[
 \operatorname{Syrac}_n(a_1,\ldots,a_n)
 =F_n(a_n,\ldots,a_1)\pmod{3^n}.
\]
Expanding \(F_n\) gives
\[
 \operatorname{Syrac}_n(a_1,\ldots,a_n)
 =\sum_{k=1}^n3^{k-1}2^{-A_k}\pmod{3^n}.
\]
Because reversal preserves the iid geometric product law, this realization
has exactly Tao's named finite law.  Reducing the numen series modulo
\(3^n\) kills every term with \(k>n\), so
\[
 \chi_3(\mathcal R(a))\pmod{3^n}
 =\operatorname{Syrac}_n(a_1,\ldots,a_n)
\]
pointwise under the explicitly declared coupling.  This proves the displayed
equality of laws in Siegel v3 lines 3180--3184 with its sample space, measure,
reversal, deterministic realization, and finite projection all exposed; it
does not identify deterministic objects that Tao defines only in
distribution.

## Local Fourier defects in the current v3 passage

These do not affect the coordinate proof above, but they must be retained for
the later Fourier audit.

1. V3 line 3146 says the finite-character sum is over
   \(\widehat{\mathbb Z}_2\), while its denominators are powers of three and
   the characteristic function was typed on \(\widehat{\mathbb Z}_3\).
   The former is a forced subscript error.
2. With v3 line 3120's convention
   \(\varphi_3(t)=\mathbb E e^{-2\pi i\{tX\}_3}\), Fourier inversion at
   line 3144 needs the opposite sign in the reconstruction exponential.
   The printed sign reconstructs \(P(X=-m)\).  At level \(3\), where
   Tao's law is \(P(X=1)=1/3\), \(P(X=2)=2/3\), the printed sign swaps
   these two masses.
3. V3 line 3164 writes an unsubscripted \(\varphi\) in its final term;
   the typed function throughout the passage is \(\varphi_3\).

No Fourier estimate, inversion consequence, periodic-point theorem, or
Correspondence Principle is certified by this targeted crosswalk.

## Certificate and nonclaims

`certificates/siegel_v1_tao_syracuse_crosswalk_checks.py` pins the two Siegel
versions, Tao v7, and the three frozen route artifacts; checks thirteen exact
source locators; and passes 21844 run-position inverse identities, 21844
finite rational series/projection identities, and 21844 exact cylinder-mass
identities.

This morphism does not identify the shortened map, the accelerated Syracuse
map, and their clocks.  It does not supply Tao's first-passage argument,
repair the \(c_n\) estimate, prove Fourier decay, certify either Siegel
version as a whole, or imply a positive-integer Collatz endpoint.
