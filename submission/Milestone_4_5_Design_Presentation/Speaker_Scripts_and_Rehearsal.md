# Presentation rehearsal guide

Soham: slides 1–4, trailer on slide 10 and thank-you on slide 11. Ronit starts on slide 5 and presents 5–6. Prince starts on slide 7 and presents 7–9. Full speeches are embedded in the PowerPoint notes.

Target: 9 minutes 26 seconds including the 101-second trailer and brief thank-you page. Rehearse with a timer; actual pace may differ. Do not read slides 1 and 2. Give the short team/project introduction and start explaining on slide 3.

Replace [NUMBER] with the actual group number in slide 1 and its opening speech. Bring the laptop with the deck downloaded and arrive at least ten minutes before the assigned slot. Follow the posted lab schedule: the handout contains conflicting date/year and weekday combinations. Submit the PDF for Milestone 4 before presenting; no submission has been made by this task.

The video is embedded on slide 10, with sound. Click it in Slide Show mode, then advance to the thank-you page on slide 11. The separate MP4 is a playback fallback. The PDF contains a still poster; play from the PowerPoint or MP4. If the technical discussion runs long, complete the required content first and offer the trailer after the timed talk.

## Rubric coverage

| Requirement | Slide |
|---|---|
| Team names and NetIDs | 1 |
| Project name and 100-word abstract | 2 |
| Project idea | 3 |
| Original work | 4 |
| Each Arduino’s role | 5 |
| I/O device types | 6 |
| Specific use of I/O devices | 7 |
| Communication between boards | 8 |
| Team roles, process, successes and issues | 9 |
| Soham’s closing trailer | 10 |

The planned I2C/Wi-Fi relay, accepted-state servo feedback, physical power design and runtime are presented as remaining integration work. The deck does not claim those have already been tested. Chapters IV–V remain planned. No controller CAD/STL imagery has been added.

## Slide 1: Our team — Soham
Target: 8 seconds.

Hi, we’re Team [NUMBER]. Our project is Dual-Reality Maze.

Soham starts here. Replace the group-number placeholder before presenting. Say the one-line introduction, then advance through slide 2. Do not read the names or NetIDs aloud.

## Slide 2: Dual-Reality Maze — Soham
Target: 2 seconds.

[Advance without reading the abstract.]

Do not read this slide aloud. Briefly show the project name and abstract, then advance to slide 3.

## Slide 3: Project idea — Soham
Target: 55 seconds.

Our project is a cooperative fantasy puzzle game where the two players have different controls. The Explorer moves through the maze and uses light to reveal hidden information. The Architect selects passages and decides which ones should be active. Because only two passages can receive power at a time, both players have to plan their route together.

The story connects the rescue of a princess to later challenges involving a cure and lost memories. The first three chapters are playable in the laptop prototype. Chapters four and five are planned. For this project, the important interaction is how physical controls let both players affect the same game state.

Explain the cooperative interaction using the game image. The cinematic trailer plays at the end on slide 10.

## Slide 4: Original work — Soham
Target: 55 seconds.

I developed the project concept, game design, story and the overall workflow connecting the characters, puzzles and controller actions. Our original game mechanic separates movement from control of the maze. The Explorer can find a route, but the Architect has to make that route usable.

The laptop also checks whether an action is valid in the current scene. For example, the same button can continue a comic or operate a passage during gameplay. This lets us use a small set of physical controls throughout the story.

The hardware work extends that design into a coordinated system with separate controllers and physical feedback. Ronit will now explain how we divide that functionality between the three Arduino boards.

Credit Soham’s established design and story contribution accurately. The hardware system is the proposed integration. Handoff: Ronit begins on slide 5.

## Slide 5: Roles of the three Arduinos — Ronit
Target: 58 seconds.

The design uses three Arduino boards, with one board for each member of our team. The Explorer UNO R3 reads the joystick, its built-in click switch and the light sensor. It converts those readings into movement and reveal inputs.

The Architect UNO R3 reads the potentiometer and confirmation button. It reports the selected passage and the button action. Its servo will show the gate state after the game accepts a change.

The Main UNO R4 WiFi polls both controllers, communicates with the laptop and updates the LCD and buzzer. The laptop remains responsible for collision, story progression and the puzzle rules. This division keeps local input reading on each handheld controller while Main coordinates the hardware.

Ronit starts here. Describe the target architecture. The supplied standalone sketches do not yet implement the complete I2C/Wi-Fi path.

## Slide 6: I/O device types — Ronit
Target: 55 seconds.

The planned build has eight different external device types. Our seven core types are the joystick, light sensor, potentiometer, pushbutton, servo, sixteen-by-two LCD and buzzer. We also plan one RGB status LED in each of the three boxes.

The Explorer has the joystick, light sensor and RGB LED. The Architect has the potentiometer, button, servo and RGB LED. Main has the LCD, buzzer and RGB LED. That gives every board at least two different device types.

RGB means red, green and blue. Those channels make one device type, even though they can mix to produce other colors. The joystick click also does not count as another type. The LED additions are planned hardware. Prince will explain the controls and status feedback.

RGB is the eighth planned external device type. One indicator is planned in each box. Do not count its three color channels as three types. The original seven core types already exceed the six-type minimum. Handoff: Prince begins on slide 7.

## Slide 7: How the controls work — Prince
Target: 62 seconds.

Here is one example of how the devices work together. During a maze, the Explorer moves with the joystick. The Architect turns the potentiometer to select a passage, then presses the button to request a change. The laptop checks the passage rules and available power. If it accepts the action, the screen changes and the accepted gate state returns to the Architect’s servo.

The light sensor supports the reveal mechanic. On a comic screen, either player’s existing button can continue the story, so we do not need another button just for dialogue. Directional movement does not skip comic panels.

Main’s LCD shows the game or connection state, and the buzzer marks events. The planned RGB indicators show blue when powered, green when connected and red for a fault. The integrated hardware feedback still needs bench testing.

Prince starts here. Explain the example in order. Accepted-state servo feedback is planned integration; the standalone servo test currently operates locally. The color meanings are the proposed firmware mapping. Verify the actual RGB part, common-anode or common-cathode wiring, current-limiting resistors and available pins before assembly.

## Slide 8: Communication between boards — Prince
Target: 80 seconds.

Main controls the wired I2C bus and polls the two UNO R3 controllers at separate addresses. The LCD shares the bus. Each controller cable is planned to be about thirty centimetres long, with SDA, SCL and common ground. We will check the pull-ups and signal reliability on the actual wiring.

Main exchanges events with the laptop over its built-in Wi-Fi. The laptop validates actions and returns accepted state for physical feedback. The complete relay still needs implementation and bench testing.

Our fallback is to replace Main with a third UNO R3 and connect it to the laptop through USB serial. That still requires working inter-board communication and firmware changes, so replacing the board alone would not fix a wiring or power fault.

The three-ESP32 setup is a future wireless feature. Adding an ESP32 only to Main would leave the controller cables in place. For fully wireless connections, we would put one ESP32 in each box and add a network bridge for the laptop game.

Keep the current R3–R4 design as the primary architecture. Explain the USB backup briefly. The three-ESP32 design is feasible, proposed and untested. Do not promise that replacing Main cures a wiring or power fault.

Backup details for questions (not read aloud):
1. The UNO R3 and the main UNO R4 header I2C bus both operate with 5V logic. Use Wire on the R4 header, not its separate 3.3V Qwiic/Wire1 interface. A different CPU architecture does not itself prevent I2C communication. Check common ground, unique addresses, pull-ups, packet layout and servo supply before changing boards.
2. An R3 Main can poll both R3 peripherals and the LCD while forwarding compact input/state packets over USB serial. Keep the game and media on the laptop, since the R3 has only 2KB SRAM. The present game adapter opens role-specific USB ports at 9600 baud; a single combined Main stream needs a role-tagged parser and a return-state path. This is feasible engineering work, not already implemented. Replacing R4 leaves the inter-board I2C link in place.
3. The agreed fallback is an R3 Main with USB serial. Adding an ESP32 only to an R4 Main leaves the wired I2C controller connections unchanged and does not resolve a fault on that bus. The R4 already has built-in Wi-Fi. Reserve three ESP32s for the future fully wireless feature. In that future design, an R3-to-ESP32 UART link needs suitable 5V/3.3V level conversion and common ground. The R3 hardware UART is shared with USB, so serial pin allocation and programming/debug access must be planned.
4. Fully wireless option with three ESP32s: Explorer R3 communicates internally with its ESP32; Architect R3 communicates internally with its ESP32; a third ESP32 in Main acts as the network gateway. Main can retain an R3 for its local outputs, or the ESP32 can take those tasks with compatible interfaces. Main creates a local Wi-Fi access point; the two handheld ESP32s and laptop join it. Inter-box data uses ordinary Wi-Fi with framed packets, controller IDs, sequence numbers, heartbeats and reconnect handling. The laptop needs a network bridge feeding the existing game input adapter and returning accepted state. No internet is required. There are still short internal wires and independent batteries in each box.
5. ESP-NOW is another option for the handheld links, with an ESP32 gateway forwarding to the laptop over ordinary Wi-Fi. A standard laptop does not directly use the ESP-NOW peer API. The radios must share the appropriate Wi-Fi channel; acknowledgements, duplicate filtering and timeouts remain necessary. Ordinary Wi-Fi throughout is the simpler first wireless implementation to investigate.
6. Use regulated power sized for the selected ESP32 board and radio peaks, plus a separate suitable servo supply. The UNO R3 3.3V pin is rated at 50mA, so do not use it to supply an ESP32 radio. Do not connect 9V directly to an ESP32 supply or GPIO. A one-hour runtime from a PP3 battery remains unverified and needs a loaded test.
7. If the I2C bus itself remains unreliable, a polled RS-485 link with a transceiver at each board is a possible wired redesign. RS-485 is another possible redesign rather than the committed fallback. Connecting every board separately by USB is useful for diagnostics, but does not by itself demonstrate direct communication between the microcontrollers.

## Slide 9: Team process and current progress — Prince
Target: 70 seconds.

Our planned hardware responsibilities are Explorer integration for Ronit and Architect integration for me. Soham leads the game, story and overall software workflow. Main-board integration and end-to-end testing are shared responsibilities. We will agree on the packet format first, verify each controller separately, then test the combined system with the same game actions.

The current success is the playable laptop prototype, including its story flow and controller-aware actions. The supplied sketches also give us separate component tests to build from. The complete three-board communication and feedback system still needs implementation and physical verification.

Our main risks are reliable communication, servo power and battery runtime. We are considering internal nine-volt batteries, but we still need regulated servo power and a one-hour loaded test. Our next checkpoint is a complete input-to-game-to-feedback test. Soham will close with the story trailer.

Present the teammate assignments as the plan. Handoff to Soham for the closing trailer on slide 10.

## Slide 10: Cinematic story trailer — Soham
Target: 113 seconds.

To finish, this trailer shows the world and story behind the game. It combines the laptop prototype with cinematic previews. Chapters four and five are planned.

[Play the full 101-second trailer once. Stay silent during playback.]

[After playback, advance to the thank-you slide.]

Soham resumes here. Play the embedded movie on slide 10, then advance to slide 11 for the closing line. Keep the presentation within ten minutes.

## Slide 11: Thank you — Soham
Target: 8 seconds.

Thank you for exploring Dual-Reality Maze with us. We’re happy to take your questions.

After the trailer, advance here. Pause, face the audience and deliver the closing line. Leave this slide visible during questions.
