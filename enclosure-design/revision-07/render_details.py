from pathlib import Path
src=Path(__file__).with_name('render_revision07.py').read_text().split('for role in selection:')[0]
exec(compile(src,__file__,'exec'))
original=records[:]
def detail(names,filename,opened=False):
    global records
    records=[r for r in original if r['role']=='architect' and r['name'] in names]
    scene,mats=setup();scene.render.engine='BLENDER_WORKBENCH'
    scene.view_settings.exposure=0;scene.view_settings.view_transform='Standard'
    scene.display.shading.light='STUDIO';scene.display.shading.color_type='MATERIAL'
    scene.display.shading.show_cavity=True;scene.display.shading.cavity_type='BOTH'
    mats['bronze'].diffuse_color=(.45,.48,.5,1)
    load('architect','all',mats)
    if opened:
        from mathutils import Matrix
        pivot=Vector((-.073,-.0715,.058))
        for name in ['Gate_Rotor','Original_Horn_Envelope']:
            obj=bpy.data.objects.get('architect '+name)
            if obj:
                obj.matrix_world=Matrix.Translation(pivot)@Matrix.Rotation(math.radians(-110),4,'Z')@Matrix.Translation(-pivot)@obj.matrix_world
    camera(scene,(-.12,-.01,.17),(-.073,-.0715,.052),.085)
    scene.render.filepath=str(DEST/filename);bpy.ops.render.render(write_still=True)
detail(['Servo_Cassette','SG90_Body_Envelope','Gate_Rotor','Original_Horn_Envelope'],'gate-mechanism.png')
detail(['Servo_Cassette','SG90_Body_Envelope','Gate_Rotor','Original_Horn_Envelope','Gate_Window_Cover'],'gate-closed.png')
detail(['Servo_Cassette','SG90_Body_Envelope','Gate_Rotor','Original_Horn_Envelope','Gate_Window_Cover'],'gate-open.png',True)
records=original
# Interior signatures and tiny initials in the real CAD.
scene,mats=setup();scene.render.engine='BLENDER_WORKBENCH'
scene.view_settings.exposure=0;scene.view_settings.view_transform='Standard'
scene.display.shading.light='STUDIO';scene.display.shading.color_type='MATERIAL';scene.display.shading.show_cavity=True;scene.display.shading.cavity_type='BOTH'
mats['bronze'].diffuse_color=(.48,.5,.52,1)
records=[r for r in original if r['role']=='architect' and r['name'] in ['Battery_Door','Button_Cap','Switch_Cassette','Gate_Window_Cover']]
# Lay parts flat at distinct positions, retaining exported mesh geometry.
plane=next(o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('Plane'))
bpy.data.objects.remove(plane,do_unlink=True)
scene.display.shading.background_type='WORLD';scene.world.color=(.06,.075,.09)
scene.display.shading.show_shadows=True
scene.display.shading.cavity_ridge_factor=2;scene.display.shading.cavity_valley_factor=2
for i,r in enumerate(records):
    bpy.ops.wm.stl_import(filepath=str(R/'render-meshes'/r['file']))
    obj=bpy.context.object;obj.name=r['name'];obj.scale=(.001,)*3
    b=[Vector(c) for c in obj.bound_box];centre=sum(b,Vector())/8
    obj.location=Vector((i*.065-.095,0,0))-centre*.001
    if r['name']=='Switch_Cassette':
        obj.rotation_euler.x=math.pi
        obj.location=Vector((i*.065-.095,0,0))-Vector((centre.x,-centre.y,-centre.z))*.001
    obj.data.materials.append(mats['bronze'])
camera(scene,(0,.01,.4),(0,0,0),.29)
scene.render.filepath=str(DEST/'personalization.png');bpy.ops.render.render(write_still=True)
