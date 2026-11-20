# Revision 07 — printing and assembly

These are millimetre-scale design-review prototypes. Do not send all shells to print based on mesh validity alone.

1. Start with the real grip/base coupon, matching lid and battery door. Check the actual PP3 battery and snap, door release, repeated latch cycling and hand comfort. The revised blend is a geometry change, not a verified ergonomic result.
2. Test the cable-shutter samples and keepers. The I2C cover must travel 21 mm freely; Main rear USB travels 35 mm. Keep covers open while cables are installed. Secure a sleeved bundle to the internal cleat with a soft restraint; a shutter is not a cable clamp.
3. Test replaceable joystick/LCD carriers, UNO clips, switch cassette, potentiometer keeper and RGB retainers on actual parts. Nothing should press on solder joints or electronic components. Unknown PCB holes have not been guessed.
4. Test the reveal dome with the real photoresistor and RGB light on. Opaque filament may block useful light even at 0.4 mm. The clear-film frame is an alternative. Seal the two lead passages against internal light after fitting the sensor, while retaining serviceability.
5. Print the compact gate cartridge, rotor and cover as a separate mechanism trial. Measure the actual SG90 body, ears, shaft position, horn arm, hub and axial seating. Adjust the pocket rather than forcing the horn. The nominal motor reservation is 23 × 12.2 × 29 mm; a clone may differ.
6. Centre the powered servo with no mechanical load using an appropriate regulated supply. Disconnect power, fit its original nylon horn, then seat the rotor pocket over it. The original horn provides the spline; the printed pocket transfers torque. The cover provides provisional axial capture. Verify that it limits lift enough to retain the horn without rubbing the disk.
7. Start with a narrow, slow servo sweep and expand only after checking clearance. The design's nominal 110° range is a CAD motion study, not a calibrated electrical command. Verify both stops, horn retention and return movement under load. Add a clear PET shield over the viewport so fingers cannot touch the rotor. Shield attachment is still a fabrication detail, not an included printed part.
8. Install the electrical components and routing, leaving service loops. Keep the optional ESP32 and jumper-clearance regions clear unless that fallback is used. Install the I2C and USB shutter end keepers before closing the large lid.
9. Engage the lid's rear locating tabs, then its side snaps. Check the lid and independent battery door before carrying the controller.

## Slicer setup

STLs retain assembly coordinates; lay each part on a suitable surface before slicing. Curved shells and undercuts may need supports. Keep support out of closed slide tracks, blind snap receivers and small horn pockets. Choose an orientation that makes support removable and protects the grip finish. Test clips in the selected material and orientation; do not assume decorative or filled filament has enough flex.

Engraving is nominally about 0.26 mm deep. Fine “SB” text may require a smaller layer height or nozzle to resolve; inspect the slicer paths. It is acceptable for tiny hardware to stay unmarked; filename and parts-list identification remain. Do not enlarge a whole part to make its text easier to print, because that changes its fit.

Check exact mesh bounds against the selected UIC printer, build plate, brim and permitted material. No machine profile or G-code is supplied. No print form has been submitted. FreeCAD and PrusaSlicer are already installed; no additional dependencies are needed for inspection and slicing.

## Remaining measurements and tests

Actual breadboard size and backing, joystick/LCD outlines and holes, potentiometer terminals/antirotation feature, tactile switch height/travel, SG90 and supplied horn, RGB flange, buzzer dimensions, clear shield attachment, printer fit, loaded servo power and battery runtime. The Main button is a mechanical actuator; it does not itself implement the power-switching electronics.
