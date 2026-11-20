# Print review and assembly sequence

## Start with small test pieces

Use the `fit-tests` directory before full cases. Files are normalized to millimetres with their lowest surface at Z=0. Pair 01/02 tests the battery door; 03/04 tests the side-release lid latch; 05/06/07 tests the switch guide, cap and cassette. Use the intended facility material and nozzle/profile. Trial printer clearances are not universal.

Test a real battery with its snap, insulation and lead bend. The latch must release by a fingertip without bending the battery or exposing its terminals. Verify that neither locating tab jams. Test repeated opening/closing and moderate grip pressure; reject cracked, whitening or permanently bent latches.

The button should return freely and actuate before its mechanical stop. The initial cap-to-switch gap is 0.1 mm, with a nominal 0.45 mm downward cap limit. These are design assumptions, not measured travel of the user's switch. Adjust pusher height and cassette stop from the actual switch. Do not force a switch to the wrong printed stop.

## Proposed orientations

| Part | Starting orientation | Review points |
|---|---|---|
| Base | Flat bottom on bed | Battery opening, anchor tunnels and latch windows may bridge; inspect the preview. |
| Lid | Outer face down with selective build-plate supports | Curved face, raised rims and the control holders prevent a universal support-free orientation. Keep support away from flexible latch faces where possible. Compare a tilted orientation with staff. |
| Battery door | Broad outside face down | Recessed finger area and tabs need inspection. No support trapped under the release tongue. |
| Button cap | Face down, pusher upward | Test face finish and guide diameter; avoid support on the sliding shaft. |
| Switch cassette | Flat bottom down | Check upper stop-ring overhang and removal access. |
| Gate panel | Broad flat face on bed | Retain yoke-slot width; no supports inside the sliding slot. |
| Gate frame/shroud | Broad side or back down | Compare support access, rail finish and thin-bar orientation. Guard is not a handle. |
| Emblem mask | Broad face down | Small attachment tabs need inspection; preserve light-slot width. |
| Diffuser | Flat | Use a translucent insert/print. Bronze-coloured opaque plastic is not a diffuser. |

Full STL files retain their assembly coordinates, so use the slicer's place-on-bed tool and the orientations above. Do not print the entire STEP assembly as a single fused object. No final G-code or UIC-specific printer profile is included.

The layer direction must not make a repeatedly flexed latch split along layer lines. Prefer removable retention features and coupons over trusting a material name. Bronze-coloured PLA/PETG is a finish choice; silk PLA and metal-filled composites are different materials. Ask UIC which filament is available and suitable for the repeated flexing. A separate translucent diffuser can coexist with single-colour structural printing.

## Electronics and shell assembly

1. Remove all support and sharp edges. Inspect latch roots, rails and openings. Dry-fit the shell and battery door empty.
2. Seat the Arduino on its cradle supports. Use insulated, reusable nonmetallic ties through the anchor tunnels, routed around safe board edges or verified mounting locations without pressing on components, pin headers or the R4 antenna. The clear shipping/base plate in the R4 photo is not part of this cradle.
3. Lower the full-size breadboard into its tray and engage the four retaining fingers. Ensure no finger obstructs electrical contacts. If the board's backing or interlocks differ, adjust the tray first.
4. Fit the joystick carrier or potentiometer body holder. Use the actual joystick header direction and full cap swing. The bronze knob must be a matching press-fit type if screws are forbidden; the product image alone does not prove its retention method. A screwless split-collet knob can be designed after measuring the shaft if needed.
5. Fit the bare LDR, RGB LED, diffuser and mask. Insulate LED leads, provide one resistor per colour and keep emitted light from contaminating the Explorer LDR reading.
6. Insert the button cap from below, followed by the switch cassette. Secure the cassette to its support/strap features. Check actuation, free return and stop clearance before closing the lid. Main needs an additional tactile switch and an actual latching power-control module; the cap alone does not provide power switching.
7. Fit the LCD/backpack and the chosen round sounder in Main. Allow wire/trimmer access. The rectangular speaker also shown in the photos is not the selected buzzer envelope. Exact LCD angle and bezel fit require a physical check.
8. Route the sleeved I2C tether through the upper rear entry and strain-relief saddle. Secure the cable jacket, never clamp bare conductors. Leave a service loop for lid removal. Final cable/connector dimensions are still required. USB programming access is through the removable lid until an actual panel/pigtail connector is chosen.
9. Fit the battery snap and pull ribbon. Route leads through the bay's terminal passage, away from the latch tongue. Put the regulator and power-switch circuitry in the reserved zone after their footprint and thermal requirements are known.
10. Insert the lid's rear locating tabs and lower the lid until both side latches engage. Release both side latches before lifting the front for service. Do not force a tight first print.

## Architect gate

The SG90 is mounted sideways so its horn rotates in the vertical gate plane. The supplied nylon horn is reused; no unverified printed spline is claimed. A nominal 7 mm crank radius and a sliding pin in the gate's horizontal slot convert a 120-degree sweep into approximately 12.12 mm of lift. Guide rails constrain the panel; the shroud encloses the motor and rotating parts.

Fit and retain the servo in the removable cassette with nonmetallic ties and appropriate pads. Match the drive pin to the actual horn hole and use positive axial retention. The current pin and keeper are prototypes; do not rely on a loose friction-fit horn. The guard/cassette retaining details require a bench fit before operation.

With power disconnected, move the mechanism through its full sweep by hand without forcing the geartrain. Verify no binding or accessible pinch points. Then power from a current-limited suitable servo supply, start with a narrow range about centre and expand only within the physical clearances and actual servo limits. Test the intended duty cycle without stall or heating. The CAD sweep check verifies the gate panel against frame/guard; it does not certify the real horn, leads, tolerances or pinch safety.

## UIC

The user has professor permission. No fabrication form has been filled or submitted. Engineering Makerspace and Education Technology Services have different equipment and access policies. Confirm the assigned facility, printer, usable bed, material and accepted file/settings before a complete print.

References: [UIC Engineering equipment](https://makerspace.uic.edu/learn/tools/), [Education Technology STL service](https://etl.ed.uic.edu/services/3d-printing/), [Prusa material guide](https://help.prusa3d.com/filament-material-guide), [Adafruit printed button reference](https://learn.adafruit.com/3d-printed-neopixel-tactile-switch-buttons?view=all).
