# System layout

## Hardware

```mermaid
flowchart TD
    D["Dartboard"] --> A["USB camera 1"]
    D --> B["USB camera 2"]
    D --> C["USB camera 3"]
    A --> PC["Laptop running Debian"]
    B --> PC
    C --> PC
    BUTTONS["4 buttons + KY-040"] --> PICO["Raspberry Pi Pico"]
    PICO -->|"USB keyboard input"| PC
    PC -->|"Portrait output"| SCREEN["Laptop display"]
    SUPPLY["LED power supply"] --> DIMMER["Rotary LED dimmer"]
    DIMMER --> RING["Dartboard LED ring"]
```

The lighting circuit is independent from the laptop and Pico.

## Front panel

```text
       ┌────────────────────────────┐
       │                            │
       │       DARTS CONSOLE        │
       │                            │
       │      Portrait screen       │
       │                            │
       │                            │
       └────────────────────────────┘
        [BACK] [UNDO]  (●)  [CORRECT] [NEXT]
                        KY-040
                      turn / press
```

The drawing shows placement only; it is not to scale.

## Controls

```mermaid
flowchart LR
    ENC["KY-040: CLK / DT / SW"] -->|"GP2 / GP3 / GP4"| PICO["Raspberry Pi Pico"]
    BACK["Back"] -->|"GP5"| PICO
    UNDO["Undo"] -->|"GP6"| PICO
    CORR["Correct"] -->|"GP7"| PICO
    NEXT["Next"] -->|"GP8"| PICO
    PICO -->|"USB HID"| PC["Laptop"]
```

[Full wiring table](WIRING.md)

## Scoring pipeline

```mermaid
flowchart LR
    CAM["Three USB cameras"] --> DET["OpenCV calibration and bench detector"]
    DET --> OUT["Local JSON candidate stream"]
    KEYS["Pico USB keyboard input"] --> UI["Chromium kiosk"]
    UI -->|Manual throws and corrections| LOG["Match event log"]
    LOG --> RULES["Scoring replay"]
    RULES --> UI
    LOG --> STORE["Chromium local storage"]
    STORE --> LOG
```

Each event identifies the player, round and dart slot. Corrections replay the log. Events that no longer fit after a correction are visible in the history as skipped. The camera stream remains independent during hardware validation.

## Startup

```mermaid
flowchart LR
    SYSTEMD["systemd"] --> WEB["Loopback web server"]
    SYSTEMD --> TTY["tty1 kiosk session"]
    TTY --> SWAY["Sway, portrait Wayland output"]
    SWAY --> WATCH["Browser launcher"]
    WATCH --> CHROME["Chromium fullscreen"]
    CHROME --> WEB
```
## Power

```mermaid
flowchart TD
    MAINS["Wall outlet"] --> LAPPSU["Original laptop power adapter"]
    LAPPSU --> LAP["Laptop"]
    LAP --> USB["USB cameras and Pico<br/>powered hub if needed"]
    MAINS --> LEDPSU["Suitable LED power supply"]
    LEDPSU --> DIM["PWM dimmer"]
    DIM --> STRIP["LED strip"]
```

Use a suitable enclosed LED power supply. Do not expose or modify mains wiring. Check voltage, current draw and dimmer ratings before assembling the LED circuit.
