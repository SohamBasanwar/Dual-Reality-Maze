# Dual-Reality Maze - Arduino submission

Course: CS 362  
Team Number: [TEAM NUMBER REQUIRED]

Replace the team-number placeholder in all three headers before submission.

| Member | NetID |
| --- | --- |
| Soham Basanwar | sbasan3 |
| Ronit Mishra | rmish |
| Prince Patel | ppate515 |

Each .ino begins with the team number, every member's name and NetID,
project name, and the same 100-word abstract. The submission instructions
do not require working code; these files also include the project's current
implementation. Keep each Protocol.h next to its .ino if compiling.

| Sketch | Board selection | Role |
| --- | --- | --- |
| Explorer/Explorer.ino | Arduino UNO | Joystick and photoresistor input; I2C address 0x10 |
| Architect/Architect.ino | Arduino UNO | Knob/button input and servo output; I2C address 0x11 |
| Main/Main.ino | Arduino UNO R4 WiFi | Poll controllers, drive LCD/RGB/buzzer, exchange laptop data |

Open each sketch separately in Arduino IDE. Board packages used for verification:
Arduino AVR Boards 1.8.8 and Arduino UNO R4 Boards 1.6.0.
Libraries: Servo 1.3.0 and hd44780 1.3.2. Wire and WiFiS3 are supplied by the board packages.
Select the correct physical board/port before uploading.

The laptop game and launcher remain in the main project folder; they are not
required dependencies for compiling these sketches and are not duplicated here.
The game's Reveal threshold is configured in the laptop adapter, not the Explorer
sketch: A2 below 1000 activates Reveal, and 1000 or above releases it.
The buzzer currently provides a startup beep; it does not play the game soundtrack.

Communication: Main polls both R3s over a shared wired I2C bus using different
addresses. The LCD shares that bus at its own address. Each R3 A4 goes to Main SDA,
each R3 A5 to Main SCL, and both grounds go to Main GND. Main's built-in Wi-Fi
connects to the laptop running the local game bridge.

Compilation and software checks do not verify wiring or mechanical operation.
See the project hardware/arduino-system/DEMO_QUICK_START.md for operation,
diagnostics, and the final physical check before demonstrating.
