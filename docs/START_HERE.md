# Collatz workbench: where to start

## Natural-density arguments: clocks, height and source comparison

The [30 September reconstruction](../collatz_reconstruction/research_program/natural_density_audit_20260928/README.md) connects the timed almost-boundedness argument to a height-controlled prefix of the same Collatz orbit. For every diverging target f(n), the written synthesis reaches a value below f(n) on a natural-density-one set with odd, shortcut and ordinary clock bounds j log(n)/log(4/3)+O(log(n)^(4/5)), j=1,2,3, and ordinary height at most n^(1+beta), for every fixed beta>0. It includes the quantitative fixed-target exception count, complete proofs, source attribution and exact path checks.

The source comparison covers Tao v7, Allikvere v2, Mazur v2 and selected Shaik arguments, and credits Inselmann's earlier drift envelopes. The package separates written analytic proofs, finite regressions and five narrowly scoped Lean certificates. It is not a full formal validation of the source packages or a claim to solve Collatz. Read the current [168-page PDF](../collatz_reconstruction/research_program/natural_density_audit_20260928/audit.pdf) and [LaTeX source](../collatz_reconstruction/research_program/natural_density_audit_20260928/audit.tex). Earlier PDFs elsewhere retain their own dates.


This workbench studies Collatz dynamics through the literature and through new proofs, constructions and computations. Its two current PolyClank strands are the continuing literature reconstruction and the examination of recent natural-density arguments. The manuscripts below contain the mathematics; this page connects them without treating a catalogue entry or an AI review as a completed proof check.

[PolyClank discussion and other contributors' workbenches](https://www.reddit.com/r/PolyClank/comments/1wslv90/polyclank_auditing_the_collatz_literature_and/) · [Fifty-entry literature catalogue](https://www.reddit.com/r/PolyClank/wiki/collatzliterature/) · [Current work plan](WORKPLAN.md) · [How to contribute](../CONTRIBUTING.md)

## A reading route

Start with the question that interests you. The rows are connected strands, not competing descriptions of one theorem.

| Question | Start here | Then follow |
|---|---|---|
| How do the different Collatz clocks and sampling measures fit together? | [Clocks and First-Passage Measures in Tao's Collatz Theorem: PDF](../collatz_reconstruction/preprints/tao_clock_audit/output/pdf/tao_clock_audit.pdf) | [Editable source](../collatz_reconstruction/preprints/tao_clock_audit/main.tex), [claim-by-claim dependencies](../collatz_reconstruction/preprints/tao_clock_audit/proof_registry.json) |
| What has the literature reconstruction established or corrected? | [Working critical reader: PDF](../collatz_reconstruction/output/pdf/collatz_working_corpus.pdf) | [TeX](../collatz_reconstruction/tex/main.tex), [source editions and coverage](../collatz_reconstruction/state/source_registry.jsonl), [source-specific audits](../collatz_reconstruction/qa/) |
| What is in the independent research collection? | [Twenty-chapter source index](../editions/cumulative_20260916/RESULTS_INDEX.md) | [Cumulative PDF](../editions/cumulative_20260916/latex/main.pdf), [verification and amendments](../editions/cumulative_20260916/PUBLICATION_NOTES.md) |
| What does the spectral history encoding actually encode? | [Split Zero / Collatz note: PDF](../collatz_reconstruction/research_program/split_zero_history_20260913/note.pdf) | [Source and checker](../collatz_reconstruction/research_program/split_zero_history_20260913/), then the supported-cohomology chapters below |
| Where are weighted paths, survivor coding and arithmetic groupoids developed? | [Separate research companion: PDF](../collatz_reconstruction/research_companion/output/pdf/collatz_research_companion.pdf) | [Source and evidence](../collatz_reconstruction/research_companion/) |
| What is the source-faithful treatment of Maxwell C. Siegel's work? | [Critical-expository edition: PDF](../maxwell_siegel_research/output/pdf/maxwell_siegel_critical_expository_edition.pdf) | [Portable source edition](../siegel_edition/); independent deductions remain separately attributed |

### The Tao-based paper

Tao's theorem concerns orbit minima for logarithmically almost all starting integers. The separate workbench paper uses his v7 Proposition 1.11 as its analytical input and develops exact clock conversions and first-passage transport.

Its additional distributional conclusion is a compatible family of limiting first-entry laws at every threshold, obtained along one common sequence of input scales. Finite joint laws have a quantitative error bound independent of the number of thresholds. This provides a way to follow distributions through successive descents while retaining the actual clocks and harmonic sampling weights.

The [proof registry](../collatz_reconstruction/preprints/tao_clock_audit/proof_registry.json) separates that deduction from the cited analytical theorem, local proof-text repairs and finite checks. The paper does not claim a stronger orbit-minimum bound or an independent reproof of the entire Fourier–renewal argument. Begin with the v7-based manuscript; the v5 comparisons are source history, not the organizing premise of the paper.

### Navigating the twenty-chapter collection

The [chapter index](../editions/cumulative_20260916/RESULTS_INDEX.md) links every complete note to its editable LaTeX chapter.

- **Chapters 1–2: history laws and stopped affine transport.** These connect distributions of actual finite orbit histories to exact counting and to arithmetic maps at stopping times.
- **Chapters 3–11: cycles, clocks and supported integral constructions.** These introduce the orbit-graph and cohomological objects, retain finite-support data, and examine what passage to a completion loses.
- **Chapters 12–20: arithmetic reductions and common futures.** These construct specified comparisons, retain residual cases and bound the supports of the constructed maps.

The final [all-even construction](../collatz_reconstruction/research_program/all_even_join_extension_20260916/note.md) gives explicit pairs of positive odd starts whose trajectories meet. A smaller start with a common future is not automatically a value visited by the other start's forward trajectory; the construction retains both paths. Its support bounds are not universal stopping-time bounds.

### The later overview is a separate source

The [27 September overview by Claude Opus 5.5](https://zenodo.org/records/23003414/files/00-claude-opus-5-5-collatz-ep817-bridges-record.pdf) has an [editable Markdown source](https://zenodo.org/api/records/23003414/files/00-claude-opus-5-5-collatz-ep817-bridges-record.md/content). Its §1 treats selected Collatz results; §§3–4 discuss limitations of specific methods and bridges between workbenches.

It reports selected rederivations and further results, not a complete audit of every manuscript here. In particular, §1.5 reports checking the Tao-clock deduction but not the paper's §§5–6 repairs, and not the first-jet restatement beyond its statement. Keep those coverage distinctions when using it. Its Problem 817 results belong to that programme; they are not additional Collatz results merely because they share a document. The overview is linked here, not silently substituted for the original proofs.

## Evidence and source history

The [research map](../RESEARCH_MAP.json) locates programmes. The [claim records](../collatz_reconstruction/state/claims.jsonl) and [map records](../collatz_reconstruction/state/morphisms.jsonl) carry finer-grained relationships. The manuscripts and cited sources remain the authority for mathematical statements.

For a computation, follow its command, input domain and recorded output. For a Lean result, identify the declaration, hypotheses, dependencies and toolchain, then compare the checked statement with the manuscript. Neither a source file nor an old success receipt is a fresh replay.

The [16 September publication notes](../editions/cumulative_20260916/PUBLICATION_NOTES.md) distinguish the checks rerun for that edition from inherited certificates. [Quarantined early attempts](../collatz_reconstruction/research_program/QUARANTINED.md) remain identifiable history; their notice must not be applied indiscriminately to the separately dated later notes.

This navigation update is dated **28 September 2026**. It preserves manuscript locations and mathematical content. It adds no blanket certification or claim that Collatz is solved.
