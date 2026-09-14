#!/usr/bin/env python3
"""Bind the affine-packet certificate to the exact local and primary sources.

The portable arithmetic lives in the separately authored research companion.
This wrapper verifies the identities of the raw Chatnotes export, its local
technical-note antecedent, and the primary literature manifestations used by
the critical reconstruction; it then executes and checks the portable exact
certificate.  Hash identity does not authenticate a mathematical claim: the
critical chapter records the content-level source audit and its repairs.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


if not __debug__:
    raise RuntimeError(
        "affine_packet_source_and_cycle_checks.py refuses optimized Python: "
        "fail-closed assertions require __debug__"
    )


ROOT = Path(__file__).resolve().parents[1]

SOURCES = {
    "raw_chatnotes": (
        Path(
            r"C:\Users\LOCAL_USER\Documents\Papors\Chatnotes\more col thread"
            r"\ChatGPT-Implications of Affine Formula.md"
        ),
        143_053,
        "abb1abbb948dc140394de3d35f0efbde9b3facdf718c24b065b8d0adb951366e",
    ),
    "local_openai_technical_note": (
        Path(
            r"C:\Users\LOCAL_USER\Documents\Erdos Strauss and related"
            r"\ES-Fable-C123-support\external_sources"
            r"\combined_live_theorem_package_dependencies"
            r"\odd_step_collatz_orbit_packets_note.pdf"
        ),
        546_452,
        "13f49961a60b870fa7a6f0f646758b4d72c1a4e4267f347606cc8a3238d552f1",
    ),
    "crandall_1978": (
        Path(
            r"C:\Users\LOCAL_USER\Documents\Papors\OS"
            r"\on-the-3x-1-problem-5cygpgqcjg.pdf"
        ),
        964_602,
        "acafa9070e7c5e4b167d70d7cace81da39489710804c510ff8db4369133217f4",
    ),
    "bohm_sontacchi_1978": (
        Path(
            r"C:\Users\LOCAL_USER\Documents\Erdos Strauss and related"
            r"\maxwell_siegel_research\external_literature"
            r"\prior_art_2026-08-24\bohm_sontacchi_1978_bdim.pdf"
        ),
        373_523,
        "aa5591bc3bb504a2edfc42dbb19ade98beb63ba6ec3a00f356699e8d161de8d0",
    ),
    "lagarias_1990": (
        ROOT / "external_literature/dependency_gate_2026-08-25/lagarias_1990_impan.pdf",
        2_559_375,
        "7dc39db8d59c141b19eebfbd76e48c4e7d3906f97d0c7187739d2a7561399005",
    ),
    "urata_2003": (
        ROOT / "external_literature/urata_2003_official_aichi.pdf",
        78_688,
        "82c23a89958562c9385e9b6ae5d3c2e82f26c8afd6ff259fdd36c61c64f25cd4",
    ),
    "laarhoven_de_weger_2012_source_tex": (
        Path(
            r"C:\Users\LOCAL_USER\Documents\arxiv_latex\library"
            r"\collatz_reconstruction\latex\1209.3495v1\main.tex"
        ),
        52_459,
        "51b2c072646d33fc7f37fcd23e966f4435dc3e2026cd3fe83b6717829c31e0eb",
    ),
}

PORTABLE_CERTIFICATE = (
    ROOT / "research_companion/certificates/affine_packet_residue_checks.py"
)
PORTABLE_CERTIFICATE_BYTES = 34_101
PORTABLE_CERTIFICATE_SHA256 = (
    "3684832af599c1f761cb61665e0d907406a67135b0c595c6acce3731b05bfb60"
)
EXPECTED_METRICS_SHA256 = (
    "50106a4261308568466d6f4b4d9e16a09921a5efde5ac258c60cbf66577c97ba"
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def verify_file(path: Path, expected_bytes: int, expected_sha256: str) -> None:
    assert path.is_file(), path
    assert path.stat().st_size == expected_bytes, path
    assert digest(path) == expected_sha256, path


def main() -> int:
    identities = {}
    for source_id, (path, expected_bytes, expected_sha256) in SOURCES.items():
        verify_file(path, expected_bytes, expected_sha256)
        identities[source_id] = {
            "bytes": expected_bytes,
            "sha256": expected_sha256,
        }

    raw_path = SOURCES["raw_chatnotes"][0]
    raw_lines = raw_path.read_text(encoding="utf-8").splitlines()
    assert len(raw_lines) == 3021

    verify_file(
        PORTABLE_CERTIFICATE,
        PORTABLE_CERTIFICATE_BYTES,
        PORTABLE_CERTIFICATE_SHA256,
    )
    run = subprocess.run(
        [sys.executable, str(PORTABLE_CERTIFICATE)],
        cwd=PORTABLE_CERTIFICATE.parent,
        text=True,
        capture_output=True,
        check=False,
    )
    assert run.returncode == 0, run.stderr
    portable = json.loads(run.stdout)
    assert portable["metrics_sha256"] == EXPECTED_METRICS_SHA256
    assert portable["metrics"]["total_words_scanned_by_each_method"] == 4_734_620
    assert portable["metrics"]["independent_full_scan_methods"] == 2
    assert portable["metrics"]["total_integral_words"] == 0
    assert set(portable["checks"].values()) == {"PASS"}

    output = {
        "certificate": "affine-packet source identity and portable arithmetic binding",
        "checks": {
            "seven_exact_source_manifestations": "PASS",
            "raw_chatnotes_3021_physical_lines": "PASS",
            "portable_certificate_identity": "PASS",
            "portable_certificate_execution": "PASS",
            "portable_metrics_identity": "PASS",
        },
        "source_identities": identities,
        "raw_chatnotes_physical_lines": len(raw_lines),
        "portable_certificate": {
            "bytes": PORTABLE_CERTIFICATE_BYTES,
            "sha256": PORTABLE_CERTIFICATE_SHA256,
            "metrics_sha256": EXPECTED_METRICS_SHA256,
        },
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
