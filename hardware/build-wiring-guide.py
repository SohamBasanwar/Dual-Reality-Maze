"""Build labeled circuit sheets, a browser checklist, PNGs and a printable PDF."""
from pathlib import Path
import html, json, textwrap, csv
import fitz

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'hardware/wiring-guide'
PDF = ROOT / 'output/pdf/Dual-Reality-Maze-Wiring-Guide.pdf'
OUT.mkdir(parents=True, exist_ok=True)
PDF.parent.mkdir(parents=True, exist_ok=True)
W,H=1800,1270
C={'power':'#b92d35','ground':'#374151','analog':'#b36b00','digital':'#8541b0','sda':'#008470','scl':'#2167b3'}
INK='#142c42'; MUTED='#536778'; BORDER='#d8e2e9'
R3='https://content.arduino.cc/assets/A000066-full-pinout.pdf'
R4='https://docs.arduino.cc/resources/pinouts/ABX00087-full-pinout.pdf'
SPEC='https://github.com/arduino/docs-content/blob/main/content/hardware/uno/boards/uno-r4-wifi/tech-specs.md'

class Sheet:
 def __init__(self,n,title,subtitle):
  self.n=n;self.title=title;self.subtitle=subtitle;self.s=[];self.rows=[]
  self.rect(0,0,W,H,'#f3f7fa',r=0);self.rect(0,0,W,123,INK,r=0)
  self.text(40,49,f'DUAL-REALITY MAZE / WIRING SHEET {n:02}',17,'#9cd9d2',bold=True)
  self.text(40,91,title,36,'white',bold=True);self.text(1760,86,'POWER OFF BEFORE WIRING',18,'#ffd6a5',anchor='end')
  self.text(40,153,subtitle,20)
 def rect(self,x,y,w,h,fill='white',stroke='none',r=10,sw=1):
  self.s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
 def text(self,x,y,t,size=18,color=INK,bold=False,anchor='start'):
  self.s.append(f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" font-weight="{"bold" if bold else "normal"}" text-anchor="{anchor}" fill="{color}">{html.escape(str(t))}</text>')
 def para(self,x,y,t,width=42,size=19,color=INK,line=27):
  for i,l in enumerate(textwrap.wrap(t,width=width,break_long_words=False,break_on_hyphens=False)):self.text(x,y+i*line,l,size,color)
 def line(self,pts,color=MUTED,width=3,dash=None):
  p=' '.join(f'{x},{y}' for x,y in pts);d=f' stroke-dasharray="{dash}"' if dash else ''
  self.s.append(f'<polyline points="{p}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"{d}/>')
 def dot(self,x,y,color=MUTED,r=5):self.s.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>')
 def circle(self,x,y,r,fill,stroke='none',sw=2):self.s.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
 def panel(self,x,y,w,h,title):
  self.rect(x,y,w,h,'white',BORDER);self.text(x+20,y+33,title,22,bold=True)
 def wire(self,pts,cat,label=None):
  self.s.append(f'<g class="wire" data-category="{cat}">')
  self.line(pts,'white',9);self.line(pts,C[cat],4)
  self.dot(*pts[0],C[cat],4);self.dot(*pts[-1],C[cat],4)
  if label:self.text((pts[0][0]+pts[-1][0])/2,pts[0][1]-11,label,16,C[cat],True,'middle')
  self.s.append('</g>')
 def resistor(self,x,y,value,cat='digital'):
  self.rect(x,y-10,78,20,'#fff7dd',C[cat],r=1,sw=2);self.text(x+39,y-18,value,16,C[cat],True,'middle')
 def board(self,kind,used):
  self.panel(40,190,420,700,'PIN LOCATOR / top view')
  self.text(250,255,'USB connector at the top',18,MUTED,anchor='middle')
  x,y=145,285
  self.rect(x,y,235,540,'#00828b',r=22)
  for xx,yy in [(160,300),(365,300),(160,808),(365,808)]:self.circle(xx,yy,9,'#f3f7fa','#b2ccce')
  self.rect(280,268,65,54,'#c9cdd0','#879397',r=3)
  self.text(313,293,'USB-C' if kind=='R4' else 'USB-B',12,INK,True,'middle')
  self.rect(170,275,48,75,'#263138',r=2);self.text(194,367,'DC jack',12,'white',anchor='middle')
  self.text(263,392,'UNO '+kind,28,'white',True,'middle')
  if kind=='R3':
   self.rect(225,540,65,215,'#202b31',r=2);self.text(257,640,'328P',16,'white',True,'middle')
   for yy in range(550,740,14):
    self.rect(218,yy,7,5,'#b7c1c4',r=0);self.rect(290,yy,7,5,'#b7c1c4',r=0)
  else:
   self.rect(218,325,53,40,'#959a93',r=2)
   for row in range(12):
    for col in range(8):self.dot(226+col*10,510+row*10,'#d4b96b',2.5)
   self.rect(290,675,44,44,'#283337',r=2);self.text(312,734,'RA4M1',12,'white',anchor='middle')
   self.rect(210,805,35,17,'#ddd',r=2);self.text(250,854,'Qwiic unused (3.3V)',17,'#a53232',anchor='middle')
  left=['BOOT' if kind=='R4' else 'NC','IOREF','RESET','3.3V','5V','GND','GND','VIN']
  right=['SCL','SDA','AREF','GND','D13','D12','D11','D10','D9','D8','D7','D6','D5','D4','D3','D2','D1','D0']
  for i,pin in enumerate(left+['A0','A1','A2','A3','A4','A5']):
   yy=450+i*21 if i<8 else 640+(i-8)*25
   self.rect(149,yy-7,12,14,'#111c25',r=0);on=pin in used
   if on:self.circle(155,yy,6,'#f7c45c')
   self.text(136,yy+5,pin,16,INK if on else '#84929b',on,'end')
  for i,pin in enumerate(right):
   yy=375+i*22+(14 if i>=10 else 0)
   self.rect(364,yy-7,12,14,'#111c25',r=0);on=pin in used
   if on:self.circle(370,yy,6,'#f7c45c')
   self.text(388,yy+5,pin,16,INK if on else '#84929b',on)
  self.text(60,874,'Gold marks = pins used on this sheet.',17,MUTED)
 def schematic(self):self.panel(480,190,820,700,'CIRCUIT / connect matching terminal labels')
 def terminal(self,y,label,cat):
  self.rect(510,y-16,160,32,'#eff4f8',r=5);self.text(655,y+6,label,18,C[cat],True,'end');return (680,y)
 def component(self,x,y,w,h,title,subtitle=None):
  self.rect(x,y,w,h,'#f8fafb','#a7bac7',r=8,sw=2);self.text(x+15,y+30,title,21,bold=True)
  if subtitle:self.text(x+15,y+54,subtitle,16,MUTED)
 def table(self,rows,notes):
  self.rows=rows;self.panel(1320,190,440,700,'WIRE CHECKLIST')
  y=252
  for i,(a,b) in enumerate(rows):
   self.rect(1338,y-16,16,16,'white','#9aaebc',r=2)
   self.text(1367,y,a,18,bold=True);self.text(1367,y+23,b,17,MUTED);y+=54
  for n in notes:
   y+=13;self.para(1340,y,n,36,17,line=23);y+=len(textwrap.wrap(n,36,break_long_words=False))*23
 def steps(self,items):
  self.text(40,936,'ASSEMBLY ORDER',24,bold=True)
  for i,(heading,body) in enumerate(items):
   x=40+i*435;self.rect(x,958,415,209,'white',BORDER)
   self.circle(x+28,988,16,INK);self.text(x+28,994,i+1,18,'white',True,'middle')
   self.text(x+55,995,heading,21,bold=True);self.para(x+20,1030,body,36,18,line=25)
 def footer(self,extra=''):
  self.text(40,1202,'Line colors identify signals; use pin labels even if your jumper colors differ. Dots mark electrical junctions.',18,MUTED)
  self.text(40,1230,'Board illustration is simplified; it is not a drill template or a breadboard-hole map. See Sources in the browser guide.',16,MUTED)
  self.text(1760,1230,f'{self.n:02} / Dual-Reality Maze',16,MUTED,anchor='end')
 def svg(self):return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">' + ''.join(self.s)+'</svg>'

pages=[]
a=Sheet(1,'Architect controller - UNO R3','Potentiometer + pushbutton + servo. The controller RGB LED is not fitted.')
a.board('R3',{'5V','GND','A0','A4','A5','D2','D9'});a.schematic()
a.component(1040,250,225,190,'10k potentiometer','Use the actual wiper pin.')
for y,pin,cat,dest in [(320,'R3 5V','power','Outer terminal'),(365,'R3 A0','analog','Center / wiper'),(410,'R3 GND','ground','Other outer')]:
 a.wire([a.terminal(y,pin,cat),(1040,y)],cat);a.text(1055,y+6,dest,17)
a.component(1040,475,225,120,'Pushbutton')
for y,pin,cat,dest in [(535,'R3 D2','digital','Electrical side A'),(575,'R3 GND','ground','Electrical side B')]:
 a.wire([a.terminal(y,pin,cat),(1040,y)],cat);a.text(1055,y+6,dest,17)
a.component(1040,640,225,140,'SG90 servo','Match signal / + / GND.')
a.wire([a.terminal(710,'R3 D9','digital'),(1040,710)],'digital');a.text(1055,716,'Signal',18)
a.text(1120,764,'+5V',17,C['power'],True,'middle');a.text(1200,764,'GND',17,C['ground'],True,'middle')
a.component(1020,835,245,44,'Regulated 5V supply')
a.wire([(1120,835),(1120,780)],'power')
a.wire([(1200,835),(1200,780)],'ground')
a.wire([a.terminal(810,'R3 GND','ground'),(1200,810)],'ground');a.dot(1200,810,C['ground'])
a.para(720,756,'Servo +5V is separate from the Arduino USB +5V rail.',24,17,C['power'],24)
a.table([('R3 5V','Pot outer terminal'),('R3 A0','Pot center / wiper'),('R3 GND','Pot other outer terminal'),('R3 D2','Button electrical side A'),('R3 GND','Button electrical side B'),('R3 D9','Servo signal'),('External +5V','Servo positive'),('External GND + servo GND','Join R3 GND'),('R3 A4 / A5 / GND','Main A4 / A5 / GND')],['Button uses INPUT_PULLUP: no external pull-down resistor.'])
a.steps([('Local power','With USB unplugged, connect the R3 5V and GND to separate local rails. Wire the three pot terminals.'),('Button','Use one leg from each electrical side. A 4-leg button has two internally joined pairs. Verify open at rest, closed when pressed.'),('Servo supply','Use regulated 5V with adequate peak current; provision at least 1A for one SG90. Common ground is required. Do not join the two +5V rails.'),('Then test','Add 470-1000uF (correct polarity) and 100nF across the servo supply near the plug. Test the unloaded horn before adding the gate.')]);a.footer();pages.append(('01-architect',a))

e=Sheet(2,'Explorer controller - UNO R3','Joystick + bare photoresistor. Reveal activates below 1000 in the laptop game.')
e.board('R3',{'5V','GND','A0','A1','A2','A4','A5','D2'});e.schematic()
e.component(1040,245,225,285,'Joystick module','Read printed pin names.')
for y,pin,cat,dest in [(315,'R3 5V','power','VCC / +5V'),(360,'R3 GND','ground','GND'),(405,'R3 A0','analog','VRx'),(450,'R3 A1','analog','VRy'),(495,'R3 D2','digital','SW / click')]:
 e.wire([e.terminal(y,pin,cat),(1040,y)],cat);e.text(1060,y+6,dest,18)
e.text(1040,580,'BARE PHOTORESISTOR',20,bold=True)
e.wire([e.terminal(620,'R3 5V','power'),(1130,620)],'power')
e.line([(1130,620),(1130,640)],C['power'],4);e.circle(1130,663,25,'#fff7dd',C['analog']);e.line([(1114,659),(1146,659),(1114,670),(1146,670)],C['analog'],2)
e.text(1170,669,'LDR',18);e.wire([(1130,689),(1130,715)],'analog')
e.wire([e.terminal(715,'R3 A2','analog'),(1130,715)],'analog');e.dot(1130,715,C['analog'],7);e.text(1160,721,'Junction',17,C['analog'])
e.line([(1130,715),(1130,747)],C['analog'],4);e.rect(1120,747,20,55,'#fff7dd',C['ground'],r=1,sw=2);e.text(1160,779,'10k ohm',18)
e.wire([e.terminal(838,'R3 GND','ground'),(1130,838),(1130,802)],'ground')
e.table([('R3 5V','Joystick VCC / +5V'),('R3 GND','Joystick GND'),('R3 A0','Joystick VRx'),('R3 A1','Joystick VRy'),('R3 D2','Joystick SW'),('R3 5V','One photoresistor leg'),('Other photoresistor leg','A2 AND one 10k resistor leg'),('Other 10k resistor leg','R3 GND'),('R3 A4 / A5 / GND','Main A4 / A5 / GND')],['A2 is the junction between the LDR and resistor, not a direct connection to 5V.'])
e.steps([('Joystick first','Power off. Connect 5V, GND, VRx, VRy and SW by their printed labels. Do not infer the pin order from a different module.'),('LDR strip A','On a breadboard, put 5V and one LDR leg on the same connected five-hole strip. The LDR has no polarity.'),('LDR strips B / C','Strip B: other LDR leg + A2 jumper + resistor leg. Strip C: other resistor leg + GND. All three strips must be distinct.'),('Check Reveal','Cover the LDR: the value should fall below 1000. Uncover to reach 1000 or above and rearm. Keep it away from internal LED light.')]);e.footer();pages.append(('02-explorer',e))

m=Sheet(3,'Main hub - UNO R4 WiFi','16x2 I2C LCD + common-cathode RGB LED + small passive piezo. Use the 5V header bus.')
m.board('R4',{'5V','GND','A4','A5','SDA','SCL','D3','D5','D9','D6'});m.schematic()
m.component(1040,245,225,220,'16x2 I2C LCD','4-pin backpack connector')
for y,pin,cat,dest in [(315,'R4 SDA','sda','SDA'),(355,'R4 SCL','scl','SCL'),(395,'R4 5V','power','VCC'),(435,'R4 GND','ground','GND')]:
 m.wire([m.terminal(y,pin,cat),(1040,y)],cat);m.text(1060,y+6,dest,18)
m.component(1040,510,225,235,'RGB LED','Bare / common cathode')
for y,pin,cat,dest,color in [(580,'R4 D9','digital','Red anode','#c53740'),(625,'R4 D5','digital','Green anode','#108a55'),(670,'R4 D3','digital','Blue anode','#296dcb')]:
 m.wire([m.terminal(y,pin,cat),(1040,y)],cat);m.resistor(825,y,'680 ohm');m.text(1060,y+6,dest,18,color,True)
m.wire([m.terminal(715,'R4 GND','ground'),(1040,715)],'ground');m.text(1060,721,'Common cathode',17)
m.component(1040,785,225,85,'Small passive piezo')
m.wire([m.terminal(824,'R4 D6','digital'),(1040,824)],'digital');m.resistor(825,824,'1k ohm');m.text(1060,830,'+ / signal',17)
m.wire([m.terminal(858,'R4 GND','ground'),(1040,858)],'ground');m.text(1060,864,'- / GND',17)
m.table([('R4 5V / GND','LCD VCC / GND'),('R4 SDA / SCL','LCD SDA / SCL'),('R4 D9 -> 680 ohm','RGB red anode'),('R4 D5 -> 680 ohm','RGB green anode'),('R4 D3 -> 680 ohm','RGB blue anode'),('RGB common cathode','R4 GND'),('R4 D6 -> 1k ohm','Small passive piezo +'),('Piezo -','R4 GND'),('R4 SDA / SCL / GND','Both R3 controllers')],['8mA maximum per R4 GPIO. The RGB resistor value corrects the older 330-ohm guide.'])
m.steps([('LCD first','Power off. Connect the LCD backpack by GND, VCC, SDA, SCL labels. Adjust the contrast trimmer if the backlight is on but text is absent.'),('RGB branches','Use a separate 680-ohm resistor for each color. Verify the common cathode and color pins for your actual LED; leg order varies.'),('Buzzer type','The 1k series resistor limits the small passive piezo branch current. A high-current or active buzzer needs a transistor driver; do not substitute it directly.'),('Finish at Main','R3 cables: Main A4/A5. LCD: SDA/SCL. Not Qwiic. D2 is unused. Optional four-LED fading is on sheet 05. Then wire both R3 cables as on sheet 04.')]);m.footer();pages.append(('03-main',m))

b=Sheet(4,'Connect both R3 controllers to Main','One shared I2C bus: Main polls unique addresses. Both controllers can be used at the same time.')
b.panel(40,190,1720,700,'SYSTEM CONNECTIONS / all grounds common; each board powered through its own USB cable')
for x,title,sub in [(80,'ARCHITECT / UNO R3','Address 0x11'),(700,'MAIN / UNO R4 WiFi','Bus controller / 100 kHz'),(1310,'EXPLORER / UNO R3','Address 0x10')]:
 b.component(x,280,360,250,title,sub)
 for y,label in [(385,'A4 / SDA' if x!=700 else 'A4 / SDA'),(430,'A5 / SCL' if x!=700 else 'A5 / SCL'),(475,'GND')]:b.text(x+180,y+6,label,21,anchor='middle')
for y,cat in [(385,'sda'),(430,'scl'),(475,'ground')]:
 b.wire([(440,y),(700,y)],cat);b.wire([(1060,y),(1310,y)],cat)
b.text(570,353,'30 cm cable',18,MUTED,True,'middle');b.text(1185,353,'30 cm cable',18,MUTED,True,'middle')
b.component(690,650,380,180,'LCD backpack','Shares the same SDA / SCL bus')
for xx,label,cat,yy in [(750,'SDA','sda',385),(830,'SCL','scl',430),(910,'GND','ground',475)]:
 b.wire([(xx,530),(xx,650)],cat);b.text(xx,628,label,18,C[cat],True,'middle');b.dot(xx,530,C[cat])
 b.text(xx,548,'',16)
b.text(880,485,'',18)
# These short exits represent the corresponding labeled terminals of the Main block.
for xx,label in [(750,'SDA'),(830,'SCL'),(910,'GND'),(990,'5V')]:b.text(xx,520,label,15,anchor='middle')
b.wire([(990,530),(990,650)],'power');b.text(990,628,'Main 5V',18,C['power'],True,'middle')
b.rows=[('Architect R3 A4','Main R4 SDA'),('Architect R3 A5','Main R4 SCL'),('Architect R3 GND','Main R4 GND'),('Explorer R3 A4','Main R4 SDA (same bus)'),('Explorer R3 A5','Main R4 SCL (same bus)'),('Explorer R3 GND','Main R4 GND'),('LCD SDA / SCL','Main A4 (SDA) / SCL'),('LCD VCC / GND','Main 5V / GND'),('If pull-ups absent: SDA','4.7k ohm to Main 5V'),('If pull-ups absent: SCL','4.7k ohm to Main 5V')]
b.para(90,590,'Architect USB-B -> powered USB hub or laptop. The servo has a separate regulated 5V supply with common ground.',30,21,line=31)
b.para(1310,590,'Explorer USB-B -> powered USB hub or laptop.',27,21,line=31)
b.para(1310,740,'Main USB-C provides power. Main built-in Wi-Fi -> laptop game. No controller Wi-Fi modules are required.',29,21,line=31)
b.text(90,798,'NO 5V jumper between boards.',22,C['power'],True)
b.para(90,833,'Only SDA + SCL + GND belong in each controller cable.',40,19,line=26)
b.steps([('Ground first','Unplug USB and the servo supply. Architect GND -> Main GND. Explorer GND -> Main GND. Include the servo supply negative in this common ground.'),('Add the two signals','Architect A4 -> Main A4 (SDA); A5 -> Main A5 (SCL). Explorer A4 -> the SAME Main A4 (SDA); A5 -> the SAME Main A5 (SCL). Use breadboard junctions to fan out.'),('Check pull-ups','If the LCD backpack lacks suitable pull-ups, add one 4.7k from SDA to Main 5V and one 4.7k from SCL to Main 5V. Do not add a pair at every board.'),('Power and connect','Power all boards together. Start Maze.bat -> Connect Main Wi-Fi. Confirm both controllers OK, then blue Main status. Keep the joystick centered during reconnect.')]);b.footer();pages.append(('04-three-board-i2c',b))

o=Sheet(5,'Optional Main lighting - four green LEDs','Use this sheet only if fitting the four decorative LEDs. They fade together from one transistor channel.')
o.panel(40,190,1720,700,'LOW-SIDE MOSFET DRIVER / LED current comes from the 5V rail, not directly from D10')
o.text(140,280,'Main 5V',24,C['power'],True);o.wire([(260,273),(1510,273)],'power')
for x in [650,900,1150,1400]:
 o.wire([(x,273),(x,335)],'power');o.rect(x-10,335,20,55,'#fff7dd',C['power'],r=1,sw=2);o.text(x+22,366,'330 ohm',18,C['power'],True);o.line([(x,390),(x,430)],C['power'],4)
 o.circle(x,455,25,'#e6f5df','#268045',3);o.text(x,461,'LED',15,'#268045',True,'middle');o.text(x+36,436,'+',19,C['power'],True);o.text(x+36,485,'-',19,C['ground'],True)
 o.wire([(x,480),(x,550)],'ground');o.dot(x,273,C['power']);o.dot(x,550,C['ground'])
o.wire([(650,550),(1400,550)],'ground');o.wire([(1050,550),(1050,615)],'ground');o.dot(1050,550,C['ground'])
o.component(960,615,230,115,'Logic-level','N-channel MOSFET')
o.text(1050,610,'DRAIN',18,C['ground'],True,'middle');o.text(1090,754,'SOURCE',18,C['ground'],True);o.text(947,663,'GATE',18,C['digital'],True,'end')
o.wire([(280,680),(960,680)],'digital');o.text(140,686,'Main D10',23,C['digital'],True);o.resistor(500,680,'1k ohm')
o.wire([(1050,730),(1050,825),(290,825)],'ground');o.text(140,831,'Main GND',23,C['ground'],True)
o.wire([(740,680),(740,735)],'digital');o.dot(740,680,C['digital']);o.rect(730,735,20,50,'#fff7dd',C['ground'],r=1,sw=2);o.text(780,769,'100k ohm pull-down',20)
o.wire([(740,785),(740,825)],'ground');o.dot(740,825,C['ground'])
o.para(1310,670,'Identify G/D/S from the exact MOSFET datasheet. Package leg order is not standardized.',30,21,line=30)
o.rows=[('Main 5V','One 330-ohm resistor per green LED anode (four branches)'),('Four LED cathodes','MOSFET drain'),('MOSFET source','Main GND'),('Main D10','1k-ohm resistor to MOSFET gate'),('MOSFET gate','100k-ohm pull-down to Main GND')]
o.steps([('Separate resistors','Main 5V -> one 330-ohm resistor -> each green LED anode. Repeat four times; do not share one resistor.'),('Join cathodes','Join all four LED cathodes at the MOSFET drain. MOSFET source -> Main GND.'),('Control input','D10 -> 1k-ohm resistor -> gate. Add a 100k gate-to-GND resistor so the MOSFET defaults off.'),('Test fade','The current firmware fades D10. Use a MOSFET specified for operation at a 5V gate. Keep the center RGB optical area separate if desired.')]);o.footer();pages.append(('05-optional-green-lighting',o))

combined=fitz.open()
for name,sheet in pages:
 svg=sheet.svg();(OUT/(name+'.svg')).write_text(svg,encoding='utf-8')
 vector=fitz.open(stream=svg.encode(),filetype='svg');pagepdf=fitz.open('pdf',vector.convert_to_pdf())
 # Scale the vectors to landscape A3, retaining selectable text.
 dst=combined.new_page(width=1190.55,height=841.89);dst.show_pdf_page(dst.rect,pagepdf,0)
 pagepdf[0].get_pixmap(matrix=fitz.Matrix(1.2,1.2),alpha=False).save(OUT/(name+'.png'))
 with (OUT/(name+'.csv')).open('w',newline='',encoding='utf-8-sig') as f:
  wr=csv.writer(f);wr.writerow(['From','Connect to']);wr.writerows(sheet.rows)
combined.save(PDF,garbage=4,deflate=True)

blocks=[]
for name,sheet in pages:
 rows=''.join(f'<label><input type="checkbox" data-key="{name}-{i}"><b>{html.escape(a)}</b> → {html.escape(b)}</label>' for i,(a,b) in enumerate(sheet.rows))
 blocks.append(f'<section id="{name}"><h2>{sheet.title}</h2><p>{sheet.subtitle}</p><p class="tools"><a href="{name}.png">Full-resolution image</a> · <a href="{name}.svg">Vector SVG</a> · <a href="{name}.csv">Wire checklist CSV</a></p><div class="diagram">{sheet.svg()}</div><div class="checks">{rows}</div></section>')
sources=f'<li><a href="{R3}">Arduino UNO R3 official full pinout</a></li><li><a href="{R4}">Arduino UNO R4 WiFi official full pinout</a></li><li><a href="{SPEC}">Arduino UNO R4 WiFi GPIO and Qwiic limits</a></li>'
document='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Dual-Reality Maze - wiring guide</title><style>
*{box-sizing:border-box}body{margin:0;background:#edf3f6;color:#142c42;font:17px/1.6 system-ui,sans-serif}header,main{max-width:1500px;margin:auto;padding:28px}header h1{margin:0;font-size:38px}nav{display:flex;gap:8px;flex-wrap:wrap;margin:18px 0}a{color:#126b83}nav a,button{background:white;border:1px solid #bbcbd4;border-radius:6px;padding:8px 14px;color:#142c42;text-decoration:none;cursor:pointer}.notice{padding:18px 22px;border-left:5px solid #bf7125;background:#fff6e9}section{background:white;border:1px solid #d5e0e6;border-radius:12px;padding:24px;margin:25px 0}h2{margin:0}.diagram{overflow:auto}.diagram svg{display:block;width:100%;height:auto;min-width:850px}.zoom .diagram svg{width:1800px;max-width:none}.wire{transition:opacity .15s}.checks{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:18px}.checks label{background:#f1f6f8;padding:10px;font-size:15px;cursor:pointer}.checks input{margin-right:8px}#filters{display:flex;flex-wrap:wrap;gap:7px}button.active{background:#142c42;color:white}small{color:#536778}@media(max-width:900px){.checks{grid-template-columns:1fr}header,main{padding:14px}}@media print{header,.tools,.checks,#sources{display:none}main,section{padding:0;margin:0;border:0}section{break-after:page}.diagram svg{min-width:0;width:100%}@page{size:A3 landscape;margin:6mm}}
</style><header><h1>Build one controller at a time</h1><p>Architect → Explorer → Main → shared I2C. Pin assignments match the current three-board firmware. All diagrams are original simplified wiring illustrations, not electrical simulation results.</p><nav>'''+''.join(f'<a href="#{n}">{s.n:02} {s.title.split(" - ")[0]}</a>' for n,s in pages)+'''</nav><div class="notice"><b>Correction:</b> use a separate <b>680-ohm resistor for each Main RGB color</b>. The UNO R4 has an 8mA GPIO limit; the older 330-ohm value could exceed that limit. Each USB-powered board keeps its own +5V rail. Share GND. The servo supply positive stays separate. Disconnect power before rewiring.</div><p><a href="../../output/pdf/Dual-Reality-Maze-Wiring-Guide.pdf">Download the five-page printable PDF</a> · <button id="zoom">Toggle full-size diagrams</button></p><div id="filters"><button class="active" data-cat="all">All wires</button>'''+''.join(f'<button data-cat="{k}">{k.upper()}</button>' for k in C)+'''</div><small>Filter colors to trace a signal. Check off each connection as you build. A line crossing is not a junction unless a dot marks it.</small></header><main>'''+''.join(blocks)+f'''<section id="sources"><h2>Sources and component assumptions</h2><ul>{sources}</ul><p>Read against the current Architect, Explorer, Main and Protocol.h files. The LED drawing assumes a bare common-cathode RGB. The buzzer drawing assumes a small passive piezo. A button uses INPUT_PULLUP (D2 to GND), not the old pull-down circuit. The LDR is bare with a 10k resistor, not an AO/DO sensor module.</p><p>The main LCD and both controllers share SDA/SCL. Arduino R3 A4 is SDA and A5 is SCL. Main uses the 5V header bus; its Qwiic connector is a separate 3.3V bus and is not used. Pin-label order on modules, RGB LEDs and MOSFET packages must be checked for the actual part.</p><p>Assembly order: local GND and low-current components; signal wires; servo supply connections with common ground; interboard GND then SDA/SCL; inspect for shorts; power all boards together; connect the game. Do not connect or remove jumper wires while powered.</p><p>The diagrams give electrical connections, not exact breadboard hole coordinates. Five holes in a terminal strip are connected; the opposite side of the center trench is separate. Long power rails may be split halfway. Use continuity checks and jumpers for intended joins.</p></section></main>'''+'''<script>
document.getElementById('zoom').onclick=()=>document.body.classList.toggle('zoom');
document.querySelectorAll('[data-cat]').forEach(b=>b.onclick=()=>{document.querySelectorAll('[data-cat]').forEach(x=>x.classList.toggle('active',x===b));document.querySelectorAll('.wire').forEach(w=>w.style.opacity=b.dataset.cat==='all'||w.dataset.category===b.dataset.cat?'1':'.12');});
document.querySelectorAll('[data-key]').forEach(c=>{try{c.checked=localStorage.getItem('maze-wiring-'+c.dataset.key)==='yes'}catch{}c.onchange=()=>{try{localStorage.setItem('maze-wiring-'+c.dataset.key,c.checked?'yes':'no')}catch{}}});
</script></html>'''
(OUT/'index.html').write_text(document,encoding='utf-8')
(OUT/'sources.json').write_text(json.dumps({'pinouts':[R3,R4],'r4_limits':SPEC,'checked':'2026-11-20','rgb_series_ohms':680,'piezo_series_ohms':1000,'not_a_simulation':True},indent=2),encoding='utf-8')
print(f'Created {len(pages)} sheets, PNGs, SVGs and browser guide. PDF: {PDF}')
