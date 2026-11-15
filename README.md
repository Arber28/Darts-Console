# Darts Console

An offline darts console for a portrait laptop display, driven by four buttons and a push-button rotary encoder. Its standalone web interface supports manual scoring, fourteen game modes, saved profiles, guests, match history and statistics.

## Run

Open `web/index.html` in a browser to try the interface. For the dedicated 9:16 display, follow the [Debian kiosk setup](docs/INSTALL_LINUX.md). The local kiosk uses Chromium and Sway.

Turn the encoder to navigate and press it to confirm. Back returns to the previous screen. Undo reverses the last recorded throw. Correct opens the throw history, and Next ends the turn. On a keyboard, the matching keys are arrows, Enter, Escape, F4, F2 and F5. During a match, choose **Enter throw** to record a dart manually.

Default profiles are Emre, Arber, Adnan, Atakan, Amir and Ali. Player order is randomized at match start.

## Tests

```sh
node --test tests/scoring.test.js
python3 -m unittest discover -s tests -p 'test_*.py'
sh tests/kiosk-smoke.sh
```

The kiosk smoke test requires Debian with Chromium and unprivileged user namespaces. It runs with only loopback networking.

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Build checklist](docs/BUILD_PLAN.md)
- [Game rules](docs/GAME_MODES.md)
- [Hardware parts](docs/BOM.md)
- [Pico firmware and wiring](docs/WIRING.md)
- [Camera calibration and detection bench procedure](docs/DETECTION.md)
- [Reference links](docs/LINKS.md)

The camera bench tool awaits physical validation. Use manual scoring on the kiosk.
