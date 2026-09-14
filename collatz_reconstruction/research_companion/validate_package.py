from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "MANIFEST.json"
ALLOWED_UNMANIFESTED = {"MANIFEST.json"}
LOCAL_SCRATCH_PREFIXES = {"tmp", "audit", "output"}
REPRODUCIBLE_BUILD_ENV = {
    "SOURCE_DATE_EPOCH": "1788026400",
    "FORCE_SOURCE_DATE": "1",
    "TZ": "UTC",
}
PDF_ID_PATTERN = re.compile(
    rb"/ID\s*\[<([0-9A-Fa-f]{32})>\s*<([0-9A-Fa-f]{32})>\]"
)
PDF_DATE_FIELDS = (b"CreationDate", b"ModDate")
CANONICAL_PDF_ID = b"0123456789ABCDEF0123456789ABCDEF"
CANONICAL_PDF_DATE = b"D:20260829180000Z"


if not __debug__:
    raise RuntimeError(
        "validate_package.py refuses optimized Python: fail-closed checks require __debug__"
    )


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def fail(message: str) -> None:
    raise AssertionError(message)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def canonical_pdf_bytes(data: bytes) -> bytes:
    """Erase producer-controlled PDF identity/date bytes for source comparison."""
    data, id_count = PDF_ID_PATTERN.subn(
        b"/ID [<" + CANONICAL_PDF_ID + b"> <" + CANONICAL_PDF_ID + b">]",
        data,
    )
    if id_count != 1:
        fail(f"expected exactly one PDF trailer ID, found {id_count}")
    for field in PDF_DATE_FIELDS:
        pattern = re.compile(rb"/" + field + rb"\s*\([^)]*\)")
        data, date_count = pattern.subn(
            b"/" + field + b" (" + CANONICAL_PDF_DATE + b")", data
        )
        if date_count != 1:
            fail(f"expected exactly one PDF {field.decode()} entry, found {date_count}")
    return data


def validate_manifest(data: dict) -> list[str]:
    if data.get("schema_version") != "1.0":
        fail("unsupported manifest schema")
    declared = data.get("files")
    if not isinstance(declared, dict) or not declared:
        fail("manifest files must be a nonempty object")

    output = data.get("output_pdf")
    if not isinstance(output, dict):
        fail("manifest must declare output_pdf")
    output_name = output.get("path")
    if not isinstance(output_name, str) or not output_name:
        fail("manifest output_pdf.path must be a nonempty string")
    output_relative = Path(output_name)
    if output_relative.is_absolute() or ".." in output_relative.parts:
        fail("output PDF path must be package-relative")
    output_name = output_relative.as_posix()
    if output_name != "output/pdf/collatz_research_companion.pdf":
        fail("unexpected output PDF path")

    actual = {
        rel(path)
        for path in ROOT.rglob("*")
        if path.is_file()
        and rel(path) not in ALLOWED_UNMANIFESTED
        and rel(path) != output_name
        and "__pycache__" not in path.parts
        and path.relative_to(ROOT).parts[0] not in LOCAL_SCRATCH_PREFIXES
    }
    expected = set(declared)
    if actual != expected:
        fail(
            "source inventory mismatch: "
            f"missing={sorted(expected - actual)} unexpected={sorted(actual - expected)}"
        )

    for name, record in declared.items():
        path = ROOT / Path(name)
        if not path.is_file():
            fail(f"missing declared file: {name}")
        if path.stat().st_size != record.get("bytes"):
            fail(f"byte-count mismatch: {name}")
        if digest(path) != record.get("sha256"):
            fail(f"SHA-256 mismatch: {name}")

    output_path = ROOT / output_name
    if not output_path.is_file():
        fail("declared output PDF is missing")
    if output_path.stat().st_size != output.get("bytes"):
        fail("output PDF byte-count mismatch")
    if digest(output_path) != output.get("sha256"):
        fail("output PDF SHA-256 mismatch")
    if not output_path.read_bytes().startswith(b"%PDF-"):
        fail("declared output is not a PDF")
    return sorted(expected)


def validate_private_path_absence(files: list[str]) -> None:
    textual = [
        name
        for name in files
        if Path(name).suffix in {".tex", ".md", ".py", ".json"}
        and name != "validate_package.py"
    ]
    drive_candidate = re.compile(
        r"(?i)(?<![A-Za-z0-9_])([A-Za-z]):([\\/])([^\s{}]*)"
    )
    unc_path = re.compile(
        r"\\\\[A-Za-z0-9][A-Za-z0-9._-]+[\\/][A-Za-z0-9][^\s{}]*"
    )
    unix_private = re.compile(r"(?i)(?:/users/|/home/|/root/|/tmp/|/mnt/)")
    forbidden_route_names = (("B" + "CM").lower(), ("ade" + "lic").lower())

    def contains_windows_absolute_path(text: str) -> bool:
        """Reject concrete drive paths without mistaking TeX maps for paths.

        TeX routinely contains type declarations such as ``E_w:\\mathbb Z``
        and set builders such as ``O:\\nu_2(3n+1)=a``.  A backslash-style
        candidate is accepted as a filesystem path only when it has a second
        nonempty component, begins at a standard private/system root, or names
        a one-component file with an extension.  Forward-slash drive paths are
        unambiguous in the package's TeX and are rejected directly.
        """

        standard_roots = {
            "users",
            "documents",
            "program",
            "program files",
            "program files (x86)",
            "windows",
            "temp",
            "tmp",
        }
        for match in drive_candidate.finditer(text):
            separator = match.group(2)
            tail = match.group(3)
            if separator == "/":
                return True
            components = [part for part in re.split(r"[\\/]", tail) if part]
            if len(components) >= 2:
                return True
            if components:
                first = components[0]
                if first.lower() in standard_roots:
                    return True
                if re.search(r"\.[A-Za-z0-9]{1,16}$", first):
                    return True
        return False

    detector_cases = {
        r"C:\Users\name\paper.tex": True,
        r"D:\work\paper.tex": True,
        r"C:\secret.txt": True,
        "C:/Users/name/paper.tex": True,
        r"E_w:\mathbb Z": False,
        r"O:\nu_2(3n+1)=a": False,
    }
    for sample, expected in detector_cases.items():
        if contains_windows_absolute_path(sample) is not expected:
            fail(f"Windows-path detector self-test failed for {sample!r}")
    unc_detector_cases = {
        r"\\server\share\paper.tex": True,
        r"\\host/share/paper.tex": True,
        r"\\x/2,&x\text{ even}": False,
    }
    for sample, expected in unc_detector_cases.items():
        if bool(unc_path.search(sample)) is not expected:
            fail(f"UNC-path detector self-test failed for {sample!r}")

    for name in textual:
        text = read_text(ROOT / name)
        if (
            contains_windows_absolute_path(text)
            or unc_path.search(text)
            or unix_private.search(text)
        ):
            fail(f"absolute or private machine path in {name}")
        if "codex://" in text.lower() or "file://" in text.lower():
            fail(f"nonportable URI in {name}")
        if name.endswith((".tex", ".md")):
            lowered = text.lower()
            if any(token in lowered for token in forbidden_route_names):
                fail(f"rejected unrelated route appears in public source: {name}")


def resolve_tex_input(owner: Path, target: str) -> Path:
    raw = Path(target)
    if raw.is_absolute() or ".." in raw.parts:
        fail(f"external TeX input in {rel(owner)}: {target}")
    candidate = owner.parent / raw
    if candidate.suffix == "":
        candidate = candidate.with_suffix(".tex")
    resolved = candidate.resolve()
    try:
        resolved.relative_to(ROOT)
    except ValueError:
        fail(f"TeX input escapes package root in {rel(owner)}: {target}")
    if not resolved.is_file():
        fail(f"missing TeX input in {rel(owner)}: {target}")
    return resolved


def validate_tex_closure(files: list[str], manifest: dict) -> dict[str, int]:
    tex_files = [ROOT / name for name in files if name.endswith(".tex")]
    roots = [path for path in tex_files if path.name == "main.tex"]
    if roots != [ROOT / "main.tex"]:
        fail("package must contain exactly one root main.tex")

    all_text = "\n".join(read_text(path) for path in tex_files)
    for owner in tex_files:
        text = read_text(owner)
        for target in re.findall(r"\\(?:input|include)\{([^}]+)\}", text):
            included = resolve_tex_input(owner, target)
            if rel(included) not in files:
                fail(f"unmanifested TeX input: {rel(included)}")

    labels = set(re.findall(r"\\label\{([^}]+)\}", all_text))
    references = set(
        re.findall(r"\\(?:ref|eqref|autoref|pageref)\{([^}]+)\}", all_text)
    )
    missing_labels = references - labels
    if missing_labels:
        fail(f"unresolved TeX labels: {sorted(missing_labels)}")

    bibitems = set(re.findall(r"\\bibitem\{([^}]+)\}", all_text))
    citations: set[str] = set()
    for group in re.findall(r"\\cite(?:\[[^]]*\])?\{([^}]+)\}", all_text):
        citations.update(key.strip() for key in group.split(",") if key.strip())
    missing_citations = citations - bibitems
    if missing_citations:
        fail(f"unresolved citation keys: {sorted(missing_citations)}")

    declared_ids = set(manifest.get("resolved_ids", []))
    used_ids = set(re.findall(r"\b(?:CLM|MOR|SRC|GAP|PRG)-[A-Z0-9-]+\b", all_text))
    if used_ids - declared_ids:
        fail(f"unresolved stable IDs: {sorted(used_ids - declared_ids)}")

    for target in re.findall(r"\\path\{([^}]+)\}", all_text):
        candidate = ROOT / Path(target)
        if not candidate.is_file() or rel(candidate) not in files:
            fail(f"missing or unmanifested path target: {target}")

    if "Live edition" in all_text or "Working critical reconstruction" in all_text:
        fail("critical-reader authorship leaked into research companion")
    return {
        "tex_files": len(tex_files),
        "labels": len(labels),
        "references": len(references),
        "citations": len(citations),
    }


def run_certificate(filename: str) -> dict:
    process = subprocess.run(
        [sys.executable, str(ROOT / "certificates" / filename)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=180,
    )
    result = json.loads(process.stdout)
    status = str(result.get("status", "")).upper()
    if not status and filename == "affine_packet_residue_checks.py":
        checks = result.get("checks")
        if (
            result.get("certificate")
            == "exact affine-packet and modular-residue checks"
            and isinstance(checks, dict)
            and checks
            and all(value == "PASS" for value in checks.values())
        ):
            status = "PASS"
    if status != "PASS":
        fail(f"portable certificate did not pass: {filename}")
    return result


def run_certificates() -> dict[str, dict]:
    finite = run_certificate("finite_actions_checks.py")
    arctangent = run_certificate("arctangent_relation_lattice_checks.py")
    groupoid_motivic = run_certificate("groupoid_motivic_interface_checks.py")
    affine_packet = run_certificate("affine_packet_residue_checks.py")
    affine_crt = run_certificate("affine_crt_synchronization_checks.py")
    affine_series = run_certificate("affine_packet_series_checks.py")
    affine_signed_necklace = run_certificate("affine_signed_necklace_checks.py")
    expected_arctangent_metrics = {
        "columns": 795,
        "candidate_primes": 1008,
        "good_rows": 794,
        "bad_rows": 214,
        "rank_F3": 793,
        "nullity_F3": 2,
        "rank_before_38821": 792,
        "first_full_rank_prime": 38821,
        "character_matrix_trits_sha256":
            "15071896fda6f1d4e75b42c91db02a2155777baa4a7eb7bdb79c6959959e1ab6",
    }
    metrics = arctangent.get("metrics", {})
    for key, expected in expected_arctangent_metrics.items():
        if metrics.get(key) != expected:
            fail(
                "arctangent certificate metric mismatch: "
                f"{key}={metrics.get(key)!r}, expected {expected!r}"
            )
    checks = arctangent.get("checks", {})
    if checks.get("character_entry_checks") != 631230:
        fail("arctangent certificate did not check all 631,230 character entries")
    if arctangent.get("integer_lattice_lift", {}).get("conclusion") != (
        "L=Z R1 direct-sum Z R2 on the certified grid"
    ):
        fail("arctangent certificate did not report the exact integer lattice lift")
    expected_groupoid_checks = {
        "alternative_representation_checks": 14378,
        "cayley_checks": 870,
        "character_product_checks": 192,
        "groupoid_elements": 9108,
        "groupoid_product_checks": 6000,
        "groupoid_representatives": 23486,
        "metrics_sha256":
            "89791d5517538fcd6adc111c67dc40aa03442a1b43960fe65a8f3b7c896f749c",
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
    groupoid_checks = groupoid_motivic.get("checks", {})
    for key, expected in expected_groupoid_checks.items():
        if groupoid_checks.get(key) != expected:
            fail(
                "groupoid/motivic certificate metric mismatch: "
                f"{key}={groupoid_checks.get(key)!r}, expected {expected!r}"
            )
    if groupoid_motivic.get("raw_l2_counterexample", {}).get("conclusion") != (
        "V_1 delta_1=0, hence V_1^* V_1 is not the identity"
    ):
        fail("groupoid/motivic certificate lost the exact l2 counterexample")
    if affine_packet.get("metrics_sha256") != (
        "50106a4261308568466d6f4b4d9e16a09921a5efde5ac258c60cbf66577c97ba"
    ):
        fail("affine packet certificate metric digest mismatch")
    packet_metrics = affine_packet.get("metrics", {})
    if packet_metrics.get("total_words_scanned_by_each_method") != 4_734_620:
        fail("affine packet certificate scan count mismatch")
    if packet_metrics.get("total_integral_words") != 0:
        fail("affine packet certificate lost the exact finite exclusion")
    if affine_crt.get("word_count") != 5005 or affine_crt.get("joint_origin_count") != 0:
        fail("affine CRT certificate lost the complete (10,16) count")
    if affine_crt.get("joint_dense_table_sha256_compact_json") != (
        "c96f9a23ccf99710306d4188d737826fc3d03818e0fd80680fa3d9bd3ce626d3"
    ):
        fail("affine CRT joint table digest mismatch")
    if affine_series.get("words") != 4095:
        fail("affine series certificate word count mismatch")
    if affine_series.get("tail_affine_equalities") != 16_380:
        fail("affine series tail-equality count mismatch")
    if affine_series.get("source_tail_wrong_value") != "1/2":
        fail("affine series source-error witness mismatch")
    if affine_series.get("Lean_launched") is not False:
        fail("affine series certificate unexpectedly reports a Lean launch")
    if affine_signed_necklace.get("metrics_sha256") != (
        "e5b5e44e3737c67631a79231b0b333ceebb7166a387d38d2028c4ca27836cb6b"
    ):
        fail("signed necklace certificate metric digest mismatch")
    necklace_metrics = affine_signed_necklace.get("metrics", {})
    expected_necklace_metrics = {
        "parameter_pairs": 100,
        "composition_words": 39_202,
        "primitive_composition_words": 39_022,
        "primitive_orbits": 6_136,
        "positive_primitive_points": 38_097,
        "negative_primitive_points": 925,
        "coprime_parameter_pairs": 62,
        "unrestricted_moreau_sums": 7,
    }
    for key, expected in expected_necklace_metrics.items():
        if necklace_metrics.get(key) != expected:
            fail(
                "signed necklace certificate metric mismatch: "
                f"{key}={necklace_metrics.get(key)!r}, expected {expected!r}"
            )
    if affine_signed_necklace.get("Lean_launched") is not False:
        fail("signed necklace certificate unexpectedly reports a Lean launch")
    return {
        "finite_actions": finite,
        "arctangent_relations": arctangent,
        "groupoid_motivic_interfaces": groupoid_motivic,
        "affine_packet_residues": affine_packet,
        "affine_CRT_synchronization": affine_crt,
        "affine_packet_series": affine_series,
        "affine_signed_necklaces": affine_signed_necklace,
    }


def _build_pdf_once(build_root: Path) -> bytes:
    latexmk = shutil.which("latexmk")
    if latexmk is None:
        fail("latexmk is required for the deterministic source-to-PDF check")
    output_dir = build_root / "output"
    auxiliary_dir = build_root / "auxiliary"
    output_dir.mkdir()
    auxiliary_dir.mkdir()
    environment = os.environ.copy()
    environment.update(REPRODUCIBLE_BUILD_ENV)
    process = subprocess.run(
        [
            latexmk,
            "-pdf",
            "-interaction=nonstopmode",
            "-halt-on-error",
            f"-outdir={output_dir}",
            f"-auxdir={auxiliary_dir}",
            "main.tex",
        ],
        cwd=ROOT,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )
    if process.returncode != 0:
        diagnostics = (process.stdout + "\n" + process.stderr).strip()
        fail(
            "deterministic LaTeX rebuild failed "
            f"(exit {process.returncode}): {diagnostics[-4000:]}"
        )
    rebuilt = output_dir / "main.pdf"
    if not rebuilt.is_file():
        fail("deterministic LaTeX rebuild produced no main.pdf")
    return rebuilt.read_bytes()


def validate_source_to_pdf(output: dict) -> None:
    """Rebuild twice in isolated directories and compare exact PDF bytes."""
    with tempfile.TemporaryDirectory(prefix="collatz-companion-verify-") as first:
        with tempfile.TemporaryDirectory(prefix="collatz-companion-verify-") as second:
            first_bytes = _build_pdf_once(Path(first))
            second_bytes = _build_pdf_once(Path(second))
    first_canonical = canonical_pdf_bytes(first_bytes)
    second_canonical = canonical_pdf_bytes(second_bytes)
    if first_canonical != second_canonical:
        fail("reproducible LaTeX rebuilds are not byte-identical")
    declared_path = ROOT / output["path"]
    declared_canonical = canonical_pdf_bytes(declared_path.read_bytes())
    if first_canonical != declared_canonical:
        fail("canonical source rebuild does not match the declared output PDF")
    declared_size = len(declared_canonical)
    declared_sha256 = hashlib.sha256(declared_canonical).hexdigest()
    rebuilt_sha256 = hashlib.sha256(first_canonical).hexdigest()
    if len(first_canonical) != declared_size:
        fail(
            "canonical source-to-PDF byte-count mismatch: "
            f"rebuilt={len(first_canonical)} declared={declared_size}"
        )
    if rebuilt_sha256 != declared_sha256:
        fail(
            "canonical source-to-PDF SHA-256 mismatch: "
            f"rebuilt={rebuilt_sha256} declared={declared_sha256}"
        )


def run() -> dict:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    files = validate_manifest(manifest)
    validate_private_path_absence(files)
    tex_metrics = validate_tex_closure(files, manifest)
    certificates = run_certificates()
    validate_source_to_pdf(manifest["output_pdf"])
    return {
        "schema_version": "1.0",
        "status": "PASS",
        "manifested_source_files": len(files),
        "tex": tex_metrics,
        "finite_certificate_check_families": len(
            certificates["finite_actions"]["checks"]
        ),
        "arctangent_certificate_check_families": len(
            certificates["arctangent_relations"]["checks"]
        ),
        "arctangent_certificate_metrics":
            certificates["arctangent_relations"]["metrics"],
        "groupoid_motivic_certificate_check_families": len(
            certificates["groupoid_motivic_interfaces"]["checks"]
        ),
        "groupoid_motivic_certificate_metrics":
            certificates["groupoid_motivic_interfaces"]["checks"],
        "affine_packet_certificate_check_families": len(
            certificates["affine_packet_residues"]["checks"]
        ),
        "affine_packet_certificate_metrics":
            certificates["affine_packet_residues"]["metrics"],
        "affine_CRT_certificate_checks":
            certificates["affine_CRT_synchronization"]["checks"],
        "affine_series_certificate_metrics": {
            key: certificates["affine_packet_series"][key]
            for key in (
                "words",
                "packet_coefficients",
                "tail_affine_equalities",
                "rational_recurrence_checks",
            )
        },
        "affine_signed_necklace_certificate_metrics":
            certificates["affine_signed_necklaces"]["metrics"],
        "output_pdf": manifest["output_pdf"],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
