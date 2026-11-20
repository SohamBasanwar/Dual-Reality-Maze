import FreeCAD as A
import json
from pathlib import Path
R=Path(__file__).resolve().parent
reports=[]
for role in ['explorer','architect','main']:
    d=A.openDocument(str(R/'cad'/f'{role}-revision05.FCStd'))
    parts=d.getObject('PrintedParts').Group
    overlaps=[]
    for i,a in enumerate(parts):
        for b in parts[i+1:]:
            # Bounding-box reject before expensive solid intersection.
            if not a.Shape.BoundBox.intersect(b.Shape.BoundBox):continue
            v=a.Shape.common(b.Shape).Volume
            if v>.05:overlaps.append({'a':a.Name,'b':b.Name,'volume_mm3':round(v,3)})
    # Check the moving gate against frame and guard at 5 degree increments.
    motion=[]
    if role=='architect':
        gate=d.getObject('Gate_Panel').Shape
        for angle in range(-60,61,5):
            import math
            lift=7*(math.sin(math.radians(angle))+math.sin(math.pi/3))
            moved=gate.copy();moved.translate(A.Vector(0,0,lift))
            for fixed in ['Gate_Frame','Gate_Shroud']:
                v=moved.common(d.getObject(fixed).Shape).Volume
                if v>.05:motion.append({'angle_deg':angle,'fixed':fixed,'volume_mm3':round(v,3)})
    shutter=[]
    if role=='main':
        for travel in range(36):
            s=d.getObject('USB_Shutter').Shape.copy();s.translate(A.Vector(-travel,0,0))
            for fixed in ['Base','Lid','USB_Shutter_Keeper']:
                v=s.common(d.getObject(fixed).Shape).Volume
                if v>.05:shutter.append({'travel_mm':travel,'fixed':fixed,'volume_mm3':round(v,3)})
    fits=[]
    for n in ['Breadboard_Envelope','Battery_Envelope','UNO_PCB_Envelope','ESP32_Optional_Envelope','ESP32_Wiring_Clearance','USB_Plug_Clearance','RGB_LED_Envelope','Joystick_PCB','Joystick_Mechanism','Potentiometer_Envelope','Tactile_Switch_Envelope','LCD_PCB_Envelope','LCD_Display_Envelope','LCD_Backpack_Envelope','Buzzer_Envelope','Bare_Light_Sensor','SG90_Body_Envelope']:
        o=d.getObject(n)
        if not o:continue
        conflicts=[]
        for p in parts:
            v=o.Shape.common(p.Shape).Volume
            if v>.05:conflicts.append({'part':p.Name,'volume_mm3':round(v,3)})
        fits.append({'reference_volume':n,'conflicts':conflicts})
    report={'role':role,'printed_part_intersections':overlaps,'gate_slider_intersections':motion,'shutter_travel_intersections':shutter,'reserved_volume_checks':fits,'physical_fit_verified':False}
    print(json.dumps(report),flush=True);reports.append(report);A.closeDocument(d.Name)
(R/'ASSEMBLY_REVIEW.json').write_text(json.dumps(reports,indent=2))
