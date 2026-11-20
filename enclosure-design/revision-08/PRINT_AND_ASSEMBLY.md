# Revision 08 — prototype printing and assembly

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
