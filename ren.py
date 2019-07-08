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
            print('Undefined variable '+pio.Items(v))
            exit()
        return VarC(w)
    if OperationP(t):
        o, opds = OperationD(t)
        ropds = pop.ConsAll2(opds,Rename,m)
        return OperationC(o,ropds)
    if WhereP(t):
        subj, wk, body = WhereD(t)
        l = WhereLocalsL(t)
        n = NewMap(l)
        m1 = map.Update(m,n)
        rsubj = Rename(subj,m1)
        rbody = pop.Empty
        while body != pop.Empty: #run through definitions in body
            df,body = pop.ConsD(body)
            rdf = Rdefinition(df,m,m1)
            rbody = pop.Append(rbody,List1(rdf))
        return WhereC(rsubj,wk,rbody)

    if CallP(t):
        fun,actsl = CallD(t)
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
    
def Rdefinition(d,m,m1): #rename a definition m being the outer map
    lhs, es, rhs = DefinitionD(d)
    if es == EQUALWord:              #recursive definition
        if VarP(lhs):
            return DefinitionC(Rename(lhs,m1),EQUALWord,Rename(rhs,m1))
        l = CallActualsL(lhs)
        lv = pop.ConsAll(l,Var)
        n = NewMap(lv)
        n1 = map.Update(m1,n)
        return DefinitionC(Rename(lhs,n1),EQUALWord,Rename(rhs,n1))
        #nonrecursive definition
    if VarP(lhs):
        return DefinitionC(Rename(lhs,m1),EQUALWord,Rename(rhs,m)) #rhs renamed with outer map
    l = CallActualsL(lhs)
    lv = pop.ConsAll(l,Var)
    n = NewMap(lv)
    n1 = map.Update(m1,n)
    m2 = map.Update(m,n)
    return DefinitionC(Rename(lhs,n1),EQUALWord,Rename(rhs,m2))
    

if __name__ == "__main__":
    pg = prs.ParseFile("testprog.lu")
    rpg = Rename(pg,pop.EmptySet)
    prp.Term(rpg)
    print()