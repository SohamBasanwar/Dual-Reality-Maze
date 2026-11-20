# Four green accents — wiring and software

This is an integration helper, not installed or flashed game firmware. The actual game pin map has not been verified. Choose an unused PWM output compatible with the existing buzzer/RGB/servo libraries before connecting it. UNO R3 and R4 both list D3, D5, D6, D9, D10 and D11 as recommended PWM outputs; that does not mean every one is free in this project.

Use four ordinary diffused green LEDs, nominal 5 mm, one at each G1–G4 breadboard location shown in LIGHTING_LAYOUT.json. These are nominal mechanical envelopes, not a confirmed purchased LED. Actual breadboard hole rows and leg bends need fitting. Each LED requires its OWN series resistor. Do not parallel bare LEDs on one shared resistor.

## Circuit

Regulated +5 V → four parallel branches, each [resistor → green LED anode/cathode] → MOSFET drain. MOSFET source → ground. Arduino ground → the same ground. Verified PWM pin → approximately 100–330 ohm gate resistor → MOSFET gate; approximately 100 kilohm gate-to-source pull-down keeps it off at reset. Choose a logic-level MOSFET specified at the board's gate voltage. Keep the LED supply current off the GPIO pin.

Compute each LED resistor from R >= (maximum supply voltage − minimum LED forward voltage) / chosen peak LED current. Use the LED datasheet and round UP to a standard resistor value; verify resistor power. A conservative initial target is 3–5 mA peak per LED, or 12–20 mA total for four LEDs. This may or may not be bright enough after diffusion: optical testing sets the final current, within the LED and supply ratings. PWM reduces average current; it does not reduce the instantaneous LED current while on.

The 9 V PP3 plan needs a properly rated 5 V regulator for this branch, rather than feeding 9 V directly to 5 V electronics. Do not assume the Arduino's onboard regulator has enough spare capacity. The one-hour runtime target remains untested, including Main's Wi-Fi, LCD and RGB loads. Never use the RGB LED's pins to power the four accent LEDs.

## Integrating the fade

Include BreathingAccent.h and create `BreathingAccent accent;`. In setup call `accent.begin(yourVerifiedUnusedPwmPin);`. In the normal loop call `accent.update(millis());`. Keep the standard 8-bit analogWrite range (0–255), or adapt the helper if the rest of the firmware changes PWM resolution. The helper defaults to a 4-second cycle and a brightness ceiling of 160/255. It uses no delays and leaves the central RGB status behaviour independent. `accent.off()` stops the effect; begin() starts it again from dark.

No new library installation is required beyond the appropriate Arduino board package. A software-only harness checks timing and duty-cycle behaviour. Powered hardware, timer coexistence, electrical safety and optical brightness have not been tested.

## Build sequence

1. Test one LED, its resistor and the driver on the bench before adding four.
2. Test one optical sample with the actual bronze and translucent materials. Bronze structural walls must be opaque at the chosen wall thickness; use an opaque liner if a flashlight shows transmission.
3. Install each green LED on its marked breadboard area. Aim its dome up into the matching light well. Leave room for leads and avoid the adjustable jaws.
4. Put each translucent lens on the outside of its window, then press on its matching bronze bezel. The fitted bezel captures the lens. Release the two tabs from inside for service.
5. Install the RGB LED and its original quarter-turn keeper. Route a flexible wire extension through the new shield's offset passages. Fit the shield last; disconnect the extension before rotating it during servicing so the LED legs are not twisted.
6. Close the lid slowly with power off. No wires may be pinched by a light well, latch or slider. Check all four LEDs align with their wells.
7. Check green-only, RGB-only and both-on operation in a dark room. Improve opaque lining or diffuser material if there are hotspots or unwanted mixing. The renders show intended placement and appearance, not measured optical performance.

## References

- Arduino PWM: https://support.arduino.cc/hc/en-us/articles/9350537961500-Use-PWM-output-with-Arduino
- Driver principle (the linked guide uses a different strip voltage; do not copy its supply unchanged): https://learn.adafruit.com/rgb-led-strips/usage
- Captured translucent diffuser construction: https://learn.adafruit.com/midi-neopixel-visualizer/cad-files
