
cstack = []
clayers = [0]

def Ctop(N):
    #/* the item on the stack N frames below the top */
    return(cstack[ - (N + 1)])
    
def Ctop0():
    """ the element atop the cstack """
    assert clayers[-1] < len(cstack), 'top of empty layer'
    return cstack[-1]
    
def Cpush0(x):
    cstack.append(x)
    
def Cpop0():
    """ the element atop the cstack """
    assert clayers[-1] < len(cstack), 'popping empty layer'
    return cstack.pop()
    
def Cpush(n,x):
    """ pop n items and push x """
    assert clayers[-1]+n < len(cstack)+1, 'overpopping  cstack '
    for i in range(n): cstack.pop()
    cstack.append(x)

def Cblayer():
    """begin a new, empty layer"""
    cbottom = len(cstack)
    clayers.append(cbottom)
    
def Celayer():
    """ end layer but don't pop """
    assert len(clayers)>1, 'no layers to end'
    clayers.pop()

def CemptyP():
    return len(cstack) == clayers[-1]

def Cempty():
    while not CemptyP():
        cstack.pop()
        


def Cdepth():
    #/* the depth of the current layer */
    return len(cstack)-clayers[-1]

def Creturn(k): 
    #/* replace all the stack by k */
    Cempty()
    Cpush0(k)

