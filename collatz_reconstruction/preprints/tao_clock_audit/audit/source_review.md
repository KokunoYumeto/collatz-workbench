# Independent source audit: Tao, Sections 5 and 6

Date: 2026-09-04. Scope: a fresh read of the primary TeX, not an adoption of
the workbench's earlier QA verdicts. This review is read-only with respect to
the workbench; no Lean, Lake, Git, source mutation, or external communication
was used.

## Witnesses and read scope

- Tao, arXiv:1909.03562v7, local primary TeX
  `C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/latex/1909.03562v7/collatz.tex`.
  SHA-256 `bfbc39432d4084a276416cb019a592003c868fa32f18e2f90028ac325ae5c19d`.
  Section structure checked; lines 649–1095 read continuously. In particular,
  Section 5 Proposition 5.2 and Lemma 5.3, and Section 6 Lemma 6.2 and
  Corollary 6.3, were read in their surrounding argument.
- Tao, arXiv:1909.03562v5, sibling `1909.03562v5/collatz.tex`.
  SHA-256 `c676b362b30807aa6690d0d4f16b8c8e84324732f5c0eb72ccfd875000276ae0`.
  Lines 976–997 and 1039–1089 read for the reserve and offset comparisons.
- Local reconstruction `tex/chapters/01_literature_spine.tex`, lines
  2484–2608 and 2736–2898; and
  `tex/chapters/01g_tao_fourier_renewal.tex`, lines 1–192. These are audited
  claims, not independent source authority.
- The two specified QA files were consulted as audit hints. Their historical
  completion labels and stronger rhetorical classifications are not findings
  of this review. The journal PDF was not reread; this review makes no fresh
  assertion about its exact wording or pagination.

The canonical index contract, recovery entrypoint, topic-route schema,
Documents ancestor instructions, and project DIRECTIVES were read. Root
maintains the separate preprint's topic route and query history.

## Decisive conclusion

A short, carefully delimited expository note is mathematically supported.
Section 5 contains an incorrect endpoint trim and an invalid uniform
summation; both have short, complete repairs that recover exactly the source
statements used downstream. Section 6 contains a substantive difference
between v5 and v7, but the strengthened reserve is already Tao's own v7
revision. Explaining its exact numerical margin is legitimate; attributing
that revision to the present audit is not.

These findings do not strengthen the conclusion of Tao's almost-boundedness
theorem, do not show that theorem false, and do not certify the entire proof.
The present audit establishes only the stated Section 5–6 facts. It does not
settle the separate renewal argument in Section 7. A claim that the whole
theorem has been independently revalidated requires a separately checked
complete dependency chain.

## 1. Proposition 5.2: logarithmic coordinates require a multiplicative trim

Put `L = log x` and `lambda = log(4/3)`. On the good valuation event, v7
lines 741–757 give

    |T_x(N) - log(N/x)/lambda| <= K L^(3/5).

The source interval `I_y` (lines 716–719) moves both time endpoints inward
by `L^(4/5)`. Line 759 instead trims the input interval by adding and
subtracting `2 L^(4/5)` in the original integer coordinate. That additive
change modifies `log(N/y)` by only `O(L^(4/5)/y)` near the lower endpoint.
It does not imply the displayed time margin from the preceding estimate.
The scalar `subset` sign is also a typographical error, but not the
mathematical issue.

The following replacement proves the required claim. Retain the source
interval `I_y` unchanged and take

    R_y = [y exp(L^(4/5)), y^alpha exp(-L^(4/5))].

Its image under `N -> log(N/x)/lambda` has an additional margin
`(1/lambda - 1)L^(4/5)` beyond the endpoints of `I_y`. Since `lambda < 1`,
this dominates `K L^(3/5)` for large `x`. The interval is nonempty because
its logarithmic width is

    (alpha - 1) log y - 2 L^(4/5) > 0.

For `N` logarithmically distributed over the odd integers in `[y,y^alpha]`,
the elementary estimate

    sum_{a <= M <= b, M odd} 1/M = (1/2)log(b/a) + O(1/a)

shows that the excluded probability is `O(L^(-1/5))`, uniformly for
`y = x^alpha` and `y = x^(alpha^2)`. Adding the good-event exception
`O(L^(-10))` proves the source conclusion at line 762 with `c=1/5`.

The time estimate itself can be made explicit by applying the good-orbit
bound at the first crossing and the previous time. First-passage finiteness
within `n_0` follows from

    (alpha^3 - 1)L - lambda n_0 + O(L^(3/5)) < 0,

with the source `alpha=1.001` and `n_0=floor(L/(10 log 2))`.

This is a proof-text correction with an elementary replacement. It is not a
new distributional conclusion. Downstream Section 5 uses `I_y` and its
high-probability conclusion, not the discarded additive restriction.

## 2. Lemma 5.3: the needed uniform estimate survives

Let `m=m_0`, `r=n-m`, `A=a_1+...+a_m`, and `b=a_m`, with every `a_i>=1`.
Partition the source coefficient `c_n(X)` by the unique length-`m`
valuation tuple. Write the corresponding contribution as `c_(n,a)(X)`.

The exact crossing relations are

    3^m 2^(-A) M + F_m(a) <= x
      < 3^(m-1) 2^(-(A-b)) M + F_(m-1)(a_1,...,a_(m-1)).

The printed right-hand coefficient at v7 line 868 is `3^m`; the exact
coefficient is `3^(m-1)`. The same error occurs inside the valuation at
line 899. These are local exponent typos: the coarse estimates immediately
following them remain true after the exact identities are restored.

Because `F_(m-1)=o(x)`, the crossing relations imply, for sufficiently
large `x`,

    M_0 = 3^(-m) 2^(A-b) x < M <= M_1 = 3^(-m) 2^A x.

The tuple fixes one odd-input class modulo `2^(A+1)`. The extra condition
`M = X mod 3^r` gives one class modulo `q=2^(A+1)3^r`. The elementary
progression estimate is

    sum_{M_0 <= M <= M_1, M=a mod q} 1/M
      <= 1/M_0 + q^(-1) log(M_1/M_0).

On `2^A <= x^(1/2)`,

    q/M_0 = 2^(b+1)3^n/x <= 2 x^(-17/50),

using `3^n <= x^(4/25)` from `n<=n_0`. Thus

    c_(n,a)(X) << b 2^(-A).

On `2^A>x^(1/2)`, put
`H=3^(m-1)2^(-(A-b))M`. The last-step valuation gives

    2^b <= 3(H+F_(m-1))+1 <= 5H

for large `x`. Consequently `M >> 3^(-m)2^A`, and the same progression
estimate gives

    c_(n,a)(X) << 3^n 2^(-A) + b 2^(-A).

These are the source estimates before its last weakening. Their correct
uniform summation is

    sum_(a_1,...,a_m>=1) b 2^(-A) = 2,

and

    3^n sum_(2^A>x^(1/2)) 2^(-A)
      <= 3^n x^(-1/4) (1+sqrt(2))^m
      <= x^(-8999/100000),

since `m<=L/100000`, `3^5<2^8`, and `1+sqrt(2)<e`. Therefore

    c_n(X) << 2 + x^(-8999/100000) << 1

uniformly in the source variables.

By contrast the weakened majorant actually printed at lines 913–914 is

    sum_(a_1,...,a_m>=1) 2^(-A/2) = (1+sqrt(2))^m.

It is not bounded independently of `x`; here `m` grows with `log x`.
Thus the printed final summation is genuinely invalid as a uniformity
argument. The replacement does not require a new theorem from outside the
paper: retaining the sharper preceding weights and doing the tail split
closes it.

The exact endpoint identities and both resulting estimates in the current
local reconstruction are correct at this scope. The improved proof is
worth exposing because it displays exactly where uniformity is preserved.
It should not be advertised as a stronger almost-boundedness theorem.

## 3. Section 6: distinguish Tao's version repair from this exposition

Let `a=log(4/3)`, `b=log 2`, and suppose a length-`K` positive tuple obeys

    S_j >= 2j - C(sqrt(j log n)+log n),
    l=S_K <= n log(3)/b - rho C^2 log n.

Clearing denominators in the reversed offset gives the positive integer

    U = sum_(j=1)^K 3^(j-1) 2^(l-S_j).

Its elementary upper bound has exponential cost

    -rho b C^2 log n + b C log n
      -a j + b C sqrt(j log n).

Completing the square gives the exact maximum

    sup_(t>=0) [-a t+b C sqrt(t log n)]
      = [b^2/(4a)] C^2 log n.

The positive-coefficient series contributes at most a polynomial factor
`O(1+C^2 log n)`. Hence choosing first `C` and then `n` sufficiently large
proves `U<3^n` whenever

    rho > rho_* = b/(4a) = 0.6023552099... .

V5 lines 983 and 991 retain only `rho=1/2`. Its line 1074 also replaces
`2^(-C^2 log n/2)` by `exp(-C^2 log n/2)`, losing the factor `log 2`.
The true leading margin for `rho=1/2` is positive:

    b^2/(4a) - b/2 = 0.0709472252... .

The existing local counterfamily at 01g lines 138–171 is valid. In brief,
set `lambda=2a/b`, `J=floor(lambda^(-2) C^2 log n)`, take

    a_i=2-[floor(lambda i)-floor(lambda(i-1))]  (i<=J),
    a_i=2                                            (i>J),

choose `l` just below `n log(3)/b-C^2 log n/2` with the required parity,
and set `K=(l+floor(lambda J))/2`. These positive coordinates satisfy the
broad interval concentration bounds. The `j=J` term of `U/3^n` has
logarithm

    [b^2/(4a)-b/2] C^2 log n + O(1),

so exceeds one eventually. This refutes the universal size estimate used
in that v5 proof under its broadly stated corollary hypotheses.

It does NOT provide two colliding residues. More importantly, this
counterfamily at the upper edge of the half-reserve window does not obey
the actual stopping event `E_k intersect B_k`: its terminal sum is too far
past the crossing threshold when its final increment equals two.

On the actual stopping event, with `T=n log(3)/b-C^2 log n`, the final
increment satisfies

    S_(k+1) <= T+1+C(sqrt(log n)+log n)
              <= T+6 C log n
              <= n log(3)/b - 0.99 C^2 log n

for `C>=600`. The consecutive-interval condition controls the final
increment even though `E_k` omitted the single-coordinate conditions.
This proves the tighter reserve already printed by Tao in v7 lines
989 and 997. V7 lines 1080–1084 use the correct `log 2` and explicitly
compare the two numerical constants. Attribution must say so.

The exact threshold is a boundary of this fluctuation-and-size argument,
not an invariant of the Collatz conjecture. A statement claiming necessity
for every conceivable proof, or failure of separation at every reserve
below this boundary, is unsupported. The local proposition proves the
sufficient range and gives a concrete failure of the size claim at one
excluded value; do not silently enlarge that into a universal necessity
theorem.

## 4. Offset injectivity: a typo, not an obstruction

V7 Lemma 6.2 line 1051 (v5 line 1045) prints

    F_n(a_1,...,a_n) = 3^n 2^(-S_n) + F_(n-1)(a_2,...,a_n).

The correct leading coefficient is `3^(n-1)`. The least 2-adic valuation
of `F_n` is exactly `-S_n`: after multiplying by `2^S_n`, its first term
is odd and every later term even. Equality of two offsets thus recovers
the same total `S_n`. Subtracting the correct leading term reduces the
equality to length `n-1`; induction recovers the tail, then `a_1`.
The source injectivity conclusion is unchanged.

## 5. Earlier QA language that must not enter a preprint as a correction

- `exp(O(L^(3/5)))` is standard two-sided multiplicative control: it lies
  between `exp(-K L^(3/5))` and `exp(K L^(3/5))`. Exposing its lower bound
  is good exposition, not repair of an allegedly unsigned expression.
- `log O(M_1/M_0)` can denote `log(C M_1/M_0)` for a suitable positive
  absolute constant. Replacing it with `O(1+log(M_1/M_0))` is clearer,
  but this typography alone does not establish a mathematical error.
- A period exponent can be made nonnegative by choosing a sufficiently
  large multiple of the period. That is a suppressed choice, not a new
  dynamical theorem.
- A previous local audit not having finished a dependency is not evidence
  that Tao left that dependency unproved. Do not export an old workflow
  status as an open mathematical problem.

Recommended framing: an explicit reconstruction of selected uniformity,
coordinate, and reserve estimates in Tao's proof, including two local
Section 5 proof-text corrections and a precise account of the author's
Section 6 version revision. The mathematically substantial content is the
complete checkable reconstruction, not a claim that the celebrated theorem
has a stronger conclusion or was rescued from falsity.
