"""Actual-part fit samples. FreeCAD Python; no nominal substitute geometries."""
from pathlib import Path
import json
import FreeCAD as A
import Part,MeshPart
R=Path(__file__).resolve().parent
O=R/'fit-tests';O.mkdir(exist_ok=True);checks=[]
def save(n,s,purpose):
    s=s.removeSplitter()
    if not s.isValid() or len(s.Solids)!=1:raise RuntimeError((n,len(s.Solids)))
    bb=s.BoundBox;s.translate(A.Vector(-bb.XMin,-bb.YMin,-bb.ZMin))
    mesh=MeshPart.meshFromShape(Shape=s,LinearDeflection=.02 if n=='01-rounded-grip-base' else .13,AngularDeflection=.12 if n=='01-rounded-grip-base' else .22,Relative=False)
    # BRep bounds can include untrimmed spline poles. Normalize from the actual
    # triangulated surface so test coupons rest at Z=0 in the slicer.
    actual=mesh.BoundBox;matrix=A.Matrix();matrix.move(A.Vector(-actual.XMin,-actual.YMin,-actual.ZMin));mesh.transform(matrix)
    mesh.write(str(O/(n+'.stl')))
    checks.append({'file':n+'.stl','valid_brep':True,'solids':1,'purpose':purpose})
e=A.openDocument(str(R/'cad'/'explorer-revision10.FCStd'))
grip=Part.makeBox(75,79,70,A.Vector(171,132,-1))
save('01-rounded-grip-base',e.Base.Shape.common(grip),'Actual battery-side grip section; pair with lid sample to assess feel and underside access.')
save('02-rounded-grip-lid',e.Lid.Shape.common(grip),'Actual rounded lid section. Cropped leading edge is deliberately open.')
save('03-battery-door',e.Battery_Door.Shape.copy(),'Independent PP3 door. Actual cell and snap required.')
crop=Part.makeBox(59,24,35,A.Vector(83,-6,12))
save('04-i2c-shutter-track',e.Base.Shape.common(crop),'Actual rear I2C shutter receiver section.')
save('05-i2c-shutter',e.I2C_Rear_Shutter.Shape.copy(),'Sliding cover; target travel 21 mm.')
save('06-i2c-keeper',e.I2C_Rear_Keeper.Shape.copy(),'End keeper; full enclosure lid captures its head.')
save('07-joystick-carrier',e.Joystick_Carrier.Shape.copy(),'Try actual PCB before attempting a full lid.')
save('08-joystick-receiver',e.Lid.Shape.common(Part.makeBox(48,38,30,A.Vector(173,23,30))),'Actual lid and blind snap receiver around joystick.')
save('09-uno-edge-clip',e.UNO_Edge_Clip_1.Shape.copy(),'Replaceable board edge clip.')
save('20-reveal-pod',e.Lid.Shape.common(Part.makeCylinder(13,20,A.Vector(123,117,53))),'Actual isolated sensor seat, opaque floor and bayonet collar. Round crop avoids cutting through the curved outer shoulder. Test insertion and removal with real sensor.')
save('21-reveal-dome',e.Reveal_Dome.Shape.copy(),'Actual 0.4 mm roof dome. Compare light readings with RGB active before selecting this roof.')
A.closeDocument(e.Name)
m=A.openDocument(str(R/'cad'/'main-revision10.FCStd'))
save('10-lcd-carrier',m.LCD_Carrier.Shape.copy(),'Fit the actual LCD PCB and backpack; measure hole pattern before adding any pins.')
save('11-lcd-receiver',m.Lid.Shape.common(Part.makeBox(96,48,31,A.Vector(70,19,37))),'Actual LCD window and receiver sample.')
save('12-usb-track',m.Base.Shape.common(Part.makeBox(82,18,31,A.Vector(58,-5,18))),'Existing rear USB track, separate from the two new side I2C ports.')
save('13-usb-shutter',m.USB_Shutter.Shape.copy(),'Main rear USB cover; 35 mm target travel.')
save('14-usb-keeper',m.USB_Shutter_Keeper.Shape.copy(),'USB end stop.')
A.closeDocument(m.Name)
a=A.openDocument(str(R/'cad'/'architect-revision10.FCStd'))
save('15-breadboard-button-cap',a.Button_Cap.Shape.copy(),'Full-length breadboard actuator. Confirm installed switch height and free gap before use.')
save('16-button-stem-guide',a.Button_Stem_Guide.Shape.copy(),'Snap-in stem guide and downward stop; test return and release.')
save('17-button-roof',a.Lid.Shape.common(Part.makeBox(42,40,35,A.Vector(28,75,30))),'Actual button roof opening and guide receivers. Test with the cap and guide over the real breadboard switch.')
save('18-servo-cassette',a.Servo_Cassette.Shape.copy(),'Fit the real servo body and mounting ears in the loose cassette.')
save('19-servo-retainer',a.Servo_Retainer.Shape.copy(),'Snap bridge for the servo cassette; test release and movement under load.')
A.closeDocument(a.Name)
(O/'VALIDATION.json').write_text(json.dumps(checks,indent=2))
print(len(checks),'fit samples exported')
