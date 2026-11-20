from pathlib import Path
import FreeCAD as A
import Part,MeshPart
R=Path(__file__).resolve().parent;O=R/'inspection-meshes';O.mkdir(exist_ok=True)
for role,name,p,size in [('explorer','explorer-reveal-seat',(106,100,51),(34,34,23)),('architect','pot-mount-seat',(183,28,39),(28,28,20)),('main','buzzer-mount-seat',(28,98,42),(30,32,23))]:
    d=A.openDocument(str(R/'cad'/f'{role}-revision09.FCStd'))
    shape=d.Lid.Shape.common(Part.makeBox(*size,A.Vector(*p)))
    MeshPart.meshFromShape(Shape=shape,LinearDeflection=.13,AngularDeflection=.22,Relative=False).write(str(O/(name+'.stl')))
    A.closeDocument(d.Name)
