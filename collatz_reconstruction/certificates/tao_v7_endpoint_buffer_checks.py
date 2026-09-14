"""Deterministic checks for the bounded Tao-v7 endpoint-buffer repair.

The TeX proof and TAO-V7-F001 audit prove the asymptotic implication.  This
certificate pins the controlling v7 source and frozen routes, checks the exact
source locators used by the repair, and verifies the rational exponent and
constant inequalities on which the asymptotic comparison rests.  It is not a
certificate for Proposition 5.2, Proposition 1.14, Theorem 1.3, or the
Fourier/renewal arguments that remain open in PO-COL-000001.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ARCHIVE = Path(
    r"C:\Users\LOCAL_USER\Documents\arxiv_latex\library\collatz_reconstruction"
    r"\source\1909.03562v7.eprint"
)
SOURCE_TEX = Path(
    r"C:\Users\LOCAL_USER\Documents\arxiv_latex\library\collatz_reconstruction"
    r"\latex\1909.03562v7\collatz.tex"
)
PINNED = {
    SOURCE_ARCHIVE: (
        1_226_861,
        "ba81acd6254838251f1ee585256a6f9f223cdc9c73bed0a3c4fd25782d0124ad",
    ),
    SOURCE_TEX: (
        164_932,
        "bfbc39432d4084a276416cb019a592003c868fa32f18e2f90028ac325ae5c19d",
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


def log_bounds(value: Fraction, terms: int = 30) -> tuple[Fraction, Fraction]:
    """Exact enclosure from log(value)=2*atanh((value-1)/(value+1))."""

    assert value > 1
    z = (value - 1) / (value + 1)
    partial = 2 * sum(
        (z ** (2 * j + 1) / (2 * j + 1) for j in range(terms + 1)),
        Fraction(0),
    )
    remainder_upper = (
        2
        * z ** (2 * terms + 3)
        / ((2 * terms + 3) * (1 - z * z))
    )
    return partial, partial + remainder_upper


def require_source_fragments(lines: list[str]) -> int:
    required = {
        718: r"I_y \coloneqq \left[\frac{\log( y / x )}{\log \frac{4}{3}} + \log^{0.8} x, \frac{\log( y^\alpha / x )}{\log \frac{4}{3}} - \log^{0.8} x\right],",
        756: r"T_x(\mathbf{N}_y) = \frac{\log( \mathbf{N}_y / x )}{\log \frac{4}{3}} + O( \log^{0.6} x);",
        759: r"$$ \mathbf{N}_y \subset [y + 2 \log^{0.8} x, y^\alpha - 2 \log^{0.8} x];$$",
        762: r"\P( T_x(\mathbf{N}_y) \in I_y) = 1 - O( \log^{-c} x ).",
        791: r"$$ \Syr^{n'}(\mathbf{N}_y) = \exp(O(\log^{0.6} x)) (4/3)^{n-m_0-n'} \Syr^{n-m_0}(\mathbf{N}_y) \geq \exp(O(\log^{0.6} x)) \Syr^{n-m_0}(\mathbf{N}_y) $$",
        820: r"Since $n \in I_y$, we conclude from \eqref{iy-def} that the right-hand side of \eqref{this} lies in $[y, y^\alpha]$; from \eqref{max}, \eqref{fn-def} we also see that this right-hand side is a odd integer.  Since $\mathbf{N}_y \equiv \Log( 2\N+1 \cap [y,y^\alpha] )$ and",
        842: r"$$ \# I_y = (1 + O( \log^{-c} x  )) \frac{\alpha-1}{\log \frac{4}{3}} \log y,$$",
        889: r"\sum_{M_0 \leq M \leq M_1: M = a \mod q} \frac{1}{M}  \ll \frac{1}{q} \log O \left( \frac{M_1}{M_0} \right).",
        922: r"Applying Proposition \ref{tv-bound}, Lemma \ref{loam} and the triangle inequality, one can thus write the preceding expression as",
    }
    for line_number, fragment in required.items():
        assert lines[line_number - 1].strip() == fragment, line_number
    return len(required)


def main() -> int:
    for path, (size, digest) in PINNED.items():
        assert path.is_file(), path
        assert path.stat().st_size == size, (path, path.stat().st_size)
        assert sha256(path) == digest, path

    source_lines = SOURCE_TEX.read_text(encoding="utf-8").splitlines()
    source_locator_checks = require_source_fragments(source_lines)

    alpha = Fraction(1001, 1000)
    endpoint_exponent = Fraction(4, 5)
    orbit_error_exponent = Fraction(3, 5)
    reconstruction_error_exponent = Fraction(7, 10)
    total_log_exponent = Fraction(1, 1)

    assert endpoint_exponent - orbit_error_exponent == Fraction(1, 5)
    assert total_log_exponent - endpoint_exponent == Fraction(1, 5)
    assert endpoint_exponent - reconstruction_error_exponent == Fraction(1, 10)

    lambda_lower, lambda_upper = log_bounds(Fraction(4, 3))
    log_two_lower, log_two_upper = log_bounds(Fraction(2, 1))
    assert Fraction(1, 4) < lambda_lower < lambda_upper < 1
    assert log_two_upper < 1

    # The v7 choice n_0=floor(log(x)/(10 log 2)) reaches below x on the
    # good path because alpha^3-1 is strictly smaller than a fixed lower
    # bound for log(4/3)/(10 log 2).
    assert alpha**3 - 1 < Fraction(1, 300)
    assert Fraction(1, 300) < Fraction(1, 40)
    assert Fraction(1, 40) < lambda_lower / (10 * log_two_upper)

    # C=1 is an admissible fixed multiplicative-buffer constant because
    # C/lambda-1 has a positive exact rational lower bound.  Multiplying by
    # L^(4/5) then dominates every fixed K*L^(3/5).
    delta_lower = 1 / lambda_upper - 1
    assert delta_lower > 0

    # For y=x^beta, beta in {alpha,alpha^2}, the retained log interval is
    # nonempty once L^(-1/5) is below this exact threshold.  The same ratio,
    # up to the odd-harmonic integral-test error, controls excluded mass.
    interval_thresholds = {}
    for beta in (alpha, alpha**2):
        coefficient = (alpha - 1) * beta
        assert coefficient > 0
        threshold = (Fraction(2, 1) / coefficient) ** 5
        assert threshold > 0
        interval_thresholds[str(beta)] = str(threshold)

    report = {
        "status": "PASS",
        "pinned_hashes": len(PINNED),
        "source_locator_checks": source_locator_checks,
        "alpha": str(alpha),
        "endpoint_minus_orbit_error_exponent": "1/5",
        "total_mass_minus_endpoint_exponent": "1/5",
        "endpoint_minus_reconstruction_error_exponent": "1/10",
        "lambda_lower": str(lambda_lower),
        "lambda_upper": str(lambda_upper),
        "buffer_delta_lower": str(delta_lower),
        "interval_nonempty_L_thresholds": interval_thresholds,
        "scope": "endpoint buffer and exact local asymptotic comparisons only",
    }
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
