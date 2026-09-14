"""Validate this bounded result's recorded identities without repository scans."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
state = json.loads((root / "state.json").read_text(encoding="utf-8"))
checked = []
for item in state["artifacts"] + [dict(path=state["request"]["file"], sha256=state["request"]["sha256"])]:
    path = root / item["path"]
    actual = hashlib.sha256(path.read_bytes()).hexdigest().upper()
    if actual != item["sha256"]:
        raise SystemExit(f"Artifact changed: {path.name}")
    checked.append(path.name)
source_changes = []
for source in state["sources"]:
    if "path" in source:
        path = Path(source["path"])
        if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest().upper() != source["sha256"]:
            source_changes.append(source["id"])
if source_changes:
    raise SystemExit("Primary source version changed or unavailable; re-read: " + ", ".join(source_changes))
run = subprocess.run([sys.executable, "-B", str(root / "check_history.py")],
                     check=True, capture_output=True, text=True, timeout=60)
result = json.loads(run.stdout)
if result["status"] != "pass" or result["forward"]["words"] != 2047 or result["odd_return"]["words"] != 511:
    raise SystemExit("Certificate scope/result changed")
print(json.dumps({"status":"pass", "artifacts":checked, "primary_sources_unchanged":True,
                  "certificate":result["status"], "remote_status":"Historical receipt only; this validator does not contact Reddit"}, indent=2))
