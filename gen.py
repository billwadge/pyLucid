#character and item generators

def CharStringC(s):
    """Create a new char generator from string s"""
    return ['s',0,s]  #kind marker 's', pointer initially 0, string s
    
def CharFilenameC(s):
    """Create a new char generator from file named s"""
    f = open(s,"r")
    t = f.read() #read the whole darn file into t
    f.close()
    return CharStringC(t)
       
def CurrentChar(g): 
    """ return the current char and advance """
    [m,p,s]=g #unbundle g
    assert m=='s' #must currently be a string generator
    if p >= len(s): 
        return '' #no more chars in string
    ch = s[p]
    return ch
    
def NextChar(g):
    """return current char but advance generator"""
    [m,p,s]=g #unbundle g
    ch = CurrentChar(g)
    g[1]=p+1
    return ch

def LookChar(g): #one char lookahead
    [m,p,s]=g #unbundle
    if p>=len(s)-1: return '' #looking at last char
    return s[p+1]
    
def ResetChar(g,s):
    """reset the char generator g with string s"""
    g[0]='s' #make it a string based generator
    g[1]=0
    g[2]=s


     
    