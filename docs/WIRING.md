# Wiring: Raspberry Pi Pico (RP2040)

**All GPIO signals are 3.3 V. Never feed 5 V into GPIO.**

| Device | Pin | Pico GPIO |
|---|---|---|
| KY-040 | CLK | GP2 |
| KY-040 | DT | GP3 |
| KY-040 | SW | GP4 |
| KY-040 | + | 3V3 OUT |
| KY-040 | GND | GND |
| BACK button | one contact | GP5 |
| CORRECT button | one contact | GP6 |
| MENU button | one contact | GP7 |
| All 3 buttons | other contact | GND |

Firmware uses internal pull-ups for all inputs; a pressed button connects its GPIO to GND.

Connect the Pico to the laptop using USB. The computer recognizes it as a standard HID keyboard once CircuitPython and the HID library are installed.

Some KY-040 boards have resistors and a different pin order: check silk-screen labels, not physical positions. If rotation is reversed, swap CLK/DT or change the firmware mapping. Test the circuit before soldering or printing the enclosure.
