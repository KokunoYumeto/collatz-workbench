from __future__ import annotations

import argparse
from collections import Counter, OrderedDict, defaultdict
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tempfile
from typing import Any, Iterable
import zipfile

from jsonschema import Draft202012Validator


MANIFEST_NAME = "MANIFEST.sha256"
EXPECTED_ZIP_ROOT = "maxwell_siegel_critical_expository_edition_source"
EXPECTED_SOURCE_FREEZE_ID = "MS-CE-20260824-A"
EXPECTED_CLAIM_LEDGER_SHA256 = "e9ba4255f50c99b1763c136d6307b27ee554146eccfa283e3bd711e5577a2b8c"
EXPECTED_DOCUMENT_INDEX_SHA256 = "98a9aafe9e05f35055922de2124f141276d63a0ed6a5cc48c1db6f3972f226a9"
EXPECTED_CLAIM_SCHEMA_SHA256 = "694062452cec1e603cc2cd89cb3d926d5e0c4c3906f6b2fd9d1c2dc0e6c33e55"
EXPECTED_DOCUMENT_SCHEMA_SHA256 = "b8e3c3bc0b029e93facf1356c376be6aad025042ea82f19447c24aecf05af696"

EXPECTED_STATUS_COUNTS = OrderedDict(
    (
        ("verified_as_stated", 24),
        ("verified_corrected", 127),
        ("prior_art_overlap", 7),
        ("conditional", 4),
        ("heuristic", 1),
        ("contradicted", 17),
        ("unresolved", 12),
    )
)

EXPECTED_ATTRIBUTION_COUNTS = {
    "siegel": 91,
    "prior_literature": 17,
    "new_synthesis": 84,
    "user_note": 0,
}

EXPECTED_NONPROMOTED_CLAIMS = OrderedDict(
    (
        (
            "contradicted",
            [
                "CLM-0003",
                "CLM-0060",
                "CLM-0076",
                "CLM-0090",
                "CLM-0109",
                "CLM-0149",
                "CLM-0150",
                "CLM-0170",
                "CLM-0171",
                "CLM-0172",
                "CLM-0178",
                "CLM-0179",
                "CLM-0180",
                "CLM-0181",
                "CLM-0187",
                "CLM-0188",
                "CLM-0189",
            ],
        ),
        ("conditional", ["CLM-0092", "CLM-0169", "CLM-0182", "CLM-0184"]),
        ("heuristic", ["CLM-0093"]),
        (
            "unresolved",
            [
                "CLM-0091",
                "CLM-0108",
                "CLM-0135",
                "CLM-0137",
                "CLM-0138",
                "CLM-0158",
                "CLM-0173",
                "CLM-0174",
                "CLM-0183",
                "CLM-0185",
                "CLM-0186",
                "CLM-0191",
            ],
        ),
    )
)

EXPECTED_DOCUMENT_IDS = (
    "DOC-0003",
    "DOC-0008",
    "DOC-0010",
    "DOC-0012",
    "DOC-0014",
    "DOC-0015",
    "DOC-0016",
    "DOC-0017",
    "DOC-0020",
    "DOC-0024",
    "DOC-0053",
    "DOC-0085",
    "DOC-0086",
    "DOC-0087",
    "DOC-0088",
    "DOC-0089",
)

# SHA-256 of canonical JSON for each record with cited_locators removed.  The
# locators themselves are independently and exactly reconstructed from the
# claim ledger below; this pins the remaining public bibliographic identity.
EXPECTED_DOCUMENT_IDENTITY_SHA256 = {
    "DOC-0003": "c0a3970c61fdac9145538234753acbc62a5dba167ae50a7ee49613c4ee184bba",
    "DOC-0008": "31bdde3f8c7a976a68e87654c61993867b6d9cb74b552bb7b79c6c923592108e",
    "DOC-0010": "2352412c67d7b5d7f405a1cff4158eadfbdbdfa867e3f10ea509f772ee15cfbf",
    "DOC-0012": "b93c899782dfdd94c4d3893c3e4d4fc50b83a580d6ab996453cf022358186d7a",
    "DOC-0014": "9f48305352437d776d461d2d2f19e747d80b1fa85925083d765114269cdc5eee",
    "DOC-0015": "59e95a06354048d3f9ade7942cc972a6bf57639bfaeb58cb8e7e4f5119709939",
    "DOC-0016": "1e431829b7b6f04236a262fbb04164be6b13c577b1e204088ae2538f96a6e9ca",
    "DOC-0017": "f1a0fc480b4cdcf1d81747ebfac2df53f7c15bb37834ba6d1523d073975810af",
    "DOC-0020": "dd7120643fd6781fea7a00a66a35651ed385f526ad52c6f3ecf502b68efdd079",
    "DOC-0024": "0111f89b19b7efc91bbab17e4d5b4491b9a784e486417978a107d88dd32a85c6",
    "DOC-0053": "4e4a5251e0fe4e5dd16ee46e7fb42df100dad20963ac4bd1790aff487c2c5c80",
    "DOC-0085": "6ee46a71f5b852c41a732ac1ee81a3e53f4732747f86c8bde403e835dff1814b",
    "DOC-0086": "aeea95f8a523ae9e2bdf671e96d471370bd5da8014fbf23484f25cd123e3a1fd",
    "DOC-0087": "7381e8ecc3977136a2c74d03093370a8adc66bfb546ad92a843fd268a4e1f1bf",
    "DOC-0088": "e5fd2023647e433c92b690c67bf5a039a6c9b627e801f629f39aee32d9e933d5",
    "DOC-0089": "157fd1e454aace461dd94808994bed57cdcd3331633dc3d6f02722b53d363898",
}

EXPECTED_DOCUMENT_LOCATOR_VERSIONS = {
    "DOC-0003": ("arXiv:1909.09733v3",),
    "DOC-0008": ("arXiv:2007.15936v3",),
    "DOC-0010": ("arXiv:2111.07882v2",),
    "DOC-0012": ("arXiv:2111.07883v2",),
    "DOC-0014": ("arXiv:2208.11082v2",),
    "DOC-0015": ("arXiv:2307.00436v1",),
    "DOC-0016": ("arXiv:2412.02902v1",),
    "DOC-0017": ("arXiv:2507.13358v1",),
    "DOC-0020": ("arXiv:2601.17030v3",),
    "DOC-0024": ("Matthews author-form witness",),
    "DOC-0053": ("Laarhoven-de Weger 2012",),
    "DOC-0085": ("public author Web II exposition",),
    "DOC-0086": ("MathOverflow answer 333801",),
    "DOC-0087": ("B\u00f6hm-Sontacchi 1978",),
    "DOC-0088": ("Bernstein-Lagarias 1996",),
    "DOC-0089": ("Kohl 2008",),
}

EXPECTED_TEX_FILES = (
    "critical_expository_edition/main.tex",
    "critical_expository_edition/chapters/00_editorial_method.tex",
    "critical_expository_edition/chapters/01_canonical_corpus.tex",
    "critical_expository_edition/chapters/02_arithmetic_dynamics.tex",
    "critical_expository_edition/chapters/03_hydra_maps.tex",
    "critical_expository_edition/chapters/04_numen.tex",
    "critical_expository_edition/chapters/05_correspondence.tex",
    "critical_expository_edition/chapters/06_dreamcatchers.tex",
    "critical_expository_edition/chapters/07_contour_mellin.tex",
    "critical_expository_edition/chapters/08_pq_fourier.tex",
    "critical_expository_edition/chapters/09_rising_fseries.tex",
    "critical_expository_edition/chapters/10_synthesis.tex",
    "critical_expository_edition/chapters/11_source_register.tex",
)

EXPECTED_TEX_SHA256 = {
    "critical_expository_edition/main.tex": "815333a15e63a9b7f39ac8e277cd20007dd886457c9d7a4d35e8d5c1201ec71c",
    "critical_expository_edition/chapters/00_editorial_method.tex": "4ca84b090da44dcffa6ca5eed1269fe2a3481f5bd5b682bee273f7127fe26ec7",
    "critical_expository_edition/chapters/01_canonical_corpus.tex": "e49e95b0d839bcb5473a3323e0fed6510d8b27de399d11e04cbdbcf8d2c309c8",
    "critical_expository_edition/chapters/02_arithmetic_dynamics.tex": "24cb982e9e76ad734d692fc453fd420b157c7b1107760640c05b4d2cfb7e99bc",
    "critical_expository_edition/chapters/03_hydra_maps.tex": "eadfef26af338fb748c6b9184426ea50b4d1b3735c062065148a9e5cadc5a2c5",
    "critical_expository_edition/chapters/04_numen.tex": "98eb08b29df3058e829d6b816c158b839c5fd8a64815f32f9473abe848f6fc20",
    "critical_expository_edition/chapters/05_correspondence.tex": "17e312123afe89d1aa87ec3069b140d29522b79691be86314da8e261bcee1aa5",
    "critical_expository_edition/chapters/06_dreamcatchers.tex": "c3ad85155b5f34cce34d14a6e61e2aa0e578f467e4f7f8cc0bd1e8db06cf4ff6",
    "critical_expository_edition/chapters/07_contour_mellin.tex": "097d7ab21b0860fc6580160114296843a1503c0d409551564b7d8418dee5628e",
    "critical_expository_edition/chapters/08_pq_fourier.tex": "b0c0563c5f5de95241dcc539e5b1c4bfe92a75b75ee1e81b32a6fd0b176abc6e",
    "critical_expository_edition/chapters/09_rising_fseries.tex": "ed85f1ee73a6f10d135cf7cb4460fc3c913502088376e6fc411cfda0ca56fcc2",
    "critical_expository_edition/chapters/10_synthesis.tex": "037d657bb5b613438248b10bf6fc6c03755231f7fdf214d6a28cbcea2c99ce35",
    "critical_expository_edition/chapters/11_source_register.tex": "b75e22d5ae0b2c423e6d63d68a8b6d265d76f2da04c90d1094b9f987d022c7e8",
}

EXPECTED_INPUTS = (
    "chapters/00_editorial_method",
    "chapters/01_canonical_corpus",
    "chapters/02_arithmetic_dynamics",
    "chapters/03_hydra_maps",
    "chapters/04_numen",
    "chapters/05_correspondence",
    "chapters/06_dreamcatchers",
    "chapters/07_contour_mellin",
    "chapters/08_pq_fourier",
    "chapters/09_rising_fseries",
    "chapters/10_synthesis",
    "chapters/11_source_register",
)

EXPECTED_RELEASE_FILES = (
    "README.md",
    "RELEASE_METADATA.json",
    *EXPECTED_TEX_FILES,
    "apparatus/CLAIM_LEDGER.jsonl",
    "apparatus/claim_ledger.schema.json",
    "apparatus/release_document_index.jsonl",
    "apparatus/release_document_index.schema.json",
    "scripts/verify_release.py",
    "qa/claim_ledger_closure.json",
    "qa/release_verification.md",
)

EXPECTED_RELEASE_FILE_SET = frozenset(EXPECTED_RELEASE_FILES)

EXPECTED_METADATA = {
    "schema_version": "1.0",
    "source_freeze_id": EXPECTED_SOURCE_FREEZE_ID,
    "release_date": "2026-08-24",
    "manifest_path": MANIFEST_NAME,
    "title": (
        "Hydra Maps, Numens, and (p,q)-Adic Analysis: A Critical Expository "
        "Edition of the Mathematical Work of Maxwell C. Siegel"
    ),
    "source_author": "Maxwell C. Siegel",
    "pdf_author_metadata": "Maxwell C. Siegel (source works)",
    "editorial_scope": (
        "Critical apparatus, typed reconstructions, counterexamples, and edition-supplied "
        "proofs are distinguished from Siegel's source text."
    ),
    "stable_pdf": {
        "filename": "maxwell_siegel_critical_expository_edition.pdf",
        "sha256": "3e89313b9d47e27390bdfe79dfc3d87ae204dc39de9f451dd136241107810061",
        "bytes": 1198545,
        "pages": 76,
        "page_width_points": 612,
        "page_height_points": 792,
        "pdf_version": "1.5",
    },
    "source": {
        "tex_file_count": len(EXPECTED_TEX_FILES),
        "document_record_count": len(EXPECTED_DOCUMENT_IDS),
        "claim_record_count": 192,
        "claim_ledger_sha256": EXPECTED_CLAIM_LEDGER_SHA256,
    },
    "reference_toolchain": {
        "latexmk": "4.88",
        "pdftex": "MiKTeX-pdfTeX 4.27 (MiKTeX 26.5)",
        "pdftex_engine": "pdfTeX 1.40.29",
        "pdflatex_format": "pdflatex 2026.8.21",
        "latex2e": "2025-11-01",
        "python": "3.13.9",
        "jsonschema": "4.26.0",
        "source_date_epoch": 1787529600,
    },
    "reproducibility_boundary": (
        "Source bytes, text, metadata, page geometry, and page rasters are reproducible "
        "under the recorded build; PDF trailer identifiers can vary with the build path."
    ),
}

# Assemble these at runtime so a scan of this verifier does not match its own
# deny-list.  The rules target project-private identifiers, not ordinary words.
PROHIBITED_LITERALS = (
    "019f" + "e2cf-438a-7112-859c-119accee0e9e",
    "codex" + "://threads",
    ".co" + "dex/",
    "Kok" + "uno",
    "Chat" + "notes",
    "Gem" + "ini",
    "WT " + "Theorems",
    "Rory" + " O'Dwyer",
    "Rory" + " O" + chr(0x2019) + "Dwyer",
    "zeta " + "thread",
    "private" + "-ish",
)

MANIFEST_LINE_RE = re.compile(r"^([0-9a-f]{64})  (.+)$")
CLAIM_ID_RE = re.compile(r"^CLM-([0-9]{4})$")
DOCUMENT_ID_RE = re.compile(r"^DOC-[0-9]{4}$")
LINE_RANGE_RE = re.compile(r"^([0-9]+)-([0-9]+)$")
LABEL_RE = re.compile(r"\\label\{([^{}]+)\}")
REFERENCE_RE = re.compile(r"\\(?:ref|eqref|pageref|cref|Cref)\{([^{}]+)\}")
CITATION_RE = re.compile(r"\\cite(?:\[[^\]]*\])*\{([^{}]+)\}")
BIBITEM_RE = re.compile(r"\\bibitem(?:\[[^\]]*\])?\{([^{}]+)\}")
FILE_COMMAND_RE = re.compile(
    r"\\(input|include|includegraphics|bibliography|addbibresource|"
    r"lstinputlisting|verbatiminput|includepdf)\*?\s*"
    r"(?:\[[^\]]*\]\s*)?\{([^{}]+)\}"
)
WINDOWS_ABSOLUTE_RE = re.compile(
    r"(?<![A-Za-z0-9+.-])[A-Za-z]:[\\/]"
    r"(?:Users|Documents and Settings|Windows|Program Files(?: \(x86\))?|ProgramData|Temp)"
    r"(?:[\\/]|$)",
    re.IGNORECASE,
)
POSIX_HOME_RE = re.compile(r"(?<![A-Za-z0-9])/(?:home|Users)/")
THEOREM_ENV_RE = re.compile(
    r"\\begin\{(theorem|lemma|proposition|corollary)\}"
    r"(?:\[[^\]]*\])?(.*?)\\end\{\1\}",
    re.DOTALL,
)
PROOF_PREFIX_RE = re.compile(
    r"(?:[ \t]*(?:%[^\r\n]*)?\r?\n|[ \t])*\\begin\{proof\}",
)

CLAIM_REQUIRED_KEYS = frozenset(
    {
        "schema_version",
        "claim_id",
        "statement",
        "attribution",
        "source_locators",
        "hypotheses",
        "status",
        "checks",
        "dependencies",
        "notes",
    }
)
PATH_LOCATOR_KEYS = frozenset({"kind", "path", "label", "lines", "title"})
DOCUMENT_LOCATOR_KEYS = frozenset(
    {"kind", "document_id", "version", "locator", "lines", "sha256"}
)
CHECK_KEYS = frozenset({"kind", "result", "detail"})


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_sha256(value: Any) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256_bytes(encoded)


def add_failure(failures: list[str], message: str) -> None:
    failures.append(message)


def is_nonblank_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def file_sha256(path: Path, relative: str, failures: list[str]) -> str | None:
    try:
        return sha256_bytes(path.read_bytes())
    except OSError as error:
        add_failure(failures, f"{relative}: cannot hash file: {error}")
        return None


def validate_expected_file_hash(
    root: Path,
    relative: str,
    expected_digest: str,
    failures: list[str],
) -> None:
    actual_digest = file_sha256(root / PurePosixPath(relative), relative, failures)
    if actual_digest is not None and actual_digest != expected_digest:
        add_failure(
            failures,
            f"{relative}: canonical release SHA-256 mismatch, expected {expected_digest}, "
            f"found {actual_digest}",
        )


def read_utf8(path: Path, relative: str, failures: list[str]) -> str | None:
    try:
        data = path.read_bytes()
    except OSError as error:
        add_failure(failures, f"{relative}: cannot read file: {error}")
        return None
    if b"\x00" in data:
        add_failure(failures, f"{relative}: contains a NUL byte")
    if b"\r" in data:
        add_failure(failures, f"{relative}: contains a carriage return; release text must use LF")
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as error:
        add_failure(failures, f"{relative}: invalid UTF-8: {error}")
        return None


def safe_relative_path(value: str) -> bool:
    if not value or "\\" in value or value.startswith("/") or value.endswith("/"):
        return False
    if re.match(r"^[A-Za-z]:", value):
        return False
    if "//" in value:
        return False
    raw_parts = value.split("/")
    if any(part in {"", ".", ".."} for part in raw_parts):
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and path.as_posix() == value


def tex_argument_items(value: str) -> list[str]:
    without_line_comments = re.sub(r"(?<!\\)%[^\n]*(?:\n|$)", "", value)
    return [item.strip() for item in without_line_comments.split(",") if item.strip()]


def parse_json_file(path: Path, relative: str, failures: list[str]) -> Any | None:
    text = read_utf8(path, relative, failures)
    if text is None:
        return None
    if not text.endswith("\n"):
        add_failure(failures, f"{relative}: missing final LF")
    try:
        return json.loads(text)
    except json.JSONDecodeError as error:
        add_failure(failures, f"{relative}: invalid JSON: {error}")
        return None


def parse_jsonl(path: Path, relative: str, failures: list[str]) -> list[dict[str, Any]]:
    text = read_utf8(path, relative, failures)
    if text is None:
        return []
    if not text.endswith("\n"):
        add_failure(failures, f"{relative}: missing final LF")
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line:
            add_failure(failures, f"{relative}:{line_number}: blank JSONL line")
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as error:
            add_failure(failures, f"{relative}:{line_number}: invalid JSON: {error}")
            continue
        if not isinstance(value, dict):
            add_failure(failures, f"{relative}:{line_number}: record is not an object")
            continue
        rows.append(value)
    if not rows:
        add_failure(failures, f"{relative}: contains no records")
    return rows


def format_json_path(parts: Iterable[Any]) -> str:
    rendered = ""
    for part in parts:
        if isinstance(part, int):
            rendered += f"[{part}]"
        else:
            rendered += ("." if rendered else "") + str(part)
    return rendered or "<record>"


def validate_records_against_schema(
    rows: list[dict[str, Any]],
    schema: Any,
    relative: str,
    failures: list[str],
) -> None:
    if not isinstance(schema, dict):
        add_failure(failures, f"{relative}: schema is not an object")
        return
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as error:
        add_failure(failures, f"{relative}: invalid Draft 2020-12 schema: {error}")
        return
    validator = Draft202012Validator(schema)
    for line_number, row in enumerate(rows, start=1):
        try:
            errors = sorted(
                validator.iter_errors(row),
                key=lambda item: tuple(str(part) for part in item.absolute_path),
            )
        except Exception as error:
            add_failure(
                failures,
                f"{relative}:{line_number}: schema validation could not complete: "
                f"{type(error).__name__}: {error}",
            )
            continue
        for error in errors:
            location = format_json_path(error.absolute_path)
            add_failure(failures, f"{relative}:{line_number}:{location}: {error.message}")


def parse_manifest(root: Path, failures: list[str]) -> OrderedDict[str, str]:
    relative = MANIFEST_NAME
    text = read_utf8(root / relative, relative, failures)
    entries: OrderedDict[str, str] = OrderedDict()
    if text is None:
        return entries
    if not text.endswith("\n"):
        add_failure(failures, f"{relative}: missing final LF")
    previous_path: str | None = None
    casefolded: dict[str, str] = {}
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = MANIFEST_LINE_RE.fullmatch(line)
        if match is None:
            add_failure(failures, f"{relative}:{line_number}: expected lowercase SHA-256, two spaces, path")
            continue
        digest, entry_path = match.groups()
        if not safe_relative_path(entry_path):
            add_failure(failures, f"{relative}:{line_number}: unsafe or noncanonical path {entry_path!r}")
            continue
        if entry_path == MANIFEST_NAME:
            add_failure(failures, f"{relative}:{line_number}: manifest cannot hash itself")
        if entry_path in entries:
            add_failure(failures, f"{relative}:{line_number}: duplicate path {entry_path!r}")
            continue
        folded = entry_path.casefold()
        if folded in casefolded:
            add_failure(
                failures,
                f"{relative}:{line_number}: case-colliding paths {casefolded[folded]!r} and {entry_path!r}",
            )
        else:
            casefolded[folded] = entry_path
        if previous_path is not None and entry_path <= previous_path:
            add_failure(failures, f"{relative}:{line_number}: entries are not strictly lexicographically sorted")
        previous_path = entry_path
        entries[entry_path] = digest
    manifest_set = set(entries)
    if manifest_set != EXPECTED_RELEASE_FILE_SET:
        missing = sorted(EXPECTED_RELEASE_FILE_SET - manifest_set)
        extra = sorted(manifest_set - EXPECTED_RELEASE_FILE_SET)
        if missing:
            add_failure(failures, f"{relative}: missing whitelist entries: {missing}")
        if extra:
            add_failure(failures, f"{relative}: unapproved entries: {extra}")
    return entries


def verify_tree_and_hashes(
    root: Path,
    manifest: OrderedDict[str, str],
    failures: list[str],
) -> None:
    actual_files: set[str] = set()
    casefolded: dict[str, str] = {}
    try:
        candidates = sorted(root.rglob("*"), key=lambda item: item.as_posix())
    except OSError as error:
        add_failure(failures, f"release tree cannot be enumerated: {error}")
        return
    for path in candidates:
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            add_failure(failures, f"{relative}: symlinks are not permitted")
            continue
        if not path.is_file():
            continue
        if not safe_relative_path(relative):
            add_failure(failures, f"{relative}: unsafe or noncanonical filesystem path")
            continue
        folded = relative.casefold()
        if folded in casefolded:
            add_failure(failures, f"case-colliding files: {casefolded[folded]!r} and {relative!r}")
        else:
            casefolded[folded] = relative
        actual_files.add(relative)
    expected_actual = EXPECTED_RELEASE_FILE_SET | {MANIFEST_NAME}
    if actual_files != expected_actual:
        missing = sorted(expected_actual - actual_files)
        extra = sorted(actual_files - expected_actual)
        if missing:
            add_failure(failures, f"release tree missing files: {missing}")
        if extra:
            add_failure(failures, f"release tree has unmanifested files: {extra}")
    for relative, expected_digest in manifest.items():
        path = root / PurePosixPath(relative)
        if not path.is_file() or path.is_symlink():
            continue
        try:
            actual_digest = sha256_bytes(path.read_bytes())
        except OSError as error:
            add_failure(failures, f"{relative}: cannot hash file: {error}")
            continue
        if actual_digest != expected_digest:
            add_failure(
                failures,
                f"{relative}: SHA-256 mismatch, expected {expected_digest}, found {actual_digest}",
            )


def iter_json_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from iter_json_strings(item)
    elif isinstance(value, dict):
        for key, item in value.items():
            yield str(key)
            yield from iter_json_strings(item)


def prohibited_hits(text: str) -> list[str]:
    lowered = text.casefold()
    hits = [literal for literal in PROHIBITED_LITERALS if literal.casefold() in lowered]
    if WINDOWS_ABSOLUTE_RE.search(text):
        hits.append("absolute Windows path")
    if POSIX_HOME_RE.search(text):
        hits.append("absolute home path")
    return hits


def scan_release_text(
    root: Path,
    parsed_json_values: dict[str, Any],
    failures: list[str],
) -> None:
    for relative in (*EXPECTED_RELEASE_FILES, MANIFEST_NAME):
        text = read_utf8(root / PurePosixPath(relative), relative, failures)
        if text is None:
            continue
        hits = prohibited_hits(text)
        if hits:
            add_failure(failures, f"{relative}: prohibited raw content: {sorted(set(hits))}")
    for relative, value in parsed_json_values.items():
        for string in iter_json_strings(value):
            hits = prohibited_hits(string)
            if hits:
                add_failure(
                    failures,
                    f"{relative}: prohibited decoded JSON content: {sorted(set(hits))}",
                )
                break


def validate_claim_runtime_shapes(
    claims: list[dict[str, Any]],
    failures: list[str],
) -> None:
    """Defend every later traversal even if a bundled schema is malformed."""
    for line_number, claim in enumerate(claims, start=1):
        prefix = f"CLAIM_LEDGER.jsonl:{line_number}"
        keys = set(claim)
        if keys != CLAIM_REQUIRED_KEYS:
            add_failure(
                failures,
                f"{prefix}: claim fields differ from the exact runtime shape; "
                f"missing={sorted(CLAIM_REQUIRED_KEYS - keys)}, "
                f"extra={sorted(keys - CLAIM_REQUIRED_KEYS)}",
            )
        if claim.get("schema_version") != "1.0":
            add_failure(failures, f"{prefix}: schema_version must be '1.0'")
        if not is_nonblank_string(claim.get("statement")):
            add_failure(failures, f"{prefix}: statement must be a nonblank string")

        for name in ("hypotheses", "notes", "dependencies"):
            values = claim.get(name)
            if not isinstance(values, list) or any(not is_nonblank_string(item) for item in values):
                add_failure(failures, f"{prefix}: {name} must be an array of nonblank strings")

        checks = claim.get("checks")
        if not isinstance(checks, list) or not checks:
            add_failure(failures, f"{prefix}: checks must be a nonempty array")
        else:
            for check_number, check in enumerate(checks, start=1):
                if not isinstance(check, dict):
                    add_failure(failures, f"{prefix}: check {check_number} is not an object")
                    continue
                if set(check) != CHECK_KEYS:
                    add_failure(
                        failures,
                        f"{prefix}: check {check_number} fields must be exactly {sorted(CHECK_KEYS)}",
                    )
                for name in CHECK_KEYS:
                    if not is_nonblank_string(check.get(name)):
                        add_failure(
                            failures,
                            f"{prefix}: check {check_number}.{name} must be a nonblank string",
                        )

        locators = claim.get("source_locators")
        if not isinstance(locators, list) or not locators:
            add_failure(failures, f"{prefix}: source_locators must be a nonempty array")
            continue
        canonical_locators: list[str] = []
        for locator_number, locator in enumerate(locators, start=1):
            locator_prefix = f"{prefix}: source locator {locator_number}"
            if not isinstance(locator, dict):
                add_failure(failures, f"{locator_prefix} is not an object")
                continue
            has_path = "path" in locator
            has_document = "document_id" in locator
            if has_path == has_document:
                add_failure(
                    failures,
                    f"{locator_prefix} must be exactly one of an edition-path or document locator",
                )
                continue
            allowed = PATH_LOCATOR_KEYS if has_path else DOCUMENT_LOCATOR_KEYS
            extra = sorted(set(locator) - allowed)
            if extra:
                add_failure(failures, f"{locator_prefix} has unapproved fields {extra}")
            if not is_nonblank_string(locator.get("kind")):
                add_failure(failures, f"{locator_prefix}.kind must be a nonblank string")
            if has_path:
                path_value = locator.get("path")
                if not isinstance(path_value, str) or not safe_relative_path(path_value):
                    add_failure(failures, f"{locator_prefix}.path is unsafe or noncanonical")
                label = locator.get("label")
                lines = locator.get("lines")
                if label is None and lines is None:
                    add_failure(failures, f"{locator_prefix} requires label and/or lines")
                if label is not None and not is_nonblank_string(label):
                    add_failure(failures, f"{locator_prefix}.label must be a nonblank string")
                if lines is not None and (
                    not isinstance(lines, str) or LINE_RANGE_RE.fullmatch(lines) is None
                ):
                    add_failure(failures, f"{locator_prefix}.lines must be a numeric start-end range")
                if "title" in locator and not is_nonblank_string(locator.get("title")):
                    add_failure(failures, f"{locator_prefix}.title must be a nonblank string")
            else:
                document_id = locator.get("document_id")
                if not isinstance(document_id, str) or DOCUMENT_ID_RE.fullmatch(document_id) is None:
                    add_failure(failures, f"{locator_prefix}.document_id is invalid")
                if not is_nonblank_string(locator.get("version")):
                    add_failure(failures, f"{locator_prefix}.version must be a nonblank string")
                position_names = [name for name in ("locator", "lines") if name in locator]
                if len(position_names) != 1:
                    add_failure(
                        failures,
                        f"{locator_prefix} must contain exactly one of locator or lines",
                    )
                elif not is_nonblank_string(locator.get(position_names[0])):
                    add_failure(
                        failures,
                        f"{locator_prefix}.{position_names[0]} must be a nonblank string",
                    )
                digest = locator.get("sha256")
                if digest is not None and (
                    not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None
                ):
                    add_failure(failures, f"{locator_prefix}.sha256 is invalid")
            canonical_locators.append(
                json.dumps(locator, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            )
        if len(canonical_locators) != len(set(canonical_locators)):
            add_failure(failures, f"{prefix}: duplicate source locators")


def validate_claim_graph(
    claims: list[dict[str, Any]],
    failures: list[str],
) -> dict[str, dict[str, Any]]:
    by_id: dict[str, dict[str, Any]] = {}
    physical_ids: list[str] = []
    for line_number, claim in enumerate(claims, start=1):
        claim_id = claim.get("claim_id")
        if not isinstance(claim_id, str) or CLAIM_ID_RE.fullmatch(claim_id) is None:
            add_failure(failures, f"CLAIM_LEDGER.jsonl:{line_number}: invalid claim_id {claim_id!r}")
            continue
        physical_ids.append(claim_id)
        if claim_id in by_id:
            add_failure(failures, f"CLAIM_LEDGER.jsonl:{line_number}: duplicate claim_id {claim_id}")
        else:
            by_id[claim_id] = claim
    expected_ids = [f"CLM-{number:04d}" for number in range(1, len(claims) + 1)]
    if physical_ids != expected_ids:
        add_failure(failures, "CLAIM_LEDGER.jsonl: claim IDs are not contiguous and ordered from CLM-0001")
    graph: dict[str, list[str]] = {}
    for claim_id, claim in by_id.items():
        dependencies = claim.get("dependencies")
        if not isinstance(dependencies, list) or any(not isinstance(item, str) for item in dependencies):
            add_failure(failures, f"{claim_id}: dependencies must be a string array")
            graph[claim_id] = []
            continue
        if len(dependencies) != len(set(dependencies)):
            add_failure(failures, f"{claim_id}: duplicate dependencies")
        graph[claim_id] = list(dependencies)
        for dependency in dependencies:
            dependency_match = CLAIM_ID_RE.fullmatch(dependency)
            if dependency_match is None:
                add_failure(failures, f"{claim_id}: invalid dependency ID {dependency!r}")
            elif int(dependency_match.group(1)) >= int(CLAIM_ID_RE.fullmatch(claim_id).group(1)):
                add_failure(failures, f"{claim_id}: dependency {dependency} is not strictly backward")
            if dependency == claim_id:
                add_failure(failures, f"{claim_id}: self-dependency")
            elif dependency not in by_id:
                add_failure(failures, f"{claim_id}: unresolved dependency {dependency}")
    state: dict[str, int] = {claim_id: 0 for claim_id in by_id}
    stack: list[str] = []
    cycle_reported = False

    def visit(claim_id: str) -> None:
        nonlocal cycle_reported
        state[claim_id] = 1
        stack.append(claim_id)
        for dependency in graph.get(claim_id, []):
            if dependency not in state:
                continue
            if state[dependency] == 0:
                visit(dependency)
            elif state[dependency] == 1 and not cycle_reported:
                start = stack.index(dependency)
                cycle = stack[start:] + [dependency]
                add_failure(failures, f"claim dependency cycle: {' -> '.join(cycle)}")
                cycle_reported = True
        stack.pop()
        state[claim_id] = 2

    for claim_id in by_id:
        if state[claim_id] == 0:
            visit(claim_id)
    return by_id


def document_locator_projection(
    claims: list[dict[str, Any]],
    failures: list[str],
) -> OrderedDict[str, list[dict[str, Any]]]:
    grouped: OrderedDict[str, OrderedDict[tuple[Any, ...], dict[str, Any]]] = OrderedDict(
        (document_id, OrderedDict()) for document_id in EXPECTED_DOCUMENT_IDS
    )
    allowed = {"kind", "document_id", "version", "locator", "lines", "sha256"}
    for claim in claims:
        claim_id = claim.get("claim_id")
        locators = claim.get("source_locators")
        if (
            not isinstance(claim_id, str)
            or CLAIM_ID_RE.fullmatch(claim_id) is None
            or not isinstance(locators, list)
        ):
            continue
        for locator in locators:
            if not isinstance(locator, dict) or "document_id" not in locator:
                continue
            document_id = locator.get("document_id")
            if not isinstance(document_id, str) or DOCUMENT_ID_RE.fullmatch(document_id) is None:
                add_failure(failures, f"{claim_id}: invalid document_id in source locator {document_id!r}")
                continue
            if document_id not in grouped:
                add_failure(failures, f"{claim_id}: document {document_id} is outside the release set")
                continue
            extra = sorted(set(locator) - allowed)
            if extra:
                add_failure(failures, f"{claim_id}: document locator has nonrelease fields {extra}")
            kind = locator.get("kind")
            version = locator.get("version")
            position_fields = [name for name in ("locator", "lines") if locator.get(name)]
            if not isinstance(kind, str) or not kind:
                add_failure(failures, f"{claim_id}: document locator lacks kind")
                continue
            if not isinstance(version, str) or not version:
                add_failure(failures, f"{claim_id}: document locator lacks version")
                continue
            if len(position_fields) != 1:
                add_failure(failures, f"{claim_id}: document locator must have exactly one locator/lines field")
                continue
            position_name = position_fields[0]
            position_value = locator[position_name]
            if not isinstance(position_value, str) or not position_value:
                add_failure(failures, f"{claim_id}: document locator position is empty")
                continue
            digest = locator.get("sha256")
            if digest is not None and (
                not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None
            ):
                add_failure(failures, f"{claim_id}: document locator has invalid SHA-256")
                continue
            key = (kind, version, position_name, position_value, digest)
            document_groups = grouped[document_id]
            if key not in document_groups:
                item: dict[str, Any] = {
                    "claim_ids": [],
                    "kind": kind,
                    "version": version,
                    position_name: position_value,
                }
                if digest is not None:
                    item["sha256"] = digest
                document_groups[key] = item
            document_groups[key]["claim_ids"].append(claim_id)
    return OrderedDict(
        (document_id, list(document_groups.values()))
        for document_id, document_groups in grouped.items()
    )


def validate_document_index(
    claims: list[dict[str, Any]],
    documents: list[dict[str, Any]],
    failures: list[str],
) -> int:
    document_ids = [row.get("document_id") for row in documents]
    if document_ids != list(EXPECTED_DOCUMENT_IDS):
        add_failure(
            failures,
            "release_document_index.jsonl: records are not the exact required 16-document sequence",
        )
    valid_document_ids = [item for item in document_ids if isinstance(item, str)]
    if len(valid_document_ids) != len(set(valid_document_ids)):
        add_failure(failures, "release_document_index.jsonl: duplicate document IDs")
    projection = document_locator_projection(claims, failures)
    referenced_ids: set[str] = set()
    for claim in claims:
        locators = claim.get("source_locators")
        if not isinstance(locators, list):
            continue
        for locator in locators:
            if not isinstance(locator, dict):
                continue
            document_id = locator.get("document_id")
            if isinstance(document_id, str) and document_id:
                referenced_ids.add(document_id)
    if referenced_ids != set(EXPECTED_DOCUMENT_IDS):
        missing = sorted(set(EXPECTED_DOCUMENT_IDS) - referenced_ids)
        extra = sorted(referenced_ids - set(EXPECTED_DOCUMENT_IDS))
        add_failure(
            failures,
            f"claim/document release-set mismatch; missing={missing}, extra={extra}",
        )
    by_id = {
        document_id: row
        for row in documents
        if isinstance((document_id := row.get("document_id")), str)
    }
    version_mismatches = 0
    for document_id in EXPECTED_DOCUMENT_IDS:
        row = by_id.get(document_id)
        if row is None:
            continue
        identity = {key: value for key, value in row.items() if key != "cited_locators"}
        identity_digest = canonical_json_sha256(identity)
        expected_identity_digest = EXPECTED_DOCUMENT_IDENTITY_SHA256[document_id]
        if identity_digest != expected_identity_digest:
            add_failure(
                failures,
                f"{document_id}: public bibliographic identity differs from the frozen canonical record",
            )
        actual_locators = row.get("cited_locators")
        expected_locators = projection[document_id]
        if actual_locators != expected_locators:
            add_failure(
                failures,
                f"{document_id}: cited_locators are not the exact deduplicated claim-ledger projection",
            )
        identifiers = row.get("public_identifiers")
        if not isinstance(identifiers, list):
            add_failure(failures, f"{document_id}: public_identifiers must be an array")
            identifiers = []
        arxiv_values = {
            item.get("value")
            for item in identifiers
            if isinstance(item, dict) and item.get("kind") == "arxiv"
        }
        for item in identifiers:
            if not isinstance(item, dict):
                add_failure(failures, f"{document_id}: public identifier is not an object")
                continue
            kind = item.get("kind")
            value = item.get("value")
            url = item.get("url")
            if kind == "arxiv" and isinstance(value, str):
                expected_url = f"https://arxiv.org/abs/{value}"
                if url != expected_url:
                    add_failure(
                        failures,
                        f"{document_id}: arXiv identifier value and URL do not agree exactly",
                    )
            elif kind == "doi" and isinstance(value, str):
                expected_url = f"https://doi.org/{value}"
                if url != expected_url:
                    add_failure(
                        failures,
                        f"{document_id}: DOI identifier value and URL do not agree exactly",
                    )
        observed_versions = tuple(
            sorted(
                {
                    locator.get("version")
                    for locator in expected_locators
                    if isinstance(locator.get("version"), str)
                }
            )
        )
        if observed_versions != EXPECTED_DOCUMENT_LOCATOR_VERSIONS[document_id]:
            version_mismatches += 1
            add_failure(
                failures,
                f"{document_id}: locator versions differ from the frozen canonical version set",
            )
        for locator in expected_locators:
            version = locator.get("version", "")
            match = re.fullmatch(r"arXiv:([0-9]{4}\.[0-9]{4,5}v[0-9]+)", version)
            if match and match.group(1) not in arxiv_values:
                add_failure(
                    failures,
                    f"{document_id}: locator version {version} has no matching public arXiv identifier",
                )
    return version_mismatches


def validate_tex_and_locators(
    root: Path,
    claims: list[dict[str, Any]],
    failures: list[str],
) -> dict[str, int]:
    texts: dict[str, str] = {}
    for relative in EXPECTED_TEX_FILES:
        text = read_utf8(root / PurePosixPath(relative), relative, failures)
        if text is not None:
            texts[relative] = text
    main = texts.get("critical_expository_edition/main.tex", "")
    file_commands: list[tuple[str, str, str]] = []
    for relative, text in texts.items():
        for match in FILE_COMMAND_RE.finditer(text):
            command, target = match.groups()
            file_commands.append((relative, command, target))
    actual_inputs = [target for relative, command, target in file_commands if command == "input"]
    if actual_inputs != list(EXPECTED_INPUTS):
        add_failure(failures, f"main TeX input sequence differs from release closure: {actual_inputs}")
    for relative, command, target in file_commands:
        if relative != "critical_expository_edition/main.tex" or command != "input":
            add_failure(failures, f"{relative}: unapproved file command \\{command}{{{target}}}")
    if not main:
        add_failure(failures, "critical_expository_edition/main.tex: missing or unreadable")

    label_locations: dict[str, list[str]] = defaultdict(list)
    for relative, text in texts.items():
        for match in LABEL_RE.finditer(text):
            label_locations[match.group(1)].append(relative)
    for label, locations in sorted(label_locations.items()):
        if len(locations) != 1:
            add_failure(failures, f"duplicate TeX label {label!r}: {locations}")
    all_labels = set(label_locations)
    for relative, text in texts.items():
        for match in REFERENCE_RE.finditer(text):
            for label in tex_argument_items(match.group(1)):
                if label not in all_labels:
                    add_failure(failures, f"{relative}: unresolved TeX reference {label!r}")
    bibitems: dict[str, list[str]] = defaultdict(list)
    citations: list[tuple[str, str]] = []
    for relative, text in texts.items():
        for match in BIBITEM_RE.finditer(text):
            bibitems[match.group(1)].append(relative)
        for match in CITATION_RE.finditer(text):
            for key in tex_argument_items(match.group(1)):
                citations.append((relative, key))
    for key, locations in sorted(bibitems.items()):
        if len(locations) != 1:
            add_failure(failures, f"duplicate bibliography key {key!r}: {locations}")
    for relative, key in citations:
        if key not in bibitems:
            add_failure(failures, f"{relative}: unresolved citation {key!r}")

    theorem_labels: dict[str, str] = {}
    theorem_count = 0
    proof_closed_count = 0
    for relative, text in texts.items():
        for environment_match in THEOREM_ENV_RE.finditer(text):
            theorem_count += 1
            environment = environment_match.group(1)
            body = environment_match.group(2)
            label_match = LABEL_RE.search(body)
            if label_match is None:
                add_failure(
                    failures,
                    f"{relative}: {environment} environment has no theorem label",
                )
            else:
                prefix = body[: label_match.start()]
                if prefix.strip():
                    add_failure(
                        failures,
                        f"{relative}: {environment} label is not the first substantive token",
                    )
                label = label_match.group(1)
                if label in theorem_labels:
                    add_failure(failures, f"duplicate theorem-family label {label!r}")
                else:
                    theorem_labels[label] = relative
            if PROOF_PREFIX_RE.match(text, environment_match.end()) is None:
                add_failure(
                    failures,
                    f"{relative}: {environment} environment is not immediately followed by a proof",
                )
            else:
                proof_closed_count += 1

    tex_set = set(EXPECTED_TEX_FILES)
    allowed_path_fields = {"kind", "path", "label", "lines", "title"}
    ledger_label_locations: dict[str, set[str]] = defaultdict(set)
    exact_label_locator_count = 0
    for claim in claims:
        claim_id = claim.get("claim_id", "<unknown>")
        locators = claim.get("source_locators")
        if not isinstance(locators, list):
            continue
        for locator in locators:
            if not isinstance(locator, dict) or "path" not in locator:
                continue
            extra = sorted(set(locator) - allowed_path_fields)
            if extra:
                add_failure(failures, f"{claim_id}: path locator has unapproved fields {extra}")
            path_value = locator.get("path")
            if not isinstance(path_value, str) or not safe_relative_path(path_value):
                add_failure(failures, f"{claim_id}: unsafe path locator {path_value!r}")
                continue
            if path_value not in tex_set:
                add_failure(failures, f"{claim_id}: nonedition or unbundled path locator {path_value!r}")
                continue
            text = texts.get(path_value)
            if text is None:
                continue
            label = locator.get("label")
            lines = locator.get("lines")
            if label is None and lines is None:
                add_failure(failures, f"{claim_id}: TeX path locator has neither label nor lines")
            if label is not None:
                if not isinstance(label, str):
                    add_failure(failures, f"{claim_id}: TeX label locator is not a string")
                elif label_locations.get(label) != [path_value]:
                    add_failure(
                        failures,
                        f"{claim_id}: label {label!r} does not resolve uniquely in {path_value}",
                    )
                else:
                    exact_label_locator_count += 1
                    ledger_label_locations[label].add(path_value)
            if lines is not None:
                if not isinstance(lines, str) or (match := LINE_RANGE_RE.fullmatch(lines)) is None:
                    add_failure(failures, f"{claim_id}: invalid TeX line range {lines!r}")
                else:
                    start, end = (int(match.group(1)), int(match.group(2)))
                    line_count = len(text.splitlines())
                    if start < 1 or end < start or end > line_count:
                        add_failure(
                            failures,
                            f"{claim_id}: TeX line range {lines} is outside {path_value} (1-{line_count})",
                        )

    ledger_covered_count = 0
    for label, relative in theorem_labels.items():
        if ledger_label_locations.get(label) != {relative}:
            add_failure(
                failures,
                f"theorem-family label {label!r} is not covered by a resolving claim-ledger locator",
            )
        else:
            ledger_covered_count += 1
    return {
        "theorem_family_environments": theorem_count,
        "ledger_covered": ledger_covered_count,
        "immediately_proof_closed": proof_closed_count,
        "exact_label_locators": exact_label_locator_count,
    }


def compare_exact_json(
    relative: str,
    actual: Any,
    expected: Any,
    failures: list[str],
    path: str = "",
) -> None:
    location = f"{relative}:{path or '<root>'}"
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            add_failure(
                failures,
                f"{location}: expected object, found {type(actual).__name__}",
            )
            return
        actual_keys = set(actual)
        expected_keys = set(expected)
        if actual_keys != expected_keys:
            add_failure(
                failures,
                f"{location}: exact keys differ; missing={sorted(expected_keys - actual_keys)}, "
                f"extra={sorted(actual_keys - expected_keys)}",
            )
        for key in expected_keys & actual_keys:
            child = f"{path}.{key}" if path else str(key)
            compare_exact_json(relative, actual[key], expected[key], failures, child)
        return
    if isinstance(expected, list):
        if not isinstance(actual, list):
            add_failure(
                failures,
                f"{location}: expected array, found {type(actual).__name__}",
            )
            return
        if len(actual) != len(expected):
            add_failure(
                failures,
                f"{location}: expected {len(expected)} items, found {len(actual)}",
            )
        for index, (actual_item, expected_item) in enumerate(zip(actual, expected)):
            compare_exact_json(
                relative,
                actual_item,
                expected_item,
                failures,
                f"{path}[{index}]",
            )
        return
    if type(actual) is not type(expected):
        add_failure(
            failures,
            f"{location}: expected {type(expected).__name__}, found {type(actual).__name__}",
        )
        return
    if actual != expected:
        add_failure(failures, f"{location}: expected {expected!r}, found {actual!r}")


def schema_failure_count(rows: list[dict[str, Any]], schema: Any) -> int:
    if not isinstance(schema, dict):
        return 1
    try:
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        return sum(1 for row in rows for _ in validator.iter_errors(row))
    except Exception:
        return 1


def dependency_metrics(claims: list[dict[str, Any]]) -> dict[str, Any]:
    ids = {
        claim_id
        for claim in claims
        if isinstance((claim_id := claim.get("claim_id")), str)
        and CLAIM_ID_RE.fullmatch(claim_id) is not None
    }
    edge_count = 0
    all_targets_exist = True
    all_edges_strictly_backward = True
    graph: dict[str, list[str]] = {}
    for claim in claims:
        claim_id = claim.get("claim_id")
        if not isinstance(claim_id, str) or CLAIM_ID_RE.fullmatch(claim_id) is None:
            continue
        dependencies = claim.get("dependencies")
        if not isinstance(dependencies, list):
            dependencies = []
            all_targets_exist = False
            all_edges_strictly_backward = False
        valid_dependencies: list[str] = []
        claim_number = int(CLAIM_ID_RE.fullmatch(claim_id).group(1))
        for dependency in dependencies:
            edge_count += 1
            if not isinstance(dependency, str) or CLAIM_ID_RE.fullmatch(dependency) is None:
                all_targets_exist = False
                all_edges_strictly_backward = False
                continue
            valid_dependencies.append(dependency)
            if dependency not in ids:
                all_targets_exist = False
            if int(CLAIM_ID_RE.fullmatch(dependency).group(1)) >= claim_number:
                all_edges_strictly_backward = False
        graph[claim_id] = valid_dependencies

    state = {claim_id: 0 for claim_id in graph}
    acyclic = True

    def visit(claim_id: str) -> None:
        nonlocal acyclic
        state[claim_id] = 1
        for dependency in graph.get(claim_id, []):
            if dependency not in state:
                continue
            if state[dependency] == 0:
                visit(dependency)
            elif state[dependency] == 1:
                acyclic = False
        state[claim_id] = 2

    for claim_id in graph:
        if state[claim_id] == 0:
            visit(claim_id)
    return {
        "edge_count": edge_count,
        "all_targets_exist": all_targets_exist,
        "all_edges_strictly_backward": all_edges_strictly_backward,
        "acyclic": acyclic,
    }


def chapter10_result_counts(chapter_text: str) -> dict[str, int]:
    start_marker = r"\subsection{Result-status table}"
    end_marker = r"\subsection{Source-by-source repair ledger}"
    start = chapter_text.find(start_marker)
    end = chapter_text.find(end_marker, start + len(start_marker)) if start >= 0 else -1
    if start < 0 or end < 0:
        return {
            "reconstructed_and_proved": -1,
            "source_checked": -1,
            "withdrawn_or_invalid": -1,
            "conditional_or_formal": -1,
        }
    table = chapter_text[start:end]
    counts = Counter(re.findall(r"\\textbf\{([RSCW])\}\s*&", table))
    return {
        "reconstructed_and_proved": counts["R"],
        "source_checked": counts["S"],
        "withdrawn_or_invalid": counts["W"],
        "conditional_or_formal": counts["C"],
    }


def expected_closure_record(
    root: Path,
    claims: list[dict[str, Any]],
    claim_schema: Any,
    theorem_metrics: dict[str, int],
    document_version_mismatches: int,
) -> dict[str, Any]:
    claim_ids = [claim.get("claim_id") for claim in claims]
    expected_ids = [f"CLM-{number:04d}" for number in range(1, len(claims) + 1)]
    all_locators = [
        locator
        for claim in claims
        for locator in (
            claim.get("source_locators") if isinstance(claim.get("source_locators"), list) else []
        )
        if isinstance(locator, dict)
    ]
    path_locators = [locator for locator in all_locators if "path" in locator]
    document_locators = [locator for locator in all_locators if "document_id" in locator]
    status_counts = Counter(
        status for claim in claims if isinstance((status := claim.get("status")), str)
    )
    attribution_counts = Counter(
        attribution
        for claim in claims
        if isinstance((attribution := claim.get("attribution")), str)
    )
    nonpromoted = OrderedDict(
        (
            status,
            [claim.get("claim_id") for claim in claims if claim.get("status") == status],
        )
        for status in EXPECTED_NONPROMOTED_CLAIMS
    )
    chapter_text = read_utf8(
        root / "critical_expository_edition/chapters/10_synthesis.tex",
        "critical_expository_edition/chapters/10_synthesis.tex",
        [],
    ) or ""
    ledger_digest = file_sha256(
        root / "apparatus/CLAIM_LEDGER.jsonl",
        "apparatus/CLAIM_LEDGER.jsonl",
        [],
    ) or ""
    schema_digest = file_sha256(
        root / "apparatus/claim_ledger.schema.json",
        "apparatus/claim_ledger.schema.json",
        [],
    ) or ""
    dependency = dependency_metrics(claims)
    return {
        "schema_version": "1.0",
        "source_freeze_id": EXPECTED_SOURCE_FREEZE_ID,
        "status": "pass",
        "claim_ledger": {
            "path": "apparatus/CLAIM_LEDGER.jsonl",
            "sha256": ledger_digest,
            "record_count": len(claims),
            "first_id": claim_ids[0] if claim_ids else None,
            "last_id": claim_ids[-1] if claim_ids else None,
            "unique_contiguous_ids": claim_ids == expected_ids and len(claim_ids) == len(set(claim_ids)),
        },
        "schema": {
            "path": "apparatus/claim_ledger.schema.json",
            "sha256": schema_digest,
            "failure_count": schema_failure_count(claims, claim_schema),
        },
        "dependency_graph": dependency,
        "locators": {
            "total": len(all_locators),
            "edition_path_locators": len(path_locators),
            "nonedition_path_locators": sum(
                1 for locator in path_locators if locator.get("path") not in EXPECTED_TEX_FILES
            ),
            "document_locators": len(document_locators),
            "document_version_mismatches": document_version_mismatches,
            "exact_label_locators": theorem_metrics["exact_label_locators"],
            "failures": 0,
        },
        "formal_closure": {
            "theorem_family_environments": theorem_metrics["theorem_family_environments"],
            "ledger_covered": theorem_metrics["ledger_covered"],
            "immediately_proof_closed": theorem_metrics["immediately_proof_closed"],
            "chapter_10_rows": chapter10_result_counts(chapter_text),
        },
        "status_counts": {
            status: status_counts[status]
            for status in EXPECTED_STATUS_COUNTS
            if status_counts[status] or status in EXPECTED_STATUS_COUNTS
        },
        "attribution_counts": {
            attribution: attribution_counts[attribution]
            for attribution in ("siegel", "prior_literature", "new_synthesis")
        },
        "nonpromoted_claims": nonpromoted,
    }


def validate_frozen_counts(
    claims: list[dict[str, Any]],
    theorem_metrics: dict[str, int],
    closure_expected: dict[str, Any],
    failures: list[str],
) -> None:
    if len(claims) != 192:
        add_failure(failures, f"CLAIM_LEDGER.jsonl: expected 192 records, found {len(claims)}")
    status_counts = Counter(claim.get("status") for claim in claims)
    actual_status_counts = {status: status_counts[status] for status in EXPECTED_STATUS_COUNTS}
    if actual_status_counts != dict(EXPECTED_STATUS_COUNTS):
        add_failure(
            failures,
            f"CLAIM_LEDGER.jsonl: frozen status counts differ: {actual_status_counts}",
        )
    attribution_counts = Counter(claim.get("attribution") for claim in claims)
    actual_attribution_counts = {
        attribution: attribution_counts[attribution]
        for attribution in EXPECTED_ATTRIBUTION_COUNTS
    }
    if actual_attribution_counts != EXPECTED_ATTRIBUTION_COUNTS:
        add_failure(
            failures,
            f"CLAIM_LEDGER.jsonl: frozen attribution counts differ: {actual_attribution_counts}",
        )
    actual_nonpromoted = closure_expected["nonpromoted_claims"]
    if actual_nonpromoted != EXPECTED_NONPROMOTED_CLAIMS:
        add_failure(
            failures,
            "CLAIM_LEDGER.jsonl: frozen nonpromoted claim-ID sets differ",
        )
    expected_theorem = {
        "theorem_family_environments": 48,
        "ledger_covered": 48,
        "immediately_proof_closed": 48,
        "exact_label_locators": 129,
    }
    if theorem_metrics != expected_theorem:
        add_failure(
            failures,
            f"TeX/ledger formal closure differs from the frozen counts: {theorem_metrics}",
        )
    expected_chapter_rows = {
        "reconstructed_and_proved": 23,
        "source_checked": 2,
        "withdrawn_or_invalid": 11,
        "conditional_or_formal": 6,
    }
    if closure_expected["formal_closure"]["chapter_10_rows"] != expected_chapter_rows:
        add_failure(
            failures,
            "chapter 10 result-status row counts differ from the frozen 23/2/11/6 boundary",
        )
    if closure_expected["dependency_graph"]["edge_count"] != 214:
        add_failure(failures, "claim dependency edge count differs from the frozen value 214")
    if closure_expected["locators"]["total"] != 398:
        add_failure(failures, "claim source-locator count differs from the frozen value 398")
    if closure_expected["locators"]["edition_path_locators"] != 206:
        add_failure(failures, "edition path-locator count differs from the frozen value 206")
    if closure_expected["locators"]["document_locators"] != 192:
        add_failure(failures, "document-locator count differs from the frozen value 192")


def find_recursive_keys(value: Any, target_keys: set[str]) -> list[str]:
    hits: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if str(key).casefold() in target_keys:
                hits.append(str(key))
            hits.extend(find_recursive_keys(item, target_keys))
    elif isinstance(value, list):
        for item in value:
            hits.extend(find_recursive_keys(item, target_keys))
    return hits


def verify_zip_archive(zip_path: Path) -> tuple[dict[str, Any], list[str]]:
    failures: list[str] = []
    expected_inner_files = EXPECTED_RELEASE_FILE_SET | {MANIFEST_NAME}
    expected_archive_files = {
        f"{EXPECTED_ZIP_ROOT}/{relative}" for relative in expected_inner_files
    }
    allowed_directories = {f"{EXPECTED_ZIP_ROOT}/"}
    for relative in expected_inner_files:
        parts = PurePosixPath(relative).parts
        for length in range(1, len(parts)):
            allowed_directories.add(
                f"{EXPECTED_ZIP_ROOT}/{'/'.join(parts[:length])}/"
            )
    archive_files: set[str] = set()
    archive_names: set[str] = set()
    casefolded_names: dict[str, str] = {}
    total_uncompressed = 0
    extracted_summary: dict[str, Any] | None = None
    try:
        with zipfile.ZipFile(zip_path, "r") as archive:
            infos = archive.infolist()
            if len(infos) > len(expected_archive_files) + len(allowed_directories):
                add_failure(failures, "ZIP archive has more entries than the exact release permits")
            for info in infos:
                name = info.filename
                if not name or "\\" in name or name.startswith("/") or "\x00" in name:
                    add_failure(failures, f"ZIP entry has an unsafe name: {name!r}")
                    continue
                canonical_subject = name[:-1] if info.is_dir() and name.endswith("/") else name
                if not safe_relative_path(canonical_subject):
                    add_failure(failures, f"ZIP entry has a noncanonical path: {name!r}")
                    continue
                if name in archive_names:
                    add_failure(failures, f"ZIP archive has a duplicate entry: {name!r}")
                archive_names.add(name)
                folded = name.casefold()
                if folded in casefolded_names and casefolded_names[folded] != name:
                    add_failure(
                        failures,
                        f"ZIP archive has case-colliding entries: "
                        f"{casefolded_names[folded]!r} and {name!r}",
                    )
                else:
                    casefolded_names[folded] = name
                if info.flag_bits & 0x1:
                    add_failure(failures, f"ZIP entry is encrypted: {name!r}")
                unix_mode = (info.external_attr >> 16) & 0xFFFF
                if info.create_system == 3 and unix_mode:
                    file_type = stat.S_IFMT(unix_mode)
                    if file_type == stat.S_IFLNK:
                        add_failure(failures, f"ZIP entry is a symbolic link: {name!r}")
                    elif file_type not in {0, stat.S_IFREG, stat.S_IFDIR}:
                        add_failure(failures, f"ZIP entry has an unsupported Unix file type: {name!r}")
                if info.is_dir():
                    if name not in allowed_directories:
                        add_failure(failures, f"ZIP archive has an unapproved directory entry: {name!r}")
                    continue
                archive_files.add(name)
                if name not in expected_archive_files:
                    add_failure(failures, f"ZIP archive has an unapproved file entry: {name!r}")
                total_uncompressed += info.file_size
                if info.file_size > 16 * 1024 * 1024:
                    add_failure(failures, f"ZIP entry is unexpectedly large: {name!r}")
                if info.file_size > 1024 * 1024 and info.compress_size > 0:
                    if info.file_size / info.compress_size > 1000:
                        add_failure(failures, f"ZIP entry has an unsafe compression ratio: {name!r}")
            if total_uncompressed > 64 * 1024 * 1024:
                add_failure(failures, "ZIP archive exceeds the release uncompressed-size limit")
            if archive_files != expected_archive_files:
                missing = sorted(expected_archive_files - archive_files)
                extra = sorted(archive_files - expected_archive_files)
                if missing:
                    add_failure(failures, f"ZIP archive is missing exact release files: {missing}")
                if extra:
                    add_failure(failures, f"ZIP archive has extra release files: {extra}")
            if not failures:
                try:
                    corrupt = archive.testzip()
                except (OSError, RuntimeError, zipfile.BadZipFile) as error:
                    add_failure(failures, f"ZIP CRC verification could not complete: {error}")
                    corrupt = None
                if corrupt is not None:
                    add_failure(failures, f"ZIP CRC verification failed at {corrupt!r}")

            if not failures:
                with tempfile.TemporaryDirectory(prefix="maxwell_siegel_release_verify_") as temporary:
                    temporary_root = Path(temporary)
                    for info in infos:
                        if info.is_dir():
                            continue
                        relative_inside = info.filename[len(EXPECTED_ZIP_ROOT) + 1 :]
                        destination = temporary_root / EXPECTED_ZIP_ROOT / PurePosixPath(relative_inside)
                        destination.parent.mkdir(parents=True, exist_ok=True)
                        try:
                            data = archive.read(info)
                            destination.write_bytes(data)
                        except (OSError, RuntimeError, zipfile.BadZipFile) as error:
                            add_failure(
                                failures,
                                f"ZIP entry {info.filename!r} could not be safely extracted: {error}",
                            )
                            break
                    if not failures:
                        extracted_summary, extracted_failures = verify(
                            temporary_root / EXPECTED_ZIP_ROOT
                        )
                        failures.extend(f"extracted release: {item}" for item in extracted_failures)
    except (OSError, RuntimeError, zipfile.BadZipFile, zipfile.LargeZipFile) as error:
        add_failure(failures, f"ZIP archive cannot be read: {type(error).__name__}: {error}")
    except Exception as error:
        add_failure(
            failures,
            f"ZIP verification failed safely: {type(error).__name__}: {error}",
        )
    summary = {
        "schema_version": "1.0",
        "status": "pass" if not failures else "fail",
        "mode": "zip",
        "zip_path": str(zip_path),
        "archive_file_count": len(archive_files),
        "expected_archive_file_count": len(expected_archive_files),
        "uncompressed_bytes": total_uncompressed,
        "extracted_release_summary": extracted_summary,
        "failure_count": len(failures),
        "failures": failures,
    }
    return summary, failures


def verify(root: Path) -> tuple[dict[str, Any], list[str]]:
    failures: list[str] = []
    manifest = parse_manifest(root, failures)
    verify_tree_and_hashes(root, manifest, failures)

    claim_schema_relative = "apparatus/claim_ledger.schema.json"
    document_schema_relative = "apparatus/release_document_index.schema.json"
    claim_relative = "apparatus/CLAIM_LEDGER.jsonl"
    document_relative = "apparatus/release_document_index.jsonl"
    metadata_relative = "RELEASE_METADATA.json"
    closure_relative = "qa/claim_ledger_closure.json"

    validate_expected_file_hash(
        root, claim_relative, EXPECTED_CLAIM_LEDGER_SHA256, failures
    )
    validate_expected_file_hash(
        root, document_relative, EXPECTED_DOCUMENT_INDEX_SHA256, failures
    )
    validate_expected_file_hash(
        root, claim_schema_relative, EXPECTED_CLAIM_SCHEMA_SHA256, failures
    )
    validate_expected_file_hash(
        root, document_schema_relative, EXPECTED_DOCUMENT_SCHEMA_SHA256, failures
    )
    for relative, expected_digest in EXPECTED_TEX_SHA256.items():
        validate_expected_file_hash(root, relative, expected_digest, failures)

    claim_schema = parse_json_file(root / claim_schema_relative, claim_schema_relative, failures)
    document_schema = parse_json_file(root / document_schema_relative, document_schema_relative, failures)
    metadata = parse_json_file(root / metadata_relative, metadata_relative, failures)
    closure = parse_json_file(root / closure_relative, closure_relative, failures)
    claims = parse_jsonl(root / claim_relative, claim_relative, failures)
    documents = parse_jsonl(root / document_relative, document_relative, failures)

    validate_records_against_schema(claims, claim_schema, claim_relative, failures)
    validate_records_against_schema(documents, document_schema, document_relative, failures)
    validate_claim_runtime_shapes(claims, failures)
    validate_claim_graph(claims, failures)
    document_version_mismatches = validate_document_index(claims, documents, failures)
    theorem_metrics = validate_tex_and_locators(root, claims, failures)

    closure_expected = expected_closure_record(
        root,
        claims,
        claim_schema,
        theorem_metrics,
        document_version_mismatches,
    )
    validate_frozen_counts(claims, theorem_metrics, closure_expected, failures)
    if not isinstance(closure, dict):
        add_failure(failures, f"{closure_relative}: closure receipt must be an object")
    else:
        compare_exact_json(closure_relative, closure, closure_expected, failures)

    if not isinstance(metadata, dict):
        add_failure(failures, f"{metadata_relative}: metadata must be an object")
    else:
        compare_exact_json(metadata_relative, metadata, EXPECTED_METADATA, failures)
        circular_keys = find_recursive_keys(
            metadata,
            {"manifest_sha256", "manifest_digest", "manifest_hash"},
        )
        if circular_keys:
            add_failure(
                failures,
                f"{metadata_relative}: circular manifest digest field(s) are forbidden: {circular_keys}",
            )

    parsed_values = {
        claim_schema_relative: claim_schema,
        document_schema_relative: document_schema,
        metadata_relative: metadata,
        closure_relative: closure,
        claim_relative: claims,
        document_relative: documents,
    }
    scan_release_text(root, parsed_values, failures)

    summary = {
        "schema_version": "1.0",
        "status": "pass" if not failures else "fail",
        "manifest_entry_count": len(manifest),
        "expected_file_count_including_manifest": len(EXPECTED_RELEASE_FILES) + 1,
        "claim_record_count": len(claims),
        "document_record_count": len(documents),
        "tex_file_count": len(EXPECTED_TEX_FILES),
        "failure_count": len(failures),
        "failures": failures,
    }
    return summary, failures


def default_root() -> Path:
    script = Path(__file__).resolve()
    candidate = script.parent.parent
    return candidate


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify the complete portable Maxwell Siegel edition source release."
    )
    source = parser.add_mutually_exclusive_group()
    source.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Extracted release root; defaults to the parent of this script's directory.",
    )
    source.add_argument(
        "--zip",
        type=Path,
        default=None,
        help="Portable release ZIP; validates archive safety, CRCs, extraction, and contents.",
    )
    args = parser.parse_args()
    try:
        if args.zip is not None:
            zip_path = args.zip.resolve()
            if not zip_path.is_file():
                summary = {
                    "schema_version": "1.0",
                    "status": "fail",
                    "mode": "zip",
                    "failure_count": 1,
                    "failures": ["release ZIP is not a file"],
                }
                print(json.dumps(summary, ensure_ascii=False, separators=(",", ":")))
                return 1
            summary, failures = verify_zip_archive(zip_path)
        else:
            root = (args.root if args.root is not None else default_root()).resolve()
            if not root.is_dir():
                summary = {
                    "schema_version": "1.0",
                    "status": "fail",
                    "mode": "directory",
                    "failure_count": 1,
                    "failures": ["release root is not a directory"],
                }
                print(json.dumps(summary, ensure_ascii=False, separators=(",", ":")))
                return 1
            summary, failures = verify(root)
            summary["mode"] = "directory"
    except Exception as error:
        failures = [f"verification failed safely: {type(error).__name__}: {error}"]
        summary = {
            "schema_version": "1.0",
            "status": "fail",
            "mode": "zip" if args.zip is not None else "directory",
            "failure_count": len(failures),
            "failures": failures,
        }
    print(json.dumps(summary, ensure_ascii=False, separators=(",", ":")))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
