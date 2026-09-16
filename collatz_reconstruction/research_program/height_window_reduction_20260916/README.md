# Sharp first-crossing windows and integral global height reduction

Read the complete `note.md`. This is an additive Collatz continuation from published
PR #2 head `9afcbe2dc9bace77c1ae705b1cd128da22fe8f8b`. Publication is reported
separately; local source creation and a CI workflow file do not prove remote upload.

## Proved results

For a first coefficient crossing at odd step m, retain b_j=bit_length(3^j)-1.
The exact maximum of C/(2^A-3^m) over its full ordered word domain is

```
Theta_m = Cstar_m / (2^(b_m+1)-3^m),
Cstar_0=0, Cstar_m=3*Cstar_(m-1)+2^b_(m-1).
```

The maximizer has each proper prefix sum b_j and final sum b_m+1. Consequently
all first-crossing exceptions through any finite horizon M occur among the original
positive odd integers up to max floor(Theta_m). This is proved for every horizon,
not extrapolated from tested words. It uses no logarithm bound or Matveev theorem.
The shortened first-crossing endpoint is explicitly distinguished from the subsequent
odd endpoint and is checked at its own original clock.

At horizon **10,280**, the candidate ceiling is **5,624,777**. Every one of the
**2,812,388** odd sources from 3 to that ceiling has a complete original first-crossing
descent certificate. Thus first-crossing descent is established for every positive
starting integer n>=2 in that horizon, with unbounded final exponents. The point n=1
is retained separately. Global crossing existence and unrestricted-horizon coverage
are not established. This intersects the established Terras CST problem; no priority
or published computational record claim is made.

The new global comparison calculus synchronizes *any two original word images* by
their exact non-coprime congruences. Both full source progressions, their inverse
parameters, and their strict height interval remain. The family

```
1731+2916*t  -> 2597+4374*t <- T^7(1215+2048*t),  t>=0
```

relates an original source to a smaller member of its component even though the left
sources have no incoming Collatz edge. The right word is (1,1,1,1,1,2,3). The signed
integral first-jet chain has net clock -6. No edge reversal is called a forward iterate.

A fixed ordered rule set (one-step descent, three expanding-word inverses, then this
family) defines a **global finite-column chain-homotopy retraction**. Each recursion
terminates by decrease of its original integer endpoints. It retains the full first-jet
kernel and cycle indices. The exact remaining nonbase roots satisfy

```
n mod 36 in {3,7,15,19,27},
n mod 8748 != 8731, n mod 2916 != 1731.
```

They are selected arithmetic roots, not asserted counterexamples. The old/new
homotopies and both projection compositions are proved in note.md. A subgroup filtration
of the original first-jet kernel by source height records which new component classes
can first appear; reducing to a lower class is not automatically annihilating it.

## Reproduction (Python standard library)

From the repository root:

```sh
python -B collatz_reconstruction/research_program/height_window_reduction_20260916/replay.py --full --predecessor
```

`--full` regenerates the original-source ledger, repeats both source scans, and runs
the independent auditor on all rows. `--keep-ledger /path/sources.jsonl.gz` preserves
that regenerated file. Without `--full`, only manifested source checks and both structural
regressions run. The independently distributed ledger can also be replayed directly:

```sh
python -B collatz_reconstruction/research_program/height_window_reduction_20260916/audit_sources.py --horizon 10280 --ledger sources.jsonl.gz --output independent.json
```

Other exact calculations:

```sh
python -B collatz_reconstruction/research_program/height_window_reduction_20260916/height_control.py reduce 1731
python -B collatz_reconstruction/research_program/height_window_reduction_20260916/height_control.py coalescence --left 1 --right 1 1 1 1 1 2 3 --parameter 0
python -B collatz_reconstruction/research_program/height_window_reduction_20260916/height_control.py crossing 27
```

## Verification scopes

The two structural runs each have **67,172 named checks**, including the complete
65,535-word exponent-sum-16 domain, 1,600 small word pairs, original affine family
identities, both global retractions, and thirteen rejected false/malformed controls.
The complete proof window is separately counted: **9,808,846 original returns** and
**19,623,792 divisions**, across all 2,812,388 source rows. Both shortened and odd
crossing endpoints are checked. The independent source auditor imports neither the
main contribution nor any predecessor. Full source-data hashes and separate receipts
are in `source_scan.json`, `independent_source_audit.json`, and `envelope.json`.

The published original first-jet receiver is a byte-pinned dependency. The previous
pending `global_cylinder_control_20260916` package is preserved in the optional combined
patch, not used as a proof premise. The older pending 33-file arithmetic/shadow package
is not included. No new Lean execution, independent external mathematical review,
complete-source convergence theorem, positive counterexample, or GitHub CI outcome is
claimed by these local files.
