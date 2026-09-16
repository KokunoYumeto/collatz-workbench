# Collatz: entrance distributions, the limits of random histories, and finite arithmetic certificates

The Collatz conjecture asks whether repeatedly replacing an even positive integer by n/2 and an odd one by 3n+1 always reaches 1. This workbench studies three related questions: how trajectories descend statistically, how long a probabilistic model describes their complete histories, and how to certify statements about individual trajectories using exact integer equations.

It is a **PolyClank** project: open, cumulative mathematical collaboration between people and language models, in the spirit of Polymath. The public work includes proofs, source files, executable checks and records of development, so another person can continue from the mathematics rather than from a summary of a conversation. The work described here was developed under **Kokuno Yumeto**, with **ChatGPT 5.6 Sol, Ultra mode, in Codex**, and **GPT-6 Astra**. Participation instructions are below.

## From Tao’s theorem to compatible entrance distributions

There is a substantial history behind the statistical approach. Terras (1976) and Everett (1977) proved that the proportion of starts up to X that eventually fall below themselves tends to one as X grows: a natural-density statement. Allouche and Korec obtained stronger bounds on how far they fall. Repeating such arguments is difficult because descended values may concentrate in the exceptional set for the next descent. Tao explains this obstruction and the earlier results in [*Almost all orbits of the Collatz map attain almost bounded values*, §1.1, version 7](https://arxiv.org/html/1909.03562v7#S1.SS1).

Tao’s theorem, first announced in 2019, says that for **every** function f(n) tending to infinity, the minimum of the orbit starting at n is less than f(n) for a set of starting values of logarithmic density one. Here logarithmic density weights n by 1/n: the exceptional starts up to X have total weight negligible compared with the sum of 1/n over all starts up to X. The function f may grow arbitrarily slowly. This is [Tao’s Theorem 1.3](https://arxiv.org/html/1909.03562v7#S1.Thmtheorem3).

To state the workbench’s additional deduction, follow only the odd values of an orbit. One step now means applying 3n+1 and dividing by 2 until an odd number remains. Call this map T. Thus 3 → 5 → 1, with respectively one and four divisions. If m such steps use A divisions altogether, they represent m+A steps of the original Collatz map. Keeping these clocks distinct is important when comparing statistical statements.

For a threshold x≥1, let p_x(n) be the first odd orbit value at most x, including n itself if it is already at most x. Write † when the orbit never enters that range. Entrance through nested thresholds satisfies an exact identity:

`p_x(p_y(n)) = p_x(n)  whenever 1≤x≤y`, with `p_x(†)=†`.

In words, one can first wait until the orbit reaches y and then continue until it reaches x. [Tao’s Proposition 1.11](https://arxiv.org/html/1909.03562v7#S1.Thmtheorem11) controls how little the entrance distribution changes when the starting scale is increased. Our deduction turns that approximate agreement into an exactly compatible limiting family.

**Entrance-law result.** Set α=1.001, fix a sufficiently large b, and put `t_j=b^(α^j)` for j≥0. Choose an odd starting integer N_j from `[t_(j+1), t_(j+2)]`, with probability proportional to 1/n. For every fixed x≥1, the distribution of p_x(N_j) converges to a probability λ_x on the odd integers at most x together with †. There are constants C,c>0 such that, whenever x≤t_j,

`Σ_z |Pr(p_x(N_j)=z) − λ_x(z)| ≤ C/(log t_j)^c`.

Here log is the natural logarithm. These limits agree exactly across thresholds: choosing z with distribution λ_y and following it to x produces distribution λ_x for x≤y. Moreover, for any finite list x₁≤⋯≤x_r of thresholds at least 1, the **joint** distribution of all r entrance values converges with the same bound, provided x_r≤t_j. The error does not acquire a factor r.

The proof explains both conclusions. Tao’s adjacent-scale errors are bounded by a constant times `(log t_j)^(-c)`. Since `log t_j=α^j log b`, these errors have a convergent geometric sum. Exact composition transports the estimates to every smaller threshold. Finally, the entrance at the largest threshold determines all subsequent smaller-threshold entrances, so observing them together introduces no additional error. See Kokuno Yumeto, [*Clocks and First-Passage Measures in Tao’s Collatz Theorem*, §§3–4](https://github.com/KokunoYumeto/collatz-workbench/blob/main/collatz_reconstruction/preprints/tao_clock_audit/output/pdf/tao_clock_audit.pdf).

This supplies distributions for simultaneous descent observations, with quantitative control, from Tao’s analytic estimate. It is an additional distributional conclusion, not an improvement of his orbit-minimum bound or a correction to his theorem. The family is constructed for the chosen base b; independence from an arbitrary different base is not established.

## How long does the random-history model remain accurate?

The preceding result concerns entrance locations. A more demanding question asks for the distribution of the **entire sequence of divisions**. The familiar model treats successive division counts as independent, with probabilities 1/2, 1/4, 1/8, … for one, two, three, … divisions. Tao makes a finite-history version precise in [Proposition 1.9 and §4](https://arxiv.org/html/1909.03562v7#S4). The workbench determines a sharp boundary for this approximation under interval sampling.

Choose n uniformly from **N consecutive positive odd integers**, starting anywhere. Let P be the distribution of its first m division counts, and G the independent-geometric distribution just described. Define Δ(P,G) as the largest difference between the probabilities that P and G assign to the same event; equivalently, half the sum of their absolute probability differences. Thus Δ ranges from 0 to 1.

**History cutoff result.** Put L=log₂N. For each fixed real c, take

`m = floor(L/2 + c√L)`.

Then, as N tends to infinity,

`Δ(P,G) → Φ(2c)`,

uniformly over the location of the interval, where Φ is the standard normal cumulative distribution function. In particular, for every fixed 0<δ<1/2, the distance tends to zero when `1≤m≤(1/2−δ)log₂N`, and to one when `m≥(1/2+δ)log₂N`. The middle of the transition has limiting distance 1/2. The proof and explicit finite-sample bounds are in Kokuno Yumeto, [*Actual Collatz history laws: exact counting and a Gaussian total-variation threshold*, Theorems 3.1 and 4.1](https://github.com/KokunoYumeto/collatz-workbench/blob/main/collatz_reconstruction/research_program/history_law_cutoff_20260914/RESEARCH_NOTE.md).

Why this scale? A prescribed history using A divisions occupies exactly one residue class among the odd integers modulo `2^(A+1)`, giving model probability `2^(-A)`. Exact residue counting controls the approximation from above. Conversely, N starting integers can produce at most N distinct histories, which limits how much of the geometric distribution they can represent. Its typical total division count is about 2m; the transition occurs when this reaches log₂N. Matching these two estimates yields the Gaussian profile.

This distinguishes modelling a complete history from modelling a selected observable. Beyond the cutoff, the complete-history approximation fails, but an entrance location or another statistic that forgets part of the history may still be well approximated. That distinction connects the result to the first section: Tao controls the particular distributions needed for descent, rather than requiring unlimited independent histories. The sampling here is uniform on a finite interval, whereas the entrance-law theorem uses logarithmic weights.

## From statistical information to certificates for individual starts

Statistics do not certify an individual orbit. A separate construction, developed from the project’s Split-Zero work on retaining the information lost by a map, gives an integral algebraic form of that question.

Its resulting abelian group B has an elementary presentation. Introduce a symbol v_n for every positive odd integer, allow finite integer linear combinations, and impose `v_n=v_T(n)` for every actual Collatz edge. For every actual directed cycle, also impose that the sum of its vertex symbols is zero. A component means vertices connected by edges when their directions are ignored. The first relation identifies their symbols. If the component contains a cycle of length m, the second relation becomes `m v=0`.

**Integral classification.** Each component with a cycle of length m contributes exactly the group ℤ/mℤ; each component without a cycle contributes ℤ. The fixed point 1 contributes ℤ/ℤ=0. Consequently,

`B=0  ⇔  every positive integer eventually reaches 1`.

The constructive part is that a finite integer certificate for v_n=0 yields an actual finite path from n to 1 using its recorded edges; conversely, such a path supplies a certificate. Summing the certificate’s coefficients over n’s component forces an integer multiple of its cycle length to equal 1. The cycle therefore has length one, and the only positive fixed point is 1. For example, 3 → 5 → 1 gives `v_3=v_5=v_1=0`, with the last equality supplied by the cycle at 1. The full construction identifies this group with the kernel retained by a first-order change in the edge equations. See Kokuno Yumeto, [*Intrinsic Split-Zero support and the integral first-jet defect of Collatz*, Theorems 1–2 and §§5–8](https://github.com/KokunoYumeto/collatz-workbench/blob/main/collatz_reconstruction/research_program/intrinsic_zero_firstjet_20260915/note.md).

The integer coefficients matter: allowing division by every nonzero integer would erase the ℤ/mℤ contributions of hypothetical longer cycles. Arithmetic constructions in the continuation produce families of pairs m<n whose actual paths meet, hence v_n=v_m. Such comparisons reduce a certificate problem to a smaller source without asserting that n itself visits m. The [all-even common-future extension, Theorem 2 and §§4–6](https://github.com/KokunoYumeto/collatz-workbench/blob/main/collatz_reconstruction/research_program/all_even_join_extension_20260916/note.md), proves parameterized families and bounds the finite support needed for their certificates. Coverage of every start, and therefore B=0, remains unproved.

Together these results provide three different kinds of control: compatible probabilities for descent observations, a precise range for the full-history random model, and exact certificates and reductions for individual sources. Their proofs and scope are separate; none is presented as a proof of the Collatz conjecture.

## PolyClank: how to participate

The point of PolyClank is that the next contribution need not come from the same person or the same model. The [Collatz workbench](https://github.com/KokunoYumeto/collatz-workbench) is the shared starting point; the [cumulative edition](https://github.com/KokunoYumeto/collatz-workbench/releases/tag/cumulative-2026-09-16) provides a readable PDF and downloadable sources. The written arguments establish the general statements; the executable checks make particular calculations reproducible. Neither a model’s confidence nor a test run substitutes for a proof.

1. **Get the material.** Open the repository and choose **Code → Download ZIP**, or use **Fork** to make your own GitHub copy. Give your AI the relevant source files and linked paper, or open the downloaded folder in your coding assistant. A repository link alone may not give a chat model access to its contents.
2. **Work in your own session.** Continue with whatever you and your AI find worth pursuing. Keep the resulting write-up or changed files; retaining the conversation as well makes the reasoning and corrections inspectable.
3. **Send it back.** With a fork, save your changes on a branch and open **Pull requests → New pull request**, targeting `KokunoYumeto/collatz-workbench`, branch `main`. Without a Git workflow, [open an issue](https://github.com/KokunoYumeto/collatz-workbench/issues/new), paste the contribution or attach its files, and link the AI conversation if you want to share it. Remove private material before sharing.

That makes the project a continuing collaboration rather than a finished announcement: readers can inspect the precise result, reproduce its calculations, and return their own continuation through the same public record.
