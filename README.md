# Darts Console

A standalone darts scoring console built from an old laptop, three USB cameras and a Raspberry Pi Pico.

The laptop runs the interface on a portrait-mounted screen. Four buttons and a push-button rotary encoder handle navigation. A separate dimmer controls the dartboard light.

## Project status

The hardware layout is settled, and there is a working keyboard-controlled interface demo. Camera-based hit detection and the full scoring engine still need to be built and tested.

## Documentation

| Document | Contents |
|---|---|
| [System layout](docs/ARCHITECTURE.md) | Hardware diagram, front panel, signal flow and power |
| [Parts list](docs/BOM.md) | Components, estimated costs and purchase notes |
| [Wiring](docs/WIRING.md) | Pico pinout and button connections |
| [Linux setup](docs/INSTALL_LINUX.md) | Debian installation and offline kiosk plan |
| [Game rules](docs/GAME_MODES.md) | Rules for planned game modes |
| [Build checklist](docs/BUILD_PLAN.md) | Remaining jobs and tests |
| [Links](docs/LINKS.md) | Downloads, documentation and printable mounts |

## Controls

All controls sit **below** the portrait screen:

```text
[BACK]  [UNDO]  (ROTARY / OK)  [CORRECT]  [NEXT]
```

- Turn the encoder to move through a menu; press it to confirm.
- Back returns to the previous screen.
- Undo reverses the last throw once scoring history is implemented.
- Correct opens manual hit correction.
- Next ends a turn or moves to the next player once game logic is implemented.

The Pico sends standard USB keyboard events. See [Wiring](docs/WIRING.md) for the key mapping.

## Try the interface

Open `web/index.html` in a browser. No server or internet connection is needed.

Keyboard controls: Up/Down, Enter, Escape, F4 (Undo), F2 (Correct), F5 (Next). The Undo and Next shortcuts currently show placeholders; they do not alter scores.

## Pico firmware

1. Install [CircuitPython for Raspberry Pi Pico](https://circuitpython.org/board/raspberry_pi_pico/).
2. Copy Adafruit's `adafruit_hid` library into `CIRCUITPY/lib/`.
3. Copy `firmware/code.py` to `CIRCUITPY/code.py`.
4. Connect the encoder and buttons according to [Wiring](docs/WIRING.md).

## Players

Default names: Emre, Arber, Adnan, Atakan, Amir and Ali. Guest players can be added. Player order is randomized when a game starts.

## Next jobs

Test the cameras on Linux, choose an offline detection method, implement scoring and corrections, then build the enclosure and configure automatic startup.
