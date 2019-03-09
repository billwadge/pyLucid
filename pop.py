# An implementation of pop2 data types in python
#numbers are ('n',n) n a python number
#lists are ('l',[h,t]) h a popitem t a poplist
#empty list ('l',[])
#words are ('w',s) s a python string
#strings are ('s',s) s a python string
#sets are ('e',els) els like a list
#empty set is ('e',[])
#

import pio

def ForAll(l,p):
    """ run down list or set checking of p is true of every element """
    m,els = l
    if m=='e': l = ('l',els) #if l a set make it a list
    #print('->')
    while l != Empty:
        #print('-- '+pio.Items(l))
        h,l = DeCons(l)
        #print('-^ '+pio.Items(l)+"$$"+pio.Items(h))
        if not p(h): return False
    return True
    
def ForSome(l,p):
    """ check if p is true of some element """
    m,els = l
    if m=='e': l = ('l',els) #if l a set make it a list
    while l != Empty:
        h,l = DeCons(l)
        if  p(h):return True
    return False
    
def Filter(l,p):
    """ return a list of those elements of l for which p is true """
    m,els = l
    if m=='e': l = ('l',els) #if l a set make it a list
    res = Empty
    while l != Empty:
        h,l = DeCons(l)
        if p(h):
            res = Append(res,List1(h))
    m1, els1 = res
    return (m,els1)
    

def NumC(n):
    assert type(n)==int or type(n)==float,'numc given non number'
    return ('n',n)

def StringC(s): #create a popstring corresponding to  python string s
    assert type(s)==str,'stringc given a non string'
    return ('s',s)

def WordC(s): #create a popword  with name python string s
    assert type(s)==str,'wordc on a nonstring'
    assert len(s)!=0,'wordc on the empty string'
    return ('w',s)
    
def BoolC(b):
    if b: return TRUEWord
    return FALSEWord

    
Empty = ('l',[])
def BoolVal(i):
    return i == TRUEWord
    

def EodP(i):
    return i == EODWord
    
def EosP(i):
    return i == EOSWord

def EmptyP(l):
    if ListP(l): return l == Empty
    if SetP(l): return l == EmptySet
    assert False, 'emptyp given bogus argument  '+str(l)
    
def Head(pl): #the head of poplist pl
    k,l = pl
    assert k=='l','Head given nonlist '+str(pl)
    assert l != [],'head given empty list'
    h,t = l
    return h

def Tail(pl): #the tail of pop list pl
    k,l = pl
    assert k=='l','Tail given nonlist' + str(pl)
    assert l != [],'Tail given empty list'
    h,t = l
    return ('l',t)

def Cons(h,pl): #result of consing popitem h on the head of poplist pl
    k,l = pl   
    assert k=='l','cons given a non list'
    return ('l',[h,l])
    
def AddElement(l,e):
    return Append(l,List1(e))
    
def DeCons(pl):
    assert not EmptyP(pl), 'Hail expects nonempty list'
    return Head(pl),Tail(pl)

def ConsD(pl):
    #assert not EmptyP(pl), 'ConsD expects nonempty list'+str(pl)
    k,l =pl
    h,t=l
    return h, ('l',t)
    #return Head(pl),Tail(pl)
"""
def Dups(l):
    #duplicates in list l of words
    assert False, 'dups '+str(l)
    if EmptyP(l): return Empty
    h,t = DeCons(l)
    if Occurs(h,l):
        return Cons(h,Dups(t))
    else:
        return Dups(t)
"""
def Occurs(x,l):
    while l != Empty:
        h,l = DeCons(l)
        if EqualP(h,x): return  True
    return False
    
    
def HeadA(pl,h1):
    """ change the head of list pl to be h1 """
    k,l = pl
    assert k=='l', 'HeadA given nonlist'
    assert l != [], 'HeadA given empty list '
    l[0] = h1
    
def TailA(pl,t1):
    """ change the tail of list pl to be t1 """
    k,l = pl
    assert k=='l', 'TailA given nonlist'
    assert l != [], 'TailA given empty list '
    m,r1 = t1
    l[1] =r1
    
def Length(l):
    assert ListP(l), 'Length given nonlist '+str(l)
    n = 0
    while l != Empty:
        h,l = DeCons(l)
        n = n+1
    return n
        
def ListCopy(pl):
    """ return a fresh copy of pl """
    k,l = pl
    assert k=='l', 'ListCopy given non list'
    if l == []: return []
    h,t = l
    t = PyListCopy(t)
    if ListP(h): h = ListCopy(h)
    return ('l',[h,t])
    
    
    
def PyListCopy(pyl):
    assert isinstance(pyl,list), 'PyListCopy given non python list'
    if pyl  == [] :  return []
    pyh,pyt = pyl
    if ListP(pyh): pyh = ListCopy(pyh)
    pyt = PyListCopy(pyt)
    return [pyh,pyt]
    
def Reverse(l):
    assert ListP(l), 'Reverse given non list'
    if EmptyP(l): return l
    rl = Empty
    while l != Empty:
        rl = Cons(Head(l),rl)
        l = Tail(l)
    return rl
    
def Append(l1,l2):
    assert ListP(l1), 'first arg of Append non list'+str(l1)
    assert ListP(l2), 'second arg of Append non list'+str(l2)
    if EmptyP(l1): return l2
    return Cons(Head(l1),Append(Tail(l1),l2))
    
def AppendAll(l,f):
    """ run down l applying f and appending the results """
    res = Empty
    while l !=  Empty:
       h,l = DeCons(l)
       res = Append(res,f(h))
    return res
    
def ConsAll(l,f):
    """ run down l applying f and consing the results (map) """
    m = Empty
    while l != Empty:
        h,l = DeCons(l)
        m = Append(m,List1(f(h)))
    return m
    
def DoAll(l,f):
    while not EmptyP(l):
        h,l = ConsD(l)
        f(h)
    
def ConsAll2(l,f,m):
    """ run down l applying f with parm m and consing the results (map) """
    fl = Empty
    while l != Empty:
        h,l = DeCons(l)
        fl = Append(fl,List1(f(h,m)))
    return fl
       
def Dups(l):
    """ returns set of items duplicated in l """
    dupl = EmptySet
    while l != Empty:
        x,l = DeCons(l)
        if Occurs(x,l): dupl = Add(x,dupl)
    #assert False, str(l)+str(dupl)
    return dupl

def List1(a):
    """a list of length 1 """
    return Cons(a,Empty)
    
def List2(a,b):
    """a list of length 2"""
    return Cons(a,List1(b))
    
def DeList2(l):
    return El1(l),El2(l)
    
def List3(a,b,c):
    """a list of length 3"""
    return Cons(a,List2(b,c))
    
def List4(a,b,c,d):
    """a list of length 4"""
    return Cons(a,List3(b,c,d))
    
def El1(k):
    """first element of k"""
    assert k!= Empty, 'El1 given empty ist'
    assert k != '', 'El1 given eod '
    return Head(k)
    
def El2(k):
    """second element of list"""
    return El1(Tail(k))
    
def El3(k):
   """third element of ist"""
   return El2(Tail(k))
   
def El4(k):
   """fourth element of list"""
   return El3(Tail(k))
   
def El(i,k):
    """ith element of k"""
    assert i>0, 'El given i<1'
    while i>1:
        k = Tail(k)
        i = i-1
    return Head(k)
    
def Length(l):
    n = 0
    while not EmptyP(l):
        n = n+1
        l = Tail(l)
    return n

def Fringe(l):
    """ linear list of all nonlists appearing in l, in order"""
    fr = Empty
    while not EmptyP(l):
        i,l = DeCons(l)
        if ListP(i):
            sfr = Fringe(i)
            fr = Append(fr,sfr)
        else:
            fr = Append(fr,Singleton(i))
    return fr
      
def EqualP(i1,i2):
    """Equality test between popitems"""
    m1,d1 = i1
    m2,d2 = i2
    if m1!=m2: return False
    if m1=='s' or m1=='w' or m1=='n':
        return d1==d2
    if m1 == 'e': return SetEqualP(i1,i2)
    if i1==Empty and i2==Empty: return True
    if i2==Empty or i2==Empty: return False
    if not EqualP(Head(i1),Head(i2)): return False
    return EqualP(Tail(i1),Tail(i2))
    
def ListP(i): #is it a poplist
    if not isinstance(i,tuple): return False #not a popitem
    k,d = i
    return k=='l'

def StringP(i): #is it a popstring
    k,d = i
    return k == 's'

def WordP(i): #is it a popword
    k,d = i
    return k == 'w'

def NumP(i):
    k,d = i
    return k == 'n'
    
def SetP(i):
    k,d = i
    return k == 'e'
    
def NumVal(pn):
    #print('Numval '+str(pn))
    k,i = pn
    assert k=='n', 'NumVal given non number '+str(pn)
    return i
    
def WordName(pw):
    k,s = pw
    assert k == 'w', 'Wordname given non word '+str(pw)
    return s
    
def StringVal(ps): #s as a python string
    k,s = ps
    assert k == 's', 'StringVal given nonstring'
    return s
    
#----------------- sets ------------------------


def Enumeration(s):
    """ return a list that enumerates elts of s """
    m, elts = s
    return ('l',elts)
    

def EmptySetP(s):
    return s == EmptySet
    

def Member(w,s):
    m, elts = s
    em = ('l',elts)         #change marker to make it a list
    return Occurs(w,em)

def Add(w,s):
    if Member(w,s):
        return s
    else:
        return SafeAdd(w,s)
        

def SafeAdd(w,s):
    m, elts = s
    return ('e',[w,elts])
        
def DeMember(s): 
    assert not EmptySetP(s), 'demember given empty set '
    assert SetP(s), 'demember given  non set '+str(s)
    m, els = s
    return els[0], ('e',els[1])
        
def AddD(s): 
    assert not EmptySetP(s), 'addd given empty set '
    assert SetP(s), 'add given  non set '+str(s)
    m, els = s
    return els[0], ('e',els[1])
    
def Union(r,s):
    # returns the union of r and s 
    if EmptySetP(r): return s;
    if EmptySetP(s): return r;
    while r != EmptySet:
       e,r = DeMember(r)
       s = Add(e,s)
    return s
    
def DisjointUnion(s1,s2):
    return SafeElements(Append(Enumeration(s1),Enumeration(s2)))
    

def Intersection(r,s):
    # returns the intersection of r and s 
    if EmptySetP(r): return EmptySet
    if EmptySetP(s): return EmptySet
    ints= EmptySet
    while not EmptySetP(r):
        e,r = DeMember(r)
        if Member(e,s): 
            ints = SafeAdd(e,ints)
        else:
            continue
    return ints


def Difference(r,s):
    d = EmptySet
    while not EmptySetP(r):
        e,r = DeMember(r)
        if Member(e,s):
            continue
        else:
            d = SafeAdd(e,d)
    return d
    

def Those(r,p):
    """set comprehension"""
    th = EmptySet
    while not EmptySetP(r):
        e,r = DeMember(r)
        if p(e):
            th = SafeAdd(e,th)
        else:
            continue
    return th
        

def UnionAll(s,f):
    """ union of the results of applying f to elements of s """
    un = EmptySet
    while not EmptyP(s):
        e,s = DeMember(s)
        un = Union(f(e),un)
    return un

def Singleton(x):
    return Add(x,EmptySet)
    
            
def NoDups(s):
    """ eliminate dups in an alleged set """
    t = EmptySet
    while not EmptySetP(s):
        e,s = DeMember(s)
        if Member(e,s):
            continue
        else:
            t = Add(e,t)
    return t
    
def Elements(l):
    """ set of all elements occurring in list l """
    m, els = l
    return NoDups(('e',els))
    
def SafeElements(l):
    """ set of all elements occurring in list l """
    """ no duplicates """
    m, els = l
    return ('e',els)
    
def Closure(s):
    """ transitive closure of s """
    tc = EmptySet
    while not EmptyP(s):
        e,s = DeMember(s)
        if SetP(e):
            tc = Add(e,tc)
        else:
            tc = Union(tc,Closure(e))
    return tc
            
"""
def Member(e,s)
    if EmptyP(s) return  False
    l, m, r = Split(s)
    if Less(e,m): return Member(e,l)
    if Less(m,e): return Member(e,r)
    return True
    
def Member(e,s)
    while True :
        if EmptyP(s): return false
        l, m, r = Split(s)
        if EqualP(e,m): return True
        if Less(e,m):
            s=l;
        else:
            s=r
            
def Union(s1,s2)
    if EmptyP(s1): return s2
    if EmptyP(s2): return s2
    l1,m1,r1 = Split(s1)
    l2,m2,r2 = Split(s2)
    if m1==m2 : return join(union(l1,l2),m1,union(l1,l2))
    if m1<m2.........
    
Add(x,s)
    if s==0 return Join(0,x,0)
    l,m,r = split(s)
    if x==m return s
    if x<m: return join(Add(x,l),m,r)
    else  : return join(l,m,Add(x,r))
    
        
"""

EmptySet = ('e',[])
OPWord = WordC('op')
VARWord =  WordC('var')
QUOTEWord = WordC('"')
DQUOTEWord = WordC('"')
IFWord = WordC("if")
THENWord = WordC("then")
ELSEWord = WordC("else")
FIWord = WordC("fi")
CALLWord = WordC("call")
YCALLWord = WordC("ycall")
ACTUALWord = WordC("actual")
GLOBALWord = WordC("global")
WHEREWord = WordC("where")
WHERELOOPWord = WordC("whereloop")
ENDWord = WordC("end")
EQUALWord = WordC("=")
SEMICOLONWord = WordC(";")
VALOFWord = WordC("valof")
LLISTPARENWord = WordC("[%")
RLISTPARENWord = WordC("%]")
LSETPARENWord = WordC("{%")
RSETPARENWord = WordC("%}")
OUTPUTWord = WordC("output")
IDWord = WordC("id")
EODWord = WordC("eod")
EOSWord = WordC("eos")

TRUEWord = WordC('true')
FALSEWord = WordC('false')
Eod = EODWord
Eos = EOSWord
