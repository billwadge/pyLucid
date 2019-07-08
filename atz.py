import pop,pio,exp,prp,gen,prs

def Awhere(wc):
    """ atomize subject and rhs of where clause adding generated defs to body """
    subject, wk,body = exp.WhereD(wc)
    atomicsubject, atomicdefs = Aexpr(subject)
    assert pop.ListP(atomicdefs), 'oops'
    while body != pop.Empty:
        mdef ,body = pop.DeCons(body)
        newdef, eqns = Adefinition(mdef); 
        assert pop.ListP(eqns), 'arg'
        atomicdefs = pop.Append(atomicdefs,eqns)
        atomicdefs = pop.Cons(newdef,atomicdefs)
    return exp.WhereC(atomicsubject,wk,atomicdefs),pop.Empty
    
def Adefinition(df):
    """atomize a definition, returning atomic def and deflist"""
    rhs = exp.Rhs(df); lhs = exp.Lhs(df)
    assert exp.VarP(lhs), 'cannot handle compund definitions'
    if exp.LiteralP(rhs): #equated to a literal, no action
        return df,pop.Empty
    arhs, defs = Aexpr(rhs)
    return exp.DefinitionC(lhs,pop.EQUALWord, arhs), defs
    
def Aexpr(e):
    """ returns e1 dl where dl is the list of atomic definitions generated
        and e1 is the new atomic expression """
    if exp.OperationP(e): return Aoperation(e)
    if exp.VarP(e): return e, pop.Empty
    if exp.WhereP(e): return Awhere(e)
    assert not exp.CallP(e), ' cannot do function calls '
    assert exp.LiteralP(e), ' bad arg to Aexpr'
    v = VarGen()
    d = exp.DefinitionC(v,pop.EQUALWord,e)
    return v, pop.List1(d)
    
def Aoperation(e):
    """ returns e1 dl where dl is the list of atomic definitions generated
        and e1 is the new atomic expression """
    o = exp.OperationSymbol(e)    #operator
    l = exp.OperationOperandL(e)  #operands
    vl = pop.Empty                #new variables introduced
    aeqs = pop.Empty              #list of equations generated
    while l != pop.Empty:          #iterate down operand list
        opd = pop.Head(l);l = pop.Tail(l)  #get next operand and advance
        if exp.VarP(opd):      #if it's a var nothing to do
            vl = pop.Cons(opd,vl)
            continue
        ae, dl = Aexpr(opd)         # process the operand
        aeqs = pop.Append(dl,aeqs)     # collect equations generated
        if not exp.VarP(ae):
            nv = VarGen()               # generate a new variable
            vl = pop.Cons(nv,vl)           # save it  
            d = exp.DefinitionC(nv,pop.EQUALWord,ae)      # generate new atomic definition
            aeqs = pop.Cons(d,aeqs) 
        else:
            vl = pop.Cons(ae,vl)
    vl = pop.Reverse(vl)               # variables accumulated in reverse order
    e1 = exp.OperationC(o,vl)           # new atomic expression
    return e1, aeqs                # return the atomic expression and equations generated
    
varcount = 0

def VarGen():
    global varcount
    s = str(varcount+100)
    varcount = varcount+1
    var = 'V'+s[1:]
    return exp.VarC(pop.WordC(var))
    
if __name__ == "__main__":
    prog = ''
    while True:
        ln = input()
        if ln==';': break
        prog = prog + ' ' + ln
    cg = gen.CharStringC(prog)
    ig = pio.ItemGenChargenC(cg)
    e = prs.Expr(ig)
    pio.WriteItemln(e)
    prp.Term(e);print()
    e1,dl = Aexpr(e)
    prp.Term(e1);print(' where')
    while dl != pop.Empty:
        prp.Definition(pop.Head(dl));print()
        dl = pop.Tail(dl)
    