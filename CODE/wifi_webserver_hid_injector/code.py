from secrets import secrets

"""
You will need to create a secrets file called secrets.py
add in your network information like so:

secrets = {
    'ssid': 'MYNETWORK',
    'password': 'STRONGAFPW',
}

save it and try again...

"""

import mdns
import microcontroller
import time
import math
import socketpool
import wifi
import board
import neopixel
import touchio
import digitalio
import asyncio
import ipaddress

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse

from adafruit_httpserver.mime_type import MIMEType
from adafruit_httpserver.request import HTTPRequest
from adafruit_httpserver.response import HTTPResponse
from adafruit_httpserver.server import HTTPServer
from adafruit_httpserver.methods import HTTPMethod

from colors import *

touch1_pin = touchio.TouchIn(board.TOUCH1)
touch2_pin = touchio.TouchIn(board.TOUCH2)
touch2_pin.threshold = 13000

pixel_pin = board.EYES
num_pixels = 2
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.05, auto_write=False)
pixels.fill(LOW_RED)
pixels.show()

MAX_BRITE_VAL = 0.28

mouse = Mouse(usb_hid.devices)
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)  # We're in the US :)

print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])

#  set static IP address
# ipv4 =  ipaddress.IPv4Address("192.168.0.66")
# netmask =  ipaddress.IPv4Address("255.255.255.0")
# gateway =  ipaddress.IPv4Address("192.168.0.1")
# wifi.radio.set_ipv4_address(ipv4=ipv4,netmask=netmask,gateway=gateway)

print("Available WiFi networks:")
for network in wifi.radio.start_scanning_networks():
    print(
        "\t%s\t\tRSSI: %d\tChannel: %d"
        % (str(network.ssid, "utf-8"), network.rssi, network.channel)
    )
wifi.radio.stop_scanning_networks()

time.sleep(1)

print("Connecting to", secrets["ssid"])
wifi.radio.connect(secrets["ssid"], secrets["password"])
print("Connected to", secrets["ssid"])
print("My IP address is", wifi.radio.ipv4_address)

mdns_server = mdns.Server(wifi.radio)
mdns_server.hostname = "DEEPNET_USBKEY"
mdns_server.advertise_service(service_type="_http", protocol="_tcp", port=80)

# websocket = socketpool.Socket()
pool = socketpool.SocketPool(wifi.radio)
server = HTTPServer(pool)


def html_body(content, title="DEEPNET ESP32S2 USBKEY", style=""):
    return f"""
    <!DOCTYPE html>
    <html>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>
        {title}
    </title>
    {style}
    <body>
        <center>
            <div style="max-width:80%;height:auto;">
                {content}
            </div>
        </center>
    </body>
    </html>
    """


def webpage(data):
    return html_body(
        f"""<h1>DEEPNET WEBSERVER TEST 1</h1>
        <p>We will see how this goes...</p>
        <p>{data}</p>"""
    )


def index(data):
    return html_body(
        f"""
        <h1>DEEPNET WEBSERVER TEST 1</h1>
        <p>We will see how this goes...</p>
        <div style="max-width:80%;height:auto;">
            <p>
                <form accept-charset="utf-8" method="POST">
                    <button class="button" name="command1" value="RUN" type="submit">
                        RUN SCRIPT 1
                    </button>
                </form>
            </p>
            <p>
                <form accept-charset="utf-8" method="POST">
                    <button class="button" name="command2" value="RUN" type="submit">
                        RUN SCRIPT 2
                    </button>
                </form>
            </p>
            <p>
                <form accept-charset="utf-8" method="GET">
                    <button class="button" name="reset" value="reset" type="submit">
                        Reset
                    </button>
                </form>
            </p>
        </div>
        <div>
            <p>{data}</p>
        </div>
        """
    )


pages = {"index": index}


def page_render(pagename, data):
    return f"{pages[pagename](data)}"


@server.route("/", method=HTTPMethod.GET)
def base(request: HTTPRequest):
    """
    Serve the default index.html file.
    """
    print("request:", request.path)
    pixels.fill(SPECIAL)
    pixels.show()
    data = {
        "temperature": microcontroller.cpu.temperature,
        "frequency": microcontroller.cpu.frequency,
        "voltage": microcontroller.cpu.voltage,
        "headers": request.headers,
        "body": request.body,
        "connection": request.connection,
        "method": request.method,
        "client addr": request.client_address,
    }
    with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
        response.send(page_render(pagename="index", data=data))


#  if a button is pressed on the site


@server.route("/", method=HTTPMethod.POST)
def buttonpress(request: HTTPRequest):
    #  get the raw text
    raw_text = request.body.decode("utf8")
    data = {"RAW TEXT": raw_text}
    if "command1" in raw_text:
        pixels.fill(BLUE)
        pixels.show()
    if "command2" in raw_text:
        pixels.fill(GREEN)
        pixels.show()
    with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
        response.send(page_render(pagename="index", data=data))


def breakth_leds():
    led_breath_value = (math.sin(time.monotonic() * 0.980) / 2.0) + 0.5
    brite = (MAX_BRITE_VAL * led_breath_value) + (MAX_BRITE_VAL * 0.1)
    pixels.brightness = brite
    pixels.show()


def webserver_task():
    server.poll()
    time.sleep(0.01)


def main():
    port_num = 80
    print(f"Listening on http://{wifi.radio.ipv4_address}:{port_num}")
    server.start(str(wifi.radio.ipv4_address), port=port_num)
    pixels.fill(PURPLE)
    pixels.show()
    while True:
        breakth_leds()
        webserver_task()


if __name__ == "__main__":
    main()
