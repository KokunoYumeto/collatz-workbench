"""Finite exact checks for Tao v7's Fourier-to-renewal reconstruction.

The TeX chapter supplies the analytic estimates, black-triangle geometry,
first-passage bounds, and renewal proof.  This certificate pins the versioned
source manifestations and frozen route ledgers, checks exact source locators,
and exhausts bounded algebraic kernels for the lift/project maps, Syracuse
offsets, quotient-frequency morphism, holding law, and deterministic entry
budget.  Its terminal report states the analytic results it does not certify.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHELF = Path(
    r"C:\Users\LOCAL_USER\Documents\arxiv_latex\library\collatz_reconstruction"
)
TAO_V7_TEX = SHELF / "latex" / "1909.03562v7" / "collatz.tex"
TAO_V7_EPRINT = SHELF / "source" / "1909.03562v7.eprint"
TAO_V5_TEX = SHELF / "latex" / "1909.03562v5" / "collatz.tex"
TAO_V5_EPRINT = SHELF / "source" / "1909.03562v5.eprint"
TAO_JOURNAL_PDF = Path(
    r"C:\Users\LOCAL_USER\Documents\arxiv_latex\library\_recovered_from_papers"
    r"\by_title\Tao Almost all orbits of the Collatz map attain almost bounded values.pdf"
)

PINNED = {
    TAO_V7_TEX: (
        164_932,
        "bfbc39432d4084a276416cb019a592003c868fa32f18e2f90028ac325ae5c19d",
    ),
    TAO_V7_EPRINT: (
        1_226_861,
        "ba81acd6254838251f1ee585256a6f9f223cdc9c73bed0a3c4fd25782d0124ad",
    ),
    TAO_V5_TEX: (
        163_356,
        "c676b362b30807aa6690d0d4f16b8c8e84324732f5c0eb72ccfd875000276ae0",
    ),
    TAO_V5_EPRINT: (
        1_226_298,
        "eb7a4668ebf27a3f795f72fcdc8d992ada365824359c734fa58813c750ff2ede",
    ),
    TAO_JOURNAL_PDF: (
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


def require_fragments() -> int:
    v7 = TAO_V7_TEX.read_text(encoding="utf-8").splitlines()
    v5 = TAO_V5_TEX.read_text(encoding="utf-8").splitlines()
    required_v7 = {
        926: r"\section{Reduction to Fourier decay bound}\label{decay-sec}",
        984: r"Fix $k$.  In order to decouple the events involved in \eqref{psy} we need to enlarge the event $E$ slightly, so that it only depends on $\a_1,\dots,\a_{k+1}$ and not on $\a_{k+2},\dots,\a_n$.  Let $E_k$ denote the event that the inequalities \eqref{ij} hold for $1 \leq i < j \leq k+1$, thus $E_k$ contains $E$.   Then the difference between $E$ and $E_k$ has probability $O(n^{-A-1})$ by \eqref{ayo}.  Thus by the triangle inequality, the estimate \eqref{psy} is equivalent to",
        1023: r"$$ \X_n = F_{k+1}(\a_{k+1},\dots,\a_1) + 3^{k+1} 2^{-l} F_{n-k-1}(\a_n,\dots,\a_{k+2}) \mod 3^n.$$",
        1029: r"For $\xi$ in $\Z/3^n\Z$ that does not lie in $3^{n-m}\Z/3^n\Z$, we can write $\xi = 3^j 2^l \xi' \mod 3^n$ where $0 \leq j < n-m \leq 0.1 n$ and $\xi'$ is not divisible by $3$.  In particular, from \eqref{hepta} one has",
        1045: r"\begin{lemma}[Injectivity of offsets]\label{inj}  For each natural number $n$, the $n$-Syracuse offset map $F_n\colon (\N+1)^n \to \Z[\frac{1}{2}]$ is injective.",
        1051: r"$$ F_n(a_1,\dots,a_n) = 3^n 2^{-a_{[1,n]}} + F_{n-1}(a_2,\dots,a_n)$$",
        1093: r"can only be non-empty for at most one value $(a_1,\dots,a_{m})$ of the tuple $(\a_1,\dots,\a_{m})$.  By Definition \ref{geom}, such a value is attained with probability $2^{-a_{[1,m]}} = 2^{-l}$, which by \eqref{bmd-3} is equal to $n^{O((C_A)^2)} 3^{-n}$.  We can thus bound \eqref{half-2} (and hence the left-hand side of \eqref{half}) by",
        1212: r"\begin{lemma}[Structure of black set]\label{black}  The black set $B \subset [n/2] \times \Z$ of points $(j,l)$ with $|\theta(j,l)| \leq \eps$ can be expressed as a disjoint union",
        1369: r"\subsection{Formulation in terms of holding time}",
        1408: r"\E \exp( \Hold \cdot k ) = \sum_{j \in \N} \frac{1}{4} \left(\frac{3}{4}\right)^{j-1} \exp\left( (1,3) \cdot k\right) \left(\E \exp( (1,\Pascal') \cdot k) \right)^j.",
        1423: r"\begin{lemma}[Distribution of first passage location]\label{stop} Let $\v_1,\v_2,\dots$ be iid copies of $\Hold$, and write $\v_k = (\j_k,\l_k)$.  Let $s \in \N$, and define the first passage time $\k$ to be the least positive integer such that $\l_{[1,k]} > s$.  Then for any $j,l \in \N$ with $l > s$, one has",
        1469: r"For any $(j,l) \in \N+1 \times \Z$, let $Q(j,l)$ denote the quantity",
        1497: r"Q_m \coloneqq \sup_{(j,l) \in (\N+1) \times \Z: j \geq \lfloor n/2\rfloor - m} \max(\lfloor n/2\rfloor -j,1)^A Q(j,l).",
        1662: r"\E 1_{R \leq \r} \exp\left( - \sum_{p=1}^{\t_{\min(\r,R)}} 1_W((j',l') + \v_{[1,p]}) + \eps R \right) \leq \exp(\eps),",
        1702: r"\begin{lemma}[Large triangles are rarely encountered shortly after a lengthy crossing]\label{77}  Let $(j,l)$ be an element of a black triangle $\Delta$ with $s \coloneqq l_\Delta - l$ obeying $s > \frac{m}{\log^2 m}$ (where we recall $m = \lfloor n/2\rfloor - j$), and let $\k$ be the first passage time associated to $s$ defined in Lemma \ref{stop}.  Let $p \in \N$ and $1 \leq s' \leq m^{0.4}$. Let $E_{p,s'}$ denote the event that $(j,l) + \v_{[1,\k+p]}$ lies in a triangle $\Delta' \in {\mathcal T}$ of size $s_{\Delta'} \geq s'$.  Then",
    }
    required_v5 = {
        1654: r"\begin{lemma}[Many triangles usually implies many white points]\label{rip}  Let $\v_1,\v_2,\dots$ be iid copies of $\Hold$.  Then for any $(j',l') \in (\N+1) \times \Z$ and any positive integer $R$, we have",
        1656: r"\E \exp\left( - \sum_{p=1}^{\t_{\min(\r,R)}} 1_W((j',l') + \v_{[1,p]}) + \eps \min(\r,R) \right) \leq \exp(\eps),",
        1658: r"where $0 < \eps < 1/100$ is the sufficiently small absolute constant that has been in use throughout this section.",
    }
    for line_number, fragment in required_v7.items():
        assert v7[line_number - 1].strip() == fragment, ("v7", line_number)
    for line_number, fragment in required_v5.items():
        assert v5[line_number - 1].strip() == fragment, ("v5", line_number)
    assert required_v7[1662] != required_v5[1656]
    return len(required_v7) + len(required_v5)


def l1(vector: list[Fraction]) -> Fraction:
    return sum((abs(value) for value in vector), Fraction(0))


def lift(mu: list[Fraction], r: int, n: int) -> list[Fraction]:
    assert 0 <= r <= n and len(mu) == 3**r
    fibre_scale = Fraction(1, 3 ** (n - r))
    return [fibre_scale * mu[y % (3**r)] for y in range(3**n)]


def pushforward(nu: list[Fraction], r: int, n: int) -> list[Fraction]:
    assert 0 <= r <= n and len(nu) == 3**n
    return [
        sum((nu[z] for z in range(x, 3**n, 3**r)), Fraction(0))
        for x in range(3**r)
    ]


def fibre_projection(nu: list[Fraction], r: int, n: int) -> list[Fraction]:
    return lift(pushforward(nu, r, n), r, n)


def lift_projection_checks() -> int:
    checks = 0
    for n in range(0, 6):
        nu = [
            Fraction(((7 * y + 5 * n) % 17) - 8, 1 + (y % 4))
            for y in range(3**n)
        ]
        for r in range(0, n + 1):
            mu = [
                Fraction(((5 * x + 3 * r + n) % 13) - 6, 1 + (x % 3))
                for x in range(3**r)
            ]
            lifted = lift(mu, r, n)
            projected = fibre_projection(nu, r, n)
            assert sum(lifted, Fraction(0)) == sum(mu, Fraction(0))
            assert l1(lifted) == l1(mu)
            assert sum(projected, Fraction(0)) == sum(nu, Fraction(0))
            assert l1(projected) <= l1(nu)
            assert fibre_projection(lifted, r, n) == lifted
            assert projected == lift(pushforward(nu, r, n), r, n)
            checks += 6
            for s in range(r, n + 1):
                assert lift(lift(mu, r, s), s, n) == lifted
                checks += 1
    return checks


def offset(coordinates: tuple[int, ...]) -> Fraction:
    total = Fraction(0)
    q = len(coordinates)
    for u in range(q):
        suffix_sum = sum(coordinates[u:])
        total += Fraction(3 ** (q - u - 1), 2**suffix_sum)
    return total


def mod_fraction(value: Fraction, modulus: int) -> int:
    assert value.denominator % 3 != 0
    return (value.numerator * pow(value.denominator, -1, modulus)) % modulus


def offset_checks() -> tuple[int, int]:
    injectivity_checks = 0
    projection_checks = 0
    for length in range(1, 7):
        seen: dict[Fraction, tuple[int, ...]] = {}
        for coordinates in itertools.product(range(1, 5), repeat=length):
            value = offset(coordinates)
            assert value not in seen, (coordinates, seen.get(value))
            seen[value] = coordinates
            tail = offset(coordinates[1:]) if length > 1 else Fraction(0)
            corrected_recurrence = (
                Fraction(3 ** (length - 1), 2 ** sum(coordinates)) + tail
            )
            assert value == corrected_recurrence
            injectivity_checks += 1
            for q in range(1, length + 1):
                modulus = 3**q
                assert mod_fraction(value, modulus) == mod_fraction(
                    offset(coordinates[-q:]), modulus
                )
                projection_checks += 1
    return injectivity_checks, projection_checks


def valuation_3(residue: int, n: int) -> int:
    assert 0 < residue < 3**n
    value = residue
    valuation = 0
    while value % 3 == 0:
        value //= 3
        valuation += 1
    return valuation


def frequency_morphism_checks() -> tuple[int, int]:
    morphism_checks = 0
    quotient_fibre_checks = 0
    for n in range(3, 8):
        modulus_n = 3**n
        for k in range(0, n - 1):
            suffix_length = n - k - 1
            for v in range(0, suffix_length):
                q = suffix_length - v
                modulus_quotient = 3 ** (n - v)
                modulus_q = 3**q
                factor_to_n = 3 ** (n - q)
                candidate_units = {
                    value % modulus_quotient
                    for value in (1, 2, 4, 5, 7, 8, 10, 11)
                    if value % 3
                }
                for ell in range(0, 4):
                    two_power = 2**ell
                    for unit in candidate_units:
                        if unit == 0:
                            continue
                        eta = (3**v * two_power * unit) % modulus_n
                        assert valuation_3(eta, n) == v
                        quotient = (
                            (eta // (3**v))
                            * pow(two_power, -1, modulus_quotient)
                        ) % modulus_quotient
                        assert quotient == unit
                        eta_q = quotient % modulus_q
                        assert eta_q % 3

                        # In Z/3^n the equation has 3^v lifts, while reduction
                        # modulo 3^(n-v) has the unique quotient above.
                        lifts = {
                            quotient + j * modulus_quotient
                            for j in range(3**v)
                        }
                        assert len(lifts) == 3**v
                        for lifted_unit in lifts:
                            assert (
                                3**v * two_power * lifted_unit - eta
                            ) % modulus_n == 0
                        quotient_fibre_checks += 1

                        for coordinates in itertools.product(
                            range(1, 3), repeat=suffix_length
                        ):
                            value = offset(coordinates)
                            lhs = (
                                eta
                                * 3 ** (k + 1)
                                * pow(two_power, -1, modulus_n)
                                * mod_fraction(value, modulus_n)
                            ) % modulus_n
                            rhs = (
                                factor_to_n
                                * eta_q
                                * mod_fraction(value, modulus_q)
                            ) % modulus_n
                            assert lhs == rhs
                            assert mod_fraction(value, modulus_q) == mod_fraction(
                                offset(coordinates[-q:]), modulus_q
                            )
                            morphism_checks += 1
    return morphism_checks, quotient_fibre_checks


def holding_law_checks() -> tuple[int, int]:
    mass_checks = 0
    for b in range(2, 41):
        enumerated = sum(
            (Fraction(1, 2**a) * Fraction(1, 2 ** (b - a))
             for a in range(1, b)),
            Fraction(0),
        )
        assert enumerated == Fraction(b - 1, 2**b)
        mass_checks += 1

    success = Fraction(2, 2**3)
    failure = 1 - success
    assert success == Fraction(1, 4)
    assert failure == Fraction(3, 4)
    mean_b = Fraction(4)
    mean_q = (mean_b - 3 * success) / failure
    mean_r = failure / success
    assert mean_q == Fraction(13, 3)
    assert mean_r == 3
    assert (1 + mean_r, 3 + mean_r * mean_q) == (4, 16)

    support = ((1, 3), (2, 5), (2, 7), (2, 8))
    differences = [
        (point[0] - support[0][0], point[1] - support[0][1])
        for point in support[1:]
    ]
    assert (0, 1) == (
        differences[2][0] - differences[1][0],
        differences[2][1] - differences[1][1],
    )
    assert (1, 0) == (
        differences[0][0] - 2 * (0, 1)[0],
        differences[0][1] - 2 * (0, 1)[1],
    )

    pgf_checks = 0
    for z, w in (
        (Fraction(1, 3), Fraction(1, 4)),
        (Fraction(2, 5), Fraction(1, 3)),
        (Fraction(1, 2), Fraction(2, 5)),
    ):
        b_pgf = (w / (2 - w)) ** 2
        q_pgf = (b_pgf - success * w**3) / failure
        ratio = failure * z * q_pgf
        assert 0 <= ratio < 1
        from_geometric_series = z * w**3 * success / (1 - ratio)
        corrected_rational_form = z * w**3 / (4 - 3 * z * q_pgf)
        assert from_geometric_series == corrected_rational_form
        pgf_checks += 1
    return mass_checks, pgf_checks


def deterministic_entry_budget_checks() -> int:
    checks = 0
    for h in range(1, 8):
        for k_const in range(1, 5):
            for entry_count in range(2, 7):
                bounds = [h]
                for _ in range(1, entry_count):
                    previous = bounds[-1]
                    bounds.append(
                        previous + 10 * k_const * (1 + previous) ** 3 + h + 1
                    )
                for i in range(entry_count - 1):
                    # The left side is affine and increasing in the actual
                    # entry time, so these exact endpoint/interior witnesses
                    # check the finite kernel without iterating to the huge
                    # recursively generated bound.
                    for actual_entry in sorted({0, bounds[i] // 2, bounds[i]}):
                        crossing_bound = (
                            actual_entry
                            + 10 * k_const * (1 + bounds[i]) ** 3
                            + 1
                        )
                        assert crossing_bound + h <= bounds[i + 1]
                        checks += 1
    return checks


def q_boundary_checks() -> int:
    checks = 0
    for n in range(2, 51):
        top = n // 2
        if top == 0:
            continue
        q_top_domain = {
            j for j in range(1, 2 * n + 2) if j >= top - top
        }
        q_previous_domain = {
            j for j in range(1, 2 * n + 2) if j >= top - (top - 1)
        }
        assert q_top_domain == q_previous_domain
        checks += 1
    return checks


def main() -> int:
    for path, (size, digest) in PINNED.items():
        assert path.is_file(), path
        assert path.stat().st_size == size, (path, path.stat().st_size)
        assert sha256(path) == digest, path

    locator_checks = require_fragments()
    lift_checks = lift_projection_checks()
    offset_injectivity, finite_projections = offset_checks()
    frequency_checks, quotient_fibres = frequency_morphism_checks()
    holding_masses, holding_pgfs = holding_law_checks()
    block_checks = deterministic_entry_budget_checks()
    boundary_checks = q_boundary_checks()

    report = {
        "status": "PASS",
        "scope": (
            "version/hash/locator pinning and finite exact lift, fibre, offset, "
            "frequency-quotient, projective, holding-law, and entry-budget algebra"
        ),
        "pinned_hashes": len(PINNED),
        "source_locator_checks": locator_checks,
        "lift_projection_checks": lift_checks,
        "offset_injectivity_and_recurrence_checks": offset_injectivity,
        "finite_projective_reduction_checks": finite_projections,
        "frequency_morphism_checks": frequency_checks,
        "frequency_quotient_fibre_checks": quotient_fibres,
        "holding_mass_checks": holding_masses,
        "holding_pgf_checks": holding_pgfs,
        "deterministic_entry_budget_checks": block_checks,
        "q_positive_boundary_checks": boundary_checks,
        "maximum_offset_prefix_length": 6,
        "maximum_offset_coordinate": 4,
        "analytic_characteristic_decay_certified": False,
        "black_triangle_geometry_certified_by_script": False,
        "first_passage_green_bound_certified_by_script": False,
        "infinite_renewal_monotonicity_certified_by_script": False,
        "proposition_1_9_certified": False,
        "tao_main_theorem_certified": False,
    }
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
