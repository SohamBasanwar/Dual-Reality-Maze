# Dual-Reality Maze — ergonomic revision 2

October 23, 2026. Current design study; supersedes the earlier half-breadboard enclosure layout. No printing form has been submitted. This revision contains editable OpenSCAD code, actual CAD previews, component layout drawings and one-color artwork. It is not a final fitted manufacturing release.

## Shape and comfort

Explorer and Architect share a 240 × 183 × 54 mm nominal body, excluding knobs and the Architect gate cage. A wide electronics bridge holds a full-size breadboard. Two rounded, outward-splayed handles extend below it, leaving a central finger recess. The bottom perimeter tapers inward over 8 mm; the upper perimeter tapers over 14 mm. Shallow 2 mm wide channels mark the grip pads. All major plan-view corners are rounded. The broad front body is a consequence of retaining a full Uno and full breadboard.

This is an ergonomic design direction, not a tested comfort claim. The handles are approximately 63 mm wide at their lower oval ends and up to 54 mm thick. They are deliberately larger than a retail controller. First evaluate a cardboard top silhouette and an empty shell or grip-only prototype with all teammates; check thumb reach, wrist posture, cable pull and ten minutes of holding. If small hands cannot comfortably reach the controls, reduce handle thickness locally or use a supported tabletop/lap position. Do not scale the whole model down because the breadboard would stop fitting. No palm-side spikes or fine abrasive texture.

The design draws on [Xbox's published controller design discussion](https://news.xbox.com/en-us/2020/03/16/xbox-series-x-controller/): sculpted grips, rounded contact areas and restrained tactile texture. The shell and fantasy graphics are project-specific. No Xbox dimensions or proven ergonomic performance are claimed for this design.

Main becomes a 240 × 180 × 66 mm rounded octagonal portal console. The LCD sits inside a portal frame, a recessed-control area identifies the crystal power button, and the portal crest occupies the lower face. Rear cables keep the front clear. It is a desktop console; angled LCD viewing can be evaluated with an external wedge before changing the enclosure's flat printable lid.

## Layout and clearances

Coordinates are millimeters from rear-left in top view; z=0 is the bottom. Reference component dimensions are in COMPONENT_REFERENCE.csv. Cable and jumper allowances are separate from component bodies. Component envelopes are visible in exploded CAD views; the colored gray blocks represent planning envelopes, not purchased hardware models.

| Enclosure | Lower tray | Upper/control placement |
|---|---|---|
| Explorer | Breadboard (37,18), envelope 166×55×10, bottom z=7; R3 (85,78), 68.6×53.4, reserved height20 | Joystick center(43,94), sensor center(197,94); crest centered near(120,42) |
| Architect | Same breadboard and R3 placement | Pot center(43,94); confirm button(197,84); servo body at(164.5,111.9,25), 23×12.2×29; nominal shaft/guard center(176,118) |
| Main | Breadboard (37,18); R4(28,105); power-distribution reserved zone(130,112), 80×42×22 | LCD PCB(79.7,27), 80.6×36 with 19 mm depth reserved; button(120,99); buzzer vent region around(197,114) |

The Architect's servo is right of the Uno, with about 10.9 mm between their body envelopes. Its tabs, shaft offset, horn and full motion sweep must be matched before producing a cradle. The cage is 58×34×27 above the lid; it is a separate nominal shell, not a tested safety guard. The complete Architect height is about 81 mm, or more if the final mechanism requires it. Keep the moving gate clear of fingers, wires and breadboard leads. A captured fork above the horn must replace the usual horn screw; it must retain axial movement without binding rotation. This keeper is not yet fitted or modeled.

Reserve roughly 20 mm above breadboard bodies for low-profile jumper bends, rather than packing wires against the lid. Main's LCD/backpack occupies z44–63, leaving 27 mm from the breadboard top to its lower envelope. Tall upright jumpers may exceed that space. Explorer's joystick occupies z30–50 and sits outside the breadboard footprint. The actual joystick cap swing must be checked against the 28 mm trial opening.

Route harnesses in perimeter gutters, held by reusable straps through printed saddles. The current rear exits are pigtail/grommet openings; they do not pretend to be fitted USB socket cutouts. Use short internal USB cables to the boards and a rear service connection. Leave access to reset, USB plugs and LCD contrast adjustment. Keep metal hardware, cable bundles and foil decals away from the R4 antenna area; determine its exact clearance from the actual board and manufacturer layout.

## Screwless service access

The CAD has 3 mm walls, floor and roof, component locating rails, a lid alignment skirt and strap saddles. Breadboard adhesive may secure it to a removable tray; do not glue the breadboard directly into an inaccessible shell. PCB retention should contact bare board edges, with insulating supports under permitted areas. Reusable straps or sliding wedges can secure the tray without screws. Never strap across a socket, solder joint, antenna or component.

Final lid locking keys, board-retaining clips, joystick/button brackets, servo cradle, horn keeper and cable grommets are still fit-dependent design work. The present lid skirt aligns the parts but is not a qualified latch. Do not mistake it for a finished snap-fit. A replaceable clip is preferable to a delicate integral PLA latch that breaks the whole shell. Prototype mating clearances before committing to all three housings.

## One master power button

Use a separate momentary pushbutton under a blunt faceted crystal cap on Main. It operates a latching electronic power-switch module connected ahead of all loads. One press turns on the distribution rail; another turns it off. It is distinct from the Architect gameplay button. A simple power switch requires no Arduino program, so it still works when all three processors are off.

```text
External regulated 5 V DC supply (mains adapter stays outside enclosure)
    -> input protection / correctly rated latching power-switch module
         <- crystal cap -> captured momentary switch -> control input
    -> protected star distribution in Main
         -> USB-C power lead -> Main R4 + LCD/buzzer logic
         -> USB-B power lead -> Explorer R3 + sensors
         -> USB-B power lead -> Architect R3 + controls
         -> dedicated regulated servo branch -> SG90 motor power
Common ground joins all boards, servo supply return and I2C reference.
SDA/SCL/GND run as signal wiring alongside, not as a power feed.
```

[Pololu 2808 LV](https://www.pololu.com/product/2808?coupon=25THANVC121) is a reference for the required latching behavior: it supports external momentary switches and switches load current electronically. It is a candidate, not a confirmed BOM choice or a guarantee of current capacity inside this enclosure. Select and thermally qualify the switch, source, connectors, wire and branch protection together using measured startup/servo load plus margin. Its maximum advertised current is not a safe enclosure operating target. Its PCB alone does not include USB outputs, fuses or strain relief.

The shared supply powers boards through their USB connectors using correctly wired power leads. It does not come from the Main Arduino's 5 V pin. Do not carry servo or combined system current through solderless breadboard rails or thin signal jumpers. Separate servo distribution avoids forcing motor current through logic power paths. The SG90 manufacturer's nominal voltage is 4.8 V; verify the actual servo's accepted supply range before connecting a nominal 5 V branch.

During programming, disconnect that board's shared USB power feed before plugging in a laptop USB cable. If other I2C devices are left unpowered, disconnect their bus branches or use appropriate isolation to prevent signal-line back-power. The master switch cannot shut off a board that is independently powered by a laptop. A ready-made USB-C source/pigtail must preserve the required connector signaling; do not assume a bare USB-C socket is a complete power interface.

The crystal in CAD is an aesthetic cap study (22 mm diameter, 10 mm tall). The guide, retaining flange, switch travel, hard stop and accidental-press recess need to match the selected momentary switch. It is not an electrically functional printed switch. A power symbol combined with the existing portal diamond can be applied in one color.

## Appearance and application

Use one filament color for each part and one ink color for decoration. Retain the Explorer lantern/young explorer crest, Architect caster/rune crest, and Main portal crest from the actual project artwork. Flat 56 mm crest patches sit on the controllers; Main uses a 42 mm portal emblem below its button. These are native SVG paths. The previews show gray housing with dark graphics only to distinguish material from markings.

For the first build, use a single-color sticker on the flat panel: clean, dry and degrease with a plastic-compatible method, test adhesion on a scrap, align using a paper guide, then apply from center outward. Avoid wrapping a large decal over compound grip curves. Keep grip artwork sparse and use small separate rune strips. Fine character details work better as printed stickers or engraving on a separate approved plaque than as cut vinyl. For vinyl, simplify details and test weeding at the final size. Through-cut designs need bridges for disconnected islands. Ask fabrication staff whether the specific substrate is suitable before laser marking; do not assume direct laser engraving of an assembled PLA enclosure is acceptable.

Large raised/debossed runes can be modeled into the plastic using sufficiently broad strokes. The detailed crest shown in the CAD assembly is a surface graphic visualization and is deliberately excluded from the exported base/lid solids. It is not validated FDM relief. This separates durable tactile shapes from fine artwork.

## UIC printing routes

[Engineering Makerspace](https://makerspace.uic.edu/make/digital-fabrication-lab/) accepts STL in millimeters and requires closed non-self-intersecting meshes. Its listed Voron build envelope is 290×290×285 mm; the proposed parts fit the nominal envelope, though staff still choose orientation and supports. Published guidance uses approximately 2 mm minimum features, a 0.6 mm nozzle, 0.3 mm layers and 20% gyroid; it recommends 0.5 mm horizontal and 1 mm vertical separation for multipart assemblies. These are starting guidelines, not an automatic snap-fit tolerance. Start in PLA and check the assembled fit. The current CAD skirt uses a provisional 0.5 mm gap per side, which must be evaluated with a fit coupon.

On October 23, the signed-in [Engineering submission page](https://project.mksp.uic.edu/projects/new) showed title, description, project category/reference, process, material, color, optional settings and file uploads; its 3D-printing selector accepted 3mf/obj/step/stl/stp and indicated a 50 MB upload limit. Only the process selector was inspected. No project details or files were entered and nothing was submitted. The user's latest instruction is to complete design before using the form.

The linked [College of Education ETL service](https://etl.ed.uic.edu/services/3d-printing/) is separate. It limits service to its college community, requires professor approval for students and director pre-approval, accepts STL only and asks for at least one week of notice. It requests purpose/course/professor, position, deadline and dimensions. It says prints are single-color, but gives no precise printer model variant, build envelope or mechanical-fit tolerances. Professor permission already obtained does not by itself establish ETL eligibility/director approval. Do not transfer RRB machine specifications to ETL.

## Code: what exists and what remains

| Area | Verified project state |
|---|---|
| Game/story code | Exists in maze-source/work; built Story Edition and later chapters present |
| Controller adapter | maze-source/work/story/controllers.js connects two separate USB serial ports at 9600 baud and exposes mazeControllers input hooks |
| Existing Arduino ZIPs | Explorer and Architect are component tests; Main initializes LCD/buzzer and has an empty loop |
| New enclosure CAD code | cad/ergonomic_enclosures.scad exists; role and part parameters generate the family |
| Three-board I2C transport | Not implemented in the supplied controller tests |
| Main built-in Wi-Fi game bridge | Not implemented in the inspected adapter/sketches |
| LCD/servo synchronized to game state | Not integrated; Architect's original servo is an independent demo toggle |
| Master power button | Electrical design proposal; needs selected switch/distribution hardware; basic latching operation needs no firmware |

For the integrated firmware, keep the laptop authoritative for maze rules. Main should poll debounced input snapshots/counters from both R3s, forward them to the laptop, and relay accepted game-state feedback to LCD/servo. A stale-link timeout must neutralize held movement and show a disconnected state. Use game-accepted passage state for the servo so a rejected move does not open it. Show READY only after both controller heartbeats and laptop link are live. These are implementation requirements, not a claim that firmware has been written or flashed.

## Release gate

Mesh checks establish only closed, positive-volume CAD solids. The physical parts, total mass, comfort, lid retention, component mounts, connectors, servo sweep, power rail behavior and I2C cable reliability have not been tested. The reference dimensions allow the layout to advance now. Exact module identification is still needed for final fitted openings: web dimensions cannot identify an unknown part already on the desk. Inspect the paper layout and empty grip prototype, then fit the mounts and export each manufacturing part to millimeter STL. Keep the current study out of the fabrication queue until that step is done.
