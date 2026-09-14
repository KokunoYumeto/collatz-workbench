"""Finite exact checks for the Krasikov--Lagarias 2003 intake.

The companion audit reconstructs the published difference-inequality proof
chain and proves the exact shortened/unshortened clock morphism.  This script
pins the published scan, the arXiv v1 source manifestations, F029, and the
immutable routing artifacts.  It checks exact source signatures, the
published page count, the rational exponent comparison, and bounded instances
of the clock embedding, its omitted intermediate states, target-one
reachability, and the cycle-target transfer.

It does not certify the unprinted k=11 feasible vector, independently prove
Krasikov--Lagarias Theorem 2.2 or 6.1, prove an infinite-density statement,
or prove the Collatz conjecture.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHELF = Path(
    r"C:\Users\LOCAL_USER\Documents\arxiv_latex\library\collatz_reconstruction"
)
SOURCE_TEX = SHELF / "latex" / "math.0205002v1" / "30apr02.tex"
SOURCE_ARCHIVE = SHELF / "source" / "math.0205002v1.eprint"
PUBLISHED_PDF = (
    SHELF
    / "published"
    / "Krasikov-Lagarias-2003-Bounds-difference-inequalities.pdf"
)
F029 = ROOT / "qa" / "KRASIKOV-LAGARIAS-2003-F029-difference-inequality-audit.md"

PINNED = {
    SOURCE_TEX: (
        69_729,
        "04fa4d484fe89256f6771f5651338891219385f6e049ffaf41035541016232cd",
    ),
    SOURCE_ARCHIVE: (
        26_236,
        "c35de018067ae838c17b647f0ce0354141a8bcfaa45b4966be2bb9a380252951",
    ),
    PUBLISHED_PDF: (
        217_588,
        "8433f68c6f04a008b7c1af4d2b11ee1007a74f987da56a658d8fa331b32eff9c",
    ),
    F029: (
        18_261,
        "7bc00b095f99f55ae94f226a5b865223ecc2de030501536e1d26d2f71f01d187",
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


def require_fragment(lines: list[str], number: int, fragment: str) -> None:
    actual = lines[number - 1]
    assert fragment in actual, (number, fragment, actual)


def shortened_t(n: int) -> int:
    assert n > 0
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def unshortened_u(n: int) -> int:
    assert n > 0
    return n // 2 if n % 2 == 0 else 3 * n + 1


def iterate_t(n: int, steps: int) -> int:
    for _ in range(steps):
        n = shortened_t(n)
    return n


def main() -> None:
    for path, (expected_bytes, expected_hash) in PINNED.items():
        assert path.stat().st_size == expected_bytes, path
        assert sha256(path) == expected_hash, path

    source_lines = SOURCE_TEX.read_text(encoding="latin-1").splitlines()
    assert len(source_lines) == 1900

    source_signatures = {
        179: r"Bounds for the $3x+1$ Problem using Difference Inequalities",
        196: r"(April 30, 2002)",
        243: r"$T(n) = n/2$ if $n$ is an even integer, $(3n+1)/2$",
        371: r"\pi_a (x) :=  \#\{n: 1 \le n \le x",
        375: r"\pi_a^*(x) := \# \{n: n \le x",
        382: r"a \equiv m~(\bmod~3^j)",
        386: r"some $a \equiv m~(\bmod~3^k)$",
        394: r"$$ \phi_k^m(y) \ge 1.$$",
        404: r"\phi_{k-1}^m(y) = \min[ \phi_k^m(y)",
        410: r"\phi_k^m(y) = \phi_k^{2m}(y - 1)",
        412: r"for $y \equiv ~2(\bmod~3).$",
        416: r"[3^k] := \{ m~(\bmod~3^k):~ m \equiv 2",
        435: r"\phi_k^m(y) \ge \phi_k^{4m}(y-2)",
        440: r"\phi_k^m(y) \ge \phi_k^{4m}(y-2).",
        445: r"\phi_k^m(y) \ge \phi_k^{4m}(y-2)",
        532: r"c_{k-1}^m & \le & c_k^{m+3^k}",
        534: r"c_{k-1}^m & \le & c_k^{m+2 \cdot 3^k}",
        560: r"m + 3^{k-1}",
        584: r"\begin{theorem}~\label{th21}",
        590: r"\phi_k^m(y) \ge \Delta_1 \cdot c_k^m \lambda^y",
        594: r"\Delta_1 := \frac{1}",
        828: r"\beta_1 > \beta_2 > \beta_3 > \cdots",
        843: r"\delta = \beta_2 - \beta_1 > 0",
        847: r"\beta_j = \beta_1 + (j-1) \delta",
        848: r"\beta_j < 0$ for sufficiently large $j$",
        1201: r"\begin{theorem}\label{th41}",
        1335: r"\begin{theorem}\label{th51}",
        1352: r"\Delta := \la^{-\nu}",
        1376: r"y \in [0, \bv]",
        1436: r"holds for all $k \in [3^m]$",
        1463: r"\phi_k^m (y) \ge \Delta c_m^k \la^y",
        1517: r"For each positive $a \not\equiv 0",
        1518: r"T^{(j}(n) = a",
        1520: r"\pi_a(x) \ge x^{0.84}",
        1527: r"\lambda = 1.7922310",
        1529: r"\gamma = \log_2 \lambda \approx 0.84175",
        1575: r"11 & 0.8417560 & 1.7922310 & 98.4009647",
        1619: r"satisfy $\lambda_{k} \le \lambda_{k+1},$",
        1625: r"show that the values $\lambda_k$ are strictly increasing",
        1731: r"\section*{Appendix:  Inequalities for $k=2$}",
    }
    for number, fragment in source_signatures.items():
        require_fragment(source_lines, number, fragment)

    info = subprocess.run(
        ["pdfinfo", str(PUBLISHED_PDF)],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    ).stdout
    page_match = re.search(r"(?m)^Pages:\s+(\d+)\s*$", info)
    assert page_match is not None
    assert int(page_match.group(1)) == 22

    exponent_margin = 1_792_231**25 - 2**21 * 10**150
    expected_margin = int(
        "648178083018818411714642008170663937814358542678770282183616"
        "501865598105365875101282794946841201725532580228256170356677"
        "43037735765387257538455190506275751"
    )
    assert exponent_margin == expected_margin
    assert exponent_margin > 0

    initial_values = 10_000
    shortened_steps = 200
    embedding_checks = 0
    omitted_intermediate_checks = 0
    bounded_target_one_checks = 0
    bounded_reaching_one = 0

    for initial in range(1, initial_values + 1):
        t_state = initial
        u_state = initial
        shortened_hit_one = False
        unshortened_hit_one = False

        for _ in range(shortened_steps + 1):
            assert t_state == u_state
            embedding_checks += 1
            shortened_hit_one |= t_state == 1
            unshortened_hit_one |= u_state == 1

            if t_state % 2:
                intermediate = unshortened_u(u_state)
                assert intermediate == 3 * t_state + 1
                assert intermediate >= 4
                assert intermediate != 1
                omitted_intermediate_checks += 1
                unshortened_hit_one |= intermediate == 1
                u_state = unshortened_u(intermediate)
            else:
                u_state = unshortened_u(u_state)
            t_state = shortened_t(t_state)

        assert shortened_hit_one == unshortened_hit_one
        bounded_target_one_checks += 1
        bounded_reaching_one += int(shortened_hit_one)

    cycle_transfer_checks = 0
    for target, cycle_maximum in ((1, 2), (2, 2)):
        for r in range(1, 21):
            lifted_target = 2**r * target
            assert iterate_t(lifted_target, r) == target
            if lifted_target > cycle_maximum:
                assert lifted_target not in (1, 2)
            cycle_transfer_checks += 1

    f029_text = F029.read_text(encoding="utf-8")
    f029_signatures = (
        "Theorem 6.1 is recorded as a published computer-assisted theorem.",
        "Reproducibility of the \\(k=11\\) feasibility premise remains open.",
        "This supplies the omitted cycle-target handoff",
        "singleton fibres on its image, diagonal kernel pair",
        "it cannot lose",
        "the Collatz conjecture;",
    )
    for signature in f029_signatures:
        assert signature in f029_text, signature

    result = {
        "status": "PASS",
        "pinned_artifacts": len(PINNED),
        "source_lines": len(source_lines),
        "source_signature_checks": len(source_signatures),
        "published_pdf_pages": 22,
        "exact_exponent_margin": exponent_margin,
        "exact_exponent_consequence": "log_2(1.7922310)>21/25",
        "clock_embedding_initial_values": initial_values,
        "clock_embedding_shortened_steps_each": shortened_steps,
        "clock_embedding_checks": embedding_checks,
        "omitted_intermediate_checks": omitted_intermediate_checks,
        "bounded_target_one_equivalence_checks": bounded_target_one_checks,
        "bounded_initial_values_reaching_one_within_horizon": bounded_reaching_one,
        "cycle_target_lift_checks": cycle_transfer_checks,
        "f029_signature_checks": len(f029_signatures),
        "explicitly_not_certified": [
            "the unprinted k=11 feasible coordinate vector",
            "feasibility of L_11^NT(1.7922310)",
            "Krasikov--Lagarias Theorem 2.2",
            "Krasikov--Lagarias Theorem 6.1 independently of its publication",
            "any infinite-density statement",
            "the Collatz conjecture",
        ],
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
