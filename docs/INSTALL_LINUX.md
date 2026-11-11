# Linux installieren – geplanter Offline-Kiosk

## Ziel
Alten Laptop ohne Touchpad/Tastaturgehäuse als Recheneinheit nutzen; Display im **Hochformat**, automatische Anmeldung und Start der Darts Console. Die Anwendung soll **ohne Internet am Aufstellort** funktionieren.

## Wichtige Downloads (offiziell)
- [Debian herunterladen](https://www.debian.org/distrib/)
- [Debian Installationshandbuch](https://www.debian.org/releases/stable/installmanual)
- [Debian Wiki](https://wiki.debian.org/)
- [Debian-Paketübersicht](https://packages.debian.org/stable/)
- [Raspberry Pi Pico – CircuitPython](https://circuitpython.org/board/raspberry_pi_pico/)
- [Adafruit CircuitPython HID Library](https://github.com/adafruit/Adafruit_CircuitPython_HID)

## Voraussetzungen
1. Laptop-Modell, CPU und Anschlüsse prüfen.
2. Passendes internes Laufwerk auswählen (Modell und Größe **noch offen**).
3. Installations-USB-Stick und ggf. USB-Tastatur vorbereiten.
4. Für Installation und Softwarepakete vorübergehend Internet einplanen; später offline testen.
5. Kamera-UVC-Unterstützung und Performance **vor** endgültigem Gehäusebau testen.

## Vorgeschlagener Ablauf
1. Aktuelles Debian-Stable-Installationsmedium von der offiziellen Seite laden und auf USB-Stick schreiben.
2. Debian installieren; möglichst schlank, ohne unnötige Desktop-Dienste. Für die Browser-UI wird dennoch eine grafische Sitzung benötigt.
3. Benutzer für die Console anlegen und Grafik-/Browser-Kiosk einrichten. Konkrete Pakete erst nach Hardwaretest festlegen.
4. Display unter der gewählten Grafik-Sitzung um **90°** drehen; richtige Richtung und Auflösung prüfen.
5. `web/index.html` im Browser als lokale Datei testen. Aktuell ist das **nur eine Bedienungsdemo**, keine echte Treffererkennung.
6. Pico mit CircuitPython und `firmware/code.py` einrichten; Tasten und Drehregler testen.
7. Drei Kameras einzeln und gleichzeitig prüfen. Bei USB-Strom- oder Bandbreitenproblemen aktiven Hub vorsehen.
8. Später Offline-Scoring-Engine anbinden, Autostart und automatische Wiederherstellung nach Neustart einrichten.
9. WLAN/Internet trennen und einen vollständigen Offline-Test durchführen.

## Hilfreiche Prüfkommandos (Debian)

```bash
uname -m
lsusb
lsblk
# Kamerageräte, falls v4l-utils installiert:
v4l2-ctl --list-devices
# USB-/Kernelmeldungen:
dmesg | tail -n 50
```

**Nicht blind ausführen:** Displayrotation und Kiosk-Autostart hängen davon ab, ob X11 oder Wayland läuft und welcher Grafiktreiber verfügbar ist. Keine feste Boot-Konfiguration vor dem Test übernehmen.

## Pico-Tasten
- Drehen: Pfeil hoch/runter
- Drücken: Enter
- BACK: Escape
- UNDO: F4
- CORRECT: F2
- NEXT: F5

Die Tasten senden bereits HID-Eingaben. Vollständige Undo-/Weiter-Funktionen benötigen die spätere Spiellogik.

## Was noch fehlt
- Verifiziertes Laptop-Modell und Displayanschluss
- Ausgewähltes Laufwerk
- Verifizierte Kamera-Module und Halterungsmaße
- Offline-Erkennungssoftware und echte Scoring-Engine
- Finaler Kiosk-Service, Persistenz, Backup/Restore
