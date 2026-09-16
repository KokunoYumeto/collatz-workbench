# Continuation handoff

## Exact delivered state

Local entry point: `collatz_reconstruction/research_program/stopped_affine_transport_20260914/README.md`.

The arithmetic continuation is implemented, proved, and replayed locally. It is not pushed. Current GitHub contents, PR #1, the claimed predecessor commit, and any unpushed local Codex session were not independently recovered. No remote SHA is assigned to this delivery.

## The retained state to use

A node contains the current family `(a,d,b,N)`, the original-source coefficients `(a0,d0)` on the same parameter, and the full concatenated packet `(word,A,L,C)`. The two coefficient identities in note (9.1) are mandatory node invariants.

For a branch use the exact compatibility mask and chart `(g,P,s,u,target_d)` in note (3.2)–(3.9). Preserve the image complex `[Z --target_d--> Z]` and the affine odd-index coset `(u-1)/2 mod target_d`. Mark restriction `v=r+M*l` changes the actual target step to `M*target_d`; it is not erased.

Do not restart a cutoff-overflow point without a certificate. Keep that point's original-source identity in the unresolved set. Absorb the actual value 1 before invoking the strict-descent observer. The finite observer's overflow and the infinite observer's never-certified atom have different explicit definitions; neither is deleted.

## Implemented bridge to cohomology and Hurwitz data

The arithmetic image complex measures the target lattice. Its integral and local coefficient maps are in Section 4. The finite incidence complex records the actual source-to-label map; its homotopy and present-zero basis are in Section 10. The chain-level relation is now the span in (10.0c): support incidence <- affine incidence -> image complex. Its connecting moment map has image equal to the original lattice step; the retained-anchor homotopy and marked-lattice quotient maps are proved in (10.0f)–(10.0j). The exact source fibers are (5.6).

Actual counts, including zeros and overflow, enter the finite moment/Hurwitz construction through (10.6). The label dictionary and all idempotents are retained. Every weight is recovered by the displayed triangular and Lagrange inverses.

## Integration actions

Read the actual current repository methodology and the existing Collatz-history note before merging; these could not be fetched in this session. Compare conventions with the complete definitions in note Section 1. The intended path is new and add-only, but an existing file at that path must be reviewed rather than overwritten.

From the desired repository root, the delivered patch can be checked with `git apply --check stopped_affine_transport_20260914.patch` and applied with `git apply stopped_affine_transport_20260914.patch`. The check is required because no current repository tree was available as a base. No existing file or global entry point is modified by the patch.

Replay `verify.py` normally and with `-O`, compare the result bytes, and verify `MANIFEST.sha256`. The current finite result is 175,269 checks, including 180 marked-law fixtures. Review the written proofs separately from their finite fixtures.

## Mathematical continuation object

The deterministic object now available is the exact restart tree carrying its original-source parameter maps, image complexes, and zero-preserving observation fibers. A concrete continuation operates on its unresolved integer fibers while retaining those invariants. The completed reference law and its tail bound do not replace that integer-fiber calculation.

The delivered three-round replay is finite and records its overflow. It is neither a proof of universal source coverage nor a conditional theorem assuming such coverage. All stated mathematical results in the note are proved for their explicitly defined domains.
