from pathlib import Path
import csv,html,json,zipfile,shutil
R=Path(__file__).parent/'arduino-system'
text=(R/'WIRING.md').read_text(encoding='utf-8')
for role,section in [('Explorer','Explorer UNO R3'),('Architect','Architect UNO R3'),('Main','Main UNO R4 WiFi')]:
 block=text.split('## '+section)[1].split('\n## ')[0]
 rows=[]
 for line in block.splitlines():
  if line.startswith('|') and '---' not in line:
   rows.append([v.strip() for v in line.strip('|').split('|')])
 with (R/(role+'-wiring.csv')).open('w',newline='',encoding='utf-8-sig') as f:csv.writer(f).writerows(rows)
with (R/'Interboard-wiring.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f);w.writerow(['From','To','Signal','Notes'])
 for board in ['Explorer R3','Architect R3']:
  for pin,main in [('A4','SDA header'),('A5','SCL header'),('GND','GND')]:w.writerow([board+' '+pin,'Main '+main,main,'30 cm; no +5V cable connection'])
 for pin in ['SDA','SCL','GND','5V']:w.writerow(['Main '+pin,'LCD '+('VCC' if pin=='5V' else pin),pin,'Use 5V headers; not Qwiic'])
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630"><rect width="1200" height="630" fill="#101c2c"/><style>text{font:18px sans-serif;fill:#eef3fa}.title{font:bold 26px sans-serif}rect.board{fill:#203a52;stroke:#c9a86b;stroke-width:2}.wire{fill:none;stroke:#77d9ce;stroke-width:4}</style><text x="40" y="45" class="title">Dual-Reality Maze — connection overview</text><rect class="board" x="40" y="110" width="285" height="140" rx="12"/><text x="60" y="145">Explorer · UNO R3 · 0x10</text><text x="60" y="180">Joystick / LDR</text><text x="60" y="220">A4 SDA · A5 SCL · GND</text><rect class="board" x="40" y="330" width="285" height="140" rx="12"/><text x="60" y="365">Architect · UNO R3 · 0x11</text><text x="60" y="400">Pot / button / servo</text><text x="60" y="440">A4 SDA · A5 SCL · GND</text><rect class="board" x="480" y="210" width="310" height="180" rx="12"/><text x="500" y="250">Main · UNO R4 WiFi</text><text x="500" y="290">5V header SDA / SCL</text><text x="500" y="325">RGB / buzzer / LED driver</text><text x="500" y="365">I2C controller · 100 kHz</text><rect class="board" x="505" y="75" width="260" height="80" rx="10"/><text x="530" y="105">16×2 I2C LCD</text><text x="520" y="135">5V / GND / SDA / SCL</text><rect class="board" x="930" y="230" width="230" height="130" rx="10"/><text x="965" y="270">Laptop game</text><text x="950" y="310">Local game + bridge</text><path class="wire" d="M325 205H410V270H480M325 425H410V330H480M635 155V210M790 295H930"/><text x="345" y="185">30 cm</text><text x="345" y="460">30 cm</text><text x="813" y="270">USB or Wi-Fi</text><text x="813" y="330">Two-way data</text><text x="40" y="525">I2C cables contain SDA, SCL and common GND. Keep independently powered +5V rails separate.</text><text x="40" y="560">Servo: separate regulated 5V supply + common GND. Do not use the 3.3V Qwiic socket.</text><text x="40" y="595">One suitable pull-up pair on the bus; check LCD backpack first. See WIRING.md for every pin.</text></svg>'''
(R/'connection-overview.svg').write_text(svg,encoding='utf-8')
for role in ['Explorer','Architect','Main']:
 with (R/(role+'-wiring.csv')).open(encoding='utf-8-sig') as f: rows=list(csv.reader(f))[1:]
 h=110+len(rows)*70
 parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="{h}" viewBox="0 0 1400 {h}"><rect width="1400" height="{h}" fill="#f3f6fa"/><style>text{{font:17px sans-serif;fill:#152d44}}.title{{font:bold 26px sans-serif}}</style><text x="30" y="40" class="title">{role} — terminal connection chart</text><text x="30" y="75">Logical connections, not an exact breadboard footprint. Read the accompanying power and resistor notes.</text>']
 for i,row in enumerate(rows):
  y=100+i*70
  parts.append(f'<rect x="25" y="{y}" width="235" height="50" rx="8" fill="#dce7f1"/><text x="35" y="{y+30}">{html.escape(row[0])}</text><path d="M260 {y+25}H325" stroke="#278a82" stroke-width="3"/><rect x="325" y="{y}" width="1040" height="50" rx="8" fill="white"/><text x="338" y="{y+22}">{html.escape(row[1])}</text><text x="338" y="{y+43}" style="font-size:14px">{html.escape(row[2])}</text>')
 parts.append('</svg>');(R/(role+'-connections.svg')).write_text(''.join(parts),encoding='utf-8')
sections=[]
for name in ['START_HERE.md','WIRING.md']:
 sections.append('<section><h2>'+name+'</h2><pre>'+html.escape((R/name).read_text(encoding='utf-8'))+'</pre></section>')
(R/'Guide.html').write_text('<!doctype html><meta charset="utf-8"><title>Arduino wiring and setup</title><style>body{max-width:1150px;margin:30px auto;font:16px system-ui;color:#172333}img{width:100%}pre{white-space:pre-wrap;font:15px/1.6 Consolas,monospace}h1,h2{color:#234c6b}</style><h1>Dual-Reality Maze: Arduino setup</h1><img src="connection-overview.svg">'+''.join(f'<h2>{role} connections</h2><img src="{role}-connections.svg">' for role in ['Explorer','Architect','Main'])+''.join(sections),encoding='utf-8')
shutil.copy2(Path(__file__).parents[1]/'maze-source/work/story/hardware-hub.js',R/'hardware-hub.js')
target=Path.home()/'Downloads/Dual-Reality-Maze-Arduino-System.zip'
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=5) as z:
 for p in R.rglob('*'):
  if p.is_file():z.write(p,'Dual-Reality-Maze-Arduino-System/'+str(p.relative_to(R)))
with zipfile.ZipFile(target) as z:assert z.testzip() is None
print(target, target.stat().st_size)
