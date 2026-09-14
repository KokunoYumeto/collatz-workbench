# Clocks and First-Passage Measures in Tao's Collatz Theorem

A separate preprint draft by Kokuno Yumeto, developed through human--LLM collaboration. The existing Collatz workbench is not replaced by this paper.

## Content

The paper takes Tao's V7 as its baseline. It proves exact C/T/S clock identities, a finite-cutoff logarithmic sampling comparison, and a general summable first-passage transport theorem. From Tao's Proposition 1.11 it constructs limiting first-entry distributions for every threshold along one common input-scale sequence, with exact threshold compatibility and a quantitative bound for finite joint laws independent of the number of thresholds. The family retains its common-base parameter; independence from arbitrary different scale phases is not claimed. The original fixed-threshold and diverging-threshold orbit-minimum conclusions remain Tao's. Two Section 5 proof steps and a sufficient Section 6 reserve bound are made explicit. Obsolete-version comparisons are retained only in local audit history.

This is not a stronger orbit-minimum bound or an independent reproof of the entire Fourier--renewal argument. The paper does not infer that a sourced theorem is open merely because this draft does not reprove it. This is a working draft, not a public publication or submission.

## Build

The TeX project has no private or absolute input dependencies. From this directory, run:

```text
pdflatex -interaction=nonstopmode -halt-on-error -jobname=tao_clock_audit -output-directory=output/pdf main.tex
pdflatex -interaction=nonstopmode -halt-on-error -jobname=tao_clock_audit -output-directory=output/pdf main.tex
python certificates/check_finite.py
```

Create `output/pdf` first if the TeX distribution requires it. In the canonical Overleaf project 6a91f06e408dd545780c660f, this manuscript is `tao_preprint.tex` with its dependencies under `tao/`; pdfLaTeX is sufficient. Do not create a new project. This is a working author project, not a public publication.

The finite certificate uses only the Python standard library and exact rational arithmetic. Optimized `python -O` intentionally fails rather than silently disabling the checks. It certifies the listed finite identities, not the analytic theorem.

`MANIFEST.json` lists the portable files and their hashes. `source_manifest.json` gives bibliographic identities, exact editions, read loci, and source hashes, without reproducing protected source text. The `audit` directory contains local review records and is excluded from the portable source package. `output/pdf/tao_clock_audit.pdf` is the reader artifact.
