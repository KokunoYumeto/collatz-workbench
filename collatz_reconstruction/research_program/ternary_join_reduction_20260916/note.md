# All ternary layers: bounded original-support reductions and a longer crossing window

16 September 2026. Additive continuation for `KokunoYumeto/collatz-workbench`, PR #2,
read at `9afcbe2dc9bace77c1ae705b1cd128da22fe8f8b`. The current receiver is the
absolute integral first-jet complex in `intrinsic_zero_firstjet_20260915`.
The local `height_window_reduction_20260916` is a source of the preceding envelope
and common-future calculus. Its pending files are not claimed to be published by
this addition. The definitions and proofs used here are supplied below; execution
depends only on the published first-jet validator, whose original hash is checked.

The main new construction has two complete families at every positive ternary
valuation, a finite catalogue of all indicated one-step/common-future comparisons,
and a whole-source retraction with a quadratic bound on original vertex support.
The first-crossing certificate advances from 10,280 to 10,945 odd steps. None of
these results asserts that all remaining roots vanish. No logarithm estimate,
probabilistic hypothesis, or RH estimate is used.

## 1. Original maps and complete affine cylinders

Use the unchanged positive-odd source X and map

\[
T(n)=(3n+1)/2^{a(n)},\qquad a(n)=\nu_2(3n+1).
\]

For a word w=(a_1,...,a_k) put A_j=sum_{i<=j}a_i, A=A_k, U=2^A, L=3^k and

\[
C=\sum_{j=0}^{k-1}3^{k-1-j}2^{A_j},\qquad f_w(x)=(Lx+C)/U.
\tag{1}
\]

The complete source and target are

\[
\rho+2Ut\longmapsto\eta+2Lt,\qquad t\ge0,
\quad \rho\equiv(U-C)L^{-1}\pmod{2U},\quad0<\rho<2U,
\quad\eta=(L\rho+C)/U.\tag{2}
\]

The parameter inverses are (n-rho)/(2U) and (y-eta)/(2L) on these actual images.
Terminal oddness in (2) implies each original prefix oddness: reduce the full
numerator modulo 2^{A_j+1}; its first j terms form the prefix numerator times an
odd power of three, its next term has valuation exactly A_j, and all later terms
vanish. Consecutive prefix equations then give the exact valuations a_j.
Positivity propagates from the positive starting value. The same congruences work
for the negative source rho-2U; every one of its original iterates is negative,
since 3x+1<0 for a negative odd integer. Therefore

\[
0<\eta<2L.\tag{3}
\]

This sign argument is about the original formulas on a stated additional source;
it is not an identification of positive and negative cycles.

## 2. Two source families at every original ternary valuation

Fix integers b>=1 and e in {2,6}. Define

\[
h_e=(2^e+2)/3\in\{2,22\},\qquad
 a=a(b,e)=\min\{a\ge1:2^{a+e+2b}<3^{a+b}\}.
\tag{4}
\]

This minimum exists with an elementary explicit bound:

\[
a(b,e)\le b+2e,\qquad a(b+1,e)-a(b,e)\in\{0,1\}.\tag{5}
\]

Indeed at a=b+2e the ratio in (4) is (8/9)^{b+e}<1. Increasing b multiplies that
ratio by 4/3, and then increasing a by one multiplies it by 2/3. The product is
8/9<1, proving the adjacent increment claim along with minimality.

Keep the original right word

\[
w_{b,e}=(1)^a\,(e)\,(2)^{b-1}\,(3).\tag{6}
\]

Its length is a+b+1, and its exponent sum is a+e+2b+1. Put

\[
Q=3^{a+b},\qquad J=2^{e+2b},\qquad K=2^{a+e+2b}<Q.
\]

Define the EXACT larger-source set

\[
\mathcal R_{b,e}=\{n>0:\ n\equiv3\pmod4,\quad
 Jn+h_e3^b\equiv0\pmod Q\}.\tag{7}
\]

This is one full positive residue class modulo 4Q. Let n_0 be its representative
in (0,4Q), and set

\[
m_0=\frac{Kn_0+2^ah_e3^b}{Q}-1.
\]

### Theorem 1. Complete lower-source joins on every layer

For every b,e above, all original pairs in the designated fibre are

\[
\boxed{\begin{aligned}
n(t)&=n_0+4Qt,\\
m(t)&=m_0+4Kt,\\
y(t)&=(3n_0+1)/2+6Qt,\qquad t\in\mathbb Z_{\ge0},
\end{aligned}}\tag{8}
\]

and they obey the ORIGINAL forward paths

\[
n(t)\xrightarrow{1}y(t)\xleftarrow{\ w_{b,e}\ }m(t),\qquad 0<m(t)<n(t).
\tag{9}
\]

Every n(t) has actual valuation nu_3(n(t))=b. Its ternary unit n(t)/3^b is 1
modulo 3 for e=2 and 2 modulo 3 for e=6. In particular it has no incoming original
odd-return edge. The two families at different (b,e) are disjoint. No claim is made
that (7) covers every source with that valuation and unit.

**Proof with the original coordinates.** Congruence (7) first forces 3^b|n. With
z=n/3^b it is Jz+h_e=0 modulo 3^a. Since a>=1, J=1 modulo3, and h_e is a unit
modulo3, z is a unit of the asserted residue. Thus b is exactly the valuation,
not just a divisibility lower bound. The original input is n=3^b z with n=3 mod4.

Set w=(Jz+h_e)/3^a. It is a positive even integer with nu_2(w)=1: J is divisible
by 16, h_e=2 modulo4, and division by odd 3^a preserves valuation. Define

\[
m=2^a w-1=\frac{Kn+2^ah_e3^b}{Q}-1.\tag{10}
\]

After j of the first a odd returns its ORIGINAL value is

\[
x_j=3^j2^{a-j}w-1\qquad(0\le j\le a).\tag{11}
\]

For j<a, nu_2(x_j+1)>=2, so the next exponent is exactly one. At j=a,

\[
x_a=2^e(4/3)^b n+h_e-1.
\tag{12}
\]

The next original exponent is exactly e, since 3h_e-2=2^e and

\[
T(x_a)=1+4^b n/3^{b-1}.
\]

For the subsequent b-1 steps, the value after j of those steps is

\[
1+4^{b-j}n/3^{b-1-j}\qquad(0\le j\le b-1).
\tag{13}
\]

They have exact exponent two and end at 1+4n. The last exponent is exactly three:
3(1+4n)+1=4(3n+1), and n=3 modulo4 gives nu_2(3n+1)=1. The endpoint is (3n+1)/2.
Thus every displayed edge is integral, odd at its odd-return endpoints, positive,
and has its original prescribed valuation. Conversely equality of these two word
endpoints, using (1), gives (10) and hence (7). The first n=3 modulo4 condition is
necessary for the left word (1). This proves the full source domain.

For strict height, (10) reads

\[
m=(K/Q)n+h_e(2/3)^a-1.
\]

Equation (4) implies
h_e(2/3)^a < (h_e/2^e)(3/4)^b < 1. Both K/Q<1 and this negative constant term
therefore give m<n, while m=2^a w-1>0 gives positivity. Since both endpoints are odd,
n-m>=2. CRT between Q and 4 gives (8); subtracting and dividing any of the three
original progressions supplies its inverse parameter. An incoming edge to n would
give 3x+1=2^c n=0 modulo3, impossible. QED.

For e=2,b=1 this is the previously retained family 1731+2916t to 1215+2048t.
For e=2,b=2 it gives

\[
6219+8748t\longrightarrow9329+13122t\longleftarrow5823+8192t.
\tag{14}
\]

For e=6,b=2, a=12, and it gives

\[
\boxed{13704327+19131876t\longrightarrow20556491+28697814t
\longleftarrow12017663+16777216t.}\tag{15}
\]

The right word in (15) is (1)^12,(6),(2),(3). This is a lower-component relation,
not a purported forward descent from the left source to the right source.

### Complete treatment of longer leading runs in this template

For a'>=a(b,e) the same formula with a' gives a subfamily of (7), since its
congruence modulo 3^{a'+b} implies the original congruence modulo 3^{a+b}.
Both source morphisms remain available and generally have different smaller
endpoints. The minimal a(b,e) thus covers the complete height-reducing template
family with longer leading runs, rather than being a sample of the a-axis.

The membership test at an arbitrary n is finite: compute its ACTUAL b=nu_3(n),
read its ternary unit, select e=2 or 6, compute a by integer comparison, and test
(7). The accepted path has at most 2b+2e+1 odd returns on its right leg. This is a
bound on the constructed witness, not on an arbitrary orbit's stopping time.

## 3. A complete finite catalogue of further original comparisons

There is also a useful all-length rule for any right word w of length k>=2 with

\[
a_k\text{ odd},\qquad 2^{A-1}<3^{k-1}.\tag{16}
\]

Its target eta is 5 modulo6, because eta is odd and eta=2^{-a_k}=-1 modulo3.
Thus its entire image is inside the original image of the left word (1). Using
(2), every pair is

\[
\boxed{\begin{aligned}
n(t)&=(2\eta-1)/3+4\cdot3^{k-1}t,\\
m(t)&=\rho+2^{A+1}t,\\
y(t)&=\eta+2\cdot3^kt,\qquad t\ge0.
\end{aligned}}\tag{17}
\]

The common endpoint, either source, and their affine lattice steps have the same
inverse parameter. These pairs have m(t)<n(t) throughout. To prove it, note
C>=3^k-2^k, by termwise comparison A_j>=j. For k>=2,
3^k-2^k>3^{k-1}>2^{A-1}. Define D_0=(C-2^{A-1})/3>0; integrality follows from
the odd final exponent. The original equation is

\[
m=(2^{A-1}n-D_0)/3^{k-1}<n.\tag{18}
\]

Its numerator is positive on (17), since m starts at the positive rho. Equation
(3) also proves 0<(2eta-1)/3<4*3^{k-1}. Hence this is an ENTIRE residue class
without omitted small positive representatives. No bounded search is needed for
these statements at arbitrary k.

The finite catalogue takes exactly all (16) with 2<=k<=12. For each k the exponent
sum has the precise bound A<=(3^{k-1}).bit_length(). There are 20,397 words. Their
independent composition count is

\[
\sum_{k=2}^{12}\sum_{A=k}^{\operatorname{bitlength}(3^{k-1})}
\sum_{\substack{j\ge1\text{ odd}\\j\le A-k+1}}
\binom{A-j-1}{k-2}.\tag{19}
\]

Every original candidate and its active/redundant face label is regenerated and
checked. Both original affine coefficient columns are divided by their prescribed
2-powers, retaining the odd constant and even slope at EVERY original intermediate
point. This verifies the whole variable-source family, not merely its anchor.

## 4. Exact residue cover, without deleting redundant faces

The old retained retraction first uses a forward one-return descent, then inverses
on the actual images of (1), (1,2), (1,1,1,2,1,1,4), and then the e=2,b=1 join.
Its nonbase roots are exactly

\[
n\bmod36\in\{3,7,15,19,27\},\quad
n\not\equiv8731\pmod{8748},\quad n\not\equiv1731\pmod{2916}.\tag{20}
\]

These follow directly by solving the original expanding affine image congruences;
the inverse of (1,2) is (8n-5)/9 and the longer inverse is (2048n-2363)/2187.
All their least admitted remaining sources are in the positive inverse domain.
The point 1 remains the separate original base root.

At the common period P=4*3^11=708588, (20) has 98,091 nonbase root residues.
Visit (17) in the declared order (period, larger-source anchor, exponent sum, word).
A family is selected exactly when it covers at least one still-retained old root
residue. Its original full family remains its domain; prioritization restricts
execution, not its mathematical source. This yields 370 selected families and
93,025 remaining residues. The 5,066 removed residues equal the sum of the disjoint
newly covered counts. A second sweep using the UNION OF ALL 20,397 candidates
independently reproduces exactly the same remaining set. The signed row/word and
all mask hashes are recorded in verification.json's full reconstructed result.
These are counts for a specified arithmetic reduction; they are not probabilities
or counts of counterexamples.

Let R_12 denote that explicitly regenerated residue set. The fixed new retraction
uses all the old rules, then the selected catalogue, then Theorem 1 on its remaining
inputs. Its nonbase roots are exactly

\[
\{n>1:n\bmod708588\in R_{12}\}\setminus
\bigcup_{b\ge1,e\in\{2,6\}}\mathcal R_{b,e}.\tag{21}
\]

The infinite layer subtraction is an effective single test on the actual valuation
of n. It is not approximated by imposing a finite b cap.

The old/catalogue rules already cover the whole e=2 families b=1,2,3,4 and the e=6
family b=1. Every e=2 family b>=5 and e=6 family b>=2 is new relative to the catalogue.
For b<=10 these assertions are finite original residue comparisons. For b>=11,
every member has 3^11|n and n=3 modulo4, hence has the single residue 177147 modulo
708588; that residue lies in R_12. This proves the comparison at every larger b,
not by extrapolation from testing 64 layers. It also proves that no fixed catalogue
length of twelve has already supplied these infinite-layer exclusions.

For example the catalogue gives 91+324t -> 71+256t as a height relation, from the
original right word (1,1,2,2,1) meeting the left word (1). Cancelling their actual
common last edge recovers the four-edge inverse path; its cancellation is recorded,
not interpreted as absence of the source.

## 5. Integral first-jet maps and nested retractions

On the absolute original graph use D=Z[epsilon]/epsilon^2, q=1+epsilon, and

\[
d_\epsilon e_n=V_n-qV_{T(n)},\qquad q^j=1+j\epsilon\quad(j\in\mathbb Z).
\]

The inverse q^{-1}=1-epsilon is integral. For original forward legs l:n->y and
r:m->y of lengths s,t, their weighted chains give

\[
\boxed{d_\epsilon(B_l(n)-q^{s-t}B_r(m))=V_n-q^{s-t}V_m.}\tag{22}
\]

Both legs, not only their difference, are retained by the checker. Theorem 1 has
s-t=-(a+b). The coefficient kernel receiver sends V_n to [epsilon V_n]. Multiplying
(22) by epsilon gives the exact lower-height relation xi_n=xi_m. It does not assert
that either class is zero before a lower-source boundary is supplied.

Each chosen move has m<n. Recurse on the original positive integer, leaving roots
as H(V_r)=0 and Q(V_r)=V_r. For a move with chain B and signed clock k, define

\[
H(V_n)=B+q^kH(V_m),\quad Q(V_n)=q^kQ(V_m),\quad F=I-Hd_\epsilon.
\tag{23}
\]

The recursion terminates on EVERY original input, independent of Collatz. Its
intermediate original path values need not decrease. The identities are

\[
d_\epsilon H=I-Q,\quad Q^2=Q,\quad HQ=0,
\quad d_\epsilon F=Qd_\epsilon,\quad F^2=F,\quad FH=0.
\tag{24}
\]

The first telescopes (22). The next two hold because Q ends at roots and H is zero
there. Substituting dH=I-Q and HQ=0 in F^2 and FH proves the remaining statements.
Thus the projections F,Q and the inclusion of their image complex give an actual
chain-homotopy retraction. In edge degree its full presentation is

\[
C^0_D/\operatorname{im}H\xrightarrow{\sim}\operatorname{im}F,\qquad[e]\mapsto Fe,
\]

with inverse Fe mapped to [e], since ker F=im H. The projected edges have these
relations; they are not declared an independent basis.

The catalogue and all-layer rules act only after the preceding rules fail. The old
route is therefore unchanged up to its retained root. Appending the new route there
gives the correction K=H_new-H_old, whose original boundary is Q_old-Q_new and
whose chain lies in the old image: F_old K=K. Consequently

\[
F_new F_old=F_old F_new=F_new,\qquad
Q_new Q_old=Q_old Q_new=Q_new.\tag{25}
\]

These apply both at the catalogue extension and the infinite-layer extension. They
prove preservation through specific maps, not through a comparison of dimensions.
All arithmetic choices are independent of epsilon, so constant reduction sends
q^k to 1 and commutes with all the maps. The original first-jet comparison kernel
and its cycle-index/free component submodules are preserved. In particular e_1
is retained and F(e_1)=e_1; no integer cycle period is inverted.

## 6. A quantitative bound on the whole-system retraction

### Theorem 2. Polynomial original-support control

For every original odd input n>=3, the construction above uses only original odd
vertices at most

\[
\boxed{64n^2+21.}\tag{26}
\]

Before like edge terms are collected, its homotopy column has at most

\[
\boxed{K(n)=\frac{n-1}{2}\left(2\lfloor\log_3 n\rfloor+14\right)}\tag{27}
\]

signed monomial edge terms. Its constant coefficients have total absolute sum at
most K(n); its epsilon coefficients have total absolute sum at most K(n)^2. The
logarithm in (27) is equivalently the largest b with 3^b<=n, so all bounds are
integer-computable. This is a bound on the retraction to retained roots, not on
all actual stopping times.

**Proof.** Each selected move drops between positive odd integers by at least two,
so there are at most (n-1)/2 moves. The finite catalogue has right-leg length at
most twelve, and its left leg has length one; old inverse paths are shorter.
The all-layer right leg has a+b+1<=2b+2e+1<=2b+13 edges, and its left leg adds one.
Its actual b=nu_3(current source)<=floor(log_3 n). Thus (27) bounds the total terms.

On an all-layer move with larger source x<=n, the right leg first rises to the
explicit maximum (12), then every subsequent exponent is at least two and the
values decrease. Since (4/3)^b<=3^b<=x and e<=6,h_e<=22, (12) is at most
64x^2+21<=64n^2+21. The left target is (3x+1)/2, smaller than that bound.
For every finite catalogue or inverse leg, its smaller source is below x and its
length is at most twelve. Each original map is bounded by g_1(z)=(3z+1)/2 on the
same positive input, hence all intermediate values are less than
(3/2)^12(x+1)<130(x+1)<=64x^2+21 for x>=3. Forward descent is already below x.
This proves (26) along every concatenated leg.

All weights in (23) are signed q-powers. Their exponent is a sum of previous
signed leg lengths plus the position within the current leg, whose absolute
value is at most the total number K(n) of traversed edges. Each term consequently
has constant amplitude +/-1 and epsilon amplitude of absolute value at most
K(n). Collection cannot increase either absolute-sum bound. QED.

The induced original-height filtration maps satisfy

\[
Q(C^1_{\le n})\subset C^1_{\le n},\qquad
H(C^1_{\le n})\subset C^0_{\le64n^2+21},
\quad F(C^0_{\le n})\subset C^0_{\le256n^2+21}.
\tag{28}
\]

The last uses T(x)<2x, so each H column in Hd(e_x) obeys the bound at source 2n.
This does not assert that H preserves height without an increase. Under expansion
to the original elementary map, intermediate odd-step values 3x+1 are at most
192n^2+64 in an H column; the divisions do not increase that bound.

For finite declared equation support E, include its original targets and the
finite original supports of these H columns. This enlargement preserves unions
and inclusions. Equations (24)-(28) describe its actual comparison with larger
support stages. The reconstructed supported zero keeps its original fibre and
relations. An infinite diagram is being controlled by bounds on every original
column, rather than by identifying it with an absent scalar.

## 7. Extending the sharp crossing-height window

Retain b_j=bitlength(3^j)-1, b_0=0, and the exact original coefficients

\[
C_0^*=0,\quad C_m^*=3C_{m-1}^*+2^{b_{m-1}},\quad
D_m^*=2^{b_m+1}-3^m,\quad \Theta_m=C_m^*/D_m^*.
\tag{29}
\]

For a first odd-return coefficient crossing at m, every proper A_j<=b_j and the
final A_m>=b_m+1. Thus

\[
C_m^*-C_p=\sum_{j<m}3^{m-1-j}(2^{b_j}-2^{A_j})\ge0,
\quad C_p/(2^{A_m}-3^m)\le\Theta_m.\tag{30}
\]

The maximum is attained at the original word with consecutive prefix sums b_j and
final sum b_m+1. The differences and prefix sums are inverse operations. This is a
sharp bound on the word domain; attainment is not an assertion of an integer
non-descending source in that word's cylinder. The original non-descent equation
forces n<=floor(Theta_m).

For the shortened map S(n)=(3n+1)/2 on odd n and n/2 on even n, each original odd
edge of exponent a expands to 1 followed by a-1 even divisions. The first shortened
coefficient crossing with m odd steps occurs at b_m+1 total shortened steps. Its
numerator remains C_p and its denominator is 2^{b_m+1}; (30) therefore applies at
that possibly even endpoint as well. This supplies the exact clock comparison.

Define H_M=max_{m<=M}floor(Theta_m). All exceptions by horizon M lie among original
odd n<=H_M. This proof is valid for every chosen M without a logarithm theorem.
The coefficient-stopping-time question itself is the established Terras problem;
we do not claim it originated here [RT].

The previous retained window had M=10280,H_M=5624777. The current exact recurrence
gives

\[
\boxed{H_{10945}=6728242,\quad\text{largest odd candidate }6728241.}\tag{31}
\]

The attaining record is (m,b_m+1,H)=(10281,16295,6728242); the next record is
(10946,17349,8129266). Thus testing the next original source interval extends the
entire horizon through 10945, not just the single next value 10281.

Every original odd source 3<=n<=6728241 has been checked, with ledger row
[n, actual odd endpoint, complete first-crossing exponent word]. There are
3,364,120 rows, 551,732 new rows beyond the previous interval. Both the odd endpoint
and the earlier shortened crossing endpoint are strictly below n. The latter is
computed as terminal*2^{A-bitlength(3^m)}, not inferred from its later odd value.

The independent auditor imports neither join_control nor the first-jet code. It
replays every individual division, every proper coefficient prefix, and the
original consecutive source labels. It checks 11,738,935 original odd-return
edges and 23,482,682 divisions. The longest first crossing in this finite source
interval is 141 odd returns; this measured statistic does not replace the proved
horizon in (31). Inductive endpoint heights give a maximum total 248 odd returns,
at source 6649279, on this certified finite interval.

It follows from (30)-(31) and the complete ledger that every original n>=2 whose
first shortened coefficient crossing uses at most 10945 odd steps descends at
that crossing. Starting integers and the final valuations are unbounded. Even
starting sources descend on their first division. The original fixed loop n=1
is retained separately. No source with no crossing is accepted by this theorem.

Each row ends at a smaller positive odd integer. Induction in the original source
order supplies actual finite arrival certificates throughout the interval, so the
original kernel-height subgroup generated by xi_n=[epsilon V_n], n<=6728241, is
zero with its source rows retained.

## 8. Witness extraction and remaining global task

The source first-jet theorem states that a finite integral witness (b,c) obeying

\[
db=0,\qquad dc-Pb=V_n\tag{32}
\]

extracts an actual path from n to 1. Its proof uses the ORIGINAL integral component
relation -km=1 and thus forces the actual cycle length m=1. It does not allow
rational division by a longer period.

From (24), multiply an H column by epsilon. It is a relation epsilon V_n minus
epsilon V_root. Add its constant edge coefficients to the linear part of the
root's original witness (32); leave the constant cycle untouched. The full result
is again (32) at n. The unchanged authenticated validator performs the extraction.
Six examples, including n=13704327 outside (31), are delivered. Its new arithmetic
root is 5341183 inside (31), its signed reduction clock is -16, and its extracted
ACTUAL forward path to 1 has 89 odd returns. The root is not misreported as an
actual forward iterate at that signed clock. Infinite progressions are proved for
lower-source relations; these six point arrival witnesses do not prove arrival
of all their variable endpoints.

The complete first-jet component kernel is preserved by (24)-(25). A nonbase cycle
retains its Z/mZ component and a nonperiodic component its Z. Its least original
integer must now exceed 6728241, belong to (21), and have no first coefficient
crossing with at most 10945 odd steps. These are necessary original-source
restrictions; the remaining root set is not claimed empty.

The next arithmetic work can enlarge either leg of the common-future family,
construct additional coefficient templates on (21), or sharpen (30) on remaining
source residues. A family must retain its exact source domain and both inverse
parameters. The polynomial support bound (26) makes the present whole-system
retraction quantitatively available for such further comparisons; it does not
supply global applicability of a next root reduction. No unproved well-founded
rank, zero measure argument, or infinite intersection assumption is used.

## 9. Verification, integration and sources

The general algebraic and arithmetic-family results above have their written proofs.
The finite catalogue and original-source window have COMPLETE bounded certificates.
Regression checks additionally test 128 layer objects with b<=64, four source
parameters per layer, exact affine coefficients, old/new projection identities,
negative controls and original witness extraction. General b coverage is proved by
(4)-(13), not extrapolated from that test range. Both ordinary and optimized outputs
are compared byte for byte. A typed-cache bug caught by a Boolean-as-integer negative
control during development was repaired before the accepted runs; those invalid
inputs remain rejected tests, not silently removed cases.

`verify.py --output full.json` reconstructs all 370 selected families, all masks,
examples and regression records. `replay.py --full --predecessor` regenerates the
complete source ledger in both execution modes and audits every row independently.
The source ledger is an external deliverable and a reproducible optional artifact;
its hash is pinned in `window_certificate.json`. No large binary need be trusted
without this reconstruction. Source/current Git identities and publication scope
are recorded separately; an expected or scheduled CI result is not called a pass.

[HW] Owner-directed local continuation, *Global height reduction: sharp crossing
windows and original coalescence maps*, 16 September 2026. Supplied
`Collatz_Height_Window_Proof.md` and its complete ZIP. The source-height envelope,
all-pair common-future formula and unbounded retraction definitions are prior work
of this workbench, reproduced where used. Exact input file hashes are in SOURCE_INTAKE.

[FJ] KokunoYumeto/collatz-workbench, `intrinsic_zero_firstjet_20260915`, at commit
9afcbe2dc9bace77c1ae705b1cd128da22fe8f8b. Original firstjet.py SHA-256
`a53cef65109285f377e2c1344ae662c4a74574a30c1c40dfffebc9ed6cca06b0`.
https://github.com/KokunoYumeto/collatz-workbench/tree/9afcbe2dc9bace77c1ae705b1cd128da22fe8f8b/collatz_reconstruction/research_program/intrinsic_zero_firstjet_20260915

[SZ] Owner's Split-Zero support-fibre and killed-representative construction, traced
in [FJ]. Its support fibre and original relation quotient are not defined as
chronological weighted-automata histories. No additional Zeta numerical estimate is
imported here, and no claim about the complete current RH programme is made.

[RT] Olivier Rozier and Claude Terracol, *Paradoxical behavior in Collatz sequences*,
arXiv:2502.00948, version 5, 17 May 2026; DOI 10.1016/j.disc.2026.115167.
https://arxiv.org/abs/2502.00948
The coefficient-stopping-time conjecture and paradoxical segments are established
literature. No published verification record or novelty priority is claimed here.
