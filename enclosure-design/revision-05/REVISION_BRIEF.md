# Revision 05 — reference-led mechanical revision

25 October 2026. Supersedes revision 04 for appearance development; preserves it unchanged.

The supplied concept is the exterior design target: broad curved shoulders, inward waist, tapered descending grips, an ornamental face border, eye/gate/portal emblems, upper-shoulder Architect gate, and a layered desktop Main console. The illustrated interior is not dimensionally reliable. Actual components and service clearances control the inside.

## Required changes

- Replace constant-height, straight extruded walls with bulging/tapered sections and a downward sweep at the grip ends. Keep screwless battery doors and internal retention.
- Keep one full-size 166 × 55 × 10 mm provisional breadboard per enclosure, 9V grip bays in the handhelds, and a separate Main battery bay.
- Reserve optional ESP32 development-board and jumper-wire space. The user has not selected a board. A reservation is not a universal ESP32 socket or verified radio layout. The nominal design allowance is 60 × 32 mm, with a separate vertical wiring allowance, and no fixed mounting-hole pattern.
- Main must accept either UNO R4 WiFi or UNO R3 using a common conservative cradle envelope. Provide rear cable access behind a captive sliding shutter, with room for a USB plug and strain relief. No screw fasteners.
- Retain controls, RGB diffuser emblems, protected servo gate and component service access.
- Keep generated supports separate from the printable parts. Review overhangs in the actual printer profile; round edges alone do not determine support requirements.

## Review standard

Deliver actual CAD and renders of that CAD, including an internal view and shutter open/closed views. Clearly distinguish a mechanical prototype from a physically fitted, electrically tested, print-approved enclosure. No new image-generation render will substitute for geometry.

## References checked

- Espressif DevKitC V4: https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html
- Official DevKitC dimensions (48.26 × 27.94 mm, not a guarantee for clones): https://dl.espressif.com/dl/schematics/esp32_devkitc_v4_dimensions.pdf
- Antenna layout guidance: https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32/pcb-layout-design.html
- Prusa support/orientation guidance: https://help.prusa3d.com/article/support-material_1698
- UIC Engineering equipment: https://makerspace.uic.edu/learn/tools/
- Separate Education service accepts STL: https://etl.ed.uic.edu/services/3d-printing/

The antenna area needs clearance from metal, wiring and other electronics. A breadboard contains metal contacts; a board physically fitting on it is not proof of a satisfactory antenna arrangement. Keep the optional mounting solution movable until the exact ESP32 and header dimensions are chosen. Bronze-coloured insulating polymer is the finish assumption; conductive coating and metal-filled material are not assumed near an antenna.
