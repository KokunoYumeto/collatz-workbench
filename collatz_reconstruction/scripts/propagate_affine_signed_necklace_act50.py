from __future__ import annotations

import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

EXPECTED = {
    "state/source_registry.jsonl": "3a000ea4bcfa129055bf47eaca2b2153909f0b82181d1ac90c2ed5bb80519975",
    "state/claims.jsonl": "608cd37d102cf7ee93ceb1d7abefe619c504090aeaf4f5a2fab82d545aa91210",
    "state/programmes.jsonl": "63cd8efafcfbbf9f9eb47d66d11c892bb4a97252b823bdedfa917991a0a42ef1",
    "state/affine_packet_current.json": "61ef9902b3ac5d5837bfd17f86509e91e6122738eb19ea5cc877466d505e3432",
    "state/affine_analytic_current.json": "3bfda9379b6f72a8d38d7c61100165aed5749718b483d0f9b4bf7d6032ff38d8",
    "state/project_state.json": "0c89d764749df79bd6917a269f5c0761cf25aa1d8e026b37b547dbd248bbd12f",
    "state/coverage.json": "a6ee8cfd3766aeeaf4d0ea16a39373590decc4056e960e1cf19fc4f832052ebe",
    "state/overleaf_current.json": "4fac5856a1487e6857e872b789174c9c8911f94178622ba31f39da304ddeb1d3",
    "state/action_receipts.jsonl": "6a5bed33e921a55967f8824cb40c4a4c8ceb4826bf3a5bb9dbf71f88e78ee553",
}

SUPPORT = {
    "TODO.md": "7d5065c0e55e98e6ade826f851b8d06ef4684d10473ce14f6050c4246d203136",
    "research_companion/chapters/04_affine_packets_parity_necklaces_and_residue_automata.tex": "6537c8391e349aaa4aa4361c5fd0dee8fd44fc112a685f7edf19240587c19476",
    "tex/chapters/06_affine_packet_source_audit.tex": "27f1f0986c8191bba5ce9e5711e2e1c154fad6bf6b2406f73149ffae5d7c171e",
    "research_companion/certificates/affine_signed_necklace_checks.py": "8e51437eb64c5c9cee6601d6fe654383302a3ee3d1430c52981ec9b773c29c97",
    "research_companion/audit/affine_signed_necklace_checks_20260905.json": "b2037db0fe04451f54e5edb6742d9b811735324a471a0c924d1b2d6b976d866d",
    "research_companion/audit/affine_signed_necklace_reconstruction_20260905.json": "c76f9f5e111c38289e63c0aa609bf2634c0df89ed4df415ad146ae3445feb455",
    "research_companion/bibliography.tex": "5c2737630d5e8e1c597c78bdfb12b26b7fdd424ea1d9f0e1e6f0004859518ad1",
    "tex/chapters/99_source_register.tex": "791a8c4bd83e11c3987d6d432ac5c7db0e25c063499159b92df6f1d04a02ba1c",
}

SOURCE_ID = "SRC-COL-000052"
CLAIM_ID = "CLM-COL-000200"
RECEIPT_ID = "ACT-COL-000050"


def sha(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def read_json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def read_jsonl(relative: str) -> list[dict]:
    return [
        json.loads(line)
        for line in (ROOT / relative).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def jsonl_bytes(records: list[dict]) -> bytes:
    return (
        "\n".join(
            json.dumps(record, ensure_ascii=False, separators=(",", ":"))
            for record in records
        )
        + "\n"
    ).encode("utf-8")


def file_record(relative: str) -> dict:
    path = ROOT / relative
    return {"path": relative, "bytes": path.stat().st_size, "sha256": sha(path)}


def append_unique(values: list, value) -> None:
    if value not in values:
        values.append(value)


def put_file_record(records: list[dict], relative: str) -> None:
    current = file_record(relative)
    for index, record in enumerate(records):
        if record.get("path") == relative:
            records[index] = current
            return
    records.append(current)


def commit(outputs: dict[str, bytes]) -> None:
    staged: list[tuple[Path, Path]] = []
    backups: list[tuple[Path, bytes]] = []
    try:
        for relative, payload in outputs.items():
            target = ROOT / relative
            descriptor, temporary = tempfile.mkstemp(
                prefix=f".{target.name}.act50-", suffix=".tmp", dir=target.parent
            )
            os.close(descriptor)
            temporary_path = Path(temporary)
            temporary_path.write_bytes(payload)
            staged.append((target, temporary_path))
            backups.append((target, target.read_bytes()))
        replaced: list[Path] = []
        try:
            for target, temporary_path in staged:
                os.replace(temporary_path, target)
                replaced.append(target)
        except Exception:
            for target, original in reversed(backups):
                if target in replaced:
                    target.write_bytes(original)
            raise
    finally:
        for _, temporary_path in staged:
            temporary_path.unlink(missing_ok=True)


def main() -> None:
    for relative, expected in {**EXPECTED, **SUPPORT}.items():
        require(sha(ROOT / relative) == expected, f"preflight hash mismatch: {relative}")

    now = datetime.now(timezone.utc).isoformat()
    chapter = file_record(
        "research_companion/chapters/04_affine_packets_parity_necklaces_and_residue_automata.tex"
    )
    critical = file_record("tex/chapters/06_affine_packet_source_audit.tex")
    certificate = file_record(
        "research_companion/certificates/affine_signed_necklace_checks.py"
    )
    certificate_receipt = file_record(
        "research_companion/audit/affine_signed_necklace_checks_20260905.json"
    )
    reconstruction_audit = file_record(
        "research_companion/audit/affine_signed_necklace_reconstruction_20260905.json"
    )

    sources = read_jsonl("state/source_registry.jsonl")
    require(sources[0].get("next_id") == SOURCE_ID, "unexpected next source ID")
    require(
        all(record.get("source_id") != SOURCE_ID for record in sources[1:]),
        f"duplicate {SOURCE_ID}",
    )
    sources[0]["next_id"] = "SRC-COL-000053"
    sources.append(
        {
            "record_type": "source_document",
            "schema_version": "1.0",
            "source_id": SOURCE_ID,
            "authors": ["Richard P. Stanley"],
            "title": "Enumerative Combinatorics, Volume 2",
            "bibliographic_identity": {
                "edition": "second edition",
                "series": "Cambridge Studies in Advanced Mathematics",
                "series_volume": 208,
                "publisher": "Cambridge University Press",
                "publication_year": 2024,
                "doi": "10.1017/9781009262538",
                "isbn_hardback": "978-1-009-26249-1",
                "isbn_paperback": "978-1-009-26248-4",
            },
            "manifestations": [
                {
                    "path": "C:/Users/LOCAL_USER/Documents/Papors/OS/Hardy-Littlewood-Pólya theorem/Enumerative Combinatorics Volume 2 Second Edition ( etc.).pdf",
                    "role": "controlling_local_published_book_PDF",
                    "bytes": 20_755_788,
                    "sha256": "5b5d3bfa241c1fd4302cc7817aab1bf73c66795ce2a462ffc14837149cdcf457",
                    "pdf_pages": 802,
                }
            ],
            "route_ids": [],
            "route_integrity": {
                "status": "completed_index_queried_without_exact_route_then_authorized_OS_shelf_file_read_directly",
                "frozen_ledgers_mutated": False,
                "routing_metadata_used_as_theorem_evidence": False,
            },
            "reading": {
                "status": "complete_for_fixed_content_primitive_necklace_formula",
                "locators": [
                    "physical PDF p.498 / printed p.480: Exercise 7.89(a), equations (7.149)-(7.150)",
                    "physical PDF p.573 / printed p.555: solution identifies primitive necklaces counted by occurrences of each colour",
                    "physical PDF front matter: author, edition, publisher, year, DOI, ISBN and series identity",
                ],
                "method": "Relevant pages rendered and visually inspected at original detail; bibliographic front matter extracted and checked. No whole-book reading claimed.",
                "source_objects": {
                    "multivariate_Lyndon_series": "L_n(x)=sum_alpha f(alpha)x^alpha over weak compositions alpha of n",
                    "Witt_formula": "L_n=(1/n) sum_{d|n} mu(d) p_d^(n/d)",
                    "binary_coefficient": "For content (m,A-m), coefficient extraction gives (1/A) sum_{d|gcd(A,m)} mu(d) binom(A/d,m/d).",
                },
            },
            "audit": {
                "path": reconstruction_audit["path"],
                "sha256": reconstruction_audit["sha256"],
                "status": "direct_page_and_formula_crosswalk",
            },
            "nonclaims": [
                "No whole-book reading is claimed.",
                "The source contains no Collatz-specific sign partition or exponent-packet groupoid.",
                "The fixed-content enumeration is classical and is not claimed as a new result.",
                "No protected bulk book text is copied into the portable or Overleaf packages.",
            ],
        }
    )

    claims = read_jsonl("state/claims.jsonl")
    require(claims[0].get("next_id") == CLAIM_ID, "unexpected next claim ID")
    require(
        all(record.get("claim_id") != CLAIM_ID for record in claims[1:]),
        f"duplicate {CLAIM_ID}",
    )
    claims[0]["next_id"] = "CLM-COL-000201"
    claims.append(
        {
            "record_type": "claim",
            "schema_version": "1.0",
            "claim_id": CLAIM_ID,
            "claim_type": "independent_constructive_deduction_with_classical_enumerative_lineage",
            "status": "proved",
            "statement": "For m>=1 and A>=m, with g=gcd(m,A), the number of primitive pointed exponent words is W(m,A)=sum_(d|g)mu(d)binom(A/d-1,m/d-1). The exact-period rational orbit count is N_orb=W/m=(1/A)sum_(d|g)mu(d)binom(A/d,m/d). Its positive and negative parts are the indicators of 2^A>3^m and 2^A<3^m times N_orb, respectively; equality is impossible. The corresponding point counts are m times the orbit counts. If gcd(m,A)=1, every word is primitive, so N_orb=binom(A-1,m-1)/m and N_pt=binom(A-1,m-1). At m=1,A=1 this is the negative fixed point -1; m=1,A>=2 gives one positive rational fixed point; A=m>1 contributes no exact-period-m orbit.",
            "source_ids": ["SRC-COL-000052", "SRC-COL-000013", "SRC-COL-000004"],
            "dependencies": ["CLM-COL-000182", "CLM-COL-000183", "CLM-COL-000184"],
            "morphism_refs": ["MOR-COL-000064", "MOR-COL-000065"],
            "local_source_refs": ["CHATINT-COL-000002"],
            "source_locators": [
                "Raw affine Chatnotes physical lines 1041-1083",
                "Local antecedent TeX lines 2537-2628 and 2750-2791",
                "Stanley 2024 physical PDF p.498 / printed p.480, Exercise 7.89(a), equations (7.149)-(7.150); solution physical PDF p.573 / printed p.555",
                "Lagarias 1990 printed pp.36-39, especially equations (2.1) and (2.4)-(2.7)",
                "Laarhoven-de Weger v1 source lines 303-315",
            ],
            "proof_locator": {
                "path": chapter["path"],
                "label": "thm:signed-fixed-content-necklace-count",
            },
            "formal_status": {
                "status": "general_written_proof_and_bounded_exact_certificate_no_Lean",
                "artifact": certificate["path"],
                "artifact_sha256": certificate["sha256"],
                "execution_receipt": certificate_receipt["path"],
                "execution_receipt_sha256": certificate_receipt["sha256"],
                "reconstruction_audit": reconstruction_audit["path"],
                "reconstruction_audit_sha256": reconstruction_audit["sha256"],
                "metrics_sha256": "e5b5e44e3737c67631a79231b0b333ceebb7166a387d38d2028c4ca27836cb6b",
                "verified_metrics": {
                    "parameter_pairs": 100,
                    "composition_words": 39_202,
                    "primitive_words": 39_022,
                    "primitive_orbits": 6_136,
                    "positive_primitive_points": 38_097,
                    "negative_primitive_points": 925,
                },
            },
            "source_repairs": [
                "Raw line 1083 conflates primitive words with periodic points; the proof separates pointed words, cyclic orbits and individual points.",
                "The antecedent's pointed-periodic-word biconditional is already repaired in CLM-COL-000193 and is not used here.",
                "The common-divisor Möbius convolution and both directions of the primitive-root decomposition are stated explicitly.",
            ],
            "nonclaims": [
                "No novelty or priority is claimed for the fixed-content necklace formula.",
                "The bounded certificate does not replace the all-parameter proof.",
                "Rational orbit counts and their signs do not establish integrality or global Collatz termination.",
                "No complete reconciliation of all 3021 raw lines or of the wider corpus follows from this block.",
            ],
        }
    )

    programmes = read_jsonl("state/programmes.jsonl")
    programme = next(
        record for record in programmes if record.get("programme_id") == "PRG-COL-0001"
    )
    programme["status"] = (
        "bounded_reconstruction_extended_through_affine_packets_analytic_series_"
        "and_signed_fixed_content_counts_remote_resync_pending"
    )
    append_unique(programme["literature_sources"], SOURCE_ID)
    append_unique(
        programme["definitions"],
        "primitive pointed packet words, fixed-content cyclic orbit classes, individual orbit points, and their denominator-sign split",
    )
    append_unique(programme["proved_results"], CLAIM_ID)
    append_unique(
        programme["repairs"],
        "separated primitive pointed words, cyclic rational orbits, and individual orbit points in the raw signed-count block",
    )
    append_unique(
        programme["contradictions_and_retractions"],
        "the local antecedent's equality-of-pointed-periodic-words iff cyclic-conjugacy-of-roots biconditional is false; CLM-COL-000193 retains the valid base-point-aligned statement",
    )
    cert_programme_record = {
        **certificate,
        "status": "PASS_bounded_exact_signed_fixed_content_necklace_checks",
        "execution_receipt": certificate_receipt["path"],
        "execution_receipt_sha256": certificate_receipt["sha256"],
    }
    if not any(
        item.get("path") == certificate["path"] for item in programme["certificates"]
    ):
        programme["certificates"].append(cert_programme_record)
    programme["signed_necklace_reconstruction"] = {
        "claim": CLAIM_ID,
        "source": SOURCE_ID,
        "raw_locator": "CHATINT-COL-000002 physical lines 1041-1083",
        "proof": {"path": chapter["path"], "label": "thm:signed-fixed-content-necklace-count"},
        "critical_crosswalk": critical,
        "certificate": cert_programme_record,
        "audit": reconstruction_audit,
        "remote_sync_complete": False,
        "whole_raw_reconciliation_complete": False,
    }

    packet = read_json("state/affine_packet_current.json")
    packet.update(
        checkpoint="AFFINE-SIGNED-NECKLACE-20260905",
        updated_utc=now,
        scope="Exact fixed-content primitive-word, cyclic-orbit and orbit-point counts, transported through the packet groupoid and split by the sign of 2^A-3^m; raw lines 1041-1083 reconciled, wider affine reading active",
        remote_sync_status="local_signed_necklace_revision_remote_resync_pending",
        next_action="Reconcile raw affine physical lines 1091-1208: packet envelopes, integer-candidate bounds and the one-large-exponent staircase. State actual integral-cycle consequences separately from rational packet geometry.",
        whole_source_coverage_reconciled=False,
        portable_apparatus_complete=False,
        fresh_context_full_recovery_pass_claimed=False,
        formal_status="all-parameter proof and exact finite Python certificate; no Lean launch; package rebuild pending",
    )
    append_unique(packet["claims"], CLAIM_ID)
    for relative in (
        chapter["path"],
        critical["path"],
        certificate["path"],
        certificate_receipt["path"],
        reconstruction_audit["path"],
    ):
        put_file_record(packet["files"], relative)
    packet["source_reading"]["signed_count_block"] = (
        "Root-direct raw physical lines 1041-1208; lines 1041-1083 admitted through CLM-COL-000200."
    )
    packet["source_reading"]["Stanley2024"] = (
        "Physical PDF pp.498 and 573 rendered and directly inspected for Exercise 7.89(a) and its solution."
    )
    packet["signed_necklace_reconstruction"] = {
        "claim": CLAIM_ID,
        "source": SOURCE_ID,
        "morphisms": ["MOR-COL-000064", "MOR-COL-000065"],
        "certificate": certificate,
        "execution_receipt": certificate_receipt,
        "audit": reconstruction_audit,
        "remote_sync_complete": False,
        "page_QA_complete": False,
    }

    analytic = read_json("state/affine_analytic_current.json")
    analytic.update(
        updated_utc=now,
        status="local_signed_fixed_content_necklace_reconstruction_admitted_remote_resync_pending_raw_reconciliation_active",
        active_tex=chapter["path"],
        parallel_tex=critical["path"],
        scope="Fixed-content primitive packet words, exact-period rational orbits, orbit points and the denominator-sign split",
        remote_synced=False,
        full_goal_complete=False,
        whole_raw_audit_complete=False,
        Lean_launched=False,
        next_action="Reconcile raw affine physical lines 1091-1208: packet envelopes and the one-large-exponent staircase, with exact separation of rational and integral-cycle consequences.",
    )
    append_unique(analytic["claims_reserved"], CLAIM_ID)
    append_unique(analytic["claims"], CLAIM_ID)
    analytic["signed_necklace_reconstruction"] = {
        "claim": CLAIM_ID,
        "source": SOURCE_ID,
        "raw_locator": "CHATINT-COL-000002 physical lines 1041-1083",
        "proof": chapter,
        "critical_crosswalk": critical,
        "certificate": certificate,
        "execution_receipt": certificate_receipt,
        "audit": reconstruction_audit,
        "morphisms_used": ["MOR-COL-000064", "MOR-COL-000065"],
        "typed_source_repairs": [
            "raw line 1083 word/orbit/point conflation",
            "antecedent pointed-periodic-word biconditional already repaired by CLM-COL-000193",
        ],
        "remote_sync_complete": False,
        "package_validation_complete": False,
        "page_QA_complete": False,
    }

    project = read_json("state/project_state.json")
    project.update(
        updated_utc=now,
        next_action="Reconcile raw affine physical lines 1091-1208: prove the exact packet envelopes and one-large-exponent staircase, then propagate only their proved rational and integral consequences.",
        last_receipt_id=RECEIPT_ID,
        active_task="primary_raw_affine_packet_envelope_staircase_reconciliation",
    )
    request = project["current_request_state"]
    request.update(
        active_local_tex=chapter["path"],
        active_parallel_tex=critical["path"],
        active_tex_sha256=chapter["sha256"],
        active_parallel_tex_sha256=critical["sha256"],
        active_write_status="signed_fixed_content_necklace_result_admitted_local_package_and_remote_resync_pending_raw_affine_reconciliation_active",
        latest_immediate_request_status="Tao_preprint_verified_V7_only_signed_affine_necklace_block_proved_and_literature_crosswalked",
    )
    request["active_content_reading"] = {
        "source": "CHATINT-COL-000002",
        "source_sha256": "abb1abbb948dc140394de3d35f0efbde9b3facdf718c24b065b8d0adb951366e",
        "bounded_direct_read_records": [
            {
                "path": "research_companion/audit/affine_raw_lines_0001_0900_20260904.json",
                "physical_lines": "1-900",
                "sha256": "0299448c8fd0de315be1a0e2902fbe21c52c69ac841a739c976a88b00a238a7d",
            },
            {
                "path": "research_companion/audit/affine_raw_lines_0901_3021_20260904.json",
                "physical_lines": "901-3021",
                "sha256": "35e550dc3013d60130e3199df09259a037b3455b90e928a9fa3d687f1f2",
            },
        ],
        "root_direct_recheck": "physical lines 1041-1208",
        "mathematically_reconciled_this_action": "physical lines 1041-1083",
        "next_block": "physical lines 1091-1208",
        "whole_source_mathematical_reconciliation_complete": False,
    }
    project["latest_local_admission"] = {
        "receipt_id": RECEIPT_ID,
        "claim": CLAIM_ID,
        "source": SOURCE_ID,
        "audit": reconstruction_audit,
        "remote_sync_complete": False,
        "sealed_checkpoint_remains": project["current_checkpoint"],
    }

    coverage = read_json("state/coverage.json")
    coverage["coverage_status"] = (
        "active_signed_fixed_content_necklace_block_reconciled_"
        "portable_build_visual_and_remote_sync_pending_wider_raw_reconciliation_active"
    )
    for layer in coverage["layers"]:
        if layer.get("layer_id") == "LIT":
            layer.update(
                status="foundational_spine_in_progress_52_bounded_content_read_source_documents_including_Stanley_fixed_content_necklace_source_remaining_literature_continues",
                documents_read=52,
                documents_admitted=52,
                reading_count_boundary="Count is admitted source_document records, not whole-source reads. SRC-COL-000052 was read only at the exact fixed-content necklace and bibliographic locators.",
            )
        elif layer.get("layer_id") == "CHAT":
            layer.update(
                status="pinned_Zn_export_complete_direct_locator_audit_affine_export_has_bounded_direct_read_records_for_1_3021_and_incremental_mathematical_reconciliation_through_signed_count_block",
                bounded_direct_read_records=[
                    "research_companion/audit/affine_raw_lines_0001_0900_20260904.json",
                    "research_companion/audit/affine_raw_lines_0901_3021_20260904.json",
                ],
                reconciled_affine_blocks=[
                    "CHATINT-COL-000002:959-1040 packet/cyclic transport represented by CLM-COL-000182 through CLM-COL-000184",
                    "CHATINT-COL-000002:1041-1083 signed fixed-content counts represented by CLM-COL-000200",
                ],
                next_continuous_range="CHATINT-COL-000002:1091-1208 packet envelopes and one-large-exponent staircase",
                whole_affine_mathematical_reconciliation_complete=False,
            )
        elif layer.get("layer_id") == "FORMAL":
            inventory = sorted(
                path.relative_to(ROOT).as_posix()
                for directory in (ROOT / "certificates", ROOT / "research_companion/certificates")
                for path in directory.glob("*.py")
            )
            require(len(inventory) == 30, "unexpected current certificate inventory")
            layer.update(
                status="30_distinct_current_Python_certificate_artifacts_with_recorded_PASS_runs_signed_necklace_certificate_rerun_current_optimized_runs_fail_closed",
                artifacts_verified=30,
                artifact_counting_rule="Distinct current .py files under certificates and research_companion/certificates with a recorded normal PASS run at their respective checkpoint; not all 30 were rerun in ACT50.",
                artifact_inventory=inventory,
                signed_necklace_certificate={
                    "path": certificate["path"],
                    "sha256": certificate["sha256"],
                    "status": "PASS",
                    "check_families": 9,
                    "metrics_sha256": "e5b5e44e3737c67631a79231b0b333ceebb7166a387d38d2028c4ca27836cb6b",
                },
            )
    coverage["post_ACT50_signed_fixed_content_necklace_reconstruction"] = {
        "receipt_id": RECEIPT_ID,
        "claim": CLAIM_ID,
        "source": SOURCE_ID,
        "morphisms_used": ["MOR-COL-000064", "MOR-COL-000065"],
        "certificate": certificate,
        "execution_receipt": certificate_receipt,
        "audit": reconstruction_audit,
        "companion_chapter": chapter,
        "critical_chapter": critical,
        "remote_sync_complete": False,
        "portable_package_validation_complete": False,
        "visual_QA_complete": False,
        "full_raw_3021_line_reconciliation": False,
        "whole_corpus_complete": False,
    }

    overleaf = read_json("state/overleaf_current.json")
    overleaf.update(
        status="signed_fixed_content_necklace_local_revision_remote_resync_pending",
        updated_utc=now,
        pending_action="Build and visually inspect the signed fixed-content revision, refresh the 18-file portable companion manifest and seven-certificate validator, then upload the exact nine-path delta to this same canonical project.",
        pending_remote_delta=[
            "companion/bibliography.tex",
            "companion/chapters/04_affine_packets_parity_necklaces_and_residue_automata.tex",
            "companion/certificates/affine_signed_necklace_checks.py",
            "critical/chapters/06_affine_packet_source_audit.tex",
            "critical/chapters/99_source_register.tex",
            "SOURCE_MAP.json",
            "PACKAGE_STATUS.json",
            "README.md",
            "MANIFEST.json",
        ],
        tao_unchanged_by_current_sync=True,
    )
    overleaf["local_signed_necklace_revision"] = {
        "claim": CLAIM_ID,
        "source": SOURCE_ID,
        "proof": chapter,
        "critical_crosswalk": critical,
        "certificate": certificate,
        "execution_receipt": certificate_receipt,
        "audit": reconstruction_audit,
        "package_validation_complete": False,
        "visual_QA_complete": False,
        "remote_sync_complete": False,
        "canonical_project_unchanged": True,
        "new_project_created": False,
    }

    receipts = read_jsonl("state/action_receipts.jsonl")
    receipt_numbers = sorted(int(record["receipt_id"].rsplit("-", 1)[1]) for record in receipts)
    require(receipt_numbers == list(range(1, 50)), "action receipt IDs are not exactly 1-49")
    receipts.append(
        {
            "record_type": "action_receipt",
            "schema_version": "1.0",
            "receipt_id": RECEIPT_ID,
            "timestamp_utc": now,
            "action": "signed_fixed_content_affine_packet_necklace_formula_classical_lineage_exact_groupoid_transport_denominator_sign_split_typed_word_orbit_point_repair_and_global_local_state_admission",
            "inputs": [
                "CHATINT-COL-000002 physical lines 1041-1083",
                "SRC-COL-000052",
                "SRC-COL-000013",
                "SRC-COL-000004",
                "MOR-COL-000064",
                "MOR-COL-000065",
            ],
            "outputs": [
                chapter["path"],
                critical["path"],
                "research_companion/bibliography.tex",
                "tex/chapters/99_source_register.tex",
                certificate["path"],
                certificate_receipt["path"],
                reconstruction_audit["path"],
                "research_companion/README.md",
                "research_companion/provenance.json",
                "research_companion/validate_package.py",
                "state/source_registry.jsonl",
                "state/claims.jsonl",
                "state/programmes.jsonl",
                "state/affine_packet_current.json",
                "state/affine_analytic_current.json",
                "state/project_state.json",
                "state/coverage.json",
                "state/overleaf_current.json",
                "state/action_receipts.jsonl",
                "TODO.md",
            ],
            "result": "local_all_parameter_proof_literature_crosswalk_bounded_exact_certificate_and_global_state_propagation_pass_package_visual_and_remote_sync_pending",
            "claims": [CLAIM_ID],
            "sources": [SOURCE_ID],
            "morphisms_used": ["MOR-COL-000064", "MOR-COL-000065"],
            "artifacts": {
                "companion_chapter": chapter,
                "critical_chapter": critical,
                "certificate": certificate,
                "certificate_execution": certificate_receipt,
                "reconstruction_audit": reconstruction_audit,
            },
            "mathematical_boundary": {
                "raw_lines_reconciled": "1041-1083",
                "next_raw_lines": "1091-1208",
                "fixed_content_formula_classical": True,
                "Collatz_specific_groupoid_transport_and_sign_split_proved": True,
                "word_orbit_point_types_separated": True,
                "whole_raw_affine_coverage_reconciled": False,
                "whole_corpus_complete": False,
            },
            "certificate_metrics": {
                "status": "PASS",
                "parameter_pairs": 100,
                "composition_words": 39_202,
                "primitive_words": 39_022,
                "primitive_orbits": 6_136,
                "positive_primitive_points": 38_097,
                "negative_primitive_points": 925,
                "metrics_sha256": "e5b5e44e3737c67631a79231b0b333ceebb7166a387d38d2028c4ca27836cb6b",
            },
            "portable_package_validation_complete": False,
            "visual_QA_complete": False,
            "remote_sync_complete": False,
            "goal_complete": False,
            "Lean_started": False,
            "AGENTS_edits": False,
            "new_project": False,
            "tao_reader_baseline": "V7_only_zero_V5_references",
        }
    )

    outputs = {
        "state/source_registry.jsonl": jsonl_bytes(sources),
        "state/claims.jsonl": jsonl_bytes(claims),
        "state/programmes.jsonl": jsonl_bytes(programmes),
        "state/affine_packet_current.json": json_bytes(packet),
        "state/affine_analytic_current.json": json_bytes(analytic),
        "state/project_state.json": json_bytes(project),
        "state/coverage.json": json_bytes(coverage),
        "state/overleaf_current.json": json_bytes(overleaf),
        "state/action_receipts.jsonl": jsonl_bytes(receipts),
    }
    commit(outputs)

    print(
        json.dumps(
            {
                "status": "PASS",
                "source": SOURCE_ID,
                "claim": CLAIM_ID,
                "receipt": RECEIPT_ID,
                "outputs": {
                    relative: {"bytes": (ROOT / relative).stat().st_size, "sha256": sha(ROOT / relative)}
                    for relative in outputs
                },
                "remote_sync_complete": False,
                "whole_raw_reconciliation_complete": False,
                "Lean_launched": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
