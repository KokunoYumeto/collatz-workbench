# Intrinsic Split-Zero support and the Collatz first-jet kernel

Read `note.md`. This additive continuation begins at PR #2 commit `2a77e3bc9435f181bc4c9c3957224a7d93b4e887`. Its source rereading traces the archived scalar core, chapter-14 semimodule theorem, actual internal quotient/cohomology construction, and early Rees first variations. It does not use the user's informal "history" as the weighted-automata term.

## What is proved

On the original ABSOLUTE graph keep both the fixed vertex and loop. With source/target incidence J,P, the original differential is d=J-P. Over the dual integers D=Z[epsilon]/epsilon^2 use d_epsilon=d-epsilon*P. Constant reduction is a specified cochain map.

Its degree-one comparison kernel is computed in full:

```
B_E = ker H^1(K_epsilon -> K)
    = epsilon H^1(K_epsilon)
    = coker(beta: ker d -> coker d),  beta(c) = -[P*c].
```

On a primitive ACTUAL cycle of length m, beta is multiplication by -m. Its entire first-jet module is D/(m*epsilon), with reduction kernel Z/mZ. A full nonperiodic component has module D and kernel epsilon*Z. The actual fixed loop m=1 has zero kernel while its nonempty source module remains supported. Finite open components are individually retained as unresolved frontiers, not certified infinite orbits.

The proof therefore gives the exact restatement `Collatz <=> B_X=0` on the full original source. Every nontrivial positive cycle has length at least two, by the original fixed-point equation. No vanishing of B_X is asserted.

A finite integral witness for epsilon*V_n to vanish is `(b,c)` with

```
d*b = 0,
d*c - P*b = V_n.
```

The checker verifies the full equations and then extracts an actual finite path from n to 1 from the witness support. Rational division of a period-m witness by m is rejected. Repeated position words must first be mapped into their actual orbit; `(2,2)` is the twice-covered fixed point, not an actual period-two component.

## Commands

From the repository root:

```sh
python -B collatz_reconstruction/research_program/intrinsic_zero_firstjet_20260915/replay.py
python -B collatz_reconstruction/research_program/intrinsic_zero_firstjet_20260915/firstjet.py diagram 1 3 5 13
python -B collatz_reconstruction/research_program/intrinsic_zero_firstjet_20260915/firstjet.py witness 27 --cap 100
python -B collatz_reconstruction/research_program/intrinsic_zero_firstjet_20260915/firstjet.py diagram 5 7 --forcing -1
```

The last command is an explicitly changed-map control, not a positive 3n+1 counterexample.

## Execution and continuation

The new ordinary/optimized pair has 39,211 exact checks and byte-identical results. It includes 128 finite equation supports, 2,187 support inclusions, 1,024 support compositions, 32 abstract period controls, and 1,024 original singleton witnesses with 25,437 independently replayed return equations. Twelve malformed inputs are rejected. The general theorems are in the note; tests are not a global convergence proof or independent external audit. No new Lean execution or numerical cycle bound is claimed.

Continue on complete arithmetic families of the ORIGINAL witnesses `(b,c)` and their parameter domains, or on retained nonzero first-jet classes. The finite-support colimit is proved, but exhaustion of all original singleton classes remains the arithmetic task. Retain integral coefficients: rationalization would kill every finite cycle-index obstruction while preserving support labels.

This directory supersedes no previous proof record. The terminology clarification concerns only the informal phrase "history of a zero"; original automata histories remain explicitly named trajectory-word data. All inherited contribution files, the Zeta repository, PR #1 and main remain untouched by this addition. Publication and CI status belong to the separate remote receipt.
