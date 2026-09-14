# Supported-zero structure and the Collatz proof programme

15 September 2026. Additive continuation of PR #2 at source commit
`6b3ded8880946b2c3140a9d79f1aa1d658d36b8c`.

Read **[note.md](note.md)**. It states and proves the structural restatement and
records the outstanding arithmetic obligations separately from established lemmas.
No inherited contribution is replaced, and no numerical cycle bound is advanced.

## Exact results

The maximal-one-run lemma retains the original source parameter, all intermediate
vertices, the terminal exponent and both clocks. It proves both clock counts are
cofinal on every infinite positive orbit that stays above 1. This gives an explicit
inverse for the v-action on the original cohomology; the u-action already had the
induced transfer operator as inverse.

The source cohomology therefore has a proved Laurent structure. Its complete
component decomposition has one `L/(1-W_C)` summand per actual nonbase periodic
component and one `L` summand per actual nonperiodic component, with
`L=Z[u,u^-1,v,v^-1]`. The actual base component has a retained finite-column
relative contraction. The note gives every component map and inverse, the full
cycle chain homotopy, the absolute/base-relative exact sequence, and the
fraction-field map with its entire periodic torsion kernel.

The original positive cone separates singleton absorption from signed path mergers.
The raw forcing polynomial and original word are retained, with the exact finite
duality and arithmetic coefficient map back to the original integral cycle equations.

## What remains to be proved

The proof programme in Sections 11-12 specifies periodic-torsion exhaustion,
generic nonperiodic-module exhaustion, ordinary-integer support in the complete
survivor-source tree, and construction of an original positive finite-column
contraction. These are targets, not assumed theorems. The program design separates
a small exact certificate checker from the search engine. Finite jets, signed
cancellations, and alphabet exits are not accepted as global convergence proofs.

## Replay

From this directory:

```sh
sha256sum -c MANIFEST.sha256
python -B verify.py --check verification.json
python -O -B verify.py --check verification.json
```

The recorded local executions passed 38,994 exact checks per run and returned
byte-identical results. The suite covers 2,048 actual block sources through 4095,
255 complete formal word-circle fixtures with total exponent at most 8, original
large-parameter run identities, Laurent coordinate comparisons, positive-cone
absorption and eleven rejected malformed inputs or false conclusions.
Formal word circles and the synthetic all-2 ray are explicitly not certified
positive Collatz orbits. The `3n-1` cycle is an explicitly changed-forcing control.
These are finite regressions; the general algebraic statements are proved in the
note. No independent external review, proof-assistant execution or new global
Collatz result is claimed.

The original completion proof was read in full from the uploaded file and checked
against authenticated Git blob `9f00643cb135acd77defec9e05ad63b632443a50`.
The actual current PR, the support-reconstruction source, and CONTRIBUTING were
also read. Source locators and attribution are in Section 13 of the note.
The adjacent workflow checks the new source hashes and both executions with
read-only permissions. A remote CI outcome belongs to the publication receipt,
not to a prediction in this README.
