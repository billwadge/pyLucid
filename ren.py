""" rename a program so logically distinct variables have different names,
    similar to their original ones """
import pop,pio,prp,map,prs
from exp import *
    
def Rename(t,m):
    """ return t renamed according to map m """
    if LiteralP(t): return t
    if VarP(t):
        v = Var(t)
        ok, w = map.Apply(m,v)
        if not ok:
            print('Variable not in rename map '+pio.Items(v))
            exit()
        return VarC(w)
    if OperationP(t):
        o, opds = DeOperation(t)
        ropds = pop.ConsAll2(opds,Rename,m)
        return OperationC(o,ropds)
    if WhereP(t):
        subj, body = DeWhere(t)
        l = WhereLocalsL(t)
        n = NewMap(l)
        m1 = map.Update(m,n)
        rsubj = Rename(subj,m1)
        rbody = pop.ConsAll2(body,Rename,m1)
        return WhereC(rsubj,rbody)
    if DefinitionP(t):
        lhs, rhs = DeDefinition(t)
        if VarP(lhs):
            return DefinitionC(Rename(lhs,m),Rename(rhs,m))
        l = CallActualsL(lhs)
        lv = pop.ConsAll(l,Var)
        n = NewMap(lv)
        m1 = map.Update(m,n)
        return DefinitionC(Rename(lhs,m1),Rename(rhs,m1))
    if CallP(t):
        fun,actsl = DeCall(t)
        rfun = Rename(fun,m)
        ractsl = pop.ConsAll2(actsl,Rename,m)
        return CallC(rfun,ractsl)
    assert False, 'rename a strange term '+str(t)
        
def NewMap(l):
    rmap = pop.EmptySet
    while l != pop.Empty:
        h,l = pop.DeCons(l)
        rh = NewVar(h)
        rmap = map.Extend(rmap,h,rh)
    return rmap
    
varcount = map.EmptyMap
    
def NewVar(v):
    global varcount
    ok,n = map.Apply(varcount,v)
    if not ok: map.Extend(varcount,v,0);n=0
    suffix = str(n)
    varcount = map.MapS(varcount,v,n+1)
    if n !=0: 
        rvname = pop.WordName(v)+'_'+suffix
    else:
        rvname = pop.WordName(v)
    return pop.WordC(rvname)
    

if __name__ == "__main__":
    pg = prs.ParseFile("testprog.lu")
    rpg = Rename(pg,pop.EmptySet)
    prp.Term(rpg)
    print()