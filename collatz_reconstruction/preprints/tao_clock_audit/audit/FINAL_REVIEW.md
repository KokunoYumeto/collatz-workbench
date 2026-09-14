# Local preprint release review

Latest delivery addendum, 2026-09-04 13:37:35 UTC: the revised 15-page
Tao preprint is uploaded and compiled in the one canonical Overleaf project.
The live build `1a06ca2a2d9-fa47409cb632f010` reports zero errors, warnings,
or other log items. The model disclosure was read in the compiled remote PDF.
See `../../overleaf/sync_20260904/reader_revision_remote_receipt.json` relative
to the preprint root, or the project-root locator
`overleaf/sync_20260904/reader_revision_remote_receipt.json`.
This supersedes the synchronization-pending statements in the dated local
checkpoints below. No new project, sharing change, or public publication was
performed during this revision; critical/companion sources were unchanged.

The first checkpoint below is preserved history. Its artifact hashes,
pagination, and manuscript descriptions apply at its stated time. The dated
reader-revision addendum at the end identifies the later verified release.

Recorded 2026-09-04 13:09:52 UTC. This records a verified local working draft,
not completion of the Collatz corpus reconstruction and not public publication.
The current user directive is `raw/USR-0015-canonical-overleaf-only.txt`,
relative to `collatz_reconstruction`. Its SHA-256 is
`7ef38dc207ef753c339fb642025df7f00af52a0aa0fed4ca120b89a9278d1710`.

## Exact artifacts at the 2026-09-04 13:09:52 UTC checkpoint

- `output/pdf/tao_clock_audit.pdf`: 16 pages, 458,611 bytes; SHA-256
  `0f853efabe384fef511ea02c70dbe3e057a53af3d9339085e945cc20f674d8a8`.
- `output/tao_clock_audit_source.zip`: 13 entries, 30,300 bytes; SHA-256
  `6c45feb172ac10414ad53be06c1065c5ff8709fb8cea4ef77cd94e0b9fea2106`.
- `main.tex`: SHA-256
  `2087b3710ac9d62a6a8361b3b69d085a6b1ae1bc0a120abb5e39c7862d3bbce5`.
- `MANIFEST.json`: SHA-256
  `43c40d835d9a6210049e6a93f1d0a8b90fbd523efa1fffb36fbf71033ab5cce0`.

These identities were checked directly from the current files for this record.
The README-only change for the authorized working Overleaf copy changed the
manifest and ZIP; it did not change any TeX source or the reader PDF.

## Mathematical scope verified against the current draft

The abstract, introduction, and concluding scope statement in `main.tex` and
`sections/versions.tex` were read directly for this record. They claim:

1. Exact identities relating the ordinary, division-counting, and odd-return
   Collatz clocks, together with finite harmonic-weight transport.
2. A summable first-passage transport theorem using a separate failure state,
   and a total-variation entrance-law limit along the specified scale sequence
   with quantitative error and compatible threshold projections.
3. A deduction of Tao's full fixed-threshold and arbitrary-diverging-threshold
   conclusions from his cited Proposition 1.11. The original quantifiers are
   retained; no stronger orbit-minimum bound is claimed.
4. Complete local Section 5 proofs of the multiplicative endpoint estimate
   and uniform coefficient bound. These completions preserve the conclusions
   they support.
5. An explanation of the author's own Section 6 reserve revision and a
   separation of genuine local source-display issues from harmless notation.

Tao's Fourier-renewal estimate remains a cited analytic input. The draft does
not claim to reprove the entire analytic first-passage argument, to establish
Collatz convergence, or to complete a historical audit of all Collatz
literature. The statistical architecture and tightness formulation retain
their attribution to Tao. The source-specific read loci and hashes are in
`source_manifest.json`; the finite dependency labels are in
`proof_registry.json`. This release record is not another mathematical audit.

## Classification corrections controlling subsequent use

The current `sections/versions.tex` explicitly supersedes these older audit
classifications wherever they occurred in prior working notes:

- At fixed alpha and c, the expressions
  `O((alpha^(j-2) log y)^(-c))` and `O((alpha^j log y)^(-c))`
  specify the same Landau estimate. Expanding the fixed multiplicative
  factor is not a source correction.
- `exp(O(L^(3/5)))` already supplies two-sided multiplicative control.
  Writing separate upper and lower estimates is an exposition or verification
  step, not evidence of a sign error.
- The larger retained Section 6 reserve in v7 is Tao's own revision of v5.
  The explicit reserve calculation in this draft explains its margin; it does
  not claim that this draft first supplied the revised reserve.
- A separately named failure state clarifies the typing and composition of
  passage maps. It does not exhibit a Collatz orbit that fails to pass.

These corrections are now recorded in the live preprint and this release
record before any further consequence is drawn from the old classifications.
The user's request to preserve the mathematical workbench was respected:
the preprint is separate, and the original workbench chapters were not
rewritten as part of this release. That preservation does not authorize
continued reliance on the superseded classifications.

## Verification performed

`audit/portability_receipt.json` records the isolated rebuild completed at
2026-09-04 13:05:44 UTC. All 13 ZIP members were safe, had exact expected
membership, passed CRC checks, and were byte-identical to the current authored
sources. The extracted `verify.py` succeeded: 12 source files, 48 TeX labels,
7 used bibliography keys, and 14 proof records. Its finite certificate passed
86,238 clock-segment checks, 256 harmonic cutoffs, 12,800 finite-map nested
passage checks, and 1,554 positive valuation words using exact arithmetic.
Those checks support the specified finite identities, not Tao's analytic
input or the limiting theorem by experimentation.

Two isolated pdfLaTeX passes succeeded. No rejected final TeX diagnostics
remained. All 16 rebuilt pages have exactly the same extracted text and page
geometry as the release PDF; byte equality is not required for metadata that
varies with compilation time. The root agent separately reported a fresh
direct inspection of all four contact sheets, covering pages 1 through 16,
and a visual PASS. The unchanged PDF hash above identifies that inspection.
This subagent did not substitute text extraction for visual inspection.

No Lean worker, Git operation, upload, or workbench TeX modification was
performed by these portability and local-release-record actions. The earlier
review agents supplied separate LLM-assisted checks; they are not described
as independent human peer review.

## Canonical Overleaf destination and unfinished delivery action

Use only https://www.overleaf.com/project/6a91f06e408dd545780c660f . The critical
edition, research companion, and Tao preprint must remain distinct TeX entry
files within this one project. Do not create a new project. The user deleted
the separate Tao project `6a9ac23b455ee99da3ad98f3`; that identifier is inactive
history, not a destination, and the project must not be recreated.

At this local release checkpoint, canonical-project synchronization and remote
compiled-output verification remain pending. This record does not claim that
the user can already inspect the updated preprint there. A later live service
receipt must establish that fact. Do not change sharing permissions or publish
publicly. The broad corpus goal remains active and incomplete.

## Reader-revision release addendum: 2026-09-04 13:36:20 UTC

The controlling reader-style and model-attribution request is now
`raw/USR-0016-preprint-reader-and-model.txt`, read directly for this addendum.
Its SHA-256 is
`297af33aac959129c12f18c202231655de15193d5417f10f5416257b146eb7dd`.
The canonical-project restriction in USR-0015 remains in force.

The manuscript has been revised for a mathematical reader. The abstract and
introduction lead with the clock identities, transported measures, limiting
first-entry laws, and estimates; the analytic input is identified as Tao's
Proposition 1.11. Internal workbench history and repeated defensive
claim/nonclaim narration have been removed from the reader text. Their
substantive classifications remain in this audit record, including the
Landau-notation and two-sided-exponential points above. Tao's own v7 reserve
revision remains explicitly attributed in the manuscript.

The concise closing computational-assistance note identifies **ChatGPT 5.6
Sol, Ultra mode, in Codex**, with its source-comparison, proof-development,
and computational-checking roles. The human author byline remains Kokuno
Yumeto. No model name has been added as an author. Exact theorem hypotheses,
proofs, and analytic dependency have been retained. A final source clarification
names the printed and corrected finite partial expressions explicitly;
the mathematical subsection heading also has a plain-text PDF bookmark.
`audit/reader_style_revision.md` records those editorial actions and checks.

### Current standalone release identities

The following identities were checked directly from the current files:

- `output/pdf/tao_clock_audit.pdf`: 15 pages, 456,718 bytes; SHA-256
  `ad14a2c31c7cb4c11328fa237f6a987de06c016263551eb0ff894e988dcb000f`.
- `output/tao_clock_audit_source.zip`: 13 entries, 28,916 bytes; SHA-256
  `a51c2243deee6a24f63a212045f7fb62b61bd5f24b77f8f2a7157c016ec4d728`.
- `main.tex`: SHA-256
  `328f160e473d4e3b196d149ef03f950194710f3fa29b1ff8b22c322d21202298`.
- `MANIFEST.json`: SHA-256
  `a40dae1bd6bc8568faa12ae5a364e867f069d53a019c43d52c9054180bbe2b22`.

These replace the earlier checkpoint identities as the local release under
review; the earlier identities remain historical evidence, not current file
hashes.

### Verification of this revision

The current `audit/portability_receipt.json` records PASS at
2026-09-04 13:33:37 UTC for an isolated extraction of the current ZIP. Exact
membership, safe paths, member hashes, and CRC checks passed. The extracted
verifier again checked 12 authored source files, 48 TeX labels, 7 cited
bibliography keys, and 14 proof records, with the same exact finite-certificate
counts recorded above. Cross-references stabilized after three pdfLaTeX
passes, within the checker's four-pass ceiling. Every final warning is
rejected, including hyperref warnings, together with overfull, underfull,
and unresolved-reference diagnostics. The final diagnostic list was empty.

All 15 rebuilt pages have exactly the current standalone PDF's extracted text
and page geometry. The root agent also directly inspected all 15 final pages
in `tmp/pdfs/ad14a2c31c7cb4c1` and reported PASS: no clipping, overlap,
unresolved references, or malformed mathematical layout. The current
`audit/release_receipt.json` records that visual result. Text comparison is
not being substituted for the root's visual inspection.

### Delivery state at this addendum

Uploading the revision into the sole canonical project
https://www.overleaf.com/project/6a91f06e408dd545780c660f is underway.
The remote compiled result has **not yet been verified at this checkpoint**;
this addendum therefore makes no delivery claim. The root agent will append
the live service receipt after checking the uploaded files and compiled
output. No new project, public publication, or sharing-permission change is
authorized. The critical edition and research companion remain distinct
from this preprint within that project, and the original mathematical
workbench remains preserved. The broader corpus goal is still active and
incomplete.
