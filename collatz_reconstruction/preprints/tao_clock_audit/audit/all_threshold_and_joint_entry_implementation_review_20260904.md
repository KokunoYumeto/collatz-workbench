# Review of the implemented entrance-family and joint-law results

Review ID: `AUD-TAO-V7-ENTRANCE-IMPLEMENTATION-20260904-0002`.
Date: 2026-09-04. Verdict: **PASS at the stated mathematical and framing
scope**. This reviews the actual edited files, not merely the proposal in
`all_threshold_entrance_family_v7_review_20260904.md`.

## Reviewed snapshots

Paths are relative to `collatz_reconstruction/preprints/tao_clock_audit/`.
The three requested files were read completely; the unchanged transport
definitions were checked against the preceding direct reading.

| File | SHA-256 |
| --- | --- |
| `main.tex` | `c4423fcf4d9be9db296d6db0ee4d922a4be04667cafeb30c7a81d167d90284a5` |
| `sections/consequences.tex` | `853f19899655f2fd1605a12d7dc819513410c09e812d5dc70210c5b60e2d7ea5` |
| `sections/transport.tex` | `b3233b2b79614e1279a9d880eb7e82c21d5822873085bdaadf49332c2cd88678` |
| `sections/versions.tex` | `8e98ab6298102e4fc11b6e1a42ca884d8c442cc09f982380f945315f80b557d1` |

The controlling primary-source identity remains Tao's V7 `collatz.tex`,
SHA-256 `bfbc39432d4084a276416cb019a592003c868fa32f18e2f90028ac325ae5c19d`.
Its Section 1.3 and Section 3 relation was directly read and recorded in
the preceding review. No other source version was read here.

## `cor:limit`, consequences lines 54-132

The common base is fixed before quantifying over thresholds. The definition
`lambda_(x,j)^(b) = K_x mu_(t_(j+1))` is well-defined for every real x >= 1
and j >= 0: all input scales exceed b >= s_*, while E_x is finite and
contains the absorbing failure state. The norm is consistently unhalved l1.

For x <= t_j, both displayed identities at the start of the proof are
correct. In the second identity, the operator sequence is
`K_x K_(t_j) K_(t_(j+1))`; nested passage reduces it to K_x. The adjacent
difference is therefore bounded by e(t_j), with the same B' and c used in
the completed input estimate. The tail is
`B' (log t_j)^(-c) / (1-alpha^(-c))`, with no shifted index or missing
factor of alpha. The estimate is uniform over all 1 <= x <= t_j.

Finite-dimensional completeness, positivity and total mass one justify
the probability limit. Exact compatibility at arbitrary thresholds follows
from the common input sequence and holds before taking the limit as well.

For x >= b, the unique k with `t_k <= x < t_(k+1)` exists, including x=b
and exact lattice thresholds. The proof uses `r=t_k>x^(1/alpha)` and
`lambda_(r,k)^(b)=nu_r`. It applies the rate at threshold r, not at x and
an index too small for x. Nonnegativity and `p_r(dagger)=dagger` give the
correct direction
`lambda_x^infinity(dagger) <= lambda_r^infinity(dagger)`.
Substitution gives precisely
`B x^(-c/alpha) + L_c alpha^c (log x)^(-c)`.

The paragraph at lines 126-132 correctly retains the base-phase question,
proves equality for shifted bases, and identifies the old threshold-based
construction only at thresholds t_k. It does not silently identify limits
from arbitrary bases.

## `cor:joint-entry`, consequences lines 134-170

The finite joint state space is correctly typed as a subset of the product
of the E_(x_i). Its compatibility equations include failures. The map

    J(z) = (p_(x_1)(z), ..., p_(x_r)(z))

has domain E_(x_r) and codomain C. Since p_(x_r) fixes E_(x_r), its last
coordinate is z. For a compatible tuple, repeatedly substituting the
adjacent equations and using nested passage gives
`z_i=p_(x_i)(z_r)`. This proves surjectivity, injectivity and the stated
inverse. The argument also covers r=1, equal successive thresholds, and
the absorbing point.

An injective deterministic pushforward preserves l1 for signed measures:
each image atom receives the mass of exactly one source atom, and atoms
outside the image receive zero. Thus the claimed isometry, rather than
only contraction, is correct.

The finite joint law is exactly `J_* lambda_(x_r,j)^(b)` by nested passage.
Its limiting law has the explicit point-mass description

    Lambda(z_1,...,z_r) = lambda_(x_r)^infinity(z_r)
                         if z_i=p_(x_i)(z_r) for every i,
                       = 0 otherwise.

Consequently the joint l1 error equals the largest-threshold marginal's
l1 error, proving the bound with no factor depending on r. Projection to
coordinate i gives `K_(x_i) lambda_(x_r)^infinity`, hence the required
marginal by exact compatibility. No independence or coupling assumption
between different N_j is used or needed.

## Introduction and version-section framing

The abstract and introduction explicitly use one common sequence of
starting scales. Their joint-error statement is supported by the isometry
proof. Main lines 114-116 expressly identify the family as a distributional
consequence and retain Tao's ownership of the quantitative orbit-minimum
bound. The reviewed prose does not claim a stronger orbit-minimum theorem,
a new Fourier estimate, or established literature-wide priority.

The reserve subsection attributes the 0.99 reserve to Tao and describes
the explicit sufficient bound without claiming necessity. The dyadic-weight
and threshold-envelope passages identify local displayed errors and retain
the limiting conclusion; they do not frame them as refutations of Tao's
theorem. Their assertions were not expanded into a new full proof audit in
this implementation check.

One optional wording refinement was sent to the parent: versions line 71
says "exactly the improved reserve". "Exactly the retained reserve" would
avoid an unanchored comparison or a suggestion that this paper enlarged
Tao's margin. The surrounding attribution already makes its meaning clear;
this is not a mathematical defect or a blocking revision.

## Action boundary

No source, TeX, manifest, ledger or remote object was edited. No build,
Lean, Git, additional agent or upload was run. This report is the sole
new artifact from the implementation recheck. Build and rendered-output
checks are owned by the parent task and are not claimed here.
