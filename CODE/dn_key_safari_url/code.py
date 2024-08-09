#This sample code uses spotlight to open safari on macOS or iOS and navigate to a webpage
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

async def led_updater():
    while True:
        brightness = (math.sin(time.monotonic() * 2) + 1) / 2
        pixels.brightness = 0.4 + 0.6 * brightness  # Adjust brightness dynamically
        pixels.fill(deep_purple if not touch2_pin.value else green)
        pixels.show()
        await asyncio.sleep(0.05)

async def touch_loop():
    while True:
        if touch2_pin.value:
            print("Touch 2 Activated - Opening Safari")
            # Commands to open Spotlight and type Safari
            keyboard.press(Keycode.COMMAND, Keycode.SPACE)  # Command-Space to open Spotlight
            keyboard.release_all()
            await asyncio.sleep(0.5)
            keyboard_layout.write("safari\n")
            await asyncio.sleep(1)  # Wait for Safari to open

            # Ensure focus on the address bar
            keyboard.press(Keycode.COMMAND, Keycode.L)  # Command-L to focus the address bar
            keyboard.release_all()
            await asyncio.sleep(0.5)

            # Type the URL and press Enter
            url = "https://deepnet.store/pages/dn_key_s3"
            for char in url:
                keyboard_layout.write(char)
                await asyncio.sleep(0.001)  # Small delay between characters to ensure they are registered
            keyboard.press(Keycode.RETURN)
            keyboard.release_all()

            await asyncio.sleep(2)  # Allow some time for the page to load
            while touch2_pin.value:
                await asyncio.sleep(0.1)  # Hold until the touch is released

        await asyncio.sleep(0.1)  # Check touch state every 0.1 seconds

async def main():
    tasks = [
        asyncio.create_task(led_updater()),
        asyncio.create_task(touch_loop())
    ]
    await asyncio.gather(*tasks)

print("Starting")
asyncio.run(main())