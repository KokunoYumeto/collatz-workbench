"""One watched rerun; preserve the certificate and every existing receipt."""
from datetime import datetime, timezone
import hashlib
import json
from math import gcd
import os
from pathlib import Path
import subprocess
import sys
import time
from uuid import uuid4

import psutil

BASE = Path(__file__).resolve().parents[1]
CERT = BASE / "certificates/affine_crt_synchronization_checks.py"
OLD = BASE / "audit/affine_crt_synchronization_checks_20260904_final.json"
CAP = 5_000_000_000
EXPECTED_CERT = "ee0340744c8886ff55a7246ae0141576eac3ec60d262b7431bc3579c0198d71e"
EXPECTED_TABLE = "c96f9a23ccf99710306d4188d737826fc3d03818e0fd80680fa3d9bd3ce626d3"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_new(path, value):
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, indent=2)
        handle.write("\n")


def mathematical_fields(receipt):
    return {key: value for key, value in receipt.items()
            if key not in {"execution", "recorded_utc", "command_argv"}}


def validate_table(receipt):
    table = receipt["full_joint_table_rows_mod_13_columns_mod_499"]
    assert len(table) == 13 and all(len(row) == 499 for row in table)
    assert all(type(value) is int and value >= 0 for row in table for value in row)
    assert sum(map(sum, table)) == 5005
    assert [sum(row) for row in table] == receipt["full_marginal_mod_13"]
    assert [sum(row[v] for row in table) for v in range(499)] == receipt["full_marginal_mod_499"]
    assert table[0][0] == 0
    assert sum(value > 0 for row in table for value in row) == 3473
    strata = {"1": 0, "13": 0, "499": 0, "6487": 0}
    for u, row in enumerate(table):
        for v, multiplicity in enumerate(row):
            residue = (3992 * u + 2496 * v) % 6487
            strata[str(gcd(residue, 6487))] += multiplicity
    assert strata == receipt["gcd_strata_all_words"]
    actual_hash = hashlib.sha256(json.dumps(table, separators=(",", ":")).encode()).hexdigest()
    assert actual_hash == receipt["joint_dense_table_sha256_compact_json"] == EXPECTED_TABLE
    return {"cells_checked": 6487, "entries": 5005, "support": 3473,
            "gcd_strata_recomputed_from_table": strata, "table_sha256": actual_hash}


def main():
    assert __debug__ and not sys.flags.optimize
    assert sha(CERT) == EXPECTED_CERT
    old_hash = sha(OLD)
    old = json.loads(OLD.read_text(encoding="utf-8"))
    old_table_check = validate_table(old)
    root = BASE.parent
    pinned = [root / "DIRECTIVES.md", root / "state/affine_packet_topic_route.json",
              BASE / "chapters/04_affine_packets_parity_necklaces_and_residue_automata.tex", CERT, OLD]
    before = {str(path.relative_to(root)): sha(path) for path in pinned}
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = BASE / "audit" / f"affine_crt_watched_review_{stamp}_{uuid4().hex[:8]}"
    run_dir.mkdir()
    new_path = run_dir / "certificate_receipt.json"
    command = [sys.executable, str(CERT), "--receipt", str(new_path)]
    started = time.monotonic()
    samples = []
    terminated_reason = None
    with (run_dir / "stdout.json").open("xb") as out, (run_dir / "stderr.txt").open("xb") as err:
        child = subprocess.Popen(command, cwd=BASE, stdout=out, stderr=err,
                                 creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        watcher = psutil.Process(os.getpid())
        while True:
            descendants = watcher.children(recursive=True)
            participants = [watcher] + descendants
            rss_sum, private_sum, enforced_sum = 0, 0, 0
            observed = []
            for process in participants:
                try:
                    info = process.memory_info()
                    private = getattr(info, "private", info.rss)
                    rss_sum += info.rss
                    private_sum += private
                    enforced_sum += max(info.rss, private)
                    observed.append({"pid": process.pid, "created": process.create_time()})
                except psutil.NoSuchProcess:
                    pass
            samples.append({"elapsed_ms": int(1000 * (time.monotonic() - started)),
                            "aggregate_rss_bytes": rss_sum,
                            "aggregate_private_bytes": private_sum,
                            "enforced_aggregate_bytes": enforced_sum,
                            "processes": observed})
            if enforced_sum >= CAP or time.monotonic() - started >= 30:
                terminated_reason = "aggregate_memory_cap" if enforced_sum >= CAP else "30_second_timeout"
                for process in reversed(descendants):
                    try:
                        process.kill()
                    except psutil.NoSuchProcess:
                        pass
                child.wait(timeout=5)
                break
            if child.poll() is not None and not descendants:
                break
            time.sleep(0.025)
    receipt = {
        "recorded_utc": datetime.now(timezone.utc).isoformat(),
        "command": command, "cwd": str(BASE), "worker_exit_code": child.returncode,
        "cap_bytes": CAP, "guard_poll_interval_ms": 25,
        "cap_metric": "Sum over watcher plus its entire descendant tree of max(RSS, private bytes), with kill at >=cap",
        "guard_timeout_seconds": 30, "terminated_reason": terminated_reason,
        "sampled_peak_enforced_aggregate_bytes": max(row["enforced_aggregate_bytes"] for row in samples),
        "samples": samples, "certificate_receipt": str(new_path),
        "existing_final_receipt_sha256": old_hash, "input_hashes_before": before,
        "old_receipt_complete_table_validation": old_table_check,
    }
    if terminated_reason is None and child.returncode == 0:
        new = json.loads(new_path.read_text(encoding="utf-8"))
        assert mathematical_fields(old) == mathematical_fields(new)
        receipt["new_receipt_complete_table_validation"] = validate_table(new)
        receipt["all_mathematical_fields_equal_prior_receipt"] = True
        receipt["new_certificate_receipt_sha256"] = sha(new_path)
        receipt["new_certificate_process_reported_peak_bytes"] = new["execution"]["peak_working_set_bytes"]
    receipt["input_hashes_after"] = {str(path.relative_to(root)): sha(path) for path in pinned}
    receipt["inputs_unchanged"] = receipt["input_hashes_after"] == before
    assert sha(CERT) == EXPECTED_CERT and sha(OLD) == old_hash
    receipt["status"] = "pass" if child.returncode == 0 and terminated_reason is None and receipt["inputs_unchanged"] else "fail"
    write_new(run_dir / "watcher_receipt.json", receipt)
    print(json.dumps({key: value for key, value in receipt.items() if key != "samples"}, indent=2))
    print("WATCHER_RECEIPT=" + str(run_dir / "watcher_receipt.json"))
    return 0 if receipt["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
