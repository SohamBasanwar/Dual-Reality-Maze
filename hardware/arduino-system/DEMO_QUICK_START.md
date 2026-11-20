# Dual-Reality Maze - demonstration setup and troubleshooting

## Starting the game

1. Power all three boards with their game sketches installed. Keep one game tab open.
2. Double-click Start Maze.bat in the main project folder. It starts the local bridge
   and opens http://127.0.0.1:8080 in your default browser. Keep the project folders together.
3. Choose Connect Main Wi-Fi in the panel at the bottom left. This requests a Windows
   connection to the saved DualRealityMaze profile. For a first-time laptop connection,
   select DualRealityMaze in Windows Wi-Fi and enter MazeDemo362, then click the game button.
4. Windows may say No Internet. Stay connected: the game runs locally and Main is the access point.
5. Check Explorer OK and Architect OK, live raw readings, and Main's RGB status.
   Red means startup/fault; green means hardware ready; blue means fresh Wi-Fi game feedback.
6. Center the joystick, calibrate if needed, fold the panel, and select Begin adventure
   or Skip the prologue · Play. The latter starts Chapter I directly.

Connecting in Windows alone is not enough: click Connect Main Wi-Fi inside the game too.
Node.js is required; no npm install is needed. Chrome or Edge is required for USB serial.

## Check before presenting

- Explorer: move in four directions, click, and cover/uncover the photoresistor.
  Light below 1000 activates Reveal. Readings of 1000 or above release it for the next
  cover. Reveal still follows the game's charge/cooldown and scene rules.
- Architect: turn the knob to select passages, then press D2 to toggle an allowed
  passage. Show the game state and physical servo agreeing. Closed/open pulse widths
  are 1200/1800 microseconds; confirm these fit the actual gate before adding a load.
- Main: show the LCD timer/status and RGB readiness. The buzzer beeps at startup.
- Use an early, familiar puzzle rather than spending the demonstration in story screens.
- Rehearse once using the same laptop, USB hub, cables, and power arrangement as the demo.

## If something fails

| Symptom | What to check |
| --- | --- |
| Batch file closes or does not open the game | Run Start Maze.bat from a terminal to read the error. Node.js and hardware/arduino-system/game.html must exist. The launcher pauses on errors. |
| Port 8080 occupied | Close the older game bridge that owns it; do not terminate an unrelated service blindly. Retry the launcher. |
| DualRealityMaze not listed | Check Main power and that Main's game firmware is running. If necessary power-cycle the boards. A laptop reconnect cannot repair a missing access point. |
| Laptop joins the network but controls do not work | Click Connect Main Wi-Fi inside the game. Only use one game tab. Check both controller statuses in its panel. |
| Explorer or Architect OFFLINE | With power off, check A4/SDA, A5/SCL, and common GND. Check correct sketch/address: Explorer 0x10, Architect 0x11. The LCD and both boards intentionally share the bus. |
| Knob/button wrong | Architect potentiometer wiper A0; button D2 to GND, using INPUT_PULLUP. Explorer joystick click also uses its own board's D2. |
| Reveal never activates | Confirm raw A2 crosses below 1000 when covered and back to at least 1000 uncovered. Check the 10 kOhm resistor and actual connected breadboard strips, not just wire proximity. |
| Servo jitters or boards reset | Check the power source and common ground. Use a suitable regulated servo supply for the loaded mechanism; USB hub power may not support servo peaks. Do not tie separately powered board 5V rails together. |
| LCD is blank | Check 5V/GND and SDA/SCL, backpack contrast, and bus wiring. Use Main's 5V SDA/SCL header, not Qwiic. |
| Red after a Wi-Fi loss | Movement stops; keep the joystick centered while reconnecting. Enabled automatic retries are limited to one every 15 seconds while the game tab is visible. |
| USB connection fails | Close Serial Monitor and other port users. Select Main, not an R3. USB upload/serial trouble was observed previously on this laptop; verify this fallback before relying on it. |

Wi-Fi records previously showed driver-reported disconnections. They did not identify
the underlying hardware/driver/power cause. Auto-rejoin mitigates the interruption;
it does not guarantee the link will never drop. Do not disable network protections
or change drivers immediately before the demonstration without a separate test.

Download diagnostic log in the game panel after a failure. It records readings,
connection events, and player coordinates. The bridge startup log is at
%LOCALAPPDATA%\DualRealityMaze\bridge.log. Disconnect stops further automatic join requests.

The November 20 checks cover software and compilation. No Arduino hardware was
detected at the start of that session; a fresh physical run is still required.
