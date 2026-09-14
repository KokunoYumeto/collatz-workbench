"""Finite exact checks for the repaired Tao Proposition 1.9 proof.

The accompanying TeX chapter proves the quantified probability estimate.
This certificate pins the v5, v7, journal, and frozen-route manifestations;
checks the exact source defects and repair locators; and exhaustively verifies
the finite valuation-cylinder morphism, its fibres, the positive-composition
counts, and the negative-binomial tail identity on bounded domains.

It does not certify Proposition 1.11, either main theorem, or any statement
about natural density or convergence of Collatz orbits.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from fractions import Fraction
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
V7_TEX = Path(
    r"C:\Users\LOCAL_USER\Documents\arxiv_latex\library\collatz_reconstruction"
    r"\latex\1909.03562v7\collatz.tex"
)
V7_ARCHIVE = Path(
    r"C:\Users\LOCAL_USER\Documents\arxiv_latex\library\collatz_reconstruction"
    r"\source\1909.03562v7.eprint"
)
V5_TEX = Path(
    r"C:\Users\LOCAL_USER\Documents\arxiv_latex\library\collatz_reconstruction"
    r"\latex\1909.03562v5\collatz.tex"
)
V5_ARCHIVE = Path(
    r"C:\Users\LOCAL_USER\Documents\arxiv_latex\library\collatz_reconstruction"
    r"\source\1909.03562v5.eprint"
)
JOURNAL_PDF = Path(
    r"C:\Users\LOCAL_USER\Documents\arxiv_latex\library\_recovered_from_papers"
    r"\by_title\Tao Almost all orbits of the Collatz map attain almost bounded values.pdf"
)
PROOF_TEX = ROOT / "tex" / "chapters" / "01h_tao_valuation_law.tex"

PINNED = {
    V7_TEX: (
        164_932,
        "bfbc39432d4084a276416cb019a592003c868fa32f18e2f90028ac325ae5c19d",
    ),
    V7_ARCHIVE: (
        1_226_861,
        "ba81acd6254838251f1ee585256a6f9f223cdc9c73bed0a3c4fd25782d0124ad",
    ),
    V5_TEX: (
        163_356,
        "c676b362b30807aa6690d0d4f16b8c8e84324732f5c0eb72ccfd875000276ae0",
    ),
    V5_ARCHIVE: (
        1_226_298,
        "eb7a4668ebf27a3f795f72fcdc8d992ada365824359c734fa58813c750ff2ede",
    ),
    JOURNAL_PDF: (
        1_008_484,
        "55c817c73498f940ed1e70f10208105922f1f7c89e378dcb629040c534151a2b",
    ),
    ROOT / "state" / "index_routes.jsonl": (
        274_170,
        "b05028694bf133b9b19f2b0c0a771323b7a47ae872c0712769267aaf1f1eff38",
    ),
    ROOT / "state" / "document_routes.jsonl": (
        324_776,
        "e439a5f9a70253b00824df5be791415e1c068d574c23f6f7f61851c19a88b2a5",
    ),
    ROOT / "state" / "index_snapshot.json": (
        799,
        "7d5a17440a3cb039f2bfbb4814567b5805117002136cc65687de738ee99af62f",
    ),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_line(lines: list[str], number: int, fragment: str) -> None:
    assert lines[number - 1].strip() == fragment, (number, lines[number - 1])


def require_source_locators() -> int:
    v7 = V7_TEX.read_text(encoding="utf-8").splitlines()
    v5 = V5_TEX.read_text(encoding="utf-8").splitlines()

    v7_required = {
        269: r"\begin{proposition}[Distribution of $n$-Syracuse valuation]\label{rach}  Let $n \in \N$, and let $\mathbf{N}$ be a random variable taking values in $2\N+1$.  Suppose there exist an absolute constant $c_0 > 0$ and some natural number $n' \geq (2+c_0) n$ such that $\mathbf{N} \mod 2^{n'}$ is approximately uniformly distributed in the odd residue classes $(2\Z+1)/2^{n'}\Z$ of $\Z/2^\ell\Z$, in the sense that",
        460: r"\begin{proof}  It is clear from \eqref{s-iter} that $\Aff_{\vec a^{(n)}(N)} \in 2\N+1$.  It remains to prove uniqueness.  The claim is easy for $n=0$, so suppose inductively that $n \geq 1$ and that uniqueness has already been established for $n-1$.  Suppose that we have found a tuple $\vec a \in (\N+1)^n$ for which $\Aff_{\vec a}(N)$ is an odd integer.  Then",
        469: r"$$ a_n = \nu_2( 3\Syr^{N-1}(N) + 1 )$$",
        603: r"\begin{lemma}[Tail bound]\label{tail}  We have",
        608: r"$$ \P( |\vec a^{(n)}(\mathbf{N})| \geq n' ) = \sum_{k=0}^{n-1}  \P( \a_{[1,k]} < n' \leq \a_{[1,k+1]} )$$",
        623: r"$$ \P( \a_{[1,k]} \leq n' < \a_{[1,k+1]} ) \ll \sum_{a_1,\dots,a_k \in \N+1: a_{[1,k]} < n'} 2^{-n'}.$$",
        633: r"\sum_{\vec a \in (\N+1)^n: |\vec a| < m} |\P(\vec a^{(n)}(\mathbf{N})=\vec a) - \P(\Geom(2)^n=\vec a)| + O( 2^{-cn} ).$$",
        638: r"\sum_{\vec a \in (\N+1)^n: |\vec a| < m} |\P(\vec a^{(n)}(\mathbf{N})=\vec a) - 2^{-|\vec a|}| \ll 2^{-cn}.",
        645: r"This constrains $\mathbf{N}$ to a single odd residue class modulo $2^{|\vec a|+1}$.  For $|\vec a| < n'$, the probability of falling in this class can be computed using \eqref{boy}, \eqref{tv-1} as $2^{-|\vec a|} + O( 2^{-n'} )$.  The left-hand side of \eqref{mup} is then bounded by",
        646: r"$$ \ll 2^{-n'} \# \{ \vec a \in (\N+1)^n: |\vec a| < n' \} = 2^{-n'} \binom{n'-1}{n}.$$",
        647: r"The claim now follows from Stirling's formula (or Chernoff's inequality), as in the proof of Lemma \ref{tail}.  This completes the proof of Proposition \ref{rach}.",
    }
    v5_required = {
        269: v7_required[269],
        597: r"\begin{lemma}[Tail bound]\label{tail}  We have",
        602: v7_required[608],
        617: v7_required[623],
        627: v7_required[633],
        632: v7_required[638],
        639: v7_required[645],
        640: v7_required[646],
        641: v7_required[647],
    }
    for number, fragment in v7_required.items():
        require_line(v7, number, fragment)
    for number, fragment in v5_required.items():
        require_line(v5, number, fragment)

    proof = PROOF_TEX.read_text(encoding="utf-8")
    proof_fragments = [
        r"\label{lem:Tao-Prop19-residue-fibre}",
        r"\label{eq:Tao-Prop19-TV-contraction}",
        r"\label{eq:Tao-Prop19-binomial-bound}",
        r"\label{prop:Tao-v7-Prop19-valuation-law}",
        r"\label{eq:Tao-Prop19-first-crossing}",
        r"\label{eq:Tao-Prop19-model-tail}",
        r"s_{n,n'}(\vec a)",
        r"\mathbin{\times_{\mathcal D_{n,n'}}}",
    ]
    for fragment in proof_fragments:
        assert fragment in proof
    return len(v7_required) + len(v5_required) + len(proof_fragments)


def valuation_2(value: int) -> int:
    assert value > 0
    answer = 0
    while value % 2 == 0:
        answer += 1
        value //= 2
    return answer


def syracuse_valuations(value: int, length: int) -> tuple[int, ...]:
    assert value > 0 and value % 2 == 1
    output: list[int] = []
    for _ in range(length):
        exponent = valuation_2(3 * value + 1)
        output.append(exponent)
        value = (3 * value + 1) // (2**exponent)
        assert value > 0 and value % 2 == 1
    return tuple(output)


def positive_tuples(length: int, total_less_than: int):
    if length == 0:
        if total_less_than > 0:
            yield ()
        return
    for values in itertools.product(range(1, total_less_than), repeat=length):
        if sum(values) < total_less_than:
            yield values


def cylinder_residue(values: tuple[int, ...]) -> tuple[int, int]:
    length = len(values)
    partials = [0]
    for value in values:
        partials.append(partials[-1] + value)
    total = partials[-1]
    numerator_offset = sum(
        3 ** (length - index) * 2 ** partials[index - 1]
        for index in range(1, length + 1)
    )
    modulus = 2 ** (total + 1)
    inverse = pow(3**length, -1, modulus)
    residue = (inverse * (2**total - numerator_offset)) % modulus
    return residue, modulus


def run_finite_checks() -> dict[str, int]:
    fibre_checks = 0
    valuation_equivalence_checks = 0
    lift_stability_checks = 0
    composition_checks = 0
    disjoint_partition_checks = 0
    negative_binomial_checks = 0
    binomial_weight_checks = 0
    explicit_section_checks = 0
    noninjective_fibre_checks = 0

    for length in range(1, 6):
        for precision in range(length + 1, min(11, length + 7)):
            tuples = list(positive_tuples(length, precision))
            assert len(tuples) == comb(precision - 1, length)
            composition_checks += 1

            assigned: dict[int, tuple[int, ...]] = {}
            odd_residues = range(1, 2**precision, 2)
            for values in tuples:
                total = sum(values)
                residue, modulus = cylinder_residue(values)
                assert residue % 2 == 1
                fibre = [
                    value
                    for value in odd_residues
                    if value % modulus == residue
                ]
                assert len(fibre) == 2 ** (precision - total - 1)
                fibre_checks += 1

                # The least positive odd representative of the cylinder is
                # the explicit zero-high-digits section used in the TeX map.
                section_value = residue
                assert 0 < section_value < modulus <= 2**precision
                assert syracuse_valuations(section_value, length) == values
                explicit_section_checks += 1

                for value in fibre:
                    observed = syracuse_valuations(value, length)
                    assert observed == values
                    valuation_equivalence_checks += 1
                    assert value not in assigned
                    assigned[value] = values

                    for high_digit in range(1, 4):
                        lifted = value + high_digit * 2**precision
                        assert syracuse_valuations(lifted, length) == values
                        lift_stability_checks += 1

            for value in odd_residues:
                observed = syracuse_valuations(value, length)
                if sum(observed) < precision:
                    assert assigned[value] == observed
                else:
                    assert value not in assigned
                disjoint_partition_checks += 1

            # Under the proposition's n'>(2n) range, the all-one tuple has a
            # fibre of size at least two.  This is the exact obstruction to a
            # left (and therefore two-sided) inverse of the valuation map.
            if precision >= 2 * length + 1:
                one_residue, one_modulus = cylinder_residue((1,) * length)
                one_fibre = [
                    value
                    for value in odd_residues
                    if value % one_modulus == one_residue
                ]
                assert len(one_fibre) == 2 ** (precision - length - 1)
                assert len(one_fibre) >= 2
                noninjective_fibre_checks += 1

            model_tail = Fraction(
                sum(comb(precision - 1, k) for k in range(length)),
                2 ** (precision - 1),
            )
            model_interior = sum(
                (
                    Fraction(comb(total - 1, length - 1), 2**total)
                    for total in range(length, precision)
                ),
                Fraction(0, 1),
            )
            assert model_tail == 1 - model_interior
            negative_binomial_checks += 1

    for c0 in (Fraction(1, 10), Fraction(1, 2), Fraction(1), Fraction(2)):
        p0 = Fraction(1, 1) / (2 + c0 / 2)
        z0 = p0 / (1 - p0)
        assert 0 < z0 < 1
        threshold = (Fraction(2, 1) / c0).__ceil__()
        for length in range(max(1, threshold), max(1, threshold) + 12):
            precision = ((2 + c0) * length).__ceil__()
            population = precision - 1
            assert Fraction(length, population) <= p0
            left = Fraction(
                sum(comb(population, k) for k in range(length + 1)),
                2**population,
            )
            right = z0 ** (-length) * ((1 + z0) / 2) ** population
            assert left <= right
            assert right < 1
            binomial_weight_checks += 1

    return {
        "fibre_checks": fibre_checks,
        "valuation_equivalence_checks": valuation_equivalence_checks,
        "lift_stability_checks": lift_stability_checks,
        "positive_composition_count_checks": composition_checks,
        "disjoint_partial_partition_checks": disjoint_partition_checks,
        "negative_binomial_identity_checks": negative_binomial_checks,
        "binomial_exponential_weight_checks": binomial_weight_checks,
        "explicit_section_checks": explicit_section_checks,
        "noninjective_fibre_checks": noninjective_fibre_checks,
    }


def main() -> int:
    for path, (size, digest) in PINNED.items():
        assert path.is_file(), path
        assert path.stat().st_size == size, (path, path.stat().st_size)
        assert sha256(path) == digest, path

    locator_checks = require_source_locators()
    metrics = run_finite_checks()
    report = {
        "status": "PASS",
        "scope": (
            "pinned v5/v7/journal identity and finite exact valuation-cylinder, "
            "fibre, composition, lift, and negative-binomial algebra"
        ),
        "pinned_hashes": len(PINNED),
        "source_and_proof_locator_checks": locator_checks,
        **metrics,
        "proposition_1_9_analytic_tail_proof_certified_by_script": False,
        "proposition_1_11_certified": False,
        "theorem_1_6_certified": False,
        "theorem_1_3_certified": False,
        "natural_density_claimed": False,
        "convergence_to_one_claimed": False,
    }
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
