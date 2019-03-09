""" compile a table of function arities """
import pio, pop, map, prs, prp, ren
from exp import *

def Aritytab(e,m):
    """ compile a table of arities for funs in e """
    if LiteralP(e): return m
    if VarP(e): return m
    if OperationP(e):
        o, opds = OperationD(e)
        return AritytabList(opds,m)
    if WhereP(e):
        subj, wk, body = WhereD(e)
        m = Aritytab(subj,m)
        return AritytabList(body,m)
    if VarDefinitionP(e):
        v, es, rhs = VarDefinitionD(e)
        m = map.Extend(m,v,pop.NumC(0))
        return Aritytab(rhs,m)
    if FunDefinitionP(e):
        f, formals, es, rhs = FunDefinitionD(e)
        n = pop.Length(formals)
        while formals != pop.Empty:
           formal, formals = pop.ConsD(formals)
           m = map.Extend(m,formal,pop.NumC(0))
        m = map.Extend(m,f,pop.NumC(n))
        return Aritytab(rhs,m)
    if CallP(e):
        fun,actuals = CallD(e)
        return AritytabList(actuals,m)
    assert False, 'corrupt expression'+str(e)
    
def ArityCheck(e,m):
    """ check that the vars in e are used consistent with the arity map m """
    if LiteralP(e): return True, None, None
    if VarP(e):
        ok, n = map.Apply(m,Var(e))
        if not ok: print('undefined variable '+pio.Words(Var(e)));exit()
        if pop.NumVal(n) != 0: return False, Var(e), pop.NumVal(n)
        return True, None, None
    if OperationP(e): 
        o, opds = OperationD(e)
        return ArityCheckList(opds,m)
    if WhereP(e):
        subj, wk, body = WhereD(e)
        ok, var, n = ArityCheckList(body,m)
        if not ok: return False, var, n
        return ArityCheck(subj,m)
    if VarDefinitionP(e):
        v, es, rhs = VarDefinitionD(e)
        ok, n = map.Apply(m,v)
        if not ok: print( 'undefined variable '+str(v));exit()
        if pop.NumVal(n) != 0: return False, v, pop.NumVal(n)
        return ArityCheck(rhs,m)
    if FunDefinitionP(e):
        f, formals,es, rhs = FunDefinitionD(e)
        ok, n = map.Apply(m,f)
        if not ok: print( 'undefined variable '+str(f))
        if pop.NumVal(n) != pop.Length(formals): return False, f, pop.NumVal(n)
        return ArityCheck(rhs,m)
    if CallP(e):
        fun, actuals = CallD(e)
        ok, n = map.Apply(m,Var(fun))
        if not ok: 
            print('undefined var '+str(Var(fun)));
            exit()
        if pop.NumVal(n) != pop.Length(actuals):
            return False, Var(fun), pop.NumVal(n)
        return ArityCheckList(actuals,m)
    assert False, 'corrupt expression'+str(e)
    
def ArityCheckList(l,m):
    while l != pop.Empty:
        e,l = pop.ConsD(l)
        ok, v, n = ArityCheck(e,m)
        if not ok: return  False, v, n
    return True, None, None
        
       
       
    
def AritytabList(l,m):
    while l != pop.Empty:
        e,l = pop.ConsD(l)
        m = Aritytab(e,m)
    return m
    


if __name__ == "__main__":
    pg = prs.ParseFile("testprog.lu")
    print('renamed program ')
    rpg = ren.Rename(pg,pop.EmptySet)
    prp.Termln(rpg)
    m = Aritytab(rpg,map.EmptyMap)
    pio.WriteItemln(m)
    ok,var,arity = ArityCheck(rpg,m)
    if ok:
        print('arities check out ')
    else:
        prp.printf("Variable ")
        pio.WriteItem(var)
        prp.printf(" should have arity ")
        print(arity)
    print(ArityCheck(rpg,m))