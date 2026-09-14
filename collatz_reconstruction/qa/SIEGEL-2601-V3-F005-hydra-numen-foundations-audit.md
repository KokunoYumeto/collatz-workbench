# SIEGEL-2601-V3-F005 — Hydra and numen foundations audit

## Status and controlling witness

This is a content-level audit of the foundational Hydra, numen, and
Correspondence-Principle part of Maxwell C. Siegel, *The Hydra Map and Numen
Formalisms for Collatz-Type Problems*, arXiv:2601.17030v3. It is not a review
of the entire paper and it is not a completion claim for the Siegel corpus.

- frozen route: DOCROUTE-COL-DDC6C05F3E6FF90BDB1B
- logical work: WORK-0010
- arXiv identity: 2601.17030v3, submitted 2026-02-12
- controlling source TeX:
  C:/Users/LOCAL_USER/Documents/Papors/Eigen shizzle/p-adic collatz duder/_online_archive_2026-08-16/latex/2601.17030v3/Hydra_Map_Formalism.tex
- source-TeX bytes: 120443
- source-TeX SHA-256:
  53d55d69acb7af48efd6af1a37c70bfcd858a82b9d56571d8cc0282063dcb8b1
- arXiv source-archive SHA-256:
  3efea2ef685040d6d0c613dfa247b7ac43c6d71b2cb60c88cbeb2aaca5a10680
- controlling layout PDF:
  C:/Users/LOCAL_USER/Documents/Papors/Eigen shizzle/p-adic collatz duder/_online_archive_2026-08-16/pdf/2601.17030v3.pdf
- layout-PDF bytes: 669678
- layout-PDF SHA-256:
  d596e33a651b05300d96a4c2719fae64022eb1abea6b2063a132f08a780139f8
- topical shelf source:
  C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/source/2601.17030v3.eprint
- topical shelf TeX:
  C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/latex/2601.17030v3/Hydra_Map_Formalism.tex

The source TeX was read at lines 606–1604. Printed pages 7–20 were read and
visually checked; printed page 21 was checked as the section boundary.
Definition 7.3 and Propositions 7.4–7.6 were then read at lines 1900–2166 and
printed pages 25–29; printed pages 27–29 were visually checked in full.

The v2-to-v3 source comparison was checked. Sections 4–6 are unchanged
mathematically between v2 and v3. The material v3 change is in Section 7,
where an adjoint-identity formula receives its missing argument and the
Fourier-inversion normalization is changed to include the local degree. The
remaining Fourier defects below survive that revision.

The completed sibling Siegel status map was used only to locate likely fault
lines after the primary source had been read. Every finding below was checked
against the version-pinned TeX. No sibling status label is evidence for
admission here.

## Exact source data and composition order

Let \(K\) be the source's global field, let \(\mathbb F\) be its base field,
let \(\mathcal O_K\) be its integer ring, and let
\(\Lambda\subsetneq\mathcal O_K\) be a nonzero ideal of finite index \(p\).
After choosing and retaining an enumeration of
\(\mathcal O_K/\Lambda\), the branch indexed by
\(j\in\{0,\ldots,p-1\}\) is

\[
H_j(z)=r_j(z)+c_j,
\qquad
r_j\in\operatorname{End}_{\mathbb F}^{\times}(K),
\quad c_j\in K.
\]

The operators \(r_j\) are not assumed to be scalar multiplications. Operator
products below mean composition in the displayed order.

For a finite word
\(\mathbf j=(j_1,\ldots,j_N)\), the source uses least-significant digit first:

\[
\operatorname{DigSum}_p(\mathbf j)
=\sum_{a=1}^{N}j_ap^{a-1}.
\]

Its affine word is

\[
H_{\mathbf j}=H_{j_1}\circ\cdots\circ H_{j_N}.
\]

Thus the rightmost branch \(H_{j_N}\) acts first on an input. Put

\[
M_{\mathbf j}=r_{j_1}\circ\cdots\circ r_{j_N},
\qquad
X_{\mathbf j}=H_{\mathbf j}(0).
\]

With \(P_0=I\) and
\(P_m=r_{j_1}\circ\cdots\circ r_{j_m}\), direct affine composition gives

\[
X_{\mathbf j}
=\sum_{m=0}^{N-1}P_m(c_{j_{m+1}}).
\]

For concatenation \(\mathbf i\wedge\mathbf j\), the exact identities are

\[
M_{\mathbf i\wedge\mathbf j}
=M_{\mathbf i}\circ M_{\mathbf j},
\qquad
X_{\mathbf i\wedge\mathbf j}
=M_{\mathbf i}(X_{\mathbf j})+X_{\mathbf i}.
\]

These are valid finite-word results from source Definitions 6.1–6.2 and
Proposition 6.1. They do not require a convergence hypothesis and do not
assert that the word is the actual itinerary of a point.

## Preliminary type defects that affect the formalism

Four earlier statements must be repaired before the displayed objects can be
used at their full stated scope.

1. Printed page 9 says that every \(\mathcal O_K\) has a finite
   \(\mathbb Z\)-basis. That is the number-field case. The paper explicitly
   also allows finite extensions of \(\mathbb F_q(T)\), where the correct
   coefficient ring is
   \(\mathcal O_{\mathbb F}=\mathbb F_q[T]\):
   \(\mathcal O_K\) is a finite torsion-free, hence free, module over that PID.
   The same coefficient-ring correction is needed for the word “lattice.”
2. In Definition 6.3, an element \(i\in\mathcal O_K/\Lambda\) is itself a
   coset, so the enumeration condition is
   \(i=\Lambda_{\beta(i)}\), not \(i\in\Lambda_{\beta(i)}\). After replacing
   cosets by digit labels, \(\operatorname{DigSum}_p\) uses the digits \(j_n\)
   directly; applying \(\beta\) again is ill-typed.
3. The quotient model
   \(\mathbb Z[[x]]/(x-p)\) can be identified with the \(p\)-adic completion
   when equipped with the quotient of the \(x\)-adic topology. The source's
   ideal \((x-p)\) is the kernel of that quotient, not a maximal ideal, and its
   zero image cannot induce the asserted topology. The invariant definition
   used here is
   \(\mathbb Z_p=\varprojlim_n\mathbb Z/p^n\mathbb Z\), including composite
   \(p\).
4. The source's operator-norm supremum includes \(z=0\) while dividing by
   \(|z|_\ell\). The domain must exclude zero. More substantially, an
   arbitrary \(\mathbb F\)-linear endomorphism of \(K\) need not be bounded at
   a chosen place and therefore need not extend to \(K_\ell\). For
   \(K=\mathbb Q(\sqrt2)\) at one real embedding, field conjugation is an
   invertible \(\mathbb Q\)-linear map, but rational approximants to
   \(-\sqrt2\) give nonzero \(z_n\to0\) whose conjugates do not tend to zero.
   Every completion-level use below therefore includes finite operator norm,
   equivalently continuity at that place, as a hypothesis.

## The two integrality predicates are incompatible as printed

Source Definition 5.3 requires every affine extension to satisfy

\[
H_j(z)\in\mathcal O_K
\quad\text{for every }z\in\mathcal O_K
\quad\text{and every }j.
\tag{G}
\]

Source Definition 5.4 then calls the Hydra *integral* when

\[
H_j(z)\in\mathcal O_K
\quad\Longleftrightarrow\quad
z\in j+\Lambda
\quad(z\in\mathcal O_K).
\tag{E}
\]

Since \(\Lambda\) is proper, \(p\ge2\). Fix \(j\) and choose
\(z\in\mathcal O_K\setminus(j+\Lambda)\). Condition (G) says that
\(H_j(z)\) is integral, while (E) says that it is not. Consequently no
object can satisfy both literal definitions. In particular, Theorem 6.1 has
an empty hypothesis class when the paper's definitions are read literally.

The source's own shortened Collatz example confirms the intended distinction:
\((3z+1)/2\) is not integral on even inputs, so it violates (G), although it
has property (E) for the odd coset.

The constructive repair retains different predicates.

1. **Selected-branch admissibility:**
   \(H_j(j+\Lambda)\subseteq\mathcal O_K\). This and only this is needed to
   define the piecewise map \(H:\mathcal O_K\to\mathcal O_K\).
2. **Exact integrality on global integers:**
   \(H_j^{-1}(\mathcal O_K)\cap\mathcal O_K=j+\Lambda\). This says that the
   affine extension detects its assigned coset among global integers.
3. **Completion-level inverse integrality at \(v\):**
   \(H_j^{-1}(\mathcal O_{K_v})=j+\Lambda\mathcal O_{K_v}\). This stronger
   predicate is what a backward branch-correctness argument at \(v\) would
   need; it is not the printed definition and is not automatically implied by
   the global predicate.

Exact integrality implies selected-branch admissibility; it is not global
integrality of every branch extension. All later use in this reconstruction
will name the predicate explicitly instead of silently choosing one meaning
of the source word “integral.”

## Exact scalar bridge, with the modulus retained

Specialize to \(K=\mathbb Q\), \(\mathcal O_K=\mathbb Z\), and
\(\Lambda=D\mathbb Z\), but do not assume that a general
\(\mathbb Q\)-linear operator Hydra is scalar. For a scalar branch
\(H_i(n)=a_in+b_i\), selected-branch admissibility is equivalent to the
existence of integers

\[
m_i=Da_i,
\qquad s_i=-Db_i,
\qquad s_i\equiv i m_i\pmod D,
\]

for which

\[
H_i(n)=\frac{m_in-s_i}{D}
\qquad(n\equiv i\pmod D).
\]

Indeed, admissibility gives \(H_i(i),H_i(i+D)\in\mathbb Z\), hence
\(Da_i\in\mathbb Z\) and then \(Db_i\in\mathbb Z\); evaluating at \(i\)
gives the congruence. The converse is immediate. This is an exact two-sided
bridge to the retained-modulus Matthews presentation, not a normalization.

Moreover, the full integrality locus of the branch is

\[
\{n\in\mathbb Z:m_in\equiv s_i\pmod D\}
=i+\frac{D}{\gcd(m_i,D)}\mathbb Z.
\]

Therefore exact integrality holds precisely when
\(\gcd(m_i,D)=1\) for every branch. This is the already audited Matthews
relatively-prime condition. Passing onward to a reduced rcwa coefficient list
uses the separately proved fixed-modulus Matthews–Kohl morphism. No such
scalar rcwa conclusion is available for a genuinely non-scalar
\(\mathbb F\)-linear \(r_j\).

## Descent to nonnegative integers and the missing initial term

Appending zeros to the right of a word does not change its base-\(p\) digit
sum. The finite-word value \(X_{\mathbf j}=H_{\mathbf j}(0)\) descends through
this identification because the source's centered condition
\(c_0=H_0(0)=0\) makes every appended zero act on the terminal zero as
\(H_0(0)=0\).

The multiplier does not descend by the same argument:

\[
M_{\mathbf j\wedge(0)}=M_{\mathbf j}\circ r_0,
\]

which need not equal \(M_{\mathbf j}\). Any notation \(M_H(n)\) must
therefore specify the canonical base-\(p\) word for \(n\), including its exact
length, rather than pretending that \(M_H\) factors through every DigSum
fibre. This missing choice is consequential in Theorem 6.1.

Independently, every function \(f:\mathbb N_0\to K\) satisfying

\[
f(pn+j)=r_j(f(n))+c_j
\tag{R}
\]

is determined by \(a=f(0)\), where

\[
(I-r_0)a=c_0.
\]

Thus properness, meaning that \(I-r_0\) is invertible, gives the unique
initial value \(a=(I-r_0)^{-1}c_0\). For the canonical digits
\(n=\sum_{m=0}^{N-1}d_mp^m\), recursion (R) gives the exact formula

\[
f(n)=P_N(a)+\sum_{m=0}^{N-1}P_m(c_{d_m}),
\qquad
P_m=r_{d_0}\circ\cdots\circ r_{d_{m-1}}.
\tag{F}
\]

The source proof of Lemma 6.1 uses only the sum in (F), although the lemma
assumes properness rather than centeredness. The omitted term \(P_N(a)\)
vanishes identically in the centered proper case, because then \(a=0\). In
the uncentered case it must be retained.

## Correct convergence theorem

Fix a completion \(K_\ell\) at which every branch operator used below is
bounded, and use the induced operator norm. For
\(\mathfrak z=\sum_{m\ge0}d_mp^m\in\mathbb Z_p\), define the truncation

\[
f_N(\mathfrak z)
=P_N(a)+\sum_{m=0}^{N-1}P_m(c_{d_m}).
\]

Let \(q_{j,m}=m^{-1}\#\{0\le k<m:d_k=j\}\), and put
\(\alpha_j=\log\lVert r_j\rVert_\ell\). Submultiplicativity gives

\[
\lVert P_m\rVert_\ell
\le \prod_{j=0}^{p-1}\lVert r_j\rVert_\ell^{m q_{j,m}}.
\]

An exact upper envelope for the exponent is

\[
L^+(\mathfrak z)=
\sum_{\alpha_j<0}\alpha_j\liminf_{m\to\infty}q_{j,m}
+\sum_{\alpha_j>0}\alpha_j\limsup_{m\to\infty}q_{j,m}.
\]

If \(L^+(\mathfrak z)<0\), then some \(\eta<1\) and all sufficiently large
\(m\) satisfy \(\lVert P_m\rVert_\ell\le\eta^m\). Formula (F), the finite
set of translations, and the geometric-series test prove both
\(P_N(a)\to0\) and convergence of the translation series. This proves the
pointwise sufficient condition. The source's displayed density convention is
reversed: it uses a limsup frequency with a negative logarithm and a liminf
frequency with a positive logarithm, which supplies a lower rather than an
upper envelope.

For Haar-almost every \(\mathfrak z\in\mathbb Z_p\), each digit frequency is
\(1/p\). Hence

\[
\prod_{j=0}^{p-1}\lVert r_j\rVert_\ell<1
\]

implies \(L^+(\mathfrak z)<0\), almost-everywhere convergence, and a measurable
limit on its conull convergence domain. It does not define a total function
on the null complement until values there are separately assigned.

If

\[
\rho=\max_j\lVert r_j\rVert_\ell<1,
\]

then \(\lVert P_m\rVert_\ell\le\rho^m\) uniformly. The truncations converge
uniformly on \(\mathbb Z_p\), so the limit is continuous. Wherever the two
limits involved exist, passage through

\[
f_N(p\mathfrak z+j)=r_j(f_{N-1}(\mathfrak z))+c_j
\]

gives the exact digit functional equation.

If \(\ell\) is nonarchimedean and
\(\max_j\lVert r_j\rVert_\ell\le1\), the correct finite-truncation bound is

\[
|f_N(\mathfrak z)|_\ell
\le
\max\left\{|a|_\ell,\max_j|c_j|_\ell\right\}.
\]

The source omits \(|a|_\ell\). This omission is real: over
\(\mathbb Q_2\), take \(r_0=3\), \(c_0=1\). Then
\(a=(1-3)^{-1}=-1/2\), so \(|a|_2=2\) while \(|c_0|_2=1\).

Finally, source equation (6.29) prints equality between the norm of a sum and
the sum of the termwise bounds. Only “at most” follows from the triangle
inequality; in a nonarchimedean completion the sharper bound is the maximum.

## Exact uniqueness boundary

Properness proves uniqueness of (R) on \(\mathbb N_0\). In the uniformly
contractive case, continuity and density of \(\mathbb N_0\) in \(\mathbb Z_p\)
prove uniqueness among continuous extensions. The truncation limit also
defines a canonical extension wherever that specified limit exists.

The functional equations alone do not determine a literal function on all of
\(\mathbb Z_p\). They propagate values only inside tail-equivalence classes of
digit strings. For example, with \(p=2\), \(c_0=c_1=0\), and
\(r_0=r_1=1/2\), choose a non-eventually-periodic digit string. Its
tail-equivalence class is countable and has no shift cycle. Assign one nonzero
seed value there, propagate it by the invertible branch factors, and set the
function to zero off that class. The resulting countably supported Borel
function satisfies the same digit equations but is not the zero function.
Thus the source's unqualified continuation-uniqueness sentence is false as a
statement about literal functions. No uniqueness beyond the truncation-limit
class, the continuous class, or another explicitly imposed regularity class
is admitted.

## Eventually periodic codes

A rational element of \(\mathbb Z_p\) has an eventually periodic base-\(p\)
digit sequence, and conversely. Group the corrected series after the finite
prefix by positions in one repeated word. Each tail is an operator-geometric
series on a finite-dimensional \(\mathbb F\)-cyclic subspace of \(K\). If such
a series converges in \(K_\ell\), then its term tends to zero; on the cyclic
subspace \(I-R\) has zero kernel and is invertible over \(\mathbb F\). Its sum
therefore lies in \(K\). This repairs the source's rational-value remark
without treating an operator as a scalar quotient or calling an
\(\mathbb F\)-linear combination a \(K\)-linear one.

For a purely periodic word \(\mathbf w\), put
\(M=M_{\mathbf w}\), \(X=X_{\mathbf w}\). Repeated concatenation gives

\[
X_{\mathbf w^{\wedge m}}
=\sum_{k=0}^{m-1}M^k(X).
\]

If \(\lVert M\rVert_\ell<1\), the Neumann series proves that \(I-M\) is
invertible and

\[
z_{\mathbf w}=(I-M)^{-1}X
\]

is the unique fixed point of the affine extension \(H_{\mathbf w}\) in
\(K_\ell\). The source's fractions \((1-M^m)/(1-M)\) and \(X/(1-M)\)
must be read as operator compositions, and the printed identity
\(\lVert M^m\rVert=\lVert M\rVert^m\) must be replaced by the sufficient
submultiplicative inequality
\(\lVert M^m\rVert\le\lVert M\rVert^m\).

This is a formal affine-word fixed point. It is an actual \(N\)-step point of
the piecewise Hydra only after the reverse-chronological branch conditions are
proved:

\[
z_{\mathbf w}\in w_N+\Lambda,
\quad
H_{w_N}(z_{\mathbf w})\in w_{N-1}+\Lambda,
\quad\ldots\quad,
H_{w_2}\circ\cdots\circ H_{w_N}(z_{\mathbf w})\in w_1+\Lambda.
\]

No formal fixed point is promoted to a Hydra cycle without these checks.

## Proposition 4.2 is false at its stated generality

Source Proposition 4.2 assumes only a uniform positive separation between
distinct points of a subset \(Y\) of a valued field and concludes that every
orbit is preperiodic or norm-divergent. Its proof uses the stronger assertion
that every bounded subset of \(Y\) is finite.

A nontrivially valued counterexample is \(K=\mathbb Q((t))\) with the
\(t\)-adic absolute value, \(Y=\mathbb Z\subset K\), and \(T(n)=n+1\).
Distinct integers have distance one, so \(Y\) is uniformly discrete. The orbit
of zero is injective and bounded with norm one after its first term; it is
neither preperiodic nor divergent.

The proof becomes valid after replacing uniform discreteness by bounded
finiteness:

\[
\#\{y\in Y:|y|\le R\}<\infty
\quad\text{for every }R>0.
\]

For a number field, \(\mathcal O_K\) is a lattice under the full Minkowski
embedding and is boundedly finite for a norm on that full space. It need not
be discrete under one archimedean embedding: for example
\(\mathbb Z[\sqrt2]\) has nonzero elements arbitrarily close to zero in either
single real embedding. Escape in a full Minkowski norm also does not imply
escape under every individual archimedean absolute value.

## Correspondence Principle: exact admitted boundary

Theorem 6.1 is printed as a theorem but followed by “Proof (Sketch).” Beyond
the empty literal hypothesis class caused by Definitions 5.3–5.4, its sketch
has the following independent defects.

1. The notation \(M_H(n)\) is undefined without a canonical-word and length
   choice; only \(X_H\), not \(M_H\), was proved to descend through DigSum.
   Repeating a canonical word need not repeat an arbitrary representative
   with appended zeros.
2. The length symbol \(\lambda_p(n)\) in
   \(B_p(n)=n/(1-p^{\lambda_p(n)})\) is not defined.
3. The proof of part II invokes a nonexistent hypothesis “(iii).”
4. \(M_q\) appears where the surrounding definitions provide only \(M_H\).
5. Operator quotients and a false norm-power equality are used; the corrected
   Neumann-series formulas above suffice only for the formal affine word.
6. The crucial assertion that a formal word fixed point has the prescribed
   piecewise itinerary is outsourced to an earlier web paper and is not proved
   in the arXiv source. The notions \(v(\Lambda)\) and “correctness” used there
   are not defined in this paper.
7. Global exact integrality as stated on \(\mathcal O_K\) does not by itself
   justify pulling an integral endpoint backward through intermediate points
   that have not first been proved to lie in \(\mathcal O_K\). A
   completion-level inverse-image predicate also does not automatically imply
   global coset membership.
8. From the existential statement that a periodic point has a rational numen
   code, the sketch infers that an irrational code cannot map to a preperiodic
   point. That requires control of every fibre of \(X_H\), especially the zero
   fibre; it does not follow from the stated part I.
9. The all-zero word and the centered fixed point \(0\) are outside condition
   (i) and the displayed \(B_p(n)\), which both begin at \(n\ge1\).
10. Part II depends on the false general Proposition 4.2. Even its repaired
    Minkowski form would establish escape in a full lattice norm, not
    divergence for every individual archimedean absolute value.
11. The conclusion calls \(X_H(\mathfrak z)\), a point, a “divergent
    trajectory.” The typed conclusion would concern its forward orbit.

Accordingly, the two Correspondence-Principle conclusions are recorded as
source claims with unresolved proof obligations, not as admitted theorems. The
bounded repeated-word fixed-point result above is retained. No assertion is
made that every periodic point is exactly the image of the stated rational
code domain, that an irrational code with integral value has a divergent
orbit, or that the zero fibre has the needed rationality property.

The IFS assertion in source Remark 6.7 is also withheld. Its use of a zero
digit as an identity branch versus as the first IFS map changes whether
eventually-zero strings descend and what boundary points are represented; a
typed domain, a specified continuation, contractivity and affine/invertibility
hypotheses, and an exact surjectivity proof are required before admission.
Coding overlap also prevents the stated omission claim from following merely
from an eventually-\(f_1\) address.

## The v3 Fourier repair remains incomplete

The v3 source changes Proposition 7.6, and printed pages 27–29 were therefore
checked even though the Fourier programme is not otherwise admitted in this
foundational pass. Two corrected displayed arguments in v3 do not close the
proposition.

Let \(L=K_\ell\) lie over \(\mathbb Q_q\), and let the paper's additive
character be

\[
\psi_L(x)=\exp\!\left(2\pi i
\{\operatorname{Tr}_{L/\mathbb Q_q}(x)\}_q\right).
\]

The standard \(q\)-adic character has conductor \(\mathbb Z_q\). Therefore
the annihilator of \(\mathcal O_L\) under the trace pairing is, by definition,

\[
\mathfrak D_{L/\mathbb Q_q}^{-1}
=\{t\in L:\operatorname{Tr}_{L/\mathbb Q_q}(t\mathcal O_L)
\subseteq\mathbb Z_q\},
\]

the inverse different. Hence the dual is

\[
\widehat{\mathcal O_L}\simeq
L/\mathfrak D_{L/\mathbb Q_q}^{-1},
\]

not generally \(L/\mathcal O_L\). The two agree only under the corresponding
conductor/trivial-different normalization. The finite Fourier formula for a
ball \(\mathfrak w+\pi_\ell^n\mathcal O_L\) must consequently sum over

\[
\pi_\ell^{-n}\mathfrak D^{-1}/\mathfrak D^{-1}
\]

with normalization \(q^{-nf}\), where
\(f=[L:\mathbb Q_q]/e_{K,\ell}\). This follows directly from character
orthogonality and does not depend on an uncorrected radius presentation of
the quotient representatives.

There is a second, independent operator defect. For a general bounded
\(\mathbb Q_q\)-linear extension of \(r_j\), trace duality gives a unique
adjoint \(r_j^\dagger\) satisfying

\[
\operatorname{Tr}(t\,r_j(x))
=\operatorname{Tr}(r_j^\dagger(t)\,x).
\]

Thus a Fourier recursion uses
\(\widehat\mu(r_j^\dagger t)\), not
\(\widehat\mu(r_j(t))\), unless self-adjointness has separately been proved.
In the basis \((1,\sqrt2)\) of \(\mathbb Q(\sqrt2)\), the invertible map with
matrix
\(\begin{psmallmatrix}1&1\\0&1\end{psmallmatrix}\) has trace-pairing adjoint
\(\begin{psmallmatrix}1&0\\1/2&1\end{psmallmatrix}\), so the two are not
formally interchangeable.

Further printed defects remain. Proposition 7.5 multiplies values in a mere
abelian group, shadows one summation variable, and leaves another unbound.
\(B_{H,\ell}\) is undefined when all translations vanish and may be negative
where the invoked proposition requires a nonnegative integer. The proof
compares a real norm with a field element, reverses the sign on the
uniformizer norm, and replaces division by \(\pi_\ell^B\) with division by the
real number \(q^{B/e}\). Moreover, a characteristic function of a general
\(L\)-valued variable is naturally defined on \(L\); treating it as a
function on a quotient dual requires an integral-support statement that the
paper has not supplied at Definition 7.3.

Proposition 7.6 is therefore registered as requiring correction. The inverse
different, dual-adjoint operator, support, and scaling questions remain a
separate proof obligation; no Fourier inversion consequence is used below.

## Propagation and open obligations

The following consequences must travel together in every downstream artifact:

- the repaired selected-branch, global exact-integrality, and completion-level
  inverse-integrality predicates;
- the retained-modulus scalar Matthews morphism and its non-scalar exception;
- the exact finite word order and affine formulas;
- the non-descent of \(M_H\) without a canonical-word choice;
- the initial-value term for uncentered proper systems;
- the corrected upper-Lyapunov sign convention;
- the exact uniqueness class;
- the formal-word-versus-actual-itinerary boundary;
- the boundedly-finite replacement for Proposition 4.2;
- the conditional, unresolved status of both Correspondence-Principle parts;
  and
- the inverse-different and dual-adjoint corrections before any Fourier use.

Formal certification remains open for the finite affine-word identities,
scalar admissibility/exact-integrality bridge, corrected truncation formula,
Lyapunov estimate, repeated-word Neumann fixed point, and explicit
branch-correctness predicates. The full Correspondence Principle cannot be
closed until its fibre, local-to-global integrality, and divergence arguments
are supplied or its statement is weakened to exactly what those arguments
prove. Proposition 7.6 requires its own corrected local Fourier statement and
proof before use.
