from pathlib import Path
import sys
R=Path(__file__).resolve().parent
source=R/'build_revision08.py'
s=source.read_text(encoding='utf-8-sig').split('    # Internal stop')[0]
def trace(frame,event,arg):
    if event=='line' and frame.f_code.co_name=='build' and 230<=frame.f_lineno<=265:
        b=frame.f_locals.get('body')
        if b:print('BODY TRACE',frame.f_lineno,b.isValid(),b.Volume,flush=True)
    if event=='line' and frame.f_code.co_name=='build' and frame.f_lineno in [264,265,272,273,274,275,278,279,280,281]:
        q=frame.f_locals.get('door');b=frame.f_locals.get('body')
        print(frame.f_lineno,'door',q.Volume if q else None,'body',b.Volume if b else None,flush=True)
        if frame.f_lineno==272:
            m=frame.f_globals
            b.exportBrep(str(R/'probe-original.brep'))
            sh=m['moved'](b,z=2.4);diff=b.cut(sh)
            print('CUT',diff.Volume,[(z,b.isInside(m['V'](40,170,z),.001,True),sh.isInside(m['V'](40,170,z),.001,True),diff.isInside(m['V'](40,170,z),.001,True)) for z in [1,3,7,17]],flush=True)
            diff.exportBrep(str(R/'probe-skin.brep'))
    return trace
g={'__file__':str(source),'__name__':'probe'}
exec(compile(s,str(source),'exec'),g)
sys.settrace(trace)
g['build']('explorer')
