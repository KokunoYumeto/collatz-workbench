# Affine antecedent: bounded manifestation comparison

Audit ID: `AUD-COL-AFFINE-VERSION-20260904-0001`.
Date: 2026-09-04. Scope: the antecedent statements used in critical chapter 06
and research companion chapter 04, not a new full audit of either note.

## Conclusion

The wrapper's 61-page PDF and the indexed V5 62-page PDF contain the same
mathematical text in the twelve statement/proof blocks collated below. Their
sixteen token-difference hunks are all reference substitutions: unresolved
`??` or `[?]` in the 61-page PDF versus reference numbers in the 62-page PDF.
No mathematical revision was found in these blocks. The indexed TeX agrees
with the formulas, hypotheses, proofs and even defective cross-reference
commands at the inspected loci.

These are distinct file manifestations, not identical files. The 61-page
PDF has an empty Contents block (p. 2), whereas the 62-page PDF has a populated
Contents list (pp. 2-3), and their displayed title dates differ. This supports
a difference in compilation state and repagination at the examined loci.
It does not establish which exact build inputs produced either PDF, nor that
every unexamined passage is identical. No rebuild was performed and no
source-version chronology is inferred merely from filenames or dates.

The comparison also corrects the present edition's account of its antecedent:
Theorem 10.1 already explicitly proves the affine cyclic-transport arrow.
The edition supplies the exact valuation and divisibility checks; it did not
discover an affine arrow absent from the antecedent. The Hamiltonian source
locator is p. 55, not p. 54. The complete packet-average theorem and proof are
pp. 21-23, with its auxiliary binomial lemma on p. 20.

## Exact witnesses

All paths below are read-only source locators. A and C have matching printed
and one-based physical page numbers at every inspected locus.

**A: controlling local antecedent PDF**

`C:/Users/LOCAL_USER/Documents/Erdos Strauss and related/ES-Fable-C123-support/external_sources/combined_live_theorem_package_dependencies/odd_step_collatz_orbit_packets_note.pdf`

- 546,452 bytes; 61 pages.
- SHA-256: `13f49961a60b870fa7a6f0f646758b4d72c1a4e4267f347606cc8a3238d552f1`.
- Title page: *Affine Packets, Cyclic Orbit Packets, Dyadic Dilation,
  Lambert-Mahler Series, Hydra/Numen Structure, and Exact Rational Periodic
  Orbit Enumeration in the Odd-Step Collatz Algebra*; author line
  `OpenAI technical note`; displayed date May 24, 2026.
- PDF metadata creation/modification: `D:20260524080406Z`.

**B: indexed V5 TeX**

`C:/Users/LOCAL_USER/Documents/Papors/Chatnotes/automata/V5/odd_step_collatz_orbit_packets_note.tex`

- 114,074 bytes; 4,099 physical lines.
- SHA-256: `406ef13e43ae0af68fabdbda4dd16145d313407f7d38ea22311803c7533cfec7`.
- Title/author commands: lines 53-56; date command is `\date{\today}` at
  line 57; `\tableofcontents` at line 80. Thus a PDF title date is not a
  reliable authored-version identifier by itself.

**C: indexed V5 PDF**

`C:/Users/LOCAL_USER/Documents/Papors/Chatnotes/automata/V5/odd_step_collatz_orbit_packets_note.pdf`

- 566,720 bytes; 62 pages.
- SHA-256: `878d3ddbb3fefc0c781aa7ca0cd6536dcd7b5d7a46df18ecdb3662eee47d3ab1`.
- Same title and author line as A; displayed date March 21, 2026.
- PDF metadata creation/modification: `D:20260321135918Z`.

Both PDFs report `LaTeX with hyperref`, `pdfTeX-1.40.26` and PDF 1.7. Those
metadata fields are descriptive evidence, not a producing-build receipt.

## Route and method

The controlling request was followed after reading current `DIRECTIVES.md`,
`state/affine_packet_topic_route.json`, and the canonical
`Zeta-Function-Foundation/config/literature_index_entrypoint.json`.
The exact A locator and pin were read from
`certificates/affine_packet_source_and_cycle_checks.py`. The canonical local
query `odd step packets` routes B/C through
`PUBUNIT-CF4FD708E6C6DE523385FD85`. The query was for routing only.

The read-only comparison script
`affine_antecedent_version_compare_20260904.py` pins all three source hashes.
It extracts native PDF text, verifies and omits each final page-number line,
then compares whitespace-delimited tokens between explicit statement
boundaries. It does not discard reference tokens, signs, equations or numbers.
The companion JSON records every token difference, exact block text hashes,
page spans, source identities and coverage limits. Token equality is a
collation check, not a proof of mathematical correctness or of PDF production
from a particular TeX file.

## Inspected source crosswalk

| Passage | A pages | C pages | B physical lines | Collation result |
| --- | --- | --- | --- | --- |
| Theorem 2.1 and Corollary 2.2: affine formula and numerator recurrence | 4-5 | 5-7 | 141-268 | Four reference replacements only |
| Theorem 3.1 and Corollary 3.2: translations and their groupoid identities | 8 | 9-10 | 452-520 | Identical extracted block text |
| Theorem 4.2: complex Abel coordinate | 11 | 12-13 | 699-736 | `??` becomes `Theorem 4.1` only |
| Theorem 4.4: transport of Abel/Schroeder coordinates | 12 | 13 | 742-781 | `(??)*` becomes `(1.3)*` only |
| Corollary 6.5: concentration | 18 | 19 | 1154-1166 | Reference replacement only |
| Corollary 6.7: multiplicity | 19 | 20 | 1208-1223 | Identical extracted block text |
| Theorem 6.10: packet average, complete proof | 21-23 | 22-24 | 1307-1461 | Three reference replacements only |
| Theorem 10.1: cyclic affine transport | 36 | 37 | 2359-2419 | Identical extracted block text |
| Theorem 10.3: primitive-necklace classification | 37 | 38 | 2434-2481 | Reference replacement only |
| Theorem 11.1: Burnside count | 39 | 40 | 2558-2605 | Reference replacement only |
| Theorem 11.2: primitive count | 40 | 41 | 2607-2628 | Two reference replacements only |
| One-letter Hamiltonian and Theorem 19.1 | 55 | 56 | 3647-3677 | Citation and equation-reference replacements only |

The populated references are not automatically correct. For example,
Theorem 4.4's proof still refers to `(1.3)*`, which is the earlier definition
of `c(p)`, and the packet-average proof refers to `(1.6)*`, the earlier
definition of `Q`. These outputs correspond to the literal source commands
using `eq:c-def` and `eq:Q-def`, not to a mathematical revision.

The translation identities in Corollary 3.2 are between `I_{p,q}` for arbitrary
packet elements `p,q` with a fixed label `(m,A)`. They should not be silently
substituted for the companion's separately typed rotation arrows `(p,j)` and
pointed parity-word groupoid comparison.

## Consequences for the existing source audit

1. **Cyclic affine transport was already explicit.** A p. 36, C p. 37,
   B lines 2381-2405 prove
   `g_(sigma p)(g_(a1)(x_p)) = g_(a1)(x_p)` and use uniqueness of the fixed
   point to conclude `g_(a1)(x_p) = x_(sigma p)`. The final passage to the
   genuine odd-type map is asserted at B line 2418 without explicitly writing
   the valuation. The source's odd numerator and odd denominator yield
   `nu_2(3x_p+1)=a1`; the current companion makes that check, nonvanishing,
   the empty-tail convention and both directions of divisibility explicit.
   Therefore the old heading/description "missing arrow" should distinguish
   the explicit pre-existing affine transport from the newly explicit
   valuation/divisibility verification. This is an attribution correction,
   not a claim that the companion's proofs are invalid.

2. **Theorem 10.3 contains a pointed-word misstatement, unchanged in both
   PDFs.** The final paragraph on A p. 37 / C p. 38, B line 2480, says equality
   of infinite periodic words is equivalent to primitive roots being cyclic
   shifts. The reverse implication as written is false: `(1,2)^infinity`
   and `(2,1)^infinity` are unequal as pointed sequences. Equality of pointed
   infinite periodic words forces equal primitive roots, which is stronger
   than the direction the proof needs. Replacing that sentence by the true
   pointed statement preserves the orbit-classification theorem. No new
   endpoint or unresolved mathematical requirement is introduced.

3. **The original five repair loci persist in B/C.** The Abel theorem still
   lacks the required logarithm increment compatibility (B 700, 724-728),
   while its transport theorem explicitly requires compatible branches
   (751). The concentration proof retains its reversed displayed sign
   (1164); the increase statement survives. The maximizer count still omits
   `A=m` (1215-1223), when the single all-ones word is the sole maximizer.
   The packet-average proof still sets `r=m-2` (1340), although the cited
   binomial lemma requires `r>=0` (1239); the singleton `m=1` case needs its
   direct calculation and satisfies the displayed formula. The Hamiltonian
   still specifies only the action on basis vectors, not the maximal
   multiplication-operator domain (3649-3654).

4. **Source coordinates for the last repair must remain specific.** Here
   `H_1` acts on `ell^2(N_{>=1})`, with `u(a)=a log 2-log 3`. The maximal
   domain is the sequences `xi` satisfying
   `sum_(a>=1) |u(a)|^2 |xi_a|^2 < infinity`. The general `L^2` formulation
   in the edition can be specialized to this actual source object. Its
   source page is A p. 55 / C p. 56, not A p. 54. The trace calculation in
   Theorem 19.1 is the same geometric sum in all three witnesses; no claim
   of a BCM-system identification follows from this version comparison.

## Coverage and action boundary

The section structure, title/contents and the twelve listed mathematical
blocks were inspected. The PDF renders checked visually were A pp.
11, 18, 19, 21, 36, 37, 55 and C pp. 12, 13, 19, 20, 22, 37, 38, 56.
The auxiliary binomial lemma and complete packet-average proof were read
through native text and TeX. Native text from other explicitly named nearby
pages was used to establish boundaries; this is not a new full-note reading
claim. A second agent read the exact V5 windows independently, and the
reported passages were rechecked directly before inclusion here.

No TeX, source, claim ledger, wrapper pin, corpus index, Lean file, or
Overleaf state was changed. No build, Lean process, Git operation or upload
was run. Only this audit, its bounded collation helper/receipt, and temporary
page renders were created. The parent task owns downstream propagation.

Unexamined mathematics, full bibliography accuracy, human authorship lineage,
and exact producing-build provenance remain outside this bounded report.
The comparison supplies content correspondence at the listed loci, not a
permission to transfer every theorem from one manifestation to another.
