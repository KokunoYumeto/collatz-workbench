# Weighted Odd-Step Paths, Survivor Coding, Arithmetic Groupoids, and Toric Period Morphisms for the Collatz Map

This directory is an independent, Overleaf-compatible LaTeX project for the
separately authored Collatz research companion. It does not import the
critical/expository reader, private notes, local books, scans, or machine
paths. The intellectual provenance of the programme is stated in the paper;
all admitted mathematics is rederived there.

The first section develops the weighted path and finite-residue theorem
package together with the Gaussian signed-valuation morphism for Collatz
prefix angles.  It proves the unweighted non-torsion theorem, the exact
exceptional two-letter lattice, and a coefficient-unbounded 795-column
relation-lattice theorem; the all-length classification is stated separately
as a conjecture.  The second section constructs the exact odd two-adic survivor coding, locates
the positive-integer itineraries, computes the full-label-shift pressure, and
crosswalks it to the fixed-base periodic definition of Gurevich pressure. It
also proves the exact bidegree fibres and the object-idempotent and
formal-scheme obstructions that delimit the tested tropical and prismatic
interfaces. The third section constructs the discrete arithmetic orbit
groupoid and its cocycles, the `3`-adic germ groupoid and faithful arithmetic
functor, the exact torus-coordinate isomorphism, Kummer `1`-motive squares,
the Cayley isomorphism of pairs, and the multiplication-induced Nori edge.
The fourth section identifies positive exponent packets with pointed parity
words, proves the exact comparison of the odd-return, shortened, and full
clocks, constructs the cyclic packet groupoid and residue recursion, and
retains the common word under a synchronized Chinese-remainder isomorphism.
It also gives complete exact packet calculations through odd-return period
sixteen.  The fifth section derives the two-state rational offset family,
proves the coefficientwise inverse of its dyadic dilation map, determines the
exact Taylor domains, and constructs a meromorphic continuation whose finite
dyadic poles, orders, and leading coefficients are all explicit.
Public authors are cited only for their own definitions and theorems; the
Collatz-specific deductions are proved inside this companion.

## Build

Upload the files listed in `MANIFEST.json` as one project or build locally
from this directory.  The local `tmp/` tree, when present, contains only QA
scratch and is deliberately outside the portable source inventory.

```text
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The single root is `main.tex`; all TeX inputs are relative to this directory.

## Reproducible checks

Python 3.10 or newer is required for the certificate and verifier.  On a
POSIX system use `python3`; on Windows use `py -3` (or an equivalent Python
3.10+ launcher):

```text
python3 certificates/finite_actions_checks.py
python3 certificates/arctangent_relation_lattice_checks.py
python3 certificates/groupoid_motivic_interface_checks.py
python3 certificates/affine_packet_residue_checks.py
python3 certificates/affine_crt_synchronization_checks.py
python3 certificates/affine_packet_series_checks.py
python3 certificates/affine_signed_necklace_checks.py
python3 validate_package.py
```

```text
py -3 certificates/finite_actions_checks.py
py -3 certificates/arctangent_relation_lattice_checks.py
py -3 certificates/groupoid_motivic_interface_checks.py
py -3 certificates/affine_packet_residue_checks.py
py -3 certificates/affine_crt_synchronization_checks.py
py -3 certificates/affine_packet_series_checks.py
py -3 certificates/affine_signed_necklace_checks.py
py -3 validate_package.py
```

The first certificate recomputes bounded instances of the exact block, cocycle,
source-fibre, predecessor, finite-semigroup, reduction, typed-action,
prefix-refinement, exceptional-preimage, failed-update, and pressure formulas.
The pressure checks include fixed-base periodic partitions on finite alphabet
truncations.  The second certificate proves the complete integer relation
lattice for all 795 angles indexed by $1\leq k\leq15$ and
$k\leq A\leq60$, using exact Gaussian products, cubic-character rows, rank,
and an integral saturation lift.  It certifies no angle outside that grid.
The third certificate checks bounded exact instances of representative
independence, groupoid multiplication, path embedding, the arithmetic-to-germ
functor, `3`-adic branch inverses, torus characters, `1`-motive squares,
character multiplication, Cayley inversion, and the explicit failed
`ell^2(O)` isometry. None of the certificates replaces the infinite
topological, analytic, or categorical proofs, proves the all-length
Collatz--Machin rigidity conjecture, or proves the Collatz conjecture.
The fourth certificate checks the packet--parity map, three exact clocks,
cyclic transport, finite-state residue recursion, the 99-class period-eight
table, and two independent exact packet scans.  The fifth checks the complete
joint residue table at $(m,A)=(10,16)$, both Chinese-remainder inverses, all
synchronized transitions, primitive/imprimitive strata, and both marginals.
The sixth checks the affine recurrences, the repaired periodic-tail algebra,
the exact formal dilation coefficients, explicit divergence witnesses, and
the rational constants used in the normal-convergence bound.  Its finite
checks accompany, rather than replace, the general analytic proofs.
The seventh checks the exact fixed-content primitive-word and necklace
counts, the packet--binary cyclic bijection, the denominator sign split,
the point/orbit distinction, and the coprime specialization.  Its bounded
enumeration accompanies the all-parameter proof in the fourth section.
`validate_package.py` checks the manifest,
source closure,
forbidden private paths, bibliography/label closure, the certificate, and a
deterministic two-build source-to-PDF match for the declared output.

## Status

This is a working research edition. Its successful build and package checks
establish the integrity of this theorem package, not completion of the wider
Collatz corpus project.
