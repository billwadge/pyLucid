from exp import *
import gen,pop,pio,prs,prp

def CheckDups(e):
    """ check there are no duplicated locals in (e) """
    #print("Checking "+pio.Items(e))
    if LiteralP(e):
        return True
    if VarP(e):
        return True
    if OperationP(e):
        pop.ForAll(OperationOperandL(e),CheckDups)
        return True
    if WhereP(e):
        subj, wk, body = WhereD(e)
        CheckDups(subj)
        pop.ForAll(body,CheckDups)
        l = WhereLocalsL(e)
        dupset = pop.Dups(l)
        if pop.EmptySetP(dupset): return True
        c,d = pop.MembeDr(dupset)
        print("Where local "+pop.WordName(c)+" duplicated")
        exit()
    if DefinitionP(e):
        l = DefinitionFormalsL(e)
        dupset = pop.Dups(l)
        if not pop.EmptySetP(dupset):
            c,d = pop.AddD(dupset)
            print("Formal parameter "+pop.WordName(c)+" duplicated")
            exit()
        lhs,es,rhs = DefinitionD(e)
        CheckDups(rhs)
        return True
    if CallP(e):
        pop.ForAll(CallActualsL(e),CheckDups)
        return True
    assert False, 'weird term for checkdups '+str(e)
    
def CheckLocals(e):
    """ check that locals are variables """ 
    #prp.printf('chl -> ');prp.Term(e);print()
    if LiteralP(e):
        return True
    if VarP(e):
        return True
    if OperationP(e):
        pop.ForAll(OperationOperandL(e),CheckLocals)
        return True
    if CallP(e):
        args = CallActualsL(e)
        pop.ForAll(args,CheckLocals)
        return True
    if WhereP(e):
        subj,wk, body = WhereD(e)
        CheckLocals(subj)
        pop.ForAll(body,CheckLocals)
        ll=WhereLhssL(e)
        while ll != pop.Empty:
            lhs, ll = pop.DeCons(ll)
            if VarP(lhs): continue
            if CallP(lhs) and VarP(CallFun(lhs)): continue
            prp.printf('locals of a where clause must be variables not ')
            prp.Term(lhs)
            print()
            exit()
        return True
    if DefinitionP(e):
        lhs,es,rhs = DefinitionD(e)
        if CallP(lhs):
            ll = CallActualsL(lhs)
            while ll != pop.Empty:
                v, ll = pop.DeCons(ll)
                if VarP(v): continue
                print('Formals of a function definition must be variables not ')
                prp.Term(v)
                print()
                exit()
        CheckLocals(rhs)
        return True
    assert False, 'weird term for checklocals '+pio.Items(e)

def ProgramEmbedded(pg):
    if WhereP(pg):
        subj,wk,body = WhereD(pg)
        NoEmbeddeds(subj)
        pop.ForAll(body,NoEmbeddeds)
        return
    return NoEmbeddeds(pg)
    
def NoEmbeddeds(e):
    #print('--> ');prp.Term(e);print()
    if LiteralP(e):
        return True
    if VarP(e):
        return True
    if CallP(e):
        return True
    if OperationP(e):
        pop.ForAll(OperationOperandL(e),NoEmbeddeds)
        return True
    if WhereP(e):
        print('Embedded where clause:')
        prp.Term(e);print()
        exit()
    if DefinitionP(e):
        lhs,es,rhs = DefinitionD(e)
        if WhereP(rhs):
            subj,wk,body = WhereD(rhs)
            NoEmbeddeds(subj)
            pop.ForAll(body,NoEmbeddeds)
            return True
        else:
            NoEmbeddeds(rhs)
            return True
    assert False, 'weird term for NoEmbeddeds '+str(e)

if __name__ == "__main__":
    pg = prs.ParseFile("testprog.lu")
    print("check locals")
    CheckLocals(pg)
    print("check dups")
    CheckDups(pg)
    print("check embeddings")
    ProgramEmbedded(pg)