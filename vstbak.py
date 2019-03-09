import pio,prp
vstack = []
vlayers = [0]

def Vtop(N):
    #/* the item on the stack N frames below the top */
    return(vstack[ - (N + 1)])
    
def Vpop(n):
    """ pop n items  """
    assert vlayers[-1]+n < len(vstack)+1, 'overpopping  vstack '
    for i in range(n): vstack.pop()
    
def Vtop0():
    """ the element atop the vvstack """
    assert vlayers[-1] < len(vstack), 'top of empty layer'
    return vstack[-1]
    
def Vpush0(x):
    vstack.append(x)
    
def Vpop0():
    """ the element atop the vstack """
    assert vlayers[-1] < len(vstack), 'popping empty layer'
    return vstack.pop()
    
def Vpush(n,x):
    """ pop n items and push x """
    assert vlayers[-1]+n < len(vstack)+1, 'overpopping  vstack '
    for i in range(n): vstack.pop()
    vstack.append(x)

def Vblayer():
    """begin a new, empty layer"""
    vbottom = len(vstack)
    vlayers.append(vbottom)
    
def Velayer():
    """ end layer but don't pop """
    assert len(vlayers)>1, 'no layers to end'
    vlayers.pop()

def VemptyP():
    return len(vstack) == vlayers[-1]
    
def Vdump(): 
    for i in vstack:
        pio.WriteItem(i)
        prp.printf(' ')
    print()
"""


vstdump(f)
FILE *f;
/* dump the contents of the vstack */
{ int i,L;

	for (i = vstptr - 1; i >= 0; i--) {
		L = 20;
		ibdwrite(f,vstack[i],5,&L);
		fprintf(f," ");
	}
	fprintf(f,"\n");
}



vcycle(n)
int n;
/* cycle the top n elts of the vstack */
/* (positive n brings n'th stack element to top; negative is the reverse) */
{ item temp; int i,m;

	if (n < 0) {
		m = - n;
		if (m > vstptr-vstbottom) {
			whine("stack too small to cycle",mkint(n));
		}
		else {
			temp = vstack[vstptr - 1];
			for (i = vstptr - 1; i > vstptr - m; i--) {
				vstack[i] = vstack[i - 1];
			}
			vstack[vstptr - m] = temp;
		}
	}
	else {
		if (n > vstptr-vstbottom) {
			whine("stack too small to cycle",mkint(n));
		}
		else {
			temp = vstack[vstptr - n];
			for (i = vstptr - n; i < vstptr - 1; i++) {
				vstack[i] = vstack[i+1];
			}
			vstack[vstptr - 1] = temp;
		}
	}
}
"""
def Vempty():
    while not VemptyP():
        vstack.pop()
        


"""
def vbottom(i):
    #/* the item ith from the bottom of the current layer */
    if(i<0 || (i+vstbottom >= vstptr):) whine("vbottom out of range",mkint(i));
    return vstack[vstbottom+i];
"""

def Vdepth():
    #/* the depth of the current layer */
    return len(vstack)-vlayers[-1]

def Vreturn(k): 
    #/* replace all the stack by k */
    Vempty()
    vpush0(k)

