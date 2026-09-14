# Common-input entrance laws at every threshold

Review ID: `AUD-TAO-V7-ENTRANCE-FAMILY-20260904-0001`.
Date: 2026-09-04. Bounded mathematical review of the proposed replacement
for `cor:limit`. No TeX, source, ledger, Overleaf or Lean changes.

## Verdict

The proposed all-threshold construction and both quantitative bounds are
correct. The essential specification is that **one base b is fixed for the
whole family**. Write the limit as `lambda_x^{infinity,(b)}` until independence
of the base is proved. This gives an exact compatible family for every real
threshold x >= 1, extending the old lattice-threshold construction.

It is a direct additional consequence of Tao V7's Proposition 1.11, not an
additional analytic estimate: the proof uses summable first-passage errors,
exact nested passage, and contraction. V7 Section 1.3 describes approximately
transported measures, and Section 3 telescopes their event probabilities to
prove quantitative tightness. Neither inspected section states or constructs
the exact all-threshold limiting family below. No claim of literature-wide
novelty is made from this bounded source comparison.

## Exact source identities and coverage

Primary source:

`C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/latex/1909.03562v7/collatz.tex`

SHA-256:
`bfbc39432d4084a276416cb019a592003c868fa32f18e2f90028ac325ae5c19d`.

Direct content reading:

- Section 1.3, physical source lines 310-339, complete. Lines 316-320 define
  first-passage location, merging failure with 1. Lines 326-335 give the
  logarithmic-block laws, failure bound, and adjacent-scale total-variation
  estimate. Lines 337-339 explain the approximate transport mechanism and
  summability of the weaker log-log error regime.
- Section 3, lines 535-593, complete. Theorem 3.1 is lines 539-546;
  event transport and the telescoping argument are lines 550-587.
- The unhalved total-variation convention is explicit at lines 259-265:
  the distance is the sum of absolute point-mass differences.

Draft snapshots read completely:

| Relative to `collatz_reconstruction/preprints/tao_clock_audit/` | SHA-256 |
| --- | --- |
| `main.tex` | `328f160e473d4e3b196d149ef03f950194710f3fa29b1ff8b22c322d21202298` |
| `sections/transport.tex` | `b3233b2b79614e1279a9d880eb7e82c21d5822873085bdaadf49332c2cd88678` |
| `sections/consequences.tex` | `9e2c769217f24e4f7da7137c792955faca28ab2488e682e57dbb51c220e85c49` |

Relevant draft locators: `transport.tex` exact kernel identities at lines
51-54 and definitions of nu_s, d(s), e(s) immediately after line 80;
`consequences.tex` unmerged estimates at lines 48-51 and existing
`cor:limit` at lines 54-101. Hashes identify the reviewed snapshots, not
any later parent edits. No other source version was read for this task.

## Statement with all quantifiers

Let O be the positive odd integers and E = O union {dagger}. Let p_x and
K_x be the draft's first-passage map and pushforward, retaining dagger as
the absorbing failure state. Thus, for 1 <= x <= y,

    K_x K_y = K_x = K_y K_x,
    ||K_x eta||_1 <= ||eta||_1

for signed summable measures eta on E. Fix alpha = 1001/1000. Let mu_s be
the exact harmonic probability on O intersect [s,s^alpha], with its
original finite denominator, and choose s_* >= 2 large enough that these
blocks are nonempty and the estimates below hold for every s >= s_*.

Define

    nu_s = K_s mu_(s^alpha),
    d(s) = nu_s({dagger}),
    e(s) = ||nu_s - K_s nu_(s^alpha)||_1.

Tao's proposition and the draft's unmerging inequality give constants
B, B', c > 0, independent of s, such that

    d(s) <= B s^(-c),
    e(s) <= B' (log s)^(-c)             (s >= s_*).

Fix **one** real b >= s_* and set t_j = b^(alpha^j) for integers j >= 0.
For every real x >= 1 and every integer j >= 0 define

    lambda_(x,j)^(b) = K_x mu_(t_(j+1)).

Then there is a probability measure lambda_x^{infinity,(b)} on the finite
set E_x = (O intersect [1,x]) union {dagger}. For every j >= 0 satisfying
t_j >= max(x,s_*),

    ||lambda_(x,j)^(b) - lambda_x^{infinity,(b)}||_1
       <= B'/(1-alpha^(-c)) * (log t_j)^(-c).                 (1)

For every pair of real thresholds 1 <= x <= y,

    K_x lambda_y^{infinity,(b)} = lambda_x^{infinity,(b)}.    (2)

In particular, the estimate (1) is uniform over 1 <= x <= t_j for the
given j. No large-threshold condition on x itself is necessary for
existence or compatibility.

For every x >= b define

    k = floor(log_alpha(log x / log b)),    r = t_k.

Then k >= 0 and x^(1/alpha) < r <= x. The failure mass satisfies

    lambda_x^{infinity,(b)}({dagger})
       <= B r^(-c) + B'/(1-alpha^(-c)) * (log r)^(-c)         (3)
       <= B x^(-c/alpha)
          + B' alpha^c/(1-alpha^(-c)) * (log x)^(-c).

Thus it tends to zero as x tends to infinity at fixed b.

## Proof checks

### Cauchy estimate

Since t_(j+1) = t_j^alpha and t_(j+2) = t_j^(alpha^2), the nested
identities give the exact expression

    e(t_j) = ||K_(t_j) mu_(t_(j+1))
                 - K_(t_j) mu_(t_(j+2))||_1.

When x <= t_j,

    lambda_(x,j+1)^(b) - lambda_(x,j)^(b)
      = K_x [K_(t_j) mu_(t_(j+2))
                         - K_(t_j) mu_(t_(j+1))].

Its norm is at most e(t_j). For l > j with t_j >= max(x,s_*), summing
from i=j to l-1 yields

    ||lambda_(x,l)^(b) - lambda_(x,j)^(b)||_1
       <= B' (log t_j)^(-c)
                       * sum_(h=0)^(l-j-1) alpha^(-ch).

The finite-state probability simplex is closed in l1 and complete.
Therefore this tail is Cauchy, has a probability limit, and the infinite
geometric sum gives (1). The finitely many j preceding the threshold
crossing do not affect convergence. The measures for those j remain
well-defined because their input scales exceed b >= s_*.

### Compatibility

For x <= y, the equality

    K_x lambda_(y,j)^(b)
      = K_x K_y mu_(t_(j+1))
      = K_x mu_(t_(j+1))
      = lambda_(x,j)^(b)

holds for **every** j; it does not require t_j >= y. Passing to the limits
is justified by the l1 contraction of K_x. This proves (2).

All real thresholds are legitimate: p_x depends only on which positive
odd integers lie below x, so there is no measurability or uncountable-choice
difficulty hidden in the phrase "for every real x". Each limit is unique
as the limit of its explicitly specified sequence.

### Failure estimate

The definition of k gives

    alpha^k <= log x/log b < alpha^(k+1),
    r <= x < r^alpha,

and hence the claimed bracket for r. At j=k, the threshold r is itself a
scale point, so

    lambda_(r,k)^(b) = K_r mu_(r^alpha) = nu_r.

Using (1) at threshold r and index k gives

    lambda_r^{infinity,(b)}({dagger})
       <= d(r) + B'/(1-alpha^(-c)) * (log r)^(-c).

Because r <= x, (2) implies K_r lambda_x^{infinity,(b)} =
lambda_r^{infinity,(b)}. The preimage of dagger under p_r includes dagger,
and the measure is nonnegative; therefore

    lambda_x^{infinity,(b)}({dagger})
       <= lambda_r^{infinity,(b)}({dagger}).

This proves (3). Notice that it uses the rate at **r**, not at x and index
k: when r < x, the latter index would not satisfy the condition for (1).
The x-only bound follows from r > x^(1/alpha).

## Relation to the old corollary and publication framing

The old `cor:limit` is correct, but uses base u for threshold u separately.
Call those older limits gamma_u. The common-input construction above
satisfies lambda_(t_k)^{infinity,(b)} = gamma_(t_k): for the old sequence
at base t_k, its j-th input is the new sequence's (j+k)-th input. Thus
deleting k initial inputs identifies their limits exactly.

For a general x off this lattice, the proof does not identify
lambda_x^{infinity,(b)} with gamma_x, which is generated by base x. It also
does not identify limits from two arbitrary bases b and b'. Consequently
the new theorem should not assert compatibility of all the independently
based gamma_x merely by dropping the lattice condition in the old text.
It should replace the construction itself by one common sequence, as
specified above. Bases b' = b^(alpha^k) do give the same family by a shift
of the input index.

Reader-facing mathematical contribution: Tao's approximate scale transport
is converted into exact compatible entrance laws at every threshold, with
an explicit l1 convergence rate and a quantitative failure tail. Attribute
the analytic estimates to Tao; present the limiting construction and its
proof as the additional result here. V7 Section 3's fixed-threshold
tightness bound and its already stated qualitative consequences remain
Tao's results. The all-threshold family does not require a new Fourier or
renewal argument, and no such analytic improvement was verified in this
review.

No finite calculation is needed to justify this general result. No code
execution was used as a substitute for any implication above.
