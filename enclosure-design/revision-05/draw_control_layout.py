"""Engineering diagram from the CAD's control coordinates; not a concept render."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
R=Path(__file__).resolve().parent
outlines=json.loads((R/'layout-outlines.json').read_text())
im=Image.new('RGB',(1800,1050),'#101820');d=ImageDraw.Draw(im)
def font(n,bold=False):return ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf' if bold else 'C:/Windows/Fonts/arial.ttf',n)
cream='#f1e7d3';gold='#dab47b';ink='#15212b';blue='#87c7ed'
d.text((50,32),'Controls, openings and internal mounting zones',font=font(38,True),fill=cream)
d.text((50,88),'Nominal CAD layout — actual part dimensions and travel still need physical verification',font=font(23),fill='#b7c5cf')
legends={
'explorer':['1  Joystick: opening and underside PCB carrier','2  Photoresistor: exposed sensor opening','3  RGB LED: behind eye emblem and diffuser'],
'architect':['1  Potentiometer: shaft hole and body cradle','2  Pushbutton: guided cap and switch cassette','3  SG90 servo: upper-shoulder gate mechanism','4  RGB LED: behind gate emblem and diffuser'],
'main':['1  16×2 LCD: window, PCB and I2C backpack space','2  Buzzer: sound openings and body cradle','3  RGB LED: behind portal emblem and diffuser','4  Power actuator: guided cap; circuit provisional','5  Rear USB access: captive sliding shutter']}
for i,role in enumerate(['explorer','architect','main']):
    ox=50+i*580;oy=190;s=1.95
    d.text((ox,138),role.upper(),font=font(27,True),fill=gold)
    xy=lambda x,y:(ox+x*s,oy+y*s)
    d.polygon([xy(*p) for p in outlines[role]],fill='#31404a',outline=gold,width=3)
    def circle(x,y,r,fill=ink,width=3):
        a=xy(x-r,y-r);b=xy(x+r,y+r);d.ellipse([a,b],fill=fill,outline=gold,width=width)
    def rect(x,y,w,h,fill=ink):d.rounded_rectangle([xy(x,y),xy(x+w,y+h)],radius=5,fill=fill,outline=gold,width=3)
    def num(x,y,n):
        px,py=xy(x,y);d.ellipse((px-16,py-16,px+16,py+16),fill=gold);d.text((px,py),str(n),font=font(20,True),fill=ink,anchor='mm')
    if role=='explorer':
        circle(49,42,14.2);circle(197,42,3.2,blue);circle(123,67,26,'#1c5576')
        num(49,18,1);num(218,42,2);num(123,67,3)
    elif role=='architect':
        circle(49,42,11);circle(49,42,4);circle(197,95,8.4);rect(173,17,46,30);circle(123,67,26,'#1c5576')
        num(49,18,1);num(219,95,2);num(196,32,3);num(123,67,4)
    else:
        rect(80.7,29,72,26,'#276643');circle(117,108,26,'#1c5576');circle(117,145,8.4)
        for x in [33,181]:
            for y in [103,109,115,121]:rect(x,y,20,2.5)
        rect(102,-3,30,6);num(117,41,1);num(213,112,2);num(117,108,3);num(117,166,4);num(117,8,5)
    yy=640
    for line in legends[role]:
        d.text((ox,yy),line,font=font(21),fill=cream);yy+=42
    d.text((ox,900),'Inside: full-size breadboard + UNO cradle',font=font(20),fill=blue)
    d.text((ox,930),'Battery bay + optional ESP32/jumper space',font=font(20),fill=blue)
d.text((50,999),'All three RGB assemblies include a concealed LED seat, screwless quarter-turn keeper, lead passage and diffuser.',font=font(22),fill=gold)
im.save(R/'previews'/'control-layout.png')
print('Labelled control-layout diagram saved.')
