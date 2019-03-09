""" assembler turning assembly into popcode """

"""
a : " v        [" v]
a : + b c      [ breakc "a eval "b eval + ]
a : next b     [ inctime "b eval dectime ]
a : first b    [ savetime 0  settime "b eval restoretime ]
a : fby b c    [ waresearch breakc ["b eval] [dectime "c eval inctime] time 0 eq if waresave]
a : ycall b i  [ waresearch breakc i pushplace "b eval popplace dup waresave]
a : actual a b c d ...
               [ waresearch breakc [ a b c d ... ] saveplace popplace ncase eval waresave ]
a : attime b c [ waresearch breakc "c eval savetime settime "b eval restoretime waresave ]
a : index      [ time ]
a : if p x y   [ waresearch breakc "x "y "p eval if eval waresave ]
a : or p q     [ "p eval [" true] breakc "q eval ]
a : and p q    [ "p eval not ["false] breakc "q eval ]
a : [% x y z   [ "x eval "y eval "z eval 3 [% ]

"""
import pio,clc,pop


def Assemble(ap): 
    mp = {}
    for v in ap:   #run through and Assemble each variables definition
        while True:
            o,opds = ap[v]
            if o == '"': code =  AssembleLiteral(opds); break
            if o in clc.strict:  code =   AssembleStrict(o,opds); break
            if o == 'fby': code =  AssembleFby(opds); break
            if o == 'sby': code =  AssembleSby(opds); break
            if o == 'first':code =  AssembleFirst(opds); break
            if o == 'init': code =   AssembleInit(opds); break
            if o == 'next': code =   AssembleNext(opds); break
            if o == 'succ': code =   AssembleSucc(opds); break
            if o == 'if':  code =  AssembleIf(opds); break
            if o == 'actual':  code =   AssembleActual(opds); break
            if o == 'ycall':  code =   AssembleYcall(opds); break
            if o == 'and':  code =   AssembleAnd(opds); break
            if o == 'or':  code =   AssembleOr(opds); break
            if o == 'attime':  code =   AssembleAttime(opds); break
            if o == 'atspace':  code =   AssembleAtspace(opds); break
            if o == 'index':  code =   AssembleIndex(); break
            if o == 'sindex':  code =   AssembleSindex(); break
            assert False, 'ill defined variable: '+v+' '+o
        mp[v] = code
    return mp


def AssembleLiteral(opds):
    return pop.List3(pop.WordC("vpop0"),pop.QUOTEWord,opds)

def AssembleStrict(o,opds):
    n = len(opds)
    if n == 2:
        return(pio.Popliteral('[vpop0 "%s eval "%s eval %s]'%(opds[0],opds[1],o)))
    if n == 1:
        return pio.Popliteral('[vpop0 "%s eval %s]'%(opds[0],o))
    if n == 0:
        return pio.Popliteral('[vpop0 %s]' % o)
    code = '[vpop0 '
    for opd in opds:
        code = code + ' "%s eval ' % opd
    code = code + ('%s %s]' % (str(n),o))
    #print(code);exit()
    return pio.Popliteral(code)
    
def AssembleNext(opds):
    return pio.Popliteral('[ vpop0 inctime "%s eval dectime ]' % opds[0])
    
def AssembleSucc(opds):
    return pio.Popliteral('[ vpop0 incspace "%s eval decspace ]' % opds[0])
    
def AssembleFby(opds):
    return pio.Popliteral('[ savevar setvar waresearch [restorevar] breakc ["%s eval] [dectime "%s eval inctime] time 0 eq if waresave restorevar]'%(opds[0],opds[1]))
    
def AssembleSby(opds):
    return pio.Popliteral('[ savevar setvar waresearch [restorevar] breakc ["%s eval] [decspace "%s eval incspace] space 0 eq if waresave restorevar]'%(opds[0],opds[1]))

def AssembleFirst(opds):
    return pio.Popliteral('[ vpop0 savetime 0 settime "%s eval restoretime ]'%opds[0])

def AssembleInit(opds):
    return pio.Popliteral('[ vpop0 savespace 0 setspace "%s eval restorespace ]'%opds[0])
    
def AssembleAttime(opds):
    return pio.Popliteral('[ savevar setvar waresearch [restorevar] breakc "%s eval savetime settime "%s eval restoretime waresave restorevar ]'%(opds[1],opds[0]))
    
def AssembleAtspace(opds):
    return pio.Popliteral('[ savevar setvar waresearch [restorevar] breakc "%s eval savespace setspace "%s eval restorespace waresave restorevar ]'%(opds[1],opds[0]))
    
def AssembleYcall(opds):
    return pio.Popliteral('[ savevar setvar waresearch [restorevar] breakc "%s eval pushplace "%s eval popplace vpop0 waresave restorevar]'%(opds[1],opds[0]))
    
def AssembleIf(opds):
    return pio.Popliteral('[ savevar setvar waresearch [restorevar] breakc ["%s eval]["%s eval]"%s eval if waresave restorevar ]'%(opds[1],opds[2],opds[0]))
    
def AssembleIndex():
    return pio.Popliteral('[vpop0 time]')
    
def AssembleSindex():
    return pio.Popliteral('[vpop0 space]')
    
def AssembleAnd(opds):
    return pio.Popliteral('[vpop0 "%s eval not ["false] breakc "%s eval ]' % (opds[0],opds[1]))
    
def AssembleOr(opds):
    return pio.Popliteral('[vpop0 "%s eval ["true] breakc "%s eval ]' % (opds[0],opds[1]))
    
def AssembleActual(opds):
    s = ''
    for opd in opds:
        s = s+' '+opd
    return pio.Popliteral('[ savevar setvar waresearch [restorevar] breakc [ %s] saveplace popplace select eval restoreplace waresave restorevar ]' % s)
    
    
    
if __name__ == "__main__":
    o = "[%"
    opds = ["a","b","c","d"]
    pio.WriteItemln(AssembleActual(opds))