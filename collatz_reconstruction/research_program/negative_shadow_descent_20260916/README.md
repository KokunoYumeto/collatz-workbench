# Positive shadow descent from retained integral sections

**16 September 2026 — additive Collatz continuation.** Read `note.md` for the complete proofs. Current remote source pin: `d0c987b12c20be5978f496ab1ef2a60018caa5e5`. Publication status is supplied by the delivery receipt, not inferred from the presence of this file.

## Proved arithmetic

The nine original signed anchors -5,-7,-17,-25,-37,-55,-41,-61,-91 retain their original `3*x+1` packets. The two-letter packets have `(U,L)=(8,9)`; the seven-letter packets have `(2048,2187)`. Their integral forcing classes vanish with specified negative primitives. A positive source following r copies is exactly `n=2*U^r*t-h`, `t>=1`, and maps to `2*L^r*t-h`.

For every r,s>=1 and every falling tail `(c_1,...,c_s)`, `c_i>=2`, the full positive source strictly descends throughout the actual coefficient-crossing domain

```
U^r * 2^(sum c_i) > L^r * 3^s.
```

There is no restriction on repetition count, tail length, or the individual exponents. The full affine correction is retained. The proof uses two all-length integer gap inequalities, Matveev's explicitly cited theorem, exact rational logarithm bounds, and 32,512 complete integer base rows. It does not use a large verified interval of starting integers. The cones `s>=ceil(r/2)` for the two-letter packets and `s>=ceil(r/4)` for the seven-letter packets also have elementary proofs without the logarithm input.

Every actual positive cycle must have a contracting full coefficient. Therefore this excludes all cycles whose traversal word is a cyclic rotation of a repeated listed packet followed by an all-falling tail. It covers arbitrarily many separated rise runs, but not arbitrary mixed words. It is not a claimed numerical cycle record or global convergence proof.

## Intrinsic supported-zero data actually used

The negative integral primitive, the original section defect, the positive source cone, and the inverse affine coordinate are retained with the supported zero forcing class. The translation between the negative anchor and the actual fixed point at 1 is `h+1`; it is not removed. A zero anchored forcing for a pure-two tail keeps its original differential and multiplier.

Every accepted positive block returns to the unchanged first-jet kernel by

```
d_epsilon(epsilon * path) = epsilon*V_source - epsilon*V_endpoint.
```

An existing integral endpoint witness splices through this exact equation. An individual descent is not promoted to convergence for every variable endpoint without a further witness.

## Mixed-switch continuation

For the original `t == 1 mod 8` stratum after `(1,2)^r`, the next exponent is three and the following maximal one-run has exact length

```
k = nu_2(9^r*t-1)-3,
t == 9^(-r)*(1+2^(k+3))  (mod 2^(k+4)).
```

At `t=1`, this is `k=nu_2(r)`. The dependence on t is retained: arbitrary reset depths still occur. The rule's failed application at `r=12,t=1` is followed by a separate full original-cylinder first-descent certificate, not left as a false success or divergence verdict.

## Run

Python 3.11+; standard library only. The unchanged first-jet dependency must exist alongside this directory.

```sh
python -B collatz_reconstruction/research_program/negative_shadow_descent_20260916/replay.py
python -B collatz_reconstruction/research_program/negative_shadow_descent_20260916/shadow_descent.py query 17 4 1
python -B collatz_reconstruction/research_program/negative_shadow_descent_20260916/shadow_descent.py family 5 8 3
python -B collatz_reconstruction/research_program/negative_shadow_descent_20260916/shadow_descent.py reset 12
python -B collatz_reconstruction/research_program/negative_shadow_descent_20260916/shadow_descent.py repair
```

The replay checks every new manifest hash, the authenticated first-jet Git blob, all finite gap rows, positive source lifts, the exact reset strata, and ordinary/optimized byte equality. `--predecessor` additionally replays the unchanged first-jet suite.

With the separately delivered earlier arithmetic atlas present:

```sh
python -B collatz_reconstruction/research_program/negative_shadow_descent_20260916/crosscheck_atlas.py --check
```

That optional crosswalk identifies 72 existing full cylinders covering 41,638 original points in the earlier interval. Of those, 56 cylinders and 5,188 points have multiple rise runs. This finite crosswalk is not a premise of the unrestricted-parameter theorem, and no new discovery starts were added for it.

## Evidence and status

`gap_bases.json.gz` contains every finite base row. `examples.json` contains the original descent paths and finite integral witnesses. `verification.json` gives the rational intervals and exact checking scopes. `SOURCE_INTAKE.json` pins the actual source and the explicit external mathematical input. `TASK_STATE.md` records the residual arithmetic.

The result has written proofs and exact computational certificates. No Lean execution or independent external mathematical review is claimed. Old sources and recorded results remain unchanged. The proposed workflow is read-only; only an actual observed remote run can certify GitHub CI for a publication.
