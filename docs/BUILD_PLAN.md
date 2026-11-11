# Build checklist

## Hardware

- [x] Settle on a portrait screen, four buttons and a push-button rotary encoder
- [x] Choose preliminary Pico pin assignments
- [x] Plan separate LED dimming
- [ ] Confirm laptop connections and test portrait display output
- [ ] Choose a storage drive
- [ ] Check camera mounting dimensions and test all three cameras on Linux
- [ ] Choose the LED strip, dimmer and power supply
- [ ] Adjust and print the mounts and console enclosure

## Software

- [x] Build a basic offline menu demo
- [x] Add keyboard input through Pico firmware
- [x] Write down the proposed game rules
- [ ] Configure Debian to start the interface automatically
- [ ] Select and test local camera-based hit detection
- [ ] Implement scoring, bust rules and checkout logic
- [ ] Implement throw history, Undo and manual correction
- [ ] Finish player switching and save game state
- [ ] Test a full match without an internet connection

## Bench tests

| Test | Expected result | Result |
|---|---|---|
| Pico connection | Recognized as a USB keyboard | Not tested |
| Encoder | Up, down and Enter | Not tested |
| Four buttons | Escape, F4, F2 and F5 | Not tested |
| Display | Correct portrait orientation | Not tested |
| Three cameras | Stable simultaneous streams | Not tested |
| Calibration | Dart hits map to the right segments | Not tested |
| X01 bust | Score returns to the start of the turn | Not tested |
| Undo | Previous state is restored | Not tested |
| LED ring | Independent dimming and switching | Not tested |
| Offline restart | Console launches without Wi-Fi | Not tested |

## Before closing the enclosure

Measure button holes, encoder shaft clearance, camera hole spacing and screen dimensions. Test USB power under load. Use 3.3 V Pico signals and keep LED power separate.
