# Darts Console — handoff for game-screen development

**Status:** 2026-11-19. This is the canonical project handoff for a new ChatGPT conversation. **Work directly on GitHub `Arber28/Darts-Console`, branch `main`**, and inspect the current source before making changes. No redesign or destructive rewrite of approved screens.

## Immediate goal

Develop and thoroughly test the **live match / game screen** (and closely related pause, correction and victory interactions). Use high reasoning effort if available. Discuss the desired layout with the user when a visual decision is unresolved; make focused changes in the real `web/index.html` (plus `web/scoring.js` only where required). Commit directly to `main`, then provide a commit-pinned raw.githack.com viewer link. Never claim the laptop has updated until confirmed.

## Project and runtime

- Private GitHub repo: **`Arber28/Darts-Console`**, default integration branch **`main`**.
- Main interface: **`web/index.html`** — standalone HTML/CSS/JS, including views, input/softkeys, selection, animation, player appearance and stats. **`web/scoring.js`** — scoring/replay engine; preserve and test it.
- Old laptop for the Darts Console (NOT the Lenovo Legion 5): Lenovo type **80SV**, Intel HD Graphics 620, 8 GB RAM, 128 GB SATA SSD, Debian 13, internal 1920x1080 display rotated **portrait**, Sway + Chromium kiosk.
- Laptop host usually `Dart-Console`, SSH user `arber`, formerly IP `192.168.0.135`; `arber` is not in sudoers, use `su -` where necessary.
- Local service `http://127.0.0.1:8765/?kiosk`, `darts-web.service` and tty1/Sway kiosk; local data in browser `localStorage`, key **`darts-console-v1`**. Do not clear browser profile/localStorage or silently reset existing matches.
- Updating from GitHub in Settings pulls **web HTML and scoring JS**, but not backend/deploy files. First-time backend and Wi-Fi helper integration requires re-running `deploy/install-kiosk.sh` as root. The WLAN helper additionally requires NetworkManager; do not recklessly alter networking.
- A previous discrepancy between code served locally and the old on-screen Chromium UI was not fully diagnosed. **Do not equate GitHub content, local HTTP 200 and what is visible on the physical screen**; verify the actual display.

## Physical controls — non-negotiable

**Exactly FOUR permanent physical buttons and ONE clickable rotary encoder.** Layout: **Button 1 · Button 2 · Encoder · Button 3 · Button 4**.

- Footer must maintain **five perfectly fixed and uniformly positioned horizontal centers** on ALL screens; labels and encoder center must NEVER shift with changing text, number of actions or view. Buttons are physically mounted.
- Softkey labels are contextual and may be empty where no action applies. Important/destructive action labels may use red.
- Encoder: thin, white outline circle. **White filled center only when clicking does something**; otherwise circle outline ONLY.
- All screens must be operable without a physical keyboard/mouse; rotating selects, pressing activates when appropriate. Do not show irrelevant buttons or helper descriptions.
- Avoid uncontrolled page scroll, focus jumps and accidental activation of the wrong action. Pages should start at top after navigation. Fixed footer never overlaps content. The center position is always exact.

## Design decisions already approved — preserve

- Portrait-oriented, minimal modern **dark** UI; flat colors, strong typography, consistent spacing, **NO gradients** or gratuitous graphic effects.
- Layout needs to fit the real portrait display, and raw.githack.com iPhone Safari preview should be checked as a secondary representation. The physical screen is the actual target.
- Global header: `Darts Console` at upper left, page title at upper right (same font size, weight and position globally). Main menu has its own branded header. Do not let titles grow/shrink between views.
- Keep in-page content clean: **do not append unnecessary paragraphs, explanations, tips, counts or footnotes at the bottom**. Only crucial controls, warnings and information.
- Intro animation/logo on kiosk application startup and automatic switch to main menu. BIOS/Lenovo preboot logo remains unchanged. Animation preference may reduce effects.
- Main menu = tall spaced **2×2 grid**: SPIEL (blue), SPIELER (green), STATISTICS (yellow/orange), SETTINGS (purple), each outlined in its own color. Four respective physical buttons have color-only bars, no text; encoder is inactive and its circle is **not** center-filled on main menu.
- Game selection: equal clean cards **names only**, with Quick Play/All Games filter; no descriptive clutter on cards. Footer actions include BACK, INFO, RANDOM, Quick Play/All Games. Info screen displays short German intro then numbered rules, opens scrolled to top; info softkeys BACK, VORHERIGES, NÄCHSTES, SPIEL AUSWÄHLEN.
- Match setup: compact 2-column player grid with badges, correctly synchronized count and ✓/+, checkout options only where relevant. Bottom softkeys **BACK · GAST · encoder · ALLE/KEINE · START**. BACK to game selection clears all temporary guests; saved player selection may remain. Match player order is randomized when starting.
- Player names **canonical UPPERCASE everywhere**, including persisted profiles, matches, stats and guests. Fixed defaults: **EMRE, ARBER, ADNAN, ATAKAN, AMIR, ALI**. No separate `Emre` profile. New names use uppercase-only on-screen keyboard.
- Player creation/edit is a 3-step flow **NAME → LOGO → FARBE**, with unified vertical positioning between steps. 24 selectable profile logos from **Pack A Fighters** (Ninja, Samurai, Ritter, Wikinger, Gladiator, Assassin, Magier, Soldat), **Pack B Dark/Characters** (Schädel, Dämon, Geist, Joker, Kapuze, Cyborg, Alien, Teufel), **Pack C Symbols** (Krone, Blitz, Flamme, Zielscheibe, Dart, Schild, Stern, Pokal). **NO Pack D**. 24 vivid selectable colors, no black/white/gray in regular selection. Color options are stand-alone circles, NO rectangular frames; selected color has **white circular outline** and checkmark.
- Temporary **GAST 1, GAST 2, ...** always have fixed **WHITE** profile color and an exclusive person-with-plus icon, unavailable to regular players. Guest badge should appear during matches as for all players. Guest IDs are temporary and reset when backing out to game selection.
- Player administration list: uppercase names, match/win counts right-aligned, profile logo and color on the left. Physical buttons: BACK, NEU, BEARBEITEN, LÖSCHEN.
- Statistics screens: concise scoreboard/rankings with top-three gold/silver/bronze identifiers, player details, Records with record holders, History most recent game at top but historical match ID represents original match creation chronology (first match #01). No duplicate list screens. Confirm match deletion; use playful `... du Loser?` confirmation wording as user previously approved. Destructive DELETE in red; removed matches recalculate stats/records. Historical match detail shows remaining points and winner.
- Settings dashboard: in-place **Standard-Checkout** dropdown; in-place **Darstellung** accordion (iOS-like Animationen toggle, Lesbarkeit presets Dezent/Standard/Klar); WLAN & Network; Software Updates; About. No redundant single-setting screens. Do not put explanatory filler/footer blocks below sections. Backend WLAN is only usable after system setup and actual network support.

## Current live match screen: source features already present — do not lose

View `game()` in `web/index.html`, based on `derived()` and `Scoring.replay(data.active)`.
- Current player with **their color+logo badge**, enormous **remaining score** as the screen's primary number; for non-501 modes display mode-appropriate score, lives or target.
- Turn status (up to 3 darts), cumulative turn points; three dart slots. Show checkout recommendations **inside free slots**, gold for suggested aim / white for recorded hits. Do not replace this with a separate sprawling instruction area.
- A subtle **dart-hit animation** when an actual new throw is recorded; not on mere navigation or historical correction.
- Standings with all players, their colored icons and scores; current player identifiable.
- Manual dart entry and score correction/undo must be possible when camera/Autodarts misidentifies a hit. There are already `menu`, `segment` and `correction` screens; inspect how event sourcing and replay work before changes.
- Victory screen with monochrome confetti/animation, clear winner and two prominent actions **Play again** / **Back to main menu**, flat backgrounds and **no gradient**.
- A `MATCH OPTIONS` affordance exists (pause/resume/leave). Keep or improve, do not discard functionality.

## Scoring / game modes

Source `modes` currently contains 14 modes: 501, Cricket, Around the Clock, High Score, Baseball, Knockout, 301, 701, Killer, Shanghai, Gotcha!, Halve-It, Bermuda Triangle, Tic-Tac-Toe.

`web/scoring.js` handles pure scoring, legal dart values/multipliers, match start, event logs, deterministic replay, per-game logic, wins and busts. Checkout variants: **Straight Out**, **Double Out**, **Master Out**. Don't regress:
- Single/double/triple, outer and inner bull, miss; valid dart entry.
- x01 exact-zero checkout, Bust and impossible finish behavior.
- Fourteen game modes' different score semantics and conditions; avoid assuming everything behaves like 501.
- Undo/corrections recompute from recorded history and affect standings, stats and history.
- Preserve stored data schema and upgrade/migrate as needed rather than deleting localStorage.

## How to work on the game page in the new chat

1. Fetch the actual **latest `main`** files: `web/index.html`, `web/scoring.js`, relevant docs. Identify existing game views, key routing, CSS, data schema, and functions handling throws and rematches. Do not base edits solely on old screenshots or assume the last recorded SHA is still current.
2. First show/concretely describe a **portrait-screen game mockup/layout proposal** that follows approved visual rules, for user to adjust. Do not redesign completed player/setup/settings/stats screens.
3. Separate concerns: screen layout; fixed button actions per state (playing, manual input, correction, pause, win); rotary selection; mode-specific variations.
4. Implement incremental, tested updates in `main`. Check syntax and app startup (not only a parse-only `new Function` check), then exercise selection, match transitions, three throws, score updates, busts, checkouts, correction, win/rematch, and multiple modes. Avoid stale-function errors which previously caused a blank UI.
5. Return **commit-pinned** GitHack viewer link: `https://raw.githack.com/Arber28/Darts-Console/<commit-SHA>/web/index.html`. Viewer is a static preview; on-device backend features may be unavailable.
6. Never represent GitHub commits or a successful local HTTP request as proof the physical laptop has updated. Update from Settings or follow the root installer procedure as appropriate and verify on-screen.

## Critical remaining cautions

- Existing virtual key mapping uses Escape/F4/F2/F5. Physical Pico buttons are only useful once firmware and host input mapping are verified; don't claim that hardware is already operational.
- The 3 OV2710 cameras and Autodarts integration are project goals, but **end-to-end live camera scoring is not yet verified**. The UI/scoring must work with manual input while camera setup is pending.
- The user wants highly polished, functional results with minimal text clutter and direct source changes on `main`, not generic example code or lengthy speculative explanations.
