"""A map is a single-valued set of pairlists"""
from pio import *
from pop import *

def MapC(s,f):
    """ create a map by running over set s applying function f """
    fs = EmptyMap
    while s != EmptyMap:
        x,s =AddD(s)
        fs = Extend(fs,x,f(x))
    return fs
    
    
def Apply(m,x):
    """ apply m to x returning True, m(x) if x in domain of m"""
    """otherwise, False, None"""
    while not EmptySetP(m):
        p,m = AddD(m)
        a,b = List2D(p)
        if EqualP(a,x): return True,b
       # WriteItem(a);print(' ');WriteItemln(x)
    return False, None
    
def SafeApply(m,x):
    """ apply knowing x is in the domain of m """
    while not EmptySet(m):
        p,m = DeMember(m)
        a,b = List2D(p)
        if EqualP(a,x): return b
    assert False, 'safeapply not safely applied'
    
def Extend(m,x,y):
    """extend m by adding m(x)=y"""
    return SafeAdd(List2(x,y),m)
    
def MapS(m,a,b):
    """modify or extend m so m(a)=b"""
    n = EmptySet
    while not EmptySetP(m):
        p,m = DeMember(m)
        x,y = List2D(p)
        if EqualP(x,a):  #found a
            m = Add(List2(a,b),m)
            return Union(m,n)
        else:
            n = Add(p,n)
    return Add(List2(a,b),n) #never found a
    
def Range(m):
    """ the range of map m """
    r = EmptySet
    while not EmptySetP(m):
        p,m = DeMember(m)
        a,b = List2D(p)
        r = Add(b,r)
    return r
    
def Domain(m):
    """ the domain of map m """
    d = EmptySet
    while not EmptySetP(m):
        p,m = DeMember(m)
        a,b = List2D(p)
        d = SafeAdd(a,d)
    return d
    
def Star(m,s):
    """ {m(x): x in s} """
    r = EmptySet
    while not EmptySetP(s):
        x,s = DeMember(s)
        ok,y = Apply(m,x)
        if ok: r = Add(y,r)
    return r
        
def Compose(m1,m2):
    """composition of m1 and m2"""
    cm = EmptySet
    n1 = m1
    while not EmptySetP(n1):
        e1,n1 = DeMember(n1)
        x1,y1 = List2D(e1)
        n2 = m2
        while not EmptySetP(n2):
            e2,n2 = DeMember(n2)
            x2,y2 = List2D(e2)
            if EqualP(y1,x2):
                cm = Extend(cm,x1,y2)
    return cm

def Update(f,g):
    """ union of f and g with g overriding f """
    f1 = Restrict(f,Difference(Domain(f),Domain(g)))
    return DisjointUnion(f1,g)
    
def Restrict(m,s):
    """ m restricted to set s """
    f = EmptySet
    while not EmptySetP(m):
        p,m = DeMember(m)
        x,y = List2D(p)
        if Member(x,s):
            f = SafeAdd(p,f)
        else:
            continue
    return f
    
EmptyMap = EmptySet
    
efdict = Popliteral('{[dog chien][cat chat][mouse sourie]}')
fgdict = Popliteral('{[chien Hund][chat Katze][sourie Maus]}')
animals = Popliteral('{cat dog}')
efdictdelta = Popliteral('{[bird oiseau][pig cochon]}')