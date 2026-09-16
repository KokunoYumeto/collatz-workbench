# Positive shadows of retained integral cycle sections

**16 September 2026. Collatz workbench continuation.**

The published Collatz source was read at `d0c987b12c20be5978f496ab1ef2a60018caa5e5`. Its first-jet comparison remains unchanged. The separately delivered `defect_rank_descent_20260915` package is still an additive local predecessor; it is not silently assigned a remote commit. This contribution gives new all-length arithmetic families and a small independent gap certificate. The large preceding source atlas is **not** a premise of the new all-length theorem.

The elementary descriptions of the signed cycles and the general logarithm theorem are not claimed as discoveries. The arithmetic deductions below are independently proved. Neither a published cycle record nor a resolution of all positive sources is claimed.

## 1. Original map and the nine retained integral sections

Use the same formula on nonzero odd integers of either sign:

\[
T(x)=\frac{3x+1}{2^{\nu_2(3x+1)}}.
\]

The positive source used for the conclusion is always \(X=\{1,3,5,\ldots\}\). No replacement of the forcing by \(3x-1\) is made. For an ordered word \(p=(a_1,\ldots,a_m)\), retain

\[
A_j=\sum_{i=1}^j a_i,\quad A=A_m,\quad U=2^A,\quad L=3^m,
\quad C=\sum_{j=0}^{m-1}3^{m-1-j}2^{A_j}.
\]

Composition in chronological order is

\[
f_p(x)=\frac{Lx+C}{U}.
\tag{1}
\]

The following two signed cycles are verified directly under this original formula:

\[
-5\xrightarrow{1}-7\xrightarrow{2}-5,
\]
\[
-17\xrightarrow{1}-25\xrightarrow{1}-37\xrightarrow{1}-55
\xrightarrow{2}-41\xrightarrow{1}-61\xrightarrow{1}-91
\xrightarrow{4}-17.
\tag{2}
\]

For each of their nine distinct vertices \(-h\), let \(p_h\) be the original exponent word beginning at that vertex. All rotations and their original starting vertices are retained:

| \(h\) | \(p_h\) | \((m,A)\) |
|---:|---|---|
| 5 | (1,2) | (2,3) |
| 7 | (2,1) | (2,3) |
| 17 | (1,1,1,2,1,1,4) | (7,11) |
| 25 | (1,1,2,1,1,4,1) | (7,11) |
| 37 | (1,2,1,1,4,1,1) | (7,11) |
| 55 | (2,1,1,4,1,1,1) | (7,11) |
| 41 | (1,1,4,1,1,1,2) | (7,11) |
| 61 | (1,4,1,1,1,2,1) | (7,11) |
| 91 | (4,1,1,1,2,1,1) | (7,11) |

For each row,

\[
L>U,\qquad C=h(L-U),\qquad f_{p_h}(-h)=-h.
\tag{3}
\]

Thus the original marked class \([C]\) in \(\mathbb Z/(U-L)\mathbb Z\) vanishes, with its actual integral primitive \(-h\). This is a **negative** primitive, not a positive Collatz cycle. For the two-letter rows the ambient group has modulus one; for the seven-letter rows it has modulus 139. Their zero forcing classes do not identify those different presented objects or their different sections.

The retained extension matrix is

\[
M_p=\begin{pmatrix}L&C\\0&U\end{pmatrix}.
\]

For the integral section \(s_n(1)=e_2+ne_1\), the actual intertwining defect is

\[
M_ps_n(1)-s_n(U)=\bigl(C-(U-L)n\bigr)e_1
=(L-U)(n+h)e_1.
\tag{4}
\]

Changing the section changes (4), although its quotient class remains \([C]=0\). This is the information from the supported section which will be used on the positive source. The exact coordinate change \(z=n+h\), inverse \(n=z-h\), gives \(z\mapsto(L/U)z\) for this packet. Neither the original positive domain nor the inverse translation is removed.

## 2. Complete positive shadow lattice, with inverse maps

### Proposition 1. Positive realizations of a repeated retained packet

For every \(h\) in (2) and integer \(r\ge1\), the complete positive source realizing \(p_h^r\) is

\[
\boxed{\quad n=2U^r t-h,\quad t\in\mathbb Z_{\ge1},\qquad
T^{mr}(n)=2L^r t-h.\quad}
\tag{5}
\]

The inverse source and target parameters are \((n+h)/(2U^r)\) and \((y+h)/(2L^r)\), on these stated images. The source step \(2U^r\) and target step \(2L^r\) remain different, original integers.

**Proof.** Formula (3) gives by composition

\[
f_{p_h^r}(x)=\frac{L^r(x+h)}{U^r}-h.
\tag{6}
\]

For an actual positive source, both its initial and terminal values are odd. The section defect for the repeated word is
\((L^r-U^r)(n+h)\); its equality to \(U^r(f(n)-n)\) makes it divisible by \(2U^r\). Since \(L^r-U^r\) is odd, it is coprime to \(2U^r\), proving the source congruence in (5).

Conversely write \(-h_j\) for the successive vertices of the signed orbit repeated \(r\) times, and \(A_j\) for the original prefix sums of that repeated word. At every position,

\[
x_j=-h_j+2^{Ar+1-A_j}3^j t.
\tag{7}
\]

These are integers and are odd, because each correction is even. The original affine equations give \(3x_{j-1}+1=2^{a_j}x_j\); hence their valuations are exactly \(a_j\). The starting value in (5) is positive: \(U\ge h+1\) for the listed anchors. Positivity propagates along the displayed equations. Formula (7) proves every intermediate original value and gives (5) at the endpoint. Positivity of \(n\) forces \(t\ge1\); every such integer is allowed. The inverse identities are substitutions. ∎

There is an exact common path object, not an assumed map from a negative cycle to a positive cycle. Take the finite position **interval** with vertices \(0,\ldots,mr\) and its consecutive edges. Evaluation at \(-h_j\) and at \(x_j\) gives two maps into the original signed and positive graphs. They preserve both source and target maps, and hence their incidence differentials and the first-jet differentials. The negative evaluation identifies its endpoints. The positive evaluation has endpoints (5); identifying them would require the additional, generally false, equality \(2U^r t-h=2L^r t-h\). That endpoint defect is retained.

The source module, its original relation submodule, the supported label \(p_h\), and its selected integral primitive are therefore all used. No chronological meaning is assigned to intrinsic Split-Zero support.

## 3. The second section: arbitrary falling tails around the fixed point 1

Let \(q=(c_1,\ldots,c_s)\), where \(s\ge1\) and every \(c_i\ge2\). Put

\[
B_j=\sum_{i=1}^j c_i,\quad B=B_s,\quad U_q=2^B,\quad L_q=3^s,
\]
\[
C_q=\sum_{j=0}^{s-1}3^{s-1-j}2^{B_j},\qquad
E_q=C_q+3^s-2^B.
\]

The change of coordinate \(w=x-1\), inverse \(x=w+1\), gives the **exact** formula

\[
f_q(x)-1=\frac{3^s(x-1)+E_q}{2^B},
\qquad
E_q=\sum_{i=1}^s3^{s-i}2^{B_{i-1}}(4-2^{c_i}).
\tag{8}
\]

It follows that \(E_q\le0\), with equality exactly for the pure-two tail. Every coefficient in the sum is positive and each final factor is nonpositive, proving both assertions. Equivalently, appending \(c\) changes \(E\) to \(3E+(4-2^c)2^{B_{\rm old}}\).

A zero \(E_q\) remains a supported forcing value. The pure-two tail still has all its original edges, original differential, and multiplier \(3^s/4^s\). It is not removed from the word or its module.

The two section coordinates are related by the exact affine map

\[
w=z-(h+1),\qquad z=w+(h+1).
\tag{9}
\]

The translation \(h+1\) is the critical retained term. Dropping it would falsely replace coefficient contraction by actual descent.

## 4. The arithmetic gap that controls that translation

### Theorem 2. Two all-length integer gap inequalities

For either row

\[
(U,L,K)=(8,9,4)\quad\text{or}\quad(2048,2187,46),
\]

and integers \(r,s\ge1\), \(B\ge2s\), define

\[
D=U^r2^B-L^r3^s.
\]

On the complete positive-gap domain \(D>0\),

\[
\boxed{\quad D>K(2^B-3^s).\quad}
\tag{10}
\]

The next section proves the theorem by an explicit logarithm bound and a complete finite certificate. The coarser cones at the end of that section have a separate elementary proof.

The result is a statement about the indicated original integers, not a numerical approximation to the ratio of the two sides. All \(r,s,B\) are unrestricted within the displayed domain.

## 5. Proof of the gap theorem

Write the required positive margin as

\[
H(r,s,B)=(U^r-K)2^B-(L^r-K)3^s.
\tag{11}
\]

The listed constants satisfy \(U\ge2K\), \(U<L\), and

\[
16U-9L>7K.
\tag{12}
\]

The first row has difference 47 versus 28; the second has difference 13085 versus 322.

### 5.1 An elementary whole half-space

For \(s\ge2r\), \(B\ge2s\), it suffices to take \(B=2s\), because \(U^r-K>0\). After division by \(3^s\), the margin is increasing in \(s\), so it suffices to take \(s=2r\). At that value the desired comparison is

\[
(16U)^r-(9L)^r>K(16^r-9^r).
\]

Use \(a^r-b^r=(a-b)\sum_{j=0}^{r-1}a^{r-1-j}b^j\). By (12), and the termwise bounds \(16U\ge16\), \(9L\ge9\), the left side is strictly larger than
\(7K\sum16^{r-1-j}9^j=K(16^r-9^r)\). This proves the entire half-space.

### 5.2 Reduce every other case to its first crossing

It remains to take \(1\le s<2r\). For fixed \(r,s\), let \(B_0\) be the least integer \(B\ge2s\) with \(D>0\). It exists and

\[
2s\le B_0\le4r,
\tag{13}
\]

because \(U^r2^{4r}>L^r3^{2r}\ge L^r3^s\) by (12). The margin (11) increases with \(B\). A failure anywhere therefore gives a failure at \(B_0\).

Define the **same original** logarithmic gap

\[
\Lambda=\frac{U^r2^{B_0}}{L^r3^s}-1
=2^{A_*}3^{-m_*}-1>0,
\]
\[
A_*=Ar+B_0\le15r,\qquad m_*=mr+s\le9r.
\tag{14}
\]

The letters \((m,A)\) here are (2,3) or (7,11). A supposed failure of (10) gives

\[
D\le K(2^{B_0}-3^s)<K2^{B_0},
\]

and hence

\[
\Lambda<\frac{K}{U^r-K}\le\frac{2K}{U^r}\le\frac{92}{8^r}.
\tag{15}
\]

The retained correction \(K\) has not been omitted in this estimate.

### 5.3 The established transcendence input

Use the rational-number instance of Matveev's theorem printed as Theorem 2.1 in [M]. The positive rational numbers are exactly 2 and 3, and their nonzero integer exponents are \(A_*\) and \(-m_*\). Unique prime factorization proves that the expression is nonzero. The heights are \(\log2\) and \(\log3\). Its coefficient is safely bounded by

\[
1.4\,30^5\,2^{4.5}\log2\log3
<\frac{14}{10}30^5\cdot24\cdot\frac7{10}\cdot\frac{11}{10}
=628689600<10^9.
\]

Since \(2^{A_*}>3^{m_*}\), we have \(A_*>m_*\), so the exponent maximum may be taken as \(A_*\). The resulting bound is

\[
\log\Lambda>-10^9(1+\log A_*).
\tag{16}
\]

This external transcendence theorem is an explicit dependency. Neither the finite Python tests nor this note are offered as a new proof of Matveev's theorem.

Combining (15) and (16), and using \(\log8>1\), forces

\[
r<10^9(1+\log(15r))+\log92.
\tag{17}
\]

This gives \(r<10^{12}\). Indeed the finite rational sums
\(\sum_{j=0}^{100}36^j/j!>15\cdot10^{12}\) and
\(\sum_{j=0}^{6}5^j/j!>92\) prove the needed upper logarithm bounds at \(10^{12}\). At that endpoint the right side of (17) is less than \(37\cdot10^9+5<10^{12}\). The derivative of left minus right is \(1-10^9/r>0\) thereafter.

### 5.4 A completely rational denominator certificate

For \(x=2,3\), put \(z=(x-1)/(x+1)\). The positive series and its geometric remainder give

\[
2\sum_{j=0}^{127}\frac{z^{2j+1}}{2j+1}<\log x<
2\sum_{j=0}^{127}\frac{z^{2j+1}}{2j+1}
+\frac{2z^{257}}{257(1-z^2)}.
\tag{18}
\]

Let the corresponding rational bounds be \(l_2,u_2,l_3,u_3\). The certificate checks, entirely by integer cross-multiplication,

\[
\frac{83130157078217}{52449289519716}
<\frac{l_3}{u_2}<\frac{\log3}{\log2}
<\frac{u_3}{l_2},
\]
\[
\frac{u_3}{l_2}+2^{-128}
<\frac{350861368503572}{221368876767703}.
\tag{19}
\]

The two outer fractions have determinant one, and their denominators sum to

\[
273818166287419>9\cdot10^{12}.
\tag{20}
\]

Here is the precise denominator fact used. Between \(p/q<t/u\) with \(tq-pu=1\), an original fraction \(a/b\) has positive integers \(k=aq-pb\), \(j=tb-au\). Direct expansion gives \(b=uk+qj\ge u+q\). The fraction \(a/b\) need not be reduced; original multiplicities are retained.

For \(r\ge128\), the alleged failure satisfies

\[
0<\frac{A_*}{m_*}-\frac{\log3}{\log2}
=\frac{\log(1+\Lambda)}{m_*\log2}
<\frac{184}{8^r}<2^{-128}.
\tag{21}
\]

The last inequality is checked at 128 by \(184\cdot2^{128}<8^{128}\) and persists thereafter. We used \(\log(1+\Lambda)<\Lambda\) and \(\log2>1/2\). Equations (17), (20) give \(m_*<9\cdot10^{12}\), contradicting the denominator fact and (19). This excludes every \(r\ge128\) at once.

### 5.5 The complete remaining finite base

For each of the two triples, the verifier checks every

\[
1\le r\le127,\qquad 1\le s\le2r,
\]

computes the least \(B_0\ge2s\) by integer doubling, and verifies

\[
(U^r-K)2^{B_0}>(L^r-K)3^s.
\]

There are exactly 16256 rows for each triple, 32512 total. The full triples \((r,s,B_0)\) are delivered in `gap_bases.json.gz`. The checker regenerates them, verifies first-crossing minimality and the strict margin, and compares every byte of the canonical table. It also records a hash of every exact integer margin. The smallest margins are 1 and 1631-46=1585 respectively. Increasing \(B\) preserves the comparison, while Section 5.1 treats every longer tail. This completes the proof of Theorem 2. ∎

### 5.6 Stronger elementary cones requiring no logarithm theorem

For the first triple, the gap margin is positive throughout
\(s\ge\lceil r/2\rceil\), \(B\ge2s\). For the second it is positive throughout
\(s\ge\lceil r/4\rceil\), \(B\ge2s\).

Here is an elementary induction. Let \(d=2\) or 4 respectively, and \(\mu=3L^d\). The listed constants satisfy \(4U^d>3L^d\) and \(\mu>7\). For the pure-two margins,

\[
H(r+d,s+1,2s+2)-\mu H(r,s,2s)
=(4U^d-3L^d)U^r4^s
+K\bigl((\mu-4)4^s-(\mu-3)3^s\bigr)>0.
\tag{22}
\]

The last bracket is positive for \(s\ge1\), since its value after division by \(3^s\) is at least \((\mu-7)/3\). The finitely many seeds \(r=1,\ldots,d\), \(s=1\) have positive margins and are explicitly checked. This gives the boundary \(s=\lceil r/d\rceil\); monotonicity gives all larger \(s,B\). This result is independent of [M]. The full positive-gap domain in (10) is wider and uses the proof above.

## 6. The actual positive descent theorem

### Theorem 3. Repeated-shadow/falling-tail descent, at the actual coefficient crossing

For any of the nine \(p_h\), let an original positive source realize

\[
p_h^r(c_1,\ldots,c_s),\qquad r,s\ge1,\quad c_i\ge2.
\]

On the entire domain

\[
\boxed{\quad U^r2^B>L^r3^s,\qquad B=\sum_i c_i,\quad}
\tag{23}
\]

its endpoint is strictly below its source. The domain uses the **actual total tail exponent**, not the all-two comparison total. All repetitions, tail lengths and individual exponents are unbounded.

**Proof.** By Proposition 1, \(n=2U^r t-h\), \(t\ge1\). The original combined numerator is

\[
C_{\rm total}=3^s h(L^r-U^r)+U^r C_q.
\]

Use the original endpoint equation and (8) to obtain the exact displacement

\[
\boxed{\quad n-y=
\frac{2Dt-(h+1)(2^B-3^s)-E_q}{2^B}.\quad}
\tag{24}
\]

Equivalently its numerator is
\(2[D-K_h(2^B-3^s)]+2D(t-1)-E_q\), with \(K_h=(h+1)/2\).
For the two-letter anchors \(K_h\le4\), and for the seven-letter anchors \(K_h\le46\). Since \(2^B>3^s\), Theorem 2 proves the first bracket positive. The remaining terms are nonnegative. Thus \(n-y>0\). Both endpoints are actual odd integers, so their difference is at least two. Every term in (24), including a supported zero \(E_q=0\), remains present. ∎

This also locates the formal positive fixed point of the whole word below the least possible positive source of its repeated prefix:

\[
0<\frac{C_{\rm total}}D<2U^r-h.
\tag{25}
\]

Indeed substituting \(t=1\) in the original section displacement proves
\(D(2U^r-h)-C_{\rm total}>0\); this is an integer comparison, not a claim that this lower bound already realizes the tail.

### Corollary 3.1. Complete cycle-word exclusion

There is no positive integer cycle with a traversal word which is a cyclic rotation of \(p_h^r(c_1,\ldots,c_s)\), with the parameters above. Repetitions of such a traversal are not new cases.

**Proof.** An actual positive cycle obeys
\(2^{Ar+B}=\prod(3+1/x_i)>3^{mr+s}\). Thus (23) holds on that original traversal. Theorem 3 makes its endpoint strictly smaller than its starting vertex, contradicting closure. A traversal consisting only of \(p_h^r\) has the sole affine fixed point \(-h\) by (6), outside the positive source. Rotation is the invertible reindexing of the same original vertices and edges. ∎

This excludes arbitrary numbers of separated rises, not just one consecutive run of exponent one. For example every word \((1,2)^r\) followed by any nonempty all-falling tail belongs to this exclusion family. The seven-letter motifs give another family with several rise and fall transitions in each repeated packet.

The result is not an all-word cycle exclusion. In the earlier count sector \((m,A,k)=(3631,5755,1507)\), it eliminates the original ordering
\((1,2)^{1507}(2)^{617}\), and its retained cyclic rotations. The other gap orderings remain present. No stronger global numerical cycle bound is inferred.

## 7. Full source/target cylinders for every admitted falling word

The universal statement can be used without replacing its source by sampled starts. Let \(r_q\) be the least positive odd residue for the original tail word:

\[
r_q\equiv(2^B-C_q)(3^s)^{-1}\pmod{2^{B+1}}.
\]

At the repeated-packet endpoint \(x=2L^rt-h\), the legal tail condition is exactly

\[
t\equiv t_0:=\frac{r_q+h}{2}(L^r)^{-1}\pmod{2^B}.
\tag{26}
\]

Take \(0\le t_0<2^B\), and let \(t_{\min}=t_0\) for \(t_0>0\), otherwise \(t_{\min}=2^B\). The complete positive source and target are

\[
\boxed{
\begin{aligned}
n(v)&=2U^r t_{\min}-h+2U^r2^Bv,\\
y(v)&=y_0+2L^r3^s v,\qquad v\in\mathbb Z_{\ge0},
\end{aligned}}
\tag{27}
\]

where \(y_0=(L^r3^s n(0)+C_{\rm total})/(U^r2^B)\). The inverse parameters are \((n-n(0))/(2U^r2^B)\) and \((y-y_0)/(2L^r3^s)\). Formula (26) follows by dividing the even congruence \(2L^rt-h\equiv r_q\pmod{2^{B+1}}\) by two, whose inverse step is multiplication by two. The odd number \(L^r\) is invertible modulo \(2^B\). These calculations prove compatibility, completeness, and both inverse identities. The zero residue case is retained and has its correct positive lower bound.

In this chart

\[
n(v)-y(v)=n(0)-y_0+2Dv.
\]

The whole-cylinder descent comes from (24), not from point sampling.

## 8. Return to the unchanged integral first-jet comparison

The absolute original graph, its maps \(J,P\), and the ring \(\mathbb Z[\epsilon]/\epsilon^2\) are the predecessor's. In particular

\[
d_\epsilon=d-\epsilon P,\qquad d=J-P.
\]

For the actual finite edge chain \(c_{p,q}(n)\) of (27),

\[
d_\epsilon(\epsilon c_{p,q}(n))
=\epsilon V_n-\epsilon V_y.
\tag{28}
\]

The constant boundary is zero because the constant chain coefficient here is zero; the linear boundary is the original telescoping edge boundary. Thus in the retained reduction kernel \(\mathfrak B_X\),
\([\epsilon V_n]=[\epsilon V_y]\) with \(y<n\) on (23).

An existing finite integral witness \(d_\epsilon(b_y+\epsilon c_y)=\epsilon V_y\) splices to

\[
d_\epsilon\bigl(b_y+\epsilon(c_{p,q}(n)+c_y)\bigr)=\epsilon V_n.
\tag{29}
\]

No division by a cycle length or change to rational coefficients occurs. The unchanged predecessor validator checks both coefficients and extracts an actual path to 1. The new verifier executes (29) on the delivered examples.

Equation (28) alone is a descent relation, not a claim that every variable endpoint \(y(v)\) is already known to reach 1. It excludes every admitted source from being the least vertex of a nonbase component, whether that component is periodic or nonperiodic. Full source coverage still requires more arithmetic.

## 9. The exact remaining falling-tail language

For a fixed \(p_h^r\), a falling tail not yet certified by (23) must have

\[
U^r2^B<L^r3^s,
\qquad B\le H_s:=\lfloor\log_2(L^r3^s)\rfloor-Ar.
\tag{30}
\]

There is no equality between the original powers of 2 and 3. The logarithm floor is computed exactly as an integer bit length. A tail of \(s\) exponents at least two has \(B\ge2s\). Only \(s<2r\) can remain by Section 5.1, and the stronger elementary cones give the smaller cutoffs as well.

For each remaining \(s\), the complete number of such words is

\[
\binom{H_s-s}{s}.
\tag{31}
\]

Subtracting one from each original exponent gives a composition with positive parts and sum at most \(H_s-s\); stars and bars gives (31), with inverse adding one. The ordered parts themselves and their source cylinders remain available. The empty tail is retained separately.

Thus at fixed repetition count, the next exponent-one switch can occur only after a finite, exactly specified list of uncontracted falling tails. Crossing tails have no positive exception box: Theorem 3 proves descent on their complete positive source. This does not make the whole orbit finite; it identifies the original mixed-switch frontier left by these new rules.

## 10. An exact reset law, followed by an actual repair

For the \(h=5\) packet, take the entire stratum \(t\equiv1\pmod8\) in (5). Its next exponent is exactly three, because

\[
3(2\cdot9^rt-5)+1=2(3\cdot9^rt-7),
\quad \nu_2(3\cdot9^rt-7)=2.
\]

After that step the original value is

\[
x=\frac{3\cdot9^rt-7}{4},\qquad
\nu_2(x+1)=\nu_2(9^rt-1)-2.
\]

Consequently its next maximal exponent-one run has exact length

\[
\boxed{k=\nu_2(9^rt-1)-3,}
\tag{32}
\]

with complete parameter stratum

\[
t\equiv9^{-r}(1+2^{k+3})\pmod{2^{k+4}}.
\tag{33}
\]

The endpoint after those \(k\) ones is
\(3^{k+1}(9^rt-1)/2^{k+2}-1\). The next exponent is at least two. Formulas (32)-(33) are inverse descriptions of the exact valuation, and their residues automatically lie in \(1\pmod8\). They retain the dependence on \(t\), which permits arbitrary reset depths.

On the particular anchor ladder \(t=1\), this becomes

\[
k=\nu_2(r).
\tag{34}
\]

An elementary proof suffices: an odd exponent in \(9^d-1\) leaves its valuation at 3, since its geometric quotient has an odd number of odd summands. Doubling multiplies by \(9^d+1\), of valuation one. Hence \(\nu_2(9^r-1)=3+\nu_2(r)\). This is an exact reset law, not a global decreasing-rank assertion for arbitrary \(t\).

At \(r=12,t=1\), the source \(137438953467\) follows \((1,2)^{12}\), then exponent three, but the latter endpoint is still \(211822152359\). The next exponent is one, so the falling-tail theorem correctly retains this switch. Formula (34) determines the next run to have length two.

Continuing on that same original source gives the complete first-descent word

\[
w=(1,2)^{12}(3,1,1,2,1,2,1,2,1,7),
\quad |w|=34,\quad A(w)=57.
\]

Its original coefficients are

\[
L=16677181699666569,\quad U=144115188075855872,
\quad C=81607860757265581.
\]

Every proper prefix has \(D_j\le0\), and the final source satisfies \(Dn_0>C\). Therefore the entire original cylinder has its first strict descent at that last return:

\[
\boxed{
137438953467+2^{58}v
\longmapsto
15904599857+33354363399333138v,
\qquad v\ge0.
}
\tag{35}
\]

The proof is the original prefix inequality \(T^j(n)<n\iff D_jn>C_j\), the literal cylinder congruence, and the positive final constant and slope of \(Dn-C\). The checker recomputes every prefix and independently replays three lifts. Thus the failed applicability of one rule produces another complete arithmetic family. Formula (35) is not generalized to every \(r\) without proof.

## 11. Evidence, reproduction, and remaining scope

`verify.py` checks the signed original cycles, complete positive shadow congruences, 32512 integer gap rows, the rational logarithm intervals, original falling-word cylinders, supported zero tail forcings, first-jet boundaries, finite splices and reset strata. It rejects malformed anchor, exponent, lattice and status records. `gap_bases.json.gz` contains the complete base tables; `examples.json` contains the actual original paths and integral witnesses. `verification.json` separates the executed scopes. Ordinary and optimized outputs must agree byte for byte.

`crosscheck_atlas.py` is an optional crosswalk into the earlier local source atlas. It does not participate in the all-length proof. It identifies already-proved first-descent cells that are instances of this theorem; it neither rediscovers their points nor treats that finite collection as proof for the unrestricted repetition parameter.

No positive infinite survivor is certified by a finite remaining word label. No new common interval bound or numerical cycle record is claimed. The next arithmetic calculation is on the exact switch residues (33), the residual word families (30), and their original source parameters. The full conjecture still requires coverage of every ordinary positive source, or a rigorously surviving one. All statements above retain the ordinary integer lattice and the exact maps into the original first-jet kernel.

## Sources

**[P]** `intrinsic_zero_firstjet_20260915/note.md` and `firstjet.py`, Collatz repository commit `d0c987b12c20be5978f496ab1ef2a60018caa5e5`. The executed dependency is the unchanged `firstjet.py`, Git blob `97f9ef5ad535f7ec18259d41fab6a3557be17d98`. This supplies the original integral kernel and finite-witness validator, not Theorem 2.

**[A]** The separately delivered `defect_rank_descent_20260915` local contribution: section defects and their exact repetition congruences; original source atlas; all-length rise/fall and logarithm certificate. Its files remain unchanged. The gap proof above re-establishes the needed integer and rational comparisons independently and has no dependency on that atlas or its convergence interval.

**[M]** A. Languasco, F. Luca, P. Moree and A. Togbe, *Sequences of integers generated by two fixed primes*, Abhandlungen aus dem Mathematischen Seminar der Universitat Hamburg 95 (2025), 123-148, DOI `10.1007/s12188-025-00293-9`, Theorem 2.1. Its rational-number formulation of Matveev's established theorem was read in the primary publisher text during this continuation. The paper attributes its formulation to Bugeaud, Mignotte and Siksek and the underlying theorem to Matveev. No primary-literature file is copied into this package.

The original Split-Zero construction and research direction remain attributed to the owner's programme. Standard affine composition, finite graph incidence, geometric sums, and rational denominator lemmas are not assigned new priority here. This is a written mathematical contribution with exact computational certificates, not an independent external review or a new Lean proof.
