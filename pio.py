import pop,gen
from gen import *
lcletters = 'abcdefghijklmnopqrstuvwxyz'
ucletters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
letters = lcletters+ucletters
digits = '0123456789'
signchars = '+-*/=<>#:$|&^'
whitechars = ' \n\t'
punctuations = '"(),.;'
numformat=''
parsing = True

def skipwhites(g):
    """skip white chars in char generator g"""
    global parsing
    while CurrentChar(g)!='': #not end of input
        char = CurrentChar(g)
        if char == '/' and LookChar(g) == '/' and parsing: #skip a comment
            skipcomment(g)
        if CurrentChar(g) not in whitechars:break #found something
        NextChar(g) #skip a white char
        
def skipcomment(g):
    NextChar(g); NextChar(g)
    while CurrentChar(g) != "\n" and CurrentChar(g) != '': #skip to end of line
        NextChar(g)

def ItemRead(g): 
    """read the next item from character generator g returning it and leaving g starting at the first unused char"""
    skipwhites(g)
    ch = CurrentChar(g)
    if ch == '': #end of input
        return '' #eod
    
    if ch=='[' and LookChar(g) == '%': #list builder open word
        NextChar(g);NextChar(g)
        return pop.WordC('[%')
    if ch=='%' and LookChar(g) == ']':
        NextChar(g);NextChar(g)
        return pop.WordC('%]')
    if ch=='{' and LookChar(g) == '%': #set builder open word
        NextChar(g);NextChar(g)
        return pop.WordC('{%')
    if ch=='%' and LookChar(g) == '}':
        NextChar(g);NextChar(g)
        return pop.WordC('%}')
        
    if ch in '~'+digits: return NumRead(g)           #should be a number
    if ch in letters: return IdentRead(g)            #should be an identifier word
    if ch in signchars: return SignRead(g)           #should be a sign word
    if ch in punctuations: return PunctuationRead(g) #should be a punctuation word
    if ch == "'": return StringRead(g)               #a string
    if ch == '[': return ListRead(g)  
    if ch == '{': return  SetRead(g)             #a set
    assert False, 'unexpected character:'+ch

def IdentRead(g):
    ident = ''
    while CurrentChar(g) != '':
        if CurrentChar(g) not in letters+digits+'_':
            break
        ident = ident + NextChar(g)
    return pop.WordC(ident)
    
def SignRead(g):
    sign = '' 
    while CurrentChar(g) != '':
        if CurrentChar(g) not in signchars:
            break
        sign = sign + NextChar(g)
    return pop.WordC(sign)
    
def PunctuationRead(g):
    return pop.WordC(NextChar(g))
    
def StringRead(g):
    NextChar(g)             #skip quote
    s=''
    while CurrentChar(g) != '':
        ch = CurrentChar(g)
        ch1 = LookChar(g)
        if ch == "'": break
        if ch == '\\' and ch1 != '' and  ch1 in "\\'nt\"":
            NextChar(g)
            s=s+'\\'
        s = s+NextChar(g)
    assert CurrentChar(g) == "'", 'no string closing quote'
    NextChar(g)
    return pop.StringC(s)
    
def ListRead(g):
    NextChar(g)
    l = ListBodyRead(g)
    return l
    
def ListBodyRead(g):
    skipwhites(g)
    assert CurrentChar(g) != '', 'incomplete list'
    if CurrentChar(g) == ']': 
        NextChar(g)
        return pop.Empty
    i = ItemRead(g)
    m = ListBodyRead(g)
    return pop.Cons(i,m)
    
def SetRead(g):
    NextChar(g)
    l = SetBodyRead(g)
    return l
    
def SetBodyRead(g):
    skipwhites(g)
    assert CurrentChar(g) != '', 'incomplete set'
    if CurrentChar(g) == '}': 
        NextChar(g)
        return pop.EmptySet
    i = ItemRead(g)
    m = SetBodyRead(g)
    return pop.Add(i,m)
    
def NumRead(g):
    sign = 1
    Float = False
    if CurrentChar(g) == '~':
        sign = -1
        NextChar(g)
    ch = CurrentChar(g)
    num = ''
    assert ch != '' and ch in digits,  'expecting digit, found '+ch
    while CurrentChar(g) != '':
        if CurrentChar(g) == '.':
            assert not Float, 'two decimal points'
            Float=True
            num = num+'.'
            NextChar(g)
            ch = CurrentChar(g)
            assert ch !='', 'float terminates after decimal point'
            assert ch in digits, 'unexpected char after decimal point:'+ch
        if CurrentChar(g) not in digits: break
        num = num+NextChar(g)
    if Float: return pop.NumC(float(sign)*float(num)) 
    return pop.NumC(sign*int(num))
    
def IdentP(w):
    if not pop.WordP(w): return False
    m,s = w
    return s[0] in letters
        
def Nums(n):        #pop number n as a string
    global numformat
    assert pop.NumP(n), 'nums given non number'
    sign =  ''
    n = pop.NumVal(n)
    if numformat != '':  return numformat % n
    if n < 0:
        sign = '~'
        n = -n
    return sign+str(n)
 
def Lists(l):      #pop list l as a python string
    assert pop.ListP(l), 'lists given a non list'
    m = l
    b = '['
    while not pop.EmptyP(m):
         b = b+ Items(pop.Head(m))
         m = pop.Tail(m)
         if  not pop.EmptyP(m): b=b+' '
    return b+']'

def Words(w):
    k,s = w
    assert k=='w', 'Words given a nonword'
    return s
    
def Strings(ps):
    k,s = ps
    assert k=='s', 'Strings given a non string '+str(ps)
    return "'"+s+"'"
    
def Sets(s):
    """ a string of s as a set literal  """
    lit = '{'
    while not pop.EmptySetP(s):
        e,s = pop.DeMember(s)
        lit = lit+Items(e)
        if not pop.EmptySetP(s):
            lit = lit+' '
    return lit+'}'
    
def WriteItemln(i):
    print(Items(i))
    
def WriteItem(i):
    print(Items(i),end='')
    
def Items(i):      #pop item i as a python string
    if i=='': return '' #eod
    if pop.ListP(i):   return Lists(i)
    if pop.NumP(i):    return Nums(i)
    if pop.WordP(i):   return Words(i)
    if pop.StringP(i): return Strings(i)
    if pop.SetP(i):    return Sets(i)
    assert False, 'Items given non item '+str(i)
    
def ItemGenListC(pl):
    """Create an item generator from poplist pl"""
    return ["l",'',pl] #list marker, current item, list from now on
    
def ItemGenChargenC(g):
    """create an item generator from char generator g"""
    return ['c','',g]

def ItemGenStringC(s):
    """create an item generator form python string s """
    g = CharStringC(s) #a char generator based on s
    return ItemGenChargenC(g)
    
def CurrentItem(ig):
    """The current item of item generator ig - does not advance"""
    [m,ci,r] = ig
    if m == 'l':
        if ci == '':
           if pop.EmptyP(r): return '' #end of data
           ig[1] = pop.Head(r)
           return ig[1]
        return ci
    if m == 'c':
        if ci == '':
            skipwhites(r)
            d = ItemRead(r)
            if d == '' : return ''
            ig[1] = d
            return d
        return ci
    assert False, 'unknown item generator type '+m
    
def NextItem(ig):
    """return current item, advancing"""
    d  = CurrentItem(ig)
    if d=='': return ''
    [m,ci,r]  = ig
    if m == "l":
        if EmptyP(r):
            ig[1] = ''
        else:
            ig[2] = pop.Tail(r)
            if EmptyP(ig[2]):
                ig[1] =  ''
            else:
                ig[1] = pop.Head(ig[2])
        return d
    if m == "c":
        ig[1] = ItemRead(r)
        ig[2]=r
        return d
    assert False, 'unlnown generator type '+m
    
def Popliteral(s):
    """item in python string s """
    cg = gen.CharStringC(s) 
    return ItemRead(cg)
    
def ItemReadFile(fname):
    f = open(fname,"r")
    i = f.read()
    f.close()
    ig = ItemGenStringC(i)
    return NextItem(ig)
    
def printf(s):
    print(s, end='')
    
def Dump5(ig):
    """write up to next 5 items from ig"""
    n = 5
    while n>0:
        ci = CurrentItem(ig)
        if ci == '': printf("EOD");break
        WriteItem(ci); printf(' ')
        NextItem(ig)
        n = n-1

def wi(i):
    WriteItem(i)
    
def win(i):
    WriteItemln(i)
      
        
          