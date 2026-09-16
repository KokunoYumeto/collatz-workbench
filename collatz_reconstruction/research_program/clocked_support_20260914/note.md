# Two-clock cohomology, original integral forcing, and a source-complete finite certificate

14 September 2026. Collatz-only continuation of `KokunoYumeto/collatz-workbench`, authenticated source head `6a30f1dc23110fae0abbe3b3bd5e60072a842385`.

The contribution retains the workbench's original two-clock weight, not a new normalization. It gives its marked cyclic complex, exact integral-arithmetic specialization, component cokernel, completion maps, and a clock-preserving lift of the previously constructed descent retractions. A reversible source database closes the previously retained 403-rise sector and gives an all-length 678-rise exclusion. The actual infinite residual source remains.

## 0. Source relationships and notation

**[W]** `research_companion/chapters/01_weighted_path_and_finite_residue_actions.tex`, Git blob `f0142c0d4c237ed068a0762a08c6622df5dbcfee`, in the same authenticated commit. The first-return category, odd-block expansion, two-clock weights, endpoint series, finite-support transfer operator, and completed inverse are already present there. This continuation does not claim those constructions as new. The inspected source passages are lines 1–155 and 260–555.

**[C]** `research_program/cycle_relative_cohomology_20260914/note.md`, the relative actual-orbit complex and exact descent retractions.

**[S]** `research_program/residual_splice_20260914/note.md` and `integral_blocks.md`, the complete first-descent fibers, root splicing, original integral comparison and retained 403-rise sector. The source note has Git blob `b31acf3b485b9565b1bbf878f1e1a98d5e704ad8`.

All paths above are relative to `collatz_reconstruction/`. Original forcing is +1 unless a control is expressly labelled otherwise. Nothing here supplies a morphism from the entire Zeta theta quotient to the entire Collatz orbit complex, or imports an RH conclusion. The finite support/Hurwitz relationship already recorded in the repository remains available. The new arrows below begin with the actual Collatz path operator of [W].

Put
\[
 X=\{1,3,5,\ldots\},\qquad T(n)=\frac{3n+1}{2^{a(n)}},
 \qquad a(n)=\nu_2(3n+1),\qquad R=\mathbb Z[u,v].
\]
The weight of the original edge at n is
\[
 w_n=u v^{a(n)-1}.
 \tag{C1}
\]
For a path of m odd returns and exponent sum A it is exactly \(u^m v^{A-m}\). This is [W]'s convention. The explicit expansion of exponent a into one shortened odd step and a−1 shortened even steps recovers both clocks and has the inverse obtained by grouping at odd returns.

The variable v in R is a clock variable; the symbol \(V_n\) below is an original vertex basis vector. No original integer is rescaled in these definitions.

## 1. The relative complex comes from the original transfer operator

Let E and V be free R-modules on the original nonbase edges \(E_n\) and vertices \(V_n\), respectively, for n in X excluding 1. Define
\[
 d_{u,v} E_n=V_n-w_nV_{T(n)},\qquad V_1=0.
 \tag{C2}
\]
Give E degree zero and V degree one, and write
\[
 \mathcal K^\bullet_{u,v}=[E\xrightarrow{d_{u,v}}V].
\]
At u=v=1, this is precisely [C]'s relative chain complex with degree reindexing \(\mathcal K^i=C_{1-i}\): the map on every original edge and vertex is the identity. Thus H^1 of this reindexed complex is the old H_0, and H^0 is the old H_1. This states the degree correspondence explicitly.

The transfer formula of [W], on finite-support vectors, is
\[
 (Lf)(y)=u\sum_{T(x)=y}v^{a(x)-1}f(x).
\]
Each input basis vector has exactly one image, so \(L V_n=w_nV_{T(n)}\). Identifying \(E_n\) with \(V_n\) gives \(d=I-L\), literally. On the original module including 1, \(R V_1\) is invariant because \(L V_1=uvV_1\). Passing to the specified quotient by this submodule gives (C2). On complexes, only the subcomplex
\[
 [R E_1\xrightarrow{1-uv}R V_1]
\]
is removed. No other source or zero coefficient is used as a reason to remove a basis label.

### Proposition 1. Polynomial injectivity and original path boundaries

The map d in (C2) is injective. For a finite actual path \(n_0\to\cdots\to n_m\), stopping on its first hit of 1, put
\[
 W_0=1,\qquad W_j=\prod_{i<j}w_{n_i},\qquad
 P_p=\sum_{j=0}^{m-1}W_j E_{n_j}.
\]
Then
\[
 dP_p=V_{n_0}-W_mV_{n_m}.
 \tag{C3}
\]

**Proof.** The two terms belonging to each intermediate vertex cancel with their identical original prefix monomial, giving (C3). For injectivity, identify E and V by labels and write \(L=uS\), where \(S V_n=v^{a(n)-1}V_{T(n)}\). In \((I-uS)f=0\), comparison of the constant coefficient in u gives f_0=0; the subsequent coefficients give f_j=Sf_{j-1}=0. A polynomial vector has finitely many coefficients, all zero. This works on the declared finite-support modules, without any convergence assumption. ∎

The original graph's closed-cycle kernel at u=v=1 is therefore not obtained by declaring the generic polynomial kernel to be nonzero. The cycle information is retained in the polynomial cokernel and in its explicitly computed specialization below.

## 2. A faithful marked cyclic complex

Keep a nonempty original labelled exponent word \(p=(a_1,\ldots,a_m)\). Define
\[
 A_j=\sum_{i=1}^j a_i,\quad A_0=0,\quad
 w_i=uv^{a_i-1},\quad W_j=\prod_{i=1}^j w_i,
\]
\[
 W=W_m=u^m v^{A_m-m},\qquad
 N_p(u,v)=\sum_{i=1}^m W_{i-1}.
 \tag{C4}
\]
The position-circle boundary sends edge i to vertex i minus \(w_i\) times vertex i+1, cyclically. Its algebraic dual on the finite free modules is
\[
 (J_ph)_i=h_i-w_i h_{i+1},\qquad h_{m+1}=h_1.
 \tag{C5}
\]
The duality is the original evaluation pairing: \(\langle d e,h\rangle=\langle e,J_ph\rangle\). Neither (C5) nor (C2) is identified with the integer matrix B before the specialization in Section 3.

### Theorem 2. Explicit polynomial comparison, both homotopies, and forcing

The maps
\[
 \phi_0(h)=h_1,\qquad \phi_1(b)=\sum_{i=1}^mW_{i-1}b_i
\]
give a chain map
\[
 [R^m\xrightarrow{J_p}R^m]\longrightarrow[R\xrightarrow{1-W}R].
 \tag{C6}
\]
A section is
\[
 (\psi_0t)_1=t,\qquad (\psi_0t)_i=\left(\prod_{k=i}^m w_k\right)t\ (i\ge2),
 \qquad \psi_1t=(t,0,\ldots,0).
\]
Define
\[
 (Hb)_1=0,\qquad
 (Hb)_i=\sum_{j=i}^m\left(\prod_{k=i}^{j-1}w_k\right)b_j\quad(i\ge2).
 \tag{C7}
\]
They satisfy
\[
 \phi_1J_p=(1-W)\phi_0,\quad J_p\psi_0=\psi_1(1-W),\quad
 \phi_0\psi_0=\phi_1\psi_1=I,
\]
\[
 J_pH=I-\psi_1\phi_1,\qquad HJ_p=I-\psi_0\phi_0.
 \tag{C8}
\]
Consequently the marked cohomology is
\[
 H^0=0,\qquad H^1\cong R/(1-W),\qquad [b]\longmapsto[\phi_1(b)].
 \tag{C9}
\]
For the unit forcing vector its mark is \([N_p]\). The exact inverse of the forced equation is
\[
 (1-W)t=\phi_1(b),\qquad h=\psi_0t+Hb.
 \tag{C10}
\]
All maps and identities are over R, and remain valid after every specified coefficient homomorphism.

**Proof.** Multiplication of (C5) by W_{i−1} telescopes to \((1-W)h_1\), proving the first chain equation. In J_pψ_0, all rows except the first cancel; the first is (1−W)t. The section identities follow from the first coordinate. For i≥2, the tail sum (C7) obeys \((Hb)_i-w_i(Hb)_{i+1}=b_i\), including the final row with \((Hb)_1=0\). The first row is \(-\sum_{i\ge2}W_{i-1}b_i=b_1-\phi_1(b)\). This proves the first homotopy. Applying the same telescope to J_ph in each tail gives \(h_i-(\prod_{k=i}^m w_k)h_1\), proving the second. The scalar 1−W is nonzero in the integral domain R, giving (C9). Formula (C10) follows by applying J_p and φ_0 and then using both homotopies. For m=1 the formulas give H=0 and J_p=(1−w_1); the two cyclic contributions are in the same matrix entry. ∎

For completeness, the position-chain complex, rather than its dual, has an equally explicit comparison with [R→R]. Send vertex 1 to 1, vertex i≥2 to \(Q_i=\prod_{k=i}^m w_k\), edge 1 to 1, and other edges to zero. The scalar sections send 1 to vertex 1 and to \(\sum_iW_{i-1}E_i\). The homotopy sends vertex 1 to zero and vertex i≥2 to its weighted forward tail to vertex 1. Telescoping proves both homotopy identities. These maps connect the two cyclic cokernel descriptions through the same scalar complex; an unexplained equality of a matrix and its transpose is not used.

### Proposition 3. The retained determinant and forcing polynomial recover the word

The pair (W,N_p) determines the entire original labelled word. Its inverse is explicit. Write \(W=u^m v^B\). In N_p the coefficient of u^j is a single monomial \(v^{b_j}\), for 0≤j<m. Put \(b_m=B\). The exact image conditions are
\[
 b_0=0,\qquad 0=b_0\le b_1\le\cdots\le b_m,
\]
with coefficient 1 at each of these m original positions. The inverse is
\[
 a_i=1+b_i-b_{i-1}\quad(1\le i\le m).
 \tag{C11}
\]

**Proof.** By definition \(b_j=A_j-j\), giving every stated condition and (C11). Conversely, (C11) yields positive integers with cumulative exponents j+b_j, whose total weight and forcing polynomial are exactly the supplied pair. Both compositions are identities on the specified image. ∎

The raw polynomial N_p is retained, not only its quotient class. Merely retaining W forgets precisely the original words with the same m,A. For example,
\[
 W_{(1,3)}=W_{(2,2)}=u^2v^2,
\qquad N_{(1,3)}=1+u,\quad N_{(2,2)}=1+uv.
 \tag{C12}
\]
Thus the determinant alone has a nontrivial word fiber, and (C11) supplies the actual repair. This faithful marker uses the original weights of [W]; no priority claim is made for polynomial encoding of finite words.

## 3. The original integral cycle obstruction is an exact specialization

For the same word retain
\[
 L=3^m,\quad U=2^{A_m},\quad D=U-L,\qquad
 C=\sum_{i=1}^m3^{m-i}2^{A_{i-1}},
\]
\[
 (B_px)_i=2^{a_i}x_{i+1}-3x_i.
 \tag{C13}
\]
Let \(\Lambda=\mathbb Z[1/3]\). The specified coefficient homomorphism is
\[
 \alpha:R\longrightarrow\Lambda,\qquad u\longmapsto2/3,\quad v\longmapsto2.
 \tag{C14}
\]
It sends \(w_i\) to \(2^{a_i}/3\). Directly, including all original signs and factors,
\[
 \alpha(J_p)=-B_p/3,\qquad
 \alpha(1-W)=-D/3^m,\qquad
 \alpha(N_p)=C/3^{m-1}.
 \tag{C15}
\]
Thus the original forced system B_px=b becomes \(\alpha(J_p)x=-b/3\); its scalar forcing mark in (C6) becomes
\[
 \alpha(\phi_1)(-b/3)=-F_p(b)/3^m,
 \quad F_p(b)=\sum_{i=1}^m3^{m-i}2^{A_{i-1}}b_i.
 \tag{C16}
\]
Multiplication by the specified unit \(-3^m\) identifies the scalar equation with
\[
 D t=F_p(b).
 \tag{C17}
\]
The degree-zero map from the localized original complex to the evaluated position complex is the identity, and its degree-one map is multiplication by −1/3. Its inverse is the identity in degree zero and multiplication by −3 in degree one. This is the chain isomorphism responsible for (C15)–(C17).

### Proposition 4. Localization at 3 retains the original integral forcing class

For original integral b, solvability of B_px=b in \(\Lambda^m\) is equivalent to solvability in \(\mathbb Z^m\). The map on original cokernels is the explicit isomorphism
\[
 \mathbb Z/D\mathbb Z\longrightarrow\Lambda/D\Lambda.
 \tag{C18}
\]
It preserves the distinguished original class \([F_p(b)]\), in particular [C] for b=1. It also retains the reduced denominator of the unique rational primitive.

**Proof.** The integer D is odd and coprime to 3, since U is a power of 2 and L a power of 3. The telescoping row F_p satisfies \(F_pB_p=D e_1^T\), is primitive (its endpoint coefficients are coprime powers of 3 and 2), and both cokernels have determinant order |D| before localization. Its explicit integral identification is [C]'s calculation and [S]'s integral block comparison. For (C18), the inverse sends \(a/3^r\) to \(a(3^r)^{-1}\bmod D\). Independence of the chosen fraction and both inverse identities follow by multiplication by powers of 3, invertible modulo D.

An integral b with a localized preimage has 3^r b in B_p Z^m for some r. Its original cokernel class is killed by 3^r, hence is zero in Z/D by coprimality. An integral preimage therefore exists and equals the localized one, since B_p is injective. Equivalently its unique rational coordinates are integer adjugate numerators divided by D, and localization at 3 cannot remove a denominator coprime to 3. ∎

The coefficient embedding Z→Λ is not replaced by an identity on lattices. Its extra degreewise quotient is the 3-primary group \((\Lambda/\mathbb Z)^m\). On this group B_p is an automorphism: its adjugate multiplied by the inverse of D is an explicit inverse, because D acts invertibly on 3-primary torsion. Hence that quotient complex is acyclic. This accounts for the extra localized elements through their actual quotient and maps.

The original positive cycle criterion remains D>0 and D|C; the full original coordinates and actual valuations are reconstructed as in [C,S]. The ring change alone does not assert positivity or the existence of an integer cycle. The word (1,3) has (D,C)=(7,5), whereas (2,2) has (7,7). Their identical clock determinants in (C12) give different original forcing classes through (C16). The second word maps to the actual fixed vertex 1 and is removed only by the declared relative graph quotient.

The prime-power control (1,1,2,4,3) retains D=1805 and C=475. Its scalar equation has 19 solutions modulo 19 and none modulo 361, because gcd(1805,19)=19 divides 475 while gcd(1805,361)=361 does not. Formula (C18) and [S]'s integral inverse preserve that obstruction; no passage to rational coefficients substitutes for this test.

## 4. What the clocked cokernel records for actual components

Let \(\mathscr C\) be the set of actual nonbase periodic components, each equipped with one chosen point on its primitive cycle. Let \(\mathscr A\) be the set of actual nonperiodic components, each equipped with a chosen original forward ray \(x_0,x_1,\ldots\). These are sets defined by the actual map, not assertions that either kind of nonbase component exists.

For a primitive cycle c let m_c,A_c be its actual clocks and \(W_c=u^{m_c}v^{A_c-m_c}\). For a chosen nonperiodic ray let
\[
 B_j=\sum_{i<j}(a(x_i)-1),\qquad W_j=u^jv^{B_j},
\qquad M_x=\bigcup_{j\ge0}W_j^{-1}R
 \subset\mathbb Z[u^{\pm1},v^{\pm1}].
 \tag{C19}
\]
The union is increasing because W_j divides W_{j+1}. Each element remains a finite Laurent polynomial; the union is not silently replaced by a completion.

### Theorem 5. Component classification with explicit maps

The cohomology of the actual relative complex is
\[
 H^0(\mathcal K)=0,\qquad
 H^1(\mathcal K)\cong
 \bigoplus_{c\in\mathscr C} R/(1-W_c)
 \ \oplus\ \bigoplus_{x\in\mathscr A}M_x.
 \tag{C20}
\]
The original base component contributes zero. Every cycle summand has its displayed annihilator ideal (1−W_c); every nonperiodic summand is a nonzero torsion-free R-module inside the stated Laurent domain.

**Proof.** Finite-support modules decompose by actual components, and d respects this decomposition. Proposition 1 gives H^0=0.

On the component reaching 1, the actual finite path from n to 1 has boundary V_n by (C3), so every generator of the cokernel vanishes. Equivalently, before taking the relative quotient, this component has exactly R/(1−uv), and the subcomplex at 1 maps onto that summand by its original generator. Taking the relative quotient removes precisely it.

For a periodic component, use the weighted finite path from every vertex to the chosen cycle point to express its class as a monomial times that point's class. One traversal of the primitive cycle gives exactly the relation (1−W_c)V=0. Send each vertex to the weight of its first path to the chosen point, reduced modulo (1−W_c). Every edge relation maps to zero; at the chosen point it is precisely 1−W_c. The reverse map sends 1 to the chosen vertex. The path relations and the primitive return prove both inverse identities. This gives the displayed quotient, whose annihilator is its defining principal ideal.

For a nonperiodic component, every vertex eventually meets the chosen ray. To see this, adjacent vertices have forward orbits that meet, and this property is transitive along each finite undirected path. For T^d(n)=x_j, send
\[
 [V_n]\longmapsto\frac{\prod_{i<d}w_{T^i(n)}}{W_j}\in M_x.
 \tag{C21}
\]
Changing the meeting point to a later point multiplies numerator and denominator by the same actual path weight. Nonperiodicity ensures that two meeting descriptions align in this way, so the map is well defined. It respects the edge relation by the first weight factor. Conversely send f/W_j to f[V_{x_j}]. Equality of two fractions can be tested at a common later denominator W_k, and the original ray path relations make their images equal. These are inverse maps on generators, and therefore on all finite sums. The target is a nonzero submodule of a domain, proving torsion-freeness. ∎

This classification does not decide the actual component of a source whose behavior has not been determined. It specifies exactly what a component would contribute through the displayed maps, with no deletion from a reference-measure statement.

### Repetitions and the actual orbit map

For a solved positive integral word, the position vertex i maps to V_{x_i} and edge i maps to E_{x_i}. The original equations prove that the exponent weight is the actual w_{x_i}, so this is a chain map for (C2). Its degreewise kernel consists exactly of coefficient vectors whose sums over each repeated original vertex/edge label vanish. The full coordinate dictionary is retained.

For r repetitions of a primitive cycle of weight W_c, the source cokernel maps by
\[
 R/(1-W_c^r)\longrightarrow R/(1-W_c),\qquad[f]\longmapsto[f].
 \tag{C22}
\]
Its kernel is \((1-W_c)/(1-W_c^r)\). The weighted fundamental path maps to
\[
 (1+W_c+\cdots+W_c^{r-1})P_c.
\]
At u=v=1 this gives exactly r times the original cycle chain, not one traversal. Repetitions of (2) map entirely to the removed base vertex and loop.

### Recovery of the old cycle kernel

The coefficient homomorphism u→t,v→1 has kernel (v−1) and sends (C20)'s cycle summand to Z[t]/(1−t^{m_c}), and its ray summand to Z[t,t^{-1}]. On a ray this follows directly by specializing the explicit increasing union: the denominator W_j becomes t^j. The kernel of the map on that union is (v−1)M_x, as follows by writing an element at one denominator and dividing its polynomial numerator by v−1.

Now use the exact sequence of complexes given by multiplication by t−1 and evaluation t=1. Its connecting map is explicit. For an ordinary primitive cycle chain \(\sum_i E_i\), lift it to \(\sum_i t^{i-1}E_i\); its differential is
\[
 (1-t^m)V_1=-(t-1)(1+t+\cdots+t^{m-1})V_1.
\]
Thus the connecting class is \(-[1+t+\cdots+t^{m-1}]\), the generator of the (t−1)-torsion subgroup in Z[t]/(1−t^m). The Laurent ray module has no such torsion. Quotienting either component module by t−1 gives Z. This recovers exactly [C]'s ordinary cycle kernel and the degree-zero component obstruction, with their signs and degree correspondence accounted for.

## 5. Two completion maps and the support they retain

Let \(E_0=\mathbb Z[v]^{(X\setminus\{1\})}\) and \(\widehat R=\mathbb Z[v][[u]]\). There is an explicit injective map
\[
 \iota:\widehat R^{(X\setminus\{1\})}\longrightarrow E_0[[u]],
 \quad (f_n(u,v))_n\longmapsto\sum_{j\ge0}\left(\sum_n[u^j]f_n\,V_n\right)u^j.
 \tag{C23}
\]
Its image is exactly the series with one common finite vertex-support set for all u coefficients. The target permits the finite vertex support to depend on the coefficient index. The quotient is precisely the latter series modulo the common-finite-support series. These formulas specify the relation between the two constructions, rather than merely giving them different names.

On E_0[[u]],
\[
 (I-uS)^{-1}=\sum_{j\ge0}u^jS^j
 \tag{C24}
\]
is defined coefficientwise. Each coefficient is a finite original vertex sum. This is the forward-column form of [W]'s completed transfer inverse, specialized to the relative source; [W] already contains the existence of the completed inverse.

### Theorem 6. Exact source-support test for the inverse column

For an original source n, the unique completed inverse column is
\[
 G_n=\sum_{j\ge0}u^jv^{A_j(n)-j}V_{T^j(n)},\qquad V_1=0.
 \tag{C25}
\]
The formula stops contributing after the first hit of 1. Its membership has the following complete description:

* On an orbit reaching 1, G_n is a polynomial vector, with u-degree exactly its positive number of odd returns to 1 minus one (and the zero column for n=1).
* On an orbit eventually entering a nonbase cycle, G_n lies in the image of (C23) and is not a polynomial in u. Its actual tail is a finite weighted cycle numerator divided by 1−W_c, with its original entry prefix retained.
* On a nonperiodic orbit, G_n is outside the image of (C23): its nonzero coefficients have infinitely many distinct original vertex labels.

Consequently
\[
 [V_n]=0\text{ in }H^1(\mathcal K_{u,v})
 \quad\Longleftrightarrow\quad
 G_n\text{ is a polynomial vector}
 \quad\Longleftrightarrow\quad n\text{ reaches }1.
 \tag{C26}
\]

**Proof.** Coefficient comparison in (I−uS)G_n=V_n uniquely gives the displayed successive terms, retaining both clocks and the actual label. Arrival at 1 makes all subsequent relative terms zero. A repeated nonbase vertex makes the deterministic orbit periodic from its first repetition; the finite prefix and geometric cycle tail give the stated rational expression. Without any repeated vertex, the support is unbounded in vertex labels. Conversely, finitely many encountered vertex labels force a repetition or a base hit. These statements prove every support characterization and (C26), since Proposition 1 makes a polynomial preimage unique and its inclusion in the completion must equal G_n. ∎

The scalar extension from R to \(\widehat R\) does not by itself produce (C24) on the common-finite-support module: on a ray its cokernel is the nonzero increasing union \(\bigcup_j W_j^{-1}\widehat R\), with the same fraction maps as (C21). For a finite cycle, 1−W_c is a unit in \(\widehat R\), so that cycle summand becomes zero. Passing further through (C23) makes the ray column available and the entire completed complex acyclic. This computes what each map removes.

Also, evaluation u=1 on polynomials does not extend to a unital homomorphism \(\mathbb Z[v][[u]]\to\mathbb Z[v]\) fixing v: 1−u is a unit in the source and would map to zero. The exact inclusion of polynomials and this unit obstruction explain why an available formal inverse is not automatically a finite-support contraction at the original parameter value.

The global Collatz target is therefore the source-dependent polynomial membership in (C26) for every n. No uniform degree bound over all positive integers is required or asserted. A completed inverse already exists without that membership; its existence is not the missing proof.

## 6. Retraction and root splicing retain the original clocks

Let h,Q,F be one of [C,S]'s actual path retractions. Retain the original path from n to its chosen root r(n), its length \(\ell_n\), and its full exponent word. Let P_n be its chain (C3) and M_n its terminal monomial. Define
\[
 h_w(V_n)=P_n,\qquad Q_w(V_n)=M_nV_{r(n)},\qquad
 F_w=I-h_wd.
 \tag{C27}
\]
Root paths have length zero, and the relative base vertex is zero. These are maps on the original finite-support polynomial modules. The predecessor's positive edge multiplicities and the original starting point reconstruct the path's chronological order: iterate its deterministic successor for the sum of the multiplicities, then verify both the endpoint and the complete edge-count dictionary. The code does exactly that rather than inventing an ordering of a sparse vector.

### Theorem 7. Clocked homotopy and extension identities

The maps satisfy
\[
 dh_w=I-Q_w,\qquad h_wQ_w=0,\qquad Q_w^2=Q_w,
\]
\[
 F_w^2=F_w,\qquad dF_w=Q_wd.
 \tag{C28}
\]
For an extension attached at old roots as in [S], let \(\Gamma_r\) be its full weighted path from an old root to a final old root, including each old endpoint path. Define
\[
 K_w(V_n)=M_n\Gamma_{r(n)},\qquad h'_w=h_w+K_w.
 \tag{C29}
\]
Then
\[
 dK_w=Q_w-Q'_w,\quad F_wK_w=K_w,
 \quad Q'_wQ_w=Q_wQ'_w=Q'_w,
 \quad F'_wF_w=F_wF'_w=F'_w.
 \tag{C30}
\]
At u=v=1 these are exactly the old retraction and root-splice maps.

**Proof.** Equation (C3) proves the first equation of (C28). The maps h vanish at their roots, and their root monomials are 1, proving the other vertex identities. Then \(h_wdh_w=h_w(I-Q_w)=h_w\), yielding edge idempotence and the chain equation. In a concatenation, the second path chain is multiplied by the first path's terminal monomial. Thus (C29) is the actual added chain and telescopes to dK_w=Q_w−Q'_w. Final roots are old roots with no added path, so K_wQ_w=K_w, K_wQ'_w=0 and h_wQ'_w=0. In particular h_wdK_w=0 and hence F_wK_w=K_w. The remaining equations follow by multiplying I−h_wd and I−(h_w+K_w)d and applying those identities. The evaluation homomorphism u=v=1 sends every prefix monomial to 1, recovering the original chains coefficient for coefficient. ∎

For a genuine weighted cycle path P_c based at n,
\[
 F_wP_c=P_c-(1-W_c)h_w(V_n).
 \tag{C31}
\]
This is the exact relation before specialization. At u=v=1, it becomes literal equality with the old closed cycle chain. One must not assert that a generic weighted cycle path has zero boundary: its boundary is exactly (1−W_c)V_n.

### An actual omitted-clock defect and its repair

Use the old one-edge descent 5→1, with exponent 4. At the old root 7 the new original block is
\[
 7\xrightarrow{1}11\xrightarrow{1}17\xrightarrow{2}13\xrightarrow{3}5.
\]
It has terminal monomial \(u^4v^3\). The correct new column is
\[
 P_{7\to5}+u^4v^3 E_5.
\]
Its boundary is V_7. Appending E_5 without that monomial produces instead
\[
 V_7+(1-u^4v^3)V_5.
 \tag{C32}
\]
The verifier computes this residual literally, then checks the corrected path and both compositions in (C30). This is a concrete example in which retaining a clock is required for the equation to hold.

## 7. A reversible source database closes the 403-rise sector

The previous retained sector was m=971,A=1539 with 403 exponent-1 positions and possible minimum in [99781,330749]. The new certificate retains every positive odd source 3≤n≤330749, its exact first-descent word, the full affine cylinder and target progression, and its source parameter.

The database uses a finite ordered word dictionary and one dictionary ID for each source row. The source for row i is n=3+2i. For its exact word p, the original cell is
\[
 n=r+2Ut,\qquad T^m(n)=q+2Lt,
\]
with all of r,U,q,L,C,D and the first-descent interval retained. Its decoder returns
\[
 n=3+2i,\quad p=\text{dictionary}[\text{id}_i],\quad
 t=(n-r)/(2U),\quad y=q+2Lt.
 \tag{C33}
\]
The inverse encoder looks up that exact word and checks the same original n,t,y. This is an inverse on the specified valid source records; it is not an assertion that a count or hash recovers a word. Gzip is only a byte container: decompression is verified to recover the exact canonical JSON.

The declared labels (1) and (2,2) remain present with empty first-descent fibers and zero source counts. They are not removed from the dictionary. Counts may be placed in \(G(\mathbb Z)=\mathbb Z\sqcup\{\tau\}\) by assigning an integer to each declared label and τ to an undeclared label. The reflection fixes each integer and maps τ to 0. Its zero fiber is exactly {τ,0}; the separate declaration mask distinguishes them. The full word, cell and original source maps are retained in addition to this mask, so neither an integral forcing class nor a vanished coefficient is inferred from the support label alone.

### Theorem 8. Executed source-complete finite polynomial contraction

The delivered database and independent integer replay establish that every positive odd n≤330749 reaches 1. They also construct a closed actual witnessed graph with 262615 nonbase vertices, on which the original unit edge cochain has an explicitly reconstructed nonnegative integral primitive of maximum 164. On that witnessed graph, the clocked operator satisfies
\[
 S^{164}=0,\qquad
 (I-uS)^{-1}=\sum_{j=0}^{163}u^jS^j.
 \tag{C34}
\]
Here \(S V_n=v^{a(n)-1}V_{T(n)}\), with V_1=0, so every coefficient and original edge remains in (C34).

**Proof and executable certificate.** `sector_certificate.py` generates the actual first-descent word for each of the 165374 source rows, retaining any failure rather than accepting it. The saved database has 13989 occupied word cells and the two present zero cells. `independently_verify` replays the original +1 operation using repeated integer division, separately from the generator's valuation implementation. It checks every exponent, absence of an earlier descent, the original affine source/target parameter inverses, every complete cell's count on the interval, and the coverage of every original source row. There are 575110 replayed original return equations. Every target is a strictly smaller positive odd integer, so strong induction beginning at 1 supplies convergence for each seed.

More explicitly, assign height 0 to 1 and work through the source rows in increasing order. For a first-descent path ending at y<n, height(y) is already defined. Assign the intermediate vertices the remaining path length plus height(y); all overlaps must agree and are checked. The resulting original edge table is closed under the actual map except for the explicitly included basepoint, and height(n)−height(T(n))=1 is verified on all 262615 nonbase vertices. Its maximum is 164; its largest original vertex is 8216025965. Hence every sequence of 164 original edges reaches the relative zero vertex. This proves the first identity in (C34) on every basis column. Multiplication of the finite geometric sum proves both inverse identities. The bound concerns this finite witnessed graph, not all original positive integers. ∎

The new source interval includes 115485 additional odd seeds above the prior bound 99779. It closes the entire old 403-rise sector without enumerating its gap tuples: the possible minimum of each tuple is an actual source in the certified interval, and therefore cannot lie on a nonbase cycle.

### Theorem 9. All-length exclusion through 678 exponent-1 positions

No nontrivial positive integer cycle has at most 678 exponent-1 positions in its primitive odd-return word.

**Proof.** Theorem 8 gives the minimum lower bound s=330751. For an actual positive cycle,
\[
 3^m<2^A=\prod_i(3+1/x_i)\le(3s+1)^m/s^m.
\]
With k exponent-1 positions, the unchanged identity \(A=2m-k+\sum_{a_i\ge3}(a_i-2)\) implies
\[
 (4s)^m\le2^k(3s+1)^m.
 \tag{C35}
\]
The certificate computes the least power of 2 strictly above 3^m by repeated doubling and verifies
\[
 2^{\lceil\log_2(3^m)\rceil}s^m>(3s+1)^m
 \quad(1\le m\le1635).
 \tag{C36}
\]
The logarithm is notation for that exact least-power integer; no floating-point logarithm is used. It also verifies
\[
 (4s)^{1634}>2^{678}(3s+1)^{1634}.
 \tag{C37}
\]
Because 4s>3s+1, (C37) persists at every larger length and for all k≤678. Thus (C35) forces m≤1633, while (C36) excludes every such length. All finite comparisons and every source premise are regenerated by the delivered checker. ∎

This is an internal, self-contained workbench bound, not a claim to exceed published Collatz cycle bounds. In particular k counts exponent-1 positions, not the local-minimum count used in other cycle nomenclature. The original clock map in [S] still gives local-minimum count m−k in a nontrivial shortened cycle.

The next retained sector with k=679 is forced to
\[
 m=1636,\quad A=2593,\quad
 330751\le\min x_i\le583287.
 \tag{C38}
\]
The checker verifies the two adjacent minimum-endpoint inequalities, excludes the next power of 2 at that period, and excludes larger lengths for k=679 by (C35). Then \(\sum_{a_i\ge3}(a_i-2)=0\): the word contains 679 ones and 957 twos. Cutting at the ones retains gap lengths \(r_i\ge0\), \(\sum r_i=957\), the original rotation offset, and [S]'s anchored equations
\[
 2\cdot4^{r_i}y_{i+1}-3^{r_i+1}y_i=2\cdot3^{r_i},\qquad y_i=x_i-1.
 \tag{C39}
\]
The complete integral inverse in [S] and the marked clock specialization in Section 3 both remain attached. Neither a solution nor an exclusion of this entire next sector is asserted.

## 8. What is new here, what is retained, and the outstanding task

The existing weighted sums, path category, ordinary graph homology, affine packet identities and completed inverse are sourced, not rediscovered under new names. The continuation adds the explicit marked cyclic R-comparison and its original integral specialization; the component cokernel and scalar-versus-support completion maps; the clocked residual retraction and omitted-clock residual (C32); and the reversible finite certificate establishing (C34)–(C37).

The original word is recoverable from (W,N_p), the original integral forcing is recoverable through (C14)–(C18), and actual component behavior is attached through original integer vertices. The available formal inverse is kept in its actual completion. This identifies the productive role of retained data without a priority claim about an undefined acronym or a claim that no other method can prove these results.

The global remaining task is polynomial membership of G_n for each original positive source, or an actual nonzero original source class with a certified orbit obstruction. Merely constructing G_n in the completion has already been done and does not settle that membership. The next finite sector is (C38)–(C39); the old infinite nonperiodic and first-crossing exception sources are unchanged. Zero reference mass never removes one of those vertices.

This session used authenticated GitHub reads and the uploaded source archive. The accessible GitHub tool surface exposed read operations only; no write operation or CLI connection was available. Consequently this continuation is supplied as an additive patch against the authenticated head, not described as a pushed commit, PR update, or successful new GitHub CI run. The original eight replays and the new ordinary/optimized pair were executed locally; their receipts distinguish that from the earlier remote CI.

## 9. Verification controls

The symbolic suite checks 364 full-word fixtures: every word of lengths 1 through 5 with letters 1 through 3, and the original five-letter prime-power fixture. Each homotopy is checked as a polynomial matrix identity on its basis columns; the arithmetic evaluation is checked against the unchanged original B matrix. The source database is independently replayed and every saved cell is compared with the untouched predecessor constructor. The suite has 33503 named algebraic/source checks in addition to its separately counted 575110 original return equations; the counts are not advertised as independent mathematical reviews.

The periodic positive control is T_−(n)=(3n−1)/2^{ν₂(3n−1)}, with the genuine orbit 5→7→5 and weight u²v. Its exact relation to the signed original map is T_−(n)=−T_+(−n), using ν₂(−q)=ν₂(q). It is not a positive +1 Collatz counterexample. Its r-fold weighted path is checked against (1+u²v+⋯+(u²v)^{r−1}) times the primitive path, for r≤16.

The ray control is expressly the synthetic map n→n+2, assigned the test weight uv. Its length-j boundary is V_3−u^jv^jV_{3+2j}, with j distinct original test labels. This checks the support-completion mechanism; it is never assigned to an unverified +1 orbit. Twelve malformed inputs are rejected, including an erased forcing coefficient, a removed original source row, a changed forcing sign, and erased supported-zero labels.
