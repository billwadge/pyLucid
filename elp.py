""" eliminate where and whereloop clauses"""
from map import *
from pop import *
from exp import *
import pio,prs,prp

def Bump(am,s):
    """ up grade active map by bumping values of m and mapping members of s to 0"""
    #print('Current map ',pio.Items(am),' ',pio.Items(s))
    uam = Empty
    while am != EmptyMap:
        p,am = AddD(am)
        px,py = El1(p), El2(p)
        upy = NumC(1 + NumVal(py))
        uam = Extend(uam,px,upy)
    s0 = MapC(s,Zero)
    am1 = Update(uam,s0)
    #print('New map is ',pio.Items(am1))
    return am1
    
def Zero(x):
    return NumC(0)

def Eloop(t,am):
    #print('Elooping ',pio.Items(t),' ',pio.Items(am))
    """ hereditarily turn whereloops into wheres using active and contemp"""
    if LiteralP(t): return t
    
    if VarP(t): return Activate(t,am)
     
    if OperationP(t):
        o,opds = OperationD(t)
        eopds = Empty
        while opds != Empty:
            opd,opds = ConsD(opds)
            eopd = Eloop(opd,am)
            eopds = Append(eopds,List1(eopd))
        return OperationC(o,eopds)
        
    if CallP(t):
        fun,args = CallD(t)
        eargs = Empty
        while args != Empty:
            arg,args = ConsD(args)
            earg = Eloop(arg,am)
            eargs = Append(eargs,List1(earg))
        return CallC(fun,eargs)
        
    if WhereReallyP(t):
        #print("WhR ", pio.Items(t))
        subj,wk,body = WhereD(t)
        locals = WhereLocalsL(t)
        localsset = Elements(locals)
        l0 = MapC(localsset,Zero)
        aml = Update(am,l0)
        #print('Updated aml ',pio.Items(aml))
        esubj = Eloop(subj,aml)
        ebody = ConsAll2(body,Eloop,aml)
        return WhereC(esubj,wk,ebody)
        
    if WhereLoopP(t):
        subj,wk,body = WhereD(t)
        locals = WhereLocalsL(t)
        localsset = Elements(locals)
        aml = Bump(am,localsset)
        esubj = Operation1C(CONTEMPWord,Eloop(subj,aml))
        ebody = ConsAll2(body,Eloop,aml)
        return WhereC(esubj,WHEREWord,ebody)
        
    if VarDefinitionP(t):
        v, es, rhs = VarDefinitionD(t)
        erhs = Eloop(rhs,am)
        return VarDefinitionC(v,es,erhs)
        
    if FunDefinitionP(t):
       fun, formals,es,rhs = FunDefinitionD(t)
       am1 = Update(am,MapC(Elements(formals),Zero))
       erhs = Eloop(rhs,am1)
       return FunDefinitionC(fun,formals,es,erhs)
       
    print('Cannot Eloop ',pio.Items(t));exit()
       
def Activate(v,m):
    """apply appropriate number of actives """
    t = v
    ok,pn = Apply(m,Var(v))
    assert ok, 'unmapped var '+str(v)
    if not ok: print( str(v)+" not mapped");exit()
    n = NumVal(pn)
    for i in range(n):
        t = Operation1C(ACTIVEWord,t)
    return t
    

if __name__ == "__main__":
    pg = prs.ParseFile("loopprog.lu")
    epg = Eloop(pg,EmptyMap)
    prp.Termln(epg)
    
        