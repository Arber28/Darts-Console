# Parts list

Prices are notes from earlier shopping, not current quotes. Check availability, shipping and mounting dimensions before ordering.

| Qty. | Part | Estimated cost | Notes |
|---:|---|---:|---|
| 3 | OV9732 USB UVC camera modules | €38.26 total | Earlier three-camera listing, including €2.27 shipping; module and hole dimensions still need checking |
| 1 | KY-040 rotary encoder with push button | €1.84 | Check shaft length and panel mounting |
| 4 | Normally open push buttons | €2.40 total | Estimate based on €0.60 each |
| 1 | Raspberry Pi Pico (RP2040) | €3–5 | Native USB HID support required |
| 1 | USB cable for Pico | Open | Match the Pico connector |
| 1 | Powered USB hub, if needed | Open | Depends on laptop USB power and bandwidth |
| 3 | USB camera extension cables | Open | Length depends on camera positions |
| As needed | Screws, nuts, inserts and cable ties | Open | Measure against the printed parts |
| 1 | Internal storage drive | Open | 2.5-inch SATA HDD or SSD; model and capacity undecided |
| 1 | LED strip for dartboard ring | Open | Choose voltage, length and density |
| 1 | LED power supply, if needed | Open | Match the LED strip's total load |
| 1 | Standalone rotary PWM LED dimmer with on/off | Open | No Pico connection; model undecided |
| 1 | Existing dartboard light | Already owned | May be reused or replaced |
| As needed | Printed camera mounts and enclosure parts | Already have printer | Printing cost excluded |

**Known parts subtotal: €45.50–€47.50.** This covers only the camera estimate, encoder, four buttons and Pico. It does not include the drive, LED parts, USB accessories, mounting hardware or additional shipping.

## Layout

Portrait display with four buttons below it:

```text
BACK    UNDO     [ENCODER]     CORRECT    NEXT
                  press = OK
```

There are no buttons above the screen and no dedicated Menu button.

## Lighting

The LED ring has its own power supply and rotary dimmer. It must not draw power from Pico GPIO pins. Choose the strip, supply and dimmer together so their voltage and current ratings match. Dimmer location is not decided.

## Laptop

The plan is a lightweight Debian installation that opens the darts interface automatically. The old laptop has 8 GB RAM; performance with three camera streams has not been tested. An SSD would be faster than an HDD, but no drive has been selected.

## References

- [B3D Autodarts DIY V2 camera mounts – Printables](https://www.printables.com/model/1243079-b3d-autodarts-diy-automatische-punkteerfassung-fur)
- [B3D Autodarts DIY V2 – Cults3D](https://cults3d.com/de/modell-3d/spiel/b3d-autodarts-diy-automatic-score-steeldart-v2)
- [GXIVISION OV9732 camera candidate](https://www.ebay.at/itm/356589930771)
- [KY-040 encoder example](https://funduinoshop.com/elektronische-module/keypads-und-buttons/rotary-encoder/ky-040-drehimpulsgeber-rotary-encoder)
- [12 mm button example](https://www.berrybase.at/mikro-drucktaster-12mm-rund-printmontage-schliesser-farbe-schwarz)

Before buying cameras, check the actual mounting hole spacing, lens angle, focus distance, UVC support and compatibility with the eventual detection software. Similar-looking OV9732 boards do not necessarily share the same dimensions.
