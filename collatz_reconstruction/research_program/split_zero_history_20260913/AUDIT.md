# Split Zero history and finite Collatz reconstruction audit

Date: 2026-09-13. Scope: source proof inspection, exact finite deductions, and
the standalone arithmetic certificate `check_history.py`. No Lean was run.
No source in the Split Zero programme was edited.

## Primary definitions and reconstruction statements actually inspected

1. `C:/Users/LOCAL_USER/Documents/Papors/Chatnotes/split_zero_projective_monads_surcomplex/split_zero_projective_monads_surcomplex.tex`, lines 254–356 and 583–685: the actual definitions and proofs for `G(R)=R disjoint union {tau}`, supported zero `e=0_R`, pair normal form `(p,chi)`, universal ring reflection, Boolean character, and product masks. In particular `chi(e)=chi(r)=1` for every supported scalar `r`. This character detects absence versus support; it does not distinguish arithmetic zero from a nonzero amplitude or compute parity. Masks satisfy `epsilon_A+epsilon_B=epsilon_(A union B)` and `epsilon_A epsilon_B=epsilon_(A intersection B)`.
2. `C:/Users/LOCAL_USER/Documents/Papors/Chatnotes/globalization nte/2/split_zero_secondary_note.tex`, lines 458–762: complete extraction, reconstruction, and equivalence proofs for support diagrams. Fibres are `M_l={x:ex=l}`, their zero is `l`, and transition maps are `x -> x+l'`. Reconstruction requires the modules and transition maps as well as the join-semilattice; it is not inversion of an already collapsed amplitude.
3. `C:/Users/LOCAL_USER/Documents/Papors/Chatnotes/Globalization idempotent Collatz'/support_idempotent_homogenization_note.tex`, full source read, especially lines 189–307 (translation obstruction and its support-homogeneous repair), 308–379 (branch matrices and finite digit formula), 381–444 (convergence hypotheses), and 446–540 (specialization compatibility). The source uses `R=Z[1/2][q]`, vectors `(x,h)`, and matrices `M0=[[1/2,e],[tau,1]]`, `M1=[[q/2,1/2],[tau,1]]`. Its digit F-series composes matrices in the opposite order from a forward time orbit; the derived forward formula below fixes the order explicitly.
4. `C:/Users/LOCAL_USER/Documents/math/output/split_zero_rh_tandem_2026-09-12/tex/historical_hurwitz_jets.tex`, lines 23–301, all definitions and proofs H1–H13 read. H1 uses the original compact probability input on `[0,L]`, original displacement `t`, and `|t|L<1`. H2 proves `b_n(rho) != 0` for every `n>=1` at any actual nontrivial zero. H4 requires a simple zero for a scalar branch. H10–H13, lines 231–301, remove simplicity by retaining the full monic cluster polynomial and all multiplicities. They prove equivalence of its `t`-jet through order `N` and moments through order `N`; no RH hypothesis is used.
5. `C:/Users/LOCAL_USER/Documents/math/output/split_zero_rh_tandem_2026-09-12/sources/Split_Support_Quotient_Propagation_2026-09-11/RESEARCH_NOTE.md`, lines 217–288 and 968–998 directly inspected: the reflected module is a filtered colimit; `ker(N_k -> Lin(N)) = union_(k'>=k) ker rho_(k,k')`. Lines 248–250 explicitly deny reconstruction from a label beside an already-reflected amplitude. The supported cohomology retains fibre zeros, while the quotient still kills boundary amplitudes. The actual ladder `G(R/(g s^(m+1))) -> G(R/(g s^m))` maps the nonzero origin class `[g s^m]` to supported zero, while `tau` maps only to `tau`.
6. `C:/Users/LOCAL_USER/Documents/math/output/split_zero_rh_tandem_2026-09-12/tex/tau_chain.tex`, full section read, especially lines 75–87 and 581–603: actual source corrections keep the representative and `K_R` alongside fixed quotient and finite-jet data; supported boundaries become their original labelled zero. They are not recovered from that zero alone.

An independent source-reading subagent additionally inspected current
`tex/support_diagrams.tex` lines 125–200, the quotient-propagation note's finite
spectral-jet statement at lines 676–710, and the original
`split_support_geometry_arithmetic_curve_v11.tex` lines 1356–1454. These give,
respectively, retained comparison kernels, finite jet kernels with no
infinite-jet assertion, and recovery of an encoded finite support state by all
threshold characters. No theorem reversing an arbitrary spectral sequence was
found in these selected sources. Spectral jets and spectral sequences must not
be identified.

## Derived finite forward-word result

For a chronological binary word `w=(d_0,...,d_(N-1))`, put
`s_j=sum_(i<j)d_i`, `m=sum_j d_j`. With `T_d(x)=(q^d x+d)/2`, direct
composition gives

```
T_(d_(N-1)) ... T_(d_0)(x) = (q^m x + P_w(q))/2^N,
P_w(q) = sum_j d_j 2^j q^(m-1-s_j).
```

The successive nonzero coefficients of `P_w`, read in descending degree, are
exactly `2^(j_0),...,2^(j_(m-1))`. Therefore `(N,P_w)` reconstructs every bit,
including final zero bits. An integer `n` realizes this parity prefix exactly
when `3^m n+P_w(3)=0 mod 2^N`; this is a unique residue class because `3^m` is
odd. The proof is inductive division by two: the first congruence forces the
first parity, and division leaves the suffix congruence. This gives the
all-length proof; the script exhausts finite lengths through 10.

The spectrum of the full triangular word matrix only records
`{q^m/2^N,1}`. For example chronological words `01` and `10` have that same
spectrum but translations `1/2` and `1/4`. Booleanizing either original branch
matrix also gives the same matrix because both `e` and `1/2` are supported.
Thus these reduced data lose order. For the source's opposite-order F-series,
`X_17(q)=1/2+q/32` and `X_28(q)=1/8+q/16+q^2/32` are distinct but both
specialize to `19/32` at `q=3`; their difference is `(q-3)(q+4)/32`.

## Finite spectral application: proof audit

Assume integers `m>=1`, `A>=m` and the complete, known set `W` of positive
exponent words of length `m` and sum `A`. Its size is
`K=binomial(A-1,m-1)`. If `a_j` are chronological exponents, the odd-iterate
formula is `2^A x_m=3^m x_0+B_w`, where
`B_w=sum_(j=0)^(m-1) 3^(m-1-j) 2^(a_0+...+a_(j-1))`.

The unique odd residue `r(w)` in `[1,2^(A+1))` satisfying
`3^m r+B_w=2^A mod 2^(A+1)` realizes the specified *exact* exponent word.
Successive divisibility first forces each required division; the next
positive exponent forces the preceding quotient odd, and the displayed
final congruence forces the last quotient odd. Distinct words therefore have
distinct residues, by uniqueness of the exact valuation itinerary.

For nonnegative known-node weights `lambda_w` summing to one, take
`mu=sum_w lambda_w delta_(r(w))`, with `L=max_w r(w)`. H10–H13 show that the
full local monic zero-cluster `t`-jet through order `K-1` at any actual
nontrivial zeta zero determines `m_0,...,m_(K-1)`. All multiplicities and the
original displacement coordinate are required. Define

```
ell_w(y)=product_(v!=w) (y-r(v))/(r(w)-r(v)).
lambda_w = integral ell_w(y) dmu(y)
         = sum_j [y^j]ell_w(y) m_j.
```

This is exact finite reconstruction. For any known arithmetic predicate on
`W`, summing its Lagrange polynomials gives its probability mass. In
particular `D=2^A-3^m` is nonzero and `D divides B_w` detects an integer fixed
point of that word. Such a fixed point is positive precisely when `D>0`;
divisibility alone includes negative integer cycles when `D<0`.

For `(m,A)=(2,4)`, ordered words `(1,3),(2,2),(3,1)` have `B=5,7,11`, nodes
`19,1,29`, and `D=7`. Only the middle word qualifies. Its mass is exactly
`(m_2-48 m_1+551)/504`, by the polynomial `(y-19)(y-29)/504`.

For `K>=2`, order `K-2` cannot determine all weights, even among strictly
positive probabilities. Put
`v_i=1/product_(j!=i)(r_i-r_j)`; then
`sum_i v_i r_i^n=0` for `0<=n<=K-2` and equals one for `n=K-1`.
Small positive and negative perturbations of uniform weights in this
direction give different probabilities with identical lower moments, hence
identical lower cluster jets by H10–H13. This sharpness statement is for all
weights. A particular predicate can require fewer jets if its interpolant
has lower degree. A singleton predicate has degree exactly `K-1`.

The analytic family encodes the chosen finite arithmetic measure. The
argument does not produce that measure or its spectral jet without input,
impose an asymptotic drift inequality, or prove Collatz convergence.

## Certificate scope and result

`check_history.py` uses only the Python standard library and exact integer /
`fractions.Fraction` arithmetic. It independently composes polynomial affine
maps, reconstructs words, scans all parity residues through length 10, and
checks several integer lifts. It verifies the exact specialization and
same-spectrum collisions. For every `1<=m<=A<=9`, it checks exact odd-return
residues, interpolation identities at every node, recovery under uniform and
nonuniform positive weights, arithmetic-predicate mass, and the explicit
Vandermonde ambiguity with strictly positive perturbations. It also checks
actual integer returns for qualifying divisibility cases, including the sign.

The script emits JSON on stdout; it does not evaluate zeta numerically or
claim to computationally certify H1–H13. Those are covered by the source proof
review above. Finite enumeration supplements the general proofs and does not
replace them.

Run result on 2026-09-13: `python -B check_history.py` exited zero in about
5.3 seconds and emitted `status: pass`. It checked 2,047 forward words and
residue classes with 6,141 integer lifts; 45 odd-return packets containing
511 words; 90 probability reconstructions; and 28 strictly positive
lower-jet ambiguity pairs. The largest packet had 70 nodes. The exact
`(m,A)=(2,4)` nodes and mass polynomial passed.

## Independent review of the completed note

The newly written `note.tex` was read end to end on 2026-09-13, at SHA256
`D855CFC1B2D51C398ED8EF3681F04D8B5DC947BE77225AE43F1F5A012BF124A7`.
No mathematical error was found. The review checked the following actual
proofs and definitions, not only theorem statements:

- The chronological affine induction, coefficient inverse, empty/all-zero
  case, parity-congruence induction, and reversal map to the source's
  opposite-order F-series.
- The distinction between external `tau`, supported `e`, the Boolean
  character, and the separately supplied parity idempotent in `R^N`.
  The explicit specialization collision and the triangular-matrix spectral
  loss have the stated coefficients and order.
- The exact odd-return cylinder, including the terminal oddness condition
  modulo `2^(A+1)`, pairwise distinct residue coordinates, and the rotation
  identity that propagates integrality of `B_w/D`. The positivity condition
  `D>0` is kept where positive periodic candidates are counted.
- The joint holomorphicity bounds and contour construction, the full
  multiplicity-preserving monic cluster, both triangular inverse equations,
  and the converse equality of jets from equality of moments. These agree
  with the directly inspected H1–H13 source proofs.
- The Lagrange inverse on known distinct nodes, strictly positive
  Vandermonde perturbations proving the all-weight lower bound, arithmetic
  predicate interpolation without independence assumptions, and all numbers
  and simple-zero signs in the `(m,A)=(2,4)` example.
- The pushforward fibre/kernel calculation and the enlarged `(S,lambda)`
  input: retained zero-weight labels are additional data, not information
  secretly recovered from the measure's spectral family.

No edit was made to `note.tex` during this review. The Reddit draft was not
yet present at this review point; any subsequent public-text review is
recorded separately below.

## Review of the new public spectral/parity wording

The spectral/parity section of `reddit_after.md` was reviewed at SHA256
`B348C2F31C560CD1618A1C12AC0664294A975BA094A542C5A7E4A9E51158B8AE`.
Its formulas, order conventions, exact residue encoding, full-cluster
inverse, arithmetic-predicate recovery, and numerical example agree with
the note and certificate. The review did not cover the separate packet-sum
or Tao paragraphs.

One edge-case omission was reported to the root agent: the sentence about
two distinct strictly positive probabilities witnessing sharpness needs
the condition `K>=2`. If `m=1` or `A=m`, the packet has `K=1` and only one
probability vector. The note's theorem already handles that case correctly.
No other mathematical error was found in the reviewed public addition.
