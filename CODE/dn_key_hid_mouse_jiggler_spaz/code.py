import time
import asyncio
import math
import random

import board
import neopixel
import touchio
import usb_hid

from adafruit_hid.mouse import Mouse

touch1_pin = touchio.TouchIn(board.TOUCH1)
touch2_pin = touchio.TouchIn(board.TOUCH2)
touch2_pin.threshold = 23000

pixel_pin = board.EYES
num_pixels = 2
pixels = neopixel.NeoPixel(pixel_pin, num_pixels,
                           brightness=0.08, auto_write=False)
pixels.fill((65, 0, 20))  # Initial LED color
pixels.show()

time.sleep(2)

mouse = Mouse(usb_hid.devices)


DO_MOUSE_JIGGLE = False
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

async def led_updater():
    global DO_MOUSE_JIGGLE
    led_breath_value = 0
    brite = (0.2 * led_breath_value) + 0.005
    while True:
        # set brightness
        led_breath_value = (math.sin(time.monotonic() * 2.0) + 1.0) / 2.0
        brite = (0.15 * led_breath_value) + 0.015
        pixels.brightness = brite
        # set color from mode
        if DO_MOUSE_JIGGLE:
            pixels.fill(GREEN)
        elif not DO_MOUSE_JIGGLE:
            pixels.fill(RED)
        pixels.show()
        await asyncio.sleep(0.04)

async def touch_loop():
    global DO_MOUSE_JIGGLE
    touch1_active = False
    touch2_active = False
    while True:
        if touch1_pin.value and not touch1_active:
            touch1_active = True
            print(" TOUCH 1 ")
        elif not touch1_pin.value and touch1_active:
            touch1_active = False
        if touch2_pin.value and not touch2_active:
            touch2_active = True
            DO_MOUSE_JIGGLE = not DO_MOUSE_JIGGLE
            print(" TOUCH 2 ", DO_MOUSE_JIGGLE)
        elif not touch2_pin.value and touch2_active:
            touch2_active = False
        await asyncio.sleep(0.01)

async def jiggle_mouse(max_distance=8):  # Adjust max distance as needed
    while True:
        if DO_MOUSE_JIGGLE:
            # Generate random movement values
            x_direction = random.choice([-1, 1]) * random.randint(6, max_distance)
            y_direction = random.choice([-1, 1]) * random.randint(3, max_distance)
            mouse.move(x=x_direction, y=y_direction)
        await asyncio.sleep(0.01)  # Adjust delay between movements

async def main():
    tasks = [
        asyncio.create_task(led_updater()),
        asyncio.create_task(touch_loop()),
        asyncio.create_task(jiggle_mouse())
    ]
    await asyncio.gather(*tasks)


# if __name__ == "__name__":
print("Starting")
asyncio.run(main())
