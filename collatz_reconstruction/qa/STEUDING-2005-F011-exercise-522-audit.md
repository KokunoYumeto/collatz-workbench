# STEUDING-2005-F011 — Exercise 5.22, Serret equivalence, and Markoff constant

## Controlling source and exact scope

This is a content-level audit of Jörn Steuding, *Diophantine Analysis*,
CRC Press/Taylor & Francis Group, copyright 2005, eBook PDF version dated
2011-07-13, ISBN 978-1-4200-5720-1.  The controlling manifestation is

`C:/Users/LOCAL_USER/Documents/Papors/OS/Mason-Stothers theorem/Diophantine Analysis (Jorn Steuding).pdf`

with 271 physical PDF pages, 2,257,201 bytes, and SHA-256
`ea31b76c5c400f91b23038885c3576224496457633be84bcc22d335e3e323b88`.
The `used often` manifestation has the same byte count and hash.  The frozen
routes are `DOCROUTE-COL-DE9A4ADCD5B1583634BE`,
`ROUTE-COL-5E4E81196518AB637C8A`, and
`ROUTE-COL-84B920C98DAE08025C11`.

The relevant content was read at these exact locators:

- physical PDF p. 55 / printed p. 42, §3.4: infinite simple continued
  fractions, convergence, irrationality, and uniqueness;
- physical pp. 91–93 / printed pp. 78–80, §§5.5–5.6: unimodular
  equivalence (5.9)–(5.10), finite-prefix matrices, Lemma 5.6, and Serret's
  Theorem 5.7;
- physical pp. 93–94 / printed pp. 80–81, §5.7: the Markoff constant,
  formula (5.11), and invariance under equivalence in Theorem 5.8;
- physical p. 100 / printed p. 87: Exercise 5.22 itself;
- physical p. 267 / printed p. 254, bibliography entry [97]: exact identity of the
  Lagarias 1985 state-of-the-art reference.

The exercise is an instruction to prove and compute.  It is not a printed
theorem with a supplied proof.  Everything below labelled “edition proof” or
“edition calculation” supplies that missing work and makes no novelty claim.

## Source objects without normalization

Steuding uses the positive integers \(\mathbb N=\{1,2,\ldots\}\) and the
unshortened recursion

\[
 U(n)=
 \begin{cases}
 n/2,&n\equiv0\pmod2,\\
 3n+1,&n\equiv1\pmod2.
 \end{cases}
\]

This is the same branch order and clock as the edition's \(U\), not its
shortened map \(T\) and not Crandall's odd first-return map
\(C_{\mathrm{Cr}}\).  For \(m\in\mathbb N\), put

\[
 x_j(m)=U^j(m),\qquad
 \Theta(m)=[x_0(m),x_1(m),x_2(m),\ldots].
\]

Every digit is a positive integer.  Section 3.4 therefore makes
\(\Theta(m)\) a convergent infinite simple continued fraction and an
irrational real number.  Its first digit is recovered exactly by

\[
 \lfloor\Theta(m)\rfloor=m.
\]

Let the Gauss tail map be

\[
 \mathcal G(y)=\frac1{y-\lfloor y\rfloor}
\]

on nonintegral real numbers.  Literal removal of the first partial quotient
gives the exact morphism equation

\[
 \mathcal G(\Theta(m))=\Theta(U(m)).
\]

Thus \(\Theta\) is a bijection from \(\mathbb N\) onto its explicitly
defined image, with inverse \(\lfloor\cdot\rfloor\), and it conjugates \(U\)
to \(\mathcal G\) restricted to that image.  It does **not** map onto all
irrationals, all positive reals, or an independently characterized Gauss
invariant set.

Steuding's equivalence relation is

\[
 \alpha\sim\beta
 \quad\Longleftrightarrow\quad
 \alpha=\frac{a\beta+b}{c\beta+d}
 \quad\text{for some }a,b,c,d\in\mathbb Z,
 \quad ad-bc=\pm1.
\]

Theorem 5.7 says that two irrational simple continued fractions are
equivalent exactly when their partial-quotient sequences are eventually
identical, allowing a finite deletion from each sequence.

## Source defect and corrected Serret matrix step

The relevant source text contains the following visible defects before the
proof of Theorem 5.7 is even reached.

1. Printed p. 78 calls the integer matrices of determinant \(\pm1\) the
   special linear group \(\mathrm{SL}_2(\mathbb Z)\).  That set is
   \(\mathrm{GL}_2(\mathbb Z)\); \(\mathrm{SL}_2(\mathbb Z)\) has
   determinant \(+1\).  The source immediately uses matrices \(A_n\) of
   determinant \(-1\).
2. Lemma 5.6 states \(c>d>0\) without noting that a Möbius matrix is
   determined only up to simultaneous sign.  A constructive application
   must choose its representative.  Its sufficiency direction is left as
   an easy induction; the Euclidean algorithm on the coprime lower row,
   the two finite continued-fraction presentations controlling determinant
   parity, and an integral adjustment of \(a_0\) supply that construction.

The converse proof of Theorem 5.7 on printed p. 80 then contains three more
visible defects.

1. It says that the original matrix in (5.9) has \(c>d>0\) “by Lemma 5.6.”
   That lemma characterizes matrices already expressible as a finite
   continued-fraction prefix; applying it at this point is circular and is
   unnecessary.
2. After composing the matrix with the \(m\)-th convergent matrix of
   \(\beta\), the lower-right entry is printed as
   \(S=ap_{m-1}+bq_{m-1}\), duplicating \(R\).  Matrix multiplication gives
   \(S=cp_{m-1}+dq_{m-1}\).
3. The convergent error is printed with \(\alpha\):
   \(p_{m-j}=\alpha q_{m-j}+\delta_j/q_{m-j}\).  These are convergents of
   \(\beta\), so the symbol must be \(\beta\).  The ensuing factors printed
   as \(c\alpha+d\) must likewise be \(c\beta+d\).

The needed step repairs constructively.  Start with an arbitrary
\(M=\left(\begin{smallmatrix}a&b\\c&d\end{smallmatrix}\right)\in
\mathrm{GL}_2(\mathbb Z)\) satisfying \(\alpha=M\beta\), and replace \(M\)
by \(-M\), if needed, so that \(D=c\beta+d>0\).  If \(p_m/q_m\) is the
\(m\)-th convergent of \(\beta\), then

\[
 M\begin{pmatrix}p_m&p_{m-1}\\q_m&q_{m-1}\end{pmatrix}
 =\begin{pmatrix}P_m&R_m\\Q_m&S_m\end{pmatrix},
\]

where

\[
 Q_m=cp_m+dq_m=Dq_m+c\varepsilon_m,
 \qquad
 S_m=cp_{m-1}+dq_{m-1}=Dq_{m-1}+c\varepsilon_{m-1},
\]

and \(\varepsilon_j=p_j-\beta q_j\to0\).  Hence \(S_m>0\) for all
sufficiently large \(m\).  Moreover,

\[
 Q_m-S_m
 =D(q_m-q_{m-1})+c(\varepsilon_m-\varepsilon_{m-1})>0
\]

eventually, because
\(q_m-q_{m-1}=(a_m-1)q_{m-1}+q_{m-2}\to\infty\).  Thus
\(Q_m>S_m>0\).  The Euclidean algorithm, equivalently the constructive
sufficiency direction of Lemma 5.6, writes this composite unimodular matrix
as a finite continued-fraction prefix.  If
\(\gamma=[b_{m+1},b_{m+2},\ldots]\), then both \(\alpha\) and \(\beta\)
are finite prefixes of the same \(\gamma\).  This proves the required
converse without any assumption that the original \(c,d\) satisfy
\(c>d>0\).

## Edition proof of Exercise 5.22

Set

\[
 b=(4,2,1,4,2,1,\ldots),
 \qquad
 \beta=[\overline{4,2,1}].
\]

The overbar is present in the printed exercise but disappears in ordinary
PDF text extraction.  Without it, \([4,2,1]=13/3\) would be rational, while
every \(\Theta(m)\) is irrational; Section 5.5 explicitly separates
rational and irrational equivalence classes.  The finite fraction is
therefore not an admissible reading of the exercise.

The unshortened recursion satisfies
\(U(4)=2\), \(U(2)=1\), and \(U(1)=4\).

Assume first that the Collatz conjecture in the exact source form holds.
For every \(m\in\mathbb N\), there is an index \(r\) such that the tail
\((U^{r+j}(m))_{j\ge0}\) is a cyclic shift of \(b\).  Therefore the partial
quotient sequence of \(\Theta(m)\) is eventually identical to that of
\(\beta\).  Serret's Theorem 5.7 gives \(\Theta(m)\sim\beta\).

Conversely, suppose \(\Theta(m)\sim\beta\).  Serret's theorem provides
indices \(r,s\ge0\) for which

\[
 U^{r+j}(m)=b_{s+j}\qquad(j\ge0).
\]

In particular \(U^r(m)\in\{4,2,1\}\), and the deterministic recursion then
runs forever around \(4,2,1\).  Applying this pointwise for every positive
integer \(m\) is exactly the Collatz conjecture stated in the exercise.
Hence

\[
 \bigl(\forall m\in\mathbb N,\ U^j(m)\text{ eventually enters }4,2,1\bigr)
 \quad\Longleftrightarrow\quad
 \bigl(\forall m\in\mathbb N,\ \Theta(m)\sim[\overline{4,2,1}]\bigr).
\]

This is a lossless reformulation: the full orbit is retained as the full
partial-quotient sequence, and \(m\) is recovered from its first digit.

## Edition calculation of the Markoff constant

Steuding defines

\[
 \lambda(\alpha)=\liminf_{q\to\infty}q\lVert q\alpha\rVert
\]

and gives, in (5.11),

\[
 \lambda(\alpha)=\liminf_{n\to\infty}
 \left(
 [a_{n+1},a_{n+2},\ldots]
 +[0,a_n,a_{n-1},\ldots,a_1]
 \right)^{-1}.
\]

Write \(s=\sqrt{229}\), and index the period by
\(a_{3r}=4\), \(a_{3r+1}=2\), \(a_{3r+2}=1\).  The purely periodic value is

\[
 \beta=4+\frac1{2+\frac1{1+1/\beta}}
       =\frac{11+s}{6},
 \qquad 3\beta^2-11\beta-9=0.
\]

No phase is discarded.  Along the three residue classes of \(n\), the
forward tail, limiting reversed tail, their sum, and its reciprocal are

| \(n\bmod3\) | forward tail | reversed-tail limit | sum | reciprocal |
|---:|---:|---:|---:|---:|
| 0 | \((13+s)/10\) | \((s-13)/10\) | \(s/5\) | \(5/s\) |
| 1 | \((7+s)/18\) | \((s-7)/18\) | \(s/9\) | \(9/s\) |
| 2 | \((11+s)/6\) | \((s-11)/6\) | \(s/3\) | \(3/s\) |

The finite reversed fractions in (5.11) converge to the displayed reversed
periodic tails on their respective residue subsequences.  Therefore

\[
 \boxed{\lambda([\overline{4,2,1}])
 =\min\left\{\frac5{\sqrt{229}},\frac9{\sqrt{229}},
                    \frac3{\sqrt{229}}\right\}
 =\frac3{\sqrt{229}}.}
\]

The exact quadratic-field identities and the literal cycle are reproduced by
`certificates/steuding_522_checks.py`.

## Exact crosswalk and nonclaims

- Steuding's recursion is the edition's whole-step \(U\).  Its clock is not
  Crandall's accelerated odd-return clock.  The already proved bridge is
  \(C_{\mathrm{Cr}}^j(x)=U^{A_j+j}(x)\) on odd starts, with cumulative
  valuation clock \(A_j\).
- The exercise's equivalence-class criterion is an exact endpoint
  reformulation, not evidence that the endpoint holds.
- Theorem 5.8 gives the one-way consequence
  \(\Theta(m)\sim\beta\Rightarrow\lambda(\Theta(m))=3/\sqrt{229}\).
  Equality of Markoff constants is not the converse of Theorem 5.8 and does
  not imply eventual equality of continued-fraction digits.
- The Markoff constant depends only on the real continued fraction and says
  nothing by itself about stopping times, orbit minima, accelerated periods,
  the exclusion of nontrivial cycles, or unbounded orbits.
- Lagarias [97] is exactly the already read 1985 *American Mathematical
  Monthly* article.  The exercise imports no additional unnamed Collatz
  theorem from that citation.
- No copyrighted bulk text from the book is reproduced in this audit.
