from pathlib import Path
import csv,json
R=Path(__file__).resolve().parent
parts=[r for r in json.loads((R/'scene.json').read_text()) if not r['component']]
def plan(n):
    if n=='Base':return ('Opening upward; centre underside on bed','Selective supports under rounded grips, latch undercuts and rear/side shutter overhangs','Block support in blind shutter tracks and small sockets; verify extraction path.')
    if n=='Lid':return ('Exterior upward; support open underside as needed','Selective supports under roof spans and hanging holders','Paint supports; keep supports off snap engagement faces, lead bores and optical seat. Test crop first.')
    if n=='Battery_Door':return ('Inspect curved inside face; orient to keep latch bending within layers','Local supports may be needed under contoured skin/tabs','Keep supports away from grip-facing skin and catch root. Use actual grip coupon.')
    if n in ['Gate_Panel','Gate_Pin_Keeper']:return ('Broad planar face on bed','Usually none in this orientation','Check yoke slot / C opening in layer preview; do not let brim close the working slot.')
    if n=='Gate_Drive_Pin':return ('Head on bed, pin axis upward','Usually none; inspect groove bridging','Tiny groove and keeper are fit-critical. Consider a measured nylon push-rivet if FDM feature fails.')
    if n=='Gate_Shroud':return ('Upright from lower rim','Selective supports under arch and cap','Keep front opening, guide pocket and release hooks accessible after support removal.')
    if n in ['Gate_Frame','Servo_Cassette']:return ('Foundation downward, mechanism upright','Inspect local bridges and snap-foot undercuts','Do not support inside closed guide tracks. Fit as a standalone gate assembly first.')
    if n=='Servo_Retainer':return ('Rotate bridge broad top face onto bed, legs upward','Usually none; inspect small hook ledges','Keep bending beams continuous and not loaded across weak layer seams. Test the actual material.')
    if n=='Button_Cap':return ('Button face on bed, long stem upward','Inspect flange underside; brim may help stability','Protect the visible top and SB. Check stem straightness; do not leave support scars in guide contact area.')
    if n=='Button_Stem_Guide':return ('Side orientation or large stop-ring face on bed; compare in slicer','Selective support at two rings / connecting bars','Use crop test. Clear 5.7 mm guide bore and latch pockets without enlarging the mating model.')
    if n in ['Joystick_Carrier','LCD_Carrier','Switch_Cassette']:return ('Largest frame face down; orient clip beams for flex','Local supports beneath retention lips if bridging fails','Preserve PCB ledges, clip roots and carrier receiver fit; actual module test required.')
    if n=='Reveal_Dome':return ('Open rim down','Inspect dome interior; avoid trapped supports under optical membrane','Prefer tested orientation with accessible support removal. Thin optical roof must be continuous.')
    if n in ['Emblem_Diffuser','Emblem_Mask']:return ('Broad flat face on bed','Usually none; small mask tabs may need local support','Diffuser is translucent optical material or a cut sheet; opaque structural filament cannot diffuse light.')
    if 'Shutter' in n:return ('Plate broad face down with finger tab upward','Usually none; inspect plate edge / keeper feature','No support or elephant-foot swelling on running surfaces; do not scale part to fix it.')
    if 'Keeper' in n or 'Clip' in n:return ('Broadest stable face down; orient flex in layer plane where possible','Usually none, inspect each hook','Keep fit surfaces and small openings clean. Test retention and removal before full build.')
    return ('Inspect broad stable face in slicer','Part-dependent','Prototype coupon first.')
with (R/'PRINT_PLAN.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f);w.writerow(['Assembly','Printed part','Quantity','STL','Suggested starting orientation','Support expectation','Fit / removal note'])
    for r in parts:w.writerow([r['role'],r['name'],1,r['file'],*plan(r['name'])])
print('Print plan:',len(parts),'assembly parts. Test crops and optical alternatives listed separately.')
