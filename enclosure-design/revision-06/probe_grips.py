from build_revision06 import *
f=sculpted_outline();H=58;split=42
levels=[(0,-6),(3,-4.5),(8,-2.5),(15,-1),(24,-.2),(33,-1.2),(split,-3),(H-10,-4.8),(H-5,-7.5),(H,-11)]
b=soft_loft(f,levels).common(ceiling(246,H,False))
g=grip_limit()
for n,s in [('original',b),('limit',g),('limited',b.common(g))]:
 print(n,s.isValid(),len(s.Solids),s.Volume,s.BoundBox,flush=True)
 s.exportBrep(str(ROOT/(n+'.brep')))
c=soft_loft(f,[(4,-7.8),(8,-6),(15,-4.4),(24,-3.6),(33,-4.6),(split,-6.4),(H-10,-8.2),(H-4,-11.5),(H+1,-14)]).common(ceiling(246,H-3.8,False)).common(grip_limit(3.4))
body=union([b.common(g),extr(rr(23.5,122.5,37,68,4),0,6)])
h=body.cut(c)
for n,s in [('cavity',c),('hollow',h),('base',h.common(ceiling(246,42,False))),('lid',h.cut(ceiling(246,42.28,False)))]:
 print(n,s.isValid(),len(s.Solids),s.Volume,s.BoundBox,flush=True)
 s.exportBrep(str(ROOT/(n+'.brep')))
ba=h.common(ceiling(246,42,False));li=h.cut(ceiling(246,42.28,False))
print('SEAM overlap',ba.common(li).Volume,'CUT',ba.cut(li).Volume,flush=True)
