# Power, status lighting and one-hour target

User decision, 24 October 2026: internal common store-bought rectangular 9V batteries, such as Duracell; at least one hour for presentation use. The photographed Hovxjzk rechargeable battery is an example, not the selected final cell.

## Mechanical battery allocation

Each bay reserves 30 × 61 mm in plan, with a 23 mm nominal height allocation. A common PP3 envelope is 26.5 × 48.5 × 17.5 mm including the battery terminals. The additional length is for the snap connector and a gentle lead bend; actual connector size still needs checking. A flexible pull ribbon should sit beneath the cell, clear of the latch. Disconnect by gripping the snap connector, not by pulling its wires.

Controller batteries occupy one grip. Main's battery is below its left-side service area. All have separate recessed battery doors. Changing batteries does not expose the breadboard or require opening the main shell.

## Electrical suitability

UNO R3 accepts 7–12 V at its appropriate VIN/barrel input; UNO R4 WiFi accepts 6–24 V. A fresh 9V battery is within these input ranges. That fact does not establish runtime or immunity to servo-induced voltage dips. Never connect unregulated 9V to a 5V pin, an RGB LED or the SG90.

Use a separate regulated servo branch, with common ground, local decoupling and suitable current capacity for the actual servo's measured peaks. TowerPro lists 4.8 V operation for its SG90; confirm the usable supply range of the supplied servo before setting a regulator. The regulator cannot make a weak battery deliver more power than it contains.

The R3's linear regulator dissipates approximately (Vin − 5 V) × board current. For illustration only, 9 V and 60 mA produce about 0.24 W of regulator heat. That 60 mA value is a scenario, not a measurement of this build. Main also powers Wi-Fi, LCD/backlight and indicators. The photographed rectangular speaker is not interchangeable with the piezo buzzer and must not be driven directly from a GPIO as a substitute.

No exact one-hour claim is justified yet. Manufacturer battery capacity and discharge curves depend on load and cutoff voltage. The 750mAh marking on a rechargeable example must not be treated as the capacity of an alkaline replacement.

## A real Main master button

The printed cap operates a small momentary switch. That switch must control a latching power circuit; it must not carry the servo load directly.

A candidate for the Main local battery is Pololu's Mini Pushbutton Power Switch LV (2808), whose external A/B switch connection supports a remote tactile button. It is a candidate, not an installed component. Its recommended voltage range includes 9V. Module height with wires/connectors, load temperature and final wiring must be checked.

Three independent batteries mean a Main-only power switch does not turn off the other boards. Complete shared control requires additional per-controller load switches and a designed master-enable/shutdown path (or an appropriately rated multi-pole mechanical arrangement). Do not tie the three positive battery terminals together. SDA/SCL are data lines, not a power-enable circuit. Unpowered-node I2C backfeeding must be prevented or isolated in the final circuit.

Reserve space in the opposite controller grip for power electronics and in the sleeved tether for additional control conductors, if required. The current CAD block is an allowance, not a selected module footprint. A simpler alternative is one local power switch per unit; that changes the requested single-button behaviour and has not been substituted without discussion.

## RGB status proposal

The images appear to include a four-lead LED, but its common-anode/common-cathode type, lead order and forward voltages are not established. The LED cup currently reserves a nominal 5 mm package. Use one current-limiting resistor per colour. Size these from the actual LED and driver voltage.

For a conservative direct-drive example only: a 5V output with a 1kΩ series resistor and 2–3V LED forward voltage gives roughly 2–3mA. UNO R4's published GPIO limit is 8mA per pin; a brighter emblem or a different LED needs a transistor driver rather than increased GPIO load. Also check total port/current limits. A dim room test will determine whether one LED illuminates the diffuser adequately.

Proposed indications: blue short startup pulse; green steady when all required connections are ready; amber slow pulse while waiting; red repeated double flash for a fault; purple slow fade for idle. Patterns accompany colour. Red can indicate a detected link error; a dead battery cannot be expected to keep an error light running. Keep the Explorer LDR outside the emblem's light path and test optical leakage.

## Runtime acceptance test before full-shell printing

1. Record the actual battery model, regulator settings and loaded voltages. Test each unit separately first.
2. Run the intended game for at least 60 minutes with LCD/backlight, Wi-Fi, RGB and representative gate movements active. Log resets, link errors, battery voltage, servo supply minima and regulator temperature.
3. Repeat using the intended demonstration batteries and the heaviest expected gate operation. Do not deliberately hold a stalled servo.
4. Verify startup/shutdown, battery removal, detached-controller behaviour and absence of I2C backpowering.
5. If the one-hour criterion fails, change the battery/source or power architecture before committing to full cases. An AA-based or regulated rechargeable pack could require a larger/different bay; it is not assumed to fit the PP3 reservation.

## Sources

- Arduino board comparison and input voltage: https://support.arduino.cc/hc/en-us/articles/9350551575964-What-s-the-difference-between-UNO-R3-and-UNO-R4-boards
- UNO R4 WiFi GPIO and power: https://store.arduino.cc/products/uno-r4-wifi
- SG90 manufacturer's dimensions and voltage: https://towerpro.com.tw/product/sg90-analog/
- Duracell Plus 9V data and load/cutoff qualification: https://www.duracell.com/wp-content/uploads/2020/02/9V-Duracell-Plus.pdf
- Common PP3 dimensional drawing: https://data.energizer.com/pdfs/522_ap.pdf
- Candidate power switch: https://www.pololu.com/product/2808
