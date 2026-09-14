# Collatz history-law continuation: local-session handoff

This is a Collatz-only continuation of the September 13 history/Hurwitz note at repository revision `63407034387466870f9e092dcdf39fb5a1ec0399`. Start with [the mathematical note](RESEARCH_NOTE.md), then [the exact checker](check_history_law.py) and [its recorded output](verification.json).

The main result is the uniform critical-window limit

\[
\Delta\left(P_{N,b,\lfloor(\log_2 N)/2+c\sqrt{\log_2 N}\rfloor},G_m\right)
\longrightarrow\Phi(2c),
\]

where the starting integer is uniform on N consecutive positive odd integers, `m` is the displayed horizon, and Delta is half the L1 distance. The proof retains the original exact odd-return cylinders, proves explicit finite upper and lower bounds, and uses the binomial central limit calculation. It is not an assertion about an arbitrarily chosen random model in place of integer starts. It does not imply convergence of individual Collatz trajectories.

The note also proves an exact first-descent count on each cylinder using all affine offsets. Its capped certificate retains an explicit overflow count. Finite capped distributions, including overflow and present zero-weight labels, pass through the predecessor's finite spectral reconstruction without changing the displacement coordinate or claiming an analytic conditioning estimate.

## Source and attribution

The mathematical source is `../split_zero_history_20260913/note.tex`, Git blob `5fec479a48c4253eadffb9ed3c78da81b58a0000` at the revision above. Its complete mathematical text and accompanying historical audit were read. The research-companion README and repository contribution guidance were also inspected, but the whole companion and workbench were not re-audited.

Tao V7 (arXiv:1909.03562v7), Definition 1.7, Proposition 1.9 and Section 4, supplies the established geometric-valuation/cylinder counting context. This contribution explicitly credits that mechanism and gives its own interval discrepancy, support obstruction and critical-window proof. It neither assumes Proposition 1.9's residue-uniformity hypothesis for arbitrary intervals nor claims a stronger orbit-minimum theorem. The references in the note contain the primary-source links. No global novelty or independent peer review is asserted.

The contribution was written and checked in a ChatGPT web session on 14 September 2026. It is additive, does not edit any earlier manuscript or publication manifest, and does not promote the historically quarantined attempts. The previous web-session integral-extension ZIP remains a separate contribution, not an audited dependency of this one. No zeta-workbench file, private conversation, machine-specific locator, third-party bulk source, or new license is included.

## Reproduce

Python 3.10 or newer, standard library only. From this directory:

```sh
python -B check_history_law.py > verification.normal.json
python -O -B check_history_law.py > verification.optimized.json
```

Both modes were executed, exited successfully, and produced byte-identical output matching `verification.json`. Check the file identities in `MANIFEST.json` before assigning that execution statement to modified code. The manifest covers the other four files and excludes itself. The finite verification is not a Lean certificate, a numerical zeta calculation, or a numerical certification of the Gaussian limit. No existing repository-wide CI or checker was replayed.

## Next bounded task

Use the full-history threshold as a constraint, not a reason to stop. Specify a joint arithmetic observation that discards enough history to avoid the support obstruction, while retaining the relevant affine descent barrier. Compute its actual fibres or transition law and compare its distribution beyond the full-word scale. The existing capped counter provides exact fixtures and preserves the number of undecided starting integers. Do not infer independence between residue tests merely because each marginal looks geometric.

This directory is ready for review in a separate contribution branch. It is not an automatic replacement for the original local-session state, and the original source revision remains pinned above.
