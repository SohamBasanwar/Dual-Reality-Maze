from pathlib import Path
import csv
R=Path(__file__).resolve().parent
with (R.parent/'revision-05'/'DIMENSION_CHECKLIST.csv').open(newline='',encoding='utf-8-sig') as f:rows=list(csv.reader(f))
for row in rows:
    if row and row[0]=='UNO R3':row[-1]='Header and plug heights; underside clearance; safe clip contacts; actual outline and mounting-hole coordinates'
rows += [
 ['Reveal dome','User-requested raised isolated pod','20 mm hood; 24 mm collar; about 11 mm above roof','Check finger reach and bayonet fit; surrounding raised details clear'],
 ['Photoresistor leads','Actual part not measured','Two 1.0 mm bores at provisional 2.54 mm spacing','Measure disc diameter/thickness and lead diameter/spacing; fit opaque sleeves if needed'],
 ['Optical roof','Same-filament test requested','0.4 / 0.6 / 0.8 mm alternate membranes','Test actual filament and lighting; compare covered/uncovered readings while cycling RGB'],
 ['Clear-film alternative','Optional fallback','7.2 mm disc; 0.2-0.3 mm thick','Choose clear sheet; keep adhesive outside optical aperture; calibrate again'],
 ['I2C shutter and sleeve','User specifies 30 cm jumper leads','18 x 12 mm opening; 21 mm travel','Actual bundle and connector dimensions; bend allowance; usable span after internal loops'],
 ['Gate original horn','SG90 family only','7 mm provisional crank radius','Measure spline seating, horn hub, hole size/radius; test axial keeper and actual movement limits'],
 ['Push-in carriers','Unmeasured holes intentionally deferred','Replaceable edge carrier / clips','Actual joystick LCD and servo holes, safe PCB contacts, clip retention and repeated release'],
 ['Rounded grips','Xbox sculpted geometry used as reference','Large-breadboard prototype footprint retained','Hand trial of actual-size grip coupon before committing to full enclosures']]
with (R/'DIMENSION_CHECKLIST.csv').open('w',newline='',encoding='utf-8') as f:csv.writer(f).writerows(rows)
print('Updated measurement checklist')
