# Bill of materials

Updated 2026-11-16. Hardware choices reflect the current build rather than the earlier AliExpress shortlist.

## Cost accounting

**€70.25** is the owner's calculated *project-attributed cost*: only parts and quantities allocated to this project, not the full cost of multi-packs or previously owned equipment.

The **three GXIVISION OV2710 cameras were ordered and paid** on 2026-11-16 for **€47.45 total** (€41.45 item price plus €6.00 shown at checkout). The remaining €22.80 in the owner-provided project figure is not broken down by item; do not treat it as verified separate purchase receipts.

## Hardware and sourcing

**Status terminology:** *Ordered* = confirmed order screenshot. *On hand / no purchase needed* = owner says not to buy it for this project; this does not assert a new order. Exact product URLs will be added individually after the owner supplies them.

| Build qty | Part | Status | Exact product link | Notes |
|---:|---|---|---|---|
| 3 | GXIVISION **OV2710 S2M07**, 2 MP, 1080p, 100° lens, USB, 2 m cables | **Ordered / paid** | [AliExpress listing](https://a.aliexpress.com/_EGOiQmK) | AliExpress, Dart Machine Specialty Store; €47.45 charged total |
| 1 | **RP2040-Zero** board, RP2040, USB-C | On hand / no purchase planned | [Amazon listing](https://amzn.eu/d/09UHp4mh) | AYWHP 3-pack was considered; only one board is used. Not pin-compatible with standard Pico |
| 1 | **KY-040** rotary encoder with push button | On hand / no purchase planned | [Amazon listing](https://amzn.eu/d/05MyUipj) | AYHYHLJZ 4-pack considered; use one |
| 4 | **Blue clicky MX-style keyboard switches** | On hand / no purchase planned | [Amazon listing](https://amzn.eu/d/0eZNfhsp) | Gsbnjuy 30-pack considered; four used; print compatible keycaps |
| 1 | **UGREEN 4-port USB 3.0 hub**, 15 cm cable | On hand / no purchase planned | [Amazon listing](https://amzn.eu/d/0cIdLONb) | Test three cameras simultaneously |
| 1 length | **KSIBNW COB LED strip**, 3 m roll, 6000 K white, 5 V USB, dimmer | On hand / no purchase planned | [Amazon listing](https://amzn.eu/d/03nj8HNP) | 8 mm width, 25 mm cut increments, advertised 9 W/m and CRI >90; final ring circumference not measured |
| 1 | Existing laptop with portrait display, 8 GB RAM | Already owned | — | Host computer and screen |
| 1 | Suitable SSD | Already owned | — | No purchase needed |
| 1 | USB-C **data** cable | Already owned | — | For RP2040-Zero |
| as needed | Silicone/hookup wire, jumper leads, heat shrink | Already owned | — | No purchase needed |
| 1 | LED power supply | Already owned | — | Owner plans to test 5 V / 3 A. Check current draw, wire and dimmer ratings before full brightness |
| as needed | Screws, brass threaded inserts | Already owned | — | M3/M2.5 available |
| 1 | Dartboard | Already owned | — | Existing board |
| 4 | Printed keycaps | Self-print | — | MX-compatible stem |
| 1 | Printed encoder knob | Self-print | — | Fit actual shaft |
| as needed | Camera mounts, LED ring, controller enclosure | Self-print | [B3D Autodarts DIY V2](https://www.printables.com/model/1243079-b3d-autodarts-diy-automatische-punkteerfassung-fur) | Verify STL dimensions before printing |

## Control layout

All controls are **below** the portrait display, with no top-row buttons:

```text
[BACK] [UNDO]   [ROTARY / PRESS = OK]   [CORRECT] [NEXT]
```

Seven GPIO inputs are needed: four buttons, two rotary signals, and the encoder push button.

## Technical checks before assembly

- Confirm actual RP2040-Zero pin mapping and update `docs/WIRING.md` / `firmware/code.py` for the chosen board before flashing firmware.
- Verify OV2710 module footprint and hole spacing against the B3D STL camera mounts.
- Test all three cameras over the UGREEN hub on Debian.
- Measure the actual LED-ring channel circumference; do not assume a 60 cm diameter.
- At the advertised 9 W/m, 1.90 m of COB strip would be rated 17.1 W / 3.42 A at 5 V; 5 V / 3 A is below that full-power figure. Start dimmed and keep LED power separate from the camera USB hub.
- No additional storage, hookup wire, USB-C data cable, or LED supply purchase is currently planned.
