from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


if not __debug__:
    raise RuntimeError(
        "seal_act43_groupoid_motivic.py refuses optimized Python: fail-closed checks require __debug__"
    )


ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable
RECEIPT_ID = "ACT-COL-000043"
AUDIT_REL = "qa/ACT43-GROUPOID-MOTIVIC-RELEASE-AUDIT.md"
RECOVERY_REL = "qa/ACT43-FRESH-CONTEXT-RECOVERY.md"
TRANSCRIPT_REL = "qa/ACT43-VALIDATION-TRANSCRIPT.json"
RECOVERY_VALIDATOR_REL = "scripts/validate_act43_recovery.py"

PRESEAL_PINS = {
    "state/project_state.json": (19_955, "e3fcb8c9fd039a46f5088bb17c4c7f2af4f2a248dc9f689b81ae2fe631dc1f47"),
    "state/coverage.json": (14_176, "d1a9bad7dd853ebd062beb7dc3e8c436fc203e61a459d12eca2fada3420f4610"),
    "state/action_receipts.jsonl": (210_450, "97219936b6ff4266b7b375fec04aeeca159574a8f57b7a3de3fa214941105bba"),
    "TODO.md": (30_589, "e59108b94d6459b4342268d77cdd1b745cccd35914edac562b9becb46f7307fe"),
    "state/source_registry.jsonl": (178_667, "68610c65277e8893263e10f058b5c79ac593d59512654d57bbb203b66c4c09e5"),
    "state/claims.jsonl": (230_195, "6a4c35ff2a977d5e01a038d9c03ecf2ea346c779b332fa61b044a20facdd2495"),
    "state/morphisms.jsonl": (107_914, "e7f053aed8dcaaedfb667e73a96c2b16b4be07091ae64246d5c067014b50d7b2"),
    "state/chatnotes_intake.jsonl": (21_039, "e6ed2b8526de0e1e0beadb99c01b610affe0aecdbf2946929da696673e31a82e"),
    "state/programmes.jsonl": (11_211, "87d36968d26e058a7fce1cf5c10cfd05f93a2aa14eeb2537187077e612727577"),
    "state/topic_routes.jsonl": (29_252, "c26ec78aa2a801b765a9c91049c72e7bc796532a74f6166270fe71e2ce6823a2"),
    "research_companion/MANIFEST.json": (2_037, "8e09c9c21fb6d08cfc66bb765945cf8fa44a96ee68260f35fc57870e617c18e9"),
    RECOVERY_VALIDATOR_REL: (15_046, "ca3d0f7173c5e2f5f20af0699841ac44db044419facf4c1d3cc7f4cf721d4ebc"),
}

PDF_PINS = {
    "working": {
        "path": "output/pdf/collatz_working_corpus.pdf",
        "pages": 176,
        "bytes": 1_630_444,
        "sha256": "c03e4000464940377b2bdef87e19d0d92e9c4ddba7a570424ac5b0c72fbbf15e",
        "font_rows": 29,
        "log_path": "tmp/pdfs/act43_groupoid_motivic_final_root_20260830_03/main.log",
        "log_bytes": 34_440,
        "log_sha256": "ca2b648e364413cfe0fc25efc5d3a226a1f13229c4d092cfea8912c531444a64",
        "underfull": 6,
    },
    "companion": {
        "path": "research_companion/output/pdf/collatz_research_companion.pdf",
        "pages": 42,
        "bytes": 636_148,
        "sha256": "5c734ac770501539c36f9fe782395b26483caa09e8ec15d8602ded23eeb65441",
        "font_rows": 22,
        "log_path": "research_companion/tmp/pdfs/act43_groupoid_motivic_final_companion_20260830_04/main.log",
        "log_bytes": 31_264,
        "log_sha256": "e3443f945b40094a39cbebf0462b47815cdcfb23145190436c9b94dbd2942e43",
        "underfull": 2,
    },
}

RENDER_PINS = {
    "root_pages": {
        "path": "tmp/qa/act43_release_root_160dpi_01/pages",
        "files": 176,
        "bytes": 58_530_850,
        "sha256": "2dfc78d765c7c2f1b8ac90031708c7a87d557811234e054970c20c34a6bc6e77",
    },
    "root_contact_sheets": {
        "path": "tmp/qa/act43_release_root_160dpi_01/contact_sheets",
        "files": 15,
        "bytes": 7_804_730,
        "sha256": "e24bc32ea6675abbf595a79d617517d3da04e3641c9a05c7e7b4a23d317b22a4",
    },
    "companion_pages": {
        "path": "tmp/qa/act43_release_companion_200dpi_01/pages",
        "files": 42,
        "bytes": 17_174_756,
        "sha256": "28e941bb4c111e2dc379166e01393959e6d1f67f735bc861b1ba4a2ccc82242b",
    },
    "companion_contact_sheets": {
        "path": "tmp/qa/act43_release_companion_200dpi_01/contact_sheets",
        "files": 3,
        "bytes": 1_756_417,
        "sha256": "d1b0941a25852c31bcdbc782045fb54228dbf7f4a641bbd8fa8f2d86217d0c2c",
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
    "research_companion/certificates/groupoid_motivic_interface_checks.py",
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


def text_sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


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


def record(relative: str) -> dict:
    path = ROOT / relative
    return {"path": relative, "bytes": path.stat().st_size, "sha256": sha256(path)}


def load_json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def write_json(relative: str, value: object) -> None:
    (ROOT / relative).write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def run(relative: str, *, optimized: bool = False, timeout: int = 1200) -> dict:
    command = [PYTHON]
    if optimized:
        command.append("-O")
    command.append(relative)
    process = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    return {
        "command": " ".join(command[1:]),
        "exit_code": process.returncode,
        "stdout_bytes": len(process.stdout.encode("utf-8")),
        "stdout_sha256": text_sha256(process.stdout),
        "stderr_bytes": len(process.stderr.encode("utf-8")),
        "stderr_sha256": text_sha256(process.stderr),
        "stdout": process.stdout,
        "stderr": process.stderr,
        "combined": process.stdout + process.stderr,
    }


def compact(result: dict, *, parsed: object | None = None) -> dict:
    value = {
        key: result[key]
        for key in (
            "command",
            "exit_code",
            "stdout_bytes",
            "stdout_sha256",
            "stderr_bytes",
            "stderr_sha256",
        )
    }
    if parsed is not None:
        value["parsed_result"] = parsed
    return value


def parse_json_result(result: dict) -> dict:
    require(
        result["exit_code"] == 0,
        f"command failed: {result['command']}\n{result['stdout'][-2000:]}\n{result['stderr'][-2000:]}",
    )
    return json.loads(result["stdout"])


def verify_preseal() -> None:
    for relative, expected in PRESEAL_PINS.items():
        path = ROOT / relative
        require(path.is_file(), f"preseal file missing: {relative}")
        actual = (path.stat().st_size, sha256(path))
        require(actual == expected, f"preseal pin mismatch: {relative}: {actual}")
    for relative in (AUDIT_REL, RECOVERY_REL, TRANSCRIPT_REL):
        require(not (ROOT / relative).exists(), f"checkpoint output already exists: {relative}")


def verify_artifacts() -> dict:
    evidence: dict[str, object] = {"pdfs": {}, "renders": {}}
    pdfinfo = shutil.which("pdfinfo")
    pdffonts = shutil.which("pdffonts")
    pdftotext = shutil.which("pdftotext")
    require(pdfinfo is not None and pdffonts is not None and pdftotext is not None, "Poppler text/font tools are required")
    for name, pin in PDF_PINS.items():
        pdf = ROOT / pin["path"]
        log = ROOT / pin["log_path"]
        require((pdf.stat().st_size, sha256(pdf)) == (pin["bytes"], pin["sha256"]), f"PDF pin mismatch: {name}")
        require((log.stat().st_size, sha256(log)) == (pin["log_bytes"], pin["log_sha256"]), f"log pin mismatch: {name}")
        log_text = log.read_text(encoding="utf-8", errors="replace")
        diagnostics = {
            "latex_warnings": len(re.findall(r"LaTeX Warning", log_text, re.IGNORECASE)),
            "package_warnings": len(re.findall(r"Package .* Warning", log_text, re.IGNORECASE)),
            "undefined": len(re.findall(r"undefined references|Citation .* undefined|Reference .* undefined", log_text, re.IGNORECASE)),
            "overfull": len(re.findall(r"Overfull \\hbox|Overfull \\vbox", log_text, re.IGNORECASE)),
            "underfull": len(re.findall(r"Underfull \\hbox|Underfull \\vbox", log_text, re.IGNORECASE)),
            "fatal": len(re.findall(r"Fatal error|Emergency stop|! LaTeX Error", log_text, re.IGNORECASE)),
        }
        require(
            diagnostics
            == {
                "latex_warnings": 0,
                "package_warnings": 0,
                "undefined": 0,
                "overfull": 0,
                "underfull": pin["underfull"],
                "fatal": 0,
            },
            f"unexpected build diagnostics: {name}: {diagnostics}",
        )
        info = subprocess.run(
            [pdfinfo, str(pdf)],
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            check=False,
        )
        fonts = subprocess.run(
            [pdffonts, str(pdf)],
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            check=False,
        )
        text = subprocess.run(
            [pdftotext, "-enc", "UTF-8", str(pdf), "-"],
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            check=False,
        )
        require(info.returncode == fonts.returncode == text.returncode == 0, f"PDF static tool failed: {name}")
        page_match = re.search(r"^Pages:\s+(\d+)$", info.stdout, re.MULTILINE)
        require(page_match is not None and int(page_match.group(1)) == pin["pages"], f"page mismatch: {name}")
        font_rows = [line for line in fonts.stdout.splitlines()[2:] if line.strip() and not set(line.strip()) <= {"-"}]
        require(len(font_rows) == pin["font_rows"], f"font row mismatch: {name}: {len(font_rows)}")
        require(
            all(re.search(r"\syes\s+yes\s+yes\s+\d+\s+\d+\s*$", line) for line in font_rows),
            f"unembedded, unsubsettled, or non-Unicode font: {name}",
        )
        forbidden_patterns = [
            r"\?\?", r"codex://", r"file://", r"C:\\Users", r"\bTODO\b", r"\bTBD\b",
            r"\bplaceholder\b", r"\bopen obligation\b", r"\bproof obligation\b",
            r"\bconditional theorem\b", "\ufffd", r"operatorname", r"qquad", r"\\begin\{", r"\\cite\{",
        ]
        text_hits = {pattern: len(re.findall(pattern, text.stdout, re.IGNORECASE)) for pattern in forbidden_patterns}
        require(not any(text_hits.values()), f"forbidden extracted text: {name}: {text_hits}")
        evidence["pdfs"][name] = {**pin, "diagnostics": diagnostics, "text_hits": text_hits}
    for name, pin in RENDER_PINS.items():
        actual = aggregate_hash(ROOT / pin["path"])
        expected = (pin["files"], pin["bytes"], pin["sha256"])
        require(actual == expected, f"render aggregate mismatch: {name}: {actual}")
        evidence["renders"][name] = pin
    evidence["visual_review"] = {
        "root_contact_sheets_inspected": list(range(1, 16)),
        "root_all_pages_covered": 176,
        "root_new_chapter_pages_inspected_at_original_detail": list(range(160, 166)),
        "companion_contact_sheets_inspected": [1, 2, 3],
        "companion_all_pages_covered": 42,
        "companion_new_chapter_pages_inspected_at_original_detail": list(range(33, 41)),
        "defects": [],
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
    for relative, expected_status in (
        ("scripts/validate_state.py", "pass"),
        ("scripts/validate_chatnotes_intake.py", "pass"),
    ):
        result = run(relative)
        parsed = parse_json_result(result)
        require(parsed.get("status") == expected_status and parsed.get("failure_count") == 0, f"validator failed: {relative}")
        transcript["normal"].append(compact(result, parsed=parsed))
    root_results = []
    for relative in ROOT_CERTIFICATES:
        result = run(relative)
        require(result["exit_code"] == 0, f"certificate failed: {relative}\n{result['stderr'][-2000:]}")
        root_results.append(compact(result))
    transcript["root_certificate_suite"] = {
        "count": len(root_results),
        "all_passed": True,
        "results": root_results,
    }
    portable_results = {}
    for relative in PORTABLE_CERTIFICATES:
        result = run(relative)
        parsed = parse_json_result(result)
        require(parsed.get("status") == "PASS", f"portable certificate failed: {relative}")
        portable_results[relative] = compact(result, parsed=parsed)
    transcript["portable_certificates"] = portable_results
    groupoid = portable_results["research_companion/certificates/groupoid_motivic_interface_checks.py"]["parsed_result"]
    expected_metrics = {
        "alternative_representation_checks": 14378,
        "cayley_checks": 870,
        "character_product_checks": 192,
        "groupoid_elements": 9108,
        "groupoid_product_checks": 6000,
        "groupoid_representatives": 23486,
        "metrics_sha256": "89791d5517538fcd6adc111c67dc40aa03442a1b43960fe65a8f3b7c896f749c",
        "motive_square_checks": 1344,
        "path_composition_checks": 5600,
        "path_embedding_checks": 1120,
        "prefix_endomorphism_obstruction_checks": 1,
        "torus_character_checks": 192,
        "xi_functor_checks": 6000,
        "xi_injective_images": 9108,
        "xi_representation_checks": 23486,
        "z3_inverse_checks": 6534,
    }
    require(groupoid.get("checks") == expected_metrics, "groupoid/motivic metrics changed")
    require(
        groupoid.get("raw_l2_counterexample", {}).get("conclusion")
        == "V_1 delta_1=0, hence V_1^* V_1 is not the identity",
        "exact raw l2 counterexample changed",
    )
    package_result = run("research_companion/validate_package.py")
    package = parse_json_result(package_result)
    require(package.get("status") == "PASS", "companion package validation failed")
    transcript["package_validation"] = compact(package_result, parsed=package)
    optimized_targets = [
        "certificates/chatnotes_symbolic_completion_checks.py",
        "research_companion/certificates/finite_actions_checks.py",
        "research_companion/certificates/arctangent_relation_lattice_checks.py",
        "research_companion/certificates/groupoid_motivic_interface_checks.py",
        "research_companion/validate_package.py",
    ]
    for relative in optimized_targets:
        result = run(relative, optimized=True)
        require(result["exit_code"] != 0 and "refuses optimized Python" in result["combined"], f"optimized run did not fail closed: {relative}")
        transcript["optimized_fail_closed"].append(compact(result))
    transcript["finished_utc"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    return transcript


def make_recovery(stamp: str, transcript: dict, validator: dict) -> str:
    return f"""# ACT43 fresh-context recovery

Timestamp: {stamp}

Status: PASS for the bounded checkpoint `{RECEIPT_ID}`. The durable corpus goal remains active.

## Recovery basis

Recovery used only the external directive, machine-readable state, raw-source and source-record pins, the two TeX trees, executable certificates, and final artifacts. Compaction text was not used as evidence.

The recovered state is exact:

- 49 content-read literature source records;
- 181 typed claim records and 62 typed morphism records;
- 17 Chatnotes intake records, two natural programme records, and four topic routes;
- direct-locator coverage of all physical lines 1--17437 of the pinned `Z_n Symmetries` export;
- 25 current Python certificate artifacts, including the groupoid/motivic checker;
- a 176-page critical reconstruction and a separate 42-page research companion;
- a hard Lean/Lake ceiling of 2,147,483,648 bytes per session/process tree, one-worker maximum, and a current no-launch hold.

The next mathematical intake is the remaining full direct audit of `CHATINT-COL-000002`, the 3,021-line `ChatGPT-Implications of Affine Formula.md` export. Its prior agent intake and selected-window report are locator hints only; the raw file itself controls. Every consequential source dependency must first be routed through the completed canonical index.

## Executable recovery

Run `python {validator['path']}` from the project root. The validator checks complete ID sets and headers, `{RECEIPT_ID}`, the 2 GiB rule, artifact identities, PDF pages/fonts/text, render aggregates, coverage fields, the state and Chatnotes validators, the groupoid/motivic certificate, and the isolated package rebuild.

Validation transcript: `{transcript['path']}` ({transcript['bytes']} bytes; SHA-256 `{transcript['sha256']}`).
Recovery validator: `{validator['path']}` ({validator['bytes']} bytes; SHA-256 `{validator['sha256']}`).
"""


def make_audit(stamp: str, evidence: dict, transcript: dict, recovery: dict, validator: dict) -> str:
    groupoid = load_json(TRANSCRIPT_REL)["portable_certificates"]["research_companion/certificates/groupoid_motivic_interface_checks.py"]["parsed_result"]
    checks = groupoid["checks"]
    return f"""# ACT43 groupoid and motivic release audit

Timestamp: {stamp}

Status: PASS for checkpoint `{RECEIPT_ID}`. The durable Collatz corpus goal remains active; this record makes no global completion, publication, upload, or Collatz-endpoint claim.

## Mathematical scope sealed

The direct chronological audit of physical lines 11088--14011 closes the last unaudited interval of the pinned 17,437-line `Z_n Symmetries` export. Four primary literature records fix the exact external framework: Deaconu's self-covering groupoid hypotheses; Huber--Wuestholz 1-motives and Kummer periods; Huber--Mueller-Stach's contravariant Nori edges; and Barbieri-Viale--Kahn's derived and Cartier-dual 1-motive framework.

The separately proved extension constructs:

- the discrete arithmetic orbit groupoid, its exact integer and real cocycles, the faithful positive-odd path functor, its point-mass algebra embedding, and gauge/time actions on full and reduced completions;
- the clopen 3-adic branch homeomorphisms, their Hausdorff etale germ groupoid, and the injective cocycle-preserving arithmetic-to-germ functor;
- the explicit failures of the printed raw `l2(O)` isometry and of left prefixing as an algebra endomorphism;
- the unimodular isomorphism between arithmetic and degree torus coordinates, actual Kummer 1-motive squares, and their logarithmic periods;
- the Cayley isomorphism of marked pairs, the exact contravariant Nori edge, the multiplication map of Kummer pairs, and differential period additivity.

The extension does not assert amenability, equality of full and reduced groupoid completions, an unidentified crossed-product equality, equilibrium classification, a universal path-indexed Nori category, a motivic Galois action on the path algebra, or a Collatz endpoint.

## Hardened state

The state now contains 49 sources, 181 claims, 62 morphisms, 17 Chatnotes intake records, two programmes, four topic routes, and 43 receipts. The new records are `SRC-COL-000046`--`000049`, `CLM-COL-000174`--`000181`, `MOR-COL-000055`--`000062`, `CHATINT-COL-000017`, and `TOPIC-COL-GROUPOID-MOTIVIC-0004`. Consequences were propagated through both TeX trees, both programme records, bibliography/provenance, TODO, and package manifest before this seal.

## Executable mathematics

All 22 root certificate artifacts and all three portable certificate artifacts passed. The new checker reports {len(checks)} named check families, including {checks['groupoid_product_checks']} groupoid products, {checks['alternative_representation_checks']} alternative representatives, {checks['xi_functor_checks']} functor products, {checks['xi_representation_checks']} germ representations, {checks['z3_inverse_checks']} 3-adic inverse checks, {checks['motive_square_checks']} motive squares, and {checks['cayley_checks']} Cayley checks. Its metric digest is `{checks['metrics_sha256']}`. Five optimized-Python probes failed closed.

## Package and PDF validation

The companion package contains 11 manifested source files, 5 TeX files, 130 labels, 66 references, and 15 citation keys. Its normal validator and two isolated deterministic source-to-PDF rebuilds passed.

The accepted PDFs are:

- working corpus: 176 pages, 1,630,444 bytes, SHA-256 `c03e4000464940377b2bdef87e19d0d92e9c4ddba7a570424ac5b0c72fbbf15e`;
- research companion: 42 pages, 636,148 bytes, SHA-256 `5c734ac770501539c36f9fe782395b26483caa09e8ec15d8602ded23eeb65441`.

All 29 and 22 respective font rows are embedded, subset, and Unicode. Both build logs have zero LaTeX warnings, package warnings, undefined references/citations, overfull boxes, and fatal diagnostics; the retained six and two underfull boxes are nonactionable inherited paragraph spacing. Extracted text has zero unresolved markers, private paths/URIs, placeholders, retired heuristic terms, replacement characters, or raw TeX command leakage.

Fresh renders cover all 176 root pages at 160 dpi and all 42 companion pages at 200 dpi. All 18 contact sheets were inspected. Root pages 160--165 and companion pages 33--40 were additionally inspected at original detail; no clipping, overlap, broken glyph, black block, footer collision, or other visual defect was found.

The render aggregate hash updates SHA-256, in ordinal filename order, first with each UTF-8 filename and then with the raw file bytes, without a delimiter.

## Resource and recovery status

No Lean/Lake process was launched. A direct task-path process check found no task-owned Lean/Lake worker. The hard ceiling is exactly 2 GiB (2,147,483,648 bytes) per session/process tree, only one worker may run, and the current coordination hold remains active. No Git, upload, publication, cleanup, archive, or `AGENTS.md` write occurred.

Validation transcript: `{transcript['path']}` ({transcript['bytes']} bytes; SHA-256 `{transcript['sha256']}`).
Fresh-context record: `{recovery['path']}` ({recovery['bytes']} bytes; SHA-256 `{recovery['sha256']}`).
Recovery validator: `{validator['path']}` ({validator['bytes']} bytes; SHA-256 `{validator['sha256']}`).
"""


def update_todo() -> None:
    path = ROOT / "TODO.md"
    text = path.read_text(encoding="utf-8")
    marker = """  - [x] Run the portable exact Gaussian relation-lattice certificate on all
    795 columns `(k,A)` with `1<=k<=15` and `k<=A<=60`; verify rank 793 and
    nullity two over `F_3`, the two exact Gaussian products, the primitive
    saturation minor, the torsion-free integral lift, and the complete prefix-
    chain restriction without any coefficient cutoff.
"""
    addition = marker + """  - [x] Run the portable arithmetic-groupoid and motivic-interface
    certificate: verify representative independence, products, path and germ
    functoriality, exact 3-adic inverses, torus characters, 1-motive squares,
    Cayley and multiplication identities, and both explicit operator defects.
"""
    require(marker in text and addition not in text, "TODO certificate insertion point changed")
    text = text.replace(marker, addition, 1)
    marker = """  - [x] Seal the ACT42 symbolic/arctangent checkpoint: rebuild and validate the
    169-page working corpus and 34-page companion, inspect all rendered pages,
    verify embedded/subset Unicode fonts and zero actionable diagnostics, and
    pass external-state-only recovery.  This is a checkpoint, not global
    completion.
"""
    addition = marker + """  - [x] Seal the ACT43 groupoid/motivic checkpoint: validate the
    176-page working corpus and 42-page companion, inspect every rendered page
    plus all new theorem pages at original detail, verify 25 current
    certificates, and pass fresh-context recovery under the 2 GiB Lean rule.
"""
    require(marker in text and addition not in text, "TODO release insertion point changed")
    text = text.replace(marker, addition, 1)
    marker = """  - [x] Revalidate the expanded ACT42 companion as a nine-file independent
    Overleaf-compatible package: four TeX files, 91 labels, 50 references, 11
    citation keys, exact manifest inventory, two deterministic source-to-PDF
    rebuilds, all-page visual QA, and no upload or publication.
"""
    addition = marker + """  - [x] Revalidate the expanded ACT43 companion as an eleven-file
    independent Overleaf-compatible package: five TeX files, 130 labels, 66
    references, 15 citation keys, three portable certificates, two isolated
    deterministic rebuilds, all-page visual QA, and no upload or publication.
"""
    require(marker in text and addition not in text, "TODO package insertion point changed")
    text = text.replace(marker, addition, 1)
    path.write_text(text, encoding="utf-8")


def update_coverage(audit: dict, recovery: dict, transcript: dict) -> None:
    coverage = load_json("state/coverage.json")
    coverage["coverage_status"] = "active_after_ACT43_groupoid_motivic_checkpoint_full_direct_Zn_export_audit_complete_affine_export_direct_audit_next"
    layers = {layer["layer_id"]: layer for layer in coverage["layers"]}
    lit = layers["LIT"]
    lit["status"] = "foundational_spine_in_progress_49_content_read_source_documents_groupoid_one_motive_Nori_and_Cartier_dual_boundaries_crosswalked_remaining_literature_continues"
    lit["documents_read"] = 49
    lit["documents_admitted"] = 49
    chat = layers["CHAT"]
    chat["status"] = "pinned_Zn_export_all_17437_physical_lines_direct_locator_audited_second_3021_line_affine_export_has_agent_intake_and_selected_direct_windows_full_direct_recheck_next"
    chat["continuous_direct_ranges"] = ["CHATINT-COL-000001:1-17437"]
    chat["next_continuous_range"] = "CHATINT-COL-000002:1-3021_full_direct_raw_recheck"
    formal = layers["FORMAL"]
    formal["status"] = "25_distinct_current_Python_certificate_artifacts_rerun_PASS_groupoid_motivic_symbolic_finite_action_and_Gaussian_checks_hardened_optimized_runs_fail_closed"
    formal["artifacts_verified"] = 25
    artifact = "research_companion/certificates/groupoid_motivic_interface_checks.py"
    if artifact not in formal["artifact_inventory"]:
        formal["artifact_inventory"].append(artifact)
    formal["artifact_counting_rule"] = "distinct current .py files under certificates and research_companion/certificates that passed a normal run at ACT43"
    formal["groupoid_motivic_certificate_families"] = 16
    syn = layers["SYN"]
    syn.update(
        {
            "status": "ACT43_176_page_working_corpus_and_42_page_separately_authored_companion_built_package_validated_and_all_pages_visually_checked",
            "working_pdf_pages": 176,
            "working_pdf_bytes": 1_630_444,
            "working_pdf_sha256": PDF_PINS["working"]["sha256"],
            "research_companion_pdf_pages": 42,
            "research_companion_pdf_bytes": 636_148,
            "research_companion_pdf_sha256": PDF_PINS["companion"]["sha256"],
            "root_rendered_page_count": 176,
            "root_render_dpi": 160,
            "root_render_bytes": RENDER_PINS["root_pages"]["bytes"],
            "root_render_sha256": RENDER_PINS["root_pages"]["sha256"],
            "root_contact_sheet_count": 15,
            "root_contact_sheet_bytes": RENDER_PINS["root_contact_sheets"]["bytes"],
            "root_contact_sheet_sha256": RENDER_PINS["root_contact_sheets"]["sha256"],
            "current_pages_visually_checked": 218,
            "root_all_pages_contact_sheet_checked": 176,
            "root_pages_checked_at_original_detail": list(range(160, 166)),
            "independent_rendered_page_count": 42,
            "independent_render_bytes": RENDER_PINS["companion_pages"]["bytes"],
            "independent_render_sha256": RENDER_PINS["companion_pages"]["sha256"],
            "independent_contact_sheet_count": 3,
            "independent_contact_sheet_bytes": RENDER_PINS["companion_contact_sheets"]["bytes"],
            "independent_contact_sheet_sha256": RENDER_PINS["companion_contact_sheets"]["sha256"],
            "independent_current_pages_visually_checked": list(range(1, 43)),
            "independent_pages_checked_at_original_detail": list(range(33, 41)),
            "independent_render_dpi": 200,
            "checkpoint_visual_qa_passed": True,
            "visual_qa_complete": True,
            "final_build_directory": "tmp/pdfs/act43_groupoid_motivic_final_root_20260830_03",
            "companion_build_directory": "research_companion/tmp/pdfs/act43_groupoid_motivic_final_companion_20260830_04",
            "final_layout_sha256": PDF_PINS["working"]["sha256"],
            "companion_layout_sha256": PDF_PINS["companion"]["sha256"],
            "final_log_sha256": PDF_PINS["working"]["log_sha256"],
            "companion_log_sha256": PDF_PINS["companion"]["log_sha256"],
            "actionable_log_diagnostics": 0,
            "unresolved_placeholder_hits": 0,
            "literal_quad_leak_hits": 0,
            "embedded_subset_font_rows": 29,
            "companion_embedded_subset_font_rows": 22,
            "unembedded_font_rows": 0,
            "final_root_render_directory": RENDER_PINS["root_pages"]["path"],
            "final_independent_render_directory": RENDER_PINS["companion_pages"]["path"],
            "final_root_contact_sheet_directory": RENDER_PINS["root_contact_sheets"]["path"],
            "final_independent_contact_sheet_directory": RENDER_PINS["companion_contact_sheets"]["path"],
            "nonactionable_underfull_warnings": {"root": 6, "companion": 2},
            "groupoid_motivic_certificate": {
                "path": "research_companion/certificates/groupoid_motivic_interface_checks.py",
                "bytes": 17_495,
                "sha256": "ca460277a54e016a6ef84377cde5cc2e670f08c6cf3f57073f2a3c62d6400916",
                "status": "PASS_exact_groupoid_germ_torus_motive_and_Cayley_checks",
                "check_families": 16,
                "metrics_sha256": "89791d5517538fcd6adc111c67dc40aa03442a1b43960fe65a8f3b7c896f749c",
            },
        }
    )
    syn["fresh_render_policy"] = {
        "current_pdf_pages_freshly_rendered": 218,
        "root_render_dpi": 160,
        "companion_render_dpi": 200,
        "current_all_contact_sheets_inspected": 18,
        "all_pages_checked": 218,
        "original_detail_pages": {"root": list(range(160, 166)), "companion": list(range(33, 41))},
        "reason": "All 176 root and 42 companion pages were covered by contact-sheet inspection; every page of both new theorem chapters was additionally inspected at original detail. No visual defect was found.",
    }
    syn["package_validation"] = {
        "manifested_source_files": 11,
        "tex_files": 5,
        "labels": 130,
        "references": 66,
        "citations": 15,
        "finite_certificate_check_families": 30,
        "arctangent_certificate_check_families": 9,
        "groupoid_motivic_certificate_check_families": 16,
        "normal_run": "PASS",
        "optimized_python_run": "FAIL_CLOSED",
        "source_to_pdf_rebuild": "PASS_two_canonical_rebuilds_match_declared_output",
        "validation_transcript": transcript,
    }
    recovery_layer = layers["RECOVERY"]
    recovery_layer.update(
        {
            "status": "ACT43_groupoid_motivic_artifact_state_sealed_and_external_state_recovery_passed",
            "checkpoint_passed": True,
            "checkpoint_record": audit["path"],
            "latest_receipt": RECEIPT_ID,
            "passed": True,
            "act43_fresh_context_test": {
                "status": "PASS_external_state_only_recovery",
                **recovery,
                "checkpoint": RECEIPT_ID,
                "goal_status": "active",
                "completion_claimed": False,
                "working_pdf_pages": 176,
                "research_companion_pdf_pages": 42,
                "validator_failures": 0,
                "expected_route_warnings": 8,
                "ledger_maximum_rule": "derive from complete ID set plus header; never use physical JSONL tail",
            },
        }
    )
    write_json("state/coverage.json", coverage)


def update_project(audit: dict, recovery: dict, transcript: dict, stamp: str) -> None:
    project = load_json("state/project_state.json")
    project["current_checkpoint"] = {
        "receipt_id": RECEIPT_ID,
        **audit,
        "scope": "complete_direct_Zn_export_groupoid_germ_torus_Kummer_Cayley_and_Nori_interface_reconstruction_full_artifact_QA",
        "global_completion": False,
        "post_checkpoint_state_changed": False,
        "fresh_context_recovery_required_after_current_intake": False,
        "fresh_context_recovery": {**recovery, "status": "PASS_external_state_only_recovery"},
        "validation_transcript": transcript,
    }
    resource = project["resource_policy"]
    resource["lean_worker_private_working_set_limit_bytes"] = 2_147_483_648
    resource["maximum_overlapping_lean_builds"] = 1
    resource["required_resume_mode"] = "current_hold_no_launch; after_verified_release_single_bounded_worker_with_process_tree_watcher_killing_at_2_GiB"
    resource["last_enforcement_utc"] = stamp
    resource["last_enforcement_result"] = "direct_task_path_process_check_found_no_task_owned_Lean_or_Lake_worker; Noether_coordinator_notified_of_2_GiB_rule; current_hold_retained; no_Lean_or_Lake_started"
    resource["enforcement_events"].append(
        {
            "module": "all_task_owned_Lean_Lake",
            "action": "ACT43_preseal_direct_task_path_check_no_active_worker_2_GiB_cap_and_current_hold_reverified_coordinator_notified",
            "pids": [],
            "timestamp_utc": stamp,
            "memory_limit_bytes": 2_147_483_648,
        }
    )
    resource["serial_coordination_status"] = "no_task_owned_worker_current_hold_active_fresh_verified_release_required_before_any_future_formal_run"
    project["artifact_architecture"]["separately_authored_research_companion"] = "research_companion/main.tex (ACT43 independent 11-file package validated: arithmetic orbit groupoids, 3-adic germ functor, toric coordinates, Kummer motives, Cayley pairs, and exact Nori arrows; not uploaded)"
    project["next_action"] = "Complete a direct physical-line audit of CHATINT-COL-000002, the pinned 3021-line ChatGPT-Implications of Affine Formula.md export. Treat CHATINT-COL-000005 and CHATINT-COL-000006 only as locator hints, read the raw file itself, type every surviving definition, calculation, theorem, map, contradiction, and exact nonclaim separately, and route every consequential source dependency through the completed canonical index before proceeding. Keep Gemini and archived-task intake deferred, do not contact the quarantined zeta task, do not publish or upload, and keep Lean/Lake idle under the 2 GiB-per-session ceiling until a verified release."
    project["last_receipt_id"] = RECEIPT_ID
    project["updated_utc"] = stamp
    write_json("state/project_state.json", project)


def append_receipt(stamp: str, evidence: dict, audit: dict, recovery: dict, transcript: dict) -> None:
    groupoid = load_json(TRANSCRIPT_REL)["portable_certificates"]["research_companion/certificates/groupoid_motivic_interface_checks.py"]["parsed_result"]
    receipt = {
        "record_type": "action_receipt",
        "schema_version": "1.0",
        "receipt_id": RECEIPT_ID,
        "timestamp_utc": stamp,
        "action": "seal_ACT43_groupoid_motivic_interfaces_complete_direct_Zn_export_audit_expanded_independent_companion_full_visual_QA_2_GiB_resource_rule_and_fresh_context_recovery",
        "inputs": [
            "ACT-COL-000042",
            "raw/USR-0012.txt",
            "CHATINT-COL-000017",
            "SRC-COL-000046 through SRC-COL-000049",
            "CLM-COL-000174 through CLM-COL-000181",
            "MOR-COL-000055 through MOR-COL-000062",
            "PRG-COL-0001 and PRG-COL-0002",
            "TOPIC-COL-GROUPOID-MOTIVIC-0004",
        ],
        "outputs": [
            TRANSCRIPT_REL,
            AUDIT_REL,
            RECOVERY_REL,
            RECOVERY_VALIDATOR_REL,
            "state/project_state.json",
            "state/coverage.json",
            "TODO.md",
            PDF_PINS["working"]["path"],
            PDF_PINS["companion"]["path"],
        ],
        "result": "pass_bounded_checkpoint_goal_active_no_completion_claim",
        "measurements": {
            "mathematics": {
                "claims": [f"CLM-COL-{number:06d}" for number in range(174, 182)],
                "morphisms": [f"MOR-COL-{number:06d}" for number in range(55, 63)],
                "programmes": ["PRG-COL-0001", "PRG-COL-0002"],
                "chatnotes_intake": "CHATINT-COL-000017",
                "literature_sources": [f"SRC-COL-{number:06d}" for number in range(46, 50)],
                "direct_Zn_range_completed": "1-17437",
                "next_direct_source": "CHATINT-COL-000002:1-3021",
            },
            "certificates": {
                "distinct_current_python_artifacts_passed": 25,
                "root_suite_passed": 22,
                "portable_suite_passed": 3,
                "groupoid_motivic_check_families": len(groupoid["checks"]),
                "groupoid_motivic_metrics": groupoid["checks"],
                "raw_l2_counterexample": groupoid["raw_l2_counterexample"]["conclusion"],
                "optimized_runs": "FAIL_CLOSED",
            },
            "package": {
                "manifested_source_files": 11,
                "tex_files": 5,
                "labels": 130,
                "references": 66,
                "citations": 15,
                "source_to_pdf": "PASS_two_canonical_rebuilds_match_declared_output",
                "manifest": record("research_companion/MANIFEST.json"),
                "validation_transcript": transcript,
            },
            "pdfs": evidence["pdfs"],
            "renders": evidence["renders"],
            "visual_review": evidence["visual_review"],
            "checkpoint": audit,
            "fresh_context": {**recovery, "status": "PASS_external_state_only_recovery"},
            "resource_policy": {
                "Lean_or_Lake_started": 0,
                "limit_bytes_per_session_or_process_tree": 2_147_483_648,
                "maximum_overlapping_builds": 1,
                "current_hold_retained": True,
                "task_owned_workers_at_preseal": 0,
                "Git_commands_started": 0,
                "uploads_or_public_mutations": 0,
                "cleanup_or_archive_actions": 0,
                "AGENTS_md_writes": 0,
            },
        },
        "notes": [
            "ACT43 seals a corpus checkpoint only; the global literature-first Collatz goal remains active.",
            "The companion package is Overleaf-compatible and was not uploaded.",
            "Ledger maxima were derived from complete ID sets and headers, not physical JSONL tails.",
            "The pinned Z_n Symmetries export now has direct-locator coverage for all 17,437 physical lines; the second pinned affine export is next.",
        ],
    }
    with (ROOT / "state/action_receipts.jsonl").open("a", encoding="utf-8", newline="") as handle:
        handle.write(json.dumps(receipt, ensure_ascii=False, separators=(",", ":")) + "\n")


def main() -> None:
    verify_preseal()
    stamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    evidence = verify_artifacts()
    transcript = run_validations(stamp)
    transcript["artifact_validation"] = evidence
    transcript["visual_review_authority"] = "direct page-image inspection with independently rechecked chapter-page reports"
    write_json(TRANSCRIPT_REL, transcript)
    transcript_record = record(TRANSCRIPT_REL)
    validator_record = record(RECOVERY_VALIDATOR_REL)
    (ROOT / RECOVERY_REL).write_text(
        make_recovery(stamp, transcript_record, validator_record), encoding="utf-8"
    )
    recovery_record = record(RECOVERY_REL)
    (ROOT / AUDIT_REL).write_text(
        make_audit(stamp, evidence, transcript_record, recovery_record, validator_record),
        encoding="utf-8",
    )
    audit_record = record(AUDIT_REL)
    update_todo()
    update_coverage(audit_record, recovery_record, transcript_record)
    update_project(audit_record, recovery_record, transcript_record, stamp)
    append_receipt(stamp, evidence, audit_record, recovery_record, transcript_record)
    print(
        json.dumps(
            {
                "schema_version": "1.0",
                "status": "PASS",
                "receipt_id": RECEIPT_ID,
                "audit": audit_record,
                "recovery": recovery_record,
                "transcript": transcript_record,
                "next_action": load_json("state/project_state.json")["next_action"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def resume_verified_partial_seal() -> None:
    expected_partial = {
        "state/project_state.json": (19_955, "e3fcb8c9fd039a46f5088bb17c4c7f2af4f2a248dc9f689b81ae2fe631dc1f47"),
        "state/action_receipts.jsonl": (210_450, "97219936b6ff4266b7b375fec04aeeca159574a8f57b7a3de3fa214941105bba"),
        "state/coverage.json": (15_192, "3016af439f430f6ace81f846440828467220ae5e5c1dd525393523227245aa77"),
        "TODO.md": (31_693, "df1cefa7bf77da99cd14f07db7c1e495f15b28877a311cda1a72791d3c42c43a"),
        TRANSCRIPT_REL: (31_925, "d6d7890dfd3c93d7f00ccfa1dc07cccea4e39d2f3a4c67f93d93d9ad4c81a1bc"),
        RECOVERY_REL: (2_055, "b7c29b4a0d92dfcc6612b515063fed3a785c0168adbd87787bea7127cae44c78"),
        AUDIT_REL: (5_071, "d1f9e8bb8d7e8ac2775977c173b6c84fef24774527ee8562fb51ccfaa22da7e1"),
    }
    for relative, expected in expected_partial.items():
        path = ROOT / relative
        require(path.is_file(), f"partial-seal file missing: {relative}")
        actual = (path.stat().st_size, sha256(path))
        require(actual == expected, f"partial-seal pin mismatch: {relative}: {actual}")
    transcript_data = load_json(TRANSCRIPT_REL)
    require(transcript_data.get("checkpoint") == RECEIPT_ID, "partial transcript checkpoint mismatch")
    evidence = transcript_data.get("artifact_validation")
    require(isinstance(evidence, dict), "partial transcript lacks artifact validation")
    stamp = transcript_data["started_utc"]
    audit_record = record(AUDIT_REL)
    recovery_record = record(RECOVERY_REL)
    transcript_record = record(TRANSCRIPT_REL)
    update_project(audit_record, recovery_record, transcript_record, stamp)
    append_receipt(stamp, evidence, audit_record, recovery_record, transcript_record)
    print(
        json.dumps(
            {
                "schema_version": "1.0",
                "status": "PASS",
                "receipt_id": RECEIPT_ID,
                "resume_mode": "verified_partial_after_schema_key_correction",
                "audit": audit_record,
                "recovery": recovery_record,
                "transcript": transcript_record,
                "next_action": load_json("state/project_state.json")["next_action"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    if "--resume-verified-partial" in sys.argv:
        resume_verified_partial_seal()
    else:
        main()
