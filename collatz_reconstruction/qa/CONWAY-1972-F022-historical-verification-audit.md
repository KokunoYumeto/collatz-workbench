# Conway 1972 historical-verification audit (F022)

## Identity and manifestation boundary

- Canonical work: J. H. Conway, “Unpredictable iterations,” in *Proceedings
  of the 1972 Number Theory Conference*, University of Colorado, Boulder,
  1972, pp. 49–52.
- Authoritative machine identity: zbMATH document 3526785,
  **Zbl 0337.10041**.  The pinned API response is
  `tmp/source_inspection_conway_1972_20260826/zbmath_document_3526785.json`,
  1,270 bytes, SHA-256
  `04ee3fd45574b476c3978476264e262056a137319d7fdb2d7db71a43ac1b72ea`.
- Content-readable manifestation: the five-page 2010 AMS reprint extract,
  reprint pp. 219–223, inspected from a third-party host.  Local inspection
  copy:
  `tmp/source_inspection_conway_1972_20260826/conway_1972_unpredictable_iterations_ams2010_reprint_inspection.pdf`,
  172,046 bytes, five PDF pages, SHA-256
  `b8cb28578dd2b125235c827e9b4e37e0a1ef0252c83da62d40551f6885ca9bf2`.
  This is a copyrighted inspection manifestation, not an original 1972
  proceedings scan and not evidence of an official open-access or
  redistribution licence.  No source text is bulk-copied into the edition.
- Reprint boundary: Conway's original text occupies reprint pp. 219–221.
  Editorial commentary begins on the lower part of p. 221 and continues
  through pp. 222–223.  All five pages were rendered at 300 dpi and read;
  the original/article and later/editorial layers are not conflated.
- Routing history: exact searches of the immutable route ledgers and a
  targeted authorized-root filename search found no manifestation.  The
  frozen ledgers were neither rebuilt nor mutated.

## What the article reports

On reprint p. 219 (original proceedings p. 49), Conway defines

\[
 g(n)=\begin{cases}n/2,&n\text{ even},\\3n+1,&n\text{ odd},\end{cases}
\]

and formulates reaching 1 under an iterate of this ordinary one-step map.
He then reports the **inclusive** verification range (n\le10^9) and
attributes the computation to **D. H. Lehmer, Emma Lehmer, and J. L.
Selfridge**.  The displayed map is literally the edition's unshortened map
(U); it is not Crandall's accelerated odd first-return map.

The sentence supplies no citation, date, institution, computer, program,
algorithm, range partition, stopping criterion, independent replication,
checksum, log, output, or preserved data.  No underlying Lehmer–Lehmer–
Selfridge computation paper was located in this targeted repair.  The typed
status is therefore:

> published contemporaneous assertion and attribution verified; underlying
> computation record not located and reproducibility open.

Conway's theorem concerns generalized periodic-ratio maps.  Near the end of
his original text on reprint p. 221, he explicitly says that the theorem says
nothing about the particular Collatz game.  The (10^9) report is background
computational evidence, not a proved consequence of the theorem.

## Exact ordinary-to-accelerated transfer

Let (N\in\mathbb N_{>0}), and assume that every ordinary orbit starting at
(1\le n\le N) reaches 1.  For an odd (m\le N), let
(e_i=v_2(3C_{mathrm{Cr}}^i(m)+1)) and
(A_j=\sum_{i<j}e_i).  The already proved first-return morphism gives

\[
 C_{mathrm{Cr}}^j(m)=U^{A_j+j}(m).
\]

The states on the left are exactly the successive odd states of the ordinary
orbit.  Since 1 is odd, an ordinary occurrence (U^r(m)=1) is one of these
odd returns, so (C_{mathrm{Cr}}^j(m)=1) for some (j).  Because
(C_{mathrm{Cr}}(1)=1), an accelerated self-return
(C_{mathrm{Cr}}^k(m)=m>1) would be periodic from (m) and could not enter
1.  Hence ordinary verification through (N) implies accelerated
self-return exclusion for every odd (1<m\le N).  The proof preserves both
clocks and supplies the exact variable-time map; it does not identify their
step counts.

At (N=10^9), Conway's inclusive report directly gives a hypothetical cycle
minimum (m_0>10^9).  Crandall's weaker strict form (1<m<10^9), together
with the fact that (m_0) is odd while (10^9) is even, independently gives
the same endpoint (m_0\ge1{,}000{,}000{,}001).

## Repair of Crandall references [1] and [5]

Crandall reference [1] identifies Conway's paper but gives pp. 45–52; the
canonical proceedings range is pp. 49–52.  Reference [5] prints
“Zentralblatt für Mathematik, Band 233, p. 10041.”  The official zbMATH
record shows that the intended identifier is **Zbl 0337.10041**, again
Conway's paper.  Thus:

- `233` is a defective rendering of the volume/accession prefix `0337`;
- `10041` is the identifier suffix, not a printed page;
- reference [5] does not identify a second publication or computation; and
- references [1] and [5] collapse to one logical work but retain their two
  distinct defective printed presentations in the source audit.

## Consequences and nonclaims

- The source identity, inclusive endpoint, named attribution, and exact clock
  transfer are closed at content level.
- Crandall's conditional (k>17985) accelerated-period conclusion may be
  based on the published report at its historical scope.
- The report is not a modern exhaustive-verification record and has no
  reproducible certificate in the located source.
- The audit does not assert that the underlying computation record never
  existed; it records that none was located.
- The computation does not prove the Collatz conjecture beyond its finite
  enumerated range, exclude all nontrivial cycles, or establish convergence.
- Conway's generalized undecidability theorem is not projected onto the
  particular Collatz map.
