# Dual-Reality Maze: one family, three role-specific designs

**Revision USB-WiFi / October 22, 2026.** This is the current enclosure architecture. It supersedes the earlier battery and USB-data-relay assumptions. The output is a dimensioned design plan, monochrome artwork and adjustable reference CAD. The shell and fitted component openings are not released for final printing.

## The shared construction

Explorer and Architect use the same rounded gamepad outline, two full-hand grips and a serviceable upper shell. Their lower tray holds the Uno and a breadboard side by side. Controls mount at the upper level so the hands do not touch the circuit. Main uses a matching rounded desktop box with the same border and portal vocabulary. All dimensions are millimeters.

| Housing | Nominal outer width × depth × body height | Construction |
|---|---|---|
| Explorer | 214 × 138 × 54 | Two grips, upper joystick and exposed sensor |
| Architect | 214 × 138 × 54, plus about 29 guard height | Two grips, knob, button and central guarded gate |
| Main | 160 × 120 × 48 | Desktop LCD box, side USB-C access |

These are starting dimensions, chosen around a **provisional 83 × 55 mm half breadboard**, not measurements of your hardware. A full breadboard will require a different tray. The controller size comes from the full Uno, breadboard, upper controls and wire bends. Grip comfort and reach need a paper/cardboard test. Shell walls are 2.8 mm, the floor 3 mm and the top panel 2.8 mm. The reference CAD uses a locating rim. Final removable retention keys or service clips must be fitted and tested before the lid becomes a working screwless closure.

Support the boards on insulated ledges, with no floor contact under solder joints. Four safe edge stops locate each PCB. Add removable retaining keys after checking where they can touch the real board without pressing on components. The breadboard sits in a shallow pocket with end stops and a removable crossbar. Keep its adhesive backing covered so it can be removed for service. Use captive cable saddles and a service loop between the lid and tray. The CAD contains nominal ledges and routing saddles, not measured component clamps.

## Explorer: Lantern of Discovery

The top left carries the joystick, centered at **(47,43)**. A provisional **28 mm swing opening** leaves room for the cap, but its full diagonal movement and click must be measured. A sensor opening at **(166,22)** sits near the right index finger. It has a raised reveal ring so it is easy to locate by touch. The sensor itself must receive room light and remain easy to cover. A bare photoresistor and a sensor breakout require different holders.

The lower tray locates the R3 at **(17,24)** and the assumed half breadboard at **(99,24)**. The USB-B connector faces the left side through a plug-sized service opening. The I²C harness exits the cable edge at the rear center, with a saddle inside the box and a keyed disconnect outside. No battery cavity is included.

The exterior artwork uses the existing young Explorer’s cap, backpack and lantern. A reveal ring and short maze trace reinforce the light mechanic. Place the character crest on the right top panel and a small role badge on the front wall. The supplied side badge is a flat decal patch, not a full wrap around a curved grip. Use the 70 mm crest master for a larger side or presentation graphic. The top layout uses a smaller crest, best printed or engraved after checking detail size.

## Architect: Keeper of the Gates

The knob center is **(45,40)**, the confirm button **(169,40)** and the gate shaft **(107,91)**. The dial ring has five ticks matching the game’s five passage selections. The knob needs a grippable edge, clearance for fingers and a physical sweep test. The button opening is provisional: a small tactile switch needs a captive printed plunger rather than the panel hole used for a larger pushbutton.

The lower R3 and breadboard positions match Explorer. The SG90 occupies a separate lower-center bay beyond the assumed breadboard’s front edge. Its body is held by a cradle and a removable retention key. The reference file shows broad mounting lands only. Measure its tabs, body, lead and shaft. The small gate moves inside a **58 × 33 × 29 mm nominal guard** with narrow viewing slots. Keep the moving part and the hands separated and test the complete sweep, wire routing and release access.

**Screwless horn retention:** the usual servo horn has a center screw. This design requires a measured axial keeper under the guard so the horn cannot lift off. The keeper must allow free rotation without touching the shaft or binding the horn. Its geometry and gate coupling remain unresolved until the supplied horn is measured. Do not operate the gate as a finished assembly until that retention and guard test passes.

The adult Architect’s swept hair, beard, robe and floating rune cube match the existing game art. His crest sits between the knob and button, above the gate guard. Broad gate motifs sit on the grip shoulders. The front badge and dial ring share the Explorer’s one-color line weight.

## Main: Portal Nexus

The 16×2 display faces upward, centered at **(80,29)**. The provisional visible opening is **72 × 25 mm**, and the assumed LCD PCB is **80 × 36 mm**. Measure both the front bezel and the I²C backpack, including header and contrast trimmer height. The display needs a slide-in carrier or removable rear keeper that supports the PCB, with no pressure on the glass.

The R4 occupies **(12,60)** on the lower tray, with USB-C facing left. Its official store planar dimensions are **68.85 × 53.34 mm**, but connectors and the actual board must be checked. Put the buzzer near the right-side slots and retain it in a measured cradle. Explorer and Architect harnesses enter separately at the rear right and join a small accessible wiring point. Keep the R4 antenna region clear of the LCD metal frame, bundled wires, metallic foil and any metal decoration. Confirm the actual antenna position and orientation before fixing the carrier.

The portal crest goes below the LCD. A geometric LCD frame, two converging maze traces and a front badge tie it to the two controllers. Use nonmetallic ink or vinyl near the built-in antenna. The laptop remains the game display.

## Power and communication

Explorer R3 and Architect R3 use USB power. Main R4 uses USB-C power. Connect R3 **A4/SDA**, **A5/SCL** and **GND** to the Main’s 5V-header I²C bus. The LCD shares that bus. Do not substitute the R4’s Qwiic connector. Main uses its built-in Wi-Fi for laptop data. No external radio hardware is included.

Keep separately powered USB **positive supply rails separate**. The common inter-board harness carries signal lines and common ground. Review pull-ups, LCD address and controller addresses together. Start with a short harness and validate the actual cable at the chosen bus rate. A handheld cable is a strain-relieved harness, not loose breadboard jumpers hanging from a header.

Give the SG90 a dedicated, suitably rated regulated supply near 5V, using an appropriate USB power source and the servo’s actual voltage specification. Its ground joins the Architect signal ground. Keep its motor-current path off the Uno’s I/O pins and avoid feeding an external positive rail back into the board’s USB supply. Reserve a small rear entry for this lead. Measure peak load, voltage drop and resets with the gate installed before fixing the power connector. This is a power layout requirement, not a tested power circuit.

The current game has a direct USB serial controller prototype. The I²C relay and Main-to-laptop Wi-Fi firmware/game transport are still integration tasks. The enclosures provide physical access for the requested architecture without claiming it is already implemented.

## Applying the single-color artwork

The files in `assets/` are native SVG paths in exactly one solid ink, with transparent negative spaces. Black and white versions are supplied. The PNG versions retain transparency. The generated reference originals are preserved separately. Existing game sources supplied the Explorer, Architect and portal identity.

| Process | Use and limits |
|---|---|
| Single-color sticker or direct print | Best for the full character crests, especially the smaller top-panel placements. Print a paper proof at actual size first. |
| Surface engraving / etching | Use the black SVG as the mark area. Confirm the surface and material with staff. Fine facial details are surface marks, not thin printed walls. |
| Adhesive vinyl | Use the larger crest, transfer tape and a small weeding test. The fine floating islands need careful transfer. Convert role-name text to paths in the cutter software. |
| Laser through-cut stencil or acrylic | The current crests contain disconnected islands. They need bridges or a backing carrier before through-cutting. Do not cut them as a free-standing plate. |
| Raised / recessed 3D print | Use a simplified badge after enforcing the printer’s minimum feature size. The detailed crests are not directly qualified as FDM relief geometry. |

Artwork masters contain no drilling geometry. `layouts/*-top-art.svg` is the transparent decoration layer. `*-paper-template.svg` is a separate nominal fit-check drawing. Avoid engraving control holes or border construction lines by accidentally using a technical sheet as the art layer. Do not globally scale the enclosure to adjust a joint: change the relevant CAD parameter.

## UIC Engineering Makerspace preparation

Engineering Makerspace’s Voron guidance lists a 0.6 mm nozzle, 0.3 mm layers, approximately 2 mm minimum features and a 290 × 290 × 285 mm machine envelope. Actual part limits depend on orientation. It recommends 0.5 mm horizontal and 1 mm vertical separation for assemblies, bed contact, accessible supports and support-free internal geometry with 45° maximum overhang walls. Prototype in PLA. Submit closed non-self-intersecting STL meshes in millimeters. Staff choose orientation and settings. [UIC Digital Fabrication Lab](https://makerspace.uic.edu/make/digital-fabrication-lab/)

Treat those clearances as starting guidance, not a universal snap-fit formula. Print a small ledge/closure coupon in the intended material and orientation first. The reference CAD includes a ledge-fit study with 0.3 / 0.5 / 0.7 mm horizontal separation. It does not qualify the final retention mechanism. Professor permission is already provided.

## Measurements required before final STL release

Use `MEASURE_BEFORE_PRINT.csv`. Confirm actual breadboards first. Then record total installed component heights, joystick swing/click, sensor package, knob/bushing, switch/plunger, SG90 tabs and horn sweep, LCD PCB/window/backpack, buzzer, USB plug envelopes and final harness connector. Measure in the plugged-in condition. The board outline alone cannot establish the USB opening or wire-bend clearance.

Before releasing the complete models, check: actual-fit tray, fingertip reach, stable board retention, lid release without tools, cable pull resistance, full gate motion without rubbing, horn retention, USB access, Main Wi-Fi connectivity and loaded servo power. Full STL production and print submission follow these checks.

## Sources and design provenance

- Existing game: `images/explorer.png`, `images/magic-and-knowledge.png`, `images/title-screen.png`.
- [Arduino UNO R3 documentation](https://docs.arduino.cc/hardware/uno-rev3/) and [UNO R4 WiFi documentation](https://docs.arduino.cc/hardware/uno-r4-wifi/): nominal board geometry and supported interfaces.
- [TowerPro SG90 Digital](https://towerpro.com.tw/product/sg90-7/): nominal dimensions and supply guidance. Check the actual supplied variant.
- [Prusa design guidance](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135): fit and print-direction considerations.
- [Formlabs enclosure guide](https://formlabs.com/global/blog/designing-3d-printed-snap-fit-enclosures/): general removable retention design reference, not a substitute for UIC FDM parameters.

The reference artwork was generated with the built-in image tool using the existing game images, then converted into native one-ink SVG paths. Exact prompts are in `ART_PROMPTS.md`. No game artwork was overwritten. The CAD is a nominal mechanical study, not a claim of measured or physically tested fit.
