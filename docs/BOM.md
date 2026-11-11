# Einkaufsliste / Bill of Materials

Prices below are **previously discussed estimates, not live-verified offers**. Delivery to Austria, taxes and shipping must be checked at checkout.

| Qty | Part | Approx. total | Status / notes |
|---:|---|---:|---|
| 3 | USB UVC OV9732 camera modules (DECXIN candidate) | €38.26 | Previous eBay 3-pack quote including €2.27 shipping; not verified; 38×38 mm PCB, claimed 28×28 mm hole spacing; verify before ordering |
| 1 | KY-040 rotary encoder, preferably threaded shaft | €1.84 | Previous estimate, shipping extra |
| 3 | Normally-open momentary pushbuttons, black | €1.80 | Previous estimate, ensure mount fits printed panel |
| 1 | Raspberry Pi Pico / compatible RP2040 board | €3–5 | Must support native USB HID |
| 1 | USB cable for Pico | unknown | Check connectors on selected Pico |
| 1 | Powered USB hub, if laptop ports/power are insufficient | unknown | May be needed for 3 cameras + Pico |
| 3 | USB camera extension cables | unknown | Length depends on dartboard mounting |
| as needed | Screws, nuts, inserts, cable ties | unknown | Measure from selected STL files |
| 1 | Storage drive (2.5-inch SATA HDD or SSD) | TBD | No specific model, capacity, or price selected yet; verify laptop compatibility before purchase |
| 1 | LED strip for dartboard lighting ring | TBD | Required for planned printed ring; determine ring circumference, LED density, voltage, power supply and diffuser before buying |\n| 1 | LED strip power supply (if needed) | TBD | Match selected strip voltage and total wattage; check whether existing supply can be reused |\n| 1 | Logic-level MOSFET LED switching module | TBD | For PC-controlled on/off (optional PWM dimming) via existing Pico; select based on strip voltage/current; common ground and suitable protection required |\n| 1 | Existing dartboard light | already owned | May be reused or replaced by the planned LED ring |
| printed | Camera mounts, enclosure, button caps | existing printer | Printing costs excluded by preference |

**Known partial subtotal excluding storage, LED strip, LED switch module and any required LED power supply: €43.90–€45.90**, excluding unknown items and any additional shipping. This is **not a complete project total**.

## LED control plan\n- LED ring should be switchable independently from the Darts Console interface.\n- Reuse the Raspberry Pi Pico for control; send commands over USB serial (or implement an equivalent bidirectional interface alongside HID).\n- Pico GPIO drives a suitable logic-level MOSFET module, **never the LED strip directly**.\n- LED strip uses a correctly rated power supply. Voltage, power, and wiring remain to be determined.\n- Optionally add brightness control through PWM. This is planned, not implemented in current firmware/UI.\n\n## Storage and OS plan\n- Debian minimal with automatic launch into a full-screen offline darts UI (kiosk mode).\n- No permanent camera video recording planned.\n- 8 GB laptop RAM expected to be adequate, subject to scoring-engine tests.\n- A 2.5-inch SATA HDD works, but boots and loads more slowly than an SSD.\n- The Hitachi HDD is a **candidate, not an ordered or confirmed component**; SMART screenshot is not a complete health guarantee.\n\n## References
- B3D Autodarts DIY V2 printable mounts: https://www.printables.com/model/1243079-b3d-autodarts-diy-automatische-punkteerfassung-fur
- Alternate listing: https://cults3d.com/de/modell-3d/spiel/b3d-autodarts-diy-automatic-score-steeldart-v2
- GXIVISION OV9732 candidate (previously discussed): https://www.ebay.at/itm/356589930771
- KY-040 example: https://funduinoshop.com/elektronische-module/keypads-und-buttons/rotary-encoder/ky-040-drehimpulsgeber-rotary-encoder
- 12mm button example: https://www.berrybase.at/mikro-drucktaster-12mm-rund-printmontage-schliesser-farbe-schwarz

## Before purchasing cameras
Confirm physical hole spacing, lens angle, fixed-focus range, Linux/Windows UVC compatibility, USB bandwidth and actual compatibility with the chosen offline recognition software. Do not assume that similarly named OV9732 modules have identical mounting holes.
