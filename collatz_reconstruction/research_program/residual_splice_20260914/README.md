# Residual-source continuation: exact tails, splicing, and integral cycle blocks

**14 September 2026.** Continues issue #3 and PR #2 of `KokunoYumeto/collatz-workbench`, from the authenticated checkpoint `32b8f3b9cc6dcfc4387ff783c4f4a6f6a365f717`. No imported source or historical receipt is rewritten. This is a reviewable research contribution, not a proof of the full Collatz conjecture.

Read **[the main proof](note.md)** and **[the integral block comparison](integral_blocks.md)**. **[Task state](TASK_STATE.md)** records the remaining source calculation. The executable source uses only the Python standard library and the unchanged adjacent predecessor.

## What changed mathematically

The continuation compiles the entire first-descent fiber of an actual exponent word, preserving its original source and target progressions, affine offset, parameter interval, and every original edge. It then proves an unbounded last-exponent rule: after a specified noncontracting prefix, all exponents above an explicitly computed threshold are a certified descent family. Their source is one arithmetic progression; every actual exponent is recovered from its parameter. This replaces an exponent-overflow case by an exact finite next-step partition plus a proved whole tail, without asserting that the infinite-depth frontier is empty.

For example, every `11+32v`, `v>=0`, has first descent under the original word `(1,2,2+v2(10+27v))`. The exact 37-return family `27+2^60 t -> 23+900567811781994726 t` adds a source family rejected by the old reference-3 stopping test at that word. Root-level splicing attaches these paths to the previous retraction; both compositions with the old projection and the chain homotopy are proved. Every actual cycle chain remains literally unchanged, and the degree-zero component obstruction remains represented.

The integral block equivalence has explicit maps, integral inverse matrices, and both homotopies. The affine inverse includes its forcing correction. It therefore retains the original prime-power obstruction, not just rational solvability: the control word `(1,1,2,4,3)` has 19 solutions modulo 19 and none modulo 361 before and after compression.

A finite source-certificate feedback loop closes four period windows. Its final 49,889 actual descent certificates prove convergence for all odd sources at most 99,779 by strong induction. The resulting exact integer period comparisons exclude **every nontrivial positive cycle with at most 402 exponent-1 positions in its primitive odd-return word, at every length and with all exponents allowed**. This extends the present workbench's previous exclusion; it is not advertised as exceeding published cycle bounds. All original forcing, period, positivity, and word conditions remain attached to the unexcluded sector.

## Reproduce from the repository root

```sh
python -B collatz_reconstruction/research_program/residual_splice_20260914/replay.py
```

This checks the new source manifest, replays all six unchanged predecessor executions, and runs the new verifier in ordinary and optimized Python. Both new outputs must match the committed `verification.json` byte-for-byte. It never updates a source or result file.

To inspect the exact finite next-step partition of the prefix `(1,2)`:

```sh
python -B collatz_reconstruction/research_program/residual_splice_20260914/tail_descent.py 1 2
```

To regenerate only the new result:

```sh
python -B collatz_reconstruction/research_program/residual_splice_20260914/verify.py --output /tmp/collatz-residual-result.json
```

The current result records **964,104 named exact checks**, 340 small word fixtures, 360 block fixtures, 5,175 compiled first-descent cells, 4,011 unbounded tails, and 14 rejected invalid inputs. The first-coefficient-crossing scan has exponent-sum bound 18. The seed budget is 100,000; unresolved sources and the next period window are retained. These are execution scopes, not claims of exhaustive all-source coverage or independent external mathematical review.

## Preservation and provenance

The local input was the previously published 25-file contribution archive, not a newly cloned full repository. The GitHub connector supplied the current branch/PR/issue state, the exactness-method chapter, and source identities. The original cycle note's computed Git blob matches the authenticated blob `9ccb58df9c05f2f156234ee6af8dad4e616135f7`; all 21 frozen payload identities and all six original replays passed before extension. No unpushed Codex session was read. The present added workflow has read-only contents permission and does not publish or merge research automatically.

The two proof files credit the exact predecessor and the inspected primary literature. Published first-passage, affine, and cycle mechanisms are not claimed as newly discovered. No external computational record, numerical cycle bound, or coefficient-stopping conjecture is assumed as a premise. Multiple sessions by the same operator are not independent reviewers.

Repository publication status and the completed head's CI outcome belong to the PR comment and publication receipt, not to a predicted commit in this file. The original `main`, PR #1, Zeta repository, and prior payload are outside this additive edit.
