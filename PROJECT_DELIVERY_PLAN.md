# Dual-Reality Maze delivery plan

## October 23 enclosure revision

The latest enclosure study is `enclosure-design/ergonomic-v2/index.html`, packaged in `Dual_Reality_Maze_Ergonomic_Design_v2.zip`. It includes three revised CAD shapes, full-breadboard layouts, source dimensions, one-color decals and a single master-power proposal. Eight solids pass mesh checks; lower component footprints are contained and non-overlapping. Physical fit, grip comfort, screwless retaining parts and power qualification remain open. The game/USB prototype exists; the I2C/Wi-Fi hub firmware and game-state hardware feedback are still unfinished. The user explicitly asked to finish the design before filling any fabrication form; no form was submitted.

## Order of work

1. Finish and verify the updated game and controller interface. Status: done. The root Story Edition matches the tested build.
2. Finish the trailer from actual project scenes, add speech where available without paid generation, verify the exported MP4. Status: done. The 33.46-second 1080p cut includes the King's Clipchamp opening line and music. Eight source clips and stills remain available.
3. Prepare the milestone presentation with the trailer embedded, speaker notes, hardware diagrams, communication plan, controls, timeline, materials, references and contribution credit. Status: done. The 18-slide editable deck is in submission/.
4. Prepare the required written milestone contract PDF with all five detailed sections and an abstract below 100 words. Status: done. Six pages, 84-word abstract.
5. Validate all slides, document pages, video and required metadata. Create one clear submission folder. Status: done. Package/layout/font/import checks passed and video decoded. Native PowerPoint playback still needs the user's presentation-device rehearsal. Group number remains the requested placeholder.
6. Enclosure phase: the user confirmed Engineering Makerspace in RRB and handheld gamepad grips. A five-page design plan, three monochrome role designs, technical layouts and adjustable reference CAD are now in enclosure-design/. Seven nominal CAD solids passed watertightness/volume checks. Exact component fit, lid retainers and screwless horn keeper still require measurements before final print release.

## Confirmed details

- Soham Basanwar, sbasan3, sbasan3@uic.edu (email follows the supplied NetID).
- Ronit Mishra, rmish, rmish@uic.edu.
- Prince Patel, ppate515, ppate515@uic.edu (latest correction takes precedence).
- One Main Uno R4 WiFi plus two controllers: Explorer and Architect, each Uno R3. Latest architecture: wired I2C between boards, all boards USB powered, Main built-in Wi-Fi to laptop. No battery bays or external radios. Servo needs dedicated regulated power support. USB_WiFi_Revision contains the corrected presentation and contract.
- Milestone year 2026, confirmed by the user.
- Group number: use [NUMBER] until the user supplies it.

## Attribution and accountability

The user identifies Soham as the originator of the project concept, game design, story and overall workflow. Credit those contributions explicitly. Do not claim that all members completed equal work, and do not make accusations about teammates. Separate completed contributions from proposed assignments.

Proposed ownership, subject to team agreement:

- Soham: creative direction, game/story integration, workflow, presentation and demo coordination.
- Ronit: Explorer controller assembly, joystick/light-sensor calibration, firmware evidence and tests.
- Prince: Architect controller assembly, potentiometer/button/servo behavior, firmware evidence and tests.
- Shared integration: actual R4/controller communication, power checks, wiring strain relief, end-to-end demonstration and enclosure fit checks.

For each task, record the owner, expected result, due date, source/code evidence, tester and completion status. Review weekly and before each presentation/demo. Never substitute a proposed assignment for a verified contribution.

## Scope and known limits

- No changes to original storyline or artwork.
- No mention of generation tools or methods in the presentation. No false declaration about how work was produced.
- No Gradescope submission or teammate messages have been authorized.
- The browser upload gate declined the game-file upload to Clipchamp. Keep media local; do not work around that restriction through another browser or indirect upload.
- ElevenLabs authorization remains limited to the six-line prologue sample after the user configures local credentials and voice IDs. The remaining 44 lines are not approved.
- Main's current ZIP is an LCD/buzzer test. A proposed I2C/R4 relay must be identified as planned until firmware and real hardware have been tested.
- The original Architect test sketch moves its servo on every confirmation. Laptop-controlled servo feedback is pending.

## Enclosure gate

Before final print release, confirm: actual breadboard sizes, module dimensions/heights, USB plug envelopes, servo horn and cradle, regulated servo supply connection, harness connectors, lid retention and fit coupon results. Current nominal CAD assumes half breadboards. The confirmed facility is Engineering Makerspace in RRB. Controller shape is handheld gamepad grips. All boards use USB power, with no battery compartments. Professor permission is already provided and does not need to be requested again.
