import pio,prp
vstack = []
vstackptr = 0
vstacksize = 0

def Vtop(N):
    global vstack,vstackptr,vstacksize
    #/* the item on the stack N frames below the top */
    return(vstack[vstackptr - (N + 1)])
    
def Vpop(n):
    """ pop n items  """
    global vstack,vstackptr,vstacksize
    assert vstackptr >= n, 'overpopping vstack '+str(n)
    vstackptr -= n
    
def Vtop0():
    global vstack,vstackptr,vstacksize
    """ the element atop the vvstack """
    assert vstackptr>0,'top of empty stack'
    return vstack[vstackptr-1]
    
def Vpush0(x):
    global vstack,vstackptr,vstacksize
    if vstackptr < vstacksize:
        vstack[vstackptr] = x
        vstackptr += 1
    else:
        vstack.append(x)
        vstackptr += 1
        vstacksize += 1
    
def V1push0(x):
    global vstack,vstackptr,vstacksize
    if vstackptr < vstacksize:
        vstack[vstackptr] = x
        vstackptr += 1
    else:
        vstack.append(x)
        vstackptr += 1
        vstacksize += 1
    
def V2push0(x):
    global vstack,vstackptr,vstacksize
    if vstackptr < vstacksize:
        vstack[vstackptr] = x
        vstackptr += 1
    else:
        vstack.append(x)
        vstackptr += 1
        vstacksize += 1
    
def V3push0(x):
    global vstack,vstackptr,vstacksize
    if vstackptr < vstacksize:
        vstack[vstackptr] = x
        vstackptr += 1
    else:
        vstack.append(x)
        vstackptr += 1
        vstacksize += 1
    
def Vpop0():
    """ the element atop the vstack """
    global vstack,vstackptr,vstacksize
    assert vstackptr > 0, 'popping empty vstack'
    vstackptr -= 1
    return vstack[vstackptr]
    
def Vpush(n,x):
    """ pop n items and push x """
    global vstack,vstackptr,vstacksize
    assert vstackptr >=n , 'overpopping  vstack '+str(n)
    vstackptr -= n
    Vpush0(x)

def VemptyP():
    global vstack,vstackptr,vstacksize
    return vstackptr==0
    
def Vdump(): 
    global vstack,vstackptr,vstacksize
    for i in range(vstackptr):
        pio.WriteItem(vstack[i])
        prp.printf(' ')
    print()

def Vempty():
    global vstack,vstackptr,vstacksize
    vstackptr=0
        

def Vdepth():
    #/* the depth of the current layer */
    return vstackptr

def Vreturn(k): 
    #/* replace all the stack by k */
    Vempty()
    Vpush0(k)

