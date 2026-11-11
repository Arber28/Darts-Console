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
    CAM["Three camera feeds"] --> DET["Hit detection"]
    DET --> SEG["Board segment"]
    SEG --> RULES["Game rules"]
    RULES --> STATE["Scores and throw history"]
    STATE --> UI["Console interface"]
    KEYS["Pico controls"] --> UI
    UI -->|"Corrections"| STATE
```

This is the intended software flow, not a working camera pipeline. The detection engine, camera calibration, scoring history and correction logic still need to be implemented.

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
