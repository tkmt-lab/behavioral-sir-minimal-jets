"""Closed inventory, metadata and optional bounded PDF/private-path inspection."""
from pathlib import Path,PurePosixPath
import argparse,ast,hashlib,json,re,shutil,subprocess,sys,zlib
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def files(root):
    out=set()
    for p in root.rglob('*'):
        rel=p.relative_to(root)
        if rel.parts[0]=='.git':continue
        assert not p.is_symlink(),str(rel)
        if p.is_file():out.add(rel.as_posix())
    return out

def inventory(root):
    names=set()
    for line in (root/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1);rel=PurePosixPath(name)
        assert re.fullmatch('[0-9a-f]{64}',digest) and not rel.is_absolute() and '..' not in rel.parts
        assert name not in names and name!='SHA256SUMS'
        names.add(name);p=root/name
        assert p.is_file() and not p.is_symlink() and sha(p)==digest,name
    assert files(root)==names|{'SHA256SUMS'},'inventory mismatch'
    return len(names)+1

def fp(root,record):
    p=root/record['path'];assert p.is_file()
    assert p.stat().st_size==record['bytes'] and sha(p)==record['sha256'],record['path']

def public_view(view,name,markers):
    assert not any(token in view for token in markers),('local path found',name)
    # Construct patterns without embedding an internal identifier or path.
    patterns=[rb'\bR'+rb'[0-9]{3}\b',bytes.fromhex('737475646965732f')+rb'[^\s]+',
              rb'\b'+bytes.fromhex('6472616674')+rb'\b']
    # Two-character ratings are meaningful in text, not compressed PDF/font bytes.
    if not name.endswith('.pdf'):patterns += [rb'\bN[1-5]\b', rb'\b(?:'+bytes.fromhex('636f6f7264696e61746f727c4661626c657c436c61756465')+rb')\b']
    for pattern in patterns:
        assert re.search(pattern,view,re.I) is None,('internal identifier/path or edition label found',name)
    if name != 'VERIFICATION-RECORD.md':
        workflow = bytes.fromhex('7072657061726174696f6e7c706c616e6e65647c70656e64696e677c756e7075626c69736865647c6e6f74207965742072656c6561736564')
        assert re.search(rb'\b(?:'+workflow+rb')\b',view,re.I) is None,('workflow state outside dated history',name)

def public_content(root):
    for name in files(root):
        p=root/name
        if p.suffix!='.pdf':public_view(p.read_bytes(),name,[])
    return 'PASS'

def pdf_and_paths(root):
    # Generic path vocabulary encoded so this scanner does not match its own source.
    markers=[bytes.fromhex(x) for x in ['2f55736572732f','2f566f6c756d65732f','2f707269766174652f','2f7661722f666f6c646572732f','2f686f6d652f','2f776f726b73706163652f','2f746d702f']]
    pdfs=[]
    for name in files(root):
        p=root/name;raw=p.read_bytes();views=[raw]
        if p.suffix=='.pdf':
            pdfs.append(name)
            for tool,tail in [('pdftotext',[str(p),'-']),('pdfinfo',[str(p)])]:
                assert shutil.which(tool),'--pdf requires existing '+tool
                r=subprocess.run([tool,*tail],capture_output=True,timeout=30)
                assert r.returncode==0,(name,tool)
                public_view(r.stdout,name+'.text',markers);views.append(r.stdout)
            for m in re.finditer(rb'\bstream\r?\n(.*?)\r?\nendstream\b',raw,re.S):
                try:views.append(zlib.decompress(m[1]))
                except zlib.error:pass
        for view in views:
            public_view(view,name,markers)
    return dict(pdfs=pdfs,known_private_path_patterns='PASS',internal_identifiers_and_paths='PASS',edition_labels='PASS',scope='Bounded raw/PDF-text/metadata/deflate scan; not exhaustive sensitive-data detection')

def main():
    if not __debug__:raise SystemExit('Python assertions must remain enabled.')
    ap=argparse.ArgumentParser();ap.add_argument('--pdf',action='store_true');args=ap.parse_args()
    count=inventory(ROOT);c=load(ROOT/'claims.json');assert c['version']=='1.0.0' and c['article_version']=='1.0'
    provenance=load(ROOT/'PROVENANCE.json')
    assert {r['path'] for r in provenance['files']}==files(ROOT)-{'PROVENANCE.json','SHA256SUMS'}
    for record in provenance['files']:fp(ROOT,record)
    s=c['scope'];assert s['fixed_known_k']==['2','3','5/2'] and s['known_N0'] and s['positive_real_domain'] and s['all_positive_same_k_competitors']
    assert s['local_minimum']==4 and s['global_minimum']==5 and s['genericity']=='Euclidean open dense true set'
    assert not any(s[k] for k in ['all_k_classified','all_points_ambiguous_at_order_four','unknown_k','unknown_N0','noisy_data','formal_proof','human_peer_review','external_package_comparison_executed'])
    paper=(ROOT/c['paper']['path']).read_text();fp(ROOT,c['paper']);fp(ROOT,c['pdf'])
    labels=re.findall(r'\\label\{([^}]+)\}',paper);refs=re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',paper)
    assert len(labels)==len(set(labels)) and set(refs)<=set(labels)
    for claim in c['claims']:
        assert claim['paper_label'] in labels
        for ev in claim['evidence']:fp(ROOT,ev)
    source=load(ROOT/'source-derivatives.json')
    assert len(source['records'])==16
    for row in source['records']:fp(ROOT,row)
    changed=[r for r in source['records'] if r['changed']]
    expected_changes={'producer/limits.py','independent/stage1_explore.py',
        'independent/check_source_certificate.py','independent/source-certificate-check.json',
        'companion/paper-behavioral-sir-v3.0-en.tex','companion/paper-behavioral-sir-v3.0-en.pdf'}
    assert {r['path'] for r in changed}==expected_changes
    for row in source['records']:
        assert row['source']=='original-input:'+row['path']
        differs=(row['bytes'],row['sha256'])!=(row['source_bytes'],row['source_sha256'])
        assert row['changed']==differs
        assert (row['change']!='none')==differs
    assert "subprocess.check_output(['git'" not in (ROOT/'independent/check_source_certificate.py').read_text()
    cert=load(ROOT/'producer/output/certificate.json')['cases'];assert [r['k'] for r in cert]==['2','3','5/2']
    first=load(ROOT/'independent/stage1-certified-pairs.json')['cases'];extra=load(ROOT/'independent/extra-pairs.json')['cases']
    assert set(first)=={'2','3','5/2','7/2','1+sqrt(2)'} and set(extra)=={'7/2','1+sqrt(2)'}
    assert all(r['strict_inclusion'] and r['unique_root_in_box'] for r in [*first.values(),*extra.values()])
    vp=load(ROOT/'version-plan.json');assert vp['status']=='release-edition'
    assert vp['release_date']=='2026-11-10' and vp['tag']=='v1.0.0'
    repo='https://github.com/tkmt-lab/behavioral-sir-minimal-jets'
    assert vp['repository_code']==repo and vp['packet_version']==c['version'] and vp['article_version']==c['article_version']
    citation=load(ROOT/'CITATION.cff');zenodo=load(ROOT/'.zenodo.json')
    assert citation['date-released']==vp['release_date'] and citation['repository-code']==repo
    assert citation['preferred-citation']['date-released']==vp['release_date']
    assert zenodo['publication_date']==vp['release_date']
    assert any(r['identifier']==repo for r in zenodo['related_identifiers'])
    assert vp['verification_record']=='VERIFICATION-RECORD.md'
    # Edition checks make no assertion that an external upload or DOI operation occurred.
    assert load(ROOT/'.zenodo.json')['version']=='1.0.0' and load(ROOT/'CITATION.cff')['version']=='1.0.0'
    val=load(ROOT/'pdf-validation.json');assert val['pages']==8 and val['all_pages_viewed'] and val['pdf_sha256']==c['pdf']['sha256']
    assert val['inspected_pages']==list(range(1,val['pages']+1))
    assert val['source_sha256']==c['paper']['sha256']
    cv=val['companion'];assert cv['pages']==9 and cv['all_pages_viewed'] and cv['inspected_pages']==list(range(1,10))
    assert cv['source_sha256']==sha(ROOT/'companion/paper-behavioral-sir-v3.0-en.tex')
    assert cv['pdf_sha256']==sha(ROOT/'companion/paper-behavioral-sir-v3.0-en.pdf')
    assert 'lem:observable' in labels and 'app:observable' in labels
    assert load(ROOT/'observability-check.json')['status']=='PASS'
    for record in c['cover_observability']['fixed_companion']:fp(ROOT,record)
    for name in files(ROOT):
        if name.endswith('.py'):ast.parse((ROOT/name).read_text())
    content_status=public_content(ROOT)
    result=dict(public_content=content_status,status='PASS',files=count,version='1.0.0',algebraic_cases=3,interval_cases=7,scope_and_hashes='PASS')
    if args.pdf:result['pdf_scan']=pdf_and_paths(ROOT)
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
