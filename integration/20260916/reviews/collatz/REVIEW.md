# Collatz delivery and PR #2 bounded review

## Verdict

The bilateral-root note's stated family, integral-retraction, and support-bound results are proved as written, with its explicitly finite catalogue and crossing window verified by the declared finite certificates. The intrinsic first-jet note's original-graph classification and integral witness extraction are also correct as written. This verdict is confined to these two fully read notes and the exact predecessor portions listed below; it is **not** an independent proof audit of all 95 files in PR #2.

The package is suitable for integration as an additive research contribution. One reproducibility defect needs either repair or an explicit platform qualification: native Windows writes CRLF in several `Path.write_text` outputs, while replay scripts compare them against committed LF files. The mathematical values agree exactly; the ordinary and optimized runs agree byte-for-byte with each other. The original Linux CI checks at the pinned head all pass.

## Exact objects, domains, and claims reviewed

1. On the positive odd integers, `T(n)=(3n+1)/2^nu_2(3n+1)`. Words retain original positive integral exponents, affine numerator `(3^k n+C)/2^A`, full positive source cylinder, and original target progression. The least positive image anchor lies below `2*3^k`, justified by the same affine map at its negative odd predecessor.
2. Bilateral Theorem 1 compares the actual left word `(1,2,1)` and right word `1^a,e,2^(b-1),1,1,3`, with `b>=1`, `e in {2,6}`, and the least contracting `a`. The exact two-modulus source class, both parameter inverses, original valuations, common endpoint, and smaller positive right source are proved. These are shared-future comparisons, not an assertion that the right source is a forward iterate of the left.
3. Theorem 2's mixed-family intersections force `9 | 42` or `9 | 6`. Minimal contraction precision is at least two, so the disjointness argument applies at every admitted ternary layer.
4. Theorem 3's maximal leading run is `nu_3(J*(n/3^b)+h)`. The parameter strata retain both nonzero units modulo three. Increasing this run decreases the original right source without changing the common peak or later path. Its chain comparison uses the original incoming edges and signed integral clock.
5. Theorems 4–5 use `D=Z[epsilon]/epsilon^2`, `q=1+epsilon`, and `d E_n=V_n-q V_T(n)`. All `q^k=1+k epsilon`, including negative integral `k`, are units; no cycle period is inverted. Strictly decreasing selected source height makes the chosen recursion terminate at retained roots. The identities `dH=I-Q`, `F=I-Hd`, both idempotences, `FH=0`, and nested projections follow from the original chains. The bound applies to the support of these homotopy columns, including unreduced roots, not to all Collatz trajectories or stopping times.
6. The exact operational bound is `R(n)=max(130(n+1),floor(64*n*4^k/3^k)+21)`, `k=floor_log3(n)`, and for `n>=27`, `R(n)<=64*n^(log_3 4)+21`. The longer leading run does not increase its actual peak; this is the load-bearing point in improving the old quadratic estimate. The uncollected edge count bounds both constant coefficients and first-jet coefficients as stated.
7. For the intrinsic first-jet comparison, the kernel is `C^1/(d C^0+P ker d)`, explicitly isomorphic to the actual kernel of constant reduction on first cohomology. A genuine primitive cycle of length `m` contributes `Z/mZ`, an acyclic component contributes `Z`, and the actual fixed loop at 1 remains present with zero defect. Finite frontier summands are not called divergent trajectories. The finite integral equations `db=0`, `dc-Pb=V_n` force an actual path to 1 within their original finite support; the component augmentation argument excludes all other periods.
8. The crossing envelope bounds the original affine numerator for a first coefficient crossing. Streaming every bounded candidate verifies both the first shortened-map crossing and its final odd-return endpoint; these are not conflated. The envelope extends the resulting horizon claim to unbounded starting integers, but says nothing about an orbit without a crossing in the stated horizon.

## Dependency graph and checks

- Original positive odd map and integer word formula → exact cylinder and target maps → complete two-word intersection and strict height intervals.
- Pinned ternary predecessor, Sections 2, 4, 5, 6 → old layer congruences, old retained residue set, old retraction order, and explicit old-layer peak. These sections were read from authenticated `b2dac4c2cc4a5eedde0af36d6749390c77fa4a62`, not from its PR summary.
- New family calculations → maximal-run strata → signed original chains → nested retraction → subquadratic original-support bound.
- Complete 112,050-row domain + independent formula/valuation replay → finite catalogue and exact residue cover. Positive-composition counts and strict lexical ordering establish exhaustive coverage, not sampling.
- Direct graph homology proof → integral first-jet receiver and path extraction. All eight supplied first-jet dependency files match the exact remote Git blobs at the package base.
- Written envelope + full 4,064,632-row independent source audit → stated 11,610-odd-step crossing horizon. No logarithm theorem or zeta estimate enters this implication.

Boundary cases checked in prose/code include empty word, fixed loop, period-one and repeated position circles, changed-forcing two-cycle, finite frontiers, `b=1`, both middle exponents, zero extra depth, both units, incompatible target fibres, false valuations, fractional witnesses, and truncated or duplicated ledgers. No defect in the stated mathematical implication was found. The broad novelty/literature status and all historic source-attribution records were not independently re-established in this bounded delivery review.

## Fresh execution

All commands execute the supplied, unchanged sources. They are recorded in `run_review.py`, individual receipts, stdout, stderr, and result files. The watcher sampled the aggregate process-tree RSS every 0.1 seconds with a 5,000,000,000-byte ceiling. No Lean process or Git scan was launched.

| Check | Fresh result |
| --- | --- |
| Original `replay.py --predecessor` | Native Windows fails after a passing 39,211-check first-jet run because of LF/CRLF bytes; failure preserved under `structural/`. |
| First-jet normal and optimized runs | 39,211 exact checks each; native outputs byte-identical; exact parsed values equal the committed receipt; CRLF-to-LF byte comparison isolates the portability defect. |
| Bilateral normal and optimized runs | 1,905,007 checks each; outputs exactly equal the committed bytes, SHA-256 `2560770274e1bf779f91e43f07906a4117a0857b0655e8c196192e02437767c4`. |
| Independent family audit | All 112,050 rows; 24,107 compatible families; 332,467 original affine equations; all nine malformed-ledger controls rejected. |
| Independent original-source audit | All 4,064,632 rows, 14,186,680 return equations and 28,378,002 repeated divisions; exact parsed output equals `evidence/audit11610.json`. |
| Source ledger | Uncompressed SHA-256 `87e6e08b9028b53f0ff6642a68777c68f8c0d3d7db436d39cfdb37af8021853b`. |
| Inputs | All package input hashes unchanged before/after each run. Complete package manifest passed. |

Structural native replay used 60.76 seconds and peaked at 142,172,160 RSS bytes. Independent source replay used 34.48 seconds and peaked at 39,460,864 bytes. The complete source producer was **not rerun**; the existing full ledger was independently verified instead. No larger source scan was needed for publication.

## PR and payload integration

- Current main: `63407034387466870f9e092dcdf39fb5a1ec0399`.
- PR #2: `research/stopped-cycle-cohomology-20260914`, exact reviewed head `b2dac4c2cc4a5eedde0af36d6749390c77fa4a62`, 11 commits and 95 added files. It was draft, mergeable and clean at snapshot. Its body advertises an older mixed-switch head; do not use that prose as its current identity.
- Nine successful exact-replay checks exist on that actual head; full service records are in `pr2_checks.json`. Those CI results are executable evidence, not a full independent proof audit of the predecessor stack.
- PR #1 is separate and add-only. It is being reviewed separately by the parent and is not a dependency of the bilateral increment.
- `ADDITIONS.json` lists exactly 17 new repository files. All should be added at their declared paths after PR #2's dependencies are present. The eight `intrinsic_zero_firstjet_20260915` copies are preserved identity witnesses, not additional changes.
- The package's complete `evidence/` directory is important and should be published alongside the new body (e.g. its `delivery/evidence/`), including both compressed full ledgers, not only summary JSON. They total about 33 MB compressed. Preserve `ADDITIONS.json`, `PACKAGE.json`, original delivery receipt and add-only patch as historical package provenance; they should not be rewritten to imply a new publication was already done.
- The attached private conversation transcript is a provenance/reference input, not automatically a public upload. Its final response explicitly says the 17-file increment was local and not pushed. Current authenticated GitHub agrees.

## Workflow safety and platform repair

All eight predecessor workflows and the new workflow use `pull_request` rather than `pull_request_target`, read-only contents permissions, no secrets, hosted Ubuntu, bounded job timeouts, and `persist-credentials: false`. Seven predecessor workflows and the new one pin actions by commit. The original stopped-cycle workflow alone uses `actions/checkout@v7` and `actions/setup-python@v7`; pinning those two to the same verified commits used elsewhere is recommended. No command or API in the contribution writes remote state during replay.

To make native Windows byte replay work without changing any mathematics, specify `newline='\n'` on `Path.write_text` for the first-jet verification output and the bilateral family/source auditor and source-scan outputs, then update only the source hashes that bind those changed executable bytes. Retain the original delivered package and this failure record. The bilateral structural producer already uses `write_bytes` and is byte-portable. Do not claim the original unmodified full replay passed natively on Windows.

## Zeta notification candidate

The direct edge is the intrinsic Split-Zero support diagram and its explicit first-jet constant-reduction comparison. It supplies the original integral kernel, source-labelled support transitions, and chain-homotopy retractions, with finite cycle-index torsion distinguished from nonperiodic free summands. The new bilateral construction provides a subquadratic original-support bound for those specific maps. Notify the zeta owner with links to the first-jet note and bilateral note after publication; these are exact maps and bounds useful for comparison. Do not describe them as an RH estimate, transport an unproved zeta endpoint, or replace the first-jet kernel with the earlier finite Hurwitz history encoding. The package expressly imports no zeta estimate.
