import pop,pio,exp,gen,prs

indentation = 0
indent = 4

def printf(s):
    print(s,end ='')

def NewLine():
    printf("\n");
    for i in range(indentation):
        printf(" ")


def Indent():
    global indentation, indent
    indentation = indentation + indent


def Exdent():
    global indentation, indent
    indentation = indentation - indent

def bprp(t):
    printf("(");Term(t);printf(")")

def Prefix(t):
    s = exp.OperationSymbol(t); a = exp.OperationOperand1(t)
    pio.WriteItem(s);printf(" ")
    if(exp.Rprecedence(s) > TermLprecedence(a)):
        bprp(a)
    else:
        Term(a);

def Infix(t):
    """print a term with an infix operator"""
    s = exp.OperationSymbol(t) 
    a1 = exp.OperationOperand1(t);a2 = exp.OperationOperand2(t)
    if(exp.Lprecedence(s) > TermRprecedence(a1)):
        bprp(a1)
    else:
        Term(a1)
    printf(" ")
    pio.WriteItem(s)
    printf(" ")
    if(exp.Rprecedence(s) > TermLprecedence(a2)):
        bprp(a2)
    else:
        Term(a2)


def Operation(t):
    s = exp.OperationSymbol(t)
    al = exp.OperationOperandL(t)
    n = pop.Length(al)
    if(n==0):
        printf(" ");pio.WriteItem(exp.OperationSymbol(t));printf(" ");return
    if(exp.PrefixP(s)):
        Prefix(t); return
    if(exp.InfixP(s)):
        Infix(t); return
    if(s==exp.LLISTPARENWord):
        printf("[% ");Termlist(al);printf(" %]");return
    if s == exp.LSETPARENWord:
        printf("{% ");Termlist(al);printf(" %}");return
    pio.WriteItem(exp.OperationSymbol(t));printf("(");Termlist(al);printf(")")

def If(t):
    printf("if ");Term(exp.IfCondition(t))
    printf(" then ");Term(exp.IfAlternativeTrue(t))
    printf(" else ");Term(exp.IfAlternativeFalse(t))
    printf(" fi");

def Call(t):
    """ print a function call"""
    fun = exp.CallFun(t)
    al = exp.CallActualsL(t)
    Term(fun)
    printf("(")
    Termlist(al)
    printf(")")

def Where(t):
    Term(exp.WhereSubject(t))
    Indent()
    NewLine()
    printf("where")
    Indent()
    NewLine()
    Definitions(exp.WhereDefinitionsL(t))
    Exdent()
    NewLine()
    printf("end")
    Exdent()
    
def Definitions(dl):
    while not pop.EmptyP(dl):
        Definition(pop.Head(dl))
        printf(";")
        dl = pop.Tail(dl)
        if pop.EmptyP(dl): return
        NewLine()
        
def Definition(d):
    Term(exp.Lhs(d))
    printf(" = ")
    Term(exp.Rhs(d))

def Listexpression(t):
    printf("[% ")
    Termlist(exp.ListexpressionArgL(t))
    printf(" %]")
    
def Termlist(m):
    if(pop.EmptyP(m)): return
    while True:
        Term(pop.Head(m));  m = pop.Tail(m)
        if pop.EmptyP(m): return
        printf(",");

def Varlist(m):
    if(pop.EmptyP(m)): return
    while True:
        pio.WriteItem(pop.Head(m));  m = pop.Tail(m);
        if(pop.EmptyP(m)): return;
        printf(",")
      
def Term(t):
    #print('Prping ',t)
    if(t==exp.Unterm): printf("?");return
    if(exp.VarP(t)): pio.WriteItem(exp.Var(t)); return
    if(exp.LiteralP(t)):
        lv = exp.LiteralValue(t)
        if pop.WordP(lv): printf(' "'+pio.Words(lv)+'" '); return
        pio.WriteItem(lv); return
    if exp.IfP(t): If(t); return
    if(exp.OperationP(t)): Operation(t); return
    if(exp.CallP(t)): Call(t); return
    if(exp.WhereP(t)): Where(t); return
    if(exp.DefinitionP(t)): Definition(t); return
    if exp.ListexpressionP(t) : Listexpression(t);return
    printf('Huh? ');pio.WriteItem(t);print()
    assert False, 'strange term for prp.Term: '+str(t)

def Termln(t):
    Term(t)
    print()
    
"""
def TermPrint(t)
    tt = Etype(t)
    p = FindBest(tt,printer)
    p(t)
    
def FindBest(tt,d)
    if tt in d: return d[tt]
    p = FindBest(super[tt],d)
    d[tt] = p
    return p
    
super['+'] = 'infixop'
super['*'] = 'infixop'
super['**'] = 'infixop'
super['first'] = 'prefixop'
super['next'] = 'prefixop'
super['infixop'] = 'op'
super['prefixop'] = 'op'
super['[%'] = 'multiop'
super['multiop'] = 'op'
super['op'] ='ex'
    

"""

def TermRprecedence(t):
    # the force with which term t binds from the right (to its left operands) 
    if(exp.VarP(t) or exp.LiteralP(t)): return 100;
    if(exp.OperationP(t)):
        s = exp.OperationSymbol(t);
        if(exp.InfixP(s) or exp.PostfixP(s)):  return exp.Rprecedence(exp.OperationSymbol(t));
        return 100;
    return 100

def TermLprecedence(t):
    # the force with which term t binds from the left (to its right operands) */
    if(exp.VarP(t) or exp.LiteralP(t)): return 100;
    if(exp.OperationP(t)):
        s = exp.OperationSymbol(t)
        if(exp.InfixP(s) or exp.PrefixP(s)):  return exp.Lprecedence(exp.OperationSymbol(t));
        return 100
    return 100
    
"""
def If(c):
    ol = OperationOperandL(c);
    PrpIndent();PrpNewline();
    printf("if ");PrpTerm(el1(ol));
    PrpIndent();PrpNewline();
    printf("then ");PrpTerm(el2(ol));
    PrpNewline();
    printf("else ");PrpTerm(el3(ol));
    PrpExdent();PrpNewline();
    printf("fi ");PrpExdent();
}
"""

if __name__ == "__main__":
    
    progfile = open("testprog.lu")
    progs = progfile.read()
    progfile.close()
    cg = gen.CharStringC(progs)
    ig = pio.ItemGenChargenC(cg)
    prog=prs.Expr(ig)
    print('Program is ')
    pio.WriteItemln(prog)
    Term(prog);print()