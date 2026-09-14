# Affine-packet general-theorem audit

Date: 2026-09-04. Scope: independent audit of the general mathematical
statements in `chapters/04_affine_packets_parity_necklaces_and_residue_automata.tex`
and inspection of its portable arithmetic certificate. This report records
proof-ready repairs; it does not apply them to the manuscript or certificate.

## Exact audited identities

Paths below are relative to `collatz_reconstruction` unless absolute.

- `research_companion/chapters/04_affine_packets_parity_necklaces_and_residue_automata.tex`:
  SHA-256 `b1f0483c8878c169d9bd08c23ea3078b55040b5219a734be51b61c4c6c8628d4`.
- `research_companion/certificates/affine_packet_residue_checks.py`:
  SHA-256 `6757f38673dbeb69d76a85f6e5f8fd53b32e0dd9d2a53dd16b969832b8a4879e`.
- `external_literature/dependency_gate_2026-08-25/lagarias_1990_impan.pdf`:
  SHA-256 `7dc39db8d59c141b19eebfbd76e48c4e7d3906f97d0c7187739d2a7561399005`.

The hashes above were computed directly from the audited files. The wrapper
`certificates/affine_packet_source_and_cycle_checks.py` was read completely
for its exact source locators and its binding of the portable certificate.
It pins the latter at 17,744 bytes and the SHA-256 above, so changing that
certificate subsequently requires propagation of its wrapper identity.

## Instructions and literature route

The project directives, Documents ancestor instructions, canonical index
contract, recovery entrypoint, and topic-route schema were read. The index
was used for routing, not as mathematical evidence; it was not rebuilt.
The root agent retained responsibility for raw Chatnotes provenance and
project-state propagation.

Queries executed through the canonical `scripts/query_corpus.py`, both
research-literature and local-unpublished layers, limit four per layer:

1. `Lagarias rational cycles`.
2. `Collatz affine`.

The relevant published indexed unit is
`PUBUNIT-68BAB8443C053C8266594E1B`, Laarhoven--de Weger,
*The Collatz conjecture and De Bruijn graphs*. Its source was read at
`C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/latex/1209.3495v1/main.tex`:
the opening definition and section description, source lines 45--60, and
the necklace/Lyndon-word and rational-cycle discussion, approximately
lines 302--321. Its section structure was inspected. The source explicitly
uses the shortened odd branch `(3n+1)/2`.

Lagarias's PDF is scanned; native text extraction from the first five
physical pages produced no substantive text. Physical PDF page 3, containing
printed pages 36--37, was rendered in memory and visually read. Section 2,
Theorem 2.1, formula (2.1), and the proof specify the odd-denominator rational
domain, shortened branches `U_0(x)=x/2`, `U_1(x)=(3x+1)/2`, and the rational
point with the prescribed periodic parity word. Those are the source facts
used below. The entire Lagarias paper was not read in this bounded audit.

The local query also routed, but did not content-read, these possible
provenance witnesses, which were communicated to the root agent:

- `PUBUNIT-438CC647B15CADA2BEB230B6`,
  `C:/Users/LOCAL_USER/Documents/Papors/Chatnotes/automata/packetz/collatz_packet_note.tex`.
- `PUBUNIT-004F3DB5D12B4A71C77EDE18`,
  `C:/Users/LOCAL_USER/Documents/Papors/Chatnotes/automata/v4/collatz_dyadic_dilation_note.tex`.

These local hits are not evidence for a theorem or attribution in this report.

## Overall finding

The general results survive with explicit domain and convention repairs.
No counterexample to the packet--parity bijection, cyclic groupoid
isomorphism, cyclic transport identity, typed cycle criterion, minimum strip,
or residue generating-series theorem was found at their intended domains.
Several displayed statements or proofs are presently incomplete at boundary
cases or leave their clocks and arrows insufficiently typed.

## 1. Packet domain and empty-tail repair

Chapter lines 32--44 define positive packets without explicitly saying
`m >= 1`. At `m=A=0`, the subsequent assertion `2^A != 3^m` is false.
Actual periodic packets must have `m >= 1` and `A >= m`.

The decompositions at lines 154--159 use `C(p')` for
`p'=(a_2,...,a_m)`. At `m=1` this is the empty packet, whose numerator has
not been defined. Define `C(empty)=0` and `A(empty)=0` as auxiliary
conventions only; do not attach a rational point `x_empty`, whose prospective
denominator is zero. Then for `p=(a)` the two decompositions read

    C(p) = 1 + 2^a C(empty) = 1,
    C(sigma p) = 3 C(empty) + 2^0 = 1.

The cyclic identity becomes `3+(2^a-3)=2^a`, including `a=1`.
All claims of oddness and nonzero denominator refer to nonempty packets.

## 2. Correct the parity-numerator product

At chapter line 59 the source contains `v_j,2^j`, a literal comma, rather
than the intended product. Replace it with `v_j\,2^j`:

    N(v) = sum_(j=0)^(A-1) v_j 2^j 3^(v_(j+1)+...+v_(A-1)).

This is the product used by the portable certificate and by Lagarias,
Theorem 2.1, printed page 36. The proof of `N(E(p))=C(p)` then substitutes
the one-positions `S_0,...,S_(m-1)` exactly as written.

## 3. Type the rational domain and the three clocks

The word called "ordinary" at lines 51 and 433--434 belongs to the
shortened map, not the full map whose odd branch is `3x+1`. Define

    Z_(2) = {u/v in Q : v is odd},
    T(x) = (3x+1)/2 for odd x, and x/2 for even x,
    C_full(x) = 3x+1 for odd x, and x/2 for even x.

Both maps have domain and codomain `Z_(2)`; parity is the parity of an
odd-denominator numerator. The chapter's `U_2` is its odd subset.
The accelerated map `Phi` is a partial map on `U_2`, excluding `-1/3`.
The reported 155,047 certificate steps are shortened-map steps.

For `x_i=x_(sigma^i p)` and indices modulo `m`, the cyclic affine identity
gives `3x_i+1=2^(a_(i+1)) x_(i+1)`. Since `x_(i+1)` is odd,

    T^r(x_i) = 2^(a_(i+1)-r) x_(i+1),
        1 <= r <= a_(i+1),
    C_full^r(x_i) = 2^(a_(i+1)-r+1) x_(i+1),
        1 <= r <= a_(i+1)+1.

These formulas identify every intervening value: all before the terminal
one are even. Concatenation proves the exact clocks

    T^(S_j)(x_p) = x_(sigma^j p),
    C_full^(S_j+j)(x_p) = x_(sigma^j p).

A complete packet therefore has `m` odd returns, `A` shortened steps,
and `A+m` full steps. The parity word `E(p)` has length `A` because it
uses the shortened clock. For example, `p=(2)` gives `x_p=1`, one odd
return, two shortened steps, and three full steps.

The partial-map exception causes no failure for packet periodic points:
`3x_p+1=2^(a_1) C(sigma p)/D` is nonzero. Hence none of their cyclic
rotates equals the excluded value `-1/3`.

## 4. Complete both directions of divisibility transport

At chapter lines 192--194, oddness of `D` gives invertibility of 2, but
does not by itself justify the converse divisibility implication. Record

    gcd(D_(m,A),6) = 1.

Indeed, `D=2^A-3^m` is odd and `D mod 3 = 2^A mod 3` is nonzero.
The identity

    3C(p)+D = 2^(a_1) C(sigma p)

then proves both directions explicitly. If `D | C(p)`, invert 2 modulo
`D` to obtain `D | C(sigma p)`. If `D | C(sigma p)`, obtain `D | 3C(p)`
and invert 3 modulo `D`. Negative `D` presents no issue: divisibility
uses the same principal ideal as `|D|`.

## 5. Exact cyclic groupoids, inverses, and stabilizers

The intended theorem is correct. Specify that the packet action is by
`Z/mZ`, the binary rotation action is by `Z/AZ`, and the target is the
full subgroupoid on binary words beginning in one. An arrow from `v` is
`(v,t)` with `v_t=1`. Distinct rotation residues remain distinct arrows
even when they have the same target.

For `p`, its one-positions are exactly

    0=S_0 < S_1 < ... < S_(m-1) < A.

Thus `j -> S_j` is a bijection on each source fibre. The inverse arrow
map finds the unique `j` such that `t=S_j`. The object inverse reads
the positive cyclic gaps between consecutive ones, including the final
gap to the boundary at `A`.

Composition is preserved because

    S_j(p) + S_k(sigma^j p) = S_(j+k mod m)(p) mod A.

The identity arrow `j=0` maps to the identity `t=0`. For `j>0`,

    S_(m-j)(sigma^j p) = A-S_j(p),

which proves preservation of inverse arrows. For `j=0`, both inverses
are again the identity. This supplies all functor and inverse-functor
identities, not just the object-rotation equation.

For exact stabilizers, let `p=u^r`, where `u` is primitive of length `d`,
and set `B=A(u)`. Then `m=rd`, `A=rB`, and

    Stab(p) = {kd mod m : 0 <= k < r},
    Stab(E(p)) = {kB mod A : 0 <= k < r}.

The functor sends `kd` to `kB`. To prove that the second set contains
all stabilizers, a stabilizing binary rotation must start at a one,
hence equal some `S_j`. The object identity and injectivity of `E`
give `sigma^j p=p`, so `j` is a multiple of `d`. Packet repetition
then gives `S_(kd)=kB`. Therefore the least binary period is exactly
`B`, the stabilizers have the same order `r`, and primitivity is
equivalent in the two coordinate systems. Passing to isomorphism
classes gives the stated necklace bijection.

## 6. Typed cycle criterion and its converse

The stated integrality and sign tests are correct: `D | C` is equivalent
to integrality before cancellation; an integral odd-over-odd quotient is
odd; and `C>0` makes its sign the sign of `D`.

For an explicit converse from an actual orbit to the fixed-point formula,
put `f_a(x)=(3x+1)/2^a`. Induction gives

    f_(a_m) o ... o f_(a_1)(x) = (3^m x+C(p))/2^A.

At an actual periodic starting point this equals `x`, so `Dx=C(p)`.
Since `D != 0`, its rational solution is uniquely `x_p`. The cyclic
transport identity supplies all actual odd-step arrows for the reverse
direction. If a primitive packet produced a shorter odd period, the
deterministic valuation itinerary would repeat with that proper divisor
of `m`, contradicting packet primitivity. Thus the exact-period claim
is valid.

## 7. Residue domains and matrix conventions

For residue calculations, allow `m>=1` and integer `A>=0`, with

    Pi_(m,A) = empty, R_(m,A)(q) = empty, v_(m,A)^(q) = 0  when A<m.

The displayed base case `R_(1,A)(q)={1}` at line 297 must be restricted
to `A>=1`. At `A=0` the packet set is empty. The existing certificate
already implements this distinction.

Use a positive odd modulus `q`. Either state `q>=3` for multiplicative
order, or explicitly set `ord_1(2)=1` for the singleton modulus. The
latter convention preserves the trivial boundary case.

With column count vectors, define the matrix by

    M_(m,a)^(q) e_r = e_(3^(m-1)+2^a r).

The inverse is

    (M_(m,a)^(q))^(-1) e_s = e_(2^(-a)(s-3^(m-1))).

These formulas specify its orientation and prove it is a permutation.
The inverse of 2 exists because `q` is odd. At `q=1`, the matrix is
the one-by-one identity and the unique residue is `bar(1)=bar(0)`.

## 8. Complete proof of the rational generating series

Work in column-vector formal series `Z^q[[z]]`. Unique first-part
decomposition gives the count identity

    v_(m,A)^(q)
      = sum_(a=1)^(A-m+1) M_(m,a)^(q) v_(m-1,A-a)^(q).

Every coefficient has only finitely many contributing `a`, so this
identity may be summed as a formal Cauchy product. If
`lambda=ord_q(2)`, then `M_(m,a+lambda)^(q)=M_(m,a)^(q)`. Write every
positive `a` uniquely as `b+k lambda`, where `1<=b<=lambda` and
`k>=0`. This yields

    sum_(a>=1) z^a M_(m,a)^(q)
      = (sum_(b=1)^lambda z^b M_(m,b)^(q))/(1-z^lambda).

Together with `V_1(z)=z e_bar(1)/(1-z)`, this proves the displayed
recursion. More explicitly, put

    P_j(z) = sum_(b=1)^lambda z^b M_(j,b)^(q).

Then

    V_m^(q)(z)
      = P_m(z) P_(m-1)(z) ... P_2(z) z e_bar(1)
        / ((1-z)(1-z^lambda)^(m-1)).

The displayed order of matrix multiplication is essential. Every
coordinate is consequently rational in `z`. For `q=1`, this reduces
to `V_m(z)=z^m/(1-z)^m`, the ordinary positive-composition count.

## 9. Minimum strip, modular exclusion, and finite consequence

The cycle product identity and the strict minimum-strip inequalities
are valid. In a nonconstant positive cycle at least one entry exceeds
the minimum, giving strictness at the upper endpoint. The constant
positive integral case solves `x=1/(2^a-3)` and is exactly `x=1,a=2`.
The explicitly displayed orbit `3 -> 5 -> 1` also excludes 3 and 5
from a nontrivial positive cycle, so its odd minimum is at least 7.

The prime-factor exclusion implication is valid for any positive
divisor `q | D`, even if `q` is composite: `D | C` would imply
`q | C`, which contradicts absence of zero in the residue set.

The finite-period theorem follows from the displayed exact strip and
the exhaustive divisibility scans. The scan algorithms were inspected:
the separator construction enumerates all positive compositions and the
depth-first implementation does so by a distinct numerator recurrence.
The range `m <= A < 2m` used by the strip routine contains every possible
candidate because `22/7<4`. No extra period range was inferred.

## Executable checks actually run

The full portable certificate was not invoked. Its bounded functions
were executed through `runpy.run_path`:

- `check_packet_parity_morphism()`: PASS, 12,089 packets and 155,047
  shortened rational steps.
- `exact_strip()`: PASS, the displayed candidate list through `m=17`.
- `period_eight_classes()`: PASS, 792 words, 99 classes of size eight,
  231 residues modulo 233 with exactly `[0,138]` missing, 15 minimal
  representatives divisible by 7 and none divisible by 233 or 1631.
  The CSV byte count 3,358 and its SHA-256
  `13bd2d5451530fc7ab674720b5f142b489d0a1111161730a6d013f8fab69025b`
  also passed.

An additional independent in-memory test used all positive packets
with `1<=m<=5` and `m<=A<=m+5`. It checked the lists of one-positions,
the exact stabilizers, every rotation arrow and inverse, and every
composable pair. Result: PASS for 461 packets, 1,980 arrows/inverses,
and 8,910 composable pairs.

For moduli 1, 3, 5, and 9, `1<=m<=5`, and `0<=A<=m+5`, the test
compared direct residue count vectors against first-part recursion,
their supports against the portable `residue_set` routine, and the
periodicity of `2^a mod q`. Result: PASS for 180 residue-vector/support
cases, including empty packet sets at `A<m` and the singleton modulus.
The general formal-series proof above is not inferred from these finite
tests.

The two full 4,734,620-word streaming scans were **not rerun** in this
bounded audit. Their source was inspected, but fresh execution of the
full period-sixteen certificate and the source-binding wrapper remains
the responsibility of the integrating root workflow. This report does
not claim new full-scan receipts.

## Certificate additions to make at integration

The present portable certificate explicitly checks one-step packet
rotation and bounded primitive-period equivalence. It does not directly
enumerate the inverse/composition/stabilizer checks above or residue
count-vector multiplicities for the general generating-series interface.
Those bounded tests can be incorporated on the next certificate revision.
The wrapper's pinned portable size/hash and dependent receipts must then
be updated. The chapter's cycle-clock wording must change with the
certificate descriptions so the 155,047 steps are not represented as
full-map steps.

No TeX, certificate, existing project-state file, AGENTS file, Git state,
Lean process, or Overleaf content was changed by this audit. This report
was the sole new file written when the root agent requested durable
preservation of the completed findings.
