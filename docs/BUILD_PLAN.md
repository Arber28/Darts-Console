# Bauplan, Tests und offene Entscheidungen

## Bauphasen
- [x] Bedienkonzept: Hochkant-Display, vier Tasten unten und drückbarer KY-040
- [x] Vorläufige Pico-Pinbelegung und CircuitPython-HID-Demo
- [x] Spielmodus-Regeln dokumentiert
- [x] Eigenständige LED-Steuerung mit Drehdimmer geplant
- [ ] Laptop-Hardware und Displayrotation testen
- [ ] Laufwerk auswählen (noch kein konkretes Modell)
- [ ] Drei Kameras bestellen, Lochabstände und Linux-UVC testen
- [ ] LED-Streifen, Dimmer und passendes Netzteil auswählen
- [ ] Druckteile an reale Komponenten anpassen
- [ ] Linux-Kiosk und Pico-Tasten gemeinsam testen
- [ ] Treffererkennung auswählen/implementieren und kalibrieren
- [ ] Vollständige Spiellogik, Undo, Korrektur, Spielerwechsel entwickeln
- [ ] Dauerlauf- und Offline-Test

## Testmatrix
| Test | Erwartung | Status |
|---|---|---|
| Pico USB erkannt | HID-Tastatur am Laptop | offen |
| Encoder drehen/drücken | Hoch/Runter/Enter | offen |
| Vier Tasten | Escape/F4/F2/F5 | offen |
| Bildschirmrotation | Lesbares Hochformat | offen |
| Drei Kameras parallel | Stabile Videostreams | offen |
| Kamerakalibrierung | Richtige Segmenterkennung | offen |
| Bust bei X01 | Zug korrekt zurückgesetzt | offen |
| Undo nach Spielerwechsel | Historie korrekt wiederhergestellt | offen |
| LED-Ring | Separat schaltbar/dimmbar | offen |
| Offline-Neustart | UI ohne WLAN verfügbar | offen |

## Sicherheit und Praxistipps
- Pico-GPIO ausschließlich mit 3,3-V-Signalen; Taster nach GND.
- LEDs nicht direkt an Pico anschließen; eigener Dimmer und geeignete Versorgung.
- Netzteile und USB-Verbraucher nicht überlasten.
- Vor endgültigem Druck Tasterdurchmesser, Encoder-Gewinde, Displaymaße und Kameralöcher messen.
- Automatische Erkennung und Scoring sind **noch nicht fertig**. Kein Test gilt als bestanden, nur weil ein Menü angezeigt wird.
