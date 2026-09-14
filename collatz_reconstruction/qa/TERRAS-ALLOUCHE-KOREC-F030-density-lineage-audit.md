# Terras--Allouche--Korec F030 — stopping-time and power-descent lineage

## Scope and status

This audit content-reads the four primary manifestations that control the
natural-density descent statements cited in the introduction of Tao's
`1909.03562v5`, `1909.03562v7`, and 2022 journal paper.  It records the maps,
clocks, finite residue coordinates, density arguments, source defects, exact
repairs, and nonclaims before those results are used in the live reader.

This is a critical-source and proof audit, not a claim that the Collatz
conjecture is solved.  The four source maps are retained as printed; their
relation to the reader's unshortened map is made only through the already
proved variable-time clock morphisms.

## Frozen-route result and controlling manifestations

Exact title and author queries against
`state/index_routes.jsonl` and `state/document_routes.jsonl` returned no
matching manifestation for any of the four papers.  That is a bounded routing
miss, not a nonexistence claim.  The frozen ledgers were not changed.  The
following primary scans were then acquired directly to the authorized topical
shelf and read in content.

1. Riho Terras, “A stopping time problem on the positive integers,” *Acta
   Arithmetica* **30** (1976), 241--252, DOI
   `10.4064/aa-30-3-241-252`.

   - local path:
     `C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/published/Terras-1976-A-stopping-time-problem.pdf`;
   - 646395 bytes;
   - SHA-256
     `2b9c296a05541c5b52f63482a09982519546eba36f581bddd853af6ca014bf89`;
   - seven landscape physical pages, with printed p. 241 on physical page 1
     right, pp. 242--251 in two-page spreads, and p. 252 on physical page 7
     left.

2. Riho Terras, “On the existence of a density,” *Acta Arithmetica* **35**
   (1979), 101--102, DOI `10.4064/aa-35-1-101-102`.

   - local path:
     `C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/published/Terras-1979-On-the-existence-of-a-density.pdf`;
   - 134556 bytes;
   - SHA-256
     `6cb5efbda449752cc0e815f630680f4153aa3ee62a548307041f7968b5d0e47b`;
   - two landscape physical pages, with printed p. 101 on physical page 1
     right and p. 102 on physical page 2 left.

3. Jean-Paul Allouche, “Sur la conjecture de
   ‘Syracuse--Kakutani--Collatz’,” *Séminaire de Théorie des Nombres de
   Bordeaux*, année 1978--1979, exposé no. 9, 15 December 1978, printed
   pp. 9-01--9-15; text received 8 March 1979.

   - local path:
     `C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/published/Allouche-1979-Syracuse-Kakutani-Collatz.pdf`;
   - 1160082 bytes;
   - SHA-256
     `96f959368e5417dcc6d432e4831f3cf957e7b0db687b916a6aed0262102a01b6`;
   - seventeen physical pages: a GDZ cover, printed pp. 9-01--9-15, and a
     terminal blank page;
   - GDZ work identifier `PPN320141322_0008`, article identifier `LOG_0014`.

4. Ivan Korec, “A density estimate for the (3x+1) problem,” *Mathematica
   Slovaca* **44** (1994), no. 1, 85--89, MR 1290275, Zbl 0797.11027.

   - local path:
     `C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/published/Korec-1994-A-density-estimate.pdf`;
   - 383521 bytes;
   - SHA-256
     `3111bcc638a563fa4395d8a090a4b563116f1ffe30aee136f6e24a76d4d97c77`;
   - six physical pages: a DML-CZ cover followed by printed pp. 85--89;
   - stable DML-CZ record `http://hdl.handle.net/10338.dmlcz/133225`.

The three Tao manifestations used for the crosswalk remain pinned under
`SRC-COL-000005` and `SRC-COL-000027`.  Both arXiv source versions print the
same introductory formula at source line 165.  The journal prints the same
formula on physical p. 2.

## Terras 1976: exact objects and finite coordinates

Terras works on

\[
 \mathbb N=\{0,1,2,\ldots\}.
\]

On printed p. 241 he defines the parity indicator and shortened map

\[
 X(n)=\begin{cases}1,&n\text{ odd},\\0,&n\text{ even},\end{cases}
 \qquad
 Tn=\frac{3^{X(n)}n+X(n)}2.
\]

Thus this \(T\) is exactly the reader's shortened map, not Tao's one-step
unshortened map.  Terras Definition 0.1 sets

\[
 \chi(n)=\min\{k\in\mathbb Z_{>0}:T^k n<n\},
\]

with value \(\infty\) when the set is empty.  In particular
\(\chi(0)=\chi(1)=\infty\).  The word “positive” in the definition of \(k\)
matters: time zero is not a stopping event.

For \(k\geq0\), printed p. 242 introduces

\[
 X_k(n)=X(T^k n),\qquad
 S_k(n)=\sum_{i=0}^{k-1}X_i(n),\qquad
 \lambda_k(n)=2^{-k}3^{S_k(n)}.
\]

Theorem 1.1 gives the affine remainder representation

\[
 T^k n=\lambda_k(n)n+\rho_k(n),
\]

where

\[
 \rho_k(n)=\frac{\lambda_k(n)}2
 \left(
 X_0(n)\lambda_1(n)^{-1}+\cdots+
 X_{k-1}(n)\lambda_k(n)^{-1}
 \right).
\]

Every displayed term is nonnegative on this state space.  The chronological
encoding vector is

\[
 E_k(n)=(X_0(n),\ldots,X_{k-1}(n)).
\]

Theorem 1.2 proves the exact fibre statement

\[
 E_k(n)=E_k(m)\quad\Longleftrightarrow\quad n\equiv m\pmod{2^k}.
\]

Consequently the restriction of \(E_k\) to any complete residue block of
length \(2^k\) is a bijection onto \(\{0,1\}^k\).  Corollaries 1.3 and 1.4
express this respectively as periodicity and as independence of the
coordinates \(X_0,X_1,\ldots\) under natural density.  No stochastic model is
substituted for the arithmetic map: the probability statements are exact
finite residue counts followed by density limits.

## The coefficient stopping time and its relation to actual stopping

Definition 1.5 on printed p. 243 defines the coefficient stopping time

\[
 \tau(n)=\min\{k\in\mathbb Z_{>0}:\lambda_k(n)<1\},
\]

again allowing \(\infty\).  Proposition 1.8 proves

\[
 \tau(n)\leq\chi(n).
\]

Theorem 1.9 is stronger than this pointwise inequality.  If
\(\tau(n)=k\), then there is \(M>0\) such that every sufficiently large
\(m\equiv n\pmod{2^k}\) has \(\chi(m)=k\).  Since there are only finitely many
residue classes modulo \(2^k\), the sets

\[
 \{n:\tau(n)=k\}
 \quad\text{and}\quad
 \{n:\chi(n)=k\}
\]

differ in only finitely many integers for each fixed \(k\).

Definition 1.10 uses the complete block \([1,2^k]\):

\[
 \mathbb P[\tau=k]
 =2^{-k}\#\{n\in[1,2^k]:\tau(n)=k\}.
\]

Theorem 1.11 prints, for every positive \(k\), the existence and identity

\[
 F(k)=\lim_{m\to\infty}\frac1m
 \#\{n\leq m:\chi(n)\geq k\}
 =\mathbb P[\tau\geq k].
\]

Its proof first obtains the point-mass identities and then says only “By
forming sums.”  The 1979 note supplies the explicit finite-complement
argument needed for the tail density; the present edition therefore uses the
1979 proof as the rigorous closure of this step rather than silently treating
an infinite-density interchange as harmless.

## Terras 1976 source defects and exact repairs

### 1. Proposition 1.7 omits a necessary sign hypothesis

The affine identity gives

\[
 T^k n<n
 \quad\Longleftrightarrow\quad
 \rho_k(n)<(1-\lambda_k(n))n.
\]

Division by \(1-\lambda_k(n)\) preserves the inequality only when
\(\lambda_k(n)<1\).  Proposition 1.7 nevertheless prints the unconditional
equivalence

\[
 T^k n<n
 \quad\Longleftrightarrow\quad
 \frac{\rho_k(n)}{1-\lambda_k(n)}<n.
\]

It is false as printed: for \(n=1,k=1\),

\[
 T(1)=2\not<1,\qquad
 \lambda_1(1)=\frac32,\qquad
 \rho_1(1)=\frac12,
\]

while \(\rho_1/(1-\lambda_1)=-1<1\).  Theorem 1.9 uses the formula only
under \(\tau(n)=k\), which supplies \(\lambda_k(n)<1\), so that use is valid.
The edition states the hypothesis at every use.

### 2. Wrong internal citation in Theorem 1.9

The proof of Theorem 1.9 cites “Proposition 1.9” for the fact
\(\tau\leq\chi\).  The relevant result is Proposition 1.8.  This is a locator
defect, not a mathematical enlargement.

### 3. Definition 1.12 drops the final prefix index

Printed Definition 1.12 calls a binary sequence of length \(k\) admissible
when its initial prefixes satisfy the coefficient inequality for
\(1\leq i\leq k-2\).  Formula (9), the stopping-time event, and Theorem 1.14's
recurrence require all proper nonempty prefixes, namely

\[
 1\leq i\leq k-1.
\]

The literal (k-2) range is inconsistent already at length (2).  The
edition records the print and uses the forced (k-1) range.

### 4. Theorem 1.17 drops \(+1\) from the terminal-string bound

Put

\[
 \gamma=\frac{\log2}{\log3}.
\]

For a terminal word of length \(k\), let \(a\) be the number of zeros and
\(b=k-a\) the number of ones.  Its last digit is zero and its length-
\(k-1\) prefix is active.  Therefore

\[
 \frac{3^b}{2^{k-1}}>1,
\]

so the exact algebra is

\[
 b>(k-1)\gamma,
 \qquad
 a-1<(k-1)(1-\gamma),
 \qquad
 a<1+(k-1)(1-\gamma).
\]

The source instead prints \(a<(k-1)(1-\gamma)\), dropping \(+1\), and then
uses the too-small cutoff \(a\leq\lfloor k(1-\gamma)\rfloor\).  At \(k=2\),
the word \((1,0)\) is terminal and has \(a=1\), while
\(\lfloor2(1-\gamma)\rfloor=0\), giving an explicit counterexample to the
printed support assertion.

The theorem is repaired without changing its conclusion.  The correct
integer cutoff is

\[
 a\leq \left\lfloor (k-1)(1-\gamma)\right\rfloor+1.
\]

Its ratio to \(k\) still tends to \(1-\gamma<1/2\), because
\(3^2=9>8=2^3\) gives \(\gamma>1/2\).  The same binomial-tail/central-limit
argument therefore proves

\[
 F(k)=\mathbb P[\tau\geq k]\longrightarrow0.
\]

The monotonicity of \(F(k)\) is immediate from the nested tail events.

### 5. Tail notation appears before its direct block definition

Definition 1.10 explicitly defines the point masses and finite lower-tail
sums.  Theorem 1.11 then invokes \(\mathbb P[\tau\geq k]\) before formula
(6) gives its direct complete-block count.  The 1979 note defines both
\(\mathbb P[\tau<k]\) and \(\mathbb P[\tau\geq k]\) in the same block before
using them.  The edition follows that typed order.

## Terras 1979: the finite-complement density closure

The 1979 note opens by recording that A. Garsia, H. Moeller, and the editors
had expressed doubts about existence and correctness of the 1976 density
formula.  It retains the same shortened map and stopping times.  For a set
\(A\) of positive integers it defines

\[
 \delta(A)=\lim_{m\to\infty}\frac1m\#\{n\leq m:n\in A\},
\]

when the limit exists.  It writes \([\chi=k]\), \([\chi<k]\), and
\([\chi\geq k]\) for the corresponding sets.

The theorem on printed p. 101 is unambiguously

\[
 \delta[\chi\geq k]=\mathbb P[\tau\geq k].
\]

Both comparison symbols are \(\geq\), not \(>\).  The proof is finite:

1. the 1976 point-mass/coset argument gives
   \(\delta[\chi=j]=\mathbb P[\tau=j]\) for each fixed \(j\);
2. finite additivity over \(1\leq j<k\) gives
   \(\delta[\chi<k]=\mathbb P[\tau<k]\);
3. \([\chi<k]\) and \([\chi\geq k]\) are complementary, hence
   \(\delta[\chi<k]+\delta[\chi\geq k]=1\);
4. the two finite-block probabilities satisfy
   \(\mathbb P[\tau<k]+\mathbb P[\tau\geq k]=1\).

No infinite sum of densities occurs.

Combining this theorem with the repaired 1976 coefficient-tail estimate gives

\[
 \overline\delta\{n:\chi(n)=\infty\}
 \leq \delta[\chi\geq k]
 =F(k)\longrightarrow0.
\]

Thus the positive integers with finite stopping time have natural density
one.  This is an exceptional-set argument through upper density; it does not
assert finite stopping for every integer.

## Allouche's generalized residue map

Allouche fixes positive integers \(n,d\), assumes \(d\geq2\) and
\(\gcd(n,d)=1\), chooses a complete system

\[
 A_d=\{0,r_1,\ldots,r_{d-1}\}\subset\mathbb Z
\]

of representatives modulo \(d\), and lets
\(\varphi:\mathbb Z\to A_d\) send each integer to its chosen representative.
He defines \(g:\mathbb Z\to\mathbb Z\) by

\[
 g(\ell)=
 \begin{cases}
  \ell/d,&\ell\equiv0\pmod d,\\[2mm]
  (n\ell-\varphi(n\ell))/d,&\ell\not\equiv0\pmod d.
 \end{cases}
\]

For \(n=3,d=2,A_2=\{0,-1\}\), this is exactly Terras's shortened map on
integers.  The representative \(-1\) is part of the source presentation and
is not silently replaced by \(1\).

For \(k\geq1\) and \(j\in\mathbb Z\), printed p. 9-04 defines

\[
 \alpha(k,j)=
 \#\{v\in\{0,\ldots,k-1\}:g^v(j)\not\equiv0\pmod d\}.
\]

Lemma 1, proved on pp. 9-05--9-06, gives for every
\(\lambda\in\mathbb Z\)

\[
 g^k(d^k\lambda+j)
 =n^{\alpha(k,j)}\lambda+g^k(j),
 \qquad
 \alpha(k,d^k\lambda+j)=\alpha(k,j).
\]

Its induction proves the stronger intermediate coordinate

\[
 g^u(d^k\lambda+j)
 =n^{\alpha(u,j)}d^{k-u}\lambda+g^u(j),
 \qquad 1\leq u\leq k,
\]

from which the displayed \(u=k\) identity follows.

This is an exact affine coordinate on every residue fibre modulo \(d^k\).
The domain, codomain, fibre, and information retained are explicit: \(j\)
selects the residue class, \(\lambda\) is its integral quotient coordinate,
and the branch count \(\alpha(k,j)\) is constant on that fibre.

Lemma 2 on p. 9-06 sets

\[
 P_k(j)=g^k(j)-\frac{n^{\alpha(k,j)}}{d^k}j.
\]

Under the section's standing assumption \(n>d\), let

\[
 M=\frac{1}{n-d}\sup_{z\in\mathbb Z}|\varphi(z)|.
\]

Then

\[
 |P_k(j)|\leq M\frac{n^k}{d^k}.
\]

The exact recurrence used to prove the bound is

\[
 P_{k+1}(j)=
 \begin{cases}
  P_k(j)/d,&g^k(j)\equiv0\pmod d,\\[1mm]
  (n/d)P_k(j)-\varphi(ng^k(j))/d,
    &g^k(j)\not\equiv0\pmod d.
 \end{cases}
\]

For the classical representatives \(A_2=\{0,-1\}\), one has \(M=1\).
Lemma 3 on pp. 9-07--9-08 gives the exact branch-count fibres

\[
 \#\{0\leq j<d^k:\alpha(k,j)=i\}
 =\binom{k}{i}(d-1)^i
 \qquad(0\leq i\leq k).
\]

Allouche's Theorem 1 is not merely a qualitative equidistribution statement.
Fix \(a>1\), put

\[
 k=\left\lfloor\frac{\log x}{a\log n}\right\rfloor,
\]

and let \(A,B\in\mathbb Q\) be distinct from every number
\(n^\alpha/d^\beta\), where \(\alpha\in\mathbb N\) and
\(\beta\in\mathbb N_{>0}\).  If \(C\) is the maximum of the absolute
denominators of \(A\) and \(B\), \(\theta=1_{(A,B)}\), and

\[
 F(x)=\sum_{\ell\leq x}
 \theta\!\left(\frac{g^k(\ell)}{\ell}\right),
\]

then the theorem has three separately hypothesized cases.

1. If \(A<B<0\), then \(F(x)=O(Cx^{1/a})\).
2. If \(A<B\), \(B>0\), and, for some \(\varepsilon>0\),
   \[
    \frac{d-1}{d}-\frac{\log d}{\log n}
      -\frac{\log B}{k\log n}\geq\varepsilon,
   \]
   then, for \(k\geq k_0(\varepsilon)\), there is an
   \(\eta\in(0,1)\) for which
   \[
    F(x)=O\!\left(Cx^{1/a}
      +x^{,1-\frac{|\log\eta|}{a\log n}}\right).
   \]
3. If \(0<A<B\) and
   \[
    \frac{\log d}{\log n}+\frac{\log A}{k\log n}
      -\frac{d-1}{d}\geq\varepsilon,
   \]
   the same estimate holds.

The implied constants depend only on \(n,d,A_d\).  The proposition on
pp. 9-08--9-10 is the exact finite-coordinate handoff:

\[
 \left|
 \sum_{\ell\leq x}\theta\!\left(\frac{g^k(\ell)}{\ell}\right)
 -\frac{x}{d^k}\sum_{i=0}^k\binom{k}{i}(d-1)^i
   \theta\!\left(\frac{n^i}{d^k}\right)
 \right|
 \leq \frac52d^k+MCn^k.
\]

Lemma 4 supplies the binomial concentration estimate

\[
 \frac1{d^k}
 \sum_{\left|i-\frac{d-1}{d}k\right|>\varepsilon k}
 \binom{k}{i}(d-1)^i\leq\eta^k
\]

for all sufficiently large \(k\), with \(0<\eta<1\).  The theorem is the
combination of this proposition and Lemma 4.  The exact classical power
consequence below is reproved directly from these source lemmas, so every
change of variable and exceptional block is visible.

## Exact classical consequence of Allouche's lemmas

Specialize to \(n=3,d=2,A_2=\{0,-1\}\), so \(g=T\), and write

\[
 A_m(y)=\alpha(m,y)=\sum_{i=0}^{m-1}(T^i(y)\bmod2).
\]

Lemma 2 gives the exact decomposition and bound

\[
 T^m(y)=\frac{3^{A_m(y)}}{2^m}y+P_m(y),
 \qquad
 |P_m(y)|\leq\left(\frac32\right)^m.
\]

Define

\[
 c_A=\frac32-\log_3 2.
\]

Fix \(c>c_A\), and choose \(\eta>0\) with
\(c_A+\eta<c\).  On the ternary-height block

\[
 3^m\leq y<3^{m+1},
\]

suppose

\[
 A_m(y)\leq\left(\frac12+\eta\right)m.
\]

Then

\[
 \frac{3^{A_m(y)}}{2^m}y
 \leq
 y\left(\frac{3^{1/2+\eta}}2\right)^m
 \leq C_\eta y^{c_A+\eta}
\]

for a fixed constant \(C_\eta\), while

\[
 \left(\frac32\right)^m
 \leq y^{\log_3(3/2)}.
\]

The error exponent is strictly smaller than \(c_A\), since

\[
 \log_3(3/2)+\log_3 2=1<\frac32.
\]

Hence \(T^m(y)<y^c\) for all sufficiently large \(m\) outside the displayed
branch-count exceptional set.

Lemma 3 says that on every complete residue block of length \(2^m\), the
exceptional proportion is exactly a binomial upper tail.  It tends to zero.
The interval \([3^m,3^{m+1})\) consists of complete \(2^m\)-blocks plus at
most two end fragments, whose total relative size is

\[
 O(2^m/3^m)=O((2/3)^m).
\]

Thus the exceptional proportion in each ternary-height block tends to zero.
Summing the geometrically increasing blocks proves that

\[
 \{y\in\mathbb N_{>0}:\exists r\geq0,\ T^r(y)<y^c\}
\]

has natural density one for every strict \(c>c_A\).  The proof does not cover
the endpoint \(c=c_A\).  Through the already proved shortened/unshortened
clock embedding, the same one-way conclusion holds with Tao's
\(\operatorname{Col}_{\min}\).

This proof is an edition reconstruction from Allouche's printed affine and
counting lemmas.  The exponent is not printed as a decimal theorem statement
in Allouche's seminar text.  Korec p. 86 explicitly identifies the result as
a special case of Allouche and prints the bound

\[
 \frac32-\log_3 2=0.86907\ldots.
\]

## Allouche Theorem 2: equal asymptotic branches do not determine dynamics

Theorem 2 on p. 9-04 announces two functions
\(F,G:\mathbb Z\to\mathbb Z\)
with the same branchwise leading terms:

\[
 F(\ell)=\frac\ell d+O(1),\quad
 G(\ell)=\frac\ell d+O(1)
 \quad(\ell\equiv0\pmod d),
\]

and

\[
 F(\ell)=\frac{n\ell}d+O(1),\quad
 G(\ell)=\frac{n\ell}d+O(1)
 \quad(\ell\not\equiv0\pmod d).
\]

For every integer \(\ell\), the \(F\)-orbit is eventually periodic, with only
finitely many periods in total.  By contrast, outside a finite set,

\[
 |G^k(\ell)|\longrightarrow\infty.
\]

The displayed construction on p. 9-12 first chooses \(u\) with
\(d<n<d^u\).  For each \(\ell\not\equiv0\pmod d\), it chooses
\(\theta_\ell\) with

\[
 0\leq\theta_\ell<d^u,
 \qquad n\ell+\theta_\ell\equiv0\pmod{d^u},
\]

and displays

\[
 F(\ell)=
 \begin{cases}
  \ell/d+d^{u-1}-d^{i-1},
    &\ell\equiv d^i\pmod{d^u},\quad 1\leq i\leq u,\\[1mm]
  (n\ell+\theta_\ell)/d,
    &\ell\not\equiv0\pmod d.
 \end{cases}
\]

It later puts \(G(\ell)=F(\ell)+1\).  The displayed divisible branch is
given only on the residue classes

\[
 \ell\equiv d^i\pmod{d^u},\qquad 1\leq i\leq u.
\]

These classes do not exhaust the multiples of \(d\).  For example, when
\(d=2\) and \(u=3\), the class \(\ell\equiv6\pmod8\) is absent.  Thus the
printed cases do not literally define the asserted map
\(F:\mathbb Z\to\mathbb Z\).

The exact local completion is as follows.  For every \(\ell\equiv0\pmod d\),
let \(\rho_\ell\) be the unique integer satisfying

\[
 0\leq\rho_\ell<d^{u-1},\qquad
 \frac\ell d+\rho_\ell\equiv0\pmod{d^{u-1}},
\]

and define

\[
 F(\ell)=\frac\ell d+\rho_\ell.
\]

On each displayed source class \(\ell\equiv d^i\pmod{d^u}\), this gives
\(\rho_\ell=d^{u-1}-d^{i-1}\) for \(i<u\), and \(\rho_\ell=0\) for
\(i=u\), exactly agreeing with the printed formula.  It also supplies the
two properties used subsequently:

\[
 F(\ell)\equiv0\pmod{d^{u-1}},\qquad
 \left|F(\ell)-\frac\ell d\right|<d^{u-1}.
\]

This completion is an independently stated repair, not text silently
attributed to Allouche.  With it in place, pp. 9-12--9-14 prove a uniform
bound for the \(F\)-iterates and set \(G=F+1\); they then prove an expanding
lower bound for \(G^k\), with a finite exceptional set supplied by finite
predecessor fibres.  The repaired theorem shows that equal branch slopes and
\(O(1)\) asymptotics do not determine periodicity.  It is not a theorem about
the classical Collatz map's endpoint.

## Korec 1994: exact theorem and proof

Korec works on the nonnegative integers with the same shortened map

\[
 T(y)=\begin{cases}(3y+1)/2,&y\text{ odd},\\y/2,&y\text{ even}.
 \end{cases}
\]

For real \(c\), printed p. 85 defines

\[
 M_c=\{y\in\mathbb N:\exists n\in\mathbb N,\ T^n(y)<y^c\}.
\]

Theorem 1 is:

\[
 c>\log_4 3
 \quad\Longrightarrow\quad
 \delta(M_c)=1.
\]

The inequality is strict.  No endpoint statement at \(c=\log_4 3\) is
printed or proved.

On p. 86 Korec defines

\[
 X_k(y)=1_{\{T^k(y)\text{ odd}\}},\qquad
 E_k(y)=(X_0(y),\ldots,X_{k-1}(y)),\qquad
 S_k(y)=\sum_{i=0}^{k-1}X_i(y),
\]

and

\[
 U(m,d)=\#\{0\leq y<2^m:S_m(y)\leq md\}.
\]

Lemma 1 restates the exact fibre theorem

\[
 E_m(x)=E_m(y)\quad\Longleftrightarrow\quad x\equiv y\pmod{2^m}.
\]

Therefore every interval of \(2^m\) consecutive nonnegative integers has the
same \(S_m\)-counts.  Lemma 2 uses the central limit theorem to prove

\[
 d>\frac12\quad\Longrightarrow\quad
 \frac{U(m,d)}{2^m}\longrightarrow1.
\]

For the proof of Theorem 1, fix \(\varepsilon>0\) and
\(c>\log_4 3\), with \(c<1\) harmlessly assumed.  Given a large cutoff \(a\),
choose the least positive integer \(m\) for which

\[
 a\leq m^2 2^m.
\]

For

\[
 m2^m\leq y<a,
\]

the paper prints on p. 87

\[
 d=\frac12\left(\frac{c}{\log_4 3}+\frac12\right)
\]

and immediately claims

\[
 \frac12<d<\frac{c}{\log_2 3}.
\]

This is false as printed, because

\[
 \frac12\left(\frac{c}{\log_4 3}+\frac12\right)
 =\frac{c}{\log_2 3}+\frac14
 >\frac{c}{\log_2 3}.
\]

The local repair forced by the following comparison is

\[
 d_*=\frac12\left(\frac{c}{\log_2 3}+\frac12\right).
\]

Because \(c>\log_4 3=\tfrac12\log_2 3\), the number
\(c/\log_2 3\) is strictly greater than \(1/2\); hence \(d_*\), their
arithmetic mean, satisfies

\[
 \frac12<d_*<\frac{c}{\log_2 3}.
\]

For every \(p<m\), \(T^p(y)\geq y/2^p>m\).  If
\(k=S_m(y)\), multiplying the exact one-step ratios gives

\[
 \begin{aligned}
 T^m(y)
 &<y\left(\frac{3m+1}{2m}\right)^k
       \left(\frac12\right)^{m-k}\\
 &=y\frac{3^k}{2^m}
       \left(1+\frac1{3m}\right)^k\\
 &\leq y\frac{3^k}{2^m}
       \left(1+\frac1{3m}\right)^m
 <y\frac{3^k}{2^{m-1}}.
 \end{aligned}
\]

Thus \(T^m(y)<y^c\) follows from

\[
 (m^2 2^m)^{1-c}3^k\leq2^{m-1},
\]

Korec calls this equivalent to the printed inequality (4) on p. 87:

\[
 \frac{k}{m}
 \leq
 \frac{c}{\log_2 3}
  -\frac{1+2(1-c)\log_2m}{m}.
\]

Exact base-two logarithmic rearrangement instead gives

\[
 \frac{k}{m}
 \leq
 \frac{c}{\log_2 3}
 -\frac{1+2(1-c)\log_2m}{m\log_2 3}.
\]

Thus the word ``equivalently'' is false.  Since \(0<c<1\), the numerator
being subtracted is positive; since \(\log_2 3>1\), the printed inequality
subtracts more and is therefore a stronger sufficient condition.  It does
not invalidate the proof once the parameter is repaired.

There is one further boundary mismatch.  The proof text uses
\(S_m(y)<md\), whereas the definition of \(U(m,d)\) and the final full-block
count use \(S_m(y)\leq md\).  For the repaired \(d_*\), the right side of
the exact rearrangement tends to \(c/\log_2 3>d_*\).  Consequently, for all
sufficiently large \(m\), the implication holds with

\[
 \frac{S_m(y)}m\leq d_*,
\]

including the boundary.  Korec's block count may then be used exactly as
defined.  The paper partitions the interval into full blocks of length
\(2^m\), uses Lemma 2 in each block, and shows both the initial range below
\(m2^m\) and the unused terminal fragment have relative size tending to
zero.  This proves natural density one after the three local repairs:

1. replace \(\log_4 3\) by \(\log_2 3\) in the definition of \(d\);
2. restore the missing factor \(\log_2 3\) in the denominator of the
   correction term in the claimed equivalence (or retain the printed,
   stronger sufficient inequality without calling it equivalent);
3. propagate the non-strict boundary \(S_m(y)\leq md_*\) used by \(U\).

The witness iterate in this proof is \(n=m\), and

\[
 m\leq\log_2y
\]

on the retained interval.  It is therefore bounded as a function of the
starting value but not by a constant independent of \(y\), exactly as Korec
states on p. 86.

Korec's two examples on pp. 88--89 show that density-one finite stopping by
itself does not formally imply a power-descent theorem for an arbitrary map,
and that a power threshold can be genuine.  They are logical separation
examples, not counterexamples to Korec's Collatz theorem.

## Exact Tao crosswalk and correction

Tao v5 and v7 source line 165, and the 2022 journal p. 2, print

\[
 \theta>\frac32-\frac{\log3}{\log2}\approx0.869.
\]

The formula and decimal cannot both be correct.  Indeed

\[
 3^2=9>8=2^3
 \quad\Longrightarrow\quad
 \frac{\log3}{\log2}>\frac32,
\]

so the printed expression is negative.  The Allouche consequence above and
Korec's explicit retrospective statement give the forced correction

\[
 \boxed{\theta>\frac32-\log_3 2
       =\frac32-\frac{\log2}{\log3}}
 \approx0.8690702464.
\]

Tao's Korec threshold is printed correctly:

\[
 \boxed{\theta>\log_4 3
       =\frac{\log3}{\log4}}
 \approx0.7924812504.
\]

Theorem 1 of Korec is a natural-density theorem for the shortened map.  The
reader's exact whole-orbit clock proves that the shortened state \(T^n(y)\)
occurs in the unshortened orbit; hence Korec's conclusion implies Tao's
\(\operatorname{Col}_{\min}(y)<y^c\) statement without identifying the two
clocks one iterate at a time.

Tao v7 source line 695 remarks that optimizing his introductory Syracuse
descent parameters recovers Korec.  The exact limiting exponent coordinate is
visible from the accelerated first-return formula.  If \(r\) odd returns use
valuation sum \(A_r\), then

\[
 \operatorname{Syr}^r(N)
 =\frac{3^r}{2^{A_r}}N+\text{positive affine remainder}.
\]

At the typical scale \(A_r\sim2r\) and the longest scale permitted by the
input size, \(r\sim\log_4N\), the main multiplicative term has exponent

\[
 1+\log_4(3/4)=\log_4 3.
\]

This is an exact parameter identity, not a replacement proof of Korec's
natural-density theorem.  Tao's locally displayed loose choices
\(n_0=0.1\log_2x\) and \(A_{n_0}>1.9n_0\) only give a weaker numerical bound;
the source itself says the parameters must be optimized.  The undefined
\(1.9n\) at v7 line 689 is the separate, already recorded \(n_0\)-subscript
defect and is not duplicated as a new finding here.

## Dependency graph

The admitted consequences have the following exact dependencies.

1. Terras finite stopping at natural density one:

   - 1976 Theorem 1.2 and Corollaries 1.3--1.4: exact parity fibres;
   - 1976 Theorem 1.9: point-mass/coset handoff;
   - 1979 theorem: finite-complement tail-density identity;
   - repaired 1976 Theorem 1.17: coefficient-tail limit;
   - upper-density containment of the infinite-stopping set.

2. Allouche strict power exponent \(c_A\):

   - generalized-map definition;
   - Lemma 1 affine residue coordinate;
   - Lemma 2 remainder bound;
   - Lemma 3 exact binomial branch counts;
   - explicit ternary-height/dyadic-period block cover;
   - shortened-to-unshortened one-way orbit-state inclusion.

   The exponent extraction does not depend on Allouche's Theorem 2 or on the
   repair of its missing divisible residue classes.

3. Korec strict power exponent \(\log_4 3\):

   - Terras parity-fibre lemma;
   - binomial central-limit tail;
   - Korec's exact product estimate and block decomposition, with the printed
     parameter denominator, logarithmic equivalence, and strict/non-strict
     boundary repaired as displayed above;
   - shortened-to-unshortened one-way orbit-state inclusion.

4. Tao introductory correction:

   - exact elementary sign check for the printed expression;
   - Korec p. 86 and the reconstructed Allouche consequence for the intended
     formula;
   - no inference from the decimal alone.

## Nonclaims

- None of the four papers proves the Collatz conjecture or finite stopping for
  every positive integer.
- Natural density one is not set equality and does not remove a possible
  infinite exceptional set.
- Neither the Allouche nor Korec proof includes its endpoint exponent.
- Theorems about the shortened map are not silently rewritten as fixed-time
  theorems about Tao's unshortened or accelerated maps.
- The Allouche affine formula and branch-slope asymptotics do not determine
  global orbit behaviour.  Allouche's Theorem 2 supplies the opposite logical
  warning only after the missing divisible residue classes in its displayed
  definition of \(F\) are completed by the explicit bounded correction above.
- Korec's theorem survives three local printed defects; the source's displayed
  parameter and claimed equivalence are not reproduced as if literally valid.
- Tao's line-695 optimization remark is not used as a substitute for Korec's
  natural-density proof.
- No quantitative convergence rate for either density-one theorem is claimed
  beyond the estimates explicitly displayed in the primary proofs.
- The finite certificate
  `certificates/terras_allouche_korec_checks.py` checks source pins, exact
  algebraic kernels, residue fibres, finite block identities, source-defect
  counterexamples, and rational logarithm enclosures.  It does not certify a
  central limit theorem, an infinite natural-density limit, Tao's theorem, or
  the Collatz conjecture.
