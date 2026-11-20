# Three-person presentation guide

Use PowerPoint slide positions, not the small footer numbers. The normal run has 13 visible slides. Six hidden slides remain Q&A support. Soham presents the cinematic trailer. Only the marked spoken sections are meant to be read aloud. Ronit and Prince can adapt their optional wording while retaining the facts.

| Presenter | Main slides | Focus |
| --- | --- | --- |
| Soham | 1, 2, 3, 5, 6, 19 | Introduction, cinematic trailer, story and closing |
| Ronit | 8, 9, 11 | Hardware, input/output devices and communication |
| Prince | 13, 14, 15, 17 | Original work, materials, schedule and responsibilities |

Hidden support: 4 and 7 (Soham), 10 and 12 (Ronit), 16 and 18 (Prince). Suggested rehearsal target: about 8–9 minutes including the 101-second trailer, adjusted to the actual class time. Group number remains a placeholder. Detailed 3D modelling is the next separate task after the user supplies the reference image.

## Slide 1: Dual-Reality Maze

SOHAM — MAIN PRESENTATION — about 20 seconds

READ ALOUD
“Hi everyone. I’m Soham, and I’m presenting with Ronit Mishra and Prince Patel. Our project is Dual-Reality Maze: The Architect’s Oath. It is a cooperative fantasy game where two players solve the same maze through different physical controls. I’ll introduce the game and story, Ronit will explain the hardware, and Prince will cover the project plan.”

PRESENTER CUES — DO NOT READ ALOUD
Face the audience for the first sentence. Advance to slide 2 yourself. The group number is still a placeholder: replace it before the assessed presentation, and do not read “[NUMBER]” aloud.

RUN ORDER FOR ALL THREE SPEAKERS
Soham: slides 1, 2, 3, 5, 6. Ronit: slides 8, 9, 11. Prince: slides 13, 14, 15, 17. Soham closes on slide 19. Slides 4, 7, 10, 12, 16 and 18 stay hidden and are Q&A support only. These are PowerPoint positions in the 19-slide file, not the small printed footer numbers. Rehearse for roughly 8–9 minutes including the 101-second trailer, then adjust to the assigned class time.

AVOID
Do not claim the complete physical system is already finished. Read only the READ ALOUD section, not the cues.

## Slide 2: Project overview

SOHAM — MAIN PRESENTATION — about 30 seconds

READ ALOUD
“The two players have different jobs. The Explorer moves through the maze, finds items and reads the route. The Architect selects gates and bridges to make a path possible. Only two passages can stay powered at once, so they need to coordinate. The laptop displays the game world, while three Arduino boards form our planned physical interface: one for each player and one Main controller.”

PRESENTER CUES — DO NOT READ ALOUD
Point once to the maze image when explaining the two roles. Use ‘planned physical interface’ to distinguish it from the playable laptop prototype.

NEXT LINE
“Before we go into the hardware, I’ll show you the world this interaction is designed for.” Advance to slide 3.

AVOID
Do not describe this as a single-player game or say that each person needs a separate laptop. The story has five planned chapters; the current playable prototype covers Chapters I–III.

## Slide 3: Cinematic story trailer

SOHAM — MAIN PRESENTATION — about 20 seconds of speech plus the 101-second movie

BEFORE PLAYBACK — READ ALOUD
“This trailer introduces the kingdom, the two heroes and the attack that brings them together. It combines footage from the laptop prototype with cinematic story previews. Chapters Four and Five show where the story is going and are marked Coming Soon.”

PLAYBACK CUES — DO NOT READ ALOUD
Start the embedded movie in Slide Show mode. Confirm that laptop audio is audible before presenting. Let the entire movie play without talking over the King or narrator. The correct movie is Dual_Reality_Maze_Origin_Trailer.mp4, approximately 1 minute 41 seconds. Do not open or play older hidden movie objects. If playback fails, use the same local MP4, or briefly describe the rescue premise and continue without repeatedly troubleshooting in front of the audience.

AFTER PLAYBACK — READ ALOUD
“That is the story arc. The gameplay underneath it depends on the Explorer and Architect working together.” Advance to slide 5; hidden slide 4 is skipped automatically.

AVOID
Do not call every cinematic shot playable gameplay or claim that all five chapters are implemented. Do not narrate the movie while it is speaking.

## Slide 4: Two players, complementary controls

SOHAM — HIDDEN SUPPORT SLIDE — Q&A only

USE ONLY IF ASKED
“The Explorer handles movement and collecting objectives. The Architect changes selected gates and bridges. They share one maze state, and only two passages can remain powered at a time. That limit makes communication between the players part of the puzzle.”

CONTEXT
Use this slide to explain why two people are needed. The laptop keeps collision rules and progression authoritative; physical input requests an action rather than bypassing the game rules.

AVOID
Do not insert this slide into the normal talk or repeat the full overview. Do not say the Architect moves the Explorer directly.

RETURN
After answering, return to the closing slide or the slide where the question began.

## Slide 5: Five chapters, one complete story

SOHAM — MAIN PRESENTATION — about 25 seconds

READ ALOUD
“The story is planned across five chapters. The first three are playable in the laptop prototype. Chapter One introduces the rescue and the three runes. Chapter Two follows the search for a cure in the sky gardens. Chapter Three recovers the Princess’s lost memories. Each chapter builds on the same cooperative controls while introducing a different objective. The final two chapters complete the story we are planning.”

PRESENTER CUES — DO NOT READ ALOUD
Move left to right across the three images. Keep this to the main objective of each chapter. Advance to slide 6.

AVOID
Do not say the whole five-chapter game is finished. ‘One complete story’ refers to the planned narrative arc. Do not walk through every puzzle or spoil every ending.

## Slide 6: The story continues

SOHAM — MAIN PRESENTATION — about 20 seconds

READ ALOUD
“These are the two planned final chapters. The Clockwork Citadel uses rotating routes and machinery to restore a bell and reveal the Hollow King’s plan. The Heart Beyond the Veil brings the earlier mechanics together for the final bindings and reunion. These images show the direction we are working toward; both chapters are still Coming Soon.”

HANDOFF — READ ALOUD
“Ronit will now explain how the physical controllers support the game.” Ronit continues on slide 8; hidden slide 7 is skipped automatically.

PRESENTER CUES — DO NOT READ ALOUD
Point to each Coming Soon label. Keep the future content brief so it does not overshadow the required hardware design.

AVOID
Do not describe these images as completed levels or promise that optional chapter expansion will take priority over hardware integration.

## Slide 7: Story and gameplay workflow

SOHAM — HIDDEN SUPPORT SLIDE — Q&A only

USE ONLY IF ASKED
“The game moves through a title screen, comic, automatic cinematic, active play and a result screen. During a comic, either the Explorer’s joystick click or the Architect’s button means Continue. During gameplay, those controls return to their gameplay actions. The current scene decides what an input means.”

CONTEXT
The laptop-side scene guards prevent movement from skipping a comic or a comic confirmation from operating a gate. Story transitions lock normal gameplay controls. Physical transport of these events is a separate integration step.

AVOID
Do not say every control is active in every scene. Do not imply that automatic cinematic playback needs repeated button presses.

RETURN
Resume the original slide or the closing Q&A slide after the answer.

## Slide 8: Three-board hardware architecture

Ronit starts here.

RONIT — MAIN PRESENTATION — about 45–50 seconds

START WITH
“The hardware is divided into three boards, with a different responsibility for each.”

CONTEXT TO COVER IN YOUR OWN WORDS
Explorer Uno R3 reads the joystick and light sensor. Architect Uno R3 reads the potentiometer and pushbutton and provides a servo output. Main Uno R4 WiFi polls both controllers over the wired I²C bus, handles the LCD and buzzer, and relays data to the laptop using its built-in Wi-Fi. The laptop displays the game and decides which actions are valid. The approximately 30 cm controller links are wired.

OPTIONAL WORDING
“The two R3 boards collect local inputs, and the R4 coordinates communication. We use short wired I²C connections between boards, then the R4’s built-in Wi-Fi for the laptop link. This separates the controller roles while keeping one game state on the laptop. This is the planned integrated architecture; the complete physical connection still needs testing.”

AVOID
Do not mention HC-12 or Bluetooth as part of this design. Do not say the end-to-end bus and Wi-Fi relay are already implemented or tested. The R4’s 3.3 V Qwiic connector is not the proposed 5 V header bus.

NEXT
“The next slide shows the devices attached to each board.” Continue to slide 9.

## Slide 9: Inputs and outputs meet the device requirement

RONIT — MAIN PRESENTATION — about 35–40 seconds

START WITH
“The device choices give both players a distinct role and meet the project’s hardware requirement.”

CONTEXT TO COVER IN YOUR OWN WORDS
There are three microcontrollers and seven external device types: joystick, light sensor, potentiometer, pushbutton, servo, LCD and buzzer. The Explorer has the joystick and light sensor. The Architect has selection and confirmation controls plus the servo. Main provides status and sound output.

OPTIONAL WORDING
“The joystick controls movement, while the light sensor supports the reveal mechanic. The Architect selects with the potentiometer and confirms with the button. The servo represents a physical gate, while the LCD and buzzer give feedback. Counting device types, this gives us seven, compared with the minimum six required for our three-person group.”

AVOID
Do not count the joystick click as an eighth device type. ‘Servo feedback’ means visible physical output; we are not claiming that the SG90 measures and reports its shaft angle. Device count alone does not prove integration is complete.

NEXT
“Here is how these inputs are intended to reach the game.” Continue to slide 11; hidden circuit slide 10 is skipped automatically.

## Slide 10: Initial circuit connections

RONIT — HIDDEN SUPPORT SLIDE — Q&A only

USE ONLY IF ASKED
“These are the initial pin assignments from the supplied circuits. The Explorer uses A0 and A1 for the joystick axes, D2 for the joystick click and A2 for the light reading. The Architect uses A0 for the potentiometer, D2 for the button and D9 for the servo signal. Main connects the LCD and controller bus on SDA and SCL, with the buzzer on D6.”

TECHNICAL CONTEXT
Explorer click uses INPUT_PULLUP; the supplied Architect button has an external 10 kΩ pull-down. Use a common ground. The standard R3 bus pins are A4/SDA and A5/SCL. Main uses its labelled SDA/SCL header interface. Use USB power and suitable regulated 5 V servo support. These are initial assignments requiring physical verification.

AVOID
Do not wire the 5 V bus into the R4’s 3.3 V Qwiic connector. Do not claim this diagram proves that the complete circuit has run successfully. Do not read every pin in the main presentation.

RETURN
Return to the original slide or closing Q&A slide.

## Slide 11: Communication plan and software sketch

RONIT — MAIN PRESENTATION — about 45–50 seconds

START WITH
“This sketch shows the planned flow from a physical input to an accepted game action.”

CONTEXT TO COVER IN YOUR OWN WORDS
Each R3 reads and debounces inputs, then replies when Main polls it. Main forwards the data to the laptop. The laptop checks the current scene, collision rules and passage-power limits before accepting an action. Accepted state returns for the display, buzzer and intended servo response. Button edges and sequence numbers help prevent a held or repeated packet from becoming repeated actions.

OPTIONAL WORDING
“For example, pressing the Architect’s button requests a gate change. The laptop first checks whether that change is allowed. The physical output should follow the accepted result, so the servo agrees with the game rather than moving independently. The diagram is proposed pseudocode for the integrated firmware. The laptop input mapping exists, but the complete I²C and Wi-Fi relay still needs implementation and real-board testing.”

AVOID
Do not present the pseudocode as firmware already running on all three boards. A local servo test is not the same as accepted-state control. Do not promise measured latency or reliability figures that have not been measured.

HANDOFF
“Prince will now explain the original work, materials and remaining development plan.” Prince continues on slide 13; hidden slide 12 is skipped automatically.

## Slide 12: One button action depends on the scene

RONIT — HIDDEN SUPPORT SLIDE — Q&A only

USE ONLY IF ASKED
“The same physical button has a different meaning depending on the scene. Either button can confirm or continue during menus and comics. In active play, the Architect button requests the selected passage action, and the Explorer click can collect fruit in the orchard. Directions move or select; they do not skip dialogue.”

TECHNICAL CONTEXT
The laptop prototype includes scene-aware input mapping and centering guards to prevent carry-over. A two-button press within the configured 160 ms window opens the pause menu. These are laptop-side behaviors; integration with the wired physical controllers remains a separate test.

AVOID
Do not imply that holding a button sends unlimited confirmations. Do not describe every button as a permanent extra keyboard key. Do not claim the legacy local servo test already follows accepted game state.

RETURN
Return to the question’s original slide or closing Q&A slide.

## Slide 13: Original work in the project

Prince starts here.

PRINCE — MAIN PRESENTATION — about 30 seconds

START WITH
“The original work is how the story, cooperative mechanics and physical controls fit together.”

CONTEXT TO COVER IN YOUR OWN WORDS
Explain asymmetric player roles, the limit of two powered passages, scene-aware controls and chapter-specific objectives. Attribute the project concept, game design, story and overall workflow to Soham, as shown on the slide. Keep that attribution separate from proposed hardware responsibilities.

OPTIONAL WORDING
“Soham developed the concept, game design, story and overall workflow. The Explorer and Architect have different abilities, and the two-passage power limit makes coordination necessary. The story also changes what the controls mean, so the physical interface supports both dialogue and gameplay. Our next implementation work connects that design to the controller hardware.”

AVOID
Do not say that every component or library was invented by the group. Do not claim all five chapters are playable or assign completed contributions without evidence. Keep the credit factual and professional.

NEXT
“These are the materials needed for that physical build.” Continue to slide 14.

## Slide 14: Expected materials

PRINCE — MAIN PRESENTATION — about 30–35 seconds

START WITH
“The materials are organized around the two player controllers and the Main unit.”

CONTEXT TO COVER IN YOUR OWN WORDS
One Uno R4 WiFi, two Uno R3 boards, the seven device types, full-size breadboards, USB leads and approximately 30 cm I²C cables. Power is USB, with suitable regulated 5 V support for the servo and a common ground. Printed housings and a master-switch arrangement are planned.

OPTIONAL WORDING
“The two handheld controllers need room for their Arduino, a full-size breadboard and accessible controls. Main holds the R4, LCD and buzzer. We are using USB power and a regulated servo branch. Before finalizing the housings, we will measure the actual boards and modules, check cable exits and provide strain relief and service access.”

AVOID
Do not mention 9 V batteries, battery holders or wireless-module compartments; those are no longer the chosen design. Do not claim the enclosures are print-ready or that a master switch can power every unit without a verified power design. Detailed enclosure modelling follows the presentation and the supplied reference image.

NEXT
“The schedule places integration and testing before the final demonstration.” Continue to slide 15.

## Slide 15: Week-by-week development schedule

PRINCE — MAIN PRESENTATION — about 35–40 seconds

START WITH
“The next priority is completing and testing the physical system.”

CONTEXT TO COVER IN YOUR OWN WORDS
Summarize phases rather than reading every table row. The schedule uses 2026: design presentation Monday October 26, demonstration Monday November 23. It reserves time for the bus prototype, R4 relay and accepted-state feedback, then end-to-end hardware and failure-recovery tests, followed by enclosure fit and rehearsal.

OPTIONAL WORDING
“After the design presentation on October 26, the main work is the I²C connection, the R4’s Wi-Fi relay and feedback from accepted game state. We then test the full system, power behavior and recovery from disconnections. Enclosure fit and rehearsal come before the November 23 demonstration. The earlier October rows show our planned checkpoints, not evidence that every task has already been completed.”

AVOID
Do not claim a past milestone was submitted on time unless that has been confirmed. Do not use the inconsistent 2025 dates from the original rubric. Do not promise optional new chapters at the expense of the required physical demonstration.

NEXT
“To keep that work accountable, each task needs a clear owner and evidence.” Continue to slide 17; hidden slide 16 is skipped automatically.

## Slide 16: Verification and remaining integration

PRINCE — HIDDEN SUPPORT SLIDE — Q&A only

USE ONLY IF ASKED
“The laptop prototype has three playable chapters and checks for story navigation, scene locks, input handling and passage-power limits. The remaining integration is the actual I²C bus, R4 Wi-Fi relay, servo response to accepted state, physical calibration and power checks, followed by a complete demonstration with the boards.”

CONTEXT
Separate software evidence from physical evidence. The trailer’s recorded voices and cinematic playback are separate from a complete in-game actor-recording rollout. Ronit can add hardware details if needed.

AVOID
Do not say that software checks prove the physical build works. Do not invent a completed board-to-laptop test, measured latency or final enclosure fit. Do not describe the 3D models as approved for printing before measurement and fit checks.

RETURN
Resume the original slide or return to the closing Q&A slide.

## Slide 17: Team responsibilities and commitment

PRINCE — MAIN PRESENTATION — about 35 seconds

START WITH
“This is the proposed division of implementation work and how we will track it.”

CONTEXT TO COVER IN YOUR OWN WORDS
The slide assigns Soham game design, story, workflow, laptop integration and presentation; Ronit the Explorer circuit and joystick/light calibration; Prince the Architect circuit and button/potentiometer/servo behavior. R4 communication, wiring review, integration evidence and the demonstration are shared responsibilities. These are planned assignments for team agreement, not claims that the hardware work is already complete.

OPTIONAL WORDING
“Ronit’s proposed hardware focus is the Explorer controller, and mine is the Architect controller. Soham leads the game design, story, workflow and laptop integration. We will review the Main communication and complete-system tests together. Each task should have an owner, deadline, test evidence and a reviewer, so progress and contributions are clear.”

AVOID
Do not turn proposed assignments into past-tense accomplishments or claim that every task was completed equally. Do not announce an unconfirmed group number. Any formal team commitment remains subject to the course requirements.

HANDOFF
“Soham will close the presentation.” Soham continues on slide 19; hidden references slide 18 remains available for questions.

## Slide 18: References and submission details

PRINCE — HIDDEN SUPPORT SLIDE — Q&A only

USE ONLY IF ASKED
“Our design references are the course requirements, the supplied circuit sketches and diagrams, our editable game source, and the official Arduino board and Wire documentation. The written contract contains the required abstract and detailed sections. The final group number still needs to replace the placeholder.”

CONTEXT
Team: Soham Basanwar, sbasan3, sbasan3@uic.edu; Ronit Mishra, rmish, rmish@uic.edu; Prince Patel, ppate515, ppate515@uic.edu. A single Gradescope submission must select all three members. This presentation does not by itself confirm that submission occurred.

REFERENCES — DO NOT READ EVERY LINK ALOUD
User-provided CS 362 Milestone 3 rubric; supplied Explorer, Architect and Main ZIP sketches and diagram.json files; MAZE_README.md and editable game source.
Uno R4 WiFi: https://docs.arduino.cc/hardware/uno-r4-wifi/
Uno R3: https://docs.arduino.cc/hardware/uno-rev3/
Wire: https://docs.arduino.cc/language-reference/en/functions/communication/wire/

AVOID
Do not read email addresses or the placeholder group number during the main talk. Do not say the slides replace the required written PDF contract. Return to the closing slide after the answer.

## Slide 19: The design behind the adventure

SOHAM — MAIN PRESENTATION — about 25 seconds

READ ALOUD
“To close, I developed the project concept, game design, story and overall workflow. Our next step is to connect the physical controllers to the laptop prototype and verify the complete system together. One player finds a way forward, while the other makes that way possible. Thank you. We’re happy to take questions.”

PRESENTER CUES — DO NOT READ ALOUD
Pause before inviting questions. Keep the attribution factual and brief. Invite Ronit to add hardware and communication detail, or Prince to add materials and schedule detail.

AVOID
Do not claim that all five chapters or the complete physical system are finished. Do not describe proposed teammate assignments as completed work.

END
Leave this slide visible during questions. Hidden slides 4, 7, 10, 12, 16 and 18 are optional support only.
