# Revision 09 — where each component is held

26 October 2026. This is a CAD prototype with nominal component dimensions. Neither photographs nor a similar online listing establish the exact hole coordinates of the parts you own.

## Direct answers

| Assembly | Component | Screwless attachment in the CAD | Installation / release |
|---|---|---|---|
| Explorer | Joystick module, including its click switch | Separate edge-capture carrier with PCB ledges and upper retaining lips; carrier pushes into receivers under the lid | Fit the module in the loose carrier, then seat the carrier. Release its side ears from inside. Verify full stick tilt and click travel. |
| Explorer | Bare photoresistor | Small raised isolated seat above the roof; two lead bores; separate quarter-turn dome | Rotate the dome to align its two tabs with the collar slots, lift it off, insert the sensor and feed its leads through, then replace and turn the dome. Do not rotate the sensor or twist its leads. |
| Architect | Potentiometer | Integral cylindrical cup and removable quarter-turn lower keeper | Remove knob, place the body from inside, pass the shaft through the roof, and turn the keeper into place. Body size, antirotation lug and terminal clearance remain fit items; use a removable thin insulating shim if the measured body needs preload. |
| Architect | SG90 servo | Separate body cassette, keyed lower push-in feet, and NEW removable snap bridge across its top | Insert the servo into the loose cassette from above, latch the bridge into its side pockets, then install the cartridge. Two provisional slots leave room for the mounting ears. Release the bridge beams to remove it. No threaded screws or assumed ear-hole pins. |
| Architect | Pushbutton on breadboard | NEW long printed stem integral with the external cap; separate snap-in guide/stop with two bearings | Insert the cap from beneath the lid, latch the guide below it, then align the switch on the breadboard under the stem. Pressing the external cap downward presses the actual switch downward. The switch's own spring returns the cap. |
| Main | 16×2 LCD / I2C backpack | Separate flat edge-capture carrier under the window | Fit the PCB into the carrier, keeping the backpack and trimmer clear; snap the carrier into the lid. Corrected the reference stack so the display and PCB are connected, rather than separate bounding boxes. |
| Main | Buzzer | Integral round cup, sound slots and removable lower bayonet ring | Insert the sounder from beneath the lid with sound opening toward the slots; fit the ring with the wires through its centre. Actual buzzer diameter still needs confirmation. |
| Main | Power-control cap | Short guided cap and switch cassette | This is a control actuator. It is not itself an electrical latching power switch, and cannot turn independently battery-powered controllers on through an unpowered I2C bus. The load-switch/power circuit is still to be selected. |
| All three | RGB LED | Integral light cup, LED flange seat and quarter-turn lower keeper | Install LED through its underside seat, fit keeper, then diffuser and symbol mask. Use individual insulating sleeves on the leads. |
| All three | Arduino | Cradle, support pads and two replaceable push-in edge clips | Seat PCB on supports, then fit edge clips. Keep solder joints and connectors clear; remove the R4's supplied clear base if using this cradle. |
| All three | Full-size breadboard | Base rails, lateral stops and four retaining fingers | Press the board into the base cradle. Confirm backing plate/interlocks fit the 166×55×10 mm allowance. |

The joystick belongs to **Explorer**, not Main. Main has the LCD, buzzer, RGB and power-control actuator. This preserves the agreed project layout.

## What “push screws” means here

The design uses **snap-fit clips**, **edge-capture PCB carriers**, **bayonet / quarter-turn keepers**, and a **snap-in servo retaining bridge**. These are screwless mechanisms. It does **not** yet have fixed printed pins through every PCB mounting hole.

Commercial hole-based alternatives are called **snap-lock PCB supports**, **push-in PCB spacers**, **nylon push rivets**, or **removable arrowhead PCB supports**. Their hole diameter, board thickness, panel thickness and grip length must match the actual hardware. The [Essentra PCB hardware guide](https://essentracomponents.bynder.com/m/13ad13f3d908c724/original/Essentra_PCB-Buyers-Guide_-UK.pdf) shows these families. Do not buy an arbitrary pin size based only on the product name. The current edge carriers remain usable without relying on guessed hole patterns; they can be edited or replaced after the real board is measured.

## Architect button reach

The previous switch cassette sat near the lid. That did not implement the requested breadboard switch. Revision 09 replaces that cassette on Architect with a stem guide.

- Breadboard bottom Z=5 mm, nominal board thickness 10 mm, top Z=15 mm.
- Nominal switch actuator height above the breadboard: **7.3 mm** (unconfirmed projected-plunger variant).
- Actuator top: Z=22.3 mm. Stem tip at rest: Z=22.45 mm; nominal free gap **0.15 mm**.
- Printed stop allows **0.45 mm** downward motion from the drawn rest pose: 0.15 mm gap plus 0.30 mm nominal actuator motion.
- The 5 mm-diameter stem runs through two guides. The cap flange transfers excess travel to the printed stop, rather than allowing unlimited pressure on the switch.
- The outer button centre remains at exported X=49, Y=95 mm. Its breadboard position must be aligned to the actual socket grid; no PCB-hole coordinates have been inferred.

These are design settings, not a guarantee for the pictured switch. A switch with a different actuator height needs a different stem length; an incorrectly long stem can hold the switch on. Measure the installed height with the switch seated in the actual breadboard. Edit `architect_button_switch_height_above_breadboard_mm`, rest gap and stroke in `dimensions.json`, regenerate the cap/guide, and test the small assembly first. Do not scale a mating STL. Confirm the switch legs fit the breadboard without stressing or shorting the contacts.

## Photoresistor access and light isolation

The dome is a separate printed part, not a sealed bump. Its two bayonet tabs align with entry slots at a quarter turn from the locked pose. The sensor sits above an opaque floor, so the internal RGB cup does not have a direct opening into the sensor cavity. The only penetrations through that floor are the two 1 mm lead passages. Seal those passages with opaque insulating sleeves or a small removable opaque seal if light leaks around the real leads.

The 0.4 mm roof is an optical test. Bronze/black opaque filament may transmit too little ambient light even at that thickness. Try the supplied 0.4, 0.6 and 0.8 mm alternatives, or use the clear-film frame with a small clear insert. Print only one selected dome for the final assembly. A transparent optical insert is a functional material, separate from the single-colour decorative finish.

## Why the earlier internal images looked incomplete

They deliberately displayed only the **base** hardware. Most controls are mounted to the removable **lid**. New underside and close-up views show those components and carriers. Blue/green/black volumes represent purchased electronics, not printable parts. The **orange block** is reserved space for an unselected regulator/load-switch circuit. The green block is an optional ESP32 allowance. Neither block is an extra part to print, and neither means that the electrical design is finished.

## Dimension references and confidence

| Photo family | Published reference | CAD use / remaining uncertainty |
|---|---|---|
| Black five-pin joystick module | [Joy-IT KY-023](https://www.joy-it.net/en/products/COM-KY023JM) lists a 34×39×26 mm overall envelope | Not enough to determine PCB mounting holes, header projection or shaft offset. Existing 34×26 mm PCB allowance remains provisional. |
| Blue SG90 servo | [TowerPro SG90 Analog](https://towerpro.com.tw/product/sg90-analog/) lists 23×12.2×29 mm and a 32.3 mm drawing dimension | Used as a family envelope. Ear span/location, horn and clone tolerances still need actual fit checks. New ear clearances are provisional, not an exact identification. |
| 16×2 character LCD | [Adafruit 181](https://www.adafruit.com/product/181) lists 80.6×36 mm PCB, 69×24 mm screen and 8.4 mm combined height | Corrected stack layout. CAD retains a conservative 1.6 mm PCB thickness, whereas this reference lists 1 mm. Actual backpack, header and PCB thickness remain unverified. |
| Square tactile button | [Omron B3F family drawing](https://omronfs.omron.com/en_US/ecb/products/pdf/en-b3f.pdf) includes 6 mm and 12 mm body families and multiple actuator heights | A related mechanical reference only; the photo does not identify an Omron model. 12×12 mm / 7.3 mm button setup is provisional. |
| Bare LDR, RGB, round buzzer and shaft potentiometer | Photos identify component families but no legible manufacturer part numbers | No claim of exact online identification. Seat sizes remain in `DIMENSION_CHECKLIST.csv`. |

## Software, tools and supplies

Already installed: **FreeCAD** for native solids, **PrusaSlicer** for orientation/support inspection, **OpenSCAD** optional (not required for these FreeCAD sources). No additional application or plugin is required. The CAD scripts use FreeCAD's bundled Python.

Useful physical tools: digital caliper or a ruler for an initial check, flush cutters, small deburring/file tools, non-marring tweezers, and a multimeter. For assembly: insulated wire sleeves/heat-shrink, reusable silicone straps for strain relief, optional thin closed-cell insulating shim, and a clear optical film if the filament blocks light. Select the regulated servo-power and load-switch electronics before final wiring; the orange reserved volume is not a purchase specification.

See `PRINT_PLAN.csv` for each printed part's starting orientation and support precautions. No machine-specific G-code or UIC submission has been produced.
