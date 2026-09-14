# Independent clock and historical-source review

Date: 2026-09-04. Scope: bounded independent review for the separate Tao-focused preprint. No workbench edits, Lean, Git, descendant agents, or external publication were performed. This document is a review, not an assertion that the whole Tao proof or the whole historical corpus has been independently verified.

## Findings that control the framing

1. The unshortened, shortened, and odd-to-odd maps have exact variable-time orbit identifications. Their orbit minima agree after taking the odd part of the initial value. This is already explicitly recognized by Tao, Section 1.2; spelling out the clocks is useful exposition, not a new strengthening of Tao's theorem.
2. The local v7 TeX, line 165, reverses the logarithm quotient in its retrospective Allouche threshold. The correct threshold is `3/2 - log(2)/log(3) = 0.869070...`, not `3/2 - log(3)/log(2) = -0.084962...`. Korec, printed p. 86, gives the former explicitly. Allouche's actual affine and branch-count lemmas yield it directly, as proved below. This is an introductory transcription error, not a correction to Tao's almost-bounded-orbit theorem.
3. The local v7 TeX, line 206, assigns density `2^(-a)` to the fixed layer `nu_2(N)=a`. The correct absolute logarithmic density is `2^(-a-1)`. Consequently the sum over `0 <= a <= a_0` is `1 - 2^(-a_0-1)`. Correcting these two expressions leaves the Collatz/Syracuse equivalence intact.
4. An exact finite-cutoff comparison of logarithmic measures proves that the odd-part pushforward and direct logarithmic sampling on odd integers differ in total variation by at most `(H_X - H_floor(X/2))/H_X`. This makes the density transport quantitative and removes any need for an unexamined interchange of infinite sums and limits. It is an elementary derived lemma; no novelty claim is established by this review.
5. Tao already gives the equivalence between the arbitrary-divergent-bound theorem and tightness of orbit minima in the remark and diagonal footnote at local v7 line 175. That equivalence itself must not be advertised as new or as an independent proof of Tao's analytic theorem.

## Source identity, routing, and exact reading boundary

The canonical literature-index contract and recovery entrypoint were read before mathematical work. Canonical queries `Terras`, `Korec`, and `Allouche` returned the following units. The primary contents, not the query metadata or the older F030 audit, support the mathematical statements below.

| Source | Canonical unit | Primary loci directly checked |
|---|---|---|
| Terras, *A stopping time problem on the positive integers*, Acta Arith. 30 (1976), 241-252 | PUBUNIT-1DD2C3376CB6FD02D8AF3761 | Scan physical pages 1-2: printed 241-243, including definition of shortened T and stopping time, Theorems 1.1-1.2, Corollaries 1.3-1.4 |
| Terras, *On the existence of a density*, Acta Arith. 35 (1979), 101-102 | PUBUNIT-C0876EE694A648CC6F862B7C | Both printed pages 101-102, theorem and full finite-complement proof |
| Allouche, *Sur la conjecture de Syracuse-Kakutani-Collatz*, Seminaire de Theorie des Nombres de Bordeaux (1978-1979), expose 9, 9-01--9-15 | PUBUNIT-137B5746B9EDEC4CFC0D6F2B | Scan physical 2,5-9: printed 9-01 and 9-04--9-08; generalized map, branch-count definition, Lemmas 1-3 and their proofs; beginning of finite-coordinate proposition |
| Korec, *A density estimate for the 3x+1 problem*, Math. Slovaca 44 (1994), 85-89 | PUBUNIT-8DD31103A7429CACB4085CF8 | Printed 85-86 by native extraction, printed 86 additionally visually checked: map, Theorem 1, retrospective Allouche exponent, parity fibres, binomial count |
| Tao, *Almost all orbits of the Collatz map attain almost bounded values*, arXiv:1909.03562v7 | PUBUNIT-847E4E7212BFCD7A613CA573 | Primary collatz.tex lines 136-235: introduction, logarithmic measure, main theorem, tightness remark, accelerations, density handoff and affine iterate |

Local primary paths use the directory
`C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/`.
It is the contract's verified C:-to-F: access route, not a distinct edition.

Fresh SHA-256 values:

```text
latex/1909.03562v7/collatz.tex
bfbc39432d4084a276416cb019a592003c868fa32f18e2f90028ac325ae5c19d
published/Terras-1976-A-stopping-time-problem.pdf
2b9c296a05541c5b52f63482a09982519546eba36f581bddd853af6ca014bf89
published/Terras-1979-On-the-existence-of-a-density.pdf
6cb5efbda449752cc0e815f630680f4153aa3ee62a548307041f7968b5d0e47b
published/Allouche-1979-Syracuse-Kakutani-Collatz.pdf
96f959368e5417dcc6d432e4831f3cf957e7b0db687b916a6aed0262102a01b6
published/Korec-1994-A-density-estimate.pdf
3111bcc638a563fa4395d8a090a4b563116f1ffe30aee136f6e24a76d4d97c77
```

The existing literature-spine chapter, lines 1-180, was also read as a comparison artifact, not as primary historical evidence. The current official arXiv record was checked: v7 is dated 16 July 2026, and the journal version is *Forum of Mathematics, Pi* 10 (2022), e12. Thus a draft may say "Tao's 2019 result", but its bibliography must distinguish the 2019 first submission, 2022 journal version, and the v7 manifestation actually audited. The official record currently describes its changes as including a correction to Lemma 7.9; this review does not audit that lemma or assess that correction.

Primary online identity records: [Tao](https://arxiv.org/abs/1909.03562v7), [Korec](https://dml.cz/handle/10338.dmlcz/133225). The EuDML Allouche record returned HTTP 403 in this run; its local primary scan, not an online summary, was read.

## Exact comparison of the three clocks

Put P = {1,2,...} and O = {1,3,5,...}. Define

\[
C:P\to P,\qquad
C(n)=\begin{cases}3n+1&n\text{ odd},\\n/2&n\text{ even},\end{cases}
\]
\[
T:P\to P,\qquad
T(n)=\begin{cases}(3n+1)/2&n\text{ odd},\\n/2&n\text{ even},\end{cases}
\]
and
\[
a(x)=\nu_2(3x+1),\qquad S:O\to O,\quad
S(x)=(3x+1)/2^{a(x)}.
\]

These are respectively Tao's `Col`, `Col_2`, and `Syr`. The letter C here is editorial notation and must not be confused with Crandall's source symbol for his odd-to-odd map.

### Proposition 1: shortened-to-unshortened orbit reconstruction

For N in P let y_j=T^j(N), let
\[
\epsilon_j=1_{O}(y_j),\qquad
i_N(j)=j+\sum_{r=0}^{j-1}\epsilon_r.
\]
Then `i_N:N_0 -> N_0` is strictly increasing and
\[
C^{i_N(j)}(N)=y_j.
\]
Its omitted times are exactly `i_N(j)+1` with `epsilon_j=1`, and their states are `3y_j+1`. In particular,
\[
\min_{r\geq0}C^r(N)=\min_{j\geq0}T^j(N).
\]

Proof. For even y, C(y)=T(y); for odd y, C^2(y)=T(y), with intermediate value C(y)=3y+1. Induction on j proves the intertwining. The increment of i_N is 1 or 2, proving strict increase and the description of every missing time. Every omitted state is greater than its preceding retained state y_j; therefore it cannot lower the full-orbit minimum. The reverse inequality follows because every T-state is retained. This also describes the inverse on the image: j is the unique index with i_N(j) equal to the given image time. Its fibres on the image are singletons and its equality kernel is the diagonal.

For a real B, if `h_T(N,B)=min{j>=0:T^j(N)<=B}` is finite, then the first C-time below B is exactly `i_N(h_T(N,B))`. An omitted state cannot be the first such state since its preceding retained state is smaller. If no such T-time exists, no C-time exists either. There is no assertion that the two first-hit times have the same integer value.

### Proposition 2: odd milestones and valuation sums

Write N=2^b x_0 with x_0 odd. Let
\[
x_j=S^j(x_0),\quad a_{j+1}=\nu_2(3x_j+1),\quad
A_0=0,\quad A_j=\sum_{r=1}^j a_r.
\]
Every a_r is a positive integer, and for every j>=0,
\[
T^{b+A_j}(N)=x_j,
\qquad
C^{b+A_j+j}(N)=x_j.
\]
For a=a_{j+1} the entire next odd-to-odd blocks are
\[
T^{b+A_j+r}(N)=\frac{3x_j+1}{2^r}=2^{a-r}x_{j+1}
\quad(1\leq r\leq a),
\]
\[
C^{b+A_j+j+r}(N)=\frac{3x_j+1}{2^{r-1}}
=2^{a-r+1}x_{j+1}
\quad(1\leq r\leq a+1).
\]
The initial b steps in either clock are N, N/2,...,x_0. These blocks exhaust all subsequent times: A_j>=j, so both milestone sequences tend to infinity. Their interiors are even; their terminal states are the next odd state. Consequently
\[
\min C^{\mathbb N_0}(N)=\min T^{\mathbb N_0}(N)
=\min S^{\mathbb N_0}(x_0).
\]

Proof. The initial even divisions give x_0. At x_j the quantity 3x_j+1 is positive with exact valuation a. Each quotient before the terminal one has positive valuation, forcing the next halving branch. This proves the displayed intermediate values and the exact first-return times a for T and a+1 for C. Induction concatenates the blocks. Each omitted even state is a positive power of two times the terminal odd state, so cannot give a lower global minimum. The assertions include the fixed Syracuse orbit x_j=1: its T-clock period is 2 and its C-clock period is 3, as a_j=2.

This is a full reconstruction from the odd orbit, its valuation sequence, and the initial b. Forgetting the valuation sums forgets elapsed time. In particular one Syracuse step is not one shortened step and not one unshortened step. Identical whole-orbit minimum events on the same initial space have identical counting and logarithmic measures; this deterministic clock comparison itself produces no factor in the density. The factor of one half below comes from changing the initial space from all positive integers to odd integers.

## Finite logarithmic transport through the odd-part map

For integer X>=1 define
\[
H_X=\sum_{n=1}^X\frac1n,\qquad
O_X=\sum_{\substack{m\leq X\\m\text{ odd}}}\frac1m,
\qquad p(n)=n/2^{\nu_2(n)}.
\]
Let mu_X be the probability measure assigning `1/(n H_X)` to n in [1,X], and let lambda_X assign `1/(m O_X)` to each odd m<=X. Both measures have explicitly stated finite domains. We use total variation `sup_E |mu(E)-nu(E)|` for probabilities on a common discrete set.

### Proposition 3: quantitative comparison

For every set E of odd positive integers,
\[
\left|\mu_X\big(p^{-1}(E)\big)-\lambda_X(E)\right|
\leq\frac{H_X-H_{\lfloor X/2\rfloor}}{H_X},
\qquad H_0=0.
\]
Thus the same bound holds in total variation, and it is `O(1/log X)` as X tends to infinity.

Proof. For odd m<=X set `r_m=floor(log_2(X/m))`. Its exact fibre is
\[
p^{-1}(m)\cap[1,X]=\{m,2m,\ldots,2^{r_m}m\}.
\]
Its mu_X-mass is `(2-2^(-r_m))/(m H_X)`, by the finite geometric sum. Write
\[
B_E=\sum_{\substack{m\leq X\\m\in E}}\frac1m,
\quad D_E=\sum_{\substack{m\leq X\\m\in E}}\frac{2^{-r_m}}m,
\quad D=D_O.
\]
Partitioning [1,X] by the displayed fibres gives `H_X=2O_X-D`. Separating even and odd terms of H_X gives `2O_X=2H_X-H_floor(X/2)`; hence `D=H_X-H_floor(X/2)`. If q=B_E/O_X, then
\[
\mu_X(p^{-1}E)-\lambda_X(E)=\frac{qD-D_E}{H_X}.
\]
Here 0<=q<=1 and 0<=D_E<=D, so the absolute value is at most D/H_X. Finally D tends to log 2 while H_X grows as log X. The proof also covers X=1.

Corollary. The upper and lower logarithmic densities of p^{-1}(E) among all positive integers equal respectively the upper and lower relative logarithmic densities of E among odd positive integers. This follows directly from the finite bound, with no existence assumption on the densities. Because the whole-orbit minimum is preserved by p, its all-integer and odd-integer logarithmic laws have the same asymptotic tightness and the same asymptotic tails at each fixed threshold. This is the precise measure-level consequence needed for the exposition.

For a fixed valuation a>=0, the event `nu_2(n)=a` has mass
\[
\frac{2^{-a}O_{\lfloor X/2^a\rfloor}}{H_X}
\longrightarrow 2^{-a-1}.
\]
More generally if E has relative logarithmic density delta among odds, then `2^a E` has absolute logarithmic density `2^(-a-1) delta`. Summing the finitely many layers a=0,...,a_0 gives `1-2^(-a_0-1)` for full-density events on those layers. The omitted tail tends to `2^(-a_0-1)`, then tends to zero as a_0 grows.

For a nonmonotone divergent bound f on all positive integers, the Syracuse theorem is applied separately to `g_a(m)=f(2^a m)` for each fixed a; each g_a still tends to infinity. The corrected finite-layer argument then proves the all-integer statement. Conversely, for a divergent bound g on odd integers, define f(n)=g(n) on odds and f(n)=n on evens. This f tends to infinity, and a zero-log-density exceptional set on all integers has zero relative-log-density intersection with the odds, whose harmonic mass is asymptotically half the total. This proves both directions without any monotonicity assumption on f or g.

## Historical exponent: an independent extraction from Allouche

Allouche's printed map is on Z and is
\[
g(\ell)=\ell/d\quad(d\mid\ell),\qquad
g(\ell)=\big(n\ell-\varphi(n\ell)\big)/d\quad(d\nmid\ell),
\]
where n,d are coprime positive integers and varphi selects a fixed complete residue system modulo d. Specializing to `n=3,d=2,A_2={0,-1}` gives exactly the shortened T, not the unshortened C. His alpha(k,y) counts the nondivisible branches among the first k steps; here it is the number of odd T-inputs.

The proofs in printed pp. 9-04--9-08 yield
\[
T^m(y)=3^{\alpha(m,y)}2^{-m}y+P_m(y),
\qquad |P_m(y)|\leq(3/2)^m,
\]
and alpha(m,y) is periodic modulo 2^m with exact counts
\[
\#\{0\leq y<2^m:\alpha(m,y)=i\}=\binom mi.
\]
The remainder bound uses `M=(n-d)^(-1) sup|varphi|=1` in this specialization.

Set `c_A=3/2-log_3 2` and fix c>c_A. Choose eta>0 with c_A+eta<c. In the integer block `3^m <= y < 3^(m+1)`, every y satisfying `alpha(m,y)<=(1/2+eta)m` obeys
\[
T^m(y)\leq C_\eta y^{c_A+\eta}+y^{\log_3(3/2)}<y^c
\]
for all sufficiently large m. The fixed constant C_eta absorbs the bounded difference between m and log_3(y); the other exponent is `1-log_3 2<c_A`.

In a complete 2^m residue block the exceptional proportion is the upper tail of Binomial(m,1/2). Its mean is m/2 and variance m/4, so Chebyshev bounds this proportion by `1/(4 eta^2 m)`, which tends to zero. Partitioning `[3^m,3^(m+1))` into complete 2^m-blocks plus at most two end fragments adds only `O((2/3)^m)` to the proportion. These exceptional proportions tend to zero. To obtain natural density zero globally, split the sum into finitely many initial blocks and the remaining blocks whose exceptional proportions are uniformly at most any prescribed epsilon; the possible final partial block has at most the exceptional count of its full block, `o(3^m)=o(X)` when `3^m<=X<3^(m+1)`. Hence almost every y in natural density has some shortened iterate below y^c. Proposition 1 transfers the identical orbit-minimum event to C.

This proves precisely the strict exponent range; it does not assert its endpoint. It agrees with Korec's explicit historical sentence on p. 86. By contrast the reversed logarithm ratio makes c_A negative: taking theta=0 under that printed inequality would demand an orbit minimum strictly below 1 for almost every positive initial value, which is impossible. The printed decimal identifies the intended quotient without ambiguity.

## Historical paragraph suitable for the introduction

A concise mathematically accurate narrative is:

"The density results for the Collatz problem use several iteration conventions. Terras's parity coordinates are attached to the shortened map, with one division by two per step; Allouche's affine branch counts and Korec's power-descent estimate use this same clock in their classical specialization. Tao states his theorem for the unshortened map and proves it using the odd-to-odd Syracuse map, with one multiplication by three per step. Exact variable-time identities preserve orbit minima while retaining the elapsed-time information. Keeping this bookkeeping explicit leads naturally to a comparison of the associated logarithmic sampling measures."

Support: Terras 1976 pp. 241-243; Allouche pp. 9-01 and 9-04--9-08; Korec pp. 85-86; Tao v7 Section 1.2, particularly the acceleration formulas and identity (c-ident). The 1979 Terras note is worth citing if discussing fixed-stopping-level density limits: its actual proof takes a finite sum of point masses followed by complementary sets, rather than an infinite interchange of densities. This review has not independently rerun the remainder of Terras's 1976 tail proof or Korec's 1994 proof, and should not be represented as having done so.

## Recommendations to the main author

- Use the deterministic clock reconstruction and the finite logarithmic pushforward estimate as explicit, fully proved expository propositions.
- State the two introductory slips at their exact loci and their exact repairs, if relevant to the paper's focus. Do not promote them into an analytic gap or imply that they invalidate the main theorem.
- Keep the Allouche extraction short or in an appendix. Its purpose is historical accuracy and an example of exact clock bookkeeping, not to displace the Tao-focused argument.
- Attribute the arbitrary-divergent-bound/tightness equivalence to Tao's own remark and footnote. Any claimed additional result must be identified separately and checked against that source statement.
- Say exactly which analytic implications are newly proved in the draft and which are cited from Tao. This bounded review supplies no independent proof of the high-frequency or first-passage estimates in the body of Tao's paper.
