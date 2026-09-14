"""Run the portable research-companion validator under one process-tree cap.

The runner owns exactly one ``validate_package.py`` process tree, records its
stdout verbatim, samples aggregate memory, kills only that owned tree if it
reaches the cap or timeout, and writes a machine-readable receipt.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import psutil


PROJECT = Path(__file__).resolve().parents[1]
PACKAGE = PROJECT / "research_companion"
VALIDATOR = PACKAGE / "validate_package.py"
AUDIT_ROOT = PACKAGE / "audit" / "package_validation"
CAP_BYTES = 5_000_000_000
TIMEOUT_SECONDS = 900
SAMPLE_SECONDS = 0.1


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def live_owned_processes(known: dict[int, float]) -> list[psutil.Process]:
    live: dict[int, psutil.Process] = {}
    for pid, created in list(known.items()):
        try:
            process = psutil.Process(pid)
            if process.create_time() != created or not process.is_running():
                continue
            live[pid] = process
            for child in process.children(recursive=True):
                known[child.pid] = child.create_time()
                live[child.pid] = child
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return list(live.values())


def kill_owned_tree(known: dict[int, float]) -> None:
    live = live_owned_processes(known)
    for process in reversed(live):
        try:
            process.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    _, survivors = psutil.wait_procs(live, timeout=5)
    if survivors:
        raise RuntimeError(
            f"owned validator PIDs survived termination: {[p.pid for p in survivors]}"
        )


def assert_no_other_validator() -> None:
    target = str(VALIDATOR).casefold()
    current_pid = psutil.Process().pid
    for process in psutil.process_iter(["pid", "cmdline"]):
        if process.pid == current_pid:
            continue
        command = " ".join(process.info.get("cmdline") or []).casefold()
        if target in command:
            raise RuntimeError(
                f"another companion validator is already active at PID {process.pid}"
            )


def main() -> None:
    assert VALIDATOR.is_file(), VALIDATOR
    assert_no_other_validator()
    run_id = datetime.now(timezone.utc).strftime("run_%Y%m%dT%H%M%SZ")
    run_dir = AUDIT_ROOT / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    stdout_path = run_dir / "validator_stdout.json"
    receipt_path = run_dir / "watch_receipt.json"
    command = [sys.executable, "-X", "utf8", str(VALIDATOR)]
    started_utc = utc_now()
    started = time.monotonic()
    known: dict[int, float] = {}
    peak_rss = 0
    peak_private = 0
    samples = 0
    termination_reason: str | None = None
    creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    with stdout_path.open("wb") as stream:
        process = subprocess.Popen(
            command,
            cwd=PACKAGE,
            stdout=stream,
            stderr=subprocess.STDOUT,
            creationflags=creationflags,
        )
        known[process.pid] = psutil.Process(process.pid).create_time()
        try:
            while True:
                live = live_owned_processes(known)
                rss = 0
                private = 0
                for member in live:
                    try:
                        memory = member.memory_info()
                        rss += memory.rss
                        private += getattr(
                            memory, "private", getattr(memory, "pagefile", memory.rss)
                        )
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                samples += 1
                peak_rss = max(peak_rss, rss)
                peak_private = max(peak_private, private)
                if max(rss, private) >= CAP_BYTES:
                    termination_reason = "aggregate_process_tree_memory_cap"
                    kill_owned_tree(known)
                    break
                if time.monotonic() - started > TIMEOUT_SECONDS:
                    termination_reason = "validator_timeout"
                    kill_owned_tree(known)
                    break
                if process.poll() is not None and not live:
                    break
                time.sleep(SAMPLE_SECONDS)
        except Exception:
            kill_owned_tree(known)
            raise
        returncode = process.wait(timeout=5)

    output = stdout_path.read_bytes()
    parsed = None
    if returncode == 0 and termination_reason is None:
        parsed = json.loads(output.decode("utf-8"))
    tree_clear = not live_owned_processes(known)
    receipt = {
        "schema_version": 1,
        "run_id": run_id,
        "started_utc": started_utc,
        "finished_utc": utc_now(),
        "command": command,
        "cwd": str(PACKAGE),
        "returncode": returncode,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "cap_bytes": CAP_BYTES,
        "timeout_seconds": TIMEOUT_SECONDS,
        "sample_seconds": SAMPLE_SECONDS,
        "peak_aggregate_rss_bytes": peak_rss,
        "peak_aggregate_private_bytes": peak_private,
        "samples": samples,
        "task_process_pids": sorted(known),
        "termination_reason": termination_reason,
        "process_tree_clear": tree_clear,
        "stdout_path": stdout_path.relative_to(PROJECT).as_posix(),
        "stdout_sha256": sha256(output),
        "validator_result": parsed,
    }
    receipt_path.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": parsed.get("status") if parsed else "FAILED",
                "receipt": str(receipt_path),
                "returncode": returncode,
                "termination_reason": termination_reason,
                "process_tree_clear": tree_clear,
                "peak_aggregate_rss_bytes": peak_rss,
                "peak_aggregate_private_bytes": peak_private,
            },
            indent=2,
        )
    )
    if (
        returncode != 0
        or termination_reason is not None
        or not tree_clear
        or not isinstance(parsed, dict)
        or parsed.get("status") != "PASS"
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
