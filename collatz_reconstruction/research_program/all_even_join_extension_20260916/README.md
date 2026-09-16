# All even interior exponents, with the original support budget retained

Read `note.md`. This addition expands both original common-future templates from
interior exponents 2 and 6 to **every positive even exponent**. It preserves the
original two paths, source congruences, height difference, and signed first-jet
coefficient. It does not identify a lower-source relation with a zero singleton.

The exact source layer is `b + nu_3(e-1)`, with
`h_e=(2^e+2)/3`. The inner valuation identity and the complete forward paths are
proved, not inferred from tests. On a fixed original source n, only
`2 <= e <= floor(log_2(n-1))-1` can occur, and `b=nu_3(n)-nu_3(e-1)` is fixed
for each e. The unbounded parameter family therefore has a complete finite
membership test at every input.

The default `Retraction` retains the entire old rule ordering and tries the new
families only at old roots. Its support acceptance test retains the predecessor's
subquadratic bound. `Retraction(budgeted=False)` accepts every template but uses
the separately proved, larger support bound. These two scopes must not be mixed.

A full genuinely new source progression is

```
20241207 + 1549681956*t  -> 30361811 + 2324522934*t
14024703 + 1073741824*t  -> 30361811 + 2324522934*t
```

The left word is `(1)`; the right is `(1)^16,8,2,3`. Every nonnegative integer
parameter passes the old support budget, and the whole left progression was
retained by the preceding root rule. The proof checks that latter statement on
the complete periodic parameter domain, not just the anchor.

From the repository root:

```sh
python -B collatz_reconstruction/research_program/all_even_join_extension_20260916/replay.py
python -B collatz_reconstruction/research_program/all_even_join_extension_20260916/all_even.py family 2 8
python -B collatz_reconstruction/research_program/all_even_join_extension_20260916/all_even.py source 20241207
```

The new suite has 87,989 checked identities per ordinary/optimized execution. The
separate affine auditor checks all 512 declared test families and 24,180 original
coefficient equations without importing either implementation. The finite fixture
domain is b=1..16 and even e=2..32; the all-parameter assertions rely on the written
proofs. Fourteen invalid controls are rejected. No new crossing-horizon claim or
independent external mathematical review is made.

The cumulative LaTeX anthology is in the top-level delivery archive's `latex`
directory. Source-time claims in inherited notes remain historical. Main was read
at `9453b5306b3a897389dece309f9c119dffbcc489`; PR 2 is now merged. This new addition
was not pushed by the current session. Its add-only patch never edits an inherited
file, force-pushes, or merges.
