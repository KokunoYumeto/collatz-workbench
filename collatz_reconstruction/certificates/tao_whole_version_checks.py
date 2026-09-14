"""Deterministic checks for the Tao v5/v7 whole-version audit.

This script pins the two arXiv source manifestations, the published journal
PDF, and the immutable routing artifacts.  It checks the complete line-diff
counts, the exact source tail and bibliography boundary, citation-key closure,
the recorded substantive source signatures, and exact rational enclosures for
the Section 6 exponential margin.

It does not prove Tao's analytic characteristic-decay estimate, any infinite
probabilistic limit, the journal's typeset mathematical identity with either
arXiv version, or the Collatz conjecture.  Journal hunk classification remains
an independently read page-level audit pinned by the PDF hash.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHELF = Path(
    r"C:\Users\LOCAL_USER\Documents\arxiv_latex\library\collatz_reconstruction"
)
V5_TEX = SHELF / "latex" / "1909.03562v5" / "collatz.tex"
V7_TEX = SHELF / "latex" / "1909.03562v7" / "collatz.tex"
JOURNAL_PDF = Path(
    r"C:\Users\LOCAL_USER\Documents\arxiv_latex\library\_recovered_from_papers"
    r"\by_title\Tao Almost all orbits of the Collatz map attain almost bounded values.pdf"
)

PINNED = {
    V5_TEX: (
        163_356,
        "c676b362b30807aa6690d0d4f16b8c8e84324732f5c0eb72ccfd875000276ae0",
    ),
    V7_TEX: (
        164_932,
        "bfbc39432d4084a276416cb019a592003c868fa32f18e2f90028ac325ae5c19d",
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

EXPECTED_CITED_KEYS = {
    "allouche",
    "baker",
    "barina",
    "bourgain",
    "carletti",
    "chamber",
    "crandall",
    "eric",
    "everett",
    "kl",
    "km",
    "kont",
    "korec",
    "ks",
    "lag",
    "ls",
    "lw",
    "olive",
    "sinai",
    "tao:chowla",
    "terras",
    "thomas",
    "wirsch",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_fragment(lines: list[str], number: int, fragment: str) -> None:
    assert fragment in lines[number - 1], (number, fragment, lines[number - 1])


def git_diff_metrics(ignore_all_space: bool) -> tuple[int, int, int]:
    command = [
        "git",
        "-c",
        "core.safecrlf=false",
        "diff",
        "--no-index",
    ]
    if ignore_all_space:
        command.append("--ignore-all-space")
    command.extend(["--unified=0", "--", str(V5_TEX), str(V7_TEX)])
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    assert result.returncode == 1, result.stderr
    lines = result.stdout.splitlines()
    hunks = sum(line.startswith("@@") for line in lines)
    additions = sum(
        line.startswith("+") and not line.startswith("+++") for line in lines
    )
    deletions = sum(
        line.startswith("-") and not line.startswith("---") for line in lines
    )
    return hunks, additions, deletions


def log_bounds(value: Fraction, terms: int = 80) -> tuple[Fraction, Fraction]:
    """Exact enclosure from log(value)=2*atanh((value-1)/(value+1))."""

    assert value > 0
    z = (value - 1) / (value + 1)
    assert 0 <= z < 1
    partial = sum(
        (z ** (2 * index + 1) / (2 * index + 1) for index in range(terms)),
        Fraction(),
    )
    lower = 2 * partial
    first_omitted = 2 * z ** (2 * terms + 1) / (2 * terms + 1)
    upper = lower + first_omitted / (1 - z * z)
    return lower, upper


def source_boundary_checks() -> dict[str, int | str | bool]:
    v5_text = V5_TEX.read_text(encoding="utf-8")
    v7_text = V7_TEX.read_text(encoding="utf-8")
    v5 = v5_text.splitlines()
    v7 = v7_text.splitlines()
    assert len(v5) == 1_945
    assert len(v7) == 1_956

    require_fragment(v5, 1848, r"This (finally!) concludes the proof")
    require_fragment(v7, 1859, r"This (finally!) concludes the proof")
    assert v5[1848] == ""
    assert v7[1859] == ""
    require_fragment(v5, 1852, r"\begin{thebibliography}{10}")
    require_fragment(v5, 1941, r"\end{thebibliography}")
    require_fragment(v5, 1945, r"\end{document}")
    require_fragment(v7, 1863, r"\begin{thebibliography}{10}")
    require_fragment(v7, 1952, r"\end{thebibliography}")
    require_fragment(v7, 1956, r"\end{document}")

    v5_bib = v5[1851:1941]
    v7_bib = v7[1862:1952]
    assert len(v5_bib) == len(v7_bib) == 90
    assert [line.rstrip() for line in v5_bib] == [line.rstrip() for line in v7_bib]
    normalized_v5_bib = re.sub(r"\s+", "", "\n".join(v5_bib))
    normalized_v7_bib = re.sub(r"\s+", "", "\n".join(v7_bib))
    assert normalized_v5_bib == normalized_v7_bib
    assert len(normalized_v5_bib) == 3_600

    normalized_v5 = re.sub(r"\s+", "", v5_text)
    normalized_v7 = re.sub(r"\s+", "", v7_text)
    assert len(normalized_v5) == 138_900
    assert len(normalized_v7) == 140_369
    assert hashlib.sha256(normalized_v5.encode()).hexdigest() == (
        "9f5d7629cc54e2f8660df82d2787ca256dacae145c905cad705e1dacbbb1375f"
    )
    assert hashlib.sha256(normalized_v7.encode()).hexdigest() == (
        "ca759f46014aaafab75e643e8ba13ee3befd5decb3e2f095c4ee712ab9193693"
    )

    return {
        "v5_line_count": len(v5),
        "v7_line_count": len(v7),
        "post_v7_1860_mathematical_lines": 0,
        "bibliography_lines_each": len(v5_bib),
        "bibliography_normalized_characters_each": len(normalized_v5_bib),
        "bibliography_exact_after_whitespace_deletion": True,
        "whole_files_exact_after_whitespace_deletion": False,
    }


def citation_checks() -> dict[str, int | list[str]]:
    lines = V7_TEX.read_text(encoding="utf-8").splitlines()
    active_lines = [line for line in lines if not line.lstrip().startswith("%")]
    calls: list[str] = []
    for line in active_lines:
        calls.extend(re.findall(r"\\cite\{([^}]+)\}", line))
    bibliography = {
        match.group(1)
        for line in active_lines
        if (match := re.match(r"\s*\\bibitem\{([^}]+)\}", line))
    }
    cited = set(calls)
    assert len(calls) == 25
    assert cited == EXPECTED_CITED_KEYS
    assert len(bibliography) == 24
    assert cited <= bibliography
    assert bibliography - cited == {"terras2"}
    return {
        "citation_calls": len(calls),
        "unique_cited_keys": len(cited),
        "active_bibliography_items": len(bibliography),
        "unresolved_citation_keys": len(cited - bibliography),
        "active_uncited_keys": sorted(bibliography - cited),
    }


def substantive_signature_checks() -> int:
    v5 = V5_TEX.read_text(encoding="utf-8").splitlines()
    v7 = V7_TEX.read_text(encoding="utf-8").splitlines()
    checks = [
        (v5, 326, "For each sufficiently large $y$"),
        (v7, 326, "For any $y$ with"),
        (v7, 334, "implied constants here are also absolute"),
        (v7, 344, r"\label{syr-forward}"),
        (v7, 366, "after relabeling the variables"),
        (v7, 367, r"\label{fn-recurse}"),
        (v7, 385, r"\label{syr3}"),
        (v7, 393, "ancient'' Syracuse iteration"),
        (v7, 428, "uniform in the parameters"),
        (v7, 440, "this also follows from"),
        (v5, 440, "Alex Kontorovich, Alexandre Patriota"),
        (v7, 446, "Alex Kontorovich, Lech Mazur, Alexandre Patriota"),
        (v5, 789, r"\Pass_x(\mathbf{N}_y) = n-m_0"),
        (v7, 795, r"T_x(\mathbf{N}_y) = n-m_0"),
        (v5, 791, r"T_x(\mathbf{N}_y) = T_x"),
        (v7, 797, r"\Pass_x(\mathbf{N}_y) = \Pass_x"),
        (v5, 983, r"\frac{1}{2} (C_A)^2"),
        (v7, 989, r"0.99 (C_A)^2"),
        (v5, 991, r"\frac{1}{2} (C_A)^2"),
        (v7, 997, r"0.99 (C_A)^2"),
        (v5, 1029, r"1_{\overline{E}_k"),
        (v7, 1035, r"1_{E_k"),
        (v5, 1074, r"\exp( - \frac{(C_A)^2}{2} \log n )"),
        (v5, 1075, r"\frac{(C_A)^2}{4}"),
        (v7, 1080, r"\exp( - 0.99 \log 2 (C_A)^2 \log n )"),
        (v7, 1084, r"\frac{\log^2 2}{4 \log \frac{4}{3}}"),
        (v5, 1656, r"\eps \min(\r,R)"),
        (v7, 1662, r"1_{R \leq \r}"),
        (v7, 1758, r"\label{jjd}"),
        (v7, 1782, r"l_\Delta - l - \l_{[1,\k+p]}"),
        (v5, 1821, r"\E \exp"),
        (v7, 1829, r"\E 1_{R \leq \r}"),
        (v7, 1849, "We argue by contradiction"),
        (v7, 1851, r"E_{p,4^A(1+p^3)}"),
    ]
    for lines, number, fragment in checks:
        require_fragment(lines, number, fragment)
    return len(checks)


def section_six_margin_checks() -> dict[str, bool | int | str]:
    log_two_lower, log_two_upper = log_bounds(Fraction(2))
    log_four_thirds_lower, log_four_thirds_upper = log_bounds(Fraction(4, 3))

    cost_lower = log_two_lower**2 / (4 * log_four_thirds_upper)
    cost_upper = log_two_upper**2 / (4 * log_four_thirds_lower)
    v5_reserve_upper = Fraction(1, 2) * log_two_upper
    v7_reserve_lower = Fraction(99, 100) * log_two_lower

    assert cost_lower > v5_reserve_upper
    assert cost_upper < v7_reserve_lower

    threshold_lower = log_two_lower / (4 * log_four_thirds_upper)
    threshold_upper = log_two_upper / (4 * log_four_thirds_lower)
    assert threshold_lower > Fraction(3, 5)
    assert threshold_upper < Fraction(61, 100)

    # A fully rational sufficient overshoot budget used in the audit:
    # for n>=2, log n>=log 2>2/3, hence sqrt(log n)<=2 log n and
    # 2<=3 log n.  The one-step concentration overshoot is then at most
    # 6*C_A*log n for C_A>=1, which is at most .01*C_A^2*log n for C_A>=600.
    assert log_two_lower > Fraction(2, 3)
    c_a = 600
    assert 6 * c_a <= Fraction(1, 100) * c_a * c_a

    return {
        "v5_half_reserve_below_optimized_cost": True,
        "v5_printed_exponential_drops_log_two": True,
        "v5_explicit_counterexample_family_certified_by_script": False,
        "v7_point99_reserve_above_optimized_cost": True,
        "reserve_fraction_threshold_strictly_between": ["3/5", "61/100"],
        "explicit_sufficient_CA_for_point99_overshoot_only": c_a,
        "implicit_O_CA_logN_constant_made_explicit_by_source": False,
        "analytic_fourier_decay_certified_by_script": False,
    }


def journal_layout_checks() -> dict[str, int]:
    result = subprocess.run(
        ["pdfinfo", str(JOURNAL_PDF)], capture_output=True, text=True, check=True
    )
    match = re.search(r"^Pages:\s+(\d+)\s*$", result.stdout, re.MULTILINE)
    assert match and int(match.group(1)) == 56
    return {"journal_pdf_pages": int(match.group(1))}


def main() -> int:
    for path, (size, digest) in PINNED.items():
        assert path.is_file(), path
        assert path.stat().st_size == size, (path, path.stat().st_size, size)
        assert sha256(path) == digest, path

    raw_hunks, raw_additions, raw_deletions = git_diff_metrics(False)
    semantic_hunks, semantic_additions, semantic_deletions = git_diff_metrics(True)
    assert (raw_hunks, raw_additions, raw_deletions) == (124, 147, 136)
    assert (semantic_hunks, semantic_additions, semantic_deletions) == (28, 49, 38)

    report = {
        "status": "PASS",
        "scope": "whole-version source, bibliography, citation, and Section 6 finite margin checks",
        "pinned_hashes": len(PINNED),
        "raw_zero_context_hunks": raw_hunks,
        "raw_added_lines": raw_additions,
        "raw_deleted_lines": raw_deletions,
        "whitespace_only_hunks": raw_hunks - semantic_hunks,
        "substantive_hunks": semantic_hunks,
        "substantive_added_lines": semantic_additions,
        "substantive_deleted_lines": semantic_deletions,
        "substantive_source_signature_checks": substantive_signature_checks(),
        **source_boundary_checks(),
        **citation_checks(),
        **section_six_margin_checks(),
        **journal_layout_checks(),
        "journal_hunk_matrix_certified_by_script": False,
        "tao_main_theorem_reproved_by_this_script": False,
        "collatz_conjecture_claimed": False,
    }
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
