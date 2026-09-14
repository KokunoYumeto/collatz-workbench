"""Read-only verification of the bounded affine CRT checkpoint, not the corpus."""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT = ROOT / "qa/ACT46-AFFINE-CRT-CHECKPOINT.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def record_digest(row):
    return hashlib.sha256(json.dumps(row, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":")).encode()).hexdigest()


def records(name, key):
    rows = [json.loads(line) for line in (ROOT / "state" / name).read_text(
        encoding="utf-8-sig").splitlines() if line.strip()]
    pairs = [(r[key], r) for r in rows if key in r]
    if len(dict(pairs)) != len(pairs):
        raise ValueError(f"Duplicate {key}")
    return dict(pairs)


def main():
    errors = []

    def check(condition, message):
        if not condition:
            errors.append(message)

    if not __debug__:
        raise SystemExit("Optimized Python is not accepted.")
    cp = read_json(CHECKPOINT)
    forbidden = {"state/project_state.json", "state/affine_packet_current.json",
                 "state/overleaf_current.json", "state/action_receipts.jsonl",
                 "qa/ACT46-AFFINE-CRT-VALIDATION.json",
                 "qa/ACT46-FULL-STATE-VALIDATION.json", "TODO.md",
                 "qa/ACT46-AFFINE-CRT-CHECKPOINT.json"}
    for pin in cp["pins"]:
        check(pin["path"] not in forbidden, "Circular/mutable checkpoint pin")
        path = Path(pin["path"])
        if not path.is_absolute():
            path = ROOT / path
        check(path.is_file(), f"Missing pin: {pin['path']}")
        if path.is_file():
            check(path.stat().st_size == pin["bytes"], f"Size changed: {pin['path']}")
            check(digest(path) == pin["sha256"], f"Hash changed: {pin['path']}")

    claims = records("claims.jsonl", "claim_id")
    maps = records("morphisms.jsonl", "morphism_id")
    sources = records("source_registry.jsonl", "source_id")
    pools = {"claims.jsonl": claims, "morphisms.jsonl": maps,
             "source_registry.jsonl": sources}
    for pin in cp["record_pins"]:
        row = pools[pin["ledger"]].get(pin["id"])
        check(row is not None and record_digest(row) == pin["sha256"],
              f"Record changed: {pin['id']}")
    for key in cp["new_claims"]:
        check(key in claims, f"Missing claim {key}")
    for key in cp["new_morphisms"]:
        check(key in maps, f"Missing morphism {key}")
    for row in [claims[k] for k in cp["new_claims"] if k in claims] + [
            maps[k] for k in cp["new_morphisms"] if k in maps]:
        locus = row["proof_locator"]
        text = (ROOT / locus["path"]).read_text(encoding="utf-8")
        check(text.count("\\label{" + locus["label"] + "}") == 1,
              f"Unresolved/ambiguous proof label {locus['label']}")
        for dependency in row.get("dependencies", []):
            check(dependency in claims, f"Missing dependency {dependency}")
        for dependency in row.get("claim_refs", []):
            check(dependency in claims, f"Missing morphism claim {dependency}")
        for source in row.get("source_ids", row.get("source_refs", [])):
            check(source in sources, f"Missing source {source}")
    check(sources["SRC-COL-000051"]["manifestations"] == [],
          "Belaga must not acquire a fictitious local manifestation.")
    check(not sources["SRC-COL-000051"]["online_witnesses"][0]["primary_PDF_acquired"],
          "Belaga witness boundary changed; re-audit it explicitly.")

    receipt = read_json(ROOT / cp["certificate_receipt"])
    table = receipt["full_joint_table_rows_mod_13_columns_mod_499"]
    check(len(table) == 13 and all(len(row) == 499 for row in table), "Table shape")
    check(all(type(n) is int and n >= 0 for row in table for n in row), "Table coefficients")
    check(sum(map(sum, table)) == 5005, "Total word mass")
    check(sum(n > 0 for row in table for n in row) == 3473, "Joint support")
    check(table[0][0] == 0, "Joint origin")
    rows = list(map(sum, table))
    cols = [sum(table[u][v] for u in range(13)) for v in range(499)]
    check(rows == receipt["full_marginal_mod_13"], "Row marginals")
    check(cols == receipt["full_marginal_mod_499"], "Column marginals")
    check(all(rows) and all(cols) and rows[0] == 410 and cols[0] == 35, "Marginal supports/masses")
    strata = {1: 0, 13: 0, 499: 0, 6487: 0}
    for u, row in enumerate(table):
        for v, count in enumerate(row):
            strata[math.gcd(3992 * u + 2496 * v, 6487)] += count
    check(strata == {1: 4560, 13: 410, 499: 35, 6487: 0}, "GCD strata")
    compact = json.dumps(table, separators=(",", ":")).encode()
    check(hashlib.sha256(compact).hexdigest() == receipt["joint_dense_table_sha256_compact_json"],
          "Full table compact hash")
    check(digest(ROOT / "research_companion/certificates/affine_crt_synchronization_checks.py")
          == receipt["certificate_sha256"], "Executed certificate identity")

    build = read_json(ROOT / cp["build_receipt"])
    check(len(build["builds"]) == 4 and build["tao_unchanged"], "Four builds/Tao preservation")
    check(build['status'] == 'compiled_visual_review_pass', 'Build visual status')
    visual = read_json(ROOT / cp['visual_receipt'])
    check(visual['status'] == 'PASS' and not visual['material_visual_defects'], 'Visual result')
    check(visual['total_rendered_pages_inspected'] == 110, 'Visual count')
    check(build['visual_review_receipt']['sha256'] == digest(ROOT / cp['visual_receipt']),
          'Build-to-visual receipt hash')
    total_visual = 0
    stage = ROOT / cp['staging_directory']
    for path, expected in build['source_hashes'].items():
        check(digest(ROOT / path) == expected, f'Live source changed: {path}')
    for path, expected in build['canonical_after'].items():
        check((stage / path).is_file() and digest(stage / path) == expected,
              f'Staged file changed: {path}')
    manifest = read_json(stage / 'MANIFEST.json')
    manifest_paths = [row['path'] for row in manifest['files']]
    check(len(manifest_paths) == len(set(manifest_paths)), 'Duplicate manifest path')
    actual_paths = {p.relative_to(stage).as_posix() for p in stage.rglob('*') if p.is_file()}
    check(set(manifest_paths) | {'MANIFEST.json'} == actual_paths, 'Manifest inventory')
    for row in manifest['files']:
        path = stage / row['path']
        check(path.is_file() and path.stat().st_size == row['bytes']
              and digest(path) == row['sha256'], f'Manifest mismatch: {row["path"]}')
    for item in build["builds"]:
        check(len(item["passes"]) == 3 and all(
            p["returncode"] == 0 and p["termination_reason"] is None
            and p["process_tree_clear"] for p in item["passes"]), "Build pass failure")
        check(not item["undefined_reference_errors"], "Unresolved TeX reference")
        check(digest(Path(item["pdf"])) == item["pdf_sha256"], "Built PDF hash")
        check(digest(Path(item['build_pdf'])) == item['pdf_sha256'], 'Build-copy PDF hash')
        expected_pages = (list(range(1,22)) + list(range(40,54))
                          if 'companion' in item['name'] else [1,2,3] + list(range(167,184)))
        reviewed = visual['coverage'][item['name']]
        check(reviewed['visually_inspected_pages'] == expected_pages,
              f'Exact visual scope: {item["name"]}')
        check(reviewed['pdf_sha256'] == item['pdf_sha256'] and reviewed['total_pages'] == item['pages'],
              'Visual PDF identity')
        check(item['visual_review'] == reviewed and reviewed['status'] == 'PASS'
              and not reviewed['material_visual_defects'], 'Build visual linkage')
        needed = set(item['prefix_comparison']['different_pages'])
        lo, hi = item['changed_chapter_page_range']
        needed.update(range(lo, hi+1))
        check(needed <= set(expected_pages), 'Changed or reflowed pages omitted')
        check([r['page'] for r in item['rendered_pages']] == expected_pages, 'Render coverage')
        for rendered in item['rendered_pages']:
            path = Path(rendered['path'])
            check(path.is_file() and digest(path) == rendered['sha256'], 'Rendered page hash')
        total_visual += len(expected_pages)
        for p in item['passes']:
            check(p['cap_bytes'] == 5_000_000_000 and p['timeout_seconds'] == 180
                  and p['peak_aggregate_rss_bytes'] < p['cap_bytes']
                  and p['peak_aggregate_private_bytes'] < p['cap_bytes'], 'Build resource cap')
    check(total_visual == 110, 'Summed visual coverage')
    remote = read_json(ROOT / cp["remote_receipt"])
    check(remote["project_id"] == "6a91f06e408dd545780c660f", "Wrong remote project")
    check(remote["status"] == "eight_files_uploaded_both_roots_remote_compiled", "Remote sync incomplete")
    check(not remote["pending_metadata"], "Metadata upload incomplete")
    check(remote['local_build_receipt_sha256'] == digest(ROOT / cp['build_receipt'])
          and remote['visual_review_sha256'] == digest(ROOT / cp['visual_receipt']),
          'Remote receipt local linkage')
    check(len(remote['uploaded']) == 8 and {r['path'] for r in remote['uploaded']}
          == set(build['changed_canonical_paths']), 'Eight upload paths')
    for row in remote['uploaded']:
        check(digest(stage / row['path']) == row['local_uploaded_sha256'], 'Uploaded local identity')
    check(remote['remote_download_sha256'] is None, 'Do not imply remote byte download verification')
    for entry, pages in [("main.tex", 183), ("research_companion.tex", 53)]:
        check(remote["builds"][entry]["pages"] == pages
              and remote["builds"][entry]["errors"] == 0, f"Remote build {entry}")
    check(not cp["whole_corpus_complete"] and not cp["whole_raw_affine_coverage_reconciled"],
          "Bounded checkpoint must not assert global/source completion")
    result = {"id": "AFFINE-CRT-CHECKPOINT-VALIDATION-20260904",
              "status": "pass" if not errors else "fail",
              "checkpoint_sha256": digest(CHECKPOINT), "pin_count": len(cp["pins"]),
              "new_claim_count": len(cp["new_claims"]), "new_morphism_count": len(cp["new_morphisms"]),
              "table_cells_rechecked": 6487, "errors": errors,
              "visual_pages_hash_checked": total_visual,
              "scope": "Bounded checkpoint pins, source/proof linkage, stored table, build and remote receipts.",
              "nonclaims": ["Does not rerun enumeration or prove the general theorems mechanically.",
                            "Does not replace full state validation or fresh-context reading.",
                            "Does not certify whole-corpus coverage or unbundled private apparatus."]}
    print(json.dumps(result, indent=2))
    return bool(errors)


if __name__ == "__main__":
    sys.exit(main())
