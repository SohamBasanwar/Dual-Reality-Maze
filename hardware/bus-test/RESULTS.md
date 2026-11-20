> Historical November 9 report. See RECHECK-2026-11-10.md for current LCD, Wi-Fi, button, RGB, buzzer and servo results.

# Physical communication test — 9 November 2026

PASS: Main UNO R4 WiFi (COM5) exchanged checked I2C commands and responses with both UNO R3 boards. The laptop was connected through the user's Thunderbolt hub. User confirmed separate common-ground connections.

| Board | USB port | Identified role | Captured valid packets / total |
|---|---|---|---|
| UNO R3, serial 4423831323935150C1D1 | COM6 | Empty board / intended Architect | 1101 / 1101 |
| UNO R3, serial 44238313239351608051 | COM8 | Joystick board / Explorer | 1100 / 1100 |
| UNO R4 WiFi, serial 3CDC75F153AC | COM5 | Main I2C controller | Receives both streams |

Every captured packet had the expected length, address, protocol identifier and checksum, and echoed the unique command sent by Main. All reported I2C transmission status codes were zero. Changing sequence counters verified that the R3 loops were running. Bus configured to 100 kHz; actual clock waveform not measured. Captures lasted 10, 55 and 45 seconds.

Joystick axes on COM8 both reached 0–1023 during the user's movement test; resting readings were approximately X=498–499, Y=527. COM6's unused analog inputs fluctuated near 127–140; these are floating readings, not valid control values.

## Click button remains unresolved

No LOW sample on COM8 D2 was captured, including during the user's reported five-second hold. User reports SW connected to D2. This does not invalidate the working I2C and X/Y tests. The click signal has not been verified functional. Next physical check: with power disconnected, trace SW to the actual D2 header and verify switch continuity between SW and GND when pressed; inspect the jumper and joystick header joint.

## Firmware currently installed

Temporary diagnostic sketches remain on all boards: MainProbe, Probe_COM6 and Probe_COM8. They do not drive actuators or update the game/LCD display. No production firmware was restored automatically.

Diagnostic addresses were assigned before identifying the joystick: COM6=0x10, COM8=0x11. For the production firmware, upload **Explorer to COM8** (which changes it to 0x10), **Architect to COM6** (changes it to 0x11), then **Main to COM5**. Power down/restart together after changing both role assignments; do not use a mixed diagnostic/production configuration. Ports can change on reconnection; use BOARD_MAPPING.json and USB serial IDs to identify them.

The tests do not establish Wi-Fi, LCD, LED, buzzer, servo, complete game operation or long-term reliability. Raw captures and TEST_RESULTS.json are beside this report. Capture.ps1 can repeat the serial diagnostic capture while these sketches are installed and no other program owns COM5.


