# Live hardware test results — 10 November 2026

User confirmed that the live joystick display and the wider servo movement worked. The servo sweep was reported smooth.

Wi-Fi HTTP responses at this snapshot: 540. Invalid board samples among those returned responses: 0.

Joystick X: 0–1023. Y: 0–1023. Press counter: 3 → 17. Latest resting reading: X=499, Y=527.

The laptop sent sweep commands over Wi-Fi to the R4, which forwarded them over I2C to Architect. Architect reported changing commanded pulse widths. The user separately confirmed actual shaft movement. The Stop command was acknowledged. These telemetry values are commands, not measured servo shaft angles.

One temporary Wi-Fi interruption generated 13 HTTP timeouts. Windows had returned to the regular network; the user did not switch it manually. Reconnecting to DualRealityMaze recovered the page. R4 uptime continued across the interruption. The inspected Windows events did not establish the cause. This is a functional pass with an unresolved connectivity interruption, not a claim of uninterrupted long-term reliability.

The page and server remain available at http://127.0.0.1:8086 and the laptop remains connected to DualRealityMaze. Ethernet remains available for Internet. No serial connection is used by this live page. USB still supplies board power.

All boards retain diagnostic firmware. Sweeps stop automatically after about 11 seconds. Use an appropriate regulated 5V servo supply and common ground before testing the finished loaded gate. No extreme 0–180 degree mechanical endpoint calibration was performed.

Raw data: wifi-live.jsonl. Summary snapshot: RESULTS.json. Instructions: README.md.
