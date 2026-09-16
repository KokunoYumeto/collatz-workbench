# Publication notes — 16 September 2026

This edition publishes the supplied twenty-chapter collection together with the missing research-source additions. Previously published files are preserved except for the public-facing root overview. The dated original delivery is retained as a release asset. The current reading edition repairs the typesetting defects described below.

## Two small active-source amendments

The formulas R_*(n) and K_*(n) in the all-even note use k(n)=floor(log₂(n−1))−1 and therefore apply for positive odd n>1. The fixed root n=1 is handled separately. The publication copy makes that domain explicit. This clarification does not change the common-future families, finite search, or support proofs. The clarification is included in the current reading edition; it also applies to chapter 20 of the original archived anthology.

The standalone affine auditor now writes its JSON receipt with explicit UTF-8 bytes. The supplied version used text-mode newline conversion, which made a byte-for-byte replay comparison fail on Windows despite identical JSON values. The active source uses deterministic line endings, retaining the literal expected-byte comparison. This is a serialization repair, not a change to an arithmetic test.

The source hashes of these amendments are recorded in [AMENDMENTS.json](AMENDMENTS.json). The original delivery's manifests identify the original files, not the amended publication files.

## Corrected typesetting

The supplied Markdown-to-LaTeX conversion interpreted some unmarked caret expressions as Markdown superscripts spanning several mathematical terms. For example, the intended denominator `2^A-3^m` was typeset with `A-3` in one exponent. Explicitly delimited mathematical expressions were not the source of that conversion error. The current reading edition was rebuilt with those Markdown reinterpretations disabled and checked against the original mathematical notes. Original formulas and coefficients, rather than their corrupted typography, are retained. The regenerated source map and formula inventories document the reading edition; the unchanged original PDF, TeX and manifests remain in the source ZIP.

## What was checked for publication

The new proof was read at its stated scope, including ternary valuations, positive source progressions, exact path exponents, strict smaller-source comparison, the finite template search, support bounds, and integral chain identities. An additional model-based mathematical review is not independent external peer review.

Fresh ordinary and optimized checker runs report 87,989 checks per run. The separately implemented affine auditor reports 512 families and 24,180 affine equations. The published replay retains its negative controls and predecessor checks. Earlier large crossing ledgers remain accompanied by their original receipts; no new global crossing scan is claimed by this publication.

The package's manifest identities and the original predecessor-archive CRCs were verified. PDF checks cover the front matter, mathematical chapters, and the repaired formulas. The twenty included chapters are determined by the master TeX; historical duplicate chapter-numbering files remain in the original delivery.

## Repository and original archive

Research sources are in their original `collatz_reconstruction/research_program/` locations. The cumulative typesetting is under `editions/cumulative_20260916/latex/`. The chapter-index source links have been relocated to these public paths. The source ZIPs remain in the complete release download, avoiding duplicate large archive blobs in Git history.

Five newly restored historical workflows are manual-only, so publication does not automatically launch full historical scans and atlas rebuilds. The new all-even workflow is restricted to its relevant source paths. All existing workflows remain unchanged. Supplied workflow versions remain in the original archive.

The archive's `tools/verify_archive.py`, integration scripts, and historical receipts refer to the unpacked original delivery layout. They are supplied for that purpose, not as evidence of a new remote action. The current repository contains additional material beyond the cumulative ZIP.
