# Portable release verification

Release: `MS-CE-20260824-A`  
Date: 2026-08-24  
Disposition: source, mathematical-status, build, and visual gates pass

## Frozen source

The complete TeX input closure consists of the following thirteen files.

| Relative path | SHA-256 |
|---|---|
| `critical_expository_edition/main.tex` | `815333a15e63a9b7f39ac8e277cd20007dd886457c9d7a4d35e8d5c1201ec71c` |
| `critical_expository_edition/chapters/00_editorial_method.tex` | `4ca84b090da44dcffa6ca5eed1269fe2a3481f5bd5b682bee273f7127fe26ec7` |
| `critical_expository_edition/chapters/01_canonical_corpus.tex` | `e49e95b0d839bcb5473a3323e0fed6510d8b27de399d11e04cbdbcf8d2c309c8` |
| `critical_expository_edition/chapters/02_arithmetic_dynamics.tex` | `24cb982e9e76ad734d692fc453fd420b157c7b1107760640c05b4d2cfb7e99bc` |
| `critical_expository_edition/chapters/03_hydra_maps.tex` | `eadfef26af338fb748c6b9184426ea50b4d1b3735c062065148a9e5cadc5a2c5` |
| `critical_expository_edition/chapters/04_numen.tex` | `98eb08b29df3058e829d6b816c158b839c5fd8a64815f32f9473abe848f6fc20` |
| `critical_expository_edition/chapters/05_correspondence.tex` | `17e312123afe89d1aa87ec3069b140d29522b79691be86314da8e261bcee1aa5` |
| `critical_expository_edition/chapters/06_dreamcatchers.tex` | `c3ad85155b5f34cce34d14a6e61e2aa0e578f467e4f7f8cc0bd1e8db06cf4ff6` |
| `critical_expository_edition/chapters/07_contour_mellin.tex` | `097d7ab21b0860fc6580160114296843a1503c0d409551564b7d8418dee5628e` |
| `critical_expository_edition/chapters/08_pq_fourier.tex` | `b0c0563c5f5de95241dcc539e5b1c4bfe92a75b75ee1e81b32a6fd0b176abc6e` |
| `critical_expository_edition/chapters/09_rising_fseries.tex` | `ed85f1ee73a6f10d135cf7cb4460fc3c913502088376e6fc411cfda0ca56fcc2` |
| `critical_expository_edition/chapters/10_synthesis.tex` | `037d657bb5b613438248b10bf6fc6c03755231f7fdf214d6a28cbcea2c99ce35` |
| `critical_expository_edition/chapters/11_source_register.tex` | `b75e22d5ae0b2c423e6d63d68a8b6d265d76f2da04c90d1094b9f987d022c7e8` |

Static current-byte checks pass:

- 224 labels, all unique;
- 280 reference uses over 156 keys, with no missing key;
- 18 citation uses over 8 keys, with no missing bibliography key;
- 31 unique bibliography keys;
- zero NUL bytes, bare carriage returns, placeholder tokens, or Unicode dash
  substitutions;

## Mathematical-status closure

`apparatus/CLAIM_LEDGER.jsonl` contains 192 contiguous unique records and has
SHA-256
`e9ba4255f50c99b1763c136d6307b27ee554146eccfa283e3bd711e5577a2b8c`.
Its schema and graph checks pass: 214 strictly backward acyclic dependency
edges, 398 valid locators, and 192 document locators resolved against the
bundled 16-record index. All 48
theorem-family environments are ledger-covered and immediately followed by a
proof. Chapter 10's 23 reconstructed/proved rows, 2 checked-source rows, 11
withdrawn-or-invalid rows, and 6 conditional/formal rows all have explicit
atomic mappings.

The exact nonpromoted statuses and IDs are recorded in
`qa/claim_ledger_closure.json`. They remain source-status boundaries and are
not treated as positive theorems.

## Reference build

The source was built from a clean output directory with the documented
Latexmk command and fixed source-date environment. The final log is 61,728
bytes at SHA-256
`48597b30b3ccd8a52c15cddb53f39d8cdb1a5b936c25f5e76e83e208ab289e89`.
It contains no overfull box, LaTeX/package warning, undefined reference or
citation, multiply defined label, or rerun request.

The approved PDF is 1,198,545 bytes at SHA-256
`3e89313b9d47e27390bdfe79dfc3d87ae204dc39de9f451dd136241107810061`.
It is PDF 1.5, has 76 US-letter pages of `612 x 792` points, and carries the
exact title and author metadata in `RELEASE_METADATA.json`. Every listed font
is embedded.

## Visual verification

Every one of the 76 pages was rendered at 144 DPI and inspected. The review
covered margins, clipping, overlaps, running heads, page numbers, tables,
equations, theorem/proof transitions, chapter transitions, glyphs, and
references. The final exact-source-title correction changed only page 75
relative to the preceding fully inspected candidate; that page was reinspected
individually at original detail, and the other 75 retained byte-identical
inspected rasters. No visual defect remains.

## Rebuild identity boundary

A build in a different path is required to reproduce text, metadata, page
geometry, and all 76 page rasters. Its binary PDF hash may differ solely
because pdfTeX can vary the trailer identifier with the build path. The
separately distributed approved PDF is therefore bound by the exact hash
above; extracted-source rebuilds are compared by input hashes, text,
metadata, geometry, and page rasters.
