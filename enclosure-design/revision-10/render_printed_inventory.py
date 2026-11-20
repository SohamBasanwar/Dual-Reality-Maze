"""Render each final printed assembly part only, after validation passes."""
from pathlib import Path
src=Path(__file__).with_name('render_revision10.py').read_text(encoding='utf-8').split('for role in selection:')[0]
exec(compile(src,__file__,'exec'))
from bpy_extras.object_utils import world_to_camera_view
checks=json.loads((R/'ASSEMBLY_REVIEW.json').read_text())
for a in checks:
    for key in ['printed_part_intersections','gate_slider_intersections','shutter_travel_intersections','reveal_hood_rotation_and_removal_intersections','button_stroke_intersections']:
        assert not a[key],(a['role'],key)
    assert all(not x['conflicts'] for x in a['reserved_volume_checks'])
meshes=json.loads((R/'MESH_VALIDATION.json').read_text())
assert len(meshes['checks'])>=86 and all(q['watertight'] for q in meshes['checks'])
all_parts=[r for r in records if not r['component']]
T=DEST/'part-thumbnails';T.mkdir(exist_ok=True)
for i,r in enumerate(all_parts):
    records=[r];s,m=setup()
    s.render.engine='BLENDER_WORKBENCH';s.view_settings.exposure=0;s.view_settings.view_transform='Standard'
    s.display.shading.light='STUDIO';s.display.shading.color_type='MATERIAL';s.display.shading.show_shadows=True;s.display.shading.show_cavity=True;s.display.shading.cavity_type='BOTH';s.display.shading.background_type='WORLD';s.world.color=(.16,.18,.21)
    m['bronze'].diffuse_color=(.64,.65,.66,1)
    for key in ['explorer','architect','main']:m[key].diffuse_color=(.55,.67,.69,1)
    for o in list(bpy.data.objects):
        if o.type=='MESH' and o.name.startswith('Plane'):bpy.data.objects.remove(o,do_unlink=True)
    load(r['role'],'all',m);bpy.context.view_layer.update()
    ob=next(o for o in bpy.data.objects if o.type=='MESH')
    pts=[ob.matrix_world@Vector(p) for p in ob.bound_box]
    low=Vector(tuple(min(p[i] for p in pts) for i in range(3)));high=Vector(tuple(max(p[i] for p in pts) for i in range(3)))
    center=(low+high)/2;span=max(high-low)
    direction=Vector((.35,.5,1))
    if r['name'] in ['Base','Lid','Servo_Cassette','Gate_Frame','Button_Stem_Guide','Switch_Cassette']:direction=Vector((.25,.4,-1))
    if 'Shutter' in r['name']:direction=Vector((.6,-1,.3))
    if r['name']=='I2C_Left_Shutter':direction=Vector((1,.2,.35))
    if r['name']=='I2C_Right_Shutter':direction=Vector((-1,-.2,.35))
    camera(s,center+direction.normalized()*.5,center,span*1.32)
    s.render.resolution_x=560;s.render.resolution_y=400
    bpy.context.view_layer.update()
    pp=[world_to_camera_view(s,s.camera,p) for p in pts]
    projected_width=max(p.x for p in pp)-min(p.x for p in pp)
    projected_height=max(p.y for p in pp)-min(p.y for p in pp)
    s.camera.data.ortho_scale*=max(2*max(abs(p.x-.5) for p in pp)/.86,2*max(abs(p.y-.5) for p in pp)/.86)
    s.render.filepath=str(T/(r['role']+'-'+r['name']+'.png'));bpy.ops.render.render(write_still=True)
print(len(all_parts),'actual printed part thumbnails rendered')
