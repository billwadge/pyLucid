""" commands to calculate data operations """
from clc import Calculate
from mch import *

def EnterOpp(s,p,m)
    """register popcode command s as  procedure p with parameter m """
    opmap[s] = p
    pmmap[s] = p
    

def Mcalc0(nm):
    V2push0(Calculate(nm,[])

def Mcalc1(nm):
    """ perform unary operation nm on vstack """
    opds = [Vpop0()]
    V2push0(Calculate(nm,opds))
    
def Mcalc2(nm)
    """ perform binary operation nm on vstack """
    opd1 = Vpop0()
    opd0 = Vpop0()
    if opd0 == EODWord or opd1 == EODWord
        res = EODWord
    else:
        res = Calculate(nm, [opd0,opd1])
    V2push0(res)
    
    
for nm in ["+","*","**","/","eq","ne","<","<=",">",">=","mod","::","^"]:
    EnterOpp(nm,Mcalc2,nm)
    
for nm in ["hd","tl","-","not","sin","cos","tan","exp","log","log10","abs","sqrt",
    "islist","isword","isstring","isnum","isbool","iseod"]:
    EnterOpp(nm,Mcalc1,nm)
    
for nm in ["true","false","pi","phi","eod"]:
    EnterOpp(nm,Mcalc0,nm)
    
        