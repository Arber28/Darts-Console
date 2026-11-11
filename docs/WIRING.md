# Wiring: Raspberry Pi Pico (RP2040)

**All GPIO signals are 3.3 V. Never feed 5 V into GPIO.**

## Portrait console control layout
Below the portrait display, from left to right: **BACK | UNDO | [KY-040 rotary encoder] | CORRECT | NEXT**. The KY-040 is also a pushbutton (OK/Enter). No upper row or separate MENU button.

| Device | Pin | Pico GPIO | USB HID key |
|---|---|---|---|
| KY-040 | CLK | GP2 | Arrow up/down with DT |
| KY-040 | DT | GP3 | Direction input |
| KY-040 | SW | GP4 | Enter |
| KY-040 | + | 3V3 OUT | — |
| KY-040 | GND | GND | — |
| BACK button | one contact | GP5 | Escape |
| UNDO button | one contact | GP6 | F4 |
| CORRECT button | one contact | GP7 | F2 |
| NEXT button | one contact | GP8 | F5 |
| All four buttons | other contact | GND | — |

All button inputs use internal pull-ups: pressed = GPIO connected to GND. Connect Pico via USB; CircuitPython and Adafruit HID library are required. KY-040 pin order varies: check board labels. Swap CLK/DT or firmware direction mapping if rotation is reversed.

The LED ring is **independent**: standalone rotary PWM dimmer and appropriately rated LED supply, with no Pico GPIO connection.

**Current demo limitation:** The web UI handles F4/F5 as control shortcuts, but true scoring history and player advancement require the future scoring engine; do not interpret a demo message as an actual score change.
