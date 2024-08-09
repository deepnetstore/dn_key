# This sample code opens terminal on macOS and runs cmatrix (if installed)
# you are free to do other cool stuff ;)
import time
import asyncio
import math

import board
import neopixel
import touchio
import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

# Setup touch pin 2
touch2_pin = touchio.TouchIn(board.TOUCH2)
touch2_pin.threshold = 23000  # Adjust the threshold as needed

# Setup LED pixels
pixel_pin = board.EYES
num_pixels = 2
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False)
deep_purple = (80, 0, 130)  # Adjusted RGB for a deeper purple
green = (0, 255, 0)         # RGB for green

# Initialize USB HID devices
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)

touch2_active = False  # Global state for touch activation

async def led_updater():
    while True:
        if not touch2_active:
            brightness = (math.sin(time.monotonic() * 2) + 1) / 2
            min_brightness = 0.4
            max_brightness = 1.0
            scaled_brightness = min_brightness + (max_brightness - min_brightness) * brightness
            pixels.brightness = scaled_brightness
            pixels.fill(deep_purple)
        else:
            pixels.brightness = 1.0
            pixels.fill(green)
        pixels.show()
        await asyncio.sleep(0.05)

async def touch_loop():
    global touch2_active
    while True:
        if touch2_pin.value and not touch2_active:
            touch2_active = True
            print("Touch 2 Activated - Opening Terminal")
            # Commands to open Spotlight and type Terminal
            keyboard.press(Keycode.COMMAND, Keycode.SPACE)  # Command-Space to open Spotlight
            keyboard.release_all()
            await asyncio.sleep(0.5)  # Short delay to let Spotlight open
            keyboard_layout.write("terminal\n")  # Writes 'terminal' and presses Enter
            await asyncio.sleep(1)  # Wait for Terminal to open
            keyboard_layout.write("cmatrix\n")  # Types
        elif not touch2_pin.value and touch2_active:
            touch2_active = False
        await asyncio.sleep(0.1)  # Check touch state every 0.1 seconds

async def main():
    tasks = [
        asyncio.create_task(led_updater()),
        asyncio.create_task(touch_loop())
    ]
    await asyncio.gather(*tasks)

print("Starting")
asyncio.run(main())