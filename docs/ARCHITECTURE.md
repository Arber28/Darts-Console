# Architektur und Grafiken

> Planungsstand, **kein Nachweis einer fertigen automatischen Punkteerkennung**. Mermaid-Diagramme werden direkt auf GitHub gerendert.

## 1. Gesamtsystem

```mermaid
flowchart TD
  D["Dartscheibe"] --> C1["USB-Kamera 1"]
  D --> C2["USB-Kamera 2"]
  D --> C3["USB-Kamera 3"]
  C1 --> L["Alter Laptop / Debian Linux"]
  C2 --> L
  C3 --> L
  P["Pico RP2040<br/>4 Tasten + KY-040"] -->|"USB HID: Tastaturbefehle"| L
  L -->|"Bildausgabe, 90° gedreht"| S["Laptop-Display hochkant"]
  L --> V["Offline-Treffererkennung<br/>(noch auszuwählen)"]
  V --> G["Scoring-Engine<br/>(noch zu implementieren)"]
  G --> UI["Darts Console UI"]
  UI --> S
  PS["Passendes LED-Netzteil"] --> DIM["Separater PWM-Drehdimmer<br/>Ein/Aus + Helligkeit"]
  DIM --> LED["LED-Ring"]
  LED -.-> D
```

**Wichtig:** Die LED-Beleuchtung ist elektrisch unabhängig von Pico und Laptop. Kein LED-Strom über GPIO.

## 2. Gehäuseansicht – Vorderseite, schematisch

```text
       ┌────────────────────────────┐
       │         DISPLAY            │
       │          HOCHKANT          │
       │                            │
       │     Punkte / Spieler       │
       │     Menüs / Spielmodi      │
       │                            │
       └────────────────────────────┘
       [ZURÜCK] [UNDO]  (◉)  [KORR.] [WEITER]
                         KY-040
                      drehen + drücken
```

Die Darstellung ist **nicht maßstabsgetreu**. Tasten und Drehregler befinden sich **alle unter dem Display**.

## 3. GPIO-Zuordnung

```mermaid
flowchart LR
  E["KY-040<br/>CLK / DT / SW"] -->|"GP2 / GP3 / GP4"| P["Raspberry Pi Pico"]
  B["ZURÜCK"] -->|"GP5"| P
  U["UNDO"] -->|"GP6"| P
  K["KORREKTUR"] -->|"GP7"| P
  N["WEITER"] -->|"GP8"| P
  P -->|"USB"| PC["Laptop"]
```

Taster jeweils zwischen GPIO und GND; interne Pull-ups aktiviert. KY-040 nur mit 3,3 V betreiben. Detaillierte Tabelle: [WIRING.md](WIRING.md).

## 4. Geplanter Softwarefluss

```mermaid
flowchart LR
  CAM["3 Kamera-Streams"] --> DET["Trefferlokalisierung"]
  DET --> MAP["Segment + Multiplikator<br/>z. B. T20"]
  MAP --> RULE["Spielmodus-Regeln"]
  RULE --> STATE["Spielstand / Zug-Historie"]
  STATE --> DISPLAY["Vollbild-UI"]
  HID["Pico HID"] --> DISPLAY
  DISPLAY -->|"Korrektur / Undo"| STATE
```

**Noch offen:** Auswahl und Test einer lokal lauffähigen Kamera-/Scoring-Lösung, Kalibrierung, Synchronisierung der Kameras, zuverlässige Korrekturen und persistente Speicherung.

## 5. Stromversorgung (Blockschaltbild, kein Netzschaltplan)

```mermaid
flowchart TD
  MAINS["230 V Steckdose"] --> LAP["Original-Laptop-Netzteil"]
  LAP --> LAPTOP["Laptop"]
  LAPTOP --> USB["USB: Pico + Kameras<br/>ggf. aktiver Hub"]
  MAINS --> SUPPLY["Geeignetes, geprüftes LED-Netzteil"]
  SUPPLY --> DIMMER["PWM-Drehdimmer"]
  DIMMER --> STRIP["LED-Streifen"]
```

230-V-Seite **nicht selbst offen verdrahten**. Fertiges, passendes Netzteil verwenden; LED-Spannung, Stromaufnahme, Kabelquerschnitt und Dimmerbelastbarkeit vor dem Kauf abgleichen.
