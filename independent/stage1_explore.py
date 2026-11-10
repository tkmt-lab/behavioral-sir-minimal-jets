#!/usr/bin/env python3
"""Exploration from ODE only. No producer source reads, no prior model formulas."""
from fractions import Fraction as Q
import math,json,time,signal,resource
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def mul(a,b,n):return [sum((a[j]*b[i-j] for j in range(i+1)),0) for i in range(n+1)]
def flow(y,q,b,p,g,k,N=5):
    yy,qq,bb,pp=[y],[q],[b],[p]
    for n in range(N):
        qm=[qq[0]-g]+qq[1:]
        dy=mul(yy,qm,n)
        qyb=mul(mul(qq,yy,n),bb,n);pdy=mul(pp,dy,n)
        dq=[-qyb[i]-k*z for i,z in enumerate(mul(pdy,qq,n))]
        db=[-k*z for z in mul(pdy,bb,n)]
        dp=[-z for z in mul(pp,pdy,n)]
        for st,rhs in zip((yy,qq,bb,pp),(dy,dq,db,dp)):st.append(rhs[n]/(n+1))
    return [x*math.factorial(i) for i,x in enumerate(yy)]

class Dual:
    def __init__(self,a,da=0,db=0):
        if isinstance(a,Dual):self.v,self.a,self.b=a.v,a.a,a.b
        else:self.v,self.a,self.b=a,da,db
    def __add__(self,b):b=Dual(b);return Dual(self.v+b.v,self.a+b.a,self.b+b.b)
    __radd__=__add__
    def __neg__(self):return Dual(-self.v,-self.a,-self.b)
    def __sub__(self,b):return self+-Dual(b)
    def __rsub__(self,b):return Dual(b)+-self
    def __mul__(self,b):b=Dual(b);return Dual(self.v*b.v,self.a*b.v+self.v*b.a,self.b*b.v+self.v*b.b)
    __rmul__=__mul__
    def __truediv__(self,b):
        b=Dual(b);return Dual(self.v/b.v,(self.a*b.v-self.v*b.a)/(b.v*b.v),(self.b*b.v-self.v*b.b)/(b.v*b.v))
    def __rtruediv__(self,b):return Dual(b)/self

def reconstruct(y,v,w,p,q,k):
    g=q-v/y;c=w/y-v*v/(y*y)
    b=-c/(q*y)-k*p*v/y
    return g,b

def solve_pair(y,v,w,t,z,p,q,k):
    for i in range(40):
        if abs(q)<1e-9:return None
        pd,qd=Dual(p,1,0),Dual(q,0,1)
        g,b=reconstruct(y,v,w,pd,qd,k)
        jj=flow(y,qd,b,pd,g,k,4);f=jj[3]-t;h=jj[4]-z
        det=f.a*h.b-f.b*h.a
        if abs(det)<1e-14:return None
        dp=(-f.v*h.b+f.b*h.v)/det;dq=(-f.a*h.v+f.v*h.a)/det
        p+=dp;q+=dq
        if not math.isfinite(p+q) or abs(p)+abs(q)>1e5:return None
        if abs(dp)+abs(dq)<1e-10:
            g,b=reconstruct(y,v,w,p,q,k)
            if p>0 and p*y<1 and g>0 and b>0:
                return p,q,g,b,det
            return None
    return None

def main():
    start=time.perf_counter();signal.alarm(60);out=[]
    for k in [2.,3.,2.5,3.5,1+math.sqrt(2)]:
        y,q,b,p,g=1.,2.,1.,.5,1.;j=flow(y,q,b,p,g,k)
        roots=[]
        for pp in [.05,.2,.4,.6,.8,.95]:
            for qq in [.2,.5,1,2,3,5,8,12]:
                r=solve_pair(*j[:5],pp,qq,k)
                if r and all(abs(r[0]-s[0])+abs(r[1]-s[1])>1e-6 for s in roots):roots.append(r)
        vals=[]
        for pp,qq,gg,bb,det in roots:
            vals.append({'p':pp,'q':qq,'g':gg,'b':bb,'a':pp/(1-pp*y),'S':qq/bb,'Z':1/bb,'det_2x2':det,'jets':flow(y,qq,bb,pp,gg,k)})
        out.append({'k':k,'true_jets':j,'positive_roots_found_numerically':vals})
    result={'exploratory_not_certificate':True,'fixed_grid_p':[.05,.2,.4,.6,.8,.95],'fixed_grid_q':[.2,.5,1,2,3,5,8,12],'cases':out,'seconds':time.perf_counter()-start,'rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    (ROOT/'stage1-exploration.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
if __name__=='__main__':main()
