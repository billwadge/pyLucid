import pio,prp,exp,gen,prs,atz,pop,pre,ali,ari,map,ren,glb,ewh,sys,asm,clc,elp
from clc import *
import profile

codetable = {}
head = {}
tail = {}
warehouse = {}
Pempty = 0
fetchedvars = set()


newcode = 0
vreg=pop.WordC("error")
treg=0   #t0
htreg=[] #t1 t2 t3 etc
sreg=0
preg = Pempty
evalcount = 0
actcount = 0
evaldepth  = 0
wsaves = 0
wfinds = 0
nextindex = 0
endoffile = False
ig = pio.ItemGenStringC('')

def Pcons(i,t):
    """ the hashcons (code) for the place code with head i and tail code t """
    global newcode
    if (i,t) in codetable: return codetable[(i,t)]
    newcode += 1
    codetable[(i,t)] = newcode
    head[newcode] = i
    tail[newcode] = t
    return newcode 
    
def PconsD(l):
    return head[l],tail[l]
    
def Ptail(l):
    return tail[l]

def Phead(l):
    return head[l]

def Eval(ap,nm):
    """value of nm in assembly program ap"""
    global AssemblyProgram,warehouse
    AssemblyProgram = ap
    s,val = EvalVar(nm)
    return val
    
def WevalVar(v):
    global warehouse,wsaves,wfinds,fetchedvars
    tag = (v,treg,tuple(htreg),sreg,preg)
    #print('Searching ',tag)
    if tag in warehouse:
        val,age = warehouse[tag]
        #print('got ',val, ' from wh')
        wfinds += 1
        fetchedvars.add(v)
        return val
    save, val = EvalVar(v)
    if save :
        warehouse[tag] = [val,0]
        wsaves += 1
        #print('Saving '+str(tag)+' = '+str(val))
    return val
    
def ev(v):
    return NumVal(WevalVar(v))
       
    
def EvalVar(v):
    """ value of var named v at time treg and place preg in AssemblyProgram"""
    global evalcount
    global AssemblyProgram, strict,treg,htreg,sreg,preg
    evalcount += 1
    #print((v,treg,tuple(htreg),sreg,preg),flush=True)
    o, opds = AssemblyProgram[v]
    if o in strict: 
        return False,EvalStrict(o,opds)
    if o == '"': return False,opds           #opds is actually the literal value
    waresave = o in wareables
    if o in evs: return waresave, evs[o](opds)
    assert False, 'ill defined variable: '+v+' '+o
    
def If(opds):
    p = WevalVar(opds[0])
    if p == EODWord: return EODWord
    if p == EOSWord: return EOSWord
    if pop.BoolVal(p):
        return WevalVar(opds[1])
    else:
        return WevalVar(opds[2])
        
def Attime(opds):
    global treg
    tsave = treg
    o1 = WevalVar(opds[1])
    if o1==EODWord or o1 == EOSWord: return o1
    treg = NumVal(o1)
    val = WevalVar(opds[0])
    treg = tsave
    return val
        
def Atspace(opds):
    global sreg
    ssave = sreg
    o1 = WevalVar(opds[1])
    if o1==EODWord or o1 == EOSWord: return o1
    sreg = NumVal(o1)
    val = WevalVar(opds[0])
    sreg = ssave
    return val
    
def Fby(opds):
    global treg
    if treg > 0: 
        treg -= 1
        val=WevalVar(opds[1])
        treg +=1
        return val
    return WevalVar(opds[0])
    
def Ybf(opds):
    global treg
    if treg < 0: 
        treg += 1
        val=WevalVar(opds[0])
        treg -=1
        return val
    return WevalVar(opds[1])
    
def Sby(opds):
    global sreg
    if sreg > 0: 
        sreg -= 1
        val=WevalVar(opds[1])
        sreg +=1
        return val
    return WevalVar(opds[0])
    
def First(opds):
    global treg
    tsave = treg
    treg=0
    val = WevalVar(opds[0])
    treg = tsave
    return val
    
def Init(opds):
    global sreg
    ssave = sreg
    sreg=0
    val = WevalVar(opds[0])
    sreg = ssave
    return val
    
def Next(opds):
    global treg
    treg += 1
    val = WevalVar(opds[0])
    treg -= 1
    return val
    
def Index(opds):
    global treg
    return NumC(treg)


def Hash(opds):
    global treg
    n = WevalVar(opds[0])
    tsave = treg
    treg  = NumVal(n)
    val = Input(opds)
    treg = tsave
    return val
    
def Dollar(opds):
    global sreg
    n = WevalVar(opds[0])
    ssave = treg
    sreg  = NumVal(n)
    val = Input(opds)
    sreg = ssave
    return val


    
def Iseod(opds):
    #print("Iseod called with ",opds)
    val = WevalVar(opds[0])
    if val == EODWord:
        return TRUEWord
    else:
        return FALSEWord
        
def Iseos(opds):
    val = WevalVar(opds[0])
    if val == EOSWord: return TRUEWord
    if val == EODWord: return EODWord
    return FALSEWord
"""      
def Input(opds):
    global warehouse, nextindex,  endoffile, treg,ig
    if treg < nextindex: #already read it in, should be in warehouse
        tag = ('input',treg,(),0,0)
        if tag in warehouse:
            val,age = warehouse[tag]   
            return val
        assert False, 'lost input'
    if endoffile: # reached the end of file, result is eod
        return EODWord
    tsave = treg
    treg = nextindex
    while True: # read up to current treg or eod
        i = pio.NextItem(ig)
        #print('Reading i: ',i)
        if i != '': 
            warehouse[('input',treg,(),0,0)] = (i,0)
            if  treg == tsave:
                nextindex = treg+1
                return i
            treg += 1
            continue
       
        try:
            buff = input()
        except:
            endoffile = True
            nextindex  = treg
            treg = tsave
            return EODWord
        ig = pio.ItemGenStringC(buff)
        
"""
def Input(opds):
    global warehouse, nextindex,  endoffile, treg,sreg,ig
    if treg < nextindex: #already read it in, should be in warehouse
        tag = ('input',treg,(),sreg,0)
        if tag in warehouse:
            age,val = warehouse[tag]   
            return val
        assert False, 'lost input'
    if endoffile: # reached the end of file, result is eod
        return EODWord
    tsave = treg
    ssave = sreg
    treg = nextindex #read in whole lines
    sreg = 0
    while True:   
        try:
            buff = input()
        except:
            endoffile = True
            nextindex  = treg
            treg = tsave
            sreg = ssave
            return EODWord
        ig = pio.ItemGenStringC(buff)  
        while pio.CurrentItem(ig) != '':
            tag = ('input',treg,(),sreg,0)
            warehouse[tag] = (0,pio.NextItem(ig))
            sreg += 1
        warehouse[('input',treg,(),sreg,0)] = (0,EOSWord)
        sreg = 0
        treg += 1
        if treg >tsave: break
    treg = tsave
    sreg = ssave
    nextindex = treg+1
    tag = ('input',treg,(),sreg,0)
    age,val = warehouse[tag]
    return val
    


def Pre(opds):
    global treg
    treg -= 1
    val = WevalVar(opds[0])
    treg += 1
    return val
    
def Asa(opds):
    global treg
    x = opds[0]
    p = opds[1]
    streg = treg
    treg = 0
    while True:
        pv = WevalVar(p)
        if pv==EOSWord or pv==EODWord:
            treg = streg
            return pv
        pb = BoolVal(pv)
        if pb:break
        treg += 1
    val = WevalVar(x)
    treg = streg
    return val
        
def Succ(opds):
    global sreg
    sreg += 1
    val = WevalVar(opds[0])
    sreg -= 1
    return val
    
def Sindex(opds):
    global sreg
    return NumC(sreg)
    
def Apply(opds):
    funbody = WevalVar(opds[0]) #function body as a pop string
    n = len(opds) - 1
    while True:
        funarg = WevalVar(opds[1])
        x = NumVal(funarg)
        if n==1: break
        funarg = WevalVar(opds[2])
        y = NumVal(funarg)
        if n == 2: break
        funarg = WevalVar(opds[3])
        z = NumVal(funarg)
        if n==3: break 
        assert False, 'too many args to apply '+str(n)
    funbodys = pio.Items(funbody)[1:-1] #scrap quotes
    #print('funbodys ',funbodys)
    res = eval(funbodys)
    return NumC(res)
    
    
def CONTEMP(opds):
    htreg.insert(0,treg)
    val = WevalVar(opds[0])
    htreg.pop(0)
    return val
    
def ACTIVE(opds):
    global htreg
    z = htreg.pop(0)
    val = WevalVar(opds[0])
    htreg.insert(0,z)
    return val
    
def FIRST(opds):
    global htreg
    z = htreg[0]
    htreg[0] = 0
    val = WevalVar(opds[0])
    htreg[0] = z
    return val
    
def NEXT(opds):
    global htreg
    htreg[0] += 1
    val = WevalVar(opds[0])
    htreg[0] -= 1
    return val
    
def FBY(opds):
    global htreg
    if htreg[0] == 0: return WevalVar(opds[0])
    htreg[0] -= 1
    val = WevalVar(opds[1])
    htreg[0] += 1
    return val
    
def CURRENT(opds):
    global treg, htreg
    tsave = treg
    treg = htreg[0]
    val = WevalVar(opds[0])
    treg = tsave
    return val
    
def INDEX(opds):
     global htreg
     return NumC(htreg[0])
     
def ATTIME2(opds):
    t0 = WevalVar(opds[1])
    t1 = WevalVar(opds[2])
    s0 = treg
    s1 = htreg[0]
    treg = t0
    htreg[0] = t1
    val = WevalVar(opds[0])
    htreg[0] = s1
    treg = s0
    return val
     
"""
k = index asa p;
ktot = 0 FBY ktot+k;
X ATTIME2(T0,T1)

p  f  f  f  t ... t ... f  t ... f  f  f  f  f t ....
t0 0  1  2              0        0  1  2  3  4
t1 0  0  0              2        3  3  3  3  3

3 0 1 5 ...
||
V
0 1 2 3 0 0 1 0 1 2 3 4 5 ...
||
V
0 1 2 0 1 0 1 2 3 4 ...



"""
    

def Actual(opds):
    global preg,actcount
    actcount += 1
    ph,pt = PconsD(preg)
    act = opds[ph]
    psave = preg
    preg = pt
    val = WevalVar(act)
    preg =psave
    return val
    
def Ycall(opds):
    global preg
    n = NumVal(WevalVar(opds[1])) 
    f = opds[0]
    psave =preg
    preg = Pcons(n,preg)
    val = WevalVar(f)
    preg = psave
    return val


def And(opds):
    p = WevalVar(opds[0])
    if not pop.BoolVal(p):
        return pop.FALSEWord
    else:
        return WevalVar(opds[1])
        
def Or(opds):
    p = WevalVar(opds[0])
    if pop.BoolVal(p):
        return pop.TRUEWord
    else:
        return WevalVar(opds[1])

wareables ={'fby','ybf','sby','asa','attime','Fby','contemp','current','if','and','or','actual','ycall'}
evs = {}
evs['first']=First; evs['next'] = Next; evs['fby'] = Fby; evs['pre'] = Pre; evs['ybf'] = Ybf
evs['asa'] = Asa; evs['attime'] = Attime; evs['index'] = Index; evs['#'] = Hash; evs['$'] = Dollar
evs['init'] = Init; evs['succ'] = Succ; evs['sby'] = Sby; evs['&'] = Sby; evs['sindex'] = Sindex
evs['iseod'] = Iseod; evs['iseos'] = Iseos
evs['if'] = If; evs['and'] = And; evs['or']=Or; evs['input'] = Input
evs['ycall'] = Ycall; evs['actual'] = Actual;
evs['active'] = ACTIVE; evs['contemp'] = CONTEMP; evs['current'] = CURRENT; 
evs['First'] = FIRST; evs['Next'] = NEXT; evs['Fby'] = FBY; evs['Index'] = INDEX
evs['Attime2'] = ATTIME2; evs['apply'] = Apply


def EvalStrict(o,opds):
    """ evaluate a strict data operation o applied to operands opds (var names) """
    #print('evalstr ',o,opds)
    resarray = []   
    foundeos = False  
    for w in opds: #evaluate opds and collect array of results
        r = WevalVar(w)    #evaluate operand
        if pop.EodP(r):       # if eod shows up
            return pop.Eod     #return eod
        if pop.EosP(r): foundeos = True
        resarray.append(r) # collect result
        #print('added to resarray ',r)
    if foundeos: return pop.Eos
    #print('resarray ',resarray);exit()
    return Calculate(o,resarray) # calculate results


    """ produce assembly program asprog 
        a dictionary  which assigns to each variable an array of strings
        the operator followed by the operands
    """
def Assembly(aprog):
    """ convert atomic program aprog to assembly program asprog """
    asprog = {}
    subj,wk,dl = exp.WhereD(aprog)
    if exp.VarP(subj):
        subj = exp.Operation1C(exp.IDWord,subj)
    odef = exp.DefinitionC(exp.VarC(exp.OUTPUTWord),pop.EQUALWord,subj)
    dl = pop.Cons(odef,dl)
    asprog={}   #initialize the assembly program, a dictionary
            #that assigns to every variable name a tuple consisting
            #of the operation symbol and the array of the names of the variables
            #all python strings
    while dl != pop.Empty:              #loop through the definitions of the atomized program
        df,dl = pop.DeCons(dl) 
        lhs,es,rhs = exp.DefinitionD(df)  #dismantle current definition
        vname = pio.Words(exp.Var(lhs)) #get name of var being defined
        if exp.LiteralP(rhs):           #if its a literal treat quote mark as a pseudo op
            asprog[vname]= ('"',exp.LiteralValue(rhs))
            continue
        if exp.VarP(rhs):              # rhs a single variable, add id operator
            rhs = exp.Operation1C(exp.IDWord,rhs)
                                   #its an operation applied to operands
        o,ods = exp.OperationD(rhs)    #break rhs into operation symbol and operand list
        odsa = []                      #initialize array of operands
        while ods != pop.Empty:        #iterate through operand list
            vw, ods = pop.ConsD(ods)  #get current operand, a var, and advance
            vws = pio.Words(exp.Var(vw))        #name of current operand, a var, as a string
            odsa.append(vws)    #append to the array
                                           #finished looping throug operands, so odsa complete
        asprog[vname] = (pio.Words(o),odsa)
    return asprog

def Compile(f):
    """ compile the program in file f to atomic equations """
    pio.parsing=True
    pg = prs.ParseFile(f)
    print('Program is ')
    #pio.WriteItemln(pg)
    prp.Termln(pg);
    print('Defs to import ',prs.defined)
    defs = pop.Empty
    for w in prs.defined:        #read parse and add defs of defined operators like wvr
        wname = WordName(w)
        f = open("defs/"+wname+".lu","r")
        sourcedef = f.read()
        f.close()
        ig = pio.ItemGenStringC(sourcedef)
        df = prs.Definition(ig)
        #print('Adding df')
        #prp.Termln(df);exit()
        defs = pop.AddElement(defs,df)
    subj,wk,body = exp.WhereD(pg)
    body = pop.Append(body,defs)     #add imported definitions
    pg = exp.WhereC(subj,wk,body)
    print('Expanded program')
    prp.Termln(pg)
    #print("check locals")
    pre.CheckLocals(pg)
    print("check dups")
    pre.CheckDups(pg)
    print("check embeddings")
    pre.ProgramEmbedded(pg)
    print('renamed program ')
    rpg = ren.Rename(pg,pop.EmptySet)
    prp.Termln(rpg)
   
    m = ari.Aritytab(rpg,map.EmptyMap)
    ok,var,arity = ari.ArityCheck(rpg,m)
    if ok:
        k =  1
        print('arities check out ')
    else:
        prp.printf("Variable ")
        pio.WriteItem(var)
        prp.printf(" should have arity ")
        print(arity)
        exit()
    lpg = elp.Eloop(rpg,map.EmptyMap)
    print('Delooped program ')
    prp.Termln(lpg)
    
    fpg = ewh.Eprogram(lpg)
    print('flattened program')
    pio.WriteItemln(fpg)
    prp.Termln(fpg)
 
    atab,ftab, ypg = ali.ActualTable(fpg,map.EmptyMap,map.EmptyMap)
    print('alified program')
    prp.Termln(ypg);
    defs = ali.ActualDefs(atab,ftab)
    subj,wk,body =  exp.WhereD(ypg)
    body = pop.Append(body,defs) #add ali defs
    ypg = exp.WhereC(subj,wk,body)
    #print('globalized program')
    ypg = glb.Gprogram(ypg)
    #prp.Termln(ypg)
    print('reflattend program') 
    ypg = ewh.Eprogram(ypg)
    prp.Termln(ypg)
    print('atomized program')
    apg,dfs = atz.Aexpr(ypg)
    prp.Termln(apg)
    return apg
  
    
def AssemblyDisplay(asprog):
    for vname in asprog:
        o,odsa = asprog[vname]
        prp.printf(vname+': ')
        if o == '"':
            prp.printf('" ');pio.WriteItemln(odsa)
            continue
        prp.printf(o+' ')
        for od in odsa: prp.printf(od);prp.printf(' ')
        print()

if __name__ == "__main__":
    pio.parsing = True
    if len(sys.argv) == 1:
        print('Compiling testprog.lu')
        apg = Compile("testprog.lu")
    else:
        print('Compiling ',sys.argv[1])
        apg = Compile(sys.argv[1])
        
   
    
    asprog = Assembly(apg)
    #print('------------- Assembly Program -------------')
    AssemblyDisplay(asprog)
    
    
    #sys.setrecursionlimit(10000)
    
    # evaluate pronouns 
    columns = 1
    rows = 3
    numformat = ''
    if "rows" in asprog: rows = NumVal(Eval(asprog,"rows"))
    if "columns" in asprog: columns = NumVal(Eval(asprog,"columns"))
    if "numformat" in asprog: pio.numformat = StringVal(Eval(asprog,"numformat"))
    
#def runprog():
    for t in range(rows):
        treg = t
        for s in range(columns):
            sreg = s
            val = Eval(asprog,"output")
            if EosP(val) or EodP(val): break
            pio.WriteItem(val)
            pio.printf(' ')
        print()
        if pop.EodP(val): break
    #runprog()
    print('Number of evals: '+str(evalcount))
    print('warehouse saves '+str(wsaves)+' warehouse finds '+str(wfinds))
    print('Number of place codes generated '+str(newcode))
    print('Number of calculations ',clc.calccount)
    print("Vars fetched ",fetchedvars)
   
    