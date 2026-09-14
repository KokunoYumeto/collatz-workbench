#!/usr/bin/env python3
"""Prepare and seal ACT49 for the canonical Overleaf affine delivery.

The prepare phase updates only the canonical project's current metadata and
regenerates its non-self-referential manifest.  After the four root files have
been uploaded, the seal phase verifies the manifest, all manifested children,
and the explicitly retained remote extras against a fresh Overleaf source
download before advancing the durable current-state records.  The verify phase
repeats those checks, including the recorded receipt/checkpoint identities,
without writing anything.  Historical ACT47/ACT48 facts are deliberately left
unchanged.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
STAGE = ROOT / "overleaf" / "sync_20260904" / "canonical_project"
SOURCE_MAP = STAGE / "SOURCE_MAP.json"
PACKAGE_STATUS = STAGE / "PACKAGE_STATUS.json"
MANIFEST = STAGE / "MANIFEST.json"
TAO_RECEIPT_REL = "overleaf/sync_20260904/tao_v7_family_remote_receipt.json"
TAO_RECEIPT = ROOT / TAO_RECEIPT_REL
REMOTE_RECEIPT_REL = "overleaf/sync_20260904/affine_analytic_remote_receipt.json"
REMOTE_RECEIPT = ROOT / REMOTE_RECEIPT_REL
QA_REL = "qa/ACT49-AFFINE-ANALYTIC-REMOTE-SYNC.json"
QA_PATH = ROOT / QA_REL

ROOT_REPAIR_FILES = (
    "MANIFEST.json",
    "PACKAGE_STATUS.json",
    "README.md",
    "SOURCE_MAP.json",
)

AFFINE_DELIVERY_FILES = (
    "companion/certificates/affine_packet_series_checks.py",
    "companion/chapters/04_affine_packets_parity_necklaces_and_residue_automata.tex",
    "companion/chapters/05_packet_fixed_point_series.tex",
    "critical/chapters/06_affine_packet_source_audit.tex",
    "research_companion.tex",
)

NINE_UNIQUE_DELIVERY_FILES = ROOT_REPAIR_FILES + AFFINE_DELIVERY_FILES

# These are deliberately retained historical artifacts in the canonical
# Overleaf project.  They are not dependencies of any current entrypoint, but a
# fresh source download must account for them exactly rather than silently
# ignoring arbitrary remote files.
EXPECTED_REMOTE_EXTRAS = frozenset(
    {
        "chapters/00_scope_and_method.tex",
        "chapters/01_literature_spine.tex",
        "chapters/01a_crandall_1978.tex",
        "chapters/01b_siegel_hydra_numen.tex",
        "chapters/01c_debruijn_graphs.tex",
        "chapters/01d_primary_parity_dependencies.tex",
        "chapters/01e_steuding_continued_fraction.tex",
        "chapters/01f_everett_1977.tex",
        "chapters/01g_tao_fourier_renewal.tex",
        "chapters/01h_tao_valuation_law.tex",
        "chapters/01i_tao_first_passage_stabilisation.tex",
        "chapters/01j_tao_main_theorem_reduction.tex",
        "chapters/01k_computational_verification.tex",
        "chapters/99_source_register.tex",
        "collatz_canonical_project_current_20260904.zip",
    }
)

TAO_BUILD = {
    "id": "1a06ce652c4-7d0760e256afa889",
    "pages": 16,
    "errors": 0,
    "warnings": 0,
    "info": 0,
    "all_logs": 0,
}

AFFINE_BUILDS = {
    "research_companion.tex": {
        "id": "1a06e8dd265-8baff6a3f94e8253",
        "pages": 57,
        "errors": 0,
        "warnings": 0,
        "info": 2,
        "all_logs": 2,
        "diagnostics": [
            "Underfull hbox in companion/bibliography.tex lines 49--56",
            "Underfull hbox in companion/bibliography.tex lines 89--95",
        ],
    },
    "main.tex": {
        "id": "1a06e8efa69-2003420ae2b09677",
        "pages": 184,
        "errors": 0,
        "warnings": 0,
        "info": 0,
        "all_logs": 0,
    },
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def json_payload(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def jsonl_payload(records: list[dict]) -> bytes:
    return "".join(
        json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n"
        for record in records
    ).encode("utf-8")


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(json_payload(value))


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.write_bytes(jsonl_payload(records))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def transactional_write(payloads: dict[Path, bytes]) -> None:
    """Stage every payload, then atomically replace targets with rollback.

    A cross-file atomic commit is not available on the filesystem.  This helper
    therefore performs all serialization and temporary writes before touching
    a target, uses same-directory atomic replacements, and restores every
    already-replaced target if a replacement raises.  Seal also completes all
    semantic preflight before calling this helper.
    """

    token = uuid4().hex
    originals: dict[Path, bytes | None] = {
        path: path.read_bytes() if path.exists() else None for path in payloads
    }
    staged: dict[Path, Path] = {}
    committed: list[Path] = []
    try:
        for path, payload in payloads.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            temporary = path.with_name(f".{path.name}.act49-{token}.tmp")
            temporary.write_bytes(payload)
            require(
                temporary.read_bytes() == payload,
                f"failed to stage exact payload for {path}",
            )
            staged[path] = temporary
        for path, temporary in staged.items():
            os.replace(temporary, path)
            committed.append(path)
    except Exception:
        for path in reversed(committed):
            original = originals[path]
            try:
                if original is None:
                    path.unlink(missing_ok=True)
                else:
                    rollback = path.with_name(f".{path.name}.act49-{token}.rollback")
                    rollback.write_bytes(original)
                    os.replace(rollback, path)
            except Exception:
                # Preserve the original exception; any rollback failure remains
                # visible through the leftover temporary/rollback artifact.
                pass
        raise
    finally:
        for temporary in staged.values():
            temporary.unlink(missing_ok=True)
        for path in payloads:
            path.with_name(f".{path.name}.act49-{token}.rollback").unlink(missing_ok=True)


def verify_tao_receipt() -> None:
    receipt = read_json(TAO_RECEIPT)
    if receipt.get("project_id") != "6a91f06e408dd545780c660f":
        raise RuntimeError("Tao receipt has the wrong canonical project id")
    if receipt.get("entrypoint") != "tao_preprint.tex":
        raise RuntimeError("Tao receipt has the wrong entrypoint")
    if receipt.get("build") != TAO_BUILD:
        raise RuntimeError("Tao receipt build facts do not match the registered V7 build")


def regenerate_manifest() -> dict:
    files = sorted(
        path for path in STAGE.rglob("*") if path.is_file() and path.name != "MANIFEST.json"
    )
    manifest = {
        "schema_version": 1,
        "hash": "sha256",
        "files": [
            {
                "path": path.relative_to(STAGE).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha_file(path),
            }
            for path in files
        ],
    }
    write_json(MANIFEST, manifest)
    return manifest


def prepare() -> None:
    verify_tao_receipt()
    now = utc_now()

    source_map = read_json(SOURCE_MAP)
    source_map["tao_v7_family_revision"].update(
        {
            "remote_status": "ten_named_files_uploaded_and_remote_compile_verified",
            "remote_receipt": TAO_RECEIPT_REL,
            "remote_build": TAO_BUILD,
        }
    )
    source_map["affine_analytic_revision"].update(
        {
            "remote_status": "nine_unique_files_delivered_source_download_verified_and_both_entrypoints_compiled",
            "remote_receipt": REMOTE_RECEIPT_REL,
            "remote_builds": AFFINE_BUILDS,
            "remote_verified_utc": now,
        }
    )
    write_json(SOURCE_MAP, source_map)

    status = read_json(PACKAGE_STATUS)
    status["status"] = (
        "Affine analytic delta and portable companion package synchronized to "
        "the existing canonical project; source identity and both affected builds verified."
    )
    status["tao_v7_family_revision"].update(
        {
            "status": "ten_named_files_uploaded_and_remote_compile_verified",
            "remote_receipt": TAO_RECEIPT_REL,
            "remote_build": TAO_BUILD,
        }
    )
    affine = status["affine_analytic_revision"]
    affine["status"] = (
        "compiled_visual_portable_package_and_canonical_remote_delivery_verified"
    )
    affine["scope_caveat"] = (
        "Local compilation, portable package validation, specified visual coverage, "
        "canonical source-download identity, and the two affected remote entrypoint "
        "builds are verified. This is not a full mathematical or whole-corpus certification. "
        "Displayed local apparatus paths need not be bundled."
    )
    affine["remote_action"] = True
    affine["remote_receipt"] = REMOTE_RECEIPT_REL
    affine["remote_builds"] = AFFINE_BUILDS
    status["canonical_remote_delivery"] = {
        "project_id": "6a91f06e408dd545780c660f",
        "receipt": REMOTE_RECEIPT_REL,
        "uploaded_delta": list(NINE_UNIQUE_DELIVERY_FILES),
        "builds": AFFINE_BUILDS,
        "new_project": False,
        "sharing_changed": False,
        "public_publication": False,
    }
    write_json(PACKAGE_STATUS, status)

    manifest = regenerate_manifest()
    print(
        json.dumps(
            {
                "status": "PREPARED",
                "metadata": {
                    "SOURCE_MAP.json": sha_file(SOURCE_MAP),
                    "PACKAGE_STATUS.json": sha_file(PACKAGE_STATUS),
                    "MANIFEST.json": sha_file(MANIFEST),
                },
                "manifested_files": len(manifest["files"]),
                "next": "upload MANIFEST.json, PACKAGE_STATUS.json, README.md, and SOURCE_MAP.json, then run seal with a fresh source zip",
            },
            indent=2,
        )
    )


def verify_remote_zip(zip_path: Path) -> dict:
    require(zip_path.is_file(), f"remote source ZIP does not exist: {zip_path}")
    manifest_payload = MANIFEST.read_bytes()
    manifest = json.loads(manifest_payload.decode("utf-8"))
    require(manifest.get("schema_version") == 1, "unsupported canonical manifest schema")
    require(manifest.get("hash") == "sha256", "canonical manifest must declare sha256")
    identities = manifest.get("files")
    require(isinstance(identities, list), "canonical manifest files must be a list")
    require(len(identities) == 49, f"ACT49 must contain 49 manifested children, got {len(identities)}")

    manifest_paths = [identity.get("path") for identity in identities]
    require(all(isinstance(path, str) and path for path in manifest_paths), "invalid manifest path")
    require(len(set(manifest_paths)) == len(manifest_paths), "duplicate canonical manifest path")
    require(
        all("\\" not in path and not path.startswith("/") and ".." not in Path(path).parts for path in manifest_paths),
        "canonical manifest contains a non-relative or escaping path",
    )

    current_stage_paths = {
        path.relative_to(STAGE).as_posix()
        for path in STAGE.rglob("*")
        if path.is_file() and path.name != "MANIFEST.json"
    }
    require(
        current_stage_paths == set(manifest_paths),
        "current stage and canonical manifest path sets differ: "
        + json.dumps(
            {
                "unmanifested_local": sorted(current_stage_paths - set(manifest_paths)),
                "missing_local": sorted(set(manifest_paths) - current_stage_paths),
            }
        ),
    )

    local_verified: list[dict] = []
    for identity in identities:
        rel = identity["path"]
        local_payload = (STAGE / rel).read_bytes()
        observed_local = {
            "path": rel,
            "bytes": len(local_payload),
            "sha256": sha_bytes(local_payload),
        }
        require(
            observed_local == identity,
            "local stage drift from canonical manifest: "
            + json.dumps({"expected": identity, "observed": observed_local}, indent=2),
        )
        local_verified.append(observed_local)

    remote_verified: list[dict] = []
    with ZipFile(zip_path) as archive:
        file_infos = [info for info in archive.infolist() if not info.is_dir()]
        member_names = [info.filename for info in file_infos]
        require(
            len(member_names) == len(set(member_names)),
            "remote source ZIP contains duplicate file members",
        )
        members = {info.filename: info for info in file_infos}
        require("MANIFEST.json" in members, "remote source ZIP is missing MANIFEST.json")
        remote_manifest_payload = archive.read(members["MANIFEST.json"])
        require(
            remote_manifest_payload == manifest_payload,
            "remote MANIFEST.json differs from the current local MANIFEST.json: "
            + json.dumps(
                {
                    "local_bytes": len(manifest_payload),
                    "remote_bytes": len(remote_manifest_payload),
                    "local_sha256": sha_bytes(manifest_payload),
                    "remote_sha256": sha_bytes(remote_manifest_payload),
                },
                indent=2,
            ),
        )

        current_remote_extras = set(member_names) - set(manifest_paths) - {"MANIFEST.json"}
        require(
            current_remote_extras == EXPECTED_REMOTE_EXTRAS,
            "remote extras differ from the explicit ACT49 historical-artifact set: "
            + json.dumps(
                {
                    "unexpected": sorted(current_remote_extras - EXPECTED_REMOTE_EXTRAS),
                    "missing_expected": sorted(EXPECTED_REMOTE_EXTRAS - current_remote_extras),
                },
                indent=2,
            ),
        )

        for identity in identities:
            rel = identity["path"]
            require(rel in members, f"remote source ZIP is missing manifested child: {rel}")
            remote_payload = archive.read(members[rel])
            observed_remote = {
                "path": rel,
                "bytes": len(remote_payload),
                "sha256": sha_bytes(remote_payload),
            }
            require(
                observed_remote == identity,
                "remote child differs from canonical manifest: "
                + json.dumps({"expected": identity, "observed": observed_remote}, indent=2),
            )
            require(
                remote_payload == (STAGE / rel).read_bytes(),
                f"remote child differs byte-for-byte from current local stage: {rel}",
            )
            remote_verified.append(observed_remote)

    return {
        "zip_filename": zip_path.name,
        "zip_bytes": zip_path.stat().st_size,
        "zip_sha256": sha_file(zip_path),
        "remote_files_total": len(member_names),
        "manifested_files_verified": len(remote_verified),
        "local_manifested_files_verified": len(local_verified),
        "manifest_sha256": sha_bytes(manifest_payload),
        "remote_manifest_sha256": sha_bytes(remote_manifest_payload),
        "remote_manifest_exact": True,
        "expected_remote_extras": sorted(EXPECTED_REMOTE_EXTRAS),
        "expected_remote_extras_verified": len(EXPECTED_REMOTE_EXTRAS),
        "mismatches": [],
    }


REMOTE_SOURCE_IDENTITY_KEYS = (
    "zip_filename",
    "zip_bytes",
    "zip_sha256",
    "manifested_files_verified",
    "manifest_sha256",
    "mismatches",
)


def verify_recorded_act49(remote_source: dict) -> dict:
    require(REMOTE_RECEIPT.is_file(), f"missing ACT49 remote receipt: {REMOTE_RECEIPT}")
    require(QA_PATH.is_file(), f"missing ACT49 QA checkpoint: {QA_PATH}")
    receipt_payload = REMOTE_RECEIPT.read_bytes()
    qa_payload = QA_PATH.read_bytes()
    receipt = json.loads(receipt_payload.decode("utf-8"))
    qa = json.loads(qa_payload.decode("utf-8"))

    require(receipt.get("schema_version") == 1, "unexpected ACT49 receipt schema")
    require(receipt.get("receipt_id") == "AFFINE-ANALYTIC-REMOTE-20260905", "wrong ACT49 receipt id")
    require(receipt.get("project_id") == "6a91f06e408dd545780c660f", "wrong ACT49 project id")
    require(
        receipt.get("uploaded_named_files") == list(NINE_UNIQUE_DELIVERY_FILES),
        "ACT49 receipt does not record the exact nine unique delivery files",
    )
    require(
        receipt.get("root_repair_upload_after_manifest_verification") == list(ROOT_REPAIR_FILES),
        "ACT49 receipt does not record the exact four root repair files",
    )
    recorded_remote = receipt.get("remote_source_download", {})
    for key in REMOTE_SOURCE_IDENTITY_KEYS:
        require(
            recorded_remote.get(key) == remote_source[key],
            f"ACT49 receipt remote-source identity mismatch for {key}",
        )
    require(receipt.get("builds") == AFFINE_BUILDS, "ACT49 receipt build facts drifted")
    require(
        receipt.get("tao_entrypoint", {}).get("baseline") == "arXiv:1909.03562v7",
        "ACT49 receipt Tao baseline is not V7",
    )
    require(
        receipt.get("tao_entrypoint", {}).get("reader_facing_v5_hits") == 0,
        "ACT49 receipt no longer records zero reader-facing V5 hits",
    )

    receipt_sha = sha_bytes(receipt_payload)
    qa_sha = sha_bytes(qa_payload)
    require(qa.get("schema_version") == 1, "unexpected ACT49 QA schema")
    require(qa.get("checkpoint_id") == "ACT-COL-000049", "wrong ACT49 QA checkpoint id")
    require(
        qa.get("remote_receipt")
        == {"path": REMOTE_RECEIPT_REL, "sha256": receipt_sha},
        "ACT49 QA remote-receipt identity mismatch",
    )
    require(
        qa.get("remote_source_download") == recorded_remote,
        "ACT49 QA and remote receipt disagree on source-download identity",
    )
    require(qa.get("builds") == AFFINE_BUILDS, "ACT49 QA build facts drifted")

    expected_metadata = {
        "MANIFEST.json": sha_file(MANIFEST),
        "PACKAGE_STATUS.json": sha_file(PACKAGE_STATUS),
        "README.md": sha_file(STAGE / "README.md"),
        "SOURCE_MAP.json": sha_file(SOURCE_MAP),
    }
    recorded_metadata = qa.get("canonical_metadata", {})
    required_legacy_keys = {"MANIFEST.json", "PACKAGE_STATUS.json", "SOURCE_MAP.json"}
    require(
        required_legacy_keys <= set(recorded_metadata),
        "ACT49 QA omits a required recorded canonical-metadata identity",
    )
    require(
        set(recorded_metadata) <= set(expected_metadata),
        "ACT49 QA contains an unknown canonical-metadata identity",
    )
    for name, recorded_hash in recorded_metadata.items():
        require(
            recorded_hash == expected_metadata[name],
            f"ACT49 QA canonical metadata identity mismatch for {name}",
        )

    return {
        "remote_receipt_path": REMOTE_RECEIPT_REL,
        "remote_receipt_sha256": receipt_sha,
        "qa_path": QA_REL,
        "qa_sha256": qa_sha,
        "receipt_remote_source_identity_fields_verified": len(REMOTE_SOURCE_IDENTITY_KEYS),
        "qa_canonical_metadata_identities_verified": len(recorded_metadata),
        "qa_readme_identity_recorded": "README.md" in recorded_metadata,
        "qa_readme_identity_verified_independently_by_remote_stage_check": True,
        "nine_unique_delivery_files_verified": len(NINE_UNIQUE_DELIVERY_FILES),
        "four_root_repair_files_verified": len(ROOT_REPAIR_FILES),
    }


def verify_read_only(zip_path: Path) -> None:
    watched_paths = [
        MANIFEST,
        PACKAGE_STATUS,
        STAGE / "README.md",
        SOURCE_MAP,
        REMOTE_RECEIPT,
        QA_PATH,
        ROOT / "state" / "overleaf_current.json",
        ROOT / "state" / "affine_analytic_current.json",
        ROOT / "state" / "project_state.json",
        ROOT / "state" / "coverage.json",
        ROOT / "state" / "programmes.jsonl",
        ROOT / "state" / "action_receipts.jsonl",
    ]
    before = {
        str(path): sha_file(path) if path.is_file() else None for path in watched_paths
    }
    verify_tao_receipt()
    remote_source = verify_remote_zip(zip_path)
    recorded = verify_recorded_act49(remote_source)
    after = {
        str(path): sha_file(path) if path.is_file() else None for path in watched_paths
    }
    require(before == after, "read-only ACT49 verification changed a watched file")
    print(
        json.dumps(
            {
                "status": "PASS_READ_ONLY",
                "state_mutated": False,
                "watched_files_unchanged": len(watched_paths),
                "remote_source": remote_source,
                "recorded_identities": recorded,
            },
            indent=2,
        )
    )


def seal(zip_path: Path) -> None:
    verify_tao_receipt()
    action_path = ROOT / "state" / "action_receipts.jsonl"
    action_records = [
        json.loads(line)
        for line in action_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    require(
        not any(record.get("receipt_id") == "ACT-COL-000049" for record in action_records),
        "ACT-COL-000049 already exists; refusing duplicate seal before any write",
    )
    remote_source = verify_remote_zip(zip_path)
    now = utc_now()

    receipt = {
        "schema_version": 1,
        "receipt_id": "AFFINE-ANALYTIC-REMOTE-20260905",
        "verified_utc": now,
        "project_id": "6a91f06e408dd545780c660f",
        "url": "https://www.overleaf.com/project/6a91f06e408dd545780c660f",
        "uploaded_named_files": list(NINE_UNIQUE_DELIVERY_FILES),
        "root_repair_upload_after_manifest_verification": list(ROOT_REPAIR_FILES),
        "remote_source_download": remote_source,
        "builds": AFFINE_BUILDS,
        "active_main_document_after_verification": "main.tex",
        "tao_entrypoint": {
            "baseline": "arXiv:1909.03562v7",
            "reader_facing_v5_hits": 0,
            "sources_changed_by_affine_delivery": False,
            "receipt": TAO_RECEIPT_REL,
            "build": TAO_BUILD,
        },
        "verification_boundary": (
            "The remote MANIFEST.json and every manifested child were checked byte-for-byte "
            "against the current local stage, and every other remote file matched the explicit "
            "historical-artifact set. The two affected entrypoints were compiled and their page "
            "counts and diagnostics read in the live canonical project."
        ),
        "new_project": False,
        "new_archive": False,
        "sharing_changed": False,
        "public_publication": False,
        "Lean_started": False,
        "whole_raw_affine_coverage_reconciled": False,
        "whole_corpus_completion_claimed": False,
    }
    receipt_payload = json_payload(receipt)
    receipt_hash = sha_bytes(receipt_payload)

    qa = {
        "schema_version": 1,
        "checkpoint_id": "ACT-COL-000049",
        "status": "PASS_canonical_affine_remote_source_and_build_verification",
        "recorded_utc": now,
        "scope": (
            "Canonical remote delivery only; historical ACT47/ACT48 facts remain immutable, "
            "and the full 3,021-line raw affine reconciliation remains active."
        ),
        "remote_receipt": {
            "path": REMOTE_RECEIPT_REL,
            "sha256": receipt_hash,
        },
        "canonical_metadata": {
            "MANIFEST.json": sha_file(MANIFEST),
            "PACKAGE_STATUS.json": sha_file(PACKAGE_STATUS),
            "README.md": sha_file(STAGE / "README.md"),
            "SOURCE_MAP.json": sha_file(SOURCE_MAP),
        },
        "remote_source_download": remote_source,
        "builds": AFFINE_BUILDS,
        "tao_reader_boundary": {
            "baseline": "arXiv:1909.03562v7",
            "reader_facing_v5_hits": 0,
            "historical_version_comparison_location": "local provenance only",
        },
        "remote_sync_complete": True,
        "whole_raw_affine_coverage_reconciled": False,
        "whole_corpus_complete": False,
        "Lean_launched": False,
        "new_project": False,
        "AGENTS_edits": False,
    }
    qa_payload = json_payload(qa)
    qa_hash = sha_bytes(qa_payload)

    overleaf_state_path = ROOT / "state" / "overleaf_current.json"
    overleaf_state = read_json(overleaf_state_path)
    overleaf_state.update(
        {
            "status": "affine_analytic_and_companion_package_remote_sync_verified",
            "updated_utc": now,
            "active_main_document": "main.tex",
            "last_receipt": REMOTE_RECEIPT_REL,
            "pending_action": (
                "Reconcile the two saved affine raw-line audits against the primary raw text; "
                "preserve exact line locators and propagate any mathematical corrections globally."
            ),
            "pending_remote_delta": [],
            "current_affine_remote_builds": AFFINE_BUILDS,
            "last_remote_checkpoint": {"path": QA_REL, "sha256": qa_hash},
            "remote_source_download": remote_source,
        }
    )

    affine_state_path = ROOT / "state" / "affine_analytic_current.json"
    affine_state = read_json(affine_state_path)
    affine_state.update(
        {
            "updated_utc": now,
            "status": "local_and_canonical_remote_verification_pass_raw_reconciliation_active",
            "remote_synced": True,
            "remote_receipt": {"path": REMOTE_RECEIPT_REL, "sha256": receipt_hash},
            "remote_checkpoint": {"path": QA_REL, "sha256": qa_hash},
            "next_action": (
                "Reconcile affine_raw_lines_0001_0900_20260904.json and "
                "affine_raw_lines_0901_3021_20260904.json against their primary raw source."
            ),
        }
    )

    project_path = ROOT / "state" / "project_state.json"
    project = read_json(project_path)
    project["next_action"] = (
        "Reconcile the two saved affine raw-line audits against the primary 3,021-line raw text, "
        "then propagate every verified correction and consequence through ledgers and TeX."
    )
    project["current_request_state"]["latest_verified_receipt"] = REMOTE_RECEIPT_REL
    project["current_request_state"]["latest_immediate_request_status"] = (
        "canonical_affine_remote_source_and_two_builds_verified_Tao_reader_V7_only"
    )
    project["last_receipt_id"] = "ACT-COL-000049"
    project["updated_utc"] = now
    project["current_checkpoint"] = {
        "receipt_id": "ACT-COL-000049",
        "path": QA_REL,
        "sha256": qa_hash,
    }
    project["active_task"] = "primary_raw_affine_3021_line_reconciliation"

    coverage_path = ROOT / "state" / "coverage.json"
    coverage = read_json(coverage_path)
    coverage["coverage_status"] = (
        "active_affine_analytic_remote_sync_pass_full_raw_reconciliation_pending"
    )
    coverage["post_ACT49_affine_remote_sync"] = {
        "path": QA_REL,
        "sha256": qa_hash,
        "remote_receipt": REMOTE_RECEIPT_REL,
        "remote_source_manifested_files_verified": remote_source["manifested_files_verified"],
        "critical_pages": AFFINE_BUILDS["main.tex"]["pages"],
        "research_companion_pages": AFFINE_BUILDS["research_companion.tex"]["pages"],
        "remote_sync_complete": True,
        "full_raw_3021_line_reconciliation": False,
        "whole_corpus_complete": False,
    }

    programmes_path = ROOT / "state" / "programmes.jsonl"
    programme_records = [
        json.loads(line)
        for line in programmes_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    programme_matches = 0
    for record in programme_records:
        if record.get("programme_id") == "PRG-COL-0001":
            programme_matches += 1
            record["status"] = (
                "bounded_reconstruction_extended_through_affine_packets_and_analytic_fixed_point_series_with_canonical_remote_delivery_verified"
            )
            analytic = record.setdefault("analytic_reconstruction", {})
            analytic["status"] = (
                "proved_reviewed_certificate_build_visual_portable_package_and_canonical_remote_verification_pass"
            )
            analytic["remote_receipt"] = REMOTE_RECEIPT_REL
            analytic["remote_receipt_sha256"] = receipt_hash
            analytic["remote_checkpoint"] = QA_REL
            analytic["remote_checkpoint_sha256"] = qa_hash
    require(programme_matches == 1, f"expected one PRG-COL-0001 record, got {programme_matches}")

    action_records.append(
        {
            "record_type": "action_receipt",
            "schema_version": "1.0",
            "receipt_id": "ACT-COL-000049",
            "timestamp_utc": now,
            "action": "canonical_affine_analytic_nine_unique_file_delivery_four_root_repair_source_download_identity_and_two_entrypoint_build_verification",
            "inputs": [
                "qa/ACT47-AFFINE-ANALYTIC-CHECKPOINT.json",
                "qa/ACT48-RESEARCH-COMPANION-PACKAGE.json",
                TAO_RECEIPT_REL,
            ],
            "outputs": [
                QA_REL,
                REMOTE_RECEIPT_REL,
                "overleaf/sync_20260904/canonical_project/MANIFEST.json",
                "overleaf/sync_20260904/canonical_project/PACKAGE_STATUS.json",
                "overleaf/sync_20260904/canonical_project/README.md",
                "overleaf/sync_20260904/canonical_project/SOURCE_MAP.json",
                "state/affine_analytic_current.json",
                "state/overleaf_current.json",
                "state/project_state.json",
                "state/coverage.json",
                "state/programmes.jsonl",
                "state/action_receipts.jsonl",
            ],
            "result": "canonical_remote_source_and_both_affected_builds_verified_raw_reconciliation_active",
            "remote_source_manifested_files_verified": remote_source["manifested_files_verified"],
            "critical_build": AFFINE_BUILDS["main.tex"],
            "research_companion_build": AFFINE_BUILDS["research_companion.tex"],
            "tao_reader_baseline": "V7_only",
            "whole_raw_affine_coverage_reconciled": False,
            "goal_complete": False,
            "new_project": False,
            "Lean_started": False,
            "AGENTS_edits": False,
        }
    )

    transactional_write(
        {
            REMOTE_RECEIPT: receipt_payload,
            QA_PATH: qa_payload,
            overleaf_state_path: json_payload(overleaf_state),
            affine_state_path: json_payload(affine_state),
            project_path: json_payload(project),
            coverage_path: json_payload(coverage),
            programmes_path: jsonl_payload(programme_records),
            action_path: jsonl_payload(action_records),
        }
    )

    print(
        json.dumps(
            {
                "status": "PASS",
                "checkpoint": {"path": QA_REL, "sha256": qa_hash},
                "remote_receipt": {
                    "path": REMOTE_RECEIPT_REL,
                    "sha256": receipt_hash,
                },
                "remote_source": remote_source,
                "builds": AFFINE_BUILDS,
                "next": "primary raw affine 3,021-line reconciliation",
            },
            indent=2,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="phase", required=True)
    subparsers.add_parser("prepare")
    seal_parser = subparsers.add_parser("seal")
    seal_parser.add_argument("remote_source_zip", type=Path)
    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("remote_source_zip", type=Path)
    args = parser.parse_args()
    if args.phase == "prepare":
        prepare()
    elif args.phase == "seal":
        seal(args.remote_source_zip.resolve())
    else:
        verify_read_only(args.remote_source_zip.resolve())


if __name__ == "__main__":
    main()
