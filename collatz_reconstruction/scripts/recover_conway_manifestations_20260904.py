"""Recover two registered Conway source bodies only on exact byte identity.

This script does not amend the registry, validator, or mathematical artifacts.
Differing downloads are retained solely as candidates under project tmp.
"""

from __future__ import annotations

import concurrent.futures
import hashlib
import json
from pathlib import Path
import sys
import tempfile
from datetime import datetime, timezone

import requests


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ID = "SRC-COL-000024"
RECEIPT = ROOT / "qa/CONWAY-SRC-COL-000024-RECOVERY-20260904.json"
EXPECTED = {
    "conway_1972_unpredictable_iterations_ams2010_reprint_inspection.pdf": (
        "https://gwern.net/doc/cs/computable/1972-conway.pdf",
        172046,
        "b8cb28578dd2b125235c827e9b4e37e0a1ef0252c83da62d40551f6885ca9bf2",
    ),
    "zbmath_document_3526785.json": (
        "https://api.zbmath.org/v1/document/3526785",
        1270,
        "04ee3fd45574b476c3978476264e262056a137319d7fdb2d7db71a43ac1b72ea",
    ),
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def pinned_inputs() -> dict:
    return {
        str(path.relative_to(ROOT)): digest(path.read_bytes())
        for path in (
            ROOT / "DIRECTIVES.md",
            ROOT / "state/source_registry.jsonl",
            ROOT / "qa/CONWAY-1972-F022-historical-verification-audit.md",
        )
    }


def fetch(manifestation: dict, candidate_dir: Path) -> dict:
    relative = Path(manifestation["path"])
    target = (ROOT / relative).resolve()
    assert target.is_relative_to(ROOT / "tmp/source_inspection_conway_1972_20260826")
    url, expected_bytes, expected_hash = EXPECTED[target.name]
    assert manifestation["retrieval_url"] == url
    assert manifestation["bytes"] == expected_bytes
    assert manifestation["sha256"] == expected_hash
    result = {
        "original_path": relative.as_posix(),
        "requested_url": url,
        "expected_bytes": expected_bytes,
        "expected_sha256": expected_hash,
        "target_existed_before": target.exists(),
        "restored": False,
    }
    try:
        # Bounded GET of the exact registered URL. Do not reserialize the body.
        with requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; local-source-integrity-check/1.0)",
                "Accept-Encoding": "identity",
            },
            timeout=(15, 35),
            stream=True,
        ) as response:
            result.update(
                final_url=response.url,
                http_status=response.status_code,
                response_headers={
                    key: response.headers[key]
                    for key in ("Content-Type", "Content-Length", "ETag", "Last-Modified", "Content-Encoding")
                    if key in response.headers
                },
            )
            response.raise_for_status()
            body = bytearray()
            for chunk in response.iter_content(chunk_size=65536):
                body.extend(chunk)
                if len(body) > 2 * 1024 * 1024:
                    raise ValueError("Download exceeds the 2 MiB candidate ceiling")
        data = bytes(body)
        actual_hash = digest(data)
        candidate = candidate_dir / target.name
        with candidate.open("xb") as stream:
            stream.write(data)
        result.update(
            candidate_path=candidate.relative_to(ROOT).as_posix(),
            actual_bytes=len(data),
            actual_sha256=actual_hash,
            exact_registered_identity=(len(data) == expected_bytes and actual_hash == expected_hash),
        )
        if not result["exact_registered_identity"]:
            result["status"] = "different_candidate_preserved_original_not_restored"
        elif target.exists():
            result["target_current_sha256"] = digest(target.read_bytes())
            result["status"] = (
                "already_present_exact"
                if result["target_current_sha256"] == expected_hash
                else "target_conflict_preserved_no_overwrite"
            )
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as stream:
                stream.write(data)
            result["target_current_sha256"] = digest(target.read_bytes())
            assert result["target_current_sha256"] == expected_hash
            result.update(status="restored_exact_registered_bytes", restored=True)
    except Exception as error:
        result.update(status="acquisition_or_restoration_error", error=f"{type(error).__name__}: {error}")
    return result


def main() -> int:
    if RECEIPT.exists():
        raise FileExistsError(f"Preserve existing recovery receipt: {RECEIPT}")
    before = pinned_inputs()
    records = [
        json.loads(line)
        for line in (ROOT / "state/source_registry.jsonl").read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    ]
    matches = [record for record in records if record.get("source_id") == SOURCE_ID]
    assert len(matches) == 1
    manifestations = matches[0]["manifestations"]
    assert {Path(item["path"]).name for item in manifestations} == set(EXPECTED)
    candidate_dir = Path(tempfile.mkdtemp(prefix="source_recovery_conway_20260904_", dir=ROOT / "tmp"))
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda item: fetch(item, candidate_dir), manifestations))
    after = pinned_inputs()
    success = all(item["status"] in ("restored_exact_registered_bytes", "already_present_exact") for item in results)
    receipt = {
        "receipt_id": "CONWAY-SRC-COL-000024-RECOVERY-20260904",
        "recorded_utc": datetime.now(timezone.utc).isoformat(),
        "source_id": SOURCE_ID,
        "historical_receipt_id": "ACT-COL-000026",
        "command": f'"{sys.executable}" scripts/recover_conway_manifestations_20260904.py',
        "script_sha256": digest(Path(__file__).read_bytes()),
        "input_sha256_before": before,
        "input_sha256_after": after,
        "pinned_inputs_unchanged": before == after,
        "all_registered_manifestations_recovered_exactly": success,
        "results": results,
        "scope": "Exact registered body recovery only; no fresh mathematical audit or broader corpus completion claim.",
        "restrictions_observed": [
            "GET only; no public upload or record mutation",
            "No Git, Lean, AGENTS edits, cleanup, registry or validator edits",
            "Differing candidates are not substituted or represented as registered identity",
            "Copyrighted PDF remains local inspection material, not a redistribution artifact",
        ],
    }
    with RECEIPT.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(receipt, stream, indent=2, ensure_ascii=False)
        stream.write("\n")
    print(json.dumps(receipt, indent=2, ensure_ascii=False))
    return 0 if success and before == after else 1


if __name__ == "__main__":
    raise SystemExit(main())
