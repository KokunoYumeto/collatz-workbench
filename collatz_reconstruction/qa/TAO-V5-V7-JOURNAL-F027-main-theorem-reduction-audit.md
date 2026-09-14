# Tao v5/v7/journal F027 — exact main-theorem reduction audit

## Scope and routing receipt

This audit reconstructs exactly the dependency chain
\[
\text{Proposition 1.11}\Longrightarrow\text{Theorem 3.1}
\Longrightarrow\text{Theorem 1.6}\Longrightarrow\text{Theorem 1.3}.
\]
It does not close the whole-paper, whole-corpus, Chatnotes, Gemini, formal
release, or publication gates. Before the chain was admitted, the immutable
route ledgers were queried and the same three exact source records used at
F026 were recovered:

- ROUTE-COL-77768C71C4B3C049A8B8;
- ROUTE-COL-F8A670E4F671DDE694CB;
- DOCROUTE-COL-8F0EDA4DC27DA85735AB.

Routing metadata was used only to locate manifestations. Mathematical content
was read in the source TeX and the separately retained journal PDF. The
frozen routing artifacts remain:

- state/index_routes.jsonl: 274170 bytes, SHA-256
  b05028694bf133b9b19f2b0c0a771323b7a47ae872c0712769267aaf1f1eff38;
- state/document_routes.jsonl: 324776 bytes, SHA-256
  e439a5f9a70253b00824df5be791415e1c068d574c23f6f7f61851c19a88b2a5;
- state/index_snapshot.json: 799 bytes, SHA-256
  7d5a17440a3cb039f2bfbb4814567b5805117002136cc65687de738ee99af62f.

The quarantined task 019fe2cf-438a-7112-859c-119accee0e9e was not
contacted, messaged, steered, or used as evidence.

## Exact manifestations and locators

### Controlling v7 source

- TeX:
  C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/latex/1909.03562v7/collatz.tex;
  164932 bytes; SHA-256
  bfbc39432d4084a276416cb019a592003c868fa32f18e2f90028ac325ae5c19d.
- Logarithmic law: lines 159–163.
- Theorem 1.3: lines 169–170.
- Syracuse map and odd-part identity: lines 180–193.
- Odd logarithmic law and Theorem 1.6: lines 199–206.
- First-passage definitions and Proposition 1.11: lines 316–335.
- Section 3 and the main reduction: lines 535–593.

### Version-pinned v5 comparison

- TeX:
  C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/latex/1909.03562v5/collatz.tex;
  163356 bytes; SHA-256
  c676b362b30807aa6690d0d4f16b8c8e84324732f5c0eb72ccfd875000276ae0.
- Introduction locators: lines 159–206.
- Proposition 1.11: lines 326–335.
- Section 3 and the main reduction: lines 529–587.

After all whitespace is removed, v5 lines 529–587 and v7 lines 535–593 are
exactly equal; each normalized string has length 4748. This is a local
comparison result, not a declaration that the complete source files are
text-identical.

### Published journal comparison

- PDF:
  C:/Users/LOCAL_USER/Documents/arxiv_latex/library/_recovered_from_papers/by_title/Tao Almost all orbits of the Collatz map attain almost bounded values.pdf;
  1008484 bytes; 56 pages; SHA-256
  55c817c73498f940ed1e70f10208105922f1f7c89e378dcb629040c534151a2b.
- Logarithmic density and main theorem: physical page 3.
- Syracuse setup and Theorem 1.6: physical page 4.
- Proposition 1.11: physical page 8.
- Theorem 3.1 and final reductions: physical pages 15–17.

Those pages were read visually and reproduce the same reduction and defects.
No whole-document identity is inferred.

## Exact theorem boundaries

For fixed \(\alpha=1001/1000\), let \(\mathbf N_s\) have logarithmic law on
the odd integers in \([s,s^\alpha]\). Proposition 1.11 supplies, at
sufficiently large scales, failure probability \(O(s^{-c})\) and the
unhalved total-variation estimate
\[
d_{\rm TV}\bigl(\operatorname{Pass}_s(\mathbf N_{s^\alpha}),
                 \operatorname{Pass}_s(\mathbf N_{s^{\alpha^2}})\bigr)
\ll(\log s)^{-c}.
\]
Theorem 3.1 seeks the uniform fixed-threshold harmonic estimates
\[
\sum_{\substack{M\le X,\ M\ {\rm odd}\\
 \operatorname{Syr}_{\min}(M)>N_0}}\frac1M
\ll\frac{\log X}{(\log N_0)^c},
\qquad
\sum_{\substack{N\le X\\
 \operatorname{Col}_{\min}(N)>N_0}}\frac1N
\ll\frac{\log X}{(\log N_0)^c}.
\]
Theorem 1.6 replaces the fixed \(N_0\) by an arbitrary real function on odd
positive integers tending to infinity. Theorem 1.3 transfers the resulting
strict inequality to all positive integers.

## Eight verified source defects

1. **Reversed tail envelope.** V7 lines 591–593 / v5 lines 585–587 define
   \(\widetilde f(x)=\inf_{N\ge x}f(N)\), then apply it to a sum over
   \(N\le x\). The displayed estimate is false. For odd \(N\), take
   \(f(1)=0\) and \(f(N)=e^N\) for \(N\ge3\). The term \(N=1\) contributes
   one while the asserted right side is \(O(\log x/x^c)\to0\).

2. **Dropped equality.** The complement of
   \(\operatorname{Syr}_{\min}(N)<f(N)\) is
   \(\operatorname{Syr}_{\min}(N)\ge f(N)\). The source estimates only the
   strict \(>\) event, with no argument that equality is negligible.

3. **Changed codomain.** Theorem 1.6 allows real-valued \(f\); line 591
   silently changes this to \(f\ge0\). Since \(f\to\infty\), exceptional
   values can be confined to a finite prefix, but that reduction must be
   stated.

4. **Dyadic factor two and missing rescaling.** Line 206 assigns density
   \(2^{-a}\) to \(\nu_2(N)=a\) and \(1-2^{-a_0}\) to the union through
   \(a_0\). The exact densities are \(2^{-(a+1)}\) and
   \(1-2^{-(a_0+1)}\). The odd theorem must be applied to
   \(g_a(M)=f(2^aM)\), not \(f(M)\).

5. **Omitted \(J=0\).** The first index \(J\) can be zero. The case is
   direct: if \(s\le N_0^{1/\alpha}\), every input in
   \([s,s^\alpha]\) is at most \(N_0\), so the bad block event is empty.

6. **Empty small blocks.** Some narrow intervals contain no odd integer, so
   \(\mathbf N_s\) and \(B_s\) are undefined. The recurrence is restricted
   to a fixed sufficiently large cutoff \(X_*\); smaller cases are direct.

7. **False redundancy parenthetical.** At v7 line 552 / v5 line 546 /
   journal page 15, finite passage is said to be redundant for
   \(x\ge N_0\). Under the convention \(\operatorname{Pass}_x=1\) when
   \(T_x=\infty\), membership in \(E_{N_0}\) does not imply finite passage.
   The proof retains the condition, so the recurrence is not damaged.

8. **Shifted recurrence exponent.** Substitution of
   \(s=y^{\alpha^{j-2}}\) gives
   \(O((\alpha^{j-2}\log y)^{-c})\), not
   \(O((\alpha^j\log y)^{-c})\). Their ratio is the fixed factor
   \(\alpha^{2c}\), which is explicitly absorbed.

The base failure estimate similarly has the literal form
\(O((y^{1/\alpha})^{-c})=O(y^{-c/\alpha})\); the printed form is valid only
after renaming the positive exponent.

## Indexed first-passage morphism

For \(1\le u\le v\) and \(T_u(N)<\infty\), define
\[
d_{u,v}(N)=T_u(N)-T_v(N)\ge0,\qquad \sigma_d(k)=k+d.
\]
Then
\[
\operatorname{Pass}_u(N)=
\operatorname{Syr}^{d_{u,v}(N)}(\operatorname{Pass}_v(N)).
\]
For indexed tails
\(\mathcal O_w^N(k)=\operatorname{Syr}^k(\operatorname{Pass}_w(N))\),
\[
\mathcal O_u^N=\mathcal O_v^N\circ\sigma_{d_{u,v}(N)}.
\]
The shift is injective with image \(d+\mathbb N\), singleton fibres on its
image, and diagonal equality kernel. This proves value-set inclusion and
transport of membership in
\[
E_{N_0}=\{M\ {\rm odd}:\operatorname{Syr}_{\min}(M)\le N_0\}.
\]
It does not assert that \(\mathcal O_v^N\) is injective; periodic repetitions
can collapse distinct indices.

## Exact recurrence and iteration

Define
\[
b_{N_0}(s)=\mathbb P\left(
T_s(\mathbf N_{s^\alpha})<\infty,\
\operatorname{Pass}_s(\mathbf N_{s^\alpha})\in E_{N_0}\right).
\]
On the space carrying \(\mathbf N_{s^{\alpha^2}}\), the indexed-tail
morphism and marginal total variation give
\[
b_{N_0}(s^\alpha)\ge b_{N_0}(s)-C(\log s)^{-c}.
\]
No coupling is constructed.

For \(s>N_0^{1/\alpha}\), let \(J\ge1\) be least such that
\[
y=s^{\alpha^{-J}}<N_0^{1/\alpha}.
\]
Then
\[
y^\alpha\ge N_0^{1/\alpha},\qquad
y\ge N_0^{1/\alpha^2},\qquad
y^\alpha<N_0.
\]
At \(r_0=y^{1/\alpha}\), finite passage places the passage location below
\(N_0\), so \(b_{N_0}(r_0)\ge1-Cr_0^{-c}\). Iterating at the exact scales
\(y^{\alpha^{j-2}}\) gives
\[
\sum_{j=1}^J(\alpha^{j-2}\log y)^{-c}
\le\frac{\alpha^c}{1-\alpha^{-c}}(\log y)^{-c}
\ll(\log N_0)^{-c}.
\]
Thus
\[
\mathbb P(\operatorname{Syr}_{\min}(\mathbf N_s)>N_0)
\ll(\log N_0)^{-c}.
\]

For an applied cover scale \(s\ge2\), the block normalizer satisfies
\(H_s\ll\log s\); if \(1<s<2\), the block contains no odd integer and its
local sum is zero. For target \(X>N_0\),
put \(z_k=X^{\alpha^{-k}}\) and take \(L\) least with \(z_L\le N_0\).
Then \(z_L>N_0^{1/\alpha}\), the blocks
\([z_k,z_k^\alpha]=[z_k,z_{k-1}]\) cover \([z_L,X]\), the leftover is
bad-free, and
\[
\sum_{k=1}^L\log z_k\le\frac{\log X}{\alpha-1}.
\]
This proves the odd fixed-threshold estimate. The exact decomposition
\[
\sum_{\substack{N\le X\\\operatorname{Col}_{\min}(N)>N_0}}\frac1N
=\sum_{a\ge0}2^{-a}
\sum_{\substack{M\le X/2^a,\ M\ {\rm odd}\\
\operatorname{Syr}_{\min}(M)>N_0}}\frac1M
\]
together with the termwise nonnegative truncated bound
\[
\sum_{\substack{a\ge0\\X/2^a\ge2}}
2^{-a}\log(X/2^a)
\le \log X\sum_{a\ge0}2^{-a}
=2\log X
\]
proves the all-integer part of Theorem 3.1.  No negative tail terms from the
untruncated signed expression are used.

## Exact fixed-tail repair of Theorem 1.6

For arbitrary real \(f\to\infty\), define the complete bad set
\[
D_f=\{M\ {\rm odd}:\operatorname{Syr}_{\min}(M)\ge f(M)\}.
\]
For each integer \(K\ge2\), choose \(Y_K\) so that \(f(M)>K\) for every odd
\(M\ge Y_K\). Then
\[
\sum_{\substack{M\le X\\M\in D_f}}\frac1M
\le H_{\rm odd}(Y_K)
+C\frac{\log X}{(\log K)^c}.
\]
Divide by \(H_{\rm odd}(X)=\frac12\log X+O(1)\), let \(X\to\infty\) with
\(K\) fixed, and only then let \(K\to\infty\). This proves zero relative odd
logarithmic density of the full bad set. It repairs the reversed envelope,
the equality case, the real codomain, nonmonotonicity, and the limit order.

## Exact dyadic morphism and Theorem 1.3

Let
\[
\mathcal O=2\mathbb N+1,\qquad
\mathcal S_a=\{N:\nu_2(N)=a\}.
\]
The maps
\[
\iota_a(M)=2^aM,\qquad \pi_a(N)=N/2^a
\]
are two-sided inverses between \(\mathcal O\) and \(\mathcal S_a\), with
singleton fibres, diagonal equality kernels, and no starting-coordinate
information loss. Globally,
\[
N\longleftrightarrow(\nu_2(N),N/2^{\nu_2(N)})
\]
is a bijection with the disjoint union of all odd strata. For every
\(A\subseteq\mathcal O\),
\[
\sum_{\substack{N\in\iota_a(A)\\N\le X}}\frac1N
=2^{-a}\sum_{\substack{M\in A\\M\le X/2^a}}\frac1M.
\]
Therefore
\[
\sum_{\substack{N\le X\\\nu_2(N)=a}}\frac1N
=2^{-a}H_{\rm odd}(X/2^a)
=2^{-(a+1)}\log X+O_a(1).
\]

The minimum identity is proved at orbit level. The initial even segment from
\(2^aM\) ends at \(M\) without falling below \(M\). Between consecutive odd
Syracuse states \(M_j,M_{j+1}\), the Collatz segment is
\[
M_j,\ 2^{q_j}M_{j+1},\ldots,2M_{j+1},M_{j+1},
\qquad q_j=\nu_2(3M_j+1),
\]
and every intermediate value is at least \(M_{j+1}\). Hence
\[
\operatorname{Col}_{\min}(2^aM)=\operatorname{Syr}_{\min}(M).
\]

For fixed \(a\), apply Theorem 1.6 to \(g_a(M)=f(2^aM)\). For fixed \(A\),
the first \(A+1\) bad strata have total harmonic mass \(o(\log X)\), while
\[
\sum_{\substack{N\le X\\\nu_2(N)>A}}\frac1N
=2^{-(A+1)}H(X/2^{A+1}).
\]
After division by \(H(X)\), first send \(X\to\infty\) at fixed \(A\), then
send \(A\to\infty\). No uniformity in \(a\) and no interchange of limits is
used. This proves Theorem 1.3 with the strict inequality intact.

As an independent cross-check, the fixed-threshold Collatz part of Theorem
3.1 and the same fixed-\(K\) tail argument prove Theorem 1.3 directly.

## Nonclaims and dependency boundary

The reconstruction proves logarithmic-density statements only. It does not
prove natural density, an absolute almost-everywhere orbit bound, passage for
an individual orbit, convergence to one, absence of divergent or periodic
exceptional orbits, invariance of logarithmic measure, or a coupling of
first-passage laws. The dyadic map is a bijection on the displayed
starting-number coordinates and preserves orbit minima at the declared
scope. It is not itself a time-preserving conjugacy: full Collatz time is
reconstructed by expanding each odd Syracuse step with
\(q_j=\nu_2(3M_j+1)\), deterministically computed from its odd source state
\(M_j\).

The exact TeX proof is tex/chapters/01j_tao_main_theorem_reduction.tex. The
finite certificate is certificates/tao_main_reduction_checks.py; it checks
source identities and locators, normalized v5/v7 equality, finite
first-passage tail shifts, geometric-error arithmetic, constructive covers,
dyadic bijections, weight transport, and finite orbit-minimum identities. It
does not certify the analytic total-variation estimate, infinite limiting
arguments, or source Proposition 1.11 independently of F026.

## Resource-policy enforcement during the audit

No Lean build was launched by this corpus task. An external descendant of
task 01a0355f-b609-7b22-9015-a2112fc1494c repeatedly started uncapped
R107DeficitProgression processes while this work was in progress. Exact
observed trees included:

- root shell 8316, sequentially observed with Coordinates.lean
  (32080/36992/34112) and FullSupport.lean (56864/24540/58352);
- Coordinates.lean: 38088/18848/35064/36672;
- DifferenceExact.lean: 32360/22516/22912/48388;
- Fibres.lean: 18832/32944/49288/36468;
- Complement.lean: 38044/17548/25260/12756;
- aggregate lake build R107DeficitProgression: 35876/55088/25044.

Verified current trees were stopped child-to-root; several sequential
children exited or changed between inspection and stop. The parent task was
sent the controlling global rule: do not restart an uncapped build, run at
most one Lean build, and permit a worker only under a process-tree watcher
that kills it at 3 GiB. The final audit at
2026-08-28T10:00:15.0014853Z found no R107 Lean/Lake process tree.
