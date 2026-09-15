# Supported anchored defects, exact cycle periods, and an alphabet-exit certificate

**14 September 2026. Collatz workbench continuation.**

Source: `KokunoYumeto/collatz-workbench`, commit `6a30f1dc23110fae0abbe3b3bd5e60072a842385`, PR #2. All inherited files remain unchanged. The proofs below use the actual original odd-return map and the preserved integral cycle and residual-source constructions. The finite certificate is executed by `verify.py`; source preservation and all ten ordinary/optimized executions are checked by `replay.py`. No independent external mathematical review, Lean verification, or global convergence result is asserted.

## 1. What the Split-Zero technique contributes, with an exact comparison

For a ring R, use the supplied support extension G(R)=R disjoint union {tau}. The external tau is the additive identity and multiplicative absorber. Operations on supported elements are their original ring operations. Thus e=0_R is a supported zero, with e distinct from tau. There are explicit semiring maps

\[
 \pi:G(R)\longrightarrow R,\qquad
 \chi:G(R)\longrightarrow\mathbb B,
\]

where pi fixes R and sends tau to 0, while chi sends tau to 0 and every element of R, including e, to 1. The Boolean operations are OR and AND. Direct case checking shows that both maps preserve addition and multiplication. The map

\[
 (\pi,\chi):G(R)\longrightarrow R\times\mathbb B
 \tag{S1}
\]

is an isomorphism onto the subsemiring

\[
 \{(0,0)\}\ \cup\ \{(r,1):r\in R\}.
\]

Its inverse sends (0,0) to tau and (r,1) to the supported r. Both compositions are identities. The zero fiber of pi alone is {tau,e}; every nonzero fiber is a singleton. This also specifies exactly how ordinary coefficient calculations with a retained Boolean support coordinate implement the supplied technique. No exclusivity or priority claim for these elementary operations is made.

Here R=Z or Q. The exponent word, source lattice, forcing vector and graph edges are additional retained data, not information reconstructed from chi alone. `Supported` implements (S1) over Q and tests both zero values, cancellation, multiplication and distributivity.

### A zero-forcing row is still an actual relation

For the one-letter word (2), the anchored cycle equation is (4-3)y=0. Its complex is [Z --1--> Z], with both cohomology groups zero. Deleting the zero-forcing row produces [Z --> 0], whose H^0 is Z. The exact comparison is q^0=id and q^1=0. Its kernel complex is [0 --> Z]. In the associated long exact sequence the connecting map from H^0([Z-->0]) to H^1([0-->Z]) is multiplication by 1, computed by lifting the source generator and applying the original differential. The extra kernel created by row deletion is therefore explicitly accounted for. The supported zero never licensed deletion of that differential.

### The coefficient map to the complex analytic setting

The inclusion Z -> C induces G(Z) -> G(C), taking tau to tau and the supported integer zero to the supported complex zero. Through (S1), this is the restriction of inclusion times id_B, so it preserves the two zero labels injectively. For the original return complex [Z --D--> Z], coefficient extension gives [C --D--> C]. At D nonzero, its contracting homotopy is multiplication by 1/D in degree one. Thus the induced H^1 map is the explicitly zero map Z/DZ -> 0, even though the support coordinates remain present. For (1,3), D=7 and the forcing class [5] is nonzero integrally; its complex primitive is 5/7. This proves the precise loss under this coefficient change. We retain the original integral complex rather than substitute its complex-coefficient contraction.

The peer Zeta guide currently studies spectral cohomology and original period/Gram calculations. That guide provides context, not an arithmetic estimate used here. No identification of its theta complex with the Collatz cycle complex is asserted. The coefficient maps just specified are the comparisons used in this note.

## 2. Original forcing and anchored primitive

Let

\[
 T(n)=\frac{3n+1}{2^{a(n)}},\quad a(n)=\nu_2(3n+1),\qquad
 X=\{1,3,5,\ldots\}.
\]

For an original nonempty exponent word p=(a_1,...,a_m), retain

\[
 A_j=\sum_{i=1}^j a_i,\quad A_0=0,\quad
 U=2^{A_m},\quad L=3^m,\quad D=U-L,
\]
\[
 C=\sum_{i=1}^m3^{m-i}2^{A_{i-1}},\qquad
 F_p(n)=(Ln+C)/U.
\]

The preserved cycle differential and functional are

\[
 (B_px)_i=2^{a_i}x_{i+1}-3x_i,\quad x_{m+1}=x_1,
\]
\[
 f_i=3^{m-i}2^{A_{i-1}},\quad fB_p=D e_1^T.
 \tag{A1}
\]

The predecessor proves H^0=0 and H^1=Z/DZ with [b] sent to [fb]. The actual cyclic forcing is b=1, with marked coordinate [C]. Its rational primitive is x_i=C(p_i)/D, for the retained rotations p_i. Integrality, positivity, and the actual valuation equations remain required to obtain a positive integer orbit.

The affine coordinate map y=x-1 has inverse x=y+1. Substitution gives

\[
 B_py=b_p,\qquad (b_p)_i=4-2^{a_i},\qquad fb_p=C-D.
 \tag{A2}
\]

This is a bijection of the two specified solution sets, not a claim that translation is a linear chain map. Its forcing difference is the original boundary -B_p1. Consequently

\[
 [b_p]=[1],\qquad [C-D]=[C]\text{ in }\mathbb Z/D\mathbb Z.
 \tag{A3}
\]

The same integral class is retained. What changes is its specified primitive and the exact observable below. The trivial word repetitions (2)^m have y=0. Conversely y=0 forces every right-hand side 4-2^{a_i} to vanish, so every letter is 2 and x=1. An actual nontrivial positive cycle never meets 1, since T(1)=1; therefore all its x_i are at least 3 and y_i are positive even integers.

The block maps from `../residual_splice_20260914/integral_blocks.md` still apply. In that notation the anchored right-hand side maps to Rb_p, and the inverse is y=S_0z+Hb_p, followed by x=y+1. Dropping Hb_p does not give this affine inverse. Equations (A2)-(A3) make the comparison with the existing marked obstruction literal.

## 3. An anchored period character with its complete zero domain

For n>1 define

\[
 \eta(n)=\frac{2^{a(n)}(T(n)-1)}{3(n-1)}
 =1+\frac{4-2^{a(n)}}{3(n-1)}.
 \tag{P1}
\]

This is a nonnegative rational value. A step into 1 gives eta=0, retained as a supported zero. At n=1 the ratio is not defined: its retained equation is 4*0=3*0+0, with exponent 2 and zero forcing. No 0/0 is assigned a value.

For an actual finite path starting above 1 and stopped no later than its first arrival at 1, multiplication of the exact edge equations gives

\[
 \prod_{j=0}^{m-1}\eta(T^j(n))
 =\frac{2^{A_m}}{3^m}\frac{T^m(n)-1}{n-1}.
 \tag{P2}
\]

The identity includes terminal value 1: both sides are then supported zero. Its proof cancels only the positive intermediate factors. No canceled intermediate factor is zero.

On the subgraph with both endpoints above 1, all eta values are positive. Let C_1 be the free abelian group on its actual edges, C_0 the free abelian group on its vertices, and partial(e_n)=v_n-v_T(n). Define multiplicative homomorphisms

\[
 \rho(v_n)=n-1,\qquad \lambda(e_n)=2^{a(n)}/3.
\]

They extend by products with the original integer chain coefficients. Their exact relation is

\[
 \eta(c)=\lambda(c)\rho(\partial c)^{-1}.
 \tag{P3}
\]

Thus eta and lambda differ by the specified vertex coboundary, and define the same class in multiplicative degree-one graph cohomology. In particular every actual closed cycle c satisfies

\[
 \eta(c)=\lambda(c)=2^A/3^m.
 \tag{P4}
\]

The kernel of lambda consists exactly of finite chains with both sum c_n a(n)=0 and sum c_n=0, by unique prime factorization. The kernels of rho and eta are likewise the simultaneous integer prime-valuation equations of their displayed rational products. These describe the fibers as cosets of the stated kernels; no unspecified spectral quotient is used.

The predecessor's retractions preserve closed chains literally, F(c)=c. Formula (P4) is therefore unchanged on every actual nontrivial cycle under those retractions. We do not extend the positive-group character to a general retraction path that enters 1: that path has the supported zero endpoint in (P2), not an invertible character value.

### Theorem P. A cycle inequality controlled by the original exponent-1 positions

For a nontrivial positive integer cycle with every vertex at least s>=3, and k occurrences of exponent 1,

\[
 \boxed{\quad
 1<\frac{2^A}{3^m}
 \le \left(\frac{3s-1}{3s-3}\right)^k.
 \quad}
 \tag{P5}
\]

**Proof.** The ordinary cycle equations give 2^A=product(3+1/x_i)>3^m. By (P1), an exponent-1 edge has factor 1+2/(3(x_i-1)), at most (3s-1)/(3s-3). An exponent-2 edge has factor exactly 1: its zero anchored forcing remains a supported relation and its original exponent still contributes to A. Every exponent at least 3 has a factor strictly between 0 and 1, since the next cycle vertex exceeds 1. Bound those latter factors above by 1, retain the original k factors, and use (P4). This proves (P5). In particular k cannot be zero. No independence, asymptotic estimate, or probabilistic coefficient model occurs. QED.

For a fixed contracting pair (m,A), (P5) is an exact integer test

\[
 2^A(3s-3)^k\le3^m(3s-1)^k.
 \tag{P6}
\]

Its right-to-left ratio strictly decreases with integer s>=2. An accepted integer and rejection of the next one therefore certify its exact ceiling. For (m,A,k)=(971,1539,403), the ceiling is 274546. The prior unanchored ceiling was 330749. Both endpoint comparisons are checked on integers.

## 4. The complete next exponent partition and its exact parameter maps

Keep a legal prefix q, including the empty prefix, with the original chart

\[
 n=r+2Ut,\quad x=F_q(n)=u+2Lt,\quad Uu=Lr+C.
 \tag{C1}
\]

For the empty word use L=U=1, C=0, r=u=1. Every prefix source under consideration is a positive odd integer. The next three cases are

\[
 a=1,\qquad a=2,\qquad a\ge3.
 \tag{C2}
\]

The first two cases are precisely the original legal cylinders of q1 and q2. The last case is exactly

\[
 t=t_0+4v,\qquad
 t_0\equiv-\frac{3u+1}{2}(3L)^{-1}\pmod4,\quad0\le t_0<4,
\]
\[
 n=r+2Ut_0+8Uv.
 \tag{C3}
\]

The full exponent in this last case remains recoverable:

\[
 a=\nu_2(3u+1+6Lt).
 \tag{C4}
\]

Indeed, 3x+1 is positive and even. Its valuation is at least 3 precisely when (3u+1)/2+3Lt is divisible by 4. Since 3L is odd, (C3) is its complete solution. Its inverse is v=(n-r-2Ut_0)/(8U), and t=(n-r)/(2U). This proves both the partition and its full label recovery. The lower bound a>=3 is not a substitution a=3.

For each of the two exact-exponent children, the original descent test remains

\[
 F_p(n)<n\quad\Longleftrightarrow\quad D_p>0\text{ and }D_p n>C_p.
 \tag{C5}
\]

At a node that has not previously descended, (C5) splits the current source interval into a descent part above floor(C_p/D_p) and a retained part at or below it. For D_p<=0 there is no descent part. Empty parts keep their labels and original equations.

### A synchronized congruence has its own retained map

The cover also imposes n=c mod M. To intersect this with n=r mod Q, put g=gcd(Q,M). Compatibility is g divides c-r. In the compatible case choose

\[
 t_0\equiv ((c-r)/g)(Q/g)^{-1}\pmod{M/g},\quad 0\le t_0<M/g,
\]
\[
 \alpha=r+Qt_0,\quad\Delta=Q(M/g),\qquad n=\alpha+\Delta z.
 \tag{C6}
\]

Both original residue equations are recovered by this substitution. Conversely every joint solution has this form, because its original t=(n-r)/Q solves the displayed linear congruence. The inverses are z=(n-alpha)/Delta and t=(n-r)/Q. Intersecting with the retained interval [l,h] gives exactly

\[
 \left\lceil\frac{l-\alpha}{\Delta}\right\rceil
 \le z\le
 \left\lfloor\frac{h-\alpha}{\Delta}\right\rfloor.
 \tag{C7}
\]

The code retains incompatible residue defects, compatible empty intervals, the original r,Q,c,M, and both parameter maps. It does not replace the source progression by a uniformly sampled interval.

## 5. An actual alphabet-exit map, not a convergence certificate

Define the graph G_12 on the actual positive odd vertices by retaining exactly the original edges e_n for which a(n) is 1 or 2. Let E be the actual vertex set with a(n)>=3. The inclusion of G_12 into the original orbit graph is identity on vertices and on the retained edges and commutes with partial. Every E-vertex is present but has no outgoing edge in G_12.

An original positive integral solution for a word in {1,2} maps its position circle into G_12: position i goes to x_i and its edge goes to e_x_i. The original equations establish those edge memberships and the boundary identity. The block-circle expansion of the predecessor sends each block edge to the sum of its original edges, so its fundamental cycle maps to the same full cycle chain. Repetitions keep their integer multiplicities.

There is also the explicit relative chain map from the complex relative to (v_1,e_1) to the one additionally relative to E: q_1 is the identity, and q_0 kills the E-vertices and fixes the others. Its degree-zero kernel is the free group on E; its degree-one kernel is zero. Because both complexes have no degree-two chains, q induces an injection on H_1. In particular, a nontrivial {1,2} cycle stays a nonzero cycle on its original edges.

A prefix in (C3) gives a path of allowed original edges from n to z in E, with boundary v_n-v_z. This becomes a boundary certificate for v_n in the exit-relative complex. It remains v_n-v_z in the original graph. There is no assertion that z reaches 1.

For a proposed cycle minimum n, either of two original facts excludes membership: a path descends below n, or a path of allowed edges reaches E. The former contradicts minimality; the latter contradicts the proposed {1,2} word. This is the exact relationship used by the finite certificate. It does not erase the possibility of a cycle having an exponent at least 3.

## 6. Discharge of the complete 403-rise sector

The preserved residual-splice certificate proves an actual first descent for every odd source from 3 through 99779. Strong induction proves that all those sources reach 1. Its existing all-length theorem excludes at most 402 exponent-1 positions. The new calculation keeps that common source bound unchanged.

### Theorem Q. No nontrivial positive cycle has at most 403 exponent-1 positions in its primitive odd-return word

**Proof.** Its minimum is at least s=99781 by the replayed predecessor certificate. The original product and exponent identities give

\[
 (4s)^m\le2^k(3s+1)^m,\qquad
 A=2m-k+E,\quad E=\sum_{a_i\ge3}(a_i-2)\ge0.
 \tag{Q1}
\]

For k<=403, exact integer comparison at m=972 and monotonicity of (4s)/(3s+1)>1 force m<=971. For every length 1 through 970, the exact comparison is 2^bitlength(3^m) * s^m > (3s+1)^m; thus the least power of 2 greater than 3^m already exceeds the upper cycle bound. These 970 comparisons are checked independently by a least-power-of-two loop. At m=971 the only admissible exponent sum is A=1539; the next power fails the upper bound. Then E=k-403>=0, giving k=403 and E=0. Thus the word consists of 403 ones and 568 twos.

Theorem P bounds its minimum by 274546. Its outgoing exponent must be 1, since an exponent 2 would descend at a source greater than 1. Its incoming exponent must be 2, since exponent 1 strictly increases a positive source. The first fact gives n=3 mod4. The second gives 4n=3x+1 for its original predecessor x, hence n=1 mod3. The CRT inverse (C6) identifies these two conditions with n=7 mod12. The possible minima are exactly

\[
 n=99787,99799,\ldots,274543,
 \tag{Q2}
\]

with 14564 elements. No word-order choice has been discarded: every original cycle in the sector maps its minimum to a member of (Q2).

Starting from this precise source, the complete partitions (C2)-(C7) give a finite proof tree. At every nonempty node all previous actual returns have been at least the original source. The tree retains the original word, congruences, all coefficients, and all empty child masks. This instance uses the code's excess budget 0; the positive-budget comparison is proved in the companion note. It closes after 2957 branching nodes; no nonempty prefix exceeds 32 allowed returns and no OPEN leaf remains. Of its 8871 terminal labels, 7721 have empty integer fibers and keep their present labels. Exactly 1150 labels are occupied: 1133 actual alphabet-exit tails and 17 first-descent cells. Their cardinalities sum to

\[
 13399\text{ exit sources}+1165\text{ descent sources}=14564.
 \tag{Q3}
\]

The certificate checks disjointness and conservation at every node and checks every terminal fiber by independently enumerating the ORIGINAL dyadic progression and imposing n=7 mod12, without using the generator's CRT inverse. A separate repeated-division interpreter reads every n in (Q2), verifies its full word and endpoint classification, and accumulates the original path boundary. Every one descends or exits the allowed alphabet. Section 5 excludes both cases for the proposed cycle minimum. This proves the theorem. QED.

This is a computer-assisted finite certificate combined with the displayed all-length inequalities. It advances the self-contained workbench bound, not a claimed published cycle record. It does not depend on independent random exponents or on the distributional estimates in the earlier notes.

The proof-tree generator accepts arbitrary finite depth caps. A cap reached before closure creates an explicit OPEN leaf; the verifier rejects its use as a proof of this exclusion. Other rejected controls include an erased empty label, a forged original word, a deleted occupied fiber, and an alphabet exit incorrectly promoted to descent.

## 7. What remains and how to reproduce the work

The companion `turns_and_unit_excess.md` proves the ordered adjacent-turn period identity, retains the exponent-3 negative forcing, and completely discharges the 404-rise sector too. Its two source classes have different exact incoming-edge constraints. The next 405-rise sector remains at m=971, A=1539 with total excess 2: either two threes and 564 twos, or one four and 565 twos, together with the 405 ones. These original letters and their placement remain part of the task; a zero-budget alphabet exit is not a certificate for that larger fiber.

For the nonperiodic direction, (P2) retains the endpoint displacement as well as both clocks. No uniform bound on that endpoint or on the residual integer-supported source has been proved here. The old residual roots and their degree-zero obstruction remain. The alphabet-exit operation is confined to its specified word fiber and does not supply a source-complete contraction of the original graph.

Run from the repository root:

```
python -B collatz_reconstruction/research_program/anchored_defect_20260914/replay.py
```

To materialize every tree node and every retained zero label:

```
python -B collatz_reconstruction/research_program/anchored_defect_20260914/anchored_cycles.py --full-cover --output cover.json
```

The full-tree hash, independent witness hash, example actual paths, all period endpoints, and rejected controls are retained in `verification.json`. The generator, independently enumerated fiber checks, and repeated-division interpreter are supplied in full.

## Sources and attribution

**[S]** The supplied Split-Zero support extension, used in the pinned Collatz `split_zero_history_20260913/note.tex`, subsection “Support, specialization, and what each forgets.” Equation (S1) proves the representation used here. User direction is retained as Split-Zero cohomology and the related exact-map technique; an earlier speech-to-text acronym is not used as a mathematical attribution.

**[P]** Pinned Collatz `cycle_relative_cohomology_20260914/note.md`, Sections 1, 5 and 6: original marked cycle complex, actual relative graph and chain retractions. `residual_splice_20260914/note.md`, Theorem 4 and the executed 99779 source bound; `integral_blocks.md`, equations B5-B13 and its integral affine inverse. All are retained unchanged and replayed.

**[Z]** The connected peer Zeta `CURRENT_RESEARCH.md`, blob `9eefdcb14ca6fa22efb29fd60a01429512bfbadc`, read 14 September 2026, opens with original Gamma volumes, intrinsic sums, period Gram matrices and section-corrected residuals. This current programme context is not a premise of Theorems P or Q. No Zeta file is changed.

**[R]** O. Rozier and C. Terracol, *Paradoxical behavior in Collatz sequences*, arXiv:2502.00948v5, 17 May 2026, Introduction and equation (2), `https://arxiv.org/html/2502.00948v5`. The shortened-clock affine expression maps to ours by expanding each odd-return a into one odd shortened step followed by a-1 even steps: shortened length is A, odd count is m, and the remainder is C/U. This explicit comparison places the coefficient/offset calculation in the existing literature. Their conjectural global assertions and numerical bounds are not premises here. No priority claim for affine coding, cycle products, or elementary cohomological algebra is made.
