import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const stateDir = path.join(root, "state");
const auditPath =
  "qa/TAO-V5-V7-JOURNAL-F028-whole-version-citation-audit.md";
const certificatePath = "certificates/tao_whole_version_checks.py";
const auditBytes = 17255;
const auditSha =
  "bf00a90d3acd819435a7ef2da0ebeae032d752b8c921c1f97ff23ddff2a0b095";
const certificateBytes = 12614;
const certificateSha =
  "c13f10f397c3abcd562a99702705b6e6a6d76731b78d2fe0aeb0a0a36f54d26f";
const updatedUtc = "2026-08-28T13:30:44.0448013Z";

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function sha256(pathname) {
  const crypto = awaitImportCrypto();
  return crypto
    .createHash("sha256")
    .update(fs.readFileSync(pathname))
    .digest("hex");
}

let cryptoModule;
function awaitImportCrypto() {
  if (!cryptoModule) {
    throw new Error("crypto module not initialised");
  }
  return cryptoModule;
}

async function initialiseCrypto() {
  cryptoModule = await import("node:crypto");
}

function readJson(pathname) {
  return JSON.parse(fs.readFileSync(pathname, "utf8"));
}

function writeJson(pathname, value) {
  fs.writeFileSync(pathname, JSON.stringify(value, null, 2) + "\n", "utf8");
}

function readJsonl(pathname) {
  return fs
    .readFileSync(pathname, "utf8")
    .split(/\r?\n/)
    .filter((line) => line.length > 0)
    .map((line) => JSON.parse(line));
}

function writeJsonl(pathname, records) {
  fs.writeFileSync(
    pathname,
    records.map((record) => JSON.stringify(record)).join("\n") + "\n",
    "utf8",
  );
}

function appendUnique(array, value) {
  if (!array.includes(value)) array.push(value);
}

function appendObjectUnique(array, key, value) {
  const index = array.findIndex((item) => item[key] === value[key]);
  if (index === -1) array.push(value);
  else array[index] = value;
}

await initialiseCrypto();
assert(
  fs.statSync(path.join(root, auditPath)).size === auditBytes,
  "F028 byte count changed; update the propagation pins",
);
assert(
  sha256(path.join(root, auditPath)) === auditSha,
  "F028 hash changed; update the propagation pins",
);
assert(
  fs.statSync(path.join(root, certificatePath)).size === certificateBytes,
  "whole-version certificate byte count changed; update the propagation pins",
);
assert(
  sha256(path.join(root, certificatePath)) === certificateSha,
  "whole-version certificate hash changed; update the propagation pins",
);

const substantiveHunks = [
  { hunk: 14, v5: "326", v7: "326", journal: "p.8 Proposition 1.11 opening", journal_class: "v7", classification: "Proposition 1.11 domain and nonempty-set qualification" },
  { hunk: 15, v5: "334", v7: "334", journal: "p.8 after (1.20)", journal_class: "v7", classification: "absolute implied constants" },
  { hunk: 17, v5: "344", v7: "344-346", journal: "p.9 equation (1.21)", journal_class: "v7", classification: "syr-forward label" },
  { hunk: 19, v5: "364-365", v7: "366-369", journal: "p.9 Lemma 1.12 proof and (1.24)", journal_class: "v7", classification: "explicit reversal relabelling and fn-recurse label" },
  { hunk: 21, v5: "381", v7: "385-387", journal: "p.10 Remark 1.13 and (1.25)", journal_class: "v7", classification: "syr3 label" },
  { hunk: 22, v5: "387", v7: "393", journal: "p.10 below (1.25), footnote 4", journal_class: "v7", classification: "reversal dependency and ancient-iteration footnote" },
  { hunk: 25, v5: "422", v7: "428", journal: "p.11 after Proposition 1.17/(1.28)", journal_class: "v7", classification: "uniform n and unit-frequency domain" },
  { hunk: 26, v5: "430", v7: "436", journal: "p.12 before (1.29)", journal_class: "v7", classification: "fn-recurse cross-reference" },
  { hunk: 27, v5: "434", v7: "440", journal: "p.12 after (1.29)", journal_class: "v7", classification: "syr3 derivation and full random-variable name" },
  { hunk: 28, v5: "440", v7: "446", journal: "p.55 acknowledgments/funding", journal_class: "v5", classification: "Lech Mazur acknowledgment added only in v7" },
  { hunk: 43, v5: "789", v7: "795", journal: "p.23 converse bullet first concluding display", journal_class: "v5", classification: "passage-time symbol repair" },
  { hunk: 44, v5: "791", v7: "797", journal: "p.23 following display", journal_class: "v5", classification: "passage-location symbol repair" },
  { hunk: 57, v5: "983", v7: "989", journal: "p.28 equation (6.7)", journal_class: "v5", classification: "one-half to 0.99 Section 6 reserve" },
  { hunk: 58, v5: "991", v7: "997", journal: "p.29 equation (6.8)", journal_class: "v5", classification: "reserve propagated to l-window" },
  { hunk: 63, v5: "1029", v7: "1035", journal: "p.30 equation (6.11)", journal_class: "v7", classification: "complemented E_k corrected to E_k" },
  { hunk: 64, v5: "1070", v7: "1076", journal: "p.31 after (6.14)", journal_class: "v5", classification: "sufficiently-small epsilon changed to suitable choice" },
  { hunk: 66, v5: "1074-1076", v7: "1080-1082", journal: "p.31 three-line bound before (6.15)", journal_class: "v5", classification: "Section 6 exponent chain repaired" },
  { hunk: 67, v5: "1078", v7: "1084", journal: "p.31 before (6.15)", journal_class: "v5", classification: "exact numerical margin supplied" },
  { hunk: 94, v5: "1656", v7: "1662", journal: "p.49 Lemma 7.9 equation (7.57)", journal_class: "v5", classification: "Lemma 7.9 restricted to R<=r" },
  { hunk: 95, v5: "1661", v7: "1667", journal: "p.49 after (7.57)", journal_class: "v5", classification: "missing parenthesis repair" },
  { hunk: 96, v5: "1668-1670", v7: "1674-1675", journal: "p.49 after (7.58)", journal_class: "v5", classification: "r=0 branch removed after restriction" },
  { hunk: 97, v5: "1676", v7: "1681", journal: "p.49 Z((j',l'),R) display", journal_class: "v5", classification: "P(r=0) term removed" },
  { hunk: 104, v5: "1753", v7: "1758-1760", journal: "p.51 equation (7.65)", journal_class: "v7", classification: "jjd label" },
  { hunk: 105, v5: "1772", v7: "1779", journal: "p.52 below (7.66)", journal_class: "v7", classification: "exact equation references" },
  { hunk: 106, v5: "after 1774", v7: "1782", journal: "p.52 middle line of following display", journal_class: "v7", classification: "missing algebraic substitution inserted" },
  { hunk: 110, v5: "1821-1827", v7: "1829-1838", journal: "p.54 Lemma 7.9 application through (7.67)", journal_class: "hybrid", classification: "v5 expectation and conclusion with v7 explicit F_* definition" },
  { hunk: 112, v5: "1838", v7: "1849", journal: "p.54 below (7.68)", journal_class: "v7", classification: "explicit contradiction hypothesis" },
  { hunk: 113, v5: "1840", v7: "1851", journal: "p.54 final paragraph", journal_class: "v7", classification: "incorrect 1+p^3 event name conflicts with defined (1+p)^3 event" },
];
assert(substantiveHunks.length === 28, "substantive hunk matrix must have 28 rows");

const wholeVersionReconciliation = {
  status: "complete_source_to_source_and_page_read_journal_classification",
  audit_record: auditPath,
  audit_bytes: auditBytes,
  audit_sha256: auditSha,
  terminal_boundary: {
    v7_line_count: 1956,
    v7_proof_end_line: 1859,
    v7_line_1860_blank: true,
    v7_bibliography_lines: "1863-1952",
    v7_document_end_line: 1956,
    post_v7_1860_mathematical_lines: 0,
    v5_line_count: 1945,
    v5_proof_end_line: 1848,
    v5_bibliography_lines: "1852-1941",
    v5_document_end_line: 1945,
    journal_terminal_pages: "55-56",
  },
  raw_diff: { hunks: 124, additions: 147, deletions: 136 },
  substantive_diff: { hunks: 28, additions: 49, deletions: 38 },
  whitespace_only_hunks: 96,
  whitespace_deleted_whole_files: {
    exactly_equal: false,
    v5_length: 138900,
    v5_sha256:
      "9f5d7629cc54e2f8660df82d2787ca256dacae145c905cad705e1dacbbb1375f",
    v7_length: 140369,
    v7_sha256:
      "ca759f46014aaafab75e643e8ba13ee3befd5decb3e2f095c4ee712ab9193693",
  },
  exact_bibliography_comparison: {
    lines_each: 90,
    whitespace_deleted_characters_each: 3600,
    exactly_equal_after_whitespace_deletion: true,
    complete_source_identity_inferred: false,
  },
  journal_matrix: {
    v7_like_hunks: 15,
    v5_like_hunks: 12,
    hybrid_hunks: 1,
    invisible_hunks: 0,
    whole_manifestation_identified_with_version: false,
  },
  substantive_hunks: substantiveHunks,
};

const citationInventory = {
  active_citation_calls: 25,
  unique_cited_keys: 23,
  active_bibliography_items: 24,
  unresolved_cited_keys: [],
  active_uncited_keys: ["terras2"],
  proof_body_logical_citation_dependencies: 0,
  already_content_read_keys: ["crandall", "everett", "lag"],
  cited_but_not_in_source_registry_keys: [
    "allouche",
    "baker",
    "barina",
    "bourgain",
    "carletti",
    "chamber",
    "korec",
    "kont",
    "km",
    "ks",
    "kl",
    "ls",
    "lw",
    "olive",
    "eric",
    "sinai",
    "tao:chowla",
    "terras",
    "thomas",
    "wirsch",
  ],
  route_result:
    "frozen_route_and_exact_filename_miss_only_not_a_nonexistence_claim",
  priority: [
    "terras",
    "allouche",
    "korec",
    "kl",
    "barina",
    "eric",
    "olive",
    "sinai",
    "carletti",
    "wirsch",
    "thomas",
    "lw",
    "kont",
    "km",
    "ls",
    "ks",
    "chamber",
    "tao:chowla",
    "bourgain",
    "baker",
    "terras2",
  ],
};

const wholeVersionCertificate = {
  path: certificatePath,
  bytes: certificateBytes,
  sha256: certificateSha,
  status: "pass_finite_exact_source_bibliography_citation_and_margin_scope",
  metrics: {
    pinned_hashes: 6,
    raw_zero_context_hunks: 124,
    whitespace_only_hunks: 96,
    substantive_hunks: 28,
    substantive_source_signature_checks: 34,
    citation_calls: 25,
    unique_cited_keys: 23,
    active_bibliography_items: 24,
    unresolved_citation_keys: 0,
    post_v7_1860_mathematical_lines: 0,
    journal_pdf_pages: 56,
    explicit_sufficient_CA_for_point99_overshoot_only: 600,
  },
  explicitly_not_certified_by_script: [
    "page-read journal hunk matrix",
    "explicit asymptotic v5 counterexample family",
    "analytic characteristic-function decay",
    "implicit O(C_A log n) source constant",
    "Tao main theorem",
    "Collatz conjecture",
  ],
};

const sourcesPath = path.join(stateDir, "source_registry.jsonl");
const sources = readJsonl(sourcesPath);
const sourceHeader = sources[0];
assert(sourceHeader.next_id === "SRC-COL-000028", "unexpected source next_id");
const src005 = sources.find((item) => item.source_id === "SRC-COL-000005");
const src027 = sources.find((item) => item.source_id === "SRC-COL-000027");
assert(src005 && src027, "Tao source records missing");

src005.reading.status =
  "complete_v7_mathematical_text_through_line1859_and_complete_v5_v7_whole_source_comparison_with_journal_hunk_classification_Section6_margin_repaired_at_exact_local_scope_cited_source_intake_whole_paper_adversarial_formal_package_QA_and_recovery_gates_open";
for (const locator of [
  "v7 proof ends at source line 1859; line 1860 is blank; bibliography lines 1863-1952; document end line 1956",
  "complete v5/v7 whole-source comparison: 124 raw hunks and 28 non-whitespace hunks",
  "published journal all-28-hunk matrix plus terminal physical pages 55-56",
  auditPath,
  certificatePath,
  "tex/chapters/01g_tao_fourier_renewal.tex Proposition prop:Tao-Section6-reserve-repair",
]) {
  appendUnique(src005.reading.locators, locator);
}
src005.reading.whole_version_reconciliation = wholeVersionReconciliation;
src005.reading.citation_inventory = citationInventory;
appendUnique(
  src005.reading.source_defects,
  "V5 lines 983, 991, and 1074-1078 and journal pp. 28-31 retain a half-window whose exponentiated reserve (log 2)/2 is below the optimized cost log^2(2)/(4 log(4/3)); v5 also drops log 2 in the displayed exponential. The printed Archimedean size assertion fails on an explicit concentration-admissible family.",
);
appendUnique(
  src005.reading.source_defects,
  "V5 line 1029 prints 1_{overline E_k} although the factorized Fourier coefficient and following Plancherel line require 1_{E_k}; v7 line 1035 and journal equation (6.11) give the exact repair.",
);
appendUnique(
  src005.reading.source_defects,
  "V7 line 1851 and journal p. 54 invoke E_{p,4^A(1+p^3)}, while E_* is defined and the following inequality is used with E_{p,4^A(1+p)^3}; no identity between those parameters is admitted.",
);
src005.reading.dependency_boundaries = src005.reading.dependency_boundaries.filter(
  (item) => !item.includes("remaining Tao gates are post-line-1860"),
);
appendUnique(
  src005.reading.dependency_boundaries,
  "The v7 mathematical text ends at line 1859 and the complete v5/v7 source comparison and journal hunk matrix are closed in F028. Remaining Tao gates are content-level cited-source intake, consolidated whole-paper adversarial release audit, formal/package validation, visual QA, and fresh-context recovery.",
);
appendUnique(
  src005.reading.nonclaims,
  "The v5 Section 6 Archimedean size assertion fails on an explicit admissible family; this does not exhibit colliding tuples or prove the separation corollary false by every method.",
);
appendUnique(
  src005.reading.nonclaims,
  "The Section 6 threshold log(2)/(4 log(4/3)) belongs to the exact displayed optimization-and-absorption argument; 0.99 is convenient rather than canonical.",
);
src005.reading.whole_version_certificate = wholeVersionCertificate;
src005.reading.whole_version_adversarial_audit = {
  status:
    "complete_source_diff_and_page_read_journal_matrix_with_exact_Section6_local_repair",
  audit_record: auditPath,
  audit_bytes: auditBytes,
  audit_sha256: auditSha,
  final_tex_path: "tex/chapters/01g_tao_fourier_renewal.tex",
  final_tex_status: "edited_in_ACT33_rebuild_and_visual_QA_pending",
};

src027.bibliographic_identity.journal_relation =
  "the 2022 Forum of Mathematics Pi manifestation is classified hunk-by-hunk as 15 v7-like, 12 v5-like, and one hybrid across all 28 substantive v5-v7 source differences; no whole-text identity with either arXiv version is inferred";
src027.reading.status =
  "complete_whole_source_comparison_against_v7_all_28_substantive_hunks_and_journal_manifestation_classified_v5_Section6_and_Lemma7_9_proof_defects_retained_v7_controlling";
for (const locator of [
  "complete v5 source lines 1-1945 compared against complete v7 source lines 1-1956",
  "published journal all-28-hunk matrix and physical pages 55-56 terminal boundary",
  auditPath,
  certificatePath,
]) {
  appendUnique(src027.reading.locators, locator);
}
src027.reading.dependency_boundaries = src027.reading.dependency_boundaries.filter(
  (item) =>
    !item.includes("Only the targeted comparison intervals") &&
    !item.includes("Agreement of the journal display with v5"),
);
appendUnique(
  src027.reading.dependency_boundaries,
  "The complete v5/v7 source comparison is admitted under SRC-COL-000005.reading.whole_version_reconciliation. The published journal remains a distinct mixed manifestation and is not text-identified with either arXiv version.",
);
src027.reading.whole_version_comparison_ref = {
  source_id: "SRC-COL-000005",
  field: "reading.whole_version_reconciliation",
  audit_record: auditPath,
};
src027.reading.section_6_manifestation_defects = [
  {
    locators: ["v5 lines 983, 991, 1074-1078", "journal pp. 28-31"],
    class: "insufficient_exponential_reserve_and_dropped_log_two",
    exact_boundary:
      "v5 contributes (log 2)/2=0.3465735903... below log^2(2)/(4 log(4/3))=0.4175208154...; an explicit admissible family refutes the printed universal size assertion",
    nonclaim:
      "no tuple collision is exhibited and the standalone corollary is not disproved by every method",
  },
  {
    locators: ["v5 line 1029", "v7 line 1035", "journal equation (6.11)"],
    class: "complemented_event_substitution",
    exact_repair:
      "1_{E_k intersect B_k intersect C_{k,l}} replaces unsupported 1_{overline E_k intersect B_k intersect C_{k,l}}",
  },
];
src027.reading.whole_version_certificate_ref = wholeVersionCertificate;
writeJsonl(sourcesPath, sources);

const claimsPath = path.join(stateDir, "claims.jsonl");
const claims = readJsonl(claimsPath);
const claimsHeader = claims[0];
assert(
  claimsHeader.next_id === "CLM-COL-000122" ||
    claimsHeader.next_id === "CLM-COL-000123",
  "unexpected claim next_id",
);
const clm114 = claims.find((item) => item.claim_id === "CLM-COL-000114");
assert(clm114, "CLM-COL-000114 missing");
appendUnique(clm114.dependencies, "CLM-COL-000122");
appendUnique(clm114.source_locators, auditPath);
appendUnique(
  clm114.nonclaims,
  "The v5/journal half-window argument is not used; CLM-COL-000122 supplies the exact v7 reserve boundary and retains the no-collision and no-main-theorem nonclaims.",
);
let clm122 = claims.find((item) => item.claim_id === "CLM-COL-000122");
if (!clm122) {
  clm122 = {
    record_type: "claim",
    schema_version: "1.0",
    claim_id: "CLM-COL-000122",
    claim_type: "source_version_proof_defect_with_exact_local_repair",
    status: "proved_at_exact_local_Section6_margin_and_event_scope",
    statement:
      "For a=log(4/3), b=log 2, positive prefix coordinates satisfying a_[1,j]>=2j-C_A(sqrt(j log n)+log n), and l<=n log(3)/b-rho C_A^2 log n, completing the square gives fluctuation cost b^2 C_A^2 log n/(4a), so the Archimedean separation sum is below 3^n whenever rho>b/(4a) after the stated order of choices. The v5 value rho=1/2 is below this threshold and an explicit all-interval-concentration-admissible family makes one printed summand exceed 3^n. On E_k intersect B_k, the stopping overshoot is at most 6 C_A log n, hence at most 0.01 C_A^2 log n for C_A>=600, supplying the v7 rho=0.99 window. The factorized collision mass requires E_k, not its complement.",
    source_ids: ["SRC-COL-000005", "SRC-COL-000027"],
    dependencies: [],
    source_locators: [
      "Tao arXiv:1909.03562v5 source lines 983, 991, 1029, and 1070-1078",
      "Tao arXiv:1909.03562v7 source lines 989, 997, 1035, and 1076-1084",
      "published journal physical pages 28-31",
      auditPath,
    ],
    proof_locator: {
      path: "tex/chapters/01g_tao_fourier_renewal.tex",
      label: "prop:Tao-Section6-reserve-repair",
    },
    audit_locator: auditPath,
    formal_status: {
      status:
        "finite_exact_source_and_rational_margin_certificate_pass_asymptotic_counterexample_proved_in_TeX_not_certified_by_script",
      artifact: certificatePath,
      artifact_bytes: certificateBytes,
      artifact_sha256: certificateSha,
      verified_finite_metrics: wholeVersionCertificate.metrics,
      explicitly_not_certified_by_script:
        wholeVersionCertificate.explicitly_not_certified_by_script,
    },
    open_obligation_ids: ["PO-COL-000001"],
    nonclaims: [
      "The v5 printed size assertion fails, but no pair of colliding tuples is constructed and the standalone corollary is not disproved by every method.",
      "The coefficient 0.99 is convenient rather than canonical.",
      "The threshold log(2)/(4 log(4/3)) belongs to this exact optimization-and-absorption argument.",
      "No analytic Fourier-decay estimate, Tao main theorem, Collatz conjecture, natural-density result, or fixed orbit bound is certified by this claim.",
    ],
  };
  claims.push(clm122);
}
claimsHeader.next_id = "CLM-COL-000123";
writeJsonl(claimsPath, claims);

const obligationsPath = path.join(stateDir, "proof_obligations.jsonl");
const obligations = readJsonl(obligationsPath);
assert(
  obligations.filter((item) => item.record_type === "proof_obligation").length ===
    8,
  "all eight obligations must remain present",
);
const po1 = obligations.find((item) => item.obligation_id === "PO-COL-000001");
assert(po1, "PO-COL-000001 missing");
po1.status =
  "in_progress_after_complete_whole_version_reconciliation_and_citation_inventory_remaining_cited_literature_whole_paper_adversarial_formal_package_QA_and_release_recovery_gates_open";
po1.statement =
  "Complete the remaining whole-paper proof-dependency and release certification of Tao arXiv v7. The v7 mathematical proof ends at line 1859; line 1860 is blank and no mathematical content follows it. All 28 substantive v5/v7 source hunks and the journal's 15-v7/12-v5/one-hybrid manifestation matrix are classified. The exact Section 6 reserve and E_k repairs are proved, and the finite F028 source/citation/margin certificate passes. Proposition 5.2, Propositions 1.14, 1.9, 1.11, repaired Theorem 3.1, Theorem 1.6, and Theorem 1.3 remain closed at their declared scopes. Content-level intake of the claim-driving cited literature, consolidated whole-paper adversarial release audit, remaining formal/certificate coverage, package validation, final visual QA, and fresh-context release recovery remain open.";
appendUnique(po1.claim_refs, "CLM-COL-000122");
appendObjectUnique(po1.surviving_defects, "class", {
  locators: ["v5 lines 983, 991, 1074-1078", "journal pp. 28-31"],
  class: "v5_journal_Section6_half_window_proof_failure",
  summary:
    "The exponentiated half-window reserve is below the optimized square-root cost and v5 drops log 2; an explicit admissible family refutes the printed universal size assertion without producing a collision.",
});
appendObjectUnique(po1.surviving_defects, "class", {
  locators: ["v5 line 1029", "v7 line 1035", "journal equation (6.11)"],
  class: "v5_complemented_Ek_error_repaired",
  summary:
    "The factorized Fourier coefficient requires E_k, not its complement; v7 and the journal carry the exact event.",
});
appendObjectUnique(po1.surviving_defects, "class", {
  locators: ["v7 line 1851", "journal pp. 53-54"],
  class: "final_event_parameter_mismatch",
  summary:
    "The final invocation uses 1+p^3 although E_* and the next inequality use (1+p)^3; no identity is admitted.",
});
po1.required_checks = po1.required_checks.map((item) =>
  item.startsWith("Content-read and classify every remaining mathematical passage")
    ? "Content-read the claim-driving cited literature absent from the local source registry, beginning with Terras, Allouche, Korec, and Krasikov-Lagarias; preserve exact source conventions, theorem thresholds, proof dependencies, defects, computation boundaries, and nonclaims."
    : item,
);
po1.closure_rule =
  "Close only after every surviving source defect has exact source and audit locators, the claim-driving cited literature is content-read and crosswalked, version provenance remains explicit, every consequence is propagated, and consolidated adversarial audit, deterministic/formal checks, portable package rebuild, final visual QA, and fresh-context recovery pass. F024 through F028 are closed at their declared scopes; all eight project obligations remain open.";
for (const item of [
  "verified that v7's proof ends at line 1859, line 1860 is blank, and the remaining source tail is bibliography and document closure with zero post-line-1860 mathematical lines",
  "compared the complete v5 and v7 source files: 124 raw hunks, 28 substantive hunks, and 96 whitespace-only hunks",
  "classified every substantive hunk against the journal as 15 v7-like, 12 v5-like, and one hybrid without identifying the journal with either source version",
  "proved the exact Section 6 reserve threshold, explicit v5 size-assertion counterexample family, v7 0.99 stopping window, and forced E_k event repair under CLM-COL-000122",
  "inventoried 25 active citation calls, 23 unique cited keys, 24 bibliography items, zero unresolved keys, one uncited active item, and zero proof-body logical citation dependencies",
  "passed certificates/tao_whole_version_checks.py at its finite exact source, bibliography, citation, and rational-margin scope with explicit analytic and journal-page noncertification",
]) {
  appendUnique(po1.completed_checks, item);
}
po1.local_checkpoint.status =
  "pass_complete_whole_version_reconciliation_and_Section6_local_repair_remaining_cited_literature_and_release_gates_open";
appendUnique(po1.local_checkpoint.claim_refs, "CLM-COL-000122");
appendObjectUnique(po1.local_checkpoint.certificates, "path", {
  path: certificatePath,
  sha256: certificateSha,
  status: "pass_finite_exact_source_bibliography_citation_and_margin_scope",
});
appendUnique(
  po1.local_checkpoint.proof_locators,
  "tex/chapters/01g_tao_fourier_renewal.tex#prop:Tao-Section6-reserve-repair",
);
po1.local_checkpoint.source_dependency_limit =
  "arXiv:1909.03562v7 complete mathematical text through proof end line 1859 plus complete v5/v7 source comparison and published-journal 28-hunk matrix; claim-driving cited-source intake and release gates remain open";
po1.local_checkpoint.full_obligation_closed = false;
appendUnique(po1.audit_records, auditPath);
writeJsonl(obligationsPath, obligations);

const coveragePath = path.join(stateDir, "coverage.json");
const coverage = readJson(coveragePath);
const lit = coverage.layers.find((item) => item.layer_id === "LIT");
const formal = coverage.layers.find((item) => item.layer_id === "FORMAL");
const recovery = coverage.layers.find((item) => item.layer_id === "RECOVERY");
assert(lit && formal && recovery, "coverage layers missing");
lit.status =
  "foundational_spine_in_progress_27_documents_Tao_v7_complete_mathematical_text_through_line1859_complete_v5_v7_28_hunk_and_journal_15_12_1_reconciliation_Section6_local_repair_and_citation_inventory_complete_claim_driving_cited_literature_and_release_gates_open_Crandall_Conway_chain_closed_underlying_historical_computation_unlocated_Siegel1929_full_text_pending";
formal.status =
  "finite_generalized_residue_itinerary_lean_kernel_Lagarias_Crandall_Steuding_Everett_Pillai_fixed_difference_Herschfeld_primitive_root_continued_fraction_Tao_endpoint_Proposition5_2_Siegel_Tao_coordinate_Fourier_renewal_Proposition1_9_Proposition1_11_main_reduction_and_whole_version_source_citation_margin_finite_exact_certificates_verified_analytic_and_remaining_obligations_typed_open";
formal.artifacts_verified = 17;
recovery.status =
  "ACT32_checkpoint_passed_as_prior_boundary_state_advanced_in_ACT33_through_complete_Tao_whole_version_reconciliation_and_Section6_local_repair_fresh_ACT33_cited_literature_package_visual_and_release_recovery_gates_open";
writeJson(coveragePath, coverage);

const projectPath = path.join(stateDir, "project_state.json");
const project = readJson(projectPath);
assert(project.last_receipt_id === "ACT-COL-000032", "ACT32 receipt must remain current until ACT33 seals");
assert(project.current_checkpoint.receipt_id === "ACT-COL-000032", "ACT32 checkpoint must remain immutable");
project.next_action =
  "Continue PO-COL-000001 by routing and content-reading the claim-driving Tao citations absent from the source registry, beginning with Terras, Allouche, Korec, and Krasikov-Lagarias, then perform the consolidated whole-paper adversarial/formal/package/visual/recovery gates. The v7 mathematical text ends at line 1859; F028 closes the complete v5/v7 source comparison, the journal 15/12/1 hunk matrix, citation inventory, and exact Section 6 local repair under CLM-COL-000122. Preserve all theorem scopes, maps, fibres, defects, counterexample boundaries, and nonclaims. Do not enter Chatnotes, Gemini, or archived tasks yet; do not contact the quarantined task; enforce the single bounded watched Lean-worker rule. Keep all eight obligations and the durable goal active.";
project.updated_utc = updatedUtc;
project.resource_policy.last_enforcement_utc = updatedUtc;
project.resource_policy.last_enforcement_result =
  "delegated_global_rule_reaudit_found_no_active_Lean_Lake_Elan_or_R107DeficitProgression_process_tree; no_tree_required_termination; no_uncapped_or_overlapping_build_started";
appendObjectUnique(project.resource_policy.enforcement_events, "audit_utc", {
  module: "R107DeficitProgression_and_all_Lean_Lake",
  action: "delegated_rule_reaudit_no_active_matching_process_tree",
  pids: [],
  audit_utc: updatedUtc,
});
assert(project.completion_claimed === false, "completion must remain false");
assert(project.codex_goal.status === "active", "goal must remain active");
writeJson(projectPath, project);

console.log(
  JSON.stringify({
    status: "PASS",
    source_records: sources.length - 1,
    claims: claims.length - 1,
    obligations: obligations.length - 1,
    new_claim: "CLM-COL-000122",
    all_obligations_open: obligations
      .filter((item) => item.record_type === "proof_obligation")
      .every((item) => !["closed", "complete"].includes(item.status)),
    f028_sha256: auditSha,
    certificate_sha256: certificateSha,
  }),
);
