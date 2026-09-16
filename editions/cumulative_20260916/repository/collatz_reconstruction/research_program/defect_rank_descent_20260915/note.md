# Arithmetic descent from retained section defects

15 September 2026. Continuation of the original positive-integer Collatz workbench at `d0c987b12c20be5978f496ab1ef2a60018caa5e5`.

## 0. Scope and source order

This contribution advances two arithmetic operations rather than proposing another vanishing reformulation. The original integral affine-section defect gives an exact, source-dependent limit on repeated packets. Its change under a packet switch gives a precise resonance equation. A separate argument proves strict descent for an unbounded family of rise/fall words, with arbitrarily large fall exponents. The first-jet maps then turn these original paths into supported boundary relations. A proof-carrying symbolic cover provides the finite-source computation.

The predecessor is `intrinsic_zero_firstjet_20260915/note.md`, with original code blob `97f9ef5ad535f7ec18259d41fab6a3557be17d98` and note blob `d336b734a090b72bfffc70cdd9a4543504d3ded3`. Its support is a declared set of original equations, not an automata trajectory log. Its differential is `d_epsilon = J - P - epsilon P` over the dual integers. The current source was read through the connected repository; the uploaded original bytes match those Git blob identities. The structural predecessor is also replayed. All inherited files remain unchanged.

The companion `logarithmic_run_exclusion.md` completes the positive-gap domain using the explicitly cited Matveev logarithm bound and exact rational Farey certificates. It also proves the all-length restriction `m>226a` for the initial exponent-one run a at an actual cycle minimum, and excludes the complete family with one cyclic run of exponent-one letters. Nine previously certified original sources in the supported-zero equation fibre sharpen that run bound from 213 to 226 without adding discovery starts. Those are established-theorem-dependent proofs, not consequences inferred from a sampled frequency.

The original cylinder, affine numerator and descent-cell formulas occur in the earlier cycle and residual-splice contributions. They are rederived where needed below. The dyadic coding/periodicity mechanism has a substantial prior literature; [BL] identifies the classical conjugacy programme. No priority claim is made for periodic coding, monotone-run formulas, or cylinder sieves. [RT] explicitly distinguishes coefficient contraction from actual descent. Its current v5 text was consulted for that distinction; no unproved coefficient-stopping-time assertion is a premise here. The new derivations, finite certificates and their exact scope are the subject of this note.

The code is standard-library Python. General arguments are written below; finite checks are not being counted as general proofs. The rational run cone and the numerical cycle bound additionally use the explicitly listed finite integer certificates. No global Collatz resolution, independent external mathematical review, or proof-assistant execution is asserted.

## 1. The original section defect, not only its quotient class

For a nonempty positive-exponent word `p=(a_1,...,a_m)`, retain

\[
A_j=\sum_{i=1}^j a_i,\quad A_0=0,\quad
L=3^m,\quad U=2^{A_m},\quad D=U-L,
\]
\[
C=\sum_{j=0}^{m-1}3^{m-1-j}2^{A_j},\qquad
g_p(n)=\frac{Ln+C}{U}.
\tag{1}
\]

The underlying branch is `g_a(x)=(3x+1)/2^a`, in chronological order. Appending a letter gives `(L,U,C) -> (3L,2^a U,3C+U)`. Thus (1) is proved by induction, including its original additive numerator. Both C and D are odd, D is nonzero, and gcd(D,6)=1.

The integral `Z[t]`-module on `Z e_1 + Z e_2` with t-matrix

\[
\begin{pmatrix}L&C\\0&U\end{pmatrix}
\]

has specified submodule `Z_L e_1` and quotient `Z_U`. A Z-linear quotient section at an integer n is `s_n(1)=e_2+n e_1`. Its failure to intertwine t is precisely

\[
t s_n(1)-s_n(U)=h_p(n)e_1,\qquad
\boxed{h_p(n)=C-Dn.}
\tag{2}
\]

Changing the section by k changes h by `-Dk`. The resolution `0 -> Z[t] --(t-U)--> Z[t] -> Z_U -> 0`, after applying `Hom(-,Z_L)`, gives the marked extension group `Z/DZ` and class `[C]`. Equation (2), rather than that class alone, is retained in this continuation. Every h_p(n) has the same class [C], but can have a different exact dyadic valuation.

The section coordinate map `n -> s_n` is a bijection from Z to the Z-linear quotient sections, with inverse the e_1 coefficient of `s(1)-e_2`. The positive-odd source is its specified subset. No affine translation of section coordinates is being called a linear chain equivalence.

For p=(1), D=-1 and the quotient extension group is zero, but h_p(7)=8 and h_p(31)=32. The dyadic depths 3 and 5 will give different repeated-packet lengths. The supported source, section and defect distinguish these data despite the same zero quotient.

## 2. Exact cylinder membership through that same defect

### Theorem A. Original source-cylinder identity

For an original positive odd integer n,

\[
\boxed{
\text{the next exact exponent word is p}
\iff Ln+C\equiv U\pmod{2U}
\iff h_p(n)\equiv0\pmod{2U}.
}
\tag{3}
\]

Consequently its complete positive source cylinder is

\[
n=r_p+2Ut,\quad t\ge0,\qquad
r_p\equiv C D^{-1}\pmod{2U},\quad 1\le r_p<2U.
\tag{4}
\]

**Proof.** An actual word gives (1) with an odd integer endpoint, hence the first congruence. Conversely, expand C by its first letter. Divisibility of `Ln+C` by `2^{a_1}` forces `3n+1` divisible by that power. The new integer `n_1=(3n+1)/2^{a_1}` satisfies the suffix congruence. Repeating this argument gives all intermediate integers. Divisibility at the next letter makes each preceding intermediate integer odd; the last is odd by the final congruence. Thus each prescribed exponent is exact. Positive sources have positive intermediate values.

Since n is odd, `Un = U (mod 2U)`. Therefore `Dn=C (mod 2U)` is equivalent to `Ln+C=U (mod 2U)`. D is odd, so its modular inverse exists; the residue in (4) is odd. All positive elements in that residue class have exactly t>=0. This proves both equivalences and the inverse parameter `(n-r_p)/(2U)`. QED.

This is the same cylinder as `(U-C)L^{-1} (mod 2U)` in the earlier contribution: the preceding congruence calculation proves equality of the selected representatives. The new expression connects it to the original section defect.

## 3. Repetition has a finite arithmetic rank, except at a supported return

### Theorem B. Exact repetition rank

Let A=A_m. For each positive integer r,

\[
\boxed{n\text{ realizes }p^r\iff 2U^r\mid h_p(n).}
\tag{5}
\]

For `h_p(n) != 0`, the number of complete initial copies of p is exactly

\[
\boxed{
R_p(n)=\left\lfloor\frac{\nu_2(h_p(n))-1}{A}\right\rfloor.
}
\tag{6}
\]

At every admitted copy,

\[
h_p(g_p(n))=\frac LU h_p(n),\qquad
\nu_2(h_p(g_p(n)))=\nu_2(h_p(n))-A.
\tag{7}
\]

At `h_p(n)=0`, n is an actual positive return of p, and every copy is admitted. The original word, its possible repetitions, and the actual orbit are retained; word length is not substituted for primitive orbit length.

**Proof.** Composition gives

\[
S_r=\sum_{j=0}^{r-1}L^{r-1-j}U^j,\quad
C(p^r)=C S_r,\quad D(p^r)=D S_r.
\]

The integer S_r is odd: its first term is odd and every other term is even. Apply (3) to p^r. Its modulus is `2U^r` and its section defect is `S_r h_p(n)`, so (5) follows without dividing out an unrecorded even factor. This proves (6). Direct substitution proves (7). If h vanishes, (3) admits p and (1) gives `g_p(n)=n`; all intermediate valuations are actual by Theorem A. QED.

The endpoint after r admitted copies is specified without expanding the path:

\[
g_p^r(n)=\frac{C-L^r h_p(n)/U^r}{D}.
\tag{8}
\]

Every division is exact on the stated original source. Expanding the original word p exactly r times is the inverse path dictionary, including all intermediate integers and odd-return clocks. Formula (8) alone is not substituted for that dictionary.

The full source of exactly r copies followed by failure of another complete copy has the parameterization

\[
n=\frac{C-2^{Ar+1}z}{D}>0,\qquad z\in\mathbb Z\setminus\{0\},
\]
\[
2^{Ar+1}z\equiv C\pmod D,\qquad 0\le\nu_2(z)<A.
\tag{9}
\]

Its inverse is `z=h_p(n)/2^{Ar+1}`. Oddness follows from the odd numerator and denominator. Signs of z are not dropped. At r=0 this still means an original odd source with no complete initial copy.

For a fixed ordinary integer, arbitrarily long initial p-powers force h_p(n)=0, since an integer divisible by all powers of two is zero. Thus the intersection of all original p-power cylinders is either empty or the single positive integer `C/D`; it is present precisely when D>0 and D divides C. In the 2-adic source those compatible cylinders have the single point `C/D`, since D is odd. Its positive-integer support is tested separately by the displayed conditions. For D<0 that point is negative and is not an original positive source.

This proves in particular that an eventually periodic exponent itinerary on a positive integer gives an eventually periodic actual orbit. It does not eliminate an aperiodic positive orbit. A bound for a fixed nonzero defect is

\[
R_p(n)\le\left\lfloor\frac{\operatorname{bitlength}(|h_p(n)|)-2}{A}\right\rfloor.
\]

No bound independent of n is claimed.

## 4. Exact packet switching, and the resonance that prevents a false global rank

For two words p,q define their original integer resultant

\[
\Delta_{p,q}=D_p C_q-D_q C_p.
\]

Then for every integer x,

\[
D_p h_q(x)-D_q h_p(x)=\Delta_{p,q}.
\tag{10}
\]

For an actual p-step `y=g_p(n)`, this becomes

\[
\boxed{
D_p h_q(y)=D_q L_p\frac{h_p(n)}{U_p}+\Delta_{p,q}.
}
\tag{11}
\]

The quotient on the right is an original integer by (3). No comparison category has changed. Equations (10)-(11) are obtained by substituting (2); they retain both offsets and all coefficients.

Let `t=nu_2(h_p(n))-A_p` and `r=nu_2(Delta_pq)`, including infinity for a zero. When t and r differ, (11) gives the exact new depth `min(t,r)`, because its other multiplicative factors are odd. When they coincide, their leading dyadic terms can cancel and the new depth can be arbitrarily large. The code retains the full integer right-hand side in that resonant layer. It does not promote its lower valuation bound to an upper bound. At Delta=0 the common fixed-point relation remains specified, including any supported zero.

### A failed uniform rank bound leads to an actual descent family

Take p=(1), q=(2), so `h_p(n)=n+1`, `h_q(n)=1-n`, and Delta=-2. For

\[
r\ge2,\quad v\ge0,\quad s=6v+1,\qquad
n=\frac{2^{2r+3}s+1}{3},
\tag{12}
\]

one has `nu_2(h_p(n))=2`, but after the first exponent-1 edge,

\[
T(n)=4^{r+1}s+1,\qquad
\nu_2(h_q(T(n)))=2r+2.
\]

Thus a source of fixed first-packet depth produces arbitrarily large second-packet depth. Formula (11) places it exactly in the resonant layer; a proposed common decreasing depth would fail here.

The same complete family has the actual word `(1,2,...,2)` with r twos, and

\[
\boxed{T^{r+1}(n)=4\cdot3^r s+1<n.}
\tag{13}
\]

**Proof.** The source is integral because s=1 mod 3. Its first step is the displayed integer. Each following exponent is exactly 2, with intermediate values `1+4^{r+1-j}3^j s` for 0<=j<=r. Their original minus-one depths give exactly r consecutive twos because s is odd. The final difference is

\[
n-T^{r+1}(n)=\frac{(8\cdot4^r-12\cdot3^r)s-2}{3}.
\]

At r=2 the coefficient is 20; its recurrence is `A_(r+1)=3 A_r+8*4^r`, so it remains greater than 2. Since s>=1, the difference is positive. QED.

The source progression at fixed r is

\[
\frac{2^{2r+3}+1}{3}+2^{2r+4}v,
\]

and its target is `4*3^r+1+24*3^r v`. Both inverses to v are retained in the code. This proves the full unbounded family rather than testing large r as a substitute for its proof.

## 5. A complete run calculation with the affine correction retained

Let a>=1, b>=1, and consider an original word consisting of a ones followed by b exponents at least two. Put

\[
D_2(a,b)=2^{a+2b}-3^{a+b},\qquad
\lambda_2=(3/2)^a(3/4)^b.
\]

These refer to the explicit all-two comparison tail. The actual tail word and all its coefficients remain separately recorded.

### Lemma C1. Contracting pure-two runs cannot increase

On the complete original source of `(1)^a(2)^b`, with D_2>0, the terminal value is at most the original source. Equality is an actual return and is not deleted.

**Proof with the complete parameter domain.** The initial ones and the next even valuation give

\[
n=2^{a+1}t-1,\quad t>0\text{ odd},\qquad
x=2\cdot3^a t-1.
\]

The b actual exponent-two steps give a unique integer z>=1 with

\[
3^a t-1=4^b z,\qquad y=2\cdot3^b z+1.
\tag{14}
\]

To see integrality, `(3/4)^b(x-1)=y-1` and the latter is even; since 3 is odd, `x-1` is divisible by `2*4^b`. Conversely every z>=1 with `4^b z=-1 (mod 3^a)` gives `t=(4^b z+1)/3^a`, which is positive odd, and the displayed original source and intermediates realize exactly that word. These operations are inverse. Increasing z by 3^a increases n by `2^{a+2b+1}` and y by `2*3^{a+b}`, exactly the original cylinder steps.

The endpoint difference is

\[
\boxed{
n-y=2(k-1),\qquad
k=\frac{D_2 z+2^a}{3^a}\in\mathbb Z_{>0}.
}
\tag{15}
\]

The numerator is a positive multiple of 3^a because `4^b z=-1 (mod 3^a)`. Hence k>=1 and n-y>=0. The zero difference k=1 is retained as an actual periodic source. QED.

### Lemma C2. A higher tail exponent makes this descent strict

On the original source of `(1)^a(c_1,...,c_b)`, where each c_i>=2 and at least one c_i>=3, the inequality D_2(a,b)>0 gives strict descent.

**Proof.** All branch maps are increasing on positive rational inputs. Replacing one chosen higher exponent by 3 and the other tail exponents by 2 gives an upper bound on the SAME original terminal value. Moving that 3 to the start of the comparison tail increases the bound, since

\[
g_2g_3(x)-g_3g_2(x)=1/8>0.
\]

This is an inequality between two displayed affine composites, not a substitution of their words for the actual word. If `x=g_1^a(n)=(3/2)^a(n+1)-1`, the resulting upper bound is

\[
g_2^{b-1}g_3(x)
=1+\frac{\lambda_2}{2}(n+1)-\frac53(3/4)^b.
\tag{16}
\]

Since lambda_2<1 and n>=3, this is strictly less than `1+(n+1)/2 <= n`. All original exponents, source congruences and target integers remain in the source record. QED.

### Theorem C. An all-length, unbounded-alphabet descent cone

Every actual positive source whose word begins with a>=1 ones and then b>=ceil(3a/2) consecutive exponents at least two strictly descends by the end of those a+b returns.

**Proof.** Higher-exponent tails are handled by Lemma C2. For pure-two tails, it suffices in (15) to prove `D_2 > 3^a-2^a`, because z>=1 then forces k>=2. At the minimum b, even a=2h gives

\[
D_2=256^h-243^h\ge13\cdot243^{h-1}>9^h-4^h.
\]

Odd a=2h+1 gives

\[
D_2=32\cdot256^h-27\cdot243^h\ge5\cdot243^h
>3\cdot9^h-2\cdot4^h.
\]

Both are the required comparison. Increasing b changes D_2 to `3 D_2+2^{a+2b}`, so the strict comparison persists. No bound on the individual c_i is imposed. QED.

### Theorem C-rational. Certified rational cone

The same strict-descent conclusion holds for

\[
\boxed{b\ge\left\lceil\frac{2124a}{1507}\right\rceil.}
\tag{17}
\]

This is a computer-assisted all-length theorem with **1,507 finite base inequalities**, not a test of only 1,507 word lengths. The finite certificate is `slope_certificate(2124,1507)` and is independently replayed in `verify.py`.

**Proof.** Set q=1507,p=2124. The exact integer block comparison is

\[
U_*=2^{q+2p}=2^{5755}>3^{q+p}=3^{3631}=L_*.
\]

For every 1<=r<=q, the certificate verifies

\[
D_2(r,\lceil pr/q\rceil)>3^r-2^r.
\tag{18}
\]

Now retain the unique decomposition `a=hq+r`, with h>=0 and 1<=r<=q. The least b in (17) is `hp+ceil(pr/q)`. The exact extension step gives

\[
D_2(a+q,b+p)=L_*D_2(a,b)+(U_*-L_*)2^{a+2b}.
\tag{19}
\]

Moreover `3^a-2^a >= 3^{a-1}`, so multiplication by `L_*=3^{q+p}` sends a strict bound above `3^a-2^a` to a strict bound above `3^{a+q}-2^{a+q}`. Induction from (18) proves the required inequality for every a. Increasing b again uses the preceding recurrence. Lemmas C1-C2 complete the proof. QED.

The record includes the full recipe and checksum of (18), and also checks the elementary slopes 3/2 and 17/12 and the refinements 179/127 and 568/403. The smallest ratio `D_2/(3^r-2^r)` in the 1,507 base cases is 13/5, at (r,b)=(2,3). This finite minimum is auxiliary; the proof uses the individual strict comparisons.

A smaller slope cannot simply be assumed. The original word `(1)^22(2)^31` has

\[
D_2=-40432553845953101497907.
\]

Its actual source `31455430079290429512089599` has terminal `31521181806453574636140115`, which is larger. Both are independently replayed. More generally `(1)^{22h}(2)^{31h}` has negative D_2 for every h>=1, and every positive source in its original nonempty cylinder grows. Thus the proposed universal slope 31/22 is concretely refuted by original sources, not merely rejected numerically.

### Complete positive-gap domain

The companion `logarithmic_run_exclusion.md`, Theorem E, proves `D_2(a,b)>3^a-2^a` for **every** positive pair with `D_2(a,b)>0`, using the stated published transcendence theorem and a full finite rational certificate. Its Corollary E1 therefore strengthens the preceding rational cone to the exact condition `2^{a+2b}>3^{a+b}`, with the same arbitrary tail exponents and actual source equations. The earlier elementary and rational-cone arguments remain shorter, independently replayable routes on their stated domains.

## 6. First-jet transport of the new arithmetic paths

Keep the original absolute complex, with `J e_n=V_n`, `P e_n=V_T(n)`, `d=J-P`, and

\[
\mathbb D=\mathbb Z[\epsilon]/(\epsilon^2),\qquad
 d_\epsilon=d-\epsilon P.
\]

For an actual finite path p from n to y, let `B_p(n)=sum e_(T^j(n))`. Then

\[
 d B_p(n)=V_n-V_y,\qquad
\boxed{d_\epsilon(\epsilon B_p(n))=\epsilon V_n-\epsilon V_y.}
\tag{20}
\]

The original path has finitely many edges for every finite parameter value, although the family permits unbounded lengths and source labels. The domain-to-chain map is the linear map on the free module on the original parameter fibre that sends its n-labelled generator to B_p(n); its boundary is the difference of the specified source and terminal maps. This is the actual connection between the section/rank calculation and the first-jet complex, not an asserted equivalence between their differentials.

For a specified rule choosing one such strict-descent path for each admitted original source, this map on finite free source modules is injective. In a nonzero finite combination choose the largest original source n with nonzero coefficient. No endpoint from a smaller source can equal n, so the boundary coefficient at V_n is exactly that source coefficient. This proves injectivity. It also gives the inverse on the image by successively recovering the largest source coefficient and subtracting its original path column. The rule and its domain remain part of that inverse.

Adding (20) to an existing integral witness at y yields one at n. For the finite cover in Section 8, every endpoint is smaller, so these additions terminate by strong induction on original positive integers. The final witness has the exact form

\[
 d_\epsilon\left(-e_1+\epsilon c_n\right)=\epsilon V_n,
\tag{21}
\]

with c_n an original finite integral path chain. The predecessor checker verifies (21) and independently extracts the actual route to 1. No rational division by a cycle period is permitted. The original equation support is the union of supports in (20)-(21), not a record of the order in which they were discovered.

## 7. A whole-source first-return reduction whose first-jet clock is not shortened

The subset `Y={n>0 odd: n=1 (mod 4)}` contains the actual fixed vertex. Every original vertex reaches Y through its maximal initial string of exponent 1. In exact coordinates,

\[
\tau(n)=\nu_2(n+1)-1,\quad t=(n+1)/2^{\tau(n)+1},
\]
\[
T^j(n)=3^j2^{\tau(n)+1-j}t-1\quad(0\le j\le\tau(n)),\qquad
\theta(n)=2\cdot3^{\tau(n)}t-1\in Y.
\tag{22}
\]

The integer t is positive odd. These identities prove exact valuations and finiteness without assuming global convergence.

For y in Y define `F(y)=theta(T(y))` and `ell(y)=1+tau(T(y))`. Use a block complex on the SAME original Y-vertices with differential

\[
 d_Y E_y=V_y-(1+\ell(y)\epsilon)V_{F(y)}.
\tag{23}
\]

Let w=1+epsilon. The projection on vertices is `V_n -> w^{tau(n)}V_theta(n)`. On edges it sends e_y to E_y for y in Y, and every other original edge to zero. The inclusion fixes Y-vertices and sends E_y to its entire original path with coefficients `w^j=1+j epsilon`. The homotopy sends V_n to the similarly weighted original path from n to theta(n).

**Proof of both comparison identities.** Outside Y, the first exponent is 1, `tau(n)=1+tau(T(n))`, and the two projected endpoint terms cancel. At y in Y they give exactly (23). Telescoping proves that the inclusion is a chain map. A block has only its first source in Y, so projection after inclusion is the identity in both degrees. The homotopy equations are

\[
 d_\epsilon H=I-\iota\pi,\qquad H d_\epsilon=I-\iota\pi
\tag{24}
\]

on vertices and edges respectively: outside Y, subtracting w times the next rising tail leaves precisely e_n; at y in Y it leaves e_y minus the full block expansion. All columns are finite. QED.

The kernel of H is exactly the span of the Y-vertices. It vanishes on them. For a nonzero finite combination of other vertices, take the least original source with nonzero coefficient. Its first edge occurs with coefficient one in its own rising tail and cannot occur in a tail starting at a larger original vertex, since exponent-one edges strictly increase positive vertices. The coefficient survives. This also proves the stated kernel over the dual-integer ring without cancellation by a nonunit.

For a finite declared equation set E, adjoin the rising tails of its vertices and targets. This enlargement is finite, is idempotent, preserves unions, and supplies the support of (24). Its Y-equations are exactly E intersect Y. These explicit support maps make the comparison compatible with the Split-Zero reconstruction; no unknown forward orbit is used to define the finite enlargement.

A block cycle retains original total length `sum ell(y)`, so its connecting-map index is that sum. A compressed self-loop with ell>1 is not silently called the trivial cycle. For example the actual block `9 -> 7 -> 11 -> 17` has length 3. Assigning it the coefficient `1+epsilon` rather than `1+3 epsilon` leaves the explicit nonzero residual `-2 epsilon V_17`. The checker verifies this failed shortening and the correct map.

## 8. The symbolic source-cover certificate

For an arbitrary actual first-descent word p, let r,U,L,C,D be as in (1),(4). The complete source set is empty when D<=0. For D>0 it consists of

\[
n=r+2Ut,\qquad \ell\le t\le h,
\]
\[
\ell=\max\left(0,\left\lfloor\frac{C-Dr}{2UD}\right\rfloor+1\right),\qquad
h=\min_{\substack{j<m\\D_j>0}}\left\lfloor\frac{C_j-D_jr}{2UD_j}\right\rfloor,
\tag{25}
\]

where the empty minimum is infinity. These are exactly `D n>C` at the terminal return and `D_j n<=C_j` at every earlier return. Positivity of C_j makes earlier D_j<=0 impose no extra bound. Thus all constraints and the affine offset remain. The target progression is `u+2Lt`, with `Uu=Lr+C`; both parameter inverses are explicit.

Two occupied first-descent cells cannot intersect: an original source has one actual first-descent time and one original exponent word at that time. This proves disjointness even for nested legal cylinders whose first-descent intervals separate them.

For an odd upper source bound B, the number of sources of one cell in [3,B] is the exact integer interval count obtained from (25) and `3<=r+2Ut<=B`. If the sum of these disjoint counts equals `(B-1)/2`, the cells cover every odd source from 3 to B. Each target is a lower positive odd integer. Strong induction, beginning at 1, then proves finite first-jet witnesses (21) for the entire interval.

The search takes only the least uncovered original source, obtains its first descent, and adds its COMPLETE cell. It never treats a search cap as a proof. The acceptance checker does not assume that discovery is correct: it reconstructs every cell with the unreduced final parity congruence, verifies the constant and slope of every original prefix equation, checks the exact floor interval, and verifies the complete disjoint counting identity. A second implementation enumerates every interval slot and checks the lower positive terminal. Source labels (1) and (2,2) remain declared zero-count first-descent cases.

The delivered certificate has:

| Scope | Exact result |
|---|---:|
| Original odd interval | 3 through 1,166,399 |
| Sources covered | 583,199 |
| Distinct complete first-descent cells | 41,122 |
| Cells with unbounded positive parameter | 41,122 |
| Declared empty first-descent labels | 2 |
| Original sources actually iterated in discovery | 41,122 |
| Original return equations in those discovery words | 754,655 |
| Independently verified constant and slope equalities | 1,509,310 |
| Maximum retained word length | 141 |
| Maximum retained exponent sum | 227 |

These symbolic statements extend to every parameter in each cell. Convergence to 1 is asserted for the completely covered finite interval, not for every larger member of the cell without its lower-endpoint certificate.

## 9. The actual finite first-jet support behind that coverage

For every source occurrence in (25) within the certified interval, expand its original finite word and retain all its original edge labels. Include e_1. The resulting equation set is E_B. Every internal edge target is the next retained edge source; every terminal is a lower source in the covered interval or 1. Thus E_B is forward closed. Every vertex lies on a path to a lower covered source and hence to 1 by the proved induction.

The code separately materializes this support and recomputes each edge by repeated integer division, rather than the valuation-bit operation in discovery. It constructs a nonnegative integer height H with

\[
H(1)=0,\qquad H(n)=1+H(T(n))\quad(n\ne1).
\tag{26}
\]

Its recorded source scope is:

* 926,548 distinct original equations and vertices;
* 2,029,720 prefix-equation occurrences before deduplication;
* largest original vertex 30,079,718,549;
* maximum height 196;
* one actual component, with actual cycle (1).

All original edges and heights enter the transcript hash. The connecting map for this finite supported complex has matrix [-1]; the first-jet reduction kernel is zero, while its original nonempty source module and relations remain. This is an actual supported-zero calculation on E_B. It does not set the kernel at full infinite support to zero.

There are additionally 399 original singleton witnesses assembled from the symbolic cover and replayed by the unchanged predecessor's integral first-jet witness extractor. They contain 11,451 original returns. These samples test the interface; the complete interval claim comes from the covering proof, not from sampling.

## 10. The executed all-length cycle exclusion

For an actual nontrivial positive cycle, write m for its primitive number of odd returns, A for its exponent sum, k for its number of exponent-1 positions, and s for a lower bound on every vertex. Multiplying the ORIGINAL equations yields

\[
3^m<2^A=\prod_{i=1}^m(3+1/x_i)\le(3s+1)^m/s^m.
\tag{27}
\]

Also `A=2m-k+E`, where `E=sum_(a_i>=3)(a_i-2)>=0`. Hence

\[
(4s)^m\le2^k(3s+1)^m.
\tag{28}
\]

The observation (m,A,k,s) does not replace the word. Its fibre still consists of the ordered words with those counts whose original forced cycle equations have a positive integral primitive with that minimum. The comparisons below exclude the entire fibre without declaring a permitted numerical window realizable.

The source certificate gives s=1,166,401. The exact integer comparisons in `independent_period_check` establish

\[
2^{\operatorname{bitlength}(3^m)}s^m>(3s+1)^m
\quad(1\le m\le3630),
\tag{29}
\]

and

\[
\boxed{(4s)^{3631}>2^{1506}(3s+1)^{3631}.}
\tag{30}
\]

The independent implementation obtains the least power of two strictly above 3^m by an integer doubling loop, not by calling bit_length. Inequality (29) excludes every possible A at those m. Since `4s>3s+1`, (30) persists at every larger m and every k<=1506. Therefore:

### Theorem D. Finite arithmetic certificate, all primitive lengths

There is no nontrivial positive integer Collatz cycle whose primitive odd-return word has at most **1,506 exponent-1 positions**.

The proof is (25)-(30) and the recorded complete integer certificate. This improves this workbench's self-contained certificate, not a published cycle record. It does not use an external large-source verification bound.

The next retained budget k=1507 is forced to

\[
m=3631,\quad A=5755,\quad
1166401\le\min x_i\le1505447\quad\text{(odd minimum)}.
\tag{31}
\]

The exact ceiling over ALL integers is 1,505,448, so the odd ceiling is one smaller. The next power of two fails (27), and (28) at m=3632 excludes that and every larger length for k=1507. Thus E=0 and this sector contains exactly 1,507 ones and 2,124 twos. The all-rise-then-all-fall ordering is already excluded by Theorem C-rational; the companion also excludes every cycle with one cyclic exponent-one run, including arbitrary larger exponents. Its all-length minimum-run bound `m>226a` remains attached to the actual minimum placement. The other ordered placements have not been exhausted here. The original gap dictionary, integral forcing and actual primitive-period requirement remain attached to (31).

## 11. What is resolved here, and the exact surviving arithmetic task

The section-defect calculation handles arbitrarily long repetitions of a fixed packet: its nonzero dyadic rank strictly decreases, and its zero is an actual return with its original primitive retained. Packet switching cannot be treated as a common monotone rank; (11)-(13) give an unbounded reset and then a descent proof for that same family. The run cone provides another unbounded family of original descent relations, without bounding the individual exponents. Equations (20)-(24) preserve the original first-jet object when using those arithmetic reductions.

The remaining source is not identified with all locally compatible residue paths. An actual least vertex of a nonbase component must avoid every proved descent family. Its initial rise/fall block is outside every applicable descent cone. The companion removes the positive-gap equality case in the weak pure-two lemma by an explicit established-theorem-dependent proof; arbitrary packet-return zeros outside that family remain retained. Every nontrivial cycle has at least two cyclic exponent-one runs and satisfies the companion's original minimum-run bound. Its packet changes obey (11), including their full resonant residuals. Its compatible dyadic residues must still stabilize at one original positive integer. No proof is supplied that every such residual source is covered, and no original nontrivial cycle or divergent source is produced.

The concrete next work is to control the remaining resonant packet-switch fibres with their exact offsets, or add further complete descent families on those fibres. The atlas and first-jet witness interfaces accept such families without weakening the integer or support requirements. Increasing the finite source bound remains a separate finite calculation; it is not a substitute for that all-source task.

## 12. Reproduction and publication status

Run `python -B replay.py` in this directory. The replay checks source hashes, independently verifies the full atlas and first-jet support, and compares both ordinary/optimized outputs byte-for-byte. Add `--predecessors` to run the unchanged structural and first-jet predecessors as well. Add `--rebuild-atlas` to regenerate the symbolic cover from the least-uncovered-source search and compare its canonical uncompressed bytes. The gzip container's incidental platform header is not used as a mathematical identity for regenerated data.

`query.py` exposes repetition certificates, resonant-family examples, peak blocks and finite integral first-jet witnesses from the atlas. Source paths and clocks remain explicit. `morphisms.jsonl` records domains, formulas, inverses, support and information-loss scope for the new maps.

The current connector successfully read the repository and pinned source but exposes no write operation in this session. The local Git HTTPS read also failed to resolve the host. Plugin discovery found the installed GitHub plugin, not an additional available write action. This increment is therefore packaged as a tested additive patch against the read head, not claimed as a remote commit or CI run. The remote status is recorded in the separate delivery receipt. No inherited file or Zeta source is modified by the patch.

## References and attribution

[P1] The original workbench `intrinsic_zero_firstjet_20260915/note.md`, Sections 3-9, and its unchanged `firstjet.py`. Current read commit `d0c987b12c20be5978f496ab1ef2a60018caa5e5`.

[P2] The original `residual_splice_20260914/note.md` and `integral_blocks.md`: affine source cylinders, exact first-descent masks and integral comparison maps. The new checker reconstructs its data independently rather than silently replacing the formulas.

[P3] `supported_structure_20260915/note.md`: the original maximal exponent-1 run and supported component calculation. Its corrected source blob is `115af68c1684147e840cdd6cf690269490058f95`.

[BL] D. J. Bernstein and J. C. Lagarias, *The 3x+1 Conjugacy Map*, Canadian Journal of Mathematics 48 (1996), 1154-1169, DOI `10.4153/CJM-1996-060-x`. The publisher abstract and authors' publication index were consulted for established dyadic-coding context; no uninspected theorem from that paper is a premise.

[RT] O. Rozier and C. Terracol, *Paradoxical behavior in Collatz sequences*, arXiv `2502.00948v5`, current readable text at `https://arxiv.org/html/2502.00948v5`, especially Definitions 1.1-1.2 and the coefficient/remainder distinction. The elementary shortened-map clock expands an odd-return exponent a into one odd shortened step and a-1 divisions; grouping between successive odd states is its inverse. Thus its affine coefficient/remainder at a completed return are exactly L/U and C/U in (1). No coefficient-stopping-time conjecture is assumed.

Research direction and Split-Zero framework: KokunoYumeto. This continuation's derivations, exposition and executable finite checks were developed in the present tool-assisted session. General source provenance and standard mathematical operations are not relabelled as a priority claim.
