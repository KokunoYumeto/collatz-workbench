# Collatz cycles, relative cohomology, and counterexample-preserving descent compression

**Date:** 14 September 2026  
**Target:** `KokunoYumeto/collatz-workbench`  
**Status:** proofs and exact local replay; no external mathematical review, Lean certification, or remote publication claimed.

## 0. Source, question, and contribution

The preceding contribution is retained byte-for-byte at `../stopped_affine_transport_20260914/`. Its exact chart sends a legal word cylinder to its actual affine image, and its finite source-incidence construction records the image lattice. This continuation adds the return-to-source condition, its integral obstruction, the actual orbit graph relative to the fixed point 1, and explicit chain-homotopy compression by certified descent paths.

The central constructive result is Section 6: every checked collection of actual strict-descent paths gives a chain retraction with a displayed homotopy, and **every closed cycle chain is fixed literally by that retraction**. Unlisted vertices remain separate roots. This is the precise mechanism by which the preceding descent work can be used without deleting a possible counterexample.

The relevant cycle information is not a bare Betti number or an unmarked torsion group. A proposed word retains its forcing class, rational primitive, integral/positive membership, actual valuation word, primitive period with its reconstruction map, and its induced map into the relative orbit graph.

Rational cycle formulas have established precedents, notably Lagarias [R1]. Operator formulations of Collatz also have an existing literature, for example Mori [R2]. No priority claim is made for those underlying ideas. All specific algebraic and graph statements used below are proved here. The predecessor's probability estimates are not used to decide whether an individual integer is a counterexample.

Current GitHub files were not readable through an authenticated connection in this session. Consequently no current remote base commit, methodology inspection, PR status, or remote integration is asserted. The source actually used is the attached predecessor archive, whose manifest and executable results were replayed locally.

---

## 1. Original affine word and the closed-cycle obstruction

Write

\[
 T(n)=\frac{3n+1}{2^{\nu_2(3n+1)}}\qquad(n\in X:=\{1,3,5,\ldots\}).
\]

For a nonempty word \(p=(a_1,\ldots,a_m)\), retain

\[
 A_i=\sum_{j=1}^i a_j,\quad A_0=0,\quad
 U=2^{A_m},\quad L=3^m,\quad D=U-L,
\]
\[
 C=\sum_{i=1}^m3^{m-i}2^{A_{i-1}},\qquad
 F_p(x)=\frac{Lx+C}{U}.
 \tag{1.1}
\]

Every exponent is a positive integer. Thus \(D\ne0\) and \(\gcd(D,6)=1\). No denominator or affine term is removed.

Define the two-term cochain complex, in degrees 0 and 1,

\[
 K_p=[\mathbb Z^m\xrightarrow{B_p}\mathbb Z^m],\qquad
 (B_px)_i=2^{a_i}x_{i+1}-3x_i,\quad x_{m+1}=x_1.
 \tag{1.2}
\]

For \(m=1\), the single matrix entry is \(2^{a_1}-3\), with both contributions added in the same entry.

### Theorem 1.1. Integral forcing class and rational primitive

Put

\[
 \mathcal F_p(y)=\sum_{i=1}^m3^{m-i}2^{A_{i-1}}y_i.
\]

Then

\[
 \mathcal F_pB_p=D\,e_1^t,\qquad
 \det B_p=(-1)^{m-1}D,
 \tag{1.3}
\]
\[
 H^0(K_p)=0,\qquad H^1(K_p)\xrightarrow[\mathcal F_p]{\ \simeq\ }\mathbb Z/D\mathbb Z,
 \qquad[\mathbf1]\longmapsto[C].
 \tag{1.4}
\]

The unique rational solution of \(B_px=\mathbf1\) has coordinates

\[
 x_i=\frac{C(p_i)}D,
 \tag{1.5}
\]

where \(p_i\) starts at \(a_i\) and follows the original cyclic order. Its common reduced denominator is

\[
 q(p)=\frac{|D|}{\gcd(|D|,C)}=\operatorname{ord}([C]).
 \tag{1.6}
\]

**Proof.** In \(\mathcal F_p(B_px)\), each intermediate \(x_i\) cancels against the preceding row. The two remaining terms are \(Ux_1-Lx_1\). For \(m\ge2\), the determinant has the diagonal product and the cyclic permutation product only; their signed sum is \((-1)^{m-1}(U-L)\). The case \(m=1\) is direct.

The first and last coefficients of \(\mathcal F_p\) are \(3^{m-1}\) and \(2^{A_{m-1}}\); they are coprime. For \(m=1\), the sole coefficient is 1. Therefore \(\mathcal F_p\) is onto \(\mathbb Z\). Equation (1.3) induces an onto map from the cokernel to \(\mathbb Z/D\mathbb Z\). Both groups have order \(|D|\), proving (1.4). This also proves \(H^0=0\).

Solving the affine fixed-point equation gives \(x_1=C/D\). Applying the same telescoping calculation after cyclic relabelling gives (1.5). The exact transport is

\[
 2^{a_i}C(p_{i+1})=3C(p_i)+D.
 \tag{1.7}
\]

Both 2 and 3 are units modulo every divisor of \(D\). Hence the gcd with \(D\) is unchanged by cyclic transport, proving (1.6). ∎

### Explicit integral chain equivalence

Choose an integer column \(u\) with \(\mathcal F_pu=1\), using Bezout on the two endpoint coefficients. Define

\[
 f^0=e_1^t,\quad f^1=\mathcal F_p,\qquad
 s^0=D B_p^{-1}u,\quad s^1=u,
\]
\[
 h=B_p^{-1}(I-u\mathcal F_p).
 \tag{1.8}
\]

These give maps between \(K_p\) and \([\mathbb Z\xrightarrow D\mathbb Z]\). They are integral: the cokernel calculation shows that \(Du\) and every column of \(I-u\mathcal F_p\) lie in the image of \(B_p\). Their identities are

\[
 fs=I,\qquad B_ph=I-u\mathcal F_p,\qquad
 hB_p=I-s^0e_1^t.
 \tag{1.9}
\]

Thus the original cycle equations have a specified chain equivalence, not just an abstract cokernel identification. The checker independently constructs (1.8) by rational Gaussian elimination and verifies the integrality and both homotopy identities.

### Integral extension with its distinguished maps

The original matrix

\[
 \begin{pmatrix}L&C\\0&U\end{pmatrix}
\]

defines an extension of \(\mathbb Z[t]\)-modules with end actions \(L\) and \(U\). The resolution by multiplication by \(t-U\) gives

\[
 \operatorname{Ext}^1_{\mathbb Z[t]}(\mathbb Z_U,\mathbb Z_L)
 \simeq \mathbb Z/D\mathbb Z.
\]

Changing the lift of the quotient generator by \(n\) times the submodule generator changes the original defect to \(C-Dn\). Its extension class is therefore the same marked residue as in (1.4). The rational section is \(n=C/D\). The coefficient embedding into \(\mathbb Q\) and this section are explicit; they do not replace the original integral extension.

### Exact coefficient tests

For every positive modulus \(N\), the equation \(B_px=\mathbf1\pmod N\) has

\[
 \begin{cases}
 \gcd(D,N) &\text{when }\gcd(D,N)\mid C,\\
 0&\text{otherwise}
 \end{cases}
 \tag{1.10}
\]

solutions. Tensor the integral chain equivalence (1.8) with \(\mathbb Z/N\mathbb Z\): it leaves the single congruence \(Dz=C\), which has exactly the stated number of solutions. In particular, all prime powers, not only the radical of \(D\), participate.

For \(p=(1,1,2,4,3)\),

\[
 D=1805=5\cdot19^2,\quad C=475=5^2\cdot19,\quad q=19.
\]

The rational orbit is \((5,17,35,31,7)/19\). There are 19 solutions modulo 19 and none modulo 361. The lift residual at \((0,10,6,0,6)\) is \((1,-1,-1,5,-1)\), and its pairing with \(\mathcal F_p\) is \(-25\not\equiv0\pmod{19}\).

---

## 2. The return obstruction comes from the preceding image chart

The predecessor's exact legal cylinder is

\[
 n(v)=r+2Uv,\qquad 1\le r<2U,\qquad
 r\equiv(U-C)L^{-1}\pmod{2U}.
\]

Its actual image, with the same parameter, is

\[
 y(v)=u+2Lv,\qquad u=(Lr+C)/U.
 \tag{2.1}
\]

The positive source is \(v\ge0\). Both \(r\) and \(u\) are odd. Put

\[
 z_0=(r-1)/2,\quad z_1=(u-1)/2,\quad k=z_1-z_0=(u-r)/2.
\]

The coordinate map is explicitly \(x\mapsto(x-1)/2\) on odd integers, with inverse \(z\mapsto2z+1\). In these coordinates the joint source/image point is

\[
 (z_0+Uv,z_1+Lv).
 \tag{2.2}
\]

### Theorem 2.1. Joint lattice and its image/return morphisms

Retain the parallel lattice complex

\[
 P_p=[\mathbb Z\xrightarrow{v\mapsto(Uv,Lv)}\mathbb Z^2].
\]

It has the following integral chain maps, all with degree-zero map the identity:

\[
 P_p\longrightarrow[\mathbb Z\xrightarrow U\mathbb Z],\quad (s,t)\mapsto s,
\]
\[
 P_p\longrightarrow I_p:=[\mathbb Z\xrightarrow L\mathbb Z],\quad(s,t)\mapsto t,
\]
\[
 P_p\longrightarrow R_p:=[\mathbb Z\xrightarrow D\mathbb Z],\quad(s,t)\mapsto s-t.
 \tag{2.3}
\]

The first is the original source lattice, the second is the predecessor's image complex, and the third carries the return equation

\[
 n(v)=y(v)\quad\Longleftrightarrow\quad Dv=k.
 \tag{2.4}
\]

The original forcing and return marks obey

\[
 C=Dr+2Uk,\qquad [C]=2U[k]\text{ in }\mathbb Z/D\mathbb Z.
 \tag{2.5}
\]

Multiplication by \(2U\) is an automorphism of that quotient. The two integral solvability tests therefore agree by a specified map. Their rational primitives satisfy

\[
 r+2U(k/D)=C/D.
 \tag{2.6}
\]

**Proof.** Each map in (2.3) sends the differential \((U,L)\) to the stated target differential. Subtracting the two original formulas (2.1) gives
\((n-y)/2=Dv-k\). Rearranging \(Uu=Lr+C\) gives (2.5). Since \(D\) is odd and coprime to \(U\), the asserted unit property follows. Equation (2.6) is (2.5) divided by \(D\). ∎

For clarity, the image torsion \(\mathbb Z/L\mathbb Z\) and return torsion \(\mathbb Z/D\mathbb Z\) both arise from the same retained parallel lattice. Its cokernel is \(\mathbb Z\), via the primitive row

\[
 \lambda(s,t)=Ls-Ut.
\]

On cokernels, the image map is multiplication by \(-U^{-1}\pmod L\), and the return map is multiplication by \(L^{-1}\pmod D\), because

\[
 \lambda(s,t)\equiv-Ut\pmod L,
 \qquad \lambda(s,t)\equiv L(s-t)\pmod D.
 \tag{2.7}
\]

These are the exact comparison maps; the lattice moduli are not equated.

### Actual source incidence remains attached

For any finite set of original parameters \(v_i\), keep the source basis \(e_i\) and define

\[
 E_p=[\mathbb Z^s\longrightarrow\mathbb Z^3],\qquad
 e_i\longmapsto(1,z_0+Uv_i,z_1+Lv_i).
 \tag{2.8}
\]

Projection to coordinates \((1,z_1+Lv_i)\) is the preceding affine incidence map. Projection to the first coordinate is support incidence. There is also the chain map

\[
 E_p\longrightarrow P_p,\qquad e_i\mapsto v_i,
\quad (a,s,t)\mapsto(s-z_0a,t-z_1a).
 \tag{2.9}
\]

The chain equation is \((Uv_i,Lv_i)=(Uv_i,Lv_i)\). Thus the new return detector is attached to the same actual source columns, rather than inferred from spectral similarity.

All maps exist for empty and singleton source sets as well. No occupied-fiber rank or torsion conclusion is imposed on those cases. A solution of (2.4) belongs to a finite supplied interval only when its exact parameter lies in that interval; this mask is retained separately.

---

## 3. Trivial orbit, nontrivial orbit, and the marked primitive

### Theorem 3.1. Positive integer cycles and the anchor at 1

The original word has a positive integer closed orbit exactly when

\[
 D>0\quad\text{and}\quad [C]=0\text{ in }\mathbb Z/D\mathbb Z.
 \tag{3.1}
\]

For such an orbit, every exponent in the word is the actual valuation. Define the literal displacement

\[
 y_i=x_i-1.
\]

It satisfies

\[
 B_py=b_p,\qquad (b_p)_i=4-2^{a_i}.
 \tag{3.2}
\]

The trivial positive orbit is characterized by each of the equivalent statements

\[
 x_i=1\ (\text{all }i),\qquad y=0,\qquad b_p=0,
 \qquad a_i=2\ (\text{all }i).
 \tag{3.3}
\]

Every other positive integer closed orbit has \(x_i\ge3\), hence \(y_i\ge2\), at every position.

**Proof.** Every cyclic numerator is positive. Equation (1.5) therefore gives positivity exactly when \(D>0\); the common denominator calculation gives integrality exactly when \([C]=0\). From the integer equation in row \(i\), reduction modulo 2 makes \(x_i\) odd. The next coordinate is also odd, so \(3x_i+1=2^{a_i}x_{i+1}\) has valuation exactly \(a_i\).

Subtract \(B_p\mathbf1\), whose row is \(2^{a_i}-3\), from the original equation to obtain (3.2). Since \(B_p\) is injective, \(b_p=0\) implies \(y=0\), and the other equivalences are immediate. An orbit containing 1 remains at 1 under the actual deterministic map. Every positive odd integer other than 1 is at least 3. ∎

The anchored forcing has

\[
 \mathcal F_p(b_p)=C-D,
 \tag{3.4}
\]

which has the same cohomology class as \(C\). Thus marking this same class again cannot distinguish trivial from nontrivial integral cycles: both are exact forcings. The distinguishing object at this stage is the **unique integral primitive together with its anchor and positivity**, followed by its actual orbit map in Section 4.

For example, \((1,3)\) and \((2,2)\) both have \(D=7\) and \(H^1(K_p)=\mathbb Z/7\mathbb Z\). Their marked forcings are respectively \([5]\) and \([0]\). The latter gives \((1,1)\). The group itself is nonzero even for this repeated trivial orbit.

### Repetition has two explicit maps

Let \(p=q^r\), retaining the original word and the uniquely shortest repeating word \(q\). With \(U_q,L_q,C_q,D_q\) unchanged, put

\[
 S_r=\sum_{j=0}^{r-1}U_q^{r-1-j}L_q^j.
\]

Direct affine composition proves

\[
 D_p=S_rD_q,\qquad C_p=S_rC_q.
 \tag{3.5}
\]

The chain map

\[
 [\mathbb Z\xrightarrow{D_q}\mathbb Z]
 \longrightarrow[\mathbb Z\xrightarrow{D_p}\mathbb Z]
\]

has degree maps \((1,S_r)\). It induces the injective map
\([z]\mapsto[S_rz]\), and preserves the order of the forcing class. Meanwhile the graph map from the repeated labelled circle to the primitive orbit sends the fundamental cycle to \(r\) times the primitive cycle. Both factors, \(S_r\) and \(r\), are retained; their source maps and meanings are specified rather than interchanged.

### An arbitrary-length family excluded exactly

There is no nontrivial positive integer cycle with zero or one occurrence of the exponent 1 in its **primitive** word.

**Proof.** On every \(x>1\), a branch with \(a\ge2\) strictly decreases. This rules out a closed orbit with no exponent 1.

With exactly one exponent 1, put its source at the minimum \(n\ge3\). Its next value is \((3n+1)/2\), the maximum, since every remaining step decreases. A later exponent at least 3 would produce a value at most

\[
 \frac{3((3n+1)/2)+1}{8}=\frac{9n+5}{16}<n,
\]

contradicting minimality. All other exponents must therefore be 2. For the retained rotated word \(p=(1,2,\ldots,2)\),

\[
 D=2\cdot4^{m-1}-3^m,\qquad C-D=2\cdot3^{m-1}.
 \tag{3.6}
\]

Since \(\gcd(D,6)=1\), integrality forces \(|D|=1\). For \(m=1,2\), \(D=-1\) and the rational cycle is negative. For \(m=3\), \(D=5\); thereafter \(D_{m+1}=4D_m+3^m> D_m\). No positive case remains. ∎

This is a small, fully proved family exclusion, not a claim to supersede the much stronger cycle literature or to resolve the all-word problem.

---

## 4. The actual orbit graph relative to the trivial orbit

The graph has one vertex \(v_n\) and one edge \(e_n\) for every \(n\in X\), with actual successor \(T(n)\). Use the signed boundary convention

\[
 \partial e_n=v_n-v_{T(n)}.
\]

The base subcomplex is the vertex \(v_1\) and its loop \(e_1\). The **relative chain complex** is the actual quotient by this subcomplex:

\[
 C_1^{\rm rel}=\bigoplus_{n\in X\setminus\{1\}}\mathbb Ze_n,
 \qquad C_0^{\rm rel}=\bigoplus_{n\in X\setminus\{1\}}\mathbb Zv_n,
\]
\[
 \partial e_n=v_n-v_{T(n)},\qquad v_1=0.
 \tag{4.1}
\]

The coefficient modules here are direct sums: every chain has finite support. The quotient map sends exactly \(e_1,v_1\) to zero and leaves every other original basis element unchanged.

### The actual morphism from a solved word

A positive integral solution \(x\) of (1.2) defines a graph map from the labelled circle with \(m\) vertices:

\[
 i\longmapsto x_i,\qquad (i\to i+1)\longmapsto e_{x_i}.
 \tag{4.2}
\]

The proof of exact valuations in Theorem 3.1 makes this an actual map into the Collatz graph. On chains it sends \(v_i\mapsto v_{x_i}\), \(e_i\mapsto e_{x_i}\); the boundary equation is literal. Composing with the relative quotient kills the entire map for the trivial word. A nontrivial primitive word sends its fundamental cycle to

\[
 c_p=\sum_{i=1}^m e_{x_i}\ne0,\qquad\partial c_p=0.
 \tag{4.3}
\]

There are no degree-two chains, so this is a nonzero relative homology class. The cochain which is 1 on one chosen orbit edge and 0 on all others has pairing 1 with a primitive cycle and cannot be a coboundary. For a repeated word the pairing is its repetition count.

A primitive word has distinct orbit vertices: equality of two vertices forces equality of all following exponents under deterministic iteration and therefore a proper period of the word. This also proves the repetition assertion without changing the original word.

For completeness, the weighted equation matrix and the ordinary circle coboundary act on the same retained coordinates. Let \(R(x)_i=x_{i+1}\), and put \(\delta=I-R\). For the solved orbit,

\[
 B_p\operatorname{diag}(x_i)
 =I-\operatorname{diag}(3x_i+1)\delta.
 \tag{4.4}
\]

Indeed, the shifted coefficient is \(2^{a_i}x_{i+1}=3x_i+1\). This is an exact operator identity. The positive integer diagonal map is retained with its integral cokernel; it is not asserted to be unimodular. Passage from the forced linear system to (4.2) uses the specified positive integral solution, not a purported isomorphism from a torsion group to a free graph group.

### Theorem 4.1. Full relative groups, including nonperiodic orbits

Declare \(a\sim b\) precisely when their forward orbits meet. This is an equivalence relation and exactly the connected-component relation of the actual graph. Let \(\mathcal B\) be the components not containing 1 and \(\mathcal C\) their periodic cycles. Then

\[
 H_0(C^{\rm rel})\simeq\bigoplus_{B\in\mathcal B}\mathbb Z,
 \qquad
 H_1(C^{\rm rel})\simeq\bigoplus_{C\in\mathcal C}\mathbb Z.
 \tag{4.5}
\]

Each component in \(\mathcal B\) contains either a single periodic cycle or an injective forward ray. On the positive integers such an injective forward orbit tends to infinity.

**Proof.** Meeting of forward orbits is transitive: from a meeting of the first two and a meeting of the second and third, advance sufficiently along the second orbit. Every graph edge joins equivalent vertices; a meeting supplies a finite undirected path. Thus this is exactly connectivity.

Modulo the boundaries \(v_n-v_{T(n)}\), the vertices of one component are equal. The sum-of-coefficients functional on any component in \(\mathcal B\) annihilates every boundary and maps its common vertex class to 1. A finite combination of vertices with total coefficient zero in each component is a boundary: join its finitely many vertices by finitely many graph paths and telescope their differences. Components meeting 1 vanish in the relative quotient. This proves the first formula and gives both the quotient and its explicit finite relations.

A repeated vertex in a forward orbit produces a cycle. All vertices in its component eventually meet that cycle, so a component contains at most one cycle. Without a repeated vertex, the forward orbit is injective. An injective positive-integer orbit visits each finite set only finitely often and therefore tends to infinity.

Every finite-support closed edge chain is supported on cycles. To see this directly, remove leaves from the finite support graph; the coefficient of an edge incident to a terminal leaf is forced to zero by its boundary. The remaining finite components have all indegrees and outdegrees balanced. Since each vertex has at most one outgoing edge, their nonzero parts are directed cycles with a constant coefficient around each. The base loop was removed. The actual cycle sums are independent because their edges are disjoint. This proves the second formula. ∎

### Relative cohomology, with its coefficient space specified

Take the algebraic dual cochains

\[
 C^0_{\rm rel}=\{f:X\to\mathbb Z:f(1)=0\},\qquad
 C^1_{\rm rel}=\{g:X\setminus\{1\}\to\mathbb Z\},
\]
\[
 (\delta f)(n)=f(n)-f(T(n)).
 \tag{4.6}
\]

These are products of copies of \(\mathbb Z\), not finite-support cochains. The natural evaluation pairing with the finite-support chains (4.1) is always a finite sum. One has

\[
 H^0_{\rm rel}\simeq\prod_{B\in\mathcal B}\mathbb Z,
 \qquad
 H^1_{\rm rel}\simeq\prod_{C\in\mathcal C}\mathbb Z.
 \tag{4.7}
\]

The first map records the constant value of an invariant function on each component. The second records the period

\[
 \operatorname{per}_C(g)=\sum_{n\in C}g(n).
 \tag{4.8}
\]

Here is an explicit proof of the second identification. Every coboundary has zero period. Conversely, for a cochain with zero period on every cycle, choose one cycle vertex and prescribe its primitive value to be zero; successive equations determine the remaining values consistently around the cycle. On an acyclic component choose a forward ray \(r_0,r_1,\ldots\), prescribe \(f(r_0)=0\), and set \(f(r_{j+1})=f(r_j)-g(r_j)\). Every other vertex eventually meets the selected ray or cycle; extend backward by the finite sum of \(g\) along that path. In the component of 1 use \(f(1)=0\) and the same finite sums. This constructs a primitive on every component. Finally any integer period assignment is realized by a cochain supported on one selected edge per cycle. This proves (4.7).

The relative removal of the trivial orbit is consequently exact: its own period has been removed by the displayed subcomplex quotient. An actual nontrivial positive cycle supplies a remaining period-1 detector. An acyclic component not reaching 1 contributes to \(H^0\) but no cycle period in \(H^1\). These statements are proved by the component maps and explicit primitives above.

---

## 5. What resolves the full conjecture in this complex

Let \(\eta(n)=1\) on every relative edge. The following are equivalent, with no conjectural analytic estimate assumed:

\[
 \text{every }n\in X\text{ reaches }1;
\]
\[
 H_0(C^{\rm rel})=0;
\]
\[
 \text{for each }n>1,\quad v_n\text{ is the boundary of a finite integer edge chain};
\]
\[
 \text{there exists }h:X\to\mathbb Z_{\ge0},\quad h(1)=0,
 \quad\delta h=\eta.
 \tag{5.1}
\]

**Proof.** A path from \(n\) to 1 gives the finite chain

\[
 H(v_n)=\sum_{j=0}^{\tau(n)-1}e_{T^j(n)},\qquad
 \partial H(v_n)=v_n.
 \tag{5.2}
\]

Conversely the component augmentation in Theorem 4.1 makes such a boundary impossible in a component not containing 1. This proves the first three equivalences.

On the basin of 1, \(h(n)=\tau(n)\), the exact number of odd returns to 1, satisfies the fourth statement. A nonnegative solution gives \(h(T^j(n))=h(n)-j\) for as long as 1 has not been reached. At \(j>h(n)\) that would be negative, so every orbit reaches 1. Moreover iteration to 1 proves that any such solution equals \(\tau\). ∎

This pinpoints the extra requirement beyond eliminating cycle periods. On an acyclic component the signed integer primitive of \(\eta\) constructed in Section 4 takes values \(f(r_j)=f(r_0)-j\) on a forward ray. It is unbounded below. The original positive source and the nonnegative codomain in (5.1) detect precisely what that signed primitive fails to supply.

No global nonnegative primitive has been constructed in this contribution. The implemented certificates construct the actual columns (5.2) on proved source sets, while retaining the remaining roots and boundaries.

### Formal inversion has a specified specialization problem

Identify edge and vertex bases by their source indices and define

\[
 P(v_n)=v_{T(n)},\qquad v_1=0.
\]

Then \(\partial=I-P\). On formal power series in \(t\),

\[
 (I-tP)^{-1}v_n=\sum_{j\ge0}t^jP^jv_n.
 \tag{5.3}
\]

The equality follows coefficient by coefficient. For a source reaching 1 it is a polynomial and its evaluation at \(t=1\) is the finite chain (5.2). For a periodic source away from 1, coefficients recur on the cycle and their proposed sum is not a finite integer coefficient. For an injective forward orbit, infinitely many distinct basis vectors occur, outside the direct sum. Equation (5.3) therefore has its exact source module and specialization behavior recorded; no formal inverse is passed off as an integral finite-support contraction.

---

## 6. Certified descent gives a counterexample-preserving chain retraction

A **checked descent record** consists of an actual positive odd source \(n>1\), its full actual exponent word \(p_n\), and the terminal value \(d(n)=T^{|p_n|}(n)<n\). Its retained path chain is

\[
 b_n=\sum_{j=0}^{|p_n|-1}e_{T^j(n)},\qquad
 \partial b_n=v_n-v_{d(n)}.
 \tag{6.1}
\]

A path ending at 1 stops there, so no base loop is added. The preceding workbench's supported stopping leaves produce precisely such records using their original affine descent inequalities and actual source charts.

Take the actual finite collection of checked records stored by the algorithm. Unlisted vertices remain roots. Define recursively in increasing integer order:

\[
 r(1)=1,\quad H(v_1)=0;
\]
\[
 r(n)=n,\quad H(v_n)=0\quad\text{for an unlisted }n;
\]
\[
 r(n)=r(d(n)),\quad H(v_n)=b_n+H(v_{d(n)})
 \quad\text{for a listed }n.
 \tag{6.2}
\]

Every recursive endpoint is strictly smaller than its source, so this is a finite, well-defined construction. It does not require knowledge of an unlisted orbit's future.

Define linear maps on the original relative modules by

\[
 Q(v_n)=v_{r(n)},\qquad
 F=I-H\partial\quad\text{on }C_1^{\rm rel}.
 \tag{6.3}
\]

### Theorem 6.1. Exact compression and preservation of every cycle

The maps satisfy

\[
 \partial H=I-Q,\quad HQ=0,\quad Q^2=Q,
\]
\[
 \partial F=Q\partial,\quad F^2=F,\quad I-F=H\partial.
 \tag{6.4}
\]

Consequently the image complex

\[
 [\operatorname{im}F\xrightarrow{\partial}\operatorname{im}Q]
\]

is a chain-homotopy retract of the original relative complex, with inclusion, retraction \((F,Q)\), and homotopy \(H\) explicitly specified. Its homology and algebraic dual cohomology are preserved by those maps.

Most importantly,

\[
 \partial c=0\quad\Longrightarrow\quad Fc=c.
 \tag{6.5}
\]

Every closed cycle chain is retained **as the same chain on the original edges**.

**Proof.** Telescoping (6.1) along the finite recursion gives \(\partial H(v_n)=v_n-v_{r(n)}\). A root has no descent record, so \(H(v_{r(n)})=0\) and \(r(r(n))=r(n)\). This gives the first row of (6.4). Further,

\[
 \partial F=\partial-\partial H\partial
 =\partial-(I-Q)\partial=Q\partial.
\]

From \(H\partial H=H(I-Q)=H\),

\[
 F^2=I-2H\partial+H\partial H\partial=I-H\partial=F.
\]

The remaining homotopy identity is the definition. The retraction is the identity on its image; its inclusion followed by retraction is the displayed projection, chain homotopic to the identity. Applying \(\operatorname{Hom}(-,\mathbb Z)\) to these actual identities gives the dual cochain homotopy without assuming an exactness theorem for unspecified coefficient spaces. Finally (6.5) follows by substituting \(\partial c=0\) into (6.3). ∎

This does not contract every unresolved root to 1. It constructs a smaller, explicitly embedded complex whose nontrivial cycle and component obstructions are retained. Extending the checked descent collection extends the certificate; it does not silently supply missing records.

### Executed positive control with an actual nontrivial cycle

For detector validation only, retain the explicitly changed map

\[
 T_{-}(n)=\frac{3n-1}{2^{\nu_2(3n-1)}}.
\]

It has the positive cycle

\[
 5\xrightarrow{a=1}7\xrightarrow{a=2}5.
 \tag{6.6}
\]

The corresponding word has \(D=-1\). Its forcing is \(-\mathbf1\), not \(\mathbf1\), and its positive solution is \((5,7)\). The relation to the original signed map is the literal conjugacy

\[
 T_{-}(n)=-T_{+}(-n),
\]

with the same valuation since \(3(-n)+1=-(3n-1)\). The forcing change is tracked in every control certificate; it is not a positive Collatz counterexample.

Use only the checked descent record \(7\to5\). Then

\[
 H(v_7)=e_7,\quad H(v_5)=0,\quad Q(v_7)=Q(v_5)=v_5,
\]
\[
 F(e_7)=0,\qquad F(e_5)=e_5+e_7,
\]
\[
 F(e_5+e_7)=e_5+e_7.
 \tag{6.7}
\]

Thus compression exposes a surviving loop at root 5 while preserving its actual two-edge cycle. Its detecting cochain has value 1 on \(e_5\) and 0 on \(e_7\), and pairs to 1.

For the original map, the predecessor's block

\[
 247\to371\to557\to209\to157
\]

has boundary \(v_{247}-v_{157}\). Adding the independently computed actual path from 157 to 1 gives boundary exactly \(v_{247}\). Both that bridge and the compression identities on the checked source families are executed in `verify.py`.


### Theorem 6.2. Whole-source cutoff retractions and their compatible limit

The implementation also uses the predecessor's exact observer directly, without first replacing the infinite source by a finite list. For each integer cutoff \(H\ge0\), the observer accepts precisely the original reference-certified stopping words with total exponent sum at most \(H\). Its check on any given positive integer terminates. Apply the recursion (6.2) to these actual records; write the resulting maps as

\[
 r_H,\quad h_H:C_0^{\rm rel}\to C_1^{\rm rel},\quad
 Q_H,\quad F_H=I-h_H\partial.
\]

This defines maps on **all** original positive odd vertices: every accepted block lowers its positive source, so a queried vertex needs only finitely many accepted blocks before reaching 1 or an actual cutoff root. No decision of never-stopping is made.

For \(K\ge H\), the exact comparison identities are

\[
 r_K(r_H(n))=r_K(n),\qquad r_H(r_K(n))=r_K(n),
\]
\[
 h_K=h_H+h_KQ_H,\qquad h_HQ_K=0,
\]
\[
 Q_KQ_H=Q_HQ_K=Q_K,\qquad F_KF_H=F_HF_K=F_K.
 \tag{6.8}
\]

For every fixed vertex \(n\), \(r_H(n)\) is a nonincreasing positive integer sequence and is eventually constant. Its path chain \(h_H(v_n)\) is also eventually constant. Denote the actual eventual values by \(r_\infty(n)\) and \(h_\infty(v_n)\). These are well-defined mathematical maps with finite-support columns, even though an algorithm is not supplied that recognizes the final cutoff for an unresolved root. They give the chain-homotopy retraction

\[
 Q_\infty(v_n)=v_{r_\infty(n)},\qquad
 F_\infty=I-h_\infty\partial,
 \tag{6.9}
\]

onto a complex whose vertex basis is exactly the retained never-reference-certified positive integers, with 1 removed relatively. Every actual cycle chain remains unchanged by \(F_\infty\).

Furthermore,

\[
 r_\infty(n)=1
 \quad\Longleftrightarrow\quad
 r_H(n)=1\text{ for some finite }H
 \quad\Longleftrightarrow\quad n\text{ reaches }1.
 \tag{6.10}
\]

**Proof.** A stopping word already accepted at \(H\) is the same first reference-certified word at \(K\); raising the cutoff does not change an accepted original word. Thus the \(K\)-path follows the entire \(H\)-path and then continues from its actual root. This proves the first root identity and \(h_K=h_H+h_KQ_H\). A \(K\)-root other than 1 has no accepted word at \(K\), hence none at \(H\); it is already an \(H\)-root. This proves the other root identity and \(h_HQ_K=0\).

The \(Q\)-identities follow on each original basis vertex. For the edge maps use \(\partial h_H=I-Q_H\), the path extension identity, and \(h_HQ_K=0\) in direct multiplication of \((I-h_K\partial)(I-h_H\partial)\) and the reversed product. Both are \(I-h_K\partial\), proving (6.8).

Since a new accepted block strictly lowers the old root, the root sequence is nonincreasing in the ordinary positive integers. It is eventually constant. At any stage after that stabilization, a nonempty further descent from the root would produce a smaller root, which is impossible. The path extension identity then shows that the finite path column has stabilized as well. The finite chain identities of Theorem 6.1 pass to these eventual values on each basis column, and hence on every finite-support chain. This proves the retraction (6.9).

A final non-base root has no reference-certified word at any finite exponent cutoff, so it is exactly a never-reference-certified source. Conversely such a source is fixed at every cutoff. The vertex-basis assertion follows. Closed cycles are preserved by the same identity \(F_\infty c=c-h_\infty\partial c=c\).

The first equivalence in (6.10) follows from eventual constancy. A finite cutoff reaching root 1 supplies the actual finite path, giving convergence. Conversely a converging integer \(n\ge3\) has some actual full word \(p\) with \(F_p(n)=1\). The slope of \(F_p\) is positive, so \(F_p(3)\le F_p(n)=1<3\). Its first reference-certified stopping word therefore exists. Its terminal source also converges and is strictly smaller. Repeating this argument terminates in the positive integers and uses only finitely many finite stopping words. A cutoff exceeding all their exponent sums reaches root 1. ∎

This is an exact localization of the remaining obstruction to the never-certified source, with a full chain map, inverse-on-image, and homotopy. The residual vertex basis is not declared empty. In particular, evaluating a finite cutoff does not recognize the eventual non-base roots in (6.9).

For every finite \(H\ge1\), the explicit positive integer

\[
 n_H=2^{H+1}-1
\]

is still a cutoff root: its first \(H\) exponents are 1, and none of the formal prefixes sends the reference 3 below 3. It has no accepted leaf with exponent sum at most \(H\). Thus the finite cutoff maps genuinely have retained positive roots. This is not an assertion that their **homology classes** survive to the full graph; Section 7 gives the actual transition maps and finite killing relations.

The replay on the 512 positive odd starts at most 1023 records:

| Exponent cutoff | Sources with root 1 | Distinct other roots in that finite source |
|---:|---:|---:|
| 4 | 6 | 256 |
| 8 | 159 | 138 |
| 12 | 259 | 88 |
| 16 | 287 | 61 |
| 32 | 342 | 23 |
| 64 | 509 | 2 |
| 128 | 512 | 0 |

The counts of distinct roots are not counts of non-base components or of divergent orbits. The unchanged observer leaves 27 as a root through cutoff 64 and gives an actual path to 1 at cutoff 128. Every entry is accompanied by original edge-boundary checks; no tail probability is used to kill a root.

---

## 7. Finite frontiers and integer support at infinite depth

### Finite graph exhaustion with original boundaries

For a finite edge-source set \(S\subset X\setminus\{1\}\), retain every vertex in

\[
 V_S=\{1\}\cup S\cup T(S),
\]

but only the actual edges whose sources are in \(S\). A target outside \(S\cup\{1\}\) remains a named **frontier vertex**; no outgoing edge is invented and no frontier is sent to 1.

Every component has a basepoint, a unique frontier root, or an actual cycle. Relative \(H_1\) consists precisely of the actual cycles already contained in the observed edges. Frontier components contribute to finite \(H_0\), but their eventual component type has not thereby been decided.

For the original map, observing only \(3\to5\) gives relative \(H_0=\mathbb Z\). Adding the actual edge \(5\to1\) kills that class. The explicit inclusion is the original vertex/edge inclusion; the class is killed by the new path, not by a relabelling of the old frontier.

Under increasing actual edge sets exhausting all positive odd sources, every finite chain and every finite boundary relation appears at a finite stage. Hence the direct limit of the finite homology groups is the full homology (4.5). A vertex class vanishes in the limit exactly when one of its finite-stage actual path relations kills it. This follows directly from the finite-support definition; no uniform finite stopping bound is inferred.

### The residue tower and ordinary positive integers

For an infinite word, write \(r_m\) for the selected positive residue of its first \(m\) exponents modulo \(2^{A_m+1}\). Cylinder containment gives

\[
 r_{m+1}=r_m+2^{A_m+1}b_m,\qquad b_m\in\mathbb Z_{\ge0}.
 \tag{7.1}
\]

The exact digit \(b_m\) is retained; it is bounded above by the refinement modulus minus one. These compatible residues define a unique 2-adic point. The precise ordinary-integer criterion is

\[
 \text{the infinite word is realized by a positive integer}
 \quad\Longleftrightarrow\quad (r_m)\text{ is bounded in }\mathbb R
 \quad\Longleftrightarrow\quad r_m\text{ is eventually constant}.
 \tag{7.2}
\]

**Proof.** The residues are nondecreasing positive integers by (7.1), so boundedness is equivalent to eventual constancy. An eventual constant \(n\) satisfies every cylinder congruence; cylinder legality then gives every finite prefix of the actual orbit of \(n\). Conversely, an actual positive \(n\) has \(r_m=n\) as soon as the modulus exceeds \(n\). Since \(A_m\ge m\), that occurs. ∎

This is the exact map connecting all compatible dyadic data to ordinary positive support. No measure-zero set of codes is removed. For the word \((1,1,\ldots)\),

\[
 r_m=2^{m+1}-1,
\]

so its 2-adic point is \(-1\), with no positive integer realization. For the word \((2,2,\ldots)\), \(r_m=1\) identically.

For a periodic code \(p^\infty\), the same inverse-cylinder maps give the unique 2-adic fixed point \(C/D\). It is a positive integer exactly by Theorem 3.1. For a nonperiodic code, (7.2) remains the exact integer-membership test; this contribution does not prove that every bounded-residue code eventually has exponent 2 forever.

### The unbounded initial ascent is discharged with the original coordinates

For every positive odd integer write, using the unique valuation and its inverse chart,

\[
 n=2^ku-1,\qquad k=\nu_2(n+1)\ge1,\quad u\ge1\text{ odd}.
\]

For \(0\le j\le k-1\),

\[
 T^j(n)=3^j2^{k-j}u-1.
 \tag{7.3}
\]

The first \(k-1\) exponents are exactly 1. With

\[
 r=\nu_2(3^ku-1),
\]

the next exponent is \(r+1\), and the completed terminal value is

\[
 y=\frac{3^ku-1}{2^r}.
 \tag{7.4}
\]

These identities follow by substituting the original branch and retaining its minus-one offset at every step. They show directly that the infinite all-1 code is absent from the positive source, without discarding the arbitrarily long finite all-1 runs. The exact descent condition for this whole block is

\[
 y<n\quad\Longleftrightarrow\quad
 (2^{k+r}-3^k)u>2^r-1.
 \tag{7.5}
\]

No sign of a logarithmic average replaces the right-hand affine constant.

### Localization of an actual unresolved component

Every actual component not containing 1 has a least positive integer \(s\ge3\). Every point on its forward orbit is at least \(s\). For every prefix with original data \((D_j,C_j)\),

\[
 D_js\le C_j.
 \tag{7.6}
\]

For \(D_j>0\) this is the original no-descent inequality; for \(D_j\le0\) it holds because \(C_j>0\). It implies \(F_j(3)\ge3\): for \(D_j>0\), \(C_j\ge D_js\ge3D_j\), and for \(D_j\le0\) the same conclusion is immediate. Therefore this minimum belongs to the predecessor's retained never-reference-certified support, not to a supported descent leaf.

This applies to a periodic component and to an acyclic component by the same original-source inequality. It identifies where a counterexample would survive the exact descent process. It does not infer that this support is empty from its reference weight.

---

## 8. Executed evidence and the remaining mathematical calculation

The new replay contains 42,507 named exact checks, 344 independently solved matrix fixtures, and 468 exhaustive modular fixtures. It visits every nonempty exponent word with total exponent sum at most 20: exactly 1,048,575 words. The only positive integral words in that finite domain are the ten retained repetitions \((2)^r\), \(1\le r\le10\). This is an exhaustive bounded check, not an all-word estimate and not a new record in Collatz verification.

The checker also constructs finite-support path certificates for all 2,048 positive odd starts at most 4095. It verifies the relative graph ranks by independent rational matrix elimination on the small graph fixtures, checks the primitive and repeated cycle maps, preserves a real control cycle under descent compression, and rejects ten deliberately false or malformed inputs. Finite frontier observations are always labelled open, not divergent.

Both ordinary and optimized Python must reproduce `verification.json` byte-for-byte. The inherited 175,269-check replay and 142-check support certificate are run separately against the retained predecessor bytes. These counts are not merged into a claim of independent proof of an infinite assertion.

The remaining exact construction is a source-complete finite-support contraction, or equivalently the nonnegative integral primitive in (5.1), with all original orbit edges retained. Section 6 provides the verified extension operation for adding descent certificates without losing cycle or component obstructions. Section 7 supplies the exact positive-integer support criterion for a surviving infinite code. Neither universal source coverage nor emptiness of the remaining non-base components has been proved here.

The available work now consists of executable return and period detectors, a counterexample-preserving compression, explicit infinite-family exclusions, retained boundary/source criteria, and a replayable integration package. A positive nontrivial cycle would yield a finite certificate accepted by the original-forcing detector and a nonzero relative period. A nonperiodic failure would survive as a non-base component with the bounded-residue integer support in (7.2), even though it supplies no finite cycle period. No such original positive counterexample is asserted by this contribution.

---

## References and inspection scope

**[P]** `../stopped_affine_transport_20260914/note.md`, Sections 1–4, 9, and 10.0, with its original executable, manifest, and support certificate. The supplied files are retained unchanged and their finite outputs were replayed. This is not a claim of a fresh independent audit of every preceding infinite proof.

**[R1]** Jeffrey C. Lagarias, *The set of rational cycles for the 3x+1 problem*, Acta Arithmetica 56 (1990), 33–53. Bibliographic record: `https://eudml.org/doc/206298`; author's publication listing: `https://dept.math.lsa.umich.edu/~lagarias/3x%2B1.html`. The metadata and author's listing were inspected; no uninspected detailed result of that paper is used as a proof dependency.

**[R2]** Takehiko Mori, *Application of Operator Theory for the Collatz Conjecture*, arXiv:2411.08084. Abstract inspected at `https://arxiv.org/abs/2411.08084`. Cited to acknowledge existing operator/irreducibility formulations, not as a dependency for (4.5)–(6.5).

All proofs needed for the new computations are included above. Their status is the written argument plus exact finite replay, not an external acceptance or a claim to have settled Collatz.
