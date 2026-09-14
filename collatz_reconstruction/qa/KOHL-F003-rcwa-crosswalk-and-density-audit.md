# KOHL-F003: fixed-modulus rcwa crosswalk and density-statistic audit

## Source identity and inspected manifestation

- Stefan Kohl, *Algorithms for a Class of Infinite Permutation Groups*.
- Published identity: *Journal of Symbolic Computation* **43** (2008), no. 8,
  545--581, DOI `10.1016/j.jsc.2007.12.001`.
- Frozen route: `DOCROUTE-COL-EF8D38EAFDE006BCFFE7`.
- Local author PDF:
  `C:/Users/LOCAL_USER/Documents/Erdos Strauss and related/maxwell_siegel_research/external_literature/prior_art_2026-08-24/kohl_2008_author.pdf`.
- PDF bytes: `318101`.
- PDF SHA-256:
  `602d3fd268ff4e202a72c656006218353971917254781eb711ad4d9bcd47c629`.
- Searchable extraction:
  `C:/Users/LOCAL_USER/Documents/Erdos Strauss and related/maxwell_siegel_research/external_literature/prior_art_2026-08-24/kohl_2008_author.txt`.
- Extraction bytes: `134360`.
- Extraction SHA-256:
  `9ddfc47e41d2c891f423803ade24e50791bbfcd5cffec140141a5640ef9bd993`.
- The PDF has 37 physical pages. Physical/printed pp. 1--4 were rendered and
  inspected at original detail for the statements used here: p. 1 for
  Definition 1.1 and Remark 1.2, p. 2 for the permutation examples and group
  terminology, p. 3 for Definition 2.1, and p. 4 for Algorithm 2.2,
  Definition 2.4, and the negative-slope example.

This is a targeted content audit of the definition, coefficient representation,
and density statistic. It is not yet a content-level certification of all later
group algorithms in the 37-page article.

## Exact source presentation

Kohl Definition 1.1 fixes a map `f : Z -> Z`. A positive integer `m` is a
presentation modulus when, for every residue `i` modulo `m`, there are integers
`a_i,b_i,c_i` such that

```text
f(i+mk) = (a_i(i+mk)+b_i)/c_i            (k in Z).
```

The least possible positive presentation modulus is `Mod(f)`. Definition 2.1
uses `m=Mod(f)` and stores a reduced coefficient list: each triple is primitive
and every `c_i` is positive. Algorithm 2.2 also accepts an unreduced list and a
nonminimal presentation modulus before reducing it.

For a reduced list, Remark 1.2 records that `c_i` divides both `a_i i+b_i` and
`m`. These conditions make the displayed branch integer-valued on the entire
class `i+mZ`.

## Exact fixed-modulus crosswalk to Matthews

Fix `d>=2`. Matthews data consist of nonzero integers `m_i` and integers `r_i`
with

```text
r_i = i m_i (mod d),
T(x) = (m_i x-r_i)/d on x = i (mod d).
```

The presentation-level map to Kohl data is

```text
(d;(m_i,r_i)_i) |-> (d;(a_i,b_i,c_i)_i)
with a_i=m_i, b_i=-r_i, c_i=d.
```

It preserves the underlying function `Z -> Z` pointwise. The Matthews
congruence is exactly Kohl's branch-integrality condition for this common
denominator. Its image consists of the possibly unreduced fixed-modulus rcwa
presentations with common denominator `d` and nonzero branch slopes. On that
presentation class the inverse is `m_i=a_i`, `r_i=-b_i`.

Conversely, take a reduced rcwa coefficient list at the fixed modulus `d`, with
every `a_i` nonzero. Since `c_i | d`, put

```text
m_i = a_i d/c_i,
r_i = -b_i d/c_i.
```

Then `r_i = i m_i (mod d)` because `c_i | a_i i+b_i`, and the Matthews branch
is exactly the original rcwa branch. Returning literally to common-denominator
rcwa data scales the original triple by `d/c_i`. Reducing that scaled triple
recovers the starting reduced triple exactly. Thus the two literal coefficient
lists differ, but branchwise reduction loses no data while the retained modulus
`d` is carried alongside the reduced list.

Therefore the map-level classes agree for fixed `d>=2` and nonconstant affine
branches. The retained common-denominator presentation and the reduced list are
distinct data objects linked by the exact reversible formulas above. What loses
the displayed refinement is forgetting `d`, for example by retaining only the
least modulus after modulus minimization. No normalization is performed in the
edition.

For an arbitrary retained presentation `d`, impose the presentation-level unit
condition

```text
gcd(m_i,d)=1 for every i.
```

If a smaller modulus `q` carried affine data for the same map, comparison of
slopes on infinite intersections of compatible `q`- and `d`-classes would give
`q m_i=d m'_j`. Since `gcd(m_i,d)=1`, this forces `d|q`; hence no `q<d`
exists. The unit condition therefore forces `d=Mod(T)`, and at this least
modulus it is exactly Matthews's intrinsic "relatively prime type."

Matthews congruence also gives
`gcd(m_i,r_i,d)=gcd(m_i,d)`. Consequently the common-denominator triples are
already primitive under the unit condition, every reduced denominator remains
`d`, and Kohl's divisor is exactly `Div(T)=d`. Thus for `d>=2` Matthews
relative-prime type excludes Kohl integrality (`Div(T)=1`). Neither condition
by itself is integer-map bijectivity. For the shortened Collatz map, the
triples are `(1,0,2)` and `(3,1,2)`: it is Matthews-relatively-prime, has Kohl
divisor 2, and is surjective but not injective.

## Source defect in Remark 1.2

The printed statistic is

```text
(1/m) sum_i c_i/a_i.
```

It is undefined when a branch slope `a_i` is zero and is false for negative
slopes. The paper itself supplies a decisive internal counterexample on printed
p. 4: `f(n)=-n` is an rcwa permutation, represented at modulus 1 by the reduced
triple `(-1,0,1)`. The printed statistic equals `-1`, whereas Remark 1.2 says it
must equal `1` for a bijection.

## Proved repair

For a reduced coefficient list at modulus `m`, define

```text
D(f) = (1/m) sum_{i: a_i != 0} c_i/|a_i|.
```

Then:

1. if `f` is injective, `D(f)<=1`;
2. if `f` is surjective, `D(f)>=1`;
3. if `f` is bijective, `D(f)=1`.

Proof: on `i+mZ` with `a_i!=0`, the branch image is one residue class of
modulus `|a_i|m/c_i`, hence has natural density `c_i/(|a_i|m)`. If `a_i=0`,
the branch image is one point and has density zero. Injectivity makes the branch
images disjoint, so their density sum is at most one. Surjectivity makes their
finite union all of `Z`, so the sum of their densities, counted with possible
overlap, is at least one. Bijectivity gives both inequalities.

The absolute value and the zero-slope convention are both necessary. The repair
does not change Kohl's positive-slope Collatz calculation
`(1/2)(2/1+2/3)=4/3`.

## Consequence boundary

- The corrected density statistic concerns the integer map `f : Z -> Z`.
- The Matthews cylinder theorem concerns finite itinerary words modulo powers
  of `d`, and the conjugacy concerns the extension `Z_d -> Z_d`.
- A homeomorphic coordinate change between the two `Z_d` phase spaces does not
  make the endomap bijective: the one-sided digit shift and a relatively-prime
  generalized map are both `d`-to-one.
- No integer-orbit endpoint statement follows from the rcwa presentation or the
  `d`-adic conjugacy.
- Nothing in the inspected Kohl passages supplies the generalized `d`-adic
  conjugacy proved separately in the working edition.
