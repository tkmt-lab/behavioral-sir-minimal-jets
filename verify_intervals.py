"""Replay frozen rational interval certificates; no numerical search is used."""
from fractions import Fraction as Q
from pathlib import Path
import argparse,hashlib,json,signal,sys,time
ROOT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT/'independent'))
import certify_pairs as cp
import extra_pairs as extra
ORIGINAL_FUNCS=cp.funcs

def exact_part(record):
    return {k:v for k,v in record.items() if k not in {'summary','note','true_initial'}}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);args=ap.parse_args()
    signal.alarm(60);start=time.perf_counter();records=[]
    for file,changed,expected in [('stage1-certified-pairs.json',False,{'2','3','5/2','7/2','1+sqrt(2)'}),('extra-pairs.json',True,{'7/2','1+sqrt(2)'})]:
        data=json.loads((ROOT/'independent'/file).read_text())['cases']
        assert set(data)==expected
        cp.funcs=extra.funcs_new if changed else ORIGINAL_FUNCS
        for name,rec in data.items():
            lo,hi=map(Q,rec['k_interval'])
            if name=='1+sqrt(2)':assert 0<lo-1<hi-1 and (lo-1)**2<2<(hi-1)**2
            else:assert lo==hi==Q(name)
            ki=cp.I(lo,hi)
            boxes=[tuple(map(Q,x)) for x in rec['root_box_p_q']]
            assert all(b-a==Q(2,10**8) for a,b in boxes)
            true_p=Q(2,5) if changed else Q(1,2)
            assert not boxes[0][0]<=true_p<=boxes[0][1]
            center=[(a+b)/2 for a,b in boxes]
            got=cp.certify(ki,*map(str,center))
            if changed:
                j=cp.jac(cp.I(true_p),cp.I(2),ki)
                d=j[0][0]*j[1][1]-j[0][1]*j[1][0]
                assert not d.lo<=0<=d.hi
                got['det_true_2x2']=d.row()
                assert rec['true_initial']=={'p':'2/5','q':2,'b':1,'g':1,'y':1,'alpha':'2/3','S0':2,'Z0':1,'beta':'(5/3)^k','R0':7}
            assert exact_part(got)==exact_part(rec),(file,name)
            payload=json.dumps(exact_part(got),sort_keys=True,separators=(',',':')).encode()
            records.append(dict(group='changed-point' if changed else 'first-stage',k=name,strict_inclusion=True,contraction_norm_less_than_one=True,
                positive=True,distinct_from_true=True,both_jacobians_nonsingular=True,fifth_gap_nonzero=True,
                exact_certificate_sha256=hashlib.sha256(payload).hexdigest()))
    result=dict(status='PASS',interval_certificates=len(records),cases=records,
        method='Frozen rational boxes and exact Fraction arithmetic; original interval formulas, no root search or floating-point acceptance',seconds=time.perf_counter()-start)
    if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
if __name__=='__main__':main()
