"""Bounded PDF manifestation comparison; no mathematical equivalence inference.

Read only the three exact source manifestations.  Extract native PDF text,
remove only each verified final page-number line, locate explicit statement
boundaries, and compare whitespace-delimited tokens.  Preserve every remaining
token difference in the receipt.  This is a textual collation, not a proof
checker, TeX build, OCR operation, or global-source audit.
"""

from pathlib import Path
import bisect
import difflib
import hashlib
import json
import sys

import fitz


ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).with_suffix(".json")
SOURCES = {
    "A_controlling_pdf": (
        ROOT / "ES-Fable-C123-support/external_sources/combined_live_theorem_package_dependencies/odd_step_collatz_orbit_packets_note.pdf",
        "13f49961a60b870fa7a6f0f646758b4d72c1a4e4267f347606cc8a3238d552f1",
    ),
    "B_indexed_tex": (
        Path(r"C:\Users\LOCAL_USER\Documents\Papors\Chatnotes\automata\V5\odd_step_collatz_orbit_packets_note.tex"),
        "406ef13e43ae0af68fabdbda4dd16145d313407f7d38ea22311803c7533cfec7",
    ),
    "C_indexed_pdf": (
        Path(r"C:\Users\LOCAL_USER\Documents\Papors\Chatnotes\automata\V5\odd_step_collatz_orbit_packets_note.pdf"),
        "878d3ddbb3fefc0c781aa7ca0cd6536dcd7b5d7a46df18ecdb3662eee47d3ab1",
    ),
}
BLOCKS = [
    ("affine_path_and_recurrence", "Theorem 2.1 (", "Corollary 2.3 (", [141, 268]),
    ("translation_intertwiner_and_groupoid", "Theorem 3.1 (", "Remark 3.3.", [452, 520]),
    ("abel_coordinate", "Theorem 4.2 (", "Remark 4.3.", [699, 736]),
    ("abel_transport", "Theorem 4.4 (", "4.2\n3-adic", [742, 781]),
    ("concentration", "Corollary 6.5 (", "6.3\nExact packet", [1154, 1166]),
    ("extremizer_multiplicity", "Corollary 6.7 (", "6.4\n", [1208, 1223]),
    ("packet_average", "Theorem 6.10 (", "Definition 6.11 (", [1307, 1461]),
    ("cyclic_transport", "Theorem 10.1 (", "Definition 10.2.", [2359, 2419]),
    ("primitive_necklace_classification", "Theorem 10.3 (", "Corollary 10.4 (", [2434, 2481]),
    ("burnside", "Theorem 11.1 (", "Theorem 11.2 (", [2558, 2605]),
    ("primitive_count", "Theorem 11.2 (", "Corollary 11.3 (", [2607, 2628]),
    ("hamiltonian_and_trace", "8.1 One-letter", "8.2 Special", [3647, 3677]),
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    identities, pdf_text, offsets = {}, {}, {}
    for key, (path, expected) in SOURCES.items():
        data = path.read_bytes()
        actual = sha(data)
        if actual != expected:
            raise RuntimeError(f"Source changed: {key}: {actual}")
        info = {"path": str(path), "bytes": len(data), "sha256": actual}
        if path.suffix == ".pdf":
            with fitz.open(path) as doc:
                info.update(pages=len(doc), metadata=doc.metadata)
                native_pages = [page.get_text() for page in doc]
                info["native_text_sha256"] = sha("".join(native_pages).encode())
                parts, starts = [], []
                length = 0
                for i, native in enumerate(native_pages):
                    lines = native.splitlines()
                    if lines[-1] != str(i + 1):
                        raise RuntimeError(f"Unexpected PDF footer {key} page {i+1}")
                    part = "\n".join(lines[:-1])
                    starts.append(length)
                    parts.append(part)
                    length += len(part) + 1
                pdf_text[key] = "\n".join(parts)
                offsets[key] = starts
        else:
            info["physical_lines"] = len(data.decode("utf-8").splitlines())
        identities[key] = info
    records = []
    for block_id, start, end, tex_lines in BLOCKS:
        chunks, record = [], {"id": block_id, "tex_lines": tex_lines}
        for key in ("A_controlling_pdf", "C_indexed_pdf"):
            text = pdf_text[key]
            if text.count(start) != 1:
                raise RuntimeError(f"Nonunique start {key}: {start}")
            lo = text.index(start)
            hi = text.index(end, lo)
            chunk = text[lo:hi]
            chunks.append(chunk.split())
            record[key] = {
                "physical_pages": [bisect.bisect_right(offsets[key], lo), bisect.bisect_right(offsets[key], hi-1)],
                "text_characters": len(chunk),
                "text_sha256": sha(chunk.encode()),
                "whitespace_token_count": len(chunks[-1]),
            }
        diffs = []
        matcher = difflib.SequenceMatcher(None, chunks[0], chunks[1], autojunk=False)
        for tag, a, b, c, d in matcher.get_opcodes():
            if tag != "equal":
                diffs.append({"operation": tag, "A_tokens": chunks[0][a:b], "C_tokens": chunks[1][c:d]})
        record["all_token_differences"] = diffs
        records.append(record)
    receipt = {
        "audit_id": "AUD-COL-AFFINE-VERSION-20260904-0001",
        "scope": "Twelve exact statement/proof blocks, not whole-note mathematical equivalence or correctness",
        "index_unit": "PUBUNIT-CF4FD708E6C6DE523385FD85",
        "comparison_method": "Verified final page-number lines omitted; remaining text split on whitespace only. No equation, sign, number, reference, or substantive token suppressed.",
        "pairing_status": "TeX/PDF correspondence inspected manually at listed loci; no producing build manifest available, no byte-production claim",
        "identities": identities,
        "blocks": records,
        "pdf_pages_with_native_passages_read_not_full_page_coverage": {"A": [1,2,3,4,5,8,9,11,12,18,19,20,21,22,23,35,36,37,38,39,40,55], "C": [1,2,3,4,5,6,7,9,10,12,13,19,20,21,22,23,24,36,37,38,39,40,41,56]},
        "pdf_pages_visually_checked": {"A": [11,18,19,21,36,37,55], "C": [12,13,19,20,22,37,38,56]},
        "untested": "Remaining mathematics; complete bibliography accuracy; source authorship chronology; generating source/build environment of either PDF; no novelty or proof certificate",
    }
    OUT.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(OUT), "sha256": sha(OUT.read_bytes()), "blocks": len(records), "difference_hunks": sum(len(r["all_token_differences"]) for r in records)}, indent=2))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
