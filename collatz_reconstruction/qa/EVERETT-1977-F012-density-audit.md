# EVERETT-1977-F012 — finite parity coordinates and density-one descent

## Identity and manifestation boundary

- C. J. Everett, “Iteration of the Number-Theoretic Function
  \(f(2n)=n, f(2n+1)=3n+2\),” *Advances in Mathematics* **25** (1977),
  no. 1, 42–45.
- Publication month: July 1977.
- DOI: `10.1016/0001-8708(77)90087-1`.
- PII: `0001870877900871`.
- ISSN: `0001-8708`.
- The ScienceDirect publisher record fixes the identity and labels the article
  open archive.  Its PDF endpoint presented a CAPTCHA and was not bypassed.
- Complete mathematical content was read from the four-page VOR facsimile at
  `external_literature/dependency_gate_2026-08-25/everett_1977_paperzz_witness.pdf`.
  It has 165,514 bytes and SHA-256
  `668bd5b548136b2f8183eb932af4f39a28965a1b54f676cbe8e949043d4ff160`.
  Its title metadata is the exact PII; its four raster pages visibly retain the
  journal header, printed pages 42–45, byline, affiliation, copyright line,
  equations, and reference.  All four pages were rendered and read at 300 dpi.
- The facsimile OCR layer corrupts symbols and is not controlling.  The raster
  pages control every formula.  A publisher-hosted PDF hash remains unavailable;
  the facsimile hash is not represented as one.

## Source map, state space, and coordinates

Everett works on the nonnegative integers and writes

\[
 f(m)=
 \begin{cases}
  m/2,&m\text{ even},\\
  (3m+1)/2,&m\text{ odd}.
 \end{cases}
\]

This is exactly the corpus shortened map \(T\) restricted to
\(\mathbb Z_{\ge0}\).  It is neither the unshortened map \(U\) nor Crandall's
odd first-return map.  Everett sets \(m_n=f^n(m)\) and
\(x_n=m_n\bmod2\).  Thus the word is chronological and least-significant-bit
first when encoded as an integer.

The source includes \(m=0\) in its parity-coordinate theorem.  Its density
count later includes only positive integers.

## Theorem 1: exact finite parity fibres

For every \(N\ge1\) and every word
\(w=(x_0,\ldots,x_{N-1})\in\{0,1\}^N\), put
\(X=\sum_{n<N}x_n\).  Everett proves that the complete nonnegative fibre is

\[
 m=a_{N-1}+2^NQ_N,
 \qquad 0\le a_{N-1}<2^N,
 \qquad Q_N\in\mathbb Z_{\ge0},
\]

and on that fibre the terminal coordinate is

\[
 m_N=b_{N-1}+3^XQ_N,
 \qquad 0\le b_{N-1}<3^X.
\]

The source leaves the range of \(Q_N\) implicit in the theorem display; its
preceding and inductive uses make it \(\mathbb Z_{\ge0}\).

The induction is exhaustive.  At \(N=1\), the zero bit gives
\(m=2Q_1,m_1=Q_1\), while the one bit gives
\(m=1+2Q_1,m_1=2+3Q_1\).  At the next step, abbreviate
\(a=a_{N-1}\), \(b=b_{N-1}\).

- If \(b\) is even and \(x_N=0\), then
  \(Q_N=2Q_{N+1}\),
  \(a_N=a\), and \(b_N=b/2\).
- If \(b\) is even and \(x_N=1\), then
  \(Q_N=1+2Q_{N+1}\),
  \(a_N=a+2^N\), and
  \(b_N=(3b+3^{X+1}+1)/2<3^{X+1}\).
- If \(b\) is odd and \(x_N=0\), then
  \(Q_N=1+2Q_{N+1}\),
  \(a_N=a+2^N\), and
  \(b_N=(b+3^X)/2<3^X\).
- If \(b\) is odd and \(x_N=1\), then
  \(Q_N=2Q_{N+1}\),
  \(a_N=a\), and
  \(b_N=(3b+1)/2<3^{X+1}\).

The parity of \(b+3^XQ_N\), with \(3^X\) odd, proves that these four cases
are forced and disjoint.  They prove existence, uniqueness, both coefficient
bounds, and preservation of the same quotient coordinate.

Consequently

\[
 P_N:\mathbb Z/2^N\mathbb Z\longrightarrow\{0,1\}^N,
 \qquad
 P_N([m])=(f^n(m)\bmod2)_{0\le n<N},
\]

is a bijection.  The fibre in \(\mathbb Z_{\ge0}\) is the single class
\(a(w)+2^N\mathbb Z_{\ge0}\).  The word forgets \(Q_N\); the terminal
coordinate retains it with coefficient \(3^{X(w)}\).

The printed corollary changes representatives without explaining the change:
it replaces \(0,\ldots,2^N-1\) by \(1,\ldots,2^N\), so the zero residue is
represented by \(2^N\).  The resulting positive-representative map is still
a bijection.

The source's final “one to one” statement also gives injectivity of the
infinite parity code on nonnegative integers: equal infinite codes give equal
residues modulo every \(2^N\), hence equal integers.  It does **not** give
surjectivity from ordinary nonnegative integers onto all infinite binary
sequences.

### Exact later-literature crosswalk

Numerically encoding the word gives

\[
 \sum_{n<N}x_n2^n.
\]

This is exactly the finite chronological parity map later denoted
\(\overline Q_{3,N}\) in the edition.  Everett proves its bijectivity and
affine integer fibres.  Later sources add the permutation-order, lift,
2-adic inverse-limit, and De Bruijn-relation structures; those enlargements
are not attributed to Everett.  Everett's source quotient symbol \(Q_N\) is
not Bernstein–Lagarias's parity encoder \(Q_3\).

For a useful edition coordinate, the branch identity

\[
 2^Nm_N=3^Xm+c(w),
 \qquad
 c(w)=\sum_{j=0}^{N-1}x_j2^j
       3^{\sum_{i=j+1}^{N-1}x_i}
\]

shows that the inverse residue is

\[
 a(w)\equiv-3^{-X}c(w)\pmod{2^N}.
\]

The inverse exists because \(3^X\) is a unit modulo \(2^N\).  This closed
form is an edition deduction from the branch composition, not Everett's
displayed coordinate formula.

## Theorem 2: ordinary natural-density-one descent

Everett defines

\[
 A(M)=\#\{1\le m\le M:\exists k\ge1,\ f^k(m)<m\}
\]

and proves

\[
 \lim_{M\to\infty}\frac{A(M)}M=1.
\]

Thus “almost every” is ordinary natural density one in initial intervals
\([1,M]\).  The conclusion is first descent below the start, not convergence
to one.

### Exact dyadic count

For a length-\(N\) word let

\[
 X=\sum_{n<N}x_n,
 \qquad
 L=\frac{\log2}{\log(10/3)},
 \qquad
 \varepsilon=L-\frac12>0.
\]

The positivity is exact: \(L>1/2\) is equivalent to
\(4>10/3\).  Let \(H_N\) consist of the words satisfying

\[
 \frac12-\varepsilon<\frac XN<\frac12+\varepsilon=L.
\]

The source cites Uspensky, p. 209, for

\[
 \frac{\#H_N}{2^N}\ge1-\frac1{4\varepsilon^2N}.
\]

The estimate is exactly completed without a probabilistic heuristic.  Under
uniform counting on the finite set \(\{0,1\}^N\), the coordinate bits are
independent Bernoulli variables because every prescribed one- or two-bit
pattern has respectively \(2^{N-1}\) or \(2^{N-2}\) extensions.  Hence
\(\mathbb E X=N/2\), \(\operatorname{Var}(X)=N/4\), and Chebyshev gives the
displayed complement bound.

Put \(D_N=\{w:X(w)/N<L\}\), so \(H_N\subseteq D_N\).  Along an actual orbit,

\[
 \frac{m_{n+1}}{m_n}=\frac12\quad(x_n=0),
\]

whereas for an odd \(m_n=2Q+1>1\), necessarily \(Q\ge1\),

\[
 \frac{m_{n+1}}{m_n}
 =\frac{3Q+2}{2Q+1}\le\frac53.
\]

The word inequality is exactly

\[
 \frac XN<L
 \quad\Longleftrightarrow\quad
 (1/2)^{N-X}(5/3)^X<1.
\]

For the positive representative \(m\le2^N\) of a word in \(D_N\), either an
iterate \(m_n=1<m\) occurs with \(n<N\), or no such value occurs and every
odd factor is covered by the \(5/3\) estimate.  In the latter case

\[
 m_N=m_0\prod_{n=0}^{N-1}\frac{m_{n+1}}{m_n}
 \le(1/2)^{N-X}(5/3)^Xm_0<m_0.
\]

The sole excluded positive representative is \(m=1\).  Therefore

\[
 A(2^N)\ge\#D_N-1\ge\#H_N-1
\]

and

\[
 \frac{A(2^N)}{2^N}
 \ge1-\frac1{4\varepsilon^2N}-2^{-N}\longrightarrow1.
\]

For a completely rational edition witness,
\(L>23/40\) follows from

\[
 2^{40}3^{23}-10^{23}=3511519796081828298752>0.
\]

Thus \(\varepsilon>3/40\), and Chebyshev also gives the explicit weaker bound

\[
 \frac{A(2^N)}{2^N}\ge1-\frac{400}{9N}-2^{-N}.
\]

### Interpolation between powers of two

Write \(A_N=A(2^N)\) and

\[
 n_N
 =2^N+\{(2^{N+1}-2^N)-(A_{N+1}-A_N)\}
 =A_N+(2^{N+1}-A_{N+1}),
 \qquad 2^N\le n_N\le2^{N+1}.
\]

Here \(n_N-2^N\) is exactly the number of failures in the shell
\((2^N,2^{N+1}]\), which proves both bounds.

If \(2^N<M\le n_N\), monotonicity gives
\(A(M)/M\ge A_N/n_N\).  If \(M=n_N+k\), the dyadic interval contains only
\(2^{N+1}-A_{N+1}-(2^N-A_N)=n_N-2^N\) failures, so at least \(k\) of its
first \(n_N-2^N+k\) entries are successes.  Hence

\[
 \frac{A(M)}M\ge\frac{A_N+k}{n_N+k}\ge\frac{A_N}{n_N},
\]

where the final inequality uses \(n_N\ge A_N\).  Finally

\[
 \frac{A_N}{n_N}
 =\frac{A_N/2^N}
 {A_N/2^N+2(1-A_{N+1}/2^{N+1})}\longrightarrow1.
\]

This completes the full natural-density limit; no subsequence-only conclusion
is being substituted for the theorem.

## Exact Crandall crosswalk

For odd \(m\), define

\[
 D_T=\{m:\exists k\ge1,\ T^k(m)<m\},
 \qquad
 D_C=\{m:\exists j\ge1,\ C_{\mathrm{Cr}}^j(m)<m\}.
\]

Then pointwise on positive odd integers

\[
 D_T=D_C.
\]

One inclusion uses
\(C_{\mathrm{Cr}}^j(m)=T^{A_j}(m)\).  Conversely, if a shortened iterate
below \(m\) is even, finitely many further divisions by two reach the next
odd return and only decrease it; if it is odd, it is already an odd-return
state.  This proves the reverse inclusion without equating the clocks.

Every positive even integer descends in one shortened step.  Everett's bad
set is therefore exactly the bad odd set.  If
\(B(M)=\#(D_C\cap[1,M])\) and \(O(M)=\lceil M/2\rceil\), the exact cutoff
identity and its complement form are

\[
 A(M)=\lfloor M/2\rfloor+B(M),
 \qquad
 1-\frac{B(M)}{O(M)}
 =\frac{M}{O(M)}\left(1-\frac{A(M)}M\right).
\]

Thus Everett's ordinary natural-density-one statement is equivalent to
Crandall's reported relative-density-one statement on positive odd integers.

## Source issues, exceptions, and nonclaims

- No substantive mathematical error was found in the four-page proof.
- The abstract's unqualified phrase “every integer” is false at \(m=0\); the
  body correctly states the conjecture for \(m\ge1\).
- The positive-representative swap in the corollary and the range of \(Q_N\)
  are implicit presentation steps; both are made explicit above.
- The \(5/3\) factor excludes \(m_n=1\); the proof separates that endpoint
  before multiplying the factors.
- The cited probability estimate is not proved in the article.  The exact
  finite Chebyshev proof above supplies the dependency at the scope used.
- The introductory “verified up to the millions” sentence is historical
  context without a computational witness.
- The theorem proves neither the Collatz conjecture nor density-one
  convergence to one.  The exceptional set may be infinite of density zero.
- It gives no uniform descent-time bound, total-stopping-time bound, or
  accelerated-time bound.
- It proves no result about the unshortened clock, generalized \(qx+r\) maps,
  nontrivial cycles, or unbounded trajectories.
- Finite parity-word surjectivity is not ordinary-integer surjectivity onto
  all infinite binary sequences.
