#!/usr/bin/env python3
"""Rational interval Krawczyk certificates from our fresh ODE recurrence."""
import sys
sys.dont_write_bytecode=True
from stage1_explore import flow,reconstruct,Dual
from fractions import Fraction as Q
from pathlib import Path
import json,time,resource,signal
ROOT=Path(__file__).resolve().parent
class I:
    def __init__(self,a=0,b=None):
        if isinstance(a,I):self.lo,self.hi=a.lo,a.hi;return
        self.lo,self.hi=Q(a),Q(a if b is None else b);assert self.lo<=self.hi
    def __add__(self,b):b=I(b);return I(self.lo+b.lo,self.hi+b.hi)
    __radd__=__add__
    def __neg__(self):return I(-self.hi,-self.lo)
    def __sub__(self,b):return self+-I(b)
    def __rsub__(self,b):return I(b)+-self
    def __mul__(self,b):
        # Allow Dual's reflected operation to preserve automatic derivatives.
        if isinstance(b,Dual):return NotImplemented
        b=I(b);v=[self.lo*b.lo,self.lo*b.hi,self.hi*b.lo,self.hi*b.hi];return I(min(v),max(v))
    __rmul__=__mul__
    def __truediv__(self,b):
        if isinstance(b,Dual):return NotImplemented
        b=I(b);assert not b.lo<=0<=b.hi
        return self*I(1/b.hi,1/b.lo)
    def __rtruediv__(self,b):return I(b)/self
    def row(self):return [str(self.lo),str(self.hi)]
    def floatrow(self):return [float(self.lo),float(self.hi)]
    def absmax(self):return max(abs(self.lo),abs(self.hi))

def funcs(p,q,k):
    target=flow(I(1),I(2),I(1),I(Q(1,2)),I(1),k,5)
    g,b=reconstruct(I(1),I(1),target[2],p,q,k)
    jets=flow(I(1),q,b,p,g,k,5)
    return jets[3]-target[3],jets[4]-target[4],jets,target,g,b

def jac(p,q,k):
    f,h,*_=funcs(Dual(p,I(1),I(0)),Dual(q,I(0),I(1)),k)
    return [[f.a,f.b],[h.a,h.b]]

def certify(k,ptext,qtext):
    c=[Q(ptext),Q(qtext)];eps=Q(1,10**8);B=[I(x-eps,x+eps) for x in c]
    km=I((k.lo+k.hi)/2);J0=jac(I(c[0]),I(c[1]),km)
    m=[[z.lo for z in row] for row in J0];assert all(z.lo==z.hi for row in J0 for z in row)
    d=m[0][0]*m[1][1]-m[0][1]*m[1][0];assert d
    C=[[m[1][1]/d,-m[0][1]/d],[-m[1][0]/d,m[0][0]/d]]
    f=funcs(I(c[0]),I(c[1]),k)[:2];J=jac(*B,k)
    E=[[I(int(i==j))-sum((C[i][l]*J[l][j] for l in range(2)),I()) for j in range(2)] for i in range(2)]
    K=[I(c[i])-sum((C[i][j]*f[j] for j in range(2)),I())+sum((E[i][j]*I(-eps,eps) for j in range(2)),I()) for i in range(2)]
    assert all(b.lo<z.lo<=z.hi<b.hi for b,z in zip(B,K))
    norm=max(sum(e.absmax() for e in row) for row in E);assert norm<1
    det=J[0][0]*J[1][1]-J[0][1]*J[1][0];assert not det.lo<=0<=det.hi
    tj=jac(I(Q(1,2)),I(2),k);td=tj[0][0]*tj[1][1]-tj[0][1]*tj[1][0];assert not td.lo<=0<=td.hi
    _,_,jets,target,g,b=funcs(*B,k);a=B[0]/(1-B[0]);S=B[1]/b;Z=1/b
    assert B[0].lo>0 and B[0].hi<1 and g.lo>0 and b.lo>0 and S.hi+1<10
    diff=jets[5]-target[5];assert not diff.lo<=0<=diff.hi
    return {'k_interval':k.row(),'root_box_p_q':[z.row() for z in B],'krawczyk_image':[z.row() for z in K],
       'contraction_norm_upper':str(norm),'strict_inclusion':True,'unique_root_in_box':True,
       'preconditioner':[[str(x) for x in row] for row in C],
       'det_true_2x2':td.row(),'det_competitor_2x2':det.row(),'g':g.row(),'b':b.row(),'alpha':a.row(),'S0':S.row(),'Z0':Z.row(),'N0':10,
       'fifth_jet_competitor_minus_true':diff.row(),'summary':{'p_q':[z.floatrow() for z in B],'det_true':td.floatrow(),'det_competitor':det.floatrow(),'fifth_gap':diff.floatrow()}}

def main():
    signal.alarm(60);start=time.perf_counter()
    lo=Q('1.414213562373095048801688724209');hi=Q('1.414213562373095048801688724210');assert lo*lo<2<hi*hi
    cases=[('2',I(2),'0.4933991454316379','1.847877971633491'),('3',I(3),'0.4654318384722714','1.5328875219496054'),('5/2',I(Q(5,2)),'0.4791575947687555','1.6541569245037078'),('7/2',I(Q(7,2)),'0.4531411931609705','1.4504194668928858'),('1+sqrt(2)',I(1+lo,1+hi),'0.48161321352606246','1.6808490254898156')]
    out={name:certify(k,p,q) for name,k,p,q in cases}
    result={'method':'rational interval Krawczyk, uniform in k interval; source-independent polynomial ODE',
        'selection':'all five numerical candidates from frozen grid, no filtering','cases':out,
        'resources':{'seconds':time.perf_counter()-start,'rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'processes':1,'usd':0,'alarm_seconds':60,'memory_budget_bytes':536870912}}
    assert result['resources']['rss_bytes']<536870912
    (ROOT/'stage1-certified-pairs.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'cases':{n:r['summary'] for n,r in out.items()},'resources':result['resources']}))
if __name__=='__main__':main()
