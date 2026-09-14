"""Retire the legacy obligation fields from the active claim ledger.

The historical state/proof_obligations.jsonl file is deliberately left
byte-identical and is pinned by state/legacy_status_migration.jsonl.  This
one-shot migration removes its former active cross-references.  Only the two
source claims that genuinely depend on missing mathematical arrows receive
exact GAP-COL references; formalization, acquisition, checking, and release
work remains in TODO.md.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLAIMS = ROOT / "state" / "claims.jsonl"
LEGACY = ROOT / "state" / "proof_obligations.jsonl"
MIGRATION = ROOT / "state" / "legacy_status_migration.jsonl"

EXPECTED_CLAIMS_SHA256 = (
    "c050c4d724bf07b89f10807ca945d196160edf6891017bac58accb69d9897536"
)
EXPECTED_LEGACY_SHA256 = (
    "e807afdbf4a3f78df0c93c903a0ab6178da03b3d69aeaa6b28c99f96a83e1383"
)

EXACT_GAP_BY_CLAIM = {
    "CLM-COL-000041": ["GAP-COL-000001"],
    "CLM-COL-000042": ["GAP-COL-000002"],
}

RETIRED_KEYS = {"open_obligation_ids", "proof_obligation"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scrub(value):
    removed = 0
    if isinstance(value, dict):
        result = {}
        for key, item in value.items():
            if key in RETIRED_KEYS:
                removed += 1
                continue
            cleaned, count = scrub(item)
            removed += count
            result[key] = cleaned
        return result, removed
    if isinstance(value, list):
        result = []
        for item in value:
            cleaned, count = scrub(item)
            removed += count
            result.append(cleaned)
        return result, removed
    return value, 0


def main() -> None:
    assert sha256(CLAIMS) == EXPECTED_CLAIMS_SHA256
    assert sha256(LEGACY) == EXPECTED_LEGACY_SHA256
    assert MIGRATION.is_file()

    rows = [json.loads(line) for line in CLAIMS.read_text(encoding="utf-8").splitlines()]
    assert len(rows) == 137
    assert rows[0]["ledger"] == "claims"

    removed = 0
    migrated = []
    for row in rows:
        row, count = scrub(row)
        removed += count
        claim_id = row.get("claim_id")
        if claim_id in EXACT_GAP_BY_CLAIM:
            row["unresolved_dependency_ids"] = EXACT_GAP_BY_CLAIM[claim_id]
        if claim_id == "CLM-COL-000041":
            row["claim_type"] = "source_correspondence_statement_with_exact_gap_audit"
        migrated.append(row)

    assert removed > 0
    for row in migrated:
        text = json.dumps(row, ensure_ascii=False, separators=(",", ":"))
        assert "open_obligation_ids" not in text
        assert '"proof_obligation"' not in text

    CLAIMS.write_text(
        "\n".join(
            json.dumps(row, ensure_ascii=False, separators=(",", ":"))
            for row in migrated
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )

    print(
        json.dumps(
            {
                "status": "PASS",
                "claim_records": len(migrated) - 1,
                "retired_fields_removed": removed,
                "exact_gap_links_added": sum(len(v) for v in EXACT_GAP_BY_CLAIM.values()),
                "legacy_file_unchanged": sha256(LEGACY) == EXPECTED_LEGACY_SHA256,
                "claims_sha256": sha256(CLAIMS),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
