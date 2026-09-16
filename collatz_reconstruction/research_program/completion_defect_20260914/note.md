# Recovering supported Collatz classes from a vanishing completion

14 September 2026. Continuation of `KokunoYumeto/collatz-workbench`, read at `ce8f784da8fb48aa19065c036cd815c05628cec4` on PR #2. This contribution concerns infinite formal paths and the spaces carried to supported zero. It makes no new numerical cycle-bound claim.

## 1. Source objects, support, and comparisons

The coefficient and homology source is the Split-Zero programme's `formal/splitzero/DERIVED_MATHEMATICS.md`, Sections 1–4, at Zeta commit `91ed3b7c358a1f444d0d48c292e4a400ca509eff`, blob `fe05d32ccd314daac7c59d225c9cac3d4c1bf3d3`. It constructs support-indexed modules and their actual transition maps. For a chain map i, its module of representatives mapped to target boundaries, modulo the *original* source boundaries, is explicitly isomorphic to ker H(i). This note instantiates that construction on the original Collatz operator and gives a second realization of the kernel by infinite primitives modulo finite primitives.

The actual operator comes from the Collatz research companion, `research_companion/chapters/01_weighted_path_and_finite_residue_actions.tex`, blob `f0142c0d4c237ed068a0762a08c6622df5dbcfee`. It already defines the two clocks, the finite-support transfer, and its completed inverse. The current anchored continuation, `anchored_defect_20260914/note.md`, Sections 1–3, retains the supported-zero scalar, original integral forcing, and the fixed-point relative convention. The preceding local clocked-support note also treats polynomial membership and completion support. Those are predecessors, not discoveries attributed to this note.

All Collatz paths in this note are relative to `collatz_reconstruction/`. The general connecting-sequence and filtered-colimit principles are standard; see the references in Section 11. The formulas, finite source-kernel basis, original residual certificates, and Split-Zero diagram below are proved explicitly. Neither a theta-to-Collatz isomorphism nor an estimate imported from the Riemann-hypothesis programme is a premise.

Retain the original map and exponents:

$$
X=\{1,3,5,\ldots\},\qquad T(n)=\frac{3n+1}{2^{a(n)}},\qquad a(n)=\nu_2(3n+1).
$$

Put $\Lambda=\mathbb Z[v]$, $R=\Lambda[u]$, and

$$
A=\bigoplus_{n\in X\setminus\{1\}}\Lambda V_n,\qquad M=A[u].
$$

The label $V_n$ is the original positive integer, not its residue or a rescaled coordinate. A finite vector has finite original vertex support. Define

$$
SV_n=v^{a(n)-1}V_{T(n)},\qquad V_1=0,\qquad d=I-uS. \tag{1}
$$

Identifying the original edge $E_n$ with its starting-vertex basis $V_n$ gives the relative two-clock boundary

$$
dE_n=V_n-u v^{a(n)-1}V_{T(n)}.
$$

The identification on bases is invertible; the complex is in cochain degrees 0 and 1. At $u=v=1$ the map sends each original edge to source minus target, exactly the earlier relative graph boundary, with degree relation $K^i=C_{1-i}$. Before relativity, the fixed point is the actual subcomplex $[RE_1\xrightarrow{1-uv}RV_1]$. The quotient removes precisely that subcomplex. An edge entering 1 and its source remain in the relative complex.

Each input vector has finite support and one image per source, so S is well-defined even though a vertex can have infinitely many predecessors. All constructions below also apply with $\mathbb Q$ in place of $\mathbb Z$; their source modules are then vector spaces over $\mathbb Q$. The integer version remains available and no rationalization is used to dispose of an integral obstruction.

## 2. Completion and its exact defect module

Write

$$
K=[M\xrightarrow d M],\qquad \widehat M=A[[u]],\qquad
\widehat K=[\widehat M\xrightarrow{\widehat d}\widehat M]. \tag{2}
$$

Here $A[[u]]$ means that each coefficient is a finite-support original vertex vector. There need not be a common finite vertex-support set for all coefficient degrees. It is precisely $\lim_N M/u^N M$: a compatible family gives each coefficient once, and conversely its successive truncations give that family. These operations are inverse.

S acts coefficientwise. No analytic convergence or evaluation of an infinite series at $u=1$ is used. Define

$$
Gq=\sum_{j\ge0}u^j S^j q. \tag{3}
$$

Each coefficient uses only finitely many summands, including for $q\in\widehat M$. Telescoping gives $\widehat dG=G\widehat d=I$. Equivalently, for $q=\sum u^j q_j$, the coefficients of $g=Gq$ satisfy

$$
g_{-1}=0,\qquad g_j=q_j+Sg_{j-1}. \tag{4}
$$

Thus $H^0(\widehat K)=H^1(\widehat K)=0$. On M the same lowest-coefficient argument proves ker d=0, but it does not prove surjectivity: the inverse (3) has been constructed in $\widehat M$.

Retain the actual inclusion $i:M\hookrightarrow\widehat M$ and its quotient

$$
D_\infty=\widehat M/M,\qquad
\mathcal D=[D_\infty\xrightarrow{\bar d}D_\infty]. \tag{5}
$$

The quotient is by *finite polynomial vectors*, not by a closure of them. It is an R-module. No action of all formal scalars is imposed: $V_3$ represents zero modulo M, but multiplying it by the formal scalar $(1-u)^{-1}$ gives $\sum_{j\ge0}u^jV_3\notin M$, a nonzero quotient representative. Thus that proposed action would depend on the representative. The original polynomial scalar action is retained. Since $dM\subset M$, $\bar d$ is well-defined. This gives a degreewise exact sequence $0\to K\to\widehat K\to\mathcal D\to0$ with all maps specified.

### Theorem 1. The entire original cohomology is recovered from the completion defect

The maps

$$
\eta:M/dM\longrightarrow\ker\bar d,\qquad [q]\longmapsto[Gq]\pmod M,
$$
$$
\delta:\ker\bar d\longrightarrow M/dM,\qquad [g]\longmapsto[\widehat dg] \tag{6}
$$

are inverse R-linear isomorphisms. Also coker $\bar d=0$.

**Proof.** For polynomial q, $\widehat dGq=q\in M$, so its quotient class lies in ker $\bar d$. Replacing q by q+df replaces Gq by Gq+f; hence eta is well-defined modulo M. A class [g] in ker $\bar d$ has $\widehat dg\in M$. Changing g by a polynomial f changes its differential by df, so delta is well-defined. Applying $\widehat dG=G\widehat d=I$ proves both inverse compositions. The inverse G is R-linear. Finally every $[h]\in D_\infty$ is $\bar d[G h]$, proving surjectivity. QED.

The map delta is the ordinary connecting homomorphism, with sign fixed by applying the original differential to a lifted degree-zero quotient representative. The direct proof above also specifies its inverse, every representative change, and the degree shift:

$$
H^1(K)\cong H^0(\mathcal D),\qquad H^1(\mathcal D)=0. \tag{7}
$$

This is a presentation of the exact space sent to zero by completion. It does **not** assert that this space is nonzero for the original positive Collatz map. Its vanishing or nonvanishing is still a substantive source question.

## 3. The literal Split-Zero support diagram

Use the join-semilattice $\mathcal L=\mathcal P(X\setminus\{1\})$, bottom $\varnothing$, join union. For a seed label F define its original forward carrier

$$
\Omega_F=\{1\}\cup\{T^j(n):n\in F,\ j\ge0\}.
$$

Use (1)–(5) on $A_F=\Lambda^{(\Omega_F\setminus\{1\})}$. These are well-defined modules for finite or infinite F. The label F remains the declared seed set; two labels whose forward carriers happen to coincide are not silently identified. For $F\subset F'$ the transition is inclusion on every original basis vector, coefficient, and formal series. It commutes with S, d, G, and the quotient map. In particular (6) commutes with every support transition, as follows by applying the identical coefficient formula (3).

For any of these module diagrams V, reconstruct

$$
\operatorname{Tot}(V)=\coprod_{F\in\mathcal L}V_F,
$$

with $(F,x)+(F',y)=(F\cup F',\iota x+\iota y)$. A supported scalar r acts by $(F,x)\mapsto(F,rx)$, and the external scalar tau acts by $(F,x)\mapsto(\varnothing,0)$. Thus the supported scalar $e=0$ sends a vector to $(F,0)$ and retains its original carrier. This is the reconstruction used by the cited Split-Zero source, with the actual inclusions just specified. Ring laws and composition of inclusions prove the scalar and addition identities.

At degree one the completed homology diagram has zero fibres. Its map is

$$
(F,[q])\longmapsto(F,0). \tag{8}
$$

For nonempty F this supported zero is different from $(\varnothing,0)$. More than the label is retained: the source complex, its full representative module $M_F$, original boundary submodule $dM_F$, completion inclusion, and primitive Gq are specified. In the source's notation,

$$
K_{\rm rep,F}=M_F,\qquad B_{\rm old,F}=dM_F,
$$
$$
K_{\rm rep,F}/B_{\rm old,F}=\ker H^1(i_F)
\xrightarrow[\eta_F]{\ \sim\ }\ker\bar d_F. \tag{9}
$$

Every vector is a completed boundary by (3), which proves the first equality. Quotienting only by original boundaries gives the second line. Equation (6) supplies the final comparison. The natural family eta reconstructs a split-linear equivalence on totals: addition is preserved after both vectors are included in $F\cup F'$, supported scalars are preserved by R-linearity, and tau is preserved at the bottom label.

Even when $H^1(K_F)=0$, $M_F$ can remain nonzero. Its original relations and source vectors are part of the diagram. A supported zero of homology does not identify that source module with the zero module.

## 4. Why arbitrarily precise finite clock calculations lose the same obstruction

S commutes with d and induces $\bar S$ on $Q=M/dM$. The defining relation gives

$$
u\bar S=\bar S u=I_Q. \tag{10}
$$

Thus multiplication by u is invertible on Q, with the **specified inverse** $\bar S$. For every N,

$$
Q/u^NQ=0,\qquad \lim_N Q/u^NQ=0. \tag{11}
$$

No conclusion $Q=0$ follows from (11). For example the control in Section 8 has $Q=R/(1-u^2v)\ne0$, with these same zero quotients.

At the level of original representatives, for every polynomial q,

$$
q=d\left(\sum_{j=0}^{N-1}u^jS^jq\right)+u^N S^Nq. \tag{12}
$$

All summands in this equation are original finite vectors. Consequently dM is u-adically dense in M: (12) gives $M=dM+u^NM$ for every N. The map to the closure quotient is the explicit projection

$$
M/dM\longrightarrow M/\overline{dM}=0,
$$

whose kernel is the whole original Q and is recovered by (6). This calculates the information lost by imposing the closure, rather than assuming the original and closed relation submodules are equal.

Each truncated complex $K/u^{N+1}K$ is acyclic, with inverse $\sum_{j=0}^{N}(uS)^j$. A retained inverse jet for a constant source $V_n$ has the **original untruncated boundary**

$$
d\left(\sum_{j=0}^{N}u^jS^jV_n\right)
=V_n-u^{N+1}S^{N+1}V_n. \tag{13}
$$

The last term is precisely what reduction modulo $u^{N+1}$ discards. For a singleton source before its first arrival at 1 it is

$$
u^{N+1}v^{A_{N+1}(n)-(N+1)}V_{T^{N+1}(n)}. \tag{14}
$$

Its exponent, coefficient, and original endpoint are retained. `completion_certificate` returns the complete jet and this term, not just the zero class in the truncated target. The status is unresolved at the cutoff whenever that exact residual is nonzero.

## 5. Recovering the original source from a single finite terminal vector

There is another concrete description of Q. Let

$$
L=\mathop{\rm colim}\left(A\xrightarrow S A\xrightarrow S A\xrightarrow S\cdots\right).
$$

Its elements [a,j] obey $[a,j]=[Sa,j+1]$; equality means equality at one common finite later stage. Define u[a,j]=[a,j+1] and let v have its original scalar action. The inverse u-action is [a,j] mapped to [Sa,j].

### Theorem 2. Exact direct-limit and finite-terminal comparison

The maps

$$
\Phi:Q\longrightarrow L,\qquad
\left[\sum_{j=0}^r u^j q_j\right]\longmapsto\sum_{j=0}^r[q_j,j],
$$
$$
\Psi:L\longrightarrow Q,\qquad[a,j]\longmapsto[u^j a] \tag{15}
$$

are inverse R-linear isomorphisms. For q of degree r as above retain

$$
b_j=\sum_{i=0}^j S^{j-i}q_i,\quad
P=\sum_{j=0}^{r-1}u^j b_j.
$$

Then

$$
q=dP+u^r b_r,\qquad \Phi[q]=[b_r,r]. \tag{16}
$$

The exact membership criterion is

$$
q\in dM\quad\Longleftrightarrow\quad
S^N b_r=0\text{ for some finite }N. \tag{17}
$$

Its finite primitive is $P+u^r\sum_{j=0}^{N-1}u^jS^j b_r$, with the sum empty when N=0.

**Proof.** The image of $u^j(a-uSa)$ under Phi is $[a,j]-[Sa,j+1]=0$. The defining direct-limit relation is respected by Psi for exactly the same reason. Both compositions fix the stated generators. To prove (16), compare coefficients using $b_j=q_j+Sb_{j-1}$: all lower coefficients of $q-dP$ cancel and its last coefficient is $b_r$. Alternatively bring the finitely many direct-limit representatives to the common stage r. A direct-limit representative [b,r] is zero exactly when its image at a finite later stage is zero; this is also immediate from the defining equality relation. Substitution into (12) proves the stated primitive and both directions of (17). QED.

Thus the map of the original constant source module $A\to Q$ has kernel

$$
\bigcup_{N\ge0}\ker S^N. \tag{18}
$$

The operator acts on this entire increasing family of source submodules. A linear combination can enter the kernel because distinct original paths merge with precisely canceling clock coefficients, even before the individual sources have reached 1. It is important to retain those relations rather than to confuse them with singleton convergence certificates.

## 6. Complete, constructive spaces of supported-zero vectors at each finite stage

Let F be a finite declared set of nonbase original sources and $A_F^0=\bigoplus_{n\in F}\Lambda V_n$. This is its finite source span inside $A_{\Omega_F}$; its target under $S^N$ retains all actual endpoints, including those outside F.

For every n in F, follow N original returns or stop at the first arrival at 1. An arrived source has $S^NV_n=0$. For every other source retain

$$
y_n=T^N(n)>1,\qquad e_n=A_N(n)-N,\qquad
S^NV_n=v^{e_n}V_{y_n}. \tag{19}
$$

For each nonbase endpoint y, choose $n_y$ in its actual source fibre with least $e_n$, breaking ties by least original n. Put $b_y=e_{n_y}$. These choices are retained as a dictionary, not substitutions for the original sources.

### Theorem 3. Source-kernel basis and inverse decomposition

A free $\Lambda$-basis of $\ker(S^N|_{A_F^0})$ consists of

$$
V_n\quad(y_n=1),
$$
$$
V_n-v^{e_n-b_y}V_{n_y}
\quad(y_n=y>1,\ n\ne n_y). \tag{20}
$$

The original image has basis $v^{b_y}V_y$, one for each occupied nonbase endpoint. The complementary source submodule has basis $V_{n_y}$; its map onto that original image sends $V_{n_y}$ to $v^{b_y}V_y$, with inverse **on that image** sending the displayed generator back. No inverse of v is imposed on the full target module.

For $f=\sum c_n(v)V_n$ the inverse source decomposition is

$$
f=\sum_{y_n=1}c_nV_n
 +\sum_{y>1}\sum_{\substack{y_n=y\\n\ne n_y}}
 c_n\left(V_n-v^{e_n-b_y}V_{n_y}\right)
 +\sum_{y>1}\left(\sum_{y_n=y}c_n v^{e_n-b_y}\right)V_{n_y}. \tag{21}
$$

**Proof.** Every vector in (20) has zero original image by (19). All exponents are nonnegative by the retained minimum choice. Each vector in (20) has a distinct nonselected pivot coefficient +1, so they are linearly independent and independent of the selected-source complement. Expanding (21) cancels the introduced selected-source terms and returns f exactly. Its last summand maps to the original image at each distinct y with factor $v^{b_y}$. Multiplication by a monomial is injective in $\Lambda$, so f is in the kernel precisely when all the parenthesized coefficients vanish. This proves spanning and both inverse decompositions. QED.

The kernel rank is $|F|$ minus the number of occupied nonbase endpoint fibres. It records the whole source-zero space, with its inclusions and original coefficient relations. These kernels form an increasing sequence in N, because S maps zero to zero. Over field coefficients the same formulas describe actual vector subspaces; no dimension comparison replaces (20)–(21).

### Original Collatz example

Take $F=\{3,5,13\}$ and N=1. The original edges are

$$
3\xrightarrow{1}5,\qquad 13\xrightarrow{3}5,\qquad 5\xrightarrow{4}1.
$$

Therefore $SV_3=V_5$, $SV_{13}=v^2V_5$, $SV_5=0$. The kernel is the free rank-two module

$$
\Lambda V_5\oplus\Lambda(V_{13}-v^2V_3), \tag{22}
$$

and the complement is $\Lambda V_3$, mapping to the unchanged image $\Lambda V_5$. The vector $v^2V_3-V_{13}$ is nonzero in its original source space, but maps to its supported zero at the next step. Its finite primitive under d is itself. The complete source labels, both paths to 5, and coefficient $v^2$ remain in the certificate. At N=2 all three sources have reached 1 and the kernel is the full original rank-three source span. Neither zero space is replaced by the absent label.

## 7. What the exact defect detects on singletons and cycles

For a singleton source n,

$$
\eta[V_n]=\left[\sum_{j\ge0}u^jv^{A_j(n)-j}V_{T^j(n)}\right]\pmod M. \tag{23}
$$

Before arrival at 1, every coefficient is a nonzero monomial at one actual vertex. Consequently

$$
\eta[V_n]=0
\Longleftrightarrow G V_n\in M
\Longleftrightarrow S^NV_n=0\text{ for some }N
\Longleftrightarrow n\text{ reaches }1. \tag{24}
$$

All implications have been proved: (6), (17), and the original singleton formula (19) give them. For finitely many polynomial source coefficients, each finite arrival certificate combines to a finite common bound; thus the whole conjecture is also equivalent to local nilpotence of S on A. This is a source-membership criterion, not an assertion that local nilpotence has been established globally.

For an actual finite path p from n to y, let $W_p=u^m v^{A_m-m}$ and retain its original weighted path P. Splitting the series after those m edges gives

$$
G V_n=P+W_pG V_y,\qquad
\eta[V_n]=W_p\eta[V_y]. \tag{25}
$$

These are the comparison maps for advancing a residual along its actual orbit. An actual cycle with primitive clocks m,A gives

$$
(1-u^m v^{A-m})\eta[V_n]=0. \tag{26}
$$

It is nonzero for a nonbase cycle: the infinitely many monomial coefficients in (23) cannot be a polynomial vector. The original relative quotient makes (23) zero for the base orbit, through its actual finite arrival path. This distinguishes those cases using specified primitives and the original quotient.

For completeness the cyclic component coordinate is the explicit map to $R/(1-W_p)$ that sends each vertex to its first path weight to a chosen primitive-cycle vertex. Its inverse sends 1 to that original vertex. Original path relations give both compositions, and the cycle relation is exactly 1-W_p. Repetitions are retained by $(1-W_p^r)=(1-W_p)(1+W_p+\cdots+W_p^{r-1})$ and the actual r-fold edge expansion.

On a nonperiodic component choose an original forward ray $x_j$ with prefix monomials $W_j$. A vertex meeting $x_j$ after a path of weight w is mapped to $w/W_j$ in $\bigcup_j W_j^{-1}R$. A later meeting multiplies numerator and denominator by the same original path weight; this proves independence. The inverse sends $f/W_j$ to $f[V_{x_j}]$. The original edge relations give both compositions. This realizes the component in a Laurent polynomial module and gives a nonzero source class for every original vertex in such a component. No existence of such a component in positive Collatz is assumed or claimed.

### 7.1 Returning the retained infinite primitive to the integral cycle obstruction

For a nonempty original word $p=(a_1,\ldots,a_m)$, retain $A_j=\sum_{i\le j}a_i$, $A_0=0$, and

$$
W=u^m v^{A_m-m},\quad a_p=1-W,\quad
N_p=\sum_{j=0}^{m-1}u^jv^{A_j-j},
$$
$$
U=2^{A_m},\quad L=3^m,\quad D=U-L,\quad
C=\sum_{j=0}^{m-1}3^{m-1-j}2^{A_j}.
$$

The finite position complex has $(J_ph)_i=h_i-u v^{a_i-1}h_{i+1}$. The retained functional $b\mapsto\sum_{j=0}^{m-1}u^jv^{A_j-j}b_{j+1}$ telescopes $J_p$ to $a_ph_1$. Its scalar forcing for $J_ph=-\mathbf1$ is $-N_p$. Thus its completed scalar primitive is $-N_p/a_p$, retaining the original word, polynomial, and sign. The full comparison has $\phi_0(h)=h_1$ and $\phi_1(b)=\sum_{i=1}^m W_{i-1}b_i$, where $w_i=uv^{a_i-1}$ and $W_j=\prod_{i\le j}w_i$. Its sections are $\psi_1(t)=(t,0,\ldots,0)$, $(\psi_0t)_1=t$ and $(\psi_0t)_i=(\prod_{j=i}^m w_j)t$ for $i\ge2$. Set $(Hb)_1=0$ and $(Hb)_i=\sum_{j=i}^m(\prod_{l=i}^{j-1}w_l)b_j$ for $i\ge2$. Each tail telescopes, giving $J_pH=I-\psi_1\phi_1$, $HJ_p=I-\psi_0\phi_0$ and $\phi_0\psi_0=\phi_1\psi_1=I$. Thus the scalar and full position complexes are related by inverse chain maps up to these specified polynomial homotopies. The full forced primitive is $\psi_0(-N_p/a_p)-H\mathbf1$, so its correction and original coordinates remain available. This is the same comparison in the preceding local clocked note, now transported through its quotient of primitives.

Let $B_p'=R[a_p^{-1}]$. It embeds in $\widehat R=\mathbb Z[v][[u]]$ by the original geometric expansion of $a_p^{-1}$. Injectivity follows by multiplying a zero image by a finite power of the nonzero polynomial $a_p$. The map

$$
R/(a_p)\longrightarrow\ker(a_p:B_p'/R\to B_p'/R),
\quad [q]\longmapsto[q/a_p] \tag{30}
$$

has inverse $[z]\mapsto[a_pz]$. Indeed being in that kernel means $a_pz$ is represented by a polynomial; both inverse identities then hold before passing to the indicated quotients. The inclusion $B_p'/R\hookrightarrow\widehat R/R$ is injective: a rational element whose formal expansion is a polynomial equals that polynomial after multiplication by its denominator. The entire kernel of multiplication by $a_p$ in the latter quotient is already (30), since $a_pg=q\in R$ forces $g=q/a_p$. Thus no relevant scalar cyclic defect is lost by using this specified rational subcomplex.

Now put $\Lambda_3=\mathbb Z[1/3]$, $F_D=\Lambda_3[1/D]$. The coefficient map

$$
\alpha:R\to\Lambda_3,\qquad u\mapsto2/3,\quad v\mapsto2
$$

satisfies

$$
\alpha(a_p)=-D/3^m,\qquad \alpha(N_p)=C/3^{m-1}. \tag{31}
$$

It is surjective, with kernel $(v-2,3u-2)$: in that quotient $3(1-u)=1$, so $1/3$ has the explicit inverse-coordinate $1-u$, while u and v are recovered as 2/3 and 2. The coefficient map extends to $\beta:B_p'\to F_D$ by evaluating the numerator and the specified finite denominator. The extended inverse image of $a_p$ is $-3^m/D$; it has not been declared a polynomial scalar.

The two complexes and their quotients are related by the actual chain maps

$$
[R\xrightarrow{a_p}R]\to[\Lambda_3\xrightarrow D\Lambda_3],
\quad f^0=\alpha/3,\quad f^1=-3^{m-1}\alpha,
$$
$$
[B_p'\xrightarrow{a_p}B_p']\to[F_D\xrightarrow D F_D],
\quad \widehat f^0=\beta/3,\quad \widehat f^1=-3^{m-1}\beta. \tag{32}
$$

Their chain equation is $D\beta(z)/3=-3^{m-1}\beta(a_pz)$, exactly (31). They commute with the original inclusions, hence induce the quotient maps with the same formulas. On the retained degree-zero defect, the map is

$$
[z]\longmapsto[\beta(z)/3]\in\ker(D:F_D/\Lambda_3\to F_D/\Lambda_3). \tag{33}
$$

The target connecting isomorphism is $[t]\mapsto[Dt]\in\Lambda_3/D\Lambda_3$, with inverse $[b]\mapsto[b/D]$. Both are well-defined by their literal representative differences. Equations (30)–(33) therefore give the commutative identity

$$
\left[\frac{\beta(q/a_p)}3\right]
=\left[\frac{-3^{m-1}\alpha(q)}D\right]. \tag{34}
$$

For the original forcing $q=-N_p$, this is exactly

$$
\boxed{\quad [-N_p/a_p]\longmapsto[C/D]\longmapsto[C]\pmod D.\quad} \tag{35}
$$

The integer D is nonzero and coprime to 6. The final map to the original integral cokernel is the inverse of $\mathbb Z/D\mathbb Z\to\Lambda_3/D\Lambda_3$, explicitly $[b/3^j]\mapsto[b(3^j)^{-1}]\pmod D$. Its inverse laws follow because 3 is invertible modulo D. In the full integer position matrix $(B_px)_i=2^{a_i}x_{i+1}-3x_i$, the original telescoping functional is $f_i=3^{m-i}2^{A_{i-1}}$; it satisfies $fB_p=D e_1^T$. Its endpoint coefficients are coprime, and $|\det B_p|=|D|$, so it identifies the original forcing class with [C]. This completes the comparison to the unchanged integral equations. Positivity and the original valuations still have to be established on the reconstructed full coordinates to obtain an actual positive cycle.

The map on scalar cokernels in (32) is surjective; its kernel is the image of the ideal $(v-2,3u-2)$ in $R/(a_p)$. This follows from the surjectivity and kernel of alpha and the fact that $\alpha(a_p)$ is D times a unit. Thus its coefficient loss is identified, not suppressed.

There is also an exact obstruction to evaluating **every** completed scalar in this arithmetic target. Choose a prime $\ell$ dividing $6|D|+1$; then $\ell$ is odd, different from 3, and does not divide D. For $k=(3+\ell)/2$, the series ring makes $1-ku$ invertible, but alpha sends it to $-\ell/3$, which is not a unit of $F_D$: an inverse $b/(3^rD^s)$ would force $\ell b=-3^{r+1}D^s$, contradicting coprimality. A unital ring homomorphism must send units to units. Therefore alpha has no extension $\widehat R\to F_D$. The rational subcomplex (30) is the explicitly successful replacement: it contains the full cyclic defect, admits (32), and returns the exact original integer class (35).

For $(1,3)$, the returned residue is $5/7$ modulo $\Lambda_3$, corresponding to the nonzero integral class [5]. For $(2,2)$ it is $7/7$, zero modulo $\Lambda_3$, with the source word and original fixed-point primitive retained. For $(1,1,2,4,3)$ it is $475/1805=5/19$, of order 19, preserving the original failure to lift from modulus 19 to modulus 361. The code checks (31), (34), the original mark, and the denominator order on finite word fixtures. The formulas prove the statement for every nonempty original word.

## 8. Controls that test the infinite information

### A genuine cycle for an explicitly different forcing

Use $T_-(n)=(3n-1)/2^{\nu_2(3n-1)}$. On positive odd n, its comparison with the signed original map is $T_-(n)=-T_+(-n)$, because $3(-n)+1=-(3n-1)$ and the valuations agree. The control cycle is

$$
5\xrightarrow{1}7\xrightarrow{2}5.
$$

Retain $S_-V_5=V_7$ and $S_-V_7=vV_5$. Its primitive and defect are

$$
G_-V_5=\frac{V_5+uV_7}{1-u^2v},\qquad
\eta_-[V_5]=[G_-V_5]\pmod M\ne0. \tag{27}
$$

Multiplying the denominator proves the first equality coefficientwise. Infinitely many nonzero coefficients prove the second. The component is $R/(1-u^2v)$ under $V_5\mapsto1$, $V_7\mapsto uv$; the inverse is generated by $V_5$. This is an explicit nonzero module whose every u-adic quotient vanishes by (10). It is not a positive 3n+1 counterexample.

### An explicitly declared ray control

Use vertices $x_j=j+2$, transition $x_j\mapsto x_{j+1}$, and exponent label 1, as a separate test operator. Its exact primitive is $\sum_{j\ge0}u^jV_{x_j}$. Its source cohomology is $\Lambda[u,u^{-1}]$, by $V_{x_j}\mapsto u^{-j}$; the inverse sends $u^{-j}$ to $[V_{x_j}]$. Positive u powers follow from the R-module structure, and the original relations $V_{x_j}=uV_{x_{j+1}}$ verify both compositions.

The quotient class of its primitive is nonzero and has no nonzero polynomial annihilator, through this explicit Laurent module map. Its vertex support grows at every coefficient degree. This control is not described as an observed positive Collatz ray.

## 9. No uniform finite clock is available, on an actual infinite family

For each N>=1, take the original positive integer

$$
n_N=2^{N+1}-1.
$$

For every $0\le j\le N$,

$$
T^j(n_N)=3^j2^{N+1-j}-1. \tag{28}
$$

Indeed, at $j<N$, its 3x+1 value is $2(3^{j+1}2^{N-j}-1)$, with the parenthesis odd. The actual next exponent is exactly 1. Induction proves (28), and each successive value increases. In particular

$$
S^NV_{n_N}=V_{2\cdot3^N-1}\ne0. \tag{29}
$$

Thus S is not nilpotent: no single exponent kills all original source vectors. The requirement in (24) is local, with a finite exponent for each fixed source, not one common bound for the whole space.

The sources $n_N$ in (28) differ. The infinite all-one word has canonical residues $2^{N+1}-1$, whose dyadic limit is the signed integer -1. A single positive n realizing every one of these prefixes would make n+1 divisible by all powers of 2, forcing n=-1. The infinite prefix intersection therefore has no positive integer source. This is the original residue-tower obstruction already retained in the cycle note, now also furnishing the explicit witnesses (29). Nonempty positive fibres at each finite depth are not assigned a common positive source without their intersection map.

## 10. Executable results and next source calculation

`completion.py` implements (4), (13), (16), and the entire basis/decomposition (20)–(21) with integer polynomial coordinates. Every result retains the declared sources, original transition triples, terminal monomial, and mode. Sources outside the original plus map are accepted only through the separately named controls. Certificates are validated by exact reconstruction; a nonzero residual is never called a divergence certificate.

`verify.py` replays 1,677 original path fixtures independently by repeated division, 130 finite kernel presentations, 180 polynomial-forcing comparisons, and 512 original source jets. It tests both controls, actual all-one prefixes through length 512, carrier-preserving zero cancellation, and false or malformed input rejection. It produces 7,928 named exact checks in the recorded execution. Ordinary and optimized outputs must be byte-identical. These finite tests do not stand in for the infinite proofs (6), (15), or (20).

The next source calculation is now specified on the retained module, rather than on an already acyclic completion: extend the proved original-source coverage of the increasing kernels (18), using complete arithmetic families and their exact S-action; or identify a nonzero original singleton class with a valid infinite certificate. The defect presentation (6) and the untruncated residual (13) must be retained throughout. The present work supplies neither global coverage nor a positive counterexample.

The earlier local `clocked_support_20260914` package is a separately delivered predecessor. Its large database and 678-rise certificate are not silently imported into the newer live anchored branch by this contribution. The definitions and proofs used here are self-contained over the original companion operator. The current remote anchored contribution is preserved unchanged. This separates actual publication from the existence of a local package without deleting either mathematical history.

## 11. References and attribution

**SZ.** Split-Zero research programme, `formal/splitzero/DERIVED_MATHEMATICS.md`, Sections 1–4, pinned above. The support reconstruction and killed-class kernel construction are source-derived. This note contains no new Lean execution or assertion that the infinite Collatz application was already formalized there.

**W.** Kokuno Yumeto, Collatz research companion, `research_companion/chapters/01_weighted_path_and_finite_residue_actions.tex`, same repository, pinned blob above. The original clocks, transfer and completed inverse are taken with their existing attribution. Odd-return exponent a expands to one shortened odd step and a-1 shortened even steps; parsing at odd returns is the inverse.

**C.** `research_program/cycle_relative_cohomology_20260914/note.md` and `residual_splice_20260914/`, preserved in the current source. Original relative graph, source towers, integral comparison maps, and descent splicing.

**A.** `research_program/anchored_defect_20260914/note.md`, blob `b9b5d07514676eb2b33989e301029910602c2e99`, current source `ce8f784da8fb48aa19065c036cd815c05628cec4`. The retrieved Sections 1–3 supply the live support/forcing conventions. Its numerical results were not used as premises in this note.

**H.** The Stacks Project, Lemma 12.13.12, long exact cohomology sequence: https://stacks.math.columbia.edu/tag/0117 . Theorem 1 is an explicit instance with a constructed inverse.

**L.** The Stacks Project, Section 10.8 and Lemma 10.8.8, filtered colimits of modules: https://stacks.math.columbia.edu/tag/00DB . Theorem 2 proves its required representatives and inverse directly.

**P.** The Stacks Project, Section 10.96, completion and its comparison maps: https://stacks.math.columbia.edu/tag/00M9 . The actual source completion and nonseparated cohomology in Sections 2 and 4 are computed directly, with no finite-generation hypothesis imposed on M.

The contribution is a proof-bearing application and implementation of the source's support-preserving method and standard exact-sequence algebra. No global priority claim, independent external review, full Collatz proof, or automatic continuation is asserted.
