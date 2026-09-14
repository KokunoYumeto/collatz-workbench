# Affine CRT certificate: fresh read and watched reproduction

2026-09-04, completed after the rerun at 15:13:35 UTC. **PASS for the
single packet (m,A)=(10,16). No concrete mathematical defect found.**

The current directives, affine topic route, full companion chapter 04,
entire CRT certificate, and final receipt were read. Both complete 6,487-cell
tables were machine-checked entrywise and compared, rather than accepting
their recorded summary counts. The certificate was executed exactly once
in this review. No longer-period search was run.

This reviewing agent originally wrote the certificate. To supply an
additional independent code reading, a separate fresh-context agent,
`/root/portable_preprint_check/crt_code_readonly_review`, read the directives
and entire certificate without executing it. It found no concrete defect
and independently confirmed the positive/primitive distinction, recurrence,
rotation classes, and square multiplier. Its conclusions were checked
against the source and watched run below; it did not attest numerical
execution or a new literature result.

## Mathematical findings

The separator generator selects nine cuts among positions 1,…,15;
successive gaps give every positive composition of 16 into ten parts
exactly once. The recursive generator independently chooses each first
part and enumerates its remaining positive tail. Their ordered outputs
agree, contain 5,005 distinct words, and have the expected size C(15,9).
The displayed numerator sum, growing affine recurrence, and first-letter
recurrence agree on every word (certificate lines 35–67, 157–178).

The joint DP carries an actual pair of tail residues and applies the
**same** first part to both coordinates. It does not multiply the two
marginals or combine residues from different words. Direct enumeration,
joint DP, independent scalar DPs modulo 13, 499 and 6487, and the CRT
pushforward agree. CRT inverse coordinates are
(u,v)↦3992u+2496v mod6487. All 408,681 declared transition/inverse tests
pass, as do both CRT inverse identities on all 6,487 elements.

| gcd(C,6487) | All positive words | Primitive words | Primitive cyclic classes |
|---:|---:|---:|---:|
| 1 | 4560 | 4560 | 456 |
| 13 | 410 | 410 | 41 |
| 499 | 35 | 0 | 0 |
| 6487 | 0 | 0 | 0 |
| Total | 5005 | 4970 | 497 |

Primitive means least rotation period ten, not merely positivity of the
entries. There are another 35 words of least period five, forming seven
classes, for 504 cyclic classes in total. If p=uʳ is a proper power, r
divides both 10 and 16, so r=2 and u has length five and sum eight.
Splitting the numerator sum into its two five-term blocks proves

    C(u²)=3⁵C(u)+2⁸C(u)=499C(u).

Each of these 35 identities is checked. The finite enumeration verifies
that these are all the 499-divisible words. Thus the factor 499 alone
excludes integral periodic points from every **primitive** word in this
packet. It does not exclude all positive words by itself. The imprimitive
words instead have reduced denominator 13, since their gcd stratum is 499.

Both all-word marginal supports are full: 13 residues and 499 residues.
Their zero masses are 410 and 35. Joint support has 3,473 pairs; its
3,014 missing pairs include (0,0). Hence no word in this packet has an
integral associated point. Full marginal supports must not be stated for
the primitive subset, whose residue zero modulo 499 is absent.

The least 13-divisible witness is (1,1,1,1,1,1,2,2,2,4), numerator
65065 and other residue 195. The least 499-divisible witness is
(1,1,1,1,4)², numerator 105289 and other residue 2. Both lexicographic
and least-numerator selections agree with the prior receipt. There is
no primitive 499-divisible witness in this finite packet.

## Watched run and receipt integrity

The new audit helper `run_affine_crt_watched_review_20260904.py` launched
one certificate process, without changing its source. Every 25 ms it
sampled the watcher and its full descendant tree, enforcing a ceiling of
5,000,000,000 bytes on the sum of max(RSS, private bytes) per process.
The kill condition was aggregate ≥ ceiling; a separate 30-second timeout
was armed. Sixteen samples were recorded. Observed peak enforced aggregate
was **63,406,080 bytes**; the certificate separately reported a process
peak working set of 28,225,536 bytes. Exit code was 0, stderr was empty,
and neither termination condition fired. These are sampled watcher
measurements, not a claim of continuous kernel-level memory accounting.

Run directory:
`affine_crt_watched_review_20260904T151335Z_0212cc90/`.

- New `certificate_receipt.json`:
  `b521986a58f0c613ef882e0c22e23c3d06624b0f8ab71df38af3d96421f8670d`.
- New `watcher_receipt.json`:
  `9c3c4ff0e525607d97089817f2e4e4f8285a376a26d06b536177d7bfeb5b8830`.
- Watcher source:
  `a491a00d079d26d4c6ac0197649e1131479cedf9cae9bcf8c9ce396b795717a7`.
- Preserved prior final receipt:
  `d6e5476ba30318a0048aa0e7f99c6dbf06064056041b1a35f015219283daadce`.

Every mathematical field equals the prior final receipt, including all
6,487 joint cells, full marginals, strata, witnesses, and check counts.
The only comparison exclusions were execution metadata, recording time,
and command arguments. Each table's compact JSON SHA256 was recomputed:
`c96f9a23ccf99710306d4188d737826fc3d03818e0fd80680fa3d9bd3ce626d3`.
Row/column sums and gcd strata were independently reconstructed directly
from each stored table.

## Exact reviewed input pins

- Certificate:
  `ee0340744c8886ff55a7246ae0141576eac3ec60d262b7431bc3579c0198d71e`.
- Companion chapter 04:
  `27b74b3813f4ba5d73776dff3c0a33f545b9c380cab743d3877c3140913ca95a`.
- Affine topic route:
  `47de59d556ea1a38dd82e35ba02379a7c650ad549fd55cd1a25e4429b8d60b53`.
- Directives:
  `899fd9edf7316cf1140fc74adf77be9ed0ac49c2440a3e429b556c099dfbc711`.

All these files and the old final receipt remained hash-identical during
the watched run. No manuscript, ledger, source corpus, AGENTS file, Lean
worker, or remote project was modified. The general theory and historical
literature comparison remain the parent's separate work; the result here
is the exact finite calculation and its narrowly stated consequences.
