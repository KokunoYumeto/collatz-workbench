# Global cylinder and first-crossing control

**Read `note.md` first.** This continuation applies to every finite original
Collatz exponent word, including arbitrary nonrepeating switches. It is
based on the published head `9afcbe2dc9bace77c1ae705b1cd128da22fe8f8b`.
No files in the preceding contribution need modification.

## Proved scope

Theorem 1 proves `2^A-3^m > (3/2)^m-1` for all `2^A>3^m`, using the
explicit established Matveev bound, a rational interval and 127 exact
integer rows. Theorem 2 returns it to the original affine numerator:
`C/(2^A-3^m) < 2^(A-a_last+1)`. Hence a contracting word has at most
its one canonical source as a non-descending point in its entire original
positive cylinder. That point is tested, not declared absent.

Theorem 3 collects the ENTIRE unbounded next-exponent crossing alphabet
of each pre-crossing prefix into one original progression with an exact
valuation map. At most its old canonical prefix source can fail to
descend. The remaining low exponents are a complete finite set.

The complete symbolic audit through 18 odd returns visits 1,166,058
pre-crossing prefixes. At every node it independently checks the cylinder,
the original affine equation, the whole-tail linear margin, and the
first source of the crossing progression by repeated division. Thus the
bounded-return theorem itself is elementary, even without Theorem 1's
external logarithm input. The only non-descending crossing in that complete
domain is the original fixed point 1. Source size and last exponent have
no upper bound in that assertion. The infinite-depth frontier remains.

The original integral first-jet receiver and its support labels are retained.
A descent transports a source class to a LOWER endpoint class; it is not
a declaration of arrival at 1. Complete point witnesses are separate.

## Exact replay

From the repository root:

```sh
python -B collatz_reconstruction/research_program/global_cylinder_control_20260916/replay.py --predecessor
```

The default repeats the new check in ordinary and optimized modes. `--mode
ordinary` or `--mode optimized` selects one mode. Exact checks remain active
under optimization. The generator reconstructs every finite proof row and
matches `verification.json` byte for byte. No new Lean or independent
external mathematical verification is asserted.

Materialize the whole optional audit stream (it can be large):

```sh
python -B collatz_reconstruction/research_program/global_cylinder_control_20260916/verify.py --output full-result.json --ledger all-crossing-nodes.jsonl.gz
```

The stream's UNCOMPRESSED SHA-256 is recorded in the result. Gzip wrapper
metadata is not part of that mathematical stream identity.

Inspect the entire crossing family after an arbitrary prefix:

```sh
python -B collatz_reconstruction/research_program/global_cylinder_control_20260916/global_control.py crossing 1 2 1 1 1 2 1 1 4 --parameter 0
```

The result contains the original source and image progressions, inverse
parameter data, finite low alphabet, full high alphabet and actual endpoint.
The optional `--output` argument precedes the subcommand, for example:

```sh
python -B collatz_reconstruction/research_program/global_cylinder_control_20260916/global_control.py --output cylinder.json cylinder 1 3
```

## Continuing target

Read `TASK_STATE.md`. The result removes all but one original source from
each contracting cylinder, not all canonical candidates or ordinary-integer
realizations of the no-crossing infinite branches. The all-word theorem is
not a claimed proof of the conjecture or a published cycle/stopping-time
record. The local delivery receipt, not this README, records whether a
remote commit and CI run actually occurred.
