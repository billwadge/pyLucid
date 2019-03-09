from pop import *
import math

calccount = 0

def Pid(a):
    return a[0]

def Psum(a):
    return NumC(NumVal(a[0])+NumVal(a[1]))

def Pprod(a):
    return NumC(NumVal(a[0])*NumVal(a[1]))

def Pdiff(a):
    #print('su ',a)
    return NumC(NumVal(a[0])-NumVal(a[1]))

def Pdivide(a):
    return NumC(NumVal(a[0])/NumVal(a[1]))

def Ppow(a):
    return NumC(NumVal(a[0])**NumVal(a[1]))

def Pmod(a):
    return NumC(NumVal(a[0])%NumVal(a[1]))

def Pdiv(a):
    return NumC(NumVal(a[0])//NumVal(a[1]))
    
def Psin(a):
    return NumC(math.sin(NumVal(a[0])))
    
def Pabs(a):
    return NumC(abs(NumVal(a[0])))
    
def Pcos(a):
    return NumC(math.cos(NumVal(a[0])))
    
def Ptan(a):
    return NumC(math.tan(NumVal(a[0])))
    
def Pexp(a):
    return NumC(math.exp(NumVal(a[0])))
    
def Plog(a):
    return NumC(math.log(NumVal(a[0])))
    
def Plog10(a):
    return NumC(math.log10(NumVal(a[0])))
    
def Psqrt(a):
    return NumC(math.sqrt(NumVal(a[0])))
    
def Pconcat(a):
    return StringC(Strings(a[0])+Strings(a[1]))
    
def Plist(a):
    n = len(a)
    res = Empty
    for i in range(n):
        res = Cons(a[n-i-1],res)
    return res
    
def Pcs(a):
    return Cons(a[0],a[1])
    
def Phd(a):
    return Head(a[0])

def Ptl(a):
    return Tail(a[0])
    
def Pconcat(a):
    s0 = Strings(a[0])
    s1 = Strings(a[1])
    return StringC(s0+s1)
    
def Pappend(a):
    return Append(a[0],a[1])
    
def Pgt(a):
    return BoolC(NumVal(a[0])>NumVal(a[1]))
    
def Pge(a):
    return BoolC(NumVal(a[0])>=NumVal(a[1]))
    
def Plt(a):
    #print('lt ',a)
    return BoolC(NumVal(a[0])<NumVal(a[1]))
    
def Ple(a):
    return BoolC(NumVal(a[0])<=NumVal(a[1]))
    
def Peq(a):
    #print('eq ',a)
    return BoolC(EqualP(a[0],a[1]))
    
def Pne(a):
    return BoolC(not EqualP(a[0],a[1]))
    
def Ptrue(a):
    return TRUEWord
    
def Pfalse(a):
    return FALSEWord

def Ppi(a):
    return NumC(math.pi)
    
def Pphi(a):
    return NumC(1.618033988749895)
    
def Peod(a):
    return EODWord
    
def Peos(a):
    return EOSWord

def Pnot(a):
    return BoolC(a[0] == FALSEWord)
    
def Pisword(a):
    return BoolC(WordP(a[0]))
    
def Pisnum(a):
    return BoolC(NumP(a[0]))
    
def Pisstring(a):
    return BoolC(StringP(a[0]))
    
def Pislist(a):
    return BoolC(ListP(a[0]))
    
def Piseod(a):
    return BoolC(a[0] == EODWord)
    
def Calculate(o,resarray):
    """ calculate the result of applying strict operator o to results in array a """
    global strict,calccount
    calccount += 1
    op = strict[o]
    #print('Calculate returning '+str(op(resarray)))
    return op(resarray)
    
strict={}
 
strict['id'] = Pid   
strict["+"] = Psum
strict["-"] = Pdiff
strict["*"] = Pprod
strict["/"] = Pdivide
strict["**"] = Ppow
strict["div"] = Pdiv
strict["abs"] = Pabs
strict["sin"] = Psin
strict["cos"] = Pcos
strict["tan"] = Ptan
strict["exp"] = Pexp
strict["log"] = Plog
strict["log10"] = Plog10
strict["sqrt"] = Psqrt
strict["mod"] = Pmod
strict["^"] = Pconcat
strict["hd"] = Phd
strict["tl"] = Ptl
strict["::"] = Pcs
strict["^"] = Pconcat
strict["[%"] = Plist
strict["<>"] = Pappend
strict["<"] = Plt
strict["<="] = Ple
strict[">"] = Pgt
strict[">="] = Pge
strict["eq"] = Peq
strict["ne"] = Pne
strict["true"] = Ptrue
strict["false"] = Pfalse
strict["pi"] = Ppi
strict["phi"] = Pphi
strict["eod"] = Peod
strict["eos"] = Peos
strict["not"] = Pnot
strict["isword"] = Pisword
strict["isnum"] = Pisnum
strict["isstring"] = Pisstring
strict["islist"] = Pislist
strict["iseod"] = Piseod
    