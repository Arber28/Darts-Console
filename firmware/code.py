# Raspberry Pi Pico / CircuitPython
# KY-040 rotary encoder and four buttons as a USB keyboard.
# Copy the adafruit_hid library to CIRCUITPY/lib/ before running.

import time

import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode


keyboard = Keyboard(usb_hid.devices)


def input_pin(pin):
    io = digitalio.DigitalInOut(pin)
    io.direction = digitalio.Direction.INPUT
    io.pull = digitalio.Pull.UP
    return io


clk = input_pin(board.GP2)
dt = input_pin(board.GP3)

# Each button connects its GPIO pin to ground when pressed.
buttons = [
    (input_pin(board.GP4), Keycode.ENTER),   # Encoder press
    (input_pin(board.GP5), Keycode.ESCAPE),  # Back
    (input_pin(board.GP6), Keycode.F4),      # Undo
    (input_pin(board.GP7), Keycode.F2),      # Correct
    (input_pin(board.GP8), Keycode.F5),      # Next
]

last_clk = clk.value
last_button_states = [pin.value for pin, _ in buttons]
last_button_times = [0.0] * len(buttons)
last_step = 0.0


while True:
    now = time.monotonic()
    current_clk = clk.value

    # Read rotation on the falling CLK edge; ignore very short glitches.
    if last_clk and not current_clk and now - last_step > 0.004:
        key = Keycode.DOWN_ARROW if dt.value else Keycode.UP_ARROW
        keyboard.send(key)
        last_step = now
    last_clk = current_clk

    # Send one keypress for each debounced button press.
    for index, (pin, key) in enumerate(buttons):
        state = pin.value
        if state != last_button_states[index] and now - last_button_times[index] > 0.035:
            last_button_times[index] = now
            last_button_states[index] = state
            if not state:
                keyboard.send(key)

    time.sleep(0.002)
