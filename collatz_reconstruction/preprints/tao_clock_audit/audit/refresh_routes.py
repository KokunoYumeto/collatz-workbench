"""Refresh only this small topic route by querying the existing canonical index."""
from datetime import datetime, timezone
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CORPUS = Path(r"C:\Users\LOCAL_USER\Documents\Papors\Chatnotes\Zeta-Function-Foundation")
route = json.loads((ROOT / "audit/topic_route.json").read_text(encoding="utf-8"))
route["queries"] = []
for query in ("almost all Collatz", "first passage"):
    now = datetime.now(timezone.utc).isoformat()
    command = [sys.executable, str(CORPUS / "scripts/query_corpus.py"),
               "--layer", "all", "--index-level", "canonical",
               "--limit-per-layer", "5", "--json", query]
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", check=True)
    data = json.loads(result.stdout)
    ids = []
    for layer in data["layers"].values():
        ids.extend(item["unit_id"] for item in layer["canonical"]["results"])
    route["queries"].append({"query": query, "layer": "all", "index_level": "canonical",
        "executed_utc": now, "reason": "Recheck exact Tao source and adjacent first-passage formulations without reindexing",
        "result_unit_ids": list(dict.fromkeys(ids))})
    print(json.dumps({"query": query, "executed_utc": now, "unit_ids": ids}))

now = datetime.now(timezone.utc).isoformat()
route["updated_utc"] = now
route["sources"] = [{
    "source_class": "research_literature",
    "publication_unit_or_source_id": "PUBUNIT-847E4E7212BFCD7A613CA573",
    "exact_locators": [r"C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/latex/1909.03562v7/collatz.tex"],
    "relevance_edge": "Tao Proposition 1.11 is the exact analytic input, with Section 3 deduction and selected Section 5-6 proof steps audited",
    "toc_or_section_check": {"status": "checked", "checked_utc": now,
        "relevant_sections": ["Section 1", "Section 3", "Section 5", "Section 6"]},
    "reading_status": "fully_content_read_for_current_dependency",
    "content_loci_read": ["Sections 1 and 3 definitions and first-passage reduction", "Proposition 5.2 endpoint and Lemma 5.3 coefficient proof", "Section 6 stopping reserve and separation calculation"],
    "dependencies": ["TAO-V7 Proposition 1.11, cited analytic input"],
    "claim_or_proof_crosswalk_ids": ["PC-01", "PC-07", "PC-08", "PC-09", "PC-10", "PC-12", "PC-13", "PC-14"],
    "notes": "The independent full Fourier-renewal proof is outside this draft's claim; source_manifest.json and audit reviews give bounded source-reading scope."
}, {
    "source_class": "research_literature",
    "publication_unit_or_source_id": "PUBUNIT-7B52CC4A159765C800B92B6B",
    "exact_locators": [r"C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/latex/1909.03562v5/collatz.tex"],
    "relevance_edge": "Version-specific half-reserve comparison, not a silently current proof manifestation",
    "toc_or_section_check": {"status": "checked", "checked_utc": now, "relevant_sections": ["Section 6"]},
    "reading_status": "fully_content_read_for_current_dependency",
    "content_loci_read": ["976-997 and 1039-1089"], "dependencies": [],
    "claim_or_proof_crosswalk_ids": ["PC-14"]
}]
route["unresolved_dependencies"] = []
route["anti_loop_note"] = "Selected proof content read and crosswalked. Cited analytic input is explicit, not silently independently certified; no priority claim or whole-corpus completeness claim."
schema = json.loads((CORPUS / "config/topic_literature_route.schema.json").read_text(encoding="utf-8"))
import jsonschema
jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker()).validate(route)
(ROOT / "audit/topic_route.json").write_text(json.dumps(route, indent=2) + "\n", encoding="utf-8")
print("TOPIC_ROUTE_SCHEMA_PASS")
