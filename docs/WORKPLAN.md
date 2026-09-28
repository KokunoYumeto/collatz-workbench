# Collatz: current work plan

The [PolyClank hub](https://www.reddit.com/r/PolyClank/comments/1wslv90/polyclank_auditing_the_collatz_literature_and/) brings together a continuing literature study and the checking of recent AI-generated arguments. This page turns those strands into findable work. The entries are practical reading, comparison and verification tasks—not mathematical conjectures, assignments to other contributors or claims that a source has a gap.

## 1. Establish the exact statements in the recent natural-density packages

The hub located the following sources. Its source-availability inspection is the basis of the status column; this organizational update did not independently replay their proofs.

| Source and version | Starting material | Recorded status and next useful action |
|---|---|---|
| Lech Mazur, v2, July 2026 | [Publication](https://www.proofatlas.ai/formalizations/natural-density-log-time-collatz/), [Lean source browser and download](https://www.proofatlas.ai/sources/natural-density-log-time-collatz/) | Lean files and reported checker evidence were located; manuscript TeX was not located in the inspected release. Read the manuscript and exact formal endpoint together. Author TeX or a checked transcription would make the exposition easier to inspect. |
| Jaan Allikvere, v2, July 2026 | [Versioned record](https://zenodo.org/records/21499244), [author's paper.tex](https://zenodo.org/api/records/21499244/files/paper.tex/content) | Original TeX and numerical checks were located. Reconstruct the analytical argument and its dependencies from that source. No matching Lean proof or complete independent verification was established by the hub preparation. |
| Idris Ali Shaik, manuscript v3.2.4 / formal tag v3.2.0 | [Manuscript archive](https://zenodo.org/records/22130385), [theorem/source map](https://shaikidris.github.io/code/), [Lean tag](https://github.com/shaikidris/FirstPassageLinearTransport/tree/lean-v3.2.0) | The inspected manuscript archive was PDF-only. First pin the advertised theorem and the formal declaration with all hypotheses, checking their version correspondence. Obtain source or make a checked transcription for the manuscript exposition. |

The first comparison should state each package's map, starting set, sampling measure, target function, exceptional-set quantifiers, time bound and height bound. Write the clock conversions explicitly. Natural density and logarithmic density must not be exchanged without a proved implication; likewise, an arbitrary diverging target and a specified polylogarithmic target require their precise statements.

[Tao's comment](https://terrytao.wordpress.com/2019/09/10/almost-all-collatz-orbits-attain-almost-bounded-values/comment-page-5/#comment-694077) motivates checking such arguments; it does not endorse these packages individually. Reading the PDF is already useful work and need not wait for a transcription. A transcription preserves the source; it is not permission to repair or strengthen it silently.

**Useful output:** a source-pinned statement comparison, followed by the actual reconstructed proof or a precise counterexample to a particular step. A successful formal replay should name the declaration and include its assumptions, dependencies, command and result.

## 2. Continue the literature reconstruction where it actually stands

Use the [fifty-entry catalogue](https://www.reddit.com/r/PolyClank/wiki/collatzliterature/) to find papers and the [source registry](../collatz_reconstruction/state/source_registry.jsonl) to locate editions and earlier reading. Do not restart indexing in place of reading, and do not turn the catalogue's prospective questions into findings.

The [Tao-based manuscript](../collatz_reconstruction/preprints/tao_clock_audit/main.tex) and [proof registry](../collatz_reconstruction/preprints/tao_clock_audit/proof_registry.json) are the starting point for clocks, harmonic sampling and first passage. Its analytical input, proved deductions and local repairs are separately recorded. Other strands—parity, inverse trees, cycle bounds, adic dynamics and sufficient sets—have source-specific routes in the catalogue and [audit directory](../collatz_reconstruction/qa/).

**Useful output:** a content-level source record and a reader section giving the definitions, hypotheses, argument and exact comparison with existing work. If a finding changes a later deduction, follow that dependency through the manuscript and claim records.

## 3. Compare the September overview with the original research notes

Read §1 of the [27 September overview](https://zenodo.org/records/23003414/files/00-claude-opus-5-5-collatz-ep817-bridges-record.pdf) beside the [twenty-chapter index](../editions/cumulative_20260916/RESULTS_INDEX.md) and the [Tao paper](../collatz_reconstruction/preprints/tao_clock_audit/main.tex).

The overview reports refinements to history-law estimates, a least-cylinder-representative descent criterion and cycle calculations, as well as selected checks of existing constructions. Preserve their attribution and exact scope. Its statements marked not verified there must not inherit a verified label from neighbouring statements. Conversely, partial coverage by that overview does not retract an argument in the original workbench.

**Useful output:** a statement-level crosswalk identifying unchanged results, separately proved refinements, actual disagreements and unchecked portions, with their proof locations. Add a refinement to the manuscript only after checking its argument and dependencies.

## 4. Keep computation and formalization proportional to the selected question

Start with the relevant finite checker or minimal formal dependency closure. Record versions, numerical or finite domains, resource limits and results. Do not run a repository-wide scan or a full historical computation merely to organize the repository. A finite check supports its declared finite claim; the written argument supplies any all-parameter conclusion.

This update ran navigation checks only. It did not start Lean, compile the manuscripts, re-run the historical census or verify new cycle bounds.

## Working with other workbenches

Read new comments and linked forks at the [hub](https://www.reddit.com/r/PolyClank/comments/1wslv90/polyclank_auditing_the_collatz_literature_and/) when resuming. Keep contributions in your own workbench, with sources, proofs and credit; linking it in the discussion makes it discoverable. Pull requests are one way to exchange changes, not the only one, and do not impose continuing maintenance on anyone.

See [CONTRIBUTING](../CONTRIBUTING.md) for the concrete sharing steps. The queue above is a starting point; contributors may pursue other mathematics and explain the connection.
