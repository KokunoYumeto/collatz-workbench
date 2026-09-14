from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    records = []
    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as error:
            raise ValueError(f"{path}:{line_number}: {error}") from error
    return records


def resolve_project_path(value: str) -> Path:
    candidate = Path(value)
    return candidate if candidate.is_absolute() else (PROJECT / candidate).resolve()


def load_frozen_publication_unit_ids(
    topic_route_records: list[dict], failures: list[str]
) -> tuple[set[str], bool]:
    entrypoint_values = {
        str(row.get("corpus_entrypoint", "")).strip()
        for row in topic_route_records
        if str(row.get("corpus_entrypoint", "")).strip()
    }
    if len(entrypoint_values) != 1:
        failures.append(
            "topic routes do not identify exactly one canonical corpus entrypoint"
        )
        return set(), False
    try:
        entrypoint_path = resolve_project_path(next(iter(entrypoint_values)))
        entrypoint = json.loads(entrypoint_path.read_text(encoding="utf-8"))
        # Queries can route either corpus layer. The older implementation
        # admitted only research IDs, spuriously rejecting valid local hits.
        # Authenticate both ledgers using their own entrypoint hash pins.
        unit_rows = []
        for layer in ("research_literature", "local_unpublished_work"):
            graph = entrypoint["layers"][layer]["publication_graph"]
            units_path = Path(entrypoint["stable_access_root"]) / graph["publication_units"]
            if not units_path.is_file():
                failures.append(f"frozen {layer} publication-unit ledger is missing: {units_path}")
                return set(), False
            expected_hash = str(graph["publication_units_sha256"]).lower()
            if sha256(units_path) != expected_hash:
                failures.append(f"frozen {layer} publication-unit ledger hash mismatch: {units_path}")
                return set(), False
            layer_rows = read_jsonl(units_path)
            layer_ids = [row.get("id") for row in layer_rows]
            if None in layer_ids or len(layer_ids) != len(set(layer_ids)):
                failures.append(f"frozen {layer} publication-unit IDs are missing or duplicated")
                return set(), False
            unit_rows.extend(layer_rows)
        unit_ids = [row.get("id") for row in unit_rows]
        # A single content-identified publication unit may occur in both
        # independently pinned layers. Uniqueness is required within each.
        if None in unit_ids:
            failures.append("frozen publication-unit IDs are missing")
            return set(), False
        malformed = [
            unit_id
            for unit_id in unit_ids
            if re.fullmatch(r"PUBUNIT-[0-9A-F]{24}", str(unit_id)) is None
        ]
        if malformed:
            failures.append(f"malformed frozen publication-unit IDs: {malformed[:5]}")
            return set(), False
        return set(unit_ids), True
    except Exception as error:
        failures.append(f"frozen publication-unit validation failed: {error}")
        return set(), False


def validate_numbered_records(
    records: list[dict],
    *,
    record_type: str,
    id_key: str,
    prefix: str,
    width: int,
    failures: list[str],
) -> tuple[dict | None, list[dict]]:
    header = next((row for row in records if row.get("record_type") == "ledger_header"), None)
    body = [row for row in records if row.get("record_type") == record_type]
    if header is None:
        failures.append(f"{prefix} ledger header is missing")
    ids = [row.get(id_key) for row in body]
    if None in ids:
        failures.append(f"{prefix} record missing {id_key}")
        return header, body
    if len(ids) != len(set(ids)):
        failures.append(f"duplicate {id_key} in {prefix} ledger")
    pattern = re.compile(rf"^{re.escape(prefix)}(\d{{{width}}})$")
    numbers: list[int] = []
    for value in ids:
        match = pattern.fullmatch(str(value))
        if match is None:
            failures.append(f"malformed {id_key}: {value}")
        else:
            numbers.append(int(match.group(1)))
    if numbers and sorted(numbers) != list(range(1, max(numbers) + 1)):
        failures.append(f"noncontiguous {prefix} identifiers: {sorted(numbers)}")
    if header is not None:
        expected_next = f"{prefix}{(max(numbers, default=0) + 1):0{width}d}"
        if header.get("next_id") != expected_next:
            failures.append(
                f"{prefix} header next_id is {header.get('next_id')}, expected {expected_next}"
            )
    return header, body


def assert_acyclic_claim_graph(claims: list[dict], failures: list[str]) -> None:
    graph = {row["claim_id"]: list(row.get("dependencies", [])) for row in claims}
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str, trail: list[str]) -> None:
        if node in visited:
            return
        if node in visiting:
            failures.append("claim dependency cycle: " + " -> ".join(trail + [node]))
            return
        visiting.add(node)
        for dependency in graph.get(node, []):
            visit(dependency, trail + [node])
        visiting.remove(node)
        visited.add(node)

    for node in graph:
        visit(node, [])


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []
    state_path = PROJECT / "state" / "project_state.json"
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except Exception as error:
        print(json.dumps({"status": "fail", "failures": [str(error)]}, indent=2))
        return 1

    if state.get("completion_claimed") is not False:
        failures.append("completion_claimed must remain false before the release gate")

    codex_goal = state.get("codex_goal")
    if not isinstance(codex_goal, dict):
        failures.append("project_state.codex_goal must be an object")
    else:
        goal_thread_id = codex_goal.get("thread_id")
        if not isinstance(goal_thread_id, str) or not goal_thread_id.strip():
            failures.append("project_state.codex_goal.thread_id must be a nonempty string")
        if state.get("completion_claimed") is False and codex_goal.get("status") != "active":
            failures.append("codex goal must remain active while completion_claimed is false")

        durable_goal_path = PROJECT / "DURABLE_GOAL.md"
        if durable_goal_path.is_file() and isinstance(goal_thread_id, str):
            durable_goal_text = durable_goal_path.read_text(encoding="utf-8")
            if goal_thread_id not in durable_goal_text:
                failures.append("active Codex goal ID is missing from DURABLE_GOAL.md")

    for directive in state.get("raw_directives", []):
        path = resolve_project_path(directive["path"])
        if not path.is_file():
            failures.append(f"missing directive source: {path}")
            continue
        expected = directive.get("sha256")
        if expected and sha256(path) != expected:
            failures.append(f"directive hash mismatch: {path}")

    for route_input in state.get("routing_inputs", []):
        path = resolve_project_path(route_input["path"])
        if not path.is_file():
            failures.append(f"missing routing input: {path}")
            continue
        if sha256(path) != route_input["sha256"]:
            failures.append(f"routing input hash mismatch: {path}")

    frozen_route_artifacts = state.get("frozen_route_artifacts")
    required_frozen_paths = {
        "state/index_routes.jsonl",
        "state/document_routes.jsonl",
        "state/index_snapshot.json",
    }
    if not isinstance(frozen_route_artifacts, list):
        failures.append("project_state.frozen_route_artifacts must be a list")
    else:
        observed_frozen_paths: set[str] = set()
        for artifact in frozen_route_artifacts:
            relative_path = artifact.get("path")
            if not isinstance(relative_path, str):
                failures.append("frozen route artifact is missing a string path")
                continue
            if relative_path in observed_frozen_paths:
                failures.append(f"duplicate frozen route artifact anchor: {relative_path}")
                continue
            observed_frozen_paths.add(relative_path)
            path = resolve_project_path(relative_path)
            if not path.is_file():
                failures.append(f"missing frozen route artifact: {path}")
                continue
            if artifact.get("status") != "immutable_frozen_derivative":
                failures.append(f"frozen route artifact has nonimmutable status: {relative_path}")
            if path.stat().st_size != artifact.get("bytes"):
                failures.append(f"frozen route artifact byte mismatch: {path}")
            if sha256(path) != artifact.get("sha256"):
                failures.append(f"frozen route artifact hash mismatch: {path}")
        if observed_frozen_paths != required_frozen_paths:
            failures.append(
                "frozen route artifact anchors differ from the required set: "
                f"{sorted(observed_frozen_paths)}"
            )

    required = [
        PROJECT / "DIRECTIVES.md",
        PROJECT / "ARTIFACT_ARCHITECTURE.md",
        PROJECT / "DURABLE_GOAL.md",
        PROJECT / "WORKFLOW.md",
        PROJECT / "TODO.md",
        PROJECT / state["live_artifact"],
        PROJECT / "state" / "coverage.json",
        PROJECT / "state" / "index_routes.jsonl",
        PROJECT / "state" / "document_routes.jsonl",
        PROJECT / "state" / "topic_routes.jsonl",
        PROJECT / "state" / "index_snapshot.json",
        PROJECT / "state" / "source_registry.jsonl",
        PROJECT / "state" / "unresolved_dependencies.jsonl",
        PROJECT / "state" / "legacy_status_migration.jsonl",
        PROJECT / "state" / "proof_obligations.jsonl",
    ]
    for path in required:
        if not path.is_file():
            failures.append(f"missing required project file: {path}")

    route_records = []
    document_records = []
    topic_route_records = []
    try:
        route_records = read_jsonl(PROJECT / "state" / "index_routes.jsonl")
        document_records = read_jsonl(PROJECT / "state" / "document_routes.jsonl")
        topic_route_records = read_jsonl(PROJECT / "state" / "topic_routes.jsonl")
    except Exception as error:
        failures.append(str(error))

    for label, records in (
        ("route", route_records),
        ("document route", document_records),
    ):
        ids = [record.get("route_id") for record in records]
        if None in ids:
            failures.append(f"{label} record missing route_id")
        if len(ids) != len(set(ids)):
            failures.append(f"duplicate {label} route_id")

    for label, records in (
        ("route", route_records),
        ("document route", document_records),
    ):
        for record in records:
            if label == "route" and record.get("admission_status") != "not_admitted_from_metadata":
                failures.append(
                    "routing record improperly admitted from metadata: "
                    f"{record.get('route_id')}"
                )
            path_records = record.get("paths", [])
            if not path_records:
                failures.append(f"{label} has no indexed manifestations: {record.get('route_id')}")
                continue
            surviving = 0
            for path_record in path_records:
                path = Path(path_record["absolute_path"])
                if not path.exists():
                    warnings.append(
                        f"{label} manifestation absent after index freeze: "
                        f"{record.get('route_id')}: {path}"
                    )
                    continue
                surviving += 1
                expected = path_record.get("sha256")
                if expected and path.is_file() and sha256(path) != expected:
                    failures.append(f"indexed {label} hash mismatch: {path}")
            if surviving == 0:
                failures.append(
                    f"{label} has no surviving indexed manifestation: {record.get('route_id')}"
                )

    topic_required = {
        "schema_version",
        "topic_id",
        "topic",
        "workspace",
        "corpus_entrypoint",
        "updated_utc",
        "queries",
        "sources",
        "unresolved_dependencies",
        "refresh_reason",
    }
    query_required = {
        "query",
        "layer",
        "index_level",
        "executed_utc",
        "reason",
        "result_unit_ids",
    }
    topic_source_required = {
        "source_class",
        "publication_unit_or_source_id",
        "exact_locators",
        "relevance_edge",
        "toc_or_section_check",
        "reading_status",
        "dependencies",
        "claim_or_proof_crosswalk_ids",
    }
    topic_ids = [row.get("topic_id") for row in topic_route_records]
    if not topic_route_records:
        failures.append("state/topic_routes.jsonl has no topic records")
    if None in topic_ids or len(topic_ids) != len(set(topic_ids)):
        failures.append("topic route IDs are missing or duplicated")
    for topic_route in topic_route_records:
        missing = sorted(topic_required - topic_route.keys())
        if missing:
            failures.append(f"topic route {topic_route.get('topic_id')} missing fields: {missing}")
        if topic_route.get("schema_version") != 1:
            failures.append(f"topic route {topic_route.get('topic_id')} has non-v1 schema")
        if not str(topic_route.get("topic", "")).strip():
            failures.append(f"topic route {topic_route.get('topic_id')} has empty topic")
        queries = topic_route.get("queries", [])
        if not isinstance(queries, list) or not queries:
            failures.append(f"topic route {topic_route.get('topic_id')} has no queries")
        else:
            for query in queries:
                query_missing = sorted(query_required - query.keys())
                if query_missing:
                    failures.append(
                        f"topic route {topic_route.get('topic_id')} query missing fields: "
                        f"{query_missing}"
                    )
                if query.get("index_level") not in {"canonical", "staging", "both"}:
                    failures.append(
                        f"topic route {topic_route.get('topic_id')} query has invalid index level"
                    )
        topic_sources = topic_route.get("sources", [])
        if not isinstance(topic_sources, list) or not topic_sources:
            failures.append(f"topic route {topic_route.get('topic_id')} has no sources")
        else:
            for topic_source in topic_sources:
                source_missing = sorted(topic_source_required - topic_source.keys())
                if source_missing:
                    failures.append(
                        f"topic route {topic_route.get('topic_id')} source missing fields: "
                        f"{source_missing}"
                    )
                if not topic_source.get("exact_locators"):
                    failures.append(
                        f"topic route {topic_route.get('topic_id')} source has no exact locators"
                    )

    ledger_names = (
        "claims.jsonl",
        "morphisms.jsonl",
        "unresolved_dependencies.jsonl",
        "legacy_status_migration.jsonl",
        "programmes.jsonl",
        "action_receipts.jsonl",
    )
    for name in ledger_names:
        try:
            records = read_jsonl(PROJECT / "state" / name)
            if not records:
                failures.append(f"empty ledger without header: {name}")
        except Exception as error:
            failures.append(str(error))

    try:
        source_rows = read_jsonl(PROJECT / "state" / "source_registry.jsonl")
        _, sources = validate_numbered_records(
            source_rows,
            record_type="source_document",
            id_key="source_id",
            prefix="SRC-COL-",
            width=6,
            failures=failures,
        )
    except Exception as error:
        failures.append(str(error))
        sources = []

    try:
        claim_rows = read_jsonl(PROJECT / "state" / "claims.jsonl")
        _, claims = validate_numbered_records(
            claim_rows,
            record_type="claim",
            id_key="claim_id",
            prefix="CLM-COL-",
            width=6,
            failures=failures,
        )
    except Exception as error:
        failures.append(str(error))
        claims = []

    try:
        morphism_rows = read_jsonl(PROJECT / "state" / "morphisms.jsonl")
        _, morphisms = validate_numbered_records(
            morphism_rows,
            record_type="morphism",
            id_key="morphism_id",
            prefix="MOR-COL-",
            width=6,
            failures=failures,
        )
    except Exception as error:
        failures.append(str(error))
        morphisms = []

    try:
        gap_rows = read_jsonl(PROJECT / "state" / "unresolved_dependencies.jsonl")
        _, gaps = validate_numbered_records(
            gap_rows,
            record_type="unresolved_dependency",
            id_key="gap_id",
            prefix="GAP-COL-",
            width=6,
            failures=failures,
        )
    except Exception as error:
        failures.append(str(error))
        gaps = []

    legacy_mappings = []
    try:
        legacy_rows = read_jsonl(PROJECT / "state" / "legacy_status_migration.jsonl")
        if not legacy_rows or legacy_rows[0].get("ledger") != "legacy_status_migration":
            failures.append("legacy status migration ledger has no valid header")
        else:
            legacy_header = legacy_rows[0]
            legacy_mappings = legacy_rows[1:]
            legacy_path = resolve_project_path(legacy_header["source_path"])
            if not legacy_path.is_file():
                failures.append(f"legacy status source is missing: {legacy_path}")
            else:
                if legacy_path.stat().st_size != legacy_header.get("source_bytes"):
                    failures.append(f"legacy status source byte mismatch: {legacy_path}")
                if sha256(legacy_path) != legacy_header.get("source_sha256"):
                    failures.append(f"legacy status source hash mismatch: {legacy_path}")
            legacy_ids = [row.get("legacy_id") for row in legacy_mappings]
            expected_legacy_ids = [f"PO-COL-{number:06d}" for number in range(1, 9)]
            if legacy_ids != expected_legacy_ids:
                failures.append(
                    "legacy status migration IDs are not the exact historical sequence: "
                    f"{legacy_ids}"
                )
            if legacy_header.get("source_record_count") != len(legacy_mappings):
                failures.append("legacy status migration count disagrees with its header")
    except Exception as error:
        failures.append(str(error))

    try:
        receipt_rows = read_jsonl(PROJECT / "state" / "action_receipts.jsonl")
        receipt_ids = [row.get("receipt_id") for row in receipt_rows]
        if len(receipt_ids) != len(set(receipt_ids)) or None in receipt_ids:
            failures.append("action receipt IDs are missing or duplicated")
        receipt_numbers = []
        receipt_pattern = re.compile(r"^ACT-COL-(\d{6})$")
        for receipt_id in receipt_ids:
            match = receipt_pattern.fullmatch(str(receipt_id))
            if match is None:
                failures.append(f"malformed receipt_id: {receipt_id}")
            else:
                receipt_numbers.append(int(match.group(1)))
        if receipt_numbers and sorted(receipt_numbers) != list(
            range(1, max(receipt_numbers) + 1)
        ):
            failures.append(f"noncontiguous action receipt IDs: {sorted(receipt_numbers)}")
        if receipt_numbers:
            expected_last_receipt = f"ACT-COL-{max(receipt_numbers):06d}"
            if state.get("last_receipt_id") != expected_last_receipt:
                failures.append(
                    "project_state.last_receipt_id does not match the latest action receipt: "
                    f"{state.get('last_receipt_id')} != {expected_last_receipt}"
                )
    except Exception as error:
        failures.append(str(error))

    source_ids = {row.get("source_id") for row in sources}
    claim_ids = {row.get("claim_id") for row in claims}
    morphism_ids = {row.get("morphism_id") for row in morphisms}
    gap_ids = {row.get("gap_id") for row in gaps}
    publication_unit_ids, publication_units_loaded = load_frozen_publication_unit_ids(
        topic_route_records, failures
    )
    frozen_local_route_ids = {
        row.get("route_id") for row in route_records + document_records
    }
    for source in sources:
        route_ids = source.get("route_ids", [])
        if not isinstance(route_ids, list):
            failures.append(f"{source.get('source_id')} route_ids is not a list")
            continue
        for route_id in route_ids:
            if isinstance(route_id, str) and route_id.startswith("PUBUNIT-"):
                if publication_units_loaded and route_id not in publication_unit_ids:
                    failures.append(
                        f"{source.get('source_id')} references unknown frozen publication unit "
                        f"{route_id}"
                    )
            elif route_id not in frozen_local_route_ids:
                failures.append(
                    f"{source.get('source_id')} references unknown frozen route {route_id}"
                )
        canonical_unit_id = source.get("route_integrity", {}).get(
            "canonical_publication_unit_id"
        )
        if canonical_unit_id is not None and canonical_unit_id not in route_ids:
            failures.append(
                f"{source.get('source_id')} canonical publication unit is absent from route_ids: "
                f"{canonical_unit_id}"
            )
        if (
            canonical_unit_id is not None
            and publication_units_loaded
            and canonical_unit_id not in publication_unit_ids
        ):
            failures.append(
                f"{source.get('source_id')} references unknown canonical publication unit: "
                f"{canonical_unit_id}"
            )

    chatnotes_validator_status = "not_run"
    try:
        chatnotes_result = subprocess.run(
            [sys.executable, str(PROJECT / "scripts" / "validate_chatnotes_intake.py")],
            cwd=PROJECT,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        chatnotes_report = json.loads(chatnotes_result.stdout)
        chatnotes_validator_status = str(chatnotes_report.get("status", "unknown"))
        if chatnotes_result.returncode != 0 or chatnotes_validator_status != "pass":
            failures.append(
                "chatnotes intake validator failed: "
                + json.dumps(chatnotes_report.get("failures", []), ensure_ascii=False)
            )
    except Exception as error:
        chatnotes_validator_status = "error"
        failures.append(f"chatnotes intake validator invocation failed: {error}")

    chatnotes_intake_ids: set[str] = set()
    try:
        chatnotes_intake_ids = {
            row.get("intake_id")
            for row in read_jsonl(PROJECT / "state" / "chatnotes_intake.jsonl")
            if row.get("intake_id")
        }
    except Exception as error:
        failures.append(f"chatnotes intake reference validation failed: {error}")

    for topic_route in topic_route_records:
        for query in topic_route.get("queries", []):
            result_unit_ids = query.get("result_unit_ids", [])
            if not isinstance(result_unit_ids, list) or not result_unit_ids:
                failures.append(
                    f"topic route {topic_route.get('topic_id')} query has no result_unit_ids: "
                    f"{query.get('query')}"
                )
                continue
            for unit_id in result_unit_ids:
                if publication_units_loaded and unit_id not in publication_unit_ids:
                    failures.append(
                        f"topic route {topic_route.get('topic_id')} query references unknown "
                        f"frozen publication unit {unit_id}"
                    )
        for topic_source in topic_route.get("sources", []):
            reference = topic_source.get("publication_unit_or_source_id")
            if isinstance(reference, str) and reference.startswith("SRC-COL-"):
                if reference not in source_ids:
                    failures.append(
                        f"topic route {topic_route.get('topic_id')} references unknown source {reference}"
                    )
            elif isinstance(reference, str) and reference.startswith("CHATINT-COL-"):
                if reference not in chatnotes_intake_ids:
                    failures.append(
                        f"topic route {topic_route.get('topic_id')} references unknown intake {reference}"
                    )
            elif isinstance(reference, str) and reference.startswith("PUBUNIT-"):
                if publication_units_loaded and reference not in publication_unit_ids:
                    failures.append(
                        f"topic route {topic_route.get('topic_id')} references unknown frozen "
                        f"publication unit {reference}"
                    )
            else:
                failures.append(
                    f"topic route {topic_route.get('topic_id')} has untyped source reference {reference}"
                )
            for claim_id in topic_source.get("claim_or_proof_crosswalk_ids", []):
                if claim_id not in claim_ids:
                    failures.append(
                        f"topic route {topic_route.get('topic_id')} references unknown claim {claim_id}"
                    )

    for source in sources:
        for manifestation in source.get("manifestations", []):
            path = resolve_project_path(manifestation["path"])
            if not path.is_file():
                failures.append(f"source manifestation missing: {path}")
                continue
            if path.stat().st_size != manifestation.get("bytes"):
                failures.append(f"source manifestation byte mismatch: {path}")
            if sha256(path) != manifestation.get("sha256"):
                failures.append(f"source manifestation hash mismatch: {path}")

    tex_labels_by_path: dict[Path, set[str]] = {}
    # The separately authored Tao preprint is a third authorized proof root.
    # Keep path and exact-label checks for it, as for the two workbench texts.
    for tex_root in (PROJECT / "tex", PROJECT / "research_companion", PROJECT / "preprints" / "tao_clock_audit"):
        for path in tex_root.rglob("*.tex"):
            tex_labels_by_path[path.resolve()] = set(
                re.findall(r"\\label\{([^}]+)\}", path.read_text(encoding="utf-8"))
            )

    def validate_proof_locator(owner_id: str, locator: object) -> None:
        if not isinstance(locator, dict):
            failures.append(f"{owner_id} proof locator is not an object")
            return
        relative_path = locator.get("path")
        label = locator.get("label")
        if not isinstance(relative_path, str) or not relative_path:
            failures.append(f"{owner_id} proof locator has no path")
            return
        path = resolve_project_path(relative_path)
        if not path.is_file():
            failures.append(f"{owner_id} proof path missing: {path}")
            return
        labels = tex_labels_by_path.get(path.resolve())
        if labels is None:
            failures.append(f"{owner_id} proof path is outside the validated TeX roots: {path}")
        elif label not in labels:
            failures.append(f"{owner_id} proof label missing from {path}: {label}")

    for claim in claims:
        for source_id in claim.get("source_ids", []):
            if source_id not in source_ids:
                failures.append(f"{claim['claim_id']} references unknown source {source_id}")
        for dependency in claim.get("dependencies", []):
            if dependency not in claim_ids:
                failures.append(f"{claim['claim_id']} references unknown claim {dependency}")
        serialized_claim = json.dumps(claim, ensure_ascii=False)
        if "open_obligation_ids" in serialized_claim or '"proof_obligation"' in serialized_claim:
            failures.append(
                f"{claim['claim_id']} retains a retired legacy-status field"
            )
        for gap_id in claim.get("unresolved_dependency_ids", []):
            if gap_id not in gap_ids:
                failures.append(
                    f"{claim['claim_id']} references unknown unresolved dependency {gap_id}"
                )
        for gap_id in claim.get("related_gap_ids", []):
            if gap_id not in gap_ids:
                failures.append(f"{claim['claim_id']} references unknown exact gap {gap_id}")
        locator = claim.get("proof_locator")
        if locator:
            validate_proof_locator(claim["claim_id"], locator)
        statement_locator = claim.get("statement_locator")
        if statement_locator:
            validate_proof_locator(claim["claim_id"], statement_locator)
        for locator in claim.get("additional_proof_locators", []):
            validate_proof_locator(claim["claim_id"], locator)

    assert_acyclic_claim_graph(claims, failures)

    required_morphism_fields = {
        "domain",
        "codomain",
        "formula",
        "well_definedness",
        "preserved_structure",
        "fibres",
        "inverse_status",
        "exceptions",
        "proof_locator",
    }
    for morphism in morphisms:
        missing = sorted(required_morphism_fields - morphism.keys())
        if missing:
            failures.append(f"{morphism['morphism_id']} missing fields: {missing}")
        for claim_id in morphism.get("claim_refs", []):
            if claim_id not in claim_ids:
                failures.append(
                    f"{morphism['morphism_id']} references unknown claim {claim_id}"
                )
        for source_id in morphism.get("source_refs", []):
            if source_id not in source_ids:
                failures.append(
                    f"{morphism['morphism_id']} references unknown source {source_id}"
                )
        locator = morphism.get("proof_locator", {})
        validate_proof_locator(morphism["morphism_id"], locator)
        for locator in morphism.get("additional_proof_locators", []):
            validate_proof_locator(morphism["morphism_id"], locator)

    for gap in gaps:
        for claim_id in gap.get("dependent_claim_refs", []):
            if claim_id not in claim_ids:
                failures.append(
                    f"{gap['gap_id']} references unknown dependent claim {claim_id}"
                )
        for source_id in gap.get("source_refs", []):
            if source_id not in source_ids:
                failures.append(
                    f"{gap['gap_id']} references unknown source {source_id}"
                )
        for boundary_id in gap.get("proved_boundary_refs", []):
            if boundary_id not in claim_ids and boundary_id not in morphism_ids:
                failures.append(
                    f"{gap['gap_id']} references unknown proved boundary {boundary_id}"
                )

    for mapping in legacy_mappings:
        for gap_id in mapping.get("active_gap_refs", []):
            if gap_id not in gap_ids:
                failures.append(
                    f"{mapping.get('legacy_id')} maps to unknown exact gap {gap_id}"
                )

    shelf = Path(r"C:\Users\LOCAL_USER\Documents\arxiv_latex\library\collatz_reconstruction")
    acquisition_index = shelf / "acquisition_index.jsonl"
    if acquisition_index.is_file():
        try:
            acquisitions = read_jsonl(acquisition_index)
            for acquisition in acquisitions:
                if acquisition.get("status") != "pass":
                    failures.append(
                        f"arXiv acquisition not passing: {acquisition.get('versioned_arxiv_id')}"
                    )
                source_path = Path(acquisition["source_path"])
                if not source_path.is_file() or sha256(source_path) != acquisition["source_sha256"]:
                    failures.append(f"arXiv acquisition source mismatch: {source_path}")
                manifest_path = Path(acquisition["extraction"]["manifest_path"])
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                if manifest.get("status") != "pass":
                    failures.append(f"arXiv extraction manifest not passing: {manifest_path}")
                extraction_root = manifest_path.parent
                for file_record in manifest.get("files", []):
                    file_path = extraction_root / Path(file_record["relative_path"])
                    if not file_path.is_file():
                        failures.append(f"extracted arXiv file missing: {file_path}")
                    elif (
                        file_path.stat().st_size != file_record["bytes"]
                        or sha256(file_path) != file_record["sha256"]
                    ):
                        failures.append(f"extracted arXiv file mismatch: {file_path}")
        except Exception as error:
            failures.append(f"arXiv shelf validation failed: {error}")
        partials = [path for path in shelf.rglob("*") if path.is_file() and path.suffix in {".part", ".tmp"}]
        if partials:
            failures.append(f"undeclared partial files remain in arXiv shelf: {partials}")

    report = {
        "schema_version": "1.0",
        "status": "pass" if not failures else "fail",
        "project_id": state.get("project_id"),
        "route_record_count": len(route_records),
        "document_route_count": len(document_records),
        "topic_route_count": len(topic_route_records),
        "source_record_count": len(sources),
        "claim_record_count": len(claims),
        "morphism_record_count": len(morphisms),
        "exact_gap_count": len(gaps),
        "legacy_status_mapping_count": len(legacy_mappings),
        "chatnotes_validator_status": chatnotes_validator_status,
        "warning_count": len(warnings),
        "warnings": warnings,
        "failure_count": len(failures),
        "failures": failures,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
