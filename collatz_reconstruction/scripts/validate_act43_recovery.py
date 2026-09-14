from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


if not __debug__:
    raise RuntimeError(
        "validate_act43_recovery.py refuses optimized Python: fail-closed checks require __debug__"
    )


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_RECEIPT = "ACT-COL-000043"
EXPECTED_COUNTS = {
    "sources": 49,
    "claims": 181,
    "morphisms": 62,
    "chatnotes_intake": 17,
    "programmes": 2,
    "topics": 4,
    "receipts": 43,
}
EXPECTED_ARTIFACTS = {
    "output/pdf/collatz_working_corpus.pdf": (
        1_630_444,
        "c03e4000464940377b2bdef87e19d0d92e9c4ddba7a570424ac5b0c72fbbf15e",
    ),
    "research_companion/output/pdf/collatz_research_companion.pdf": (
        636_148,
        "5c734ac770501539c36f9fe782395b26483caa09e8ec15d8602ded23eeb65441",
    ),
    "tmp/pdfs/act43_groupoid_motivic_final_root_20260830_03/main.log": (
        34_440,
        "ca2b648e364413cfe0fc25efc5d3a226a1f13229c4d092cfea8912c531444a64",
    ),
    "research_companion/tmp/pdfs/act43_groupoid_motivic_final_companion_20260830_04/main.log": (
        31_264,
        "e3443f945b40094a39cbebf0462b47815cdcfb23145190436c9b94dbd2942e43",
    ),
    "research_companion/MANIFEST.json": (
        2_037,
        "8e09c9c21fb6d08cfc66bb765945cf8fa44a96ee68260f35fc57870e617c18e9",
    ),
    "tex/chapters/05_chatnotes_groupoid_and_motivic_interfaces.tex": (
        17_776,
        "687ed7a0ac753d82f05c74b8ef570202a8791ec170eb0f9ffb95886c83e92e21",
    ),
    "research_companion/chapters/03_arithmetic_groupoids_and_toric_period_morphisms.tex": (
        22_563,
        "aad14427358e569931071abbaa14a1d0a05da3644702ce2aa5a7f2077c99dcd4",
    ),
    "research_companion/certificates/groupoid_motivic_interface_checks.py": (
        17_495,
        "ca460277a54e016a6ef84377cde5cc2e670f08c6cf3f57073f2a3c62d6400916",
    ),
    "intake/chatnotes/ZN-SYMMETRIES-GROUPOID-MOTIVIC-DIRECT-LOCATOR-AUDIT-06.md": (
        10_636,
        "e144f9ddc0f88392ef845fbde61880aa152c930c780283cd36a0427e01d4f2bb",
    ),
}
EXPECTED_PDFS = {
    "output/pdf/collatz_working_corpus.pdf": {"pages": 176, "font_rows": 29},
    "research_companion/output/pdf/collatz_research_companion.pdf": {
        "pages": 42,
        "font_rows": 22,
    },
}
EXPECTED_RENDERS = {
    "tmp/qa/act43_release_root_160dpi_01/pages": (
        176,
        58_530_850,
        "2dfc78d765c7c2f1b8ac90031708c7a87d557811234e054970c20c34a6bc6e77",
    ),
    "tmp/qa/act43_release_root_160dpi_01/contact_sheets": (
        15,
        7_804_730,
        "e24bc32ea6675abbf595a79d617517d3da04e3641c9a05c7e7b4a23d317b22a4",
    ),
    "tmp/qa/act43_release_companion_200dpi_01/pages": (
        42,
        17_174_756,
        "28e941bb4c111e2dc379166e01393959e6d1f67f735bc861b1ba4a2ccc82242b",
    ),
    "tmp/qa/act43_release_companion_200dpi_01/contact_sheets": (
        3,
        1_756_417,
        "d1b0941a25852c31bcdbc782045fb54228dbf7f4a641bbd8fa8f2d86217d0c2c",
    ),
}


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def aggregate_hash(directory: Path) -> tuple[int, int, str]:
    files = sorted(
        (path for path in directory.iterdir() if path.is_file()),
        key=lambda path: path.name,
    )
    value = hashlib.sha256()
    total = 0
    for path in files:
        data = path.read_bytes()
        value.update(path.name.encode("utf-8"))
        value.update(data)
        total += len(data)
    return len(files), total, value.hexdigest()


def load_json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def load_jsonl(relative: str) -> list[dict]:
    return [
        json.loads(line)
        for line in (ROOT / relative).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def run_json(relative: str, timeout: int = 900) -> dict:
    process = subprocess.run(
        [sys.executable, relative],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    if process.returncode != 0:
        raise RuntimeError(
            f"command failed: {relative}\n{process.stdout[-2000:]}\n{process.stderr[-2000:]}"
        )
    return json.loads(process.stdout)


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def check_id_ledger(
    relative: str,
    prefix: str,
    width: int,
    expected: int,
    failures: list[str],
    *,
    header: bool = True,
) -> None:
    rows = load_jsonl(relative)
    bodies = [row for row in rows if row.get("record_type") != "ledger_header"]
    key = {
        "SRC-COL-": "source_id",
        "CLM-COL-": "claim_id",
        "MOR-COL-": "morphism_id",
        "CHATINT-COL-": "intake_id",
        "PRG-COL-": "programme_id",
        "ACT-COL-": "receipt_id",
    }[prefix]
    ids = [row.get(key) for row in bodies]
    expected_ids = [f"{prefix}{number:0{width}d}" for number in range(1, expected + 1)]
    require(len(bodies) == expected, f"{relative}: body count mismatch", failures)
    require(set(ids) == set(expected_ids), f"{relative}: incomplete ID set", failures)
    if prefix in {"CHATINT-COL-", "ACT-COL-"}:
        require(ids == expected_ids, f"{relative}: physical ID order mismatch", failures)
    if header:
        headers = [row for row in rows if row.get("record_type") == "ledger_header"]
        require(len(headers) == 1, f"{relative}: expected one ledger header", failures)
        if headers:
            require(
                headers[0].get("next_id") == f"{prefix}{expected + 1:0{width}d}",
                f"{relative}: next_id mismatch",
                failures,
            )


def check_pdf(
    relative: str, expected: dict, failures: list[str]
) -> dict[str, object]:
    pdfinfo = shutil.which("pdfinfo")
    pdffonts = shutil.which("pdffonts")
    pdftotext = shutil.which("pdftotext")
    require(pdfinfo is not None, "pdfinfo unavailable", failures)
    require(pdffonts is not None, "pdffonts unavailable", failures)
    require(pdftotext is not None, "pdftotext unavailable", failures)
    if not (pdfinfo and pdffonts and pdftotext):
        return {}
    path = ROOT / relative
    info = subprocess.run(
        [pdfinfo, str(path)],
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    fonts = subprocess.run(
        [pdffonts, str(path)],
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    text = subprocess.run(
        [pdftotext, "-enc", "UTF-8", str(path), "-"],
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    require(info.returncode == 0, f"pdfinfo failed: {relative}", failures)
    require(fonts.returncode == 0, f"pdffonts failed: {relative}", failures)
    require(text.returncode == 0, f"pdftotext failed: {relative}", failures)
    page_match = re.search(r"^Pages:\s+(\d+)$", info.stdout, re.MULTILINE)
    pages = int(page_match.group(1)) if page_match else -1
    require(pages == expected["pages"], f"PDF page mismatch: {relative}", failures)
    font_rows = [
        line
        for line in fonts.stdout.splitlines()[2:]
        if line.strip() and not set(line.strip()) <= {"-"}
    ]
    require(
        len(font_rows) == expected["font_rows"],
        f"font-row mismatch: {relative}",
        failures,
    )
    bad_fonts = [
        line
        for line in font_rows
        if not re.search(r"\syes\s+yes\s+yes\s+\d+\s+\d+\s*$", line)
    ]
    require(not bad_fonts, f"unembedded/non-Unicode fonts: {relative}", failures)
    forbidden = {
        "double_question": r"\?\?",
        "codex_uri": r"codex://",
        "file_uri": r"file://",
        "private_path": r"C:\\Users",
        "todo": r"\bTODO\b",
        "tbd": r"\bTBD\b",
        "placeholder": r"\bplaceholder\b",
        "retired_open_term": r"\bopen obligation\b",
        "retired_proof_term": r"\bproof obligation\b",
        "retired_conditional_term": r"\bconditional theorem\b",
        "replacement_character": "\ufffd",
        "raw_operatorname": r"operatorname",
        "raw_qquad": r"qquad",
        "raw_begin": r"\\begin\{",
        "raw_cite": r"\\cite\{",
    }
    hits = {
        name: len(re.findall(pattern, text.stdout, re.IGNORECASE))
        for name, pattern in forbidden.items()
    }
    require(not any(hits.values()), f"forbidden PDF text hits: {relative}: {hits}", failures)
    return {"pages": pages, "font_rows": len(font_rows), "text_hits": hits}


def main() -> None:
    failures: list[str] = []
    evidence: dict[str, object] = {}

    project = load_json("state/project_state.json")
    coverage = load_json("state/coverage.json")
    require(project.get("last_receipt_id") == EXPECTED_RECEIPT, "last receipt mismatch", failures)
    require(project.get("completion_claimed") is False, "global completion was claimed", failures)
    resource = project.get("resource_policy", {})
    require(
        resource.get("lean_worker_private_working_set_limit_bytes") == 2_147_483_648,
        "Lean/Lake ceiling is not exactly 2 GiB",
        failures,
    )
    require(
        resource.get("maximum_overlapping_lean_builds") == 1,
        "Lean/Lake overlap limit mismatch",
        failures,
    )
    require(
        "current_hold_no_launch" in resource.get("required_resume_mode", ""),
        "coordination hold is absent",
        failures,
    )

    check_id_ledger("state/source_registry.jsonl", "SRC-COL-", 6, 49, failures)
    check_id_ledger("state/claims.jsonl", "CLM-COL-", 6, 181, failures)
    check_id_ledger("state/morphisms.jsonl", "MOR-COL-", 6, 62, failures)
    check_id_ledger("state/chatnotes_intake.jsonl", "CHATINT-COL-", 6, 17, failures)
    check_id_ledger("state/programmes.jsonl", "PRG-COL-", 4, 2, failures)
    check_id_ledger(
        "state/action_receipts.jsonl", "ACT-COL-", 6, 43, failures, header=False
    )
    topics = load_jsonl("state/topic_routes.jsonl")
    require(len(topics) == 4, "topic route count mismatch", failures)
    require(len({row.get("topic_id") for row in topics}) == 4, "duplicate topic ID", failures)

    for relative, (size, digest) in EXPECTED_ARTIFACTS.items():
        path = ROOT / relative
        require(path.is_file(), f"missing artifact: {relative}", failures)
        if path.is_file():
            require(path.stat().st_size == size, f"byte mismatch: {relative}", failures)
            require(sha256(path) == digest, f"SHA-256 mismatch: {relative}", failures)

    for relative, expected in EXPECTED_RENDERS.items():
        actual = aggregate_hash(ROOT / relative)
        require(actual == expected, f"render aggregate mismatch: {relative}: {actual}", failures)

    pdf_evidence = {
        relative: check_pdf(relative, expected, failures)
        for relative, expected in EXPECTED_PDFS.items()
    }
    evidence["pdfs"] = pdf_evidence

    checkpoint = project.get("current_checkpoint", {})
    for key in ("path", "bytes", "sha256"):
        require(key in checkpoint, f"checkpoint missing {key}", failures)
    if checkpoint.get("path"):
        checkpoint_path = ROOT / checkpoint["path"]
        require(checkpoint_path.is_file(), "checkpoint audit missing", failures)
        if checkpoint_path.is_file():
            require(
                checkpoint_path.stat().st_size == checkpoint.get("bytes")
                and sha256(checkpoint_path) == checkpoint.get("sha256"),
                "checkpoint audit identity mismatch",
                failures,
            )
    for record_name in ("fresh_context_recovery", "validation_transcript"):
        record = checkpoint.get(record_name, {})
        path = ROOT / record.get("path", "__missing__")
        require(path.is_file(), f"{record_name} missing", failures)
        if path.is_file():
            require(
                path.stat().st_size == record.get("bytes")
                and sha256(path) == record.get("sha256"),
                f"{record_name} identity mismatch",
                failures,
            )

    lit = next(layer for layer in coverage["layers"] if layer["layer_id"] == "LIT")
    formal = next(layer for layer in coverage["layers"] if layer["layer_id"] == "FORMAL")
    syn = next(layer for layer in coverage["layers"] if layer["layer_id"] == "SYN")
    recovery = next(layer for layer in coverage["layers"] if layer["layer_id"] == "RECOVERY")
    require(lit.get("documents_read") == 49, "literature coverage count mismatch", failures)
    require(formal.get("artifacts_verified") == 25, "certificate coverage count mismatch", failures)
    require(syn.get("working_pdf_pages") == 176, "working PDF coverage mismatch", failures)
    require(
        syn.get("research_companion_pdf_pages") == 42,
        "companion PDF coverage mismatch",
        failures,
    )
    require(recovery.get("latest_receipt") == EXPECTED_RECEIPT, "recovery receipt mismatch", failures)

    if not failures:
        state = run_json("scripts/validate_state.py")
        chat = run_json("scripts/validate_chatnotes_intake.py")
        groupoid = run_json(
            "research_companion/certificates/groupoid_motivic_interface_checks.py"
        )
        package = run_json("research_companion/validate_package.py", timeout=1200)
        require(state.get("status") == "pass" and state.get("failure_count") == 0, "state validator failed", failures)
        require(chat.get("status") == "pass" and chat.get("failure_count") == 0, "Chatnotes validator failed", failures)
        require(groupoid.get("status") == "PASS", "groupoid/motivic certificate failed", failures)
        require(package.get("status") == "PASS", "companion package validator failed", failures)
        evidence["validators"] = {
            "state_warning_count": state.get("warning_count"),
            "chatnotes_records": chat.get("records"),
            "groupoid_check_families": len(groupoid.get("checks", {})),
            "package_manifested_source_files": package.get("manifested_source_files"),
        }

    result = {
        "schema_version": "1.0",
        "checkpoint": EXPECTED_RECEIPT,
        "status": "pass" if not failures else "fail",
        "expected_counts": EXPECTED_COUNTS,
        "render_aggregate_rule": "SHA-256 over ordinal filename order, updating with UTF-8 filename bytes and then raw file bytes, without a delimiter",
        "evidence": evidence,
        "failure_count": len(failures),
        "failures": failures,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
