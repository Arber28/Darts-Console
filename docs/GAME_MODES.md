# Spielmodi – Spezifikation (geplant)

Jeder aktive Spieler wirft bis zu drei Darts pro Zug. Automatische Treffererkennung und Spiel-Engines sind noch **nicht implementiert**. Manuelle Korrektur erkannter Treffer muss in jedem Modus möglich sein.

## 301 / 501 / 701 (X01)
- Startwert je nach Modus; Trefferpunkte abziehen.
- Exakt 0 zum Sieg; Checkout konfigurierbar (insbesondere Straight Out oder Double Out).
- Bust: Überwerfen; bei Double Out auch Rest 1 oder Null ohne gültiges Doppel. Der **gesamte Zug** wird auf den Punktestand vor Zugbeginn zurückgesetzt und beendet.
- Optional weitere Checkout-Regeln später.

## Cricket
- Ziele: 15, 16, 17, 18, 19, 20, Bull.
- Pro Ziel 3 Marks zum Schließen. Single/Double/Triple zählen 1/2/3 Marks; Outer Bull 1, Inner Bull 2.
- Überzählige Marks nach dem Schließen erzielen Punkte nur, solange mindestens ein Gegner das Ziel noch offen hat. Punkte entsprechen Zielwert × überschüssige Marks (Bull: 25 je Mark).
- Ist ein Ziel bei allen geschlossen, gibt es dort keine Punkte mehr.
- Sieg: alle Ziele geschlossen und Punktestand mindestens so hoch wie bei jedem Gegner.
- Teammodus später optional.

## Around the Clock
- Jeder startet bei Ziel 1 und arbeitet sich aufsteigend bis 20 vor.
- Single, Double und Triple zählen jeweils als **ein** erfolgreiches Ziel.
- Nach Treffer sofort zum nächsten Ziel, auch innerhalb desselben Zuges.
- Optional Bull als letztes Ziel.
- Sieg: zuerst alle geforderten Ziele getroffen.

## Killer (Handout-Variante)
- Jedem Spieler wird eine **eindeutige** Zahl von 1 bis 20 zugewiesen; ideal 3–8 Spieler.
- Start mit 3 Leben. Eigene Zahl zunächst mit 3 Marks aktivieren (Single 1, Double 2, Triple 3), um Killer zu werden.
- Als Killer entzieht man mit Treffern auf die Zahl eines Gegners 1/2/3 Leben (Single/Double/Triple).
- Bei 0 Leben ausgeschieden; letzter aktiver Spieler gewinnt.
- **Noch zu klären:** Zahlzuweisung (zufällig/manuell), Verhalten bei Treffern auf eigene Zahl nach Aktivierung, ob ausgeschiedene Spieler weiter Ziele darstellen und ob ein Treffer mehr als verbleibende Leben abziehen darf (vorgeschlagen: auf 0 begrenzen).

## Shanghai (7 Runden)
- In Runde 1 zählt nur die 1, in Runde 2 nur die 2 usw. bis Runde 7.
- Je Spieler 3 Darts pro Runde; gültige Treffer geben Single ×1, Double ×2, Triple ×3 Punkte.
- Single + Double + Triple der aktuellen Zahl innerhalb **eines Zuges**: sofortiger Shanghai-Sieg, unabhängig von Reihenfolge.
- Sonst gewinnt nach Runde 7 der Spieler mit den meisten Punkten.
- **Noch zu klären:** Gleichstand (gemeinsamer Sieg oder Stechen).

## Gemeinsame Bedienung
- Bestehende feste Spieler: Emre, Arber, Adnan, Atakan, Amir, Ali; Gäste optional.
- Spielerreihenfolge beim Spielstart zufällig mischen (ohne Animation).
- Jeder Modus benötigt eine eigene Ergebnis-/Statusanzeige und Korrekturmöglichkeit.
- Korrektur muss auch nach Bust, Eliminierung und einem möglichen Sieg korrekt rückgängig machen können.

## Geplanter Spieleabend
Around the Clock → 501 → Cricket → Shanghai → Killer.
