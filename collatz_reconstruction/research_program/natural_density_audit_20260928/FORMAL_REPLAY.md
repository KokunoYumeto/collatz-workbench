# The five scoped Lean certificates

These are general discrete proofs in Lean 4.15.0, not finite testing and not
a formalization of the complete natural-density argument.

| Module | Scope | Declared import |
|---|---|---|
| ClockAndRanks | Exact Collatz clocks, rank and elementary integer identities; 36 recorded declarations | Init |
| JointWitness | Same-path witness and clock/height transfer; 9 declarations | ClockAndRanks |
| Reflection | Exact finite reflection/barrier counts; 31 declarations | Lean's implicit Init |
| DyadicPrefix | Prefix and incomplete-shell counts and witness transfer; 23 declarations | JointWitness |
| CompletedHeight | Two-sided path height, integer crossing and two-candidate maximum; 29 declarations | JointWitness |

The source files and the compiler's literal axiom output are retained in the
corresponding formal_shaik_* directories. [FORMAL_RECORDS.json](FORMAL_RECORDS.json)
pins their bytes. The recorded declarations use only the reported standard
axioms; no admitted theorem is being substituted for the analytic estimates.

For a portable rebuild, place the five .lean files in one fresh build directory,
use Lean 4.15.0, and compile ClockAndRanks before JointWitness, then
DyadicPrefix and CompletedHeight. Reflection is independent. Include that build
directory in LEAN_PATH alongside the toolchain's standard library. A command
for one module is:

```text
lean -j1 -M1024 -T300000 -o ClockAndRanks.olean ClockAndRanks.lean
```

Use the corresponding module name for the remaining four commands and run
them serially under a process-tree memory watcher. The historical successful
builds used a 2 GiB aggregate watcher. No Lean build was launched in the
30 September publication step; it rechecked source, object, dependency,
compiler and axiom-output integrity in the original local environment.
The platform-specific local launch scripts and machine paths are not
redistributed here. The above portable arrangement is a rebuild recipe,
not a claim that a new build was run from this public edition.

Compare each declaration directly with its manuscript counterpart. In
particular, CompletedHeight certifies discrete height bounds, not the
real-exponent estimates or the full natural-density conclusion.

