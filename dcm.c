/*	Written by Martin Davis    14/5/85	*/
/* procedures dealing with data on the stack only */


void QUOTExec()
/* actually a no-op - just serves to get arguments put on stack */
{
}

void INTxec()
{
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
	vpush(popint(vtop0()),1);
}

void ADDxec()
{
 item c;
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
		ErrExit(VstDepth()<2,DcmMissingopd2U,erritm);
	c = popsum(vtop(1),vtop(0));
 		ErrSkip(ErrFound());
	vpush(c,2);
}

void SUBxec()
{
 item c;
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
		ErrExit(VstDepth()<2,DcmMissingopd2U,erritm);
	c = popdiff(vtop(1),vtop(0));
 		ErrSkip(ErrFound());
	vpush(c,2);
}

void TIMESxec()
{
 item c;
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
		ErrExit(VstDepth()<2,DcmMissingopd2U,erritm);
	c = popprod(vtop(1),vtop(0));
 		ErrSkip(ErrFound());
	vpush(c,2);
}

void MINUSxec()
{
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
	vpush(mkint(-intval(vtop0())),1);
 		ErrSkip(ErrFound());
}

void DIVxec()
{
 item c;
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
		ErrExit(VstDepth()<2,DcmMissingopd2U,erritm);
	c = popdiv(vtop(1),vtop(0));
 		ErrSkip(ErrFound());
	vpush(c,2);
}

void MODxec()
{
 item c;
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
		ErrExit(VstDepth()<2,DcmMissingopd2U,erritm);
	c = popmod(vtop(1),vtop(0));
 		ErrSkip(ErrFound());
	vpush(c,2);
}

void QUOxec()
{
 item c;
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
		ErrExit(VstDepth()<2,DcmMissingopd2U,erritm);
	c = popquo(vtop(1),vtop(0));
 		ErrSkip(ErrFound());
	vpush(c,2);
}

void POWERxec()
{
 item c;
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
		ErrExit(VstDepth()<2,DcmMissingopd2U,erritm);
	c = poppower(vtop(1),vtop(0));
 		ErrSkip(ErrFound());
	vpush(c,2);
}

void GExec()
{
 item c;
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
		ErrExit(VstDepth()<2,DcmMissingopd2U,erritm);
	c = popge(vtop(1),vtop(0));
 		ErrSkip(ErrFound());
	vpush(mkbool(c),2);
}

void GTxec()
{
 item c;
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
		ErrExit(VstDepth()<2,DcmMissingopd2U,erritm);
	c = popgt(vtop(1),vtop(0));
 		ErrSkip(ErrFound());
	vpush(mkbool(c),2);
}

void LExec()
{
 item c;
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
		ErrExit(VstDepth()<2,DcmMissingopd2U,erritm);
	c = pople(vtop(1),vtop(0));
 		ErrSkip(ErrFound());
	vpush(mkbool(c),2);
}

void LTxec()
{
 item c;
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
		ErrExit(VstDepth()<2,DcmMissingopd2U,erritm);
	c = poplt(vtop(1),vtop(0));
 		ErrSkip(ErrFound());
	vpush(mkbool(c),2);
}

void EQxec()
{
 item c;
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
		ErrExit(VstDepth()<2,DcmMissingopd2U,erritm);
	c = eq(vtop(1),vtop(0));
 		ErrSkip(ErrFound());
	vpush(mkbool(c),2);
}

void NExec()
{
 item c;
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
		ErrExit(VstDepth()<2,DcmMissingopd2U,erritm);
	c = eq(vtop(1),vtop(0));
 		ErrSkip(ErrFound());
	vpush(mkbool(!c),2);
}

void SINxec()
{
 item c;
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
	c = popsin(vtop0());
 		ErrSkip(ErrFound());
	vpush(c,1);
}

void COSxec()
{
 item c;
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
	c = popcos(vtop0());
 		ErrSkip(ErrFound());
	vpush(c,1);
}

void TANxec()
{
 item c;
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
	c = poptan(vtop0());
 		ErrSkip(ErrFound());
	vpush(c,1);
}

void SQRTxec()
{
 item c;
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
	c = popsqrt(vtop0());
 		ErrSkip(ErrFound());
	vpush(c,1);
}

void LOGxec()
{
 item c;
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
	c = poplog(vtop0());
 		ErrSkip(ErrFound());
	vpush(c,1);
}

void EXPxec()
{
 item c;
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
	c = popexp(vtop0());
 		ErrSkip(ErrFound());
	vpush(c,1);
}

void ABSxec()
{
 item c;
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
	c = popabs(vtop0());
 		ErrSkip(ErrFound());
	vpush(c,1);
}

void NOTxec()
{
 item c;
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
	c = popnot(vtop0());
 		ErrSkip(ErrFound());
	vpush(c,1);
}

void ORxec()
{
 item c;
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
		ErrExit(VstDepth()<2,DcmMissingopd2U,erritm);
	c = popor(vtop(1),vtop(0));
 		ErrSkip(ErrFound());
	vpush(c,2);
}

void ANDxec()
{
 item c;
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
		ErrExit(VstDepth()<2,DcmMissingopd2U,erritm);
	c = popand(vtop(1),vtop(0));
 		ErrSkip(ErrFound());
	vpush(c,2);
}

void DUPxec()
{
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
	vpush0(vtop0());
}

void HEADxec()
{
 item c;
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
	c = pophd(vtop0());
 		ErrSkip(ErrFound());
	vpush(c,1);
}

void TAILxec()
{
 item c;
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
	c = poptl(vtop0());
 		ErrSkip(ErrFound());
	vpush(c,1);
}

void CONSxec()
{
 item c;
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
		ErrExit(VstDepth()<2,DcmMissingopd2U,erritm);
	c = popcons(vtop(1),vtop(0));
 		ErrSkip(ErrFound());
	vpush(c,2);
}

void REVERSExec()
{
 item c;
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
	c = popreverse(vtop0());
 		ErrSkip(ErrFound());
	vpush(c,1);
}

void APPENDxec()
{
 item c;
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
		ErrExit(VstDepth()<2,DcmMissingopd2U,erritm);
	c = popappend(vtop(1),vtop(0));
 		ErrSkip(ErrFound());
	vpush(c,2);
}

void listxec()
/* gather the items on the stack into a list */
/* not gc safe */
{item p;
 p = nilitm;
 while( !vstempty() )  p = popcons(vtpp0(),p);
 vpush0(p);
}

copypoplist()
/* make a fresh copy of the nonempty list on top of the stack, */
/* leaving pointers to the head and tail on the stack, */
/* tl pointer on top */
{
item x,y;

	if (! islist(vtop0())) {
		whine("copypoplist given nonlist",vtop0());
	}
	if (isnil(vtop0())) {
		whine("copypoplist given empty list",vtop0());
	}
	x = vtop0();
	y = popcons(pophd(x),nilitm);
	vpush0(y); vpush0(y); x = poptl(x);
	while (! isnil(x)) { 
	 y = popcons(pophd(x),nilitm);
	 changetl(vtop0(),y);
	 vpush(y,1);
	 x = poptl(x);
	}
	vpop(2); /* remove the old copy which has stayed on the stack */
}
	
void STRINGCATxec()
{
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
		ErrExit(VstDepth()<2,DcmMissingopd2U,erritm);
	if (isnilstr(vtop(1))) {
		vpop(1);
	}
	else {
	 vcycle(2);
	 copystring();
	 changepopstringtl(vtop0(),vtop(2));
	 vpop0();
	 vpop(1);
	}
}

void STRINGTLxec()
{
 vpush0(popstringtl(vtpp0()));
}

copystring()
/* make a fresh copy of the nonempty string on top of the stack, */
/* leaving pointers to the head and tail on the stack, */
/* tl pointer on top */
{
item x,y;

	if (! isstring(vtop0())) {
		whine("copystring given nonstring",vtop0());
	}
	if (isnilstr(vtop0()))
		whine("copystring given empty string",vtop0());
	x = vtop0();
	y = popstringcons(popstringhd(x),nilstring);
	vpush0(y);vpush0(y);x = popstringtl(x);
	while (! isnilstr(x)) { 
	 y = popstringcons(popstringhd(x),nilstring);
	 changepopstringtl(vtop0(),y);
	 vpush(y,1);
	 x = popstringtl(x);
	}
	vpop(2); /* remove the old copy which has stayed on the stack */
}
	
void COLLECTxec()
{
	garbcoll();
}

void lengthxec()
{
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
	vpush(mkint(poplength(vtop0())),1);
}

void substrxec()
{
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
	vpush(popsubstr(vtop(2),intval(vtop(1)),intval(vtop0())),3);
}

void mkwordxec()
{
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
	vpush(mknewwd(stringchars(vtop0())),1);
}

void mkstringxec()
{
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
	vpush(mkstr(name(vtop0())),1);
}

void islistxec()
{
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
	vpush(mkbool(islist(vtop0())),1);
}

void isatomxec()
{
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
	vpush(mkbool(isatom(vtop0())),1);
}

void isstringxec()
{
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
	vpush(mkbool(isstring(vtop0())),1);
}

void iswordxec()
{
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
	vpush(mkbool(isword(vtop0())),1);
}

void isnumxec()
{
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
	vpush(mkbool(isnum(vtop0())),1);
}

void isintxec()
{
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
	vpush(mkbool(isint(vtop0())),1);
}

void isnilxec()
{
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
	vpush(mkbool(isnil(vtop0())),1);
}

void iserrxec()
{
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
	vpush(mkbool(iserror(vtop0())),1);
}

void mknumberxec()
/* turn the popstring on top of the stack, which should be a numeral, 
into the corresponding pop integer */
{item s,n;
		ErrExit(VstDepth()<1,DcmMissingopd1U,erritm);
 s = vtop0(); 
 n = atoi(stringchars(s));
 vpop0();
 vpush0(mkint(n));
}
