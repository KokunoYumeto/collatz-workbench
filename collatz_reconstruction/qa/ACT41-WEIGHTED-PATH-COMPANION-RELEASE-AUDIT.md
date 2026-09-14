# ACT41 weighted-path companion release audit

**Recorded:** 2026-08-29T18:28:48.9451720Z  
**Predecessor:** `ACT-COL-000040`  
**Scope:** harden the two finite certificates, make the portable package
fail closed, link its TeX source to its declared PDF by an isolated
deterministic rebuild, and perform fresh artifact QA.  This record does not
claim completion of the wider Collatz corpus.

## Source and certificate state

The core certificate
`certificates/chatnotes_weighted_path_finite_actions.py` is 21,940 bytes with
SHA-256
`bec5327bcec769fae4333827b566bd631941ec38b657c1205da2bf18502667e4`.
The portable certificate
`research_companion/certificates/finite_actions_checks.py` is 19,527 bytes
with SHA-256
`7c231230c01b1f957a289169e771b68670cfaca7d228c43b6617ab71afae71af`.

Both certificates now reject optimized Python before executing assertions.
Normal runs pass.  The bounded source-fibre test enumerates all 837,930 odd
residue classes modulo (2^{A+1}) over the 340 words with lengths 1--4 and
letters 1--4, in addition to the 340 fibre-period checks.  The core run
reports 22 check families and the portable run reports 22 check families.
`python -O` and `PYTHONOPTIMIZE=1` both terminate nonzero with the explicit
fail-closed diagnostic for each certificate.

## Portable package

`research_companion/MANIFEST.json` declares seven source files and the output
`research_companion/output/pdf/collatz_research_companion.pdf`.  The manifest
currently records the output as 451,552 bytes with SHA-256
`ff7b8f06f2d4feecd42355ad46862f3e36707ed0fad2c4046f9206da81fcb814`.
The package validator reports:

```text
status=PASS
manifested_source_files=7
tex_files=3, labels=44, references=24, citations=4
finite_certificate_check_families=22
```

The validator now rejects optimized Python, scans Windows drive paths,
UNC paths, and private POSIX roots, and inventories every file under
`output/pdf/` except the one declared output.  A temporary extra output file
was detected as an inventory mismatch and then removed at its exact fixture
path.  The path checks recognize `C:\secret.txt`, `C:\Users\...`,
`\\server\share\...`, `/root/...`, `/tmp/...`, and `/mnt/...` while leaving
ordinary HTTPS URLs admissible.

For source-to-PDF linkage, the validator runs two isolated `latexmk` builds
with `SOURCE_DATE_EPOCH=1788026400`, `FORCE_SOURCE_DATE=1`, and `TZ=UTC`.
MiKTeX gives each build a producer-controlled trailer ID; the validator
canonicalizes only that ID and the producer-controlled creation/modification
date fields for comparison, then requires the two canonical rebuilds and the
declared PDF to be byte-identical.  The final output was rebuilt under the
same fixed environment and given the canonical trailer ID.  No build log is
part of the portable package.

`python -O research_companion/validate_package.py` and the same invocation
with `PYTHONOPTIMIZE=1` both fail before a PASS result.

## PDF build and content QA

The working corpus output is 155 pages, 1,470,772 bytes, SHA-256
`1b15dca83a64878c64c7b086a97b9b0bf7c3fc8f0788cf1b1a2bc4091bbbf7ba`.
Its clean build has zero fatal, undefined-reference, overfull, or actionable
diagnostics; six underfull boxes are source-register line-breaking warnings.
All 27 font rows are embedded, subset, and Unicode-capable.  Its 155 page
renders at 160 dpi are in `tmp/qa/act41_working_all_160dpi`, with 13 visible
8-bit contact sheets in `contact_sheets8`; page PNG aggregate SHA-256 is
`77cc2095fb46404e813e5ece857b8c66488aeab2772b7250a00cc0a4ef4fe871` and
contact-sheet aggregate SHA-256 is
`8b9d88534554d0f4a9ce22e444f9c3c470bdf1bdbfd2a5843920a3a417339de1`.
All 13 sheets were inspected at original detail, and pages 131--155 were
also checked individually.

The separately authored companion output is 18 pages, 451,552 bytes, with
SHA-256
`ff7b8f06f2d4feecd42355ad46862f3e36707ed0fad2c4046f9206da81fcb814`.
Its deterministic build has zero fatal, undefined-reference, overfull, or
actionable diagnostics; one underfull bibliography box is cosmetic.  All 21
font rows are embedded, subset, and Unicode-capable.  Its 18 page renders at
200 dpi are in `tmp/qa/act41_companion_final_200dpi`, with three visible
8-bit contact sheets in `contact_sheets8`; page PNG aggregate SHA-256 is
`ea17a7ca5237954d9aa98179007741b201b43ea277ee50f6ab5ad81be3c11bd3` and
contact-sheet aggregate SHA-256 is
`ec71464de85fee1583aa4a651b18d01917d463744cceed162dbb6aef82a752c4`.
All three sheets cover all 18 pages and were inspected at original detail.
The new companion page renders are byte-identical to the prior 18-page
render set, so the fixed-date/trailer repair changes no page content.

`pdfinfo`, `pdftotext`, and `pdffonts` checks found the declared page counts,
letter geometry, no `??`, `operatorname`, `codex://`, `mathscr`, or private
machine-path leakage in extracted text, and no unembedded or non-Unicode font
rows.  Visual inspection found no blank insertion, clipping, overlap,
displaced folio, broken glyph, malformed display, or terminal fault.

## Fresh-context recovery

After the state edit, a new Python process read only the external state,
checked the active goal and ACT41 checkpoint, verified both PDF hashes, and
reran both certificates plus the package validator.  All three subprocesses
returned JSON `status=PASS`; the complete transcript and exact recovery
checks are recorded in `qa/ACT41-FRESH-CONTEXT-RECOVERY.md`.

## Status and next route

The weighted odd-step path programme is sealed at its proved scope: the
decorated-prefix representation is faithful, while finite-residue forward
and pullback representations have the stated explicit kernel element and
typed fibre criterion.  These are independent companion results, not an
enlargement of a source author's theorem.  The wider literature-first
Collatz reconstruction remains active; residual Chatnotes, Gemini material,
archived tasks, unresolved source dependencies, and any future Lean work stay
outside this release checkpoint.  No Git command, Lean/Lake process,
`AGENTS.md` write, upload, publication, or public-record mutation occurred in
this audit.
