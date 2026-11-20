import FreeCAD as A
import json,sys,Part
from pathlib import Path
R=Path(__file__).resolve().parent
selected=sys.argv[1:] or ['explorer','architect','main']
reports=[r for r in json.loads((R/'ASSEMBLY_REVIEW.json').read_text()) if r['role'] not in selected] if (R/'ASSEMBLY_REVIEW.json').exists() else []
for role in selected:
    if not (R/'cad'/f'{role}-revision10.FCStd').exists():continue
    d=A.openDocument(str(R/'cad'/f'{role}-revision10.FCStd'))
    parts=d.getObject('PrintedParts').Group
    motion_cache={}
    def motion_common(q,name,kind):
        key=(name,kind)
        if key not in motion_cache:
            b=q.BoundBox;xy,z=(40,20) if kind=='gate' else (40,1) if kind.startswith('port') else (12,18) if kind=='optical' else (1,1)
            region=Part.makeBox(b.XLength+2*xy,b.YLength+2*xy,b.ZLength+2*z,A.Vector(b.XMin-xy,b.YMin-xy,b.ZMin-z))
            motion_cache[key]=(region.BoundBox,d.getObject(name).Shape.common(region))
        b,local=motion_cache[key];a=q.BoundBox
        if not (b.XMin<=a.XMin and b.YMin<=a.YMin and b.ZMin<=a.ZMin and b.XMax>=a.XMax and b.YMax>=a.YMax and b.ZMax>=a.ZMax):
            local=d.getObject(name).Shape
        return q.common(local).Volume if local.Solids and q.BoundBox.intersect(local.BoundBox) else 0
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
            for fixed in ['Gate_Frame','Gate_Shroud','Servo_Cassette','Servo_Retainer','Lid']:
                v=motion_common(moved,fixed,'gate')
                if v>.05:motion.append({'angle_deg':angle,'fixed':fixed,'volume_mm3':round(v,3)})
            for moving in ['Original_Horn_Envelope','Gate_Drive_Pin','Gate_Pin_Keeper']:
                q=d.getObject(moving).Shape.copy()
                q.rotate(A.Vector(61,60,55),A.Vector(0,1,0),angle+60)
                for fixed in ['Gate_Frame','Gate_Shroud','Servo_Cassette','Servo_Retainer','Lid']:
                    v=motion_common(q,fixed,'gate')
                    if v>.05:motion.append({'angle_deg':angle,'moving':moving,'fixed':fixed,'volume_mm3':round(v,3)})
                v=q.common(moved).Volume
                if v>.05:motion.append({'angle_deg':angle,'moving':moving,'fixed':'moving gate panel','volume_mm3':round(v,3)})
    shutter=[]
    if role=='main':
        for travel in range(36):
            s=d.getObject('USB_Shutter').Shape.copy();s.translate(A.Vector(-travel,0,0))
            for fixed in ['Base','Lid','USB_Shutter_Keeper']:
                v=motion_common(s,fixed,'portUSB')
                if v>.05:shutter.append({'travel_mm':travel,'fixed':fixed,'volume_mm3':round(v,3)})
    ports=[('I2C_Left',A.Vector(0,-1,0)),('I2C_Right',A.Vector(0,1,0))] if role=='main' else [('I2C_Rear',A.Vector(-1,0,0))]
    for name,direction in ports:
        for travel in range(22):
            s=d.getObject(name+'_Shutter').Shape.copy();s.translate(direction*travel)
            for fixed in ['Base','Lid',name+'_Keeper']:
                v=motion_common(s,fixed,'port'+name)
                if v>.05:shutter.append({'port':name,'travel_mm':travel,'fixed':fixed,'volume_mm3':round(v,3)})
    optical=[]
    if role=='explorer':
        for angle in range(0,91,5):
            hood=d.getObject('Reveal_Dome').Shape.copy();hood.rotate(A.Vector(123,117,58),A.Vector(0,0,1),angle)
            for fixed in ['Lid','Bare_Light_Sensor']:
                v=motion_common(hood,fixed,'optical')
                if v>.05:optical.append({'angle_deg':angle,'fixed':fixed,'volume_mm3':round(v,3)})
        # At the entry-slot angle the hood must also lift off, not merely rotate.
        for dz in range(1,16):
            hood=d.Reveal_Dome.Shape.copy();hood.rotate(A.Vector(123,117,58),A.Vector(0,0,1),90);hood.translate(A.Vector(0,0,dz))
            for fixed in ['Lid','Bare_Light_Sensor']:
                v=motion_common(hood,fixed,'optical')
                if v>.05:optical.append({'lift_mm':dz,'fixed':fixed,'volume_mm3':round(v,3)})
    button=[]
    if role=='architect':
        for i in range(10):
            stroke=i*.05
            q=d.Button_Cap.Shape.fuse(d.Button_Contact_Shoe.Shape);q.translate(A.Vector(0,0,-stroke))
            for fixed in ['Button_Stem_Guide','Lid','Base','Breadboard_Envelope']:
                v=motion_common(q,fixed,'button')
                if v>.05:button.append({'stroke_mm':stroke,'fixed':fixed,'volume_mm3':round(v,3)})
    fits=[]
    for n in ['Breadboard_Envelope','Battery_Envelope','Battery_Clip_Envelope','Power_Module_Reservation','UNO_PCB_Envelope','UNO_Header_Envelope','ESP32_Optional_Envelope','ESP32_Wiring_Clearance','USB_Plug_Clearance','RGB_LED_Envelope','Joystick_PCB','Joystick_Mechanism','Potentiometer_Envelope','Tactile_Switch_Envelope','Button_Wiring_Clearance','LCD_PCB_Envelope','LCD_Display_Envelope','LCD_Backpack_Envelope','Buzzer_Envelope','Bare_Light_Sensor','SG90_Body_Envelope']:
        o=d.getObject(n)
        if not o:continue
        conflicts=[]
        for p in parts:
            if not o.Shape.BoundBox.intersect(p.Shape.BoundBox):continue
            v=o.Shape.common(p.Shape).Volume
            if v>.05:conflicts.append({'part':p.Name,'volume_mm3':round(v,3)})
        fits.append({'reference_volume':n,'conflicts':conflicts})
    report={'role':role,'printed_part_intersections':overlaps,'gate_slider_intersections':motion,'shutter_travel_intersections':shutter,'reveal_hood_rotation_and_removal_intersections':optical,'button_stroke_intersections':button,'reserved_volume_checks':fits,'physical_fit_verified':False,'optical_test_performed':False}
    print(json.dumps(report),flush=True);reports.append(report);A.closeDocument(d.Name)
(R/'ASSEMBLY_REVIEW.json').write_text(json.dumps(reports,indent=2))

