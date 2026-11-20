import FreeCAD as A
import json
from pathlib import Path
R=Path(__file__).resolve().parent
reports=[]
for role in ['explorer','architect','main']:
    if not (R/'cad'/f'{role}-revision07.FCStd').exists():continue
    d=A.openDocument(str(R/'cad'/f'{role}-revision07.FCStd'))
    parts=d.getObject('PrintedParts').Group
    overlaps=[]
    for i,a in enumerate(parts):
        for b in parts[i+1:]:
            # Bounding-box reject before expensive solid intersection.
            if not a.Shape.BoundBox.intersect(b.Shape.BoundBox):continue
            v=a.Shape.common(b.Shape).Volume
            if v>.05:overlaps.append({'a':a.Name,'b':b.Name,'volume_mm3':round(v,3)})
    # Rotary gate and stock horn against every fixed printed part.
    motion=[]
    if role=='architect':
        for angle in range(0,111,5):
            for moving in ['Original_Horn_Envelope','Gate_Rotor']:
                q=d.getObject(moving).Shape.copy()
                q.rotate(A.Vector(50,32,58),A.Vector(0,0,1),-angle)
                for fixed in parts:
                    if fixed.Name=='Gate_Rotor':continue
                    if not q.BoundBox.intersect(fixed.Shape.BoundBox):continue
                    v=q.common(fixed.Shape).Volume
                    if v>.05:motion.append({'angle_deg':angle,'moving':moving,'fixed':fixed.Name,'volume_mm3':round(v,3)})
    shutter=[]
    if role=='main':
        for travel in range(36):
            s=d.getObject('USB_Shutter').Shape.copy();s.translate(A.Vector(-travel,0,0))
            for fixed in ['Base','Lid','USB_Shutter_Keeper']:
                v=s.common(d.getObject(fixed).Shape).Volume
                if v>.05:shutter.append({'travel_mm':travel,'fixed':fixed,'volume_mm3':round(v,3)})
    ports=[('I2C_Left',A.Vector(0,-1,0)),('I2C_Right',A.Vector(0,1,0))] if role=='main' else [('I2C_Rear',A.Vector(-1,0,0))]
    for name,direction in ports:
        for travel in range(22):
            s=d.getObject(name+'_Shutter').Shape.copy();s.translate(direction*travel)
            for fixed in ['Base','Lid',name+'_Keeper']:
                v=s.common(d.getObject(fixed).Shape).Volume
                if v>.05:shutter.append({'port':name,'travel_mm':travel,'fixed':fixed,'volume_mm3':round(v,3)})
    optical=[]
    if role=='explorer':
        for angle in range(0,91,5):
            hood=d.getObject('Reveal_Dome').Shape.copy();hood.rotate(A.Vector(123,117,58),A.Vector(0,0,1),angle)
            for fixed in ['Lid','Bare_Light_Sensor']:
                v=hood.common(d.getObject(fixed).Shape).Volume
                if v>.05:optical.append({'angle_deg':angle,'fixed':fixed,'volume_mm3':round(v,3)})
    fits=[]
    for n in ['Breadboard_Envelope','Battery_Envelope','UNO_PCB_Envelope','ESP32_Optional_Envelope','ESP32_Wiring_Clearance','USB_Plug_Clearance','RGB_LED_Envelope','Joystick_PCB','Joystick_Mechanism','Potentiometer_Envelope','Tactile_Switch_Envelope','LCD_PCB_Envelope','LCD_Display_Envelope','LCD_Backpack_Envelope','Buzzer_Envelope','Bare_Light_Sensor','SG90_Body_Envelope']:
        o=d.getObject(n)
        if not o:continue
        conflicts=[]
        for p in parts:
            v=o.Shape.common(p.Shape).Volume
            if v>.05:conflicts.append({'part':p.Name,'volume_mm3':round(v,3)})
        fits.append({'reference_volume':n,'conflicts':conflicts})
    report={'role':role,'printed_part_intersections':overlaps,'gate_rotation_intersections':motion,'shutter_travel_intersections':shutter,'reveal_hood_rotation_intersections':optical,'reserved_volume_checks':fits,'physical_fit_verified':False,'optical_test_performed':False}
    print(json.dumps(report),flush=True);reports.append(report);A.closeDocument(d.Name)
(R/'ASSEMBLY_REVIEW.json').write_text(json.dumps(reports,indent=2))
