from pop import *
from cst import *
from vst import *
from evl import *
import evl
import pio,gen, clc, profile
returnblock = List1(WordC("return"))
running = False
trace = False
opmap = {}
pmmap = {}
tracing = {}
posttracing = False
icount = 0
waresaves = 0

def Machinate(b):
    """run the machine til the register and cstack are empty """
    global running,block,reg,trace,icount,tracing,posttracing,vstack,vstackptr
    running = True
    Cpush0(returnblock);Cpush0(returnblock);
    block = b
    reg = b
    while (running):
        icount += 1
        #if (EmptyP(reg)): #at end of block
        if (reg == Empty): #at end of block
            Breakxec()
            continue
        
        #token, reg = ConsD(reg)
        k,l =reg
        token,t=l
        reg = ('l',t)
        m,d = token
        """
        if posttracing>0 or trace or (WordP(token) and token in tracing):
            if  (WordP(token) and token in tracing):
                posttracing = 2
            posttracing -= 1
            if posttracing>0 :
                print('......................')
            else:
                print('+++++++++++++++++++++++')
            prp.printf('|blk ');pio.WriteItemln(block)
            prp.printf('|t,r ');pio.WriteItem(token);prp.printf(' ');pio.WriteItemln(reg)
            prp.printf('|vst ');Vdump()
            prp.printf('|tag '); print(evl.treg,evl.sreg,evl.preg)
            print('----------------------')
        """
        #if not WordP(token):    #token is literal
        if m!= 'w':
            if vstackptr == vstacksize:
                Vpush0(token)
            else:
                vstack[vstackptr] = token
                vstackptr += 1
            #Vpush0(token)       #push on to stack
            continue
        if token == QUOTEWord and not reg == Empty: #EmptyP(reg): #a quoted token
            #Vpush0(Head(reg)) #push next item
            #reg = Tail(reg)   #advance reg
            k,l = reg
            h,t = l
            #Vpush0(h)
            if vstackptr == vstacksize:
                Vpush0(h)
            else:
                vstack[vstackptr] = h
                vstackptr += 1
            reg = ('l',t)
            continue
        if not token in opmap:
            print('Undefined popinstruction '+WordName(token))
            exit()
        p = opmap[token]     #a machine instruction
        if token in pmmap: #does it need a parameter?
            p(pmmap[token])
        else:
            p()



def Mblockbegin(b):
    global reg,block
    #/* set up b to be executed */
    #/* execution not attempted by this call */ 
    Cpush0(block)
    """
    if cst.cstackptr == cst.cstacksize:
        Cpush0(block)
    else:
        cst.cstack[cst.cstackptr] = block
        cst.cstackptr += 1
    """
    Cpush0(reg)
    """
    if cst.cstackptr == cst.cstacksize:
        Cpush0(reg)
    else:
        cst.cstack[cst.cstackptr] = reg
        cst.cstackptr += 1
        
    """
    #print('beginning block')
    #pio.WriteItemln(b)
    block = b
    reg = b

def Dupxec():
    t = Vtop0()
    V1push0(t)
    
def Vpop0xec():
    Vpop0()
    #vstackptr -= 1
    
def Doxec():
 	b = Vtop0();
 	Vpop0();
 	Mblockbegin(b);
    
def Ifxec():
    if Vtop0() == TRUEWord:
        b= Vtop(2)
    else:
        b = Vtop(1)
    Vpop(3)
    Mblockbegin(b)

def EnterOp(nm,pr):
    """ enter pr in optable under name nm withouts parm"""
    opmap[WordC(nm)] = pr

def Defxec():
    """ define a popcode subroutine """
    wd = Vpop0()
    body = Vpop0()
    opmap[wd] = Mblockbegin
    pmmap[wd] = body
    
def Ludefxec():
    global ludefs
    nm = pop.WordName(Vpop0())
    code = Vpop0()
    ludefs[nm]=code
    
def Evalxec():
    v = Vtop0()
    #print('evaling ',(v,treg,sreg,preg))
    #nm = WordName(v)
    m,nm = v
    if not nm in ludefs: 
        print(' missing ludef for '+str(nm))
        exit()
    code = ludefs[nm]
    Mblockbegin(code)
 	    
def Breakcxec():
    global reg,block
    b = Vtop0()
    """
    b = vstack[vstackptr-1]
    p = vstack[vstackptr-2]
    """
    p = Vtop(1)
    Vpop(2)
    #vstackptr -= 2
    if p == TRUEWord:
        block = b
        reg = b
        
def Repeatxec():
    """ repeat a block a number of times """
    global block, reg
    count = NumVal(Vpop0()) # number if iterations
    b = Vpop0() # block to be repeated
    if count == 0: return #nothing to do
    Cpush0(block);Cpush0(reg)  #stack current block and reg
    reg = b; block = b   # set up b to be executed
    count -= 1     #decrement count
    c = List3(b, NumC(count), REPEATWord)  #construct reduced repeat
    Cpush0(c);Cpush0(c)                    #set it up to run when b is done

def Forxec():
    """ repeat through a list """
    global block,reg
    items = Vpop0()  #items to be runthrough
    b = Vpop0()      #block to be done for each item
    if EmptyP(items): return #nothing to do
    item, items = ConsD(items)
    Cpush0(block);Cpush0(reg)  #stack current block and reg
    reg = b; block = b   # set up b to be executed
    V1push0(item)         # current item on the stack
    c = List3(b,items,FORWord) #construct reduced repeat
    Cpush0(c);Cpush0(c)                    #set it up to run when b is done
    
    
def Writexec():
    global reg,block
    i = Vpop0()
    pio.WriteItem(i)  
      
def Writelnxec():
    global reg,block
    i = Vpop0()
    pio.WriteItemln(i)

def Breakxec():
    global reg,block,cstack,cstackptr
    reg = Cpop0()
    """
    cst.cstackptr -= 1
    reg = cst.cstack[cst.cstackptr]
    cst.cstackptr -= 1
    block = cst.cstack[cst.cstackptr]
    """
    block = Cpop0()
    
def Loopxec():
    global reg,block
    reg = block;

def Loopcxec():
    global reg,block
    if Vpop0() == TRUEWord:
        reg = block;

def Loopcviaxec():
    global reg,block
    b = Vpop0()
    val = Vpop0()
    if val == TRUEWord:
        reg = block
        Mblockbegin(b)
        
def Returnxec():
    global running
    running = False
    
def Traceonxec():
    global trace
    trace = True
    
def Traceoffxec():
    global trace
    trace = False
    
def Tracexec():
    i = Vpop0()
    tracing[i] = True
    
def Savetimexec():
    Opush(evl.treg)
    
def Settimexec():
    evl.treg = NumVal(Vpop0())
    """
    vstackptr -= 1
    n = vstack[vstackptr]
    evl.treg = NumVal(n)
    """
    
def Setspacexec():
    evl.sreg = NumVal(Vpop0())
    """
    vstackptr -= 1
    n = vstack[vstackptr]
    evl.sreg = NumVal(n)
    """
    
def Savevarxec():
    global ostack, ostackptr, ostacksize
    Opush(evl.vreg)
    """
    if ostackptr == ostacksize:
        Opush(evl.vreg)
    else:
        ostack[ostackptr] = evl.vreg
        ostackptr += 1
    """
def Restorevarxec():
    global ostack, ostackptr, ostacksize
    evl.vreg=Opop()
    """
    ostackptr -= 1
    evl.vreg = ostack[ostackptr]
    """
def Setvarxec():
    evl.vreg = Vpop0()
    """
    vstackptr -= 1
    evl.vreg = vstack[vstackptr]
    """
    #assert WordP(evl.vreg), 'corrupt evl.vreg '+str(evl.vreg)
    
def Restoretimexec():
    evl.treg = Opop()
    
def Savespacexec():
    global ostack, ostackptr, ostacksize
    Opush(evl.sreg)
    """
    if ostackptr == ostacksize:
        Opush(evl.sreg)
    else:
        ostack[ostackptr] = evl.sreg
        ostackptr += 1
    """
def Saveplacexec():
    global ostack, ostackptr, ostacksize
    #Opush(preg)
    if ostackptr == ostacksize:
        Opush(evl.preg)
    else:
        ostack[ostackptr] = evl.preg
        ostackptr += 1
    
def Restorespacexec():
    global ostack, ostackptr, ostacksize
    sreg = Opop()
    """
    ostackptr -= 1
    evl.sreg = ostack[ostackptr]
    """
    
def Restoreplacexec():
    global ostack, ostackptr, ostacksize
    evl.preg = Opop()
    """
    ostackptr -= 1
    evl.preg = ostack[ostackptr]
    """

def Incspacexec():
    evl.sreg += 1
    
def Decspacexec():
    evl.sreg -= 1
    
def Inctimexec():
    evl.treg += 1
    
def Dectimexec():
    evl.treg -= 1
    
def Selectxec():
    n = NumVal(Vpop0())
    l = Vpop0()
    Vpush0(El(n+1,l))
    """
    if vstackptr == vstacksize:
        Vpush0(El(n+1,l))
    else:
        vstack[vstackptr] = El(n+1,l)
        vstackptr += 1
    """
def Pushplacexec():
    h = NumVal(Vpop0())
    """
    vstackptr -= 1
    n = vstack[vstackptr]
    h = NumVal(n)
    """
    evl.preg = evl.Pcons(h,evl.preg)
    #print('preg pushed to ',preg)
    
def Popplacexec():
    Vpush0(NumC(evl.Phead(evl.preg)))
    evl.preg = evl.Ptail(evl.preg)
    #print('preg popped to ',preg)
    
def Timexec():
    V1push0(NumC(evl.treg))
    
def Spacexec():
    V1push0(NumC(evl.sreg))
    
def Waresearchxec():
    tag = (evl.vreg,evl.treg,evl.sreg,evl.preg)
    #print('looking for tag ',tag)
    if tag in evl.warehouse:
        r, age = evl.warehouse[tag]
        #print('found it ',r)
        V3push0(r)
        V3push0(TRUEWord)
        return
    Vpush0(FALSEWord)
    """
    if vstackptr == vstacksize:
        Vpush0(FALSEWord)
    else:
        vstack[vstackptr] = FALSEWord
        vstackptr += 1
    """
def Waresavexec():
    global waresaves
    r = Vtop0()
    #r = vstack[vstackptr-1]
    tag = (evl.vreg,evl.treg,evl.sreg,evl.preg)
    #assert not tag in warehouse, 'resetting  bucket '+str(tag)+' '+str(r)
    #print('storing under tag ',tag,' = ',r)
    evl.warehouse[tag] =(r,0)
    waresaves += 1

def Storexec():
    global popmemory
    ident = Vpop0()
    val = Vpop0()
    popmemory[ident] = val
    
def Fetchxec():
    global popmemory
    ident = Vpop0()
    if not ident in popmemory: 
        pio.printf('Uninitialized identifier: ')
        pio.win(ident);
        exit()
    Vpush0(popmemory[ident])
    
def EnterOpp(s,p,m):
    global opmap, pmmap
    """register popcode command s as  procedure p with parameter m """
    opmap[WordC(s)] = p
    pmmap[WordC(s)] = m
    

def Mcalc0(nm):
    V1push0(clc.Calculate(nm,[]))

def Mcalc1(nm):
    """ perform unary operation nm on vstack """
    opds = [Vpop0()]
    V1push0(clc.Calculate(nm,opds))
    
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

EnterOp("do",Doxec);
EnterOp("loop",Loopxec);
EnterOp("loopc",Loopcxec);
EnterOp("loopcvia",Loopcviaxec)
EnterOp("if",Ifxec)
EnterOp("traceon",Traceonxec)
EnterOp("traceoff",Traceoffxec)
EnterOp("trace",Tracexec)
EnterOp("break",Breakxec);
EnterOp("repeat",Repeatxec)
EnterOp("for",Forxec)
EnterOp("write",Writexec)
EnterOp("dup", Dupxec)
EnterOp("vpop0", Vpop0xec)
EnterOp("def", Defxec)
EnterOp("writeln",Writelnxec)
EnterOp("return",Returnxec)
EnterOp("breakc",Breakcxec)
EnterOp("ludef",Ludefxec)
EnterOp("eval",Evalxec)
EnterOp("select",Selectxec)
EnterOp("setvar",Setvarxec)
EnterOp("savevar",Savevarxec)
EnterOp("restorevar",Restorevarxec)
EnterOp("savetime",Savetimexec)
EnterOp("restoretime",Restoretimexec)
EnterOp("savespace",Savespacexec)
EnterOp("restorespace",Restorespacexec)
EnterOp("saveplace",Saveplacexec)
EnterOp("restoreplace",Restoreplacexec)
EnterOp("settime",Settimexec)
EnterOp("setspace",Setspacexec)
EnterOp("inctime", Inctimexec)
EnterOp("dectime", Dectimexec)
EnterOp("incspace", Incspacexec)
EnterOp("decspace", Decspacexec)
EnterOp("space", Spacexec)
EnterOp("time", Timexec)
EnterOp("pushplace", Pushplacexec)
EnterOp("popplace", Popplacexec)
EnterOp("waresearch", Waresearchxec)
EnterOp("waresave", Waresavexec)
EnterOp("->",Storexec)
EnterOp("<-",Fetchxec)
"""
#EnterOp("break2c",Break2cxec);
EnterOp("if",Ifxec);
#EnterOp("case",Casexec);
#EnterOp("ncase",Ncasexec);
#EnterOp("repeat",Repeatxec);
#EnterOp("for",Forxec);
#EnterOp("abort",Abortxec);
#EnterOp("trace",Tracexec);
EnterOp("quit",Quitxec);
#EnterOp("call",Callxec);
#EnterOp("arg",Argxec);
EnterOp("return",Returnxec);
EnterOp("(",Vstbeginlayerxec);
EnterOp(")",Vstendlayerxec);
"""

BREAKwrd = WordC("break")
QUOTEwrd = WordC('"')
REPEATWord = WordC("repeat")
FORWord = WordC("for")

ostack = []
ostackptr = 0
ostacksize = 0
ludefs = {}
popmemory = {}

    
def Opush(x):
    global ostack, ostackptr, ostacksize
    #print('Opushing ',x)
    if ostackptr == ostacksize:
        ostack.append(x)
        ostackptr += 1
        ostacksize += 1
    else:
        ostack[ostackptr] = x
        ostackptr += 1
    
def Opop():
    """ the element atop the ostack """
    global ostack, ostackptr, ostacksize
    ostackptr -= 1
    #print('Opopping ',ostack[ostackptr])
    return ostack[ostackptr]

block = Empty; reg = Empty;

returnblock = List1(WordC("return"))

if __name__ == "__main__":
    if len(sys.argv) == 1:
        apg = Compile("testprog.lu")
    else:
        apg = Compile(sys.argv[1])
    print('Atomic program')
    prp.Termln(apg)
    asprog = Assembly(apg)          #turn atomic program into assembler
    #print('Assembly program')
    """
    for vname in asprog:            #print assembly prorgam
        o,odsa = asprog[vname]
        prp.printf(vname+': ')
        if o == '"':
            prp.printf('" ');pio.WriteItemln(odsa)
            continue
        prp.printf(o+' ')
        for od in odsa: prp.printf(od);prp.printf(' ')
        print()
    """
    m = asm.Assemble(asprog)
    
    mprog = pop.Empty   #the popcode program
    
    for v in m:
        df = pio.Popliteral('['+pio.Items(m[v])+' "'+v+' ludef]')
        mprog = pop.Append(mprog,df)
        
    
    #print('---------------- Popcode -----------------')
    driver = pio.Popliteral('[traceon [ " output eval writeln inctime] 100 repeat]')
    mprog = Append(mprog,driver)
    #pio.WriteItemln(mprog)
    #profile.run('mch.Machinate(mprog)')
    mch.Machinate(mprog)
    print(mch.icount,' instructions executed')
    print(mch.waresaves, ' warehouse saves')
    print(vstacksize, 'size of vstack')
    print(cst.cstacksize, 'size of cstack')
    exit()
