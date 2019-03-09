""" compile a table of function arities """
import pio, pop, map, prs
from exp import *

def Aritytab(e,m):
    """ compile a table of arities for funs in e """
    if LiteralP(e): return m
    if VarP(e): return m
    if OperationP(e):
        o, opds = DeOperation(e)
        return AritytabList(opds,m)
    if WhereP(e):
        subj, body = DeWhere(e)
        m = Aritytab(subj,m)
        return AritytabList(body,m)
    if VarDefinitionP(e):
        v, rhs = DeVarDefinition(e)
        m = map.Extend(m,v,pop.NumC(0))
        return Aritytab(rhs,m)
    if FunDefinitionP(e):
        f, formals, rhs = DeFunDefinition(e)
        n = pop.Length(formals)
        while formals != pop.Empty:
           formal, formals = pop.DeCons(formals)
           m = map.Extend(m,Var(formal),pop.NumC(0))
        m = map.Extend(m,f,pop.NumC(n))
        return Aritytab(rhs,m)
    if CallP(e):
        fun,actuals = DeCall(e)
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
        o, opds = DeOperation(e)
        return ArityCheckList(opds,m)
    if WhereP(e):
        subj, body = DeWhere(e)
        ok, var, n = ArityCheckList(body,m)
        if not ok: return False, var, n
        return ArityCheck(subj,m)
    if VarDefinitionP(e):
        v, rhs = DeVarDefinition(e)
        ok, n = map.Apply(m,v)
        if not ok: print( 'unmapped var '+str(v));exit()
        if pop.NumVal(n) != 0: return False, v, pop.NumVal(n)
        return ArityCheck(rhs,m)
    if FunDefinitionP(e):
        f, formals, rhs = DeFunDefinition(e)
        ok, n = map.Apply(m,f)
        if not ok: print( 'unmapped var '+str(f))
        if pop.NumVal(n) != pop.Length(formals): return False, f, pop.NumVal(n)
        return ArityCheck(rhs,m)
    if CallP(e):
        fun, actuals = DeCall(e)
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
    m = Aritytab(pg,map.EmptyMap)
    pio.WriteItemln(m)
    ok,var,arity = ArityCheck(pg,m)
    if ok:
        print('arities check out ')
    else:
        prp.printf("Variable ")
        pio.WriteIem(var)
        prp.printf(" should have arity ")
        print(arity)
    print(ArityCheck(pg,m))