# Dual-Reality Maze — print preparation / Revision 12

Owner: Soham Basanwar. Units: millimetres. Keep every model at 100% scale.
Status: digital prototype. UIC publishes a Voron build volume of 290 × 290 × 285 mm. Actual assigned printer, usable exclusions, material availability and sample fit are not confirmed. Provisional plate arrangements are supplied for staff review; no production release or printer G-code is supplied.

## What to tell the operator

“This is a CS 362 enclosure project with three large shells, screwless clips and sliding mounts. Please start with the fit samples, not the full set. We need opaque structural parts in one colour and a separate run of seven small translucent optical inserts. Markings are hidden on interior faces. Please review the small clips, text, enclosed light channels and removable support access in the slicer before printing. Do not uniformly scale parts to make them fit the bed.”

The outside should be bronze-coloured if a suitable ordinary polymer is available. UIC's published stock PLA colours are translucent, white, gray, black and red; bronze is not listed. Ask about availability before buying filament. Charcoal/black is the recommended stock fallback. A bronze exterior finish is another option after fit testing, keeping coating away from optical windows, sliding faces, clips and electrical contacts. No metal-filled material is specified.

## Printer settings to discuss

| Item | Recommendation for this project | Published UIC default / limit |
|---|---|---|
| Nozzle diameter | Request 0.4 mm if available for clips, small gaps and text; 0.25 mm only if staff identify a detail that needs it | 0.6 mm FDM nozzle |
| Layer height | Request 0.20 mm for structural trials; 0.15–0.20 mm for small detailed parts if supported | 0.30 mm |
| Optical inserts | Start at 0.20 mm layers, flat, translucent PLA; slice the 0.8 mm accent lenses as solid thin parts | Translucent PLA is listed; thickness/appearance must be sampled |
| Walls | Request 3 perimeters where geometry permits; inspect the actual remaining solid sections | Small features about 2 mm minimum, geometry dependent |
| Infill | Start with 20% gyroid for substantial volumes; thin clips/lenses may become solid automatically | 20% gyroid |
| Temperature / speed / cooling | Use staff's tested profile for the actual filament and printer | Do not substitute an unrelated printer's profile |
| Supports | Local accessible supports only; keep them out of light galleries, blind rail/key slots and wire passages | Internal supports must be removable; internal unsupported walls should meet the stated 45° rule |
| Fit | Print the coupons, measure and revise individual fits | UIC recommends 0.5 mm horizontal and 1.0 mm vertical separation for multipart assemblies |

The existing digital fits include gaps around 0.15–0.35 mm and thin flexures. They do not automatically meet UIC's coarser defaults. A smaller nozzle alone does not prove that they will fit. If only the default process is available, use the coupons to determine which clearances and feature sizes need revision before releasing full shells. Do not use global XY compensation or scaling as a substitute for reviewing moving fits.

Nozzle diameter is the opening in the print head; layer height is the thickness of each deposited layer. They are different settings. The slicer profile must match the physical nozzle.

## Print order and separate batches

1. **Trial parts first:** rail/jaw/key fit coupons; one green-light coupon with its actual M23 bezel and M24 lens; a representative small clip. These parts test the process before long prints.
2. **Opaque structural run:** large bases and lids, then remaining opaque parts. Small compatible parts may fill spare bed area. Use one chosen structural filament/colour per plate.
3. **Translucent optical run:** seven inserts together where bed size allows — three emblem diffusers and four Main accent lenses. Their LEDs provide the colour, so all seven can use the same neutral translucent filament.
4. **Alternatives only if needed:** select one height insert, servo liner or button tip per location. Alternate files are substitutions, not extra installed layers.

Opaque and translucent parts are separate jobs, not a multicolour print. No detached electrical components belong on the print manifest. Keep each finished piece in its E/A/M coded bag; tiny pieces without physical lettering still have a code in the manifest and filename.

## Plate preparation already provided

`PRINT_MANIFEST.csv` and `PRINT_PREP.json` list the installed set, material group, provisional orientation, transformed bounding box, support cautions and batch priority. `arrange_plates.py` can use the eventual usable width/depth/height to pack parts by material without scaling. It supports 90° rotations in the plate plane, keeps margins and a per-part brim/support allowance, and exports plate SVGs, per-plate 3MF models, individual positioned STLs and a placement manifest.

The chosen orientations and rectangular support allowances are starting points. The packer cannot predict generated supports or toolhead collision envelopes. Final slicing must verify support extent and clearance. Print each layer across all objects on the plate; do not select sequential “complete individual objects” mode without a separate toolhead-clearance check.

Tentative layouts in uic-voron-provisional use the published Voron volume, an 8 mm boundary margin, 5 mm per-part brim/support allowance and 4 mm additional separation. The largest candidate shell footprint is about 246.3 × 209.4 mm before allowances. Staff must confirm the **usable** width × depth, printable height, printer model, nozzle diameter and supported materials. Account for clips, excluded areas and the purge line. An oversized part is reported rather than scaled down or split automatically. No final plate count, time or total cost is claimed before slicing.

## Materials and cost

These “lenses” are small custom diffuser inserts, not special purchased optical lenses. First ask UIC to print them in its listed translucent PLA. UIC says enrolled coursework projects are typically not billed, subject to their determination. Its listed billable PLA material rate is $30/kg ($0.03/g); supports, setup and any applicable charges can change a quote. This is not a guarantee that your job is free.

As checked 31 October 2026, Prusa lists a whole 1 kg clear PETG spool at about $24–30, before shipping/tax. A whole spool is unnecessary if the lab can supply the small amount. Adafruit's 12 × 12 inch diffusion acrylic sheet is $9.95, but it is 2.6 mm thick and is **not compatible** with these 0.8 mm accent-lens seats without a design revision. Do not buy that sheet for the current seats.

## Sources

- UIC process, colours and design rules: https://makerspace.uic.edu/make/digital-fabrication-lab/
- UIC billing: https://makerspace.uic.edu/learn/billing/
- Nozzle/detail tradeoffs: https://blog.prusa3d.com/everything-about-nozzles-with-a-different-diameter_8344/
- Clear PETG price reference: https://www.prusa3d.com/category/petg/
- Acrylic price and thickness reference: https://www.adafruit.com/product/4594
