
def SetRprecedence(s,n):
# symbol s binds with force n from the right 
Rprecedence[s] = n

def SetLprecedence(s,n):
# symbol s binds with force n from the right 
Lprecedence[s] = n

def Rprecedence(s):
return Rprecedence[s]

def Lprecedence(s):
return Lprecedence[s]


void NewInfix(s)
item s;
/* registers the fact that s is an infix operator */
{infixes = WsetAdd(s,infixes); 
}

void NewPostfix(s)
item s;
/* registers the fact that s is a postfix operator */
{postfixes = WsetAdd(s,postfixes);
}

void NewPrefix(s)
item s;
/* registers the fact that s is a prefix operator */
{prefixes = WsetAdd(s,prefixes);
}

void NewNullfix(s)
item s;
/* registers the fact that s is a prefix operator */
{nullfixes = WsetAdd(s,nullfixes);
}

InfixP(s)
item s;
/* is s a infix operator? */
{return WsetMember(s,infixes);
}

PostfixP(s)
item s;
/* is s a postfix operator? */
{return WsetMember(s,postfixes);
}

PrefixP(s)
item s;
/* is s a prefix operator? */
{return WsetMember(s,prefixes);
}

NullfixP(s)
item s;
/* is s a prefix operator? */
{return WsetMember(s,nullfixes);
}

FixP(s)
item s;
/* is s a fix operator? */
{return InfixP(s) || PrefixP(s) || PostfixP(s) || NullfixP(s);
}

def NewFixes(k):
    """register operator precedences"""
    while not EmptyP(k):
        r = pop.Head(k); k = pop.Tail(k);
        rp = pop.NumVal(pop.el1(r)); s = pop.el2(r); lp = pop.NumVal(pop.el3(r))
        if(rp==100 && lp == 100): NewNullfix(s); return
        if(rp==100): NewPrefix(s); SetLprecedence(s,lp); return
        if(lp==100): NewPostfix(s); SetRprecedence(s,rp); return
 

