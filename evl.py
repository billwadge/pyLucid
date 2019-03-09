import pio,prp,exp,gen,prs,atz,pop,pre,ali,ari,map,ren,glb,ewh,sys,asm,mch,vst,cst,clc
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
treg=0
sreg=0
preg = Pempty
evalcount = 0
actcount = 0
evaldepth  = 0
wsaves = 0
wfinds = 0

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
    tag = (v,treg,sreg,preg)
    #print('Searching ',tag)
    if tag in warehouse:
        val,age = warehouse[tag]
        wfinds += 1
        fetchedvars.add(v)
        return val
    save, val = EvalVar(v)
    if save :
        warehouse[tag] = [val,0]
        wsaves += 1
        #print('Saving '+str(tag)+' = '+str(val))
    return val
       
    
def EvalVar(v):
    """ value of var named v at time treg and place preg in AssemblyProgram"""
    global evalcount
    global AssemblyProgram, strict,treg,sreg,preg
    evalcount += 1
    #print((v,treg,sreg,preg),flush=True)
    o, opds = AssemblyProgram[v]
    if o in strict: 
        return False,EvalStrict(o,opds)
    if o == '"': return False,opds           #opds is actually the literal value
    if o == 'fby': return True,Fby(opds)
    if o == 'ybf': return True,Ybf(opds)
    if o == 'sby': return True,Sby(opds)
    if o == 'first':return False, First(opds)
    if o == 'init':return False, Init(opds)
    if o == 'next':return False, Next(opds)
    if o == 'pre':return False, Pre(opds)
    if o == 'succ':return False, Succ(opds)
    if o == 'if': return True,If(opds)
    if o == 'actual': return True, Actual(opds)
    if o == 'ycall': return True, Ycall(opds)
    if o == 'and': return True, And(opds)
    if o == 'attime': return True, Attime(opds)
    if o == 'atspace': return True, Atspace(opds)
    if o == 'index': return False, NumC(treg) 
    if o == 'sindex': return False, NumC(sreg) 
    assert False, 'ill defined variable: '+v+' '+o
    
def If(opds):
    p = WevalVar(opds[0])
    if pop.BoolVal(p):
        return WevalVar(opds[1])
    else:
        return WevalVar(opds[2])
        
def Attime(opds):
    global treg
    tsave = treg
    treg = NumVal(WevalVar(opds[1]))
    val = WevalVar(opds[0])
    treg = tsave
    return val
        
def Atspace(opds):
    global sreg
    ssave = sreg
    sreg = NumVal(WevalVar(opds[1]))
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
    
def Pre(opds):
    global treg
    treg -= 1
    val = WevalVar(opds[0])
    treg += 1
    return val
    
def Succ(opds):
    global sreg
    sreg += 1
    val = WevalVar(opds[0])
    sreg -= 1
    return val

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
    

def EvalStrict(o,opds):
    """ evaluate a strict data operation o applied to operands opds (var names) """
    resarray = []   
    foundeos = False  
    for w in opds: #evaluate opds and collect array of results
        r = WevalVar(w)    #evaluate operand
        if pop.EodP(r):       # if eod shows up
            return pop.Eod     #return eod
        if pop.EosP(r): foundeos = True
        resarray.append(r) # collect result
    if foundeos: return pop.Eos
    return Calculate(o,resarray) # calculate results


    """ produce assembly program asprog 
        a dictionary  which assigns to each variable an array of strings
        the operator followed by the operands
    """
def Assembly(aprog):
    """ convert atomic program aprog to assembly program asprog """
    asprog = {}
    subj,dl = exp.DeWhere(aprog)
    if exp.VarP(subj):
        subj = exp.Operation1C(exp.IDWord,subj)
    odef = exp.DefinitionC(exp.VarC(exp.OUTPUTWord),subj)
    dl = pop.Cons(odef,dl)
    asprog={}   #initialize the assembly program, a dictionary
            #that assigns to every variable name a tuple consisting
            #of the operation symbol and the array of the names of the variables
            #all python strings
    while dl != pop.Empty:              #loop through the definitions of the atomized program
        df,dl = pop.DeCons(dl) 
        lhs,rhs = exp.DeDefinition(df)  #dismantle current definition
        vname = pio.Words(exp.Var(lhs)) #get name of var being defined
        if exp.LiteralP(rhs):           #if its a literal treat quote mark as a pseudo op
            asprog[vname]= ('"',exp.LiteralValue(rhs))
            continue
        if exp.VarP(rhs):              # rhs a single variable, add id operator
            rhs = exp.Operation1C(exp.IDWord,rhs)
                                   #its an operation applied to operands
        o,ods = exp.DeOperation(rhs)    #break rhs into operation symbol and operand list
        odsa = []                      #initialize array of operands
        while ods != pop.Empty:        #iterate through operand list
            vw, ods = pop.DeCons(ods)  #get current operand, a var, and advance
            vws = pio.Words(exp.Var(vw))        #name of current operand, a var, as a string
            odsa.append(vws)    #append to the array
                                           #finished looping throug operands, so odsa complete
        asprog[vname] = (pio.Words(o),odsa)
    return asprog

def Compile(f):
    """ compile the program in file f to atomic equations """
    pg = prs.ParseFile(f)
    #print('Program is ')
    #pio.WriteItemln(pg)
    #prp.Termln(pg);
    f = open("import.lu","r")
    imp = f.read()
    f.close()
    ig = pio.ItemGenStringC(imp)
    i = pio.CurrentItem(ig)
    defs = prs.Definitions(ig)
    #print('Imported defs')
    #pio.WriteItemln(defs)
    subj,body = exp.WhereD(pg)
    #body = Append(body,defs)     #add imported definitions
    pg = exp.WhereC(subj,body)
    #print('Expanded program')
    #prp.Termln(pg)
    #print("check locals")
    pre.CheckLocals(pg)
    #print("check dups")
    pre.CheckDups(pg)
    #print("check embeddings")
    pre.ProgramEmbedded(pg)
    m = ari.Aritytab(pg,map.EmptyMap)
    ok,var,arity = ari.ArityCheck(pg,m)
    if ok:
        k =  1
        #print('arities check out ')
    else:
        prp.printf("Variable ")
        pio.WriteItem(var)
        prp.printf(" should have arity ")
        print(arity)
        exit()
    #print('renamed program ')
    rpg = ren.Rename(pg,pop.EmptySet)
    #prp.Termln(rpg)
    fpg = ewh.Eprogram(rpg)
    #print('flattened program')
    #prp.Termln(fpg)
    atab,ftab, ypg = ali.ActualTable(rpg,map.EmptyMap,map.EmptyMap)
    #print('alified program')
    #prp.Termln(ypg);
    defs = ali.ActualDefs(atab,ftab)
    subj,body =  exp.WhereD(ypg)
    body = pop.Append(body,defs) #add ali defs
    ypg = exp.WhereC(subj,body)
    #print('globalized program')
    ypg = glb.Gprogram(ypg)
    #prp.Termln(ypg)
    #print('reflattend program') 
    ypg = ewh.Eprogram(ypg)
    #prp.Termln(ypg)
    #print('atomized program')
    apg,dfs = atz.Aexpr(ypg)
    #prp.Termln(apg)
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
    if len(sys.argv) == 1:
        print('Compiling testrpog.lu')
        apg = Compile("testprog.lu")
    else:
        print('Compiling ',sys.argv[1])
        apg = Compile(sys.argv[1])
    asprog = Assembly(apg)
    #print('------------- Assembly Program -------------')
    AssemblyDisplay(asprog)
    sys.setrecursionlimit(10000)
    """ evaluate pronouns """
    columns = 1
    rows = 3
    numformat = ''
    if "rows" in asprog: rows = NumVal(Eval(asprog,"rows"))
    if "columns" in asprog: columns = NumVal(Eval(asprog,"columns"))
    if "numformat" in asprog: pio.numformat = StringVal(Eval(asprog,"numformat"))
    """
    
    """
   
    """ eval program and print result """
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