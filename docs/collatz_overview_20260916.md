# Collatz: entrance distributions, the limits of random histories, and finite arithmetic certificates

The Collatz conjecture asks whether repeatedly replacing an even positive integer by n/2 and an odd one by 3n+1 always reaches 1. This workbench studies three related questions: how trajectories descend statistically, how long a probabilistic model describes their complete histories, and how to certify statements about individual trajectories using exact integer equations.

It is a **PolyClank** project: open, cumulative mathematical collaboration between people and language models, in the spirit of Polymath. The public work includes proofs, source files, executable checks and records of development, so another person can continue from the mathematics rather than from a summary of a conversation. The work described here was developed under **Kokuno Yumeto**, with **ChatGPT 5.6 Sol, Ultra mode, in Codex**, and **GPT-6 Astra**. Participation instructions are below.

## From Tao’s theorem to compatible entrance distributions

There is a substantial history behind the statistical approach. Terras (1976) and Everett (1977) proved that the proportion of starts up to X that eventually fall below themselves tends to one as X grows: a natural-density statement. Allouche and Korec obtained stronger bounds on how far they fall. Repeating such arguments is difficult because descended values may concentrate in the exceptional set for the next descent. Tao explains this obstruction and the earlier results in [*Almost all orbits of the Collatz map attain almost bounded values*, §1.1, version 7](https://arxiv.org/html/1909.03562v7#S1.SS1).

Tao’s theorem, first announced in 2019, says that for **every** function f(n) tending to infinity, the minimum of the orbit starting at n is less than f(n) for a set of starting values of logarithmic density one. Here logarithmic density weights n by 1/n: the exceptional starts up to X have total weight negligible compared with the sum of 1/n over all starts up to X. The function f may grow arbitrarily slowly. This is [Tao’s Theorem 1.3](https://arxiv.org/html/1909.03562v7#S1.Thmtheorem3).

To state the workbench’s additional deduction, follow only the odd values of an orbit. One step now means applying 3n+1 and dividing by 2 until an odd number remains. Call this map T. Thus 3 → 5 → 1, with respectively one and four divisions. If m such steps use A divisions altogether, they represent m+A steps of the original Collatz map. Keeping these clocks distinct is important when comparing statistical statements.

Formally, the odd-return map and its division count are

```
X={1,3,5,…},
T(n)=(3n+1)/2^a(n),    a(n)=ν₂(3n+1).
```

Here ν₂(z) is the exponent of 2 dividing z.

For x≥1 and n∈X, let p_x(n) be the first value of the orbit n,T(n),T²(n),… lying in [1,x]. If there is no such value, set p_x(n)=†, a separate failure state, and set p_x(†)=†. Write E_x=(X∩[1,x])∪{†} and K_xμ=(p_x)₊μ for pushforward of a measure. Here pushforward means adding the probabilities of all starts with the same entrance value: `(K_xμ)(z)=Σ[n:p_x(n)=z]μ(n)`. It preserves total probability and cannot increase the sum of absolute differences between two distributions. These maps satisfy

```
p_x∘p_y=p_x=p_y∘p_x,       K_xK_y=K_x=K_yK_x     (1≤x≤y).
```

In words, one can first wait until the orbit reaches y and then continue until it reaches x. The same identity holds when a trajectory fails to enter: its † value is retained. This exact composition is what lets the successive statistical estimates fit together.

Take α=1001/1000. For sufficiently large s, let μ_s be the logarithmically weighted probability on the odd integers in [s,s^α]:

```
h_s=Σ[n odd, s≤n≤s^α]1/n,       μ_s(n)=1/(h_s n).
```

[Tao's Proposition 1.11, version 7](https://arxiv.org/html/1909.03562v7#S1.Thmtheorem11) gives constants B,c>0 controlling failure and the discrepancy between two adjacent starting scales. Keeping failure separate from the value 1 gives an absolute constant B′ such that, for all sufficiently large x,

```
||(K_xμ_(x^α))−(K_xμ_(x^(α²)))||₁ ≤ B′(log x)^(−c),
(K_xμ_(x^α))({†}) ≤ Bx^(−c).
```

Here ||η||₁=Σ_z|η(z)|, and log is the natural logarithm.

**First-entry limit theorem.** Fix any sufficiently large base b and put t_j=b^(α^j), j≥0. For every real x≥1 the probabilities

```
λ_(x,j)^(b)=K_xμ_(t_(j+1))
```

converge in total variation to a probability λ_x^(∞,b) on E_x. With L_c=B′/(1−α^(−c)),

```
||λ_(x,j)^(b)−λ_x^(∞,b)||₁ ≤ L_c(log t_j)^(−c)   (1≤x≤t_j),
K_xλ_y^(∞,b)=λ_x^(∞,b)                           (1≤x≤y),
λ_x^(∞,b)({†}) ≤ Bx^(−c/α)+L_cα^c(log x)^(−c)   (x≥b).
```

Thus approximate stabilization at successive starting scales yields an exactly compatible limiting family at **all** thresholds, using one common sequence of input measures. The proof sums the adjacent-scale errors: `Σ[i≥j](log t_i)^(−c)=(log t_j)^(−c)/(1−α^(−c))`. Replacing b by b^(α^k), for a nonnegative integer k, leaves this family unchanged; equality for arbitrary different bases is not established.

**Joint-law theorem.** For any integer r≥1 and finite list 1≤x₁≤⋯≤x_r, sample N_j with law μ_(t_(j+1)). The joint law of

```
(p_x₁(N_j),…,p_x_r(N_j))
```

converges with the same bound L_c(log t_j)^(−c) whenever x_r≤t_j, with no factor depending on r. Its limit is J₊λ_x_r^(∞,b), where

```
J(z)=(p_x₁(z),…,p_x_r(z))
```

is a bijection from E_x_r onto the tuples (z₁,…,z_r)∈E_x₁×⋯×E_x_r satisfying p_x_i(z_(i+1))=z_i for 1≤i<r. The inverse is projection to the last coordinate; pushforward by J preserves the ℓ¹ distance exactly.

The largest-threshold entrance therefore contains precisely the information needed for every smaller-threshold entrance. This is why observing them jointly does not multiply the error by the number of observations.

These are distributional consequences of Tao's analytic stabilization estimate. The same transport proof recovers his quantitative orbit-minimum estimate

```
Σ[1≤n≤M, C_min(n)>K]1/n ≤ A log M/(log K)^c    (K,M≥2),
```

Here A is an absolute constant, C(n)=3n+1 for odd n and C(n)=n/2 for even n, and C_min(n)=min[j≥0]C^j(n). The orbit-minimum bound is Tao's; the additional statements here specify the compatible limiting entrance laws and their joint distributions. [Full proof, §§3–4 of the preprint](https://github.com/KokunoYumeto/collatz-workbench/blob/main/collatz_reconstruction/preprints/tao_clock_audit/output/pdf/tao_clock_audit.pdf), [source](https://github.com/KokunoYumeto/collatz-workbench/blob/main/collatz_reconstruction/preprints/tao_clock_audit/sections/consequences.tex).

This supplies distributions for simultaneous descent observations, with quantitative control, from Tao’s analytic estimate. It is an additional distributional conclusion, not an improvement of his orbit-minimum bound or a correction to his theorem. The family is constructed for the chosen base b; independence from an arbitrary different base is not established.

## How long does the random-history model remain accurate?

The preceding result concerns entrance locations. A more demanding question asks for the distribution of the **entire sequence of divisions**. The familiar model treats successive division counts as independent, with probabilities 1/2, 1/4, 1/8, … for one, two, three, … divisions. Tao makes a finite-history version precise in [Proposition 1.9 and §4](https://arxiv.org/html/1909.03562v7#S4). The workbench determines a sharp boundary for this approximation under interval sampling.

Choose n uniformly from **N consecutive positive odd integers**, starting anywhere. Let P be the distribution of its first m division counts, and G the independent-geometric distribution just described. Define Δ(P,G) as the largest difference between the probabilities that P and G assign to the same event; equivalently, half the sum of their absolute probability differences. Thus Δ ranges from 0 to 1.

### Exact counting of chronological histories

Let N,m≥1 and b≥0 be integers. Sample n uniformly from

```
I(N,b)={2b+1,2b+3,…,2(b+N)−1},
```

and let P(N,b,m) be the law of the complete exponent word w=(a₁,…,a_m). Here `a_i=a(T^(i−1)(n))` is the actual number of divisions at the i-th odd return. The word records the divisions in chronological order. For any positive exponent word, put

```
A₀=0,    A_j=a₁+⋯+a_j,    A=A_m,
B_w=Σ[j=0,…,m−1] 3^(m−1−j)2^A_j.
```

On this branch, `T^m(n)=(3^m n+B_w)/2^A`. The additive term B_w is retained: the division history determines an affine map, not just a multiplier.

Let r_w be the unique odd integer in 1≤r_w<2^(A+1) satisfying

```
3^m r_w+B_w ≡ 2^A  (mod 2^(A+1)),
```

and set h_w=(r_w−1)/2. Then 2j+1 has exactly the word w if and only if j≡h_w mod 2^A. Consequently,

```
C(N,b,w)=floor((b+N−1−h_w)/2^A)−floor((b−1−h_w)/2^A),
P(N,b,m)(w)=C(N,b,w)/N,
|P(N,b,m)(w)−2^(−A)|≤1/N.
```

These statements hold for every word and every interval location b. [Proof, §2](https://github.com/KokunoYumeto/collatz-workbench/blob/main/collatz_reconstruction/research_program/history_law_cutoff_20260914/RESEARCH_NOTE.md).

This converts a trajectory question into exact residue counting. The floor difference counts the starts in the interval that lie in that residue class; the error 1/N holds for each word even when its modulus is larger than the interval.

### Finite probability bounds, including the tail

Define the product geometric law G_m(w)=2^(−A(w)) and use

```
Δ(P,G)=½Σ_w|P(w)−G(w)|.
```

For each integer H≥0, put

```
K_m(H)=binom(H,m), with K_m(H)=0 when H<m,
Q_m(H)=2^(−H)Σ[j=0,…,min(m−1,H)]binom(H,j).
```

The integer H is a cutoff on the total number of divisions. K_m(H) counts the positive words whose total is at most H; Q_m(H) is the geometric probability that the total exceeds H. The cutoff retains the tail rather than discarding its mass. For every N,m≥1 and b,H≥0,

```
max{0,Q_m(H)−N·2^(−H−1)}
  ≤ Δ(P(N,b,m),G_m)
  ≤ min{1,Q_m(H)+K_m(H)/N}.
```

The two bounds may be optimized over H separately. The upper bound also admits the rounding refinement

```
Δ ≤ min{1, Q_m(H)
       + (1/N)Σ[A=m,…,H]binom(A−1,m−1){N·2^(−A)}},
```

where braces denote fractional part. For N=2^L with integer L≥0,

```
Δ(P(2^L,b,m),G_m)
 = Q_m(L)−Σ[w∈supp P(2^L,b,m), A(w)>L]2^(−A(w)).
```

All statements are uniform in b. [Proof, §3](https://github.com/KokunoYumeto/collatz-workbench/blob/main/collatz_reconstruction/research_program/history_law_cutoff_20260914/RESEARCH_NOTE.md).

For the upper bound, sum the exact counting errors over the retained words and add the geometric tail. For the lower bound, the actual sample produces at most N different words; each word beyond the cutoff has geometric mass at most `2^(−H−1)`. This is a limitation on approximating the whole probability distribution, not a failure of an individual trajectory. In the dyadic identity, `supp P` means the words actually observed with positive probability.

### The Gaussian transition

For every fixed c∈ℝ, let L_N=log₂N and

```
m_N=floor(L_N/2+c√L_N).
```

Writing Φ for the standard normal distribution function,

```
sup[b∈ℤ, b≥0] |Δ(P(N,b,m_N),G_(m_N))−Φ(2c)| → 0
as N→∞.
```

In particular the limiting distance at c=0 is ½. For every fixed 0<δ<½, the distance tends uniformly in b to zero when 1≤m≤(½−δ)log₂N, and to one when m≥(½+δ)log₂N. The clock m counts odd returns. [Proof, §4](https://github.com/KokunoYumeto/collatz-workbench/blob/main/collatz_reconstruction/research_program/history_law_cutoff_20260914/RESEARCH_NOTE.md).

Why this scale? A prescribed history using A divisions occupies exactly one residue class among the odd integers modulo `2^(A+1)`, giving model probability `2^(-A)`. Exact residue counting controls the approximation from above. Conversely, N starting integers can produce at most N distinct histories, which limits how much of the geometric distribution they can represent. Its typical total division count is about 2m; the transition occurs when this reaches log₂N. Matching these two estimates yields the Gaussian profile.

This distinguishes modelling a complete history from modelling a selected observable. Beyond the cutoff, the complete-history approximation fails, but an entrance location or another statistic that forgets part of the history may still be well approximated. That distinction connects the result to the first section: Tao controls the particular distributions needed for descent, rather than requiring unlimited independent histories. The sampling here is uniform on a finite interval, whereas the entrance-law theorem uses logarithmic weights.

## From statistical information to certificates for individual starts

Statistics do not certify an individual orbit. A separate construction, developed from the project’s Split-Zero work on retaining the information lost by a map, gives an integral algebraic form of that question.

Its resulting abelian group B has an elementary presentation. Introduce a symbol v_n for every positive odd integer, allow finite integer linear combinations, and impose `v_n=v_T(n)` for every actual Collatz edge. For every actual directed cycle, also impose that the sum of its vertex symbols is zero. A component means vertices connected by edges when their directions are ignored. The first relation identifies their symbols. If the component contains a cycle of length m, the second relation becomes `m v=0`.

### The integral group and the maps defining it

For the precise construction, a directed edge is the actual equation `n→T(n)`. The graph includes the edge `1→1`, corresponding to the elementary cycle `1→4→2→1`. An edge vector is a finite integer combination of such edges, and a vertex vector is a finite integer combination of their endpoints. Even on the infinite graph, no infinite sums are admitted.

Let C⁰=ℤ^(X) have edge basis E_n and C¹=ℤ^(X) have vertex basis V_n. Define

```
JE_n=V_n,    PE_n=V_T(n),    d=J−P,
D=ℤ[ε]/(ε²),                d_ε=J−(1+ε)P.
```

Thus d takes an edge to its starting vertex minus its ending vertex. The ring D consists of pairs written `a+εb`, with multiplication `(a+εb)(c+εd)=ac+ε(ad+bc)`. Keeping ε while imposing ε²=0 retains a first-order coefficient; setting ε=0 forgets it. The altered differential d_ε records that coefficient on the same original edges.

Let K=[C⁰→C¹] have differential d and K_ε=[C⁰⊗D→C¹⊗D] have differential d_ε. Constant reduction r:ε→0 induces a map on H¹, where H¹ is the cokernel of the displayed differential. A cokernel here is the vertex module modulo the displayed edge relations. The kernel B consists of classes that become zero when ε is set to zero. It is the same group as the elementary presentation above, under `v_n↦[εV_n]`. It satisfies

```
B := ker(H¹(K_ε)→H¹(K))
   ≅ C¹/(dC⁰+P ker d)
   ≅ εH¹(K_ε).
```

On the full positive odd graph,

```
B ≅ ⊕[nontrivial positive cycles C] ℤ/m_Cℤ
     ⊕[nonperiodic components A] ℤ,
```

Here ⊕ denotes a direct sum, so each element has only finitely many nonzero component coordinates, and m_C is the actual primitive cycle length: the number of distinct vertices before the cycle repeats, not the length of a repeated word. More precisely, H¹(K_ε) on a cycle component of length m is D/(mε), and on a nonperiodic component it is D. The fixed loop contributes D/(ε) and zero to B.

The component calculation has a direct reason. An ordinary edge relation identifies its endpoints. Summing the edges of a cycle with m vertices then contributes m times its component generator to the extra relation; a component without a cycle supplies no such relation. This gives ℤ/mℤ in the first case and ℤ in the second.

The connecting map is β:ker d→coker d, β(u)=[−Pu]. It is injective over ℤ, and the following are equivalent:

```
Every positive integer reaches 1;
B=0;
εH¹(K_ε)=0;
β is an integral isomorphism.
```

[Proofs, §§4–7](https://github.com/KokunoYumeto/collatz-workbench/blob/main/collatz_reconstruction/research_program/intrinsic_zero_firstjet_20260915/note.md).

### Finite witnesses and extraction of an actual path

For each n∈X, write ξ_n=[εV_n]. Then ξ_n=0 if and only if finite integral edge vectors u,v satisfy

```
du=0,       dv−Pu=V_n.
```

Every such pair yields an actual finite path from n to 1 using only its finite edge support. Conversely, a first-arrival path p from n to 1 gives the certificate

```
u=−E₁,     v=Σ[edges of p]E.
```

For n=1 take v=0. [Proof, §8](https://github.com/KokunoYumeto/collatz-workbench/blob/main/collatz_reconstruction/research_program/intrinsic_zero_firstjet_20260915/note.md).

The constructive part is that a finite integer certificate for v_n=0 yields an actual finite path from n to 1 using its recorded edges; conversely, such a path supplies a certificate. Summing the certificate’s coefficients over n’s component forces an integer multiple of its cycle length to equal 1. The cycle therefore has length one, and the only positive fixed point is 1. For example, 3 → 5 → 1 gives `v_3=v_5=v_1=0`, with the last equality supplied by the cycle at 1. The full construction identifies this group with the kernel retained by a first-order change in the edge equations. See Kokuno Yumeto, [*Intrinsic Split-Zero support and the integral first-jet defect of Collatz*, Theorems 1–2 and §§5–8](https://github.com/KokunoYumeto/collatz-workbench/blob/main/collatz_reconstruction/research_program/intrinsic_zero_firstjet_20260915/note.md).

The integer coefficients matter: allowing division by every nonzero integer would erase the ℤ/mℤ contributions of hypothetical longer cycles. On a finite collection of edges, an unfinished component is just missing equations; its free generator is not evidence of a divergent orbit. The equivalence above concerns the full graph.

## Arithmetic families that reduce a source to a smaller one

A finite certificate can be assembled from comparisons between starts. If actual paths from n and m meet at the same value, their later futures agree and `ξ_n=ξ_m`. When m<n this replaces the source by a smaller one for the certificate problem, even when n never visits m. The following families make that comparison explicit in the division-word coordinates already introduced.

### Complete families for every even interior exponent

The parameters describe the two paths. The integer b is a tail parameter, e is an even division count in the longer path, and σ chooses one of two short paths. The notation `ν₃(z)` means the exponent of 3 dividing the nonzero integer z. The symbols J,Q,K in this arithmetic subsection are local integer parameters; they are not the earlier J map or K complex.

Fix integers b≥1, even e≥2, and σ∈{0,1}. Define

```
h=(2^e+2)/3,     t=ν₃(h)=ν₃(e−1),
a=min{a≥1:2^(a+e+2b−σ)<3^(a+b)},
J=2^(e+2b−σ),   Q=3^(a+b),   K=2^aJ<Q,
(d_σ,r_σ)=(4,3) if σ=0, and (32,27) if σ=1.
```

The strict inequality in the definition of a makes the coefficient of the smaller source less than one. The equality `ν₃(h)=ν₃(e−1)` identifies its exact divisibility by 3; ignoring this term would put some even-exponent families on the wrong source progression. Since the powers of 2 and 3 are coprime, the following two congruences select one residue class.

Let n₀ be the unique representative 0<n₀<d_σQ satisfying

```
n₀≡r_σ (mod d_σ),     Jn₀+h3^b≡0 (mod Q),
```

and put m₀=(Kn₀+2^ah3^b)/Q−1. The complete positive pairs for the following two word templates are

```
n(v)=n₀+d_σQv,      m(v)=m₀+d_σKv,      v∈ℤ, v≥0.

σ=0: left word (1);     right word (1^a,e,2^(b−1),3).
σ=1: left word (1,2,1); right word (1^a,e,2^(b−1),1,1,3).
```

Here 1^a and 2^(b−1) denote repeated exponents. Both actual paths have exactly their displayed valuations and a common endpoint. For every v≥0,

```
0<m(v)<n(v),      ν₃(n(v))=b+t.
```

The common endpoint is (3n(v)+1)/2 for σ=0 and (27n(v)+23)/16 for σ=1. Conversely, equality of these word endpoints on their positive sources gives precisely the displayed progression. [Proof, Theorem 2](https://github.com/KokunoYumeto/collatz-workbench/blob/main/collatz_reconstruction/research_program/all_even_join_extension_20260916/note.md).

Completeness here is for the two displayed word templates with the stated parameters, not a classification of every possible common-future pair.

### Finite membership and an additional infinite progression

For any fixed odd n>1, set k(n)=floor(log₂(n−1))−1. Every admitted coefficient-contracting template just displayed occurs among the finite tests

```
even 2≤e≤k(n),
b=ν₃(n)−ν₃(e−1)≥1,
σ∈{0,1},
```

together with its defining dyadic residue, a≤k(n), and ternary congruence. There are at most 2 floor(k(n)/2) labels to examine. For each admitted label, all admissible leading runs are exactly

```
a≤a′≤a_max:=ν₃(J(n/3^b)+h),
m_a′=2^a′(J(n/3^b)+h)/3^a′−1.
```

The maximum run gives the smallest source in that template. For a≤a′<a_max, adjacent sources satisfy T(m_(a′+1))=m_a′.

The two restrictions have arithmetic reasons: the valuation formula forces `b=ν₃(n)−ν₃(e−1)`, while `2^(a′+1)≤m_a′+1≤n−1` forces `a′≤k(n)`. The contraction inequality also forces `a≥e`: if `a≤e−1`, then `(3/2)^a<2^(e−1)`, whereas contraction requires `(3/2)^a>2^(e−σ)(4/3)^b>2^(e−1)`. Thus `e≤a≤a′≤k(n)`, and the apparent search over every even exponent is a finite test for each input. The maximal leading run selects the smallest source within the chosen template; this is an exact arithmetic search, not a claim about all Collatz stopping times.

For a concrete infinite family, take `b=2, e=8, σ=0`, giving `h=86, t=0, a=16`. For every integer v≥0, the resulting pair is

```
20,241,207+1,549,681,956v --(1)--> 30,361,811+2,324,522,934v,
14,024,703+1,073,741,824v --(1^16,8,2,3)--> the same endpoint.
```

A root means an integer to which that reduction has no applicable smaller-source move; it need not be a Collatz fixed point. Every larger source in this progression was such a root of the preceding reduction, which used a finite catalogue and the infinite e=2,6 families. The displayed e=8 family therefore adds genuine source coverage. The source difference is 6,216,504+475,940,132v. This is a shared-future source comparison; it does not assert forward iteration from the larger source to the smaller one. [Proofs, §§4–5](https://github.com/KokunoYumeto/collatz-workbench/blob/main/collatz_reconstruction/research_program/all_even_join_extension_20260916/note.md).

The two lines are paths from different starts to the same endpoint. Their difference yields an exact relation between the source classes. Because the smaller source is strictly smaller for every v≥0, this relation can be used inside a terminating reduction procedure.

### Composing the reductions with explicit certificate bounds

The remaining question is how to compose the smaller-source comparisons without losing their original edges or their clock differences. Return now to the edge and vertex modules over D. In this subsection Q denotes a linear map; it is no longer the integer modulus of the family formulas.

Put q=1+ε. For a path x₀→⋯→x_s put B=Σ[i=0,…,s−1]q^iE_x_i. Paths n→y and m→y of lengths s,t then satisfy

```
d_ε(B_left−q^(s−t)B_right)=V_n−q^(s−t)V_m,
q^j=1+jε for every integer j.
```

Here B is the weighted edge vector of this path, not the group B from the classification. The integer `s−t` is the difference in odd-return clocks of the two paths. The identity retains that difference even when it is negative.

Apply the preceding reduction rules in their existing order and use the new comparisons at their retained roots. Among new candidates passing the chosen support test, select the smallest target, with the path-length and label tie-breakers specified in the linked construction. For a selected comparison, set `B_n=B_left−q^jB_right`, with smaller source m and clock j=s−t. Define on vertex basis elements, then extend D-linearly:

```
H(V_n)=B_n+q^jH(V_m),    Q(V_n)=q^jQ(V_m),    F=I−Hd_ε.
```

Here H:C¹⊗D→C⁰⊗D, Q:C¹⊗D→C¹⊗D, and F:C⁰⊗D→C⁰⊗D. At a final root, H=0 and Q=I. Every recursion terminates and

```
d_εH=I−Q,   Q²=Q,   HQ=0,
d_εF=Qd_ε,  F²=F,   FH=0.
```

The map H records the finite edge correction, Q sends a vertex to its retained root with the clock factor attached, and F is the corresponding projection on edge vectors. The equation `d_εH=I−Q` says exactly how a source differs from its reduced representative. The identities Q²=Q and F²=F say that repeating the reduction does not change it again; `d_εF=Qd_ε` says that the edge and vertex reductions respect the original equations.

For an effective construction, its finite certificate must also have a bound on the vertices it uses. Accepting a new comparison only when both complete paths meet the predecessor's budget bounds every original vertex used in H(V_n) by

```
R₀(n)=max{130(n+1),floor(64n(4/3)^floor(log₃n))+21},
R₀(n)≤64n^(log₃4)+21  for n≥27.
```

The entire concrete progression above passes this budget. Alternatively, admitting every successful template gives, for odd n>1,

```
R_*(n)=max{130(n+1),floor((n−1)3^k(n)/2^k(n))−1}.
```

Both versions have at most

```
K_*(n)=((n−1)/2)max{24,k(n)+floor(log₃n)+6}
```

uncollected edge terms. There are at most `(n−1)/2` moves because each strictly lowers an odd source. Each move uses at most `max{24,k(n)+floor(log₃n)+6}` edges: 24 for an older comparison, and the other bound for a new one. The accumulated clock exponents have absolute value at most `K_*(n)`. Since `q^j=1+jε`, the sums of absolute constant and ε coefficients are at most `K_*(n)` and `K_*(n)²` respectively. Set `R_*(1)=1` and `K_*(1)=0`. The count is taken before equal edge terms are collected, so cancellation does not conceal the size of the certificate. These bounds concern the homotopy column H(V_n), not arbitrary F or Q columns or the height or stopping time of a forward orbit. The smaller budget R₀ applies to the budget-tested version; the unrestricted version has its own bound `R_*` displayed above. The two acceptance policies define two possibly different triples (H,Q,F). [Proofs, §6](https://github.com/KokunoYumeto/collatz-workbench/blob/main/collatz_reconstruction/research_program/all_even_join_extension_20260916/note.md), [predecessor bound](https://github.com/KokunoYumeto/collatz-workbench/blob/main/collatz_reconstruction/research_program/bilateral_root_bounds_20260916/note.md).

The remaining global assertion is B=0, equivalently the vanishing of every ξ_n; the stated reductions do not establish it.

Together these results provide three different kinds of control: compatible probabilities for descent observations, a precise range for the full-history random model, and exact certificates and reductions for individual sources. Their proofs and scope are separate; none is presented as a proof of the Collatz conjecture. The [cumulative reader](https://github.com/KokunoYumeto/collatz-workbench/blob/main/editions/cumulative_20260916/latex/main.pdf) and [chapter index](https://github.com/KokunoYumeto/collatz-workbench/blob/main/editions/cumulative_20260916/RESULTS_INDEX.md) contain the full proofs and the surrounding research.

## PolyClank: how to participate

The point of PolyClank is that the next contribution need not come from the same person or the same model. The [Collatz workbench](https://github.com/KokunoYumeto/collatz-workbench) is the shared starting point; the [cumulative edition](https://github.com/KokunoYumeto/collatz-workbench/releases/tag/cumulative-2026-09-16) provides a readable PDF and downloadable sources. The written arguments establish the general statements; the executable checks make particular calculations reproducible. Neither a model’s confidence nor a test run substitutes for a proof.

1. **Get the material.** Open the repository and choose **Code → Download ZIP**, or use **Fork** to make your own GitHub copy. Give your AI the relevant source files and linked paper, or open the downloaded folder in your coding assistant. A repository link alone may not give a chat model access to its contents.
2. **Work in your own session.** Continue with whatever you and your AI find worth pursuing. Keep the resulting write-up or changed files; retaining the conversation as well makes the reasoning and corrections inspectable.
3. **Send it back.** With a fork, save your changes on a branch and open **Pull requests → New pull request**, targeting `KokunoYumeto/collatz-workbench`, branch `main`. Without a Git workflow, [open an issue](https://github.com/KokunoYumeto/collatz-workbench/issues/new), paste the contribution or attach its files, and link the AI conversation if you want to share it. Remove private material before sharing.

That makes the project a continuing collaboration rather than a finished announcement: readers can inspect the precise result, reproduce its calculations, and return their own continuation through the same public record.
