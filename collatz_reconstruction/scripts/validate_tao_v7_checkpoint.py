"""Read-only identity and cross-reference check for the bounded ACT45 checkpoint.

This does not prove the analytic theorem, rerun the finite certificate, or
reinspect Overleaf. The remote compilation is an independently recorded UI
observation, not a byte-level remote hash verification.
"""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate():
    failures = []
    checkpoint = read_json(ROOT / "qa/ACT45-TAO-V7-FAMILY-CHECKPOINT.json")
    for record in checkpoint["files"]:
        path = ROOT / record["path"]
        if not path.is_file():
            failures.append("missing: " + record["path"])
        elif path.stat().st_size != record["bytes"] or digest(path) != record["sha256"]:
            failures.append("identity mismatch: " + record["path"])
    source = checkpoint["source"]
    if digest(Path(source["path"])) != source["sha256"]:
        failures.append("primary V7 source identity mismatch")
    for ledger, key, ids in (("claims.jsonl", "claim_id", checkpoint["claims"]),
                             ("morphisms.jsonl", "morphism_id", checkpoint["morphisms"])):
        records = [json.loads(line) for line in (ROOT / "state" / ledger).read_text(encoding="utf-8-sig").splitlines() if line.strip()]
        for identifier in ids:
            matches = [row for row in records if row.get(key) == identifier]
            if len(matches) != 1:
                failures.append("nonunique or absent record: " + identifier)
                continue
            locator = matches[0]["proof_locator"]
            proof = (ROOT / locator["path"]).read_text(encoding="utf-8")
            if locator["label"] not in re.findall(r"\\label\{([^}]+)\}", proof):
                failures.append("missing exact proof label: " + identifier)
    remote = read_json(ROOT / checkpoint["remote_receipt"])
    for filename in ("tao_preprint_current.json", "overleaf_current.json"):
        current = read_json(ROOT / "state" / filename)
        remote_state = current["overleaf"] if filename.startswith("tao_") else current["current_tao_remote_build"]
        if remote_state["build_id"] != remote["build"]["id"] or remote_state["pages"] != 16:
            failures.append("remote receipt/state mismatch: " + filename)
    project = read_json(ROOT / "state/project_state.json")
    if project["last_receipt_id"] != checkpoint["receipt_id"]:
        failures.append("latest action/checkpoint mismatch")
    if project["completion_claimed"] or checkpoint["global_completion"]:
        failures.append("unsupported full-corpus completion flag")
    canonical = ROOT / "overleaf/sync_20260904/canonical_project"
    for item in remote["uploaded_named_files"]:
        if digest(canonical / item["path"]) != item["sha256"]:
            failures.append("uploaded input changed: " + item["path"])
    # This is a content-preserving path-prefix translation, not a new root.
    local_tex = (ROOT / checkpoint["current_tex"]).read_text(encoding="utf-8")
    translated = local_tex.replace("\\input{sections/", "\\input{tao/sections/").replace("\\input{bibliography}", "\\input{tao/bibliography}")
    if translated != (canonical / "tao_preprint.tex").read_text(encoding="utf-8"):
        failures.append("canonical root is not the exact declared path translation")
    return {"status": "PASS" if not failures else "FAIL", "checkpoint": checkpoint["receipt_id"],
            "pinned_files_checked": len(checkpoint["files"]), "proof_records_checked": 3,
            "uploaded_input_hashes_checked": len(remote["uploaded_named_files"]),
            "failures": failures, "scope": "bounded_checkpoint_identity_and_cross_references_only",
            "analytic_proof_or_full_corpus_completion_claimed": False}


if __name__ == "__main__":
    try:
        report = validate()
    except Exception as error:
        report = {"status": "FAIL", "failures": [str(error)]}
    print(json.dumps(report, indent=2))
    sys.exit(0 if report["status"] == "PASS" else 1)
