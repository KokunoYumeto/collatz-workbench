# Mixed-switch control on the original Collatz source

16 September 2026. Read [note.md](note.md) for the complete proofs, exact source maps and external logarithm dependency. [SOURCE_INTAKE.json](SOURCE_INTAKE.json) pins the Zeta mixed-support reads and the unchanged Collatz first-jet validator.

## New arithmetic theorem

Let P=(1,2) and Q=(1,1,1,2,1,1,4). Take any finite ordered string containing both packet types, expand it to the original exponent word p, and retain any original cyclic phase. Repeat p at least twice, then append a nonempty tail whose exponents are all at least two. The complete positive source of this word strictly descends when its actual total multiplier crosses below one.

The number and order of switches inside p, both packet counts, its repetition count, and all falling exponents are unrestricted. The exact original affine numerator, rational primitive and its denominator lattice are retained. The proof controls those original data, rather than treating the packet actions as commuting.

The core source identity is n=(2*U^r*t-c)/d with its actual congruence 2*U^r*t=c modulo d. For PQ the retained primitive is -29839/3299, so this extends the preceding integer-anchor families rather than deleting a nonzero integral class.

The uniform integer gap proof uses a complete 210,527-row domain and the specified established Matveev bound. The coefficient envelope is proved for EVERY order and phase, not inferred from the 4,914 regression families. The complete computation is independent of the pending large positive-source atlas.

## Exact mixed information

The source read supplied original extension couplings and induced filtrations. The explicit common extension presentation and both coefficient evaluations are given in Section 1. The two-point integral overlap has cokernel Z/12Z; its induced dyadic filtration defect has orders 1,2,4,4,... with inverse maps. Actual sequential packet gluing retains the cross-term +6 or -6 and its exact unbounded reset residues. Reversing PQ to QP changes the original affine numerator by 1668; every surrounding factor is retained.

## Reproduce

From the repository root:

```sh
python -B collatz_reconstruction/research_program/mixed_switch_control_20260916/replay.py
```

This verifies the source manifest and the original firstjet Git blob, then reconstructs the full result in ordinary and optimized modes. Both result bytes must match the committed receipt's SHA-256 and length. The compact committed `verification.json` is a receipt; generate the full original records with:

```sh
python -B collatz_reconstruction/research_program/mixed_switch_control_20260916/verify.py --output full-result.json
```

Materialize every integer gap row:

```sh
python -B collatz_reconstruction/research_program/mixed_switch_control_20260916/verify.py --output full-result.json --ledger all-gap-rows.jsonl.gz
```

Query a complete original source cylinder:

```sh
python -B collatz_reconstruction/research_program/mixed_switch_control_20260916/mixed_switch.py PQ --repeat 3 --tail 3
```

The separate new workflow runs the unchanged firstjet pair before the new pair, with read-only repository permissions and pinned actions. All general maps are proved in the note; finite tests do not independently establish those general theorems.

## Continuation and integration

[TASK_STATE.md](TASK_STATE.md) retains the next exact switching task. This directory is additive to published base d0c987b12c20be5978f496ab1ef2a60018caa5e5. It does not overwrite any source, merge PR #2, or modify Zeta. The two older pending local directories are not implicitly published or adopted as proof dependencies here.

No global Collatz proof, original positive counterexample, independent external proof review, new numerical cycle record, or new Lean result is asserted.
