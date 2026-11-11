# CircuitPython / Raspberry Pi Pico: rotary encoder + 3 buttons -> USB keyboard
# Install adafruit_hid library in CIRCUITPY/lib/adafruit_hid first.
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
buttons = [
    (input_pin(board.GP4), Keycode.ENTER),
    (input_pin(board.GP5), Keycode.ESCAPE),
    (input_pin(board.GP6), Keycode.F2),
    (input_pin(board.GP7), Keycode.F3),
]
last_clk = clk.value
last_button_states = [pin.value for pin, _ in buttons]
last_button_times = [0.0] * len(buttons)
last_step = 0.0

while True:
    now = time.monotonic()
    current_clk = clk.value
    # Emit one step on each falling CLK edge, with a short noise filter.
    if last_clk and not current_clk and now - last_step > 0.004:
        key = Keycode.DOWN_ARROW if dt.value else Keycode.UP_ARROW
        keyboard.send(key)
        last_step = now
    last_clk = current_clk

    for i, (pin, key) in enumerate(buttons):
        state = pin.value
        if state != last_button_states[i] and now - last_button_times[i] > 0.035:
            last_button_times[i] = now
            last_button_states[i] = state
            if not state:  # active low
                keyboard.send(key)
    time.sleep(0.002)
