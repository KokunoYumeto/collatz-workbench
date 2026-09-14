# Exact joint-residue check for the packet (10,16)

Date: 2026-09-04. Scope: only the 5,005 positive compositions of 16 into
10 parts, together with the smaller tails needed by their residue recursion.
No longer-period cycle search, Lean build, or literature novelty claim is
part of this check.

## Inputs actually read

- `../../DIRECTIVES.md`, read at task start and reread after its concurrent
  addition of `USR-0017-tao-v7-baseline.txt`; final observed SHA256
  `d56da8bf7f87e8138fdad83d1033ed421e9a2ca596156beb10ae88a91fa00071`.
  That added Tao-baseline directive does not change this finite packet scope.
- `../../state/affine_packet_topic_route.json`, topic
  `TOPIC-COL-AFFINE-PACKETS-0005`, SHA256
  `47de59d556ea1a38dd82e35ba02379a7c650ad549fd55cd1a25e4429b8d60b53`.
- `../chapters/04_affine_packets_parity_necklaces_and_residue_automata.tex`,
  SHA256 `27b74b3813f4ba5d73776dff3c0a33f545b9c380cab743d3877c3140913ca95a`:
  full chapter read, specifically the numerator definition at equation
  `eq:packet-C-D-x`, the first-letter recurrence at
  `eq:first-letter-C-recursion`, and the residue and matrix conventions
  at `eq:packet-residue-recursion` and lines 392–393.
- Raw source `CHATINT-COL-000002`,
  `C:/Users/LOCAL_USER/Documents/Papors/Chatnotes/more col thread/ChatGPT-Implications of Affine Formula.md`,
  lines 2679–2828: the actual first-letter derivation and count-vector
  recursion were read, not inferred from routing metadata. Source SHA256
  `abb1abbb948dc140394de3d35f0efbde9b3facdf718c24b065b8d0adb951366e`.

The route's historical references remain source routes here, not new claims
that this subtask reread their PDFs. Historical comparison is being handled
separately by the parent task.

## Exact objects and independent computations

For a positive composition p=(a₁,…,a₁₀) of 16, put S₀=0 and
Sⱼ=a₁+⋯+aⱼ. The numerator is

    C(p)=Σⱼ₌₀⁹ 3⁹⁻ʲ 2^Sⱼ,
    D=2¹⁶−3¹⁰=6487=13·499.

Two separately implemented generators—separator combinations and recursive
positive compositions—produce identical lists of 5,005 distinct words.
For every word, three numerator computations agree: the displayed sum,
the growing recurrence B←3B+2^S followed by S←S+a, and the recursive
first-letter formula C(a,p′)=3⁹+2ᵃC(p′), with the appropriate length
in each recursive call. No existing certificate implementation is imported.

Primitive means least cyclic rotation period 10. Cyclic classes are formed
by the lexicographically least rotation, preserving repeated words and
their shorter orbit sizes. The identity

    3C(p)+D=2^a₁ C(σp)

is checked on all 5,005 words, as is invariance of gcd(C(p),D).

| gcd(C,D) | All words | Primitive words | Primitive cyclic classes |
|---:|---:|---:|---:|
| 1 | 4560 | 4560 | 456 |
| 13 | 410 | 410 | 41 |
| 499 | 35 | 0 | 0 |
| 6487 | 0 | 0 | 0 |
| Total | 5005 | 4970 | 497 |

There are 504 cyclic classes in all: 497 primitive classes and seven classes
of least period five. The 35 imprimitive words are exactly the squares
p=u², where u is a positive composition of 8 into five parts.
Indeed, a proper repetition number divides both 10 and 16 and hence is 2.
Direct expansion gives

    C(u²)=(3⁵+2⁸)C(u)=499C(u),
    D=(2⁸−3⁵)(2⁸+3⁵)=13·499.

These identities are additionally checked on every imprimitive word.
The finite enumeration shows that no primitive word contributes any other
499-divisible numerator. Thus 499 alone excludes primitive words in this
particular packet, even though it does not exclude all 5,005 words.

## Synchronized residues and CRT

Let Wⱼ,ᴮ(u,v) count tails of length j and sum B with numerator residues
(u,v) modulo (13,499). The base is one at (1,1) for j=1 and B≥1;
invalid ranges B<j are empty. At j≥2, each first letter a uses the same
value in both coordinates:

    (u,v) ↦ (3ʲ⁻¹+2ᵃu mod13, 3ʲ⁻¹+2ᵃv mod499).

The independently implemented joint dynamic programme agrees with every
entry of the directly enumerated joint table. Summing rows and columns
agrees with independently computed scalar recurrences modulo 13 and 499;
its CRT pushforward agrees with the independent scalar recurrence modulo
6487. The complete 13-by-499 table, including zero entries, and both full
marginal vectors are in the final JSON receipt.

The CRT map is r↦(r mod13,r mod499); its inverse is

    (u,v) ↦ 3992u+2496v mod6487.

Here 3992=499·8 is 1 modulo 13 and 0 modulo 499, while 2496=13·192
is 0 modulo 13 and 1 modulo 499. These observations prove the two inverse
identities. The same affine polynomial in both coordinates commutes with
this map. Each transition is invertible because both moduli are odd;
the inverse is multiplication by 2⁻ᵃ after subtraction of 3ʲ⁻¹.
The certificate checks both CRT inverse identities on all 6,487 elements,
and synchronized transitions and their inverses on all 408,681 triples
2≤j≤10, 1≤a≤7, 0≤r<6487.

Exact terminal support counts:

- Joint support: 3,473 of 6,487 pairs; 3,014 zero cells.
- Both marginal supports are full: 13 and 499 residues respectively.
- The marginal zero counts are 410 modulo 13 and 35 modulo 499.
- The joint count at (0,0) is zero.

Consequently, choosing a packet with a zero residue separately in each
factor does not produce one packet with both zero residues. The joint
recursion retains the common word and its multiplicity. This is an exact
finite example, not a claim of a general failure of CRT: CRT itself is
the verified bijection above.

## Least witnesses

In each nonempty divisibility class below, the lexicographically least
word also attains the least numerator. Both minimizations were checked.

- 13 divides C for p=(1,1,1,1,1,1,2,2,2,4):
  C=65065=13·5005, residue modulo 499 is 195, and the word is primitive.
- 499 divides C for p=(1,1,1,1,4,1,1,1,1,4):
  C=105289=499·211, residue modulo 13 is 2, and the least period is five.
  There is no primitive witness for divisibility by 499 in this packet.

## Reproduction and exact artifacts

From `research_companion`, run:

    python certificates/affine_crt_synchronization_checks.py --receipt audit/NEW_RECEIPT_NAME.json

Receipt paths are opened exclusively, so an existing receipt is never
overwritten. The final source SHA256 is
`ee0340744c8886ff55a7246ae0141576eac3ec60d262b7431bc3579c0198d71e`.
The final execution receipt is
`affine_crt_synchronization_checks_20260904_final.json`, SHA256
`d6e5476ba30318a0048aa0e7f99c6dbf06064056041b1a35f015219283daadce`.
It records PASS at 2026-09-04T14:31:02.180486+00:00, Python 3.13.9,
and peak working set 27,889,664 bytes; the command returned exit code zero.
All arithmetic
used for the mathematical checks is integer arithmetic.

The compact JSON serialization of the full joint table has SHA256
`c96f9a23ccf99710306d4188d737826fc3d03818e0fd80680fa3d9bd3ce626d3`.
The earlier `affine_crt_synchronization_checks_20260904.json` is preserved
as an initial-run receipt; the final run additionally pins the expected
strata and explicitly checks all 35 repeated-root identities.

A separate `python -O certificates/affine_crt_synchronization_checks.py`
test exited with code 1 and the message “Optimized Python is rejected:
assertions must remain active.” No registry, TeX, existing certificate,
AGENTS file, or remote project was changed by this subtask.
