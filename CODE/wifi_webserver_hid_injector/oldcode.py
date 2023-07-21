import time
import board
from rainbowio import colorwheel
import neopixel
import asyncio
import touchio
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
import adafruit_ducky as ducky
import math
import socketpool
import wifi
from secrets import secrets

from adafruit_httpserver.mime_type import MIMEType
from adafruit_httpserver.request import HTTPRequest
from adafruit_httpserver.response import HTTPResponse
from adafruit_httpserver.server import HTTPServer

print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])

print("Available WiFi networks:")
for network in wifi.radio.start_scanning_networks():
    print("\t%s\t\tRSSI: %d\tChannel: %d" % (str(network.ssid, "utf-8"),
            network.rssi, network.channel))
wifi.radio.stop_scanning_networks()

print("Connecting to %s"%secrets["ssid"])
wifi.radio.connect(secrets["ssid"], secrets["password"])
print("Connected to %s!"%secrets["ssid"])
print("My IP address is", wifi.radio.ipv4_address)

pool = socketpool.SocketPool(wifi.radio)
server = HTTPServer(pool)

@server.route("/change-neopixel-color")
def change_neopixel_color_handler(request: HTTPRequest):
    """
    Changes the color of the built-in NeoPixel.
    """
    r = request.query_params.get("r")
    g = request.query_params.get("g")
    b = request.query_params.get("b")

    pixel.fill((int(r or 0), int(g or 0), int(b or 0)))

    with HTTPResponse(request, content_type=MIMEType.TYPE_TXT) as response:
        response.send(f"Changed NeoPixel to color ({r}, {g}, {b})")


# async def wifi_loop():
#     # while True:
#     print(f"Listening on http://{wifi.radio.ipv4_address}:80")
#     server.serve_forever(str(wifi.radio.ipv4_address))

touch1_pin = touchio.TouchIn(board.TOUCH1)
touch2_pin = touchio.TouchIn(board.TOUCH2)
touch2_pin.threshold = 13000

pixel_pin = board.EYES
num_pixels = 2
pixels = neopixel.NeoPixel(pixel_pin, num_pixels,
                           brightness=0.05, auto_write=False)
pixels.fill((65, 0, 20))
pixels.show()

# mouse = Mouse(usb_hid.devices)
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)  # We're in the US :)

duck1 = None
duck2 = None

DO_MOUSE_JIGGLE = True
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (120, 0, 80)

MAX_BRITE_VAL = 0.28

IDLE_COLOR = GREEN
RUNNING_COLOR = RED

IDLE = 0
RUNNING = 1

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
    mode = IDLE
    color = [left_eye, right_eye]  # holds a color for each eye
    # auto_reset = True
    display_duration = 2    # seconds to show newest LED status 
    LEFT = 0
    RIGHT = 1
    mode_set = False

    def set_colors(self, left, right):
        self.color = [left, right]
        self.mode_set = True

    def set_eye_color(self, eye, color):
        self.color[eye] = color
        self.mode_set = True
    
    def show(self):
        pixels[0] = self.color[0]
        pixels[1] = self.color[1]
        pixels.show()
    
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
    global MAX_BRITE_VAL
    sync_eyes = False
    wait = 0.05
    led_breath_value = 0
    brite = 0.001
    led_status.set_colors(IDLE_COLOR, IDLE_COLOR)
    led_status.show()
    led_status.mode = IDLE
    while True:
        if led_status.mode == IDLE:
            led_status.set_colors(IDLE_COLOR, IDLE_COLOR)
            led_status.mode_set = True
            MAX_BRITE_VAL = 0.18
        elif led_status.mode == RUNNING:
            print("RUNNING")
            led_status.set_colors(RUNNING_COLOR, RUNNING_COLOR)
            led_status.mode_set = True
            MAX_BRITE_VAL = 0.22
        if led_status.mode_set:
            pixels[0] = led_status.color[0]
            pixels[1] = led_status.color[1]
            led_status.mode_set = False

        led_breath_value = (math.sin(time.monotonic() * 0.980) / 2.0) + 0.5
        brite = (MAX_BRITE_VAL * led_breath_value) + 0.01
        pixels.brightness = brite
        pixels.show()

        await asyncio.sleep(0)

async def do_touch1_action(led_status):
    print("DO TOUCH 1 ACTION")
    result = True
    duck1 = ducky.Ducky('HID_CMD1.txt', keyboard, keyboard_layout)
    led_status.set_eye_color(led_status.LEFT, BLUE)
    led_status.set_eye_color(led_status.RIGHT, BLUE)
    led_status.show()
    time.sleep(0.35)
    while result is not False:
        try:
            result = duck1.loop()
        except:
            result = False
            print("some error happened... meh-1")
    duck1.keyboard.release_all()
    await asyncio.sleep(1)
    led_status.mode = IDLE

async def do_touch2_action(led_status):
    print("DO TOUCH 2 ACTION")
    result = True
    duck2 = ducky.Ducky('HID_CMD2.txt', keyboard, keyboard_layout)
    led_status.set_eye_color(led_status.LEFT, PURPLE)
    led_status.set_eye_color(led_status.RIGHT, PURPLE)
    led_status.show()
    time.sleep(0.35)
    while result is not False:
        try:
            result = duck2.loop()
        except:
            result = False
            print("some error happened... meh-2")
    duck2.keyboard.release_all()
    await asyncio.sleep(1)
    led_status.mode = IDLE
        
async def touch_loop(led_status):
    touch1_active = False
    touch2_active = False
    after_touch_wait_time = 0.25
    last_touch_1_time = time.monotonic()
    last_touch_2_time = time.monotonic()
    while True:
        if touch1_pin.value and not touch1_active:
            touch1_active = True
            print("TOUCH 1")
            await do_touch1_action(led_status)
        elif not touch1_pin.value and touch1_active:
            touch1_active = False
        if touch2_pin.value and not touch2_active:
            touch2_active = True
            print("TOUCH 2")
            await do_touch2_action(led_status)
        elif not touch2_pin.value and touch2_active:
            touch2_active = False
        await asyncio.sleep(0)
    
async def main():
    led_status = LEDStatus()

    led_update_task = asyncio.create_task(led_updater(led_status))
    touch_input_task = asyncio.create_task(touch_loop(led_status))

    await asyncio.gather(led_update_task, touch_input_task)

asyncio.run(main()) 