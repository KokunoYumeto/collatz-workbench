# Bilateral original-source reductions, maximal integral lifts, and subquadratic support bounds

16 September 2026. Research continuation in `KokunoYumeto/collatz-workbench`.
The authenticated base is `b2dac4c2cc4a5eedde0af36d6749390c77fa4a62`,
`ternary_join_reduction_20260916`. The original integral receiver is
`intrinsic_zero_firstjet_20260915`. All earlier source files remain unchanged.

This note proves two complete new arithmetic families at every positive ternary
valuation, their exact disjointness from the preceding layer families, and an
all-depth refinement that selects the smallest source within each admitted
leading-run template. It also gives a complete finite two-sided catalogue and a
subquadratic bound on the original vertex support of the whole-source
retraction. The first-crossing window is verified through 11,610 odd steps by a
complete original-source certificate and an independent all-row audit.

These are bounds on specified constructions and proved source domains. They do
not assert that the residual root set is empty, that every orbit crosses, or that
a possible positive nontrivial cycle or nonperiodic component has been found.
No estimate from the Zeta programme is imported. The general arithmetic and
algebraic arguments below use no theorem on linear forms in logarithms.

## 1. Fixed original coordinates and the comparison receiver

Write X for the positive odd integers and retain

\[
 T(n)=\frac{3n+1}{2^{a(n)}},\qquad a(n)=\nu_2(3n+1).
\tag{1}
\]

An exponent word w=(a_1,...,a_k) has original prefix sums A_j, total A, and

\[
 L=3^k,\quad U=2^A,\quad
 C=\sum_{j=0}^{k-1}3^{k-1-j}2^{A_j},\quad
 f_w(n)=(Ln+C)/U.
\tag{2}
\]

The empty word has (L,U,C)=(1,1,0). Its complete positive odd source is 1+2t.
For every word retain the original cylinder and image

\[
 \rho+2Ut\longmapsto\eta+2Lt,\qquad t\ge0,
\quad \rho\equiv(U-C)L^{-1}\pmod{2U},\quad0<\rho<2U,
\quad\eta=(L\rho+C)/U.
\tag{3}
\]

Their inverse parameters are (n-rho)/(2U) and (y-eta)/(2L) on the displayed
images. The affine numerator satisfies the chronological recurrence C'=3C+U.
The terminal congruence in (3) gives every prefix oddness: reduce the full
numerator modulo 2^{A_j+1}, retain the j-prefix term, the next term of exact
valuation A_j, and the later terms divisible by 2^{A_j+1}. The resulting prefix
numerator is 2^{A_j} modulo 2^{A_j+1}. The successive original equations then
force the exact valuations a_j. This proves the word/cylinder correspondence
without replacing exact valuations by divisibility alone.

In particular 0<eta<2L. Positivity follows from rho>0. The same congruences at the
specified negative source rho-2U give the integral odd terminal eta-2L. Every
original odd-return image of a negative odd integer is negative; hence eta-2L<0.
This proves the image-anchor bound by two evaluations of the same affine map.
No identification of the positive and negative source domains is made.

The absolute first-jet complex has original edge and vertex bases E_n,V_n,
including E_1,V_1. Put

\[
 \mathbb D=\mathbb Z[\epsilon]/(\epsilon^2),\quad q=1+\epsilon,
 \qquad d_\epsilon E_n=V_n-qV_{T(n)}.
\tag{4}
\]

For every integer k, q^k=1+k epsilon; q^{-1}=1-epsilon is an integral unit.
Neither a cycle period nor a nonunit integer is inverted. The ordinary incidence
is d=J-P. The specified comparison kernel is

\[
 \mathfrak B_X=\ker\bigl(H^1(K_\epsilon)\to H^1(K)\bigr),\qquad
 \xi_n=[\epsilon V_n].
\tag{5}
\]

For an original finite path l:n->y of length s let B_l(n) be its weighted chain,
with coefficient q^j on its j-th edge. Telescoping gives

\[
 d_\epsilon B_l(n)=V_n-q^sV_y.
\tag{6}
\]

Thus two ORIGINAL paths l:n->y and r:m->y have the exact comparison

\[
 \boxed{d_\epsilon\bigl(B_l(n)-q^{s-t}B_r(m)\bigr)
       =V_n-q^{s-t}V_m,\quad t=|r|.}
\tag{7}
\]

Multiplication by epsilon gives xi_n=xi_m. This equality does not by itself
make either original class zero. It identifies their images through the original
finite integral relation, with both paths and their source labels retained.
In particular the integer m below is a smaller source with a common future, not
necessarily a forward iterate of n.

The predecessor proves that the full kernel (5) is a direct sum of Z/m_C Z for
actual nontrivial cycle components and Z for actual nonperiodic components. Its
finite integral witness equations are db=0, dc-Pb=V_n. They imply an actual path
to 1, extracted from the original support, since the cycle-component augmentation
would otherwise give -k*m_C=1 with m_C>1 or with no cycle. We retain that exact
receiver and independently replay the supplied original validator; no quotient
coefficient is silently rationalized.

## 2. Two nontrivial legs on every ternary layer

Fix b>=1 and e in {2,6}. Put

\[
 h_e=(2^e+2)/3\in\{2,22\},\qquad
 a=a(b,e)=\min\{a\ge1:2^{a+e+2b-1}<3^{a+b}\},
\]
\[
 J=2^{e+2b-1},\quad Q=3^{a+b},\quad K=2^aJ<Q.
\tag{8}
\]

These definitions involve only integer comparisons. The minimum exists, with

\[
 a(b,e)\le b+2e-2,\qquad
 a(b+1,e)-a(b,e)\in\{0,1\}.
\tag{9}
\]

At a=b+2e-2 the ratio K/Q is (8/9)^{b+e-1}<1. Increasing b multiplies the ratio
by 4/3; increasing a once more multiplies it by 2/3. Their product is 8/9<1,
which proves the upper increment, and monotonicity proves the lower increment.

The left ORIGINAL word is l=(1,2,1), whose map is (27n+23)/16 and whose source is
n=27 modulo32. The right word is

\[
 r_{b,e}=(1)^a,(e),(2)^{b-1},(1),(1),(3).
\tag{10}
\]

It has a+b+3 odd returns and exponent sum a+e+2b+3. Define the exact source set

\[
 \mathcal S_{b,e}=\{n>0:n\equiv27\pmod{32},\quad
                         Jn+h_e3^b\equiv0\pmod Q\}.
\tag{11}
\]

The moduli 32 and Q are coprime, so this is one complete positive residue class
modulo32Q. Let its representative in (0,32Q) be n_0 and put

\[
 m_0=(Kn_0+2^ah_e3^b)/Q-1,\qquad y_0=(27n_0+23)/16.
\]

### Theorem 1. Complete bilateral joins at every positive ternary valuation

For every b,e above, the entire designated original source fibre is

\[
 \boxed{\begin{aligned}
 n(t)&=n_0+32Qt,\\
 m(t)&=m_0+32Kt,\\
 y(t)&=y_0+54Qt,\qquad t\in\mathbb Z_{\ge0},
 \end{aligned}}
\tag{12}
\]

with the original paths

\[
 n(t)\xrightarrow{\ (1,2,1)\ }y(t)
       \xleftarrow{\ r_{b,e}\ }m(t),\qquad0<m(t)<n(t).
\tag{13}
\]

Every n(t) has actual nu_3(n(t))=b. Its unit n(t)/3^b is 2 modulo3 for e=2 and
1 modulo3 for e=6. All these sources have no incoming original odd-return edge.

**Proof with all intermediate values.** Congruence (11) forces 3^b|n. Write
n=3^b z. Then Jz+h_e=0 modulo3^a. Since J=2 modulo3 and h_e is a ternary unit,
z is a unit of the asserted class. Thus b is the exact valuation.
Set W=(Jz+h_e)/3^a. It is a positive even integer of exact dyadic valuation one:
J is divisible by eight and h_e=2 modulo4, while the divisor is odd. Define
m=2^aW-1, which is positive odd. Its first a original values are

\[
 x_j=3^j2^{a-j}W-1\quad(0\le j\le a).
\tag{14}
\]

For j<a, x_j+1 is divisible by four, giving exact next exponent one. At j=a,

\[
 x_a=Jz+h_e-1=2^{e-1}(4/3)^b n+h_e-1.
\tag{15}
\]

Because 3h_e-2=2^e, the next exponent is exactly e and its image is

\[
 v_0=1+2\,4^{b-1}n/3^{b-1}.
\]

The following b-1 exponents are exactly two, with original values

\[
 v_j=1+2\,4^{b-1-j}n/3^{b-1-j}\quad(0\le j\le b-1).
\tag{16}
\]

For j<b-1 the nonconstant part is divisible by eight, which proves exactness of
those valuations. Their last value is 2n+1. The remaining original values are

\[
 2n+1\xrightarrow{1}3n+2\xrightarrow{1}(9n+7)/2
                \xrightarrow{3}(27n+23)/16.
\tag{17}
\]

The residue n=27 modulo32 proves all three exact valuations. It also proves the
left path n -> (3n+1)/2 -> (9n+5)/8 -> (27n+23)/16 with exponents (1,2,1).
Conversely equality of the original two endpoint formulas gives
m=(Kn+2^ah_e3^b)/Q-1 and hence (11); the left path requires n=27 modulo32.
Thus the source domain is exact, rather than a subset justified only by samples.

The height difference is controlled by

\[
 m=(K/Q)n+h_e(2/3)^a-1.
\tag{18}
\]

The defining comparison K/Q<1 gives

\[
 h_e(2/3)^a<(2h_e/2^e)(3/4)^b<1.
\tag{19}
\]

Both terms in (18) therefore make m<n. Positivity follows from m=2^aW-1.
CRT gives (12); subtraction and division in any one of the three displayed
progressions supplies the inverse parameter. An incoming edge to n would require
3x+1=2^c n=0 modulo3, which is impossible. This proves every assertion. QED.

The smallest displayed case b=1,e=2 has a=3:

\[
 \boxed{1275+2592t\longrightarrow2153+4374t
                  \longleftarrow1007+2048t.}
\tag{20}
\]

At t=0 the original left path is 1275,1913,1435,2153. The original right path is
1007,1511,2267,3401,2551,3827,5741,2153. The difference of the two sources is
268+544t>0. This family can already overlap a finite catalogue; its full
integral relation remains valid there.

The case b=2,e=6 has a=10:

\[
 n(t)=8808219+17006112t,\qquad
 m(t)=8689663+16777216t,
\tag{21}
\]

with the common endpoint (27n(t)+23)/16. This is an unbounded family of original
sources beyond the finite verification interval below, not an extrapolation from
that interval.

## 3. The old and new layer families have no common source

The preceding published families use

\[
 J^{\rm old}_{b,e}=2^{e+2b},\quad
 J^{\rm old}_{b,e}(n/3^b)+h_e=0\pmod{3^{a^{\rm old}(b,e)}},
 \quad n=3\pmod4,
\tag{22}
\]

where a^old is the least positive a with 2^{a+e+2b}<3^{a+b}. Their unit classes
are 1 modulo3 for e=2 and 2 modulo3 for e=6.

### Theorem 2. Exact disjointness, including the first nonreduced lift

The union of the new families (11) is disjoint from the union of all the old
families (22). Families with different b are disjoint by the original valuation;
at a fixed b the two e values are disjoint by the original unit class.

**Proof.** The only possible mixed intersections at a fixed b pair new e=2 with
old e=6, or new e=6 with old e=2. In the first case J^old_6=32J^new_2. Multiplying
the new congruence by 32 and subtracting the old gives the constant

\[
 32h_2-h_6=64-22=42,\qquad\nu_3(42)=1.
\tag{23}
\]

In the second case J^new_6=8J^old_2, giving

\[
 h_6-8h_2=22-16=6,\qquad\nu_3(6)=1.
\tag{24}
\]

Every precision in these possible pairs is at least two; this follows either
from (8),(22) at b=1 and monotonicity, or by checking that a=1 cannot contract.
Either intersection would therefore force 9|42 or 9|6, a contradiction. QED.

The matching congruences can agree modulo3 and disagree modulo9. Equations
(23)-(24) retain exactly the obstruction at the next lift. Thus matching a unit
class alone would not establish an overlap; the original coefficient maps and
prime-power precision are essential. This statement concerns the displayed
integer source congruences, not an unproved identification with a Zeta conductor.

## 4. Maximal leading runs: the whole extra-depth axis in one finite calculation

The original source is preserved while all allowed leading runs are compared.
For n in (11), set

\[
 Z=J(n/3^b)+h_e,\qquad A_{\max}=\nu_3(Z).
\tag{25}
\]

### Theorem 3. Exact maximal lift and its full parameter strata

The possible original leading runs in this fixed template have a'<=A_max.
Every contracting one has a<=a'<=A_max, with smaller source

\[
 m_{a'}=2^{a'}Z/3^{a'}-1.
\tag{26}
\]

The smallest of these sources is m_{A_max}. For a'<A_max, the original edge
T(m_{a'+1})=m_{a'} has exact exponent one. The original maximum vertex on these
right paths is independent of a': their initial rises end at the same Z-1 and
all subsequent vertices coincide.

**Proof.** Integrality of the forced endpoint formula requires 3^{a'}|Z, hence
exactly a'<=A_max. Division by an odd power leaves nu_2(Z/3^{a'})=1, so (14)-(17)
prove the actual words. All a'>=a contract by the comparison in (8). Equation
m_{a'+1}+1=(2/3)(m_{a'}+1) proves strict decrease and, since the first odd value
has its plus-one valuation at least two, the exact exponent-one edge. The
initial rise ends at Z-1 for every a', and is increasing up to that point;
the common remaining path proves the maximum assertion. QED.

This theorem exhausts the admitted leading-run axis for the specified template.
It makes no claim that every possible right-word shape is one of these templates.

There is an exact all-depth partition of the ORIGINAL family parameter. Write
n=n_0+32Qt and

\[
 W_0=(J(n_0/3^b)+h_e)/3^a.
\]

Then

\[
 Z=3^a(W_0+32Jt).
\]

For an extra depth r>=0 and a retained unit u in {1,2}, its entire stratum is

\[
 \boxed{t=t_0+3^{r+1}s,\quad
 t_0\equiv(3^r u-W_0)(32J)^{-1}\pmod{3^{r+1}},
 \quad0\le t_0<3^{r+1},\quad s\ge0.}
\tag{27}
\]

Here A_max=a+r. The complete source and smaller-source steps are respectively

\[
 32Q\,3^{r+1},\qquad 2^{a+r}(32J)3.
\tag{28}
\]

Their constants are obtained from n(t_0) and
2^{a+r}(W_0+32Jt_0)/3^r-1. Both are original positive integers. The inverse is
s=(t-t_0)/3^{r+1}; exact valuation r follows from the displayed nonzero unit u.
Every t>=0 belongs to exactly one such stratum because W_0+32Jt is positive.
The same inverse parameters compute its common original endpoint. Thus arbitrary
extra depth is retained without a truncation or a generic large-depth flag.

### Exact comparison with the minimal-run relation

Let B_min be (7) for the minimal-run pair, with clock k_min. Let I be the original
r-edge incoming path from m_{A_max} to m_a. Its weighted chain obeys
 d_epsilon I=V_{m_Amax}-q^r V_{m_a}. The maximal pair therefore has chain

\[
 \boxed{B_{\max}=B_{\min}-q^{k_{\min}-r}I.}
\tag{29}
\]

The two original right words concatenate as 1^r followed by the minimal right
word, so this is an equality of original weighted chains, not only of boundaries.
Maximization does not supply a different root-exclusion domain: it refines the
same admitted family by composing its original relation with r existing incoming
ones. That distinction is retained in the implementation.

There is also a source-size bound on the chosen run. Put k=floor(log_3 n),
computed as the largest integer with 3^k<=n. Since J+h_e<3^{e+2b-1} and
n/3^b<3^{k+1-b},

\[
 Z\le(J+h_e)n/3^b<3^{k+b+e},\qquad
 A_{\max}\le k+b+e-1.
\tag{30}
\]

This is a proved finite search bound and an exact one-step valuation evaluation;
it is not an assumption about an arbitrary orbit's stopping time.

## 5. Complete two-leg catalogue with both nonempty original words

For original words l,r, keep all five affine data (L,U,C,rho,eta) from (2)-(3).
Put g=gcd(L_l,L_r). Their target images intersect exactly when

\[
 \eta_l\equiv\eta_r\pmod{2g}.
\tag{31}
\]

Let y_0 be the least common image value at least max(eta_l,eta_r), and put
u_0=(y_0-eta_l)/(2L_l), v_0=(y_0-eta_r)/(2L_r). Then all compatible pairs are

\[
\begin{aligned}
 n(t)&=n_0+2U_l(L_r/g)t,&n_0&=\rho_l+2U_lu_0,\\
 m(t)&=m_0+2U_r(L_l/g)t,&m_0&=\rho_r+2U_rv_0,\\
 y(t)&=y_0+2(L_lL_r/g)t,&t&\ge0.
\end{aligned}\tag{32}
\]

The common target and its period give the inverse t. The original source
parameters are u=u_0+(L_r/g)t and v=v_0+(L_l/g)t, with the inverse obtained by
subtraction and division. The height condition is exactly

\[
 (n_0-m_0)+\bigl(2U_lL_r/g-2U_rL_l/g\bigr)t>0.
\tag{33}
\]

It specifies an integer interval with either slope sign, which is retained even
when empty. Formula (31) follows from the congruence compatibility criterion;
(32) follows by adding the common target period. Thus both inverse maps and all
images are proved. No independent-distribution premise is used.

The new finite domain has these five left words:

\[
 (1,1),\ (1,2),\ (1,1,1),\ (1,1,2),\ (1,2,1).
\tag{34}
\]

They are all the indicated length-two and length-three words before coefficient
crossing. For each left word and each right length 1<=j<=12, include EVERY positive
exponent word r with

\[
 2^{A_r}L_l<U_l3^j.
\tag{35}
\]

The total sum A_r has a finite exact ceiling B(l,j), computed by integer powers.
There are binom(B(l,j),j) right words when B(l,j)>=j. This is the positive-
composition identity obtained by adjoining the unused budget as a final
nonnegative coordinate. Hence the complete domain has 112,050 pairs.

Of these, 24,107 satisfy (31). The complete certificate proves that each of
these has domain t>=0, positive constant and slope in (33), and
0<n_0<2U_lL_r/g. Both original affine coefficient columns are replayed after
EVERY original odd step and division: the endpoint constant is odd, its slope
is even, and their divisions have exactly the declared exponent. Thus the
certificate proves the entire infinite family at each row, not only its anchor.
The other 87,943 pairs are retained incompatible labelled faces.

These whole-family height assertions are finite, computer-assisted statements
on the explicitly bounded domain (34)-(35). They are not extended to all word
pairs without proof. The general formulas (31)-(33) remain valid for any words.

### The exact residue cover and its independent comparison

The published one-left-edge catalogue comprises all right words of lengths
2 through 12, with odd last exponent and 2^{A_r-1}<3^{j-1}. The new code
reconstructs its complete 20,397 words and its stated original source formulas.
The old initial arithmetic root condition is

\[
 n\bmod36\in\{3,7,15,19,27\},\quad
 n\not\equiv8731\pmod{8748},\quad n\not\equiv1731\pmod{2916}.
\tag{36}
\]

Before the published infinite layers are removed, the old catalogue leaves
93,025 root residues modulo P_0=708,588, using 370 selected original families.

Use the common new period P=8P_0=5,668,704. The lifted old set has 744,200 residues.
Visit the compatible new pairs in the declared order
(source period, first admitted source, total word length, left word, right word).
Select a family exactly when it removes a previously retained root residue.
This yields 67 selected families and 739,770 residual residues: 4,430 are removed
from this periodic set. A separate union of ALL 24,107 compatible families, in
reverse order, gives exactly the same resulting set R_new.

The complete 112,050-row ledger includes incompatible faces. An independent
checker imports no contribution or predecessor module, verifies original
coefficient formulas and valuations, checks strict lexical order and the exact
binomial count in EVERY domain bucket, and independently rebuilds both residue
masks. Completeness is therefore a proved finite-domain count together with all
rows, not an observed sample. These counts describe the specified reductions;
they are not counts or probabilities of Collatz counterexamples.

The periodic count precedes the old and new infinite layer subtractions. In
particular 4,430 is not being called the number of new classes remaining after
an uncomputed overlap with the old infinite layers.

### Which of the new infinite layers lie beyond the finite catalogue

The new e=2 families b=1,2,3,4 and e=6 family b=1 are entirely covered by the
finite stage. Every new e=2 family b>=5 and new e=6 family b>=2 lies entirely
inside its retained periodic root set and is therefore a further removal.

For 1<=b<=10 the complete residue comparison is included in the certificate:
list every residue in the image (12) modulo P and test the complete mask, using
its exact period divisibility. At b>=11 every source has 3^11|n and n=27 modulo32;
CRT gives the single residue 177147 modulo P. That residue is retained. This
proves the assertion at ALL larger layers, rather than extrapolating from a
finite b sample. Theorem 2 also proves these new sources were not removed by
any old infinite layer. Thus the cited surviving layers supply genuinely new
root reductions at arbitrarily large valuations.

## 6. A whole-source integral retraction, with its edge relations retained

Use three ordered rule stages. Stage 0 uses the published rules: one-return
forward descent; then the original image inverses of (1), (1,2), and
(1,1,1,2,1,1,4); then the old (b,e)=(1,2) join; then the 370-family catalogue;
then the old infinite-layer test (22). Stage 1 uses the 67 new families after
all stage 0 rules fail. Stage 2 uses (11), with its maximal-run choice (25), after
all stage 1 rules fail. The original fixed point1 is left as a root.

Each rule gives a finite original chain B_n and a smaller positive odd source
pi(n), with a signed integer clock k_n and

\[
 d_\epsilon B_n=V_n-q^{k_n}V_{\pi(n)}.
\tag{37}
\]

A root has H(V_r)=0 and Q(V_r)=V_r. At any other source set

\[
 H(V_n)=B_n+q^{k_n}H(V_{\pi(n)}),\quad
 Q(V_n)=q^{k_n}Q(V_{\pi(n)}),\quad F=I-Hd_\epsilon.
\tag{38}
\]

Every selected source decreases by at least two. The recursion therefore
terminates at a retained root for EVERY original input, without assuming
Collatz. Its intermediate original path vertices need not decrease.

### Theorem 4. Nested original chain retractions

For each stage the maps in (38) satisfy

\[
 d_\epsilon H=I-Q,\quad Q^2=Q,\quad HQ=0,
 \quad d_\epsilon F=Qd_\epsilon,\quad F^2=F,\quad FH=0.
\tag{39}
\]

The inclusion of [im F -> im Q], its projections F,Q, and H are an integral
chain-homotopy retraction. In edge degree the complete presentation is

\[
 C^0_{\mathbb D}/\operatorname{im}H\xrightarrow{\sim}\operatorname{im}F,
 \qquad[e]\mapsto Fe.
\tag{40}
\]

For any earlier/later pair of the three stages, with K=H_new-H_old,

\[
 F_{old}K=K,\quad F_{new}F_{old}=F_{old}F_{new}=F_{new},
 \quad Q_{new}Q_{old}=Q_{old}Q_{new}=Q_{new}.
\tag{41}
\]

**Proof.** Equation (37) telescopes to dH=I-Q. The map Q ends at roots and H is
zero there, proving Q^2=Q,HQ=0. Substituting these into F=I-Hd gives the last
three identities in (39), including FH=H-H(I-Q)=0. Also I-F=Hd is the edge-degree
homotopy equation. If Fe=0, then e=Hde is in im H; conversely FH=0 kills im H.
Thus ker F=im H, and the inverse of (40) sends Fe to [e]. In particular projected
edge columns are not assumed to be an independent new basis.

All earlier rules have priority. A later route therefore follows the earlier
route unchanged until its old root, including its terminal q-power, and then
continues there. Hence H_new=H_old+H_new Q_old and Q_new=Q_new Q_old.
The later final root is also an earlier root, so Q_old Q_new=Q_new. Applying d
and HQ=0 yields dK=Q_old-Q_new, H_old dK=0, hence F_old K=K. Substitution of
H_new into both products of I-Hd gives (41). These arguments use the actual
paths and coefficients, not only abstract isomorphism types. QED.

The choices depend on original integers, not on epsilon. Constant reduction
commutes with the maps and sends every q^k to 1. It therefore induces the same
comparison-kernel equivalence (5) at every stage. E_1 is retained and FE_1=E_1.
A longer actual weighted period has boundary (1-q^m)V_c=-m epsilon V_c; no
division by m is permitted. The integral cycle-index torsion and the free
nonperiodic summands remain represented.

For a finite declared equation support E, include its original targets and the
supports of their finite H columns. This enlargement commutes with unions and
inclusions. The resulting maps are the literal component maps in the Split-Zero
support diagram. They retain the original relation submodule, not an inferred
chronological log or an abstract zero without its map.

## 7. Subquadratic original-support bounds, including maximal lifts

Let k(n) be the largest integer k with 3^k<=n. Define the integer-computable bound

\[
 \boxed{R(n)=\max\{130(n+1),\lfloor64n\,4^{k(n)}/3^{k(n)}\rfloor+21\}.}
\tag{42}
\]

Also put

\[
 \boxed{K(n)=\frac{n-1}{2}\bigl(3k(n)+14\bigr)}\qquad(n\text{ odd}).
\tag{43}
\]

### Theorem 5. Bounds on the complete original homotopy columns

For every original odd n>=3, every original odd vertex in H(V_n), including
vertices in the two uncollected paths of each selected relation, is at most R(n).
There are at most K(n) uncollected signed monomial edge terms. The collected
constant coefficients have total absolute sum at most K(n); the epsilon
coefficients have total absolute sum at most K(n)^2.

For n>=27,

\[
 R(n)=\lfloor64n\,4^{k(n)}/3^{k(n)}\rfloor+21
       \le64n^{\log_3 4}+21.
\tag{44}
\]

Thus the original-support growth exponent is log_3(4), approximately1.262,
rather than the earlier coarse quadratic bound. The exact operational bound is
(42), with integer powers; no floating-point exponent is needed by the checker.

**Proof.** A selected source x in the route is at most n. Every finite-catalogue
or inverse leg has length at most 12 and begins below or at x. On positive inputs
g_a(y)<=g_1(y)=(3y+1)/2, and g_1^j(y)=(3/2)^j(y+1)-1. Thus these legs stay below
130(n+1). The three-edge left leg also obeys that bound.

For an old layer at x with b=nu_3(x), the explicit largest initial rise is at most
64x(4/3)^b+21, and the following falling vertices do not increase it. For a new
layer, the initial rise ends at (15), at most 32x(4/3)^b+21. The later vertices in
(16)-(17) are bounded by this or by (9x+7)/2, in turn below the bound with 64.
The maximal-lift theorem proves that increasing its leading run changes neither
this peak nor the later path. Since b<=k(n), all these values are bounded by the
second term of (42). Integer rounding gives the stated exact bound.

There are at most(n-1)/2 moves. The finite pairs have at most 15 total edge terms.
Old layers have at most 2b+14. By (30), new maximal layers have at most
A_max+b+6<=k(n)+2b+e+5<=3k(n)+11. The uniform factor3k(n)+14 therefore bounds
all moves. This proves (43). Every term is a signed q-power whose exponent is a
sum of earlier signed leg lengths and a position in the current leg. Its absolute
value is at most the total uncollected edge count K(n). Expansion q^j=1+j epsilon
and the triangle inequality prove the two collected coefficient bounds.

For k>=3, 64(4/3)^k>=4096/27>130. At n>=27 this gap, with the retained +21,
dominates130(n+1) even after flooring. Finally3^k<=n implies
(4/3)^k<=(n)^{log_3(4/3)}, proving (44). QED.

The actual source-height maps consequently obey

\[
 Q(C^1_{\le n})\subset C^1_{\le n},\quad
 H(C^1_{\le n})\subset C^0_{\le R(n)},\quad
 F(C^0_{\le n})\subset C^0_{\le R(2n)}.
\tag{45}
\]

The last uses T(x)<2x. Expanding every odd-return edge into its original odd step
and divisions gives intermediate positive integers at most3R(n)+1 for an H column.
The factors and clock assignment in that expansion are the original ones.

These bounds apply on the WHOLE original source, including unresolved roots.
They are bounds for the chosen retraction, not bounds on all Collatz stopping
times. At a retained root its H column is zero with its source and relations
still present; no conclusion of convergence is attached to that zero column.

## 8. The exact remaining roots

Let R_new be the 739,770-residue periodic set from Section 5. The final nonbase
roots are exactly

\[
 \boxed{\{n>1:n\bmod5668704\in R_{new}\}
   \setminus\left(\bigcup_{b,e}\mathcal R^{old}_{b,e}
                  \ \cup\ \bigcup_{b,e}\mathcal S_{b,e}\right).}
\tag{46}
\]

Both unions range over every b>=1 and e in {2,6}. Membership is a finite original
calculation: compute nu_3(n), its unit, and the matching old/new congruence. The
new mask also supplies the n=27 modulo32 restriction. No infinite search over b
or cutoff for maximal depth is used. The basepoint 1 is separately retained.

Every least integer of an actual component away from 1 lies in (46): an accepted
original shared-future relation would give a smaller original integer in that
same component. This follows from the two paths, not from assuming that a lower
source is already in the base component. Root residue counts therefore restrict
possible component minima; they do not count such components.

## 9. The longer sharp crossing window

The source envelope is reproduced from the preceding exact calculation, not
claimed as a new theorem in this increment. Put

\[
 b_j=\operatorname{bitlength}(3^j)-1,\quad b_0=0,\quad
 C_0^*=0,\quad C_m^*=3C_{m-1}^*+2^{b_{m-1}},
\]
\[
 D_m^*=2^{b_m+1}-3^m,\qquad\Theta_m=C_m^*/D_m^*.
\tag{47}
\]

At a first coefficient crossing with m odd returns, all proper A_j<=b_j and the
final A_m>=b_m+1. The exact difference

\[
 C_m^*-C_p=\sum_{j=0}^{m-1}3^{m-1-j}(2^{b_j}-2^{A_j})\ge0
\]

and D_p>=D_m^*>0 give C_p/D_p<=Theta_m. Equality occurs at the original word with
proper prefix sums b_j and final sum b_m+1. Thus the bound is sharp on its word
domain, not necessarily attained at an integer non-descending source. The
original non-descent equation gives n<=floor(Theta_m).

For the shortened map, the first crossing with m odd steps occurs after exactly
b_m+1 total shortened steps. Its numerator is the same C_p, even when it occurs
before the last odd-return edge has finished all its divisions. The envelope
therefore bounds exceptions at that original, possibly even, endpoint as well.
The exact expansion of an odd exponent a is one shortened odd step followed by
a-1 shortened even steps; this retains both clocks.

The complete integer recurrence through m=11610 gives

\[
 \max_{1\le m\le11610}\lfloor\Theta_m\rfloor=8129266,
 \quad\text{record at }(m,b_m+1)=(10946,17349).
\tag{48}
\]

The next record is (11611,18403,9966964). All 4,064,632 original odd sources from 3
through 8,129,265 have been scanned and independently replayed. Each has a first
coefficient crossing, strictly below its source at BOTH the first shortened
crossing and the final odd-return endpoint. There are 14,186,680 odd-return
relations and 28,378,002 independently repeated divisions in the full audit.

Together with the proved envelope, this finite certificate establishes:

> Every positive integer n>=2 whose first shortened coefficient crossing involves
> at most 11,610 odd steps strictly descends at that crossing.

Even starting integers descend at the first division; the odd cases above and
the envelope prove the rest. The starting integer and final exponent are not
bounded in this statement. Sources with no such crossing remain unclaimed.

The two producer runs, ordinary and optimized, are byte-identical. The independent
auditor imports no contribution or predecessor module, reads EVERY source row,
performs the original divisions separately, reconstructs the envelope with a
critical-prefix recurrence, and checks the smaller-source induction table. The
largest observed first crossing is 155 odd returns at 8,088,063; the largest
inductive total is 248 odd returns at 6,649,279. Those observations are not used
as unproved global clock bounds. The largest odd vertex appearing in the audited
crossing paths is 20,114,203,639,877, reached from 6,631,675; all large values are
retained as exact integers.

The smaller positive odd endpoints supply strong induction to 1 on the entire
finite interval. In particular the height-filtered original kernel
F_N=<xi_n:n<=N> has F_8129265=0, with its original finite integral witnesses.
An arbitrary lower-source relation xi_n=xi_m with m<n only kills the associated
height increment; it does not erase that retained lower subgroup.

Coefficient stopping time and merging/sufficient-set methods have established
literature; see [RT] and [M]. No priority or published verification record is
claimed. The new unrestricted family proofs do not depend on the scan or on a
literature bound.

## 10. What the results do and do not close

Any least vertex of a nonbase component must exceed 8,129,265, lie in (46), and
have no first coefficient crossing involving at most 11,610 odd steps. These are
simultaneous necessary conditions on original positive integers. The proof has
not shown that their intersection is empty.

The new all-layer domains are disjoint from the published ones, and their
maximal leading runs now have complete residue strata and bounds. The finite
two-sided domain is fully certified, and its exact cover is explicit. The
whole-system retraction has a smaller global support-growth bound while keeping
its residual component module. None of these facts assumes that a finite open
frontier is an infinite orbit or that a zero in a rationalized module vanishes
integrally.

The next arithmetic targets are further right-leg templates or genuinely new
left-leg patterns on (46), and residue-aware restrictions on the exact canonical
crossing sources. The next fixed crossing-record calculation has horizon 11611
and odd candidate ceiling 9,966,963. These are stated remaining calculations,
not scheduled tasks or assumed results. A single ever-larger finite certificate
does not establish that every original singleton vanishes.

The predecessor bound Theta_m>m/6 follows from 2^{b_j}>3^j/2 and
D_m^*<3^m, so no fixed finite source interval covers all crossing horizons under
that envelope. A global proof needs additional arithmetic on the original
remaining source, or a rigorously surviving integral source class for a
counterexample. The supplied maps preserve that distinction.

## 11. Executed evidence and source lineage

`verify.py` checks the complete 112,050-pair domain, all 24,107 compatible variable
families, all 20,397 old candidate families, both residue unions, the layer
formulas and saturation strata, original signed chain maps, the nested
retractions, support/length bounds, and four original singleton witness
extractions. It rejects seventeen malformed controls. General family statements
have the written proofs above; finite symbolic-family rows are complete finite
proof components, and point fixtures are regression evidence only.

The structural pair has 1,905,007 named checks per run and byte-identical output.
The all-pair auditor independently checks 112,050 rows and 332,467 original affine
row equations. The full source scan and its independent audit have the separate
scopes in Section 9. Counts are not summed and reported as a number of theorems.
The actual command receipts and file hashes identify the executed bytes.

The source programme and Split-Zero framework are attributed to KokunoYumeto.
This tool-assisted continuation develops the new arithmetic, proofs, and checks;
it is not an independent external mathematical review. No new Lean execution is
claimed. The complete earlier contribution is neither relicensed nor rewritten.

[WB] KokunoYumeto, Collatz workbench, `ternary_join_reduction_20260916/note.md`,
commit b2dac4c2cc4a5eedde0af36d6749390c77fa4a62. Full relevant source text and
implementation priority were read through the authenticated GitHub connector.
The new code reconstructs its arithmetic rules; it does not claim that a full
remote checkout was replayed. The local preceding height-window source is also
retained as lineage, not silently reported as newly published.

[IJ] `intrinsic_zero_firstjet_20260915/firstjet.py`, Git blob
97f9ef5ad535f7ec18259d41fab6a3557be17d98, is the unchanged executable receiver.
Its byte identity is checked before every imported witness verification.

[RT] Olivier Rozier and Claude Terracol, *Paradoxical behavior in Collatz
sequences*, arXiv:2502.00948v5 (17 May 2026), definitions 1.1–1.2 and discussion of
Terras' coefficient stopping-time conjecture. Source for attribution, not an
input to the present arithmetic proofs.
https://arxiv.org/html/2502.00948v5

[M] Keenan Monks, Kenneth G. Monks, Kenneth M. Monks and Maria Monks, *Strongly
sufficient sets and the distribution of arithmetic sequences in the 3x+1 graph*,
arXiv:1204.3904. Prior merging/sufficient-set context; no result from that paper
is used without an additional map or invoked as a premise here.
https://arxiv.org/abs/1204.3904
