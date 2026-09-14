# Reader-facing exposition revision

The current user asked for mathematical exposition addressed to a publication
reader rather than an internal assistant-to-user audit memo.

Edited only `main.tex` and `sections/versions.tex` in the portable sources.
The abstract now leads with the clock, measure-transport, entrance-law, and
local-estimate results. The introduction explains the mathematical need for
each construction and states the analytic dependency on Tao's Proposition
1.11 in one compact paragraph. The human--LLM disclosure is concise and placed
with the computational materials at the end. It identifies ChatGPT 5.6 Sol,
Ultra mode, in Codex, as the user expressly requested; the model is not placed
in the author byline.

The final mathematical section now has the title "Reserve bounds and
threshold reductions", with mathematical subsection headings. The reserve
statement and proof, all displayed estimates, the source-specific
counterexample, and the source locators are retained. Attribution of the
larger reserve to Tao's own v7 revision remains explicit. The repetitions
about what the draft does not claim, internal workbench status, and prior
audit classifications have been removed from the manuscript.

The removed classification history remains recorded in `FINAL_REVIEW.md`:
fixed alpha shifts inside Landau notation are not source corrections;
`exp(O(L^(3/5)))` is already two-sided; a distinct failure state does not
exhibit a failing Collatz orbit. Removing that audit history from the reader
text does not retract or reverse those classifications.

No theorem, definition, hypothesis, displayed equation, or proof was changed
by this subagent. A direct exact-text comparison with the last verified
isolated package (`tmp/portable_check_53ezqvlb`) confirmed that the reserve
proposition, its proof, and all seven display-math blocks in
`sections/versions.tex` are unchanged. No novelty, independent human review,
full analytic reproof, or stronger orbit-minimum bound is asserted. During
the prose-edit action this subagent performed no build, manifest regeneration,
ZIP rewrite, PDF replacement, or remote operation. The root agent subsequently
rebuilt the combined reader-style revision after parallel edits to the other
sections.

## Closing clarity and typesetting edits

The root agent made two further edits in `sections/versions.tex`: a
`texorpdfstring` alternative for the mathematical subsection heading, avoiding
hyperref PDF-bookmark warnings, and explicit identification of the printed
partial expression `1-2^(-A_0)` and the corrected `1-2^(-A_0-1)`. The latter
removes ambiguity in "both partial sums"; the printed expression was checked
directly in v7 `collatz.tex`, Section 1.2, line 206. These are a bookmark fix
and an exact source clarification, not a new mathematical result.

The final prose of all six manuscript files was read for this follow-up.
The revised introductory claims are supported by the existing mathematical
statements and do not introduce a new theorem, rate, domain, or novelty claim.
The remaining distinctions about scale phases, first-entry versus stationary
laws, and failure mass describe the actual mathematical objects rather than
the internal audit workflow. No additional memo-like passage requiring a
source change was identified.

## Final isolated verification

Completed 2026-09-04 13:33:37 UTC. `audit/portability_receipt.json` records
PASS for the refreshed 13-entry ZIP, its exact membership and hashes, the
extracted verifier, and an independent build. Cross-references stabilized
after three pdfLaTeX passes, within a four-pass ceiling. The checker rejects
every final warning, including hyperref warnings, together with overfull,
underfull, and unresolved-reference diagnostics. No final diagnostic remained.

All 15 rebuilt pages have exactly the reference PDF's extracted text and page
geometry. The final package SHA-256 is
`a51c2243deee6a24f63a212045f7fb62b61bd5f24b77f8f2a7157c016ec4d728`
(28,916 bytes); the reference PDF SHA-256 is
`ad14a2c31c7cb4c11328fa237f6a987de06c016263551eb0ff894e988dcb000f`
(456,718 bytes). No portable source or remote file was changed in this
follow-up verification.
