from pathlib import Path
import FreeCAD as A,MeshPart
R=Path(__file__).resolve().parent
for role in ['explorer','architect']:
    d=A.openDocument(str(R/'cad'/f'{role}-revision06.FCStd'))
    mesh=MeshPart.meshFromShape(Shape=d.Base.Shape.cleaned(),LinearDeflection=.02,AngularDeflection=.12,Relative=False)
    for folder in ['prototype-stl','render-meshes']:mesh.write(str(R/folder/(role+'-Base.stl')))
    A.closeDocument(d.Name)
print('Fine tessellation exported for narrow battery-land join faces')
