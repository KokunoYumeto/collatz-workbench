# Cycle detection and counterexample-preserving descent compression

This is the continuation of the **unchanged** `../stopped_affine_transport_20260914/` package. Read `note.md` for complete proofs and `TASK_STATE.md` for the live mathematical target and source/publication boundaries.

The executable uses original Collatz packets and exact integer/fraction arithmetic. It links the preceding image lattice to a return complex by a joint endpoint-incidence map, distinguishes primitive positive integer cycles from rational or repeated trivial cycles, and constructs a relative graph complex with every unresolved frontier retained.

The central result is Theorem 6.1: checked strict-descent paths give an explicit chain-homotopy retraction that fixes every cycle chain literally. Theorem 6.2 applies the unchanged predecessor observer to the entire positive source and proves the nested cutoff-map identities and their pointwise finite-support limit. The surviving source is retained; no all-integer convergence conclusion is claimed.

## Read and replay

- `note.md`: full mathematical argument, including the nonperiodic component detector.
- `cycle_detector.py`: reusable exact arithmetic, finite graph, path, and descent-compression APIs.
- `verify.py`: independent matrix and graph-rank checks, full sum-bounded word enumeration, and the executable bridge to the predecessor.
- `verification.json`: deterministic results, complete examples, control cycle, and cutoff-root evidence.
- `replay_all.py`: verify both contributions' manifests and rerun all six ordinary/optimized outputs in temporary files.

From this directory:

```sh
python replay_all.py
```

The new suite performs 42,507 named exact checks, independently solves 344 matrix fixtures, exhaustively tests 468 modular fixtures, and visits all 1,048,575 nonempty exponent words of total sum at most 20. It also builds actual finite path certificates for the 2,048 positive odd starts at most 4095. These are finite replay scopes, not a global proof or a claim to a computational record.

The original suite remains separately recorded at 175,269 checks, with its additional 142-check source certificate. Neither original file contents nor old publication-status receipts have been rewritten.

## Exact commands

```sh
# A repeated trivial cycle: marked class zero, primitive word (2), relative cycle removed.
python cycle_detector.py cycle 2 2

# A positive rational cycle with a genuine order-19 integral obstruction.
python cycle_detector.py cycle 1 1 2 4 3

# Actual finite path or a retained OPEN_BOUNDARY; a cap is not a divergence verdict.
python cycle_detector.py path 27 --cap 100

# Whole-source retraction using the exact predecessor observer.
python cycle_detector.py compress 27 --cutoff 64
python cycle_detector.py compress 27 --cutoff 128

# Original graph with the open vertex 5 retained, then its actual killing edge.
python cycle_detector.py graph 3
python cycle_detector.py graph 3 5

# Explicitly changed-forcing control, NOT a positive 3x+1 counterexample.
python cycle_detector.py cycle 1 2 --forcing -1
python cycle_detector.py graph 5 7 --forcing -1

# Exhaust the declared exponent-sum domain without conjectural pruning.
python cycle_detector.py enumerate --sum-bound 20 --output bounded_words.json
```

The control's relation to the original signed map is exactly `T_minus(n) = -T_plus(-n)`. Its forcing constant is stored, not silently changed.

## Publication boundary

Prepared for `KokunoYumeto/collatz-workbench`. At this delivery, the authenticated GitHub connector remained uninstalled/disconnected; the current Collatz tree and its method section were not recovered. The Git objects in the accompanying bundle are real **local packaging commits**, not commits verified on GitHub and not a claimed descendant of current remote `main`.

The add-only integration payload preserves any existing byte-identical contribution files and aborts before writing if any target file differs. It does not overwrite current work, force-push, merge to `main`, or change permissions. The proposed GitHub Actions workflow only reads repository contents and runs the replay; no remote CI success is asserted.
