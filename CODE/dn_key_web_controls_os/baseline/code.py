"""
DN-KEY OS-Specific Web Controls
==========================================================

This code provides a web-based control interface for the DN-KEY ESP32-S3 device with OS-specific controls

HOW TO USE:
-----------
1. Upload this code to your DN-KEY device
2. Connect to the "dn_key" WiFi network (password: 12345678)
3. Open http://192.168.4.1 in your browser
4. Select your operating system
5. Use the OS-specific controls
6. Have fun!

Author: ᧁꫝꪮᦓꪻ
Version: 3.5 (Ultra Optimized)
"""

import time
import board
import random
import neopixel
import touchio
import wifi
import socketpool
import usb_hid
import asyncio
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

# ============================================================================
# HARDWARE SETUP
# ============================================================================

# Setup LED pixels - Power optimized
pixels = neopixel.NeoPixel(board.EYES, 2, brightness=0.03, auto_write=False)

# Define colors (as tuples for memory efficiency)
GREEN, RED, BLUE, PURPLE, WHITE, ORANGE, CYAN = (0,255,0), (255,0,0), (0,0,255), (128,0,128), (255,255,255), (255,165,0), (0,255,255)

# Initialize touch pins
eyes_touch_pin = touchio.TouchIn(board.TOUCH1)
eyes_touch_pin.threshold = 30000
logo_touch_pin = touchio.TouchIn(board.TOUCH2)
logo_touch_pin.threshold = 30000

# Initialize USB HID devices
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)
mouse = Mouse(usb_hid.devices)
consumer_control = ConsumerControl(usb_hid.devices)

# ============================================================================
# STATE MANAGEMENT
# ============================================================================

# State
do_mouse_jiggle = False
led_status = 'idle'

# Status colors
STATUS_COLORS = {'idle': GREEN, 'wifi_active': BLUE, 'wifi_error': RED, 'mouse_active': ORANGE, 'touch_active': CYAN, 'error': RED, 'success': GREEN}

# ============================================================================
# LED MANAGEMENT FUNCTIONS
# ============================================================================

def set_led_status(status_type):
    """Set LED status color."""
    global led_status
    if status_type in STATUS_COLORS:
        led_status = status_type
        pixels.fill(STATUS_COLORS[status_type])
        pixels.show()

def flash_success():
    """Flash green for success."""
    global led_status
    pixels.fill(GREEN)
    pixels.show()
    time.sleep(0.15)  # Reduced from 0.2
    if led_status in STATUS_COLORS:
        pixels.fill(STATUS_COLORS[led_status])
        pixels.show()

def flash_error():
    """Flash red for error."""
    global led_status
    pixels.fill(RED)
    pixels.show()
    time.sleep(0.15)  # Reduced from 0.2
    if led_status in STATUS_COLORS:
        pixels.fill(STATUS_COLORS[led_status])
        pixels.show()

def flash_purple():
    """Flash purple for web requests."""
    global led_status
    pixels.fill(PURPLE)
    pixels.show()
    time.sleep(0.05)  # Reduced from 0.1
    if led_status in STATUS_COLORS:
        pixels.fill(STATUS_COLORS[led_status])
        pixels.show()

# Set LED to idle (green) at startup
set_led_status('idle')

# ============================================================================
# NETWORK SETUP
# ============================================================================

def start_wifi_ap():
    """Start WiFi access point for web interface."""
    try:
        wifi.radio.start_ap(ssid="dn_key", password="12345678", channel=6)
        set_led_status('wifi_active')
        return True
    except Exception as e:
        set_led_status('wifi_error')
        return False

# ============================================================================
# COMMAND EXECUTION
# ============================================================================

# OS-specific command mappings - centralized for easy maintenance
OS_COMMAND_MAP = {
    'macos': {
        'terminal': {'keys': [Keycode.COMMAND, Keycode.SPACE], 'type': "terminal\n", 'wait': 0.4, 'enter': True, 'result': "Terminal opened"},
        'screenshot': {'keys': [Keycode.COMMAND, Keycode.SHIFT, Keycode.THREE], 'result': "Screenshot taken"},
        'lock_screen': {'keys': [Keycode.COMMAND, Keycode.CONTROL, Keycode.Q], 'result': "Screen locked"},
        'finder': {'keys': [Keycode.COMMAND, Keycode.SPACE], 'type': "finder\n", 'wait': 0.4, 'enter': True, 'result': "Finder opened"}
    },
    'windows': {
        'cmd': {'keys': [Keycode.WINDOWS, Keycode.R], 'type': "cmd\n", 'wait': 0.4, 'enter': True, 'result': "Command Prompt opened"},
        'screenshot': {'keys': [Keycode.PRINT_SCREEN], 'result': "Screenshot taken"},
        'lock_screen': {'keys': [Keycode.WINDOWS, Keycode.L], 'result': "Screen locked"},
        'explorer': {'keys': [Keycode.WINDOWS, Keycode.E], 'result': "File Explorer opened"},
        'run': {'keys': [Keycode.WINDOWS, Keycode.R], 'result': "Run Dialog opened"}
    },
    'linux': {
        'terminal': {'keys': [Keycode.CONTROL, Keycode.ALT, Keycode.T], 'result': "Terminal opened (Ctrl+Alt+T)"},
        'run_command': {'keys': [Keycode.ALT, Keycode.F2], 'result': "Run Command opened (Alt+F2)"},
        'screenshot': {'keys': [Keycode.PRINT_SCREEN], 'result': "Screenshot taken (PrtSc)"},
        'lock_screen': {'keys': [Keycode.WINDOWS, Keycode.L], 'result': "Screen locked (Super+L)"}
    }
}

# Universal commands (work across all OS)
UNIVERSAL_COMMANDS = {
    'volume_up': {'type': 'consumer', 'code': ConsumerControlCode.VOLUME_INCREMENT, 'result': "Volume increased"},
    'volume_down': {'type': 'consumer', 'code': ConsumerControlCode.VOLUME_DECREMENT, 'result': "Volume decreased"},
    'volume_mute': {'type': 'consumer', 'code': ConsumerControlCode.MUTE, 'result': "Volume muted/unmuted"},
    'media_play': {'type': 'consumer', 'code': ConsumerControlCode.PLAY_PAUSE, 'result': "Media play/pause toggled"}
}

# macOS-specific special commands
MACOS_SPECIAL = {
    'cmatrix': {'keys': [Keycode.COMMAND, Keycode.SPACE], 'type': "terminal\n", 'wait': 0.8, 'type2': "cmatrix\n", 'enter': True, 'result': "Cmatrix started"},
    'open_safari': {'keys': [Keycode.COMMAND, Keycode.SPACE], 'type': "safari\n", 'wait': 0.8, 'keys2': [Keycode.COMMAND, Keycode.L], 'wait2': 0.4, 'type2': "https://deepnet.store/pages/dn_key_s3", 'enter': True, 'result': "Safari opened"}
}

def execute_os_command(command_config):
    """Execute a command based on its configuration."""
    if 'keys' in command_config:
        keyboard.press(*command_config['keys'])
        keyboard.release_all()
    
    if 'type' in command_config:
        time.sleep(command_config.get('wait', 0.1))
        keyboard_layout.write(command_config['type'])
    
    if 'keys2' in command_config:
        keyboard.press(*command_config['keys2'])
        keyboard.release_all()
    
    if 'type2' in command_config:
        time.sleep(command_config.get('wait2', 0.1))
        keyboard_layout.write(command_config['type2'])
    
    if command_config.get('enter', False):
        keyboard.press(Keycode.ENTER)
        keyboard.release_all()

def execute_command(command, os_type="macos", keyboard_mode=False):
    try:
        # Handle keyboard mode (special keys and text input)
        if keyboard_mode:
            if command == 'enter':
                keyboard.press(Keycode.ENTER)
                keyboard.release_all()
                result = "Enter key sent"
            elif command == 'tab':
                keyboard.press(Keycode.TAB)
                keyboard.release_all()
                result = "Tab key sent"
            elif command == 'escape':
                keyboard.press(Keycode.ESCAPE)
                keyboard.release_all()
                result = "Escape key sent"
            else:
                keyboard_layout.write(command)
                result = f"Text '{command}' typed"
            flash_success()
            return result
        
        # Handle universal commands (volume/media controls)
        if command in UNIVERSAL_COMMANDS:
            cmd_config = UNIVERSAL_COMMANDS[command]
            consumer_control.press(cmd_config['code'])
            consumer_control.release()
            result = cmd_config['result']
            flash_success()
            return result
        
        # Handle macOS-specific special commands
        if os_type == "macos" and command in MACOS_SPECIAL:
            cmd_config = MACOS_SPECIAL[command]
            execute_os_command(cmd_config)
            result = cmd_config['result']
            flash_success()
            return result
        
        # Handle OS-specific commands
        if os_type in OS_COMMAND_MAP and command in OS_COMMAND_MAP[os_type]:
            cmd_config = OS_COMMAND_MAP[os_type][command]
            execute_os_command(cmd_config)
            result = cmd_config['result']
            flash_success()
            return result
        
        # Handle custom commands (open terminal/command prompt and run command)
        if os_type == "macos":
            keyboard.press(Keycode.COMMAND, Keycode.SPACE)
            keyboard.release_all()
            time.sleep(0.4)
            keyboard_layout.write("terminal\n")
            time.sleep(0.8)
            keyboard_layout.write(f"{command}\n")
            keyboard.press(Keycode.RETURN)
            keyboard.release_all()
            result = f"Command '{command}' executed in Terminal"
        elif os_type == "windows":
            keyboard.press(Keycode.WINDOWS, Keycode.R)
            keyboard.release_all()
            time.sleep(0.4)
            keyboard_layout.write("cmd\n")
            keyboard.press(Keycode.ENTER)
            keyboard.release_all()
            time.sleep(0.8)
            keyboard_layout.write(f"{command}\n")
            keyboard.press(Keycode.ENTER)
            keyboard.release_all()
            result = f"Command '{command}' executed in Command Prompt"
        elif os_type == "linux":
            keyboard.press(Keycode.CONTROL, Keycode.ALT, Keycode.T)
            keyboard.release_all()
            time.sleep(0.8)
            keyboard_layout.write(f"{command}\n")
            keyboard.press(Keycode.ENTER)
            keyboard.release_all()
            result = f"Command '{command}' executed in Terminal"
        else:
            keyboard.press(Keycode.COMMAND, Keycode.SPACE)
            keyboard.release_all()
            time.sleep(0.4)
            keyboard_layout.write("terminal\n")
            time.sleep(0.8)
            keyboard_layout.write(f"{command}\n")
            keyboard.press(Keycode.RETURN)
            keyboard.release_all()
            result = f"Command '{command}' executed in terminal"
        
        flash_success()
        return result
        
    except Exception as e:
        flash_error()
        return f"Command execution failed: {str(e)}"

# ============================================================================
# TOGGLE FUNCTIONS
# ============================================================================

def toggle_mouse_jiggler():
    """Toggle mouse jiggler on/off."""
    global do_mouse_jiggle
    do_mouse_jiggle = not do_mouse_jiggle
    set_led_status('mouse_active' if do_mouse_jiggle else 'idle')

# ============================================================================
# HTML TEMPLATES (OPTIMIZED)
# ============================================================================

# Optimized CSS - single minified string (removed unused redirect feedback styles)
CSS = """body{background:#000;color:#00ff00;font-family:monospace;margin:20px;font-size:16px}
.card{background:#111;border:1px solid #00ff00;padding:20px;margin:10px 0;border-radius:10px}
.btn{background:#00ff00;color:#000;border:none;padding:15px 25px;margin:10px;border-radius:8px;cursor:pointer;font-size:1.2rem}
.btn:hover{transform:translateY(-2px);box-shadow:0 4px 8px rgba(0,255,0,0.4)}
.back-btn{background:#333;color:#00ff00}
h1{font-size:2.5rem;margin-bottom:20px}
h3{font-size:1.8rem;margin-bottom:15px}
.btn-macos{background:linear-gradient(45deg,#8A2BE2,#9370DB);color:#fff}
.btn-windows{background:linear-gradient(45deg,#0078D4,#106EBE);color:#fff}
.btn-linux{background:linear-gradient(45deg,#FCC624,#E95420);color:#fff}
.os-icon{font-size:28px;margin-bottom:10px;display:block;font-weight:bold;background:rgba(0,255,0,0.2);padding:5px;border-radius:5px}
.container{background:#111;border:1px solid #00ff00;padding:20px;margin:10px auto;border-radius:10px;max-width:600px;text-align:center}
.status{color:#00aa00;margin:20px 0}"""

# OS data - consolidated
OS_DATA = {
    'macos': {'icon': '[MAC]', 'title': 'macOS', 'style': 'btn-macos', 'placeholder': "Enter command (e.g., 'ls', 'pwd', 'brew install')"},
    'windows': {'icon': '[WIN]', 'title': 'Windows', 'style': 'btn-windows', 'placeholder': "Enter command (e.g., 'dir', 'ipconfig', 'ping google.com')"},
    'linux': {'icon': '[LIN]', 'title': 'Linux', 'style': 'btn-linux', 'placeholder': "Enter command (e.g., 'ls', 'pwd', 'sudo apt update', 'htop')"}
}

# OS-specific command mappings
OS_COMMANDS = {
    'macos': {'terminal': 'Terminal', 'finder': 'Finder', 'open_safari': 'Safari', 'screenshot': 'Screenshot', 'lock_screen': 'Lock Screen'},
    'windows': {'cmd': 'Command Prompt', 'explorer': 'File Explorer', 'run': 'Run Dialog', 'screenshot': 'Screenshot Tool', 'lock_screen': 'Lock Screen'},
    'linux': {'terminal': 'Terminal', 'run_command': 'Run Command', 'screenshot': 'Screenshot', 'lock_screen': 'Lock Screen'}
}

# Optimized URL decoding - single replacement operation
def decode_url(text):
    """Optimized URL decoding."""
    return text.replace("+", " ").replace("%20", " ").replace("%2C", ",").replace("%3F", "?").replace("%21", "!").replace("%40", "@").replace("%23", "#").replace("%24", "$").replace("%25", "%").replace("%5E", "^").replace("%26", "&").replace("%2A", "*").replace("%28", "(").replace("%29", ")").replace("%2D", "-").replace("%3D", "=").replace("%5B", "[").replace("%5D", "]").replace("%7B", "{").replace("%7D", "}").replace("%7C", "|").replace("%5C", "\\").replace("%3A", ":").replace("%3B", ";").replace("%22", '"').replace("%27", "'").replace("%3C", "<").replace("%3E", ">").replace("%2F", "/").replace("%7E", "~")

# HTML templates - optimized and consolidated (no redirect feedback)

def create_error_response(message, redirect_time=2):
    """Create an error HTML response."""
    return f"""HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
<head>
<meta http-equiv="refresh" content="{redirect_time}; url=/" />
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DN-KEY OS Controls - Error</title>
<style>{CSS}</style>
</head>
<body>
<div class="container">
<h1 style="color:#ff0000">❌ {message}</h1>
<div class="status" style="color:#aa0000">Redirecting to the main page in {redirect_time} seconds...</div>
</div>
</body>
</html>"""

def create_main_page():
    """Create the main OS selection page."""
    return f"""HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
<head>
<title>DN-KEY OS Controls</title>
<style>{CSS}</style>
</head>
<body>
<h1>DN-KEY OS Controls</h1>
<p style="font-size:20px;margin:20px 0">Select your operating system to access OS-specific controls:</p>

<div class="card">
<button class="btn btn-macos" onclick="location.href='/macos'">
<span class="os-icon">{OS_DATA['macos']['icon']}</span>
macOS Controls
</button>

<button class="btn btn-windows" onclick="location.href='/windows'">
<span class="os-icon">{OS_DATA['windows']['icon']}</span>
Windows Controls
</button>

<button class="btn btn-linux" onclick="location.href='/linux'">
<span class="os-icon">{OS_DATA['linux']['icon']}</span>
Linux Controls
</button>
</div>

<div class="card">
<h3 style="font-size:20px;margin-bottom:15px">Universal Controls</h3>
<button class="btn" onclick="location.href='/toggle_mouse'">Toggle Mouse Jiggler</button>
</div>

<div class="card">
<h3 style="font-size:20px;margin-bottom:15px">Keyboard Input</h3>
<form action="/keyboard_input" method="get">
<input type="text" name="text" placeholder="Type text to send to computer..." required style="width:80%;padding:15px;background:#222;color:#00ff00;border:1px solid #00ff00;border-radius:5px;font-size:16px;margin-bottom:10px">
<button type="submit" class="btn">Send Text</button>
<button type="button" class="btn" onclick="location.href='/keyboard_input?text=enter'">Enter</button>
<button type="button" class="btn" onclick="location.href='/keyboard_input?text=tab'">Tab</button>
<button type="button" class="btn" onclick="location.href='/keyboard_input?text=escape'">Escape</button>
</form>
</div>
</body>
</html>"""

def create_os_page(os_type, title, commands):
    """Create OS-specific control page (optimized template)."""
    os_info = OS_DATA[os_type]
    
    # Build command buttons efficiently
    command_buttons = ''.join(f'<button class="btn" onclick="location.href=\'/{os_type}/{cmd_name}\'">{cmd_display}</button>' for cmd_name, cmd_display in commands.items())
    
    return f"""HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
<head>
<title>DN-KEY {title} Controls</title>
<style>{CSS}</style>
</head>
<body>
<h1>{os_info['icon']} {title} Controls</h1>

<div class="card">
<h3>System Controls</h3>
{command_buttons}
</div>

<div class="card">
<h3>Volume & Media Controls</h3>
<button class="btn" onclick="location.href='/{os_type}/volume_up'">Volume Up</button>
<button class="btn" onclick="location.href='/{os_type}/volume_down'">Volume Down</button>
<button class="btn" onclick="location.href='/{os_type}/volume_mute'">Mute/Unmute</button>
<button class="btn" onclick="location.href='/{os_type}/media_play'">Play/Pause</button>
</div>

<div class="card">
<h3>Custom Command ({title} Terminal)</h3>
<form action="/execute_command" method="get">
<input type="text" name="cmd" placeholder="{os_info['placeholder']}" required style="width:80%;padding:15px;background:#222;color:#00ff00;border:1px solid #00ff00;border-radius:5px;font-size:16px;margin-bottom:10px">
<input type="hidden" name="os" value="{os_type}">
<button type="submit" class="btn">Execute in Terminal</button>
</form>
</div>

<button class="btn back-btn" onclick="location.href='/'">Back to OS Selection</button>
</body>
</html>"""

# ============================================================================
# COMMAND MAPPING
# ============================================================================

# Command mapping for web requests (optimized) - no feedback pages
COMMAND_MAP = {
    '/cmatrix': ('command', 'cmatrix'),
    '/safari': ('command', 'open_safari'),
    '/terminal': ('command', 'terminal'),
    '/finder': ('command', 'finder'),
    '/screenshot': ('command', 'screenshot'),
    '/lock_screen': ('command', 'lock_screen'),
    '/toggle_mouse': ('function', toggle_mouse_jiggler),
}



# ============================================================================
# WEB SERVER
# ============================================================================

def handle_request(request):
    """Handle HTTP requests - optimized version without redirect feedback."""
    request_line = request.splitlines()[0]
    request_method, path, _ = request_line.split()

    if path == "/":
        response = create_main_page()
    elif path == "/macos":
        response = create_os_page('macos', 'macOS', OS_COMMANDS['macos'])
    elif path == "/windows":
        response = create_os_page('windows', 'Windows', OS_COMMANDS['windows'])
    elif path == "/linux":
        response = create_os_page('linux', 'Linux', OS_COMMANDS['linux'])
    elif path in COMMAND_MAP:
        action_type, action_function = COMMAND_MAP[path]
        if action_type == 'command':
            execute_command(action_function)
        elif action_type == 'function':
            action_function()
        # Return to main page immediately
        response = create_main_page()
    elif path.startswith("/execute_command"):
        if "cmd=" in path:
            cmd_part = path.split("cmd=")[1]
            cmd_decoded = decode_url(cmd_part.split("&")[0])
            os_type = "macos"
            if "os=" in path:
                os_part = path.split("os=")[1]
                os_type = decode_url(os_part.split("&")[0])
            execute_command(cmd_decoded, os_type)
            # Return to OS page immediately
            response = create_os_page(os_type, OS_DATA[os_type]['title'], OS_COMMANDS[os_type])
        else:
            response = create_error_response("No command specified!")
    elif path.startswith("/keyboard_input"):
        if "text=" in path:
            text_part = path.split("text=")[1]
            text_decoded = decode_url(text_part.split("&")[0])
            execute_command(text_decoded, keyboard_mode=True)
            # Return to main page immediately
            response = create_main_page()
        else:
            response = create_error_response("No text specified!")
    elif path.startswith("/macos/"):
        command = path.split('/')[-1]
        execute_command(command, "macos")
        # Return to macOS page immediately
        response = create_os_page('macos', 'macOS', OS_COMMANDS['macos'])
    elif path.startswith("/windows/"):
        command = path.split('/')[-1]
        execute_command(command, "windows")
        # Return to Windows page immediately
        response = create_os_page('windows', 'Windows', OS_COMMANDS['windows'])
    elif path.startswith("/linux/"):
        command = path.split('/')[-1]
        execute_command(command, "linux")
        # Return to Linux page immediately
        response = create_os_page('linux', 'Linux', OS_COMMANDS['linux'])
    else:
        response = create_error_response("Page not found!")

    flash_purple()
    return response

# ============================================================================
# ASYNC TASKS
# ============================================================================

async def mouse_jiggle_task():
    """Mouse jiggling task."""
    while True:
        if do_mouse_jiggle:
            x_direction = random.choice([-1, 1]) * random.randint(6, 10)
            y_direction = random.choice([-1, 1]) * random.randint(3, 10)
            mouse.move(x=x_direction, y=y_direction)
        await asyncio.sleep(0.5)

async def touch_handlers():
    """Handle touch input events."""
    while True:
        if eyes_touch_pin.value:
            set_led_status('touch_active')
            result = execute_command('cmatrix')
            while eyes_touch_pin.value:
                await asyncio.sleep(0.1)
            set_led_status('idle')
        
        if logo_touch_pin.value:
            set_led_status('touch_active')
            result = execute_command('open_safari')
            while logo_touch_pin.value:
                await asyncio.sleep(0.1)
            set_led_status('idle')
        
        await asyncio.sleep(0.1)

# ============================================================================
# MAIN LOOP
# ============================================================================

async def main_loop():
    """Main application loop."""
    print("Starting DN-KEY OS-Specific Web Controls...")
    
    # Start WiFi access point
    if start_wifi_ap():
        print("Web interface available at: http://192.168.4.1")
        
        # Set up the web server
        pool = socketpool.SocketPool(wifi.radio)
        server_socket = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
        server_socket.setsockopt(pool.SOL_SOCKET, pool.SO_REUSEADDR, 1)
        server_socket.bind(("0.0.0.0", 80))
        server_socket.listen(1)
        server_socket.setblocking(False)
        
        # Start all async tasks
        tasks = [
            asyncio.create_task(mouse_jiggle_task()),
            asyncio.create_task(touch_handlers())
        ]
        
        # Web server task
        while True:
            try:
                client, addr = server_socket.accept()
                
                # Read request
                buffer = bytearray(1024)
                client.recv_into(buffer)
                request = buffer.decode("utf-8")
                
                # Handle request
                response = handle_request(request)
                
                # Send response
                client.send(response.encode("utf-8"))
                client.close()
                
            except OSError as e:
                if e.errno != 11:  # EAGAIN/EWOULDBLOCK
                    pass
                await asyncio.sleep(0.1)
            
            # Run other tasks
            await asyncio.sleep(0.01)
        
        # Wait for all tasks
        await asyncio.gather(*tasks)
    else:
        print("Failed to start WiFi access point")
        # Fallback to basic operation
        while True:
            time.sleep(1)

# Start the application
asyncio.run(main_loop()) 