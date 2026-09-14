#!/usr/bin/env python3
"""Repair stale historical gate wording discovered during the ACT31 state audit."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state"


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def write_jsonl_if_changed(path: Path, records: list[dict]) -> bool:
    rendered = "\n".join(
        json.dumps(record, ensure_ascii=False, separators=(",", ":"))
        for record in records
    ) + "\n"
    if path.read_text(encoding="utf-8") == rendered:
        return False
    path.write_text(rendered, encoding="utf-8", newline="\n")
    return True


chapter = ROOT / "tex" / "chapters" / "01g_tao_fourier_renewal.tex"
chapter_hash = hashlib.sha256(chapter.read_bytes()).hexdigest()
assert chapter.stat().st_size == 42_957
assert chapter_hash == "23dea1dc9f414a86ac2cfa54ffde6ba884fb96e720ed33c9cf7407cc3070e2cc"

source_path = STATE / "source_registry.jsonl"
sources = read_jsonl(source_path)
src5 = next(record for record in sources if record.get("source_id") == "SRC-COL-000005")
src5["reading"]["adversarial_audit"].update(
    {
        "final_tex_bytes": 42_957,
        "final_tex_sha256": chapter_hash,
    }
)
src5["reading"]["first_passage_certificate"]["metrics"].update(
    {
        "version_boundary_checks": 5,
        "printed_fixed_M_membership_counterexample_checks": 3,
        "lift_exponent_factor_checks": 24,
        "truncated_one_coordinate_mass_checks": 66,
        "truncated_tuple_weighted_mass_checks": 60,
        "nonuniform_square_root_majorant_checks": 37,
    }
)

claims_path = STATE / "claims.jsonl"
claims = read_jsonl(claims_path)
clm116 = next(record for record in claims if record.get("claim_id") == "CLM-COL-000116")
clm117 = next(record for record in claims if record.get("claim_id") == "CLM-COL-000117")
clm118 = next(record for record in claims if record.get("claim_id") == "CLM-COL-000118")

clm116["nonclaims"] = [
    (
        "The Fourier/renewal branch and its finite script do not themselves certify "
        "Proposition 1.9 or Proposition 1.11; F025 independently certifies Proposition "
        "1.9, and F026 separately closes its exact use with Proposition 1.14 to obtain "
        "Proposition 1.11. Theorem 1.6 and Theorem 1.3 remain behind separate gates."
        if text
        == "The Fourier/renewal branch and its finite script do not themselves certify Proposition 1.9; the independent valuation-law proof is now CLM-COL-000117, while Proposition 1.11, Theorem 1.6, and Theorem 1.3 remain behind the next named gate."
        else text
    )
    for text in clm116["nonclaims"]
]

clm117["status"] = (
    "proved_at_Tao_Proposition_1_9_source_scope_Proposition_1_11_closed_"
    "separately_under_CLM118_Theorem_1_6_gate_open"
)
clm117["nonclaims"] = [
    (
        "This claim by itself does not certify the exact Proposition 1.14 plus "
        "Proposition 1.9 to Proposition 1.11 dependency edge; that edge is separately "
        "closed under CLM-COL-000118 and MOR-COL-000029."
        if text
        == "This claim does not yet certify the exact Proposition 1.14 plus Proposition 1.9 to Proposition 1.11 dependency edge."
        else text
    )
    for text in clm117["nonclaims"]
]
clm118["formal_status"]["verified_finite_metrics"].update(
    {
        "version_boundary_checks": 5,
        "printed_fixed_M_membership_counterexample_checks": 3,
        "lift_exponent_factor_checks": 24,
        "truncated_one_coordinate_mass_checks": 66,
        "truncated_tuple_weighted_mass_checks": 60,
        "nonuniform_square_root_majorant_checks": 37,
    }
)

changed = {
    "source_registry": write_jsonl_if_changed(source_path, sources),
    "claims": write_jsonl_if_changed(claims_path, claims),
}
print(json.dumps({"status": "PASS", "changed": changed}, sort_keys=True))
