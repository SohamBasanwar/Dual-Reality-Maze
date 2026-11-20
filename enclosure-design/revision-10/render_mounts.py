"""Inspection renders of actual CAD. Run with Blender; no imagined geometry."""
from pathlib import Path
src=Path(__file__).with_name('render_revision10.py').read_text(encoding='utf-8').split('for role in selection:')[0]
exec(compile(src,__file__,'exec'))
from bpy_extras.object_utils import world_to_camera_view
original=records[:]
annotations={}

def studio():
    s,m=setup();s.render.engine='BLENDER_WORKBENCH';s.view_settings.exposure=0;s.view_settings.view_transform='Standard'
    s.display.shading.light='STUDIO';s.display.shading.color_type='MATERIAL';s.display.shading.show_shadows=True;s.display.shading.show_cavity=True;s.display.shading.cavity_type='BOTH'
    s.display.shading.cavity_ridge_factor=1.3;s.display.shading.cavity_valley_factor=1.3
    s.display.shading.background_type='WORLD';s.world.color=(.055,.065,.08)
    m['bronze'].diffuse_color=(.52,.55,.58,1)
    for o in list(bpy.data.objects):
        if o.type=='MESH' and o.name.startswith('Plane'):bpy.data.objects.remove(o,do_unlink=True)
    return s,m

def frame(s, direction=(.65,.8,1),scale_factor=1.45):
    bpy.context.view_layer.update()
    pts=[o.matrix_world@Vector(p) for o in bpy.data.objects if o.type=='MESH' for p in o.bound_box]
    low=Vector(tuple(min(p[i] for p in pts) for i in range(3))); high=Vector(tuple(max(p[i] for p in pts) for i in range(3)))
    center=(low+high)/2;span=max(high-low)
    camera(s,center+Vector(direction).normalized()*.5,center,span*scale_factor)

exclude={'Base','Battery_Door','UNO_Edge_Clip_1','UNO_Edge_Clip_2','Breadboard_Envelope','UNO_PCB_Envelope','UNO_Header_Envelope','Battery_Envelope','Battery_Clip_Envelope','Power_Module_Reservation','ESP32_Optional_Envelope','ESP32_Wiring_Clearance','USB_Shutter','USB_Shutter_Keeper','USB_Plug_Clearance','Button_Wiring_Clearance'}
for role in ['explorer','architect','main']:
    for installed in [False,True]:
        records=[r for r in original if r['role']==role and r['name'] not in exclude and not r['name'].startswith(('I2C_','Breadboard_','UNO_')) and (installed or not r['component'])]
        s,m=studio();load(role,'all',m);frame(s,(.15,.3,-1),1.30)
        s.render.filepath=str(DEST/(role+'-lid-'+('installed' if installed else 'holders')+'.png'));bpy.ops.render.render(write_still=True)

groups={
'joystick-mount':('explorer',['Joystick_Carrier','Joystick_PCB','Joystick_Mechanism'],(.6,.7,-.8)),
'lcd-mount':('main',['LCD_Carrier','LCD_PCB_Envelope','LCD_Display_Envelope','LCD_Backpack_Envelope'],(.6,.8,-1)),
'servo-mount':('architect',['Servo_Cassette','Servo_Retainer','SG90_Body_Envelope'],(.65,.8,1)),
'button-linkage':('architect',['Button_Cap','Button_Stem_Guide','Button_Contact_Shoe','Tactile_Switch_Envelope'],(.6,.85,.25)),
'buzzer-mount':('main',['Buzzer_Keeper','Buzzer_Envelope'],(.6,.8,-1)),
'pot-mount':('architect',['Potentiometer_Keeper','Potentiometer_Envelope','Bronze_Knob_Envelope'],(.6,.8,-1)),
'ldr-open':('explorer',['Reveal_Dome','Bare_Light_Sensor'],(.6,.8,1))}
for name,(role,items,direction) in groups.items():
    records=[r for r in original if r['role']==role and r['name'] in items]
    s,m=studio();load(role,'all',m)
    # Include actual cropped fixed seats from fit-test meshes for optical/button views.
    sample='20-reveal-pod.stl' if name=='ldr-open' else None
    if sample:
        # Coupon files are normalized, so use a saved assembly-position crop instead.
        bpy.ops.wm.stl_import(filepath=str(R/'inspection-meshes'/'explorer-reveal-seat.stl'))
        ob=bpy.context.object;ob.name='explorer isolated opaque seat';ob.scale=(.001,)*3;ob.location=(-.123,-.1035,0);ob.data.materials.append(m['bronze'])
        bpy.data.objects['explorer Reveal_Dome'].location.z+=.018
    if name=='button-linkage':
        bpy.ops.mesh.primitive_cube_add(size=1,location=((246-197-123)*.001,(95-103.5)*.001,.0142))
        ob=bpy.context.object;ob.name='Breadboard slice - nonprinted reference';ob.dimensions=(.028,.028,.010);ob.data.materials.append(m['breadboard'])
    if name in ['buzzer-mount','pot-mount']:
        bpy.ops.wm.stl_import(filepath=str(R/'inspection-meshes'/(name+'-seat.stl')))
        ob=bpy.context.object;ob.scale=(.001,)*3;ob.location=(-(117 if role=='main' else 123)*.001,-(90 if role=='main' else 103.5)*.001,0);ob.data.materials.append(m['bronze'])
    frame(s,direction,1.65)
    s.render.filepath=str(DEST/(name+'.png'));bpy.ops.render.render(write_still=True)
    annotations[name]=[]
    bpy.context.view_layer.update()
    for ob in bpy.data.objects:
        if ob.type!='MESH':continue
        center=sum((ob.matrix_world@Vector(p) for p in ob.bound_box),Vector())/8
        p=world_to_camera_view(s,s.camera,center)
        annotations[name].append({'label':ob.name,'point':[p.x*1600,(1-p.y)*1200]})
(R/'inspection-annotations.json').write_text(json.dumps(annotations,indent=2))
print('Mounting inspection views rendered')
