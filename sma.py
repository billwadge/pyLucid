""" assembler for stack machine """

import pio,clc,pop


def Assemble(ap): 
    mp = {}
    for v in ap:   #run through and Assemble each variable's definition
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
        mp[v] = (code,len(code))
    return mp


def AssembleLiteral(opds):
    return ['"',opds]

def AssembleStrict(o,opds):
    n = len(opds)
    if n == 2:
        return ['eval',opds[0],'eval',opds[1],o]
    if n == 1:
        return ['eval',opds[0],'eval',o]
    if n == 0:
        return [o]
    code = []
    for opd in opds:
        code.append('eval')
        code.append(opd)
    code = code.append(n);code.append(o)
    return code
    
def AssembleNext(opds):
    return ['inctime','eval',opds[0],'dectime']
    
def AssembleSucc(opds):
    return ['incspace','eval',opds[0],'decspace']
    
def AssembleFby(opds):
    return ['waresearch',['time0','if',['eval',opds[0]],['dectime','eval',opds[1],'inctime']]]
    
def AssembleSby(opds):
    return ['waresearch',['space0','if',['eval',opds[0]],['decspace','eval',opds[1],'incspace']]]
    
def AssembleFirst(opds):
    return ['savetime','zerotime','eval', opds[0], 'restoretime']

def AssembleInit(opds):
    return ['savespace','zerospace','eval', opds[0], 'restorespace']
    
def AssembleAttime(opds):
    return ['waresearch',['eval',opds[1],'savetime','settime', 'eval', opds[0], 'restoretime']]
    
def AssembleAtspace(opds):
    return ['waresearch',['eval',opds[1],'savespace','setspace', 'eval', opds[0], 'restorespace']]
    
def AssembleYcall(opds):
    return ['waresearch',['eval',opds[1],'pushplace','eval',opds[0],'popplace','vpop0']]
    
def AssembleIf(opds):
    print('opds is ',opds)
    print(opds[1])
    return ['waresearch',['eval',opds[0],'if',['eval',opds[1]],['eval',opds[2]]]]
    
    
def AssembleIndex():
    return ['time']
    
def AssembleSindex():
    return ['space']
    
def AssembleAnd(opds):
    return ['waresearch',['eval',opds[0],'if',['eval',opds[1]],['false']]]
    
def AssembleOr(opds):
    return ['waresearch',['eval',opds[0],'if',['true'],['eval',opds[1]]]]
    
def AssembleActual(opds):
    return ['waresearch',['saveplace','popplace','evali',opds,'restoreplace']]
    

    
    