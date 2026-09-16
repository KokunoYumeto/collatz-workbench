# All even interior exponents: complete source templates and budget-preserving root reduction

16 September 2026. Continuation from the original bilateral-root calculation, whose
source has now been integrated into `main` at
`9453b5306b3a897389dece309f9c119dffbcc489` in `KokunoYumeto/collatz-workbench`.
The earlier restriction to interior exponents 2 and 6 is removed on both displayed
template types. All positive even exponents are admitted. The induced ternary
order, exact integer source, and two original paths remain specified.

This note proves a larger family of comparisons, not global Collatz convergence.
A shared-future comparison identifies two original first-jet classes; it is not
necessarily forward iteration from the larger source to the smaller source.
The complete even-exponent test is finite on every original input. One version
preserves the preceding subquadratic support budget by testing actual path
support; another admits the entire enlarged template with its own proved budget.
The old support bound is not silently assigned to the unrestricted version.

## 1. Original source and first-jet receiver

Let \(X=\{1,3,5,\ldots\}\), and use
\[
T(n)=\frac{3n+1}{2^{\nu_2(3n+1)}}.
\]
An exponent word \(w=(a_1,\ldots,a_j)\) retains all its ordered exponents, prefix
sums \(A_i\), and original affine data
\[
L_w=3^j,\qquad U_w=2^{A_j},\qquad
C_w=\sum_{i=0}^{j-1}3^{j-1-i}2^{A_i},\qquad
f_w(n)=\frac{L_wn+C_w}{U_w}.
\]
Its complete positive source is the odd-terminal congruence
\[
L_w\rho_w+C_w\equiv U_w\pmod{2U_w},\qquad 0<\rho_w<2U_w,
\]
with progression and image
\[
\rho_w+2U_wt\longmapsto\eta_w+2L_wt,\qquad
\eta_w=(L_w\rho_w+C_w)/U_w,\quad t\ge0.
\]
The original predecessor supplies the exact word/cylinder proof. All valuations
in the new families are also derived independently below.

Keep the absolute original graph, including the fixed vertex and loop at 1. Over
\(\mathbb D=\mathbb Z[\epsilon]/(\epsilon^2)\), put \(q=1+\epsilon\) and
\[
d_\epsilon E_n=V_n-qV_{T(n)},\qquad q^k=1+k\epsilon\quad(k\in\mathbb Z).
\]
The last identity follows for nonnegative k by the binomial formula and for
negative k from the integral inverse \(q^{-1}=1-\epsilon\). No integer period is
inverted. For actual finite paths \(l:n\to y\) and \(r:m\to y\), of lengths s,t,
retain the weighted edge columns B_l,B_r. Their literal boundary identity is
\[
d_\epsilon\bigl(B_l(n)-q^{s-t}B_r(m)\bigr)=V_n-q^{s-t}V_m. \tag{1}
\]
Multiplying by epsilon identifies the original reduction-kernel classes
\(\xi_n=[\epsilon V_n]\) and \(\xi_m\). It does not certify their vanishing.
Every support label below is the set of original equations used, with its full
coefficient module and incoming relation map. It is not an automata word label.

## 2. The previously omitted ternary orders

For every even integer e>=2 define
\[
h_e=\frac{2^e+2}{3},\qquad t_e=\nu_3(h_e).
\]
The numerator is divisible by 3, h_e is positive, and h_e=2 modulo 4.

**Lemma 1.** For every such e,
\[
\boxed{t_e=\nu_3(e-1).} \tag{2}
\]

**Proof.** Set k=e-1, which is odd. Then
\(2^e+2=2(1-(-2)^k)\). For k coprime to 3, expansion of
\((1-3)^k\) modulo 9 gives \(1-(-2)^k=3k\) modulo 9, with valuation one.
For any integer x=1 modulo 3, write x=1+3z. Then
\(x^2+x+1=3(1+3z+3z^2)\) has valuation one. Factoring
\(x^3-1=(x-1)(x^2+x+1)\) therefore increases the valuation by exactly one
on cubing. Write k=3^r k_0 with 3 not dividing k_0 and iterate the factorization.
It gives \(\nu_3(1-(-2)^k)=1+r\). Division by 3 in h_e proves (2). QED.

In particular e=4 contributes t_e=1 and e=10 contributes t_e=2. Treating their
h_e as ternary units would put the family on the wrong original source layer.
The earlier values e=2,6 both have t_e=0 and are recovered by (2).

## 3. One exact family for every even exponent and tail length

Take b>=1, even e>=2, and a selector \(\sigma\in\{0,1\}\). Define
\[
a=a(b,e,\sigma)=\min\{a\ge1:2^{a+e+2b-\sigma}<3^{a+b}\},
\quad J=2^{e+2b-\sigma},\quad Q=3^{a+b},\quad K=2^aJ<Q. \tag{3}
\]
The minimum exists. At \(a=b+2e-2\sigma\), the ratio K/Q equals
\((8/9)^{b+e-\sigma}<1\), so
\[
a\le b+2e-2\sigma. \tag{4}
\]
Also a>=e. Indeed a<=e-1 would give
\((3/2)^a<2^{e-1}\), whereas (3) requires
\((3/2)^a>2^{e-\sigma}(4/3)^b>2^{e-1}\).
Since h_e<3^e, it follows that a>t_e.

For sigma=0 retain left word (1) and the residue n=3 modulo 4. For sigma=1 retain
left word (1,2,1) and the residue n=27 modulo 32. Write these dyadic data as
\((d_\sigma,r_\sigma)=(4,3)\) or \((32,27)\).
The complete larger-source domain is
\[
\mathcal E_{b,e,\sigma}=\{n>0:n\equiv r_\sigma\pmod{d_\sigma},
\quad Jn+h_e3^b\equiv0\pmod Q\}. \tag{5}
\]
Because J is a unit modulo Q, the second condition is one residue modulo Q.
CRT with the dyadic condition has one representative n_0 in (0,d_sigma Q).

Put
\[
m_0=\frac{Kn_0+2^ah_e3^b}{Q}-1,
\qquad y_0=f_{l_\sigma}(n_0).
\]
Then the complete pair and its common image are
\[
\boxed{\begin{aligned}
n(v)&=n_0+d_\sigma Qv,\\
m(v)&=m_0+d_\sigma Kv,\\
y(v)&=y_0+\frac{L_{l_\sigma}d_\sigma Q}{U_{l_\sigma}}v,
\qquad v\in\mathbb Z_{\ge0}.
\end{aligned}} \tag{6}
\]
The original right word is
\[
w_0=1^a,e,2^{b-1},3,\qquad
w_1=1^a,e,2^{b-1},1,1,3. \tag{7}
\]
Here repeated symbols denote the literal ordered exponents, not powers of a
map after discarding its original intermediate positions.

**Theorem 2.** All pairs (6) satisfy
\[
n(v)\xrightarrow{l_\sigma}y(v)\xleftarrow{w_\sigma}m(v),
\qquad 0<m(v)<n(v),\qquad
\boxed{\nu_3(n(v))=b+t_e.} \tag{8}
\]
Both paths have exactly their displayed valuations. Conversely the equality of
these two original word endpoints, on their positive sources, gives (5)-(6).
The parameter inverse is (n-n_0)/(d_sigma Q), with the same value recovered from
m or y using (6).

**Proof.** From (5), reduction modulo 3^b first gives 3^b dividing n. Write
z=n/3^b. Then Jz+h_e=0 modulo 3^a. Since a>t_e and J is a ternary unit,
\(\nu_3(z)=t_e\), proving the actual layer in (8). The integer
\[
W=\frac{Jz+h_e}{3^a}
\]
is positive and has dyadic valuation one: J is divisible by 8, h_e=2 modulo 4,
and division by 3^a preserves valuation one. Set m=2^aW-1.
After j of the first a original returns the value is
\[
x_j=3^j2^{a-j}W-1\quad(0\le j\le a). \tag{9}
\]
For j<a the valuation of x_j+1 is at least two; therefore the next exponent is
exactly one. At j=a, the value is
\[
x_a=\frac{J}{3^b}n+h_e-1.
\]
The identity 3h_e-2=2^e gives the exact next exponent e and endpoint
\[
1+\frac{2^{2b-\sigma}n}{3^{b-1}}.
\]
After j of the next b-1 steps the value is
\[
1+\frac{2^{2(b-j)-\sigma}n}{3^{b-1-j}}\quad(0\le j\le b-1). \tag{10}
\]
At every nonterminal position of (10), its numerator correction is divisible by
8; hence the next exponent is exactly two. The last value is 4n+1 at sigma=0,
and 2n+1 at sigma=1.

For sigma=0 the final exponent three gives (3n+1)/2, the left endpoint. For
sigma=1 the remaining exact path is
\[
2n+1\xrightarrow1 3n+2\xrightarrow1(9n+7)/2
\xrightarrow3(27n+23)/16.
\]
Its valuations follow from n=27 modulo 32. This is the left word's endpoint.
All values are positive. Reversing the original affine equality gives
\(3^{a+b}W=Jn+h_e3^b\) and hence (5); the original left valuations give the
dyadic residue. This proves completeness and both parameter inverses.

For height, retain the full affine identity
\[
m=(K/Q)n+h_e(2/3)^a-1. \tag{11}
\]
The coefficient K/Q is less than one. Also (3) implies
\[
h_e(2/3)^a<2^{\sigma-e}h_e(3/4)^b
\le \frac{2+2^{2-e}}{3}(3/4)^b<1.
\]
Thus the constant in (11) is negative and m<n. Positivity follows from
m=2^aW-1 with W>=2. QED.

No assertion that the different e-families are disjoint is made. Their overlaps
are calculated by the original congruences or by the full list at each source.
All eligible labels remain in that list, even when only one is selected.

## 4. Removing the apparent infinite search

For a fixed admitted source n, the largest leading run in the same template is
\[
A_{\max}=\nu_3\left(J(n/3^b)+h_e\right). \tag{12}
\]
Every original a' in the exact interval a<=a'<=A_max gives a smaller positive
source
\[
m_{a'}=2^{a'}\frac{J(n/3^b)+h_e}{3^{a'}}-1. \tag{13}
\]
For adjacent values,
\[
m_{a'+1}+1=\frac23(m_{a'}+1),\qquad T(m_{a'+1})=m_{a'}.
\]
The shared-future endpoint is unchanged. The rise endpoint is the same integer
\(J(n/3^b)+h_e-1\); the later right-hand path is unchanged as well. Thus (12)
selects the smallest source within this entire admitted leading-run template.
The exact signed chain correction is obtained by adjoining the original incoming
ones, as in the preceding bilateral note.

**Theorem 3.** The complete set of admitted coefficient-contracting templates
at any positive odd source n is determined by finitely many explicit tests.
For n>1 put
\[
k(n)=\lfloor\log_2(n-1)\rfloor-1,
\qquad B=\nu_3(n).
\]
Only even e with
\[
\boxed{2\le e\le k(n)} \tag{14}
\]
need be tested. For each e, the only possible tail layer is
\[
\boxed{b=B-\nu_3(e-1)\ge1.} \tag{15}
\]
There are at most two support selectors to test at that (b,e). The tests are the
original dyadic residue, a<=k(n), and (5). Thus the number of template labels
examined is at most \(2\lfloor k(n)/2\rfloor\), regardless of how large n is.

**Proof.** Every admitted smaller source has m=2^{a'}W-1 with W>=2 and m<n.
Both sources are odd, so m+1<=n-1. Hence \(2^{a'+1}\le n-1\) and
\(a'\le k(n)\). Since a'>=a>=e, (14) follows. Equation (8) and Lemma 1 give
(15), uniquely. Every admitted template is therefore in the finite list.
Conversely, a successful test of its defining congruences is in Theorem 2's
complete source domain; (12) then gives the maximal run and smallest template
source. These implications prove the exact finite search, rather than merely a
termination heuristic. QED.

This proof handles all even exponents; it does not supply a bound on arbitrary
Collatz stopping times. It eliminates an unnecessary infinite parameter search
within the stated construction.

## 5. A whole new root progression

Take b=2,e=8,sigma=0. Then h=86, t_e=0, a=16, and the original common-future pair is
\[
\boxed{\begin{aligned}
20\,241\,207+1\,549\,681\,956v
&\xrightarrow{1}30\,361\,811+2\,324\,522\,934v\\
&\xleftarrow{1^{16},8,2,3}
14\,024\,703+1\,073\,741\,824v,
\qquad v\ge0.
\end{aligned}} \tag{16}
\]
The exact height difference is
\[
6\,216\,504+475\,940\,132v>0.
\]
The left sources have actual ternary valuation two and no incoming original edge:
3x+1=2^an with 3 dividing n is impossible modulo 3. Both original paths are needed.
At v=0 the right path rises to 9,211,998,293 and then reaches the displayed common
endpoint. The comparison's signed odd-return clock is 1-19=-18.

The complete previous reduction leaves every source of (16) as a root. This is a
finite exact residue certificate, not an extrapolation from its anchor. The old
finite mask has period 5,668,704. Since the new progression has fixed ternary
valuation, the four possible old e=2,6 layer congruences have fixed moduli. Their
least common multiple with the finite-mask period makes the membership of
n_0+n_step v periodic in v with period 8. The checker tests all eight parameter
classes against the full previous mask and all four original congruences. All
eight are roots. Periodicity proves the assertion for every v>=0.

Consequently (16) is additional source coverage beyond both the preceding finite
catalogue and its infinite e=2,6 families. At its anchor the new comparison ends
at the still-retained root 14,024,703. No arrival-at-1 conclusion is inferred from
that class equality.

The other supported source orders are retained as well. For b=1,e=4,sigma=1 the
actual layer is two, not one, and the entire pair is
\[
45\,243+69\,984v\longrightarrow76\,349+118\,098v
\longleftarrow42\,367+65\,536v.
\]
This illustrates the importance of (2); no claim that this smaller family is new
relative to the old finite catalogue is made.

## 6. Budget-preserving and unrestricted global retractions

The primary new retraction first applies every old rule in its original priority.
Only at a retained root does it examine the complete finite list in Theorem 3.
For each candidate it constructs BOTH original paths, their integral chain (1),
and their maximum original vertex. It admits the candidate only when that maximum
is at most the predecessor's proved budget
\[
R_0(n)=\max\{130(n+1),\lfloor64n(4/3)^{\lfloor\log_3n\rfloor}\rfloor+21\}. \tag{17}
\]
Among the admitted candidates it selects the smallest target, with the explicit
word-length and label tie-breakers used in `all_even.py`. Rejected budget faces
are not erased from the full arithmetic candidate list. A source without an
accepted move remains a root.

All selected targets are strictly smaller odd integers. Therefore the procedure
terminates on every original input. For a selected move with chain B_n, target m,
and signed clock j, define
\[
H(V_n)=B_n+q^jH(V_m),\qquad Q(V_n)=q^jQ(V_m),
\qquad F=I-Hd_\epsilon.
\]
At roots use H=0 and Q=I. The exact identities are
\[
d_\epsilon H=I-Q,\quad Q^2=Q,\quad HQ=0,
\quad d_\epsilon F=Qd_\epsilon,\quad F^2=F,\quad FH=0. \tag{18}
\]
The first telescopes (1). The next two follow at roots. Substitution in F proves
the remaining identities. Thus these are an actual finite-column chain-homotopy
retraction, not merely an equality of module ranks.

**Theorem 4.** The budget-preserving extension still uses only original vertices
at most R_0(n) in its H column. For n>=27 the inherited bound
\[
R_0(n)\le64n^{\log_3 4}+21
\]
therefore remains valid.

**Proof.** Every chosen reduction source x is at most the original n. Old moves
have the original bound. The new acceptance test verifies that bound for both
complete original paths at x. The integer function R_0 is nondecreasing, so their
union stays below R_0(n). This also handles cancellation: support is checked on
both paths before equal edge coefficients are collected. QED.

The whole new progression (16) passes this budget. For every n there,
n>=20,241,207>3^15. Its largest right-hand value is
\[
(4096/9)n+85.
\]
The inequality
\[
(4096/9)n+85\le64(4/3)^{15}n+21
\]
holds at n=20,241,207 by integer multiplication and has strictly positive margin
slope. It holds throughout the progression. The floor in (17) does not change
this integer endpoint conclusion. The short left path has smaller values. This
proves the budget acceptance on the entire family, not only at the eight residue
representatives used to test novelty.

For completeness, an unrestricted mode admits every successful template from
Theorem 3. For positive odd n>1 its larger support budget is separately proved:
\[
\boxed{R_*(n)=\max\{130(n+1),\lfloor(n-1)3^{k(n)}/2^{k(n)}\rfloor-1\}.} \tag{19}
\]
At the fixed root n=1, set R_*(1)=1; the homotopy column H(V_1) is zero.
During the initial rising run, m+1<=n-1 and a'<=k(n), so
\(3^{a'}W-1=(3/2)^{a'}(m+1)-1\) is bounded by the second term. The later falling
steps decrease; the bilateral final three-edge segment stays below 5(n+1),
covered by the first term. The finite old paths also obey that first term.
Hence (19) holds along the entire decreasing-source recursion. In real exponents
its second term is at most \((2/3)(n-1)^{\log_2 3}-1\). This is not the smaller
budget (17), and it is not assigned that smaller exponent without the explicit
acceptance test.

Both versions have the integer uncollected-term bound, for positive odd n>1,
\[
K_*(n)=\frac{n-1}{2}\max\{24,k(n)+\lfloor\log_3n\rfloor+6\}. \tag{20}
\]
Set K_*(1)=0 at the fixed root.
There are at most (n-1)/2 strict source reductions. A new pair uses at most
k(n)+floor(log_3 n)+6 edges in total, and the finite older pairs use at most 24.
Every signed q-exponent is bounded in absolute value by that total. Therefore
collected constant coefficients have total absolute sum at most K_*(n), and
first-order coefficients at most K_*(n)^2.

The old route is unchanged until its retained root. Its new tail gives the
comparison K=H_new-H_old, with
\[
d_\epsilon K=Q_{old}-Q_{new},\quad F_{old}K=K,
\quad F_{new}F_{old}=F_{old}F_{new}=F_{new}. \tag{21}
\]
The correction lies in the old projected edge module: its boundary endpoints are
old roots, on which H_old is zero. This proves the displayed F_old identity;
substitution gives both projection compositions. The analogous Q compositions
follow from the fixed old route and the new root endpoints, including all signed
q-factors.

All arithmetic rule choices and budget tests are independent of epsilon. Hence
constant reduction commutes with these maps and transports the integral
first-jet comparison kernel through the actual homotopy equivalence. The fixed
loop stays present. Original periods are not divided out, and a still-open
component is not called absent because a particular comparison sends an amplitude
to supported zero.

## 7. Verification and the still-global task

The exact checker covers both selectors, b=1 through 16, and every even e from 2
through 32. It verifies both original affine coefficient columns at every step,
then checks actual path instances, maximal leading-run recovery, ternary layers,
first-jet boundaries, and support bounds. These are regression fixtures for the
written all-parameter proofs. The finite-search implementation is compared with
a larger direct template search on all odd inputs below 4,000. Retraction tests
verify (18) and (21) on original integral vectors, including newly reduced roots.
The separate affine auditor imports neither the new module nor its predecessor.

The next arithmetic task is the exact residual root set after these additional
families and their budget faces. The finite algorithm for template membership
does not prove that one of its templates applies to every retained source. The
unchanged first-crossing horizon remains 11,610 odd steps in this increment;
no extra crossing-window scan or numerical stopping-time record is claimed.

A complete original singleton primitive would still require a route to the
fixed component, or another proved arithmetic exhaustion of the surviving
comparison kernel. New height relations improve its presented source; they do
not erase it. The cumulative archive keeps the earlier source files and execution
receipts separately from the checks executed for this note.

## Sources and exact provenance

Research direction and Split-Zero framework: the owner's workbench. This is a
continuation developed in the present tool-assisted session, not an external
independent mathematical review or a priority claim.

The mathematical predecessor is
`bilateral_root_bounds_20260916/note.md`, with the earlier original source and
first-jet conventions preserved. The executable predecessor is the unchanged
`bilateral_control.py`, whose SHA-256 is pinned in `SOURCE_INTAKE.json`. Current
GitHub integration and PR state were read on 16 September 2026 at main
`9453b5306b3a897389dece309f9c119dffbcc489`; PR #2 is now merged. No remote write is
inferred from generating this local addition.

For historical terminology, the coefficient-stopping-time question is distinct
from the present template-exhaustion problem. The original expansion of an
odd-return exponent a to one odd shortened step followed by a-1 divisions is the
clock comparison used in earlier notes. Literature attribution remains in those
notes and in Rozier--Terracol, *Paradoxical behavior in Collatz sequences*,
https://arxiv.org/abs/2502.00948. That paper supplies no premise of Theorems 2--4.
