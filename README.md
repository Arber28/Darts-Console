# Darts Console 🎯

Offline-first DIY dart scoring console based on an old laptop, three USB cameras, a Raspberry Pi Pico, a KY-040 push encoder and four buttons.

## Status
**Early prototype.** The web UI is a keyboard-controlled offline demo; automatic camera detection and complete scoring/correction logic are **not yet implemented**. Camera compatibility and mounting dimensions remain unverified.

## Dokumentation und Schaltpläne
- [Architektur und Grafiken](docs/ARCHITECTURE.md): Systemdiagramm, Gehäuseanordnung, GPIO- und Stromversorgungsübersicht
- [Linux installieren](docs/INSTALL_LINUX.md): Debian, Hochformat, Kiosk-Plan und Offline-Tests
- [Wichtige Links](docs/LINKS.md): offizielle Downloads, Dokumentation und 3D-Druck-Projekte
- [Bauplan und Testliste](docs/BUILD_PLAN.md): Schritte, offene Entscheidungen und Prüfpunkte

## Files
- [Materialliste / BOM](docs/BOM.md): quantities, provisional prices and reference links
- [Game modes](docs/GAME_MODES.md): planned rules for X01 and additional beginner-friendly games
- [Wiring](docs/WIRING.md): Pico pinout and safety notes
- [Pico firmware](firmware/code.py): CircuitPython USB keyboard controller
- [Offline UI demo](web/index.html): game mode, checkout choice, player selection, random order, menu and correction placeholder

## Controls
Rotate KY-040 = Up/Down; press = Enter; BACK = Escape; UNDO = F4; CORRECT = F2; NEXT = F5. The encoder press is Enter.

## Enclosure / controls
Portrait-oriented laptop display with **four buttons below it**, arranged **BACK – UNDO – [rotary encoder] – CORRECT – NEXT**. No top-row buttons. The encoder rotates to navigate and presses to confirm. Game menu, rules, statistics and settings are accessed on-screen via encoder; dedicated MENU button removed. LED ring has independent rotary dimmer and power supply, not Pico-controlled.

## Players
Emre, Arber, Adnan, Atakan, Amir, Ali; optional guest players.

## Try the prototype
Open `web/index.html` locally in a desktop browser. Use Up/Down, Enter, Escape, F4, F2, F5. It requires no internet.

## Pico setup
Install CircuitPython on a Pico with native USB, copy Adafruit's `adafruit_hid` library into `CIRCUITPY/lib/`, then copy `firmware/code.py` as `CIRCUITPY/code.py`. Wire it according to [WIRING](docs/WIRING.md).

## Next steps
1. Verify 3-camera UVC support, mounting dimensions, and lens view.
2. Select and test an offline scoring engine.
3. Integrate actual throws, X01 bust/checkout rules and historical corrections.
4. Design/print camera mounts and laptop display/control housing.
5. Configure automatic boot to full-screen app.
