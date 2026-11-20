from pathlib import Path
import json,re,html
R=Path(__file__).resolve().parent;e=html.escape
parts=[r for r in json.loads((R/'scene.json').read_text(encoding='utf-8')) if not r['component']]
prep=json.loads((R/'PRINT_PREP.json').read_text(encoding='utf-8'))
source=(R.parent/'revision-11/index.html').read_text(encoding='utf-8')
source=source.replace('revision11','revision12').replace('Revision 11','Revision 12').replace('data-r11-generated','data-r12-generated')
source=source.replace('Light the maze.<br>Find every part.','Clean outside.<br>Clear inside.')
source=source.replace('Four green rune accents, a shielded RGB portal and an illustrated assembly code for every printed piece.','Hidden ownership and part codes, removable light inserts, and print batches prepared for one material at a time.')
source=source.replace('Four Main bezel receiver areas carry their matching bezel codes.','Matching bezel codes are now inside the lid.')
source=source.replace('R11_PRINT_NOTES.md','R12_PRINT_NOTES.md')
source=source.replace('<nav>','<nav><a href="#hidden">Hidden markings</a><a href="#printing">Print preparation</a>')

def fig(name,caption):return f'<figure><a href="previews/{name}.png" target="_blank"><img src="previews/{name}.png" loading="lazy" alt="{e(caption)}"></a><figcaption>{caption}</figcaption></figure>'
hidden='''<section id="hidden"><h2>The decoration stays. The lettering goes inside.</h2><p>Ownership and assembly codes are removed from exposed button tops, shutter tabs, light bezels, lid receiver areas and case bottoms. Recessed replacements sit on hidden faces. The functional icons, fantasy motifs and internal adjustment arrows remain.</p><div class="grid">'''
hidden+=fig('hidden-base-explorer','Explorer: the full name is now on the inside floor, beneath the removable lid. The outside bottom is clean.')
hidden+=fig('hidden-base-main','Main: interior owner engraving. Raised mounts and the battery compartment retain their existing layout.')
hidden+=fig('hidden-button','Architect button: code and initials beneath the cap, away from its central stem and outer stop rim.')
hidden+=fig('hidden-shutter','Main USB shutter: the finger tab is clean; the code and initials are on the inward-facing plate.')
hidden+=fig('hidden-bezel','Green-light bezel: code and initials on its underside. Keep the lens and snap legs clear of markings.')
hidden+=fig('hidden-receiver','Matching bezel code on the underside of the enclosed light gallery, visible while the lid is open.')
hidden+='''</div><p class="status">Small parts without a safe hidden face use their bag code and filename. The servo retainer is left physically unmarked because its underside contacts the servo and its arms flex. No letters are added to optical surfaces.</p></section>'''
source=source.replace('<section id="lighting">',hidden+'<section id="lighting">',1)
source=source.replace('The provisional ESP32 space moves to the centre','The provisional ESP32 space remains at the centre')

engrave='<section id="engraving"><h2>Owner engraving and printed-part sheets</h2><p>The full name is Soham Basanwar; small safe areas use SB. These are renders of actual CAD cuts. Exterior pieces use concealed faces, and tiny or optical parts use their labelled bag.</p><div class="grid">'
for name,caption in [('engraving-lid','Full name inside the lid'),('engraving-door','Full name inside the battery door'),('engraving-insert','Full name on the internal height insert'),('engraving-jaw','SB on an internal adjustment jaw')]:engrave+=fig(name,caption)
engrave+='</div><div class="grid three" style="margin-top:20px">'
for n,c in [('full-name','Printed pieces carrying the full name'),('sb','Printed pieces carrying SB'),('unmarked','Printed pieces with no owner engraving; use the matching bag code')]:engrave+=fig('printed-parts-'+n,c)
engrave+='</div></section>'
source=re.sub(r'<section id="engraving">.*?</section>',lambda _:engrave,source,flags=re.S)
ids='<section id="identify"><h2>Find the part before assembly</h2><p>E = Explorer, A = Architect, M = Main. Codes match the STL filenames. A code on an exterior part is concealed after assembly. Use labelled bags for pieces without physical codes.</p><div class="downloads"><a href="PART_LABELS.html">Printable sorting labels</a><a href="PARTS.csv">Parts CSV</a></div>'
for role in ['explorer','architect','main']:
    group=sorted([r for r in parts if r['role']==role],key=lambda r:r['assembly_code']);ids+=f'<h3 style="margin-top:35px">{role.title()} · {len(group)} pieces</h3><div class="parts-grid">'
    for r in group:
        ids+=f'<article class="part-card"><a href="prototype-stl/{e(r["file"])}"><img src="previews/part-thumbnails/{role}-{r["name"]}.png" loading="lazy" alt="{r["assembly_code"]}"><div class="part-code">{r["assembly_code"]}</div>{e(r["name"].replace("_"," "))}</a><small>{"Code on concealed/internal face" if r.get("id_location") else "Use coded bag / tray"}</small></article>'
    ids+='</div>'
ids+='</section>'
source=re.sub(r'<section id="identify">.*?</section>',lambda _:ids,source,flags=re.S)
printing='''<section id="printing"><h2>Material-separated layouts for UIC review</h2><p>The installed set is separated into <strong>88 opaque structural parts</strong> and <strong>7 translucent inserts</strong>. Print the fit samples first. Each provisional plate contains one selected material and colour, with allowances for brims and supports.</p><div class="grid"><article class="card"><h3>1 · Fit samples</h3><p>Rail, jaw and key; one lighting coupon with its matching bezel and diffuser. Check actual components and material before the full shells.</p></article><article class="card"><h3>2 · Opaque parts</h3><p>Bronze is the preferred look; UIC lists black as a stock option. Separate large shell jobs from trials, then fill compatible spare space with smaller parts.</p></article><article class="card"><h3>3 · Translucent inserts</h3><p>Three emblem diffusers plus four Main accents. Neutral translucent material can serve all seven; the LEDs provide their colours. No special purchased lenses are required if UIC can print them.</p></article><article class="card"><h3>4 · Provisional Voron layouts</h3><p>Layouts use the published 290 × 290 × 285 mm Voron volume. Staff must confirm usable exclusions, orientation and supports. The model-only 3MF files preserve separate parts and do not contain G-code.</p></article></div><div class="status">UIC publishes a 0.6 mm nozzle / 0.3 mm layers and recommends 0.5 mm horizontal / 1.0 mm vertical separation. Several current prototype fits are finer. Request a small-parts review and test coupons; do not submit the entire set as print-ready.</div><div class="downloads"><a href="print-preparation.html">Material batches &amp; orientation details</a><a href="PRINT_BRIEF.md">Printer settings and operator brief</a><a href="PRINT_MANIFEST.csv">Print manifest</a><a href="PRINT_PREP.json">Machine-readable plan</a><a href="arrange_plates.py">Plate-layout tool</a><a href="uic-voron-provisional/index.html">Provisional plate diagrams</a></div><p>UIC lists translucent PLA and says coursework is typically not billed, subject to their decision. If billed, the published PLA material rate is $30/kg. A whole clear PETG spool is roughly $24–30; the $9.95 Adafruit acrylic alternative is too thick for the current seats. Prices checked 31 October 2026; shipping and tax are additional where applicable. <a href="https://makerspace.uic.edu/make/digital-fabrication-lab/">UIC process</a> · <a href="https://makerspace.uic.edu/learn/billing/">UIC billing</a> · <a href="https://www.prusa3d.com/category/petg/">Prusa</a> · <a href="https://www.adafruit.com/product/4594">Adafruit</a></p></section>'''
source=source.replace('<footer>',printing+'<footer>',1)
source=source.replace('Revision 10 is preserved. Use the Revision 12 lid, matching light parts and current assembly map together.','Use the Revision 12 parts and current assembly map together.')
(R/'index.html').write_text(source,encoding='utf-8')
labels=(R.parent/'revision-11/PART_LABELS.html').read_text(encoding='utf-8').replace('Revision 11','Revision 12').replace('R11','R12')
(R/'PART_LABELS.html').write_text(labels,encoding='utf-8')

style=source.split('<style>')[1].split('</style>')[0]
page='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>R12 print preparation</title><style>'+style+'</style><main><a href="index.html">← Assembly guide</a><h1>One material.<br>One plate at a time.</h1><p class="status">These are material groups. Provisional Voron plates are linked below; final slicing and staff review remain pending. Rotation values are provisional XYZ degrees from assembly coordinates; all dimensions below are bounding boxes after that rotation.</p>'
for mat in ['OPAQUE','TRANSLUCENT']:
    group=sorted([r for r in prep['parts'] if r['material_group']==mat],key=lambda r:(r['stage'],r['role'],r['code']))
    page+=f'<h2>{mat.title()} · {len(group)} pieces</h2><div class="parts-grid">'
    for r in group:
        b=' × '.join(f'{x:.1f}' for x in r['print_bbox_xyz_mm'])
        page+=f'<article class="part-card"><img src="previews/part-thumbnails/{r["role"]}-{r["name"]}.png" loading="lazy" alt="{r["code"]}"><div class="part-code">{r["code"]}</div><strong>{e(r["name"].replace("_"," "))}</strong><p>{b} mm<br>Rotation: {r["rotation_xyz_deg"]}</p><small>{e(r["support_review"])}</small></article>'
    page+='</div>'
page+='<h2>Files for the operator</h2><p><a href="uic-voron-provisional/index.html">View provisional UIC Voron plates</a></p><div class="downloads"><a href="PRINT_BRIEF.md">Read the brief</a><a href="PRINT_MANIFEST.csv">Manifest</a><a href="PART_LABELS.html">Sorting labels</a><a href="PLANNER_CHECK.json">Planner verification</a></div><p>Material colour in these reference renders is illustrative. The seven optical inserts can all use neutral translucent PLA.</p></main></html>'
(R/'print-preparation.html').write_text(page,encoding='utf-8')
print('R12 guide, concealed-mark pictures and material-stage page created')
