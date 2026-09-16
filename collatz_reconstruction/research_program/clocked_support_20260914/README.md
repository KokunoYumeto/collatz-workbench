# Clocked support continuation

Continuation against authenticated Collatz branch head `6a30f1dc23110fae0abbe3b3bd5e60072a842385` (PR #2). The inherited 36 contribution files remain byte-for-byte unchanged. This directory and its separate read-only workflow are additive. No current remote publication is assigned to this local handoff.

## Read

`note.md` contains the complete proofs. It starts with the original companion's weight `u^m v^(A-m)` and transfer operator, then constructs the marked cycle comparison, original integral specialization, component cokernel, completion maps and clocked retraction. The source corpus's existing path sums and formal inverse are credited rather than presented as discoveries of this continuation.

The universal cyclic mark is `N_p=sum u^j v^(A_j-j)`. Together with `W_p=u^m v^(A-m)` it has an explicit inverse to the original word. Specializing `u=2/3,v=2` gives the original B matrix with its exact factor -3 and the original forcing C. The cokernel localization preserves the integral obstruction because `gcd(D,3)=1`. Original integer coordinates, positivity and valuation labels remain required.

The complete actual-component formula separates the nonbase periodic summands `Z[u,v]/(1-u^m v^(A-m))` from the explicitly described torsion-free ray unions. Polynomial support, common finite vertex support after scalar completion, and coefficientwise finite support have exact comparison maps. The available completed inverse is not silently substituted for a polynomial contraction.

## New executed arithmetic

The reversible database covers all 165374 odd sources from 3 through 330749. It retains 13989 occupied first-descent words and two declared zero-count labels, (1) and (2,2). Its original word-ID decoder, affine chart inverses and every valuation are independently replayed. The actual witnessed graph has 262615 nonbase vertices and a nonnegative unit-cochain primitive of maximum 164. This gives a finite polynomial inverse on that graph with original clock weights retained.

The formerly retained 403-rise sector `(m,A)=(971,1539)` is closed. Exact source and integer period certificates exclude nontrivial positive cycles with at most **678** exponent-1 positions at every length. This is an internal workbench bound, not a published-record claim. The next retained 679-position sector is `(m,A)=(1636,2593)`, with minimum in `[330751,583287]`, 679 ones and 957 twos.

No universal Collatz proof, positive counterexample, proof-assistant execution or independent external mathematical review is claimed. The original infinite residual source remains.

## Reproduce

From the actual repository root:

```sh
python -B collatz_reconstruction/research_program/clocked_support_20260914/replay.py
```

This verifies the new and inherited source hashes, replays all eight inherited executions, regenerates and exactly compares the canonical source database, and runs the new suite in ordinary and optimized Python. The gzip file is a preserved transport container; cross-version regeneration compares its decompressed canonical JSON, not a compressor-dependent wrapper.

Individual tasks:

```sh
python -B collatz_reconstruction/research_program/clocked_support_20260914/verify.py --output clocked-check.json
python -B collatz_reconstruction/research_program/clocked_support_20260914/sector_certificate.py --check collatz_reconstruction/research_program/clocked_support_20260914/source_database.json.gz
```

The scripts use the Python standard library and the unchanged predecessor files. The new suite checks the polynomial maps, 364 word fixtures, actual original paths, clocked retractions, the missing-clock defect, the full source database, complete period comparisons and 12 malformed inputs. `verification.json` records each scope separately.

## Collaboration handoff

Read `TASK_STATE.md` before extending the source. Preserve original forcing, word order, support labels, source and image progressions, and the exact terminal clock in every new root splice. Continue either the next finite minimum interval or the original marked gap system; do not replace the infinite support-membership task with an already available formal inverse.

Research direction and source conventions belong to the Kokuno Yumeto workbench. This is a ChatGPT-assisted continuation, with written proofs and local exact execution, not an independent external audit. Source intake and the available read-only GitHub tool state are recorded in `SOURCE_INTAKE.json`.

For a separately recorded replay of the new pair after the inherited suite has already passed, append `--new-only`. This still checks every inherited file hash and regenerates the database. Its receipt explicitly reports zero inherited executions rather than claiming another inherited replay.
