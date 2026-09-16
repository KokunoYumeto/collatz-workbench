# Independent review of Collatz Workbench PR 1

**Verdict: proved as written. Merge-ready at the reviewed revision.**

Reviewed on 16 September 2026: `KokunoYumeto/collatz-workbench`, PR 1,
head `6521481204342b7430f651491852a6b80d4230a5`, base
`63407034387466870f9e092dcdf39fb5a1ec0399`. The full research note and full
checker were read, rather than relying on the PR description or recorded pass.
This is an independent agent review, not a formal proof certificate or an
independent human referee report. No remote change was made by this reviewer.

## Exact claim

Sample uniformly from N consecutive positive odd integers, starting at 2b+1,
where N >= 1 and b >= 0. Let P be the distribution of the complete first m
positive odd-return valuation exponents, m >= 1, and let G(w) = 2^(-sum w).
For half-L1 total variation, the note proves exact finite interval counts,
the stated explicit upper/lower bounds, and the location-uniform limit

    sup over b >= 0 | Delta(P[N,b,m_N],G[m_N]) - Phi(2c) | -> 0,
    m_N = floor(log2(N)/2 + c sqrt(log2(N))), c fixed real.

The definition of m_N is used only for sufficiently large N, where m_N >= 1.
The descent certificate separately counts actual starts whose odd-return orbit
falls strictly below its initial value within m returns. It retains all affine
offsets and records the exact unexamined sample count as overflow.

## Dependency and proof checks

| Check | Finding |
|---|---|
| Exact odd-return cylinder | Passed. The congruence modulo 2^(A+1) includes the final oddness bit. Suffix induction forces every intermediate quotient odd. |
| Interval floor formula | Passed. Mapping n=2j+1 gives modulus 2^A and inclusive endpoint count floor((b+N-1-h)/2^A)-floor((b-1-h)/2^A). |
| Geometric tail and cardinality | Passed. Positive compositions with total <= H number binom(H,m); the geometric tail is the fair-binomial lower tail. H<m correctly gives an empty retained set and tail one. |
| Finite TV sandwich | Passed. Upper bound comes from sum min(P,G) on retained atoms. Lower bound uses at most N occupied atoms, each omitted-tail atom of G at most 2^(-H-1). No independence is assumed for actual starts. |
| Rounding and support refinements | Passed. Floor counts give the fractional-part correction. Sorting G atoms by exponent sum gives the stated optimal bound from support cardinality alone, including ties. |
| Exact dyadic formula | Passed. For N=2^L, low-exponent cylinder counts are exact; high-exponent occupied cylinders have one start, so overlap is precisely their G mass. |
| Gaussian critical window | Passed. H-=floor(L-L^(1/4)) and H+=ceil(L+L^(1/4)) leave uniform errors tending to zero. In each binomial tail, (2m-2-H)/sqrt(H) tends to 2c. The displayed characteristic-function calculation and continuity theorem give the limit. |
| Off-critical estimates | Passed. Both integer endpoint errors have the stated signs; the exponential moment bound follows from cosh(t/2)<=exp(t^2/8). The m>H case is explicitly handled. |
| Capped spectral input | Passed. All retained residue nodes are distinct even across different exponent sums, because a shared positive integer cannot have two length-m histories. Adding node zero for overflow preserves distinctness. The predecessor's proof applies to this finite node set. |
| Exact strict descent | Passed. T^j(n)<n iff D_j>0 and n>B_j/D_j. Conjunction over prefixes gives no descent iff n<=min floor(B_j/D_j). The positive fixed point n=1 is not spuriously counted as descending. |
| Capped descent interval | Passed. The retained exact descending count plus the exact number of overflow starts gives both bounds; overflow is not replaced by its geometric comparison probability. |

The proof dependency graph is acyclic: affine composition -> exact cylinders
-> interval counts -> finite TV bounds -> Gaussian cutoff. Separately, affine
prefix inequalities + cylinder counts -> finite descent bounds. The spectral
application uses exact finite weights, the established predecessor's full
cluster/moment inverse, and finite Lagrange interpolation. No statistical or
descent conclusion is extracted from the mere existence of that encoding.

## Source check

The canonical corpus was queried for `Collatz geometric`, in both literature
and local-note layers. The Tao V7 source was routed as publication unit
`PUBUNIT-847E4E7212BFCD7A613CA573`. Definition 1.7, the full-L1 convention,
Proposition 1.9 and Section 4 were read in the exact source TeX. Their cylinder
and geometric-law mechanism is credited appropriately. The note does not
assume Tao's strong residue-uniformity hypothesis for every arbitrary interval;
it establishes the relevant discrepancy directly.

The entire pinned predecessor `note.tex` (blob
`5fec479a48c4253eadffb9ed3c78da81b58a0000`) was read, including the analytic
cluster-to-moment recurrence and its restriction to actual cluster jets.
The Hurwitz Taylor identity was checked against
[DLMF 25.11.10](https://dlmf.nist.gov/25.11.E10), with a=1+t r and |t r|<1.
No global novelty search or novelty claim is made in this review.

## Finite replay

The reviewed checker has SHA256
`101914ebe50d5da54da6f3958b247d7d1a43f358f4c965736e3e161f11167ab7`.
All four payload files match their submitted manifest hashes and sizes.
The source is standard-library-only, launches no child process, and contains
no remote writes or contributed shell command execution.

Commands, sequentially, under Python 3.13.9:

    python -B check_history_law.py
    python -O -B check_history_law.py

Both completed successfully: 3.966948 seconds and 3.624114 seconds. Peak sampled
working sets were 88,010,752 and 88,297,472 bytes. A 5,000,000,000-byte working-set
watch and 180-second timeout were enforced on each reviewed single-process run.
The first wrapper attempt had a Windows process-handle exit-code retrieval
error after the checker had produced complete output; it was not accepted as a
receipt. The wrapper was repaired by retaining the process handle, and both
full runs were repeated successfully.

Both accepted output files have identical SHA256
`848575341dba3a1e8c6b8b15edab86ec13b72f622041b08e7b46313e3efa138a`.
They match submitted `verification.json` after the explicitly recorded Windows
CRLF-to-LF newline conversion. This is not a claim that the Windows output bytes
have the same hash as the submitted Unix-newline file.

Reproduced: 55 capped families, 4,422 lifts, 72 interval laws, 6,600 exact
cylinder counts, 1,224 TV envelopes, 3,006 descent equivalences, 216 descent
certificates, 21 moment reconstructions, three joint predicates, and 332,032
profile starts. All five negative controls were rejected. The N=4096,m=5,H=16
fixture gives 3,929 accounted starts, 167 overflow starts, descending interval
[3320,3487], and independent direct count 3487. This fixture does not imply
every overflow start always descends.

See `REPLAY_RECEIPT.json`, `replayed.normal.json`, `replayed.optimized.json`,
and `replay_review.ps1` for executable provenance. The finite checks do not
numerically certify the Gaussian limit; Section 4 supplies its proof.

## Integration boundaries

The five PR1 paths are new and disjoint from the paths changed by current PR2,
head `b2dac4c2cc4a5eedde0af36d6749390c77fa4a62`. Both share the same base;
PR2 is not a stack that includes PR1. PR1 can be merged independently after the
parent's final live head comparison.

Fresh GitHub readback found PR1 open, mergeable, and clean. There are zero
check runs and zero commit-status contexts. The status API's aggregate `pending`
therefore supplies no CI evidence, positive or negative. The local reviewed
replay is the execution evidence.

There is no blocking mathematical defect or unfinished required repair within
this bounded contribution. It proves neither Collatz convergence nor an
improvement to Tao's orbit-minimum theorem. The spectral application is an
exact finite encoding, not an inverse-conditioning estimate. No Lean or
numerical zeta-zero computation was run or claimed.
