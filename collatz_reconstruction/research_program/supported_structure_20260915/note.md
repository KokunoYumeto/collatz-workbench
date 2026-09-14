# A structural Split-Zero restatement of Collatz

15 September 2026. Source checkpoint: `KokunoYumeto/collatz-workbench`, PR #2, commit `6b3ded8880946b2c3140a9d79f1aa1d658d36b8c`.

This note answers a structural question: what are the complete modules behind the supported zeros, and which arithmetic assertions would remove every nonbase obstruction? It retains the original source, the integral lattice, both clocks, original word order, maps, and representative fibres. It does not claim a proof or disproof of Collatz, a new numerical cycle bound, an independently reviewed theorem, or a Lean execution.

The completion-defect source already constructs the weighted complex, the formal inverse, its defect isomorphism, the finite endpoint-kernel basis, and component coordinates. The additions here are the maximal-one-run comparison; a proof that both clocks are invertible on the original cohomology; the resulting full Laurent-module classification; its torsion/generic-fibre decomposition; the positive-cone interpretation of the death filtration; an absolute/base-relative exact sequence; and a proof-obligation and certificate design. Component index sets below mean the actual components of the original map. They may be empty. They are not hypothetical replacement graphs.

## 1. The actual source and the history presentation

Let

\[
 X=\{1,3,5,\ldots\},\quad T(n)=(3n+1)/2^{a(n)},\quad a(n)=\nu_2(3n+1),
\]
\[
 \Lambda=\mathbb Z[v],\quad R=\Lambda[u],\quad
 A=\Lambda^{(X\setminus\{1\})},\quad M=A[u].
\]

The superscript `( )` denotes finite support. Its basis vector \(V_n\) retains the original positive integer. Define

\[
 S V_n=v^{a(n)-1}V_{T(n)},\quad V_1=0,\qquad d=I-uS,
 \qquad K=[M\xrightarrow d M],\quad Q=\operatorname{coker}d. \tag{1}
\]

The complex is in cochain degrees 0 and 1. In its source degree the basis is also written \(E_n\), and the identification \(E_n\leftrightarrow V_n\) is explicit and invertible. Thus \(dE_n=V_n-u v^{a(n)-1}V_{T(n)}\). An exponent a expands to one shortened odd step and a-1 shortened even steps. Parsing at odd endpoints is its inverse. Hence u and v retain the companion's original clocks.

A useful retained object is the diagram consisting of \(M,dM,Q\), the original labelled basis, all finite path words, \(\ker S^N\), the completion inclusion, and its inverse primitives. Q alone is not the entire history. For example equal source classes have representatives differing by d of an original finite vector. Keeping that vector and d is how the relation is retained; the quotient element alone does not determine it uniquely.

For each seed label \(F\subseteq X\setminus\{1\}\), form the original forward carrier \(\Omega_F=\{1\}\cup\{T^j(n):n\in F,j\ge0\}\). Use (1) on this carrier. Inclusions of seed sets act by the original basis inclusions, not by renaming vertices. The Split-Zero total is the disjoint union over F. A supported scalar zero sends \((F,z)\) to \((F,0)\), while the external absent scalar sends it to \((\varnothing,0)\). Addition transports both terms into the union label. These are precisely the source's reconstruction formulas [SZ]. This note uses the full modules and maps in each fibre, not only their labels.

## 2. What the zero in the completed complex means

Let \(\widehat M=A[[u]]\), coefficientwise finite in the original vertex basis. The predecessor's inverse is

\[
 Gq=\sum_{j\ge0}u^jS^jq,\qquad \widehat dG=G\widehat d=I. \tag{2}
\]

Every coefficient involves a finite sum. The original kernel of d is zero as well: comparing the lowest u coefficient of df=0 successively gives every coefficient of f equal to zero. Surjectivity on M is not inferred from (2).

With \(D_\infty=\widehat M/M\) and the induced \(\bar d\), the original cohomology is recovered by

\[
 Q\xrightarrow{\eta}\ker\bar d,\quad[q]\mapsto[Gq]\bmod M,
 \qquad
 [g]\xmapsto{\delta}[\widehat dg]\bmod dM. \tag{3}
\]

Changing q by df changes Gq by f; changing g by f changes its differential by df. Equations (2) prove both inverse identities. These maps commute with every seed inclusion. Thus the fibre of the completed homology map over its supported zero is the full original Q_F, explicitly realized by (3). The class is not reconstructed from the zero symbol alone: the specified source, relation space and comparison kernel are retained.

For a singleton, before arrival at 1,

\[
 S^jV_n=v^{E_j(n)}V_{T^j(n)},\quad E_j(n)=\sum_{i=0}^{j-1}(a(T^i(n))-1).
\]

Consequently the following are exact equivalent statements:

\[
 [V_n]=0\text{ in }Q
 \ \Longleftrightarrow\ GV_n\in M
 \ \Longleftrightarrow\ S^NV_n=0\text{ for some }N
 \ \Longleftrightarrow\ T^N(n)=1\text{ for some }N. \tag{4}
\]

To prove the middle step directly, the series coefficients are distinct u degrees, with one nonzero original singleton monomial at every surviving degree. They vanish eventually exactly on arrival at 1. Equation (3) proves the first step. Its polynomial primitive is the uniquely determined original weighted path. No signed alternate primitive can shorten a genuinely infinite singleton series, by injectivity in (2).

## 3. An arithmetic lemma: maximal strings of exponent 1

### Proposition 1 (exact block, inverse parameters, and retained clocks)

For every positive odd integer n, define

\[
 r=\nu_2(n+1)-1,\qquad t=(n+1)/2^{r+1}.
\]

Then \(r\ge0\), t is positive odd, and \(n=2^{r+1}t-1\). These are mutually inverse parameter maps between positive odd n and pairs \((r,t)\) with r nonnegative and t positive odd. The first r exponents are exactly 1, with

\[
 T^j(n)=3^j2^{r+1-j}t-1\quad(0\le j\le r).
\]

The next exponent and endpoint are

\[
 b=1+\nu_2(3^{r+1}t-1)\ge2,\qquad
 y=\frac{3^{r+1}t-1}{2^{b-1}}. \tag{5}
\]

Thus the complete block is \((1)^r(b)\); it has r+1 odd returns, total exponent r+b, and weight

\[
 W=u^{r+1}v^{b-1}.
\]

**Proof.** For j<r, the displayed value plus 1 is divisible by four. Hence it is 3 modulo four, and its next valuation is exactly 1. Applying (3x+1)/2 gives the next displayed value. At j=r its value plus 1 is twice an odd integer, so the value is 1 modulo four. Its 3x+1 is \(2(3^{r+1}t-1)\), whose inner factor is positive even. This proves (5), including the exact valuation. The parameter inverse follows from the unique 2-adic valuation of n+1. For n=1, (r,t,b,y)=(0,1,2,1); its original fixed edge remains explicit before the relative quotient. QED.

For n>1 let P be the original weighted edge chain of this block. Its telescoping boundary is

\[
 dP=V_n-u^{r+1}v^{b-1}V_y. \tag{6}
\]

Its exact strict-descent test is

\[
 y<n\quad\Longleftrightarrow\quad
 (2^{b+r}-3^{r+1})t>2^{b-1}-1. \tag{7}
\]

This is obtained by multiplying the original endpoint inequality by the positive integer \(2^{b-1}\) and substituting the inverse source formula. No affine term is omitted. Grouping an orbit into these maximal blocks retains (r,b), t, every intermediate integer in (5), and the edge expansion. Parsing the original exponent list into maximal strings of ones followed by one exponent at least two is its inverse.

### Corollary 1 (both clocks are cofinal on every infinite nonbase orbit)

Along every infinite actual orbit remaining above 1, the odd-return count j and the even-step count E_j both tend to infinity. Indeed bounded nondecreasing integer E_j would be eventually constant, so all later exponents would be 1. Proposition 1 proves a finite end to that string at its actual positive starting integer. Equivalently, an infinite all-one string would force n+1 divisible by every power of two. This argument proves cofinality and does not supply an upper bound for the total stopping time.

## 4. Inverting both clocks loses no original cohomology

Put \(L=\mathbb Z[u,u^{-1},v,v^{-1}]\). The assertion here concerns Q, not M: M and all original primitives remain unlocalized.

### Theorem 1 (explicit Laurent structure on Q)

Multiplication by u and by v are bijections on Q. The canonical map

\[
 Q\longrightarrow L\otimes_R Q
\]

is therefore an isomorphism.

**Proof and inverse.** The relation \([q]=u[S q]\) makes the induced S the inverse of multiplication by u. For v-surjectivity, (6) gives

\[
 [V_n]=v\,[u^{r+1}v^{b-2}V_y], \tag{8}
\]

where b>=2. This defines a v-preimage for every original generator and hence for every polynomial class.

For injectivity, write vq=df. Reduce modulo v. In the polynomial module over \(\mathbb Z[u]\), the reduced map is \(I-uS_0\); its lowest-coefficient recursion is injective. Thus \(\bar f=0\), so f=vf_1. Cancelling v in the original free module gives q=df_1. Hence multiplication by v has zero kernel on Q. Equation (8) specifies its unique inverse on every original singleton, independent of representative after passage to Q. This inverse commutes with the original R-action by uniqueness.

The inverse of the localization map sends \(q/(u^a v^b)\) to \(\bar S^a J_v^b(q)\), where J_v is (8). These commuting inverses prove the fraction relations and both compositions. QED.

The corresponding statement holds before relativity, with n=1 giving \(v^{-1}[V_1]=u[V_1]\). This is a proved comparison, not a silent replacement of the finite source by Laurent coefficients.

## 5. Complete component modules, not only a vanishing predicate

Partition the actual functional graph into weak components. Vertices in one component have forward paths that meet: adjacency gives that property and finite chains of adjacencies preserve it. A component either meets 1, contains one other primitive directed cycle, or has an injective forward ray and no cycle. A repetition of a forward value gives the cycle; distinct cycles cannot have meeting forward paths. These observations prove the exhaustive partition.

Write \(\mathcal C_*\) for actual primitive nonbase cycle components and \(\mathcal B_\infty\) for actual components with no periodic vertex. These symbols do not assert that either set has members.

### Theorem 2 (classification with explicit maps)

As an L-module, and hence through Theorem 1 as its original R-module,

\[
 \boxed{\quad
 Q\cong
 \bigoplus_{C\in\mathcal C_*}L/(1-u^{m_C}v^{e_C})
 \ \oplus\ \bigoplus_{B\in\mathcal B_\infty} L,
 \qquad e_C=A_C-m_C.
 \quad} \tag{9}
\]

The component meeting 1 has relative cohomology zero, while its original source vectors and finite contraction columns remain retained. On every actual cycle, m_C>=1 and e_C>=1.

**Proof with component maps.**

**Base component.** For each of its vertices take the actual first-arrival path to 1. Its finite weighted chain P_n obeys dP_n=V_n and P_n=E_n+w_nP_{T(n)}. These two identities give both contraction equations on the original basis. Thus its relative complex is contractible with specified finite columns, not an absent source module.

**Cycle component.** Choose one original cycle vertex c, retaining that choice. For n other than c let P_n be its first path to c and w_n its weight; take P_c=0,w_c=1. Send \([V_n]\) to \([w_n]\) in \(R/(1-W_C)\); the inverse sends 1 to \([V_c]\). Every original edge relation is respected. At c it becomes exactly 1-W_C; all other edges telescope along their first path. These calculations prove both inverse compositions and the exact relation ideal.

There is also a full chain comparison. The scalar complex is \([R\xrightarrow{1-W_C}R]\). The target-degree projection sends V_n to w_n. The source-degree projection sends E_c to 1 and all other original E_n to zero. Its section sends the scalar target generator to V_c and the source generator to the full weighted primitive cycle chain. The homotopy sends V_n to P_n. The path recurrence gives dH=I-psi_1 phi_1 and Hd=I-psi_0 phi_0, including HdE_c=E_c-P_C. All columns are finite despite arbitrarily many incoming vertices.

Corollary 1, or the same impossible all-one argument on a cycle, gives e_C>0. In \(R/(1-u^m v^e)\), u and v already have inverses \(u^{m-1}v^e\) and \(u^m v^{e-1}\). Hence the map to \(L/(1-u^m v^e)\) is an isomorphism with these inverse actions. This proves the displayed summand without losing an integral class.

**Nonperiodic component.** Choose an original forward ray \(x_0,x_1,\ldots\), with prefix weights \(W_j=u^jv^{E_j}\). A vertex n meeting x_j along a path of weight w maps to \(w/W_j\). A later meeting multiplies numerator and denominator by the identical intervening path monomial, proving independence. The inverse sends \(f/W_j\) to \(f[V_{x_j}]\). Original edge relations give both compositions, realizing the module as \(\bigcup_j W_j^{-1}R\).

By Corollary 1, both j and E_j are unbounded and nondecreasing. For every Laurent monomial \(u^a v^b\), select a finite j with \(j+a\ge0\) and \(E_j+b\ge0\). Then

\[
 u^a v^b=\frac{u^{a+j}v^{b+E_j}}{W_j}. \tag{10}
\]

This proves that the union is the whole L and supplies the inverse with an actual finite meeting index. Equal choices of j are compared by the original path monomials. Every original vertex maps to a unit Laurent monomial and is nonzero.

Finally d never mixes different actual components; every finite vector meets finitely many of them. Splitting its coefficients by component gives the direct-sum map in (9), and adding their representatives gives its inverse. QED.

An injective positive-integer ray eventually leaves every bounded interval, since that interval has only finitely many original vertices. The theorem does not claim that such a component exists; it identifies precisely the module carried by one in the actual component decomposition.

## 6. Two complementary retained obstructions

Let \(\mathbb K=\mathbb Q(u,v)\), the fraction field of L, and retain the canonical map

\[
 \ell:Q\longrightarrow\mathbb K\otimes_L Q,\qquad q\mapsto1\otimes q.
\]

Define \(\mathcal T=\ker\ell\) and \(\mathcal F=\mathbb K\otimes_LQ\). An element maps to zero exactly when some nonzero element of L annihilates it: this is the fraction equivalence relation. This standard torsion-kernel principle is recorded in [LOC]; no finite-generation assumption is needed.

Applying (9) gives the complete descriptions

\[
 \mathcal T\cong\bigoplus_{C\in\mathcal C_*}L/(1-W_C),\qquad
 Q/\mathcal T\cong\bigoplus_{B\in\mathcal B_\infty}L,\qquad
 \mathcal F\cong\bigoplus_{B\in\mathcal B_\infty}\mathbb K. \tag{11}
\]

On a cycle, 1-W_C is nonzero in L and becomes a unit in the field, killing exactly that component. On a ray, L includes injectively in its fraction field. The kernel and image statements follow component by component, with finite support across components. The sequence \(0\to\mathcal T\to Q\to Q/\mathcal T\to0\) has the displayed component splitting. The kernel is canonical; the coordinates for each rank-one ray retain the chosen original ray.

For an original singleton the annihilator ideal in L is precisely

\[
 \operatorname{Ann}_L[V_n]=
 \begin{cases}
 L,&n\text{ reaches }1,\\
 (1-W_C),&n\text{ belongs to the nonbase cycle component }C,\\
 (0),&n\text{ belongs to a component in }\mathcal B_\infty.
 \end{cases} \tag{12}
\]

The first statement uses (4). In the second, its image is a unit monomial times 1 in L/(1-W_C), so the annihilator is exactly that ideal. In the third, its image is a unit in the domain L. This is an ideal-valued classification rather than a binary flag.

Polynomial torsion here means annihilation by a nonzero polynomial or Laurent polynomial; it is not an assertion of additive integer torsion. In fact \(L/(1-u^m v^e)\cong\mathbb Z[\mathbb Z^2/\langle(m,e)\rangle]\): send each Laurent monomial to its exponent coset, and send the coset basis back to its residue monomial. The relation identifies exactly those cosets, proving inverse ring maps. The group ring is free as an abelian group on its cosets. The ray module L is likewise free abelian. Thus Q has no additive integer torsion, and Q embeds in \(\mathbb Q\otimes_\mathbb ZQ\). The integer lattice is nevertheless retained, especially for the different, explicitly related integral forcing complex in Section 9.

Every summand in (11) also maps to zero under the original formal completion (2). The retained localization kernel distinguishes periodic torsion from nonperiodic persistence; the completion-defect isomorphism (3) recovers both. Neither projection is used without its actual kernel and source diagram.

## 7. The distinguished trivial cycle before taking the relative quotient

Use the absolute module \(M_{\rm abs}=R^{(X)}\) and the unchanged absolute edge differential. Its original fixed-loop subcomplex is

\[
 K_1=[RE_1\xrightarrow{1-uv}RV_1].
\]

The quotient complex is exactly K in (1). Every I-uS complex is injective in source degree by coefficient recursion. The degreewise exact sequence of these original complexes consequently gives

\[
 \boxed{\quad
 0\longrightarrow R/(1-uv)
 \xrightarrow{1\mapsto[V_1]}Q_{\rm abs}
 \longrightarrow Q\longrightarrow0.
 \quad} \tag{13}
\]

One may also verify injectivity and exactness directly from the component maps in Theorem 2. The actual component meeting 1 is R/(1-uv), and the other components are unchanged. Its map sends an original source to its first-arrival path weight times [V_1], with its entire finite path retained.

The same abstract binomial type occurs for the trivial cycle and other cycles. What singles out the trivial one is the specified actual fixed vertex, the original equation 4x-3x=1 forcing x=1, its actual subcomplex, and all finite incoming histories. No abstract zero or unmarked spectrum makes that selection.

## 8. What distinguishes a supported zero caused by merging from one caused by arrival

For a finite original source set F, set \(K_N(F)=\ker(S^N|_{\Lambda^{(F)}})\). Retain every endpoint \(y_n=T^N(n)\) and exponent E_N(n), stopping at first arrival at 1. At each nonbase endpoint y select an original source n_y minimizing its exponent, with that choice recorded. The predecessor proves the exact basis

\[
 V_n\ (y_n=1),\qquad
 V_n-v^{E_N(n)-E_N(n_y)}V_{n_y}\ (y_n=y>1,n\ne n_y). \tag{14}
\]

The inverse decomposition subtracts each nonselected pivot and collects the selected coefficient at the original y. This is a direct sum of the absorbed coordinate submodule and the specified coalescence-relation submodule; the complement maps to the unchanged original image generators \(v^{E_N(n_y)}V_y\). Thus two different mechanisms of supported zero coexist in a single actual kernel.

Let \(A_+=\mathbb N[v]^{(X\setminus\{1\})}\), the cone of finite vectors with nonnegative polynomial coefficients. Then

\[
 \boxed{\quad
 \ker S^N\cap A_+
 =\left\{\sum c_n(v)V_n:c_n\in\mathbb N[v],\ c_n\ne0\Rightarrow T^N(n)=1\right\}.
 \quad} \tag{15}
\]

**Proof.** At every surviving endpoint the image coefficient is a sum of nonnegative polynomials times nonzero monomials. It is zero exactly when no nonzero input coefficient contributes. Distinct endpoint basis vectors do not cancel. The reverse implication is immediate from V_1=0. QED.

For F={3,5,13}, S V_3=V_5, S V_13=v^2 V_5 and S V_5=0. Hence the first kernel is \(\Lambda V_5\oplus\Lambda(V_{13}-v^2V_3)\). The second generator retains a genuine merger relation, but neither V_3 nor V_13 has vanished after one return. At two returns all three source generators vanish. Formula (15) prevents a large signed kernel from being counted as singleton absorption.

## 9. The cycle word must pass its original arithmetic realization map

The binomial W_C in (9) retains both total clocks, not their complete order. The original ordered word and its forcing polynomial must remain marked. Put

\[
 W_p=u^m v^{A-m},\qquad N_p=\sum_{j=0}^{m-1}u^jv^{A_j-j}.
\]

Write \(b_j=A_j-j\) for j<m and read b_m from the v-degree of W_p. Then \(a_i=1+b_i-b_{i-1}\) recovers the word. Nonnegative nondecreasing b_j with b_0=0 give its exact image conditions. These differences and prefix sums are inverse operations. The raw N_p, not an unspecified quotient representative of it, is retained.

On the finite position circle the weighted graph differential has columns \(E_i\mapsto V_i-w_iV_{i+1}\). Its algebraic dual has

\[
 (J_ph)_i=h_i-u v^{a_i-1}h_{i+1}.
\]

Thus the transpose is the explicit finite free duality map relating graph positions to this equation; its forcing is specified separately. Under \(\alpha:R\to\mathbb Z[1/3]\), \(u\mapsto2/3,v\mapsto2\),

\[
 \alpha(J_p)=-B_p/3,\qquad
 (B_px)_i=2^{a_i}x_{i+1}-3x_i,
\]
\[
 D=2^A-3^m,\quad C=\sum_{j=0}^{m-1}3^{m-1-j}2^{A_j},
 \quad\alpha(1-W_p)=-D/3^m,\quad\alpha(N_p)=C/3^{m-1}. \tag{16}
\]

Consequently the original equation B_px=1 is the forced equation \(\alpha(J_p)x=-1/3\), and its scalar primitive is x_1=C/D. The integral cokernel is Z/DZ with marked forcing [C], via the original telescoping functional. The predecessor's exact localization inverse and the rational-subcomplex maps retain that integral class; they are not replaced by evaluation of arbitrary formal series.

Every positive integral cycle has D>0 and [C]=0. Both the trivial cycle and any other integral cycle obey that same marked vanishing. The unique primitive distinguishes them: x=1 for the trivial word, and every x_i>=3 on a nonbase cycle. Under the explicitly invertible affine coordinate y=x-1,

\[
 B_py=(4-2^{a_i})_i,
\]

with unchanged integral forcing class because its difference is -B_p1. This is a bijection of forced solution sets, not a claim that translation is linear.

For p=(1,3) and p'=(2,2), both W=u^2v^2 and D=7, but N_p=1+u, N_p'=1+uv, C=5 versus 7. The former has a nonintegral rational cycle; the latter is the repeated actual fixed orbit. A proof programme must reject unrealized word cycles before assigning them an actual component in (9). Repeated words retain the covering factor \(1+W+\cdots+W^{r-1}\) and their actual r-fold edge expansion.

## 10. The refined restatement

The following equivalences are proved by (3), (4), (9), (11), and (13):

\[
 \boxed{
 \begin{gathered}
 \text{Every original positive odd integer reaches }1;\\
 \text{the canonical fixed-loop map }R/(1-uv)\to Q_{\rm abs}\text{ is an isomorphism};\\
 \mathcal T=0\text{ and }\mathcal F=0;\\
 \ker(\bar d:A[[u]]/M\to A[[u]]/M)=0;\\
 A=\bigcup_{N\ge0}\ker S^N.
 \end{gathered}} \tag{17}
\]

Each line is read together with its original labelled source and maps. In particular a zero relative module does not erase the base basin's vectors, their merger kernels, clocks, or finite primitives. The first equality in (13) says that the only recurrent module in the absolute object is the actual fixed-loop module. Lines (11) separate periodic polynomial torsion from generic nonperiodic persistence, without discarding either.

There is no common finite N with S^N=0. For N>=1, the original source \(n_N=2^{N+1}-1\) has \(T^j(n_N)=3^j2^{N+1-j}-1\) for 0<=j<=N, so \(S^NV_{n_N}=V_{2\cdot3^N-1}\ne0\). The sources vary with N. This proves why the correct exhaustion in (17) is local rather than one finite global clock. The proof is Proposition 1 specialized to t=1.

## 11. A proof programme: established lemmas and outstanding arithmetic targets

This section is a dependency design, not a collection of assumed conditional theorems. The algebraic statements in Sections 1-10 have proofs. The following arithmetic targets remain unproved here.

### P0. Preserve the presented source throughout

Already available: exact original source cylinders, arbitrary-exponent strata, original block expansions, integral forcing inverses, clocked finite primitives, completion-defect recovery, the positive cone (15), and the component classification (9). The kernel checker must verify these interfaces and retain source hashes, failed candidates, and original maps. A support label by itself is not an adequate source certificate.

### P1. Eliminate the periodic torsion on the actual positive source

Target: determine the full positive integral solutions of B_px=1 for every primitive original word. The required conclusion is that only p=(2) with x=1 is primitive. Retain repetitions explicitly afterwards.

Subtasks: prove symbolic exclusions for complete families of original gap words, transport every congruence test through the integral block inverse, and combine the marked class [C], positivity, minimum placement, the original affine inequalities, and all prime powers. A prime-only test does not establish divisibility by D; a zero marked class does not identify x with 1. A surviving candidate must yield original positive integer coordinates and an independently replayed actual cycle chain. Finite windows closed by descent remain valid, but they are not an all-word theorem until their coverage is proved.

### P2. Eliminate the generic nonperiodic component module

Target: establish \(\mathcal F=0\) on the actual source. By (11) this is exactly the absence of a component whose module is L and whose every original singleton remains nonzero over the fraction field.

An analytic completion that kills all Q has already failed to distinguish these classes; (3) gives its full successful recovery. A useful new comparison must therefore carry this retained defect, not just show another completed inverse. Any norm, trace or asymptotic estimate must be evaluated on the original labelled residuals, with its kernel, topology, scalar action, and return map specified. No such global estimate is supplied here.

The direct arithmetic route is the survivor-source tree in P3. A no-descent minimum of a nonbase component has every iterate at least its original minimum; all original affine inequalities therefore remain attached. A nonperiodic component has such a minimum by well ordering of positive integers. This makes minimum-source analysis address the generic obstruction as well as cycles.

### P3. Prove arithmetic exhaustion, not only finite-jet exhaustion

A finite word p has original data L,U,C, legal residue r_p modulo 2U, and the actual affine map (Ln+C)/U. Its no-descent source is exactly

\[
 \mathcal S_p=\{n=r_p+2Ut\ge3:\ t\in\mathbb Z,\ D_jn\le C_j\ (1\le j\le|p|)\}. \tag{18}
\]

For D_j<=0 there is no upper restriction; for D_j>0 it is the explicit upper bound n<=C_j/D_j. Appending a gives L'=3L,U'=2^aU,C'=3C+U, the original congruence lift, and set inclusion \(\mathcal S_{pa}\subseteq\mathcal S_p\). Empty sets remain declared supported nodes with their equations, not deleted records. The prior unbounded-tail construction represents all large a by one exact progression plus its valuation map; Proposition 1 gives a second full block dictionary with (5)-(7).

Target: prove that every compatible infinite sequence of these no-descent source sets has empty intersection in the ordinary positive integers. The finitely branching reformulation produced by the prior whole-tail decomposition retains all integer parameters and exceptional boxes. An infinite path of nonempty finite-prefix cylinders alone is not a positive integer witness.

A concrete subtarget is a height-escape statement for the canonical residues of all surviving paths. Those residues obey \(r_{j+1}=r_j+2^{A_j+1}b_j\), b_j>=0. A bounded sequence is eventually constant; then its value realizes every prefix by the original cylinder theorem. Conversely the residues of a fixed positive realizing integer become that integer once the modulus exceeds it. Thus ordinary-integer support is exactly the eventual-constant case, including the source inequalities (18). An all-one branch is already excluded by r_j=2^{j+1}-1. The remaining nonconstant-word and first-coefficient-crossing families require new arithmetic control; the finite boxes cannot be discarded merely because each individual box is finite.

This target addresses every nonbase component: its least integer belongs to all of the source sets (18) for its itinerary. Its first exponent is 1, since T(n)<n for n>1 whenever a(n)>=2. This is a proved initial restriction, not an assumed distribution of exponents.

### P4. Assemble a finite-column, positive contraction

Target: construct for each original n a finite polynomial column h(V_n), with nonnegative monomial path coefficients, satisfying dh=I and hd=I on original finite-support modules. The exact predecessor splice identities permit an accepted actual descent to attach at an old retained root, with the old terminal clock multiplied into the new path. The extra homotopy lies in the old projected edge module and closed cycle chains are fixed literally. Thus new descent coverage cannot accidentally delete a genuine counterexample.

The original source number itself is a well-founded ranking for strict-descent splices. One must prove applicability on every residual source, or supply another explicitly defined well-founded ranking with a proved transition decrease. Calling the stopping time a ranking does not prove that it is finite. This is the still-missing global applicability assertion, not an unrecorded premise.

## 12. The program to build

Separate a small exact certificate checker from a potentially elaborate search engine. The search engine may propose words, parameter families, period obstructions, or survivor invariants; no search timeout is a mathematical certificate.

Required records:

* `source_state`: original seed label, exact integer or parameter domain, ordered exponent word, every affine prefix, integral lattice, original and weighted boundary, terminal clock, and next-step partition with all empty and exceptional cases.
* `finite_primitive`: a finite weighted edge column; the checker proves its full untruncated boundary. A symbolic family also needs its exact parameter-domain proof and word/valuation inverse. A point sample never validates its universal quantifier.
* `cycle_realization`: original primitive word, D,C, every rational primitive coordinate, verified positive integer valuations, repetition map, and actual relative period chain. Failure modes are marked forcing, positivity, valuation, and period failures separately.
* `survivor_certificate`: a fully proved original-source invariant set or exact infinite-support obstruction, excluding 1 under all its actual transitions. Finite residual jets are not admitted as this type.
* `projection_record`: exact map and coefficient domain, killed-representative module, old relation submodule, inverse/comparison maps, and original source support. A reported supported zero cites this record.

Useful computation priorities are complete symbolic arithmetic families, increasing positive-coordinate absorption, and retained affine exception boxes. Kernel dimension alone is insufficient because of (14)-(15). Generic rank and periodic torsion are different outputs of the same explicitly computed module, not substitute success criteria.

Completion-defect CI already checks the prior retained maps. This increment adds finite tests for (5)-(8), the full cycle chain comparison in Theorem 2, Laurent coset and ray-coordinate inverses, ordered forcing recovery, the positive-cone test, and false-certificate rejection. These tests are executable regression evidence; they do not establish P1-P4 globally. The notes supply the general algebraic proofs, not the number of test cases.

## 13. Sources and attribution

[SZ] `KokunoYumeto/zeta-function-research-reader`, commit `91ed3b7c358a1f444d0d48c292e4a400ca509eff`, `formal/splitzero/DERIVED_MATHEMATICS.md`, blob `fe05d32ccd314daac7c59d225c9cac3d4c1bf3d3`, Sections 1-4. This is the source of support reconstruction and the killed-representative quotient. No new Lean execution is claimed.

[CD] `KokunoYumeto/collatz-workbench`, commit `6b3ded8880946b2c3140a9d79f1aa1d658d36b8c`, `collatz_reconstruction/research_program/completion_defect_20260914/note.md`, blob `9f00643cb135acd77defec9e05ad63b632443a50`. This supplies (1)-(4), the direct-limit comparison, finite endpoint-kernel basis, and preceding component maps. The uploaded full proof was checked against this Git blob before continuation.

[W] The same repository's research companion `01_weighted_path_and_finite_residue_actions.tex`, blob `f0142c0d4c237ed068a0762a08c6622df5dbcfee`, supplies the original path category, clocks and completed transfer inverse. The older residual-splice and integral-block notes remain attached through [CD].

[LOC] The Stacks Project, Lemma 15.22.2, https://stacks.math.columbia.edu/tag/0537 : torsion as the kernel of the fraction-field map. Section 15.22, https://stacks.math.columbia.edu/tag/0549 . Definition 10.9.6, https://stacks.math.columbia.edu/tag/07JZ . The relevant fractions and kernels are also proved directly above.

Existing operator formulations are not assigned priority to this work: M. Neklyudov, *Functional analysis approach to the Collatz conjecture*, arXiv:2106.11859; T. Mori, *Application of Operator Theory for the Collatz Conjecture*, arXiv:2411.08084. Their abstracts were inspected for this attribution boundary, not used as proof premises. No isomorphism with their analytic operator spaces is asserted or needed for the maps proved here.
