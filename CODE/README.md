# dn_key - ESP32-Based HID IoT Device

**dn_key** is an ESP32-S3-based HID IoT device designed for automating tasks like HID (keyboard/mouse) emulation, web-based control, and more. With built-in Wi-Fi and Bluetooth, the dn_key offers robust connectivity and control. The device comes pre-loaded with CircuitPython, making it easy to modify behavior by updating the `code.py` file.

While our focus is on the newer ESP32-S3 variant, there are still some **dn_key (ESP32-S2)** devices in circulation, which only support Wi-Fi. Both devices are pre-loaded with CircuitPython and essential libraries, ready to use right out of the box.

## Device Variants

- **dn_key (ESP32-S3)**: The latest version, featuring both Wi-Fi and Bluetooth. It mounts as **`DN-S3-PY`** when connected to a computer.
- **dn_key (ESP32-S2)**: An earlier version that only supports Wi-Fi. It mounts as **`DEEPNET-PY`** when connected. Though no longer in production, support remains available for this variant.

## Preloaded Features

Your dn_key device comes with:

- **`code.py` file**: The primary script that defines the device's behavior. This file can be replaced or modified to adjust functionality.
- **Pre-installed libraries**: Essential libraries for HID emulation, Wi-Fi functionality, NeoPixel control, and more are already loaded onto the device in the `lib/` folder.

## Getting Started with CircuitPython

### Accessing the Device

When you plug the dn_key into your computer, it will mount as a drive:

- **ESP32-S3**: The drive will be named **`DN-S3-PY`**.
- **ESP32-S2**: The drive will be named **`DEEPNET-PY`**.

### Replacing the `code.py` File

You can replace the `code.py` file on the device with one of the examples provided in the repository. Some examples include:

- **`dn_web_controls/`**: Sets up a web server hosted by the device, allowing control over HID and other functions via a webpage.
- **`dn_key_hid_mouse_jiggler/`**: Focuses on keeping the system active by periodically moving the mouse to prevent the system from going idle.

Once you update the `code.py` file, the device will automatically restart and run the new code.

## Web Controls Example (`dn_web_controls/`)

This example enables the dn_key to create a Wi-Fi access point, allowing you to connect and interact via a webpage. The details are:

- **SSID**: `dn_key`
- **Password**: `12345678`

Once connected, you can open your browser and navigate to `http://192.168.4.1` to interact with the device through the web interface. Available actions include:

- Running terminal commands like `cmatrix`.
- Opening a webpage in Safari.
- Triggering LED effects with the NeoPixel.
- Toggling HID functions such as mouse jiggling.

## Advanced Usage with Arduino

The dn_key can also be programmed using the Arduino IDE for more advanced functionality like **DuckyScript** for keystroke injection, similar to devices like the Rubber Ducky.

### Arduino Setup

1. **Download the Arduino IDE**: [Get the Arduino IDE here](https://www.arduino.cc/en/software).
2. **Install ESP32 Core**: Go to **Preferences** in the Arduino IDE, and add this URL under "Additional Boards Manager URLs":

https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json

3. **Select Your Board**:
- For ESP32-S3, select **Tools > Board > ESP32S3**.
- For ESP32-S2, select **Tools > Board > ESP32S2**.

4. **Install Required Libraries**: Install the `Keyboard`, `Mouse`, and `WiFi` libraries to support HID and networking tasks.

### DuckyScript Example:

Here’s a simple Arduino sketch to run keystrokes:

```cpp
#include <Keyboard.h>

void setup() {
 Keyboard.begin();
 delay(1000);
 Keyboard.print("Hello, World!");
 Keyboard.releaseAll();
}

void loop() {
 // Additional automation logic here
}




