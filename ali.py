""" perform ali-anation (yaghification) of program
    assuming distinct variables and no nested fundefs"""
    
import pio, pop, map, prs, prp
from exp import *
    
def Formals(w):
    """ returns a table of lists of formals """
    formap = map.EmptyMap
    subj,wk,body = WhereD(w)
    while body != pop.Empty:
        d,body = pop.ConsD(body)
        if VarDefinitionP(d): continue
        f,formals,es,rhs = FunDefinitionD(d)
        formap = map.Extend(formap,f,formals)
    return formap
    
def ActualTable(e,atab,ftab):
    """ collects a table of actuals in the order of appearance
        returns table and yaghified program"""
    if LiteralP(e): return atab,ftab,e
    if VarP(e): return atab,ftab,e
    if OperationP(e):
        o, opds = OperationD(e)
        if pop.ListP(o): print(e);print(o);exit()
        tab,ftab, yopds = ActualTableList(opds,atab,ftab)
        return tab,ftab, OperationC(o,yopds)
    if WhereP(e):
        subj, wk, body = WhereD(e)
        atab,ftab, ysubj = ActualTable(subj,atab,ftab)
        atab,ftab, ybody = ActualTableList(body,atab,ftab)
        return atab,ftab, WhereC(ysubj,wk,ybody)
    if VarDefinitionP(e):
        v,es,rhs = VarDefinitionD(e)
        atab,ftab,yrhs = ActualTable(rhs,atab,ftab)
        return atab,ftab, DefinitionC(VarC(v),es,yrhs)
    if FunDefinitionP(e):
        f,formals,es,rhs = FunDefinitionD(e)
        atab, ftab, yrhs = ActualTable(rhs,atab,ftab)
        ftab = map.Extend(ftab,f,formals)
        return atab,ftab, DefinitionC(VarC(f),es,yrhs)
    if CallP(e):
        fun,actuals = CallD(e)
        funvar = Var(fun)
        atab,ftab,yactuals = ActualTableList(actuals,atab,ftab)
        ok, actlist = map.Apply(atab,funvar)
        if not ok : actlist = pop.Empty
        newactlist = pop.Append(actlist,pop.List1(yactuals))
        atab = map.MapS(atab,funvar,newactlist)
        return atab,ftab,OperationC(YCALLWord,pop.List2(fun,LiteralC(pop.NumC(pop.Length(newactlist)-1))))
        
def ActualTableList(l,atab,ftab):
    yl = pop.Empty
    while l!= pop.Empty:
        e,l = pop.ConsD(l)
        atab,ftab,ye = ActualTable(e,atab,ftab)
        yl = pop.Append(yl,pop.List1(ye))
    return atab,ftab, yl
    
def ActualDefs(amap,formap):
    """ generate defs for the formals in terms of actuals"""
    """amap is the actuals map formap is the formals map """
    funset = map.Domain(amap) #set of function variable
    deflist = pop.Empty
    while not pop.EmptyP(funset): #run  through the functions
        fun,funset = pop.AddD(funset)
        ok, actsl = map.Apply(amap,fun)
        if not ok: print('No actuals recorded for '+str(fun));exit()
        ok, formals = map.Apply(formap,fun)
        fms = formals
        al = actsl
        while not pop.EmptyP(fms):
            acts = pop.ConsAll(al,pop.Head)
            al = pop.ConsAll(al,pop.Tail)
            fm, fms = pop.ConsD(fms)
            actexpr = OperationC(ACTUALWord,acts)
            df = DefinitionC(VarC(fm),EQUALWord,actexpr)
            deflist = pop.Cons(df,deflist)
    return deflist
            
    


if __name__ == "__main__":
    pg = prs.ParseFile("testprog.lu")
    atab,ftab, ypg = ActualTable(pg,map.EmptyMap,map.EmptyMap)
    prp.Term(ypg);
    print()
    pio.WriteItemln(atab)
    pio.WriteItemln(ftab)
    defs = ActualDefs(atab,ftab)
    while not pop.EmptyP(defs):
        df,defs = pop.ConsD(defs)
        prp.Term(df);print()