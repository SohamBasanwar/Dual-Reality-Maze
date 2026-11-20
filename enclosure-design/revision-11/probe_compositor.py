import bpy
t=bpy.data.node_groups.new('probe','CompositorNodeTree');g=t.nodes.new('CompositorNodeGlare')
print('GLARE PROPERTIES',[(p.identifier,str(p.type)) for p in g.bl_rna.properties])
print('GLARE INPUTS',[(i.name,str(getattr(i,'default_value','none'))) for i in g.inputs])
