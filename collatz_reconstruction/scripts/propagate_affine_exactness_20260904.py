"""Propagate the checked affine checkpoint without rewriting older receipts."""
from __future__ import annotations
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = "research_companion/chapters/04_affine_packets_parity_necklaces_and_residue_automata.tex"
CRITICAL = "tex/chapters/06_affine_packet_source_audit.tex"
CERT = "research_companion/certificates/affine_packet_residue_checks.py"
WRAPPER = "certificates/affine_packet_source_and_cycle_checks.py"
ROUTE = "state/affine_packet_topic_route.json"
BUILD = "overleaf/sync_20260904/audit/affine_exactness/local_receipt.json"
NOW = datetime.now(timezone.utc).isoformat()

if not __debug__:
    raise RuntimeError("assertions must remain enabled")

def read(name):
    return json.loads((ROOT/name).read_text(encoding="utf-8"))

def write(name, value):
    (ROOT/name).write_text(json.dumps(value, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")

def identity(name):
    data = (ROOT/name).read_bytes()
    return {"path":name,"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()}

def append_records(name, records, key, next_id):
    rows = [json.loads(line) for line in (ROOT/name).read_text(encoding="utf-8").splitlines() if line.strip()]
    existing = {row.get(key):row for row in rows if key in row}
    for row in records:
        if row[key] in existing:
            if existing[row[key]] != row:
                raise RuntimeError(f"Existing record differs: {row[key]}")
        else:
            rows.append(row)
    header = next(row for row in rows if row.get("record_type") == "ledger_header")
    header["next_id"] = next_id
    (ROOT/name).write_text("".join(json.dumps(row,ensure_ascii=False,separators=(',',':'))+'\n' for row in rows),encoding="utf-8")

def main():
    certificate_receipt = read("qa/affine_packet_certificate_extension_20260904/extension_receipt.json")
    wrapper_receipt = read("qa/affine_packet_certificate_extension_20260904/wrapper.stdout.json")
    assert certificate_receipt["status"] == "PASS"
    assert set(wrapper_receipt["checks"].values()) == {"PASS"}
    assert wrapper_receipt["portable_certificate"]["metrics_sha256"] == "50106a4261308568466d6f4b4d9e16a09921a5efde5ac258c60cbf66577c97ba"
    certificate = identity(CERT)
    assert certificate["sha256"] == "3684832af599c1f761cb61665e0d907406a67135b0c595c6acce3731b05bfb60", certificate
    build = read(BUILD)
    assert len(build["builds"]) == 4 and build["tao_unchanged"]
    formal = {"status":"general_written_proof_and_bounded_exact_checks_no_Lean_formalization","artifact":CERT,"artifact_sha256":certificate["sha256"],"execution_receipt":"qa/affine_packet_certificate_extension_20260904/extension_receipt.json"}
    definitions = [
        (182,"independent_constructive_deduction","Packet gap encoding E is a bijection from positive compositions Pi_(m,A), m>=1 and A>=m, to binary words of length A and weight m beginning in one. N(E(p))=C(p) in Lagarias's shortened convention. The finite rotation groupoids are isomorphic by (p,j)->(E(p),S_j); identities, inverses, source fibres and stabilizers are computed, including imprimitive packets.","thm:packet-parity-cyclic-groupoid",[],["SRC-COL-000013","SRC-COL-000009","SRC-COL-000004"]),
        (183,"independent_constructive_deduction","For every nonempty positive exponent packet p, D=2^A-3^m is nonzero and coprime to 6, 3C(p)+D=2^a1 C(sigma p), and the rational point C(p)/D has exact first valuation a1 and odd-return image x_(sigma p). Divisibility by D is rotation-invariant in both directions. Primitive packets with D>0 and D|C(p) correspond exactly to positive integral odd cycles of their packet length.","thm:cyclic-affine-transport",["CLM-COL-000182"],["SRC-COL-000013","SRC-COL-000009"]),
        (184,"independent_constructive_deduction","On odd-denominator rationals, T has odd branch (3x+1)/2 and F has odd branch 3x+1. Their even branches are x/2. For p=u^r with primitive root u of length d and sum B, x_p=x_u has exact odd-return, shortened, and full periods d,B,B+d. Each intermediate rational value and odd-visit time S_j or S_j+j is specified. Full parity encoding inserts one zero after every one, with explicit inverse.","thm:packet-three-clocks",["CLM-COL-000183"],["SRC-COL-000013","SRC-COL-000009","SRC-COL-000004"]),
        (185,"independent_constructive_deduction","For positive odd q, first-part decomposition gives exact residue sets and multiplicity vectors, zero for A<m. The column matrices M_(m,a)e_r=e_(3^(m-1)+2^a r) have explicit inverses and period ord_q(2), with ord_1(2)=1. V_m=P_m...P_2 z e_1/((1-z)(1-z^lambda)^(m-1)) in Z^q[[z]], with an ordered matrix product and coefficientwise finite proof.","thm:packet-residue-automaton",["CLM-COL-000183"],[]),
        (186,"finite_exact_calculation","The exact minimum strip 3^m<2^A<(22/7)^m and two independent exhaustive 4,734,620-word scans exclude nontrivial positive odd cycles of exact periods 2 through 16. R_(8,13)(233) is all residue classes except 0 and 138; 792 packets form 99 primitive cyclic classes. This is a reproduced finite calculation, not a novel historical cycle-length bound.","thm:certified-period-sixteen-exclusion",["CLM-COL-000183","CLM-COL-000185"],["SRC-COL-000001"]),
    ]
    claims = [{"record_type":"claim","schema_version":"1.0","claim_id":f"CLM-COL-{n:06}","claim_type":kind,"status":"proved" if n != 186 else "verified_finite_calculation","statement":statement,"source_ids":sources,"dependencies":deps,"local_source_refs":["CHATINT-COL-000002"],"source_locators":["Raw affine export lines 959-1035 and 2683-2828; exact source manifestations in affine_packet_source_and_cycle_checks.py"],"proof_locator":{"path":CHAPTER,"label":label},"formal_status":formal,"nonclaims":["No priority claim or all-cycle exclusion; no complete Chatnotes coverage inferred from these results."]} for n,kind,statement,label,deps,sources in definitions]
    append_records("state/claims.jsonl",claims,"claim_id","CLM-COL-000187")
    mor_data = [
        (63,"packet_to_pointed_shortened_parity","Pi_(m,A), m>=1,A>=m","Binary length-A weight-m words with first bit 1","E(a1,...,am)=1 0^(a1-1)...1 0^(am-1)","Positive block lengths sum to A; one positions are S_0,...,S_(m-1).","Lagarias numerator and rational point; every fibre is a singleton.","Read successive cyclic one-to-one gaps.","thm:packet-parity-coordinate-isomorphism",182),
        (64,"packet_rotation_groupoid_isomorphism","Action groupoid of Z/m on Pi_(m,A)","Full subgroupoid of Z/A binary rotations on pointed-one words","(p,j)->(E(p),S_j(p))","Allowed rotation lengths are exactly one-positions. Prefix addition modulo A proves composition; S_(m-j)(sigma^j p)=A-S_j(p) proves inverses.","Identity, composition, inverses and stabilizers kd->kB for p=u^r; source-arrow fibres are singletons.","Recover packet from gaps and unique j from t=S_j.","thm:packet-parity-cyclic-groupoid",182),
        (65,"exact_full_shortened_odd_clock_comparison","Indexed rational periodic orbit of nonempty positive packet p","Full and shortened indexed rational orbits on Z_(2)","Phi^j(x_p)=T^(S_j)(x_p)=F^(S_j+j)(x_p); E_F inserts a zero after each one of E","Cyclic transport and oddness determine every intermediate value and exclude -1/3. Odd visits occur at exactly the specified times.","Rational state at odd visits and exact periods d,B,B+d for primitive root length d and sum B.","Read odd visits; the valuations recover the exponents and all omitted values. Full-word inverse deletes the zero immediately following each one.","thm:packet-three-clocks",184),
        (66,"residue_transition_permutation","Free column module Z^(Z/qZ), positive odd q, m>=2,a>=1","Same free column module","M_(m,a)e_r=e_(3^(m-1)+2^a r)","Multiplication by 2^a is invertible modulo odd q. For q=1 the sole matrix is identity.","Exact integer multiplicities, not just supports; singleton basis-index fibres.","M^(-1)e_s=e_(2^(-a)(s-3^(m-1))).","thm:packet-residue-automaton",185),
    ]
    morphisms = [{"record_type":"morphism","schema_version":"1.0","morphism_id":f"MOR-COL-{n:06}","name":name,"domain":domain,"codomain":codomain,"formula":formula,"well_definedness":well,"preserved_structure":preserved,"fibres":"Singletons for coordinate maps; for clock sampling, unique indices at odd visits with explicit reconstruction of omitted states.","inverse_status":inverse,"exceptions":["No empty packet point x_empty; the zero orbit is outside positive exponent encoding."],"claim_refs":[f"CLM-COL-{claim:06}"],"source_refs":["SRC-COL-000013","SRC-COL-000009"] if n != 66 else [],"proof_locator":{"path":CHAPTER,"label":label},"formal_status":formal} for n,name,domain,codomain,formula,well,preserved,inverse,label,claim in mor_data]
    for row in morphisms:
        if row["morphism_id"] == "MOR-COL-000065":
            row["fibres"] = "The odd-time maps are bijections onto the odd-visit times. The omitted even states are recovered uniquely by the displayed powers of two; repeated states retain distinct time indices."
        else:
            row["fibres"] = "Every fibre of the stated bijection is a singleton; for MOR-COL-000064 this applies separately to objects and source-arrow fibres."
        if row["morphism_id"] == "MOR-COL-000066":
            row["exceptions"] = ["The permutation and inverse statements require odd q; q=1 is the explicitly specified singleton convention."]
    append_records("state/morphisms.jsonl",morphisms,"morphism_id","MOR-COL-000067")
    route = read(ROUTE)
    for item in route["sources"]:
        if item["publication_unit_or_source_id"].startswith("LAGARIAS-"):
            item["publication_unit_or_source_id"] = "SRC-COL-000013"
        if item["publication_unit_or_source_id"].startswith("URATA-"):
            item["publication_unit_or_source_id"] = "SRC-COL-000009"
        item["claim_or_proof_crosswalk_ids"] = [f"CLM-COL-{n:06}" for n in ([182,183,184,185] if item["source_class"] == "local_unpublished_work" else [182,183,184])]
    route["updated_utc"] = NOW
    write(ROUTE,route)
    existing_routes = [json.loads(line) for line in (ROOT/"state/topic_routes.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    existing_routes = [r for r in existing_routes if r.get("topic_id") != route["topic_id"]] + [route]
    (ROOT/"state/topic_routes.jsonl").write_text("".join(json.dumps(r,ensure_ascii=False,separators=(',',':'))+'\n' for r in existing_routes),encoding="utf-8")
    current = {"schema_version":1,"checkpoint":"AFFINE-EXACTNESS-20260904","updated_utc":NOW,"scope":"Five exact affine claims and four morphisms; partial direct raw intake, not global completion","claims":[r["claim_id"] for r in claims],"morphisms":[r["morphism_id"] for r in morphisms],"files":[identity(name) for name in [CHAPTER,CRITICAL,CERT,WRAPPER,ROUTE]],"build_receipt":identity(BUILD),"source_reading":{"Lagarias":"printed pp.33,36-39 visually read","Urata":"native seven-page text and printed p.10 formulas/proofs visually read","Laarhoven":"source lines66-120,261-335","raw_affine":"direct windows921-1040,2679-2828"},"whole_source_coverage_reconciled":False,"formal_status":"written general proofs and exact finite Python checks; no Lean launch","remote_sync_status":"pending","next_action":"Verify remote current files and compile both entries in canonical Overleaf; then reconcile antecedent versions and resume raw affine content intake."}
    write("state/affine_packet_current.json",current)
    project = read("state/project_state.json")
    project["updated_utc"] = NOW
    project["current_request_state"]["active_tex_sha256"] = identity(CHAPTER)["sha256"]
    project["current_request_state"]["active_write_status"] = "checked_local_checkpoint_remote_pending"
    project["current_request_state"]["affine_checkpoint"] = "state/affine_packet_current.json"
    project["next_action"] = current["next_action"]
    write("state/project_state.json",project)
    coverage = read("state/coverage.json")
    coverage["coverage_status"] = "active_affine_exactness_checkpoint_after_ACT43_partial_intake_reconciliation_pending"
    coverage["post_ACT43_affine_checkpoint"] = {"path":"state/affine_packet_current.json","claims":current["claims"],"morphisms":current["morphisms"],"historical_layer_counts":"Older layer counters are ACT43 history, not a claim that later affine results or manuscript pages are absent.","new_full_source_reading_claimed":False}
    coverage["live_tex_advanced_after_checkpoint"] = True
    write("state/coverage.json",coverage)
    print(json.dumps({"status":"PASS","claims":current["claims"],"morphisms":current["morphisms"],"active_tex":identity(CHAPTER)},indent=2))

if __name__ == "__main__":
    main()
