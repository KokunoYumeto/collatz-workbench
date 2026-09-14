"""Finite exact checks for the Siegel-v1/Tao Syracuse coordinate morphism.

The TeX proof establishes the infinite product/Haar and 3-adic statements.
This certificate pins both versioned sources and the frozen route ledgers,
checks the controlling source locators, and exhausts a bounded kernel of the
run-length/binary-position inverse and finite 3-adic projection identities.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TAO_TEX = Path(
    r"C:\Users\LOCAL_USER\Documents\arxiv_latex\library\collatz_reconstruction"
    r"\latex\1909.03562v7\collatz.tex"
)
SIEGEL_TEX = Path(
    r"C:\Users\LOCAL_USER\Documents\arxiv_latex\library\collatz_reconstruction"
    r"\latex\2007.15936v1\Collatz_Numen_Integral.tex"
)
SIEGEL_EPRINT = Path(
    r"C:\Users\LOCAL_USER\Documents\arxiv_latex\library\collatz_reconstruction"
    r"\source\2007.15936v1.eprint"
)
SIEGEL_V3_TEX = Path(
    r"C:\Users\LOCAL_USER\Documents\arxiv_latex\library\collatz_reconstruction"
    r"\latex\2007.15936v3\main.tex"
)
SIEGEL_V3_EPRINT = Path(
    r"C:\Users\LOCAL_USER\Documents\arxiv_latex\library\collatz_reconstruction"
    r"\source\2007.15936v3.eprint"
)
PINNED = {
    TAO_TEX: (
        164_932,
        "bfbc39432d4084a276416cb019a592003c868fa32f18e2f90028ac325ae5c19d",
    ),
    SIEGEL_TEX: (
        263_079,
        "bbb6add6f9d113ce66ef68cd42dc0ffab234233a69e558f99615df7fef8a842b",
    ),
    SIEGEL_EPRINT: (
        293_342,
        "ff849b016bf3530f23cf9f921e5e9fcefbd90e2274440d26a138ef3b32ae1eb7",
    ),
    SIEGEL_V3_TEX: (
        211_321,
        "7f66c3e4a7e49600a3848a51fb53e310edafd116d69856499b0010a24e39bfdb",
    ),
    SIEGEL_V3_EPRINT: (
        55_025,
        "2cd43f78e4b6035ba339398cfb2d520f98362fd84847d48d676c5345656346f5",
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
    tao = TAO_TEX.read_text(encoding="utf-8").splitlines()
    # The historical v1 TeX is a byte-faithful legacy Latin-1 source; do not
    # silently transcode it.  Every controlled locator below is ASCII.
    siegel = SIEGEL_TEX.read_text(encoding="latin-1").splitlines()
    siegel_v3 = SIEGEL_V3_TEX.read_text(encoding="latin-1").splitlines()
    required_tao = {
        390: r"\Syrac(\Z_3) &\equiv \sum_{j=0}^\infty 3^j 2^{-\a_{[1,j+1]}}\\",
        391: r"&= 2^{-\a_1} + 3^1 2^{-\a_{[1,2]}} + 3^2 2^{-\a_{[1,3]}} + \dots",
        438: r"\Syrac(\Z/3^n\Z) \equiv 2^{-\a_1} + 3^1 2^{-\a_{[1,2]}} + \dots + 3^{n-1} 2^{-\a_{[1,n]}} \mod 3^n,",
    }
    required_siegel = {
        413: r"\chi_{p}\left(t\right)\overset{\textrm{def}}{=}h_{\beta^{-1}\left(t\right)}\left(0\right),\textrm{ }\forall t\in\mathbb{N}_{0}\label{eq:Def of Chi_p}",
        501: r"\chi_{p}\left(\sum_{k=1}^{\#_{1}\left(t\right)}2^{n_{k}}\right)=\sum_{k=1}^{\#_{1}\left(t\right)}\frac{p^{k-1}}{2^{n_{k}+1}}\label{eq:Chi formula (Version 1)}",
        568: r"\chi_{p}\left(\sum_{k=1}^{\infty}2^{n_{k}}\right)\overset{\mathbb{Z}_{p}}{=}\sum_{k=1}^{\infty}\frac{p^{k-1}}{2^{n_{k}+1}}\label{eq:2-adic interpolation of Chi_p}",
        3467: r"In this terminology, Tao's $\textrm{Syrac}\left(\mathbb{Z}/3^{n}\mathbb{Z}\right)$",
        3468: r"is the projection of $\chi_{3}$ mod $3^{n}$. In this---the author's",
    }
    required_siegel_v3 = {
        1854: r"\chi_{q}\left(\mathbf{j}\right)=\sum_{m=1}^{\left|\mathbf{j}\right|}\frac{b_{j_{m}}}{2}\prod_{k=1}^{m-1}\frac{a_{j_{k}}}{2},\textrm{ }\forall\mathbf{j}\in\textrm{String}\left(2\right)\label{eq:Formula for Chi_H in terms of bold-j}",
        1895: r"\chi_{q}\left(\mathfrak{z}\right)\overset{\mathbb{Z}_{q}}{=}\lim_{n\rightarrow\infty}\chi_{q}\left(\left[\mathfrak{z}\right]_{2^{n}}\right)\label{eq:Rising Continuity Formula for Chi_H}",
        3106: r"Surprisingly, $\chi_{3}$ is equivalent to Tao's Syracuse Random Variables.",
        3152: r"The $n$th Syracuse Random Variable is then precisely the real-valued",
        3183: r"\mathbb{P}\left(\mathbf{Syrac}\left(\mathbb{Z}/3^{n}\mathbb{Z}\right)=x\right)=\textrm{P}\left(\chi_{3}\overset{3^{n}}{\equiv}x\right),\textrm{ }\forall x\in\mathbb{Z}/3^{n}\mathbb{Z}",
    }
    for line_number, fragment in required_tao.items():
        assert tao[line_number - 1].strip() == fragment, ("Tao", line_number)
    for line_number, fragment in required_siegel.items():
        assert siegel[line_number - 1].strip() == fragment, ("Siegel", line_number)
    for line_number, fragment in required_siegel_v3.items():
        assert siegel_v3[line_number - 1].strip() == fragment, ("Siegel-v3", line_number)
    return len(required_tao) + len(required_siegel) + len(required_siegel_v3)


def cumulative_positions(run_lengths: tuple[int, ...]) -> tuple[int, ...]:
    total = 0
    positions = []
    for value in run_lengths:
        assert value >= 1
        total += value
        positions.append(total - 1)
    return tuple(positions)


def inverse_run_lengths(positions: tuple[int, ...]) -> tuple[int, ...]:
    assert positions and positions[0] >= 0
    assert all(a < b for a, b in zip(positions, positions[1:]))
    return (positions[0] + 1,) + tuple(
        positions[j] - positions[j - 1] for j in range(1, len(positions))
    )


def mod_fraction(value: Fraction, modulus: int) -> int:
    assert value.denominator % 3 != 0
    return (value.numerator * pow(value.denominator, -1, modulus)) % modulus


def main() -> int:
    for path, (size, digest) in PINNED.items():
        assert path.is_file(), path
        assert path.stat().st_size == size, (path, path.stat().st_size)
        assert sha256(path) == digest, path

    locator_checks = require_fragments()
    coordinate_checks = 0
    projection_checks = 0
    cylinder_checks = 0
    for length in range(1, 8):
        for runs in itertools.product(range(1, 5), repeat=length):
            positions = cumulative_positions(runs)
            assert inverse_run_lengths(positions) == runs
            binary_coordinate = sum(1 << position for position in positions)
            assert tuple(
                bit for bit in range(binary_coordinate.bit_length())
                if (binary_coordinate >> bit) & 1
            ) == positions

            cumulative = 0
            tao_value = Fraction(0)
            for k, run in enumerate(runs, start=1):
                cumulative += run
                tao_value += Fraction(3 ** (k - 1), 2**cumulative)
            siegel_value = sum(
                (Fraction(3 ** k, 2 ** (position + 1))
                 for k, position in enumerate(positions)),
                Fraction(0),
            )
            assert tao_value == siegel_value
            coordinate_checks += 1

            modulus = 3**length
            assert mod_fraction(tao_value, modulus) == mod_fraction(siegel_value, modulus)
            projection_checks += 1

            # The product Geom(2) mass of the run cylinder and the Haar mass
            # of the binary prefix through its final one are both 2^(-A_k).
            product_mass = Fraction(1, 2 ** sum(runs))
            haar_prefix_mass = Fraction(1, 2 ** (positions[-1] + 1))
            assert product_mass == haar_prefix_mass
            cylinder_checks += 1

    report = {
        "status": "PASS",
        "scope": "run-length/Haar coordinate morphism and finite Syracuse projections",
        "pinned_hashes": len(PINNED),
        "source_locator_checks": locator_checks,
        "coordinate_inverse_and_series_checks": coordinate_checks,
        "finite_projection_checks": projection_checks,
        "cylinder_measure_checks": cylinder_checks,
        "maximum_checked_run_length_prefix": 7,
        "maximum_checked_coordinate_value": 4,
        "prop52_cn_bound_certified": False,
        "periodic_point_correspondence_certified": False,
    }
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
