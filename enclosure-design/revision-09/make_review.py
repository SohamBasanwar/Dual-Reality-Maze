from pathlib import Path
import json,csv,html,zipfile
R=Path(__file__).resolve().parent
records=json.loads((R/'scene.json').read_text())
parts=[r for r in records if not r['component']]
with (R/'PARTS.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f);w.writerow(['Assembly','Part','STL filename','File label','Physical marking','Notes'])
    for r in parts:w.writerow([r['role'],r['name'],r['file'],'Soham Basanwar',r['personalization'],r['notes']])

def pic(src,label):return f'<figure><img src="previews/{src}" loading="lazy" alt="{html.escape(label)}"><figcaption>{label}</figcaption></figure>'
body='''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Dual-Reality Maze · Revision 09</title><style>
*{box-sizing:border-box}body{margin:0;background:#11151d;color:#e5e6eb;font:17px/1.6 system-ui}main{max-width:1200px;margin:auto;padding:44px 24px}h1{font:42px Georgia;margin:8px 0;color:#e9c68f}h2{font:29px Georgia;color:#e9c68f;margin-top:48px}h3{font-size:21px}p{max-width:900px}a{color:#9ecbff}.eyebrow{letter-spacing:.15em;font-size:12px;color:#b3a087}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:20px}figure{margin:0;background:#1a212d;border-radius:14px;overflow:hidden}img{width:100%;display:block}figcaption{padding:13px 18px;font-size:14px;color:#c8cbd5}.card{background:#1a212d;padding:22px;border-radius:12px}button{background:#caa169;color:#141922;border:0;border-radius:8px;font:inherit;padding:10px 20px;cursor:pointer;margin:6px}table{width:100%;border-collapse:collapse;font-size:14px}td,th{text-align:left;padding:12px;border-bottom:1px solid #354050;vertical-align:top}.status{padding:15px;border-left:3px solid #caa169;background:#202431}details{margin:20px 0}summary{cursor:pointer}code{font-size:13px}
</style></head><body><main><div class="eyebrow">SOHAM BASANWAR · DESIGN REVIEW · 26 OCTOBER 2026</div><h1>Dual-Reality Maze</h1><p>Revision 09 · recessed castle gate, contoured battery access and personalized parts.</p><p class="status">Actual CAD renders. Prototype fit, printed latch strength, light transmission and powered operation remain unverified.</p>'''
body+=pic('family-charcoal.png','The three matching enclosures. Colour is illustrative; final structural filament is undecided.')
body+='''<h2>The castle gate returns</h2><p>The arched portcullis and visible lifting motion are back. Its drive now sits inside the controller. The guard reaches <strong>40 mm</strong> above the 58 mm lid plane, compared with 60 mm for the earlier guard: a 20 mm reduction. The gate travels about 12.12 mm through its nominal range.</p><div class="grid"><div><figure><img id="gate" src="previews/gate-closed.png" alt="Castle gate closed"><figcaption id="gateCaption">Closed portcullis, recessed drive.</figcaption></figure><button onclick="setGate(false)">Closed</button><button onclick="setGate(true)">Open</button></div>'''
body+=pic('gate-mechanism.png','Guard removed. The original nylon horn drives a captive pin in the gate yoke. A bridge captures the horn axially; no printed spline or centre screw is assumed.')+'</div>'
body+='''<p>The closed and open views use actual CAD parts and their calculated travel. Horn fit, tiny pin durability, printed latch strength, pinch access and loaded servo operation still need physical tests. The flat rotary-window concept remains available in Revision 07 for comparison.</p>'''
body+='<h2>Controller and Main views</h2><div class="grid">'
for role in ['explorer','architect','main']:body+=pic(role+'-assembled.png',role.title()+' · assembled')
body+='</div><h2>Battery access and internal layout</h2><p>The raised service pad has been removed. The battery door is a 2.4 mm vertical skin shaped from the original oval underside and set 0.15 mm inward. Its two leading tabs and release catch remain. Physical grip and latch coupons are still essential.</p><div class="grid">'
for role in ['explorer','architect']:body+=pic(role+'-battery-door.png',role.title()+' · underside access')
for role in ['explorer','architect','main']:body+=pic(role+'-internal.png',role.title()+' · base, component reservations and provisional ESP32 space')
body+='</div>'
body+=pic('battery-contour.png','Light-material underside inspection: the door follows the grip surface without the added flat pad.')
body+=pic('battery-door-detail.png','Contoured door, inside view: full name, two locating tabs and release catch.')
body+='<h2>Your name and initials</h2><p>Large parts carry “Soham Basanwar”; selected small parts carry “SB”. Thin keepers, the guard and tiny fit-sensitive parts remain unmarked. Every printed part is labelled with your full name in its filename, CAD object label and <a href="PARTS.csv">parts list</a>.</p>'
body+='<details><summary>All printed parts and their marking</summary><table><tr><th>Assembly / part</th><th>Marking</th><th>File</th></tr>'
for r in parts:body+=f'<tr><td>{r["role"].title()} / {r["name"].replace("_"," ")}</td><td>{html.escape(r["personalization"])}</td><td><a href="prototype-stl/{r["file"]}">STL</a></td></tr>'
body+='</table></details><h2>Review and files</h2><p><a href="README.md">Design and mechanism notes</a> · <a href="PRINT_AND_ASSEMBLY.md">Print and assembly guidance</a> · <a href="DIMENSION_CHECKLIST.csv">Measurement checklist</a> · <a href="REVIEW_VALIDATION.json">Validation report</a> · <a href="../revision-06/index.html">Previous revision</a></p><div class="grid">'
for role in ['explorer','architect','main']:body+=f'<div class="card"><h3>{role.title()}</h3><a href="cad/{role}-revision09.FCStd">FreeCAD assembly</a><br><a href="cad/{role}-printed-parts.step">STEP solids</a></div>'
body+='</div><p>Open a native assembly in FreeCAD, use the parts list to select files, and test the fit coupons in PrusaSlicer before committing to full shells. No extra software or machine-specific G-code is required.</p></main><script>function setGate(open){document.getElementById("gate").src="previews/gate-"+(open?"open":"closed")+".png";document.getElementById("gateCaption").textContent=open?"Open: the portcullis lifts about 12.12 mm.":"Closed: the portcullis covers the passage."}</script></body></html>'
(R/'index.html').write_text(body,encoding='utf-8')
(R/'Open_Revision09.FCMacro').write_text("from pathlib import Path\nimport FreeCAD as App\nR=Path(__file__).resolve().parent\nfor role in ['explorer','architect','main']:\n    doc=App.openDocument(str(R/'cad'/(role+'-revision09.FCStd')))\n    for o in doc.getObject('ComponentEnvelopes').Group:o.ViewObject.Visibility=False\n    Gui.activeDocument().activeView().viewAxonometric()\n    Gui.activeDocument().activeView().fitAll()\n",encoding='utf-8')
print('Review gallery and parts list written')
