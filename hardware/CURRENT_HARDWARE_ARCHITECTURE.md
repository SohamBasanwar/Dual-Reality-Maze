# Historical hardware architecture — October 22, 2026

**Superseded for firmware/wiring on November 9, 2026:** see [arduino-system/START_HERE.md](arduino-system/START_HERE.md) and [arduino-system/WIRING.md](arduino-system/WIRING.md). The new package implements I2C hub firmware, USB/Wi-Fi transport and a separate hardware-enabled game copy. It includes RGB indicators, regulated servo power and an optional four-LED accent driver. Physical testing is pending. The earlier enclosure work is discontinued; this historical document does not override later decisions.

This user-confirmed revision supersedes the earlier battery and Main USB-data-relay plan.

- Explorer: Uno R3, breadboard, joystick/click, light sensor, USB power.
- Architect: Uno R3, breadboard, 10k potentiometer, button/pull-down, SG90, USB power and dedicated regulated servo support.
- Main: Uno R4 WiFi, I²C LCD, buzzer, USB-C power. Built-in Wi-Fi carries laptop data.
- Wired I²C: both R3s use A4/SDA, A5/SCL and common ground to Main’s header I²C bus. LCD shares that bus.
- Keep independently USB-powered positive rails separate. Servo motor power must use a suitably rated regulated source and common signal ground.
- No battery bays, HC-12, Bluetooth or external radio modules are part of this design.

The game currently has a direct-serial prototype. The I²C hub and Wi-Fi game transport are planned integration work, not implemented by the enclosure design task.

Current enclosure plan and assets: ../enclosure-design/. Current presentation and written milestone revision: ../submission/USB_WiFi_Revision/. Earlier files are retained as history.
