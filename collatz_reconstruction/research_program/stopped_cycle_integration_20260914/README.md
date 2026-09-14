# Authenticated integration: stopped transport and relative cycle cohomology

This is the current integration entry point for the 14 September 2026 continuation. The 21 files listed in `PAYLOAD_MANIFEST.json` are the complete previously delivered source payload, preserved byte-for-byte. Their statements about unavailable GitHub access record the earlier preparation sessions; they are not the status of this later authenticated integration.

Read the [cycle note](../cycle_relative_cohomology_20260914/note.md), its [research task state](../cycle_relative_cohomology_20260914/TASK_STATE.md), and the unchanged [stopped-affine note](../stopped_affine_transport_20260914/note.md). The project remains a research continuation, not a proof of universal Collatz convergence or a positive counterexample.

## Pinned intake and exact source crosswalk

The integration base is `63407034387466870f9e092dcdf39fb5a1ec0399` in `KokunoYumeto/collatz-workbench`. Authenticated reads covered `README.md`, `CONTRIBUTING.md`, `collatz_reconstruction/tex/chapters/00_scope_and_method.tex`, and the complete `collatz_reconstruction/research_program/split_zero_history_20260913/note.tex` (blob `5fec479a48c4253eadffb9ed3c78da81b58a0000`). PR #1 was read as existing, separate work and was not changed or merged.

For the manuscript's original labelled word `w=(a_1,...,a_m)`, the comparison to either imported packet is the identity on the exponent tuple, with `S_j=A_j`, `B_w=C(p)`, `2^A=U`, and `3^m=L`. The equality of numerators follows term-by-term from `B_w=sum_{j=0}^{m-1}3^(m-1-j)2^S_j` and `C(p)=sum_{i=1}^m3^(m-i)2^A_(i-1)` by the explicit index map `i=j+1`. Consequently the formal branch maps coincide. The two selected cylinder residues coincide because both lie in `[1,2^(A+1))` and solve the same congruence with invertible coefficient `3^m`. The original fixed-point numerator, cyclic rotation law, labels, and order are retained.

The peer Zeta reads were `POLYCLANK_PARTICIPATION.md` (blob `e4b0506053b9e33468df31aea2cd191edba7ed2b`) and `RESEARCH_PROGRAMMES.md` (blob `1cd168729cd40fe48b71542d94a8f793a794bdc8`). Those readings record workflow and source-handling guidance; no Zeta file was changed. No unpushed local Codex state was read.

## Replay

From the repository root:

```sh
python -B collatz_reconstruction/research_program/stopped_cycle_integration_20260914/verify_import.py
```

This verifies the exact size and SHA-256 of all 21 frozen payload files and invokes the original `replay_all.py`. That replay checks both source manifests and reproduces all three suites under ordinary and optimized Python, requiring byte-identical outputs. `--hashes-only` performs just the 21-file import check.

The original scopes remain separate: 175,269 stopped-transport checks; 142 support-certificate checks; 42,507 cycle-continuation checks, including an exhaustive visit to 1,048,575 words of exponent sum at most 20. These are finite checks, not independent certification of every written infinite proof.

## Publication and retained history

Sources were added on `research/stopped-cycle-cohomology-20260914`, descending from the pinned real base, not from the unrelated local packaging bundle. A one-shot branch-restricted workflow rebuilt only the three absent result JSON files, verified their original hashes, ran all six replays, and committed those three additions. GitHub run `34877116817`, job `104086952240`, completed successfully; the generated-results commit is `05d572e4ba40307e06c5e3ba67d1bec97aabd49e`.

The temporary materialization script and its write-enabled workflow are removed from the finished branch. The delivered read-only replay workflow is restored unchanged. `INTEGRATION_RECEIPT.json` records this checkpoint; the pull request and its checks record subsequent publication state. No force-push, merge, rewrite of inherited files, or update of `main` is part of this integration.

The continuation task operates on the original residual roots and projected original edges, adds actual certified descent families with their boundary chains, and retains both cycle periods and nonperiodic component obstructions. The original forcing `+1`, the supported zero labels, and integer-source membership remain explicit throughout.
