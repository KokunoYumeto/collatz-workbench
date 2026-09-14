from __future__ import annotations

import argparse
from datetime import datetime, timezone
import gzip
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import tarfile
import tempfile
from urllib.parse import urlparse
from urllib.request import Request, urlopen


SHELF = Path(
    r"C:\Users\LOCAL_USER\Documents\arxiv_latex\library\collatz_reconstruction"
).resolve()
MODERN_ID_RE = re.compile(r"^\d{4}\.\d{4,5}v\d+$")
LEGACY_ID_RE = re.compile(r"^[a-z][a-z-]*/\d{7}v\d+$")
ALLOWED_DOWNLOAD_HOSTS = {"arxiv.org", "export.arxiv.org"}
MAX_BYTES = 100 * 1024 * 1024
MAX_INFLATED_BYTES = 500 * 1024 * 1024


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def strict_child(path: Path, parent: Path = SHELF) -> Path:
    resolved = path.resolve()
    if resolved == parent or parent not in resolved.parents:
        raise ValueError(f"Path must be a strict child of {parent}: {resolved}")
    return resolved


def safe_member_path(name: str) -> PurePosixPath:
    normalized = name.replace("\\", "/")
    path = PurePosixPath(normalized)
    if not normalized or path.is_absolute():
        raise ValueError(f"Unsafe archive member path: {name!r}")
    if any(part in ("", ".", "..") for part in path.parts):
        raise ValueError(f"Unsafe archive member component: {name!r}")
    if ":" in path.parts[0] or "\x00" in normalized:
        raise ValueError(f"Unsafe archive member prefix: {name!r}")
    return path


def write_json_atomic(path: Path, value: object) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    os.replace(temporary, path)


def validate_download_payload(path: Path) -> str:
    """Read the complete payload and reject unsafe or truncated archives."""
    try:
        with tarfile.open(path, mode="r:*") as archive:
            seen: set[str] = set()
            total = 0
            for member in archive.getmembers():
                member_path = safe_member_path(member.name)
                normalized = member_path.as_posix()
                if normalized in seen:
                    raise ValueError(f"Duplicate archive member path: {normalized}")
                seen.add(normalized)
                if not (member.isdir() or member.isfile()):
                    raise ValueError(
                        f"Rejected link or special archive member: {member.name} type={member.type!r}"
                    )
                if not member.isfile():
                    continue
                total += member.size
                if total > MAX_INFLATED_BYTES:
                    raise ValueError(
                        f"Archive members exceed {MAX_INFLATED_BYTES} inflated bytes"
                    )
                stream = archive.extractfile(member)
                if stream is None:
                    raise ValueError(f"Could not read archive member: {member.name}")
                with stream:
                    while stream.read(1024 * 1024):
                        pass
        return "tar"
    except tarfile.ReadError:
        with gzip.open(path, "rb") as stream:
            data = stream.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise ValueError(f"Inflated single-file source exceeds {MAX_BYTES} bytes")
        prefix = data[:65536]
        if not (
            b"\\documentclass" in prefix
            or b"\\begin{document}" in prefix
            or data.lstrip().startswith(b"%!PS")
        ):
            raise ValueError("Single-file gzip payload is neither TeX nor PostScript")
        return "single_gzip"


def valid_versioned_id(versioned_id: str) -> bool:
    return bool(
        MODERN_ID_RE.fullmatch(versioned_id)
        or LEGACY_ID_RE.fullmatch(versioned_id)
    )


def storage_id(versioned_id: str) -> str:
    """Return a path-safe, injective shelf name for a validated arXiv id."""
    if not valid_versioned_id(versioned_id):
        raise ValueError(f"A versioned arXiv identifier is required: {versioned_id!r}")
    return versioned_id.replace("/", ".")


def download(versioned_id: str, shelf_id: str, source_path: Path) -> dict:
    if source_path.exists():
        return {
            "status": "existing_source_reused",
            "request_url": None,
            "final_url": None,
            "bytes": source_path.stat().st_size,
            "sha256": sha256_file(source_path),
            "headers": {},
        }

    temp_root = strict_child(source_path.parent / ".tmp")
    temp_root.mkdir(parents=True, exist_ok=True)
    recovered: list[Path] = []
    rejected_partials: list[str] = []
    for candidate in sorted(temp_root.glob(shelf_id + "-*.part")):
        try:
            validate_download_payload(candidate)
            recovered.append(candidate)
        except Exception as error:
            rejected_partials.append(
                f"{candidate.name}: {type(error).__name__}: {error}"
            )
    if len(recovered) > 1:
        raise ValueError(
            "Multiple complete partial downloads require manual hash adjudication: "
            + ", ".join(path.name for path in recovered)
        )
    if len(recovered) == 1:
        candidate = recovered[0]
        os.replace(candidate, source_path)
        return {
            "status": "recovered_complete_partial",
            "request_url": None,
            "final_url": None,
            "bytes": source_path.stat().st_size,
            "sha256": sha256_file(source_path),
            "headers": {},
            "rejected_partials": rejected_partials,
        }
    errors: list[str] = []
    for url in (
        f"https://export.arxiv.org/e-print/{versioned_id}",
        f"https://arxiv.org/e-print/{versioned_id}",
    ):
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=shelf_id + "-", suffix=".part", dir=temp_root
        )
        os.close(descriptor)
        temporary = strict_child(Path(temporary_name))
        try:
            request = Request(
                url,
                headers={"User-Agent": "Collatz-literature-audit/1.0 (source acquisition)"},
            )
            with urlopen(request, timeout=90) as response, temporary.open("wb") as output:
                final_url = response.geturl()
                final_host = (urlparse(final_url).hostname or "").lower()
                if final_host not in ALLOWED_DOWNLOAD_HOSTS:
                    raise ValueError(f"Rejected redirect host: {final_host!r}")
                total = 0
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    total += len(chunk)
                    if total > MAX_BYTES:
                        raise ValueError(f"Source payload exceeds {MAX_BYTES} bytes")
                    output.write(chunk)
                headers = {
                    key.lower(): value
                    for key, value in response.headers.items()
                    if key.lower() in {"content-type", "content-length", "etag", "last-modified"}
                }
            if total == 0:
                raise ValueError("Downloaded source payload is empty")
            validate_download_payload(temporary)
            os.replace(temporary, source_path)
            return {
                "status": "downloaded",
                "request_url": url,
                "final_url": final_url,
                "bytes": total,
                "sha256": sha256_file(source_path),
                "headers": headers,
            }
        except Exception as error:
            errors.append(f"{url}: {type(error).__name__}: {error}")
            temporary.unlink(missing_ok=True)
    raise RuntimeError("; ".join(errors))


def file_records(root: Path) -> list[dict]:
    records: list[dict] = []
    paths = sorted(
        (path for path in root.rglob("*") if path.is_file()),
        key=lambda path: path.relative_to(root).as_posix().casefold(),
    )
    for path in paths:
        records.append(
            {
                "relative_path": path.relative_to(root).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
                "extension": path.suffix.lower(),
            }
        )
    return records


def extract_tar(source: Path, work_dir: Path) -> str:
    with tarfile.open(source, mode="r:*") as archive:
        seen: set[str] = set()
        validated: list[tuple[tarfile.TarInfo, PurePosixPath]] = []
        for member in archive.getmembers():
            member_path = safe_member_path(member.name)
            normalized = member_path.as_posix()
            if normalized in seen:
                raise ValueError(f"Duplicate archive member path: {normalized}")
            seen.add(normalized)
            if not (member.isdir() or member.isfile()):
                raise ValueError(
                    f"Rejected link or special archive member: {member.name} type={member.type!r}"
                )
            validated.append((member, member_path))

        for member, member_path in validated:
            destination = work_dir.joinpath(*member_path.parts)
            strict_child(destination)
            if member.isdir():
                destination.mkdir(parents=True, exist_ok=True)
                continue
            destination.parent.mkdir(parents=True, exist_ok=True)
            source_stream = archive.extractfile(member)
            if source_stream is None:
                raise ValueError(f"Could not open archive member: {member.name}")
            with source_stream, destination.open("xb") as output:
                shutil.copyfileobj(source_stream, output, length=1024 * 1024)
    return "tar"


def extract_single_gzip(source: Path, work_dir: Path) -> str:
    with gzip.open(source, "rb") as stream:
        data = stream.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError(f"Inflated source exceeds {MAX_BYTES} bytes")
    prefix = data[:65536]
    if b"\\documentclass" in prefix or b"\\begin{document}" in prefix:
        filename = "main.tex"
        kind = "gzip_single_tex"
    elif data.lstrip().startswith(b"%!PS"):
        filename = "main.ps"
        kind = "gzip_single_postscript"
    else:
        filename = "source.bin"
        kind = "gzip_single_unknown"
    (work_dir / filename).write_bytes(data)
    return kind


def extract(
    versioned_id: str, shelf_id: str, source_path: Path, source_sha256: str
) -> dict:
    latex_root = strict_child(SHELF / "latex")
    latex_root.mkdir(parents=True, exist_ok=True)
    final_dir = strict_child(latex_root / shelf_id)
    manifest_path = final_dir / "extraction_manifest.json"
    if final_dir.exists():
        if not manifest_path.is_file():
            raise FileExistsError(f"Existing extraction has no manifest: {final_dir}")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("source_sha256") != source_sha256 or manifest.get("status") != "pass":
            raise ValueError(f"Existing extraction does not match source: {final_dir}")
        actual = file_records(final_dir)
        actual = [row for row in actual if row["relative_path"] != "extraction_manifest.json"]
        if actual != manifest.get("files"):
            raise ValueError(f"Existing extraction file manifest mismatch: {final_dir}")
        return {
            "status": "already_extracted_verified",
            "path": str(final_dir),
            "manifest_path": str(manifest_path),
            "file_count": len(actual),
        }

    temp_root = strict_child(latex_root / ".tmp")
    temp_root.mkdir(parents=True, exist_ok=True)
    work_dir = strict_child(Path(tempfile.mkdtemp(prefix=shelf_id + "-", dir=temp_root)))
    try:
        try:
            kind = extract_tar(source_path, work_dir)
        except tarfile.ReadError:
            kind = extract_single_gzip(source_path, work_dir)
        files = file_records(work_dir)
        manifest = {
            "schema_version": "1.0",
            "versioned_arxiv_id": versioned_id,
            "source_path": str(source_path),
            "source_sha256": source_sha256,
            "extracted_at_utc": utc_now(),
            "archive_kind": kind,
            "file_count": len(files),
            "tex_related_file_count": sum(
                row["extension"] in {".tex", ".ltx", ".sty", ".cls", ".bib", ".bbl"}
                for row in files
            ),
            "status": "pass",
            "safety": {
                "path_traversal_checked": True,
                "absolute_paths_rejected": True,
                "links_and_special_members_rejected": True,
                "duplicate_member_paths_rejected": True,
            },
            "files": files,
        }
        write_json_atomic(work_dir / "extraction_manifest.json", manifest)
        os.replace(work_dir, final_dir)
        return {
            "status": "extracted",
            "path": str(final_dir),
            "manifest_path": str(final_dir / "extraction_manifest.json"),
            "file_count": len(files),
        }
    except Exception:
        failure = {
            "schema_version": "1.0",
            "versioned_arxiv_id": versioned_id,
            "source_sha256": source_sha256,
            "status": "failed_partial_kept",
            "failed_at_utc": utc_now(),
        }
        write_json_atomic(work_dir / "extraction_failure.json", failure)
        raise


def acquire(versioned_id: str) -> dict:
    if not valid_versioned_id(versioned_id):
        raise ValueError(f"A versioned arXiv identifier is required: {versioned_id!r}")
    shelf_id = storage_id(versioned_id)
    source_root = strict_child(SHELF / "source")
    source_root.mkdir(parents=True, exist_ok=True)
    source_path = strict_child(source_root / f"{shelf_id}.eprint")
    acquisition = download(versioned_id, shelf_id, source_path)
    extraction = extract(versioned_id, shelf_id, source_path, acquisition["sha256"])
    return {
        "schema_version": "1.0",
        "versioned_arxiv_id": versioned_id,
        "acquired_at_utc": utc_now(),
        "source_path": str(source_path),
        "source_bytes": acquisition["bytes"],
        "source_sha256": acquisition["sha256"],
        "download": acquisition,
        "extraction": extraction,
        "status": "pass",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", action="append", required=True, dest="ids")
    arguments = parser.parse_args()
    SHELF.mkdir(parents=True, exist_ok=True)
    records: list[dict] = []
    failures: list[dict] = []
    for versioned_id in arguments.ids:
        try:
            records.append(acquire(versioned_id))
        except Exception as error:
            failures.append(
                {
                    "versioned_arxiv_id": versioned_id,
                    "error_type": type(error).__name__,
                    "error": str(error),
                }
            )
    index_path = strict_child(SHELF / "acquisition_index.jsonl")
    existing_records: dict[str, dict] = {}
    if index_path.is_file():
        for line_number, raw_line in enumerate(
            index_path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            if not raw_line.strip():
                continue
            record = json.loads(raw_line)
            record_id = record.get("versioned_arxiv_id")
            if not isinstance(record_id, str) or not valid_versioned_id(record_id):
                raise ValueError(
                    f"Invalid versioned_arxiv_id in {index_path} line {line_number}: "
                    f"{record_id!r}"
                )
            if record_id in existing_records:
                raise ValueError(
                    f"Duplicate versioned_arxiv_id in {index_path}: {record_id}"
                )
            existing_records[record_id] = record

    for record in records:
        existing_records[record["versioned_arxiv_id"]] = record

    with index_path.with_name(index_path.name + ".tmp").open(
        "w", encoding="utf-8", newline="\n"
    ) as stream:
        for record_id in sorted(existing_records):
            record = existing_records[record_id]
            stream.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
    os.replace(index_path.with_name(index_path.name + ".tmp"), index_path)
    summary = {
        "schema_version": "1.0",
        "generated_at_utc": utc_now(),
        "shelf": str(SHELF),
        "requested_count": len(arguments.ids),
        "success_count": len(records),
        "failure_count": len(failures),
        "failures": failures,
        "status": "pass" if not failures else "fail",
    }
    write_json_atomic(strict_child(SHELF / "acquisition_summary.json"), summary)
    print(json.dumps(summary, ensure_ascii=False, separators=(",", ":")))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
