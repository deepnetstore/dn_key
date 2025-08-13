"""
DN-KEY 2025 Sample Code
A simple mouse jiggler with web interface for learning and modification

This sample demonstrates:
- Basic HID mouse control
- WiFi access point setup
- Simple web server
- LED status indicators with breathing effect
- Touch controls

Features:
- Mouse jiggling with random movement
- Web interface to toggle jiggling on/off
- LED breathing effect with status feedback
- Touch control via DN logo

Tip: Use a serial monitor to see device feedback during development

Author: ᧁꫝꪮᦓꪻ
Date: 2025 - DC33 <3
"""

import time
import asyncio
import math
import random
import board
import neopixel
import touchio
import wifi
import socketpool
import usb_hid
from adafruit_hid.mouse import Mouse

# ============================================================================
# HARDWARE SETUP
# ============================================================================

# Initialize the mouse
mouse = Mouse(usb_hid.devices)

# Initialize the LED (DN-KEY has 2 RGB LEDs on the eyes)
pixels = neopixel.NeoPixel(board.EYES, 2, brightness=0.08, auto_write=False)

# Initialize touch pins
touch1_pin = touchio.TouchIn(board.TOUCH1)  # Eyes touch
touch2_pin = touchio.TouchIn(board.TOUCH2)  # DN logo touch
touch2_pin.threshold = 23000  # Tap threshold

# ============================================================================
# CONFIGURATION
# ============================================================================

# Mouse jiggling settings
JIGGLE_INTERVAL = 0.01  # seconds between movements (like spaz sample)
JIGGLE_MAX_DISTANCE = 8  # max pixels to move

# LED colors
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

# ============================================================================
# GLOBAL STATE
# ============================================================================

# Mouse jiggling state
DO_MOUSE_JIGGLE = False

# ============================================================================
# LED FUNCTIONS (with breathing effect)
# ============================================================================

async def led_updater():
    """Update LED with breathing effect - from spaz sample"""
    global DO_MOUSE_JIGGLE
    
    while True:
        # Calculate breathing effect
        led_breath_value = (math.sin(time.monotonic() * 2.0) + 1.0) / 2.0
        brite = (0.15 * led_breath_value) + 0.015
        pixels.brightness = brite
        
        # Set color based on state
        if DO_MOUSE_JIGGLE:
            pixels.fill(GREEN)
        else:
            pixels.fill(RED)
        
        pixels.show()
        await asyncio.sleep(0.04)

def flash_led(color, count=3, duration=0.2):
    """Flash LED a specific number of times"""
    for i in range(count):
        pixels.fill(color)
        pixels.show()
        time.sleep(duration)
        pixels.fill((0, 0, 0))
        pixels.show()
        time.sleep(duration)

# ============================================================================
# MOUSE FUNCTIONS
# ============================================================================

async def jiggle_mouse():
    """Move mouse in random directions - from spaz sample"""
    while True:
        if DO_MOUSE_JIGGLE:
            # Generate random movement values
            x_direction = random.choice([-1, 1]) * random.randint(6, JIGGLE_MAX_DISTANCE)
            y_direction = random.choice([-1, 1]) * random.randint(3, JIGGLE_MAX_DISTANCE)
            mouse.move(x=x_direction, y=y_direction)
        await asyncio.sleep(JIGGLE_INTERVAL)

def toggle_mouse_jiggling():
    """Toggle mouse jiggling on/off"""
    global DO_MOUSE_JIGGLE
    DO_MOUSE_JIGGLE = not DO_MOUSE_JIGGLE
    
    if DO_MOUSE_JIGGLE:
        print("Mouse jiggling: ON")
        flash_led(GREEN, 2)
    else:
        print("Mouse jiggling: OFF")
        flash_led(RED, 2)

# ============================================================================
# TOUCH FUNCTIONS
# ============================================================================

async def touch_loop():
    """Handle touch input - from spaz sample"""
    global DO_MOUSE_JIGGLE
    touch2_active = False
    
    while True:
        # DN logo touch (touch2) - toggle mouse jiggling
        if touch2_pin.value and not touch2_active:
            touch2_active = True
            toggle_mouse_jiggling()
            print(f"DN logo touched - Mouse jiggling: {DO_MOUSE_JIGGLE}")
        elif not touch2_pin.value and touch2_active:
            touch2_active = False
        
        await asyncio.sleep(0.01)

# ============================================================================
# WiFi FUNCTIONS
# ============================================================================

def start_wifi_ap():
    """Start WiFi access point"""
    try:
        wifi.radio.start_ap(ssid="dn_key", password="12345678", channel=6)
        print(f"WiFi AP: dn_key")
        print(f"Password: 12345678")
        return True
    except Exception as e:
        print(f"WiFi AP error: {e}")
        return False

# ============================================================================
# WEB SERVER FUNCTIONS
# ============================================================================

CSS = """body{background:#000;color:#00ff00;font-family:monospace;margin:0;padding:10px;font-size:20px;min-height:100vh}
.card{background:#111;border:2px solid #00ff00;padding:30px;margin:15px 0;border-radius:15px;box-shadow:0 0 25px rgba(0,255,0,0.3)}
.btn{background:linear-gradient(45deg,#00ff00,#00cc00);color:#000;border:none;padding:30px 50px;margin:25px;border-radius:12px;cursor:pointer;font-size:2.2rem;font-weight:bold;box-shadow:0 0 20px rgba(0,255,0,0.4);transition:all 0.3s ease;width:80%;max-width:300px}
.btn:hover{transform:translateY(-3px);box-shadow:0 0 30px rgba(0,255,0,0.7);background:linear-gradient(45deg,#00ff00,#00ff40)}
h1{font-size:4rem;margin-bottom:30px;text-shadow:0 0 15px #00ff00}
.container{background:#111;border:2px solid #00ff00;padding:30px;margin:10px auto;border-radius:15px;max-width:90%;text-align:center;box-shadow:0 0 30px rgba(0,255,0,0.2)}
.status{color:#00ff00;margin:25px 0;font-size:4.5rem;font-weight:bold;letter-spacing:2px}"""

def create_web_page():
    """Create the main web page HTML with cyberpunk styling"""
    status_text = "ON" if DO_MOUSE_JIGGLE else "OFF"
    status_color = "#00ff00" if DO_MOUSE_JIGGLE else "#ff0000"
    
    return f"""HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
<head>
    <title>DN-KEY Mouse Jiggler</title>
    <style>{CSS}</style>
</head>
<body>
    <div class="container">
        <h1>DN-KEY Mouse Jiggler</h1>
        
        <div class="card">
            <div class="status" style="color:{status_color};font-size:24px;font-weight:bold">
                Status: {status_text}
            </div>
            
            <form method="GET" action="/toggle">
                <button type="submit" class="btn">
                    Toggle Mouse Jiggler
                </button>
            </form>
        </div>
    </div>
</body>
</html>"""

def handle_web_request(request):
    """Handle incoming web requests"""
    global DO_MOUSE_JIGGLE
    
    # Flash purple to indicate AP connection
    flash_led(PURPLE, 2)
    
    if "GET /toggle" in request:
        # Toggle mouse jiggling
        toggle_mouse_jiggling()
        return create_web_page()
    elif "GET /" in request:
        # Show main page
        return create_web_page()
    else:
        # 404 for unknown requests
        return """HTTP/1.1 404 Not Found
Content-Type: text/plain

404 - Page not found"""

async def run_web_server():
    """Run the web server"""
    print("Starting web server...")
    
    # Set up the web server
    pool = socketpool.SocketPool(wifi.radio)
    server_socket = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
    server_socket.setsockopt(pool.SOL_SOCKET, pool.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", 80))
    server_socket.listen(1)
    server_socket.setblocking(False)
    
    print(f"Web server ready at http://192.168.4.1")
    
    while True:
        try:
            # Accept incoming connections
            client, addr = server_socket.accept()
            
            # Read the request
            buffer = bytearray(1024)
            client.recv_into(buffer)
            request = buffer.decode("utf-8")
            
            # Handle the request
            response = handle_web_request(request)
            
            # Send the response
            client.send(response.encode("utf-8"))
            client.close()
            
        except OSError:
            # No connection available, continue
            pass
        
        # Small delay to prevent busy waiting
        await asyncio.sleep(0.01)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

async def main():
    """Main application function"""
    print("DN-KEY Mouse Jiggler Starting...")
    print("=" * 40)
    
    # Initial LED indication
    pixels.fill(RED)
    pixels.show()
    time.sleep(1)
    
    # Start WiFi access point
    if start_wifi_ap():
        print("Web interface available at: http://192.168.4.1")
        
        print("Mouse Jiggler ready!")
        print("Features:")
        print("- Mouse jiggling: Random mouse movements")
        print("- Web interface: Control via browser")
        print("- Touch control: Tap DN logo to toggle")
        print("- LED breathing effect: Visual status indicators")
        print("- WiFi AP: Connect to dn_key network")
        print("")
        print("Web interface: http://192.168.4.1")
        print("Press Ctrl+C to stop")
        print("=" * 40)
        
        # Start all async tasks
        tasks = [
            asyncio.create_task(led_updater()),
            asyncio.create_task(touch_loop()),
            asyncio.create_task(jiggle_mouse()),
            asyncio.create_task(run_web_server())
        ]
        
        # Run all tasks
        await asyncio.gather(*tasks)
    else:
        print("Failed to start WiFi access point")
        flash_led(RED, 5)
        return

# ============================================================================
# START THE APPLICATION
# ============================================================================

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopping DN-KEY Mouse Jiggler...")
        pixels.fill((0, 0, 0))
        pixels.show()
    except Exception as e:
        print(f"Error: {e}")
        pixels.fill(RED)
        pixels.show()
        flash_led(RED, 5) 