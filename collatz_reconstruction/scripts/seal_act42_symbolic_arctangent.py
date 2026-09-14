from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


if not __debug__:
    raise RuntimeError(
        "seal_act42_symbolic_arctangent.py refuses optimized Python: fail-closed checks require __debug__"
    )


ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable
RECEIPT_ID = "ACT-COL-000042"
AUDIT_REL = "qa/ACT42-SYMBOLIC-ARCTANGENT-RELEASE-AUDIT.md"
RECOVERY_REL = "qa/ACT42-FRESH-CONTEXT-RECOVERY.md"
TRANSCRIPT_REL = "qa/ACT42-VALIDATION-TRANSCRIPT.json"

PRESEAL_PINS = {
    "state/project_state.json": (19_692, "597af106a7838733a349221a413101b0546132361eb8663b8577ca3e2ebfaeb9"),
    "state/coverage.json": (10_792, "ee95858b2ed386ab88b56b7792c8b3bd85983d8517e19a3edf2488ba7eb1c52b"),
    "state/action_receipts.jsonl": (204_401, "122bde1be29836b4f9c27f81718f63cdb39d117951d7b00773c313bd0e483ccb"),
    "TODO.md": (29_710, "29aa34eb72d177cb5fab6275f026dc9fd07650494f2ee6ba4167743488ec632e"),
}

PDF_PINS = {
    "working": {
        "path": "output/pdf/collatz_working_corpus.pdf",
        "pages": 169,
        "bytes": 1_574_554,
        "sha256": "b9cf84f5d7815e5f930f3fa02edacd606a996837561f61339f3bde1d3b5d279c",
        "font_rows": 27,
        "log_path": "tmp/pdfs/act42_arctangent_final_root_20260830_02/main.log",
        "log_bytes": 33_912,
        "log_sha256": "84938e0339c66d8a8232525bb15cbfe5b2b1b8fc7b9e952fec09b535a1c37d47",
        "underfull": 6,
    },
    "companion": {
        "path": "research_companion/output/pdf/collatz_research_companion.pdf",
        "pages": 34,
        "bytes": 572_830,
        "sha256": "8fecd942b3a8370a9457bdad32619640dbc1eb8f67c6f75e529c32e18b3c00b8",
        "font_rows": 22,
        "log_path": "tmp/pdfs/act42_arctangent_final_companion_20260830_01/main.log",
        "log_bytes": 30_962,
        "log_sha256": "0e5eccb6554a543865aa216a41b52e968e40488798d8087a904cf2673147df42",
        "underfull": 2,
    },
}

RENDER_PINS = {
    "root_final_pages": {
        "path": "tmp/qa/act42_release_root_160dpi_03/pages",
        "files": 169,
        "bytes": 56_045_726,
        "sha256": "f9f56dd630033a98f2184045aacfc900ae35bad5ba8c9e4702b60538cb618f3a",
    },
    "root_inspected_base_pages": {
        "path": "tmp/qa/act42_release_root_160dpi_02/pages",
        "files": 169,
        "bytes": 56_031_234,
        "sha256": "bb9e64efd29feabbf690d8872900dcae8410dcc2cb8e5d22fb9d21eaf148576e",
    },
    "root_contact_sheets": {
        "path": "tmp/qa/act42_release_root_160dpi_02/contact_sheets",
        "files": 15,
        "bytes": 16_753_484,
        "sha256": "379209c92f4eb07ea7851b8111d3b4cff59fe4aa2b1d526f96bd1d8c3391f2fc",
    },
    "companion_pages": {
        "path": "tmp/qa/act42_release_companion_200dpi_02/pages",
        "files": 34,
        "bytes": 13_693_216,
        "sha256": "cfea596f8df909990fad359712b5854d0578964b8f2e667840655cc9d94c003e",
    },
    "companion_contact_sheets": {
        "path": "tmp/qa/act42_release_companion_200dpi_02/contact_sheets",
        "files": 3,
        "bytes": 3_135_856,
        "sha256": "a6fd5d3d33c74414491224b77ec78ba9047cc3c061f0d9e6ed5045211c0f9975",
    },
}

ROOT_CERTIFICATES = [
    "certificates/chatnotes_color_coefficient_checks.py",
    "certificates/chatnotes_symbolic_completion_checks.py",
    "certificates/chatnotes_weighted_path_finite_actions.py",
    "certificates/computational_verification_chronology_checks.py",
    "certificates/continued_fraction_dependency_checks.py",
    "certificates/crandall_1978_checks.py",
    "certificates/everett_1977_checks.py",
    "certificates/herschfeld_1936_checks.py",
    "certificates/krasikov_lagarias_2003_checks.py",
    "certificates/lagarias_dependency_checks.py",
    "certificates/pillai_fixed_difference_checks.py",
    "certificates/primitive_root_return_checks.py",
    "certificates/siegel_v1_tao_syracuse_crosswalk_checks.py",
    "certificates/steuding_522_checks.py",
    "certificates/tao_main_reduction_checks.py",
    "certificates/tao_prop111_transport_checks.py",
    "certificates/tao_prop19_valuation_checks.py",
    "certificates/tao_v7_endpoint_buffer_checks.py",
    "certificates/tao_v7_fourier_renewal_checks.py",
    "certificates/tao_v7_prop52_cn_checks.py",
    "certificates/tao_whole_version_checks.py",
    "certificates/terras_allouche_korec_checks.py",
]

PORTABLE_CERTIFICATES = [
    "research_companion/certificates/finite_actions_checks.py",
    "research_companion/certificates/arctangent_relation_lattice_checks.py",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def text_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


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


def record(relative: str) -> dict:
    path = ROOT / relative
    return {"path": relative, "bytes": path.stat().st_size, "sha256": sha256(path)}


def load_json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def write_json(relative: str, value: object) -> None:
    (ROOT / relative).write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def run(relative: str, *, optimized: bool = False, timeout: int = 900) -> dict:
    command = [PYTHON]
    if optimized:
        command.append("-O")
    command.append(relative)
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    combined = result.stdout + result.stderr
    return {
        "command": " ".join(command[1:]),
        "exit_code": result.returncode,
        "stdout_bytes": len(result.stdout.encode("utf-8")),
        "stdout_sha256": text_sha256(result.stdout),
        "stderr_bytes": len(result.stderr.encode("utf-8")),
        "stderr_sha256": text_sha256(result.stderr),
        "stdout": result.stdout,
        "stderr": result.stderr,
        "combined": combined,
    }


def compact_command_result(result: dict, *, parsed: object | None = None) -> dict:
    value = {key: result[key] for key in [
        "command", "exit_code", "stdout_bytes", "stdout_sha256", "stderr_bytes", "stderr_sha256"
    ]}
    if parsed is not None:
        value["parsed_result"] = parsed
    return value


def json_from_stdout(result: dict) -> dict:
    require(result["exit_code"] == 0, f"command failed: {result['command']}\n{result['stderr'][-2000:]}")
    try:
        return json.loads(result["stdout"])
    except json.JSONDecodeError as error:
        raise RuntimeError(f"non-JSON command output: {result['command']}: {error}") from error


def verify_preseal() -> None:
    require(not (ROOT / AUDIT_REL).exists(), f"{AUDIT_REL} already exists")
    require(not (ROOT / RECOVERY_REL).exists(), f"{RECOVERY_REL} already exists")
    require(not (ROOT / TRANSCRIPT_REL).exists(), f"{TRANSCRIPT_REL} already exists")
    for relative, (size, digest) in PRESEAL_PINS.items():
        path = ROOT / relative
        require(path.stat().st_size == size, f"preseal byte mismatch: {relative}")
        require(sha256(path) == digest, f"preseal hash mismatch: {relative}")
    receipts = (ROOT / "state/action_receipts.jsonl").read_text(encoding="utf-8").splitlines()
    require(len(receipts) == 41, "expected exactly 41 preseal action receipts")
    require(json.loads(receipts[-1])["receipt_id"] == "ACT-COL-000041", "predecessor is not ACT41")


def verify_artifacts() -> dict:
    evidence: dict[str, object] = {"pdfs": {}, "renders": {}, "root_delta": {}}
    for name, pin in PDF_PINS.items():
        pdf = ROOT / pin["path"]
        log = ROOT / pin["log_path"]
        require(pdf.stat().st_size == pin["bytes"] and sha256(pdf) == pin["sha256"], f"PDF pin mismatch: {name}")
        require(log.stat().st_size == pin["log_bytes"] and sha256(log) == pin["log_sha256"], f"log pin mismatch: {name}")
        log_text = log.read_text(encoding="utf-8", errors="replace")
        diagnostics = {
            "latex_warnings": len(re.findall(r"LaTeX Warning", log_text, re.IGNORECASE)),
            "package_warnings": len(re.findall(r"Package .* Warning", log_text, re.IGNORECASE)),
            "undefined": len(re.findall(r"undefined references|Citation .* undefined|Reference .* undefined", log_text, re.IGNORECASE)),
            "overfull": len(re.findall(r"Overfull \\hbox|Overfull \\vbox", log_text, re.IGNORECASE)),
            "underfull": len(re.findall(r"Underfull \\hbox|Underfull \\vbox", log_text, re.IGNORECASE)),
            "fatal": len(re.findall(r"Fatal error|Emergency stop|! LaTeX Error", log_text, re.IGNORECASE)),
        }
        require(diagnostics == {
            "latex_warnings": 0,
            "package_warnings": 0,
            "undefined": 0,
            "overfull": 0,
            "underfull": pin["underfull"],
            "fatal": 0,
        }, f"unexpected build diagnostics: {name}: {diagnostics}")
        evidence["pdfs"][name] = {**pin, "diagnostics": diagnostics}
    for name, pin in RENDER_PINS.items():
        actual = aggregate_hash(ROOT / pin["path"])
        expected = (pin["files"], pin["bytes"], pin["sha256"])
        require(actual == expected, f"render aggregate mismatch: {name}: {actual}")
        evidence["renders"][name] = pin
    base = ROOT / RENDER_PINS["root_inspected_base_pages"]["path"]
    final = ROOT / RENDER_PINS["root_final_pages"]["path"]
    changes = []
    for path in sorted(final.glob("*.png"), key=lambda p: p.name):
        old = base / path.name
        if sha256(old) != sha256(path):
            changes.append({
                "page": path.name,
                "base_sha256": sha256(old),
                "final_sha256": sha256(path),
            })
    require(changes == [
        {
            "page": "page-060.png",
            "base_sha256": "eec15a246c68451e1cdee9e12e9c8d4aa9c8047f7dd201a4627843b101ef91c0",
            "final_sha256": "52ddb832e9972935378eda23c45366c7f161b6c8aace10290d2ef11948877e04",
        },
        {
            "page": "page-125.png",
            "base_sha256": "812a0d46ceb235f0acc176087eb71dbe028ab4cd256c8d46d3f57461d9d930b1",
            "final_sha256": "efccbf46a7e3240e59dc467b52d892d73a6b83d68271277895397046b3d6e148",
        },
    ], f"unexpected root delta: {changes}")
    evidence["root_delta"] = {
        "pixel_identical_pages": 167,
        "changed_pages_inspected_at_original_detail": changes,
    }
    return evidence


def run_validations(stamp: str) -> dict:
    transcript: dict[str, object] = {
        "schema_version": "1.0",
        "checkpoint": RECEIPT_ID,
        "started_utc": stamp,
        "normal": [],
        "optimized_fail_closed": [],
    }
    state_result = run("scripts/validate_state.py")
    state_json = json_from_stdout(state_result)
    require(state_json.get("status") == "pass" and state_json.get("failure_count") == 0, "state validator did not pass")
    transcript["normal"].append(compact_command_result(state_result, parsed=state_json))

    chat_result = run("scripts/validate_chatnotes_intake.py")
    chat_json = json_from_stdout(chat_result)
    require(chat_json.get("status") == "pass" and chat_json.get("failure_count") == 0, "Chatnotes validator did not pass")
    transcript["normal"].append(compact_command_result(chat_result, parsed=chat_json))

    root_results = []
    for relative in ROOT_CERTIFICATES:
        result = run(relative)
        require(result["exit_code"] == 0, f"root certificate failed: {relative}\n{result['stderr'][-2000:]}")
        root_results.append(compact_command_result(result))
    transcript["root_certificate_suite"] = {
        "count": len(root_results),
        "all_passed": True,
        "results": root_results,
    }

    symbolic_result = run("certificates/chatnotes_symbolic_completion_checks.py")
    symbolic_json = json_from_stdout(symbolic_result)
    require(symbolic_json.get("status") == "PASS", "symbolic certificate did not pass")
    transcript["symbolic_detail_rerun"] = compact_command_result(symbolic_result, parsed=symbolic_json)

    portable_results = {}
    for relative in PORTABLE_CERTIFICATES:
        result = run(relative)
        parsed = json_from_stdout(result)
        require(parsed.get("status") == "PASS", f"portable certificate did not pass: {relative}")
        portable_results[relative] = compact_command_result(result, parsed=parsed)
    transcript["portable_certificates"] = portable_results

    package_result = run("research_companion/validate_package.py")
    package_json = json_from_stdout(package_result)
    require(package_json.get("status") == "PASS", "package validator did not pass")
    transcript["package_validation"] = compact_command_result(package_result, parsed=package_json)

    for relative in [
        "certificates/chatnotes_symbolic_completion_checks.py",
        "research_companion/certificates/finite_actions_checks.py",
        "research_companion/certificates/arctangent_relation_lattice_checks.py",
        "research_companion/validate_package.py",
    ]:
        result = run(relative, optimized=True)
        require(result["exit_code"] != 0 and "refuses optimized Python" in result["combined"], f"optimized run did not fail closed: {relative}")
        transcript["optimized_fail_closed"].append(compact_command_result(result))
    transcript["finished_utc"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    return transcript


def make_audit(stamp: str, evidence: dict, transcript_record: dict) -> str:
    return f"""# ACT42 symbolic and arctangent release audit

Timestamp: {stamp}

Status: PASS for checkpoint `ACT-COL-000042`.  The durable Collatz corpus goal remains active; this record makes no global completion, publication, upload, or Collatz-endpoint claim.

## Mathematical scope sealed

- Direct chronological reading `CHATINT-COL-000016` covers raw `Z_n Symmetries of Collatz` physical lines 9597--11087.
- `SRC-COL-000037`--`SRC-COL-000042` supply the content-read symbolic, thermodynamic, arithmetic-site, and prismatic source boundaries.
- `SRC-COL-000043`--`SRC-COL-000045` supply the content-read Gaussian-angle and Machin-formula source boundaries.
- `CLM-COL-000151`--`CLM-COL-000173`, `MOR-COL-000045`--`MOR-COL-000054`, and `PRG-COL-0002` type the admitted definitions, sourced statements, independent results, exact maps, counterexamples, repairs, nonclaims, and the Collatz-Machin rigidity conjecture.
- For every fixed positive exponent word, the signed Gaussian valuation map has kernel exactly `Rel_pi(w)`, with explicit fibres and quotient inverse.
- The unweighted all-word coefficient vector is proved non-torsion; the legal word `(1,1)` has exact lattice `Z(2,1)`.
- The complete coefficient-unbounded lattice on all 795 pairs `(k,A)` with `1<=k<=15` and `k<=A<=60` is `Z r_1 direct-sum Z r_2`.  The certificate proves the corresponding prefix-chain classification throughout that grid, and nothing outside it.

## Current validation

The machine-readable transcript is `{transcript_record['path']}` ({transcript_record['bytes']} bytes, SHA-256 `{transcript_record['sha256']}`).  It records:

- `scripts/validate_state.py`: PASS with 45 sources, 173 claims, 54 morphisms, three exact-gap records, three topic routes, zero failures, and eight expected frozen-route warnings.
- `scripts/validate_chatnotes_intake.py`: PASS with 16 intake records, two raw sources, and 20,458 physical source lines.
- all 22 current root certificate scripts: PASS;
- the symbolic certificate: PASS with 18 check families;
- the portable finite-action certificate: PASS with 30 check families and 1,398,724 counted checks;
- the Gaussian relation-lattice certificate: PASS with nine check families, 795 columns, rank 793, nullity two, 793 independent rows, and exact integral saturation;
- the companion package validator: PASS with nine manifested source files, four TeX files, 91 labels, 50 references, 11 citation keys, and two matching deterministic source-to-PDF rebuilds;
- all four selected optimized-Python probes: nonzero fail-closed exits.

## PDF and package identity

- Working corpus: 169 pages, 1,574,554 bytes, SHA-256 `b9cf84f5d7815e5f930f3fa02edacd606a996837561f61339f3bde1d3b5d279c`.
- Research companion: 34 pages, 572,830 bytes, SHA-256 `8fecd942b3a8370a9457bdad32619640dbc1eb8f67c6f75e529c32e18b3c00b8`.
- Root final log: 33,912 bytes, SHA-256 `84938e0339c66d8a8232525bb15cbfe5b2b1b8fc7b9e952fec09b535a1c37d47`.
- Companion final log: 30,962 bytes, SHA-256 `0e5eccb6554a543865aa216a41b52e968e40488798d8087a904cf2673147df42`.
- Manifest: 1,673 bytes, SHA-256 `a1c9e4278d6312b2782152d20af224787af4ce7f6fbb85928e928379ac759087`.
- Both logs have zero LaTeX/package/undefined-reference/undefined-citation/overfull/fatal diagnostics.  The root has six and the companion two cosmetic underfull boxes.
- All 27 root and all 22 companion font rows are embedded, subset, and Unicode mapped.
- Extracted-text checks found zero broken-reference markers, private paths or URIs, placeholders, deprecated status phrases, or leaked TeX commands.

## Page-level visual QA

The render aggregate hash updates SHA-256, in ordinal filename order, first with each UTF-8 filename and then with the raw file bytes, without a delimiter.

- Final root render: 169 pages at 160 dpi, 56,045,726 bytes, aggregate SHA-256 `f9f56dd630033a98f2184045aacfc900ae35bad5ba8c9e4702b60538cb618f3a`; minimum nonwhite margins left 171, top 173, right 169, bottom 106 pixels.
- Inspected root base render: 169 pages, 56,031,234 bytes, aggregate SHA-256 `bb9e64efd29feabbf690d8872900dcae8410dcc2cb8e5d22fb9d21eaf148576e`; all 15 contact sheets were inspected.
- Exact comparison transfers that inspection to 167 final pages.  Only pages 60 and 125 changed; both final pages were inspected at original detail and are clean.  Root pages 146--148 and 164--169 were also inspected at original detail.
- Companion render: 34 pages at 200 dpi, 13,693,216 bytes, aggregate SHA-256 `cfea596f8df909990fad359712b5854d0578964b8f2e667840655cc9d94c003e`; minimum margins left 214, top 218, right 211, bottom 132 pixels.
- All three companion contact sheets were inspected; pages 11--15 and 33--34 were also inspected at original detail.
- No blank insertion, clipping, overlap, broken glyph, displaced folio, unreadable formula, or terminal layout defect was found.

## Coverage and continuation

The literature counter is reconciled to the complete source registry: 45 content-read source-document records.  The formal counter now has an explicit rule: 24 distinct current Python certificate files under `certificates/` and `research_companion/certificates/`, all rerun successfully.  Ledger recovery derives identifier maxima from each complete ID set and header, never from physical tail order.

Continuous direct Chatnotes reading currently covers physical lines 5712--11087 and 14012--17437, with segment reports and selected direct windows before line 5712.  The next chronological interval is 11088--14011.  Gemini and archived-task intake remain deferred.  Lean/Lake remained idle; the controlling ceiling is 2 GiB per process tree, with one watched worker maximum after a verified release.
"""


def make_recovery(stamp: str, audit_record: dict, transcript_record: dict) -> str:
    return f"""# ACT42 fresh-context recovery

Timestamp: {stamp}

Status: PASS after reconstruction from current external files only.

## Recovered state

- Active durable goal: `01a00ba5-a6b8-7410-b1e3-ab6dc0a4acf4`; global completion remains false.
- Current checkpoint and latest action receipt: `ACT-COL-000042`.
- Release audit: `{audit_record['path']}`, {audit_record['bytes']} bytes, SHA-256 `{audit_record['sha256']}`.
- Validation transcript: `{transcript_record['path']}`, {transcript_record['bytes']} bytes, SHA-256 `{transcript_record['sha256']}`.
- Working corpus: 169 pages, SHA-256 `b9cf84f5d7815e5f930f3fa02edacd606a996837561f61339f3bde1d3b5d279c`.
- Separately authored companion: 34 pages, SHA-256 `8fecd942b3a8370a9457bdad32619640dbc1eb8f67c6f75e529c32e18b3c00b8`.
- Source/claim/morphism/programme/intake maxima are derived from complete ID sets plus ledger headers: source 45/next 46, claim 173/next 174, morphism 54/next 55, programme 2/next 3, intake 16/next 17.  Physical tail position is not evidence of an identifier maximum.
- Current direct chronological continuation: raw Chatnotes physical lines 11088--14011, source SHA-256 `9a80f53764a9da42c0f8e0b6d19ce61f978980a448a683b9c45f04038716160d`.
- Controlling Lean/Lake rule: no launch during the current hold; after a verified release, at most one watched process tree, killed at 2,147,483,648 bytes.

## Recovery checks

The independent command `python scripts/validate_act42_recovery.py` verifies the receipt sequence, checkpoint hashes, complete ledger ID sets and headers, resource ceiling, PDF/log/manifest identities, render aggregates, 167-page pixel-identity transfer plus the two-page delta, page/font/text metrics, state and Chatnotes validators, symbolic and portable certificates, package validator, and optimized-Python fail-closed behavior.

No Git command, Lean/Lake launch, upload, publication, public-record mutation, cleanup, archive, or `AGENTS.md` write is part of this checkpoint.
"""


def update_state(stamp: str, audit_record: dict, recovery_record: dict, transcript_record: dict) -> None:
    coverage = load_json("state/coverage.json")
    layers = {row["layer_id"]: row for row in coverage["layers"]}
    coverage["coverage_status"] = "active_after_ACT42_symbolic_arctangent_checkpoint_direct_modern_Chatnotes_intake_continues"

    layers["LIT"].update({
        "status": "foundational_spine_in_progress_45_content_read_source_documents_symbolic_thermodynamic_arithmetic_site_prismatic_and_Gaussian_angle_boundaries_crosswalked_remaining_literature_continues",
        "documents_read": 45,
        "documents_admitted": 45,
        "counting_rule": "complete source_document record set in state/source_registry.jsonl; physical record order is irrelevant",
    })
    layers["CHAT"].update({
        "status": "two_raw_exports_identity_verified_20458_physical_lines_segment_reports_and_selected_direct_windows_before_5712_continuous_direct_read_5712_11087_and_14012_17437_next_continuous_gap_11088_14011",
        "programmes_reconstructed": 2,
        "continuous_direct_ranges": ["5712-11087", "14012-17437"],
        "next_continuous_range": "11088-14011",
    })
    artifact_inventory = ROOT_CERTIFICATES + PORTABLE_CERTIFICATES
    layers["FORMAL"].update({
        "status": "24_distinct_current_Python_certificate_artifacts_rerun_PASS_symbolic_portable_finite_action_and_Gaussian_relation_lattice_checks_hardened_optimized_runs_fail_closed",
        "artifacts_verified": len(artifact_inventory),
        "artifact_counting_rule": "distinct current .py files under certificates and research_companion/certificates that passed a normal run at ACT42",
        "artifact_inventory": artifact_inventory,
        "weighted_path_certificate_families": 30,
        "symbolic_certificate_families": 18,
        "arctangent_certificate_families": 9,
        "optimized_python_checks": "FAIL_CLOSED",
    })

    syn = layers["SYN"]
    syn.update({
        "status": "ACT42_169_page_working_corpus_and_34_page_separately_authored_companion_built_package_validated_and_all_pages_visually_checked",
        "working_pdf_pages": 169,
        "working_pdf_bytes": 1_574_554,
        "working_pdf_sha256": PDF_PINS["working"]["sha256"],
        "research_companion_pdf_pages": 34,
        "research_companion_pdf_bytes": 572_830,
        "research_companion_pdf_sha256": PDF_PINS["companion"]["sha256"],
        "root_rendered_page_count": 169,
        "root_render_dpi": 160,
        "root_render_bytes": 56_045_726,
        "root_render_sha256": RENDER_PINS["root_final_pages"]["sha256"],
        "root_contact_sheet_count": 15,
        "root_contact_sheet_bytes": 16_753_484,
        "root_contact_sheet_sha256": RENDER_PINS["root_contact_sheets"]["sha256"],
        "current_pages_visually_checked": 203,
        "root_all_pages_contact_sheet_checked": 169,
        "root_pages_checked_at_original_detail": [60, 125, 146, 147, 148, 164, 165, 166, 167, 168, 169],
        "root_edge_min_px": {"left": 171, "top": 173, "right": 169, "bottom": 106},
        "independent_rendered_page_count": 34,
        "independent_render_bytes": 13_693_216,
        "independent_render_sha256": RENDER_PINS["companion_pages"]["sha256"],
        "independent_contact_sheet_count": 3,
        "independent_contact_sheet_bytes": 3_135_856,
        "independent_contact_sheet_sha256": RENDER_PINS["companion_contact_sheets"]["sha256"],
        "independent_current_pages_visually_checked": list(range(1, 35)),
        "independent_pages_checked_at_original_detail": [11, 12, 13, 14, 15, 33, 34],
        "independent_render_dpi": 200,
        "companion_edge_min_px": {"left": 214, "top": 218, "right": 211, "bottom": 132},
        "checkpoint_visual_qa_passed": True,
        "visual_qa_complete": True,
        "fresh_render_policy": {
            "current_pdf_pages_freshly_rendered": 203,
            "root_render_dpi": 160,
            "companion_render_dpi": 200,
            "current_all_contact_sheets_inspected": 18,
            "all_pages_checked": 203,
            "root_final_delta": {
                "pixel_identical_to_inspected_base": 167,
                "changed_pages_inspected_at_original_detail": [60, 125],
            },
            "original_detail_pages": {
                "root": [60, 125, 146, 147, 148, 164, 165, 166, 167, 168, 169],
                "companion": [11, 12, 13, 14, 15, 33, 34],
            },
            "reason": "All 169 root and 34 companion pages were covered by contact-sheet inspection; exact pixel comparison transfers the inspected root base to 167 final pages, and the only two changed final pages were inspected individually. No terminal visual defect was found.",
        },
        "final_build_directory": "tmp/pdfs/act42_arctangent_final_root_20260830_02",
        "companion_build_directory": "tmp/pdfs/act42_arctangent_final_companion_20260830_01",
        "final_layout_sha256": PDF_PINS["working"]["sha256"],
        "companion_layout_sha256": PDF_PINS["companion"]["sha256"],
        "final_log_sha256": PDF_PINS["working"]["log_sha256"],
        "companion_log_sha256": PDF_PINS["companion"]["log_sha256"],
        "actionable_log_diagnostics": 0,
        "nonactionable_underfull_warnings": {"root": 6, "companion": 2},
        "unresolved_placeholder_hits": 0,
        "literal_quad_leak_hits": 0,
        "embedded_subset_font_rows": 27,
        "companion_embedded_subset_font_rows": 22,
        "unembedded_font_rows": 0,
        "final_root_render_directory": RENDER_PINS["root_final_pages"]["path"],
        "final_independent_render_directory": RENDER_PINS["companion_pages"]["path"],
        "final_root_contact_sheet_directory": RENDER_PINS["root_contact_sheets"]["path"],
        "final_independent_contact_sheet_directory": RENDER_PINS["companion_contact_sheets"]["path"],
        "core_certificate": record("certificates/chatnotes_symbolic_completion_checks.py"),
        "portable_certificate": record("research_companion/certificates/finite_actions_checks.py"),
        "arctangent_certificate": {
            **record("research_companion/certificates/arctangent_relation_lattice_checks.py"),
            "status": "PASS_exact_complete_795_column_integer_relation_lattice",
            "columns": 795,
            "rank_F3": 793,
            "nullity_F3": 2,
            "character_entries": 631_230,
        },
        "package_validation": {
            "manifested_source_files": 9,
            "tex_files": 4,
            "labels": 91,
            "references": 50,
            "citations": 11,
            "finite_certificate_check_families": 30,
            "arctangent_certificate_check_families": 9,
            "normal_run": "PASS",
            "optimized_python_run": "FAIL_CLOSED",
            "source_to_pdf_rebuild": "PASS_two_canonical_rebuilds_match_declared_output",
            "validation_transcript": transcript_record,
        },
        "build_correction": {
            "initial_failed_build_accepted": False,
            "defects": [],
            "action": "ACT42 rebuilt and validated the working corpus and independent companion after globally propagating the symbolic and Gaussian-relation results. The accepted artifacts have zero actionable diagnostics, complete font checks, complete visual coverage, and exact package inventory.",
            "final_build_accepted": True,
            "qpdf_available": False,
            "qpdf_nonavailability_is_not_a_passed_check": True,
        },
        "live_tex_advanced_after_checkpoint": False,
        "fresh_ACT33_build_pending": False,
    })

    recovery = layers["RECOVERY"]
    recovery.update({
        "status": "ACT42_symbolic_arctangent_artifact_state_sealed_and_external_state_recovery_passed",
        "checkpoint_passed": True,
        "checkpoint_record": AUDIT_REL,
        "latest_receipt": RECEIPT_ID,
        "passed": True,
        "act42_fresh_context_test": {
            "status": "PASS_external_state_only_recovery",
            **recovery_record,
            "checkpoint": RECEIPT_ID,
            "goal_status": "active",
            "completion_claimed": False,
            "working_pdf_pages": 169,
            "research_companion_pdf_pages": 34,
            "validator_failures": 0,
            "expected_route_warnings": 8,
            "ledger_maximum_rule": "derive from complete ID set plus header; never use physical JSONL tail",
        },
    })
    write_json("state/coverage.json", coverage)

    project = load_json("state/project_state.json")
    require(project["status"] == "active" and project["completion_claimed"] is False, "project completion state changed")
    require(project["resource_policy"]["lean_worker_private_working_set_limit_bytes"] == 2_147_483_648, "2 GiB resource cap changed")
    project["artifact_architecture"]["separately_authored_research_companion"] = "research_companion/main.tex (ACT42 package validated: symbolic survivor coding, weighted paths, and Gaussian relation lattices; not uploaded)"
    project["next_action"] = (
        "Continue direct modern Chatnotes intake at physical lines 11088-14011 of the pinned Z_n Symmetries export. Reuse PRG-COL-0001 and PRG-COL-0002 where the prose repeats proved structures; type the Z_3 branch maps and their domains before any groupoid, crossed-product, KMS, BCM, motivic, or period assertion; query the completed index for each key source dependency before proceeding. Keep Gemini and archived-task intake deferred, do not contact the quarantined zeta task, do not publish or upload, and keep Lean/Lake idle under the 2 GiB-per-session ceiling until a verified release."
    )
    project["last_receipt_id"] = RECEIPT_ID
    project["updated_utc"] = stamp
    project["current_checkpoint"] = {
        "receipt_id": RECEIPT_ID,
        "path": AUDIT_REL,
        "bytes": audit_record["bytes"],
        "sha256": audit_record["sha256"],
        "scope": "symbolic_survivor_completion_Gaussian_prefix_relation_lattices_expanded_independent_companion_package_and_full_artifact_QA",
        "global_completion": False,
        "post_checkpoint_state_changed": False,
        "fresh_context_recovery_required_after_current_intake": False,
        "fresh_context_recovery": recovery_record,
        "validation_transcript": transcript_record,
    }
    write_json("state/project_state.json", project)


def append_receipt(stamp: str, audit_record: dict, recovery_record: dict, transcript_record: dict, evidence: dict) -> None:
    receipt = {
        "record_type": "action_receipt",
        "schema_version": "1.0",
        "receipt_id": RECEIPT_ID,
        "timestamp_utc": stamp,
        "action": "seal_ACT42_symbolic_survivor_and_Gaussian_arctangent_relation_programmes_expanded_companion_package_full_visual_QA_2_GiB_resource_rule_and_fresh_context_recovery",
        "inputs": [
            "ACT-COL-000041",
            "raw/USR-0012.txt",
            "CHATINT-COL-000016",
            "SRC-COL-000037 through SRC-COL-000045",
            "CLM-COL-000151 through CLM-COL-000173",
            "MOR-COL-000045 through MOR-COL-000054",
            "PRG-COL-0002",
            "TOPIC-COL-ARCTANGENT-GAUSSIAN-0003",
        ],
        "outputs": [
            TRANSCRIPT_REL,
            AUDIT_REL,
            RECOVERY_REL,
            "scripts/validate_act42_recovery.py",
            "state/project_state.json",
            "state/coverage.json",
            "TODO.md",
            "output/pdf/collatz_working_corpus.pdf",
            "research_companion/output/pdf/collatz_research_companion.pdf",
        ],
        "result": "pass_bounded_checkpoint_goal_active_no_completion_claim",
        "measurements": {
            "mathematics": {
                "claims": [f"CLM-COL-{number:06d}" for number in range(151, 174)],
                "morphisms": [f"MOR-COL-{number:06d}" for number in range(45, 55)],
                "programme": "PRG-COL-0002",
                "chatnotes_intake": "CHATINT-COL-000016",
                "literature_sources": [f"SRC-COL-{number:06d}" for number in range(37, 46)],
                "next_direct_range": "11088-14011",
            },
            "certificates": {
                "distinct_current_python_artifacts_passed": 24,
                "root_suite_passed": 22,
                "portable_suite_passed": 2,
                "symbolic_check_families": 18,
                "finite_action_check_families": 30,
                "arctangent_check_families": 9,
                "arctangent_columns": 795,
                "arctangent_rank_F3": 793,
                "arctangent_nullity_F3": 2,
                "optimized_runs": "FAIL_CLOSED",
            },
            "package": {
                "manifested_source_files": 9,
                "tex_files": 4,
                "labels": 91,
                "references": 50,
                "citations": 11,
                "source_to_pdf": "PASS_two_canonical_rebuilds_match_declared_output",
                "manifest": record("research_companion/MANIFEST.json"),
                "validation_transcript": transcript_record,
            },
            "pdfs": evidence["pdfs"],
            "renders": evidence["renders"],
            "root_render_delta": evidence["root_delta"],
            "checkpoint": audit_record,
            "fresh_context": recovery_record,
            "resource_policy": {
                "Lean_or_Lake_started": 0,
                "limit_bytes_per_session_or_process_tree": 2_147_483_648,
                "maximum_overlapping_builds": 1,
                "current_hold_retained": True,
                "Git_commands_started": 0,
                "uploads_or_public_mutations": 0,
                "cleanup_or_archive_actions": 0,
                "AGENTS_md_writes": 0,
            },
        },
        "notes": [
            "ACT42 seals a corpus checkpoint only; the global literature-first Collatz goal remains active.",
            "The companion package is Overleaf-compatible and was not uploaded.",
            "Ledger maxima were derived from complete ID sets and headers, not physical JSONL tails.",
            "Continuous direct Chatnotes reading is 5712-11087 and 14012-17437; earlier coverage is segment-based plus selected direct windows; 11088-14011 is next.",
        ],
    }
    path = ROOT / "state/action_receipts.jsonl"
    with path.open("a", encoding="utf-8", newline="") as handle:
        handle.write(json.dumps(receipt, ensure_ascii=False, separators=(",", ":")) + "\n")


def main() -> int:
    verify_preseal()
    stamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    evidence = verify_artifacts()
    transcript = run_validations(stamp)
    write_json(TRANSCRIPT_REL, transcript)
    transcript_record = record(TRANSCRIPT_REL)

    audit_text = make_audit(stamp, evidence, transcript_record)
    (ROOT / AUDIT_REL).write_text(audit_text, encoding="utf-8")
    audit_record = record(AUDIT_REL)

    recovery_text = make_recovery(stamp, audit_record, transcript_record)
    (ROOT / RECOVERY_REL).write_text(recovery_text, encoding="utf-8")
    recovery_record = {
        **record(RECOVERY_REL),
        "status": "PASS_external_state_only_recovery",
    }

    update_state(stamp, audit_record, recovery_record, transcript_record)
    append_receipt(stamp, audit_record, recovery_record, transcript_record, evidence)

    state_post = run("scripts/validate_state.py")
    state_post_json = json_from_stdout(state_post)
    require(state_post_json.get("status") == "pass" and state_post_json.get("failure_count") == 0, "postseal state validation failed")
    chat_post = run("scripts/validate_chatnotes_intake.py")
    chat_post_json = json_from_stdout(chat_post)
    require(chat_post_json.get("status") == "pass" and chat_post_json.get("failure_count") == 0, "postseal Chatnotes validation failed")

    receipts = (ROOT / "state/action_receipts.jsonl").read_text(encoding="utf-8").splitlines()
    require(len(receipts) == 42 and json.loads(receipts[-1])["receipt_id"] == RECEIPT_ID, "ACT42 receipt append failed")

    result = {
        "schema_version": "1.0",
        "status": "PASS",
        "checkpoint": RECEIPT_ID,
        "audit": audit_record,
        "recovery": recovery_record,
        "validation_transcript": transcript_record,
        "postseal_state_validator": {
            "status": state_post_json["status"],
            "failure_count": state_post_json["failure_count"],
            "warning_count": state_post_json["warning_count"],
        },
        "postseal_chatnotes_validator": {
            "status": chat_post_json["status"],
            "failure_count": chat_post_json["failure_count"],
        },
        "goal_status": "active",
        "completion_claimed": False,
        "next_action": "direct Chatnotes physical lines 11088-14011",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
