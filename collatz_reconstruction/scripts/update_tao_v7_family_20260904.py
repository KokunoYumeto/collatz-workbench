"""Mechanical propagation/build of the reviewed V7 first-entry-family revision.

No index rebuild, Lean, Git, source-literature modification, or archive creation.
Run after the finite-certificate worker has finished its file edit.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import psutil
import fitz

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / 'preprints/tao_clock_audit'
CANON = ROOT / 'overleaf/sync_20260904/canonical_project'
AUDIT = P / 'audit/v7_family_20260904'
CAP = 5_000_000_000
NOW = datetime.now(timezone.utc).isoformat()

def readj(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def writej(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')

def pin(p):
    data=p.read_bytes()
    return {'bytes':len(data), 'sha256':hashlib.sha256(data).hexdigest()}

def run(cmd, cwd, name):
    log=AUDIT/(name+'.txt')
    with log.open('w', encoding='utf-8') as stream:
        proc=subprocess.Popen(cmd,cwd=cwd,stdout=stream,stderr=subprocess.STDOUT)
        peak=0
        deadline=time.monotonic()+240
        while proc.poll() is None:
            try:
                tree=[psutil.Process(proc.pid)]
                tree+=tree[0].children(recursive=True)
                used=sum(p.memory_info().rss for p in tree if p.is_running())
                peak=max(peak,used)
                if used>=CAP or time.monotonic()>deadline:
                    for item in reversed(tree):
                        try: item.kill()
                        except psutil.NoSuchProcess: pass
                    raise RuntimeError('Task cap or 240s timeout exceeded: '+name)
            except psutil.NoSuchProcess:
                pass
            time.sleep(.05)
        assert proc.returncode==0, (name,proc.returncode,log)
    print(name,'PASS',peak,'peak bytes',flush=True)
    return {'command':cmd,'cwd':str(cwd),'exit_code':proc.returncode,
            'peak_process_tree_rss_bytes':peak,'cap_bytes':CAP,
            'output':str(log.relative_to(ROOT)),**pin(log)}

def upsert_ledger(rel,key,records,nextid=None):
    path=ROOT/rel
    rows=[json.loads(line) for line in path.read_text(encoding='utf-8-sig').splitlines() if line]
    for item in records:
        matches=[i for i,row in enumerate(rows) if row.get(key)==item[key]]
        assert len(matches)<=1
        if matches: rows[matches[0]]=item
        else: rows.append(item)
    if nextid: rows[0]['next_id']=nextid
    path.write_text(''.join(json.dumps(r,ensure_ascii=False,separators=(',',':'))+'\n' for r in rows),encoding='utf-8')

def main():
    AUDIT.mkdir(parents=True,exist_ok=True)
    source=readj(P/'source_manifest.json')
    old=[r for r in source['sources'] if r['id']=='TAO-V5']
    if old: writej(AUDIT/'historical_comparison_source.json',old)
    source['sources']=[r for r in source['sources'] if r['id']!='TAO-V5']
    source['baseline']='TAO-V7; historical comparison sources retained in local audit only'
    writej(P/'source_manifest.json',source)
    manifest=readj(P/'MANIFEST.json')
    for entry in manifest['files']: entry.update(pin(P/entry['path']))
    writej(P/'MANIFEST.json',manifest)
    checks=[run([sys.executable,'-X','utf8','verify.py'],P,'portable_verify')]

    # Preserve the three roots. Only mapped Tao dependencies are copied.
    mapping=readj(CANON/'SOURCE_MAP.json')
    changed=[]
    for item in mapping['files']:
        if not item['source_path'].startswith('preprints/tao_clock_audit/'):
            continue
        src=ROOT/item['source_path']; dest=CANON/item['package_path']
        if not src.exists(): raise FileNotFoundError(src)
        content=src.read_bytes()
        if item['package_path']=='tao_preprint.tex':
            text=content.decode('utf-8')
            text=text.replace('\\input{sections/','\\input{tao/sections/')
            text=text.replace('\\input{bibliography}','\\input{tao/bibliography}')
            content=text.encode('utf-8')
        if not dest.exists() or dest.read_bytes()!=content:
            dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_bytes(content); changed.append(item['package_path'])
        item.update(source_sha256=pin(src)['sha256'],staged_intermediate_sha256=pin(src)['sha256'],**pin(dest))
    mapping['tao_v7_family_revision']={'updated_utc':NOW,'scope':'Common-base all-threshold first-entry and joint laws','raw_directive':'USR-0017','remote_status':'pending'}
    writej(CANON/'SOURCE_MAP.json',mapping)
    changed.append('SOURCE_MAP.json')
    status=readj(CANON/'PACKAGE_STATUS.json')
    status['tao_v7_family_revision']={'status':'local_sources_updated_remote_verification_pending','historical_archives':'Earlier archives are snapshots, not the current live files. No archive was created.'}
    writej(CANON/'PACKAGE_STATUS.json',status); changed.append('PACKAGE_STATUS.json')
    cm=readj(CANON/'MANIFEST.json')
    for item in cm['files']: item.update(pin(CANON/item['path']))
    writej(CANON/'MANIFEST.json',cm); changed.append('MANIFEST.json')

    exe=r'C:\Users\LOCAL_USER\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe'
    out=P/'output/pdf'; out.mkdir(parents=True,exist_ok=True)
    for i in range(3):
        checks.append(run([exe,'-interaction=nonstopmode','-halt-on-error','-jobname=tao_clock_audit','-output-directory='+str(out),'main.tex'],P,'pdflatex_'+str(i+1)))
    buildlog=(out/'tao_clock_audit.log').read_text(encoding='utf-8',errors='replace')
    bad=re.findall(r'(?m)^.*(?:LaTeX Warning|Package .* Warning|Overfull|Undefined control sequence|Fatal error).*$' ,buildlog)
    assert not bad,bad
    pdf=out/'tao_clock_audit.pdf'; doc=fitz.open(pdf)
    render=AUDIT/'pages'; render.mkdir(exist_ok=True)
    for i,page in enumerate(doc):
        page.get_pixmap(matrix=fitz.Matrix(1.4,1.4)).save(render/f'page_{i+1:02}.png')
    text='\n'.join(page.get_text() for page in doc)
    assert 'v5' not in text.lower()
    assert 'Coherent first-entry limits' in text
    assert 'Joint first-entry distributions' in text
    assert 'ChatGPT 5.6 Sol' in text

    evidence={'status':'written_proof_independently_reviewed_and_finite_map_checks','artifact':'preprints/tao_clock_audit/certificates/check_finite.py',
              'artifact_sha256':pin(P/'certificates/check_finite.py')['sha256'],'execution_receipt':'preprints/tao_clock_audit/audit/v7_family_20260904/portable_verify.txt',
              'analytic_input':'Tao V7 Proposition1.11 cited, not independently formalized','Lean':'not launched'}
    claims=[]
    statements=[('CLM-COL-000187','cor:limit','For a fixed b>=s*, t_j=b^(alpha^j), K_x mu_(t_(j+1)) converges for every x>=1. The l1 error is <=L_c(log t_j)^(-c) uniformly for x<=t_j. The limits obey K_x lambda_y=lambda_x for every x<=y. For x>=b, failure mass is <=B x^(-c/alpha)+L_c alpha^c(log x)^(-c). Arbitrary-base independence is not asserted.',[]),
                ('CLM-COL-000188','cor:joint-entry','For every finite ordered list of thresholds, common-input joint first-entry laws converge with the same error bound as at the largest threshold. The map J(z)=(p_x1(z),...,p_xr(z)) bijects the largest-threshold state set to adjacent-passage-compatible tuples, with inverse last projection and l1-isometric pushforward.',['CLM-COL-000187'])]
    for cid,label,statement,deps in statements:
        claims.append({'record_type':'claim','schema_version':'1.0','claim_id':cid,'claim_type':'independent_constructive_deduction','status':'proved',
                       'statement':statement,'source_ids':['SRC-COL-000005'],'dependencies':deps,'source_locators':['V7 collatz.tex 310-339,535-593'],
                       'proof_locator':{'path':'preprints/tao_clock_audit/sections/consequences.tex','label':label},'formal_status':evidence,
                       'nonclaims':['No stronger orbit-minimum bound, arbitrary-scale-phase independence, or priority claim.']})
    upsert_ledger('state/claims.jsonl','claim_id',claims,'CLM-COL-000189')
    morph={'record_type':'morphism','schema_version':'1.0','morphism_id':'MOR-COL-000067','name':'joint_first_entry_profile_bijection',
           'domain':'E_xr=(positive odds<=x_r) union {dagger}, 1<=x1<=...<=xr, r>=1',
           'codomain':'Tuples zi in E_xi with p_xi(z_(i+1))=zi',
           'formula':'J(z)=(p_x1(z),...,p_xr(z))',
           'well_definedness':'Nested first passage, including absorbing failure, gives every compatibility equation.',
           'preserved_structure':'Exact joint law, all threshold marginals, and l1 norm of signed measures under pushforward.',
           'fibres':'Singleton fibres, since the last coordinate equals z; no information loss.',
           'inverse_status':'Last-coordinate projection; nested passage proves both inverse identities.',
           'exceptions':['Requires ordered thresholds>=1; equal thresholds and r=1 are included.'],
           'claim_refs':['CLM-COL-000188'],'source_refs':['SRC-COL-000005'],
           'proof_locator':{'path':'preprints/tao_clock_audit/sections/consequences.tex','label':'cor:joint-entry'},'formal_status':evidence}
    upsert_ledger('state/morphisms.jsonl','morphism_id',[morph],'MOR-COL-000068')
    route=readj(ROOT/'state/tao_v7_topic_route.json')
    upsert_ledger('state/topic_routes.jsonl','topic_id',[route])
    current=readj(ROOT/'state/tao_preprint_current.json')
    current.update(status='v7_family_local_built_visual_and_remote_checks_pending',updated_utc=NOW,
                   latest_directive='raw/USR-0017-tao-v7-baseline.txt',topic_route='state/tao_v7_topic_route.json',
                   next_action='Visually inspect current PDF; upload only changed named files inside canonical project and verify remote compilation.',
                   added_claims=['CLM-COL-000187','CLM-COL-000188'],added_morphisms=['MOR-COL-000067'])
    current['prior_verified_artifacts_before_v7_family']=current.pop('verified_local_artifacts') if 'verified_local_artifacts' in current else current.get('prior_verified_artifacts_before_v7_family')
    current['local_v7_family_pdf']={'path':str(pdf.relative_to(ROOT)),**pin(pdf),'pages':len(doc),'visual_review':'pending'}
    current['overleaf']['sync_status']='changed_local_files_pending_upload'
    writej(ROOT/'state/tao_preprint_current.json',current)
    receipt={'receipt_id':'TAO-V7-FAMILY-LOCAL-20260904','updated_utc':NOW,'checks':checks,
             'pdf':{'path':str(pdf.relative_to(ROOT)),**pin(pdf),'pages':len(doc)},'changed_remote_paths':sorted(set(changed)),
             'files':[{'path':p,**pin(CANON/p)} for p in sorted(set(changed))],
             'claims':['CLM-COL-000187','CLM-COL-000188'],'morphisms':['MOR-COL-000067'],
             'visual_status':'pending','remote_status':'pending','whole_goal_complete':False,'new_archive':False}
    writej(AUDIT/'local_receipt.json',receipt)
    print(json.dumps(receipt,indent=2))

if __name__=='__main__':main()
