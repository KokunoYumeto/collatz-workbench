## Collatz: exact histories, integral comparisons, and new arithmetic reductions

This is an update on a continuing human–LLM mathematics project, developed with **ChatGPT 5.6 Sol in Ultra mode in Codex and GPT-6 Astra**. The work now has a public [Collatz workbench](https://github.com/KokunoYumeto/collatz-workbench), with readable proofs, executable calculations, and a [237-page cumulative collection of twenty complete chapters](https://github.com/KokunoYumeto/collatz-workbench/blob/main/editions/cumulative_20260916/latex/main.pdf). The [chapter index](https://github.com/KokunoYumeto/collatz-workbench/blob/main/editions/cumulative_20260916/RESULTS_INDEX.md) links the underlying notes and editable LaTeX; the [release](https://github.com/KokunoYumeto/collatz-workbench/releases/tag/cumulative-2026-09-16) includes the complete supplied source archives and evidence.

The project began with Maxwell C. Siegel's Collatz-related mathematics and the accompanying research notes. It has developed into several connected investigations: exact translations between different descriptions of an orbit, first-passage distributions, finite spectral reconstructions of histories, and arithmetic comparisons between positive integer sources. The [critical exposition of Siegel](https://github.com/KokunoYumeto/collatz-workbench/tree/main/siegel_edition) remains separate from the independent research. Classical and contemporary results retain their original attribution.

### One orbit, three clocks

The ordinary Collatz map takes an odd integer to 3n+1 and an even integer to n/2. The shortened map includes the first division by two in an odd step. The odd-return map is

T(n) = (3n+1)/2ᵃ, where a = ν₂(3n+1).

If a segment has m odd returns and exponent sum A, it takes A shortened steps and A+m ordinary steps. Keeping these clocks explicit lets results stated in different conventions be compared without losing their time parameters.

An ordered exponent word also determines an affine map. If w=(a₁,…,aₘ), S₀=0, Sⱼ=a₁+⋯+aⱼ, and A=Sₘ, then

B_w = Σ[j=0,…,m−1] 3^(m−1−j) 2^Sⱼ,

T_w(n) = (3^m n+B_w)/2^A.

The positive odd integers with exactly that word form a specified residue class modulo 2^(A+1). This is more information than a formal affine expression alone: the congruence verifies the exact valuations at every step. These source classes are the basis of the later constructions.

### A concrete new family of common-future comparisons

The latest [all-even-exponent continuation](https://github.com/KokunoYumeto/collatz-workbench/blob/main/collatz_reconstruction/research_program/all_even_join_extension_20260916/note.md) extends two arithmetic templates from their earlier selected exponents to every positive even interior exponent. Here is one complete family. For every integer v≥0, set

n(v) = 20,241,207 + 1,549,681,956v,

m(v) = 14,024,703 + 1,073,741,824v,

y(v) = 30,361,811 + 2,324,522,934v.

The actual odd-return paths are

n(v) —(1)→ y(v) ←(sixteen 1s, 8, 2, 3)— m(v),

and

n(v) − m(v) = 6,216,504 + 475,940,132v > 0.

Thus every larger source in this progression has an explicitly smaller positive source with the same future endpoint. The right-hand path retains all nineteen odd returns and their intermediate values. At v=0 it rises to 9,211,998,293 before reaching the displayed endpoint.

This comparison is not an assertion that forward iteration from n reaches m. Both sources reach y. That distinction is useful mathematically: it gives a smaller representative of the same eventual orbit component without inventing a forward descent that the construction does not provide. The whole progression survives the preceding comparison rules, so this is additional coverage rather than a new description of an already accepted family.

### Why the apparently infinite template search becomes finite

For even e≥2, write h_e=(2^e+2)/3. The exact identity

ν₃(h_e) = ν₃(e−1)

determines the ternary source layer. If b is the template's positive tail parameter, an admitted source satisfies ν₃(n)=b+ν₃(e−1). Consequently b is fixed once n and e are given.

There is also an explicit exponent bound. For odd n>1, put k(n)=floor(log₂(n−1))−1. Only even e with 2≤e≤k(n) need to be tested, with at most two selectors for each e. The proof derives this from the smaller source's exact formula and the inequality m<n. It therefore exhausts this family of templates on each input; it is not a numerical cutoff chosen for convenience.

Within an admitted template, the largest integral leading run is recovered by an exact 3-adic valuation. This selects the smallest source in that template while keeping the common endpoint and both original paths.

### What Split Zero contributes here

The arithmetic comparisons are carried into an integral construction that retains the source equations, their supports, and the difference between the two path lengths. Work over D=ℤ[ε]/(ε²), put q=1+ε, and attach an edge E_n to n→T(n), with boundary

dε E_n = V_n − q V_T(n).

For two paths n→y and m→y of lengths s and t, their weighted edge columns satisfy

dε(B_left − q^(s−t) B_right) = V_n − q^(s−t) V_m.

All powers of q, including negative powers, are integral units: q^j=1+jε. In the displayed family the signed clock is 1−19=−18. No cycle length or other nonunit integer is divided out.

The accepted comparisons assemble into explicit chain-homotopy retractions. Their proofs retain the surviving root classes instead of declaring them zero. The budget-preserving version checks both complete paths against

R₀(n) = max{130(n+1), floor[64n(4/3)^floor(log₃ n)] + 21}.

For n≥27, this is at most 64n^(log₃4)+21. This controls the original vertices used in the constructed chain columns. It is not a universal orbit-height or stopping-time bound. The unrestricted template construction has a separate, larger support bound.

The earlier [finite-history spectral reconstruction](https://github.com/KokunoYumeto/collatz-workbench/tree/main/collatz_reconstruction/research_program/split_zero_history_20260913) is another part of the programme: it encodes a finite distribution of arithmetic histories in a Hurwitz-zeta deformation and recovers the distribution by explicit inverses. The current integral construction keeps actual source relations and their residual classes, rather than relying on a scalar spectral invariant to carry all that information.

### First-passage measures and Tao's theorem

The separate [Clocks and First-Passage Measures in Tao's Collatz Theorem](https://github.com/KokunoYumeto/collatz-workbench/tree/main/collatz_reconstruction/preprints/tao_clock_audit) uses Tao's v7 as its baseline. It develops exact clock changes, finite-cutoff harmonic weights, composition of first-passage maps, and compatible limiting first-entry laws along a common sequence of starting scales. It is a reconstruction and extension of that framework, not a correction to Tao's almost-bounded-orbit theorem or a stronger orbit-minimum estimate.

The cumulative collection also contains exact history-law counting and a Gaussian total-variation threshold, stopped affine transport, cycle-relative cohomology, and a sequence of increasingly broad arithmetic reductions. The chapter index supplies the full statements and their hypotheses.

### Proofs, calculations, and collaboration

The new all-even checker has been rerun in ordinary and optimized Python, with 87,989 exact checks in each execution. Its separately implemented affine auditor checks 512 family fixtures and 24,180 affine-coefficient equations. These are finite reproducibility checks alongside the written all-parameter proofs. Earlier large crossing certificates are preserved with their original ranges and receipts; this update does not relabel them as newly performed computations or as a proof of all orbits.

The remaining mathematical question is how far these exact arithmetic comparisons can reduce the residual source set, and what further relations can be proved for the sources that survive. The work already supplies explicit families, finite membership algorithms, and integral maps with controlled support. Those results can be studied and improved independently of a proof of the Collatz conjecture.

The **PolyClank** aspect is the public research record: readable mathematics together with the constructions, calculations, corrections, and source history that make it possible to continue the work. The public collaboration name is **Kokuno Yumeto**; both **ChatGPT 5.6 Sol** and **GPT-6 Astra** contributed. Mathematical contributions, checks, and corrections are welcome through the workbench's issues and pull requests. A useful contribution can be a better proof, a new exact comparison, a sharper bound, or a concrete counterexample to a stated claim.
