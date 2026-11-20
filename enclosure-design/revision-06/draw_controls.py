"""Source-position placement schematic. Not a photorealistic rendering or a dimensioned drawing."""
from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parent
outlines=json.loads((R.parent/'revision-05'/'layout-outlines.json').read_text())
im=Image.new('RGB',(1800,1160),'#101820');d=ImageDraw.Draw(im)
def font(n,b=False):return ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf' if b else 'C:/Windows/Fonts/arial.ttf',n)
gold='#d8b986';white='#edf3f7';blue='#8fd4ec'
d.text((55,30),'Every controller feature has a place',font=font(42,True),fill=white)
d.text((55,90),'Placement schematic — use the actual CAD for exact shape and dimensions',font=font(25),fill='#b7c6d1')
for i,role in enumerate(['explorer','architect']):
    ox=110+i*880;oy=220;scale=2.55
    pt=lambda x,y:(ox+x*scale,oy+y*scale)
    d.text((ox,148),role.upper(),font=font(31,True),fill=gold)
    d.polygon([pt(*p) for p in outlines[role]],fill='#354853',outline='#7893a4',width=3)
    def circle(x,y,r,c):d.ellipse([pt(x-r,y-r),pt(x+r,y+r)],fill=c,outline=gold,width=3)
    def rect(x,y,w,h,c):d.rounded_rectangle([pt(x,y),pt(x+w,y+h)],radius=8,fill=c,outline=gold,width=3)
    def num(x,y,n):
        x,y=pt(x,y);d.ellipse((x-18,y-18,x+18,y+18),fill=gold);d.text((x,y),str(n),font=font(22,True),fill='#101820',anchor='mm')
    circle(123,67,26,'#216078');rect(113,-3,20,5,'#18232c')
    if role=='explorer':
        circle(49,42,14.2,'#101a22');circle(49,42,11,'#53616c');num(49,42,1)
        circle(123,117,12,'#607986');circle(123,117,10,'#8aa0aa');num(123,117,2);num(123,67,3);num(123,-13,4)
        lines=['1  Protruding joystick and underside PCB carrier','2  REVEAL: raised half-dome at the centre of the face','    Photoresistor above an opaque floor; two lead holes','    Removable roof: thin-print tests / clear-film option','3  RGB eye emblem, with a separate light cup','4  Rear sliding shutter for the I2C cable bundle']
        d.text((ox,782),'Deliberate reach: away from the joystick, grips and rear cable.',font=font(22,True),fill=blue)
    else:
        circle(49,42,11,'#a98a56');num(49,42,1);circle(197,95,8.4,'#26353e');num(197,95,2)
        rect(173,17,46,38,'#775d39')
        for x in [180,187,194,201,208]:d.line([pt(x,22),pt(x,50)],fill=gold,width=4)
        num(196,32,3);num(123,67,4);num(123,-13,5)
        lines=['1  Protruding potentiometer knob','2  Pushbutton cap and retained switch cassette','3  Servo-driven gate, frame and removable guard','    Supplied horn + captive crank pin lift the gate','4  RGB gate emblem, with a separate light cup','5  Rear sliding shutter for the I2C cable bundle']
        d.text((ox,782),'Gate detail view removes the guard so the drive is visible.',font=font(22,True),fill=blue)
    for j,line in enumerate(lines):d.text((ox,838+j*40),line,font=font(23),fill=white)
d.text((55,1110),'Provisional fit: mounting-hole locations, optical response and servo limits require the actual components.',font=font(24),fill=gold)
im.save(R/'previews'/'controller-features.png')
print('Labelled controller schematic saved')
