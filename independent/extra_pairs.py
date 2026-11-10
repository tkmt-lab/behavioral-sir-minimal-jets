#!/usr/bin/env python3
"""Stage-2 examples with both new k and changed, non-scaled initial point."""
import sys
sys.dont_write_bytecode=True
import certify_pairs as cp
from stage1_explore import flow,reconstruct,Dual,solve_pair
from fractions import Fraction as Q
from pathlib import Path
import math,json,time,resource,signal
ROOT=Path(__file__).resolve().parent
I=cp.I

def funcs_new(p,q,k):
    target=flow(I(1),I(2),I(1),I(Q(2,5)),I(1),k,5)
    g,b=reconstruct(I(1),I(1),target[2],p,q,k)
    jets=flow(I(1),q,b,p,g,k,5)
    return jets[3]-target[3],jets[4]-target[4],jets,target,g,b

def main():
    signal.alarm(60);start=time.perf_counter()
    # Keep certificate core unchanged; only the target initial point changes.
    cp.funcs=funcs_new
    lo=Q('1.414213562373095048801688724209');hi=Q('1.414213562373095048801688724210');assert lo*lo<2<hi*hi
    out={};exploration={}
    cases=[('7/2',3.5,I(Q(7,2))),('1+sqrt(2)',1+math.sqrt(2),I(1+lo,1+hi))]
    for name,kn,ki in cases:
        target=flow(1.,2.,1.,.4,1.,kn,5);roots=[]
        for p in [.05,.2,.4,.6,.8,.95]:
            for q in [.2,.5,1,2,3,5,8,12]:
                r=solve_pair(*target[:5],p,q,kn)
                if r and all(abs(r[0]-s[0])+abs(r[1]-s[1])>1e-6 for s in roots):roots.append(r)
        alt=[r for r in roots if abs(r[0]-.4)>1e-5];assert len(alt)==1
        p,q=alt[0][:2];result=cp.certify(ki,str(p),str(q))
        # Core originally reports derivative at p=1/2; replace with new true branch.
        tj=cp.jac(I(Q(2,5)),I(2),ki);d=tj[0][0]*tj[1][1]-tj[0][1]*tj[1][0];assert not d.lo<=0<=d.hi
        result['det_true_2x2']=d.row();result['summary']['det_true']=d.floatrow()
        result['true_initial']={'p':'2/5','q':2,'b':1,'g':1,'y':1,'alpha':'2/3','S0':2,'Z0':1,'beta':'(5/3)^k','R0':7}
        result['note']='The shared certificate routine also checks nonsingularity at p=1/2; that surplus check is not the new true-branch determinant.'
        exploration[name]={'grid_p':[.05,.2,.4,.6,.8,.95],'grid_q':[.2,.5,1,2,3,5,8,12],'all_positive_roots_found':roots}
        out[name]=result
    rec={'cases':out,'exploration':exploration,'resources':{'seconds':time.perf_counter()-start,'rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'usd':0,'processes':1,'alarm_seconds':60}}
    (ROOT/'extra-pairs.json').write_text(json.dumps(rec,indent=2)+'\n')
    print(json.dumps({n:r['summary'] for n,r in out.items()}))
if __name__=='__main__':main()
