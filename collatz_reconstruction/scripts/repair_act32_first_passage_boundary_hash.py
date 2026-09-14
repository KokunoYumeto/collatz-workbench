#!/usr/bin/env python3
"""Record the ACT32 downstream-boundary-only update to the F026 chapter.

The F026 audit and ACT31 receipt remain immutable historical checkpoint
evidence.  The live source record must instead pin the chapter that was
actually included in the accepted ACT32 106-page PDF.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state"
CHAPTER = ROOT / "tex" / "chapters" / "01i_tao_first_passage_stabilisation.tex"

OLD_BYTES = 20_386
OLD_SHA256 = "ec16f1047928073682df1085f055ef5582a756c3b2cd2f3bef3169b6ba138ffd"
NEW_BYTES = 20_537
NEW_SHA256 = "4757ddcbd1ca4353b51f243c65fd8d0468f7b10700f1a091c881357a24edd647"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.write_text(
        "\n".join(
            json.dumps(record, ensure_ascii=False, separators=(",", ":"))
            for record in records
        ) + "\n",
        encoding="utf-8",
    )


def append_unique(values: list, value) -> None:
    if value not in values:
        values.append(value)


def main() -> int:
    assert CHAPTER.stat().st_size == NEW_BYTES
    assert digest(CHAPTER) == NEW_SHA256

    path = STATE / "source_registry.jsonl"
    records = read_jsonl(path)
    source = next(record for record in records if record.get("source_id") == "SRC-COL-000005")
    reading = source["reading"]
    audit = reading["first_passage_adversarial_audit"]

    prior_size = audit.get("f026_checkpoint_tex_bytes", audit["final_tex_bytes"])
    prior_hash = audit.get("f026_checkpoint_tex_sha256", audit["final_tex_sha256"])
    assert prior_size == OLD_BYTES
    assert prior_hash == OLD_SHA256

    audit.update({
        "status": (
            "pass_after_first_pass_floor_and_TeX_repairs_then_second_"
            "independent_reaudit_plus_ACT32_downstream_boundary_only_update"
        ),
        "f026_checkpoint_tex_bytes": OLD_BYTES,
        "f026_checkpoint_tex_sha256": OLD_SHA256,
        "final_tex_bytes": NEW_BYTES,
        "final_tex_sha256": NEW_SHA256,
        "act32_boundary_update": {
            "locator": "tex/chapters/01i_tao_first_passage_stabilisation.tex lines 594-597",
            "scope": (
                "replace_the_historical_open_downstream_gate_sentence_by_the_"
                "F027_closed_Theorem3_1_Theorem1_6_Theorem1_3_boundary"
            ),
            "mathematical_proof_changed": False,
            "included_in_build": "tmp/tao_main_reduction_act32_final_20260828/main.pdf",
            "included_build_sha256": (
                "1aa6e7f37db0ae8c417651bfa1fa4a2634ebbe52191f69ef748a7a001148e2d8"
            ),
        },
    })
    append_unique(
        reading["locators"],
        "tex/chapters/01i_tao_first_passage_stabilisation.tex lines 594-597, ACT32 downstream-boundary-only update included in the accepted 106-page build",
    )
    main_audit = reading["main_reduction_adversarial_audit"]
    append_unique(
        main_audit.setdefault("global_boundary_repairs", []),
        "01i lines 594-597: replace the historical open main-reduction gate by the exact F027 closure and retain the whole-paper/release gates",
    )

    write_jsonl(path, records)
    print(json.dumps({
        "status": "PASS",
        "source_id": "SRC-COL-000005",
        "f026_checkpoint_sha256": OLD_SHA256,
        "current_sha256": NEW_SHA256,
        "proof_changed": False,
        "accepted_pdf_already_contains_update": True,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
