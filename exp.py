import pio
from pop import *

def SubexpressionL(e):
    """ list of proper immediate subexpressions of e """
    if LiteralP(e): return Empty
    if VarP(e): return Empty
    if OperationP(e): return OperationOperandL(e)
    if CallP(e):
        callvar, actualslist = DeCall(e)
        return Cons(callvar, actualslist)
    if DefinitionP(e):
        return List2(Lhs(e),Rhs(e))
    if WhereP(e): 
        subj, wk, defs = WhereD(e)
        return Cons(subj,defs)
    assert False, 'Weird term for subexp '+str(e)
    
def LocalsL(e):
    """ list of local or dummy variables of e """
    if DefinitionP(e):
        return DefinitionFormalsL(e)
    if WhereP(e):
        return WhereLocalsL(e)
    return Empty
    
def Definee(d):
    """ the variable defined by definition d """
    lhs, es, rhs = DefinitionD(d)
    if VarP(lhs): return Var(lhs)
    if CallP(lhs) and VarP(CallFun(lhs)):
        return Var(CallFun(lhs))
    assert False, 'Definee cant handle '+str(d)
         
def LiteralC(i):
    """literal term for value i"""
    return List2(DQUOTEWord,i)

def LiteralP(e):
    """ is e a literal?"""
    return El1(e)==DQUOTEWord

def VarC(v):
    """return a term consisting of a var"""
    return List2(VARWord,v)
    
def VarP(e):
    """does e consist of a variable?"""
    assert ListP(e), 'VarP given nonlist '+str(e)
    return El1(e)==VARWord
    
def Var(e):
    """"the variable from which the term e is constructed (assumes VarP(e))"""
    return El2(e)
    
def IfP(e):
    return El1(e) == IFWord
    
def IfCondition(e):
    return El2(e)
    
def IfAlternativeTrue(e):
    return El3(e)
    
def IfAlternativeFalse(e):
    return El4(e)
    
def IfD(e):
    return IfCondition(e),IfAlternativeTrue(e),IfAlternativeFalse(e)
    
def CallC(f,l):
    """a function call with function f and arglist l"""
    assert ListP(f), 'CallC given f nonexpression '+str(f)
    return List3(CALLWord,f,l)
    
def WhereC(s,wk,dl):
    """ create a where clause """
    return List3(wk,s,dl)
    
def WhereP(t):
    return Head(t) == WHEREWord or Head(t) == WHERELOOPWord
    
def WhereReallyP(t):
    return Head(t) == WHEREWord 
    
def WhereLoopP(t):
    return Head(t) == WHERELOOPWord

def WhereSubject(t):
    return El2(t)
    
def WhereDefinitionsL(t):
    return El3(t)
    
def WhereLocalsL(w):
    """ the local variables of where clause w """
    subj, wk, defs = WhereD(w)
    res = ConsAll(defs, Definee)
    return res
    
def WhereLhssL(w):
    subj, wk, defs = WhereD(w)
    lhss = Empty
    while defs != Empty:
        d, defs = ConsD(defs)
        lhs,es, rhs = DefinitionD(d)
        lhss = Append(lhss,List1(lhs))
    return lhss
    
def WhereD(t):
    return WhereSubject(t),WhereKind(t),WhereDefinitionsL(t)
    
def WhereKind(t):
    return El1(t)
    
def CallP(t):
    return Head(t) == CALLWord
    
def CallFun(t):
    """ the funcion being called """
    """ an expression """
    return El2(t)
    
def CallActualsL(t):
    """ the arglist of the call t """
    return El3(t)
    
def AcallC(funvar,len):
    return OperationC(ACALLWord, List2(VarC(funvar),NumC(len)))

def CallD(t):
    return CallFun(t),CallActualsL(t)
    
def ValofC(dl):
    return Cons(VALOFWord,dl)
    
def DefinitionP(d):
    return El1(d) == EQUALWord or El1(d) == ISWord
    
def VarDefinitionP(d):
    if not (El1(d) == EQUALWord or El1(d) == ISWord): return False
    lhs, es, rhs = DefinitionD(d)
    return VarP(lhs)
    
def FunDefinitionP(d):
    if not (El1(d) == EQUALWord or El1(d) == ISWord): return False
    lhs, es, rhs = DefinitionD(d)
    return CallP(lhs)
    
def FunDefinitionD(d):
    lhs, es, rhs = DefinitionD(d)
    fun, formals = CallD(lhs)
    forvars = ConsAll(formals,Var)
    return Var(fun), forvars, es, rhs
    
def FunDefinitionC(v,forvars,es,rhs):
    formals = ConsAll(forvars,VarC)
    fun = CallC(VarC(v),formals)
    return DefinitionC(fun,es,rhs)
    
def VarDefinitionD(d):
    lhs, es,rhs = DefinitionD(d)
    return Var(lhs), es,rhs
    
def VarDefinitionC(v,es,rhs):
    return DefinitionC(VarC(v),es,rhs)
       
def DefinitionC(lhs,es,rhs):
    return List3(es,lhs,rhs)
    
def DefinitionFormalsL(d):
    l,es,r= DefinitionD(d)
    if VarP(l): return Empty
    acts =  CallActualsL(l)
    return ConsAll(acts,Var)
    
def Lhs(d):
    return El2(d)
    
def Rhs(d):
    return El3(d)
    
def Es(d):
    return El1(d)
    
def DefinitionD(d):
    return Lhs(d), Es(d), Rhs(d)
    
def ListexpressionC(al):
    return Cons(LLISTPARENWord,al)
    
def ListexpressionP(d):
    return Head(d) == LLISTPARENWord
    
def SetexpressionC(al):
    return Cons(LSETPARENWord,al)
    
def SetexpressionP(d):
    return Head(d) == LSETPARENWord
    
def ListexpressionArgL(d):
    return Tail(d)

def OperationP(e):
    """is e an operation constant applied to operands"""
    return OperationSymbolP(El1(e))
    
def OperationSymbolP(o):
    return o in opsymbols

def OperationOperandL(e):
    """assumes OperationP(e), returns the list of operands """
    return Tail(e)

def OperationOperand1(e):
    """assumes OperationP(e), returns the first operand"""
    return El2(e)

def OperationOperand2(e):
    """assumes OperationP(e), returns the second operand"""
    return El3(e)
    


def DeOperation(e):
    o = OperationSymbol(e)
    l = OperationOperandL(e)
    return o,l

def OperationD(e):
    o = OperationSymbol(e)
    l = OperationOperandL(e)
    return o,l
    
    
def LiteralValue(e):
    """assumes LiteralP(e), returns the value the expreesion denotes"""
    return El2(e)

def OperationSymbol(e):
    """Assumes e is an operation applied to operands; returns the operation symbol"""
    if(LiteralP(e)): return e;
    return El1(e)

def Operation0C(o):
    """create expression from 0-ary operator 0"""
    return List1(o)
    
def Operation1C(o,e):
    return List2(o,e)
    
def Operation2C(o,e1,e2):
    return List3(o,e1,e2)
    
def Operation3C(o,e1,e2,e3):
    return List4(o,e1,e2,e3)
    
def OperationC(o,el):
    return Cons(o,el)

def Etype(t):
    """ return the type of term t is, as a string"""
    return WordName(Head(t))

def SetRprecedence(s,n):
    # symbol s binds with force n from the right 
    rpd[s] =n

def SetLprecedence(s,n):
    # symbol s binds with force n from the right 
    lpd[s] =n

def Rprecedence(s):
    return rpd[s]

def Lprecedence(s):
    return lpd[s]

def NewInfix(s):
    infixes.add(s)

def NewPostfix(s):
    postfixes.add(s)

def NewPrefix(s):
    prefixes.add(s)
    
def NewNullfix(s):
    nullfixes.add(s)
    
def InfixP(s):
    return WordP(s) and s in infixes

def PostfixP(s):
    return WordP(s) and s in postfixes

def PrefixP(s):
    return WordP(s) and s in prefixes

def NullfixP(s):
    return WordP(s) and s in nullfixes

def FixP(s):
    return InfixP(s) or PrefixP(s) or PostfixP(s) or NullfixP(s);

def NewFixes(k):
    while not EmptyP(k):
        r = Head(k); k = Tail(k);
        lp = NumVal(El1(r)); s = El2(r); rp = NumVal(El3(r));
        SetLprecedence(s,lp); SetRprecedence(s,rp)
        if(rp==100 and lp == 100): NewNullfix(s); continue
        if(lp==100): NewPrefix(s); continue
        if(rp==100): NewPostfix(s);  continue
        NewInfix(s)

def Reserve(l):
    s = set()
    while not EmptyP(l):
        s.add(Head(l))
        l = Tail(l)
    return s


lpd = {}
rpd = {}

prefixes =set()
infixes = set()
postfixes = set()
nullfixes = set()
reservedwords = Reserve(pio.Popliteral("[if then else fi where whereloop end valof]"))

NewFixes(pio.Popliteral("[[100 sin 65][100 cos 65][100 tan 65][100 exp 65][100 abs 44][100 log 65][100 log2 65][100 sqrt 65][100 pi 100][100 phi 100]]"))
NewFixes(pio.Popliteral("[[100 tl 65][100 not 65][100 isatom 65][100 islist 65][100 isnumber 65][100 isnil 65][100 iseod 65][100 isstring 65][100 isword 65][100 iserror 65]]"));
NewFixes(pio.Popliteral("[[100 first 65][100 First 65][100 init 65][100 id 65][100 current 65][100 succ 65][100 next 65][100 Next 65][100 pre 65][100 contemp 65][100 active 65][10 fby 9][100 Fby 65][10 sby 9][9 ybf 10][10 wvr 11][10 while 11][10 swvr 11][10 asa 11][10 attime 11][10 atspace 11]]"))

NewFixes(pio.Popliteral("[[20 :: 19][25 or 24][30 and 29][40 <> 39][40 < 39][40 <= 39][40 eq 39][40 ne 39][40 >= 39][40 > 39][45 - 44][45 + 44][50 * 49][50 / 49][50 div 49][50 mod 49][55 ** 54][55 ^ 54][100 hd 65][100 index 100][100 sindex 100][100 eod 100][100 eos 100][100 true 100][100 false 100]]"));

opsymbols = prefixes.union(infixes).union(prefixes).union(postfixes).union(nullfixes)
opsymbols.add(YCALLWord)
opsymbols.add(IFWord)
opsymbols.add(LLISTPARENWord)
opsymbols.add(ACTUALWord)
opsymbols.add(GLOBALWord)
opsymbols.add(EODWord)
opsymbols.add(EOSWord)



Unterm = List1(WordC("unterm"))

