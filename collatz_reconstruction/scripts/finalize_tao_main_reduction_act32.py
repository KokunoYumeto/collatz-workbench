#!/usr/bin/env python3
"""Finalize ACT32 recovery pointers and the last resource audit idempotently.

This mechanical migration deliberately does not append the action receipt.
The receipt is appended only after the checkpoint contains the hashes of the
post-migration state.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state"
STAMP = "2026-08-28T12:31:06.6949570Z"
CHECKPOINT = "qa/RECOVERY-CHECKPOINT-20260828-ACT32.md"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: dict) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def append_unique(values: list[dict], value: dict) -> None:
    if value not in values:
        values.append(value)


def main() -> int:
    checkpoint_path = ROOT / CHECKPOINT
    assert checkpoint_path.is_file(), checkpoint_path

    coverage_path = STATE / "coverage.json"
    coverage = load(coverage_path)
    recovery = next(
        layer for layer in coverage["layers"] if layer["layer_id"] == "RECOVERY"
    )
    recovery.update({
        "status": (
            "working_checkpoint_passed_state_advanced_through_Tao_v7_"
            "Proposition1_14_Proposition1_9_Proposition1_11_Theorem3_1_"
            "Theorem1_6_and_Theorem1_3_ACT32_post1860_versioned_whole_paper_"
            "later_literature_Chatnotes_and_release_recovery_gates_open"
        ),
        "checkpoint_passed": True,
        "checkpoint_record": CHECKPOINT,
        "latest_receipt": "ACT-COL-000032",
        "passed": False,
    })
    write(coverage_path, coverage)

    project_path = STATE / "project_state.json"
    project = load(project_path)
    assert project["status"] == "active"
    assert project["completion_claimed"] is False
    assert project["codex_goal"]["status"] == "active"
    project["last_receipt_id"] = "ACT-COL-000032"
    project["current_checkpoint"] = {
        "receipt_id": "ACT-COL-000032",
        "path": CHECKPOINT,
        "scope": (
            "Tao_v5_v7_journal_Proposition1_11_to_Theorem3_1_Theorem1_6_"
            "Theorem1_3_exact_repaired_main_reduction"
        ),
        "global_completion": False,
    }

    resource = project["resource_policy"]
    observation = {
        "module": "R11SupportIdealColon",
        "action": (
            "observed_unrelated_single_active_tree_below_3_GiB_and_left_"
            "untouched_no_overlap_started_by_this_task_then_ended"
        ),
        "pids": [6256, 16360, 43608],
        "lean_worker_private_working_set_bytes": 1_126_707_200,
    }
    final_audit = {
        "module": "all_Lean_Lake",
        "action": "final_audit_no_active_Lean_or_Lake_worker",
        "pids": [],
        "audit_utc": STAMP,
    }
    append_unique(resource["enforcement_events"], observation)
    append_unique(resource["enforcement_events"], final_audit)
    resource["last_enforcement_utc"] = STAMP
    resource["last_enforcement_result"] = (
        "no_active_R107_or_other_Lean_or_Lake_worker_at_final_audit; unrelated_"
        "R11SupportIdealColon_single_worker_was_observed_below_3_GiB_and_left_"
        "untouched_until_it_ended; no_overlapping_build_started_by_this_task"
    )
    project["updated_utc"] = STAMP
    write(project_path, project)

    print(json.dumps({
        "status": "PASS",
        "checkpoint": CHECKPOINT,
        "receipt_pointer": "ACT-COL-000032",
        "global_completion": False,
        "proof_obligations_closed": 0,
        "final_active_Lean_Lake_workers": 0,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
