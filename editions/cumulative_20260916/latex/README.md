# Build the corrected cumulative reader

`main.tex` includes all 20 chapter sources and compiles directly. Run from this
directory:

```sh
xelatex -interaction=nonstopmode -halt-on-error -no-shell-escape main.tex
xelatex -interaction=nonstopmode -halt-on-error -no-shell-escape main.tex
```

Requirements: XeLaTeX, the ordinary packages named in `main.tex`, DejaVu Serif,
DejaVu Sans, DejaVu Sans Mono, and Latin Modern Math. No font binaries are
redistributed. Two completed runs produced the 237-page current reader.

To regenerate the chapters from the included Markdown, run from the edition root:

```sh
python -B tools/build_latex.py
```

Regeneration uses Pandoc 3.9 syntax. `SOURCE_MAP_INPUT.json` pins the included
Markdown. `FRONT_MATTER.tex` supplies the editable introduction and preamble.
`READER_REPAIRS.json` records exact literal-character escapes applied only to
the in-memory conversion input. The converter disables Markdown superscript
and subscript interpretation, then emits complete per-chapter mathematical
inventories. It never rewrites the included Markdown.

All 2,670 explicit math tokens match their source inventories. The inherited
presentation repair `\mathbb Q\otimes_\mathbb ZQ` to
`\mathbb Q\otimes_{\mathbb Z}Q` is retained; the source is unchanged. Code and
URLs wrap, and display expressions may be scaled to fit the text width.

The final build has no overfull-box or missing-glyph warnings. All pages were
rendered, and representative pages, the formerly corrupted inline expressions,
the title credits, and the fixed-root clarification were visually inspected.
These are source and rendering checks, not a proof audit of the anthology.
