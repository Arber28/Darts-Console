# Linux setup

The current target is a Lenovo 80SV with Debian 13.7 AMD64, Intel HD Graphics 620, 8 GB of RAM, a 128 GB SATA SSD and a 1920×1080 internal eDP panel mounted in portrait. The existing installation and SSH service are sufficient.

## Install and start the kiosk

1. Keep a working SSH session or a second virtual terminal available. Run the package install as root.

   ```sh
   apt-get update
   apt-get install --no-install-recommends sway chromium dbus-user-session v4l-utils fonts-dejavu-core
   ```

2. Copy this repository or its `web` and `deploy` directories to the laptop. Run the installer as root from a shell you control.

   ```sh
   sh deploy/install-kiosk.sh
   ```

3. From SSH or a different virtual terminal, activate the display session.

   ```sh
   systemctl restart getty@tty1
   ```

The installer enables the loopback web server on port 8765 and configures tty1 to launch Sway as the dedicated `darts-kiosk` user. Sway runs Chromium fullscreen. A wrapper restarts the browser process after it exits. systemd restarts tty1 when the compositor exits and restarts the web server when it exits. Chromium keeps match state under `/var/lib/darts-kiosk/.config/darts-chromium/`. Keep this profile directory when updating or backing up the console.

To update, rerun the installer with the new source and restart tty1. The installer preserves an existing `/etc/darts-console/sway.conf`.

## Portrait orientation

The default rotates `eDP-1` by 90°. If the image is inverted relative to the mount, set `transform 270` instead in `/etc/darts-console/sway.conf` and restart tty1. On a different laptop, check the connected output under `/sys/class/drm/` and update the output name.

## Verify

```sh
systemctl is-active ssh darts-web getty@tty1
loginctl list-sessions
journalctl -b -u getty@tty1 -u darts-web
sh tests/kiosk-smoke.sh
```

The smoke test runs headless Chromium within its own network namespace. Only loopback is available inside that namespace. At the physical console, verify the image is upright, the whole display is filled, and all Pico controls work. Then test restarting without Ethernet and Wi-Fi from the laptop itself. Keep SSH or a second terminal available when testing crash recovery.

To restore the tty1 login prompt, move the dedicated drop-in `/etc/systemd/system/getty@tty1.service.d/darts-console.conf` out of that directory, run `systemctl daemon-reload`, and restart tty1. Disable `darts-web.service` if the web server is no longer needed.

## Pico controls

Flash [CircuitPython](https://circuitpython.org/board/raspberry_pi_pico/), install `adafruit_hid` to `CIRCUITPY/lib/`, then copy [the firmware](../firmware/code.py) to `CIRCUITPY/code.py`. The device maps rotation, OK, Back, Undo, Correct and Next to arrow keys, Enter, Escape, F4, F2 and F5. See [Wiring](WIRING.md) for pins and [Camera detection](DETECTION.md) for the camera bench procedure.
