# Actual Collatz history laws: exact counting and a Gaussian total-variation threshold

**Date:** 14 September 2026. **Status:** written mathematical continuation with independently implemented exact finite checks; not an independent external review or a proof of Collatz convergence.

**Working repository:** `KokunoYumeto/collatz-workbench`. **Source revision:** `63407034387466870f9e092dcdf39fb5a1ec0399`.

This note continues the *Collatz* manuscript `collatz_reconstruction/research_program/split_zero_history_20260913/note.tex`, especially its exact odd-return cylinder lemma, finite spectral reconstruction theorem, and closing distinction between encoding a distribution and estimating it. No source in the zeta repository is changed or needed to run this contribution. The separate earlier web-session integral-extension package is not incorporated or certified here.

The contribution is an explicit finite-sample law comparison, including a matching information-theoretic obstruction and its Gaussian transition, followed by an offset-preserving first-descent counter. The underlying cylinder coding and geometric comparison belong to the established literature and the existing workbench. In particular, Tao's Proposition 1.9 and Section 4 already use the same cylinder/binomial-count mechanism. This note makes no global priority claim for its deductions.

## 1. The same map, with an actual sampling measure

Use the odd-return map

\[
T(n)=\frac{3n+1}{2^{\nu_2(3n+1)}}\qquad(n\text{ positive and odd}).
\]

Fix integers \(N\ge1\), \(b\ge0\), and \(m\ge1\). Choose the starting integer uniformly from

\[
I_{N,b}=\{2b+1,2b+3,\ldots,2(b+N)-1\}.
\]

The interval contains exactly \(N\) odd integers; \(N\) is not its upper endpoint. All statements below are uniform in its location \(b\), even when \(b\) varies arbitrarily with \(N\).

Let \(P_{N,b,m}\) be the probability law of the **whole chronological word**

\[
(a_1,\ldots,a_m),\qquad a_i=\nu_2(3T^{i-1}(n)+1).
\]

The comparison law on \(\mathbb N_{>0}^m\) is

\[
G_m(w)=2^{-A(w)},\qquad A(w)=a_1+\cdots+a_m.
\]

It is the product of \(m\) geometric laws with \(\Pr(a=j)=2^{-j}\), mean 2 and variance 2. This is a *comparison* law: independence is not imposed on the actual finite-integer sample.

Throughout,

\[
\Delta(P,G)=\frac12\sum_w|P(w)-G(w)|=\sup_E|P(E)-G(E)|.
\]

Tao's V7 equation (1.9) uses the full sum, twice this convention. The Gaussian limit below is therefore \(2\Phi(2c)\) in that convention.

## 2. Exact cylinders and exact counts

Write \(A_j=a_1+\cdots+a_j\), \(A_0=0\), and retain the original affine numerator

\[
B_w=\sum_{j=0}^{m-1}3^{m-1-j}2^{A_j}.
\]

The chronological branch product is

\[
T_w(x)=\frac{3^m x+B_w}{2^{A_m}}.
\]

Let \(r_w\) be the unique odd integer in \([1,2^{A_m+1})\) satisfying

\[
3^m r_w+B_w\equiv2^{A_m}\pmod{2^{A_m+1}},
\qquad h_w=(r_w-1)/2.
\]

**Lemma 2.1 (original exact cylinder, including the last oddness bit).** A positive odd integer \(n=2j+1\) has exponent word \(w\) if and only if

\[
j\equiv h_w\pmod{2^{A_m}}.
\]

**Proof.** For one exponent the congruence says precisely that \((3n+1)/2^{a_1}\) is an odd integer, so the valuation is exactly \(a_1\). For a longer word,
\(B_w=3^{m-1}+2^{a_1}B_{w'}\). The congruence first forces \(2^{a_1}\mid 3n+1\). Divide by this power and put \(y=(3n+1)/2^{a_1}\). The resulting suffix congruence is

\[
3^{m-1}y+B_{w'}\equiv2^{A_m-a_1}\pmod{2^{A_m-a_1+1}}.
\]

Because the suffix has positive length, its right side is even and \(B_{w'}\) is odd, forcing \(y\) odd. Induction establishes all exact exponents, including the last. Reversing these steps proves necessity. The original coefficient \(3^m\) is odd, hence invertible modulo the displayed power of two. Positivity is preserved by every actual step. Substituting \(n=2j+1\) gives the stated modulus in \(j\). This is the same cylinder lemma as in the predecessor, rederived to fix the sampling convention. \(\square\)

It follows that the number of occurrences of \(w\) in \(I_{N,b}\) is exactly

\[
C_{N,b}(w)=
\left\lfloor\frac{b+N-1-h_w}{2^{A_m}}\right\rfloor
-\left\lfloor\frac{b-1-h_w}{2^{A_m}}\right\rfloor. \tag{2.1}
\]

In particular it is either \(\lfloor N2^{-A_m}\rfloor\) or \(\lceil N2^{-A_m}\rceil\), and

\[
|P_{N,b,m}(w)-2^{-A_m}|\le\frac1N. \tag{2.2}
\]

No equidistribution theorem with a fixed modulus is being reused for a moving modulus: (2.1) is an exact interval count for every modulus and every interval location.

## 3. A finite, fully explicit total-variation envelope

For \(H\ge0\), define

\[
K_m(H)=\begin{cases}\binom Hm,&H\ge m,\\0,&H<m,\end{cases}
\qquad
Q_m(H)=2^{-H}\sum_{j=0}^{\min(m-1,H)}\binom Hj.
\]

There are exactly \(K_m(H)\) positive words with \(A_m\le H\): sum \(\binom{A-1}{m-1}\) over \(m\le A\le H\). Under \(G_m\),

\[
G_m(A_m>H)=Q_m(H). \tag{3.1}
\]

Indeed, independent fair Bernoulli trials have geometric waiting times between successes; the \(m\)-th success occurs after time \(H\) precisely when the first \(H\) trials have at most \(m-1\) successes. Equivalently (3.1) follows from the finite negative-binomial sum. This also handles \(H<m\), where the answer is 1.

**Theorem 3.1 (uniform finite-sample sandwich).** For all \(N,b,m,H\) as above,

\[
\boxed{
\max\{0,Q_m(H)-N2^{-(H+1)}\}
\le\Delta(P_{N,b,m},G_m)
\le\min\{1,Q_m(H)+K_m(H)/N\}.
} \tag{3.2}
\]

Different values of \(H\) may be chosen for the two bounds, or each side may be optimized over all \(H\).

**Proof.** For any two discrete probabilities,
\(\Delta(P,G)=1-\sum_w\min(P(w),G(w))\). On the \(K_m(H)\) words of total exponent at most \(H\), (2.2) gives

\[
\sum_w\min(P(w),G(w))\ge1-Q_m(H)-K_m(H)/N.
\]

This proves the upper bound. Let \(F\) be the actual support of \(P\). There are at most \(N\) words in \(F\), because there are only \(N\) sampled starting integers. Each atom with \(A_m>H\) has \(G\)-mass at most \(2^{-(H+1)}\). Thus

\[
G(F)\le1-Q_m(H)+N2^{-(H+1)}.
\]

The event \(F^c\) has \(P\)-mass zero, and yields the lower bound. This step concerns the actual labelled word, not a projection to a spectrum or an affine multiplier. \(\square\)

### Sharper finite versions

Rounding rather than absolute discrepancy gives

\[
\Delta(P_{N,b,m},G_m)\le
\min\left\{1,Q_m(H)+\frac1N\sum_{A=m}^{H}
\binom{A-1}{m-1}\{N2^{-A}\}\right\}, \tag{3.3}
\]

where braces denote fractional part. To prove it use \(P(w)\ge\lfloor N2^{-A}\rfloor/N\) in the overlap formula. Every term is an explicit rational number; an empty sum is zero.

There is also a sharp bound from support cardinality alone. Let \(h_*\ge m-1\) be the largest integer with \(K_m(h_*)\le N\). Then

\[
\Delta(P_{N,b,m},G_m)\ge
Q_m(h_*)-\bigl(N-K_m(h_*)\bigr)2^{-(h_*+1)}. \tag{3.4}
\]

The \(N\) largest atoms of \(G_m\) consist of every word of exponent sum at most \(h_*\), followed by \(N-K_m(h_*)\) words of sum \(h_*+1\). No set of at most \(N\) atoms has larger mass. Taking its complement proves (3.4); thus it is optimal when only that support-size information is used, not a claim of optimality among Collatz samples.

For a dyadic sample size \(N=2^L\), every cylinder with \(A_m\le L\) has exactly its geometric probability. A cylinder with \(A_m>L\) contains at most one sampled starting integer. Hence

\[
\boxed{
\Delta(P_{2^L,b,m},G_m)=Q_m(L)
-\sum_{\substack{w\in\operatorname{supp}P_{2^L,b,m}\\A(w)>L}}2^{-A(w)}.
} \tag{3.5}
\]

In particular \(\Delta\le Q_m(L)\), uniformly in \(b\). This is an exact formula with an actual finite observed-support sum, not a normal approximation.

## 4. The sharp growing-history transition

Let \(L_N=\log_2N\), and let \(\Phi\) denote the standard normal cumulative distribution function.

**Theorem 4.1 (Gaussian critical window).** For every fixed real \(c\), put

\[
m_N=\left\lfloor\frac{L_N}{2}+c\sqrt{L_N}\right\rfloor.
\]

Then, as \(N\to\infty\),

\[
\boxed{
\sup_{b\ge0}\left|\Delta(P_{N,b,m_N},G_{m_N})-\Phi(2c)\right|\longrightarrow0.
} \tag{4.1}
\]

Thus the whole-word geometric model tends to total variation 0 below \((1/2-\varepsilon)\log_2N\), and to total variation 1 above \((1/2+\varepsilon)\log_2N\). The latter statement obstructs full-history approximation, not the usefulness of any particular coarser statistic.

**Proof of the critical window.** Choose \(a_N=L_N^{1/4}\),
\(H_- =\lfloor L_N-a_N\rfloor\), and
\(H_+=\lceil L_N+a_N\rceil\). For large \(N\), these are nonnegative. Since \(K_m(H)\le2^H\), (3.2) gives

\[
Q_{m_N}(H_+)-2^{-a_N-1}
\le\Delta(P_{N,b,m_N},G_{m_N})
\le Q_{m_N}(H_-)+2^{-a_N}. \tag{4.2}
\]

The errors are independent of \(b\). If \(Y_H\) is binomial with parameters \((H,1/2)\), then

\[
Q_m(H)=\Pr\left(\frac{2Y_H-H}{\sqrt H}
\le\frac{2m-2-H}{\sqrt H}\right).
\]

The centered normalized variable converges in distribution to a standard normal. In this special case its characteristic function is exactly
\((\cos(t/\sqrt H))^H\), which tends to \(e^{-t^2/2}\), since
\(\log\cos u=-u^2/2+O(u^4)\). The continuity theorem for characteristic functions gives the asserted distributional limit. For both \(H_\pm\), the threshold on the right tends to \(2c\), because \(a_N=o(\sqrt{L_N})\). Continuity of \(\Phi\) and (4.2) complete the proof, uniformly in \(b\). \(\square\)

**Explicit off-critical estimates.** If \(0<\varepsilon<1/2\) and
\(1\le m\le(1/2-\varepsilon)L_N\), then, for sufficiently large \(N\),

\[
\Delta(P_{N,b,m},G_m)
\le N^{-\varepsilon}+N^{-\varepsilon^2/(2\log 2)}. \tag{4.3}
\]

Here \(\log2\) is the natural logarithm of 2. Take
\(H=\lfloor(1-\varepsilon)L_N\rfloor\). The counting term is at most \(N^{-\varepsilon}\), and
\(H/2-(m-1)\ge\varepsilon L_N/2+1/2\). For a fair binomial variable,
\(\Pr(Y_H-H/2\le-d)\le e^{-2d^2/H}\); since \(H\le L_N\), the tail is at most \(e^{-\varepsilon^2 L_N/2}\).

For \(m\ge(1/2+\varepsilon)L_N\), set
\(H=\lceil(1+\varepsilon)L_N\rceil\). When \(\varepsilon L_N>1\),

\[
1-\Delta(P_{N,b,m},G_m)
\le \frac12N^{-\varepsilon}
+\exp\left(-\frac{2(\varepsilon L_N/2-1/2)^2}{H}\right). \tag{4.4}
\]

This follows from the lower half of (3.2) and the upper binomial tail \(\Pr(Y_H\ge m)\). If \(m>H\), that tail is simply zero, and the displayed bound remains valid. The binomial tail inequality used in both estimates follows directly from Markov's inequality and
\(\mathbb E e^{t(Y_H-H/2)}=(\cosh(t/2))^H\le e^{Ht^2/8}\), optimizing at \(t=4d/H\). No untracked large-deviation constant is needed.

The clocks remain explicit: \(m\) counts odd returns; \(A_m\) counts divisions by two, or shortened-map steps; the corresponding full-map clock is \(m+A_m\). The threshold is stated in the first clock, not silently transported to another.

## 5. What the predecessor's spectral reconstruction now receives

Fix \(m,H\). Retain all words \(W_{m,\le H}\) and add one **overflow label** \(\partial\) for \(A_m>H\). The actual finite probability vector is

\[
p_w=C_{N,b}(w)/N,\qquad
p_\partial=1-\sum_{w\in W_{m,\le H}}p_w.
\]

The comparison vector has masses \(g_w=2^{-A(w)}\), \(g_\partial=Q_m(H)\). Overflow is not discarded or renormalized away. The coarse-graining is deterministic, so its total variation is at most (3.2) or (3.3). The same bound controls the expectation error for **every** function \(f\) on words with \(0\le f\le1\), including simultaneous congruences or prime-power divisibility tests on the same \(B_w\). Those tests need not be independent, and their moduli may vary. Positivity \(2^{A(w)}-3^m>0\) must still accompany the positive integral-cycle predicate.

For the finite spectral map choose the original integer node \(r_w\) for each retained word and node 0 for overflow. Nodes remain distinct even across different sums \(A\): an equality \(r_w=r_v>0\) would give that very positive integer two different actual length-\(m\) histories, contradicting uniqueness of iteration. Also \(r_w<2^{H+1}\), and no such node is zero.

There are \(K_m(H)+1\) nodes, including overflow. The Hurwitz family is

\[
Z_p(s,t)=p_\partial\zeta(s,1)+\sum_{w\in W_{m,\le H}}p_w\zeta(s,1+tr_w).
\]

Its mass is one and its unchanged displacement coordinate obeys
\(|t|(2^{H+1}-1)<1\). The predecessor's full-cluster inverse, retaining every multiplicity of its chosen nontrivial zeta zero, determines moments through order \(K_m(H)\) from that cluster jet. Lagrange interpolation on these distinct nodes then reconstructs every mass, including overflow. In the degenerate case \(H<m\), only overflow remains, with weight one and no jet needed. This is an application of the proved finite construction, not a claim that a zero branch can be computed without the original distribution.

Supported zero weights and absent labels remain different: all displayed labels are retained even when their sample count is zero. A separate retained-label mask cannot be reconstructed from their zero masses alone. No analytic conditioning estimate for the inverse jet map follows from the total-variation estimate. For an individual polynomial observable, a moment-error bound is the sum of the absolute interpolation coefficients times the corresponding moment errors; those potentially large coefficients cannot be suppressed.

The new arithmetic input is (2.1), (3.2), and (4.1), rather than another encoding of unspecified weights. Conversely, invertible spectral encoding cannot repair the full-word obstruction above the threshold. Noninvertible observations may behave much better and must be investigated using their actual fibres.

## 6. Exact first-descent certificates with the additive term retained

The statistical theorem concerns distributions of words. First descent additionally depends on the starting integer within its cylinder. For a prefix \(w_{[1,j]}\), set

\[
B_j=\sum_{i=0}^{j-1}3^{j-1-i}2^{A_i},\qquad D_j=2^{A_j}-3^j.
\]

On the actual cylinder,

\[
T^j(n)<n\iff D_j>0\ \text{and}\ n>B_j/D_j.
\]

Define

\[
\tau(w)=\min_{1\le j\le m:D_j>0}\left\lfloor B_j/D_j\right\rfloor,
\]

with \(\min\varnothing=+\infty\). Then **no strict descent below the starting value during the first \(m\) odd returns is equivalent to \(n\le\tau(w)\)**.

This follows by taking the conjunction of the exact inequalities for every prefix. A nonpositive \(D_j\) cannot give descent because \(n,B_j>0\). Equality is not descent. In particular, the word \((2)\) at \(n=1\) has multiplier \(3/4<1\) but returns to 1; the additive term cannot be deleted.

Let

\[
U_w=\min\{b+N-1,\lfloor(\tau(w)-1)/2\rfloor\},
\]

with the infinite threshold interpreted as \(U_w=b+N-1\). The number of no-descent starts in the word's cylinder is

\[
Z_w=\begin{cases}
\left\lfloor\dfrac{U_w-h_w}{2^{A(w)}}\right\rfloor
-\left\lfloor\dfrac{b-1-h_w}{2^{A(w)}}\right\rfloor,&U_w\ge b,\\
0,&U_w<b.
\end{cases}
\]

Hence a sum-cap certificate computes

\[
D_{\rm low}=\sum_{w\in W_{m,\le H}}(C_{N,b}(w)-Z_w),\qquad
R=N-\sum_{w\in W_{m,\le H}}C_{N,b}(w).
\]

If \(D_{\rm actual}\) is the total number of sampled starts that descend by the \(m\)-th odd return, then

\[
\boxed{D_{\rm low}\le D_{\rm actual}\le D_{\rm low}+R.} \tag{6.1}
\]

The error \(R\) is the *exact number of sample starts in the retained overflow state*. It is not an assumed geometric tail. This is an executable finite certificate for actual starts, independent of any global convergence assertion.

For \(N=4096,b=0,m=5,H=16\), the checker obtains 3,929 accounted starts and 167 overflow starts. Formula (6.1) gives **3,320 to 3,487** strict-descending starts. A separate direct iteration of all 4,096 starts gives **3,487**. Agreement with the upper endpoint is a result of this particular fixture, not a general theorem that every overflow start descends.

## 7. Verification, reproduction, and remaining work

`check_history_law.py` uses the Python standard library and exact integer/Fraction arithmetic. It checks 55 capped families, 4,422 positive integer lifts, 72 actual interval laws, 6,600 cylinder counts, 1,224 TV envelopes (including their rounding refinement), 3,006 descent equivalences, 216 capped descent certificates, 21 moment-weight recoveries including zero weights and overflow, and three synchronized arithmetic-predicate recoveries. Interval fixtures include a location greater than \(10^{30}\), emphasizing the uniform-in-location statement.

A separate table examines 332,032 starting integers across sample sizes \(2^8,2^{12},2^{16},2^{18}\), at three horizons for each size. These are exact finite TV calculations with rational lower/upper bounds, including (3.4) and the dyadic identity (3.5). Decimal renderings are display only. They do not certify the Gaussian limit; its proof is Section 4. In particular the modest-size values at \(m=L/2\) are not misreported as already equal to their limiting value 1/2.

Ordinary and optimized Python runs have identical JSON output:

```sh
python -B check_history_law.py > verification.normal.json
python -O -B check_history_law.py > verification.optimized.json
```

Five negative controls reject an even start, a zero exponent, a negative interval location, lost probability mass, and the incorrect assertion that 1 strictly descends in one return. Assertions are explicit and remain active under optimization. No zeta zero was sampled, no Lean was run, no existing workbench-wide checker was rerun, and no claim about all infinite trajectories is made.

For the next local session, the useful boundary is now precise: full histories cannot remain approximately geometric after their information threshold, but an actual arithmetic pushforward can discard much of that information. The next calculation should specify a fixed jointly retained observable (for example the offset modulo powers of three together with an affine descent barrier), compute its fibres or recurrence, and bound its distribution without asserting full-word approximation beyond (4.1). The overflow/descent counter already provides finite fixtures against which such a proposal can be tested.

## References and source-use record

Kokuno Yumeto. (2026, September 13). *Finite Collatz histories through support and Hurwitz zero clusters* [Working manuscript]. In *Collatz research workbench*, revision `63407034387466870f9e092dcdf39fb5a1ec0399`, `collatz_reconstruction/research_program/split_zero_history_20260913/note.tex`. The mathematical text was read through its complete end, including exact odd-return coordinates, cluster-to-moment inversion, reconstruction, sharpness, arithmetic predicates, and the distinction between encoding and descent. Its Git blob is `5fec479a48c4253eadffb9ed3c78da81b58a0000`. The accompanying audit was read as historical provenance, not treated as a newly executed independent audit.

Tao, T. (2026, July 16). *Almost all orbits of the Collatz map attain almost bounded values* (arXiv:1909.03562, Version 7). https://arxiv.org/html/1909.03562v7 . Specifically Definition 1.7, equation (1.9), Proposition 1.9, and Section 4. The older journal publication is in *Forum of Mathematics, Pi, 10*, e12 (2022). The finite residue/binomial comparison here is explicitly credited to this established mechanism. Proposition 1.9 is not invoked by assuming its strong residue-uniformity hypothesis (1.11) for arbitrary intervals: formula (2.1) supplies the actual discrepancy instead. No strengthening of Tao's orbit-minimum theorem is claimed.

National Institute of Standards and Technology. (n.d.). *Digital Library of Mathematical Functions*, Section 25.11, equation 25.11.10. https://dlmf.nist.gov/25.11.E10 . Retrieved September 14, 2026. Used only as the primary reference for the Hurwitz Taylor identity already employed in the predecessor, not as a source of Collatz trajectory estimates.
