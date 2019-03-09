import pop,pio
    
def FindBest(tt,d):
    if tt in d: return d[tt]
    p = FindBest(super[tt],d)
    d[tt] = p
    return p
    
def Supers(s):
    """ register a bunch of supers"""
    ig = pio.ItemGenStringC(s)
    sup = pop.WordName(pio.NextItem(ig))
    while pio.CurrentItem(ig) != '':
        super[pop.WordName(pio.NextItem(ig))] = sup
    
super = {}
    
super['+'] = 'infixop'
super['*'] = 'infixop'
super['**'] = 'infixop'
super['first'] = 'prefixop'
super['next'] = 'prefixop'
super['infixop'] = 'op'
super['prefixop'] = 'op'
super['[%'] = 'multiop'
super['multiop'] = 'op'
super['op'] ='ex'
    
pr = {}
pr['ex'] = 'def'
pr['op'] = 'opdef'
pr['infix'] = 'indef'
pr['first'] = 'bleen'
pr['[%'] = 'listb'


Supers('arith + * / ** -')


