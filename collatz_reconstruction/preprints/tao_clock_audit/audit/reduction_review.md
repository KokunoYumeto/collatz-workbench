# Independent audit: first passage, tightness, and the main theorem

Audit time: 2026-09-04T11:26:55Z. Scope: the deduction from Tao's Proposition 1.11, not an independent re-audit of its Fourier/renewal proof. No Lean, Git, descendants, thread contact, or workbench edits were used.

## Sources actually read

- Local `tex/chapters/01j_tao_main_theorem_reduction.tex`, fully read; SHA-256 `53d97d24d201fe90f97fde3a4e3afbf4e21949f4fa40be559562cc995375cffa`.
- Local `tex/chapters/01i_tao_first_passage_stabilisation.tex`, definitions and Proposition 1.11 statement/proof dependencies read; SHA-256 `5c3c5e54b3d6ff82b6c0b60e1b2cb4123079813ce6ec6d647e572b91bafa4d07`. This review does not certify its earlier dependency chapters.
- `C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/latex/1909.03562v7/collatz.tex`, Section 1 definitions and theorem statements (lines 143–206, 259–337) and all of Section 3 (535–595); SHA-256 `bfbc39432d4084a276416cb019a592003c868fa32f18e2f90028ac325ae5c19d`.
- Canonical index contract, recovery entrypoint, topic-route schema, and current preprint topic route were read. Queries `Tao Collatz` in research literature and `almost all Collatz` in both layers were executed. The latter routes the v7 TeX to `PUBUNIT-847E4E7212BFCD7A613CA573`, v5 TeX to `PUBUNIT-7B52CC4A159765C800B92B6B`, and journal PDF to `PUBUNIT-808654374124DFA4A51601F4`. This auditor did not read the journal PDF or v5 content and does not independently certify their textual agreement.

## Verdict on the existing reduction

The mathematics of 01j proves the complete chain from Proposition 1.11 to Tao's quantitative Theorem 3.1, his strict-inequality Syracuse theorem for arbitrary real-valued diverging functions, and his strict-inequality Collatz theorem. No weakened main conclusion remains at this reduction stage. This verdict treats Proposition 1.11 as the supplied input theorem.

The principal argument checks are as follows.

1. Nested first-passage times satisfy `T_v(N) <= T_u(N)` for `u <= v` whenever passage below `u` is finite. The indexed tail shift used in 01j is exact and does not require the orbit map to be injective.
2. The block recurrence loses only the failure probability at the lower threshold and the difference of the two passage-location laws. The event estimate is valid with the source's unhalved total-variation convention. No coupling has been inferred.
3. The initial scale `r_0 = y^(1/alpha)` and the recurrence scales `y^(alpha^(j-2))` are consistent: after `J` recurrence steps the event uses the input block `N_s` and passage threshold `s^(1/alpha)`. The lower bound `r_0 >= N_0^(1/alpha^3)` makes all invoked scales large. The zero-step/small-block cases are handled before probability laws are used.
4. The exact geometric error sum is `alpha^c / (1-alpha^(-c)) * (log y)^(-c)`. Its constant is harmless because `alpha=1001/1000` is fixed.
5. Covering by `z_k = X^(alpha^(-k))` correctly gives `sum log z_k <= log X/(alpha-1)`. The omitted prefix contains no bad starting values because an orbit contains its initial value. Overlap at endpoints only enlarges the upper estimate.
6. The dyadic mass identity keeps both the factor `2^(-a)` and the cutoff `X/2^a`. The potentially negative values of `log(X/2^a)` are never included. The full-integer quantitative bound follows.
7. For a diverging real-valued `f`, fix `K`, then choose a finite prefix after which `f > K`. The actual complement of `m(N)<f(N)` is `m(N)>=f(N)`, which is contained in the finite prefix union `{m>K}`. Taking the cutoff limit before the `K` limit proves the asserted strict result, with no monotonicity or positivity assumption on `f`.
8. On a fixed dyadic stratum the function on odd coordinates is `M -> f(2^a M)`. Finitely many strata give a vanishing bad mass, and the omitted strata have mass `2^(-(A+1)) H(X/2^(A+1))`. Taking first `X -> infinity`, then `A -> infinity`, is valid without a uniform-in-`a` estimate.

## Two definite source corrections, and distinctions that matter

The source tail-envelope display (v7 lines 591–593) is false as written, not merely incompletely explained. On odd integers let `f(1)=0` and `f(N)=exp(N)` for `N>=3`. The left side of that display is exactly 1 for every `x>=1`: `Syr_min(1)=1`, while `Syr_min(N)<=N<exp(N)` for all other positive odd `N`. Its proposed right side is bounded by a constant times `(log x)/x^c`, which tends to zero. The fixed-threshold, finite-prefix argument proves the same main theorem without this incorrect display.

The source dyadic density at line 206 is off by a factor of two. The set `nu_2(N)=a` has logarithmic density `2^(-(a+1))`; for example, `a=0` is the odd integers and has density one half, not one. The union `0<=a<=A` has density `1-2^(-(A+1))`. These errors do not change the limit one used in the theorem.

Other items in the workbench's issue list must not all be described as errors of the same kind:

- `O((alpha^j log y)^(-c))` and `O((alpha^(j-2) log y)^(-c))` are the same Landau estimate, because their ratio is the fixed constant `alpha^(2c)`. The source line 573 is not false. Displaying the exact constant improves transparency but is not a correction to an estimate.
- The source's assertion that finite passage is redundant is unsafe with the dummy-value convention `Pass=1`: a non-passing orbit would also be sent to the good value 1. One cannot call this an established counterexample for the actual Collatz map without exhibiting a non-passing orbit, which is not available here. Correct wording: the convention does not justify dropping the finite-passage condition; a cemetery value makes the logic unconditional. The source's displayed recurrence retains the condition.
- Restricting `f` to nonnegative values in a proof of a real-valued statement is a routine finite-prefix reduction that should be written. It is not evidence that the theorem excludes negative values.
- A strict complement written with `>` instead of `>=` is a logical omission, but the strict theorem is recoverable even from a proved non-strict version by applying that version to `f-1`. The direct fixed-`K` proof is cleaner.
- Missing bounded-scale and `J=0` cases are fillable edge cases, not a new obstruction.

Tao already states qualitative tightness and its diagonal equivalence in the Introduction, line 175, including a diagonalization footnote. His Theorem 3.1 already states uniform quantitative tightness. These must not be presented as new improvements to his theorem. An exact reformulation and a more explicit proof are appropriate claims.

## A precise abstract first-entry formulation

This is a complete proof of a formulation that can stand alone in the preprint. It also yields a limiting first-entry law along a prescribed scale lattice. It is a corollary of Tao's first-passage theorem, not an improved orbit-minimum estimate. No priority claim is made.

Let `Omega` be a countable state space, `F:Omega -> Omega` a total deterministic map, and `h:Omega -> [1,infinity)` a finite height. Adjoin a point `Delta` not in `Omega`. For `u>=1` set

`tau_u(z) = min {n>=0 : h(F^n z)<=u}`,

with value infinity when this set is empty. Define `P_u(z)=F^(tau_u(z))(z)` on finite passage, and `P_u(z)=Delta` otherwise; set `P_u(Delta)=Delta`. Thus every `P_u` maps the common space `Omega_Delta` to itself. Its image is in `{h<=u} union {Delta}`.

### Exact composition

For `u<=v`, one has `P_u P_v = P_u` on all of `Omega_Delta`.

If passage below `v` fails, passage below `u` also fails. If passage below `v` succeeds, no earlier point has height at most `u`. The first subsequent time below `u`, if any, is therefore exactly the original time below `u` minus `tau_v`. This proves the identity both on success and on failure; it also holds at `Delta`.

For a map `P` and finite signed measure `eta`, its pushforward satisfies

`||P_* eta||_1 <= ||eta||_1`.

Indeed, summing the absolute value of each fibre sum is bounded by the sum of the absolute values of all summands. This is the only contraction used below.

Fix `alpha>1`. For each sufficiently large `s`, let `lambda_s` be a probability measure supported in `{s<=h<=s^alpha}`, and put

`nu_s = (P_s)_* lambda_(s^alpha)`.

Suppose for every `s>=s_*` that

`||nu_s - (P_s)_* nu_(s^alpha)||_1 <= epsilon(s)` and `nu_s({Delta}) <= delta(s)`.

These are statements about actual probability measures with a distinct failure point, not about a conditional law given successful passage.

In the Collatz application `Omega` is the odd positive integers, `F=Syr`, `h(N)=N`, and `lambda_s(N)=1/(H_s N)` on the nonempty odd block `[s,s^alpha]`. Tao's Proposition 1.11 yields `epsilon(s)<=C(log s)^(-c)` and `delta(s)<=C s^(-c)` for sufficiently large `s`.

To verify the last assertion with the changed failure convention, let `mu,eta` be two cemetery-completed passage laws and let `q` merge `Delta` with 1. Then

`||mu-eta||_1 <= ||q_*mu-q_*eta||_1 + 2|mu(Delta)-eta(Delta)|`

`<= ||q_*mu-q_*eta||_1 + 2(mu(Delta)+eta(Delta))`.

Only the coordinates 1 and `Delta` differ between the two comparisons; writing their difference as `a` and `b` reduces the inequality to `|a|+|b|<=|a+b|+2|b|`. The source failure bounds therefore absorb the extra term into `O((log s)^(-c))`. Exact composition identifies `(P_s)_*nu_(s^alpha)` with the completed law of `P_s(N_(s^(alpha^2)))`.

### Proposition: limiting first-entry laws on a scale lattice

For fixed `u>=s_*`, put `t_j=u^(alpha^j)` and

`mu_(u,j) = (P_u)_* nu_(t_j) = (P_u)_* lambda_(u^(alpha^(j+1)))`, for `j>=0`.

The second equality is the exact composition identity. At `j=0`, `(P_u)_*nu_u=nu_u`, because `P_u` fixes every point of height at most `u` and fixes `Delta`.

For each `j>=0`,

`||mu_(u,j+1)-mu_(u,j)||_1 <= epsilon(t_j)`.

Proof: insert `(P_(t_j))_*nu_(t_(j+1))`, then use `P_u P_(t_j)=P_u` and the pushforward contraction. No matching of random variables or coupling is required.

If `epsilon(s)<=C(log s)^(-c)`, the geometric series is summable. The measures `mu_(u,j)` converge in total variation to a probability measure `mu_u^infinity`, supported on `{h<=u} union {Delta}`, and

`||mu_(u,j)-mu_u^infinity||_1 <= C/(1-alpha^(-c)) * (alpha^j log u)^(-c)`.

Proof: the displayed estimate follows first for differences between indices `j` and `J>j` by summation. Completeness of `ell^1` gives a limit. Positivity and total mass one pass to the limit, and no mass can leave the common support. Letting `J` tend to infinity gives the bound.

In particular,

`mu_u^infinity({Delta}) <= delta(u) + C/[2(1-alpha^(-c))]*(log u)^(-c)`.

The factor one half is valid because the total variation of two probability measures is twice their maximal event discrepancy; omitting it also gives a correct bound.

If `v=u^(alpha^k)` for an integer `k>=0`, then the limiting laws satisfy the exact compatibility relation

`(P_u)_*mu_v^infinity = mu_u^infinity`.

At finite `j`, the left pushforward equals `mu_(u,j+k)`. Pass to the total-variation limit using contraction. This proves compatibility only on the same scale lattice. It proves neither independence of the initial phase `u`, nor compatibility for arbitrary unrelated real thresholds, nor invariance under the one-step map `F`.

### Proposition: quantitative uniform block tightness

For `m(z)=inf_(n>=0) h(F^n z)`, the same assumptions with `delta(s)<=C s^(-c)` imply

`lambda_s({m>K}) <= C' (log K)^(-c)`

uniformly for sufficiently large `K` and all defined block laws. In the positive-integer application the infimum is a minimum.

If `s<=K^(1/alpha)`, the entire input block is below `K`, so the probability is zero. Otherwise let `r>=1` be the least positive integer such that `u=s^(alpha^(-r))<=K`. If `r=1`, then `u>K^(1/alpha^2)` by the current lower bound on `s`; if `r>1`, minimality gives `u>K^(1/alpha)`. Thus in both cases `K^(1/alpha^2)<u<=K`. For large `K` every scale lies above `s_*`. Write `j=r-1`; then `s=u^(alpha^(j+1))`. The preceding telescoping estimate from index 0 to index `j` gives

`lambda_s(P_u=Delta) <= delta(u) + (1/2) sum_(i=0)^(j-1) epsilon(u^(alpha^i)) <= C'(log K)^(-c)`.

The sum is empty when `j=0`. If `m>K` then passage below `u<=K` fails, so the estimate proves the claim. Bounded `K` may be included by increasing the constant. This is the same quantitative content as Tao's block argument, recast with explicit completed measures.

For harmonic integer blocks, the exact multiplicative cover and harmonic estimate checked above now give the uniform cutoff estimate of Tao's Theorem 3.1. The first-entry limit is optional in the preprint: the finite telescoping estimate already suffices for this deduction.

## Exact tightness equivalence

The following abstract elementary lemma is useful for explaining the theorem without modifying its strength. Let `S` be an infinite subset of the positive integers, let positive weights `w(n)` satisfy `W(X)=sum_(n in S,n<=X) w(n) -> infinity`, and let `m:S->[0,infinity)` be finite-valued. Let `rho_X` be the probability measure proportional to the weights below `X`, whenever this set is nonempty. The following assertions are equivalent:

1. For every real-valued `f:S->R` tending to infinity, `rho_X(m>=f) -> 0`.
2. `lim_(K->infinity) limsup_(X->infinity) rho_X(m>K) = 0`.
3. `lim_(K->infinity) sup_X rho_X(m>K) = 0`.

The supremum in (3) is over all nonempty finite initial segments. Because finite prefixes contain only finitely many values of `m`, no additional bounded-prefix assumption is needed.

Proof that (2) implies (1): for fixed `K`, the condition `f>K` fails only on a finite prefix `S cap [1,Y_K]`. Hence

`rho_X(m>=f) <= W(Y_K)/W(X) + rho_X(m>K)`.

Take `limsup` in `X`, then let `K` tend to infinity. Equality values are covered by the exact `>=` complement.

Proof that (1) implies (2): otherwise choose `epsilon>0` such that, for every integer `j>=1`, arbitrarily large `X` have `rho_X(m>j)>=epsilon`. Inductively choose `X_j>X_(j-1)` with this property and `W(X_(j-1))/W(X_j)<=epsilon/2`. Define `f(n)=j` on `X_(j-1)<n<=X_j`, and assign any finite value on the initial prefix. Then `f(n)->infinity`. At cutoff `X_j`, the current shell alone contributes at least `epsilon/2` to `rho_(X_j)(m>=f)`: subtract the entire earlier prefix from the mass of `{m>j}`. This contradicts (1).

Proof that (2) implies (3): given `epsilon>0`, choose `K_0` so that the limsup in (2) is smaller than `epsilon/2`. For some `X_0`, `rho_X(m>K_0)<=epsilon` for all `X>=X_0`. Increase `K_0` to a number `K` exceeding every value of `m` on the finite prefix up to `X_0`. Below `X_0` the tail mass is then zero, and above it the previous upper bound persists. The implication (3) to (2) is immediate.

For `S=odd positive integers`, `w(n)=1/n`, and `m=Syr_min`, this is precisely the qualitative statistical equivalence already identified by Tao. The quantitative rate `C(log K)^(-c)` is additional information supplied by Tao's Theorem 3.1, not by this abstract equivalence.

## Recommended publication framing

A defensible central statement is: “We give a clock-explicit, measure-level exposition of Tao's first-passage argument, retain the failure state, and derive the original almost-bounded theorem through uniform tightness. We correct specified displays in the reduction and prove total-variation convergence of completed first-entry laws along the associated scale lattice.”

The paper should distinguish the local corrections to displayed proof steps from the validity of Tao's theorem. It should not say the almost-bounded theorem was weakened, falsified, or improved by this reconstruction. Whether the earlier Fourier/renewal branch has been fully revalidated is outside this reduction review; the final manuscript must state its actual dependency scope rather than infer whole-paper validation from this audit.
