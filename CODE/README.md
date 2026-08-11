# dn_key sample code

**dn_key** is an ESP32-based HID IoT device that ships with CircuitPython. It
does keyboard/mouse emulation, hosts its own web control panel, and talks to
other keys over the air. To change what it does, drop a new `code.py` on the
drive and it reboots into it.

Every folder here is a self-contained sample. Copy its `code.py` (and any `lib/`
next to it) onto the key and go. The catalog below is the quick tour.

## Samples

### Games and swarm (key to key, no computer needed)

Power the key off a battery bank and it does its own thing and talks to other
keys over ESP-NOW. No wifi to join, no pairing.

- **`dn_key_firefly_swarm/`** - flash it on a pile of keys and their eyes drift
  into blinking together like fireflies. Touch the face to send a white wave
  across the room, touch the laptop to change everyone's color.

### HID (plug into a computer, act as a keyboard/mouse)

- **`dn_key_hid_mouse_jiggler/`** - keeps a machine awake with gentle mouse
  nudges. Touch a pad to toggle it.
- **`dn_key_hid_mouse_jiggler_spaz/`** - same idea, cranked. Fast, random,
  chaotic movement for when subtle is not the point.
- **`dn_key_hid_duckyscript/`** - runs DuckyScript keystroke payloads from the
  `HID_CMD*.txt` files. Edit the scripts, pick one with a touch pad.
- **`dn_key_macOS_terminal/`** - opens Terminal on macOS and runs `cmatrix`.
- **`dn_key_safari_url/`** - opens Safari through Spotlight and navigates to a
  URL. Works on macOS and iOS.

### Web control (the key makes its own wifi, you drive it from a browser)

Connect to the key's access point, open `http://192.168.4.1`, and control it
from any phone or laptop.

- **`dn_key_basic_web_controls/`** - a simple page to fire terminal commands,
  LED effects, and the jiggler. SSID `dn_key`, password `12345678`.
- **`dn_key_web_controls_os/`** - the advanced panel with OS-specific controls
  for macOS, Windows, and Linux (shortcuts, media keys, mouse automation).
- **`dn_key_simple_mouse_jiggler_web/`** - the 2025 sample: a mouse jiggler with
  a clean web toggle and a breathing LED. Good starting point to learn from.
- **`wifi_webserver_hid_injector/`** - joins *your* wifi instead of hosting its
  own, then serves a page to fire HID payloads. Needs a `secrets.py` with your
  network info (see the sample header).

> Adding a sample? Add a one-line entry to this list in the same commit.

## Device variants

- **dn_key (ESP32-S3)**: the current version, wifi and bluetooth. Mounts as
  **`DN-S3-PY`**.
- **dn_key (ESP32-S2)**: an earlier wifi-only version, no longer in production
  but still supported. Mounts as **`DEEPNET-PY`**.

## Getting started

1. Plug the key in. It mounts as `DN-S3-PY` (S3) or `DEEPNET-PY` (S2).
2. Copy a sample's `code.py` onto the drive, along with any `lib/` folder next
   to it.
3. The key reboots and runs the new code. Edit `code.py` in place to tweak it.
4. Use a serial monitor to watch device output while you work (see the
   `helpers/` folder for a persistent monitor script).

## Web controls detail

### Basic (`dn_key_basic_web_controls/`)

Creates a wifi access point and serves a control page.

- **SSID**: `dn_key`
- **Password**: `12345678`
- **Web interface**: `http://192.168.4.1`

Actions include running terminal commands like `cmatrix`, opening a page in
Safari, triggering LED effects on the eyes, and toggling the mouse jiggler.

### Advanced OS-specific (`dn_key_web_controls_os/`)

Same connection details, with a fuller panel:

- OS-specific keyboard shortcuts and commands (macOS, Windows, Linux)
- Volume and media playback controls, system functions
- Mouse controls and automation
- Web interface with OS selection

## Arduino

The key can also be flashed from the Arduino IDE for lower-level work like
DuckyScript keystroke injection, similar to a Rubber Ducky.

1. **Install the Arduino IDE**: https://www.arduino.cc/en/software
2. **Add the ESP32 core**: in Preferences, add this under "Additional Boards
   Manager URLs":

   `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json`

3. **Select your board**: Tools > Board > ESP32S3 (or ESP32S2).
4. **Install libraries**: `Keyboard`, `Mouse`, and `WiFi`.

A minimal keystroke sketch:

```cpp
#include <Keyboard.h>

void setup() {
  Keyboard.begin();
  delay(1000);
  Keyboard.print("Hello, World!");
  Keyboard.releaseAll();
}

void loop() {
  // more automation here
}
```
