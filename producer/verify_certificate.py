"""Standalone Fraction verifier: Sturm, algebraic ODE jets, dual Jacobian.
Reads only certificate.json, imports no producer/CAS and installs nothing.
"""
from fractions import Fraction as Q
from pathlib import Path
import json,time,math,resource
from limits import start
start();began=time.perf_counter();ROOT=Path(__file__).resolve().parent
def trim(a):
    a=list(a)
    while len(a)>1 and not a[-1]:a.pop()
    return a
def plus(a,b):return trim([(a[i] if i<len(a) else Q(0))+(b[i] if i<len(b) else Q(0)) for i in range(max(len(a),len(b)))])
def scale(a,c):return trim([v*c for v in a])
def times(a,b):
    out=[Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return trim(out)
def divmodp(a,b):
    a=trim(a);b=trim(b);assert b!=[0]
    quo=[Q(0)]*max(1,len(a)-len(b)+1)
    while a!=[0] and len(a)>=len(b):
        c=a[-1]/b[-1];n=len(a)-len(b);quo[n]=c
        a=plus(a,scale([Q(0)]*n+b,-c))
    return trim(quo),a
def inverse(a,f):
    r0,r1=f,a;t0,t1=[Q(0)],[Q(1)]
    while r1!=[0]:
        quo,r2=divmodp(r0,r1);r0,r1=r1,r2;t0,t1=t1,plus(t0,scale(times(quo,t1),-1))
    assert len(r0)==1 and r0[0]
    return divmodp(scale(t0,1/r0[0]),f)[1]
def at(a,x):
    z=Q(0)
    for c in reversed(a):z=z*x+c
    return z
def sturm_count(f,l,r):
    seq=[f,[i*f[i] for i in range(1,len(f))]]
    while True:
        rem=divmodp(seq[-2],seq[-1])[1]
        if rem==[0]:break
        seq.append(scale(rem,-1))
    def changes(x):
        signs=[1 if z>0 else -1 for p in seq if (z:=at(p,x))]
        return sum(a!=b for a,b in zip(signs,signs[1:]))
    assert at(f,l) and at(f,r)
    return changes(l)-changes(r)
def ia(a,b):return a[0]+b[0],a[1]+b[1]
def im(a,b):
    v=[x*y for x in a for y in b];return min(v),max(v)
def interval(p,box):
    z=(Q(0),Q(0))
    for c in reversed(p):z=ia(im(z,box),(c,c))
    return z
class A:
    f=None
    def __init__(self,p=0):self.p=divmodp(list(p) if isinstance(p,(tuple,list)) else [Q(p)],A.f)[1]
    def __add__(self,b):
        if not isinstance(b,A):b=A(b)
        return A(plus(self.p,b.p))
    __radd__=__add__
    def __neg__(self):return A(scale(self.p,-1))
    def __sub__(self,b):return self+-b if isinstance(b,A) else self+A(-b)
    def __rsub__(self,b):return A(b)+-self
    def __mul__(self,b):
        if not isinstance(b,A):b=A(b)
        return A(times(self.p,b.p))
    __rmul__=__mul__
    def __truediv__(self,b):
        if not isinstance(b,A):b=A(b)
        return self*A(inverse(b.p,A.f))
    def __rtruediv__(self,b):return A(b)/self
    def __eq__(self,b):return self.p==(b.p if isinstance(b,A) else A(b).p)
    def __bool__(self):return self.p!=[0]
class Dual:
    def __init__(self,v,d=None):self.v=v if isinstance(v,A) else A(v);self.d=d or [A(0) for _ in range(5)]
    def __add__(self,b):
        b=b if isinstance(b,Dual) else Dual(b);return Dual(self.v+b.v,[x+y for x,y in zip(self.d,b.d)])
    __radd__=__add__
    def __neg__(self):return Dual(-self.v,[-x for x in self.d])
    def __sub__(self,b):return self+-b if isinstance(b,Dual) else self+Dual(-b)
    def __rsub__(self,b):return Dual(b)+-self
    def __mul__(self,b):
        b=b if isinstance(b,Dual) else Dual(b);return Dual(self.v*b.v,[x*b.v+self.v*y for x,y in zip(self.d,b.d)])
    __rmul__=__mul__
    def __truediv__(self,b):
        b=b if isinstance(b,Dual) else Dual(b)
        return Dual(self.v/b.v,[(x*b.v-self.v*y)/(b.v*b.v) for x,y in zip(self.d,b.d)])
    def __rtruediv__(self,b):return Dual(b)/self
def conv(a,b,n):return [sum((a[i]*b[j-i] for i in range(j+1)),0) for j in range(n+1)]
def inv(a,n):
    b=[1/a[0]]
    for j in range(1,n+1):b.append(-sum((a[i]*b[j-i] for i in range(1,j+1)),0)/a[0])
    return b
def trajectory(k,point):
    # A separate derivative-carrying recurrence for (S,I,h), h=1/Z.
    values=[Dual(v,[A(int(i==j)) for j in range(5)]) for i,v in enumerate(point)]
    a,g,sv,yv,hv=values;ss,yy,hh=[sv],[yv],[hv]
    for n in range(5):
        flow=conv(conv(ss,yy,n),hh,n);dy=[flow[j]-g*yy[j] for j in range(n+1)]
        u=[1+a*yy[0]]+[a*z for z in yy[1:]]
        dh=conv(conv(dy,hh,n),inv(u,n),n)
        ss.append(-flow[n]/(n+1));yy.append(dy[n]/(n+1));hh.append(-k*a*dh[n]/(n+1))
    return [z*math.factorial(i) for i,z in enumerate(yy)]
def det(matrix):
    a=[row[:] for row in matrix];d=A(1)
    for j in range(len(a)):
        pivot=next((i for i in range(j,len(a)) if a[i][j]),None)
        if pivot is None:return A(0)
        if pivot!=j:a[j],a[pivot]=a[pivot],a[j];d=-d
        p=a[j][j];d=d*p
        for i in range(j+1,len(a)):
            t=a[i][j]/p
            for h in range(j,len(a)):a[i][h]=a[i][h]-t*a[j][h]
    return d
def vals(a):return [str(z) for z in a.p]
records=[]
for row in json.loads((ROOT/'output/certificate.json').read_text())['cases']:
    tick=time.perf_counter();A.f=list(map(Q,row['polynomial_ascending']));box=tuple(map(Q,row['root_interval']))
    assert sturm_count(A.f,*box)==1 and 0<box[0]<box[1]<1 and not(box[0]<=Q(1,2)<=box[1])
    q=A([0,1]);g=A(list(map(Q,row['gamma_ascending'])));k=Q(row['k'])
    y=A(1);v=A(1);w=A(Q(row['jets_0_to_5'][2]));r=v+g*y
    F=y*w-v*v+k*q*v*y*r
    a=q/(1-q*y);S=-y*r*r/F;Z=-y*y*r/F;h=1/Z
    positive={name:interval(z.p,box) for name,z in [('alpha',a),('gamma',g),('S',S),('Z',Z),('R',9-S)]}
    # Reduced remainders can have cancellation; the sealed isolating interval
    # is narrow enough for these rational interval bounds to be decisive.
    assert all(pair[0]>0 for pair in positive.values()),positive
    alt=trajectory(k,[a,g,S,y,h]);true=trajectory(k,list(map(Q,row['true_alpha_gamma_S_I_h'])))
    expected=list(map(Q,row['jets_0_to_5']))
    assert all(z.v==expected[i] for i,z in enumerate(true))
    assert all(alt[i].v==expected[i] for i in range(5))
    difference=alt[5].v-true[5].v
    inverse(difference.p,A.f) # no root of f can make this difference zero
    dt=det([z.d for z in true[:5]]);da=det([z.d for z in alt[:5]])
    assert dt and da
    inverse(da.p,A.f);inverse(dt.p,A.f)
    di=interval(da.p,box);assert di[0]*di[1]>0
    records.append({'k':str(k),'sturm_roots_in_interval':1,'positive_intervals':{n:[str(v) for v in b] for n,b in positive.items()},
        'same_jet_orders':list(range(5)),'fifth_jet_difference_mod_polynomial':vals(difference),
        'true_J4_jacobian_determinant':vals(dt),'alternate_J4_jacobian_determinant':vals(da),
        'alternate_determinant_interval':[str(z) for z in di],
        'determinants_and_fifth_difference_coprime_to_root_polynomial':True,'seconds':time.perf_counter()-tick})
    print('Verified',k,'same J4, distinct J5, both 5x5 Jacobians nonzero',flush=True)
out={'status':'PASS','implementation':'Python stdlib Fraction; Sturm + polynomial quotient arithmetic + dual-number Taylor recurrence','cases':records,'seconds':time.perf_counter()-began,'max_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(ROOT/'output/certificate-check.json').write_text(json.dumps(out,indent=2)+'\n')
print('seconds',out['seconds'])
