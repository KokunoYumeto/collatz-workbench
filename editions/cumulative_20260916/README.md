# Collatz: arithmetic histories, integral comparisons, and bounded-support reductions

[Read the cumulative volume (PDF, 237 pages)](latex/main.pdf) · [Chapter and source index](RESULTS_INDEX.md) · [Editable LaTeX](latex/main.tex) · [Complete original delivery](https://github.com/KokunoYumeto/collatz-workbench/releases/tag/cumulative-2026-09-16)

This collection contains twenty full mathematical chapters on actual Collatz histories, exact arithmetic transport, integral first-jet constructions, and explicit common-future comparisons. It brings together the supplied continuation notes and their proofs, code, finite certificates, and source history. The critical exposition of Maxwell C. Siegel and the separate Tao first-passage paper remain distinct works in the [main workbench](../../README.md).

## The all-even continuation

The [current proof and implementation](../../collatz_reconstruction/research_program/all_even_join_extension_20260916/note.md) extend two common-future templates to every positive even interior exponent. For an even exponent e, the quantity h_e=(2^e+2)/3 has exact ternary valuation ν₃(h_e)=ν₃(e−1). This determines the correct source layer and makes the template search finite for each positive odd input. Both original paths and every intermediate vertex are retained.

One complete family, for every integer v≥0, is

```
n = 20,241,207 + 1,549,681,956 v
m = 14,024,703 + 1,073,741,824 v
y = 30,361,811 + 2,324,522,934 v

n --(1)--> y <--(sixteen 1s, 8, 2, 3)-- m,    0 < m < n.
```

The labels are the exact powers of two removed in successive odd returns. This is a comparison through a common future, not a claim that forward iteration from n visits m. Every n in this progression survived the preceding comparison rules; the new rule supplies an additional, fully specified reduction.

The budget-preserving extension keeps the original support bound

```
R₀(n) = max{130(n+1), floor[64n(4/3)^floor(log₃ n)] + 21}.
R₀(n) ≤ 64 n^(log₃ 4) + 21  for n ≥ 27.
```

It does so by checking both actual paths before accepting a comparison. The unrestricted version has its own larger bound. These are bounds for the supports of the constructed integral chain columns, not universal Collatz stopping-time bounds. Sources to which no accepted rule applies remain explicitly represented.

## Reading and verification

The first chapters develop history laws, stopped affine transport, cycle-relative cohomology, and supported integral defects. The later chapters construct arithmetic reductions while preserving the residual classes and their clock data. The final chapter supplies the all-even extension.

The publication review reran the new checker and its separately implemented affine auditor. The checker reports 87,989 exact checks per run; the auditor checks 512 family fixtures and 24,180 affine-coefficient equations. Ordinary and optimized executions agree. These bounded calculations accompany the all-parameter written arguments; they are not a verification of all Collatz orbits. [Publication amendments and verification scope](PUBLICATION_NOTES.md) distinguish this review from the historical receipts.

From the repository root:

```sh
python -B collatz_reconstruction/research_program/all_even_join_extension_20260916/replay.py --predecessor
```

The complete original ZIP is a release download. It includes all fourteen predecessor archives and their full ledgers. Its SHA-256 is `069406d1ee543720eeb0ceeddb15d600a32aa03fc60734c504eb8bbfa091771b`. The editable volume and browsable research sources are also available directly in this repository. The ZIP's original manifest and archive-verification commands apply to the unpacked original delivery, not to this repository's reorganized publication paths.

## Collaboration and attribution

This is a PolyClank human–LLM research workbench under the public collaboration name **Kokuno Yumeto**. Contributions were developed with **ChatGPT 5.6 Sol, Ultra mode, in Codex**, and **GPT-6 Astra**. The workbench keeps the mathematical arguments, reproducible calculations, corrections, and source relationships available for further scrutiny and extension. Existing literature retains its authors' attribution; model participation is recorded as provenance.

The supplied PDF and LaTeX are preserved in the dated source archive. The current reading edition repairs formula-typesetting errors and includes the domain clarification documented in the publication notes. This publication does not assert a proof of the Collatz conjecture, a complete formalization, or independent external peer review.
