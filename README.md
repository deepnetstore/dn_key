# dn_key

### haxxd

A pocket ESP32 offensive-security tool that runs CircuitPython, shaped like a
hooded hacker at a laptop. HID keyboard and mouse injection, wifi and Bluetooth
radios, and a control panel it hosts in your own browser. Every bit of it is
reprogrammable by editing one file on the drive.

[DEEPNET.STORE](https://deepnet.store/pages/dn_key)

Thanks for grabbing one. It shows up as a USB drive, runs whatever is in
`code.py`, and is yours to reprogram. This page is the tour.

## Quick start

1. Plug it in. It mounts as a drive: **`DN-S3-PY`** (ESP32-S3) or
   **`DEEPNET-PY`** (ESP32-S2).
2. Open `code.py` to see what it is running. Edit and save to change it, the key
   reboots into your changes automatically.
3. Want it to do something else? Grab a ready-made sample from
   **[CODE/](https://github.com/deepnetstore/dn_key/tree/main/CODE)** and drop
   its `code.py` (and any `lib/` next to it) onto the drive.

New here? [CircuitPython Essentials](https://learn.adafruit.com/circuitpython-essentials/circuitpython-essentials)
and [what CircuitPython is](https://learn.adafruit.com/welcome-to-circuitpython/what-is-circuitpython).

## Sample code

The full, browsable catalog lives in
**[CODE/](https://github.com/deepnetstore/dn_key/tree/main/CODE)**. A taste:

- **firefly swarm** - flash it on a few keys, power them off battery banks, and
  their eyes blink in sync like fireflies. Touch one to wave the whole room or
  change its color. No computer needed.
- **mouse jiggler** - keeps a machine awake, subtle or spaz mode.
- **duckyscript** - run keystroke payloads like a Rubber Ducky.
- **web controls** - the key hosts its own wifi and a control panel you drive
  from your phone at `192.168.4.1`.

## Device variants

- **dn_key (ESP32-S3)**: current version, wifi and bluetooth. Mounts as
  **`DN-S3-PY`**.
- **dn_key (ESP32-S2)**: earlier wifi-only version, no longer produced but still
  supported. Mounts as **`DEEPNET-PY`**.

## Specs

- ESP32-S3FN4R2 or ESP32-S2
- Wi-Fi (plus Bluetooth on the S3)
- 320KB SRAM, 128KB ROM, 8MB PSRAM, 4MB Flash
- USB-C male plug
- RGB addressable LED eyes
- Two capacitive touch pads (the face and the laptop logo)
- CircuitPython, USB-HID capable

## Debugging

For a serial monitor that survives reconnects while you hack on `code.py`, use
the helper in
[CODE/helpers/macOS_Linux](https://github.com/deepnetstore/dn_key/tree/main/CODE/helpers/macOS_Linux).

## Updating CircuitPython

Use the DEEPNET-provided UF2 files in this repo:

1. **Download the UF2** for your board (`dn_key_s3_*` or `dn_key_s2_*`) from the
   repo root.
2. **Enter bootloader mode:** double-tap the reset button on the back. The
   device appears as `DN_BOOT`.
3. **Install it:** drag the UF2 onto the `DN_BOOT` drive. The key reboots and
   comes back as `DN-S3-PY` or `DEEPNET-PY`.
4. **Verify:** edit and save `code.py`, reconnect, confirm your change stuck.

## License

MIT.

## Support and contributions

Questions or ideas? Open an issue or a pull request on the
[GitHub repo](https://github.com/deepnetstore/dn_key).

## Disclaimer

This device is intended **solely for educational purposes** and **security
research** by responsible professionals and enthusiasts. As blue team engineers,
we are dedicated to improving security awareness, resilience, and ethical
practices.

While this device can emulate human interface devices (HID) like keyboards and
mice, letting it execute commands on connected systems, **it must never be used
for malicious purposes**. **We do not support, condone, or provide examples of
any illegal activities**, including unauthorized access, data exfiltration, or
any form of hacking that compromises the privacy and security of individuals or
organizations.

### By using this device, you agree to the following:

- You will only use the device in compliance with all applicable laws and
  regulations.
- You will obtain proper authorization before using the device in any
  environment where it may affect systems or data that you do not own or
  control.
- You acknowledge that improper use of this device can result in legal
  consequences, and **you assume full responsibility for any actions performed
  with the device**.

We strongly encourage users to adhere to ethical standards and **only use this
device for legitimate purposes** such as testing your own systems, enhancing
security defenses, or contributing to the cybersecurity community.

### Liability

We, the creators, will not be held responsible for any damages, legal issues, or
liabilities resulting from the use or misuse of this device. By using this
device, you agree to accept full responsibility for any actions you take.

Remember: **with great power comes great responsibility**. Let's work together to
build a safer digital world.
