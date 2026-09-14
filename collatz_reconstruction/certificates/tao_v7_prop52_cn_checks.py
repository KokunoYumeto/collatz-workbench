"""Deterministic checks for the Tao-v7 Proposition 5.2 c_n repair.

The accompanying TeX proof supplies the quantified analytic argument.  This
certificate pins the controlling source and frozen route ledgers, verifies the
exact source locators, and checks the exact exponent arithmetic and generating
function identities used to replace the non-uniform majorant printed at source
lines 909--914.  It does not certify the later fine-scale-mixing, Fourier, or
renewal arguments.
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


def require_source_fragments(lines: list[str]) -> int:
    required = {
        805: r"Suppose that $\vec a = (a_1,\dots,a_{n-m})$ is a tuple in ${\mathcal A}^{(n-m)}$, and $M \in E'$.  From Lemma \ref{iter-lem}, we see that the event $\left(\Syr^{n-m_0}(\mathbf{N}_y) = M\right) \wedge \left(\vec a^{(n-m_0)}(\mathbf{N}_y) = \vec a\right)$ holds if and only if $\Aff_{\vec a}( \mathbf{N}_y) \in E'$, and the claim \eqref{approx-form} follows.",
        854: r"c_n( X ) \coloneqq 3^{n-m_0} \sum_{M \in E': M = X \mod 3^{n-m_0}} \frac{1}{M}.",
        858: r"\begin{lemma}\label{loam}  We have $c_n(X) \ll 1$ for all $n \in I_y$ and $X \in \Z/3^{n-m_0}\Z$.",
        862: r"$$ c_n(X) \leq \sum_{(a_1,\dots,a_{m_0}) \in \N^{m_0}} c_{n,a_1,\dots,a_{m_0}}(X)$$",
        868: r"3^{m_0} 2^{-a_{[1,m_0]}} M + F_{m_0}(a_1,\dots,a_{m_0}) \leq x < 3^{m_0} 2^{-a_{[1,m_0-1]}} M + F_{m_0-1}(a_1,\dots,a_{m_0-1}) $$",
        889: r"\sum_{M_0 \leq M \leq M_1: M = a \mod q} \frac{1}{M}  \ll \frac{1}{q} \log O \left( \frac{M_1}{M_0} \right).",
        898: r"Now suppose instead that $2^{a_{[1,m_0]}} > x^{0.5}$, we recall from \eqref{s-iter} that",
        908: r"&\ll 3^n 2^{-a_{[1,m_0]}} + 2^{-a_{[1,m_0]}} a_{m_0}\\",
        909: r"&\ll 2^{-a_{[1,m_0]}/2}",
        913: r"$$ c_n(X) \ll \sum_{a_1,\dots,a_{m_0} \in \N} 2^{-a_{[1,m_0]}/2}$$",
        914: r"and the claim follows from summing the geometric series.",
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
    locator_checks = require_source_fragments(source_lines)

    alpha = Fraction(1001, 1000)
    m0_coefficient = (alpha - 1) / 100
    assert m0_coefficient == Fraction(1, 100_000)

    # Exact one-coordinate generating-function values at z=1/2:
    # sum_{a>=1} z^a=z/(1-z), and
    # sum_{a>=1} a*z^a=z/(1-z)^2.
    z = Fraction(1, 2)
    geometric_mass = z / (1 - z)
    last_coordinate_moment = z / (1 - z) ** 2
    assert geometric_mass == 1
    assert last_coordinate_moment == 2

    # log(3)/log(2)<8/5 follows without floating point from 3^5<2^8.
    assert 3**5 < 2**8
    n_exponent_upper = Fraction(4, 25)

    # The square-root geometric sum is 1+sqrt(2).  The elementary bounds
    # 1+sqrt(2)<5/2<e imply that its m_0-th power is at most x^(1/100000).
    assert 2 < Fraction(9, 4)  # sqrt(2)<3/2 after squaring.
    assert Fraction(1, 1) + Fraction(3, 2) == Fraction(5, 2)
    e_partial_lower = sum((Fraction(1, 1), Fraction(1, 1), Fraction(1, 2), Fraction(1, 6)))
    assert Fraction(5, 2) < e_partial_lower
    square_root_moment_exponent_upper = Fraction(1, 100_000)

    # In the large-A branch, 2^A>x^(1/2) contributes x^(-1/4) after
    # retaining one factor 2^(-A/2).  Multiplication by 3^n and the remaining
    # square-root moment therefore has a strictly negative power of x.
    tail_exponent = (
        n_exponent_upper
        - Fraction(1, 4)
        + square_root_moment_exponent_upper
    )
    assert tail_exponent == -Fraction(8_999, 100_000)

    # Bounded finite composition checks guard the positive-coordinate domain
    # and the coefficient count used by the generating-function argument.
    composition_checks = 0
    for m in range(1, 9):
        counts = {0: 1}
        for _ in range(m):
            next_counts: dict[int, int] = {}
            for total, count in counts.items():
                for a in range(1, 33 - total):
                    next_counts[total + a] = next_counts.get(total + a, 0) + count
            counts = next_counts
        for total, count in counts.items():
            # Number of positive m-tuples with coordinate sum total.
            from math import comb

            assert count == comb(total - 1, m - 1)
            composition_checks += 1

    report = {
        "status": "PASS",
        "scope": "Proposition 5.2 event locators and uniform c_n repair only",
        "pinned_hashes": len(PINNED),
        "source_locator_checks": locator_checks,
        "alpha": str(alpha),
        "m0_log_x_coefficient": str(m0_coefficient),
        "geometric_mass": str(geometric_mass),
        "last_coordinate_weighted_mass": str(last_coordinate_moment),
        "large_A_tail_x_exponent_upper": str(tail_exponent),
        "positive_composition_checks": composition_checks,
        "fine_scale_mixing_certified": False,
        "fourier_or_renewal_certified": False,
    }
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
