# Exact stopped Collatz transport — 14 September 2026

The principal construction is an exact restart on the **original arithmetic progression**, not a replacement by uniformly sampled consecutive odd integers. It retains the full affine numerator, the power-of-three target lattice, its integral image cohomology and affine coset, synchronized residue marks, the actual first-descent index, and original-source ancestry.

This is a self-contained, add-only local contribution intended for `KokunoYumeto/collatz-workbench`. No current repository revision was read successfully, and no remote change is claimed. See `PROVENANCE.md` before integration.

## Read

`note.md` contains complete proofs. Sections 3–4 give the restart and arithmetic image complex. Section 5 supplies the exact joint-observation fibers. Sections 7–8 prove the retained-translation square-root estimate and completed stopping-law error bound. Section 9 gives exact restart composition and its dyadic/triadic comparison. Section 10.0 gives an exact chain-map span from support incidence through actual affine incidence to the image complex, with its connecting moment map and retained-anchor homotopy. The remaining parts of Section 10 give zero-preserving support and finite Hurwitz inversion.

`verify.py` is both a reusable exact-arithmetic module and its executable test suite. `verification.json` is the deterministic result. `EXECUTION_RECEIPT.json` identifies the executed bytes and ordinary/optimized replays; `MANIFEST.sha256` covers the distributed contribution files other than itself. `HANDOFF.md` records the state and integration boundaries. `example_certificate.json` fully enumerates two small finite observations, their support masks, source fibers, incidence maps, and two image cosets (including a supported zero). Rebuild it with `python make_certificate.py --output example_certificate.json`. Its 142 validation checks are additional to the main suite.

## Replay

Python 3.10 or later; standard library only. From this directory:

```sh
python verify.py --output replay.json
python -O verify.py --output replay_optimized.json
```

Both outputs should be byte-identical to `verification.json`. A cross-platform comparison is:

```sh
python -c "from pathlib import Path; a=Path('verification.json').read_bytes(); b=Path('replay.json').read_bytes(); c=Path('replay_optimized.json').read_bytes(); raise SystemExit(0 if a == b == c else 1)"
```

Checks are explicit exceptions, not optimization-disabled assertions. The suite records 175,269 successful checks and 180 marked-law fixtures. The finite checks do not substitute for the written infinite and asymptotic proofs.

## Use the actual progression chart

```python
from verify import Family, packet, chart, odd_steps, finite_law

source = Family(a=1, d=1, b=1, N=1024)  # n(t)=1+2t, t=1,...,1024
p = packet((1, 1, 3, 2))
c = chart(source, p)
print(c)
# Chart(g=1, P=128, s=123, u=157, target_d=81)
# Source t=123+128v gives n=247+256v and target y=157+162v.

P, Q, tv, occupied = finite_law(source, H=10, M=3)
print('Exact total variation:', tv)
print('Actual cutoff overflow:', P[('overflow',)])
print('Reference cutoff overflow:', Q[('overflow',)])
```

The output `target_d=81` is retained. Substituting `target_d=1` is not an allowed restart. `chart` returns `None` for a proved congruence incompatibility, which is distinct from a compatible chart with no points in the finite sample; the declared label and mask should be retained in either case.

The positive-integer descent engine starts at odd values at least 3 and separately absorbs 1. The reference parity-code renewal fixture also includes 1, with its actual repeated exponent word `(2)`, solely to verify the finite dyadic cylinder identity. It does not claim strict descent of 1.

## What has been obtained

For a compatible source `a+2dt` and word with data `(A,L,C)`, the exact source restriction is `t=s+Pv`, and its actual image is `u+2(d/g)L v`, with `g=gcd(d,2**A)`. The integer image complex is `[Z --(d/g)L--> Z]`, with its original affine coset recorded. Its local coefficient comparisons have explicit inverse chain maps and homotopies.

The stopping rule uses the entire affine expression at the literal reference 3. Every supported leaf strictly descends on every actual source value at least 3. All completed exponents and the actual earlier first descent remain recorded. The full countable stopped observation has an explicit error bound and a proved geometric reference tail, without a fixed final return horizon.

The result does not prove that every positive integer belongs to a certified stopping fiber. A never-certified atom, finite cutoff overflow, and every declared zero-weight label remain explicit. No proof of all-integer Collatz convergence or novelty over the stopping-time literature is claimed.
