# Build checklist

## Verified

- [x] Audit the existing Debian installation, SSD, graphics and USB inventory over SSH.
- [x] Install the lightweight kiosk and verify Sway, Chromium, loopback HTTP and SSH after reboot.
- [x] Implement event replay, busts, checkout rules, Corrections and Undo across turn boundaries.
- [x] Implement the fourteen modes, with explicit setup for house targets and round sequences.
- [x] Save profiles, the active match and completed results locally.
- [x] Exercise scoring through the keyboard path in Chromium at 1080×1920 with only loopback networking.
- [x] Verify nominal board regions and camera consensus on synthetic coordinates.

## Hardware acceptance

- [ ] Confirm upright portrait display and distance readability at the throw line.
- [ ] Verify browser relaunch after killing its process.
- [ ] Verify a cold start with Ethernet unplugged and Wi-Fi disabled.
- [ ] Connect the Pico, test every button and check real encoder direction and debounce.
- [ ] Mount and test simultaneous camera feeds, calibration, real throws and board clearings.
- [ ] Measure LED flicker in all three streams and confirm independent dimming.
- [ ] Validate camera candidates before connecting them to live scoring.

See the [Linux setup](INSTALL_LINUX.md) and [camera bench procedure](DETECTION.md) for verification steps.
