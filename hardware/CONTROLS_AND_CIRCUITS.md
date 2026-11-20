# Controller mapping and circuit review

## Current integrated architecture

The latest user-confirmed design uses wired I²C from both R3s to Main, USB power for all boards and Main's built-in Wi-Fi for laptop data. See `CURRENT_HARDWARE_ARCHITECTURE.md`. The direct USB serial setup below remains the implemented prototype and does not constitute the target I²C/Wi-Fi firmware.

Reviewed the actual `sketch.ino` and `diagram.json` files in the Explorer, Architect and Main ZIPs. The originals are preserved.

## What the supplied circuits currently do

| Controller | Component | Pin in supplied sketch/diagram | Existing behavior |
|---|---|---|---|
| Explorer | Joystick horizontal | A0 | LEFT / RIGHT, with center dead zone |
| Explorer | Joystick vertical | A1 | UP / DOWN, with center dead zone |
| Explorer | Joystick click | D2, INPUT_PULLUP | Prints `Joystick Button: PRESSED` on a press |
| Explorer | Photoresistor module AO | A2 | Prints light readings; the test marks values below 300 as reveal |
| Architect | Potentiometer SIG | A0 | Selects one of five positions |
| Architect | Pushbutton | D2, external 10 kΩ pull-down | Prints a confirmation on a debounced press |
| Architect | Servo signal | D9 | Standalone sketch toggles its demo servo between 0° and 90° |
| Main | I²C LCD | SDA/SCL shown as A4/A5 on the simulated Uno | Shows DUAL REALITY / READY |
| Main | Buzzer | D6 | Plays two startup tones |

All three simulation diagrams identify their board as `wokwi-arduino-uno`. The Main ZIP does not establish that the physical board is an R4 WiFi. Use the actual board's labeled SDA/SCL pins when assembling it; this task does not change wiring or flash firmware.

The Explorer diagram also contains an unconnected 10 kΩ resistor. It is not used by the shown circuit. The Architect's 10 kΩ resistor is connected as its button pull-down and must remain for the supplied `INPUT` sketch. Neither resistor is a new game control.

The Explorer/Architect diagrams terminate A4, A5 and ground on breadboard rows, but the provided sketches have no `Wire` slave handlers or board-to-board exchange. Main's `loop()` is empty. These ZIPs are independent component tests, not a functioning R4 hub protocol.

## The game controls

**Either player's button advances a comic.** Players do not need to press together to continue. Near-simultaneous or duplicate presses advance only once.

| Game state | Explorer joystick | Explorer joystick click | Architect pot | Architect button |
|---|---|---|---|---|
| Title / chapter title / result | Navigate visible actions | Confirm highlighted action | Inactive | Confirm highlighted action |
| Comic | Up opens menu; directions never advance the comic | Continue | Inactive | Continue |
| Cinematic / flight / ritual | Up/down can reach available non-game actions; automatic scene plays | Does not skip the cinematic | Inactive | Does not toggle a passage or skip the cinematic |
| Chapter I / II maze | Move | Open pause menu | Select passage | Toggle selected passage |
| Chapter III path | Move | Open pause menu | Inactive | Inactive |
| Hidden Orchard | Move | Pick a nearby fruit when the needle reaches gold | Inactive | Inactive |
| Chapter III memory hunt | Move | Open pause menu | Select passage | Toggle selected passage |
| Pause / settings menu | Up/down selects; left/right adjusts sliders, dropdowns and checkboxes | Confirm | Inactive | Confirm |

During live play, pressing the two existing buttons within 160 ms opens the pause menu. This gives the orchard a pause action while retaining joystick-click fruit picking. Single gameplay actions wait for that short chord window. Comics confirm immediately and do not require a two-button chord.

After a scene change, release the joystick to center before moving again. This prevents an old held direction from leaking into a new scene. Buttons have a 280 ms browser guard in addition to any sketch debounce. Light readings trigger Chapter I reveal on an activation edge; holding the sensor active does not repeatedly trigger it. The game's original reveal cooldown still applies.

## Simplified interface

Open **Controllers / pause**, then enable **Simple controller interface**. Connecting a controller enables it automatically.

In that mode, optional Previous, Skip and Auto-play shortcuts are hidden from comics. Each comic keeps one Continue action. Extra cinematic skip buttons and laptop toolbars are hidden. Pause, voice/subtitle settings, replay dialogue, restart and title return are consolidated in the controller menu. Browser fallback casting selectors remain available in normal laptop mode; the controller mode exposes the simpler master settings.

Entering controller mode defaults comics to manual progression. Automatic progression can still be enabled deliberately in Voice & subtitle settings.

Keyboard/mouse controls remain available in laptop mode. Comics now use Enter/Space or Continue rather than arbitrary keyboard input. This prevents movement keys and joystick emulation from skipping story panels.

## Connect the existing test sketches

1. Load each controller's existing ZIP sketch using the appropriate Arduino board configuration. No firmware was uploaded by this task.
2. Connect the Explorer and Architect R3s to the laptop with separate USB cables. Close Arduino Serial Monitor so it does not hold the ports.
3. Open the rebuilt Story Edition in desktop Chrome or Edge. Open Controllers / pause.
4. Select **Connect Explorer USB**, then choose that board's port. Repeat for Architect. Browser device permission and port selection require this one-time laptop setup.
5. Center the joystick, then use Return to game. Both connections use the sketches' existing 9600 baud setting.

The adapter accepts existing messages such as:

```text
Direction: UP | X: 512 | Y: 200
Joystick Button: PRESSED
Light Level: 200 -> REVEAL ACTIVATED
Selected: Gate B | Potentiometer: 350
CONFIRMED: Gate B
```

It ignores startup messages and `Physical Gate: OPEN/CLOSED` debug text. Laptop collision, power limits and passage occupancy remain authoritative. The five knob positions select the current game's Gate A, Gate B, Gate C, Bridge A and Bridge B. The original sketch's fourth/fifth debug labels are `Bridge` and `Trap`; they describe the old test positions and do not add a trap to the game.

The public bridge is:

```js
mazeControllers.readLine('explorer', serialLine);
mazeControllers.readLine('architect', serialLine);
mazeControllers.press('explorer');
mazeControllers.press('architect');
mazeControllers.direction('UP'); // CENTER releases movement
mazeControllers.potentiometer(512, 1023);
```

An R4 relay can later feed these same functions, but the supplied Main sketch currently does not relay either controller. This implementation does not claim that a three-board hub exists.

## Physical limitations still to resolve

- The original Architect sketch moves its demo servo locally on every confirmation. It will also move when that button is used to continue a comic. The browser cannot undo a local firmware action. For a servo that reflects an accepted game gate rather than a demonstration toggle, the firmware needs a later laptop-state feedback path. The game ignores that demo-servo message.
- Sensor lighting direction and thresholds need calibration on the real assembly. This adapter follows the test's printed activation state rather than assuming that a raw sensor value universally means darkness.
- Serial parsing, game controls, menus and release behavior were exercised in browser tests with supplied message formats. No physical Arduino, servo, LCD, buzzer or inter-board bus was tested.
