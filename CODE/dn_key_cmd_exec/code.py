"""
DN-KEY Ultra-Simple One-Time Execution - OPTIMIZED
=================================================
This script is designed for the DN-KEY device, allowing it to execute a single command based on the detected operating system (Windows, Linux, or macOS) using USB HID. It features touch inputs for OS selection and command execution, with visual feedback via NeoPixels.
It is optimized for simplicity and reliability, ensuring it works across different platforms with minimal dependencies."""

import time
import board
import neopixel
import touchio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

# ============================================================================
# CONFIGURATION
# ============================================================================
COMMANDS = {
    'windows': 'type C:\\Windows\\System32\\drivers\\etc\\hosts',
    'linux': 'cat /etc/passwd',
    'macos': 'cat /etc/hosts'
}

OUTPUTS = {
    'windows': '%TEMP%\\dnkey_output',
    'linux': '/tmp/dnkey_output',
    'macos': '/tmp/dnkey_output'
}

# Colors
COLORS = {
    'init': (0, 0, 255),      # Blue
    'select': (255, 255, 0),   # Yellow
    'ack': (255, 255, 255),    # White
    'windows': (0, 0, 255),    # Blue
    'linux': (255, 165, 0),    # Orange
    'macos': (128, 0, 128),    # Purple
    'exec': (255, 165, 0),     # Orange
    'ready': (0, 255, 0),      # Green
    'lock': (255, 0, 0),       # Red
    'off': (0, 0, 0)           # Black
}

# ============================================================================
# HARDWARE INITIALIZATION WITH BLINKING AND EXTENDED TIMING
# ============================================================================
print("Initializing DN-KEY...")

# Initialize LEDs
pixels = neopixel.NeoPixel(board.EYES, 2, brightness=0.1, auto_write=False)

# Blinking blue during hardware detection (7-9 seconds)
print("Hardware detection (blinking blue)...")
blink_start = time.time()
blink_state = True

# Extended hardware detection time for Windows/Mac compatibility
while (time.time() - blink_start) < 7.0:  # 7 seconds of blinking
    if blink_state:
        pixels.fill(COLORS['init'])  # Blue on
    else:
        pixels.fill(COLORS['off'])   # Off
    pixels.show()
    blink_state = not blink_state
    time.sleep(0.3)  # Blink every 300ms

# Solid blue for USB HID initialization
pixels.fill(COLORS['init'])
pixels.show()
print("USB HID setup...")

# USB HID initialization with more retries for Windows/Mac
max_retries = 8  # Increased for better Windows/Mac support
for attempt in range(max_retries):
    try:
        print(f"USB attempt {attempt + 1}/{max_retries}")
        keyboard = Keyboard(usb_hid.devices)
        keyboard_layout = KeyboardLayoutUS(keyboard)
        print("USB ready!")
        break
    except Exception as e:
        print(f"USB retry {attempt + 1}: {e}")
        time.sleep(2)
        # Blink during retries
        pixels.fill(COLORS['off'])
        pixels.show()
        time.sleep(0.2)
        pixels.fill(COLORS['init'])
        pixels.show()

# Touch pins
eyes_touch = touchio.TouchIn(board.TOUCH1)
eyes_touch.threshold = 30000
logo_touch = touchio.TouchIn(board.TOUCH2)
logo_touch.threshold = 30000

# Additional stabilization time for Windows/Mac
print("Stabilizing...")
time.sleep(2)

# Test keyboard
keyboard.press(Keycode.SHIFT)
keyboard.release_all()
time.sleep(0.1)

print("Hardware ready!")

# ============================================================================
# OS SELECTION (3 SECONDS YELLOW)
# ============================================================================
print("OS Selection - Touch eyes: 0=Windows, 1=Linux, 2=macOS")

pixels.fill(COLORS['select'])  # Solid yellow
pixels.show()

touch_count = 0
last_touch = 0
start_time = time.time()

# Exactly 3 seconds selection window
while (time.time() - start_time) < 3.0:
    if eyes_touch.value and (time.time() - last_touch) > 0.5:
        touch_count += 1
        last_touch = time.time()
        print(f"Touch {touch_count}")
        
        # White flash acknowledgment
        pixels.fill(COLORS['ack'])
        pixels.show()
        time.sleep(0.2)
        pixels.fill(COLORS['select'])
        pixels.show()
        
        # Wait for release
        while eyes_touch.value:
            time.sleep(0.05)
        
        if touch_count >= 2:
            break
    
    time.sleep(0.05)

# Determine OS
if touch_count == 0:
    os_type = 'windows'
    pixels.fill(COLORS['windows'])
elif touch_count == 1:
    os_type = 'linux'
    pixels.fill(COLORS['linux'])
else:
    os_type = 'macos'
    pixels.fill(COLORS['macos'])

pixels.show()
time.sleep(1)

print(f"OS: {os_type}")

# ============================================================================
# COMMAND EXECUTION FUNCTION
# ============================================================================
def run_command():
    """Execute the command for the selected OS."""
    timestamp = str(int(time.time()))
    output_file = f"{OUTPUTS[os_type]}_{timestamp}.txt"
    command = COMMANDS[os_type]
    
    print(f"Running: {command}")
    
    try:
        if os_type == 'windows':
            # Windows: Extended timing for slower systems
            keyboard.press(Keycode.WINDOWS, Keycode.R)
            keyboard.release_all()
            time.sleep(0.6)  # Increased wait time
            cmd = f'cmd /c "{command} > {output_file} 2>&1 && exit"'
            keyboard_layout.write(cmd)
            time.sleep(0.3)
            keyboard.press(Keycode.ENTER)
            keyboard.release_all()
            
        elif os_type == 'linux':
            keyboard.press(Keycode.ALT, Keycode.F2)
            keyboard.release_all()
            time.sleep(0.4)
            cmd = f"bash -c '{command} > {output_file} 2>&1'"
            keyboard_layout.write(cmd)
            time.sleep(0.2)
            keyboard.press(Keycode.ENTER)
            keyboard.release_all()
            
        else:  # macOS - FIXED: Proper terminal closure
            # Open terminal
            keyboard.press(Keycode.COMMAND, Keycode.SPACE)
            keyboard.release_all()
            time.sleep(0.5)  # Wait for Spotlight
            keyboard_layout.write("terminal")
            keyboard.press(Keycode.ENTER)
            keyboard.release_all()
            time.sleep(1.0)  # Wait for terminal to open
            
            # Execute command with silent output and immediate exit
            cmd = f"{command} > {output_file} 2>&1 && exit"
            keyboard_layout.write(cmd)
            time.sleep(0.2)
            keyboard.press(Keycode.ENTER)
            keyboard.release_all()
            
            # Terminal should close automatically due to 'exit' command
            # If it doesn't close, force close it
            time.sleep(1.5)  # Wait for command to complete
            
            # Force close terminal window (backup)
            keyboard.press(Keycode.COMMAND, Keycode.W)
            keyboard.release_all()
        
        print(f"Output: {output_file}")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def lock_screen():
    """Lock the screen based on OS."""
    try:
        if os_type in ['windows', 'linux']:
            keyboard.press(Keycode.WINDOWS, Keycode.L)
        else:  # macos
            keyboard.press(Keycode.COMMAND, Keycode.CONTROL, Keycode.Q)
        keyboard.release_all()
        print(f"{os_type} locked")
    except Exception as e:
        print(f"Lock error: {e}")

# ============================================================================
# INITIAL COMMAND EXECUTION (3-4 SECONDS)
# ============================================================================
print("Running initial command...")
pixels.fill(COLORS['exec'])
pixels.show()

run_command()

# Set to ready
pixels.fill(COLORS['ready'])
pixels.show()

print(f"Ready! OS: {os_type}")
print("Eyes=Lock, Logo=Rerun")

# ============================================================================
# TOUCH LOOP (SIMPLE)
# ============================================================================
while True:
    try:
        # Eyes touch = Lock
        if eyes_touch.value:
            pixels.fill(COLORS['lock'])
            pixels.show()
            lock_screen()
            while eyes_touch.value:
                time.sleep(0.05)
            pixels.fill(COLORS['ready'])
            pixels.show()
        
        # Logo touch = Rerun command
        if logo_touch.value:
            pixels.fill(COLORS['exec'])
            pixels.show()
            run_command()
            while logo_touch.value:
                time.sleep(0.05)
            pixels.fill(COLORS['ready'])
            pixels.show()
        
        time.sleep(0.05)
        
    except KeyboardInterrupt:
        pixels.fill(COLORS['off'])
        pixels.show()
        break
    except Exception as e:
        print(f"Error: {e}")
        pixels.fill(COLORS['lock'])
        pixels.show()
        time.sleep(1)
        pixels.fill(COLORS['ready'])
        pixels.show()

print("DN-KEY stopped")