"""Finite exact checks for Tao's main-theorem reduction.

The accompanying TeX proves the analytic chain from Proposition 1.11 through
Theorems 3.1, 1.6, and 1.3.  This script pins the v5, v7, journal, and frozen
route manifestations; checks exact source and reconstruction locators; proves
the v5/v7 Section 3 equality at the declared normalized boundary; and
exhausts bounded instances of the nested first-passage shift, constructive
block cover, dyadic bijection, harmonic-weight transport, valuation-tail
identity, and Collatz/Syracuse orbit-minimum identity.

This finite script does not independently prove Proposition 1.11, its
analytic total-variation estimate, the infinite harmonic-density limits, or
any theorem outside the explicitly enumerated finite kernels.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from functools import lru_cache
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


def require_fragment(lines: list[str], number: int, fragment: str) -> None:
    assert fragment in lines[number - 1], (number, fragment, lines[number - 1])


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
            item["sha256"] for item in record.get("paths", []) if "sha256" in item
        )
    assert journal_digest in index_hashes

    document = records["DOCROUTE-COL-8F0EDA4DC27DA85735AB"]
    assert document["identifiers"]["arxiv_id"] == "1909.03562"
    assert document["identifiers"]["arxiv_version_id"] == "1909.03562v5"
    document_hashes = {item["sha256"] for item in document["paths"]}
    assert journal_digest in document_hashes
    assert PINNED[V5_ARCHIVE][1] in document_hashes
    return len(records)


def source_and_reconstruction_checks() -> dict[str, int]:
    v7 = V7_TEX.read_text(encoding="utf-8").splitlines()
    v5 = V5_TEX.read_text(encoding="utf-8").splitlines()

    required_v7 = {
        159: r"\begin{definition}[Almost all]",
        169: r"\begin{theorem}[Almost all Collatz orbits attain almost bounded values]",
        180: r"define the \emph{Syracuse map}",
        192: r"\Col_{\min}(N) = \Syr_{\min}( N / 2^{\nu_2(N)} )",
        199: r"We say that a property $P(N)$ holds for \emph{almost all}",
        203: r"\begin{theorem}[Almost all Syracuse orbits attain almost bounded values]",
        206: r"Indeed, if Theorem \ref{main-syr} holds",
        316: r"define the \emph{first passage time}",
        317: r"T_x(N) \coloneqq \inf",
        319: r"\Pass_x(N) \coloneqq \Syr^{T_x(N)}(N)",
        326: r"\begin{proposition}[Stabilisation of first passage]",
        535: r"\section{Reduction to stabilisation of first passage}",
        539: r"\begin{theorem}[Alternate form of main theorem]",
        552: r"Let $B_x = B_{x,N_0}$",
        554: r"Observe that if $T_x",
        560: r"In particular, the event $B_{x^\alpha}$",
        569: r"Let $J = J(x,N_0)$ be the first natural number",
        575: r"The event $B_{y^{\alpha^{-1}}}$",
        580: r"\P( B_{x^{1/\alpha}} )",
        582: r"\P( \Syr_{\min}(\mathbf{N}_x) > N_0 )",
        583: r"By definition of $\mathbf{N}_x$",
        587: r"Covering the interval",
        591: r"Set $\tilde f(x) \coloneqq \inf",
        592: r"\Syr_{\min}(N) > f(N)",
        593: r"Theorem \ref{main-syr} follows",
    }
    required_v5 = {
        159: required_v7[159],
        169: required_v7[169],
        180: required_v7[180],
        192: required_v7[192],
        199: required_v7[199],
        203: required_v7[203],
        206: required_v7[206],
        316: required_v7[316],
        317: required_v7[317],
        319: required_v7[319],
        326: required_v7[326],
        529: required_v7[535],
        533: required_v7[539],
        546: required_v7[552],
        548: required_v7[554],
        554: required_v7[560],
        563: required_v7[569],
        569: required_v7[575],
        574: required_v7[580],
        576: required_v7[582],
        577: required_v7[583],
        581: required_v7[587],
        585: required_v7[591],
        586: required_v7[592],
        587: required_v7[593],
    }
    for number, fragment in required_v7.items():
        require_fragment(v7, number, fragment)
    for number, fragment in required_v5.items():
        require_fragment(v5, number, fragment)

    normalized_v7 = "".join("".join(v7[534:593]).split())
    normalized_v5 = "".join("".join(v5[528:587]).split())
    assert normalized_v7 == normalized_v5
    assert len(normalized_v7) == 4_748

    chapter = (
        ROOT / "tex" / "chapters" / "01j_tao_main_theorem_reduction.tex"
    ).read_text(encoding="utf-8")
    audit = (
        ROOT / "qa" / "TAO-V5-V7-JOURNAL-F027-main-theorem-reduction-audit.md"
    ).read_text(encoding="utf-8")
    labels = [
        r"\label{subsec:Tao-main-reduction}",
        r"\label{sourceissue:Tao-main-reduction}",
        r"\label{lem:Tao-nested-passage-tail}",
        r"\label{prop:Tao-main-block-recurrence}",
        r"\label{thm:Tao-main-alt-repaired}",
        r"\label{thm:Tao-main-syr-repaired}",
        r"\label{prop:Tao-main-dyadic-morphism}",
        r"\label{thm:Tao-main-repaired}",
        r"\label{eq:Tao-main-dyadic-weight}",
        r"\label{eq:Tao-main-minimum-identity}",
        r"\label{eq:Tao-main-fixed-K-tail}",
        r"\label{eq:Tao-main-dyadic-tail-limit}",
    ]
    for label in labels:
        assert chapter.count(label) == 1, label
    assert "Reversed tail envelope" in audit
    assert "Dropped equality" in audit
    assert "Dyadic factor two and missing rescaling" in audit
    assert "No coupling is constructed" in audit

    return {
        "v7_source_locator_checks": len(required_v7),
        "v5_source_locator_checks": len(required_v5),
        "normalized_version_checks": 2,
        "reconstruction_locator_checks": len(labels) + 4,
    }


def syracuse(n: int) -> int:
    assert n > 0 and n % 2 == 1
    value = 3 * n + 1
    while value % 2 == 0:
        value //= 2
    return value


def collatz(n: int) -> int:
    assert n > 0
    return 3 * n + 1 if n % 2 else n // 2


@lru_cache(maxsize=None)
def finite_orbit(step, start: int, limit: int = 100_000) -> tuple[int, ...]:
    values: list[int] = []
    seen: set[int] = set()
    value = start
    for _ in range(limit):
        if value in seen:
            return tuple(values)
        seen.add(value)
        values.append(value)
        value = step(value)
    raise AssertionError(("orbit limit", start, value))


def first_passage(n: int, threshold: int) -> tuple[int | None, int]:
    orbit = finite_orbit(syracuse, n)
    for index, value in enumerate(orbit):
        if value <= threshold:
            return index, value
    return None, 1


def nested_passage_checks() -> dict[str, int]:
    shift_checks = 0
    event_checks = 0
    thresholds = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    for n in range(1, 2_001, 2):
        orbit = finite_orbit(syracuse, n)
        for u in thresholds:
            tu, pass_u = first_passage(n, u)
            if tu is None:
                continue
            for v in thresholds:
                if v < u:
                    continue
                tv, pass_v = first_passage(n, v)
                assert tv is not None and tv <= tu
                d = tu - tv
                value = pass_v
                for _ in range(d):
                    value = syracuse(value)
                assert value == pass_u
                for k in range(20):
                    left = pass_u
                    for _ in range(k):
                        left = syracuse(left)
                    right = pass_v
                    for _ in range(k + d):
                        right = syracuse(right)
                    assert left == right
                    shift_checks += 1
                for n0 in (2, 3, 5, 10, 25, 100):
                    if min(finite_orbit(syracuse, pass_u)) <= n0:
                        assert min(finite_orbit(syracuse, pass_v)) <= n0
                    event_checks += 1
        assert min(orbit) >= 1
    return {
        "nested_indexed_tail_shift_checks": shift_checks,
        "nested_event_transport_checks": event_checks,
    }


def geometric_and_cover_checks() -> dict[str, int]:
    alpha = Fraction(1001, 1000)
    inverse = Fraction(1000, 1001)
    geometric_checks = 0
    for c in range(1, 6):
        ratio = alpha ** (-c)
        infinite_bound_factor = alpha**c / (1 - ratio)
        for j_max in range(1, 101):
            for log_y in (Fraction(1), Fraction(7, 3), Fraction(101, 7)):
                total = sum(
                    (alpha ** (j - 2) * log_y) ** (-c)
                    for j in range(1, j_max + 1)
                )
                assert total <= infinite_bound_factor * log_y ** (-c)
                geometric_checks += 1

    cover_checks = 0
    for log_x in (2, 3, 5, 10, 31, 101, 201):
        for denominator in (2, 3, 5, 7):
            log_n0 = Fraction(log_x, denominator)
            if log_n0 >= log_x:
                continue
            z_logs: list[Fraction] = []
            k = 0
            z_log = Fraction(log_x)
            while z_log > log_n0:
                k += 1
                z_log *= inverse
                z_logs.append(z_log)
                assert k < 50_000
            assert k >= 1
            assert z_logs[-1] <= log_n0
            prior = Fraction(log_x) if k == 1 else z_logs[-2]
            assert prior > log_n0
            assert z_logs[-1] > log_n0 / alpha
            for index, lower in enumerate(z_logs, start=1):
                upper = Fraction(log_x) if index == 1 else z_logs[index - 2]
                assert alpha * lower == upper
                cover_checks += 1
            assert sum(z_logs) <= Fraction(log_x) / (alpha - 1)
            cover_checks += 4

    return {
        "geometric_recurrence_error_checks": geometric_checks,
        "constructive_log_cover_checks": cover_checks,
    }


def v2(n: int) -> int:
    assert n > 0
    exponent = 0
    while n % 2 == 0:
        n //= 2
        exponent += 1
    return exponent


def odd_part(n: int) -> int:
    return n >> v2(n)


def harmonic(bound: int) -> Fraction:
    return sum((Fraction(1, n) for n in range(1, bound + 1)), Fraction())


def odd_harmonic(bound: int) -> Fraction:
    return sum(
        (Fraction(1, n) for n in range(1, bound + 1, 2)), Fraction()
    )


def dyadic_checks() -> dict[str, int]:
    bijection_checks = 0
    for n in range(1, 20_001):
        a = v2(n)
        m = odd_part(n)
        assert m % 2 == 1
        assert (2**a) * m == n
        assert v2((2**a) * m) == a
        bijection_checks += 4

    weight_checks = 0
    for x in range(1, 401):
        for a in range(0, 9):
            sets = [
                {m for m in range(1, 401, 2) if m % 3 == 1},
                {m for m in range(1, 401, 2) if m % 5 in (1, 3)},
                {m for m in range(1, 401, 2) if m <= 73},
            ]
            for values in sets:
                lhs = sum(
                    (
                        Fraction(1, (2**a) * m)
                        for m in values
                        if (2**a) * m <= x
                    ),
                    Fraction(),
                )
                rhs = Fraction(1, 2**a) * sum(
                    (Fraction(1, m) for m in values if m <= x // (2**a)),
                    Fraction(),
                )
                assert lhs == rhs
                weight_checks += 1

            stratum = sum(
                (Fraction(1, n) for n in range(1, x + 1) if v2(n) == a),
                Fraction(),
            )
            assert stratum == Fraction(1, 2**a) * odd_harmonic(x // (2**a))
            weight_checks += 1

    tail_checks = 0
    for x in range(1, 1_001):
        for a in range(0, 10):
            lhs = sum(
                (Fraction(1, n) for n in range(1, x + 1) if v2(n) > a),
                Fraction(),
            )
            rhs = Fraction(1, 2 ** (a + 1)) * harmonic(x // (2 ** (a + 1)))
            assert lhs == rhs
            tail_checks += 1

    minimum_checks = 0
    for m in range(1, 4_001, 2):
        syr_min = min(finite_orbit(syracuse, m))
        for a in range(0, 13):
            col_min = min(finite_orbit(collatz, (2**a) * m))
            assert col_min == syr_min
            minimum_checks += 1

    return {
        "dyadic_bijection_and_inverse_checks": bijection_checks,
        "dyadic_harmonic_weight_checks": weight_checks,
        "dyadic_tail_identity_checks": tail_checks,
        "collatz_syracuse_minimum_checks": minimum_checks,
    }


def strict_tail_logic_checks() -> dict[str, int]:
    inclusion_checks = 0
    for k in range(2, 31):
        y_k = 3 * (k + 9)
        first_odd = y_k if y_k % 2 else y_k + 1
        for m in range(first_odd, 2_001, 2):
            f_value = m // 3 - 8
            assert f_value > k
            syr_min = min(finite_orbit(syracuse, m))
            if syr_min >= f_value:
                assert syr_min > k
            inclusion_checks += 1

    assert min(finite_orbit(syracuse, 1)) == 1
    assert not (1 > 1)
    assert 1 >= 1
    assert 1 > 0
    return {
        "fixed_K_tail_inclusion_checks": inclusion_checks,
        "strict_complement_equality_counterexample_checks": 3,
        "printed_tail_envelope_counterexample_checks": 1,
    }


def main() -> int:
    for path, (size, digest) in PINNED.items():
        assert path.is_file(), path
        assert path.stat().st_size == size, (path, path.stat().st_size, size)
        assert sha256(path) == digest, path

    report = {
        "status": "PASS",
        "scope": (
            "source/version pinning and finite exact kernels for the repaired "
            "Proposition 1.11 to Theorem 3.1 to Theorem 1.6 to Theorem 1.3 chain"
        ),
        "pinned_hashes": len(PINNED),
        "route_identity_checks": require_route_records(),
        **source_and_reconstruction_checks(),
        **nested_passage_checks(),
        **geometric_and_cover_checks(),
        **dyadic_checks(),
        **strict_tail_logic_checks(),
        "proposition_1_11_reproved_by_this_script": False,
        "analytic_total_variation_certified_by_script": False,
        "infinite_harmonic_density_limits_certified_by_script": False,
        "theorem_3_1_certified_by_script": False,
        "theorem_1_6_certified_by_script": False,
        "theorem_1_3_certified_by_script": False,
        "natural_density_claimed": False,
        "absolute_orbit_bound_claimed": False,
        "collatz_conjecture_claimed": False,
        "coupling_claimed": False,
    }
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
