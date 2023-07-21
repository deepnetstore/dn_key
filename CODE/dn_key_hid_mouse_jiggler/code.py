import time
import board
import neopixel
import asyncio
import touchio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.mouse import Mouse
import math

touch1_pin = touchio.TouchIn(board.TOUCH1)
touch2_pin = touchio.TouchIn(board.TOUCH2)
touch2_pin.threshold = 13000

pixel_pin = board.EYES
num_pixels = 2
pixels = neopixel.NeoPixel(pixel_pin, num_pixels,
                           brightness=0.05, auto_write=False)
pixels.fill((65, 0, 20))
pixels.show()

mouse = Mouse(usb_hid.devices)
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)  # We're in the US :)

DO_MOUSE_JIGGLE = True
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


class LEDStatus:
    '''
    container for led status
    Modes:
    0 = rainbow cycle/ standby
    1 = no cycle, show specified color
    Color:
    - holds two color values, 
    - one for each eye.
    '''
    left_eye = (0, 0, 0)
    right_eye = (0, 0, 0)
    mode = 1
    color = [left_eye, right_eye]  # holds a color for each eye
    auto_reset = True
    display_duration = 1    # seconds to show newest LED status
    LEFT = 0
    RIGHT = 1
    mode_set = False

    def set_colors(self, left, right):
        self.color = [left, right]
        self.mode = 1

    def set_eye_color(self, eye, color):
        self.color[eye] = color
        self.mode = 1

    def get_colors(self):
        return self.color

    async def blink_eyes(self, n_blinks=3, delay_time=0.1):
        for i in range(n_blinks):
            pixels.fill(0)
            pixels.show()
            await asyncio.sleep(delay_time)
            pixels[0] = self.color[self.LEFT]
            pixels[1] = self.color[self.RIGHT]
            pixels.show()
            await asyncio.sleep(delay_time)


async def led_updater(led_status):
    # sync_eyes = True
    # wait = 0.05
    led_status.left_eye = GREEN
    led_status.right_eye = GREEN
    led_status.color = [
        led_status.left_eye,
        led_status.right_eye
    ]
    led_breath_value = 0
    brite = (0.2 * led_breath_value) + 0.005
    print("started LED Updater")
    while True:
        led_breath_value = (math.sin(time.monotonic() * 2.0) + 1.0) / 2.0
        brite = (0.15 * led_breath_value) + 0.015
        if led_status.mode == 0:
            led_status.mode = 1
            # for j in range(255):
            #     for i in range(num_pixels):
            #         rc_index = (i * 256 // 1 if sync_eyes else (1 + i)) + j
            #         pixels[i] = colorwheel(rc_index & 255)
            #     pixels.show()
            #     await asyncio.sleep(0)
        elif led_status.mode == 1:
            if not led_status.mode_set:
                print("Setting Custom mode")
                pixels[0] = led_status.color[led_status.LEFT]
                pixels[1] = led_status.color[led_status.RIGHT]
                await led_status.blink_eyes()
                await asyncio.sleep(led_status.display_duration)
                if led_status.auto_reset:
                    led_status.mode = 0
                led_status.mode_set = True
            pixels.brightness = brite
            pixels.show()
        await asyncio.sleep(0)


async def touch_loop(led_status):
    global DO_MOUSE_JIGGLE
    touch1_active = False
    touch2_active = False
    after_touch_wait_time = 0.15
    print("Started Touch Loop")
    while True:
        if touch1_pin.value and not touch1_active:
            touch1_active = True
            led_status.auto_reset = not led_status.auto_reset
            print("TOUCH 1", led_status.mode, led_status.auto_reset)
            led_status.set_eye_color(led_status.LEFT, BLUE)
            led_status.set_eye_color(led_status.RIGHT, (0, 0, 0))
            await asyncio.sleep(after_touch_wait_time)
            led_status.mode = 0 if led_status.auto_reset else 1
            led_status.mode_set = True  # if led_status.mode else False
        elif not touch1_pin.value and touch1_active:
            touch1_active = False
        if touch2_pin.value and not touch2_active:
            touch2_active = True
            led_status.mode_set = False
            print("TOUCH 2", led_status.mode, led_status.auto_reset)
            led_status.set_eye_color(
                led_status.LEFT, GREEN if not DO_MOUSE_JIGGLE else RED)
            led_status.set_eye_color(
                led_status.RIGHT, GREEN if not DO_MOUSE_JIGGLE else RED)
            DO_MOUSE_JIGGLE = not DO_MOUSE_JIGGLE
            await asyncio.sleep(after_touch_wait_time)
        elif not touch2_pin.value and touch2_active:
            touch2_active = False
        await asyncio.sleep(0)


async def jiggle_mouse(led_status, amount=2):
    while True:
        if DO_MOUSE_JIGGLE:
            Xs = int(math.sin(time.monotonic()) * amount)
            Ys = int(math.cos(time.monotonic()) * amount)
            mouse.move(x=Xs, y=Ys)
        await asyncio.sleep(0.25)
        # await asyncio.sleep(0)


async def hid_device_loop(led_status):
    while True:
        # do hid thing...
        ...


async def main():
    print("Starting Tasks")
    led_status = LEDStatus()

    tasks = [
        asyncio.create_task(led_updater(led_status)),
        asyncio.create_task(touch_loop(led_status)),
        asyncio.create_task(jiggle_mouse(led_status))
    ]

    await asyncio.gather(*tasks)

asyncio.run(main())
