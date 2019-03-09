""" make every free variable of a program where clause have global applied """
import pop,pio,prs,prp
from  exp import *

def Gprogram(pg):
    """ globalize program pg, a where clause """
    subj, wk,body = WhereD(pg)
    gbody = pop.ConsAll(body,Gdef)
    return WhereC(subj,wk,gbody)
    
def Gdef(d):
    """ globalize definition d """
    if VarDefinitionP(d): #simple var definition
        return d #nothing to do
    fun, formals,es, rhs = FunDefinitionD(d)
    grhs = Gterm(rhs,formals)
    return FunDefinitionC(fun,formals,es,grhs)
    
def Gterm(t,formals):
    """ apply globals to all nonformals in t"""
    if LiteralP(t): return t
    if VarP(t):
        if pop.Occurs(Var(t),formals): return t
        return Operation1C(GLOBALWord,t)
    if OperationP(t):
        o,opds = OperationD(t)
        gopds = pop.ConsAll2(opds,Gterm,formals)
        return OperationC(o,gopds)
    if CallP(t):
        fun, actuals = CallD(t)
        gactuals = pop.ConsAll2(actuals,Gterm,formals)
        return CallC(fun,gactuals)
    print('Cannot globalize ')
    pio.WriteItemln(t)
    exit()
    
    
if __name__ == "__main__":
    pg = prs.ParseFile("testprog.lu")
    gpg = Gprogram(pg)
    prp.Term(gpg)
    print()