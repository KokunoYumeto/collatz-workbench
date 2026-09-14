from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


if not __debug__:
    raise RuntimeError(
        "validate_act42_recovery.py refuses optimized Python: fail-closed checks require __debug__"
    )


ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def aggregate_hash(directory: Path) -> tuple[int, int, str]:
    files = sorted((path for path in directory.iterdir() if path.is_file()), key=lambda p: p.name)
    value = hashlib.sha256()
    total = 0
    for path in files:
        data = path.read_bytes()
        value.update(path.name.encode("utf-8"))
        value.update(data)
        total += len(data)
    return len(files), total, value.hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def run(command: list[str], timeout: int = 900) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout,
        check=False,
    )


def numbered_ledger(
    relative: str,
    record_type: str,
    id_key: str,
    prefix: str,
    expected_count: int,
    expected_next: str,
) -> dict:
    rows = load_jsonl(ROOT / relative)
    header = next(row for row in rows if row.get("record_type") == "ledger_header")
    body = (
        [row for row in rows if id_key in row]
        if record_type == "*"
        else [row for row in rows if row.get("record_type") == record_type]
    )
    numbers = sorted(int(str(row[id_key]).removeprefix(prefix)) for row in body)
    if numbers != list(range(1, expected_count + 1)):
        raise ValueError(f"{relative}: complete ID set is not 1..{expected_count}")
    if header.get("next_id") != expected_next:
        raise ValueError(f"{relative}: stale next_id {header.get('next_id')}")
    return {
        "path": relative,
        "records": len(body),
        "maximum_id_number_from_complete_set": max(numbers),
        "next_id": header["next_id"],
        "physical_tail_is_not_used": True,
    }


def main() -> int:
    failures: list[str] = []
    evidence: dict[str, object] = {}

    def check(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    try:
        project = load_json(ROOT / "state/project_state.json")
        coverage = load_json(ROOT / "state/coverage.json")
        layers = {row["layer_id"]: row for row in coverage["layers"]}

        check(project.get("status") == "active", "project status is not active")
        check(project.get("completion_claimed") is False, "completion_claimed is not false")
        check(project.get("codex_goal", {}).get("status") == "active", "durable goal is not active")
        check(project.get("last_receipt_id") == "ACT-COL-000042", "project last receipt is not ACT42")
        check(project.get("current_checkpoint", {}).get("receipt_id") == "ACT-COL-000042", "current checkpoint is not ACT42")
        check(project.get("resource_policy", {}).get("lean_worker_private_working_set_limit_bytes") == 2_147_483_648, "Lean/Lake cap is not 2 GiB")
        check(project.get("resource_policy", {}).get("maximum_overlapping_lean_builds") == 1, "Lean/Lake overlap maximum is not one")
        check("11088-14011" in project.get("next_action", ""), "next Chatnotes range is not 11088-14011")

        checkpoint = project["current_checkpoint"]
        audit_path = ROOT / checkpoint["path"]
        recovery_record = checkpoint["fresh_context_recovery"]
        recovery_path = ROOT / recovery_record["path"]
        check(audit_path.is_file(), "ACT42 release audit is missing")
        check(recovery_path.is_file(), "ACT42 recovery record is missing")
        if audit_path.is_file():
            check(audit_path.stat().st_size == checkpoint["bytes"], "ACT42 audit byte mismatch")
            check(sha256(audit_path) == checkpoint["sha256"], "ACT42 audit hash mismatch")
        if recovery_path.is_file():
            check(recovery_path.stat().st_size == recovery_record["bytes"], "ACT42 recovery byte mismatch")
            check(sha256(recovery_path) == recovery_record["sha256"], "ACT42 recovery hash mismatch")

        receipts = load_jsonl(ROOT / "state/action_receipts.jsonl")
        receipt_numbers = [int(row["receipt_id"].rsplit("-", 1)[1]) for row in receipts]
        check(receipt_numbers == list(range(1, 43)), "action receipts are not physical append sequence 1..42")
        check(receipts[-1].get("receipt_id") == "ACT-COL-000042", "physical receipt line 42 is not ACT42")

        ledgers = [
            numbered_ledger("state/source_registry.jsonl", "source_document", "source_id", "SRC-COL-", 45, "SRC-COL-000046"),
            numbered_ledger("state/claims.jsonl", "claim", "claim_id", "CLM-COL-", 173, "CLM-COL-000174"),
            numbered_ledger("state/morphisms.jsonl", "morphism", "morphism_id", "MOR-COL-", 54, "MOR-COL-000055"),
            numbered_ledger("state/programmes.jsonl", "programme", "programme_id", "PRG-COL-", 2, "PRG-COL-0003"),
            numbered_ledger("state/chatnotes_intake.jsonl", "*", "intake_id", "CHATINT-COL-", 16, "CHATINT-COL-000017"),
        ]
        evidence["ledger_id_derivation"] = ledgers
        check(len(load_jsonl(ROOT / "state/topic_routes.jsonl")) == 3, "topic route count is not three")

        check(layers["LIT"].get("documents_read") == 45, "literature read count is not 45")
        check(layers["LIT"].get("documents_admitted") == 45, "literature admitted count is not 45")
        check(layers["CHAT"].get("programmes_reconstructed") == 2, "programme count is not two")
        check(layers["FORMAL"].get("artifacts_verified") == 24, "current certificate artifact count is not 24")
        check(layers["RECOVERY"].get("latest_receipt") == "ACT-COL-000042", "coverage recovery receipt is stale")

        expected_files = {
            "output/pdf/collatz_working_corpus.pdf": (1_574_554, "b9cf84f5d7815e5f930f3fa02edacd606a996837561f61339f3bde1d3b5d279c"),
            "research_companion/output/pdf/collatz_research_companion.pdf": (572_830, "8fecd942b3a8370a9457bdad32619640dbc1eb8f67c6f75e529c32e18b3c00b8"),
            "tmp/pdfs/act42_arctangent_final_root_20260830_02/main.log": (33_912, "84938e0339c66d8a8232525bb15cbfe5b2b1b8fc7b9e952fec09b535a1c37d47"),
            "tmp/pdfs/act42_arctangent_final_companion_20260830_01/main.log": (30_962, "0e5eccb6554a543865aa216a41b52e968e40488798d8087a904cf2673147df42"),
            "research_companion/MANIFEST.json": (1_673, "a1c9e4278d6312b2782152d20af224787af4ce7f6fbb85928e928379ac759087"),
            "raw/USR-0012.txt": (817, "cd726fce3faa5fead6897fab54816a63c5851ac822b886287920b4f6e159ff29"),
        }
        for relative, (size, digest) in expected_files.items():
            path = ROOT / relative
            check(path.is_file(), f"missing pinned file: {relative}")
            if path.is_file():
                check(path.stat().st_size == size, f"byte mismatch: {relative}")
                check(sha256(path) == digest, f"hash mismatch: {relative}")

        render_expected = {
            "tmp/qa/act42_release_root_160dpi_03/pages": (169, 56_045_726, "f9f56dd630033a98f2184045aacfc900ae35bad5ba8c9e4702b60538cb618f3a"),
            "tmp/qa/act42_release_root_160dpi_02/pages": (169, 56_031_234, "bb9e64efd29feabbf690d8872900dcae8410dcc2cb8e5d22fb9d21eaf148576e"),
            "tmp/qa/act42_release_root_160dpi_02/contact_sheets": (15, 16_753_484, "379209c92f4eb07ea7851b8111d3b4cff59fe4aa2b1d526f96bd1d8c3391f2fc"),
            "tmp/qa/act42_release_companion_200dpi_02/pages": (34, 13_693_216, "cfea596f8df909990fad359712b5854d0578964b8f2e667840655cc9d94c003e"),
            "tmp/qa/act42_release_companion_200dpi_02/contact_sheets": (3, 3_135_856, "a6fd5d3d33c74414491224b77ec78ba9047cc3c061f0d9e6ed5045211c0f9975"),
        }
        evidence["render_aggregate_rule"] = "SHA-256 over ordinal filename order, updating with UTF-8 filename bytes and then raw file bytes, without a delimiter"
        for relative, expected in render_expected.items():
            actual = aggregate_hash(ROOT / relative)
            check(actual == expected, f"render aggregate mismatch: {relative}: {actual}")

        root_pages = ROOT / "tmp/qa/act42_release_root_160dpi_03/pages"
        base_pages = ROOT / "tmp/qa/act42_release_root_160dpi_02/pages"
        changed: list[str] = []
        for final in sorted(root_pages.glob("*.png"), key=lambda p: p.name):
            base = base_pages / final.name
            if sha256(final) != sha256(base):
                changed.append(final.name)
        check(changed == ["page-060.png", "page-125.png"], f"unexpected final-root render delta: {changed}")
        evidence["root_render_delta"] = {"pixel_identical_pages": 167, "changed_pages": changed}

        for pdf, pages, font_rows in [
            ("output/pdf/collatz_working_corpus.pdf", 169, 27),
            ("research_companion/output/pdf/collatz_research_companion.pdf", 34, 22),
        ]:
            info = run(["pdfinfo", pdf])
            check(info.returncode == 0, f"pdfinfo failed: {pdf}")
            page_match = re.search(r"^Pages:\s+(\d+)$", info.stdout, re.MULTILINE)
            check(page_match is not None and int(page_match.group(1)) == pages, f"page count mismatch: {pdf}")
            fonts = run(["pdffonts", pdf])
            rows = [line for line in fonts.stdout.splitlines()[2:] if line.strip()]
            check(fonts.returncode == 0 and len(rows) == font_rows, f"font row mismatch: {pdf}")
            check(all(re.search(r"\s+yes\s+yes\s+yes\s+", row) for row in rows), f"font embedding/subset/Unicode failure: {pdf}")
            text = run(["pdftotext", pdf, "-"])
            leak_patterns = [
                r"\?\?", r"undefined citation", r"undefined reference", r"codex://",
                r"file://", r"C:\\Users", r"PLACEHOLDER", r"\bTBD\b", r"\bTODO\b",
                r"open obligation", r"proof obligation", r"conditional theorem",
                r"operatorname", r"qquad", "\ufffd",
            ]
            check(text.returncode == 0, f"pdftotext failed: {pdf}")
            for pattern in leak_patterns:
                check(re.search(pattern, text.stdout, re.IGNORECASE) is None, f"text leak {pattern!r}: {pdf}")

        normal_commands = [
            [PYTHON, "scripts/validate_state.py"],
            [PYTHON, "scripts/validate_chatnotes_intake.py"],
            [PYTHON, "certificates/chatnotes_symbolic_completion_checks.py"],
            [PYTHON, "research_companion/certificates/finite_actions_checks.py"],
            [PYTHON, "research_companion/certificates/arctangent_relation_lattice_checks.py"],
            [PYTHON, "research_companion/validate_package.py"],
        ]
        command_status = []
        for command in normal_commands:
            result = run(command)
            command_status.append({"command": command[1], "exit_code": result.returncode})
            check(result.returncode == 0, f"recovery command failed: {command[1]}\n{result.stderr[-1000:]}")
        evidence["normal_commands"] = command_status

        optimized_commands = [
            "certificates/chatnotes_symbolic_completion_checks.py",
            "research_companion/certificates/finite_actions_checks.py",
            "research_companion/certificates/arctangent_relation_lattice_checks.py",
            "research_companion/validate_package.py",
            "scripts/validate_act42_recovery.py",
        ]
        optimized_status = []
        for relative in optimized_commands[:-1]:
            result = run([PYTHON, "-O", relative])
            combined = result.stdout + result.stderr
            optimized_status.append({"command": relative, "exit_code": result.returncode})
            check(result.returncode != 0 and "refuses optimized Python" in combined, f"optimized run did not fail closed: {relative}")
        evidence["optimized_commands"] = optimized_status

        todo = (ROOT / "TODO.md").read_text(encoding="utf-8")
        check("dependency obligation" not in todo, "deprecated dependency-obligation wording remains in TODO")
        check("remains conditional on Crandall" not in todo, "deprecated conditional wording remains in TODO")
        check("ACT42 symbolic/arctangent checkpoint" in todo, "ACT42 checkpoint is missing from TODO")

    except Exception as error:
        failures.append(f"recovery exception: {error}")

    result = {
        "schema_version": "1.0",
        "checkpoint": "ACT-COL-000042",
        "status": "PASS" if not failures else "FAIL",
        "external_state_only": True,
        "compaction_or_summary_used_as_evidence": False,
        "evidence": evidence,
        "failure_count": len(failures),
        "failures": failures,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
