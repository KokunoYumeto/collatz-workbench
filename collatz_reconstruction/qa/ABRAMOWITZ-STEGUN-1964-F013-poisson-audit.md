# Abramowitz--Stegun 1964: Crandall Lemma 6.1 dependency audit

## Identity, routing, and manifestation boundary

Crandall's reference 4 is printed as M. Abramowitz and I. Stegun (editors),
*Handbook of Mathematical Functions*, ninth printing, Dover, New York, 1965.
His remark after Lemma 6.1 says only that an exposition of various formulas
pertaining to the lemma occurs in that reference.  Crandall supplies no formula
number, section, or page.  Any exact formula identification below is therefore
an edition reconstruction, not a locator printed by Crandall.

The completed frozen Collatz route ledgers contain no Abramowitz--Stegun,
handbook, incomplete-gamma, error-function, or Poisson manifestation.  A
targeted filename repair in the authorized OS, used-often, and arxiv-library
roots also returned no exact local witness.  No frozen ledger was rescanned or
modified.

The primary identity is Milton Abramowitz and Irene A. Stegun, editors,
*Handbook of Mathematical Functions with Formulas, Graphs, and Mathematical
Tables*, National Bureau of Standards Applied Mathematics Series 55, issued
June 1964.  The NIST historical record controls this identity.  The complete
content witness is the Internet Archive facsimile contributed by the NIST
Research Library, identifier `handbookofmathem1964abra`:

- path:
  `external_literature/dependency_gate_2026-08-25/abramowitz_stegun_1964_nbs_ams55_ia_facsimile.pdf`;
- 1,082 PDF pages and 1,046 printed pages;
- 78,607,704 bytes;
- SHA-256
  `2e0205d8a35a0f544b7cd4f16fde91ba38f1527febedb37fbdc9b85a6e7b214a`;
- embedded IA metadata MD5 `fc93161892fe96594abb6839798602d0`
  and SHA-1 `a02261089cf681ed08f3e023a5967504e513aa61`.

The title page says only "Issued June, 1964".  The accompanying NBS errata
notice identifies that bare title-page form as the first printing.  This is not
silently represented as Crandall's cited ninth Dover printing.  The relevant
printed formula pages were also compared visually with the public UBC scan of
the tenth printing; the formulas used here agree at the inspected locations.
No claim of text identity between whole printings is required.

## Content read and exact locators

The following pages of the complete facsimile were rendered at 300 dpi and
read at original detail:

- PDF 294 / printed 262: 6.5.11 defines
  \(e_n(x)=\sum_{j=0}^{n}x^j/j!\); 6.5.13 identifies the corresponding
  finite exponential sum with the incomplete gamma function.
- PDF 295 / printed 263: 6.5.34 gives the fixed-\(\alpha\) transition
  \[
  \lim_{n\to\infty}\frac{e_n(\alpha n)}{e^{\alpha n}}
  =\begin{cases}0,&\alpha>1,\\[1mm]1/2,&\alpha=1,\\[1mm]1,&0\leq\alpha<1.
  \end{cases}
  \]
  Thus it directly supplies the integer diagonal
  \(e^{-n}e_n(n)\to1/2\), but not a moving-\(\alpha_n\) substitution.
- PDF 963 / printed 931: 26.2.1--26.2.6 define the normal density \(Z\),
  its lower and upper integrals \(P\) and \(Q\), and
  \(P(x)+Q(x)=1\), \(P(-x)=Q(x)\).  Hence \(P(0)=Q(0)=1/2\).
- PDF 966 / printed 934: 26.2.29 gives
  \(\operatorname{erf}x=2P(x\sqrt2)-1\) for \(x\geq0\), explaining the
  error-function language in Crandall's remark.
- PDF 972 / printed 940: 26.4.1--26.4.2 define the lower and upper
  chi-square probabilities \(P(\chi^2\mid\nu)\) and
  \(Q(\chi^2\mid\nu)=1-P(\chi^2\mid\nu)\), for
  \(0\leq\chi^2<\infty\).
- PDF 973 / printed 941: 26.4.11 prints the large-\(\nu\) normal
  approximation
  \[
  P(\chi^2\mid\nu)\sim P(z),\qquad
  z=\frac{\chi^2-\nu}{\sqrt{2\nu}},
  \]
  and 26.4.21 prints the exact Poisson identity, for even \(\nu\),
  \[
  Q(\chi^2\mid\nu)
    =\sum_{j=0}^{c-1}e^{-m}\frac{m^j}{j!},
  \qquad c=\frac\nu2,
  \qquad m=\frac{\chi^2}{2}.
  \]

The minimal exact handbook route is therefore 26.4.21 followed by 26.4.11,
with 26.2.2--26.2.6 fixing the normal notation.  The alternative pair
6.5.11 and 6.5.34 supplies only the integer diagonal directly.  It is invalid
to put \(\alpha_n=t/\lfloor t\rfloor\to1\) into 6.5.34 as though the printed
fixed-parameter limit were uniform: the displayed limiting function is
discontinuous at \(\alpha=1\).

## Exact coordinate identity

For \(n\in\mathbb N_0\) and \(t\geq0\), define
\[
 F_n(t)=e^{-t}\sum_{j=0}^{n}\frac{t^j}{j!}.
\]
Repeated integration by parts gives the literal identity
\[
 \Gamma(n+1,t)=n!e^{-t}\sum_{j=0}^{n}\frac{t^j}{j!},
\]
and A&S 26.4.21, with
\(\nu=2(n+1)\), \(\chi^2=2t\), gives
\[
 F_n(t)=\frac{\Gamma(n+1,t)}{\Gamma(n+1)}
       =Q(2t\mid2n+2).
\]
This is an exact identification, not a distributional approximation.  For
fixed \(n\),
\[
 F_n'(t)=-e^{-t}\frac{t^n}{n!}
\]
for \(t>0\); hence \(F_n\) is continuous and strictly decreasing from
\(F_n(0)=1\) to \(0\).  Its fixed-\(n\) fibres are singletons.  Across
different \(n\), no injectivity is claimed.

## Crandall's cutoff and the repaired theorem cutoff

The high-resolution source raster controls the relation sign in Crandall
Lemma 6.1.  It is a strict inequality, not a less-than-or-equal sign.  The
printed statement is
\[
 \lim_{t\to\infty}e^{-t}
 \sum_{\substack{u\in\mathbb Z_{>0}\\u<\lfloor t\rfloor}}
 \frac{t^u}{u!}=\frac12.
\]
The term \(u=0\) omitted by Crandall has mass \(e^{-t}\to0\).

Put \(n=\lfloor t\rfloor\), \(\nu=2n\), and \(\chi^2=2t\).  Formula
26.4.21 makes the sum including \(u=0,\ldots,n-1\) exactly
\(Q(\chi^2\mid\nu)\), while the standardized variable in 26.4.11 is
\[
 \frac{\chi^2-\nu}{\sqrt{2\nu}}
 =\frac{t-n}{\sqrt n}\longrightarrow0.
\]
Together with \(P(0)=Q(0)=1/2\), this is the exact handbook route to the
printed lemma.

Crandall Theorem 5.1 authorizes the height estimate only for
\(h<t=r\log_2x\).  Therefore the exact integer range in Theorem 6.1 is
\[
 1\leq h\leq\lceil t\rceil-1.
\]
The source's proof instead displays a sum through \(\lfloor t\rfloor\), which
adds the unauthorized equality term precisely when \(t\) is an integer.
Crandall's strict-cutoff Lemma 6.1 is already a lower sub-sum of the authorized
range for every real \(t\), so dropping the displayed endpoint repairs the
argument.  The sharper uniform repaired cutoff is
\(k(t)=\lceil t\rceil-1\); for it, take
\(\nu=2(k(t)+1)=2\lceil t\rceil\).  Its standardized variable is
\[
 \frac{t-\lceil t\rceil}{\sqrt{\lceil t\rceil}}\longrightarrow0,
\]
so the same half-mass limit holds.  This repairs the application, not the
statement of Lemma 6.1.

## Controlling analytic completion

A&S 26.4.11 is a telegraphic asymptotic formula on the displayed page: it
does not print an error term or a proof there.  The edition therefore keeps a
separate proof for the all-real cutoff rather than silently treating an
unwritten uniformity statement as supplied.

Let \(X_t\) be Poisson with mean \(t\) and
\(Y_t=(X_t-t)/\sqrt t\).  For fixed real \(s\),
\[
 \mathbb E e^{isY_t}
 =\exp\!\left(t\left(e^{is/\sqrt t}-1-is/\sqrt t\right)\right)
 =\exp\!\left(-\frac{s^2}{2}+O_s(t^{-1/2})\right).
\]
Lévy's continuity theorem gives \(Y_t\Rightarrow N(0,1)\).  More generally,
if \(k(t)\in\mathbb Z\) and \((k(t)-t)/\sqrt t\to0\), then, for every
fixed \(\delta>0\) and all sufficiently large \(t\),
\[
 \Pr(Y_t\leq-\delta)
 \leq \Pr\!\left(Y_t\leq\frac{k(t)-t}{\sqrt t}\right)
 \leq \Pr(Y_t\leq\delta).
\]
Taking lower and upper limits and then \(\delta\downarrow0\) gives
\[
 e^{-t}\sum_{u=0}^{k(t)}\frac{t^u}{u!}\longrightarrow\frac12.
\]
The source cutoff \(k(t)=\lfloor t\rfloor-1\), the adjacent endpoint
\(k(t)=\lfloor t\rfloor\), and the repaired theorem cutoff
\(k(t)=\lceil t\rceil-1\) all satisfy the hypothesis.  Removing \(u=0\)
changes any expression by exactly \(e^{-t}\).  This proof invokes Lévy's
continuity theorem explicitly; it is not described as elementary or
dependency-free.

## Consequence and nonclaims

For the repaired height range,
\[
 \pi(x)>(1/2-d)e^{r\log_2x}
        =(1/2-d)x^{r/\log2}
\]
eventually for each fixed \(0<d<1/2\).  The fixed prefactor is below one, so
the argument gives every \(c<r/\log2\), not the endpoint exponent
\(c=r/\log2\).  The already proved edition witness \(c=1/100\) is unchanged.

- No finite Poisson sum is asserted to equal \(1/2\).
- No convergence rate is imported from Crandall or A&S.
- A&S's identified formulas are not represented as numbers printed by
  Crandall.
- The NBS first-printing facsimile is not represented as the ninth Dover
  printing in Crandall's bibliography.
- The power-law lower count may have density zero and proves no
  almost-everywhere convergence to 1.
- Closing this handbook dependency does not close the remaining Pillai,
  Herschfeld, primitive-root, continued-fraction, or historical-computation
  dependencies in PO-COL-000008.
