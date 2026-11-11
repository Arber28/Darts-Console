# Linux setup

The old laptop will run Debian with a portrait display and start the Darts Console automatically. Wi-Fi won't be available where the board is installed, so everything must work offline after setup.

## Downloads

- [Debian installer](https://www.debian.org/distrib/)
- [Debian installation guide](https://www.debian.org/releases/stable/installmanual)
- [Debian Wiki](https://wiki.debian.org/)
- [Debian packages](https://packages.debian.org/stable/)
- [CircuitPython for Raspberry Pi Pico](https://circuitpython.org/board/raspberry_pi_pico/)
- [Adafruit USB HID library](https://github.com/adafruit/Adafruit_CircuitPython_HID)

## Before installation

Check the laptop model and USB ports, choose a compatible internal drive and prepare a bootable Debian USB stick. Keep a keyboard available for setup. Internet access is useful during installation; it shouldn't be required afterward.

## Setup order

1. Install the current Debian stable release from the official installer.
2. Set up a lightweight graphical session and a browser for the interface. Exact packages will depend on the laptop.
3. Rotate the display by 90 degrees in the graphical settings and check the resolution.
4. Open `web/index.html` locally to test the interface.
5. Install CircuitPython and the HID library on the Pico, then copy over `firmware/code.py`.
6. Test the encoder and all four buttons with the laptop.
7. Check the USB cameras one by one, then all three at once. Add a powered hub if USB power or bandwidth becomes a problem.
8. Once camera detection and scoring work, configure the interface to start automatically after boot.
9. Disconnect from the network and test a full restart.

There is no final kiosk service configuration yet. Choose the startup method after confirming whether the system uses X11 or Wayland.

## Useful commands

```bash
# CPU architecture
uname -m

# Connected USB devices
lsusb

# Available drives
lsblk

# Video devices (requires v4l-utils)
v4l2-ctl --list-devices

# Recent kernel messages
dmesg | tail -n 50
```

## Button mapping

| Control | Keyboard input |
|---|---|
| Encoder clockwise / counterclockwise | Arrow Down / Arrow Up |
| Encoder press | Enter |
| Back | Escape |
| Undo | F4 |
| Correct | F2 |
| Next | F5 |

The interface demo reacts to these inputs. Actual scoring, Undo and turn advancement still need to be implemented.

## Open hardware details

- Laptop display connection and graphics driver
- Storage drive model and capacity
- Camera module dimensions and Linux compatibility
- Detection engine and its performance with three cameras
