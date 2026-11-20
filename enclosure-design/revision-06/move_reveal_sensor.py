from pathlib import Path
p=Path(__file__).with_name('build_revision06.py')
s=p.read_text();a=s.index('            lid=cut(lid,[cyl(197,42');b=s.index('        else:\n            lid=lid.cut(cyl(cx,cy',a)
t=s[a:b]
t=t.replace('197,42','sx,sy').replace('197+dx,40.9','sx+dx,sy-1.1').replace('196.2,37.6','sx-.8,sy-4.4').replace('196.2,44.9','sx-.8,sy+2.9')
t=t.replace('            lid=union([lid,sensor])','            sensor=union([sensor,ring(sx,sy,H-.2,5.2,2.4,1.2)])\n            lid=union([lid,sensor])')
s=s[:a]+'            sx,sy=123,117  # deliberate centre-face reach, away from grips/cable/joystick\n'+t+s[b:]
p.write_text(s)
print('Reveal sensor moved to centre face, (123,117), with raised rim')
