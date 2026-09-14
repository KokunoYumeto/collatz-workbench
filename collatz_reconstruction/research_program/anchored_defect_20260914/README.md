# Anchored defects, ordered cycle periods, and complete excess-sector certificates

Continuation in `KokunoYumeto/collatz-workbench`, 14 September 2026. Source commit: `6a30f1dc23110fae0abbe3b3bd5e60072a842385`, PR #2. All 36 inherited contribution files remain unchanged. The persistent research thread is issue #3.

Read `note.md`, then `turns_and_unit_excess.md`. `morphisms.jsonl` indexes the exact maps and their proof locations. The user's technique is Split-Zero cohomology and the related support-preserving exact-map method; no speech-to-text acronym is adopted.

The construction x -> x-1 has inverse y -> y+1 and preserves the original integral forcing class by the exact boundary identity b=1-B1. Its primitive produces the original-edge factor eta(n)=2^a(T(n)-1)/(3(n-1)). Exponent-2 forcing is a supported zero, not an absent row. Entry into 1 produces a supported zero period factor; the fixed loop at 1 retains its undivided zero equation, without assigning 0/0 a value.

The cycle period is exactly 2^A/3^m. Its positive factor bound depends on the original exponent-1 positions. Adjacent high-exponent/1 turns have the exact paired factor 1+(12-2^b)/(3*2^b*n-12). This gives a sharper ordered-turn bound, with the original two-edge path and intermediate vertex retained.

Two complete finite sectors are discharged. The 403-rise sector has 14564 possible minima after its anchored ceiling and exact modulo-12 restriction; every source descends or exits the required {1,2} alphabet. The 404-rise sector has exactly one exponent 3. Its two possible incoming minimum edges give different retained residue classes, ceilings and prefix excess budgets. All 29199 possible minima are covered; every budget exit occurs within the justified first traversal. An excess exit is not a convergence certificate. Together these results exclude every nontrivial positive cycle with at most 404 exponent-1 positions at arbitrary lengths. The common convergence range stays the inherited odd-source bound 99779. No published cycle-record claim or global Collatz conclusion is made.

Run all ten executions (eight preserved and two new), including source hashes and ordinary/optimized byte comparisons, from the repository root:

```sh
python -B collatz_reconstruction/research_program/anchored_defect_20260914/replay.py
```

Materialize a complete proof tree, including its original word labels, empty branches and parameter maps:

```sh
python -B collatz_reconstruction/research_program/anchored_defect_20260914/anchored_cycles.py --full-cover --output cover-403.json
python -B collatz_reconstruction/research_program/anchored_defect_20260914/anchored_cycles.py --full-cover --excess-budget 1 --upper 275227 --residue 7 --output cover-404-incoming2.json
python -B collatz_reconstruction/research_program/anchored_defect_20260914/anchored_cycles.py --full-cover --excess-budget 0 --upper 274717 --residue 11 --output cover-404-incoming3.json
```

`verification.json` retains all three tree hashes, independent source-witness hashes, exact period comparisons, path examples and rejected false certificates. `verify.py` enumerates the original dyadic fibers independently of the generator's CRT inverse and separately interprets every candidate using repeated integer division.

The new read-only workflow also replays the inherited source. GitHub execution status belongs to the actual publication receipt and PR checks, not to this pre-publication source. No external independent review or Lean execution is claimed. The next exact arithmetic fiber and the still-unresolved ordinary-integer nonperiodic source are recorded in `TASK_STATE.md`.
