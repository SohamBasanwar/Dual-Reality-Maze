# Dual-Reality Maze: three-board hardware system

21 November 2026. Explorer UNO R3 + Architect UNO R3 + Main UNO R4 WiFi.
The game remains authoritative for collisions, chapters, gate permissions and timing.
See VERIFICATION.txt for bench results.

## Files and installation

- Open Explorer/Explorer.ino, Architect/Architect.ino and Main/Main.ino separately in Arduino IDE.
- Select Arduino UNO for each R3, Arduino UNO R4 WiFi for Main. Select each board's actual port before Upload.
- Libraries: Servo (Arduino, tested 1.3.0), hd44780 (Bill Perry, tested 1.3.2). WiFiS3 and Wire come with the board packages. Tested packages: AVR 1.8.8, Renesas UNO 1.6.0.
- Keep all supplied header tabs beside each sketch: Protocol.h for all boards and CountdownBuzzer.h for Main.
- Main also compiles for an UNO R3 as a USB-only fallback; its Wi-Fi code is excluded automatically.
- Read WIRING.md and the CSV charts before powering anything. This replaces the earlier standalone ZIP test wiring where noted.

## First test: Main USB → laptop

1. Assemble with power disconnected. Initially leave the servo horn/mechanical load detached.
2. Power both R3 boards by USB. Power Main through a USB-C **data** cable to the laptop. Separate board 5 V rails stay separate; connect all signal grounds.
3. Upload the correct sketch to each board. Main Serial Monitor at 115200 baud prints one JSON sample every 50 ms. `eOK` and `aOK` should both become true. It also prints its Wi-Fi AP address at startup.
4. Close Serial Monitor before opening the game's USB connection; one program owns the port at a time.
5. Double-click the project-root `Start Maze.bat` or this folder's `Start Hardware Game.bat` (Node.js required). It starts the bridge and opens the hardware game in your default browser. USB serial requires Chrome or Edge. Repeated launches reuse the running bridge.
6. The **Main Arduino connection** panel opens at the bottom left. Choose **Connect Main USB** and select the R4. Do not also use the older Connect Explorer/Architect USB buttons.
7. Leave the joystick centered and click **Calibrate centred joystick**. Use Invert X/Y if needed. Fold the panel and choose Begin adventure or Skip the prologue · Play.
8. Check raw X/Y, light, pot and button counters. One click should increment the relevant counter once. A held button must not keep incrementing.
9. Reveal is enabled by default. With Dark reads lower checked, an A2 reading strictly below 1000 activates Reveal; 1000 or above releases it. Cover/uncover to create a new edge. Game charge/cooldown and scene rules still apply. The panel lets you tune the threshold. For a module whose readings rise in darkness, uncheck Dark reads lower.

## R4 built-in Wi-Fi → laptop

1. The same Main firmware starts the access point `DualRealityMaze`, password `MazeDemo362`. It needs no campus Wi-Fi credentials. This is a local demo network, not an Internet connection.
2. Disconnect any game USB session. Double-click Start Maze.bat, then choose **Connect Main Wi-Fi**. On Windows the bridge requests connection to the existing DualRealityMaze profile. If the profile is missing, join once in Windows Wi-Fi settings using the password above, then retry. Windows may report “No Internet”; stay connected. The game artwork is embedded.
3. The launcher automatically starts the bridge at http://127.0.0.1:8080 using Main address 192.168.4.1. No terminal command or npm install is needed. If an older or unrelated bridge occupies port 8080, close it before retrying; the launcher reports the conflict.
4. Watch live readings in the panel, then fold it to play. The bridge forwards input and game-state feedback to Main. Use only one game tab and one laptop to control the demo.
5. The USB-C cable can remain for power. The game uses either USB serial or Wi-Fi, not both at once. To remove the USB power cable later, supply the board appropriately; Wi-Fi is not wireless power.

The local bridge binds only to 127.0.0.1. It serves the game, input/feedback routes, a health check, and Windows Wi-Fi connection/status routes. It avoids direct browser cross-origin requests to the R4. No npm install is needed.

## What each control does

Explorer joystick moves/navigates. Its click confirms menus/comics, picks fruit where appropriate, or opens pause. Architect potentiometer selects one of five controls; its button confirms/toggles. Both retain the existing game scene locks and two-button pause gesture. Covering the LDR triggers reveal on an edge, subject to game restrictions.

The physical servo represents the **currently selected** passage's accepted open/closed state, rather than every button press. It closes outside active gameplay or if laptop feedback is absent for 1.5 seconds. The Architect initializes closed at startup and commands 0 degrees closed / 90 degrees open. It follows the currently selected mechanism, holds position during healthy gameplay, and releases pulses after settling closed for 900 ms at idle or on communication loss. These are nominal servo commands; verify actual travel unloaded before fitting the gate. Use a separate regulated 5V servo supply with common ground.

Only Main carries an RGB LED: red D9, green D5, blue D3 (680 ohms per color). Main A4 is SDA and A5 is SCL; the LCD may stay on the duplicate SDA/SCL header. Red indicates startup, a missing board, failed LCD or access-point initialization (USB can still operate without Wi-Fi). Green means the hardware is connected and waiting for the game. Blue means the game is exchanging feedback over USB or Wi-Fi. After feedback stops for 1.5 seconds, healthy hardware returns to green and the servo closes. Main LCD shows controller connectivity and game time. Four optional green LEDs breathe together from one transistor-controlled channel. The buzzer gives short 660 Hz / 85 ms countdown warnings: 300, 180, 120, 60, 50, 40, 30, 25, 20, 15, then 10 through 1 seconds remaining. All current chapters last 600 seconds. Pause, idle, expiry and stale feedback silence it; duplicate updates do not repeat a warning. Main D2 is reserved, not a working master power switch.

Packets: Explorer 0x10, Architect 0x11, 12 bytes with version, sequence, three 10-bit ADC readings, 16-bit press count, button level and XOR checksum. Main polls at 100 kHz every 25 ms. Sequence changes establish freshness; 500 ms without change marks a controller offline. The laptop releases movement on lost input. Button counters prevent duplicate polling from repeating presses. Feedback uses `S,gate,mode,seconds` over USB, or the same command through the local Wi-Fi bridge. Mode: 0 idle, 1 gameplay, 2 paused. I2C feedback is a separate four-byte checked packet; callbacks do not move the servo or read analog pins.

## Seeing and tuning the real movement

Once the boards are connected, the panel exposes live sensor readings and logs the game player's position. Download **maze-hardware-log.json** after moving, pressing each button, sweeping the potentiometer and covering the sensor. We can inspect that file and the running game to tune dead zone, direction, thresholds and response. Physical testing is still required; compilation is not proof that the wiring or actual mechanism works.

The hardware game is a separate copy of the current Story Edition. The original game and original test sketches remain unchanged. `maze-source/work/story/hardware-hub.js` is the editable laptop adapter. `hardware/build-hardware-game.mjs` rebuilds this copy from the current root Story Edition.

## Bring-up order

Test Main + LCD first; then add Explorer; then Architect without servo power; finally add the regulated servo supply and LEDs. If either controller is offline, check ground, SDA/SCL swaps, header selection and duplicate/missing pull-ups. A physically stuck I2C bus can still require powering down and correcting wiring. Never reconnect an unpowered peripheral to a powered signal bus. A compile-tested USB fallback is provided; see VERIFICATION.txt for the tested configuration.

## References

### Connection recovery update

The game stops movement when input is stale or a request fails. Center the joystick during recovery. With Rejoin Main Wi-Fi checked, repeated failures request reconnection at most once every 15 seconds while this game tab is visible. Disconnect cancels future retries and ignores late input responses; an already-requested Windows join may still finish. The bridge checks whether the laptop is already on Main's network before requesting a join. It does not reset Main or change Windows drivers or power settings.

Windows WLAN records for 11 November at 16:14:40 and 16:25:57 report DualRealityMaze being disconnected by the driver. Its saved profile uses manual connection and has AutoSwitch disabled. These records establish Wi-Fi link loss, but do not identify whether the adapter, interference, AP firmware, or power caused it. Manual connection also means Windows need not rejoin Main automatically. Recovery helps reconnection; it is not a proven cure for the underlying drop. Main's current firmware initializes its access point only at startup. If DualRealityMaze disappears, check Main power and restart it before retrying.

Download diagnostic log captures connection events, readings, and player coordinates. The bridge startup log is at `%LOCALAPPDATA%\DualRealityMaze\bridge.log`. No firmware upload is required for the launcher and Reveal threshold update.

### Hardware references

- UNO R4 WiFi 5 V GPIO and pinout: https://docs.arduino.cc/hardware/uno-r4-wifi/
- R4 Wi-Fi/AP examples: https://docs.arduino.cc/tutorials/uno-r4-wifi/wifi-examples/
- Arduino I2C/Wire and R3 32-byte limit: https://github.com/arduino/reference-en/blob/master/Language/Functions/Communication/Wire.adoc
- hd44780 library/auto-detect backpack: https://github.com/duinoWitchery/hd44780
- Servo library: https://github.com/arduino-libraries/Servo

Use WIRING.md as the connection reference for these sketches, rather than older project architecture documents.

## Response and USB update (21 November 2026)

The browser now attempts one combined input/feedback exchange every 50 ms, with no overlapping requests. Main writes one buffered HTTP response and only redraws changed LCD lines. This is a maximum polling cadence, not a guaranteed 20 Hz over Wi-Fi. The panel reports measured round-trip time.

USB requests its device picker in the click gesture, explicitly sets DTR/RTS, and can switch from Wi-Fi. Open the local game in Chrome or Edge, choose Main UNO R4 WiFi (currently COM5), and close Serial Monitor first. USB feedback no longer immediately expires due to an older loop timestamp.

With Ethernet Internet connected, Wi-Fi can stay on DualRealityMaze. Without Ethernet, that local network provides no Internet.

## Onboard maze animation and fault light

The built-in R4 matrix animates an Explorer dot and portal. The selected passage opens the pixel gate. During a detected fault the matrix displays an exclamation mark when the matrix itself is available. The connection panel names the affected controller, LCD backpack, matrix initialization or access point. The LCD backpack is checked every half second after discovery. Power loss on Main itself extinguishes its indicators.

For an individual sensor, turn the knob, cover and uncover the light sensor, move the joystick, or press the button while watching its reading. A stationary input or an open analog wire can give plausible readings. The servo provides no position feedback.
