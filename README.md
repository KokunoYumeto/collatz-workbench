# Collatz research workbench

## September 16 research update

[Read the new contributions, full source lineage and integration checks](integration/20260916/README.md).


A PolyClank-style home for sustained human–LLM work on Collatz dynamics: the literature, the constructions it suggests, the proofs that survive checking, and the history needed to continue them. The aim is useful mathematics on Collatz, not a claim that the conjecture has been solved.

## Read the mathematics

| Programme | Read | Inspect the source |
| --- | --- | --- |
| Maxwell C. Siegel: Hydra maps, numens and (p,q)-adic analysis | [Critical-expository edition](maxwell_siegel_research/output/pdf/maxwell_siegel_critical_expository_edition.pdf) | [Portable edition and apparatus](siegel_edition/) |
| Collatz literature and the local research corpus | [Working critical reader](collatz_reconstruction/output/pdf/collatz_working_corpus.pdf) | [Complete TeX](collatz_reconstruction/tex/) |
| Weighted odd-step paths, survivor coding, arithmetic groupoids and period maps | [Research companion](collatz_reconstruction/research_companion/output/pdf/collatz_research_companion.pdf) | [Manuscript, certificates and provenance](collatz_reconstruction/research_companion/) |
| Clocks and first-passage measures in Tao's theorem | [Separate preprint](collatz_reconstruction/preprints/tao_clock_audit/output/pdf/tao_clock_audit.pdf) | [V7-based manuscript and checks](collatz_reconstruction/preprints/tao_clock_audit/) |
| Finite histories, support and Hurwitz zero clusters | [Split Zero / Collatz note](collatz_reconstruction/research_program/split_zero_history_20260913/note.pdf) | [Proofs, exact checker and audit](collatz_reconstruction/research_program/split_zero_history_20260913/) |

The critical edition represents Siegel's work under his own name; the independent research is a different contribution. The Tao paper studies exact clocks and first-passage distributions using Tao's V7. It does not advertise a stronger orbit-minimum theorem. The Split Zero note constructs an invertible finite spectral encoding of distributions of actual Collatz histories, retaining joint arithmetic tests; its stated result is not an orbit-descent estimate.

## Find a result, follow its history, contribute

The [research map](RESEARCH_MAP.json) identifies the programmes and their entry points. [Claims](collatz_reconstruction/state/claims.jsonl), [explicit maps](collatz_reconstruction/state/morphisms.jsonl), [source identities](collatz_reconstruction/state/source_registry.jsonl), and [programme records](collatz_reconstruction/state/programmes.jsonl) provide the detailed crosswalk. [Mathematical audits](collatz_reconstruction/qa/), manuscript-local audit directories, [finite checks](collatz_reconstruction/certificates/), and [Lean sources](collatz_reconstruction/formal/) expose the supporting work. A script or source file is not, by its presence alone, a claim of successful execution or complete formalization.

The earlier [quarantined research attempts](collatz_reconstruction/research_program/QUARANTINED.md) are preserved as history, not promoted to results. Their directory-wide historical notice predates the separately dated September 13 Split Zero note. That later note has its own proofs, source intake, and audit. The established research companion is the separate directory linked above.

This is intended to be usable without the original conversation. Read the argument, identify the exact definition or result used, and leave an intelligible contribution—an improved proof, a checked example, a correction, a new map, or a well-motivated mathematical question. [Contribution guidance](CONTRIBUTING.md) explains how to record what was actually checked. Issues and pull requests are welcome.

## Peer work and current snapshot

The Split Zero input used here is pinned in the note to [the historical Hurwitz reconstruction](https://github.com/KokunoYumeto/zeta-function-research-reader/blob/16fc4dbb817b82023c6126e636f1c6df28d4cecd/workbenches/splitzero-tandem/continuations/20260913-toda/tex/historical_hurwitz_jets.tex), especially H10–H13. The [zeta workbench](https://github.com/KokunoYumeto/zeta-function-research-reader) is a peer programme, not a substitute for these Collatz sources. A later web-session integral-extension continuation is not yet included or audited in this snapshot.

**14 September 2026:** first dedicated GitHub publication of the local workbench. The mathematical material is now browsable together; this publication does not represent a new theorem or a new proof audit. [Scope and exclusions](PUBLICATION_SCOPE.md), [source-to-public hashes](MIRROR_MANIFEST.json), and [repository inventory](repository_inventory.json) describe exactly what is included. Private raw conversations and third-party bulk literature stay local; the original mathematical work and its citations are exposed here.

Public collaboration name: **Kokuno Yumeto**. The recorded LLM contribution used **ChatGPT 5.6 Sol, Ultra mode, in Codex**. Source authors retain their own attribution. The corpus is a working research collection, not a completed proof of Collatz.
