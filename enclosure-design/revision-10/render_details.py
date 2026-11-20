from pathlib import Path
src=Path(__file__).with_name('render_revision10.py').read_text().split('for role in selection:')[0]
exec(compile(src,__file__,'exec'))
from mathutils import Matrix
original=records[:]
names=['Servo_Cassette','Servo_Retainer','SG90_Body_Envelope','Gate_Frame','Gate_Panel','Gate_Drive_Pin','Gate_Pin_Keeper','Original_Horn_Envelope','Gate_Shroud']
def studio():
    scene,mats=setup();scene.render.engine='BLENDER_WORKBENCH'
    scene.view_settings.exposure=0;scene.view_settings.view_transform='Standard'
    scene.display.shading.light='STUDIO';scene.display.shading.color_type='MATERIAL'
    scene.display.shading.show_shadows=True;scene.display.shading.show_cavity=True;scene.display.shading.cavity_type='BOTH'
    scene.display.shading.cavity_ridge_factor=1.3;scene.display.shading.cavity_valley_factor=1.3
    scene.display.shading.background_type='WORLD';scene.world.color=(.055,.065,.08)
    mats['bronze'].diffuse_color=(.35,.39,.43,1)
    return scene,mats
for kind in ['closed','open','mechanism']:
    records=[r for r in original if r['role']=='architect' and r['name'] in names and not(kind=='mechanism' and r['name']=='Gate_Shroud')]
    scene,mats=studio();load('architect','all',mats)
    if kind=='open':
        ob=bpy.data.objects['architect Gate_Panel'];ob.location.z+=.01212436
        pivot=Vector((-.062,-.0435,.055))
        for n in ['Original_Horn_Envelope','Gate_Drive_Pin','Gate_Pin_Keeper']:
            ob=bpy.data.objects['architect '+n]
            ob.matrix_world=Matrix.Translation(pivot)@Matrix.Rotation(math.radians(120),4,'Y')@Matrix.Translation(-pivot)@ob.matrix_world
    camera(scene,(-.09,.14,.12),(-.067,-.0435,.067),.132)
    scene.render.filepath=str(DEST/f'gate-{kind}.png');bpy.ops.render.render(write_still=True)

# Actual contoured underside, shown in light material for seam inspection.
records=original
scene,mats=studio();load('explorer','assembled',mats)
plane=next(o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('Plane'))
bpy.data.objects.remove(plane,do_unlink=True)
camera(scene,(.24,.29,-.37),(.07,.05,.01),.22)
scene.render.filepath=str(DEST/'battery-contour.png');bpy.ops.render.render(write_still=True)

# Door alone from its inside: engraving and unchanged catch remain visible.
records=[r for r in original if r['role']=='explorer' and r['name']=='Battery_Door']
scene,mats=studio();load('explorer','all',mats)
camera(scene,(.11,.19,.17),(.079,.055,.005),.085)
scene.render.filepath=str(DEST/'battery-door-detail.png');bpy.ops.render.render(write_still=True)
print('Portcullis motion and contoured battery access rendered')
