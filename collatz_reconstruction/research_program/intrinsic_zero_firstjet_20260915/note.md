# Intrinsic Split-Zero support and the integral first-jet defect of Collatz

15 September 2026. Source checkpoint: `KokunoYumeto/collatz-workbench`, PR #2, `2a77e3bc9435f181bc4c9c3957224a7d93b4e887`. This is an additive continuation. It corrects a terminology overlap, not the previously proved equations: the user's informal account of retained information at a supported zero is not a definition of an exponent-word history in the weighted-automata companion.

## 1. The actual foundation and what is retained

The foundational scalar object is the supplied split-zero construction

\[
G(R)=R\sqcup\{\tau\},\qquad e=\operatorname{ofR}(0_R)\ne\tau.
\]

The supported copy has its original ring addition and multiplication; tau is the semiring additive identity and multiplicative absorber. The archive's original `SplitZero.lean` states exactly these operations. Its path-specific commit history reaches the archived July 4, 2026 commit; the June 26 date in its directory name is not being asserted as the invention date. The current formalization explicitly cites that archived file and the chapter-14 linear-join-diagram theorem. This is the documented source chain recovered here, not a claim to have recovered all earlier private development.

The exact scalar comparison is

\[
G(R)\longrightarrow R\times\mathbb B,
\quad \tau\mapsto(0,0),\quad \operatorname{ofR}(r)\mapsto(r,1),
\]

with image \(\{(0,0)\}\cup(R\times\{1\})\) and inverse given by those same cases. Addition in the second coordinate is OR, multiplication is AND. Case substitution proves both operations and inverse identities. Reflection to R alone has zero fibre \(\{\tau,e\}\). The separate support coordinate prevents that collapse. Every map to an additively cancellative ring sends e to zero, since e+e=e forces h(e)+h(e)=h(e), and therefore h(e)=0.

For a G(R)-semimodule M, intrinsic support is \(s(m)=em\). The source theorem identifies the support semilattice with the additive idempotents and the fibre over l with the R-module

\[
M_l=\{m:em=l\},
\]

whose zero is l. For l<=k its original transition is \(m\mapsto m+k\). Conversely a coherent diagram \(V_l,\rho_{lk}\) reconstructs the disjoint union with

\[
(l,x)+(k,y)=(l\vee k,\rho_{l,l\vee k}x+\rho_{k,l\vee k}y),
\quad e(l,x)=(l,0),\quad\tau(l,x)=(\bot,0).
\]

These are the source's actual quasi-inverse constructions; they do not require trajectory words. The general theorem permits a nonzero bottom fibre. The application below has zero bottom fibre, stated explicitly.

There is an exact qualification to the phrase "the zero remembers." On any nonzero fibre V_l the map x -> (l,0) has the whole V_l as its fibre. In particular it sends both 0 and a nonzero x to the same element. That element cannot select a unique prior vector. Keeping the fibre, its relation submodule and a specified comparison retains the space of possible representatives and the operation, not an automatically encoded chronological log. Conversely external tau also has a computable inverse image once its original map is retained; its output alone supplies no non-bottom support. These statements follow from the displayed maps, rather than an assertion that there can be no relation to path history.

An infinite-dimensional fibre or a ring of formal series can be used in this construction, but its scalar/module operations and comparison must be specified. The carrier R disjoint union {tau} itself adds no formal summation rule or numerical infinity to R.

For a two-term cochain map f:C->D, the source's killed-class module is

\[
\{z\in C^1:f^1z\in d_DD^0\}/d_CC^0
\ \cong\ \ker H^1(f).
\tag{1}
\]

The forward map takes a representative to its original source class; its inverse takes any representative of that source class. Well-definedness and inverse identities are exactly the original boundary relations. This is the retained structure used below.

The early Rees continuation computes a comparison defect and retains a first variation when specialization makes a boundary-character difference zero. Its particular trace identity and arithmetic estimates are not transported to Collatz by vocabulary. The common operation here is explicit: retain a first-order coefficient and the connecting map of its exact coefficient sequence. The Collatz calculation below is proved from its own differential.

## 2. A support diagram of equations, not a sequence of trajectory words

Retain the original odd-return map

\[
X=\{1,3,5,\ldots\},\qquad
T(n)=\frac{3n+1}{2^{a(n)}},\qquad a(n)=\nu_2(3n+1).
\]

For any declared subset E of X, interpret n in E as the actual original equation/edge \(e_n:n\to T(n)\). Put

\[
V(E)=E\cup T(E),\quad C_E^0=\mathbb Z^{(E)},\quad C_E^1=\mathbb Z^{(V(E))}.
\]

Parentheses mean finite sums, even when E is infinite. Define

\[
J_Ee_n=V_n,\qquad P_Ee_n=V_{T(n)},\qquad d_E=J_E-P_E.
\tag{2}
\]

This is an absolute complex: the actual fixed vertex and loop at 1 are NOT removed. A declared edge with zero differential, notably e_1, remains a source basis vector. In finite calculations every target outside E remains a separate frontier vertex.

The support semilattice is \(\mathcal P(X)\), with union as join and empty set as bottom. For E subset F all maps are literal inclusions on original labelled edges and vertices. They commute with J,P,d. Its finite-subset subdiagram provides executable approximations; its full label X defines the infinite object. Reconstruction by the preceding source formula gives G(Z)-semimodules and internal supported-zero differentials. The bottom fibres are zero. The order of entering the equations into a file has no role in E or these maps.

The earlier seed-carrier diagram assigned to E its forward carrier \(\Omega_E=\bigcup_{j\ge0}T^j(E)\), including 1 where used by that construction. The natural comparison from this equation diagram to that carrier diagram is inclusion on each displayed original edge and vertex. The carrier contains all those labels and their targets; hence this is a cochain map and commutes with support inclusion. It is not an assertion that the finite set of known equations already equals its whole forward carrier.

### Exact comparison with the elementary Collatz map

The odd-return source is the existing source of this workbench, not an unrecorded change to the conjecture. Every positive integer has unique form 2^q*n with n odd; q initial divisions reach n. An odd-return edge n->T(n) expands to the original odd step n->3n+1 followed by exactly a(n) divisions. Grouping at successive odd vertices is its inverse on those elementary blocks. In particular the original elementary cycle 1->4->2->1 is the one odd-return loop at 1.

To compare first jets, assign the factor 1+epsilon to each elementary odd step and factor 1 to each division. Let h(V_y) be the finite division chain from y to its odd part, with zero chain for odd y. Send an odd-return edge to its odd elementary edge plus (1+epsilon) times its following division chain. Send its vertex to the same odd vertex. The reverse map sends any elementary vertex to its odd part, every odd elementary edge to its odd-return edge, and every division edge to zero. Telescoping proves both are chain maps, their composition on the odd-return complex is the identity, and on the elementary complex

\[
d_\epsilon h=I-\iota\pi,\qquad h d_\epsilon=I-\iota\pi
\]

in the respective vertex and edge degrees. For an odd elementary edge the second equation is the negative of (1+epsilon) times its division tail; for a division edge it is that original edge. These check both cases. All columns are finite. Thus the first-jet invariant is preserved by this specified expansion and retraction. Assigning a new 1+epsilon factor to EVERY elementary division would be a different coefficient assignment, counting m+A instead of m; it is not used here.

## 3. The first-order coefficient map

Use the ring of dual integers

\[
\mathbb D=\mathbb Z[\epsilon]/(\epsilon^2).
\]

It has unique coordinates a+epsilon*b and multiplication
\((a,b)(c,d)=(ac,ad+bc)\). Its split extension distinguishes \(\operatorname{ofR}(\epsilon)\), e, and tau; \(\operatorname{ofR}(\epsilon)^2=e\), not tau.

Constant reduction \(r:\mathbb D\to\mathbb Z\), a+epsilon*b -> a, induces G(r). The complete supported-zero fibre is

\[
G(r)^{-1}(e)=\{\operatorname{ofR}(\epsilon b):b\in\mathbb Z\},
\qquad G(r)^{-1}(\tau)=\{\tau\}.
\tag{3}
\]

Thus already at the scalar level the projected zero has a specified nontrivial kernel. No trajectory has been stipulated.

On the SAME original graph take

\[
K_E=[C_E^0\xrightarrow{d_E}C_E^1],\qquad
K_{E,\epsilon}=[C_E^0\otimes\mathbb D\xrightarrow{d_{E,\epsilon}}C_E^1\otimes\mathbb D],
\]
\[
d_{E,\epsilon}=J_E-(1+\epsilon)P_E=d_E-\epsilon P_E.
\tag{4}
\]

For integral original edge vectors b,c,

\[
d_{E,\epsilon}(b+\epsilon c)=d_Eb+\epsilon(d_Ec-P_Eb).
\tag{5}
\]

Multiplication by epsilon and constant reduction give the degreewise exact sequence

\[
0\longrightarrow K_E\xrightarrow{\epsilon}K_{E,\epsilon}
\xrightarrow r K_E\longrightarrow0.
\tag{6}
\]

Here K_E is a D-module through r. Equation (5) proves both chain equations. These maps commute with every support transition.

There is also an exact comparison with the existing weighted companion, without identifying its term "history" with Split-Zero support. On its ABSOLUTE coefficient ring R=Z[u,v], take

\[
\alpha:R\to\mathbb D,\qquad u\mapsto1+\epsilon,\quad v\mapsto1.
\tag{7}
\]

It sends its edge \(V_n-u v^{a(n)-1}V_{T(n)}\) to (4). Its kernel is
\((v-1,(u-1)^2)\); indeed
\(\alpha(f)=f(1,1)+\epsilon\partial_uf(1,1)\), and successive polynomial remainders in v-1 and u-1 prove both inclusions. It is surjective, with section of abelian groups a+epsilon*b -> a+(u-1)b. G(alpha) preserves the two zero labels; its supported-zero fibre is the supported copy of that ideal. The raw original endpoints and exponent a(n) remain in the graph record. Formula (7) is a particular comparison out of the weighted presentation, not the definition of intrinsic support.

The map (7) does not extend to a unital map from all of Z[v][[u]] to D: 1-u is a unit in that source, with its geometric-series inverse, while its prescribed image -epsilon is not a unit. The same obstruction holds after G because a supported inverse would have to multiply -epsilon to 1. The successful replacement used here is the finite first-jet ring (7) and the original finite-support complex, not evaluation of that completed inverse.

## 4. The actual connecting map and its entire zero fibre

The connecting map of (6) is

\[
\beta_E:H^0(K_E)\to H^1(K_E),\qquad
c\longmapsto[-P_Ec],\quad d_Ec=0.
\tag{8}
\]

Indeed lift c as a constant vector in K_epsilon. Its differential is -epsilon*Pc; removing the epsilon factor gives the displayed class. All signs are fixed by (4).

Define the integral first-jet defect to be the ACTUAL comparison kernel

\[
\mathfrak B_E=\ker\bigl(H^1(r):H^1(K_{E,\epsilon})\to H^1(K_E)\bigr).
\tag{9}
\]

### Theorem 1. Explicit presentation of the retained first-jet zero fibre

There are natural isomorphisms

\[
\boxed{
\mathfrak B_E\cong\operatorname{coker}\beta_E
\cong C_E^1/(d_EC_E^0+P_E\ker d_E)
\cong\epsilon H^1(K_{E,\epsilon}).
}
\tag{10}
\]

**Proof with inverse maps.** Send the class of y in the middle quotient to [epsilon*y]. An original relation d_Ec maps to d_epsilon(epsilon*c). For a cycle b, epsilon*P_Eb=-d_epsilon b. Hence the map is well-defined.

Every class in (9) has representative z0+epsilon*z1 with z0=d_Eb. Subtracting d_epsilon b leaves epsilon*(z1+P_Eb). Send the class to [z1+P_Eb]. Another choice of b differs by an original cycle, giving exactly a P_E*ker d_E relation. Changing the representative by d_epsilon(a+epsilon*c) replaces b by b+a and changes z1+P_Eb by d_Ec. Thus this inverse is well-defined. Both compositions are identity by the subtraction just performed. Finally every epsilon multiple is represented by epsilon*y, giving the last equality. QED.

In the Split-Zero source's notation the killed representatives and old relations are exactly

\[
K_{\rm rep,E}=d_EC_E^0+\epsilon C_E^1,
\quad B_{\rm old,E}=d_{E,\epsilon}(C_E^0\otimes\mathbb D).
\tag{11}
\]

Their quotient is (9); equation (10) computes it. The supported map is \((E,[z])\mapsto(E,0)\) on this kernel. At a nonempty label that is not the external absent point. The maps (10) commute with the original equation inclusions, so reconstruct a split-linear equivalence of the full diagrams. The additive and scalar identities are checked fibrewise after transport to E union F, not by treating the total as an abelian group with a single zero.

## 5. Component calculation, including infinite source sets

For the directed graph with declared edges E, every vertex has at most one outgoing edge. The free abelian degree-one quotient has one generator eta_A for each weak component A. The map is the component augmentation

\[
[\sum a_nV_n]\longmapsto(\sum_{n\in A}a_n)_A.
\tag{12}
\]

For its inverse choose the least original integer s_A in each nonempty component and map eta_A to [V_sA]. A finite undirected path from n to s_A, with a plus or minus sign for each directed original edge, has boundary V_n-V_sA. This proves both compositions and that its kernel is exactly the ORIGINAL edge-relation image. Finite sums meet only finitely many components.

The kernel of d_E has one free integral generator

\[
c_C=\sum_{n\text{ on }C}e_n
\tag{13}
\]

per actual primitive directed cycle C in E. To prove spanning, restrict any kernel vector to its finite edge support. A tree leaf forces the coefficient on its incident edge to vanish. Removing such edges leaves cycles. Outdegree at most one makes every remaining undirected cycle directed, and its boundary equation forces all its coefficients to be equal. Independence follows from disjoint cycle edges. Each weak component has at most one directed cycle: any two adjacent vertices have forward paths that meet (or the same finite sink); this property is preserved across a finite connecting path, and two different cycles cannot have meeting forward paths.

A component with a cycle of m distinct vertices has

\[
\beta_E(c_C)=-m\eta_C.
\tag{14}
\]

Every component without a cycle receives no generator under beta. This proves beta is injective over Z, including for infinite E, and proves the full defect classification

\[
\boxed{
\mathfrak B_E\cong
\bigoplus_{C\text{ cycles in }E}\mathbb Z/m_C\mathbb Z
\ \oplus\
\bigoplus_{A\text{ components without a cycle}}\mathbb Z.
}
\tag{15}
\]

Every coordinate map is (12), with reduction modulo m in a cyclic component; the inverse sends the coordinate generator to [epsilon*V_sA]. Its exact order is m by (12)-(14). A period-one component contributes a zero GROUP with its original nonempty module diagram and all equations retained. It is not relabelled absent.

For finite E, a component without a cycle has one frontier vertex with no declared outgoing equation. Its Z summand is unresolved under that finite set of equations, NOT evidence of an infinite Collatz orbit. For E=X, all outgoing equations are present. A component without a cycle has an injective forward ray and supplies the infinite-component summand in (15).

## 6. The complete first-jet cohomology modules

The preceding defect is not merely a count. On a cycle component of primitive length m,

\[
\boxed{H^1(K_{\epsilon}|_C)\cong\mathbb D/(m\epsilon).}
\tag{16}
\]

Choose an original cycle point c. For every vertex n in its component let r(n) be the first hitting length to c, with r(c)=0. The map sends V_n to (1+epsilon)^{r(n)} in the quotient. The relation at c is 1-(1+epsilon)^m=-m*epsilon; every other original edge respects its first hitting length. The inverse sends 1 to [V_c]. The actual finite path to c gives [V_n]=(1+epsilon)^{r(n)}[V_c]; the weighted finite cycle gives the single relation m*epsilon*V_c=0. These identities prove both inverse compositions. All paths used for individual vertices are finite, even with infinitely many incoming vertices.

For a full nonperiodic component choose its actual forward ray x_j from its least vertex. A vertex n meeting x_j after r steps maps to (1+epsilon)^{r-j}. Negative powers are explicitly 1+k*epsilon for integer k, because (1+epsilon)^{-1}=1-epsilon. A later meeting adds the same number to r and j. The inverse sends 1 to [V_x0]; original edges give both inverse identities. Thus

\[
\boxed{H^1(K_{\epsilon}|_A)\cong\mathbb D,\qquad
\mathfrak B_A=\epsilon\mathbb D\cong\mathbb Z.}
\tag{17}
\]

The same D presentation holds for a finite open component by choosing its frontier as reference and using the finite path to it. That statement has a different declared support and does not turn it into a nonperiodic component of the full graph.

As abelian groups the cycle module in (16) is Z plus (Z/mZ)*epsilon. Constant reduction forgets exactly the second term. The base loop m=1 therefore has H1=Z and zero first-jet kernel; a longer cycle has the retained torsion kernel Z/mZ; a full nonperiodic component has the free kernel Z. The original constant source spaces remain present in all three cases.

## 7. The integral first-jet restatement of Collatz

A positive fixed point obeys

\[
(2^a-3)n=1.
\]

For a=1 its solution is negative, for a=2 it is n=1, and for a>=3 the positive factor 2^a-3 is at least 5, so no positive integer solves the equation. The actual positive fixed point is therefore exactly 1.

On the FULL original absolute graph, (15) now gives

\[
\boxed{
\mathfrak B_X\cong
\bigoplus_{C\text{ nontrivial positive cycles}}\mathbb Z/m_C\mathbb Z
\ \oplus\
\bigoplus_{A\text{ nonperiodic components}}\mathbb Z.
}
\tag{18}
\]

All periods in the first sum are at least 2. The actual fixed loop contributes Z/1Z=0 through the unit map -1, without deleting its edge, vertex, or source fibre.

Consequently the following are equivalent, with the proofs provided by (10)-(18):

\[
\boxed{
\begin{gathered}
\text{Every positive odd integer reaches }1;\\
\ker H^1(r:K_{X,\epsilon}\to K_X)=0;\\
\epsilon H^1(K_{X,\epsilon})=0;\\
\beta_X:H^0(K_X)\to H^1(K_X)\text{ is an integral isomorphism}.
\end{gathered}}
\tag{19}
\]

Surjectivity of beta suffices because injectivity was proved in (14). This is a refinement by a specific comparison kernel, not a claim that its vanishing is established. It asks that the particular infinitesimal sources epsilon*V_n already be original finite boundaries. Their images under constant reduction are always supported zero, whether or not those boundaries exist. This is precisely why retaining the original kernel and relation map matters.

No global endpoint follows from the algebraic classification: determining that the nonbase component indexing sets are empty remains the arithmetic content. No new numerical cycle bound is asserted here.

## 8. Finite witnesses are extractable, not just formal zeros

The exact certificate for epsilon*V_n to be an original boundary is a pair of finite INTEGRAL original edge vectors b,c with

\[
d_Xb=0,\qquad d_Xc-P_Xb=V_n.
\tag{20}
\]

It is equivalent to \(d_{X,\epsilon}(b+\epsilon c)=\epsilon V_n\), by (5).

### Theorem 2. Finite integral witness and actual path extraction

Every pair (20) yields an actual finite Collatz path from n to 1 using only its finite edge support. Conversely, an actual first-arrival path p from n to 1 yields (20) with

\[
b=-e_1,\qquad c=\sum_{e\text{ in }p}e.
\tag{21}
\]

**Proof.** For the converse, d_Xc=V_n-V_1 and -P_Xb=V_1; also d_Xe_1=0. This includes n=1 with c=0.

For extraction form the finite graph on the support of b and c, retaining all its actual targets. In the component containing n, b is an integer multiple k of its unique cycle sum, or zero when it has no cycle. Component augmentation of (20) says -k*m=1. Thus a cycle exists and m=1. The fixed-point calculation proves its vertex is 1. In a finite functional component with a cycle, every vertex has a forward route to that cycle: a different terminal frontier or cycle would contradict the meeting-path property proved in Section 5. Following the declared original edges therefore reaches 1 within the number of vertices of this finite graph. The checker executes this extraction after verifying both integral equations; it does not infer it from a tolerance or a scalar zero. QED.

This theorem also computes what rationalization would discard. On a period-m component, m*epsilon*V_c is a boundary via minus the finite weighted cycle. Dividing that certificate by m over Q would erase its order-m class. Over Z, (20) rejects such a division for a singleton unless m=1.

For the explicitly changed map T_-(n)=(3n-1)/2^{nu_2(3n-1)}, the actual cycle is 5->7->5. Its first-jet defect is Z/2Z and

\[
d_\epsilon\bigl(-(e_5+e_7)-\epsilon e_7\bigr)=2\epsilon V_5.
\tag{22}
\]

The checker rejects its half as a nonintegral singleton witness. T_- is a control, related to the original SIGNED map by T_-(n)=-T_+(-n); it is not a positive 3n+1 counterexample.

On the original map, the edges 3->5->1 yield

\[
d_\epsilon(-e_1+\epsilon(e_3+e_5))=\epsilon V_3.
\tag{23}
\]

The relation involving the supported zero of the fixed loop is an actual part of this certificate, not a deleted row.

## 9. Support transitions, repeated words, and original arithmetic

For E subset F, the map on (15) sends the generator for an old component to the generator of its containing new component, with coefficient 1, followed by the target's modulus. It respects every old relation: a retained actual cycle remains the same cycle, so its period does not change; two different cycles cannot later join in a functional graph. Open components may merge or enter a known cycle. The matrices compose exactly, including modulus-one labels. This is a diagram indexed by equation support, not by chronological time.

Every finite vector and every relation in the full construction uses finitely many equations. Thus

\[
\mathfrak B_X\cong\mathop{\rm colim}_{E\subset X,\ E\text{ finite}}\mathfrak B_E.
\tag{24}
\]

Direct proof: represent a class by epsilon times finitely many original vertex vectors, include edges from those vertices in E, and use (10). Any equality in the full quotient has an original finite d-vector plus a finite cycle vector; putting their supports in a larger F proves the equality at that finite stage. This gives both inverse descriptions of the colimit. It agrees with the standard exactness of filtered module colimits, without assuming compactness of a space of infinite integer orbits.

A declared position word is not automatically an actual primitive cycle. An actual solution x_i of 2^{a_i}x_(i+1)-3x_i=1 gives the position-to-orbit maps e_i -> e_(x_i), V_i -> V_(x_i). They commute with both J and P, hence with d_epsilon and beta. A word traversing an actual primitive cycle r times maps its position cycle to r times the actual cycle. In particular the position circle for (2,2) has a Z/2Z first-jet defect, but its original realization x=(1,1) maps both edges to e_1, and maps that defect to Z/1Z=0. The kernel is accounted for by this explicit map. Using position length in place of actual primitive length would give a false counterexample.

The previous integral forcing class [C] in Z/(2^A-3^m)Z remains a separate retained invariant connected through this actual realization map. Integrality, positivity and exact valuations are verified before a position word is assigned an actual cycle. No equality of this forcing modulus with the first-jet index m is asserted. The numerical endpoints themselves recover the original exponent by 2^a=(3n+1)/T(n); its labelled edge is not replaced by an unmarked abstract cycle.

## 10. Coefficient and infinity comparisons

From (18), coefficient extension to Q kills exactly the finite cyclic defect summands and maps each free nonperiodic summand injectively to Q. Thus rational vector-space dimensions alone would miss all finite cycle-index obstructions in this particular comparison. Split-Zero support is preserved by G(Z)->G(Q), but the original integral kernel is still required. This is a computed loss, not a claim of an absence of relations between the coefficient settings.

For a prime p and integer r>=1, the exact quotient presentation gives

\[
\mathfrak B_X\otimes\mathbb Z/p^r
\cong\bigoplus_C\mathbb Z/\gcd(m_C,p^r)\mathbb Z
\oplus\bigoplus_A\mathbb Z/p^r\mathbb Z.
\tag{25}
\]

Every nontrivial finite m has a prime divisor, so vanishing of these reductions for all primes is equivalent to vanishing of (18). That detection claim uses the PROVED direct-sum form (18); it is not claimed for arbitrary abelian groups.

The infinite graph in (18) is handled without infinite sums of incident-edge coefficients. All chain columns remain finite. Along a specified injective original ray x_0->x_1->..., an enlarged module allowing locally finite edge chains contains epsilon*sum_j e_(x_j), whose componentwise boundary is epsilon*V_(x_0). Each vertex of that ray has at most two contributing edges, so this calculation is well-defined. It displays a free source class killed by that enlarged comparison. It does not compute the entire kernel of every locally finite completion. Retaining the original finite-support relation submodule prevents this completed primitive from being accepted as (20).

## 11. What the source rereading changes in the research programme

The scalar core is not a device that automatically stores words. The useful research object is a specified support diagram and a specified map, with its full fibre of representatives carried to supported zero. The original Rees work demonstrates that a specialization may erase a zeroth-order observation while a first-order comparison retains a defect. Sections 3-7 implement that operation directly on the original Collatz equations.

The newly exposed arithmetic target is the vanishing of the actual first-jet kernel (9) at full support, or equivalently the integral surjectivity in (19). It separates, within the SAME comparison, finite recurrence index from nonperiodic persistence and retains the fixed-loop source rather than starting by deleting it.

There are two concrete proof-development tasks, neither assumed here:

* Construct complete arithmetic families of finite pairs (20), retaining their source parameters and original valuations, and prove their coverage of all original positive sources. The small checker can verify individual instances and extracted paths; universal family coverage requires a written proof, not a sample or timeout. Equation (24) identifies the precise finite-support exhaustion that such a proof must establish.
* Control the original nonzero defect classes with arithmetic obstructions. The torsion part requires excluding actual primitive periods m>=2, not merely generic matrix cycles. The free part requires excluding an original nonperiodic component. Prime tests, tensor amplification, or geometric estimates are useful only with maps returning to this same original integral kernel and a proof of their coverage or bound. No estimate from the Riemann-hypothesis programme is imported.

A finite support's open free generator is a question to extend, not a divergence verdict. Example: E={3,13} has one open component at 5; adding the edge at 5 reaches an open vertex 1; adding the ACTUAL fixed-loop equation makes its first-jet defect zero. The source modules and all previously entered equations remain in the same diagram throughout.

This is a new exact presentation and executable witness interface, not a claimed proof of the global arithmetic vanishing. It gives no new numerical cycle bound, no new Lean execution, and no independent external mathematical audit.

## 12. Reproduction and scope

`firstjet.py` constructs the declared equation diagram, both original matrices, its full first-jet cohomology defect presentation, support-transition matrices and integral singleton certificates. `verify.py` checks 128 finite original equation sets; 2,187 support inclusions; 1,024 support-composition diagrams; abstract position-circle controls of lengths 1 through 32; the actual -1-forcing cycle; and 1,024 original positive odd singleton certificates, with 25,437 separately replayed original return equations. Twelve malformed or false inputs are rejected. All tests remain active under optimized Python.

The separate integer matrix calculation constructs unimodular row and column maps U,V and checks U*A*V=D, det U=det V=+/-1, and the actual diagonal divisibility. Its row additions, column additions, swaps and sign changes have the explicit inverse elementary operations. It does not substitute the diagonal matrix for the retained original source. Prime reductions of the original matrices provide additional independent rank checks.

The general statements, including full infinite source (18), are proved above. Finite matrices and path replays are implementation regression evidence. Ordinary and optimized runs each passed 39,211 exact checks and produced the same recorded bytes. `replay.py` verifies the source manifest and both executions.

## 13. Source locators and attribution

* [S0] Archived scalar core: `KokunoYumeto/modern-latex-manuscripts`, revision `f7ff59b176c7dc3941babd4cb9272dffc653070d`, `formalization/lean/classical_candidates_20260626/split_support_sidecar/SplitZero.lean`, blob `ff991f7383922e71cdf0e4a3bc85e89e18f808ef`. Read in full. Its retrieved path history has the archived July 4 commit `d7def24933004584b687842fe75e92ed5ee655a1`.
* [S1] Chapter 14, `satellites/14_globalization_cue_split_zero_and_shifted_sheets.tex`, Zeta revision `42d00e359b16d52ca71568ce5e3db5341949d929`, blob `49318a578b96462384000afa16794cfd5fe492c1`: scalar coordinate formulas, intrinsic support and linear-join-diagram equivalence. Read the algebraic source through its ideal/zero-divisor sections. Its historical presentation and empty-join qualifications are corrected in [S2]; those historical errors are not adopted here.
* [S2] `formal/splitzero/README.md` and `MATHEMATICAL_NOTE.md`, Zeta revision `652d3c7e269cef11e0f667be0401abb6014314c2`, blobs `4279feaeb3a80f203684d7f6b00a4e208b71d92d` and `7531d36aa44d8213e0e80d15f79668b6c8839ce5`. Read in full, including the required [tau]=0 presentation relation and the non-bottom ideal-poset correction.
* [S3] `formal/splitzero/DERIVED_MATHEMATICS.md`, same Zeta revision, blob `fe05d32ccd314daac7c59d225c9cac3d4c1bf3d3`, Sections 1-6: reconstruction, internal quotient, killed-representative kernel, and actual homology maps. The earlier source's own Lean scope is not a Lean verification of this new note.
* [S4] `workbenches/split-support-rees-trace/RESEARCH_NOTE.md`, same Zeta revision, blob `168775d2be296d74b8243cebd3e9fc8942f2eb31`, Sections 1-5. The retained first-variation calculation motivated the distinct comparison proved here; its tensor-growth estimates are not reassigned to Collatz.
* [C] Preserved Collatz predecessor: `supported_structure_20260915/note.md`, revision `2a77e3bc9435f181bc4c9c3957224a7d93b4e887`, blob `115af68c1684147e840cdd6cf690269490058f95`; the uploaded copy matches this blob. Its automata/word use of "history" remains that named presentation, not an intrinsic definition of Split-Zero cohomology.
* Standard homological constructions: Stacks Project, cones and termwise split sequences, https://stacks.math.columbia.edu/tag/014D ; Tor exact sequences, https://stacks.math.columbia.edu/tag/00M0 ; exact filtered module colimits, https://stacks.math.columbia.edu/tag/00DB . Equations (8)-(11) and (24) include direct proofs rather than relying on an unspecified connecting-map convention.

Research direction and Split-Zero framework: KokunoYumeto. This note's Collatz first-jet application, proof exposition and executable checks were developed in this continuation. No global priority claim is made for the standard scalar, homological or graph-theoretic operations. No Zeta file, inherited contribution, frozen edition, or remote main branch is changed by this addition.
