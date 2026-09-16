# Global height reduction: sharp crossing windows and original coalescence maps

16 September 2026. Additive continuation of `KokunoYumeto/collatz-workbench`, read at
`9afcbe2dc9bace77c1ae705b1cd128da22fe8f8b` (PR #2). The source mathematical object is
the original absolute integral first-jet complex in `intrinsic_zero_firstjet_20260915`.
The immediately preceding local `global_cylinder_control_20260916` is preserved; its
all-word power-gap proof is not a dependency of the new results below. In particular,
this increment uses no Matveev estimate, floating-point logarithm or unproved
comparison imported from the Zeta programme.

The results are: a sharp envelope for **every first coefficient crossing**; a complete
finite-window reduction valid at every chosen depth; a computer-assisted theorem
through 10,280 odd steps, for unbounded starting integers; an exact affine calculus
of **all two-path coalescence families**; and a global integral chain retraction using
both directions of original equation relations. A newly proved infinite coalescence
family removes previously retained arithmetic roots that have no incoming Collatz
edge. The remaining roots and their modules are not declared zero.

## 1. Original maps, clocks, and attribution

Write
\[
 X=\{1,3,5,\ldots\},\qquad T(n)=\frac{3n+1}{2^{a(n)}},\qquad a(n)=\nu_2(3n+1).
\]
For a finite ordered exponent word \(p=(a_1,\ldots,a_m)\), retain
\[
 A_j=\sum_{i=1}^j a_i,\quad U_p=2^{A_m},\quad L_p=3^m,\quad
 C_p=\sum_{j=0}^{m-1}3^{m-1-j}2^{A_j},\qquad f_p(x)=\frac{L_px+C_p}{U_p}.       \tag{1}
\]
The empty word has \((m,A,L,U,C)=(0,0,1,1,0)\). Its source and target are the same
positive odd integer. Nonempty words use the original chronological order.

The source cylinder and image are
\[
 n=\rho_p+2U_p t\longmapsto \eta_p+2L_p t,\quad t\in\mathbb Z_{\ge0},
\]
\[
 \rho_p\equiv(U_p-C_p)L_p^{-1}\pmod{2U_p},\quad0<\rho_p<2U_p,
 \qquad\eta_p=(L_p\rho_p+C_p)/U_p.                            \tag{2}
\]
For the empty word, \(\rho=\eta=1\). Original intermediate oddness follows from
terminal oddness: modulo \(2^{A_j+1}\), the full numerator separates into the original
prefix numerator times an odd power of three and its next term \(3^{m-j-1}2^{A_j}\).
All subsequent terms vanish. This gives
\(3^j n+C_j\equiv2^{A_j}\pmod{2^{A_j+1}}\). The consecutive prefix equations now give
each exact valuation \(a_j\). Positivity propagates from the positive initial value.
This proves the full source assertion in (2), not merely an end-value divisibility.
The two inverse parameters are the source difference divided by \(2U_p\) and the
target difference divided by \(2L_p\), on their displayed images.

For comparison with Terras's coefficient-stopping-time question, define the shortened
map
\[
 S(n)=\begin{cases}(3n+1)/2&n\text{ odd},\\n/2&n\text{ even}.\end{cases}
\]
An odd-return edge of exponent \(a\) expands to one shortened odd step and \(a-1\)
shortened even steps. Thus \(T^j(n)=S^{A_j}(n)\); the parity block is
\(1\,0^{a-1}\). Parsing at successive odd terms is the inverse. A shortened first
coefficient crossing can occur before all the last even divisions have finished;
that intermediate endpoint must be checked separately. It is not automatically the
last odd endpoint. We do check it.

The coefficient-stopping-time conjecture and the study of contracting but
non-descending segments are established parts of the literature [RT]. The affine
cylinder mechanism and the first-jet receiver are inherited workbench constructions.
No priority claim for inverse iteration, common-future equivalence or that literature
is made. The following formulas and proof certificates give the scope of this
continuation.

## 2. The sharp first-crossing envelope at every depth

Set
\[
 b_j=\lfloor\log_2 3^j\rfloor=\operatorname{bitlength}(3^j)-1,\quad b_0=0,
\]
\[
 C_m^*=\sum_{j=0}^{m-1}3^{m-1-j}2^{b_j},\qquad
 D_m^*=2^{b_m+1}-3^m>0,\qquad \Theta_m=C_m^*/D_m^*.           \tag{3}
\]
The logarithm in this notation is never numerically evaluated. Integer powers and
bit lengths give every value. The exact recurrence is
\[
 C_0^*=0,\qquad C_m^*=3C_{m-1}^*+2^{b_{m-1}}.                \tag{4}
\]

### Theorem 1. Sharp, all-depth numerator and exception envelope

For every original word with its first odd-return coefficient crossing at return
\(m\), one has
\[
 A_j\le b_j\ (j<m),\quad A_m\ge b_m+1,
\qquad \frac{C_p}{2^{A_m}-3^m}\le\Theta_m.                   \tag{5}
\]
The maximum in (5), over all such words, is exactly \(\Theta_m\), attained by the
unique ordered word
\[
 p_m^*=(b_1-b_0,\ldots,b_{m-1}-b_{m-2},b_m+1-b_{m-1}).       \tag{6}
\]
Every non-descending original source at that first crossing satisfies
\[
 n\le\lfloor\Theta_m\rfloor.                              \tag{7}
\]
The same bound applies at the **earlier shortened-map first crossing**, with its
possibly even endpoint.

**Proof.** Before a crossing, \(2^{A_j}<3^j\), which is exactly the first set of
integer inequalities. At the first crossing the denominator is at least
\(D_m^*\). The entire numerator difference is
\[
 C_m^*-C_p=\sum_{j=0}^{m-1}3^{m-1-j}(2^{b_j}-2^{A_j})\ge0.   \tag{8}
\]
All coefficients are retained in this identity. Positivity of numerator and denominator
proves (5). Equality requires every summand of (8) to vanish and the final exponent
sum to be \(b_m+1\). This is exactly (6). Its proper exponent increments are one or
two; its last increment is two or three. The word has a nonempty actual cylinder by
(2), and all its proper multipliers are above one. This proves attainment and uniqueness
on the stated word domain. It does not identify different word cylinders or claim that
the maximizing cylinder has an actual non-descending point.

The original endpoint difference is
\((C_p-(2^{A_m}-3^m)n)/2^{A_m}\), proving (7). For the shortened map, the first crossing
with \(m\) odd steps is at exactly \(b_m+1\) total shortened steps. All earlier completed
odd-return prefix sums satisfy the same inequalities. Truncating the last division run
at \(b_m+1-A_{m-1}\) retains the identical numerator \(C_p\); its denominator is exactly
\(2^{b_m+1}\). Equation (8) therefore applies again, even when the intermediate endpoint
is even. QED.

The comparison here is the identity on the formal input with the explicit coefficient
order (8). It is an inequality, not an equivalence replacing the original branch by the
critical branch. The maximizing word and its cylinder remain distinct declared data.

### Theorem 2. Complete finite-window reduction

For every chosen integer \(M\ge1\), put
\[
 H_M=\max_{1\le m\le M}\lfloor\Theta_m\rfloor.               \tag{9}
\]
All failures of first-coefficient-crossing descent with at most \(M\) odd steps are
contained in the original odd source interval \(1\le n\le H_M\). For every \(n>H_M\),
a first crossing within that horizon is an actual first strict descent, both in the
shortened map and at the subsequent odd endpoint.

**Proof.** Equation (7) excludes non-descent outside that finite interval. Every proper
shortened prefix has coefficient at least one and a nonnegative additive remainder,
so it has not strictly descended. For an odd source the remainder is positive after
the first odd step. The later divisions down to the odd endpoint only decrease that
already smaller value. This establishes both notions of first descent with their
proper clocks. The domain of a source that has no crossing by this horizon remains
unresolved; it is not accepted as convergent or divergent. QED.

A finite verification for a horizon is therefore available by testing these finitely
many original sources for that horizon. The high-throughput scan delivered here proves
the stronger fact that every tested source actually crosses and descends by a much
smaller measured number of returns. It does not infer that fact for untested sources.

The envelope itself cannot be capped at a universal constant: since
\[
 \frac{C_m^*}{3^m}=\frac13\sum_{j=0}^{m-1}\frac{2^{b_j}}{3^j}>\frac m6,
 \qquad 0<D_m^*/3^m<1,
\]
one has \(\Theta_m>m/6\). This concerns the sharp coefficient threshold, not the
existence of actual exceptions at that threshold.

## 3. Complete certificate through 10,280 odd steps

The exact recurrence (4) gives
\[
 H_{10280}=5624777,\qquad
 (m,b_m+1,\lfloor\Theta_m\rfloor)=(9616,15241,5624777)
\]
at its largest record. The next record is
\[
 (10281,16295,6728242).                                    \tag{10}
\]
`envelope.json` retains every row and the full critical-prefix-sum dictionary. Its
integer-state hash includes the complete numerator and denominator at every row,
encoded as length-delimited positive big-endian integers. Those large coefficients
are regenerated exactly; a floating-point approximation never chooses a record.

The source ledger contains **every one of the 2,812,388 positive odd sources** from
3 through 5,624,777 in strict order. Each row is `[n, endpoint, ordered_exponents]`.
It records an actual first odd-return coefficient crossing and strict descent. The
checker also examines the earlier shortened first crossing: at row end with exponent
sum A and m odd steps, that value is
\[
 x_{\rm short}=T^m(n)\,2^{A-(b_m+1)}.                       \tag{11}
\]
It is checked to be strictly below n, rather than inferred from the odd endpoint.

The full independent checker imports neither `height_control.py` nor a predecessor.
It reconstructs (3)-(4) through the original critical floor-prefix affine path, reads
every ledger row, checks the exact consecutive source labels, repeats every division,
and checks all proper coefficient prefixes. It replays **9,808,846 original odd-return
equations and 19,623,792 divisions**. The longest first crossing in this finite source
interval has 141 odd steps (224 shortened steps), at source 1,126,015. These measured
values do not replace the proved horizon 10,280 in Theorem 2.

It follows from Theorems 1-2 and the complete finite certificate that
\[
 \boxed{\text{Every positive source }n\ge2\text{ whose first shortened coefficient
 crossing uses at most }10280\text{ odd steps descends at that crossing.}}          \tag{12}
\]
Even sources descend on their first division. The source 1 is retained separately:
its odd-return loop is the actual fixed point and never strictly descends. The
statement also implies the corresponding first odd-return crossing theorem. This is
a finite-horizon theorem on **unbounded starting integers and unbounded final
valuations**, not the global coefficient-stopping-time conjecture.

Each source-row endpoint is a smaller positive odd integer in the same scanned interval.
The recursive height
\(h(n)=m(n)+h(T^{m(n)}(n)),h(1)=0\) is consequently defined by finite induction in
increasing n. It constructs a finite arrival path for every scanned source. The maximum
inductively obtained total is 222 odd returns, at 3,732,423. No guessed stopping time is
used as a premise: each decrease and each height-table index is checked. The maximum odd
vertex in the retained first-crossing paths is 439,600,764,977, on the row for 4,637,979;
that maximum is not a contiguous verified source interval.

For comparison, the horizon 18 has integer ceiling 108, so only odd sources through 107
are needed to test its possible anomalies. The preceding local contribution's complete
1,166,058-prefix audit remains correct and retained, but that exponential tree is no
longer needed for this particular bounded-horizon question.

This calculation intersects Terras's coefficient-stopping-time problem [RT]. No new
record relative to published large-start verifications, no global proof, and no claim
to originate that problem is made.

## 4. The original Split-Zero comparison and its arithmetic height filtration

Use the inherited **absolute** original graph, not a quotient deleting the fixed loop:
\[
 C^0=\mathbb Z^{(X)},\quad C^1=\mathbb Z^{(X)},\quad
 Je_n=V_n,\quad Pe_n=V_{T(n)},\quad d=J-P.
\]
Parentheses denote finite sums. Over
\(\mathbb D=\mathbb Z[\epsilon]/(\epsilon^2)\), write \(q=1+\epsilon\) and
\[
 d_\epsilon e_n=V_n-qV_{T(n)},\qquad
 q^k=1+k\epsilon\quad(k\in\mathbb Z).                       \tag{13}
\]
The inverse \(q^{-1}=1-\epsilon\) is integral in this stated ring. No nonunit integer
or cycle period is inverted.

The source comparison kernel is
\[
 \mathfrak B_X=\ker\bigl(H^1(K_\epsilon)\longrightarrow H^1(K)\bigr)
 \cong C^1/(dC^0+P\ker d),\qquad [V_n]\longmapsto[\epsilon V_n].                 \tag{14}
\]
The predecessor proves both quotient inverse maps. Its component coordinates are sums
of original coefficients, reduced modulo the actual primitive cycle length m on a
cyclic component, and unreduced on a nonperiodic component. Thus each actual cycle
contributes \(\mathbb Z/m\mathbb Z\), and each actual nonperiodic component contributes
\(\mathbb Z\). The fixed loop m=1 contributes zero through its integral unit relation;
its original support is still present. Neither nonbase indexing set is assumed nonempty.

Set \(\xi_n=[\epsilon V_n]\), and retain the subgroup filtration
\[
 \mathcal F_N=\langle\xi_n:n\le N,\ n\text{ odd}\rangle\subseteq\mathfrak B_X.
                                                                    \tag{15}
\]
Under (14), this is the direct sum of component groups whose least original integer
is at most N. Indeed every \(\xi_n\) is the coordinate generator of its own component,
all vertices of one component have the same generator, and finitely supported sums
meet only finitely many components. These coordinate maps and their inverse
\(1_C\mapsto\xi_{\min C}\) prove the assertion.

Consequently \(\mathcal F_n/\mathcal F_{n-2}\) is zero unless n is the least integer
of a nonbase component. At such a least integer it is exactly that component's
\(\mathbb Z/m\mathbb Z\) or \(\mathbb Z\). This is a filtration of the actual integral
comparison kernel, not a claim that the chain homotopies below preserve the maximum
integer occurring in a raw chain.

A relation \(\xi_n=\xi_m\) with m<n gives zero in this graded quotient but need not
give zero in \(\mathfrak B_X\). Its original lower subgroup, source vectors, and
boundary witness remain. This distinction is exactly a retained supported-zero
comparison, and is not an assertion about chronological automata histories.

The rows in Section 3 give \(d_\epsilon(\epsilon B_n)=\epsilon V_n-\epsilon V_y\)
with y<n. Concatenation with the smaller-source witness produces the original
integral certificate
\[
 d_\epsilon(-e_1+\epsilon c_n)=\epsilon V_n.                \tag{16}
\]
The fixed loop supplies the constant term. The unchanged predecessor checker receives
and extracts point examples from these certificates. The finite source scan proves
\(\mathcal F_{5624777}=0\), with its original source ledger retained.

## 5. Every expanding word supplies a complete inverse height reduction

Take any original nonempty word p with \(L_p>U_p\). Its inverse on its **actual
positive target image** is
\[
 n=\eta_p+2L_p t\quad\rightsquigarrow\quad
 x=\rho_p+2U_p t=\frac{U_pn-C_p}{L_p},\qquad t\ge0.         \tag{17}
\]
It satisfies \(0<x<n\) throughout. Equivalently, the target image consists exactly of
odd positive n with \(U_pn\equiv C_p\pmod{L_p}\) and \(n>C_p/U_p\).
Integrality and oddness recover the complete source word by (2).

This reduction follows an original path **from x to n**, not from n to x. The
parameter inverses are \((n-\eta_p)/(2L_p)\) and \((x-\rho_p)/(2U_p)\) on the stated
images. It is therefore legitimate for component-height induction even before an
actual forward descent from n is known.

For the original weighted path
\(P_p(x)=\sum_{j=0}^{m-1}q^j e_{T^j(x)}\),
\[
 d_\epsilon P_p(x)=V_x-q^mV_n,
\quad
 d_\epsilon(-q^{-m}P_p(x))=V_n-q^{-m}V_x.                 \tag{18}
\]
Multiplication by epsilon gives \(\xi_n=\xi_x\). The reverse clock is retained as the
integer coefficient \(-m\), not reset to one.

For example, the original word (1,2) gives
\[
 13+18t\rightsquigarrow11+16t,
\]
with the original two-step path in the opposite direction. In particular
27 -> 41 -> 31 gives the height reduction 31 -> 27. Its exact chain is
\[
 -(1-2\epsilon)e_{27}-(1-\epsilon)e_{41},
\]
with boundary \(V_{31}-(1-2\epsilon)V_{27}\).

## 6. All shared-future reductions have an exact integral parameterization

Take **any two finite original words**, including the empty word, called l and r.
Their complete source/image pairs are (2). Put
\[
 g=\gcd(L_l,L_r)=3^{\min(|l|,|r|)}.
\]
Their target images intersect exactly when
\[
 \eta_l\equiv\eta_r\pmod{2g}.                            \tag{19}
\]
No independence of the two sources is assumed. Both target steps are retained.
A compatible intersection has period
\(P=2L_lL_r/g\). Let y0 be the least member of the common congruence class at least
\(\max(\eta_l,\eta_r)\). Define
\[
 u_0=(y_0-\eta_l)/(2L_l),\quad v_0=(y_0-\eta_r)/(2L_r),
\]
\[
 n_0=\rho_l+2U_lu_0,\qquad m_0=\rho_r+2U_rv_0.
\]
Then **every pair of positive original sources with this common-word endpoint** is
\[
 \boxed{
 \begin{aligned}
 n(t)&=n_0+2U_l(L_r/g)t,\\
 m(t)&=m_0+2U_r(L_l/g)t,\\
 y(t)&=y_0+2(L_lL_r/g)t,
 \qquad t\in\mathbb Z_{\ge0}.
 \end{aligned}}                                                   \tag{20}
\]
The inverse is \(t=(y-y_0)/P\); the source and original image-parameter inverses in
(2) give the same t. To prove completeness, subtract the target equations to obtain
\(L_lu-L_rv=(\eta_r-\eta_l)/2\). Its homogeneous integral solutions are
\((L_r/g,L_l/g)t\). Positivity of both original parameters chooses precisely the least
common target y0 and t>=0. This also proves (19) and both inverse descriptions.

The strict height domain n(t)>m(t) is an exact integer interval. With
\[
 a=n_0-m_0,\qquad b=2(U_lL_r-U_rL_l)/g,
\]
it is: \(t\ge\max(0,\lfloor-a/b\rfloor+1)\) for b>0; all t>=0 or none according to
a>0 for b=0; and \(0\le t\le\lfloor(a-1)/(-b)\rfloor\) for b<0,a>0, otherwise none.
Incompatible and empty-height faces remain declared records, rather than being
identified with absent input data.

Let \(P_l(n),P_r(m)\) be the two original weighted chains to y(t), and
\(k=|l|-|r|\). The full chain comparison is
\[
 \boxed{d_\epsilon\bigl(P_l(n)-q^kP_r(m)\bigr)=V_n-q^kV_m.}   \tag{21}
\]
All common-target terms cancel with their original clock. The result is a relation
between original sources, not a claim that either source vanishes. In the retained
kernel, multiplying (21) by epsilon gives \(\xi_n=\xi_m\).

This family calculus is complete for lower-component comparisons. Two vertices of a
functional graph lie in one weak component exactly when their forward paths meet.
Adjacent vertices have that property; it is transitive because two meetings on the
same intermediate orbit have a later common meeting. Conversely a common endpoint
gives an undirected path. Therefore every original n whose component has a smaller
integer occurs in one of the strict domains (20). A finite search need not find all
such pairs within a predetermined word bound, and no global coverage assertion is
made from that completeness characterization.

## 7. A newly eliminated infinite family of formerly retained roots

Choose
\[
 l=(1),\qquad r=(1,1,1,1,1,2,3).
\]
Equation (20) gives
\[
 \boxed{1731+2916t\rightsquigarrow1215+2048t,\qquad t\ge0.}   \tag{22}
\]
The original paths, including all affine coefficients, are
\[
 1731+2916t\longrightarrow2597+4374t
\]
and
\[
 \begin{aligned}
 1215+2048t&\longrightarrow1823+3072t\longrightarrow2735+4608t\\
 &\longrightarrow4103+6912t\longrightarrow6155+10368t\\
 &\longrightarrow9233+15552t\longrightarrow6925+11664t
 \longrightarrow2597+4374t.
 \end{aligned}
\]
Every displayed constant is odd and every slope is even. Direct substitution into
\(3x+1=2^ay\) proves the exact valuations on the whole nonnegative integer parameter
domain. The height difference is \(516+868t>0\). This is a family proof, not an
extrapolation from its anchor.

The signed first-jet clock is -6. At t=0 the retained chain is
\[
 e_{1731}-(1-6\epsilon)e_{1215}-(1-5\epsilon)e_{1823}
 -(1-4\epsilon)e_{2735}-(1-3\epsilon)e_{4103}
 -(1-2\epsilon)e_{6155}-(1-\epsilon)e_{9233}-e_{6925},
\]
whose boundary is \(V_{1731}-(1-6\epsilon)V_{1215}\). Formula (21) supplies the identical
coefficient pattern at every parameter.

Each left source is divisible by three. It has **no incoming original Collatz edge**:
\(2^{a(x)}T(x)=3x+1\) is 1 modulo three, so T(x) is never 0 modulo three. Thus this
new lower-source relation cannot be supplied by an ancestor of the left source.
It uses the two original legs meeting later. At parameters divisible by three the
right source is also divisible by three, so neither distinct source is a forward
iterate of the other. Their common endpoint and (21), rather than a fabricated
reverse Collatz edge, prove the relation.

## 8. A genuine whole-source finite-column retraction

Fix the following **explicit** reduction rules, in order, for n>1:

1. Take the original one-return edge when its endpoint is smaller (equivalently,
   n=1 modulo four).
2. Otherwise use the inverse of the original expanding words (1), (1,2), and
   (1,1,1,2,1,1,4), in that order, on their exact images (17).
3. Otherwise use the coalescence family (22).
4. Retain n as an arithmetic root.

Leave 1 as the specified base root with its original loop still present. Every rule
has a smaller positive integer endpoint, so the recursion terminates for **every
original input**, without assuming Collatz. It need not terminate at 1.

For a rule n -> m write B_n for its exact chain (forward, inverse, or shared-future)
and k_n for its signed clock; each satisfies
\[
 d_\epsilon B_n=V_n-q^{k_n}V_m.                             \tag{23}
\]
Define recursively
\[
 H(V_n)=B_n+q^{k_n}H(V_m),\qquad Q(V_n)=q^{k_n}Q(V_m),
\]
with H(V_r)=0,Q(V_r)=V_r at a root. Every column is a finite original edge vector.
Its original intermediate vertices may be larger than n; the proof uses the decreasing
rule endpoints, not a false monotonicity assertion for all those vertices.
Set
\[
 F=I-Hd_\epsilon\quad\text{on edge vectors}.
\]

### Theorem 3. Integral chain retraction with all original obstructions retained

On the full original finite-support D-modules,
\[
 d_\epsilon H=I-Q,\quad Q^2=Q,\quad HQ=0,
\]
\[
 d_\epsilon F=Qd_\epsilon,\quad F^2=F,\quad FH=0,
 \qquad Hd_\epsilon=I-F.                                  \tag{24}
\]
Thus the image complex \([\operatorname{im}F\to\operatorname{im}Q]\), with its inclusion
and projections F,Q, is a chain-homotopy retract of the original complex over D.

**Proof.** Equation (23) telescopes under the decreasing recursion to give the first
identity. Roots have H=0 and Q=identity, so Q is idempotent and HQ=0. Applying d to
F gives Qd. Next \(F^2=I-2Hd+HdHd\); substitution of dH=I-Q and HQ=0 gives F^2=F.
The same substitution gives FH=H-HdH=HQ=0. The last identity is the definition of F.
The projection and inclusion compositions are now identities on the image, and (24)
provides the original homotopy on both degrees. All coefficients are integral dual
numbers. QED.

The image in vertex degree is the free D-module on retained original roots. In edge
degree it is not silently replaced by a free graph with independent projected edge
symbols. Its exact presentation is
\[
 C^0_{\mathbb D}/\operatorname{im}H\ \xrightarrow{\sim}\ \operatorname{im}F,
 \quad[e]\mapsto Fe,                                      \tag{25}
\]
with inverse Fe mapped to [e]. Indeed ker F=im H: inclusion follows from FH=0, and
Fe=0 gives e=Hd e. This retains the original relations between projected edge columns.

At a declared finite equation set E, include its original target vertices, then add
the finite original supports of H on those vertices. Call the result Sigma(E).
Sigma preserves unions and inclusions. The displayed maps are typed on these enlarged
supports; compositions are compared in the next such enlargement, without assuming
Sigma(E) is a finite invariant closure. The global finite-support modules are their
union. Thus the support transitions, zero coefficients and all source equations remain
available in the Split-Zero reconstruction.

The reduction of every coefficient q^k is 1, and the selected arithmetic rules do not
depend on epsilon. Reducing H, Q and F coefficientwise therefore gives the same
constructed maps on the original integer incidence complex. The squares with constant
reduction commute on each original basis vector and thus on all finite sums. The
retraction preserves the full first-jet cohomology and its reduction map, hence
both the finite period-index part and the free nonperiodic part of (14). This is not
based on dimension alone. The original fixed edge satisfies F(e_1)=e_1, since
\(d_\epsilon e_1=-\epsilon V_1\) and H(V_1)=0. On a longer actual cycle, its period
holonomy remains \(1-q^m=-m\epsilon\); no division by m occurs.

### Exact old/new comparison for the new shared-future family

Let H0,Q0,F0 use rules 1-2 only, and H1,Q1,F1 also use (22). The earlier rules have
priority and are unchanged. The new rule acts only at old roots. Append the old
reduction of its endpoint m to its original chain, retaining its q-power. This gives
a chain Gamma between two old roots, hence F0 Gamma=Gamma by (24). The accumulated
correction K=H1-H0 is a finite sum of these chains with the old clock factors. Therefore
\[
 d_\epsilon K=Q_0-Q_1,\quad F_0K=K,
\quad F_1F_0=F_0F_1=F_1,\quad Q_1Q_0=Q_0Q_1=Q_1.           \tag{26}
\]
For the last identities one can also follow the unchanged old route first and then the
new routes at its root; that is exactly the full new route. The edge identities follow
by F_i=I-H_i d, F0K=K and the same root equations. The proof uses actual concatenated
chains, not a rank estimate.

## 9. The exact remaining arithmetic root set

After rules 1-2, n>1 is a root precisely when
\[
 n\bmod36\in\{3,7,15,19,27\},\qquad n\not\equiv8731\pmod{8748}.                \tag{27}
\]
After the new family (22), add
\[
 n\not\equiv1731\pmod{2916}.                              \tag{28}
\]
Together with the actual base 1, these are the complete roots of the fixed global
retraction.

To verify the residue calculation, rule 1 removes n=1 modulo four. On the remaining
n=3 modulo four, the inverse of (1) removes n=2 modulo three. The inverse of (1,2) is
\((8n-5)/9\), removing n=4 modulo nine, i.e. n=31 modulo36 in that remaining set.
The third inverse is \((2048n-2363)/2187\), with n=-17 modulo2187. Intersecting with
n=3 modulo four gives n=8731 modulo8748. Its smallest remaining source is already
positive in the inverse domain, so no small positive exception is omitted. Finally
(22) removes exactly the class (28), which lies in the old residue class 3 modulo36
and is disjoint from the -17 class. There are 1,214 old and 1,211 new nonbase root
residues in one period 8,748. These counts describe the **specified reduction rule**,
not a density estimate for counterexamples or for all unresolved Collatz sources.

Every nonbase component minimum must survive (27)-(28), because each accepted rule
relates it by actual common-future paths to a smaller member of the same component.
By Section 3 that minimum must also exceed 5,624,777, and it cannot have a first
coefficient crossing with at most 10,280 odd steps. These are necessary restrictions,
not a proof that the remaining root set is empty or that its elements are counterexamples.

## 10. What remains globally

The new proofs and certificates eliminate a broad class of source questions, but their
remaining quantifiers are explicit. The all-depth envelope is established; its finite
source verification has the delivered horizon. The global chain retraction is
established; its roots are the nonempty explicit set (27)-(28). The all-pair coalescence
calculus is established; applicability of lower-source comparisons on every remaining
nonbase root is not proved here.

The next useful arithmetic tasks are on those roots: extend the complete source-window
certificate at its next record, find further whole shared-future families with exact
parameter domains, or control the ordinary-integer support of the surviving infinite
noncrossing paths. Formula (20) allows complete non-coprime target synchronization,
including order, coefficients and domains, rather than matching only a trajectory word.
Any new rule can be attached through (26), preserving its full original kernel.

A finite residual diagram with open frontier is not an infinite nonperiodic witness.
A class transported to a smaller-source subgroup is not automatically zero. All bounded
source rows here have independent finite certificates; no rule uses a heuristic
probability, a discarded affine term, or an assumed finite stopping time.

## 11. Implementation and acceptance

`height_control.py` implements (1)-(28), including exact image intersections, both
source parameterizations, signed D-coefficients, the two retractions and declared
arithmetic roots. `verify.py` checks the formulas on a complete exponent-sum-16 word
domain (65,535 words), every row of the 10,280-depth envelope, a complete small pair-word
domain, both support/retraction compositions, the full affine-family coefficients and
false-certificate rejection. Those are structural regression scopes, not a replacement
for the written general proofs.

`scan_sources.py` constructs the complete 2,812,388-row source certificate and an
inductive height table. `audit_sources.py` is separately implemented and imports no
contribution module. Its replay repeats every original division and checks the source
index sequence, shortened coefficient time, original endpoint, descent and induction.
The ledger hash records the entire original row stream, not an unspecified statistical
summary. Both ordinary and optimized structural and source executions are compared
byte for byte. The full proof scan and the named structural checks have separate counts.

The authentic first-jet receiver is pinned by Git blob
`97f9ef5ad535f7ec18259d41fab6a3557be17d98`. Its source is retained byte for byte.
The new finite examples are accepted by its integral validator. No new Lean run or
independent external mathematical review is claimed. Repository publication status is
in a separate receipt, not inferred from local tests.

## 12. Sources and scoped attribution

[WB] KokunoYumeto, `collatz-workbench`, PR #2 at
`9afcbe2dc9bace77c1ae705b1cd128da22fe8f8b`.
`collatz_reconstruction/research_program/intrinsic_zero_firstjet_20260915/note.md`,
Sections 3-9, and its `firstjet.py`. These supply the absolute comparison kernel,
original integral witness equations and source support conventions.
https://github.com/KokunoYumeto/collatz-workbench/tree/9afcbe2dc9bace77c1ae705b1cd128da22fe8f8b/collatz_reconstruction/research_program/intrinsic_zero_firstjet_20260915

[PREV] The supplied local `Collatz_Global_Cylinder_Proof.md` and its full archived
source, `global_cylinder_control_20260916`. Read in full for continuation. Its generic
contracting-word singleton theorem and earlier 18-return audit remain preserved. The
new first-crossing envelope is proved directly and does not use its logarithm bound.

[RT] Olivier Rozier and Claude Terracol, *Paradoxical behavior in Collatz sequences*,
arXiv:2502.00948v3 (15 March 2025), Introduction and Section 2; the current v5
(17 May 2026), Introduction, Definitions 1.1-1.2 and Section 2, was also checked.
Journal reference: Discrete Mathematics 349 (2026), 115167. It states the original
coefficient-stopping-time problem and analyzes the affine remainder of parity vectors.
The shortened/odd-return correspondence used here is proved in Section 1 above.
https://arxiv.org/html/2502.00948v3
https://arxiv.org/html/2502.00948v5

[INV] Guenther J. Wirsching, *On the problem of positive predecessor density in 3n+1
dynamics*, Discrete and Continuous Dynamical Systems 9 (2003), 771-787,
DOI 10.3934/dcds.2003.9.771. Cited as prior inverse-iteration context, not as a source
of a bound or a theorem used in this proof. No exhaustive priority survey was made.
https://www.aimsciences.org/article/doi/10.3934/dcds.2003.9.771

Research direction and Split-Zero framework: the owner's programme. New derivations,
source certificates and implementation: this tool-assisted continuation. An elementary
formula or successful test count is not by itself a claim of priority or external review.
