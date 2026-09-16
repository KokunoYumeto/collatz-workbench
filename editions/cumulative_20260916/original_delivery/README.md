# Collatz — cumulative results, full LaTeX, code and evidence

**Start with `latex/main.pdf` (236 pages), or open `latex/main.tex`.**

The volume has **20 complete mathematical chapters**, not chapter summaries. It
combines the full notes from all **14 supplied continuation ZIPs**, four further
complete notes retrieved from the pinned GitHub source, and this turn's new
all-even-interior-exponent continuation. The original 14 ZIP files remain
byte-for-byte intact under `source_archives/`, including their full proof
ledgers, tests, manifests, historical receipts and patches. The LaTeX edition is generated from the full
original mathematical notes; their original Markdown stays unchanged.

The new work is in:

```
repository/collatz_reconstruction/research_program/
all_even_join_extension_20260916/
```

Its central results are complete common-future source families for every even
interior exponent; the exact ternary layer `b + nu_3(e-1)`; a proved finite
membership search for each original input; and an extension of the prior
first-jet retraction that preserves its original support budget by checking
both actual paths. The full proof is `note.md`. It does not prove Collatz or
claim every retained root is eliminated.

## Contents and boundaries

| Location | Contents |
|---|---|
| `latex/` | Compiled cumulative volume, editable master, 20 full chapter sources, original math-token inventories, source map and typography record. |
| `repository/` | Runnable additive overlay of the supplied research files, the new addition, and four recovered GitHub notes. It is not a complete Git checkout. |
| `source_archives/` | All 14 original supplied ZIPs unchanged; 412 original file members in total. |
| `provenance/` | Exact ZIP/member hashes, all 71 standalone-input locators, repository overlay inventory, GitHub pins, and declared restoration scope. |
| `evidence/` | This session's actual replay and archive/render checks. Historical execution records stay in their source archives. |
| `tools/` | Safe additive integrator, archive verifier, LaTeX regeneration tool, and optional pinned read-only GitHub companion-file restorer. |

All supplied standalone files have an identical original member in at least one
of the preserved ZIPs. `provenance/STANDALONE_LOCATORS.json` identifies those exact
members, including the large complete ledgers; no large ledger was replaced by a
sample. Source duplication is recorded, rather than made into contradictory
independent versions. No font files or credentials are distributed.

Three historical directories were not supplied as complete local packages:
`history_law_cutoff_20260914`, `anchored_defect_20260914`, and
`ternary_join_reduction_20260916`. **Their four complete mathematical notes are
included**, retrieved and checked against the original Git blob IDs. Other
companion scripts and receipts in those three directories are not bundled.
They are listed as such in `provenance/GITHUB_ONLY.json`, with an immutable commit
pin and a restoration command below. This ZIP is therefore a cumulative archive
of all supplied results and recovered continuation proofs, not a fresh full clone
of every workbench file or a claim to possess unpushed local sessions.

## Current GitHub state

PR #2 was merged on 16 September 2026. Current `main` was read at:

```
9453b5306b3a897389dece309f9c119dffbcc489
```

That integration already contains the bilateral-root result. Some older source
receipts still say it was local or that PR #2 was open; those are preserved
historical statements, not this archive's current-state report.

**The all-even addition and this cumulative edition were not pushed in this
session.** There is no new remote commit or CI result to claim. The included
`ALL_EVEN_ADDITION.patch` contains only 13 additions; it never changes inherited
files. Do not apply an old historical patch over a changed checkout without
checking its base and current contents.

## Verify and run locally

From this archive root, verify byte identities and all original ZIP CRCs:

```sh
python -B tools/verify_archive.py
```

Run the new exact pair, the independent all-family audit, and the unchanged
first-jet predecessor pair:

```sh
python -B repository/collatz_reconstruction/research_program/all_even_join_extension_20260916/replay.py --predecessor
```

This session's new pair has **87,989 exact checks per execution**, with identical
output. The independent auditor checks all 512 declared family fixtures and
24,180 original affine-coefficient equations. Fourteen invalid controls are
rejected. The all-parameter theorems have written proofs; these bounded tests are
not a global exhaustion argument. No new millions-of-starts crossing scan or
independent external mathematical review is claimed in this edition.

Preview the new files against an existing local checkout, then explicitly apply:

```sh
python -B tools/apply_overlay.py /path/to/collatz-workbench
python -B tools/apply_overlay.py /path/to/collatz-workbench --apply
```

The default adds only this turn's new research directory and read-only workflow.
It skips identical files and rejects every different destination before writing.
`--all-supplied` deliberately selects the larger archival overlay. Neither mode
commits, pushes, merges, deletes, or overwrites a differing file.

To restore the optional GitHub companion files at the pinned revision on a
networked machine:

```sh
python -B tools/fetch_github_sources.py
python -B tools/fetch_github_sources.py --apply
```

The first command previews the complete checked payload. Both use GET requests
only and verify the original Git blob identities. `GITHUB_TOKEN` or `GH_TOKEN`
may be provided locally for access or rate limits; the token is never saved.
No live network restoration is claimed from this session; its shared additive
writer was tested locally against repeats, conflicts, path traversal and symlinks.

## LaTeX

The provided `.tex` files compile directly; Pandoc is needed only for regeneration.
See `latex/README.md` for the exact requirements and source-to-chapter map.
Original Markdown bytes are never rewritten by the typesetting operation.
The PDF is a source anthology, not a claim that all chapters constitute a single
independently audited proof. Historical assumptions, verification scopes and
open obligations remain visible in their original chapters.
