"""Reproduce sealed certificate claims using the Python standard library only."""
from pathlib import Path
import argparse,json,os,shutil,subprocess,sys,tempfile,time
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
RUNTIME_FIELDS={'seconds','rss_bytes','max_rss_bytes'}

def mathematical(value):
    if isinstance(value,dict):return {k:mathematical(v) for k,v in value.items() if k not in RUNTIME_FIELDS}
    if isinstance(value,list):return [mathematical(v) for v in value]
    return value

def main():
    if not __debug__:raise SystemExit('Assertions must be enabled; do not use python -O.')
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);args=ap.parse_args()
    start=time.perf_counter();steps=[]
    from check_packet import inventory
    inventory(ROOT)
    with tempfile.TemporaryDirectory(prefix='sir-jet-check-') as tmp:
        work=Path(tmp)
        # Copy only the closed package inventory, never local repositories or caches.
        for line in (ROOT/'SHA256SUMS').read_text().splitlines():
            _,name=line.split('  ',1);dest=work/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,dest)
        shutil.copyfile(ROOT/'SHA256SUMS',work/'SHA256SUMS')
        env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OMP_NUM_THREADS='1')
        def run(script,*extra):
            out=subprocess.run([sys.executable,'-B',str(work/script),*extra],cwd=work,env=env,capture_output=True,text=True,timeout=60)
            assert out.returncode==0,dict(script=script,stdout=out.stdout,stderr=out.stderr)
            steps.append(script)
        def compare(name):
            actual=json.loads((work/name).read_text());expected=json.loads((ROOT/name).read_text())
            assert mathematical(actual)==mathematical(expected),name
        # This checker must see the sealed producer receipt, before its reproduction.
        run('independent/check_source_certificate.py');compare('independent/source-certificate-check.json')
        interval=work/'interval-replay.json'
        run('verify_intervals.py','--output',str(interval))
        intervals=json.loads(interval.read_text());assert intervals['status']=='PASS' and intervals['interval_certificates']==7
        run('producer/verify_certificate.py');compare('producer/output/certificate-check.json')
        run('build_tables.py');compare('article-cases.json')
        assert (work/'certificate-tables.tex').read_bytes()==(ROOT/'certificate-tables.tex').read_bytes()
        run('check_observability.py','--output',str(work/'observability-check.json'))
        compare('observability-check.json')
    inventory(ROOT)
    result=dict(status='PASS',version='1.0.0',main_exponents=['2','3','5/2'],main_algebraic_certificates=3,
        independent_algebraic_rechecks=3,interval_certificates=7,additional_changed_point_exponents=['7/2','1+sqrt(2)'],
        steps=steps,only_runtime_fields_ignored=sorted(RUNTIME_FIELDS),original_package_unchanged=True,
        stdlib_only=True,external_identifiability_packages_run=False,python=sys.version.split()[0],seconds=time.perf_counter()-start)
    result['appendix_B_identities_and_printed_intervals']='PASS'
    if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
