#!/usr/bin/env python3
"""Read saved certificate data, never its producer/verifier implementation.
Own polynomial quotient, Sturm, 5-variable AD, and polynomial-state solver.
"""
import sys
sys.dont_write_bytecode=True
from stage1_explore import flow
from certify_pairs import I
from fractions import Fraction as Q
from pathlib import Path
import subprocess,json,hashlib,time,resource,signal,itertools
ROOT=Path(__file__).resolve().parent
COMMIT='a4fcc3f75d7cfc8c972a2a4e579a705edabbc8cc'
def trim(a):
    a=list(a)
    while a and not a[-1]:a.pop()
    return a

def add(a,b):return trim([(a[i] if i<len(a) else Q(0))+(b[i] if i<len(b) else Q(0)) for i in range(max(len(a),len(b)))])
def neg(a):return [-v for v in a]
def sub(a,b):return add(a,neg(b))
def mul(a,b):
    c=[Q(0)]*max(0,len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return trim(c)
def divmodp(a,b):
    a=trim(a);b=trim(b);assert b;q=[Q(0)]*max(0,len(a)-len(b)+1)
    while a and len(a)>=len(b):
        d=len(a)-len(b);c=a[-1]/b[-1];q[d]=c
        a=sub(a,[Q(0)]*d+[c*x for x in b])
    return trim(q),a

def gcdex(a,b):
    s0,s1,t0,t1=[Q(1)],[],[],[Q(1)]
    while b:
        q,r=divmodp(a,b);a,b=b,r;s0,s1=s1,sub(s0,mul(q,s1));t0,t1=t1,sub(t0,mul(q,t1))
    scale=a[-1];return [x/scale for x in a],[x/scale for x in s0],[x/scale for x in t0]

def peval(a,x):
    out=x*0
    for v in reversed(a):out=out*x+v
    return out

def sturm(a,lo,hi):
    seq=[a,[Q(i)*a[i] for i in range(1,len(a))]]
    while seq[-1]:
        r=neg(divmodp(seq[-2],seq[-1])[1])
        if not r:break
        seq.append(r)
    signs=lambda x:[1 if z>0 else -1 for p in seq if (z:=peval(p,x))]
    count=lambda ss:sum(a!=b for a,b in zip(ss,ss[1:]))
    l,h=signs(lo),signs(hi)
    return count(l)-count(h),{'sequence':[[str(x) for x in p] for p in seq],'signs_left':l,'signs_right':h}

MOD=[]
class R:
    def __init__(self,x=0):
        if isinstance(x,R):self.c=x.c[:]
        else:self.c=divmodp([Q(z) for z in x] if isinstance(x,list) else [Q(x)],MOD)[1]
    def __add__(self,b):
        if isinstance(b,AD):return NotImplemented
        return R(add(self.c,R(b).c))
    __radd__=__add__
    def __neg__(self):return R(neg(self.c))
    def __sub__(self,b):return self+-R(b)
    def __rsub__(self,b):return R(b)+-self
    def __mul__(self,b):
        if isinstance(b,AD):return NotImplemented
        return R(mul(self.c,R(b).c))
    __rmul__=__mul__
    def __truediv__(self,b):
        if isinstance(b,AD):return NotImplemented
        b=R(b);g,s,t=gcdex(b.c,MOD);assert g==[Q(1)];return self*R(s)
    def __rtruediv__(self,b):return R(b)/self
    def __bool__(self):return bool(self.c)
    def __eq__(self,b):return self.c==R(b).c
    def row(self):return [str(x) for x in self.c]

class AD:
    def __init__(self,v,d=None):
        if isinstance(v,AD):self.v,self.d=v.v,v.d;return
        self.v=v;self.d=[v*0]*5 if d is None else d
    def __add__(self,b):b=AD(b);return AD(self.v+b.v,[x+y for x,y in zip(self.d,b.d)])
    __radd__=__add__
    def __neg__(self):return AD(-self.v,[-x for x in self.d])
    def __sub__(self,b):return self+-AD(b)
    def __rsub__(self,b):return AD(b)+-self
    def __mul__(self,b):b=AD(b);return AD(self.v*b.v,[x*b.v+self.v*y for x,y in zip(self.d,b.d)])
    __rmul__=__mul__
    def __truediv__(self,b):b=AD(b);return AD(self.v/b.v,[(x*b.v-self.v*y)/(b.v*b.v) for x,y in zip(self.d,b.d)])
    def __rtruediv__(self,b):return AD(b)/self

def determinant(a):
    out=a[0][0]*0
    for perm in itertools.permutations(range(5)):
        sign=(-1)**sum(perm[i]>perm[j] for i in range(5) for j in range(i+1,5));prod=sign
        for i in range(5):prod=prod*a[i][perm[i]]
        out+=prod
    return out

def original_jac(vals,k):
    zz=[]
    for i,v in enumerate(vals):zz.append(AD(v,[v*0+int(i==j) for j in range(5)]))
    a,g,S,y,h=zz;p=a/(1+a*y);q=S*h
    jets=flow(y,q,h,p,g,k,5)
    return [x.v for x in jets],determinant([x.d for x in jets[:5]])

def main():
    global MOD
    start=time.perf_counter();signal.alarm(60)
    paths=['producer/output/certificate.json','producer/output/certificate-check.json']
    blobs={p:(ROOT.parent/'producer/output'/Path(p).name).read_bytes() for p in paths}
    cert=json.loads(blobs[paths[0]]);receipt=json.loads(blobs[paths[1]]);out=[]
    ownpairs=json.loads((ROOT/'stage1-certified-pairs.json').read_text())['cases']
    for source,rec in zip(cert['cases'],receipt['cases']):
        k=Q(source['k']);MOD=[Q(x) for x in source['polynomial_ascending']];lo,hi=map(Q,source['root_interval']);assert 0<lo<hi<1 and not lo<=Q(1,2)<=hi
        count,st=sturm(MOD,lo,hi);assert count==1
        count01,st01=sturm(MOD,Q(0),Q(1))
        p=R([0,1]);g=R([Q(x) for x in source['gamma_ascending']]);q=g+1
        jets=[Q(x) for x in source['jets_0_to_5']];b=-(jets[2]-1)/q-k*p
        a=p/(1-p);S=q/b;Z=1/b
        ownjets,det=original_jac([a,g,S,R(1),b],k)
        assert ownjets[:5]==[R(x) for x in jets[:5]]
        truejets,td=original_jac([Q(1),Q(1),Q(2),Q(1),Q(1)],k);assert truejets==jets
        assert R(rec['true_J4_jacobian_determinant'])==td
        gap=ownjets[5]-jets[5]
        assert gap==R(rec['fifth_jet_difference_mod_polynomial'])
        assert det==R(rec['alternate_J4_jacobian_determinant'])
        assert gcdex(det.c,MOD)[0]==[1] and gcdex(gap.c,MOD)[0]==[1]
        interval=I(lo,hi)
        vals={'alpha':a,'gamma':g,'S':S,'Z':Z,'R':R(9)-S}
        bounds={key:peval(value.c,interval) for key,value in vals.items()}
        assert all(v.lo>0 for v in bounds.values())
        di=peval(det.c,interval);gi=peval(gap.c,interval);assert not di.lo<=0<=di.hi and not gi.lo<=0<=gi.hi
        box=[list(map(Q,x)) for x in ownpairs[source['k']]['root_box_p_q']]
        qi=peval(q.c,interval)
        assert box[0][0]<lo<hi<box[0][1] and box[1][0]<qi.lo<=qi.hi<box[1][1]
        out.append({'k':str(k),'sturm_count_in_interval':count,'sturm':st,'sturm_count_in_0_1':count01,
            'positive_bounds':{key:v.row() for key,v in bounds.items()},'jet_0_to_4_residuals':[v.row() for v in [ownjets[i]-jets[i] for i in range(5)]],
            'fifth_difference':gap.row(),'fifth_difference_interval':gi.row(),'true_full_jacobian':str(td),'alternate_full_jacobian':det.row(),'alternate_full_jacobian_interval':di.row(),
            'gcds_with_modulus_equal_one':True,'source_root_inside_own_precommitted_Krawczyk_box':True})
    result={'input_commit':COMMIT,'implementation':'own stdlib quotient/Sturm/5D-AD; own polynomial-state ODE',
       'source':{p:{'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for p,b in blobs.items()},'cases':out,
       'resources':{'seconds':time.perf_counter()-start,'rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'usd':0,'alarm_seconds':60}}
    (ROOT/'source-certificate-check.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'cases':[{'k':r['k'],'sturm':r['sturm_count_in_interval'],'roots_0_1':r['sturm_count_in_0_1'],'true_jacobian':r['true_full_jacobian'],'source_root_inside_own_box':r['source_root_inside_own_precommitted_Krawczyk_box']} for r in out],'resources':result['resources']}))
if __name__=='__main__':main()
