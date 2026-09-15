# Split-Zero continuation: completion defects and original source kernels

Read [the complete proof](note.md). The parent inspected for this contribution is `ce8f784da8fb48aa19065c036cd815c05628cec4` on PR #2. The live anchored-period work and all earlier files are preserved. This directory makes no new numerical cycle-bound claim.

The original Collatz two-clock operator is `d = I-u*S`, where `S(V_n)=v^(a(n)-1)*V_T(n)` and only the fixed-point generator is removed relatively. Its completed inverse already exists in the research companion. The new calculation retains its exact defect:

```
original H^1  <-->  ker(d on completed primitives / polynomial primitives)
[q]          |-->  [sum u^j S^j q]
[d(g)]       <--|  [g]
```

Both inverse identities, support naturality, original relation submodules, and degree shift are proved. Every finite clock truncation is acyclic, but its original residual is retained explicitly. The source cohomology is recovered as a direct limit of the original S-action, with a constructive finite-terminal comparison.

A second result gives a complete basis and inverse decomposition for `ker(S^N)` on any declared finite span of original source vertices. It retains canceled vectors, their full source space, all original endpoint fibres, and actual clock coefficients. The original example is `S(v^2 V_3 - V_13)=0` from 3 -> 5 and 13 -> 5, not a deletion of those source labels.

Section 7.1 returns a cyclic infinite primitive through a specified rational subcomplex to the original integral forcing class:

```
[-N_p/(1-W_p)]  -->  [C(p)/D(p)]  -->  [C(p)] mod D(p).
```

It gives the coefficient maps, both chain maps, quotient inverses, and the exact obstruction to evaluating all completed series in that same arithmetic target. The full cyclic defect already lies in the rational subcomplex, so this restriction loses none of that defect. The 19-to-361 lifting failure is retained.

## Reproduce

From the repository root:

```sh
python -B collatz_reconstruction/research_program/completion_defect_20260914/replay.py
```

This verifies the source manifest and runs the new ordinary/optimized pair, requiring byte-identical output matching `verification.json`. The recorded pair has 7,928 named checks: 130 kernel presentations, 180 polynomial forcing fixtures, 512 original source jets, 340 arithmetic word fixtures, and 1,677 independently divided original paths, plus named controls and eleven rejected malformed certificates or inputs.

Examples:

```sh
python -B collatz_reconstruction/research_program/completion_defect_20260914/completion.py kernel 3 5 13 --returns 1
python -B collatz_reconstruction/research_program/completion_defect_20260914/completion.py source 27 --cap 8
python -B collatz_reconstruction/research_program/completion_defect_20260914/completion.py source 27 --cap 40
```

The first source-27 command retains its nonzero original residual. The second supplies its 41-return polynomial primitive. No finite nonzero residual is labelled an infinite orbit.

The new workflow separately runs the inherited `anchored_defect_20260914/replay.py` and this replay. A local new-pair pass is not itself a claim about that remote workflow; the publication receipt reports observed GitHub results.

## Source status

`SOURCE_INTAKE.json` pins the Split-Zero kernel construction and the current Collatz source. `TASK_STATE.md` records the exact continuing question. The earlier local clocked-support package, its source database, and its 678-rise certificate are not silently imported here. The proof needed for this contribution is self-contained and the executable code has no dependency on that unpushed package.

The infinite statements have written proofs. The finite regressions are implementation evidence, not a proof that every original singleton eventually vanishes. No original positive counterexample, global Collatz proof, independent external mathematical review, or new Lean result is claimed.
