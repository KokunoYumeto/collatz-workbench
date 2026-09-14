# Tao v5/v7/journal F025 — Proposition 1.9 valuation-law audit

## Scope and routing receipt

This audit reconstructs only the theorem numbered Proposition 1.9,
“Distribution of \(n\)-Syracuse valuation.” It does not silently substitute
the first-passage stabilisation theorem, which is Proposition 1.11.

Before proof work, the immutable route ledgers were queried for
1909.03562, first passage, Syracuse, stabilisation/stabilization,
logarithmic density, and Proposition 1.9. The direct controlling matches were:

- ROUTE-COL-77768C71C4B3C049A8B8,
  ROUTE-COL-F8A670E4F671DDE694CB, and
  DOCROUTE-COL-8F0EDA4DC27DA85735AB, all identifying Tao's work through
  the local v5/journal manifestations;
- DOCROUTE-COL-3E40D11654F4089C8795, Siegel's Syracuse-random-variable
  paper, as an adjacent coordinate source rather than a proof of Tao
  Proposition 1.9;
- the existing Matthews, Urata, and Bernstein--Lagarias routes as adjacent
  \(2\)-adic coordinate literature.

No mathematical conclusion was taken from this metadata. The controlling v7
source and the v5 and journal comparison manifestations were read directly.
The route artifacts remained:

- state/index_routes.jsonl: 274170 bytes, SHA-256
  b05028694bf133b9b19f2b0c0a771323b7a47ae872c0712769267aaf1f1eff38;
- state/document_routes.jsonl: 324776 bytes, SHA-256
  e439a5f9a70253b00824df5be791415e1c068d574c23f6f7f61851c19a88b2a5;
- state/index_snapshot.json: 799 bytes, SHA-256
  7d5a17440a3cb039f2bfbb4814567b5805117002136cc65687de738ee99af62f.

The quarantined task 019fe2cf-438a-7112-859c-119accee0e9e was not
contacted, messaged, steered, or used as evidence.

## Exact manifestations

### Controlling v7

- TeX:
  C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/latex/1909.03562v7/collatz.tex;
  164932 bytes; SHA-256
  bfbc39432d4084a276416cb019a592003c868fa32f18e2f90028ac325ae5c19d.
- E-print archive: 1226861 bytes; SHA-256
  ba81acd6254838251f1ee585256a6f9f223cdc9c73bed0a3c4fd25782d0124ad.
- Statement: source lines 269–278.
- Proof: source lines 597–647, including Tail Lemma 3.1 at 603–627.

### Comparison v5

- TeX:
  C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/latex/1909.03562v5/collatz.tex;
  163356 bytes; SHA-256
  c676b362b30807aa6690d0d4f16b8c8e84324732f5c0eb72ccfd875000276ae0.
- E-print archive: 1226298 bytes; SHA-256
  eb7a4668ebf27a3f795f72fcdc8d992ada365824359c734fa58813c750ff2ede.
- Statement: source lines 269–278.
- Proof: source lines 591–641.

### Published journal manifestation

- PDF:
  C:/Users/LOCAL_USER/Documents/arxiv_latex/library/_recovered_from_papers/by_title/Tao Almost all orbits of the Collatz map attain almost bounded values.pdf;
  1008484 bytes; SHA-256
  55c817c73498f940ed1e70f10208105922f1f7c89e378dcb629040c534151a2b.
- Statement: physical page 6.
- Proof: physical pages 17–18; journal Section 4 and equation (4.1).
- The three pages were freshly rendered at 300 dpi and inspected at original
  detail:
  - page 6: 579210 bytes, SHA-256
    730e827d91e1045b5ee6306cf3f078cf98389dc55b54b72363df17481b2d6f31;
  - page 17: 366253 bytes, SHA-256
    13eaf55f4a9a574af0dbfc01c28c3685ecf5c9cbf87cef37117f2fa564591f5;
  - page 18: 427224 bytes, SHA-256
    a229435a4374496f21f48b48cd89a7491786c2263c3452940c86d8eef277cf4f.

The manifestations are separately identified. Their local agreement on this
argument is an exact comparison result and does not authorize theorem
enlargement elsewhere in the paper.

## Exact statement and total-variation convention

The source defines
\[
d_{\rm TV}(X,Y)=\sum_r|\mathbb P(X=r)-\mathbb P(Y=r)|,
\]
without the conventional factor \(1/2\). Proposition 1.9 fixes \(c_0>0\),
\(n\in\mathbb N\), \(n'\in\mathbb N\) with
\(n'\ge (2+c_0)n\), and an odd-positive-valued random variable
\(\mathbf N\). If its law modulo \(2^{n'}\) differs by
\(O(2^{-n'})\) in this unhalved distance from the uniform law on the odd
residues, then
\[
d_{\rm TV}\!\left(\vec a^{(n)}(\mathbf N),\operatorname{Geom}(2)^n\right)
\ll_{c_0}2^{-c_1n}
\]
for some \(c_1(c_0)>0\).

The edition exposes the hypothesis constant: if, for the fixed \(c_0\), the
modular distance is at most \(K(c_0)2^{-n'}\), uniformly in \(n,n'\) and the
law of \(\mathbf N\), the conclusion is at most
\(C(c_0)(1+K)2^{-c_1n}\). This is the same theorem at explicit constant
scope, not a stronger asymptotic claim.

## Manifestation defects and repairs

The following are preserved in v5, v7, and the journal:

1. The statement names odd classes modulo \(2^{n'}\), then calls them classes
   “of \(\mathbb Z/2^\ell\mathbb Z\)” for an undefined \(\ell\). The only
   typed ambient ring is \(\mathbb Z/2^{n'}\mathbb Z\).
2. The first-crossing decomposition is correctly
   \(A_k<n'\le A_{k+1}\). One intermediate bound reverses both endpoint
   conventions to \(A_k\le n'<A_{k+1}\). The proof before and after that
   line requires the original event.
3. The central total-variation sums are printed with \(|\vec a|<m\), although
   there is no \(m\) in the section. The surrounding argument and final count
   require \(|\vec a|<n'\).
4. The \(k=0\) crossing uses the empty sum \(A_0\), which was not included in
   the earlier summation convention. The edition defines \(A_0=0\).
5. The endpoint \(n=0\) is not dispatched. Both laws are then the point mass
   on the empty tuple, so the distance is exactly zero.

The v5/v7 TeX prerequisite Lemma 2.1 additionally has:

- an affine map written without its argument at line 460;
- Syr^{N-1}(N) at line 469, where the induction requires
  Syr^{n-1}(N).

The edition proves the prerequisite directly and does not transport either
defect.

## Exact residue-cylinder morphism

For a positive tuple
\(\vec a=(a_1,\ldots,a_n)\), put
\[
A_0=0,\qquad A_j=a_1+\cdots+a_j,\qquad
C_n(\vec a)=\sum_{i=1}^n3^{n-i}2^{A_{i-1}}.
\]
The affine iterate is exactly
\[
\operatorname{Aff}_{\vec a}(N)
=\frac{3^nN+C_n(\vec a)}{2^{A_n}}.
\]
The induction in
lem:Tao-Prop19-residue-fibre proves
\[
\vec a^{(n)}(N)=\vec a
\iff \operatorname{Aff}_{\vec a}(N)\in2\mathbb N+1.
\]
Oddness of the quotient is equivalent to the one cylinder
\[
N\equiv b_{\vec a}
:=3^{-n}\!\left(2^{A_n}-C_n(\vec a)\right)
\pmod{2^{A_n+1}}.
\]
This residue is odd because \(C_n(\vec a)\) has one odd leading term and all
remaining terms even.

For \(A_n<n'\), reduction from the odd classes modulo \(2^{n'}\) to the odd
classes modulo \(2^{A_n+1}\) has fibres of size
\[
2^{n'-(A_n+1)}=2^{n'-A_n-1}.
\]
The uniform mass of the valuation cylinder is therefore exactly
\[
\frac{2^{n'-A_n-1}}{2^{n'-1}}=2^{-A_n}.
\]
The unhalved \(L^1\) distance contracts under this reduction map. The
probability error for the entire cylinder is at most \(K2^{-n'}\); it is not
multiplied by the number of its high-digit lifts.

On the partial domain with valuation total \(<n'\), the valuation map is
surjective onto
\[
\mathcal D_{n,n'}=
\{\vec a\in(\mathbb N+1)^n:|\vec a|<n'\}.
\]
Its fibre over \(\vec a\) is the cylinder above. Its set-theoretic kernel pair
is equality of the first \(n\) valuation coordinates. The least positive odd
representative of \(b_{\vec a}\pmod{2^{A_n+1}}\), viewed modulo \(2^{n'}\),
defines an explicit section: it chooses every unrecovered higher binary digit
to be zero. Thus the map is a split surjection. It has no left or two-sided
inverse. Indeed, under the proposition's \(n\ge1\) and
\(n'\ge(2+c_0)n\) hypotheses, the tuple \((1,\ldots,1)\) has fibre size
\(2^{n'-n-1}\ge2\), so the valuation map is not injective.

## Actual tail

With \(S_j=\mathsf a_1+\cdots+\mathsf a_j\) and \(S_0=0\),
\[
\{S_n\ge n'\}
=\bigsqcup_{k=0}^{n-1}\{S_k<n'\le S_{k+1}\}.
\]
For a fixed positive \(k\)-prefix with \(S_k<n'\), divisibility of the
\((k+1)\)-step affine numerator forces
\[
3^{k+1}\mathbf N+
\sum_{i=1}^{k+1}3^{k+1-i}2^{S_{i-1}}
\equiv0\pmod{2^{n'}}.
\]
The coefficient \(3^{k+1}\) is a unit and the fixed sum is odd, so this is
one odd residue class. Its probability is at most
\((2+K)2^{-n'}\).

The positive \(k\)-prefixes with total \(<n'\) are in bijection with
\(k\)-subsets of \(\{1,\ldots,n'-1\}\), hence number
\(\binom{n'-1}{k}\). Summing the disjoint first crossings reduces the tail to
a lower binomial tail.

## Model tail and the shared exponential estimate

The sum of \(n\) independent \(\operatorname{Geom}(2)\) waiting times is at
least \(n'\) exactly when the first \(n'-1\) fair Bernoulli trials contain at
most \(n-1\) successes:
\[
\mathbb P\!\left(|\operatorname{Geom}(2)^n|\ge n'\right)
=2^{-(n'-1)}\sum_{k=0}^{n-1}\binom{n'-1}{k}.
\]

The edition makes the exponential constant explicit enough to verify its
dependence. Set
\[
p_0=(2+c_0/2)^{-1}<1/2,\quad
z_0=\frac{p_0}{1-p_0},\quad
\eta(c_0)=\log2-H(p_0)>0,
\]
where \(H\) is binary entropy. For \(M=n'-1\) and all sufficiently large
\(n\), \(n/M\le p_0\), and
\[
2^{-M}\sum_{k=0}^n\binom Mk
\le z_0^{-n}\left(\frac{1+z_0}{2}\right)^M
\le e^{-\eta(c_0)M}.
\]
The finite remaining \(n\) values are absorbed into the \(c_0\)-dependent
constant. This controls:

- the actual-valuation tail;
- the geometric-model tail;
- \(2^{-n'}\binom{n'-1}{n}\), the accumulated error over all interior
  valuation cylinders.

Adding the two tails and the interior error proves Proposition 1.9 exactly at
the stated scope.

## Reproducible finite certificate

certificates/tao_prop19_valuation_checks.py pins all eight source/route
hashes and checks:

- 28 source and proof locators;
- 665 exact residue-fibre cardinalities;
- 1745 valuation/cylinder equivalences;
- 5235 high-binary-digit lift-stability instances;
- 665 explicit zero-high-digit section instances;
- 14 exact noninjective-fibre obstructions in the source parameter range;
- 29 positive-composition counts;
- 2882 disjoint partial-partition instances;
- 29 exact negative-binomial identities;
- 48 exact exponential-weight inequalities.

The script reports PASS. It explicitly reports that it does not certify the
analytic quantified tail proof, Proposition 1.11, Theorem 1.6, or Theorem
1.3. The TeX proof, source audit, and finite certificate have distinct
epistemic roles.

## Adversarial audit and final repairs

An independent read-only pass recomputed the residue-cylinder, fibre,
composition, and probability arguments against the pinned sources. Before
acceptance it required four exact repairs: dispatch the \(n=1\) induction
base before invoking the \((n-1)\)-prefix affine map; define the deterministic
prefix sums locally in the first-crossing proof; expose the hypothesis as
\(K(c_0)\), not an unqualified absolute constant; and replace an unsupported
``no canonical inverse'' sentence by the explicit section and the proved
noninjective-fibre obstruction above. The patched chapter and enlarged finite
certificate passed the final reread; no further mathematical defect was
reported.

## Dependency consequence and remaining gate

Proposition 1.9 is now proved at its source scope. Its later uses are:

1. pushforward through
   \(\vec a\mapsto F_n(\vec a)\bmod3^k\), giving the comparison between the
   actual Syracuse iterate and the finite Syracuse random variable;
2. application to the logarithmic input \(\mathbf N_y\) modulo
   \(2^{3n_0}\), giving source estimate (5.4);
3. contraction to each valuation prefix and a union bound, producing the
   good-prefix event used in Proposition 5.2.

Those uses had to be rechecked as maps rather than inferred from theorem
proximity. In particular, the source calls the modular law of
\(\mathbf N_y\) a routine integral-test consequence and does not display its
full \(L^1\) calculation. The exact edge
\[
\text{Proposition 1.14}+\text{Proposition 1.9}
\longrightarrow\text{Proposition 1.11}
\]
therefore remained the next audit gate at the ACT30 checkpoint. F026
subsequently supplied that reconstruction and closed the edge under
`CLM-COL-000118` and `MOR-COL-000029`. Theorem 1.6, Theorem 1.3, natural
density, convergence to one, and a fixed universal orbit bound remain
unclaimed.

## Accepted ACT30 artifact and visual QA

The accepted proof chapter is 13017 bytes with SHA-256
`f4d06663f534e29d41a66bcd0dd49f0329178fea5c1765a2e5836b0285cc0250`.
The enlarged finite certificate is 13567 bytes with SHA-256
`92a603632d9142a53cfa6e0b4c84da087dce98a3be957262541a0d5af4bee2a7`.

Three clean TeX passes produced
`tmp/tao_prop19_draft_20260827/main.pdf`: 92 pages, 1040323 bytes, SHA-256
`d5b2327875c541a7eac3a51be02c9169eabdec5df56ab8d16c2326e408900998`.
The final log has zero warnings, overfull/underfull boxes, undefined controls,
or errors. All 25 font rows are embedded and subset. The layout extraction is
`tmp/pdfs/tao_prop19_act30_final/main-layout.txt`, 327767 bytes, SHA-256
`a1c927412de030a0f30c8e5723f3cd5d4bd8e3e1ef764b2619edefaf9bfd35f2`.

All 92 pages were freshly rendered at 200 dpi (40047026 aggregate bytes) and
all twelve complete contact sheets (4521914 aggregate bytes) were inspected.
Pages 5--63 and 74--83 are byte-identical to the fully inspected ACT29 render;
all changed pages and the four new pages were included in the contact-sheet
inspection. Pages 2, 84--89, and 92 were additionally inspected at original
render detail. The minimum detected content margins are 213 px left, 215 px
top, 211 px right, and 132 px bottom. No clipping, overlap, malformed display,
or margin fault was found. This is a working checkpoint, not release QA or a
global completion claim.
