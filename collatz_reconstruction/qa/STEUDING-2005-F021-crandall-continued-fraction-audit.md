# Steuding--Crandall continued-fraction dependency audit

Checkpoint: `ACT-COL-000026` (to be appended after the propagated state update).

## Source identities and route boundary

The imported continued-fraction facts occur in Richard E. Crandall, “On the
\(3x+1\) Problem,” *Mathematics of Computation* 32 (1978), 1281--1292,
printed pp. 1289--1290.  Crandall labels the relevant assertions Lemmas 7.1
and 7.2 and says that the relevant material is in references 6 and 7 (J.
Roberts, *Elementary Number Theory--A Problem Oriented Approach*, 1977, and
Y. A. Khinchin, *Continued Fractions*, 1964).  The exact frozen route ledgers
contain no manifestation of either cited book.  No claim is therefore
attributed to an unread Roberts or Khinchin copy.

The independently read published support source is Jörn Steuding,
*Diophantine Analysis*, Discrete Mathematics and Its Applications, CRC
Press/Taylor & Francis Group, 2005 (eBook PDF version date 2011-07-13,
ISBN 978-1-4200-5720-1).  The controlling local manifestation is
`C:/Users/LOCAL_USER/Documents/Papors/OS/Mason-Stothers theorem/Diophantine Analysis (Jorn Steuding).pdf`,
2,257,201 bytes, SHA-256
`ea31b76c5c400f91b23038885c3576224496457633be84bcc22d335e3e323b88`.
The byte-identical `used often` manifestation has the same hash.

The Steuding pages were read from the PDF at original detail: physical pp.
51--54 (printed pp. 38--41), physical pp. 55--60 (printed pp. 42--47).  The
ten 300-dpi page witnesses are retained under
`tmp/steuding_cf_source_qa_20260826/`.
The controlling statements are Theorems 3.1 and 3.2 (printed p. 38), Theorem 3.6
and Corollary 3.7 (printed pp. 42--43), and Theorem 3.8 (printed pp. 44--45).
The latter is the law of best approximations with the exact hypotheses
\(n\ge 2\), positive integers \(p,q\), \(0<q\le q_n\), and
\(p/q\ne p_n/q_n\).

## Exact transfer used by the edition

Put \(t=\log_2 3\).  It is irrational: if \(t=a/b\) with integers
\(a\) and \(b>0\), then \(2^a=3^b\), which is impossible by unique
factorization (the cases \(a\le0\) are immediate as well).  Thus the infinite
simple continued fraction and its convergents exist.  With
\(p_{-1}=1,q_{-1}=0,p_0=a_0,q_0=1\), Steuding's recurrence gives
\[
p_n=a_np_{n-1}+p_{n-2},\qquad q_n=a_nq_{n-1}+q_{n-2}.
\]
The determinant identity gives
\(p_nq_{n-1}-p_{n-1}q_n=(-1)^{n-1}\), so each convergent is reduced.

Steuding Theorem 3.6 gives, with the complete tail \(\alpha_{n+1}),
\[
t-\frac{p_n}{q_n}
 =\frac{(-1)^n}{q_n(\alpha_{n+1}q_n+q_{n-1})}.
\]
Since \(a_{n+1}<\alpha_{n+1}<a_{n+1}+1\), this implies the two-sided
bound used by Crandall:
\[
\frac1{q_n+q_{n+1}}
 < |p_n-q_nt| < \frac1{q_{n+1}}.
\]
The lower inequality is strict because the complete tail is strictly less
than \(a_{n+1}+1\); the upper inequality uses \(\alpha_{n+1}>a_{n+1}\).

For \(0<y<q_n\) and an integer \(x>0\), Theorem 3.8 applied to
\(p=x,q=y\) yields
\[
|p_n-q_nt|<|x-yt|,
\]
because reducedness of \(p_n/q_n\) makes \(x/y=p_n/q_n\) impossible when
\(y<q_n\).  If an integer \(x\le0\) is retained in the statement, then
\(|x-yt|\ge yt>1>|p_n-q_nt|\), so the same inequality follows directly.
This proves the exact typed version needed for the positive cycle coordinate
\(x=A_k\), without silently changing the source's variables.

The printed proof's unsupported equality boundary is separate.  For \(n\ge4\), the upper bound
above gives \(|p_n-q_nt|<1/2\).  If \(y=q_n\) and \(x\ne p_n\), integrality
gives \(|x-p_n|\ge1\), hence \(|x-q_nt|>|p_n-q_nt|\).  If \(x=p_n\),
the best-approximation comparison is equality, but the cycle's positive
logarithmic gap supplies the strict exponential inequality directly.

## Exponential inequality and cycle substitution

For \(0<y<q_n\) and \(x-yt>0\), set
\(u=(x-yt)\log 2>0\).  The positive-term expansion
\(e^u-1-u=\sum_{j\ge2}u^j/j!>0\) gives
\[
|2^x-3^y|=3^y(e^u-1)
 >3^y\log2\,|x-yt|
 >3^y\log2\,|p_n-q_nt|.
\]
The first strict inequality is why the negative-gap case is not imported
from Crandall's printed Lemma 7.3.  In a positive Crandall return,
\(x=A_k\), \(y=k\), and
\(2^{A_k}-3^k>0\) by the exact return equation, so the hypotheses are
typed rather than inferred from a picture.

Combining this with the repaired Lemma 7.5 estimate, put
\(v=1/(3m)>0\).  The function \(f(v)=(1+v)^{-k}\) has
\(f''(v)=k(k+1)(1+v)^{-k-2}>0\), so strict convexity above the tangent at
zero gives \(f(v)>f(0)+f'(0)v=1-kv\).  Substitution yields the edition's
intermediate bound
\[
k>m(\log2)(3+1/m)|p_n-q_nt|\left(1-\frac{k}{3m}\right).
\]
When \(k<m/10\), the last factor is strictly greater than \(29/30\).
The final comparison also uses \(\log2>56/81>20/29\).  When
\(k\ge m/10\), the second entry \(2m/(q_n+q_{n+1})\) is strictly below
\(m/10\le k\), since \(q_n+q_{n+1}>20\).  This proves Crandall's printed
range
\[
k>\min\left\{q_n,\frac{2m}{q_n+q_{n+1}}\right\}
\qquad(n\ge4)
\]
with every sign and equality boundary exposed.  The page-image witness
controls here: OCR drops the bars from both printed occurrences of
\(\ge\) in Theorem 7.2 and its proof.

## Historical numerical boundary

The continued-fraction recurrence gives
\(q_{10}=31867\), \(q_{11}=79335\), and hence
\[
\frac{2\cdot10^9}{q_{10}+q_{11}}>17985.
\]
Crandall printed p. 1282 cites references [1] and [5] for verification of
Conjecture (2.1) below \(10^9\); printed p. 1290 uses the corresponding
self-return exclusion without a new inline citation.  Those routes are now
resolved as a single work: Crandall [5] misprints Zbl 0337.10041, the record
for Conway [1], as ``Band 233, p. 10041,'' and 10041 is an accession suffix.
Conway's content-read first page reports ordinary-map verification for the
inclusive range \(n\le10^9\) by D. H. Lehmer, Emma Lehmer, and J. L.
Selfridge, but supplies no citation, code, algorithm, machine, partition,
stopping criterion, independent check, checksum, log, or output.  The exact
odd-return morphism proves that this ordinary-map report implies the
accelerated self-return exclusion.  It does not authenticate the underlying
computation.  The inclusive report directly forces a hypothetical cycle
minimum \(m_0>10^9\); Crandall's strict-range form plus odd parity gives the
same boundary, equivalently \(m_0\ge1{,}000{,}000{,}001\).  The
accelerated least-period bound remains \(\ell>17985\).  The finite certificate
checks the arithmetic and parity implication, not the historical computation.

## Status and nonclaims

The continued-fraction dependency is closed at the exact scope used in the
repaired Crandall cycle theorem by a published, content-read source and the
displayed independent derivation.  The edition does not identify Steuding's
orbit-digit continued fraction with Crandall's continued fraction for
\(\log_2 3\), and it does not import Steuding's Exercise 5.22 as a proof of
the Collatz conjecture.  The cycle bound still does not exclude a nontrivial
cycle, prove convergence, or validate the historical \(10^9\) computation as
a modern exhaustive record.

Certificate: `certificates/continued_fraction_dependency_checks.py`.  It
uses no floating-point logarithm: a 141-term positive
`2*atanh((x-1)/(x+1))` series with an exact geometric-tail bound encloses
`log(2)` and `log(3)`, then all prefix, error, closest-competitor,
equal-denominator, parity, and historical-bound checks use rational or integer
arithmetic.
