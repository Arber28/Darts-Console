# Parts list

The links below are the selected AliExpress listings. Prices are indicative, not verified live quotes. Confirm the selected variant, shipping to Austria and dimensions before checkout. None of the items below is marked as purchased.

## Selected shopping links

| Qty. | Part | AliExpress | Notes |
|---:|---|---|---|
| 1 | KY-040 / EC11 rotary encoder with push button and knob | [Listing](https://a.aliexpress.com/_EIXCfwA) | Previously seen at €3.13. Use 3.3 V logic with the Pico; verify the specific module pinout |
| 1 | COB LED strip with dimmer | [Listing](https://a.aliexpress.com/_Evwchem) | Selected 3 m, white, 8 mm, 5 V, USB-C; previously seen at €6.42. Confirm power requirements and camera flicker |
| 1 set | Brass heat-set threaded inserts | [Listing](https://a.aliexpress.com/_EwOM3eW) | M2/M2.5/M3/M4 assortment for printed parts |
| 1 | Four-port USB hub | [Listing](https://a.aliexpress.com/_EzoNHt8) | Previously seen at €3.11. Verify that three cameras work simultaneously and that power/bandwidth suffice |
| 1 | USB-C data cable for Pico | [Listing](https://a.aliexpress.com/_EvMdUSa) | Check Pico connector; previously selected 0.25 m cable |
| 1 set | Silicone hookup wire | [Listing](https://a.aliexpress.com/_EyeIR2O) | Previously selected 26 AWG assorted colors |
| 4 | Outemu mechanical switches | [Listing](https://a.aliexpress.com/_EQpNiRG) | Four front-panel buttons; verify keycap and mounting compatibility |
| 1 | RP2040 Pico-compatible board | [Listing](https://a.aliexpress.com/_EJbclAQ) | Previously selected USB-C variant; verify exact board pinout and CircuitPython compatibility |
| 3 | OV9732 USB camera modules | [Listing](https://a.aliexpress.com/_EyPL8E2) | Previously seen at €27.60 for three; verify lens angle, hole spacing, UVC support and cable length |

## Already available or planned

- Existing laptop and its screen, to be mounted in portrait orientation.
- 3D printer for camera mounts, ring and console enclosure; printing cost excluded.
- Existing screws and heat-shrink tubing.
- A soldering iron with adjustable temperature.
- An existing dartboard light; the new LED strip may replace or supplement it.

## Still to confirm

- A suitable **5 V USB power supply** for the 3 m LED strip. A 5 V / 3 A supply was discussed, but the strip's actual maximum current and USB-C input behavior have not been confirmed. Keep LED power separate from the camera hub.
- Ring model and dimensions, camera mounting hole spacing, camera cable reach and LED channel width.
- Whether the selected hub can support all three cameras reliably.
- Whether a storage drive needs replacing before the Debian installation.
- Cable strain relief, fasteners and optional rubber feet after the printed enclosure is designed.

A separate rotary LED dimmer is **not** needed if the selected strip includes a working dimmer. A perfboard and pin headers are **optional**, since the controls can be soldered directly to the Pico. USB camera extension cables should be bought only if the supplied cables prove too short.

## Controls

The portrait display has four buttons below it and one push-button rotary encoder:

```text
BACK    UNDO     [ENCODER]     CORRECT    NEXT
                  press = OK
```

## Reference prints

- [B3D Autodarts DIY V2 camera mounts – Printables](https://www.printables.com/model/1243079-b3d-autodarts-diy-automatische-punkteerfassung-fur)
- [B3D Autodarts DIY V2 – Cults3D](https://cults3d.com/de/modell-3d/spiel/b3d-autodarts-diy-automatic-score-steeldart-v2)

Before finalizing the enclosure or lighting ring, verify dimensions against the exact downloaded STL files and actual delivered components.
