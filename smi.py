""" interpreter for stack machine """
from cst import *
from mch import *
from evl import *
import sma,profile
xcount = 0
waresaves = 0
warefetches = 0
listype = type([])

def Smachinate(mp):
    global vreg,treg,sreg,preg, xcount,listtype
    #while not CemptyP():
    #print("Smachinating",cstackptr)
    while cst.cstackptr != 0:
     cmd = Cpop0()
     xcount += 1
     #print('Executing command ',cmd)
     #Cdump();print()
     if type(cmd) == listype: # a list of commands
         Cpusha(cmd,len(cmd)) # do them in reverse order
         continue
     if cmd == '"':
         Vpush0(Cpop0()) #a literal
         continue
     if cmd == 'eval':
         var = Cpop0()  # get variable to be evaluated
         vreg = var
         df,ln = mp[var]  # get its machine code definition
         Cpusha(df,ln)   #add defn of var to cstack in reverse order
         continue
     if cmd == 'if':
         alt1 = Cpop0()
         alt2 = Cpop0()
         if Vpop0() == TRUEWord:
             Cpusha(alt1,len(alt1))
         else:
             Cpusha(alt2,len(alt2))
         continue
     if cmd in optable:
         p = optable[cmd]
         if cmd in parmtable:
             p(parmtable[cmd])
         else:
             p()
         continue
     print('Undefined command ',cmd)
     exit()
     
def islist(a):
    return type(a) == type([])
    
def inctime():
    global treg, sreg, preg
    treg += 1
    
def dectime():
    global treg, sreg, preg
    treg -=1
    
def settime():
    global treg
    treg = NumVal(Vpop0())
    
def savetime():
    global treg, sreg, preg
    Opush(treg)
    
def restoretime():
    global treg, sreg, preg
    treg = Opop()
    
def restorevar():
    global treg, sreg, preg
    vreg = Opop()
    
def time():
    global treg, sreg, preg
    Vpush0(NumC(treg))
    
def zerotime():
    global treg, sreg, preg
    treg = 0
    
def zerospace():
    global treg, sreg, preg
    sreg = 0
    
def space():
    global treg, sreg, preg
    Vpush0(NumC(sreg))
    
def setspace():
    global sreg
    sreg = NumVal(Vpop0())

def incspace():
    global treg, sreg, preg
    sreg += 1
    
def decspace():
    global treg, sreg, preg
    sreg -=1
    
def savespace():
    global treg, sreg, preg
    Opush(sreg)
    
def restorespace():
    global treg, sreg, preg
    sreg = Opop()
    
def saveplace():
    global treg, sreg, preg
    Opush(preg)
    
def restoreplace():
    global treg, sreg, preg
    preg = Opop()
    
def pushplace():
    global treg, sreg, preg
    preg = Pcons(NumVal(Vpop0()),preg)
    
def popplace():
    global treg, sreg, preg
    ph,preg = PconsD(preg)
    Vpush0(NumC(ph))
    
def evali():
    choices = Cpop0()
    i = NumVal(Vpop0())
    C1push0(choices[i])
    C1push0('eval')

def writeln():
    pio.WriteItemln(Vpop0())
     
def repeat():
    count = Cpop0()
    block = Cpop0()
    if count == 0: return
    count -= 1
    Cpusha(['repeat',count,block],3)
    Cpush0(block)
    
def waresearch():
    global vreg, treg, sreg, preg, warefetches,warehouse
    #block = Cpop0()
    cst.cstackptr -=1; block = cst.cstack[cst.cstackptr]
    tag = (vreg,treg,sreg,preg)
    print('Searching ',tag)
    if tag in warehouse:
        Vpush0(warehouse[tag])
        warefetches += 1
        print('Fetched ',tag, ' = ',warehouse[tag])
    else:
        Cpush0(vreg)
        Cpush0("waresave")
        Cpush0(block)
        """
        print('done ',cst.cstackptr)
        cst.cstack[cstackptr]=vreg;cst.cstack[cstackptr+1]="waresave";cst.cstack[cstackptr+2]=block
        cst.cstackptr += 3
        """
        
def waresave():
    global vreg, treg, sreg, preg, waresaves, warehouse
    vreg = Cpop0()
    tag = (vreg,treg,sreg,preg)
    val = Vtop0()
    print('Saving ',tag, ' = ',val)
    warehouse[tag] = val
    waresaves += 1
    #print('Saving ',tag)
    
def time0():
    global treg,sreg
    if treg == 0:
        Vpush0(TRUEWord)
    else:
        Vpush0(FALSEWord)
    
def space0():
    global treg,sreg
    if sreg == 0:
        Vpush0(TRUEWord)
    else:
        Vpush0(FALSEWord)
        
def vpop0():
    Vpop0()
        
optable = {}
parmtable = {}
    
optable['inctime'] = inctime
optable['dectime'] = dectime
optable['savetime'] = savetime
optable['settime'] = settime
optable['restoretime'] = restoretime
optable['restorevar'] = restorevar
optable['setspace'] = setspace
optable['incspace'] = incspace
optable['decspace'] = decspace
optable['savespace'] = savespace
optable['restorespace'] = restorespace
optable['saveplace'] = saveplace
optable['restoreplace'] = restoreplace
optable['pushplace'] = pushplace
optable['popplace'] = popplace
optable['time'] = time
optable['space'] = space
optable['zerotime'] = zerotime
optable['zerospace'] = zerospace
optable['writeln'] = writeln
optable['repeat'] = repeat
optable['waresearch'] = waresearch
optable['waresave'] = waresave
optable['time0'] = time0
optable['space0'] = space0
optable['evali'] = evali
optable['vpop0'] = vpop0

def EnterOpp(s,p,m):
    global optable, parmtable
    """register popcode command s as  procedure p with parameter m """
    optable[s] = p
    parmtable[s] = m
    

def Mcalc0(nm):
    Vpush0(clc.Calculate(nm,[]))

def Mcalc(nm):
    """ perform unary operation nm on vstack """
    opds = [Vpop0()]
    Vpush0(clc.Calculate(nm,opds))
    
def Mcalc2(nm):
    """ perform binary operation nm on vstack """
    opd1 = Vpop0()
    opd0 = Vpop0()
    if opd0 == EODWord or opd1 == EODWord:
        res = EODWord
    else:
        res = clc.Calculate(nm, [opd0,opd1])
    Vpush0(res)

for nm in ["+","-","*","**","/","eq","ne","<","<=",">",">=","mod","::","^"]:
    EnterOpp(nm,Mcalc2,nm)
    
for nm in ["hd","tl","~","not","sin","cos","tan","exp","log","log10","abs","sqrt",
    "islist","isword","isstring","isnum","isbool","iseod","id"]:
    EnterOpp(nm,Mcalc1,nm)
    
for nm in ["true","false","pi","phi","eod"]:
    EnterOpp(nm,Mcalc0,nm)
    
    

if __name__ == "__main__":
    if len(sys.argv) == 1:
        apg = Compile("testprog.lu")
    else:
        apg = Compile(sys.argv[1])
    #print('Atomic program')
    #prp.Termln(apg)
    asprog = Assembly(apg)          #turn atomic program into assembler
 
    print('Assembly program')
    for vname in asprog:            #print assembly prorgam
        o,odsa = asprog[vname]
        prp.printf(vname+': ')
        if o == '"':
            prp.printf('" ');pio.WriteItemln(odsa)
            continue
        prp.printf(o+' ')
        for od in odsa: prp.printf(od);prp.printf(' ')
        print()
   
        
    #print('Machine code')
    
    smprog = sma.Assemble(asprog)
    #for v in smprog:
        #print(v,' : ',smprog[v])
    
    driver = ['repeat', 5, ['eval','output','writeln','inctime']]
    Cpusha(driver,3)
    
    Smachinate(smprog)
    #profile.run('Smachinate(smprog)')
    print()
    print(cst.cstacksize,' Cstack frames')
    print(waresaves,' ware saves')
    print(warefetches,' ware fetches')
    print(xcount, ' commands executed')
    print(clc.calccount, ' calculations performed')