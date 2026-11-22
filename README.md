# Dual-Reality Maze

Two players share a ten-minute rescue mission. The **Explorer** moves through the maze and uncovers hidden paths. The **Architect** selects gates and bridges and changes which routes are open. Both watch the game on the laptop. When the Architect opens a passage, a servo on the handheld controller moves along with it.

| Chapter I · Using Reveal to find the route | Chapter II · Navigating the laboratory |
| --- | --- |
| ![Chapter I gameplay with the Reveal route visible](images/Reveal_Chapter1_Verified.jpg) | ![Chapter II gameplay in the laboratory maze](images/Chapter2_Maze_Verified.jpg) |

## Start playing on Windows

1. Install Node.js and Git LFS. Clone the project and download its game assets.

   ```powershell
   git lfs install
   git clone https://github.com/SohamBasanwar/Dual-Reality-Maze.git
   cd Dual-Reality-Maze
   git lfs pull
   ```

2. Power all three programmed boards and double-click **Start Maze.bat**. It opens the game at `http://127.0.0.1:8080`. For a fresh hardware build, follow the [illustrated wiring guide](output/pdf/Dual-Reality-Maze-Wiring-Guide.pdf) and [sketch installation instructions](hardware/arduino-system/START_HERE.md).
3. In the game's **Main Arduino connection** panel, choose **Connect Main Wi-Fi** or **Connect Main USB**. For Wi-Fi, join `DualRealityMaze` with the demo password `MazeDemo362` the first time. The game runs locally. For USB, use Chrome or Edge, close Arduino Serial Monitor, and select the **UNO R4 WiFi** in the port picker.
4. Center the joystick and choose **Calibrate centred joystick**. Check for `E:OK A:OK` on the LCD and a blue status light. Choose **Begin Adventure** for the story or **Skip the prologue · Play** for Chapter I.

## Components and controls

| Board and component | What you do or see | How it works and what it means in the game |
| --- | --- | --- |
| Explorer UNO R3 · joystick | Tilt to move. Release to stop. Press the stick inward to click. | A0 and A1 read the two axes. The game uses the dominant direction and ignores small movements near center. The D2 click advances comic panels, confirms menu choices, or opens the menu during Chapter I play. |
| Explorer · photoresistor and 10 kΩ resistor | Deliberately cover the sensor, then uncover it. | The voltage divider feeds A2. By default, a reading below 1000 triggers Reveal, highlighting a route toward the next objective. Returning to 1000 or above rearms the input. The chapter's charges and cooldown still apply. |
| Architect UNO R3 · potentiometer | Turn the knob until the desired mechanism is selected on screen. | The wiper on A0 reports the knob position. Its range selects among five mechanisms. Turning the knob selects one. The button operates it. |
| Architect · pushbutton | Press once to toggle the selection. During a comic, press to continue. | Pressing connects D2 to ground. The R3 counts each debounced press once, so holding the button does not keep toggling the gate. The laptop checks whether the move is allowed. |
| Architect · SG90 servo | Watch the horn when you open, close, or select another passage. | D9 commands **0° closed** or **90° open** for the selected passage. Selecting a closed gate after an open bridge returns the horn to 0°. The servo uses a regulated 5 V supply with common ground. |
| Main UNO R4 WiFi · 16×2 I2C LCD | Read the controller connections on the first line and mode/time on the second. | Main checks for fresh replies from both R3s and displays the remaining time supplied by the laptop. See the display key below. |
| Main · RGB status LED | Look for red, green or blue when starting or reconnecting. | Red uses D9, green D5 and blue D3, each through 680 Ω. The color reports hardware and game connection status. |
| Main · passive piezo buzzer | Listen for one startup chirp, then countdown beeps during play. | D6 sounds briefly when the timer crosses a warning point. The beeps get closer together as time runs out. |
| Main · optional four green LEDs | If fitted, the four lights brighten and fade together. | D10 controls a transistor that drives the LEDs. These are decorative. Use the separate RGB LED to check connection status. |

## Reading Main during a game

| Indicator | Meaning |
| --- | --- |
| LCD `E:OK A:OK` | **E** is Explorer and **A** is Architect. Each `OK` means Main is receiving fresh, valid input packets from that board. A `--` identifies the missing or stale controller. |
| LCD `READY`, `PLAY`, `PAUSE` | The second line shows game mode and time in minutes and seconds. For example, `PLAY 03:00` means three minutes remain in active play. `READY` means Main is outside active play or pause. Use the first line to check the R3s. |
| **Red RGB** | Normal briefly at startup. Persistent red means Main detected a fault, such as a missing controller, a missing LCD backpack, or Wi-Fi startup failure. The game panel names detected faults. To check an individual sensor wire, operate that control and watch its live reading. |
| **Green RGB** | Hardware is healthy and waiting for game feedback. If feedback stops for about 1.5 seconds, healthy hardware returns to green and the servo closes. |
| **Blue RGB** | A healthy Main is receiving fresh game feedback over Wi-Fi or USB. Blue and `READY` can appear together while the game is connected at a menu. |

The buzzer gives a **440 Hz startup chirp**. During each ten-minute round it uses the same short **660 Hz, 85 ms beep** at these times. Pausing silences the countdown. Repeated packets for the same second produce only one warning.

| Time remaining | When you hear it |
| --- | --- |
| Early warnings | Once at **5:00** (halfway), **3:00** and **2:00** |
| Final minute | At **1:00, 0:50, 0:40 and 0:30** |
| After 0:30 | At **0:25, 0:20 and 0:15** |
| Final ten seconds | Once each second from **0:10 through 0:01**. Silence at zero. |

## How the three boards communicate

![Wiring diagram showing Architect and Explorer connected to Main by A4, A5 and ground, with the LCD on the same bus](hardware/wiring-guide/04-three-board-i2c.png)

**I2C in brief.** Several devices share a data line (**SDA**) and a clock line (**SCL**). Pull-up resistors keep released lines high. The bus controller starts a transfer, clocks out a device address and a read/write bit, and exchanges bytes with that device. The receiver can acknowledge each byte on the ninth clock. A STOP releases the bus for the next transfer. Distinct addresses let several devices share the same two wires. [NXP I2C bus specification, section 3.1](https://www.nxp.com/docs/en/user-guide/UM10204.pdf)

**In this project**, Main controls the bus at **100 kHz**. Each R3 connects **A4 → Main A4 (SDA), A5 → Main A5 (SCL), and GND → Main GND**. The 5 V LCD backpack uses its own I2C address on Main's equivalent SDA/SCL headers. Each USB-powered board keeps its own 5 V rail.

1. Both R3s sample their controls independently. About every **25 ms**, Main asks **Explorer (`0x10`)** and then **Architect (`0x11`)** for their latest readings. Both players can act at once because their boards store the readings until polled. Button counters preserve short presses between polls.
2. Main checks the packet checksum and sequence number, then forwards the readings to the laptop by **Wi-Fi or USB serial**. The laptop handles movement, collisions, puzzle rules and the timer.
3. The laptop sends back the selected passage's accepted open/closed state, game mode and remaining time. Main updates the LCD, LED and buzzer and sends the gate state over I2C to Architect. This is why the physical horn follows the passage shown on screen.

[Demo and troubleshooting guide](hardware/arduino-system/DEMO_QUICK_START.md) · [Pin-by-pin wiring](hardware/arduino-system/WIRING.md) · [Submission sketches](submission/Final_Arduino_Submission) · [Game manual](MAZE_README.md)

## Source and assets

`maze-source/work` contains editable game code, chapter logic and assets.
`hardware` contains board firmware, the local server, adapter, build scripts and tests.
`images`, `voice`, and `trailer-kit` contain visual/audio assets and production sources.
`enclosure-design` retains historical enclosure design sources; those designs are
not certified print-ready and fabrication was discontinued for this project.

Generated game copies, CAD exports, render captures, local tools, private reference
photos, archives and most media/presentation exports are ignored. They remain on
the author's local disk. The completed origin trailer is retained with Git LFS.

To rebuild the hardware game after editing source:

```powershell
node hardware/build-hardware-game.mjs
node hardware/test-hardware-hub.mjs
node hardware/test-hardware-server.mjs
```

The firmware uses Arduino Wire/WiFiS3, Servo, and hd44780 libraries. External
dependencies retain their own licenses and are installed separately.

## License

Copyright (c) 2025 Soham Basanwar. All Rights Reserved.

This project uses the [proprietary license](LICENSE). Permission requests:
sohambasanwar@gmail.com.
