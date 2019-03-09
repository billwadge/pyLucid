import pio,pop,prp,gen,sys,exp

def YieldsP(o1,o2):
    return exp.Rprecedence(o1) <= exp.Lprecedence(o2)
    
def Expr(ig):
    """Parse  the next expression in item generator ig"""
    # leave ig pointing to following item or eod
    f = Factor(ig) #pickup lefthand factor
    if f=='': return '' #nothing there
    ci = pio.CurrentItem(ig)
    if ci=='': return f #nothing more to parse
    while pio.CurrentItem(ig)!='' and exp.InfixP(pio.CurrentItem(ig)):
        f=Complete(f,ig)
    if pio.CurrentItem(ig) != exp.WHEREWord: return f
    e1 = Where(f,ig)
    o = pio.CurrentItem(ig)
    if o == '': return e1
    if exp.InfixP(o): 
       pio.NextItem(ig)
       e2 = Expr(ig)
       if o == WVRWord or o==WHILEWord or o==SWVRWord: return exp.CallC(exp.VarC(o),pop.List2(e1,e2))
       return exp.Operation2C(o,e1,e2)
    while pio.CurrentItem(ig) == exp.WHEREWord:
       e1 = Where(e1,ig)
    return e1
    
def Where(e,ig):
    """ parse a where clause with parsed subject """
    Expect(pop.WHEREWord,ig)
    dl = Definitions(ig)
    Expect(pop.ENDWord,ig)
    return exp.WhereC(e,dl)
    
def Definitions(ig):
    """pick up a list of definitions"""
    d = Definition(ig)
    if d=='': return pop.Empty
    el = Definitions(ig)
    return pop.Cons(d,el)
    
def Definition(ig):
    """ pick up a definition """
    lhs = Expr(ig)
    if lhs == '': return ''
    if not Expect(pop.EQUALWord,ig):
        prp.printf('expected = found ');pio.WriteItemln(pio.CurrentItem(ig));exit()
    rhs = Expr(ig)
    if rhs == '': rhs = exp.Unterm
    df = exp.DefinitionC(lhs,rhs)
    if not Expect(exp.SEMICOLONWord,ig):
        return Interm(df)
    return df
    
def Complete(e,ig):
    # current item is an infix operator
    # return longest initial subexpression
    q = pio.NextItem(ig) # q is the infix operator
    f = Factor(ig)
    if f=='':
        if e == '': return Operation1C(q,unterm)
        return exp.Operation2C(q,e,exp.Unterm)
    while pio.CurrentItem(ig) != '' and exp.InfixP(pio.CurrentItem(ig)) and YieldsP(q,pio.CurrentItem(ig)):
        f = Complete(f,ig)
    if e == '': return exp.Operation1C(q,f)
    if q == WVRWord or q==WHILEWord or q==SWVRWord: return exp.CallC(exp.VarC(q),exp.List2(e,f))
    return exp.Operation2C(q,e,f)
    
def Factor(g):
    """ return next factor - smallest initial sub expression """
    lex = pio.CurrentItem(g)
    if lex == '': return ''
    if lex == pop.QUOTEWord: return Word(g)
    if lex == pop.IFWord: return IfExpr(g)
    if lex == pop.VALOFWord: return Valof(g)
    if lex == pop.LLISTPARENWord: return Listexpression(g)
    if lex == pop.LSETPARENWord: return Setexpression(g)
    if(exp.PrefixP(lex)): return Complete('',g); # prefix operator
    if exp.NullfixP(lex): pio.NextItem(g);return exp.Operation0C(lex)
    if(pop.NumP(lex) or pop.StringP(lex) or pop.ListP(lex)):  
        pio.NextItem(g);return exp.LiteralC(lex) #a literal
    if lex in reservedwords: return ''
    if(pio.IdentP(lex)):
        pio.NextItem(g);
        if pio.CurrentItem(g) == LparenWord: #function call
            return Call(exp.VarC(lex),g)
        return exp.VarC(lex)
    if exp.NullfixP(lex): pio.NextItem(g);return Operation0C(lex)
    if lex==LparenWord : return ParenExpr(g) #parenthesized expression
    print('Expected factor, found')
    pio.Dump5(g);print()
    exit()
    
def Valof(ig):
    """ parse a valof block"""
    Expect(pop.VALOFWord,ig)
    dl = Definitions(ig)
    Expect(pop.ENDWord,ig)
    return exp.ValofC(dl)
    
def Call(f,ig):
    Expect(LparenWord,ig)
    l = Arglist(ig) 
    if Expect(RparenWord,ig): return exp.CallC(f,l)
    return InTerm(exp.CallC(f,l))
    
def Listexpression(ig):
    Expect(pop.LLISTPARENWord,ig)
    al = Arglist(ig)
    if Expect(pop.RLISTPARENWord,ig): return exp.ListexpressionC(al)
    return(Interm(exp.ListexpressionC(al)))
    
def Setexpression(ig):
    Expect(pop.LSETPARENWord,ig)
    al = Arglist(ig)
    if Expect(pop.RSETPARENWord,ig): return exp.SetexpressionC(al)
    return(Interm(exp.ListexpressionC(al)))
       
def Arglist(ig):
    """ get a comma separated list of expressions"""
    #doesn't consume terminating item
    f = Expr(ig)
    if f == exp.Unterm: return exp.Unterm
    if pio.CurrentItem(ig) == CommaWord:
        pio.NextItem(ig)
        return pop.Cons(f,Arglist(ig))
    return pop.List1(f)
     
def Word(g):
    pio.NextItem(g)
    w = pio.NextItem(g)
    Expect(pop.QUOTEWord,g)
    return exp.LiteralC(w)
  
def IfExpr(ig):
    """parse if expression"""
    pio.NextItem(ig)
    condition = Expr(ig)
    if not Expect(exp.THENWord,ig): return ''
    alt1 = Expr(ig)
    if not Expect(exp.ELSEWord,ig): return ''
    alt2 = Expr(ig)
    if not Expect(exp.FIWord,ig): return ''
    return exp.Operation3C(exp.IFWord,condition,alt1,alt2)
    
def Expect(w,ig):
    if pio.CurrentItem(ig) == w: pio.NextItem(ig); return True
    prp.printf('Expected ');pio.WriteItemln(w)
    print('Found '); pio.Dump5(ig)
    print()
    exit()
    
def ParenExpr(g): 
    if not Expect(LparenWord,g): return Unterm
    e = Expr(g)
    if e==exp.Unterm: return exp.Unterm
    if Expect(RparenWord,g): return e
    return Interm(e)
 
def Interm(t):
    """ t wrapped up as an incomplete (unfinished) term"""
    return pop.List2(INTERMWord,t)
    
def Reserve(l):
    s = set()
    while not pop.EmptyP(l):
        s.add(pop.Head(l))
        l = pop.Tail(l)
    return s
    
LparenWord = pop.WordC("(")
RparenWord = pop.WordC(')')
CommaWord = pop.WordC(',')
WVRWord = pop.WordC("wvr")
SWVRWord = pop.WordC("swvr")
WHILEWord = pop.WordC("while")
INTERMWord = pop.WordC("interm")
reservedwords = Reserve(pio.Popliteral("[if then else fi where end valof]"))

def ParseFile(fname):
    f = open(fname,"r")
    sourceprog = f.read()
    f.close()
    ig = pio.ItemGenStringC(sourceprog)
    return Expr(ig)
    
    
if __name__ == "__main__":
    prog = ''
    while True:
        ln = input()
        if ln==';': break
        prog = prog + ' ' + ln
    cg = gen.CharStringC(prog)
    ig = pio.ItemGenChargenC(cg)
    ex = Expr(ig)
    pio.WriteItemln(ex)
    prp.Termln(ex)