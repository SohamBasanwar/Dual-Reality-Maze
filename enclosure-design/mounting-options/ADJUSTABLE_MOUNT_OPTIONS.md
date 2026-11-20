# Dual-Reality Maze — manually adjustable mounting options

Research and feasibility discussion · 27 October 2026

This is a proposal, not a new CAD revision or a verified printed mechanism. Revision 09 retains its current replaceable carriers. It does not yet provide hand-adjustable width, length and height. Existing validated files have not been changed.

## Recommended arrangement

Use a common screwless rail interface in all three enclosures, with different removable carriers for the actual components. Replace the existing cradle where necessary rather than stacking a thick adjustment platform on top of it.

1. **Width:** two sliding edge jaws approach the board from its sides.
2. **Length:** one fixed datum/end stop and one sliding stop capture the board's ends.
3. **Height:** keyed clip-in riser blocks or stepped support posts set all support points to the same height. Thin removable shims provide smaller corrections.
4. **Lock:** captive cross-pins or a sliding lock key engage an indexed rail. A small compliant pad removes rattle; the pin/key, not friction alone, prevents the carrier moving.

Adjustment would take place with the enclosure open. Rails need end stops, the locking key must be reachable, and a missing or partly engaged lock should be visually obvious. Support the PCB at clear board edges and safe underside areas, not on solder joints, chips, terminal legs or antennas.

This provides modest fit adjustment within a defined range. It cannot make a board larger than the enclosure fit, move a connector through an unchanged wall, or correct a badly located joystick shaft with no opening clearance. Maximum adjustment ranges must be established by CAD interference checks before implementation; no numerical travel range is promised by this study.

## Mechanism comparison

The project adaptations below are engineering proposals. Commercial reference products demonstrate the mechanism families; their metal load ratings and tolerances do not transfer to a miniature printed version.

| Option | Manual operation | Advantages for this project | Disadvantages / limitations | Best use |
|---|---|---|---|---|
| Captured sliding rail with indexed lock pin/key | Slide a jaw along a dovetail or T-shaped track; insert/release a captive lock in one of several positions | Positive lock, little continuous bending stress, easy to see engagement, replaceable jaws, no PCB holes needed | Discrete settings; rails and locking access occupy space; fine fit needs pads/shims; small printed pins need strength tests | Preferred for Arduino/breadboard carrier width and length |
| Ratchet rail with release tab | Push a jaw inward; a flexible pawl clicks over teeth; press release to loosen | Fast adjustment, no loose key, familiar cable-tie-like operation | Tooth pitch limits resolution; small teeth and flexures can wear or creep; can squeeze a PCB too hard; release can be awkward in a crowded enclosure | Light retaining stops or a clip-on accessory, not the primary servo restraint |
| Sliding rail with cam/wedge lock | Move freely, then close an eccentric lever or push a wedge to clamp the carriage to its rail | Continuous position adjustment; compact clamp action; quick service | More parts; clearance and friction need tuning; creep can reduce preload; lever needs room; requires a detent/positive keeper against accidental release | Optional fine-adjustable LCD or board carrier if the test mechanism proves reliable |
| Keyed spacers / stepped posts | Snap in matched spacer blocks, or select a height notch and lock it with a clip | Simple, stiff support, easy to print and replace; height can change without loading a long flexure | Discrete heights; loose stacks are unsuitable; all corners must be matched; does not itself adjust width or length | Preferred height setting for boards, LCD and servo datum correction |
| Reusable strap or split collar | Tighten a releasable strap around a body, or close a split retaining ring with a keeper | Accommodates irregular bodies and small diameter differences; few parts; no mounting-hole pattern needed | Less precise location; strap alone does not establish height or prevent all rocking; preload must avoid deforming the device | Buzzer/body retention, wiring restraint, optional small electronics; not sole joystick/servo positioning |

**Proposed priority:** indexed rails + keyed height spacers first. A cam lock is a useful second prototype when continuous adjustment matters. Avoid relying entirely on tiny ratchet teeth for the gate or joystick, which receive repeated force.

## What should differ by component

| Assembly / component | Proposed adjustable features | What should remain fixed and why |
|---|---|---|
| All three — Arduino and breadboard | Sliding end/side stops and matched height spacers on a removable tray | Cable route, safe PCB contact areas and maximum envelope; added height must preserve lid and jumper clearance |
| Optional ESP32 | Small removable edge carrier or restrained breadboard installation | Header spacing, antenna keep-out, USB access and wiring height; the selected ESP32 still matters |
| Explorer — joystick | Adjustable PCB edge jaws and small depth shims | Shaft centre at the lid opening and full stick/click travel. Asymmetric PCB variants may need a different adapter insert rather than freely moving the joystick |
| Explorer — photoresistor | Replaceable sensor-seat insert or small thickness shim | Isolated floor, lead passages and optical dome position. A universal moving tray adds no useful benefit here and can create light leaks |
| Architect — potentiometer | Replaceable split-body insert and adjustable keeper depth | Shaft centre, antirotation feature, knob clearance and terminal route |
| Architect — servo and gate | Interchangeable cassette insert, body stops and limited datum shims | Output shaft relative to horn, pin, yoke and gate rails. Arbitrary height/XY movement would change the gate geometry and could jam it |
| Architect — tactile button | Switch locator on the breadboard plus keyed interchangeable stem tips or height shims | Cap guide axis, rest gap and overtravel stop. A telescoping stem needs a secure lock; it is not implemented in R09 |
| Main — LCD | Sliding PCB edge supports with matched depth spacers | Screen centre and viewing window; adjustment cannot move the glass out of the bezel |
| Main — buzzer | Split-cup insert/strap plus depth spacer | Sound outlet remains unobstructed; leads remain unstressed |
| All three — RGB LEDs | Package-specific insert/keeper | Optical alignment and insulated lead space; a large adjustment mechanism would be wasteful |
| All three — PP3 battery doors | Existing dedicated bay; small removable pad if the actual battery rattles | Terminals, connector bend, catch and external grip contour. Do not make the palm-facing door adjustable |

The same rail/key concept could be shared across all three enclosures. The component-facing jaws and inserts should differ. The controller interiors already reserve a full-size breadboard, battery, board, optional ESP32 and wiring; a large universal three-axis platform could force a larger enclosure. The Main is easier to package, but its screen and sound openings still constrain placement.

## Research references

- [igus drylin guide catalog](https://www.igus.com/contentData/Product_Files/Download/pdf/2016%20drylin%20section.pdf): rail/carriage systems and manual clamping illustrate separating guided motion from locking. The catalog's commercial hardware is not a prescribed purchase for this project.
- [BESSEY clamp mechanism explanation](https://bessey.de/en-gb/bessey-tool/service/faqs): ratchet/lever clamp operation and release mechanisms. Our miniature printed pawl would need independent tests.
- [JW Winco eccentric cam levers](https://www.jwwinco.ca/en-us/products/2.3-Tensioning-with-eccentric-cams-and-wedge-clamps/Clamping-levers-with-eccentrical-cam): continuous adjustment and lever clamping. Many commercial examples use threaded adjustment; our screwless adaptation would require a captured pivot and separate non-threaded adjustment/lock.
- [Essentra PCB hardware guide](https://essentracomponents.bynder.com/m/7baf135c037b4280/original/Essentra_Ultimate-PCB-Guide-UK-compressed.pdf): board supports, spacers, guides and sample-fit considerations.
- [Formlabs snap-fit design guide](https://formlabs.com/blog/designing-3d-printed-snap-fit-enclosures/): flexure geometry, manufacturing tolerances and print orientation affect snap retention. Printer/material tests are necessary before choosing final clip dimensions.

## Printing: separate pieces and sensible order

Revision 09 has **50 separate assembly-part STL files**: Explorer **12**, Architect **20**, Main **18**. These are printed as individual pieces and assembled afterward. Several can share a build plate; this does not mean 50 separate printer jobs. Orient/space them in the slicer, and respect material and support requirements. The diffuser may instead be a translucent cut sheet, so 50 is the modeled assembly-piece count rather than an obligation to print 50 opaque pieces.

Integral rails, cups, ledges and latch receivers remain part of their Base or Lid STL; not every small feature in the picture is a separate piece. There are also **21 fit-test samples** and **four optical alternatives**. Do not print every test sample and optical alternative as extra final assembly pieces. Select one functional dome variant after the optical test.

### Print first, as tests

- Fit samples **01–03** together: grip base section, matching lid section and battery door. Evaluate comfort, battery fit and latch.
- Fit samples **04–06** together: I2C shutter track, shutter and keeper. Evaluate sliding clearance and cable bundle opening.
- Fit samples **12–14** together if using Main's USB fallback: USB track, shutter and keeper.
- Fit samples **20–21** together: isolated sensor pod and default dome. Test opening, removal and actual sensor readings with the chosen filament.

These tests are useful even if we adopt adjustable carriers. They are prototypes, not a promise that those samples will become final installed parts.

### Wait for the mounting decision / real-component fit

Full Bases/Lids, joystick/LCD/servo carriers, PCB clips, potentiometer keepers, button stem/guide and final gate drive hardware. An adjustable mounting upgrade could change the shell interfaces and these pieces. Printing them now risks reprinting them.

### Print final batches after fit tests

Small retainers/shutters/masks can share plates after their fit/material decisions are settled. Print the large shells after the revised internal layout is checked. Assemble one enclosure and verify it before committing to the remaining pair. The existing R09 `PRINT_PLAN.csv` supplies per-part orientation and support starting points, but it is not a final printer profile.

The companion `PRINT_FIRST.csv` lists actual existing test files and reasons. No models or print jobs were submitted or changed for this research task.
