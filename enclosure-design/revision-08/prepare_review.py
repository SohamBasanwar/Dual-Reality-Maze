from pathlib import Path
R=Path(__file__).resolve().parent
p=R/'render_details.py'
s=p.read_text().replace("pivot=Vector((-.068,-.0555,.055))","pivot=Vector((-.062,-.0435,.055))").replace("(-.073,-.055,.064)","(-.067,-.0435,.064)")
p.write_text(s)
p=R/'make_review.py'
s=p.read_text(encoding='utf-8').replace('Revision 07','Revision 08').replace('revision07','revision08').replace('Revision07','Revision08').replace('REVISION 07','REVISION 08').replace('25 OCTOBER 2026','26 OCTOBER 2026').replace('25 October 2026','26 October 2026')
s=s.replace('compact rune gate, softer battery access and personalized parts.','recessed castle gate, contoured battery access and personalized parts.')
a=s.index("body+='''<h2>A gate that fits a handheld")
b=s.index("body+='<h2>Controller and Main views",a)
s=s[:a]+'''body+=\'''<h2>The castle gate returns</h2><p>The arched portcullis and visible lifting motion are back. Its drive now sits inside the controller. The guard reaches <strong>39 mm</strong> above the 58 mm lid plane, compared with 60 mm for the earlier guard: a 21 mm reduction. The gate travels about 12.12 mm through its nominal range.</p><div class="grid"><div><figure><img id="gate" src="previews/gate-closed.png" alt="Castle gate closed"><figcaption id="gateCaption">Closed portcullis, recessed drive.</figcaption></figure><button onclick="setGate(false)">Closed</button><button onclick="setGate(true)">Open</button></div>\'''
body+=pic('gate-mechanism.png','Guard removed. The original nylon horn drives a captive pin in the gate yoke. A bridge captures the horn axially; no printed spline or centre screw is assumed.')+'</div>'
body+=\'''<p>The closed and open views use actual CAD parts and their calculated travel. Horn fit, tiny pin durability, printed latch strength, pinch access and loaded servo operation still need physical tests. The flat rotary-window concept remains available in Revision 07 for comparison.</p>\'''
''' +s[b:]
s=s.replace('The door has a rounded exposed perimeter and a broader rolled seating transition. Two leading tabs and a release catch retain it. The name sits on the inside of the door, away from the palm. Physical grip and latch coupons are still essential.','The raised service pad has been removed. The battery door is a 2.4 mm vertical skin shaped from the original oval underside and set 0.15 mm inward. Its two leading tabs and release catch remain. Physical grip and latch coupons are still essential.')
a=s.index("body+='</div><h2>Your name and initials")
b=s.index("body+='<details><summary>All printed parts",a)
s=s[:a]+'''body+='</div>'
body+=pic('battery-contour.png','Light-material underside inspection: the door follows the grip surface without the added flat pad.')
body+=pic('battery-door-detail.png','Contoured door, inside view: full name, two locating tabs and release catch.')
body+='<h2>Your name and initials</h2><p>Large parts carry “Soham Basanwar”; selected small parts carry “SB”. Thin keepers, the guard and tiny fit-sensitive parts remain unmarked. Every printed part is labelled with your full name in its filename, CAD object label and <a href="PARTS.csv">parts list</a>.</p>'
''' +s[b:]
s=s.replace('26 OCTOBER 2026','26 OCTOBER 2026').replace('Small','Small')
s=s.replace('Open: the clear arch sector aligns with the viewport.','Open: the portcullis lifts about 12.12 mm.').replace('Closed: bars across the window.','Closed: the portcullis covers the passage.')
s=s.replace('Open_Revision07','Open_Revision08')
p.write_text(s,encoding='utf-8')
print('R08 review prepared')
