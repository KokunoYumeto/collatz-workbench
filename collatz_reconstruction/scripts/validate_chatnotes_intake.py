from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
LEDGER = PROJECT / "state" / "chatnotes_intake.jsonl"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def physical_lines(path: Path) -> int:
    count = 0
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            count += block.count(b"\n")
    if path.stat().st_size == 0:
        return 0
    with path.open("rb") as handle:
        handle.seek(-1, 2)
        trailing_lf = handle.read(1) == b"\n"
    return count if trailing_lf else count + 1


def resolve(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else PROJECT / path


def main() -> int:
    failures: list[str] = []
    records: list[dict] = []
    for line_number, line in enumerate(
        LEDGER.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as error:
            failures.append(f"{LEDGER}:{line_number}: {error}")

    headers = [row for row in records if row.get("record_type") == "ledger_header"]
    if len(headers) != 1:
        failures.append(f"expected one ledger header, found {len(headers)}")
        header: dict = {}
    else:
        header = headers[0]

    body = [row for row in records if row.get("record_type") != "ledger_header"]
    by_id = {row.get("intake_id"): row for row in body}
    ids = [row.get("intake_id") for row in body]
    pattern = re.compile(r"^CHATINT-COL-(\d{6})$")
    numbers: list[int] = []
    for value in ids:
        match = pattern.fullmatch(str(value))
        if match is None:
            failures.append(f"missing or malformed intake_id: {value}")
        else:
            numbers.append(int(match.group(1)))
    if len(ids) != len(set(ids)):
        failures.append("duplicate intake_id")
    if numbers != list(range(1, len(numbers) + 1)):
        failures.append(f"noncontiguous or out-of-order intake IDs: {numbers}")
    expected_next = f"CHATINT-COL-{len(numbers) + 1:06d}"
    if header.get("next_id") != expected_next:
        failures.append(
            f"header next_id {header.get('next_id')} does not equal {expected_next}"
        )

    sources = {
        row["intake_id"]: row
        for row in body
        if row.get("record_type") == "chatnotes_source_identity"
    }
    for source_id, row in sources.items():
        path = resolve(row["path"])
        if not path.is_file():
            failures.append(f"missing raw source {source_id}: {path}")
            continue
        if path.stat().st_size != row.get("bytes"):
            failures.append(f"byte mismatch for {source_id}: {path}")
        if sha256(path) != str(row.get("sha256", "")).lower():
            failures.append(f"hash mismatch for {source_id}: {path}")
        if physical_lines(path) != row.get("physical_lines"):
            failures.append(f"physical-line mismatch for {source_id}: {path}")
        if row.get("mathematical_authority") != "none_without_independent_proof_or_source":
            failures.append(f"raw source improperly assigned authority: {source_id}")

    segment_intervals: dict[str, list[tuple[int, int]]] = {}
    for row in body:
        if row.get("record_type") != "chatnotes_segment_intake":
            continue
        source_id = row.get("source_intake_id")
        if source_id not in sources:
            failures.append(f"segment references unknown source: {row.get('intake_id')}")
            continue
        start = row.get("physical_line_start")
        end = row.get("physical_line_end")
        if not isinstance(start, int) or not isinstance(end, int) or not (1 <= start <= end):
            failures.append(f"invalid segment interval: {row.get('intake_id')}")
        elif end > sources[source_id]["physical_lines"]:
            failures.append(f"segment exceeds source: {row.get('intake_id')}")
        else:
            segment_intervals.setdefault(source_id, []).append((start, end))

    expected_complete_intervals = {
        "CHATINT-COL-000001": [(1, 6000), (6001, 12000), (12001, 17437)],
        "CHATINT-COL-000002": [(1, 3021)],
    }
    for source_id, expected in expected_complete_intervals.items():
        observed = sorted(segment_intervals.get(source_id, []))
        if observed != expected:
            failures.append(
                f"segment coverage for {source_id} is {observed}, expected {expected}"
            )

    for row in body:
        report_path = row.get("report_path")
        if report_path is not None:
            path = resolve(report_path)
            if not path.is_file():
                failures.append(f"missing report: {path}")
                continue
            if path.stat().st_size != row.get("report_bytes"):
                failures.append(f"report byte mismatch: {path}")
            if sha256(path) != str(row.get("report_sha256", "")).lower():
                failures.append(f"report hash mismatch: {path}")
        admission = str(row.get("admission_status", ""))
        if admission and "unadmitted" not in admission and admission != "no_mathematical_admission":
            failures.append(
                f"intake record has non-fail-closed admission status: {row.get('intake_id')}"
            )

    route_rows = [row for row in body if row.get("record_type") == "route_lookup"]
    for row in route_rows:
        for relative, expected_hash in row.get("frozen_hashes", {}).items():
            path = resolve(relative)
            if not path.is_file() or sha256(path) != expected_hash.lower():
                failures.append(f"frozen route mismatch: {relative}")

    frozen_route_ids: set[str] = set()
    for relative in ("state/index_routes.jsonl", "state/document_routes.jsonl"):
        for line in resolve(relative).read_text(encoding="utf-8").splitlines():
            if line.strip():
                frozen_route_ids.add(json.loads(line)["route_id"])

    for row in body:
        if row.get("record_type") == "routed_chatnotes_package_intake":
            for route_id in row.get("route_ids", []):
                if route_id not in frozen_route_ids:
                    failures.append(f"unknown frozen route ID: {route_id}")
        if row.get("record_type") != "chatnotes_code_audit":
            continue
        parent = by_id.get(row.get("parent_intake_id"))
        if not parent or parent.get("record_type") != "routed_chatnotes_package_intake":
            failures.append(
                f"code audit has invalid package parent: {row.get('intake_id')}"
            )
            continue
        package_root = resolve(parent["package_root"])
        for file_record in row.get("files_read_line_by_line", []):
            path = package_root / file_record["path"]
            if not path.is_file():
                failures.append(f"missing audited code file: {path}")
                continue
            if path.stat().st_size != file_record.get("bytes"):
                failures.append(f"audited code byte mismatch: {path}")
            if sha256(path) != str(file_record.get("sha256", "")).lower():
                failures.append(f"audited code hash mismatch: {path}")

    directive = PROJECT / "raw" / "USR-0004.txt"
    expected_directive_hash = (
        "02ae6e9787e50ad5a402e72d01b9816501b63b26a6eff0ff93692d808f74409c"
    )
    if not directive.is_file() or sha256(directive) != expected_directive_hash:
        failures.append("USR-0004 is missing or changed")

    report = {
        "schema_version": "1.0",
        "status": "pass" if not failures else "fail",
        "records": len(body),
        "sources": len(sources),
        "source_physical_lines": sum(row["physical_lines"] for row in sources.values()),
        "segment_reports": sum(
            row.get("record_type") == "chatnotes_segment_intake" for row in body
        ),
        "programme_admissions": 0,
        "failure_count": len(failures),
        "failures": failures,
    }
    print(json.dumps(report, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
