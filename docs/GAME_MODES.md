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

## Weitere anfängerfreundliche Spielmodi (geplant)

Diese Modi ergänzen die fünf Grundspiele. Die Spielregeln sind als **konkrete Hausregel-Varianten** für die Console definiert; bei einigen Spielen gibt es andere verbreitete Varianten.

### High Score — leicht
- 1–6 Spieler, 10 Runden à maximal 3 Darts (Rundenzahl konfigurierbar).
- Jeder gültige Treffer zählt seinen normalen Punktewert; Fehlwürfe 0.
- Nach der letzten Runde gewinnt der höchste Gesamtwert; Gleichstand wird angezeigt.

### Baseball — leicht
- 1–6 Spieler, 9 Innings/Runden.
- In Runde 1 zählt nur die 1, in Runde 2 die 2 usw. bis zur 9.
- Single = 1 Run, Double = 2 Runs, Triple = 3 Runs; andere Felder 0.
- Nach neun Runden gewinnt die höchste Run-Zahl.

### Gotcha! — leicht bis mittel
- 2–6 Spieler; alle starten bei 0 und versuchen **exakt 301** zu erreichen.
- Treffer erhöhen den Punktestand; wer über 301 kommt, behält den Stand vor dem Zug (Bust).
- Erreicht man **am Ende des eigenen Zuges** exakt den Punktestand eines anderen aktiven Spielers, wird dieser auf 0 zurückgesetzt. Bei mehreren Gleichständen werden alle betroffenen Gegner zurückgesetzt.
- Erreicht man exakt 301, gewinnt man sofort (vor Gotcha-Vergleich).
- Hinweis: Dies ist eine bewusst festgelegte Console-Hausregel, weil Gotcha-Regeln variieren.

### Knockout — leicht bis mittel
- 3–6 Spieler, 3 Leben pro Person.
- Pro Zug werden die Punkte aus bis zu drei Darts addiert.
- Ab dem zweiten Zug im Spiel muss die Zugsumme **strikt höher** sein als die Zugsumme des unmittelbar vorherigen Spielers in der festen Reihenfolge; andernfalls verliert man ein Leben.
- Ausgeschiedene Spieler werden übersprungen; als Vergleich gilt die letzte Zugsumme des vorherigen noch aktiven Spielers.
- Letzter Spieler mit Leben gewinnt. Für den allerersten Spieler gibt es im ersten Durchgang keinen Vergleich.
- Hinweis: Eine vereinfachte Hausregel; Knockout wird auch anders gespielt.

### Halve-It — mittel
- 2–6 Spieler; Zielabfolge standardmäßig: 20, 19, 18, 17, 16, 15, Bull (konfigurierbar).
- In jeder Runde zählen nur Treffer auf das Ziel; Singles/Doubles/Triples zählen ihre normalen Punkte, Outer Bull 25 und Inner Bull 50.
- Trifft ein Spieler in seinen drei Darts kein gültiges Ziel, wird der **bisherige Gesamtpunktestand halbiert**, abgerundet.
- Nach allen Runden gewinnt die höchste Punktzahl.

### Bermuda Triangle — mittel, optional später
- 2–6 Spieler; Variante mit wechselnden Zielen und besonderen Double-/Triple-Aufgaben.
- Wie bei Halve-It wird bei einem Zug ohne gültigen Treffer der Gesamtpunktestand halbiert.
- **Exakte Rundenfolge noch festlegen**, bevor die Spiellogik implementiert wird. Als zusätzliche Variante markieren, nicht als sofort spielbar darstellen.

### Tic-Tac-Toe Darts — mittel, optional später
- 2 Spieler oder zwei Teams.
- Neun festgelegte Zielzahlen werden einem 3×3-Raster zugeordnet.
- Ein Feld wird nach 3 Marks (Single 1, Double 2, Triple 3) besetzt; besetzte Felder sind für den Gegner gesperrt.
- Drei eigene Felder waagrecht, senkrecht oder diagonal gewinnen.
- Zielzahlen und Teamzuordnung vor der Implementierung festlegen.

## Menü-Empfehlung für Anfänger
- **Einfach starten:** High Score, Around the Clock, Baseball, 301 (Straight Out).
- **Etwas mehr Wettbewerb:** 501, Gotcha!, Knockout, Shanghai.
- **Später ausprobieren:** Halve-It, Cricket, Killer, Bermuda Triangle, Tic-Tac-Toe.
- Alle Modi sind aktuell **Spezifikation, nicht implementierte Spielfunktionen**.
