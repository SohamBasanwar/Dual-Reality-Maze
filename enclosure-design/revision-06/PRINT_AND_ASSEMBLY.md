# Prototype printing and assembly

Do not send the complete set to print before trying the fit samples. STL validity is not a fit or strength certificate. All dimensions are millimetres.

## Small tests first

1. Print the grip/base sample, matching lid sample and battery door. Try the chosen PP3 cell and its actual snap connector; leave wire slack. Check hand comfort and that the seam does not press into the palm.
2. Print an I2C shutter receiver, shutter and keeper. Remove support debris completely. Test 21 mm travel and insert the actual sleeved jumper bundle. Test the separate rear USB opening with the actual cable too.
3. Print the joystick carrier and its receiver sample, then the LCD carrier/receiver sample. Check PCB edges, solder joints and connector clearance. Do not force an unknown board into a nominal cradle.
4. Test the UNO clips, LED keeper, raised reveal dome, pot/buzzer keepers and switch cassette with their actual parts. Repeatedly insert and remove the latches before approving the material. The reveal dome has three thin printed roof alternatives plus a clear-film option; test light transmission and covered readings in the intended room.
5. Assemble the gate cassette, original servo horn, frame and gate before fitting the decorative shroud. Verify that the horn retaining bridge clears rotation and prevents axial withdrawal. Test the pin/keeper, or use an appropriately sized nylon push-rivet. The printed C keeper is particularly small and may require substitution after testing.

## Slicer preparation

- The exported STL parts retain their assembled coordinates. Use **split to objects** where appropriate, place each part on a suitable face, and inspect every layer.
- Preserve the rounded grip geometry. Supports will be needed for some curved exterior surfaces and undercuts. Choose orientation and support contact surfaces so that removal does not damage the grip finish, clip roots or mating lands.
- Do not fill closed shutter channels or hidden snap receivers with inaccessible support. Print separate keepers and carriers individually. Review blockers or change orientation where necessary.
- Do not scale an entire enclosure to correct a clip fit: that also changes the component and gate clearances. Adjust the relevant parameter and reprint a coupon.
- Match the actual UIC printer, bed, nozzle and permitted material. No machine-specific G-code is supplied. A rendering colour is not a filament specification.
- The long handheld shell is roughly 246 mm wide. The gate guard rises above the Architect lid. Check the exact STL bounds and the chosen orientation against the available bed; do not assume that a nominal 250 mm bed gives enough brim/clearance.

## Internal assembly order

1. Fit the battery-door tabs, verify its release tongue and check the cell bay without live wiring.
2. Install the breadboard and UNO into their lower trays. Insert the replaceable UNO edge clips. Check that a clip contacts a safe board edge rather than a component or header.
3. Route the sleeved I2C cable through the open hatch and secure its jacket/bundle to the internal cleat with a soft reusable restraint. Leave service loops. Install the shutter end keeper before closing the case.
4. Fit joystick/LCD carriers, button cassette and individual LED/rotary/buzzer retainers into the lid. Seat the photoresistor above the roof, route its two leads through their small passages, and fit the quarter-turn dome. Use snug opaque sleeves around the leads if needed to block internal light. Check that the lid can be lifted for service without pulling leads.
5. For Architect, seat the servo in its cassette, fit its supplied horn at a calibrated centre position, install the gate panel and drive pin, and push the frame feet into their sockets. Check the horn hub keeper and pin C keeper before adding the shroud.
6. Verify clearance through the permitted gate travel by hand with the servo unpowered and without forcing the gear train. Then test powered movement slowly with calibrated limits. Keep fingers out of the crank/slot and rail gaps.
7. Use the lid's rear locating tabs and side release latches. Check every latch and battery door before carrying the controller.

## Still open

Actual component and hole measurements; material-dependent fit and flex; potentiometer antirotation details; tiny pin/keeper durability; loaded gate limits; servo power support; battery runtime; optional ESP32 mounting and antenna location. The Main power-button actuator does not itself implement the electrical power switching circuit.
