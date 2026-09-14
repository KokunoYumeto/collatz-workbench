# Thue 1908--1909: the exact binary-form dependency in Pólya's proof

## Routing and controlling witnesses

Exact-title, author, journal, and theorem searches found no Axel Thue
manifestation in `state/index_routes.jsonl`, `state/document_routes.jsonl`, or
`state/index_snapshot.json`.  Targeted filename searches in the authorized OS,
used-often, and `arxiv_latex` roots also missed.  No frozen ledger was rebuilt
or mutated.

Two durable public-domain witnesses were therefore acquired:

1. Axel Thue, *Bemerkungen über gewisse Näherungsbrüche algebraischer
   Zahlen*, Videnskabs-Selskabets Skrifter, I. Math.-Naturv. Klasse
   (Christiania), 1908, no. 3, 34 pp.; and Axel Thue, *Om en generel i store
   hele tal uløsbar ligning*, the same series, 1908, no. 7, pp. 1--15.  Both
   occur in the complete Internet Archive/Biodiversity Heritage Library volume
   `skrifterudgivnea1908chri`, durably copied as
   `external_literature/dependency_gate_2026-08-25/thue_1908_skrifter_volume_bemerkungen_and_om_en_generel_bhl_ia.pdf`.
   The volume has 764 PDF pages, 44,033,661 bytes, and SHA-256
   `80444727aa7790eb52e833d3ed4e860e076bef73bd5ad3fe7e1bf4a555f394aa`.
   The stable item is
   `https://archive.org/details/skrifterudgivnea1908chri`.
2. Axel Thue, *Über Annäherungswerte algebraischer Zahlen*, *Journal für die
   reine und angewandte Mathematik* 135 (1909), 284--305,
   DOI `10.1515/crll.1909.135.284`.  The official SUB Göttingen/GDZ article
   scan is durably stored as
   `external_literature/dependency_gate_2026-08-25/thue_1909_ueber_annaeherungswerte_gdz.pdf`.
   It has 23 PDF pages including the repository cover, 22,332,142 bytes, and
   SHA-256
   `629f8fbe27376812abc44394a960e6ab343471764016c73e8b23e1d789f80b22`.
   The official direct PDF is
   `https://gdz.sub.uni-goettingen.de/download/pdf/PPN243919689_0135/LOG_0014.pdf`.

The controlling pages were rendered at 300 dpi and read visually.  In the
1908 volume, Thue I has its title at PDF p. 153 and Satz 12 at printed
pp. 30--31 / PDF pp. 182--183.  Thue II has its title at PDF p. 333 and the
opening theorem at printed p. 1 / PDF p. 335.  In the 1909 article, Theorem IV
starts at printed p. 303 / PDF p. 21 and completes at printed p. 304 / PDF
p. 22.

## A manifestation gap that must remain visible

Pólya cites Thue II, printed p. 3.  The complete-volume scan and an independent
National Library of Norway scan both jump from printed p. 1 to printed p. 4;
neither contains raster images of printed pp. 2--3.  Accordingly, this audit
does **not** claim direct visual verification of Thue II p. 3.  Three distinct
pieces of evidence control the dependency instead:

- Thue II printed p. 1 states the equivalent dehomogenized finite-solution
  theorem and its degree-one/degree-two power exceptions.
- Pólya 1918 printed pp. 144--145 gives the exact homogeneous formulation he
  uses and explicitly cites Thue II p. 3.
- Fabien Pazuki's close French translation, *Journal de Théorie des Nombres de
  Bordeaux* 27 (2015), 339--352, DOI `10.5802/jtnb.904`, reproduces the opening
  theorem.  It is supplementary corroboration, not a replacement primary
  witness.

The missing raster pages are a manifestation defect, not a license to invent
their typography or an unrecorded theorem.

## Thue III: irreducible forms and the quadrant extension

Theorem IV, printed pp. 303--304, states that

\[
 U(p,q)=c
\]

has not infinitely many solutions in positive integers \(p,q\) when \(c\) is
fixed and \(U\) is an integral homogeneous irreducible form of degree greater
than two.  The theorem as printed is a positive-quadrant theorem.  Its exact
extension to \(\mathbb Z^2\) is finite: for \(p,q\ne0\), write

\[
 (p,q)=(\epsilon P,\delta Q),
 \qquad (\epsilon,\delta)\in\{\pm1\}^2,
 \qquad P,Q\in\mathbb Z_{>0}.
\]

Each sign cell satisfies the Thue equation
\(U(\epsilon P,\delta Q)=c\).  Sign substitution preserves integrality,
homogeneity, degree, and irreducibility.  There are only four cells.  On an
axis, irreducibility in degree greater than one forces the relevant pure
coefficient to be nonzero; the equation is then \(u_d p^d=c\) or
\(u_0 q^d=c\), which has finitely many integer solutions.  Thus the all-integer
extension is proved without identifying signs or suppressing the axes.

This theorem alone is **not** sufficient for Pólya's proof.  His cubic may be
reducible over \(\mathbb Q\).

## Thue II and Pólya's exact exceptional-form classification

Thue II printed p. 1 says that, for \(f\in\mathbb Z[T]\) irreducible of degree
\(r>2\), the equation

\[
 q^r f(p/q)=c
\]

has finitely many integral pairs \((p,q)\).  For \(c\ne0\), it gives the more
general conclusion unless \(f\) is a power of an integral polynomial of
degree one or two.  Pólya prints the corresponding homogeneous contrapositive:
if a fixed nonzero-value equation for a binary form has infinitely many
integer solutions, then, up to a nonzero scalar, the form is a power of a
linear form or an indefinite quadratic form.  The adjective *indefinite* is
forced at fixed nonzero value because a definite quadratic has only finitely
many lattice points in a bounded level set.

For a cubic, the quadratic-power exception is impossible by degree.  The
remaining question in Pólya's proof is therefore literal: is his binary cubic
a scalar multiple of a linear cube?

## Pólya's residue-cell cubic, its map, and its nonexceptionality

In Pólya's Satz I proof, let the two essentially distinct integer linear forms
be \(an+b\) and \(cn+d\), with \(a,c\ne0\) and

\[
 \frac ba\ne\frac dc,
 \qquad
 \Delta=ad-bc\ne0.
\]

Suppose infinitely many of their products have prime support in a fixed set
\(S=\{p_1,\ldots,p_t\}\).  Reduce the two exponent vectors modulo three and
fix one of the finitely many residue cells.  In that cell write

\[
 an+b=R x^3,
 \qquad
 cn+d=S_0 y^3,
 \qquad
 R=\prod_{i=1}^t p_i^{r_i},
 \qquad
 S_0=\prod_{i=1}^t p_i^{s_i},
 \qquad 0\le r_i,s_i<3.
\]

Eliminating \(n\) gives exactly

\[
 G(x,y)=aS_0y^3-cRx^3=ad-bc=\Delta.
\]

The residue-cell map is lossless in the needed direction: a solution arising
from the cell recovers

\[
 n=\frac{Rx^3-b}{a}=\frac{S_0y^3-d}{c}.
\]

Hence distinct source integers \(n\) give distinct cubic solutions.  The
coefficients \(aS_0\) and \(cR\) are nonzero, and the standard binary-cubic
discriminant is

\[
 \operatorname{Disc}(G)=-27(aS_0)^2(cR)^2\ne0.
\]

More directly, suppose over a characteristic-zero field that
\(G=\lambda(uX+vY)^3\).  The nonzero \(X^3\) and \(Y^3\) coefficients force
\(\lambda,u,v\ne0\), while the absent \(X^2Y\) coefficient would require
\(3\lambda u^2v=0\), a contradiction.  Thus \(G\) is not a scalar linear
cube, whether or not it is irreducible over \(\mathbb Q\).  If
\(\Delta<0\), the involution

\[
 (G,\Delta,x,y)\longmapsto(-G,-\Delta,x,y)
\]

leaves the solution set and exceptional-form status unchanged and makes the
right-hand side positive.  Thue II/Pólya's classification therefore gives a
finite solution set in every residue cell, contradicting the assumed infinite
sequence.  This closes the exact dependency used by Pólya.

## Thue I, Satz 12

Satz 12, printed pp. 30--31, states that for prescribed \(h>0\) and nonzero
integer \(k\), sufficiently many pairwise distinct integers \(a_i\) force at
least one of

\[
 \prod_i a_i,
 \qquad
 \prod_i(a_i+k)
\]

to have more than \(h\) distinct prime divisors.  Its proof is the same
modulo-three template: bounded prime support would yield infinitely many
solutions to one fixed equation \(\alpha x^3-\beta y^3=k\).  Pólya cites Satz
12 for this proof pattern and then performs his own residue-cell construction.
Satz 12 is not an additional unproved premise of Pólya's Satz I.

## Dependency status and nonclaims

- Pólya's published fixed-prime gap theorem remains admitted at its exact
  printed scope.  Its explicit Thue proof dependency is now content-audited.
- Thue III is not represented as covering reducible cubics.  The Thue II
  classification is the controlling route for those cells.
- No effective upper bound for the integer solutions, no effective gap
  threshold, and no effective Pillai threshold is extracted.
- The unavailable raster of Thue II printed pp. 2--3 remains recorded as a
  source-manifestation gap.
- Fixed-difference finiteness is not Herschfeld's eventual uniqueness and
  proves no Collatz endpoint.
