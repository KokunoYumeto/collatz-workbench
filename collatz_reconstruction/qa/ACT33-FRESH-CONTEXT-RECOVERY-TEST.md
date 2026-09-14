# ACT33 final fresh-context recovery test

## Test isolation and result

The final reviewer `/root/act33_stable_recovery` was spawned with no inherited
turns and received only the project root, the current ACT33 checkpoint path,
the read-only verification task, and explicit prohibitions against editing,
Lean/Lake execution, task contact, and browsing.  The reviewer read
`qa/RECOVERY-CHECKPOINT-20260828-ACT33.md` completely, inspected the hardened
state and pinned artifacts, and ran only the existing state validator and the
three permitted finite Python certificates.

Result: **PASS, with no discrepancy**.

The audited checkpoint was 24909 bytes, SHA-256
`613a1c5b6c2f5487c171e6b0e7e3688929062cc798d616bc34604fcb9fe87b41`.
All 42 explicit artifact pins matched.

## Recovered authority and restrictions

The reviewer recovered durable goal
`01a00ba5-a6b8-7410-b1e3-ab6dc0a4acf4` as active, with project status active
and `completion_claimed=false`.  It correctly recovered that ACT33 is not a
completion, release, upload, publication, or Collatz proof; that Chatnotes,
Gemini, and archived-task intake remain later layers; that task
`019fe2cf-438a-7112-859c-119accee0e9e` is quarantined; and that route misses
are bounded routing evidence rather than nonexistence claims.

It also recovered the resource rule: no uncapped
`R107DeficitProgression`, no overlapping Lean/Lake builds, and every later
formal run requires a fresh serial release and one watched process tree killed
at 3 GiB.  It distinguished the initial bounded recursion-depth failure, the
subsequent observed bounded PASS receipt (2033 bytes, SHA-256
`302a516b27c37455cdfd8ec9e7c90a969991f7829e48e74be9dacf5bff3358a1`),
and the still later bounded attempt that overwrote the mutable shared receipt
and ended `FAIL` with exit code -1.  It verified the durable snapshot
`qa/R7R11CRTForcing-RESOURCE-SNAPSHOT-20260828T155746Z.json`: 3790 bytes,
SHA-256
`6b02d63cff539499856ced4cde800e24ad43fef15ed14c6fa615b8686b32c49a`.
That snapshot records a 3221225472-byte ceiling, 100 ms polling, peak
individual working set 451620864 bytes, peak tree working set 470077440
bytes, no memory trigger, empty standard streams, and the
16:00:44.7358266Z zero-worker audit and fresh-release notification.  The
reviewer did not infer either the later attempt's initiator or the cause of
exit -1 and performed no new live process action.

## Recovered state and mathematical boundary

`python scripts/validate_state.py` passed with 152 route records, 80 document
routes, 32 sources, 136 claims, 32 morphisms, eight proof obligations, eight
expected missing-manifestation warnings, and zero failures.  It recovered the
next IDs `SRC-COL-000033`, `CLM-COL-000137`, `MOR-COL-000033`, and
`PO-COL-000009`, and verified that every obligation PO-COL-000001 through
PO-COL-000008 remains open, in progress, or pending.

The exact ACT33 record boundary was recovered:

- F028: CLM-COL-000122;
- F029: SRC-COL-000028, CLM-COL-000123 through CLM-COL-000126, and
  MOR-COL-000032;
- F030: SRC-COL-000029 through SRC-COL-000032 and CLM-COL-000127 through
  CLM-COL-000136, with no new morphism.

The reviewer preserved the distinction between shortened and unshortened
clocks: MOR-COL-000032 transports target-one reachability and witnessed
shortened states but does not identify clocks.  It separately recovered
Terras finite stopping, Allouche strict power descent, and Korec's stronger
strict power descent as different natural-density claims, without endpoint,
density-equivalence, Tao-theorem, or Collatz promotion.

## Recovered finite-certificate scopes

All three certificates passed.

- F028 reproduced 124 raw and 28 substantive v5/v7 hunks, 25 citation calls,
  23 cited keys, 24 bibliography items, sole uncited item `terras2`, 56
  journal pages, and the exact Section 6 margin calculations.  It did not
  certify the journal hunk matrix, explicit v5 counterexample family, Fourier
  decay, Tao's theorem, or Collatz.
- F029 reproduced 2010000 clock checks, 1005735 omitted-state checks, 10000
  target-one checks, and the exact 21/25 exponent margin.  It did not certify
  the unprinted k=11 vector or its feasibility, either infinite theorem
  independently, density, or Collatz.
- F030 reproduced 16392 classical, 64165 generalized-fibre, 139 count, 16382
  parity, 1752 terminal-word, 77 repaired-coverage, 49 agreement, and 36
  boundary checks, plus the separating sample k=529254.  It did not certify a
  central-limit theorem, passage to infinite density, the full density-one
  theorems, endpoints, Tao's theorem, or Collatz.

## Recovered build and visual evidence

The reviewer matched the 124-page, 1261638-byte PDF and SHA-256
`509b415815623cd7a0c661a3cd01a66282edd339eb07888d184b9acf2ff17f72`;
124 rendered PNGs totaling 52989982 bytes; eight canonical contact sheets
totaling 13253297 bytes; margin minima 213/216/211/132; and original-detail
pages 2--5, 12, 15--24, 113, 118, and 121--124.  It recovered zero undefined
references/citations, multiply defined labels, overfull boxes, or rerun
requests; six expected underfull path warnings; 26 embedded/subset font rows;
and no unembedded font.  It correctly left `visual_qa_complete=false` and
recorded `qpdf` as unavailable rather than passed.

## Intentional pre-seal discrepancy and next action

The only discrepancy found was the explicitly declared pre-seal boundary:
`coverage.json`, `project_state.json`, and `action_receipts.jsonl` still
pointed to ACT32 and 106 pages while the verified ACT33 artifacts existed.
Their pre-receipt hashes matched the checkpoint exactly, and the receipt
ledger ended contiguously at ACT-COL-000032.  The reviewer correctly classified
this as the pending seal operation rather than an unexpected mutation or a
reason to rebuild.

The deterministic next mathematical action recovered from fresh context is
to continue PO-COL-000001 with the remaining claim-driving cited literature,
querying the frozen routes first and reading primary content.  No later corpus
layer may be entered early, and every consequence must be propagated before
use.
