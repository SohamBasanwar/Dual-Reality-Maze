from pathlib import Path
src=Path(__file__).with_name('render_review.py').read_text(encoding='utf-8').split("if not requested or 'cases'")[0]
exec(compile(src,__file__,'exec'))
for code in ['E01','E04','M02','M23','M27','M31']:
    row=next(r for r in original if r.get('assembly_code')==code);mark=row['id_location'];assert mark
    role=row['role'];records=[row];s,m=studio();m['bronze'].diffuse_color=(.61,.62,.64,1);load(role,'all',m)
    W=234 if role=='main' else 246;D=180 if role=='main' else 207
    xy=mark['xy_mm'];angle=mark['angle_deg'];target=(xy[0]+(1 if angle==90 else 2.5),xy[1]+(2.5 if angle==90 else 1),mark['z_mm'])
    center=Vector(((target[0]-W/2)*.001,(target[1]-D/2)*.001,target[2]*.001))
    if mark['underside']:
        bpy.context.view_layer.update();turn=Matrix.Translation(center)@Matrix.Rotation(math.pi,4,'X')@Matrix.Translation(-center)
        for o in bpy.data.objects:
            if o.type=='MESH':o.matrix_world=turn@o.matrix_world
    camera(s,center+Vector((.05,-.35,1)).normalized()*.5,center,.022 if code in ['E01','M02'] else .017)
    if mark['underside']:s.camera.rotation_euler.rotate_axis('Z',math.pi)
    s.render.resolution_x=1000;s.render.resolution_y=650;save(s,'id-'+code)
print('Actual engraved assembly codes rendered')
