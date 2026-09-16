# Original section defects, all-length descent, and finite first-jet certificates

15 September 2026. Continuation from `d0c987b12c20be5978f496ab1ef2a60018caa5e5` on `KokunoYumeto/collatz-workbench`, PR #2. This is an additive local payload; its delivery receipt records the current remote write limitation. It is not a new remote commit or a claim of new GitHub CI.

## Read the mathematics

`note.md` proves the exact repeated-packet rank, its resonance equation under switching, an unbounded rank-reset descent family, elementary and rational run cones, and the original first-jet expansion/retraction. It gives the complete symbolic source cover and the separate all-length 1506-exponent-one-count cycle certificate.

`logarithmic_run_exclusion.md` completes the run argument using an explicitly cited established logarithm theorem, followed by a small exact rational certificate. It proves:

- Every original word consisting of a ones and then b exponents at least two strictly descends whenever `2^(a+2b)>3^(a+b)`. The actual larger exponents and all affine offsets remain retained. This is the pure-two comparison domain, not an assertion that every contracting arbitrary word descends.
- Every nontrivial positive cycle has `m>226*a`, where a is the maximal initial run of exponent one at its actual minimum and m is its original primitive odd-return length.
- No nontrivial positive cycle has all its exponent-one letters in a single cyclic run. Other exponents and the total word length are unbounded in this statement.

Matveev's theorem is an external established dependency, cited in its inspected rational-number formulation. The checker verifies the exact instantiation and all subsequent finite inequalities, not the proof of that transcendence theorem. The elementary 3/2 run cone is also provided without that dependency. These results are not claimed as a published cycle record or global Collatz proof.

## What is actually covered

`atlas.json.gz` contains 41,122 complete first-descent cells, each with its original word, source/target progression, full parameter interval and discovery source. All 583,199 odd sources from 3 through 1,166,399 are covered disjointly. The two declared zero-count labels remain present. Acceptance reconstructs every original affine constant/slope and parity identity, then checks the complete counting identity and every interval slot.

Their original equations generate a forward-closed support of 926,548 vertices, with the actual fixed loop retained, maximum vertex 30,079,718,549 and positive integral height at most 196. Every original edge is independently replayed. The first-jet connecting map on that finite support is `[-1]`. This gives finite integral witnesses for the covered interval, not a universal coverage claim.

The same interval supplies the source bound for the all-length cycle exclusion through 1,506 exponent-one positions. Its next retained budget is `(m,A,k)=(3631,5755,1507)` with odd minimum from 1,166,401 through 1,505,447. Ordered placements, actual primitive periods and integral forcing remain required. The next window is not a found cycle.

## Reproduce

Python 3.11+; standard library only. From this directory:

```sh
python -B replay.py
python -B replay.py --predecessors --rebuild-atlas
```

The first command checks the manifest, pinned predecessor identities, complete new source/edge certificates, and ordinary/optimized output equality. The second also replays the unchanged first-jet and structural pairs and independently regenerates the atlas from least-uncovered-source discovery. Regenerated gzip containers are compared after decompression, so platform header differences cannot affect the mathematical receipt.

From the repository root:

```sh
python -B collatz_reconstruction/research_program/defect_rank_descent_20260915/replay.py --predecessors
```

The new payload leaves all existing files unchanged. The locally recovered predecessor set is not a claim to be a complete clone of every current repository file. In particular the unrelated anchored package is not re-audited by this local command.

## Query actual certificates

```sh
python query.py repeat 31 --word 1
python query.py switch 43 --first 1 --second 2
python query.py resonance 8 0
python query.py peak 9
python query.py witness 1166399 --output witness-1166399.json
python query.py logarithm
```

Repetition output `null` is used only for the infinite valuation of an actual supported return defect and its unbounded exact copy count; `supported_zero` and `external_absence` are separate explicit fields. An unsupported domain raises an error, not a divergence conclusion. Every accepted first-jet witness is integral and its untruncated boundary is checked.

## Files and status

`morphisms.jsonl` lists domains, formulas, inverses and retained information. `SOURCE_INTAKE.json` pins the read sources and proof dependencies. `TASK_STATE.md` records the surviving packet-switch and cycle-ordering source. `verification.json` separates named regressions from fully enumerated original source and edge scopes. `logarithm_verification.json` contains all rational intervals and finite base rows, including the minimum-source parameter constraints. `retained_zero_minima.json` gives nine already-supported source witnesses, reused to sharpen the minimum-run bound from 213 to 226 without adding discovery starts.

The proposed read-only workflow is included for integration; it was not run on GitHub in this session. No Lean run or independent external mathematical review is claimed. The contribution still leaves the original aperiodic residual source and cycles with multiple exponent-one runs unresolved.
