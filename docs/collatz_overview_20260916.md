# Collatz: first-entry laws from Tao’s theorem, sharp history statistics, and integral arithmetic reductions

The following statements use the positive odd-return map

```
X = {1,3,5,…},
T(n) = (3n+1)/2^a(n),     a(n)=ν₂(3n+1).
```

All graph modules below consist of finite sums on the actual labelled edges n→T(n). The vertex and loop at 1 are included. Proofs: [237-page collection](https://github.com/KokunoYumeto/collatz-workbench/blob/main/editions/cumulative_20260916/latex/main.pdf), [chapter index](https://github.com/KokunoYumeto/collatz-workbench/blob/main/editions/cumulative_20260916/RESULTS_INDEX.md).

## 1. Exactly compatible first-entry laws from Tao's stabilization theorem

For x≥1 and n∈X, let p_x(n) be the first value of the orbit n,T(n),T²(n),… lying in [1,x]. If there is no such value, set p_x(n)=†, a separate failure state, and set p_x(†)=†. Write E_x=(X∩[1,x])∪{†} and K_xμ=(p_x)₊μ for pushforward of a measure. These maps satisfy

```
p_x∘p_y=p_x=p_y∘p_x,       K_xK_y=K_x=K_yK_x     (1≤x≤y).
```

Take α=1001/1000. For sufficiently large s, let μ_s be the logarithmically weighted probability on the odd integers in [s,s^α]:

```
h_s=Σ[n odd, s≤n≤s^α]1/n,       μ_s(n)=1/(h_s n).
```

[Tao's Proposition 1.11, version 7](https://arxiv.org/html/1909.03562v7), gives constants B,c>0 controlling failure and the discrepancy between two adjacent starting scales. Keeping failure separate from the value 1 gives an absolute constant B′ such that, for all sufficiently large x,

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

Thus approximate stabilization at successive starting scales yields an exactly compatible limiting family at **all** thresholds, using one common sequence of input measures. The proof sums the adjacent-scale errors: Σ[i≥j](log t_i)^(−c)=(log t_j)^(−c)/(1−α^(−c)). Replacing b by b^(α^k), for a nonnegative integer k, leaves this family unchanged; equality for arbitrary different bases is not established.

**Joint-law theorem.** For any integer r≥1 and finite list 1≤x₁≤⋯≤x_r, sample N_j with law μ_(t_(j+1)). The joint law of

```
(p_x₁(N_j),…,p_x_r(N_j))
```

converges with the same bound L_c(log t_j)^(−c) whenever x_r≤t_j, with no factor depending on r. Its limit is J₊λ_x_r^(∞,b), where

```
J(z)=(p_x₁(z),…,p_x_r(z))
```

is a bijection from E_x_r onto the tuples (z₁,…,z_r)∈E_x₁×⋯×E_x_r satisfying p_x_i(z_(i+1))=z_i for 1≤i<r. The inverse is projection to the last coordinate; pushforward by J preserves the ℓ¹ distance exactly.

These are distributional consequences of Tao's analytic stabilization estimate. The same transport proof recovers his quantitative orbit-minimum estimate

```
Σ[1≤n≤M, C_min(n)>K]1/n ≤ A log M/(log K)^c    (K,M≥2),
```

Here A is an absolute constant, C(n)=3n+1 for odd n and C(n)=n/2 for even n, and C_min(n)=min[j≥0]C^j(n). The orbit-minimum bound is Tao's; the additional statements here specify the compatible limiting entrance laws and their joint distributions. [Full proof, §§3–4 of the preprint](https://github.com/KokunoYumeto/collatz-workbench/blob/main/collatz_reconstruction/preprints/tao_clock_audit/output/pdf/tao_clock_audit.pdf), [source](https://github.com/KokunoYumeto/collatz-workbench/blob/main/collatz_reconstruction/preprints/tao_clock_audit/sections/consequences.tex).

## 2. Exact finite history counts

Let N,m≥1 and b≥0 be integers. Sample n uniformly from

```
I(N,b)={2b+1,2b+3,…,2(b+N)−1},
```

and let P(N,b,m) be the law of the complete exponent word w=(a₁,…,a_m). For any positive exponent word, put

```
A₀=0,    A_j=a₁+⋯+a_j,    A=A_m,
B_w=Σ[j=0,…,m−1] 3^(m−1−j)2^A_j.
```

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

## 3. Finite total-variation bounds and an exact dyadic formula

Define the product geometric law G_m(w)=2^(−A(w)) and use

```
Δ(P,G)=½Σ_w|P(w)−G(w)|.
```

For each integer H≥0, put

```
K_m(H)=binom(H,m), with K_m(H)=0 when H<m,
Q_m(H)=2^(−H)Σ[j=0,…,min(m−1,H)]binom(H,j).
```

For every N,m≥1 and b,H≥0,

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

## 4. Gaussian critical window for complete histories

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

## 5. Integral classification of the first-jet obstruction

Let C⁰=ℤ^(X) have edge basis E_n and C¹=ℤ^(X) have vertex basis V_n. Define

```
JE_n=V_n,    PE_n=V_T(n),    d=J−P,
D=ℤ[ε]/(ε²),                d_ε=J−(1+ε)P.
```

Let K=[C⁰→C¹] have differential d and K_ε=[C⁰⊗D→C¹⊗D] have differential d_ε. Constant reduction r:ε→0 induces a map on H¹, where H¹ is the cokernel of the displayed differential. Its kernel B satisfies

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

where m_C is the actual primitive cycle length. More precisely, H¹(K_ε) on a cycle component of length m is D/(mε), and on a nonperiodic component it is D. The fixed loop contributes D/(ε) and zero to B.

The connecting map is β:ker d→coker d, β(u)=[−Pu]. It is injective over ℤ, and the following are equivalent:

```
Every positive integer reaches 1;
B=0;
εH¹(K_ε)=0;
β is an integral isomorphism.
```

[Proofs, §§4–7](https://github.com/KokunoYumeto/collatz-workbench/blob/main/collatz_reconstruction/research_program/intrinsic_zero_firstjet_20260915/note.md).

## 6. Finite integral witnesses and path extraction

For each n∈X, write ξ_n=[εV_n]. Then ξ_n=0 if and only if finite integral edge vectors u,v satisfy

```
du=0,       dv−Pu=V_n.
```

Every such pair yields an actual finite path from n to 1 using only its finite edge support. Conversely, a first-arrival path p from n to 1 gives the certificate

```
u=−E₁,     v=Σ[edges of p]E.
```

For n=1 take v=0. [Proof, §8](https://github.com/KokunoYumeto/collatz-workbench/blob/main/collatz_reconstruction/research_program/intrinsic_zero_firstjet_20260915/note.md).

## 7. Complete common-future families for every even interior exponent

Fix integers b≥1, even e≥2, and σ∈{0,1}. Define

```
h=(2^e+2)/3,     t=ν₃(h)=ν₃(e−1),
a=min{a≥1:2^(a+e+2b−σ)<3^(a+b)},
J=2^(e+2b−σ),   Q=3^(a+b),   K=2^aJ<Q,
(d_σ,r_σ)=(4,3) if σ=0, and (32,27) if σ=1.
```

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

## 8. Finite membership and a whole additional source progression

For any fixed odd n>1, set k(n)=floor(log₂(n−1))−1. Every admitted coefficient-contracting template in Result 7 occurs among the finite tests

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

For every integer v≥0, one specific family is

```
20,241,207+1,549,681,956v --(1)--> 30,361,811+2,324,522,934v,
14,024,703+1,073,741,824v --(1^16,8,2,3)--> the same endpoint.
```

Every larger source in this progression was a root of the preceding reduction. The source difference is 6,216,504+475,940,132v. This is a shared-future source comparison; it does not assert forward iteration from the larger source to the smaller one. [Proofs, §§4–5](https://github.com/KokunoYumeto/collatz-workbench/blob/main/collatz_reconstruction/research_program/all_even_join_extension_20260916/note.md).

## 9. Integral retractions with explicit support and coefficient bounds

Put q=1+ε. For a path x₀→⋯→x_s put B=Σ[i=0,…,s−1]q^iE_x_i. Paths n→y and m→y of lengths s,t then satisfy

```
d_ε(B_left−q^(s−t)B_right)=V_n−q^(s−t)V_m,
q^j=1+jε for every integer j.
```

Preserve the preceding rule priority and apply new comparisons at its retained roots. For a selected chain B_n, smaller source m, and clock j=s−t, define recursively

```
H(V_n)=B_n+q^jH(V_m),    Q(V_n)=q^jQ(V_m),    F=I−Hd_ε.
```

Here H:C¹⊗D→C⁰⊗D, Q:C¹⊗D→C¹⊗D, and F:C⁰⊗D→C⁰⊗D. At a final root, H=0 and Q=I. Every recursion terminates and

```
d_εH=I−Q,   Q²=Q,   HQ=0,
d_εF=Qd_ε,  F²=F,   FH=0.
```

Accepting a new comparison only when both complete paths meet the predecessor's budget bounds every original vertex used in H(V_n) by

```
R₀(n)=max{130(n+1),floor(64n(4/3)^floor(log₃n))+21},
R₀(n)≤64n^(log₃4)+21  for n≥27.
```

The entire progression in Result 8 passes this budget. Alternatively, admitting every successful template gives, for odd n>1,

```
R_*(n)=max{130(n+1),floor((n−1)3^k(n)/2^k(n))−1}.
```

Both versions have at most

```
K_*(n)=((n−1)/2)max{24,k(n)+floor(log₃n)+6}
```

uncollected edge terms. The sums of absolute constant and ε coefficients are at most K_*(n) and K_*(n)² respectively. Set R_*(1)=1 and K_*(1)=0. These bounds concern the constructed chain columns. [Proofs, §6](https://github.com/KokunoYumeto/collatz-workbench/blob/main/collatz_reconstruction/research_program/all_even_join_extension_20260916/note.md), [predecessor bound](https://github.com/KokunoYumeto/collatz-workbench/blob/main/collatz_reconstruction/research_program/bilateral_root_bounds_20260916/note.md).

The remaining global assertion is B=0, equivalently the vanishing of every ξ_n; the stated reductions do not establish it.

Public collaboration: **Kokuno Yumeto / PolyClank**, with **ChatGPT 5.6 Sol in Ultra mode in Codex and GPT-6 Astra**. The notes retain their literature attributions, including the established cylinder/geometric mechanism used in Tao's work. [Proofs, source and checks](https://github.com/KokunoYumeto/collatz-workbench).
