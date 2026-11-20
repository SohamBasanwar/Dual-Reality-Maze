"""Render the actual exported CAD meshes; no generated concept illustration."""
import bpy, json, math, sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
records=json.loads((R/'scene.json').read_text())
DEST=R/'previews';DEST.mkdir(exist_ok=True)
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
selection=args or ['family','explorer','architect','main']
finish='charcoal'
for a in list(selection):
    if a.startswith('finish='):finish=a.split('=',1)[1];selection.remove(a)
colours={'charcoal':(.09,.105,.12),'stone':(.33,.35,.35),'forest':(.055,.13,.095),'bronze':(.29,.135,.045)}

def mat(name,color,metal=0,rough=.4,emission=0):
    m=bpy.data.materials.new(name);m.use_nodes=True;m.diffuse_color=(*color,1)
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
    if emission:p.inputs['Emission Color'].default_value=(*color,1);p.inputs['Emission Strength'].default_value=emission
    return m

def setup():
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=12
    scene.cycles.use_denoising=True
    scene.render.resolution_x=1600;scene.render.resolution_y=1200;scene.render.resolution_percentage=100
    scene.world.color=(.12,.12,.12)
    scene.view_settings.view_transform='AgX';scene.view_settings.exposure=-1.7
    mats={
      'bronze':mat('Single-colour structural polymer',colours[finish],.12,.38),
      'pcb':mat('PCB reference',(.02,.12,.20),.15,.5),
      'black':mat('Black component reference',(.018,.021,.026),0,.48),
      'white':mat('Original nylon horn reference',(.8,.8,.74),0,.5),
      'breadboard':mat('Breadboard reference',(.74,.73,.65),0,.5),
      'battery':mat('PP3 reference',(.28,.29,.3),.45,.35),
      'metal':mat('Shaft reference',(.48,.51,.55),.7,.23),
      'knob':mat('Bronze knob',(.48,.23,.07),.65,.27),
      'sensor':mat('Bare LDR',(.38,.2,.09),0,.6),
      'clear_window':mat('Thin clear sensor window',(.3,.6,.67),0,.15),
      'servo':mat('SG90 reference',(.015,.04,.35),.1,.3),
      'reservation':mat('Unselected power-module reservation',(.53,.21,.035),0,.6),
      'optional':mat('Optional ESP32 space',(.05,.42,.33),0,.55),
      'clearance':mat('Reserved access space',(.20,.28,.6),0,.65),
      'lcd':mat('LCD viewing area',(.055,.2,.065),0,.3)}
    for r,c in [('explorer',(.04,.35,.9)),('architect',(.9,.4,.04)),('main',(.34,.08,.75))]:mats[r]=mat(r+' diffuser',c,0,.35,.5)
    ground=mat('Studio floor',(.025,.031,.04),0,.55)
    bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.003));bpy.context.object.data.materials.append(ground)
    for loc,energy,size in [((.35,.1,.9),18,.6),((-.4,.4,.5),9,.55),((.1,-.6,.7),22,.4)]:
        bpy.ops.object.light_add(type='AREA',location=loc);obj=bpy.context.object;obj.data.energy=energy;obj.data.shape='DISK';obj.data.size=size
        obj.rotation_euler=(Vector((0,0,.04))-obj.location).to_track_quat('-Z','Y').to_euler()
    bpy.ops.object.camera_add(location=(.36,.44,.38));scene.camera=bpy.context.object;scene.camera.data.type='ORTHO';scene.camera.data.ortho_scale=.36;scene.camera.data.clip_start=.001;scene.camera.data.clip_end=10
    return scene,mats

def load(role,mode,mats,dx=0):
    W=234 if role=='main' else 246;D=180 if role=='main' else 207
    for r in records:
        if r['role']!=role:continue
        if mode=='internal' and r['name'] not in ['Base','Battery_Door','Breadboard_Envelope','UNO_PCB_Envelope','UNO_Header_Envelope','Battery_Envelope','Battery_Clip_Envelope','Power_Module_Reservation','ESP32_Optional_Envelope','ESP32_Wiring_Clearance','USB_Shutter','USB_Shutter_Keeper','UNO_Edge_Clip_1','UNO_Edge_Clip_2'] and not r['name'].startswith('I2C_'):continue
        if mode=='assembled' and r['component'] and r['name'] not in ['Joystick_Mechanism','Bronze_Knob_Envelope','LCD_Display_Envelope','Bare_Light_Sensor','LDR_Clear_Window']:continue
        bpy.ops.wm.stl_import(filepath=str(R/'render-meshes'/r['file']))
        obj=bpy.context.object;obj.name=role+' '+r['name'];obj.scale=(.001,)*3
        bpy.ops.object.shade_smooth_by_angle(angle=.50)
        e=r['explosion'] if mode=='exploded' and not r['component'] else [0,0,0]
        obj.location=((e[0]-W/2)*.001+dx,(e[1]-D/2)*.001,e[2]*.001)
        obj.data.materials.append(mats[role if r['material']=='diffuser' else r['material']])
        # Render exact CAD mesh with no modifier that can obscure seam geometry.

def camera(scene,loc,target,scale):
    scene.camera.location=loc;scene.camera.rotation_euler=(Vector(target)-scene.camera.location).to_track_quat('-Z','Y').to_euler();scene.camera.data.ortho_scale=scale

for role in selection:
    one_mode=None
    if ':' in role:role,one_mode=role.split(':',1)
    if role=='family':
        s,m=setup()
        for r,x in [('explorer',.29),('architect',0),('main',-.29)]:load(r,'assembled',m,x)
        s.render.resolution_x=2000;s.render.resolution_y=1000
        camera(s,(.0,.8,.64),(0,0,.04),.91)
        s.render.filepath=str(DEST/f'family-{finish}.png');bpy.ops.render.render(write_still=True)
    else:
        for mode in ([one_mode] if one_mode else ['assembled','internal','exploded','top','front','side','battery-door']):
            s,m=setup();load(role,'exploded' if mode=='exploded' else 'internal' if mode=='internal' else 'assembled',m)
            if mode not in ['assembled','shutter-closed','shutter-open','rear-open','rear-closed','side-open','side-closed']:
                s.render.engine='BLENDER_WORKBENCH'
                s.view_settings.exposure=0;s.view_settings.view_transform='Standard'
                s.display.shading.light='STUDIO';s.display.shading.color_type='MATERIAL'
                s.display.shading.show_shadows=True;s.display.shading.show_cavity=True;s.display.shading.cavity_type='BOTH'
                s.display.shading.background_type='WORLD';s.world.color=(.045,.055,.07)
            if mode in ['rear-open','rear-closed']:
                camera(s,(-.14,-.4,.18),(0,-.05,.027),.30)
                if mode=='rear-open':
                    ob=bpy.data.objects.get(role+' I2C_Rear_Shutter')
                    if ob:ob.location.x-=.021
            elif mode in ['side-open','side-closed']:
                camera(s,(.42,.24,.23),(.05,.01,.028),.29)
                if mode=='side-open':
                    for name,dy in [('I2C_Left_Shutter',-.021),('I2C_Right_Shutter',.021)]:
                        ob=bpy.data.objects.get(role+' '+name)
                        if ob:ob.location.y+=dy
            elif mode in ['shutter-closed','shutter-open']:
                camera(s,(-.16,-.42,.17),(0,-.055,.028),.295)
                if mode=='shutter-open':
                    ob=bpy.data.objects.get(role+' USB_Shutter')
                    if ob:ob.location.x-=.035
            elif mode in ['internal','top']:
                camera(s,(0,0,.6),(0,0,0),.285)
                s.camera.rotation_euler.rotate_axis('Z',math.pi)
            elif mode=='front':camera(s,(0,.6,.055),(0,0,.055),.285)
            elif mode=='side':camera(s,(.6,0,.055),(0,0,.055),.285)
            elif mode=='exploded':camera(s,(.36,.44,.38),(0,0,.055),.365)
            elif mode=='battery-door':
                # Underside rendered without a floor, so door seams and thumb catch are visible.
                bpy.data.objects.remove(next(o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('Plane')),do_unlink=True)
                camera(s,(.22,.3,-.4),(0,0,.025),.30)
                for o in bpy.data.objects:
                    if o.type=='LIGHT':o.location.z=-abs(o.location.z);o.rotation_euler=(Vector((0,0,0))-o.location).to_track_quat('-Z','Y').to_euler()
            else:camera(s,(.36,.44,.38),(0,0,.05 if role=='architect' else .035),.38 if role=='architect' else .34)
            s.render.filepath=str(DEST/f'{role}-{mode}.png');bpy.ops.render.render(write_still=True)
print('CAD renders complete',flush=True)
