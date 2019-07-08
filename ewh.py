""" empty the where clauses in a program not connected to a function definition """

import pio,pop,prs,prp

from exp import *

def Eprogram(pg):
    """ return pg with only where clauses for function defs left """
    """ assume function defs at top level only """
    subj, wk, body = WhereD(pg)
    b = body
    ebody = pop.Empty 
    while not pop.EmptyP(b):       #run through dfs in body
        df, b = pop.ConsD(b)       #get current def and advance
        lhs,es, rhs = DefinitionD(df) #dismantle current def
        if not WhereP(rhs):    # no where's
            ebody = pop.AddElement(ebody,df) #add current def unchanged
            #print('ebody is',pio.Items(ebody));exit()
            continue
        rsubj, rwk, rbody = WhereD(rhs)     #dismantle rhs
        if VarDefinitionP(df): #a var defined by a where
            rhs1 = Eprogram(rhs)              #flatten rhs
            r1subj,rwk1, r1body = WhereD(rhs1)    #dismantle new flat whereclause
            ebody = pop.Append(ebody,r1body)  #add the emptied defs to the program body
            df1 = DefinitionC(lhs,es,r1subj)    #change df so var is equated to subject
            ebody = pop.AddElement(ebody,df1) #add simplified def
            continue
        #a function where definition
        rhsf = Eprogram(rhs)                  #flatten the rhs where clause
        df1 = DefinitionC(lhs,es,rhsf)     #construct new definition with flattened rhs
        ebody = pop.AddElement(ebody,df1)
    return WhereC(subj,wk,ebody)
            
            
        