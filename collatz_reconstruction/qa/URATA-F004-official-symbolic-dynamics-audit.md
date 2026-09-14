# URATA-F004: official 2-adic accelerated-symbolic audit

## Source identity and route-integrity finding

- Toshio Urata, *The Collatz Problem over 2-adic Integers*.
- Published in *The Bulletin of Aichi University of Education* **52**
  (Natural Science), 5--11, March 2003; received 5 September 2002.
- Frozen document route: `DOCROUTE-COL-FAA6A64E6107027934E4`.
- Official Aichi repository record: `https://aue.repo.nii.ac.jp/record/704`;
  handle `10424/641`; ISSN `0365-3722`.
- Official local witness:
  `external_literature/urata_2003_official_aichi.pdf`.
- Official PDF bytes: `78688`.
- Official PDF SHA-256:
  `82c23a89958562c9385e9b6ae5d3c2e82f26c8afd6ff259fdd36c61c64f25cd4`.
- All seven A4 pages, printed pp. 5--11, were rendered and read visually.

The two frozen indexed manifestations are byte-identical:

- `C:/Users/LOCAL_USER/Documents/Papors/OS/kenshi52511.pdf`;
- `C:/Users/LOCAL_USER/Documents/arxiv_latex/library/other/kenshi52511.pdf`;
- bytes `108636`;
- SHA-256
  `f2537bc6fb3f0b965d976aef5e2411f8bdd96d37d8a23b497d0d8157d7cfdc8a`.

They are not the published PDF. Their metadata identify Letter-sized XeTeX
output created 15 November 2025. They renumber the propositions, insert an
unattributed `Remark 3.1` and replacement formula, alter at least one integer
domain qualifier, and replace the journal pagination. They are retained only
as unauthenticated editorial derivatives and are not evidence for Urata's
wording, numbering, corrections, or claims. The official `82c...` witness is
the sole attribution witness used below.

## Exact maps and domains

Let

```text
U_2 = 1 + 2 Z_2 = Z_2^x,
```

the closure of Urata's odd-type rationals. On printed pp. 5--7 the paper
extends the integer Collatz function to

```text
phi : Z_2 \ {0,-1/3} -> U_2
```

by

```text
phi(x) = (3x+1)/2^v2(3x+1)  for x in U_2 \ {-1/3},
phi(x) = x/2^v2(x)           for x in Z_2 \ (U_2 union {0}).
```

Only the odd-unit restriction is used for accelerated symbolic dynamics. On
positive odd integers this restriction is exactly the already registered
Crandall first-return map. Urata also records `f(x)=2x+1/3` and
`phi(f(x))=phi(x)`, but this invariance is not itself a conjugacy.

The printed sentence that the extended exponent `e` is continuous on `Q_2`
is not fully typed after setting `e(0)=infinity`: a topology on
`Z union {infinity}` must be supplied before continuity at zero is a statement.
The later arguments need only local constancy of `v2` on `Q_2^x`; compactness
of `Z_2` is the standard independent fact and is not inferred from that
untyped sentence.

For `p>=1`, define the typed inverse branch

```text
F_p : U_2 -> U_2,
F_p(y) = (2^p y-1)/3.
```

Then `3F_p(y)+1=2^p y`, so `v2(3F_p(y)+1)=p` and
`phi(F_p(y))=y`. Conversely every odd-unit preimage has this form with its
unique positive exponent. Hence

```text
phi^{-1}(y) = {F_p(y) : p>=1}
```

and the fibre is countably infinite with exact branch label `p`.

## Official finite recurrence and Propositions 1--3

For an actual orbit `x_k=phi^k(x_0)`, put

```text
p_k = v2(3x_{k-1}+1),
S_0 = 0,
S_n = p_1+...+p_n,
C_n = sum_{j=1}^n 3^(n-j) 2^(S_{j-1}).
```

This `C_n` is an editorial reindexing of the source's displayed `C` and does
not replace it. Direct composition gives

```text
2^(S_n) x_n = C_n + 3^n x_0.
```

Official Proposition 1 states this recurrence and the corresponding full
`n`-step inverse set. Proposition 2 shows that two surviving inputs with the
same first `n` exponents satisfy `|x-y|_2 <= 2^(-S_n)`. Subtraction of the
recurrences and the fact that both `n`th iterates are odd units actually give
the sharper `2^(-(S_n+1))` bound. Proposition 3 lets `n` tend to infinity and
proves that a complete exponent sequence determines at most one starting
point.

## Defect in the printed Proposition 4 proof

Official Proposition 4 asserts that every sequence of positive integers is
the exponent sequence of a surviving odd 2-adic orbit. Its proof constructs
finite approximants `x_n` whose first `n` exponents are prescribed and whose
tail is the fixed orbit of `1`. When comparing `x_m` and `x_n` with `m<=n`,
the two approximants share only the first `m` prescribed exponents. The printed
display nevertheless uses the stronger exponent sum `S_n`; Proposition 2
supports only `S_m` there.

The printed bound is false. With `p_1=1` and `p_2=3`, the first two
approximants are

```text
x_1 = 1/3,
x_2 = 11/9,
|x_2-x_1|_2 = |8/9|_2 = 2^(-3),
```

whereas the printed `S_2=4` bound would require at most `2^(-4)`. This is a
local proof defect, not a counterexample to the proposition.

## Constructive repair and exact inverse

For an arbitrary sequence `p=(p_1,p_2,...)` of positive integers, define

```text
I(p) = - sum_{j>=1} 2^(S_{j-1}) / 3^j.
```

The terms tend to zero 2-adically because `S_{j-1}>=j-1`, so the series
converges. For every `k>=0`, define the suffix point

```text
x_k = - sum_{r>=1}
          2^(p_{k+1}+...+p_{k+r-1}) / 3^r,
```

where the empty exponent sum is zero. The leading term is `-1/3` and every
later term is even, so every `x_k` is a unit. Direct cancellation gives the
literal identity

```text
3x_k+1 = 2^(p_{k+1}) x_{k+1}.
```

Therefore `v2(3x_k+1)=p_{k+1}`, `phi(x_k)=x_{k+1}`, and no `x_k` is the
excluded point `-1/3`. This proves existence, exact branch membership, and
survival. Proposition 3 gives uniqueness. The repair does not use the false
approximant bound.

## Countable-alphabet conjugacy and exact cylinders

Define the survivor set

```text
X = U_2 \ union_{j>=0} phi^{-j}({-1/3}).
```

The exponent encoder

```text
E_U : X -> (Z_{>=1})^N_0,
E_U(x)_j = v2(3 phi^j(x)+1)
```

is bijective, with inverse `I` above, and

```text
E_U o phi = shift o E_U.
```

Finite exponent prefixes are locally constant on `X`, and the prefix estimate
makes `I` continuous. Thus this is a topological conjugacy to the one-sided
full shift on a countable alphabet. Urata proves the uniqueness and existence
components but does not use this conjugacy terminology or display `I`; the
assembled morphism and inverse formula are independently attributed.

For a word `w=(p_1,...,p_n)`, let

```text
F_w = F_{p_1} o ... o F_{p_n}.
```

Then

```text
F_w(y) = (2^(S_n)y-C_n)/3^n,
F_w(U_2) = F_w(1) + 2^(S_n+1) Z_2.
```

The ambient finite-prefix ball is `F_w(U_2)`; the actual cylinder in the
survivor system is `F_w(X)`, obtained by deleting the countable future-singular
set. Thus `n` exponent symbols determine `S_n+1` binary digits, not `n` binary
digits. This variable modulus is retained exactly.

For normalized Haar measure `mu_U` on `U_2`, the ambient ball has

```text
mu_U(F_w(U_2)) = 2^(-S_n) = product_j 2^(-p_j).
```

The deleted preimage tree is countable and Haar-null. Hence `E_U` carries Haar
measure to the Bernoulli product measure `Pr(p_j=k)=2^(-k)`. Bernoullicity and
strong mixing are independent consequences of the exact cylinder calculation,
not explicit Urata theorems and not ordinary-integer density statements.

## Bridge to the binary parity system

Let `B` be the already registered run-length map. For `x in X`, if
`p_1=E_U(x)_0`, then

```text
phi(x) = T^(p_1)(x),
phi^j(x) = T^(S_j)(x),
P(x) = B(E_U(x)).
```

Under the Bernstein--Lagarias chronological parity conjugacy, `X` corresponds
exactly to binary sequences beginning with `1` and containing infinitely many
ones. The omitted sequence `1000...` is the parity sequence of `-1/3`, and
sequences with only finitely many ones are its accelerated preimages. This
enlarges the domain, not the positive-integer conclusion: the existing
`E:Opos -> (Z_{>=1})^N_0` remains merely injective, while `E_U` is bijective on
the larger 2-adic survivor set.

## Periodic points and retained boundary

Official Propositions 5--6 give, for a genuine orbit with first `n` exponents,

```text
phi^n(x)=x  iff  (2^(S_n)-3^n)x=C_n,
x = C_n/(2^(S_n)-3^n),
```

and equivalently the complete exponent sequence is `n`-periodic. Here
`n`-periodic means period dividing `n`; the least accelerated period equals the
least shift period only after passing to least periods. Printed p. 11 asks when
the displayed rational point is an integer and does not answer that question.

## Explicit nonclaims

- The generalized rational eventual-periodicity paragraph on printed p. 6 is
  conjectural, not a theorem.
- Arbitrary exponent-sequence realization occurs over `X`, not over positive
  integers.
- Rationality of periodic 2-adic points does not imply integrality or a new
  positive-integer cycle.
- A return after `n` steps does not assert least period `n`.
- The accelerated system is a variable-time first-return system, not the
  one-step binary shift.
- Exponent-prefix cylinders have modulus `2^(S_n+1)`, not `2^n`.
- The explicit inverse series, full-shift terminology, run-length crosswalk,
  and Haar Bernoulli consequence are independent reconstructions, not quoted
  Urata statements.
- No mathematical wording or correction found only in the `f253...`
  derivative is attributed to Urata.
- Haar-almost-every conclusions do not transfer to the countable Haar-null
  subset of ordinary integers.
