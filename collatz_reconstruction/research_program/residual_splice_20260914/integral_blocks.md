# Integral block maps, retained forcing, and the next cycle sector

14 September 2026. Continuation of the original Collatz cycle complex in `../cycle_relative_cohomology_20260914/note.md` at repository commit `32b8f3b9cc6dcfc4387ff783c4f4a6f6a365f717`.

This note supplies the chain equivalence used by `residual_descent.block_comparison`. The original ordered word, the chosen block boundaries, all original coefficients, and the forcing vector remain part of the input. The compressed matrix alone is not substituted for that input.

## 1. Source complex and literal block telescoping

Let \(p=(a_1,\ldots,a_m)\), with \(a_j\ge1\), and put \(A_j=\sum_{v\le j}a_v\), \(A_0=0\). The source complex, in degrees zero and one, is
\[
 K_p=[\mathbb Z^m\xrightarrow{B}\mathbb Z^m],\qquad
 (Bx)_j=2^{a_j}x_{j+1}-3x_j,\quad x_{m+1}=x_1.
 \tag{B1}
\]
Set \(L=3^m\), \(U=2^{A_m}\), \(D=U-L\). The integer \(D\) is nonzero and coprime to 6. Retain the functional
\[
 f_j=3^{m-j}2^{A_{j-1}},\qquad fB=D e_1^T.
 \tag{B2}
\]
The determinant has absolute value \(|D|\). The first and last coefficients of \(f\) are powers of 3 and 2 respectively, so their greatest common divisor is one. Thus \(f\) induces an isomorphism
\[
 \operatorname{coker}B\longrightarrow\mathbb Z/D\mathbb Z,
 \qquad [b]\longmapsto[f b].
 \tag{B3}
\]
For completeness, (B2) proves well-definedness. Primitivity of \(f\) proves surjectivity, and the determinant proves that the two finite groups have the same order. In particular, an integral vector \(b\) lies in \(B\mathbb Z^m\) exactly when \(D\mid f b\). The matrix itself is injective over \(\mathbb Z\).

Partition the ordered word into nonempty consecutive blocks \(q_1,\ldots,q_k\), starting at original positions \(s_1=1,s_2,\ldots,s_k\). For each block retain
\[
 L_i=3^{|q_i|},\quad U_i=2^{\sum q_i},\quad
 C_i=\sum_{j=1}^{|q_i|}3^{|q_i|-j}2^{\sum_{v<j}(q_i)_v}.
\]
Define \(P_0:\mathbb Z^m\to\mathbb Z^k\) by \((P_0x)_i=x_{s_i}\). Define \(R:\mathbb Z^m\to\mathbb Z^k\) by placing the local row (B2) of block \(q_i\) in the columns of that block, with zeros elsewhere. Finally define
\[
 (Gz)_i=U_i z_{i+1}-L_i z_i,\quad z_{k+1}=z_1.
 \tag{B4}
\]
For one block, the two contributions are added in the same entry, giving \(G=(D)\), not a two-entry matrix.

The local telescoping identity is precisely
\[
 RB=G P_0. \tag{B5}
\]
No coefficient is divided out. Its affine instance is \(U_i x_{s_{i+1}}-L_i x_{s_i}=C_i\) for the original forcing \(Bx=\mathbf1\).

Write
\[
 \bar f_i=\left(\prod_{v>i}L_v\right)\left(\prod_{v<i}U_v\right).
\]
Then direct multiplication gives
\[
 \bar fG=D e_1^T,\qquad f=\bar fR. \tag{B6}
\]
The endpoint coefficients of \(\bar f\) are again coprime powers of 3 and 2. The determinant of \(G\) has absolute value \(|\prod U_i-\prod L_i|=|D|\). The same argument as (B3) gives the marked cokernel isomorphism induced by \(\bar f\). Hence the map induced by \(R\) is the identity on the original \(\mathbb Z/D\mathbb Z\) coordinate:
\[
 [b]\longmapsto[Rb],\qquad [f b]=[\bar fRb]. \tag{B7}
\]

## 2. Integral inverse and both homotopies

Each local row of \(R\) is primitive. Construct an integral right inverse \(S_1:\mathbb Z^k\to\mathbb Z^m\) as follows. For a block of one letter use its single coefficient 1. For a longer block, use the extended Euclidean algorithm to choose integers \(u_i,v_i\) with
\[
 u_i 3^{|q_i|-1}+v_i2^{\sum_{j<|q_i|}(q_i)_j}=1.
\]
Place \(u_i,v_i\) in the first and last rows of column \(i\) of \(S_1\), and zero elsewhere. Blocks have disjoint column supports, so
\[
 RS_1=I_k. \tag{B8}
\]
Use the rational inverse of the original nonsingular matrix to specify
\[
 S_0=B^{-1}S_1G,\qquad H=B^{-1}(I_m-S_1R). \tag{B9}
\]
These formulas define **integral matrices**. Indeed, by (B6)–(B8),
\[
 fS_1G=\bar fG=D e_1^T,\qquad f(I_m-S_1R)=0.
\]
Criterion (B3), applied to each column, places both numerators in \(B\mathbb Z^m\). Thus the unique rational preimages in (B9) have integer coordinates. This proves integrality rather than discarding denominators after a rational calculation.

The resulting identities are
\[
 BS_0=S_1G,\qquad P_0S_0=I_k,\qquad RS_1=I_k,
 \tag{B10}
\]
\[
 BH=I_m-S_1R,\qquad HB=I_m-S_0P_0,\qquad P_0H=0.
 \tag{B11}
\]
The first identity of (B10) and the first of (B11) follow from (B9). For the second identity of (B10), multiply by \(G\):
\[
 GP_0S_0=RBS_0=RS_1G=G.
\]
Injectivity of \(G\) implies the claim. Also
\[
 HB=B^{-1}(B-S_1RB)=I_m-S_0P_0.
\]
Finally \(GP_0H=RBH=R-RS_1R=0\), giving \(P_0H=0\).

Therefore \((P_0,R):K_p\to[\mathbb Z^k\xrightarrow G\mathbb Z^k]\) and \((S_0,S_1)\) are integral chain maps, their composition on the block complex is the identity, and their composition on the original complex is chain homotopic to the identity by the explicitly specified \(H\).

### Forced equations over every coefficient ring

Let \(b\) be a specified forcing vector. For every commutative coefficient ring, including \(\mathbb Z\) and \(\mathbb Z/N\mathbb Z\), the maps
\[
 x\longmapsto z=P_0x,\qquad
 z\longmapsto x=S_0z+Hb \tag{B12}
\]
are inverse bijections between the solution sets
\[
 Bx=b\quad\text{and}\quad Gz=Rb.
\]
In fact,
\[
 B(S_0z+Hb)=S_1Gz+(I_m-S_1R)b=b,
\]
\(P_0(S_0z+Hb)=z\), and for a source solution,
\(S_0P_0x+HBx=x\), by (B10)–(B11). These polynomial matrix identities remain true after reduction modulo \(N\); no inversion of \(D\) in the coefficient ring occurs.

The offset \(Hb\) is indispensable. Retaining only the homogeneous chain map \(S_0\) would not give the inverse of the original affine problem. Positivity and actual valuations are tested on the reconstructed full coordinates. For a positive integral solution with \(b=\mathbf1\), reduction of each original equation modulo 2 gives oddness of every \(x_j\); the original equation then gives its exact valuation \(a_j\). This recovers an actual positive Collatz cycle, not merely a block congruence.

## 3. Anchor at the actual fixed orbit, without erasing the word

Use the coordinate map \(y=x-\mathbf1\) with inverse \(x=y+\mathbf1\). For the original \(+1\) forcing the new right-hand side is
\[
 By=\mathbf1-B\mathbf1=(4-2^{a_j})_{j=1}^m.
\]
By (B5), its exact image is
\[
 G(P_0y)=(C_i+L_i-U_i)_{i=1}^k. \tag{B13}
\]
Both the original forcing and this specified affine coordinate map remain recorded.

Consider a block consisting of a 1 followed by \(r\ge0\) twos. Its unreduced data are
\[
 U_r=2\cdot4^r,\quad L_r=3^{r+1},\quad C_r=2\cdot4^r-3^r,
\]
\[
 C_r+L_r-U_r=2\cdot3^r. \tag{B14}
\]
To prove the numerator formula, apply the recurrence \(C_{r+1}=3C_r+2\cdot4^r\) with \(C_0=1\); substituting (B14) satisfies the recurrence exactly. Thus a cyclic word with one 1 at the beginning of each retained block has anchored equations
\[
 2\cdot4^{r_i} y_{i+1}-3^{r_i+1} y_i=2\cdot3^{r_i}.
 \tag{B15}
\]
Here a row represents the original block \((1,2,\ldots,2)\) of length \(r_i+1\). The gap dictionary \((r_i)\) and the rotation offset recover the original word. A cyclic rotation by offset \(h\) is inverted by rotation by \(m-h\); on vertex coordinates the index correspondence is \(i\mapsto i+h\pmod m\). No passage to unmarked rotation classes is performed.

## 4. Actual edge chains and a prime-power control

The weighted affine complex above and the actual orbit graph are connected through the solved original coordinates, not by identifying their differentials. For a positive integral solution, map original position \(j\) to actual vertex \(x_j\) and its edge to \(e_{x_j}\). The original equation proves that this is an actual orbit edge.

The ordinary chain map from the selected block circle to the full position circle sends block vertex \(i\) to position \(s_i\), and block edge \(i\) to the sum of original edges in \(q_i\). Its boundary telescopes from \(s_i\) to \(s_{i+1}\). Composing with the actual orbit map gives the original path chain for that block. The block circle's fundamental cycle maps to the same full cycle chain \(\sum_j e_{x_j}\). Passing to the predecessor's relative graph kills only the vertex and loop at the actual fixed point 1. Repeated traversals remain their explicit integer multiplicities.

For the word \(p=(1,1,2,4,3)\), split into blocks of lengths 1 and 4. The result is
\[
 G=\begin{pmatrix}-3&2\\1024&-81\end{pmatrix},\qquad
 R\mathbf1=\begin{pmatrix}1\\197\end{pmatrix},\qquad D=1805=5\cdot19^2.
\]
The block solution is \((5/19,17/19)\). The marked original cokernel coordinate is
\[
 \bar f=(81,2),\qquad \bar f R\mathbf1=81+2\cdot197=475.
\]
Its order in \(\mathbb Z/1805\mathbb Z\) is 19. The first equation modulo any odd \(N\) gives \(z_2=(1+3z_1)/2\). Substitution into the second gives
\[
 1805z_1=475\pmod N.
\]
Consequently there are exactly 19 solutions at \(N=19\) and none at \(N=361\). The bijection (B12) transfers these counts to the full five-equation system. This is the predecessor's original prime-power obstruction, retained under the new block comparison. The checker also exhausts the possible first coordinate at both moduli.

## 5. The next arithmetic sector after the executed exclusion

The accompanying `note.md`, Theorem 4, excludes all nontrivial positive cycles with at most 402 exponent-1 positions in their primitive word. Its next unexcluded 403-position sector is forced by the exact period comparisons to have
\[
 m=971,\qquad A=1539,\qquad k=403,\qquad
 99781\le\min x_j\le330749.
\]
Since \(A=2m-k+\sum_{a_j\ge3}(a_j-2)\), every letter in this sector is 1 or 2. Cut at the 403 occurrences of 1, retaining the original rotation offset. Then
\[
 r_i\ge0,\qquad \sum_{i=1}^{403}r_i=568.
\]
Equation (B15) gives a 403-equation **integral** system with total
\[
 D=2^{1539}-3^{971},
\]
and the original right-hand side retained as (B13). Formula (B12) reconstructs every original coordinate over \(\mathbb Z\) or modulo any selected prime power. Integrality, positivity, the chosen minimum placement, and the original valuation word remain required. No solution or exclusion of this entire sector is asserted here.

This identifies an exact next computation: either discharge its full possible minimum interval by additional original-source descent certificates, or prove a marked forcing obstruction for every retained gap tuple, with any finite-coefficient test transported by (B12). An unmarked diagonal spectrum, a prime-only test, or the deletion of a zero label cannot replace that calculation.

## 6. Executed scope

`verify.py` checks 360 block/partition fixtures of lengths at most four, the displayed five-letter prime-power example, arbitrary-gap formulas for \(0\le r\le15\), both affine inverse compositions, marked forcing transport, and finite-coefficient chain identities. The proofs above cover all nonempty words and nonempty consecutive block partitions. Finite checks are regression evidence for their implementation; they are not independent external review or formal proof-assistant verification.
