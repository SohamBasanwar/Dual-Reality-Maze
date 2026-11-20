# Dual-Reality Maze

A cooperative fantasy game with an Explorer controller, an Architect controller,
and a Main hub coordinating the physical controls with a laptop game.

## Windows setup

Install Node.js and Git LFS, then clone with Git so the large game assets are downloaded:

```powershell
git lfs install
git clone https://github.com/SohamBasanwar/Dual-Reality-Maze.git
cd Dual-Reality-Maze
git lfs pull
```

Double-click **Start Maze.bat**. The first launch builds the hardware-enabled game
from the Story Edition and controller adapter; subsequent launches reuse that file.
The launcher starts the local bridge and opens http://127.0.0.1:8080.
Using GitHub's source ZIP without resolving LFS files can leave asset pointers
instead of the playable game. Use the clone instructions above.

Power all three programmed boards. In the game, choose **Connect Main Wi-Fi**.
The default network is `DualRealityMaze` with demo password `MazeDemo362`.
Join once through Windows Wi-Fi settings if the network profile is not yet saved.
The access point does not provide Internet; the game runs locally.

## Hardware

| Board | Role | Devices |
| --- | --- | --- |
| Explorer UNO R3 | Movement and reveal, I2C address 0x10 | Joystick, photoresistor |
| Architect UNO R3 | Passage selection and gate control, I2C address 0x11 | Potentiometer, pushbutton, servo |
| Main UNO R4 WiFi | Poll controllers and exchange laptop data | I2C LCD, RGB LED, buzzer |

Both R3 boards connect to Main through SDA, SCL and common GND. Main communicates
with the laptop over its built-in Wi-Fi. This is not a fully wireless controller system.

- [Setup and troubleshooting](hardware/arduino-system/DEMO_QUICK_START.md)
- [Wiring and pin assignments](hardware/arduino-system/WIRING.md)
- [Arduino setup](hardware/arduino-system/START_HERE.md)
- [Submission sketches](submission/Final_Arduino_Submission)
- [Project manual](MAZE_README.md)

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
