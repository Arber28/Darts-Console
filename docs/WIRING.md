# Pico wiring

The Raspberry Pi Pico reads the four buttons and KY-040 encoder, then sends keyboard events to the laptop over USB.

## Front panel

```text
             PORTRAIT DISPLAY
          ┌────────────────────┐
          │                    │
          │                    │
          └────────────────────┘
     [BACK] [UNDO] (ENCODER) [CORRECT] [NEXT]
```

## Pinout

| Control | Component pin | Pico connection | Keyboard event |
|---|---|---|---|
| Encoder | CLK | GP2 | Up/Down rotation |
| Encoder | DT | GP3 | Rotation direction |
| Encoder | SW | GP4 | Enter |
| Encoder | + | 3V3 OUT | Power |
| Encoder | GND | GND | Ground |
| Back | One contact | GP5 | Escape |
| Undo | One contact | GP6 | F4 |
| Correct | One contact | GP7 | F2 |
| Next | One contact | GP8 | F5 |
| All four buttons | Other contact | GND | Ground |

## Button circuit

Each button uses the Pico's internal pull-up resistor:

```text
Pico GP5 ──────[ BACK button ]────── GND
Pico GP6 ──────[ UNDO button ]────── GND
Pico GP7 ──────[ CORRECT button ]─── GND
Pico GP8 ──────[ NEXT button ]────── GND
```

The encoder's push switch works the same way on GP4. CLK and DT connect to GP2 and GP3.

Use **3.3 V only** for GPIO signals. Do not connect 5 V to a Pico GPIO pin. Check the labels printed on the KY-040 board; pin order varies. If rotation is reversed, swap CLK and DT or change the direction in the firmware.

The Pico connects to the laptop using USB. The LED strip and its separate dimmer have **no connection** to the Pico.

## Software mapping

The key codes are defined in [firmware/code.py](../firmware/code.py) and handled by [web/index.html](../web/index.html). Undo and Next are wired and recognized, but the scoring actions behind them are not implemented yet.
