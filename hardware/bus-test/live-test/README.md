# Live joystick, servo and Wi-Fi test

Open http://127.0.0.1:8086 while the local test server is running.
The laptop must be joined to **DualRealityMaze**, password **MazeDemo362**.
Ethernet can provide Internet at the same time. Do not switch Wi-Fi back to the usual network while watching the test.

## Start again
From this folder run:
    node server.mjs
Then open the page above. If the server is already running, simply open the page.
Diagnostic sketches MainProbe, Probe_COM6 and Probe_COM8 must be installed. These are not the production game sketches.

## Test
1. Move the Explorer joystick fully in every direction and around its edge.
2. Click at least three times, then release to center.
3. With the Architect servo horn unloaded and clear, click Run visible sweep.
4. Watch the real horn. The page's animation displays reported command pulses, not an encoder measurement.
5. Stop servo ends pulses through Wi-Fi → R4 → I2C → Architect. Disconnect power if a physical stop is required and the network is unavailable.

The slow sweep uses 1200–1800 microsecond pulses, traverses both directions twice, returns to 1500, then detaches after approximately 11 seconds. It does not attempt unverified 0–180 degree mechanical endpoints. No movement runs automatically at boot.

USB supplies board power, but this page reads data through the R4's Wi-Fi HTTP service. No serial port is opened by the page or Node server.

## Hardware caution for the finished build
The current unloaded servo test uses R3 5V. Full gate motion under load requires an appropriately rated regulated 5V servo supply and common ground. This test does not validate loaded runtime or power capacity.

## Files
- index.html: local dashboard.
- server.mjs: loopback-only HTTP bridge to 192.168.4.1, port 8086.
- wifi-live.jsonl: timestamped Wi-Fi data and command acknowledgments.
- RESULTS.json / RESULTS.md: saved result snapshot.
- previous-wifi.txt: local record of the network used before testing; not included in shared reports.

The page updates only when receiving fresh data and disables starting a sweep while offline. R3 autonomously stops the sweep after 11 seconds even if Wi-Fi disconnects.
