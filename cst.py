import pio,prp
cstack = []
cstackptr = 0
cstacksize = 0

def Ctop(N):
    global cstack,cstackptr,cstacksize
    #/* the item on the stack N frames below the top */
    return(cstack[cstackptr - (N + 1)])
    
def Cpop(n):
    """ pop n items  """
    global cstack,cstackptr,cstacksize
    assert cstackptr >= n, 'overpopping cstack '+str(n)
    cstackptr -= n
    
def Ctop0():
    global cstack,cstackptr,cstacksize
    """ the element atop the vcstack """
    assert cstackptr>0,'top of empty stack'
    return cstack[cstackptr-1]
    
def Cpush0(x):
    global cstack,cstackptr,cstacksize
    if cstackptr < cstacksize:
        cstack[cstackptr] = x
        cstackptr += 1
    else:
        cstack.append(x)
        cstackptr += 1
        cstacksize += 1
    
def C1push0(x):
    global cstack,cstackptr,cstacksize
    if cstackptr < cstacksize:
        cstack[cstackptr] = x
        cstackptr += 1
    else:
        cstack.append(x)
        cstackptr += 1
        cstacksize += 1
    
def Cpop0():
    """ the element atop the cstack """
    global cstack,cstackptr,cstacksize
    assert cstackptr > 0, 'popping empty cstack'
    
    cstackptr -= 1
    return cstack[cstackptr]
  
def Cpusha(v,n):
    global cstack,cstackptr,cstacksize
    """ push elements of v in reverse order """
    #print("Cpushing ",v,n)
    for i in range(n):
        x = v[-(i+1)]
        if cstackptr < cstacksize:
            cstack[cstackptr] = x
            cstackptr += 1
        else:
            cstack.append(x)
            cstackptr += 1
            cstacksize += 1
        #Cpush0(v[-(i+1)])
    
def Cpush(n,x):
    """ pop n items and push x """
    global cstack,cstackptr,cstacksize
    assert cstackptr >=n , 'overpopping  cstack '+str(n)
    cstackptr -= n
    Cpush0(x)

def CemptyP():
    global cstack,cstackptr,cstacksize
    return cstackptr==0
    
def Cempty():
    global cstack,cstackptr,cstacksize
    cstackptr=0
        
def Cdump():
    print('vvvvvvvvvvvvvvvvvvvvv')
    n = min(cstackptr,8)
    for i in range(n):
        print(cstack[cstackptr-(i+1)])
    print('^^^^^^^^^^^^^^^^^^^^^')

def Cdepth():
    #/* the depth of the current layer */
    return cstackptr

def Creturn(k): 
    #/* replace all the stack by k */
    Cempty()
    Cpush0(k)

