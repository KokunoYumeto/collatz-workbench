# Matthews / Matthews--Watts (d)-adic itinerary audit

Audit ID: `MATTHEWS-F002`  
Status: content-checked for the generalized-map, cylinder, inverse-series, and ergodic scope used in the live reader  
Primary claim records: `CLM-COL-000014`--`CLM-COL-000018`  
Primary morphism record: `MOR-COL-000006`

## Routed author-form witness

Frozen route: `DOCROUTE-COL-050A016D668A2524C165`  
Author: K. R. Matthews  
Title: *Generalized 3x + 1 Mappings: Markov Chains and Ergodic Theory*  
Local PDF: `C:/Users/LOCAL_USER/Documents/Papors/Eigen shizzle/p-adic collatz duder/Generalized 3x + 1 Mappings Markov Chains and Ergodic.pdf`  
Bytes: `426445`  
SHA-256: `fecb54070ee6e22766fd1bfe3f5975033957e2ec5c2d558b1e968d9b8b32b0f6`

The footnote on author-form p. 1 says that the file contains small additions and deletions relative to the book chapter. The manifestation is therefore a nonidentical author-form witness of the chapter published in Jeffrey C. Lagarias (ed.), *The Ultimate Challenge: The 3x + 1 Problem*, American Mathematical Society, 2010, pp. 79--103. Author-form locators are not silently converted into published-page locators.

The content used here was read from author-form pp. 1--4 and 12--14. Physical pages 1, 3, 4, 12, 13, and 14 were rendered and visually checked.

## Cited primary predecessor acquired at the bridge

The frozen Collatz route slice contains no document route for the paper to which the author form refers for Theorem 2.2(i)--(ii). Before using the cylinder theorem, the official publisher record and paper were therefore checked:

- K. R. Matthews and A. M. Watts, *A generalization of Hasse's generalization of the Syracuse algorithm*, *Acta Arithmetica* 43 (1984), 167--175.
- DOI: `10.4064/aa-43-2-167-175`.
- Official record: `https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/43/2/104150/a-generalization-of-hasse-s-generalization-of-the-syracuse-algorithm`.
- Official CC-BY download: `https://www.impan.pl/shop/en/publication/transaction/download/product/104150`.
- Local PDF: `external_literature/matthews_watts_1984_impan.pdf`.
- Bytes: `332544`.
- SHA-256: `ebfd8a3c23477409820dda5a05bcecf08b7ad2007133b023c1ca6776687437b1`.

The PDF is a five-image scan containing printed pp. 167--175; every printed article page was inspected visually. The article was received 2 March 1982 and revised 16 July 1982.

## Exact source presentations

### Matthews author form

For (d\geq2), nonzero integers (m_0,\ldots,m_{d-1}), and integers (r_i\equiv i m_i\pmod d), author-form equation (3) defines
\[
 T(x)=\frac{m_i x-r_i}{d}\qquad(x\equiv i\pmod d).
\]
For an arbitrary retained presentation (d), the presentation-level unit
condition is
\[
 \gcd(m_0m_1\cdots m_{d-1},d)=1,
\]
equivalently when every (m_i) is a unit modulo (d). The source separately
defines the modulus (d(T)) as the least modulus on whose residue classes the
map is affine, and uses "relatively prime type" intrinsically at that modulus.
The displayed (d) used in an arbitrary presentation and the least modulus
(d(T)) must not be silently interchanged. In fact, the unit condition forces
the retained (d) to be least: comparison with affine data at any smaller
modulus (q) gives (q m_i=d m'_j) on compatible residue-class
intersections, and (gcd(m_i,d)=1) forces (d\mid q). Thus, once the unit
condition is proved, (d=d(T)) and Matthews's source terminology applies.

Author-form Theorem 6.1 states that every such map has a unique continuous extension
\[
 \widehat T:\mathbb Z_d\longrightarrow\mathbb Z_d
\]
with the same branch formula. Relative primeness is not needed for the extension. The theorem tacitly retains the earlier condition (d\geq2); the degenerate least-modulus value (d(T)=1) does not define the digit system used in Section 6.

Author-form Theorem 2.2(ii) says that, under relative primeness, every length-(\alpha) residue itinerary is exactly one residue class modulo (d^\alpha).

### Matthews--Watts 1984

The 1984 paper uses a different, narrower presentation. It assumes positive unit multipliers (m_1,\ldots,m_d), chooses a complete residue set
\[
 R_d=\{x_1,\ldots,x_d\},
\]
chooses (r_i\in R_d) with (r_i\equiv m_i x_i\pmod d), and defines
\[
 T(x)=\frac{m_i x-r_i}{d}\qquad(x\equiv x_i\pmod d).
\]
The exact crosswalk to the later indexed presentation is the bijection (i\mapsto x_i\bmod d), followed by the corresponding relabeling of (m_i,r_i). The positivity assumption of the earlier paper is not erased; the later author form permits arbitrary nonzero integer multipliers.

Printed equation (2.4) gives, for the actual itinerary of (n\in\mathbb Z_d),
\[
 n=\sum_{j=0}^{\infty}
 \frac{r_j(n)d^j}{m_0(n)m_1(n)\cdots m_j(n)}.
\]
Section 3, Lemma 4 identifies every finite itinerary cylinder as one residue class modulo (d^K), with the corresponding truncated version of this series. Lemma 5 gives exact independence of separated congruence cylinders, Corollary 1 proves strong mixing, and Theorem 3 proves Haar-almost-every equidistribution modulo every (d^\alpha).

## Source-scope issue in author-form Theorem 2.2(i)

For an arbitrary unrelated modulus (m), write (x=i+dq). Then
\[
 T(i+dq)=T(i)+m_iq.
\]
Consequently the number of predecessor classes contributed by branch (i) is governed by (\gcd(m_i,m)), not merely by (\gcd(m_i,d)). The author-form phrase “in the relatively prime case” is immediately qualified there by the stronger displayed condition (\gcd(m_i,m)=1) for every (i). That stronger condition is automatic for (m=d^\alpha), which is the specialization used by the itinerary-cylinder and (d)-adic arguments; it is not automatic for arbitrary (m).

For example, the shortened (3x+1) map is relatively prime at (d=2), but at (m=3) the predecessor counts are not all (2). No arbitrary-(m) uniform predecessor claim is used in the reader.

## Constructive inverse and conjugacy

For (x\in\mathbb Z_d), define the itinerary digit (i_j(x)\in\{0,\ldots,d-1\}) by
\[
 \widehat T^{j}(x)\equiv i_j(x)\pmod d
\]
and define
\[
 \operatorname{It}_T(x)=\sum_{j\geq0}i_j(x)d^j.
\]

For a prescribed digit sequence (z=\sum_{j\geq0}i_jd^j), put
\[
 X_k=\sum_{j=k}^{\infty}
 \frac{r_{i_j}d^{j-k}}{m_{i_k}m_{i_{k+1}}\cdots m_{i_j}}.
\]
All denominators are (d)-adic units. Hence each series converges, and
\[
 X_k\equiv\frac{r_{i_k}}{m_{i_k}}\equiv i_k\pmod d,
 \qquad
 \frac{m_{i_k}X_k-r_{i_k}}d=X_{k+1}.
\]
Thus (X_0) has exactly the prescribed itinerary. Conversely, repeated rearrangement of the actual branch equation gives
\[
 x=
 \sum_{j=0}^{\alpha-1}
 \frac{r_{i_j(x)}d^j}
 {m_{i_0(x)}\cdots m_{i_j(x)}}
 +
 \frac{d^\alpha\widehat T^{\alpha}(x)}
 {m_{i_0(x)}\cdots m_{i_{\alpha-1}(x)}}.
\]
The remainder tends to zero (d)-adically. Therefore
\[
 \operatorname{It}_T^{-1}\!\left(\sum_{j\geq0}i_jd^j\right)
 =\sum_{j\geq0}
 \frac{r_{i_j}d^j}{m_{i_0}\cdots m_{i_j}}.
\]

At finite level,
\[
 x\equiv y\pmod{d^\alpha}
 \quad\Longleftrightarrow\quad
 i_j(x)=i_j(y)\quad(0\leq j<\alpha)
 \quad\Longleftrightarrow\quad
 \operatorname{It}_T(x)\equiv\operatorname{It}_T(y)\pmod{d^\alpha}.
\]
The forward implication follows by applying the common branch and losing exactly one known power of (d) at each step. The reverse implication follows from the truncated inverse series. Hence the encoder is an isometry for the digit-prefix metric, its fibres are singletons, and its finite reductions are permutations.

For the digit shift
\[
 S_d\!\left(\sum_{j\geq0}a_jd^j\right)=\sum_{j\geq0}a_{j+1}d^j,
\]
one has
\[
 \operatorname{It}_T\circ\widehat T
 =S_d\circ\operatorname{It}_T.
\]
This proves the general-(d) conjugacy that author-form p. 14 presents only as something that “should hold.” It is recorded as an independent reconstruction from the printed branch and inverse-series data, with no novelty claim.

No additive or ring-homomorphism property is asserted, so a group-theoretic kernel is not applicable.

## Exact nonunit obstruction

If (g_i=\gcd(m_i,d)>1), then among the (d) lifts (x=i+dt) modulo (d^2),
\[
 T(i+dt)\equiv T(i)+m_it\pmod d
\]
assumes exactly (d/g_i) values. Thus some two-digit words beginning with (i) are absent, every attained next digit has (g_i) lifts, and the canonical itinerary encoder is not a bijection onto the full (d)-shift.

For the unshortened Collatz map in the author form, (d=2,m_1=6,r_1=-2); every odd input maps to an even value. The word (11) is absent. This obstructs the canonical itinerary encoder from being a full-shift conjugacy. It does not assert the nonexistence of every conceivable conjugacy in some other category.

## Crosswalks and nonclaims

- For the shortened (3x+1) map, the coordinate definition gives
  \(
  \operatorname{It}_T=Q_3
  \)
  pointwise. It has the same orientation as the (C_T) appearing in Matthews author-form Theorem 6.3. That theorem alone does not specify enough normalization to identify its named (C_T) pointwise; the coordinate realization supplies the identification.
- Laarhoven--de Weger Section 5.2 states a (p)-adic De Bruijn isomorphism for “appropriately chosen” branch coefficients without typing the exact coefficient gate in that sentence. Matthews's unit condition is the exact condition used here. The present proof also permits composite (d).
- Matthews--Watts Haar-almost-every statements concern (\mathbb Z_d). The embedded ordinary integers form a countable Haar-null subset. No integer-orbit endpoint follows.
- The inverse-series/conjugacy theorem does not solve the positive-integer embedding problem: it transports all (d)-adic itineraries, while the Collatz conjecture concerns the special subset (\mathbb N_{>0}\subset\mathbb Z_2).
