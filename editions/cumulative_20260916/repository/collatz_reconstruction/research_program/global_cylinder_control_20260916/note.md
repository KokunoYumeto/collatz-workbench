# Global cylinder control: arbitrary words, whole crossing tails, and retained singleton defects

16 September 2026. Additive Collatz workbench continuation, read at
`9afcbe2dc9bace77c1ae705b1cd128da22fe8f8b`, PR #2. The construction uses the
original +1 map and the published integral first-jet receiver. It does not
import an unproved estimate from the Zeta programme. The preceding 33-file
local arithmetic/shadow package is not an input. This note makes no priority
claim and no assertion of global Collatz convergence.

The main arithmetic quantifiers run over **all finite exponent words**, not
only the earlier P/Q languages, repeated cores or a bounded switch count.
The price is explicit: one original source can remain at each contracting
cylinder, and at most one original source remains across the entire
unbounded next-exponent crossing tail of a pre-crossing prefix. Those
sources are retained rather than declared zero. A separate finite proof
certificate discharges the first-crossing exception through 18 odd returns.

## 1. Original objects and source maps

Let X be the positive odd integers and

\[
 T(n)=(3n+1)/2^{a(n)},\qquad a(n)=\nu_2(3n+1).
\]

For an ordered nonempty word p=(a_1,...,a_m), a_i>=1, retain

\[
 A_j=\sum_{i=1}^ja_i,\quad A_0=0,\quad
 U=2^{A_m},\quad L=3^m,\quad D=U-L,
\]
\[
 C=C(p)=\sum_{j=0}^{m-1}3^{m-1-j}2^{A_j},\qquad
 f_p(x)=(Lx+C)/U.                                      \tag{1}
\]

The branch order is f_p=g_(a_m)...g_(a_1), g_a(x)=(3x+1)/2^a.
The complete original positive source is

\[
 \mathcal C_p=\{\rho_p+2Ut:t\in\mathbb Z_{\ge0}\},\quad
 \rho_p\equiv(U-C)L^{-1}\pmod{2U},\quad0<\rho_p<2U.       \tag{2}
\]

Its original image is y_p+2Lt, y_p=(L rho_p+C)/U, and both t inverses
are given by the displayed source or target difference divided by its
original step. In particular the target step is not changed to the source
step. The positive representative is odd: U is even and C is odd.

For completeness, the terminal-odd congruence (2) gives all intermediate
oddness conditions. Backwards from an odd last value, the recurrence
3x_j+1=2^(a_(j+1))x_(j+1), together with the prefix formula, shows each
previous numerator divisible by its power of two and every previous x_j
odd. Equivalently, modulo 2^(A_j+1), the composite numerator has its first
j terms plus a last odd contribution 2^A_j. Since every a_i>=1, terms
past that contribution vanish. Dividing the resulting congruence by
2^A_j gives odd x_j. More explicitly, for j<m the complete numerator reduces to
3^(m-j)*(3^j n+C_j)+3^(m-j-1)*2^A_j modulo 2^(A_j+1).
The terminal congruence makes this zero; division by the odd coefficient
and inversion of 3 give 3^j n+C_j congruent to 2^A_j modulo 2^(A_j+1).
The exact recurrence then forces the original valuation a_(j+1).
Positive forward values follow directly from g_a.

An explicit append map, also used by the checker, starts from
n=rho+2Ut and x=y+2Lt. To append exponent a, put

\[
 k\equiv\left(2^{a-1}-(3y+1)/2\right)(3L)^{-1}\pmod{2^a},
 \quad0\le k<2^a.                                      \tag{3}
\]

Then the new anchor is rho+2Uk, the new target is
(3y+1+6Lk)/2^a, and the new coefficients are
L'=3L, U'=2^a U, C'=3C+U. Substituting t=k+2^a v proves the whole
new progression and its inverse. Empty prefix data are
(rho,y,L,U,C)=(1,1,1,1,0); its source is all positive odds.

## 2. A proved global separation of powers

### Theorem 1. All-length separation

For every integer m>=1 and every integer A with 2^A>3^m,

\[
 \boxed{\quad 2^A-3^m>(3/2)^m-1.\quad}                  \tag{4}
\]

This is a computer-assisted theorem with one stated external input,
Matveev's established rational-number logarithm bound [MAT]. The complete
finite part is generated and checked in `power_gap_certificate.json`.
It consists of rational interval inequalities and 127 integer rows, not
a large Collatz-start computation. The general argument follows.

Take A_0=floor(m log(3)/log(2))+1; then A_0<=2m. Increasing A increases
the left side of (4), so it suffices to use A_0. A failure gives

\[
 0<\Lambda=2^{A_0}3^{-m}-1<2^{-m}.                       \tag{5}
\]

Apply [MAT, Theorem 2.1] with its two positive rational numbers 2,3,
integer exponents A_0,-m, and B=2m. Their heights are log 2, log 3.
Its coefficient is dominated by

\[
 (7/5)30^5\,23\,(7/10)(11/10)<10^9,                    \tag{6}
\]

because 2^(9/2)<23, log 2<7/10 and log 3<11/10.
Thus

\[
 -10^9(1+\log(2m))<\log\Lambda<-m\log2<-(2/3)m.        \tag{7}
\]

At m=10^12, use 2*10^12<2^41 and log2<7/10 to get

\[
 (2/3)10^{12}>10^9(1+41\cdot7/10).
\]

The difference (2/3)m-10^9(1+log(2m)) has derivative
2/3-10^9/m>0 for m>=10^12. Hence a failure has m<10^12.

All logarithm bounds are certified by rational series. For x=2 or 3,
z=(x-1)/(x+1), use

\[
 \log x=2\sum_{j=0}^{N-1}\frac{z^{2j+1}}{2j+1}+R_N,
 \quad0<R_N<\frac{2z^{2N+1}}{(2N+1)(1-z^2)}.            \tag{8}
\]

The remainder bound follows by replacing all later positive denominators
by 2N+1 and summing a geometric series. With N=160, exact rational
arithmetic gives, for alpha=log3/log2,

\[
 \frac{83130157078217}{52449289519716}
 <\alpha<\alpha+2^{-128}
 <\frac{350861368503572}{221368876767703}.                \tag{9}
\]

The outer determinant is one. A rational x/y strictly between p/q and r/s
with rq-ps=1 has y>=q+s: the positive integers k=xq-py and j=ry-sx
satisfy y=sk+qj. The identity does not require reducing x/y.
Here q+s=273818166287419>10^12.

For m>=128, (5) gives

\[
 0<A_0/m-\alpha
 =\log(1+\Lambda)/(m\log2)
 <\frac{3}{2m}2^{-m}<2^{-128}.                          \tag{10}
\]

This contradicts (9), since its original denominator m is below 10^12.
It remains to check 1<=m<=127. For each m the checker takes
A_0=bit_length(3^m) and verifies the strict integer margin

\[
 ((2^{A_0}-3^m)+1)2^m-3^m>0.                           \tag{11}
\]

All 127 rows pass and are retained in full. These cases exhaust (4).
No floating-point evaluation or guessed decimal bound occurs. QED.

## 3. Every contracting word has at most one non-descending source

The coefficient-only comparison below concerns the formal affine maps
at x=0. It does not treat zero as an actual positive odd Collatz source.
For x>=0,

\[
 g_a(x)=2^{1-a}g_1(x)\le g_1(x),\qquad g_1(x)=(3x+1)/2.
\]

Monotonicity, applied at the same input at each step, gives

\[
 0<C/U=f_p(0)\le2^{1-a_m}\big((3/2)^m-1\big).           \tag{12}
\]

The last factor 2^(1-a_m) is kept separately: bound the preceding m-1
maps by g_1^(m-1), then use g_(a_m)=2^(1-a_m)g_1. This proves (12)
without identifying different ordered affine maps or dropping C.

### Theorem 2. All-word canonical-source isolation

For every original word p with D>0,

\[
 \boxed{\quad C/D<2^{A_m-a_m+1}=2^{A_{m-1}+1}.\quad}    \tag{13}
\]

The set of its positive sources with f_p(n)>=n is exactly

\[
 \boxed{
 \{\rho_p\}\quad\text{when }C\ge D\rho_p,
 \qquad\varnothing\quad\text{when }C<D\rho_p.
 }                                                       \tag{14}
\]

All other sources in the infinite original cylinder strictly descend.
The candidate in (14) is retained even when its resulting set is empty.

**Proof.** Combine (4) and (12) to get (13). The exact displacement
f_p(n)-n=(C-Dn)/U makes every non-descending positive n at most C/D.
Every legal source except rho_p is at least rho_p+2U>2U, whereas the
right side of (13) is at most 2U. Thus only rho_p is possible. Testing
C-D rho_p gives exactly (14). On the whole source the unchanged identity is

\[
 n(t)-f_p(n(t))=\rho_p-y_p+2Dt.                          \tag{15}
\]

Its positive slope proves the rest after its first accepted parameter.
For D<0, the same formula in n gives f_p(n)>n on every positive source,
since C>0. D=0 is impossible for a nonempty word. QED.

This theorem quantifies over every finite exponent word, with arbitrary
switches, lengths, exponents and orderings. It does not say the exceptional
canonical source always descends. For example the original word

    (4,1,1,1,1,2,2,1,2,1,1,2,1,1,1,2,3)

has m=17,A=27, canonical source 165 and endpoint 167, with D>0. It already
visited 31 on its first return, so this is not a first-crossing exception.
The source and image of its whole cylinder are

\[
 165+268435456t\longmapsto167+258280326t.                 \tag{16}
\]

Every t>=1 strictly descends; t=0 is explicitly retained and has its own
verified finite arrival witness. This is an example of the coefficient-
contracting yet non-descending behavior investigated in [RT], not a new
claim that such behavior is absent.

## 4. The entire unbounded next-exponent crossing family

A pre-crossing prefix q of length l has U_j<3^j at every nonempty prefix.
Keep its data (rho,y,U,L,C) as above. Define

\[
 h=\lfloor\log_2(3L)\rfloor-A_l+1\ge2.                  \tag{17}
\]

Thus 2^(h-1)U<3L<2^hU. The next original exponent has not crossed
exactly for a=1,...,h-1. Every a>=h is a first coefficient crossing.
Neither a frequency model nor independence of exponents is used.

Let

\[
 M=2^{h-1},\quad t_0\equiv-((3y+1)/2)(3L)^{-1}\pmod M,
 \quad0\le t_0<M,
\]
\[
 n_0=\rho+2Ut_0,\quad
 b_0=(3y+1+6Lt_0)/2^h.                                  \tag{18}
\]

The full union of all crossing children is the one positive progression

\[
 \boxed{
 n=n_0+U2^h v,\quad
 T^{l+1}(n)=\frac{b_0+3Lv}{2^{\nu_2(b_0+3Lv)}},\quad
 a_{l+1}=h+\nu_2(b_0+3Lv),\quad v\ge0.
 }                                                       \tag{19}
\]

The inverse is v=(n-n_0)/(U2^h) on the displayed source. Substitution into
3T^l(n)+1 proves (19) and the full valuation, including arbitrarily large
extra divisions. Congruence (18) is equivalent to its divisibility by 2^h,
so the source is complete. The low children retain (3) and their own
labels. Together, they exhaust every next exponent and every positive
source of q.

### Theorem 3. One original test controls the whole crossing alphabet

The only possible non-descending source in (19) is the OLD canonical
prefix source rho. It belongs to (19) precisely when t_0=0, and its actual
next exponent is uniquely a*=nu_2(3y+1). It is an exception precisely when

\[
 a^*\ge h\quad\text{and}\quad (3y+1)/2^{a^*}\ge\rho.     \tag{20}
\]

Every other source in the full unbounded crossing family has its first
strict descent below its start at return l+1.

**Proof.** For any admitted child p=qa, (13) says a non-descending source
n is less than 2^(A_l+1)=2U. Its q-cylinder congruence then forces n=rho.
That source has just one actual next exponent, proving (20). Earlier
prefixes have multiplier greater than or equal to one and positive
forcing, so every proper nonempty endpoint exceeds n. Thus final descent
is its first strict descent. The empty prefix case retains n=1 as the
actual fixed-loop exception and all other crossing sources descend. QED.

Each individual family also has an elementary checkable proof once its
original coefficients have been calculated. Its undivided target line is
b_0+3Lv, its source line is n_0+U2^h v, and

\[
 U2^h>3L,\qquad n_0+U2^h>b_0+3L.                        \tag{21}
\]

The second inequality follows from (13) applied to the formal affine
word qh and the positive source n_0+U2^h>2U; the inequality (13) itself
is about all real affine inputs and does not need terminal oddness.
The implementation checks both integer inequalities directly. They
certify every v>=1 by their positive slope; v=0 is the single exact
valuation check. Thus a delivered individual family can be verified
without executing a transcendence theorem or enumerating its sources.

### An original nonrepeating example

For the single mixed prefix

    q=(1,2,1,1,1,2,1,1,4)=PQ,

retain L=19683,U=16384,C=29839,rho=10907,y=13105,h=2. Formula (19) is

\[
 \boxed{
 10907+65536v\longmapsto
 \frac{9829+59049v}{2^{\nu_2(9829+59049v)}},\quad v\ge0.
 }                                                       \tag{22}
\]

This is first strict descent after ten odd returns. The actual last
exponent is 2+nu_2(9829+59049v). Indeed the endpoint is at most
9829+59049v<10907+65536v. Arbitrarily large last exponents have positive
source representatives because 59049 is odd. No repetition of PQ and
no unspecified weight for v occurs.

## 5. Whole-system finite audit with infinite source parameters

The exact symbolic audit starts at the empty prefix. At a prefix of
length l it performs the single test (20), checks (21), and creates ALL
low children a=1,...,h-1. The full high tail (19) is retained as a complete
certificate and is not truncated by exponent size. The exact number of
nodes at each depth is independently checked by the recurrence

\[
 N_0(0)=1,\quad
 N_j(A)=\sum_{B<A}N_{j-1}(B),\quad
 j\le A\le\lfloor\log_2(3^j)\rfloor.                   \tag{23}
\]

Every original pre-crossing word satisfies precisely these prefix
bounds. Recurrence (23) and the explicit child ranges prove completeness
of the finite tree. At EVERY node the generated rho is checked against
(2) using an independent modular inverse, the original affine equation
U*y=L*rho+C is checked, and the next valuation is recomputed by repeated
division. Both whole-tail margins (21) and the actual endpoint of the
whole crossing family's first source n_0 are also checked. Thus this
finite audit supplies its own elementary affine-tail proofs and does not
need the external logarithm theorem as a premise: each v=0 is checked
directly, and the positive affine margin at v=1 proves all v>=1.

The complete run for first crossing at return at most 18 visits 1,166,058
prefixes. It retains exactly one exceptional crossing: source 1, word (2),
endpoint 1. Therefore every positive source n>=3 whose first odd-return
coefficient crossing is at most 18 has first actual strict descent at
that return. This is unbounded in the starting integer and the last
exponent. Its source-time scope is not a bound on every orbit's crossing
return, and it is not presented as a published stopping-time record.

The ordered stream can be materialized with `--ledger`. The independent
`audit_ledger.py` imports neither the main module nor the predecessor;
it reconstructs the entire depth-first domain and each original numerator,
residue, endpoint, unbounded-tail margin and canonical-point test. Its
successful full replay is included in the delivery evidence. The uncompressed
SHA-256 and per-depth counts are in verification.json. The executable
proof certificate regenerates the ENTIRE finite domain, not a sample.
The independent count recurrence does not replace the original affine
and valuation checks. The infinite-depth frontier remains unproved.

For example n=27 first crosses at return 37, reaches 23 there, and has an
independently checked 41-return witness to 1. It is outside the 18-return
finite theorem but its whole crossing cylinder is still covered by the
all-length reduction and a single original root test.

## 6. Exact transfer into the retained Split-Zero comparison

The original absolute first-jet complex has original edge and vertex
modules C^0,C^1, source and target maps J,P, d=J-P, and

\[
 d_\epsilon=d-\epsilon P,\quad \epsilon^2=0.
\]

The receiver is the already published kernel

\[
 \mathfrak B_X=
 \ker\big(H^1(K_\epsilon)\to H^1(K)\big).
\]

Its integral presentation is C^1/(dC^0+P ker d), with the inverse map to
first-order classes [z] -> [epsilon z]. The predecessor proves that a
finite integral pair db=0, dc-Pb=V_n yields an actual finite path to 1,
and that the full obstruction has cyclic Z/m summands and nonperiodic
Z summands. Those definitions and source maps remain unchanged [WB1].

Let B_p(n) be the sum of the actual original edges in an accepted word
from n to y. Its boundary and its new first-order use are

\[
 dB_p(n)=V_n-V_y,\qquad
 d_\epsilon(\epsilon B_p(n))=\epsilon V_n-\epsilon V_y.   \tag{24}
\]

Thus the all-word descent gives [epsilon V_n]=[epsilon V_y] with y<n.
It does NOT by itself assert either class is zero. An original witness
at y is transported by the explicit addition

\[
 (b_y,c_y)\longmapsto(b_y,c_y+B_p(n)).                    \tag{25}
\]

Substitution in db and dc-Pb proves the exact boundary at n. No original
edge or cycle is divided by a period and no integral denominator is
removed. The checker imports the unchanged, Git-blob-verified firstjet.py
and verifies (24), including all intermediates and terminal vertices.
For the examples with complete arrival, its unchanged witness checker
extracts the actual path.

At an equation support label E, (24) maps a declared source module into
the original equations in that support, or enlarges E by exactly the
finitely many edges of the displayed path. Unions of such supports give
the original inclusion diagram, and (24)-(25) commute with its inclusions.
Their supported zero is at that retained E. An empty exceptional set in
(14) or (20) is stored alongside its source label and integer equation,
not substituted for the external absent scalar. The word index itself
is not a definition of intrinsic Split-Zero support.

The family maps are finite-column maps on free modules even over the
infinite progression: each original basis vector has its own finite path.
There is no infinite sum in (24). Both the true singleton exception at 1
and the non-descending canonical point 165 remain available to the
original operator and subsequent certificates.

## 7. Relation to the elementary maps, with the different source moduli

Let F be the shortened elementary map: F(x)=(3x+1)/2 at odd x and
F(x)=x/2 at even x. The word p expands to the parity word

\[
 w(p)=1\,0^{a_1-1}\,1\,0^{a_2-1}\cdots1\,0^{a_m-1},
 \qquad |w|=A_m.                                       \tag{26}
\]

The composition has the exact same L,U,C as (1). Grouping at the original
odd vertices is its inverse for paths with odd terminal value. The parity
cylinder alone has modulus 2^A; additionally requiring terminal oddness
selects the original odd-return cylinder modulo 2^(A+1). These moduli are
not identified. On their common source, T^m(n)=F^A(n).

For ANY shortened parity word with k letters and m odd letters, its
original affine constant E satisfies 0<=E<= (3/2)^m-1: omitting a division
only increases the nonnegative formal constant. If 2^k>3^m, (4) gives
E<2^k-3^m, so its non-descent threshold is strictly below 2^k. Thus every
such parity cylinder also has at most its single canonical positive
representative as an exception. The all-even word has zero constant and
strictly decreases every positive source, including its least positive
source 2^k; the canonical residue zero is not a positive starting point.

The first shortened coefficient crossing can occur inside the final even
divisions of an odd-return block. Consequently the finite theorem of
Section 5 is stated with odd-return counts and is not silently asserted
as the identical count in Terras' shortened coefficient-stopping problem.
The exact expansion (26), its terminal condition and its clocks are the
comparison used here. The standard elementary map without immediate
odd-step division further expands each odd shortened step into its
original odd step plus one division, with inverse grouping.

## 8. Global restrictions and the remaining source problem

This is an all-word source-isolation theorem, not a proof that its
canonical candidates are always harmless. For any nonbase component,
its least original positive integer s has every iterate at least s.
A coefficient-crossing prefix at s is therefore a non-descending case
of (14). More precisely, at its first crossing it must pass test (20)
as the canonical source of the proper prefix. The all-word theorem
eliminates every other point of that entire infinite crossing family.
If there is no coefficient crossing, all original prefix multipliers
remain at least one and the associated itinerary stays in the infinite
pre-crossing tree. Both alternatives remain represented.

The same exact inequalities are useful for finite returns. Every actual
positive cycle has 2^A>3^m, by multiplying the unchanged cycle equations.
At every rotation its starting vertex must be the canonical representative
in (2) and satisfy (13). Its integral forcing condition is still D|C;
no canonical-root test replaces the actual cyclic solution and valuations.

At the first coefficient crossing m, all proper-prefix 2^A_j<=3^j give
C<=m*3^(m-1). Hence a non-descending original endpoint n+2k satisfies

\[
 0\le k<m/6.                                          \tag{27}
\]

Indeed (f_p(n)-n)<C/U<m/3 because U>3^m and Dn>0.
For m=1 the same strict upper bound applies to its equality at 1.
This is an additional all-length exact small-overshoot restriction,
not a claim that every allowed k occurs.

There is no fixed finite bound on the first crossing for all sources:
n_N=2^(N+1)-1 has its first N exponents equal to one, with
T^j(n_N)=3^j2^(N+1-j)-1 for 0<=j<=N. All those prefix coefficients
exceed one. The sources vary with N. This explicitly prevents promotion
of the finite tree audit to one uniform clock bound.

The next arithmetic calculation is therefore sharply specified: extend
source proofs on the actual canonical crossing points and control the
ordinary-positive-integer support of the no-crossing infinite branches.
The canonical residue towers have their original increasing representatives;
boundedness gives eventual constancy, not an automatic contradiction.
The current argument does not show their positive intersections empty.
A finite failure to cross is not an infinite-orbit certificate. The workbench
still retains both periodic and nonperiodic comparison-kernel summands.

## 9. Verification and source discipline

`power_gap_certificate.json` contains the exact finite arithmetic component
of Theorem 1. `verify.py` re-creates it, checks all 262,143 nonempty exponent
words of total sum at most 18, and checks every canonical shortened parity
source through length 14. These word tests are regression evidence; the
unrestricted quantifier comes from Sections 2-4.

The crossing audit is a DIFFERENT complete bounded proof domain with
unbounded source and last-exponent parameters. Both ordinary and optimized
runs reproduce verification.json byte for byte. All checks use explicit
exceptions rather than assert statements, so optimization cannot remove
them. Invalid-input controls include a false descent at 1, a false endpoint
descent at 165, an altered source lattice, a false valuation and a divided
nonintegral first-jet witness.

No Lean verification, independent external mathematical review or new remote
GitHub execution is implied by these files. The delivery receipt records the
actual publication state. Earlier valid source files and their original
scope statements are not rewritten by this additive continuation.

## Sources

[MAT] A. Languasco, F. Luca, P. Moree and A. Togbe, *Sequences of integers
generated by two fixed primes*, Abh. Math. Semin. Univ. Hambg. 95 (2025),
123-148, Theorem 2.1. The inspected rational-number bound is attributed there
to Matveev, in a version due to Bugeaud, Mignotte and Siksek. The proof here
uses only that displayed bound and checks its constants explicitly.
https://doi.org/10.1007/s12188-025-00293-9

[RT] O. Rozier and C. Terracol, *Paradoxical behavior in Collatz sequences*,
arXiv:2502.00948v2 (13 February 2025), Definitions 1.1-1.2, Sections 2 and 4,
and the explicit comparison of iteration conventions in Section 5. This
supplies context and attribution, not a convergence premise or numerical
bound imported into our proof.
https://arxiv.org/html/2502.00948v2

[WB1] KokunoYumeto, Collatz workbench,
`intrinsic_zero_firstjet_20260915/firstjet.py`, Git blob
`97f9ef5ad535f7ec18259d41fab6a3557be17d98`, and its complete `note.md` at
`9afcbe2dc9bace77c1ae705b1cd128da22fe8f8b`. Original integral first-jet
presentation and finite-witness extraction; used unchanged.

[WB2] Same repository and revision,
`mixed_switch_control_20260916/note.md` and `TASK_STATE.md`. The source
stages the nonrepeating/general-switch target. Its previous mixed-core gap
certificate is not a premise of the new all-word gap.

[SZ] Owner's Split-Zero construction and intrinsic fibre/quotient programme,
source chain recorded in [WB1]. The precise structure used is its comparison
kernel with original representatives, relations and support inclusions, not
a claim that an isolated scalar zero contains a unique trajectory.
