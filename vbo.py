"""
sumfor I in R:P(I) all E(I) endfor

doesn't work - time insensitive

use space dimension



sumfor I in R all E(I,X,Y,...) end
last S
whereloop
 I = elements current R;
 S = 0 fby S+ E(I,current X, current Y, ...);
end

sumfor I in R : P(I,x,y,...) all E(I,x,y,...) end
last S whereloop
 J = elements current R;
 I = J whenever P(J,current x, current y, ...);
 S = 0 fby S+ E(I,current X, current Y, ...);
end
 
sumfor I in R: P(I) all E(I) end
prodfor 
avgfor
maxfor
minfor
takefor
unionfor
intersectfor
mapfor
concatfor
consfor
appendfor
exist I in R: P(I) end
forall I in R : P(I) end
firstof I in R: P end         ?R asa P  .. no not nec constant     
lastof I in R: P end
"""
