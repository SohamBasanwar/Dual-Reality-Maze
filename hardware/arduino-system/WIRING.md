# Circuit and wire placement

All three large breadboards can be used; this is a breadboard wiring plan, not a custom PCB fabrication layout. Component pin order varies by module. Follow the printed terminal labels, not wire colour or a guessed photograph.

## Power and breadboard rails

Start with USB-powered boards for debugging. Each board's own 5V goes to its own red + rail; GND goes to its own blue/− rail. Join the ground rails between boards. **Do not join their separately USB-powered +5V rails.** Some full-size breadboard power rails split halfway: verify continuity and bridge the two halves of the same rail if required. The two sides of the centre trench are isolated; each five-hole row on one side is connected internally. Neither colour printing nor physical proximity proves continuity.

The Architect servo has a separate regulated 5V supply rated for at least 1A, with common GND. Its positive rail must not connect to the Arduino USB 5V rail. Add a 470–1000 µF electrolytic across the servo supply near its plug (observe polarity), and a 100 nF ceramic in parallel. A common PP3 9V battery is not a suitable direct servo supply. Never connect 9V to any 5V pin, sensor, LCD or servo. A battery option needs suitable regulation and a loaded runtime test; the earlier one-hour objective is not established.

## Explorer UNO R3

| Arduino pin | Connect to | Details |
|---|---|---|
| 5V | Joystick VCC; sensor supply | Own local + rail |
| GND | Joystick GND; local ground rail | Shared signal ground |
| A0 | Joystick VRx | Raw horizontal input |
| A1 | Joystick VRy | Raw vertical input |
| D2 | Joystick SW | Switch to GND; INPUT_PULLUP |
| A2 | Light-sensor node | Bare LDR: 5V → LDR → A2 → 10 kΩ → GND |
| A4 / SDA | Main header SDA | Same signal; do not connect twice |
| A5 / SCL | Main header SCL | Same signal; do not connect twice |
| GND | Main GND | Third conductor in the controller cable |

For a light-sensor module instead of a bare LDR: VCC→5V, GND→GND, AO→A2; DO unused. Do not add the bare-LDR divider on top of the module's existing divider. Use the game's polarity setting if needed.

Suggested bare-LDR placement on a standard numbered breadboard: put the sensor signal leg at e10 and its supply leg at e12; connect a10→A2 and a12→+5V. Put a 10 kΩ resistor from b10 to b15 and a15→GND. This uses three distinct row nodes. Place the sensor away from RGB light and fingers normally holding the board; an opaque barrier prevents internal light leakage. Joystick pins can connect through jumpers; do not force a module across rows that short its terminals.

On the small breadboard in this build, use three separate five-hole strips on the same side of the center trench. Strip A holds Explorer 5V and one LDR leg. Strip B holds the other LDR leg, the A2 jumper, and one 10 kOhm resistor leg. Strip C holds the other resistor leg and Explorer GND. A bare LDR works in either orientation. Use a jumper wherever two intended contacts sit on opposite sides of the trench.

## Architect UNO R3

| Arduino pin | Connect to | Details |
|---|---|---|
| 5V | One outer potentiometer terminal | 10 kΩ potentiometer |
| GND | Other outer potentiometer terminal | Swap outer leads if direction feels reversed |
| A0 | Potentiometer centre/wiper | Not an outer terminal |
| D2 | One electrical side of pushbutton | Other side goes to GND |
| D9 | Servo signal | Usually orange/yellow; check servo labels |
| A4/A5/GND | Main SDA/SCL/GND | Three-wire controller cable |
| NO Arduino power pin | Servo positive | External regulated +5V only |
| Common GND | Servo negative + external-supply negative | Signal reference must be shared |

**Button wiring change:** the old ZIP used a pull-down and active-HIGH input. This firmware uses INPUT_PULLUP and active-LOW. Remove that old 10 kΩ pull-down and rewire the button between D2 and GND. For a four-leg tactile button, identify the two internally connected pairs with a continuity meter. Use one leg from each opposite electrical side; legs in the same pair remain shorted even when not pressed. Straddle the breadboard centre trench where the package fits, then verify unpressed=open and pressed=closed before connecting D2. No external resistor is needed.

Put the servo power connections on a separately labelled rail, not the Arduino + rail. Keep its motor wires away from SDA/SCL and the potentiometer signal. The gate attaches to the supplied servo horn; test unloaded before installing any gate linkage.

The handheld controllers do not require RGB wiring.

## Main UNO R4 WiFi

| Main pin | Connect to | Details |
|---|---|---|
| USB-C | Laptop USB data port | 115200 serial + power for initial test |
| Header SDA (A4 equivalent) | Explorer A4, Architect A4, LCD SDA | 5V header bus; NOT Qwiic |
| Header SCL (A5 equivalent) | Explorer A5, Architect A5, LCD SCL | 5V header bus; NOT Qwiic |
| GND | Both R3 grounds; LCD GND; buzzer − | All signal grounds common |
| 5V | LCD VCC; Main local + rail | LCD backpack must be a 5V-compatible model |
| D3 | 330 Ω → RGB red | RGB common cathode to GND |
| D5 | 330 Ω → RGB green | Separate resistor |
| D9 | 330 Ω → RGB blue | Main RGB common lead goes to GND |
| D6 | Small passive piezo + | Piezo −→GND; use a driver for high-current/active buzzers |
| D10 | 100 Ω → logic-level N-MOSFET gate | Four green LEDs, optional channel below |
| D2 | Reserved, unconnected | No physical master-power switching implemented |

For the four green LEDs: Main +5V → **one 330 Ω resistor per LED** → LED anode. Join the four cathodes at the MOSFET drain. Source→Main GND. Gate→D10 through 100 Ω; gate→GND through 100 kΩ. Use a logic-level MOSFET specified to turn on at a 5V gate and verify its G/D/S pinout. Do not drive the four LEDs directly from one GPIO. The four LEDs fade together; there are not four separate animation channels.

For a common-anode RGB LED, common→local +5V and set RGB_COMMON_ANODE=true in that board's Protocol.h. Do not assume the longest pin or colour order without checking the specific LED. Modules with built-in resistors differ from bare LEDs.

## I2C interconnection and pull-ups

Main is the bus controller. Explorer is address 0x10, Architect 0x11. The hd44780_I2Cexp library discovers the compatible LCD backpack address/wiring (commonly 0x27 or 0x3F). No HC-12, Bluetooth or ESP32 add-on is needed.

Use each 30 cm cable for SDA, SCL and GND. Label both ends. Route SDA beside ground, keep the two branches short, and keep motor-power wiring separate. This length is reasonable to test at 100 kHz, but reliable operation must be checked on the assembled circuit.

One pull-up network belongs on the bus near Main: SDA→4.7 kΩ→Main +5V and SCL→4.7 kΩ→Main +5V **if equivalent pull-ups are not already fitted on the LCD backpack**. Check the backpack before adding them; multiple pull-ups in parallel lower the effective resistance. Do not add a pair at every board. This is not a connection between the boards' positive power rails. Use Main's labelled 5V SDA/SCL headers; the R4 Qwiic socket is a separate 3.3V bus and is unsuitable for this wiring.

Connect ground first while power is off, then SDA and SCL. Power all bus participants together for testing; avoid powering one board through another board's I2C pull-ups. If the LCD does not initialise, run the hd44780 library's I2CexpDiag example on Main with the controllers disconnected before restoring the complete circuit.

The CSV files repeat these terminal connections for assembly check-off. Breadboard hole numbers beyond the simple bare-LDR example are deliberately not guessed: actual module footprints and tactile-switch leg orientation must be checked.
