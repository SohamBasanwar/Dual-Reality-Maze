from build_revision06 import *
base=Part.Shape();base.read(str(ROOT/'explorer-pretray.brep'))
tray=extr(rr(38,66,170,59,2).cut(rr(39.7,67.7,166.6,55.6,1)),3.8,5.2)
print('input',base.Volume,base.isValid(),base.isClosed(),base.Orientation,flush=True)
print('inside',[(p,base.isInside(V(*p),.001,True)) for p in [(123,80,2),(123,80,20),(10,50,20),(40,170,15)]],flush=True)
print('COMMON',base.common(tray).Volume,'CUT',base.cut(tray).Volume,'REV',tray.fuse(base).Volume,flush=True)
rev=base.copy();rev.reverse();print('REVERSED fuse',rev.fuse(tray).Volume,flush=True)
for tol in [0,1e-7,1e-5,.001,.01]:
    s=base.fuse(tray,tol)
    print(tol,s.Volume,s.isValid(),len(s.Solids),flush=True)
