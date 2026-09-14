"""Record observed UI synchronization; never infer remote byte identity."""
from __future__ import annotations
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SYNC = "overleaf/sync_20260904/"
STAGE = SYNC + "canonical_project/"
REMOTE = SYNC + "affine_exactness_remote_receipt.json"
NOW = datetime.now(timezone.utc).isoformat()

def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def write(path, value):
    (ROOT / path).write_text(json.dumps(value, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")

def identity(path):
    data = (ROOT / path).read_bytes()
    return {"path": path, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}

def main():
    manifest = read(STAGE + "MANIFEST.json")
    for item in manifest["files"]:
        actual = identity(STAGE + item["path"])
        assert actual["sha256"] == item["sha256"], item["path"]
        assert actual["bytes"] == item["bytes"], item["path"]
    build = read(SYNC + "audit/affine_exactness/local_receipt.json")
    for item in build["builds"]:
        assert hashlib.sha256(Path(item["pdf"]).read_bytes()).hexdigest() == item["pdf_sha256"]
    paths = [
        "companion/chapters/04_affine_packets_parity_necklaces_and_residue_automata.tex",
        "companion/certificates/affine_packet_residue_checks.py",
        "critical/chapters/06_affine_packet_source_audit.tex",
        "research_companion.tex", "MANIFEST.json", "SOURCE_MAP.json", "README.md", "PACKAGE_STATUS.json",
    ]
    receipt = {
        "schema_version": 1, "receipt_id": "AFFINE-EXACTNESS-REMOTE-20260904",
        "recorded_utc": NOW, "status": "eight_named_files_uploaded_two_roots_remote_compiled",
        "canonical_project": "https://www.overleaf.com/project/6a91f06e408dd545780c660f",
        "controlling_requests": [identity("raw/USR-0015-canonical-overleaf-only.txt"), identity("raw/USR-0016-preprint-reader-and-model.txt")],
        "uploaded_local_files": [identity(STAGE + p) for p in paths],
        "method": "Three folder-context exact-file uploads and five selected root files; all overwrite lists observed and matched. Upload dialogs completed. No folder replacement.",
        "remote_builds": {
            "research_companion.tex": {"build_id": "1a06cc394a8-914039ce2d5d2f1f", "pages": 50, "errors": 0, "warnings": 0, "info": 2, "info_detail": "Underfull bibliography paragraphs at lines49-56 and89-95"},
            "main.tex": {"build_id": "1a06cc45e6a-9ebff3ebf8093f87", "pages": 182, "errors": 0, "warnings": 0, "info": 0},
        },
        "verification": "Live Overleaf page containers, PDF build links and diagnostic tabs; no remote byte-for-byte download comparison",
        "byte_for_byte_remote_verified": False,
        "default_main_document": "research_companion.tex",
        "default_selection_verified": True,
        "tao_source_changed": False,
        "tao_disclosure_reobserved": "This work was developed through human-LLM collaboration using ChatGPT 5.6 Sol, Ultra mode, in Codex, including source comparison, proof development, and computational checks.",
        "tao_build_preserved": "1a06ca2a2d9-fa47409cb632f010",
        "local_build_receipt": identity(SYNC + "audit/affine_exactness/local_receipt.json"),
        "visual_review": {"status": "PASS_requested_changed_pages", "independent_agent": "prepare_overleaf_workbenches", "companion_pages": [1,2,40,41,42,43,44,45,46,47,48], "critical_pages": [167,168,169,170,171,172], "root_rechecked_final_companion_pages": [1,43,47], "defects": [], "whole_pdf_review_claimed": False},
        "no_new_project": True, "no_sharing_change": True, "no_publication": True,
        "no_git": True, "no_lean": True, "no_AGENTS_edit": True,
        "whole_corpus_completion_claimed": False,
        "historical_zip": "Preserved, not overwritten. README and PACKAGE_STATUS identify it as pre-affine-revision, not current source.",
    }
    write(REMOTE, receipt)
    validation = subprocess.run([sys.executable, "-X", "utf8", str(ROOT/"scripts/validate_state.py")], capture_output=True, text=True, encoding="utf-8")
    result = json.loads(validation.stdout)
    write(SYNC + "audit/affine_exactness/state_validation.json", result)
    assert result["failure_count"] == 2, result
    assert all("source_inspection_conway_1972_20260826" in x for x in result["failures"]), result
    current = read("state/affine_packet_current.json")
    current.update(updated_utc=NOW, remote_sync_status="uploaded_and_remote_compiled", remote_receipt=identity(REMOTE), next_action="Reconcile affine raw-export coverage and antecedent PDF versions against direct content; recover the two missing registered Conway manifestations through evidenced source routes. The global corpus goal remains active.")
    current["remaining_validation_findings"] = result["failures"]
    current["legacy_companion_manifest_reconciled"] = False
    current["fresh_context_full_recovery_pass_claimed"] = False
    write("state/affine_packet_current.json", current)
    project = read("state/project_state.json")
    project["updated_utc"] = NOW
    project["current_request_state"]["active_write_status"] = "affine_checkpoint_locally_checked_and_remotely_compiled"
    project["current_request_state"]["affine_checkpoint"] = "state/affine_packet_current.json"
    project["next_action"] = current["next_action"]
    write("state/project_state.json", project)
    overleaf = read("state/overleaf_current.json")
    overleaf.update(updated_utc=NOW, status="affine_eight_file_update_two_roots_remote_compiled", active_main_document="research_companion.tex", last_receipt=REMOTE, pending_action="No pending upload for this affine checkpoint; keep all three separate entrypoints in the canonical project.")
    overleaf["current_affine_remote_builds"] = receipt["remote_builds"]
    write("state/overleaf_current.json", overleaf)
    ledger_path = ROOT / "state/action_receipts.jsonl"
    rows = [json.loads(line) for line in ledger_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    action = {"record_type":"action_receipt", "schema_version":"1.0", "receipt_id":"ACT-COL-000044", "timestamp_utc":NOW, "action":"affine_clock_groupoid_residue_exactness_and_canonical_overleaf_update", "inputs":["raw/USR-0015-canonical-overleaf-only.txt","raw/USR-0016-preprint-reader-and-model.txt","state/affine_packet_topic_route.json"], "outputs":["state/affine_packet_current.json",REMOTE,"output/pdf/collatz_working_corpus.pdf","research_companion/output/pdf/collatz_research_companion.pdf"], "result":"bounded_mathematics_and_remote_sync_verified_global_state_validation_has_two_missing_historical_sources", "claims":current["claims"], "morphisms":current["morphisms"], "certificate_receipt":identity("qa/affine_packet_certificate_extension_20260904/extension_receipt.json"), "build_receipt":receipt["local_build_receipt"], "remote_receipt":identity(REMOTE), "remaining_validation_findings":result["failures"], "source_reading_scope":current["source_reading"], "whole_source_coverage_reconciled":False, "whole_corpus_completion_claimed":False, "fresh_context_full_recovery_pass_claimed":False, "legacy_companion_manifest_reconciled":False}
    assert not any(row.get("receipt_id") == action["receipt_id"] for row in rows), "ACT44 already exists; inspect before changing"
    rows.append(action)
    ledger_path.write_text("".join(json.dumps(row, ensure_ascii=False, separators=(',',':'))+"\n" for row in rows),encoding="utf-8")
    print(json.dumps({"status":"recorded", "receipt":identity(REMOTE), "global_validation_status":result["status"], "goal_complete":False},indent=2))

if __name__ == "__main__":
    main()
