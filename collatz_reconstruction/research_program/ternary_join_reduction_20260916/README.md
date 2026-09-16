# Ternary-layer joins and bounded original-support reduction

Read `note.md`, then `TASK_STATE.md`. This additive continuation starts at
`9afcbe2dc9bace77c1ae705b1cd128da22fe8f8b` on the Collatz review branch. It imports
no unproved Zeta estimate and does not integrate the separately pending earlier
local packages. The needed source definitions and proofs are reproduced here.

## Proved results

For every b>=1 and e in {2,6}, an explicit minimal leading run defines the full
original pair n -> y <- m with m<n, original word (1)^a,e,(2)^(b-1),3, and actual
valuation nu_3(n)=b. The two e values cover their specified complete residue
families in the two ternary unit classes. They do not cover every integer in
either unit class. Their original targets and both inverse parameters remain.

The complete finite catalogue contains 20,397 eligible right words of lengths
2 through 12. An exact residue-cover procedure selects 370 full families. It
reduces the old 98,091 root residues to 93,025 at period 708,588. The infinite
layer family removes further specified source classes at all higher valuations.
All candidate masks, including redundant and empty new-cover faces, are retained.

The resulting first-jet retraction acts on EVERY positive odd source and has
finite integral columns. It retains unresolved roots. Its H column at source n
uses original odd vertices at most 64*n*n+21; its uncollected edge-term count is
at most ((n-1)/2)*(2*floor(log_3(n))+14). These are bounds for the reduction to
retained roots, not bounds for arbitrary Collatz stopping times.

The sharp first-crossing envelope is replayed through 10,945 odd steps. Its
candidate ceiling is 6,728,242. All 3,364,120 original odd sources through
6,728,241 pass, with 11,738,935 original return equations independently replayed
by 23,482,682 divisions. This certifies the crossing statement for unbounded
starting integers whose first crossing involves at most that many odd steps.
Sources without such a crossing remain unclaimed.

## Replay

From the repository root:

```sh
python -B collatz_reconstruction/research_program/ternary_join_reduction_20260916/replay.py
python -B collatz_reconstruction/research_program/ternary_join_reduction_20260916/replay.py --full --predecessor
python -B collatz_reconstruction/research_program/ternary_join_reduction_20260916/join_control.py layer 2 6
python -B collatz_reconstruction/research_program/ternary_join_reduction_20260916/join_control.py reduce 13704327
```

The default runs both structural regressions and checks source identities. The
full command regenerates every original-source row, repeats the scan optimized,
and runs the separate all-row auditor. `--work-dir DIR` keeps the generated
ledger and receipts. The manifest pins the complete proof by its Git-blob hash
and all other source bytes by SHA-256. No network fetch or package install is
performed by the replay.

`verification.json` pins the complete regenerated structural result (589,090
named checks per run). `verify.py --output full.json` materializes all selected
families, masks and original point witnesses. `window_certificate.json` pins
both full source receipts and the uncompressed ledger hash. General statements
have written proofs, not just regression counts. Remote commit and observed CI
status belong to the separate publication receipt. No merge is performed.
