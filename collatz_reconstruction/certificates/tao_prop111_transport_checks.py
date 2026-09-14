"""Finite exact integration checks for Tao's Proposition 1.11 edge.

The accompanying TeX proof supplies the quantified analytic argument from
Propositions 1.9 and 1.14 to first-passage stabilisation.  This certificate
pins the v5, v7, journal, and frozen-route manifestations; fixes the exact
source/version locators; and exhausts bounded instances of the affine inverse,
CRT, residue-lift, projective-offset, weighted-collapse, geometric-mass, and
parameter-arithmetic kernels used by that argument.

This finite script does not itself prove the logarithmic modular law, the
Chernoff and endpoint estimates, the uniform analytic c_n bound, either input
proposition, Proposition 1.11, or either downstream main theorem.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from fractions import Fraction
from math import gcd
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHELF = Path(
    r"C:\Users\LOCAL_USER\Documents\arxiv_latex\library\collatz_reconstruction"
)
V7_TEX = SHELF / "latex" / "1909.03562v7" / "collatz.tex"
V7_ARCHIVE = SHELF / "source" / "1909.03562v7.eprint"
V5_TEX = SHELF / "latex" / "1909.03562v5" / "collatz.tex"
V5_ARCHIVE = SHELF / "source" / "1909.03562v5.eprint"
JOURNAL_PDF = Path(
    r"C:\Users\LOCAL_USER\Documents\arxiv_latex\library\_recovered_from_papers"
    r"\by_title\Tao Almost all orbits of the Collatz map attain almost bounded values.pdf"
)

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

TAO_ROUTE_IDS = {
    "ROUTE-COL-77768C71C4B3C049A8B8",
    "ROUTE-COL-F8A670E4F671DDE694CB",
    "DOCROUTE-COL-8F0EDA4DC27DA85735AB",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_line(lines: list[str], number: int, fragment: str) -> None:
    assert lines[number - 1].strip() == fragment, (number, lines[number - 1])


def require_route_records() -> int:
    records: dict[str, dict] = {}
    for path in (
        ROOT / "state" / "index_routes.jsonl",
        ROOT / "state" / "document_routes.jsonl",
    ):
        for line in path.read_text(encoding="utf-8").splitlines():
            record = json.loads(line)
            route_id = record.get("route_id")
            if route_id in TAO_ROUTE_IDS:
                records[route_id] = record

    assert set(records) == TAO_ROUTE_IDS
    for record in records.values():
        title = record.get("title", record.get("bibliographic_identity", {}).get("title"))
        assert title == "Almost all orbits of the Collatz map attain almost bounded values"

    journal_digest = PINNED[JOURNAL_PDF][1]
    index_hashes: set[str] = set()
    for route_id in (
        "ROUTE-COL-77768C71C4B3C049A8B8",
        "ROUTE-COL-F8A670E4F671DDE694CB",
    ):
        record = records[route_id]
        hashes = record.get("hashes", {})
        if "sha256" in hashes:
            index_hashes.add(hashes["sha256"])
        index_hashes.update(hashes.get("sha256_values", []))
        index_hashes.update(
            path["sha256"]
            for path in record.get("paths", [])
            if "sha256" in path
        )
    assert journal_digest in index_hashes

    document = records["DOCROUTE-COL-8F0EDA4DC27DA85735AB"]
    assert document["identifiers"]["arxiv_id"] == "1909.03562"
    assert document["identifiers"]["arxiv_version_id"] == "1909.03562v5"
    document_hashes = {path["sha256"] for path in document["paths"]}
    assert journal_digest in document_hashes
    assert PINNED[V5_ARCHIVE][1] in document_hashes
    return len(records)


def require_source_and_reconstruction_locators() -> tuple[int, int, int]:
    v7 = V7_TEX.read_text(encoding="utf-8").splitlines()
    v5 = V5_TEX.read_text(encoding="utf-8").splitlines()

    required_v7 = {
        326: r"\begin{proposition}[Stabilisation of first passage]\label{transport}  For any $y$ with $2\N+1 \cap [y,y^\alpha]$ is non-empty (and in particular, for any sufficiently large $y$), let $\mathbf{N}_y$ be a random variable with distribution $\mathbf{N}_y \equiv \Log( 2\N+1 \cap [y,y^\alpha] )$.  Then for sufficiently large $x$, we have the estimates",
        328: r"\P( T_x(\mathbf{N}_y) = +\infty ) \ll x^{-c}",
        332: r"d_\TV( \Pass_x( \mathbf{N}_{x^\alpha} ), \Pass_x( \mathbf{N}_{x^{\alpha^2}} ) ) \ll \log^{-c} x",
        651: r"We are now ready to derive Proposition \ref{transport} (and thus Theorem \ref{main}) assuming Proposition \ref{tv-bound}.  Let $x$ be sufficiently large.  We take $y$ to be either $x^\alpha$ or $x^{\alpha^2}$.  From the heuristic \eqref{snn} (or \eqref{snn-2}) we expect the first passage time $\Pass_x(\mathbf{N}_y)$ to be roughly",
        652: r"$$ \Pass_x(\mathbf{N}_y) \approx \frac{\log \mathbf{N}_y / x}{\log(4/3)}$$",
        655: r"n_0 \coloneqq \left\lfloor \frac{\log x}{10 \log 2} \right\rfloor",
        659: r"m_0 \coloneqq \left\lfloor \frac{\alpha-1}{100} \log x \right\rfloor.",
        677: r"$$d_\TV( \mathbf{N}_y \mod 2^{3n_0}, \Unif((2\Z+1)/2^{3n_0}\Z)) \ll 2^{-3n_0} $$",
        680: r"d_\TV( \vec a^{(n_0)}(\mathbf{N}_y), \Geom(2)^{n_0} ) \ll 2^{-c n_0}.",
        684: r"\P( |\vec a^{(n_0)}(\mathbf{N}_y)| \leq 1.9 n_0 ) \leq \P( |\Geom(2)^{n_0}| \leq 1.9 n_0 ) + O(2^{-cn_0}) \ll 2^{-cn_0} \ll x^{-c}",
        689: r"and hence if $|\vec a^{(n_0)}(\mathbf{N}_y)| > 1.9 n$ then",
        712: r"\begin{proposition}[Approximate formula]  Let $E \subset 2\N+1 \cap [1,x]$ and $y = x^\alpha, x^{\alpha^2}$.  Then we have",
        714: r"\P( \Pass_x( \mathbf{N}_y ) \in E )  =  \sum_{n \in I_y} \sum_{\vec a \in {\mathcal A}^{(n-m_0)}} \sum_{M \in E'} \P( \Aff_{\vec a}(\mathbf{N}_y) = M ) + O( \log^{-c} x  )",
        718: r"I_y \coloneqq \left[\frac{\log( y / x )}{\log \frac{4}{3}} + \log^{0.8} x, \frac{\log( y^\alpha / x )}{\log \frac{4}{3}} - \log^{0.8} x\right],",
        720: r"$E'$ is the set of odd natural numbers $M \in 2\N+1$ such that $T_x(M) = m_0$ and $\Pass_x(M) \in E$ with",
        724: r"and for any natural number $n'$, ${\mathcal A}^{(n')} \subset (\N+1)^{n'}$ denotes the set of all tuples $(a_1,\dots,a_{n'}) \in (\N+1)^{n'}$ such that",
        726: r"|a_{[1,n]} - 2n| < \log^{0.6} x",
        759: r"$$ \mathbf{N}_y \subset [y + 2 \log^{0.8} x, y^\alpha - 2 \log^{0.8} x];$$",
        762: r"\P( T_x(\mathbf{N}_y) \in I_y) = 1 - O( \log^{-c} x ).",
        791: r"$$ \Syr^{n'}(\mathbf{N}_y) = \exp(O(\log^{0.6} x)) (4/3)^{n-m_0-n'} \Syr^{n-m_0}(\mathbf{N}_y) \geq \exp(O(\log^{0.6} x)) \Syr^{n-m_0}(\mathbf{N}_y) $$",
        795: r"$$ T_x(\mathbf{N}_y) = n-m_0 + T_x(\Syr^{n-m_0}(\mathbf{N}_y)) = n $$",
        797: r"$$ \Pass_x(\mathbf{N}_y) = \Pass_x(\Syr^{n-m_0}(\mathbf{N}_y)) \in E.$$",
        805: r"Suppose that $\vec a = (a_1,\dots,a_{n-m})$ is a tuple in ${\mathcal A}^{(n-m)}$, and $M \in E'$.  From Lemma \ref{iter-lem}, we see that the event $\left(\Syr^{n-m_0}(\mathbf{N}_y) = M\right) \wedge \left(\vec a^{(n-m_0)}(\mathbf{N}_y) = \vec a\right)$ holds if and only if $\Aff_{\vec a}( \mathbf{N}_y) \in E'$, and the claim \eqref{approx-form} follows.",
        810: r"M = F_{n-m_0}(\vec a) \mod 3^{n-m_0}",
        814: r"\mathbf{N}_y = 2^{|\vec a|} \frac{M - F_{n-m_0}(\vec a)}{3^{n-m_0}}.",
        823: r"$$ \P( \Aff_{\vec a}(\mathbf{N}_y) = M ) = \frac{1}{\left(1 + O( \frac{1}{x})\right)\frac{\alpha-1}{2} \log y} 2^{-|\vec a|} \frac{3^{n-m_0}}{M - F_{n-m_0}(\vec a)}.$$",
        835: r"3^{n-m_0} \sum_{\vec a \in {\mathcal A}^{(n-m_0)}} 2^{-|\vec a|} \sum_{M \in E': M = F_{n-m_0}(\vec a) \mod 3^{n-m_0}} \frac{1}{M} = Z + O( \log^{-c} x  )",
        839: r"Z \coloneqq \sum_{M \in E'} \frac{3^{m_0} \P( M = \Syrac(\Z/3^{m_0}\Z) \mod 3^{m_0})}{M}.",
        842: r"$$ \# I_y = (1 + O( \log^{-c} x  )) \frac{\alpha-1}{\log \frac{4}{3}} \log y,$$",
        850: r"\E 1_{(\a_1,\dots,\a_{n-m_0}) \in {\mathcal A}^{(n-m_0)}} c_n( F_{n-m_0}(\a_1,\dots,\a_{n-m_0}) \mod 3^{n-m_0} )",
        854: r"c_n( X ) \coloneqq 3^{n-m_0} \sum_{M \in E': M = X \mod 3^{n-m_0}} \frac{1}{M}.",
        858: r"\begin{lemma}\label{loam}  We have $c_n(X) \ll 1$ for all $n \in I_y$ and $X \in \Z/3^{n-m_0}\Z$.",
        868: r"3^{m_0} 2^{-a_{[1,m_0]}} M + F_{m_0}(a_1,\dots,a_{m_0}) \leq x < 3^{m_0} 2^{-a_{[1,m_0-1]}} M + F_{m_0-1}(a_1,\dots,a_{m_0-1}) $$",
        878: r"$$ 3^{m_0} M + 2^{a_{[1,m_0]}} F_{m_0}(a_1,\dots,a_{m_0}) = 2^{a_{[1,m_0]}} \mod 2^{a_{[1,m_0]}+1} $$",
        879: r"and so $M$ is constrained to a single residue class modulo $2^{a_{[1,m_0]}+1}$.   In \eqref{cn-def} we are also constraining $M$ to a single residue class modulo $3^{n-m_0}$; by the Chinese remainder theorem, these constraints can be combined into a single residue class modulo $2^{a_{[1,m_0]}+1} 3^{n-m_0}$.  Note from the integral test that",
        898: r"Now suppose instead that $2^{a_{[1,m_0]}} > x^{0.5}$, we recall from \eqref{s-iter} that",
        899: r"$$ a_{m_0} = \nu_2\left( 3 (3^{m_0} 2^{-a_{[1,m_0-1]}} M + F_{m_0-1}(a_1,\dots,a_{m_0-1})) + 1\right)$$",
        908: r"&\ll 3^n 2^{-a_{[1,m_0]}} + 2^{-a_{[1,m_0]}} a_{m_0}\\",
        909: r"&\ll 2^{-a_{[1,m_0]}/2}",
        913: r"$$ c_n(X) \ll \sum_{a_1,\dots,a_{m_0} \in \N} 2^{-a_{[1,m_0]}/2}$$",
        917: r"From the above lemma and \eqref{lo}, we may write \eqref{soda} as",
        922: r"Applying Proposition \ref{tv-bound}, Lemma \ref{loam} and the triangle inequality, one can thus write the preceding expression as",
        923: r"$$ \sum_{X \in \Z/3^{n-m_0}\Z} c_n(X) 3^{2m_0-n} \P( \Syrac(\Z/3^{m_0}\Z) = X \mod 3^{m_0}) +  O( \log^{-c} x  )$$",
        924: r"and the claim \eqref{zeno} then follows from \eqref{cn-def}.",
    }

    required_v5 = {
        326: r"\begin{proposition}[Stabilisation of first passage]\label{transport}  For each sufficiently large $y$, let $\mathbf{N}_y$ be a random variable with distribution $\mathbf{N}_y \equiv \Log( 2\N+1 \cap [y,y^\alpha] )$ (note for sufficiently large $y$ that $2\N+1 \cap [y,y^\alpha]$ is non-empty).  Then for sufficiently large $x$, we have the estimates",
        328: required_v7[328],
        332: required_v7[332],
        645: r"We are now ready to derive Proposition \ref{transport} (and thus Theorem \ref{main}) assuming Proposition \ref{tv-bound}.  Let $x$ be sufficiently large.  We take $y$ to be either $x^\alpha$ or $x^{\alpha^2}$.  From the heuristic \eqref{snn} (or \eqref{snn-2}) we expect the first passage time $\Pass_x(\mathbf{N}_y)$ to be roughly",
        646: required_v7[652],
        649: r"n_0 \coloneqq \left\lfloor \frac{\log x}{10 \log 2} \right\rfloor",
        653: r"m_0 \coloneqq \left\lfloor \frac{\alpha-1}{100} \log x \right\rfloor.",
        671: required_v7[677],
        674: required_v7[680],
        678: required_v7[684],
        683: required_v7[689],
        706: required_v7[712],
        708: required_v7[714],
        712: required_v7[718],
        714: required_v7[720],
        718: required_v7[724],
        720: required_v7[726],
        753: required_v7[759],
        756: required_v7[762],
        785: required_v7[791],
        789: r"$$ \Pass_x(\mathbf{N}_y) = n-m_0 + \Pass_x(\Syr^{n-m_0}(\mathbf{N}_y)) = n $$",
        791: r"$$ T_x(\mathbf{N}_y) = T_x(\Syr^{n-m_0}(\mathbf{N}_y)) \in E.$$",
        799: required_v7[805],
        804: required_v7[810],
        808: required_v7[814],
        817: required_v7[823],
        829: required_v7[835],
        833: required_v7[839],
        836: required_v7[842],
        844: required_v7[850],
        848: required_v7[854],
        852: required_v7[858],
        862: required_v7[868],
        872: required_v7[878],
        873: required_v7[879],
        892: required_v7[898],
        893: required_v7[899],
        902: required_v7[908],
        903: required_v7[909],
        907: required_v7[913],
        911: required_v7[917],
        916: required_v7[922],
        917: required_v7[923],
        918: required_v7[924],
    }

    for number, fragment in required_v7.items():
        require_line(v7, number, fragment)
    for number, fragment in required_v5.items():
        require_line(v5, number, fragment)

    # The comparison boundary is substantive: v7 broadens the harmless y
    # quantifier and repairs the v5/journal time/location interchange.
    assert required_v7[326] != required_v5[326]
    assert r"T_x(\mathbf{N}_y) = n-m_0" in required_v7[795]
    assert r"\Pass_x(\mathbf{N}_y) = n-m_0" in required_v5[789]
    assert r"\Pass_x(\mathbf{N}_y) = \Pass_x" in required_v7[797]
    assert r"T_x(\mathbf{N}_y) = T_x" in required_v5[791]

    reconstruction_fragments = {
        ROOT / "tex" / "chapters" / "01_literature_spine.tex": [
            r"\label{prop:Tao-v7-endpoint-buffer}",
            r"\label{prop:Tao-v7-Prop52-cn-repair}",
            r"\label{eq:Tao-v7-fixed-M-repaired}",
            r"\label{eq:Tao-v7-cn}",
            r"\label{eq:Tao-v7-Z-repaired}",
            r"\label{eq:Tao-v7-cn-low-A}",
            r"\label{eq:Tao-v7-cn-high-A}",
        ],
        ROOT / "tex" / "chapters" / "01g_tao_fourier_renewal.tex": [
            r"\label{def:Tao-uniform-lift}",
            r"\label{eq:Tao-lift-projective}",
            r"\label{prop:Tao-v7-Fourier-to-mixing}",
            r"\label{cor:Tao-v7-fine-scale-branch}",
        ],
        ROOT / "tex" / "chapters" / "01h_tao_valuation_law.tex": [
            r"\label{lem:Tao-Prop19-residue-fibre}",
            r"\label{prop:Tao-v7-Prop19-valuation-law}",
        ],
    }
    reconstruction_count = 0
    for path, fragments in reconstruction_fragments.items():
        text = path.read_text(encoding="utf-8")
        for fragment in fragments:
            assert fragment in text, (path, fragment)
            reconstruction_count += 1
    return len(required_v7), len(required_v5), reconstruction_count


def prefix_data(coordinates: tuple[int, ...]) -> tuple[list[int], int, int]:
    partials = [0]
    for coordinate in coordinates:
        assert coordinate >= 1
        partials.append(partials[-1] + coordinate)
    length = len(coordinates)
    numerator_offset = sum(
        3 ** (length - index) * 2 ** partials[index - 1]
        for index in range(1, length + 1)
    )
    return partials, partials[-1], numerator_offset


def offset(coordinates: tuple[int, ...]) -> Fraction:
    partials, total, numerator_offset = prefix_data(coordinates)
    del partials
    return Fraction(numerator_offset, 2**total)


def suffix_offset(coordinates: tuple[int, ...]) -> Fraction:
    length = len(coordinates)
    return sum(
        (
            Fraction(
                3 ** (length - index - 1),
                2 ** sum(coordinates[index:]),
            )
            for index in range(length)
        ),
        Fraction(0),
    )


def affine(coordinates: tuple[int, ...], value: int | Fraction) -> Fraction:
    _, total, numerator_offset = prefix_data(coordinates)
    return Fraction(3 ** len(coordinates), 2**total) * value + Fraction(
        numerator_offset, 2**total
    )


def affine_by_composition(
    coordinates: tuple[int, ...], value: int | Fraction
) -> Fraction:
    answer = Fraction(value)
    for coordinate in coordinates:
        answer = Fraction(3 * answer + 1, 2**coordinate)
    return answer


def affine_inverse(coordinates: tuple[int, ...], target: int) -> Fraction:
    _, total, numerator_offset = prefix_data(coordinates)
    return Fraction(2**total * target - numerator_offset, 3 ** len(coordinates))


def mod_fraction(value: Fraction, modulus: int) -> int:
    assert modulus >= 1 and gcd(value.denominator, modulus) == 1
    if modulus == 1:
        return 0
    return (value.numerator * pow(value.denominator, -1, modulus)) % modulus


def valuation_2(value: int) -> int:
    assert value > 0
    answer = 0
    while value % 2 == 0:
        value //= 2
        answer += 1
    return answer


def syracuse_prefix(value: int, length: int) -> tuple[tuple[int, ...], int]:
    assert value > 0 and value % 2 == 1
    coordinates: list[int] = []
    for _ in range(length):
        coordinate = valuation_2(3 * value + 1)
        coordinates.append(coordinate)
        value = (3 * value + 1) // (2**coordinate)
        assert value > 0 and value % 2 == 1
    return tuple(coordinates), value


def cylinder_residue(coordinates: tuple[int, ...]) -> tuple[int, int]:
    _, total, numerator_offset = prefix_data(coordinates)
    modulus = 2 ** (total + 1)
    residue = (
        pow(3 ** len(coordinates), -1, modulus)
        * (2**total - numerator_offset)
    ) % modulus
    assert residue % 2 == 1
    return residue, modulus


def affine_inverse_checks() -> dict[str, int]:
    recurrence_checks = 0
    congruence_checks = 0
    positive_inverse_checks = 0
    singleton_checks = 0

    for length in range(1, 6):
        modulus_3 = 3**length
        for coordinates in itertools.product(range(1, 5), repeat=length):
            coordinates = tuple(coordinates)
            _, total, numerator_offset = prefix_data(coordinates)
            assert numerator_offset % 2 == 1
            assert offset(coordinates) == suffix_offset(coordinates)
            recurrence_checks += 1
            for value in (1, 3, 17, 2 ** (total + 1) + 1):
                assert affine(coordinates, value) == affine_by_composition(
                    coordinates, value
                )
                recurrence_checks += 1

            offset_residue = mod_fraction(offset(coordinates), modulus_3)
            for target in range(1, 6 * modulus_3 + 1, 2):
                candidate = affine_inverse(coordinates, target)
                congruent = target % modulus_3 == offset_residue
                assert (candidate.denominator == 1) == congruent
                assert affine(coordinates, candidate) == target
                congruence_checks += 2

                if candidate.denominator == 1 and candidate > 0:
                    integer_candidate = candidate.numerator
                    assert integer_candidate % 2 == 1
                    observed, final_value = syracuse_prefix(
                        integer_candidate, length
                    )
                    assert observed == coordinates
                    assert final_value == target
                    positive_inverse_checks += 3

                    for shift in (-6, -4, -2, 2, 4, 6):
                        other = integer_candidate + shift
                        if other > 0:
                            assert affine(coordinates, other) != target
                            singleton_checks += 1

    # Exact counterexample to source line 805's fixed-M membership wording.
    printed_membership_witness_checks = 0
    coordinates = (1,)
    value = 3
    fixed_target = 1
    target_set = {1, 5}
    assert affine(coordinates, value) == 5
    assert affine(coordinates, value) in target_set
    assert affine(coordinates, value) != fixed_target
    printed_membership_witness_checks += 3

    return {
        "affine_recurrence_and_offset_checks": recurrence_checks,
        "affine_inverse_congruence_checks": congruence_checks,
        "positive_odd_inverse_and_valuation_checks": positive_inverse_checks,
        "affine_singleton_checks": singleton_checks,
        "printed_fixed_M_membership_counterexample_checks": printed_membership_witness_checks,
    }


def crt_checks() -> int:
    checks = 0
    for length in range(1, 5):
        for coordinates in itertools.product(range(1, 4), repeat=length):
            coordinates = tuple(coordinates)
            binary_residue, binary_modulus = cylinder_residue(coordinates)
            for residue_level in range(length, 6):
                ternary_modulus = 3**residue_level
                assert gcd(binary_modulus, ternary_modulus) == 1
                combined_modulus = binary_modulus * ternary_modulus
                seen: set[int] = set()
                for ternary_residue in range(ternary_modulus):
                    multiplier = (
                        (ternary_residue - binary_residue)
                        * pow(binary_modulus, -1, ternary_modulus)
                    ) % ternary_modulus
                    combined = (
                        binary_residue + binary_modulus * multiplier
                    ) % combined_modulus
                    assert combined % binary_modulus == binary_residue
                    assert combined % ternary_modulus == ternary_residue
                    assert combined not in seen
                    seen.add(combined)
                    checks += 3
                assert len(seen) == ternary_modulus
                checks += 1
    return checks


def l1(vector: list[Fraction]) -> Fraction:
    return sum((abs(value) for value in vector), Fraction(0))


def lift(mu: list[Fraction], coarse: int, fine: int) -> list[Fraction]:
    assert 0 <= coarse <= fine and len(mu) == 3**coarse
    scale = Fraction(1, 3 ** (fine - coarse))
    return [scale * mu[value % (3**coarse)] for value in range(3**fine)]


def pushforward(nu: list[Fraction], coarse: int, fine: int) -> list[Fraction]:
    assert 0 <= coarse <= fine and len(nu) == 3**fine
    return [
        sum(
            (nu[value] for value in range(residue, 3**fine, 3**coarse)),
            Fraction(0),
        )
        for residue in range(3**coarse)
    ]


def fibre_projection(
    nu: list[Fraction], coarse: int, fine: int
) -> list[Fraction]:
    return lift(pushforward(nu, coarse, fine), coarse, fine)


def lift_and_projective_checks() -> tuple[int, int, int]:
    lift_checks = 0
    fibre_checks = 0
    suffix_checks = 0

    for fine in range(0, 6):
        nu = [
            Fraction(((11 * value + 5 * fine) % 23) - 11, 1 + value % 5)
            for value in range(3**fine)
        ]
        for coarse in range(0, fine + 1):
            mu = [
                Fraction(((7 * value + 3 * coarse) % 17) - 8, 1 + value % 4)
                for value in range(3**coarse)
            ]
            lifted = lift(mu, coarse, fine)
            projected = fibre_projection(nu, coarse, fine)
            assert pushforward(lifted, coarse, fine) == mu
            assert sum(lifted, Fraction(0)) == sum(mu, Fraction(0))
            assert l1(lifted) == l1(mu)
            assert sum(projected, Fraction(0)) == sum(nu, Fraction(0))
            assert l1(projected) <= l1(nu)
            assert fibre_projection(projected, coarse, fine) == projected
            lift_checks += 6

            for residue in range(3**coarse):
                fibre = list(range(residue, 3**fine, 3**coarse))
                assert len(fibre) == 3 ** (fine - coarse)
                values = {lifted[element] for element in fibre}
                assert values == {
                    Fraction(mu[residue], 3 ** (fine - coarse))
                }
                fibre_checks += 2

            for middle in range(coarse, fine + 1):
                assert lift(lift(mu, coarse, middle), middle, fine) == lifted
                lift_checks += 1

    for length in range(1, 7):
        for coordinates in itertools.product(range(1, 5), repeat=length):
            coordinates = tuple(coordinates)
            full_offset = offset(coordinates)
            for coarse in range(0, length + 1):
                modulus = 3**coarse
                suffix = coordinates[length - coarse :] if coarse else ()
                assert mod_fraction(full_offset, modulus) == mod_fraction(
                    offset(suffix), modulus
                )
                suffix_checks += 1

    return lift_checks, fibre_checks, suffix_checks


def weighted_collapse_checks() -> tuple[int, int]:
    collapse_checks = 0
    factor_checks = 0
    for coarse in range(1, 4):
        coarse_weights = [
            Fraction(1 + ((5 * value + coarse) % 11), 1)
            for value in range(3**coarse)
        ]
        normalizer = sum(coarse_weights, Fraction(0))
        coarse_law = [weight / normalizer for weight in coarse_weights]
        for fine in range(coarse, 6):
            fine_modulus = 3**fine
            lifted = lift(coarse_law, coarse, fine)
            candidate_sets = [
                set(),
                set(range(1, 4 * fine_modulus + 2, 2)),
                {
                    value
                    for value in range(1, 5 * fine_modulus + 2, 2)
                    if (value * value + 3 * value + fine) % 7 in (0, 1, 4)
                },
            ]
            for candidates in candidate_sets:
                c_values = [Fraction(0) for _ in range(fine_modulus)]
                for target in candidates:
                    c_values[target % fine_modulus] += Fraction(
                        fine_modulus, target
                    )
                left = sum(
                    (
                        c_values[residue] * lifted[residue]
                        for residue in range(fine_modulus)
                    ),
                    Fraction(0),
                )
                right = sum(
                    (
                        Fraction(3**coarse, target)
                        * coarse_law[target % (3**coarse)]
                        for target in candidates
                    ),
                    Fraction(0),
                )
                assert left == right
                assert sum(c_values, Fraction(0)) == sum(
                    (Fraction(fine_modulus, target) for target in candidates),
                    Fraction(0),
                )
                collapse_checks += 2

            n_parameter = fine + coarse
            assert fine == n_parameter - coarse
            source_factor = (
                Fraction(3 ** (2 * coarse - n_parameter), 1)
                if 2 * coarse >= n_parameter
                else Fraction(1, 3 ** (n_parameter - 2 * coarse))
            )
            assert Fraction(1, 3 ** (fine - coarse)) == source_factor
            factor_checks += 2
    return collapse_checks, factor_checks


def cn_partition_checks() -> int:
    checks = 0
    for prefix_length in range(1, 5):
        for residue_level in range(prefix_length, 6):
            modulus = 3**residue_level
            candidates = {
                value
                for value in range(1, 6 * modulus + 2, 2)
                if (value + prefix_length) % 5 != 0
            }
            direct = [Fraction(0) for _ in range(modulus)]
            grouped: dict[tuple[int, ...], list[Fraction]] = {}
            for target in candidates:
                residue = target % modulus
                contribution = Fraction(modulus, target)
                direct[residue] += contribution
                coordinates, _ = syracuse_prefix(target, prefix_length)
                grouped.setdefault(
                    coordinates, [Fraction(0) for _ in range(modulus)]
                )[residue] += contribution

            recombined = [Fraction(0) for _ in range(modulus)]
            for vector in grouped.values():
                for residue, contribution in enumerate(vector):
                    recombined[residue] += contribution
            assert recombined == direct

            for target in candidates:
                coordinates, _ = syracuse_prefix(target, prefix_length)
                binary_residue, binary_modulus = cylinder_residue(coordinates)
                assert target % binary_modulus == binary_residue
                checks += 1
            checks += 1
    return checks


def surd_multiply(
    left: tuple[Fraction, Fraction], right: tuple[Fraction, Fraction]
) -> tuple[Fraction, Fraction]:
    """Multiply a+b*sqrt(2) and c+d*sqrt(2) exactly."""

    a, b = left
    c, d = right
    return a * c + 2 * b * d, a * d + b * c


def surd_power(
    value: tuple[Fraction, Fraction], exponent: int
) -> tuple[Fraction, Fraction]:
    assert exponent >= 0
    answer = (Fraction(1), Fraction(0))
    base = value
    while exponent:
        if exponent % 2:
            answer = surd_multiply(answer, base)
        base = surd_multiply(base, base)
        exponent //= 2
    return answer


def truncated_mass_checks() -> tuple[int, int, int]:
    one_coordinate_checks = 0
    tuple_mass_checks = 0
    nonuniform_majorant_checks = 0

    z = Fraction(1, 2)
    assert z / (1 - z) == 1
    assert z / (1 - z) ** 2 == 2
    one_coordinate_checks += 2

    for cutoff in range(1, 33):
        geometric = sum(
            (Fraction(1, 2**coordinate) for coordinate in range(1, cutoff + 1)),
            Fraction(0),
        )
        weighted = sum(
            (
                Fraction(coordinate, 2**coordinate)
                for coordinate in range(1, cutoff + 1)
            ),
            Fraction(0),
        )
        assert geometric == 1 - Fraction(1, 2**cutoff)
        assert weighted == 2 - Fraction(cutoff + 2, 2**cutoff)
        one_coordinate_checks += 2

    for length in range(1, 6):
        for cutoff in range(1, 7):
            direct_mass = Fraction(0)
            direct_last_moment = Fraction(0)
            for coordinates in itertools.product(
                range(1, cutoff + 1), repeat=length
            ):
                total = sum(coordinates)
                weight = Fraction(1, 2**total)
                direct_mass += weight
                direct_last_moment += coordinates[-1] * weight
            finite_geometric = 1 - Fraction(1, 2**cutoff)
            finite_moment = 2 - Fraction(cutoff + 2, 2**cutoff)
            assert direct_mass == finite_geometric**length
            assert direct_last_moment == (
                finite_geometric ** (length - 1) * finite_moment
            )
            tuple_mass_checks += 2

    # In Q(sqrt(2)), q=1/sqrt(2)=sqrt(2)/2 and
    # q/(1-q)=1+sqrt(2).  This is the exact one-coordinate sum of the
    # printed 2^(-A/2) majorant.  It is >2 and therefore its m-th power is
    # not uniformly bounded; the rational lower bound sqrt(2)>7/5 checks
    # that growth exactly on the declared finite domain.
    q = (Fraction(0), Fraction(1, 2))
    square_root_mass = (Fraction(1), Fraction(1))
    one_minus_q = (Fraction(1), Fraction(-1, 2))
    assert surd_multiply(one_minus_q, square_root_mass) == q
    assert surd_multiply(q, q) == (Fraction(1, 2), Fraction(0))
    nonuniform_majorant_checks += 2

    assert Fraction(7, 5) ** 2 < 2 < Fraction(3, 2) ** 2
    assert Fraction(1) + Fraction(3, 2) == Fraction(5, 2)
    e_partial_lower = sum(
        (Fraction(1), Fraction(1), Fraction(1, 2), Fraction(1, 6)),
        Fraction(0),
    )
    assert Fraction(5, 2) < e_partial_lower
    nonuniform_majorant_checks += 3
    for length in range(1, 17):
        rational_part, radical_part = surd_power(square_root_mass, length)
        assert radical_part > 0
        assert (
            rational_part + Fraction(7, 5) * radical_part > 2**length
        )
        nonuniform_majorant_checks += 2

    return one_coordinate_checks, tuple_mass_checks, nonuniform_majorant_checks


def log_bounds(value: Fraction, terms: int = 40) -> tuple[Fraction, Fraction]:
    """Exact enclosure from log(value)=2*atanh((value-1)/(value+1))."""

    assert value > 1
    z = (value - 1) / (value + 1)
    partial = 2 * sum(
        (z ** (2 * index + 1) / (2 * index + 1) for index in range(terms + 1)),
        Fraction(0),
    )
    remainder_upper = (
        2
        * z ** (2 * terms + 3)
        / ((2 * terms + 3) * (1 - z * z))
    )
    return partial, partial + remainder_upper


def parameter_checks() -> tuple[int, dict[str, str]]:
    checks = 0
    alpha = Fraction(1001, 1000)
    m0_coefficient = (alpha - 1) / 100
    assert m0_coefficient == Fraction(1, 100_000)
    checks += 1

    # The TeX proof declares M=20, i.e. indices 0,...,20.  Keep the
    # executable enclosure at exactly that stated truncation.
    lambda_lower, lambda_upper = log_bounds(Fraction(4, 3), terms=20)
    log_two_lower, log_two_upper = log_bounds(Fraction(2), terms=20)
    log_three_lower, log_three_upper = log_bounds(Fraction(3), terms=20)
    assert Fraction(1, 4) < lambda_lower < lambda_upper < 1
    assert Fraction(2, 3) < log_two_lower < log_two_upper < 1
    assert 1 < log_three_lower < log_three_upper < Fraction(6, 5)
    checks += 6

    interval_data: dict[str, str] = {}
    for beta in (alpha, alpha**2):
        lower_coefficient_lower = (beta - 1) / lambda_upper
        upper_coefficient_upper = (alpha * beta - 1) / lambda_lower
        n0_coefficient_lower = Fraction(1, 10) / log_two_upper
        width_coefficient_lower = (alpha - 1) * beta / lambda_upper
        assert lower_coefficient_lower > 2 * m0_coefficient
        assert upper_coefficient_upper < n0_coefficient_lower
        assert width_coefficient_lower > 0
        assert (alpha - 1) * beta > 0
        checks += 4
        interval_data[f"beta_{beta}_lower_n_coefficient_lower"] = str(
            lower_coefficient_lower
        )
        interval_data[f"beta_{beta}_upper_n_coefficient_upper"] = str(
            upper_coefficient_upper
        )
        interval_data[f"beta_{beta}_width_coefficient_lower"] = str(
            width_coefficient_lower
        )

        # With q=2^(3n_0), q<=x^(3/10).  The integral-test discrepancy
        # scale q/y is at most q^(-1) once q^2/y<=x^(3/5-beta).
        modular_discrepancy_exponent = Fraction(3, 5) - beta
        assert modular_discrepancy_exponent < -Fraction(3, 10)
        checks += 1

    endpoint_exponent = Fraction(4, 5)
    orbit_exponent = Fraction(3, 5)
    reconstruction_exponent = Fraction(7, 10)
    assert endpoint_exponent - orbit_exponent == Fraction(1, 5)
    assert endpoint_exponent - reconstruction_exponent == Fraction(1, 10)
    assert Fraction(1) - endpoint_exponent == Fraction(1, 5)
    checks += 3

    # Proposition 1.9 is used with n'=3n_0 and c_0=1.
    for n0 in range(0, 101):
        n_prime = 3 * n0
        assert n_prime == (2 + 1) * n0
        checks += 1

    # Exact exponent controls in the c_n repair.
    assert 3**5 < 2**8
    n_exponent_upper = Fraction(4, 25)
    low_A_exponent = Fraction(1, 2) + n_exponent_upper - 1
    high_A_exponent = (
        n_exponent_upper - Fraction(1, 4) + Fraction(1, 100_000)
    )
    assert low_A_exponent == -Fraction(17, 50)
    assert high_A_exponent == -Fraction(8_999, 100_000)
    checks += 3

    # The descent branch uses n_0=floor(L/(10 log 2)).  The floor only
    # changes the estimate by an absolute factor because 3/2^(19/10)<1.
    assert log_three_upper < Fraction(19, 10) * log_two_lower
    descent_exponent_upper = alpha**3 + (
        log_three_upper / log_two_lower - Fraction(19, 10)
    ) / 10
    offset_exponent_upper = log_three_upper / (10 * log_two_lower)
    assert descent_exponent_upper < Fraction(243, 250)
    assert offset_exponent_upper < Fraction(159, 1000)
    checks += 3

    # The offset term has scale at most x^(4/25), while M has leading x
    # scale; the resulting fixed power gap precedes the o(L) buffers.
    assert n_exponent_upper - 1 == -Fraction(21, 25)
    checks += 1

    data = {
        "alpha": str(alpha),
        "m0_log_x_coefficient": str(m0_coefficient),
        "lambda_lower": str(lambda_lower),
        "lambda_upper": str(lambda_upper),
        "low_A_q_over_M0_x_exponent_upper": str(low_A_exponent),
        "large_A_tail_x_exponent_upper": str(high_A_exponent),
        "descent_x_exponent_upper": str(descent_exponent_upper),
        "offset_x_exponent_upper": str(offset_exponent_upper),
        "endpoint_minus_orbit_exponent": "1/5",
        "endpoint_minus_reconstruction_exponent": "1/10",
        **interval_data,
    }
    return checks, data


def main() -> int:
    for path, (size, digest) in PINNED.items():
        assert path.is_file(), path
        assert path.stat().st_size == size, (path, path.stat().st_size)
        assert sha256(path) == digest, path

    route_checks = require_route_records()
    v7_locators, v5_locators, reconstruction_locators = (
        require_source_and_reconstruction_locators()
    )
    affine_metrics = affine_inverse_checks()
    crt_metric = crt_checks()
    lift_metric, fibre_metric, suffix_metric = lift_and_projective_checks()
    collapse_metric, factor_metric = weighted_collapse_checks()
    partition_metric = cn_partition_checks()
    one_coordinate_metric, tuple_mass_metric, majorant_metric = (
        truncated_mass_checks()
    )
    parameter_metric, parameter_data = parameter_checks()

    report = {
        "status": "PASS",
        "scope": (
            "version/hash/locator pinning and finite exact Proposition 1.11 "
            "integration kernels only"
        ),
        "pinned_hashes": len(PINNED),
        "route_identity_checks": route_checks,
        "v7_source_locator_checks": v7_locators,
        "v5_source_locator_checks": v5_locators,
        "reconstruction_locator_checks": reconstruction_locators,
        "version_boundary_checks": 5,
        **affine_metrics,
        "constructive_CRT_checks": crt_metric,
        "uniform_lift_projection_checks": lift_metric,
        "ternary_reduction_fibre_checks": fibre_metric,
        "offset_suffix_projective_checks": suffix_metric,
        "cn_uniform_lift_weighted_collapse_checks": collapse_metric,
        "lift_exponent_factor_checks": factor_metric,
        "cn_valuation_partition_checks": partition_metric,
        "truncated_one_coordinate_mass_checks": one_coordinate_metric,
        "truncated_tuple_weighted_mass_checks": tuple_mass_metric,
        "nonuniform_square_root_majorant_checks": majorant_metric,
        "exact_parameter_and_log_range_checks": parameter_metric,
        **parameter_data,
        "logarithmic_modular_law_certified_by_script": False,
        "chernoff_path_tube_certified_by_script": False,
        "multiplicative_endpoint_asymptotics_certified_by_script": False,
        "harmonic_progression_estimates_certified_by_script": False,
        "uniform_cn_analytic_bound_certified_by_script": False,
        "first_passage_event_chain_certified_by_script": False,
        "proposition_1_9_reproved_by_this_script": False,
        "proposition_1_14_reproved_by_this_script": False,
        "proposition_1_11_certified_by_script": False,
        "theorem_1_6_certified_by_script": False,
        "theorem_1_3_certified_by_script": False,
        "natural_density_claimed": False,
        "convergence_to_one_claimed": False,
    }
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
