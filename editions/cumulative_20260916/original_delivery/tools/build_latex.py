#!/usr/bin/env python3
"""Rebuild the complete LaTeX anthology from immutable original Markdown.
Requires Pandoc; compilation is a separate XeLaTeX command.
"""
from pathlib import Path
import argparse,json,subprocess,re,hashlib
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
root=ap.parse_args().root.resolve()
repo=root/'repository/collatz_reconstruction/research_program'
tex=root/'latex';chap=tex/'chapters';chap.mkdir(parents=True,exist_ok=True)
order=[('stopped_affine_transport_20260914','note.md'),('cycle_relative_cohomology_20260914','note.md'),('residual_splice_20260914','note.md'),('residual_splice_20260914','integral_blocks.md'),('clocked_support_20260914','note.md'),('completion_defect_20260914','note.md'),('supported_structure_20260915','note.md'),('intrinsic_zero_firstjet_20260915','note.md'),('defect_rank_descent_20260915','note.md'),('defect_rank_descent_20260915','logarithmic_run_exclusion.md'),('negative_shadow_descent_20260916','note.md'),('mixed_switch_control_20260916','note.md'),('global_cylinder_control_20260916','note.md'),('height_window_reduction_20260916','note.md'),('bilateral_root_bounds_20260916','note.md'),('all_even_join_extension_20260916','note.md')]
# When missing historical directories are retrieved locally, include their full notes too.
for ix,pair in reversed(list(enumerate([('history_law_cutoff_20260914','RESEARCH_NOTE.md'),('anchored_defect_20260914','note.md'),('anchored_defect_20260914','turns_and_unit_excess.md'),('ternary_join_reduction_20260916','note.md')]))):
 if (repo/pair[0]/pair[1]).is_file():
  pos=0 if ix==0 else 8 if ix in (1,2) else len(order)-2
  order.insert(pos,pair)
records=[];inputs=[]
for i,(d,fn) in enumerate(order,1):
 p=repo/d/fn;raw=p.read_bytes();stem=f'{i:02d}_{d}_{Path(fn).stem}'
 fmt='markdown+tex_math_single_backslash+tex_math_dollars+raw_tex-auto_identifiers'
 ast=json.loads(subprocess.check_output(['pandoc','-f',fmt,'-t','json',str(p)]))
 mathrec=[]
 def walk(o):
  if isinstance(o,list):return [walk(x) for x in o]
  if isinstance(o,dict):
   if o.get('t')=='Str' and len(o.get('c',''))>23 and any(ch.isdigit() for ch in o['c']) and not any(ch in o['c'] for ch in '{}\\'):
    return {'t':'RawInline','c':['latex',r'\nolinkurl{'+o['c']+'}']}
   if o.get('t')=='Str' and o.get('c','').startswith(('https://','http://')):
    return {'t':'RawInline','c':['latex',r'\url{'+o['c']+'}']}
   if o.get('t')=='Code' and '{' not in o['c'][1] and '}' not in o['c'][1]:
    return {'t':'RawInline','c':['latex',r'\nolinkurl{'+o['c'][1]+'}']}
   if o.get('t')=='Math':
    kind,text=o['c'];mathrec.append({'kind':kind['t'],'text':text})
    if kind['t']=='DisplayMath':
     tags=re.findall(r'\\tag\*?\{([^{}]*)\}',text)
     if len(tags)>1: raise ValueError((p,'multiple tags in single display',tags))
     body=re.sub(r'\\tag\*?\{[^{}]*\}','',text)
     body=re.sub(r'\n\s*\n','\n',body).strip()
     # Labels are retained verbatim; duplicate label namespaces are unlikely in these MD files.
     return {'t':'RawInline','c':['latex','\\SourceMath{'+body+'}{'+(tags[0] if tags else '')+'}']}
   return {k:walk(v) for k,v in o.items()}
  return o
 ast=walk(ast)
 out=subprocess.check_output(['pandoc','-f','json','-t','latex','--top-level-division=chapter','--no-highlight'],input=json.dumps(ast).encode()).decode()
 # Recorded TeX grouping repair only; original Markdown is immutable.
 out=out.replace(r'\mathbb Q\otimes_\mathbb ZQ',r'\mathbb Q\otimes_{\mathbb Z}Q')
 # Make code wrap rather than clipping; prose math/code data are unchanged.
 out=out.replace('\\begin{verbatim}','\\begin{Verbatim}[breaklines=true,breakanywhere=true,fontsize=\\scriptsize]').replace('\\end{verbatim}','\\end{Verbatim}')
 # Provenance immediately after the source chapter title.
 header_end=out.find('\n')
 if out.startswith('\\chapter{'):
  depth=1; j=len('\\chapter{')
  while depth:
   if out[j]=='{' and out[j-1]!='\\':depth+=1
   if out[j]=='}' and out[j-1]!='\\':depth-=1
   j+=1
  header_end=j
 provenance='\n{\\small\\sffamily Source: \\nolinkurl{'+str(p.relative_to(root))+'}.\\par}\n'
 out=out[:header_end+1]+provenance+out[header_end+1:]
 (chap/(stem+'.tex')).write_text(out)
 (chap/(stem+'.math.json')).write_text(json.dumps(mathrec,indent=2,ensure_ascii=False))
 records.append({'number':i,'source':str(p.relative_to(root)),'source_sha256':hashlib.sha256(raw).hexdigest(),'latex':f'chapters/{stem}.tex','math_tokens':len(mathrec),'display_math_tokens':sum(x['kind']=='DisplayMath' for x in mathrec),'original_content_preserved':True})
 inputs.append('\\input{chapters/'+stem+'.tex}')
(tex/'SOURCE_MAP.json').write_text(json.dumps(records,indent=2))
front=r'''\documentclass[11pt,oneside]{book}
\usepackage[a4paper,margin=23mm,headheight=16pt]{geometry}
\usepackage{fontspec}
\setmainfont{DejaVu Serif}
\setsansfont{DejaVu Sans}
\setmonofont{DejaVu Sans Mono}[Scale=0.82]
\usepackage{amsmath,amssymb,mathtools}
\usepackage{unicode-math}
\setmathfont{latinmodern-math.otf}
\usepackage{graphicx,adjustbox}
\usepackage{longtable,booktabs,array,calc,etoolbox}\AtBeginEnvironment{longtable}{\footnotesize}
\usepackage{fvextra}
\usepackage{xcolor}
\usepackage{hyperref}
\hypersetup{hidelinks,pdftitle={Collatz Research Continuations -- Cumulative Supplied Sources},pdfauthor={KokunoYumeto research programme; tool-assisted continuation}}
\usepackage{xurl}
\usepackage{newunicodechar}
\newunicodechar{∎}{\ensuremath{\blacksquare}}
\newunicodechar{⋯}{\ensuremath{\cdots}}
\usepackage{titlesec}
\titleformat{\section}{\large\bfseries\raggedright}{\thesection}{0.75em}{}
\titleformat{\subsection}{\normalsize\bfseries\raggedright}{\thesubsection}{0.75em}{}
\makeatletter
\renewcommand{\@pnumwidth}{3em}
\renewcommand{\@tocrmarg}{4em}\renewcommand*{\l@section}{\@dottedtocline{1}{1.5em}{3.5em}}
\makeatother
\usepackage{fancyhdr}
\pagestyle{fancy}\fancyhf{}
\fancyhead[L]{\small\sffamily COLLATZ RESEARCH CONTINUATIONS}
\fancyhead[R]{\small\sffamily CUMULATIVE SOURCES}
\fancyfoot[C]{\thepage}
\renewcommand{\headrulewidth}{0.3pt}
\setlength{\parindent}{0pt}\setlength{\parskip}{0.45em}
\setlength{\emergencystretch}{4em}
\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
\providecommand{\pandocbounded}[1]{#1}
\providecommand{\passthrough}[1]{#1}
\newcommand{\N}{\mathbb N}
\newcommand{\Z}{\mathbb Z}
\newcommand{\Q}{\mathbb Q}
\newcommand{\R}{\mathbb R}
\newcommand{\C}{\mathbb C}
\newsavebox{\sourceformula}\newsavebox{\sourcetag}
\newlength{\sourcewidth}
\newcommand{\SourceMath}[2]{%
 \par\addvspace{0.6em}\begingroup
 \sbox{\sourceformula}{\(\displaystyle #1\)}%
 \def\tagcontent{#2}%
 \ifx\tagcontent\empty\sbox{\sourcetag}{}\setlength{\sourcewidth}{\linewidth}%
 \else\sbox{\sourcetag}{\normalfont\small(#2)}\setlength{\sourcewidth}{\linewidth-\wd\sourcetag-1em}\fi
 \noindent\hbox to\linewidth{\hfil\adjustbox{max width=\sourcewidth}{\usebox{\sourceformula}}\hfil\usebox{\sourcetag}}%
 \endgroup\par\addvspace{0.6em}}
\setcounter{tocdepth}{1}
\begin{document}
\frontmatter
\begin{titlepage}
\vspace*{20mm}
{\sffamily\large CUMULATIVE RESEARCH ARCHIVE\par}
\vspace{12mm}
{\Huge\bfseries Collatz\par}
\vspace{3mm}
{\LARGE Research continuations\par}
\vspace{14mm}
{\Large Split-Zero comparisons, original arithmetic, and retained-source reductions\par}
\vspace{18mm}
{\large Complete recovered mathematical notes, with an additive all-even-exponent continuation\par}
\vfill
{\sffamily 16 September 2026\par}
{\small Original project: KokunoYumeto. Derivations, exposition, and executable checks in the continuations were developed in the respective tool-assisted sessions.\par}
\end{titlepage}
\chapter*{Archive scope and how to read it}
\addcontentsline{toc}{chapter}{Archive scope and how to read it}
This volume transcribes the full mathematical notes available in the fourteen
supplied continuation archives, adds four complete historical notes retrieved
from the pinned GitHub source, and adds the present all-even-exponent note.
The original Markdown, code, manifests, proof ledgers, and historical receipts
remain separately preserved in the accompanying ZIP. This is an anthology of
source versions, not a newly unified proof of Collatz.

The source-time publication and verification statements in each chapter are
retained. Some are now historical: PR 2 was merged on 16 September 2026, and the
main branch was read at commit
\texttt{9453b5306b3a897389dece309f9c119dffbcc489}.
No new GitHub publication is implied by this edition. Historical finite test
counts are not added into a claim of a new repository-wide mathematical audit.

The bundle is a cumulative archive of the supplied artifacts, not a complete
clone of every GitHub workbench file. Three additional historical directories
are pinned in \texttt{provenance/GITHUB\_ONLY.json}: the history-law,
anchored-period, and ternary-join checkpoints. Their four complete mathematical
notes were retrieved through the GitHub connection and checked byte-for-byte
against their Git blob identities. They are included in this volume and the
source overlay. Their other companion files were not supplied locally.
The accompanying \texttt{tools/fetch\_github\_sources.py} restores any missing
files in those exact pinned directories on a networked machine, without
overwriting an existing differing file. No placeholder is presented as missing
source code or evidence.

Every included chapter has a source locator and SHA-256 in
\texttt{latex/SOURCE\_MAP.json}. Formula text is preserved in per-chapter math
inventories. The typesetting conversion only extracts equation tags and scales
an overwide display to the available line width. One malformed source subscript is grouped as
$\mathbb Q\otimes_{\mathbb Z}Q$ in the presentation; the unchanged original
Markdown and the explicit typography correction record remain in the archive.
Original equation numbers are local to their source chapter. Original files, not the presentation conversion,
remain the archival record.

The current continuation is the final chapter. It proves complete common-future
families for every positive even interior exponent, corrects their ternary layer
through the exact identity $\nu_3((2^e+2)/3)=\nu_3(e-1)$, and makes template
membership a finite test at each original source. Its budget-preserving version
retains the predecessor's support bound. Unresolved roots remain represented.

\tableofcontents
\mainmatter
'''
(tex/'main.tex').write_text(front+'\n'.join(inputs)+'\n\\end{document}\n')
print('chapters',len(records),'math tokens',sum(r['math_tokens'] for r in records))
