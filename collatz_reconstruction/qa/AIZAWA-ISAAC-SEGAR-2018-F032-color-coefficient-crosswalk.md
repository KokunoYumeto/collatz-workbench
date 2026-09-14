# Aizawa--Isaac--Segar 2018/2019: source audit and Collatz boundary

## Identity and manifestations

- Authors: N. Aizawa, P. S. Isaac, J. Segar.
- Title: *Z2 x Z2 generalizations of N=1 superconformal Galilei algebras and
  their representations*.
- arXiv: `1808.09112v1`, submitted 2018-08-28; the official record has one
  version.
- Journal: *Journal of Mathematical Physics* 60 (2019), 023507.
- DOI: `10.1063/1.5054699`.
- Official e-print archive: 14,499 bytes, SHA-256
  `d5361e762a6f8f0983aabe62fa9256c9a9adf0531dc3cefccd2f187324dd76b0`.
- Extracted single source file `Z2-N1-ellv5.tex`: 48,693 bytes, SHA-256
  `168e9e0b3c524c0813c795b357c87fbacabf9d4d013f430330b63fc4a46562ab`.

The frozen index has no exact author, title, or arXiv-ID record.  Bounded
filename checks in the authorized paper, LaTeX, Obsidian, and Downloads roots
also missed.  The source was acquired from the official arXiv e-print endpoint
and placed on the topical shelf without changing the frozen ledgers.

## Content read

The complete substantive source was read at TeX-line level:

- abstract and introduction, lines 106--193;
- color-superalgebra definition and enveloping-algebra bracket, lines 203--251;
- the N=1 superconformal Galilei algebra and central extension, lines 256--296;
- both color-superalgebra constructions and complete relation tables, lines
  308--501;
- triangular decomposition, adjoint, and superadjoint operations, lines
  505--653;
- boson--fermion and color-supergroup vector-field representations, lines
  665--984;
- conclusions and explicit future-work boundary, lines 995--1024.

## Exact source results used

For `V=Z2 x Z2`, the source defines the dot-product bicharacter and the color
bracket in an enveloping algebra.  It starts from the N=1 superconformal
Galilei algebra, adjoins the quadratic composites

`P_nm={P_n,P_m}`, `Lambda_nm={P_n,X_m}`, and `X_nm=[X_n,X_m]`,

and assigns the four degrees exactly as follows:

- `00`: `H,D,K,P_nm,X_nm`;
- `01`: `P_n`;
- `10`: `Q,S,Lambda_nm`;
- `11`: `X_n`.

The displayed relation tables close in those degrees.  The source separately
treats the centrally extended algebra, gives a triangular vector-space
decomposition, defines adjoint and superadjoint operations, constructs a
boson--fermion realization, and writes a color-Grassmann vector-field
realization.

## Exact Collatz crosswalk

The paper supports the definition of a `V`-graded color superalgebra and its
specific enveloping-algebra construction.  Since `Delta={00,11}` is totally
isotropic for the paper's bilinear form, its general definitions imply the
elementary restricted-commutator lemma recorded in
`intake/chatnotes/ZN-SYMMETRIES-DIRECT-LOCATOR-AUDIT-02.md`.

The paper contains no Collatz map, parity map, affine branch family, iteration
word, weighted path, transfer operator, or action on arithmetic states.  It
does not supply a morphism from the Chatnotes coefficient labels or function
algebra to either color superalgebra.  Its closure theorem cannot be
transferred merely by reusing the same four degree names.

## Independently proved defects and repairs in the local bridge

1. The raw `e_v` multiplication belongs to `Map(V,C)` or to the Fourier
   idempotent basis of `C[V]`, not to the group-element basis.
2. The natural group basis is `V`-graded; the nonzero primitive idempotents
   cannot be homogeneous in their own nonzero labels.
3. Diagonal projection retains two labelled branches and requires the
   state-dependent parity evaluator to produce the scalar Collatz map.
4. Coordinate swap fixes the diagonal pointwise; the later exchange of its two
   basis vectors is a different, independently chosen involution.
5. The standard `O(2)` matrix relations are valid after choosing `J`, but the
   paper does not make that choice intrinsic to Collatz.
6. The raw passage supplies neither a homomorphism nor a commutative diagram
   relating the quotient map from `Spin(4) x SU(2)` to the coefficient map
   `partial : F2^2 -> F2`; shared order-two data do not define that comparison.

The deterministic coefficient certificate additionally verifies all sixteen
products in each of the function, group-element, and Fourier-idempotent bases,
all four inverse Fourier basis identities, the exact diagonal projector,
8,004 bounded integrality instances, 2,001 state-dependent parity evaluations,
and the displayed involution matrices.  These finite checks accompany the
general proofs in the TeX reconstruction; they do not replace the cited
paper's Jacobi calculation or construct a Collatz color action.

## Nonclaims

- No color-superalgebra action on Collatz states, paths, or observables has
  been constructed.
- No bracket, representation, or enveloping-algebra morphism from Collatz data
  to the paper's algebras has been given.
- No intrinsic `O(2)` action, anomaly, determinant obstruction, or spin-SU(2)
  structure for Collatz follows.
- The source does not address, imply, or reformulate the Collatz conjecture.
