# Hydra Maps, Numens, and `(p,q)`-Adic Analysis

This archive is the self-contained LaTeX source release for *A Critical
Expository Edition of the Mathematical Work of Maxwell C. Siegel*.

The mathematical source works and Siegel's terminology remain attributed to
Maxwell C. Siegel. The critical apparatus, typed reconstructions,
counterexamples, and edition-supplied proofs are identified as editorial
work rather than source text.

## Contents

- `critical_expository_edition/`: the build-complete 13-file LaTeX tree;
- `apparatus/CLAIM_LEDGER.jsonl`: 192 atomic claims with hypotheses,
  provenance, dependencies, checks, and exact status;
- `apparatus/release_document_index.jsonl`: the 16 source records cited by
  the claim ledger, with public identifiers where established;
- `scripts/verify_release.py`: the fail-closed portable integrity and
  structural verifier;
- `qa/`: portable claim-closure and release-verification receipts;
- `RELEASE_METADATA.json` and `MANIFEST.sha256`: release identity and exact
  file hashes.

The bibliography is contained in `chapters/11_source_register.tex`. The TeX
build has no external image, bibliography, data, or source-file dependency.

## Verify first

From the extracted archive root, run:

```text
python scripts/verify_release.py
```

The verifier requires the exact release whitelist and hashes, validates both
JSONL apparatus files against their schemas, checks contiguous claim IDs and
the acyclic dependency graph, resolves every ledger document ID and version
against the bundled document index, resolves every ledger TeX path and label
against the bundled TeX tree, audits TeX labels/references/citations, and
rejects undeclared archive files, absolute paths, and ledger path locators
outside the bundled TeX tree. It prints one compact JSON result and exits
nonzero on any failure.

The tested apparatus environment is Python 3.13.9 with `jsonschema` 4.26.0.

## Build the PDF

The tested TeX environment is Latexmk 4.88, MiKTeX-pdfTeX 4.27 (MiKTeX
26.5), and LaTeX2e 2025-11-01. A normal pdfLaTeX installation needs the
following direct packages or classes:

`amsart`, `fontenc`, `inputenc`, `lmodern`, `geometry`, `amsmath`, `amssymb`,
`mathtools`, `mathrsfs`, `booktabs`, `longtable`, `array`, `tabularx`,
`enumitem`, `microtype`, `xurl`, `hyperref`, and `cleveref`.

PowerShell:

```powershell
$env:SOURCE_DATE_EPOCH = "1787529600"
$env:FORCE_SOURCE_DATE = "1"
New-Item -ItemType Directory -Force build | Out-Null
Push-Location critical_expository_edition
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=../build main.tex
Pop-Location
```

POSIX shell:

```sh
export SOURCE_DATE_EPOCH=1787529600
export FORCE_SOURCE_DATE=1
mkdir -p build
cd critical_expository_edition
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=../build main.tex
cd ..
```

The expected output is a 76-page PDF 1.5 on US-letter pages (`612 x 792`
points), with the title and author metadata recorded in
`RELEASE_METADATA.json`.

## Reproducibility boundary

The frozen source reproduces the PDF text, metadata, page geometry, and every
page raster. The PDF trailer identifier may vary when the build path changes,
so a clean rebuild can have a different binary SHA-256 while remaining
content-identical. The separately delivered stable PDF has its own exact hash
in `RELEASE_METADATA.json`.

## Claim statuses

The ledger separates verified source statements, corrected results, prior-art
overlap, conditional statements, heuristic statements, contradictions, and
unresolved obligations. Conditional, heuristic, contradicted, and unresolved
records are not available as positive theorems. The exact status counts and
all conditional, heuristic, contradicted, and unresolved IDs are in
`qa/claim_ledger_closure.json`.
