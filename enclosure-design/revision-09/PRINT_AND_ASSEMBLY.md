# Revision 09 — prototype printing and assembly

All dimensions are millimetres. Start with the actual cropped fit samples, not all three complete shells.

1. Print the new contoured grip sample, matching lid and battery door. Try the actual PP3 battery and its snap connector with wire slack. Check the rim against your palm and cycle the catch repeatedly. Do not flatten the contoured door in the slicer or scale it independently.
2. Test shutter tracks and keepers with the sleeved cable bundle. I2C travel is 21 mm; the separate Main USB shutter travels 35 mm. Keep them open while connected. Secure the cable bundle to its internal cleat with a soft restraint.
3. Verify the actual joystick, LCD/backpack, UNO, potentiometer, switch, RGB and buzzer parts in their carriers. Check solder joints, headers and operating travel. PCB holes have not been guessed.
4. Test the isolated reveal dome with the RGB LED on and a finger covering the sensor. An opaque printed roof may block ambient light. Test roof alternatives or fit a clear window in the separate film-frame option. Seal light leakage around the two lead passages without trapping the wires.
5. Print the gate cartridge, frame, panel, guard and small drive pieces as a standalone mechanism trial. Measure the real SG90 body, mounting ears, shaft offset, horn hub, horn hole and pin radius. Fit its original nylon horn; do not print an assumed spline.
6. Calibrate the unloaded servo, disconnect power, then assemble the horn, headed drive pin, C keeper and slotted yoke. The frame bridge captures the horn hub, and the guard retains the upper slider. Confirm axial retention, free pin movement and rail clearance without forcing the gearbox.
7. The nominal crank radius is 7 mm, producing about 12.12 mm lift across a −60° to +60° range. Start powered testing with narrower calibrated limits and slow movement using regulated servo power. Check the entire path and guard openings, then expand only as clearances permit. Small FDM pin/keeper parts may require a measured nylon push-rivet alternative.
8. Install the cartridge/frame in the hanging collar and fit the guard. Check the latch engagements and concealed drive passage before closing the lid. The lower drive now occupies internal shoulder space; leave the reserved clearance free of wires.
9. Assemble the base components, shutters and service loops. Fit rear lid tabs and side snaps, then check the independent battery door. Keep the optional ESP32 and jumper reservation free unless that hardware is installed.

## Slicing

STLs retain their assembly positions. Orient each part deliberately. Curved shells and undercuts may need supports; make support removable and keep it out of blind slide tracks, narrow receivers and the gate's yoke slot. Inspect the contoured door's layers and latch root. Test clips in the chosen material and print orientation.

Text is engraved about 0.26 mm deep. Inspect the fine SB initials in the slicer; they may require a smaller layer height or nozzle. Do not enlarge an entire mating part just to improve lettering. Unmarked tiny parts still have identifying file labels and parts-list entries.

Check mesh bounds, brim allowance and material against the selected UIC printer. No machine profile or G-code is included. Physical fit, grip feel, latch fatigue, gate operation, optical response, power switching and battery runtime have not been certified by CAD checks.


## Revision 09 installation order

1. Fit the Arduino, breadboard and battery in their base restraints. Keep reserved optional space clear. Test the independent contoured battery door before wiring.
2. Fit joystick and LCD into their loose edge carriers, then snap the carriers into their lid receivers. Fit pot and buzzer from the underside and turn their lower keepers into place. Test antirotation and terminal clearance on the real potentiometer.
3. Remove the photoresistor hood by quarter turn and lift. Insert the sensor into its above-roof seat, feed its two leads through the isolated bores, seal light leaks and replace the hood. Do not twist the sensor leads.
4. Architect: fit the actual switch into the breadboard first. Verify the installed actuator height. Insert the long printed cap from below the lid; fit the two-bearing guide by its snap beams. Bring the lid into position and confirm the cap is not preloaded. Test free return, alignment and the 0.45 mm nominal stop. Change the stem-height parameters if needed; do not scale the STL.
5. Architect: place the SG90 in the separate cassette from above, latch the new retaining bridge, then fit the cartridge/frame and original nylon horn drive. No forced insertion under stiff integral top lips is required. Confirm real servo ear and wire clearance.
6. Fit RGB LEDs, keepers, selected optical diffusers and masks. Route wiring with service slack. Keep every moving part and guide free of wires before closing the shell.

Print the new button cap/guide/roof samples, servo cassette/retainer, and reveal pod/dome samples before full shells. `PRINT_PLAN.csv` gives a starting orientation and support caution for each of the 50 assembly parts. Review supports in PrusaSlicer; this is not an automatically validated machine setup. General support guidance: https://help.prusa3d.com/article/support-material_1698 . No printer-specific G-code is supplied.

Main's momentary power-control button still needs a suitable load-switch/latching circuit; it is not an electrical mains or battery switch by itself. Independent battery-powered controllers cannot be switched fully off/on through an unpowered I2C link alone.
