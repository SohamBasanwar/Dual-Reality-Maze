from pathlib import Path
src=Path(__file__).with_name('render_revision06.py').read_text().split('for role in selection:')[0]
exec(compile(src,__file__,'exec'))
scene,mats=setup();scene.render.engine='BLENDER_WORKBENCH';scene.view_settings.exposure=0;scene.view_settings.view_transform='Standard'
scene.display.shading.light='STUDIO';scene.display.shading.color_type='MATERIAL';scene.display.shading.show_cavity=True;scene.display.shading.cavity_type='BOTH'
scene.display.shading.background_type='WORLD';scene.world.color=(.045,.055,.07)
mats['bronze'].diffuse_color=(.4,.45,.5,1)
for r in json.loads((R/'detail-scene.json').read_text()):
    bpy.ops.wm.stl_import(filepath=str(R/'detail-meshes'/r['file']))
    o=bpy.context.object;o.scale=(.001,)*3;o.location=(-.123,-.1035,0);o.data.materials.append(mats[r['material']])
    bpy.ops.object.shade_smooth_by_angle(angle=.5)
camera(scene,(.025,.095,.085),(0,.009,.059),.042)
scene.render.filepath=str(DEST/'explorer-reveal-cutaway.png');bpy.ops.render.render(write_still=True)
scene,mats=setup();scene.render.engine='BLENDER_WORKBENCH';scene.view_settings.exposure=0;scene.view_settings.view_transform='Standard'
scene.display.shading.light='STUDIO';scene.display.shading.color_type='MATERIAL';scene.display.shading.show_cavity=True;scene.display.shading.cavity_type='BOTH'
mats['bronze'].diffuse_color=(.4,.45,.5,1)
records=[r for r in records if r['role']=='architect' and r['name'] in ['Servo_Cassette','SG90_Body_Envelope','Gate_Frame','Gate_Panel','Gate_Drive_Pin','Gate_Pin_Keeper','Original_Horn_Envelope']]
load('architect','all',mats)
camera(scene,(-.14,.09,.14),(-.073,-.061,.086),.092)
scene.render.filepath=str(DEST/'architect-gate-cutaway.png');bpy.ops.render.render(write_still=True)
