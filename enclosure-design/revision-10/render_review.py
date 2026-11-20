"""Visual guide from exported R10 solids. No concept images or invented hardware."""
from pathlib import Path
src=Path(__file__).with_name('render_revision10.py').read_text(encoding='utf-8').split('for role in selection:')[0]
exec(compile(src,__file__,'exec'))
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Matrix
original=records[:]
requested=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
roles=[a.split('=',1)[1] for a in requested if a.startswith('role=')] or ['explorer','architect','main']
base_names={'Base','Battery_Door','Breadboard_Envelope','UNO_PCB_Envelope','UNO_Header_Envelope','Battery_Envelope','Battery_Clip_Envelope','Power_Module_Reservation','ESP32_Optional_Envelope','ESP32_Wiring_Clearance','USB_Shutter','USB_Shutter_Keeper','USB_Plug_Clearance','Tactile_Switch_Envelope','Button_Wiring_Clearance'}
def isbase(r):
    return r['name'] in base_names or r['name'].startswith(('Breadboard_','UNO_','I2C_'))
def studio():
    s,m=setup();s.render.engine='BLENDER_WORKBENCH';s.view_settings.exposure=0;s.view_settings.view_transform='Standard'
    sh=s.display.shading;sh.light='STUDIO';sh.color_type='MATERIAL';sh.show_shadows=True;sh.show_cavity=True;sh.cavity_type='BOTH'
    sh.cavity_ridge_factor=1.4;sh.cavity_valley_factor=1.3;sh.background_type='WORLD';s.world.color=(.055,.065,.08)
    m['bronze'].diffuse_color=(.46,.30,.16,1)
    for o in list(bpy.data.objects):
        if o.type=='MESH' and o.name.startswith('Plane'):bpy.data.objects.remove(o,do_unlink=True)
    s.render.resolution_x=1600;s.render.resolution_y=1100
    return s,m
def frame(s,direction=(.45,.7,1),padding=.87,pts=None):
    bpy.context.view_layer.update()
    pts=pts or [o.matrix_world@Vector(p) for o in bpy.data.objects if o.type=='MESH' and not o.hide_render for p in o.bound_box]
    lo=Vector(tuple(min(p[i] for p in pts) for i in range(3)));hi=Vector(tuple(max(p[i] for p in pts) for i in range(3)));c=(lo+hi)/2
    camera(s,c+Vector(direction).normalized()*.6,c,max(hi-lo)*1.2)
    bpy.context.view_layer.update();pp=[world_to_camera_view(s,s.camera,p) for p in pts]
    s.camera.data.ortho_scale*=max(2*max(abs(p.x-.5) for p in pp)/padding,2*max(abs(p.y-.5) for p in pp)/padding)
def save(s,name):
    s.render.filepath=str(DEST/(name+'.png'));bpy.ops.render.render(write_still=True)
def extra_mesh(path,role,m,name):
    bpy.ops.wm.stl_import(filepath=str(path));o=bpy.context.object;o.name=name;o.scale=(.001,)*3
    o.location=(-(117 if role=='main' else 123)*.001,-(90 if role=='main' else 103.5)*.001,0);o.data.materials.append(m['bronze']);return o

if not requested or 'cases' in requested:
    for role in roles:
        for mode in ['closed','open','base','lid','battery-closed','battery-open','cables-closed','cables-open']:
            records=[r for r in original if r['role']==role]
            if mode=='base':records=[r for r in records if isbase(r)]
            if mode=='lid':records=[r for r in records if not isbase(r)]
            s,m=studio();load(role,'assembled' if mode in ['closed','battery-closed','battery-open','cables-closed','cables-open'] else 'all',m)
            direction=(.45,.75,1)
            if mode=='open':
                for r in records:
                    if not isbase(r):
                        o=bpy.data.objects.get(role+' '+r['name'])
                        if o:o.location.x+=.275;o.location.z+=.035
                direction=(.15,.6,1.3)
            if mode=='base':direction=(.1,.25,1.5)
            if mode=='lid':direction=(.2,.3,-1)
            if mode.startswith('battery'):
                direction=(.35,.5,-1)
                if mode.endswith('open'):bpy.data.objects[role+' Battery_Door'].location.z-=.026
            if mode.startswith('cables'):
                direction=(-.4,-1,.5)
                if mode.endswith('open'):
                    for n,v in ([('I2C_Left_Shutter',(0,-.021,0)),('I2C_Right_Shutter',(0,.021,0)),('USB_Shutter',(-.035,0,0))] if role=='main' else [('I2C_Rear_Shutter',(-.021,0,0))]):
                        bpy.data.objects[role+' '+n].location+=Vector(v)
            frame(s,direction);save(s,role+'-'+mode)

if not requested or 'adjustments' in requested:
    for role in roles:
        for item in json.loads((R/(role+'-adjustments.json')).read_text()):
            prefix=item['prefix'];names=[prefix+'_'+q for q in ['X_Jaw','X_Lock_Key','Y_Jaw','Y_Lock_Key','Height_Insert']]
            carrier=prefix+'_Carrier'
            for stage in ['nominal','minus','plus','unlocked','height']:
                records=[r for r in original if r['role']==role and r['name'] in names+[carrier]]
                s,m=studio();m['bronze'].diffuse_color=(.56,.58,.61,1);load(role,'all',m)
                if prefix in ['UNO','Breadboard']:extra_mesh(R/'inspection-meshes'/(role+'-'+prefix+'-fixed.stl'),role,m,'Fixed rail frame')
                for axis in item['axes']:
                    dv=max(axis['range_mm']) if stage=='plus' else min(axis['range_mm']) if stage=='minus' else 0
                    # Exported coordinates mirror X. + is larger pocket size.
                    dr=Vector((-axis['direction'][0],axis['direction'][1],0))
                    for name in [axis['jaw'],axis['key']]:bpy.data.objects[role+' '+name].location-=dr*dv*.001
                    if stage=='unlocked':
                        dr=axis.get('key_release_pre',[0,-1,0] if axis['axis']=='X' else [1,0,0])
                        kd=Vector((-dr[0],dr[1],dr[2]))
                        bpy.data.objects[role+' '+axis['key']].location+=kd*(axis.get('key_release_mm',10.5)*.001)
                if stage=='height':bpy.data.objects[role+' '+prefix+'_Height_Insert'].location.z+=.016
                frame(s,(.2,-.4,1.4));save(s,role+'-'+prefix.lower()+'-'+stage)
            # Tight rail view shows the real engraved +/- arrows and key.
            records=[r for r in original if r['role']==role and r['name'] in [prefix+'_X_Jaw',prefix+'_X_Lock_Key']]
            s,m=studio();m['bronze'].diffuse_color=(.64,.65,.66,1);load(role,'all',m)
            extra_mesh(R/'inspection-meshes'/(role+'-'+prefix+'-rail-detail.stl'),role,m,'Rail with recessed direction symbols')
            frame(s,(-.3,-.4,1.4));save(s,role+'-'+prefix.lower()+'-arrows')

if not requested or 'gate' in requested:
    sequence={
      '01-servo':(['Servo_Cassette','Servo_Fit_Insert','SG90_Body_Envelope','Servo_Retainer'],{'Servo_Fit_Insert':(0,0,.012),'SG90_Body_Envelope':(0,0,.030),'Servo_Retainer':(0,0,.049)}),
      '02-horn':(['Servo_Cassette','Servo_Fit_Insert','SG90_Body_Envelope','Servo_Retainer','Original_Horn_Envelope'],{'Original_Horn_Envelope':(0,.018,0)}),
      '03-frame-panel':(['Servo_Cassette','Servo_Fit_Insert','SG90_Body_Envelope','Servo_Retainer','Original_Horn_Envelope','Gate_Frame','Gate_Panel'],{'Gate_Panel':(0,0,.040)}),
      '04-pin':(['Gate_Frame','Gate_Panel','Original_Horn_Envelope','Gate_Drive_Pin','Gate_Pin_Keeper'],{'Gate_Drive_Pin':(0,.020,0),'Gate_Pin_Keeper':(0,-.018,0)}),
      '05-guard':(['Servo_Cassette','Servo_Fit_Insert','SG90_Body_Envelope','Servo_Retainer','Original_Horn_Envelope','Gate_Frame','Gate_Panel','Gate_Drive_Pin','Gate_Pin_Keeper','Gate_Shroud'],{'Gate_Shroud':(0,0,.035)}),
      '06-closed':(['Servo_Cassette','Servo_Fit_Insert','SG90_Body_Envelope','Servo_Retainer','Original_Horn_Envelope','Gate_Frame','Gate_Panel','Gate_Drive_Pin','Gate_Pin_Keeper','Gate_Shroud'],{}),
      '07-open':(['Servo_Cassette','Servo_Fit_Insert','SG90_Body_Envelope','Servo_Retainer','Original_Horn_Envelope','Gate_Frame','Gate_Panel','Gate_Drive_Pin','Gate_Pin_Keeper','Gate_Shroud'],{})}
    for stage,(names,moves) in sequence.items():
        records=[r for r in original if r['role']=='architect' and r['name'] in names]
        s,m=studio();load('architect','all',m)
        for name,v in moves.items():bpy.data.objects['architect '+name].location+=Vector(v)
        if stage=='07-open':
            bpy.data.objects['architect Gate_Panel'].location.z+=.01212436
            bpy.context.view_layer.update()
            pivot=Vector((-.062,-.0435,.055))
            for n in ['Original_Horn_Envelope','Gate_Drive_Pin','Gate_Pin_Keeper']:
                o=bpy.data.objects['architect '+n];o.matrix_world=Matrix.Translation(pivot)@Matrix.Rotation(math.radians(120),4,'Y')@Matrix.Translation(-pivot)@o.matrix_world
        frame(s,(.3,1,.6));save(s,'gate-'+stage)
print('R10 visual guide render pass complete')
