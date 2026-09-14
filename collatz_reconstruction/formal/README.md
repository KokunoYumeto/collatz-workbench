# Formal certificates

This directory is an independent pinned Lean project. The current certificate
formalizes the finite one-digit lifting kernel used in the generalized
residue-itinerary argument. At exact scope it checks:

- the literal unnormalized lift identity;
- the explicit affine inverse for unit multipliers;
- the ordinary-integer-gcd crosswalk after reduction modulo `d`;
- exactly `d/gcd(d,m_i)` attainable next digits; and
- exactly `gcd(d,m_i)` lifts over every attainable next digit.

It does not by itself formalize the inverse limit, the infinite `d`-adic
inverse series, the full homeomorphism, or the shift conjugacy. Those parts of
`PO-COL-000003` remain open.

Reproduce from this directory with:

```text
lake update
lake exe cache get
lake build GeneralizedResidueItinerary
```

The exact dependency revision is recorded in `lake-manifest.json` after
`lake update`.  Generated `.lake` contents are build cache, not source evidence.

The principal checked theorem names are:

```text
branch_numerator_on_lift
nextDigit_bijective_of_isUnit
multiplierResidueGcd_eq_intGcd
card_nextDigit_range_literal
card_nextDigit_fiber_literal
```
