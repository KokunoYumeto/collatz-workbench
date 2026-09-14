from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
UPSTREAM = PROJECT.parent / "maxwell_siegel_research"
STATE = PROJECT / "state"

INPUTS = {
    "candidates": UPSTREAM / "TOPIC_CANDIDATES.jsonl",
    "adjudications": UPSTREAM / "CANDIDATE_ADJUDICATIONS.jsonl",
    "papers": UPSTREAM / "PAPER_INDEX.jsonl",
    "sources": UPSTREAM / "SOURCE_REGISTRY.jsonl",
}

EXPECTED_SHA256 = {
    "candidates": "e1d4323d6ff6091c5aa8b4002bcce8dcfd0acaec92d767282494f4a2772b976c",
    "adjudications": "992355f0233492c997607c69d81b7228a1bb8c472f8bca286ca64500bc7b1e52",
    "papers": "12a5d0d10db49a80c4396970fb1c4572118d2bb10deed647362f0a59f4f6c6ed",
    "sources": "3e93acb4adaadad2383aba455ba8f6c832a244270b90715b181c1994d49b105b",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def dump_jsonl(path: Path, records: list[dict]) -> None:
    text = "".join(
        json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
        for record in records
    )
    path.write_text(text, encoding="utf-8", newline="\n")


def stable_route_id(prefix: str, upstream_id: str) -> str:
    token = hashlib.sha256(upstream_id.encode("utf-8")).hexdigest()[:20].upper()
    return f"{prefix}-{token}"


def main() -> None:
    observed = {name: sha256(path) for name, path in INPUTS.items()}
    if observed != EXPECTED_SHA256:
        raise SystemExit(
            "Frozen routing input mismatch:\n"
            + json.dumps({"expected": EXPECTED_SHA256, "observed": observed}, indent=2)
        )

    candidates = {row["candidate_id"]: row for row in read_jsonl(INPUTS["candidates"])}
    adjudications = read_jsonl(INPUTS["adjudications"])
    papers = {row["document_id"]: row for row in read_jsonl(INPUTS["papers"])}

    accepted_classes = {"direct", "substantive_adjacent"}
    accepted = [
        row for row in adjudications if row["classification"] in accepted_classes
    ]
    accepted.sort(key=lambda row: row["topic_candidate_id"])

    route_records: list[dict] = []
    linked_document_ids: set[str] = set()
    for adjudication in accepted:
        candidate_id = adjudication["topic_candidate_id"]
        candidate = candidates[candidate_id]
        linked_document_ids.update(adjudication["linked_document_ids"])
        route_records.append(
            {
                "schema_version": "1.0",
                "record_type": "index_route",
                "route_id": stable_route_id("ROUTE-COL", candidate_id),
                "upstream_candidate_id": candidate_id,
                "candidate_kind": candidate["candidate_kind"],
                "classification": adjudication["classification"],
                "classification_scope": adjudication["classification_scope"],
                "confidence": adjudication["confidence"],
                "edge_evidence": adjudication["evidence"],
                "bibliographic_identity": adjudication["bibliographic_identity"],
                "upstream_ids": candidate["upstream_ids"],
                "paths": candidate["paths"],
                "hashes": candidate["hashes"],
                "linked_document_ids": adjudication["linked_document_ids"],
                "audit_overlays": adjudication["audit_overlays"],
                "disposition": adjudication["disposition"],
                "reading_status": "unread_route",
                "admission_status": "not_admitted_from_metadata",
            }
        )

    direct_terms = (
        "collatz",
        "3x + 1",
        "3x+1",
        "3n + 1",
        "3n+1",
        "syracuse",
        "hailstone",
        "hydra map",
        "numen",
        "dreamcatcher",
    )
    for document_id, paper in papers.items():
        searchable = json.dumps(
            {
                "title": paper.get("title"),
                "topics": paper.get("topics"),
                "relevance": paper.get("relevance"),
                "relationships": paper.get("relationships"),
            },
            ensure_ascii=False,
        ).lower()
        if any(term in searchable for term in direct_terms):
            linked_document_ids.add(document_id)

    document_records: list[dict] = []
    for document_id in sorted(linked_document_ids):
        if document_id not in papers:
            raise SystemExit(f"Adjudication links missing document {document_id}")
        paper = papers[document_id]
        document_records.append(
            {
                "schema_version": "1.0",
                "record_type": "document_route",
                "route_id": stable_route_id("DOCROUTE-COL", document_id),
                "upstream_document_id": document_id,
                "logical_work_id": paper["logical_work_id"],
                "title": paper["title"],
                "authors": paper["authors"],
                "version": paper["version"],
                "paths": paper["paths"],
                "identifiers": paper["identifiers"],
                "topics": paper["topics"],
                "relevance": paper["relevance"],
                "relationships": paper["relationships"],
                "extraction": paper["extraction"],
                "upstream_review_status": paper["review_status"],
                "reading_status": "unread_in_collatz_reconstruction",
                "admission_status": "route_only_until_content_read",
            }
        )

    dump_jsonl(STATE / "index_routes.jsonl", route_records)
    dump_jsonl(STATE / "document_routes.jsonl", document_records)

    path_states = Counter()
    for record in route_records:
        for path_record in record["paths"]:
            path = Path(path_record["absolute_path"])
            path_states["exists" if path.exists() else "missing"] += 1

    summary = {
        "schema_version": "1.0",
        "record_type": "index_snapshot",
        "input_sha256": observed,
        "upstream_candidate_count": len(candidates),
        "accepted_route_count": len(route_records),
        "accepted_classification_counts": dict(
            sorted(Counter(row["classification"] for row in accepted).items())
        ),
        "document_route_count": len(document_records),
        "route_path_state_counts": dict(sorted(path_states.items())),
        "rule": "This is a deterministic slice of the frozen accepted index, not a content-level admission or a filesystem rescan.",
    }
    (STATE / "index_snapshot.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
