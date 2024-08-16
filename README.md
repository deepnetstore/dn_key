# dn_key  
# haxxd

[DEEPNET.STORE](https://deepnet.store/pages/dn_key)

## Info
* ESP32-S2 and ESP32-S3 based IoT devices that are CircuitPython ready!
* Plug it in and you should see the drive appear: **`DN-S3-PY`** for ESP32-S3 or **`DEEPNET-PY`** for ESP32-S2.
* Open the `code.py` file in your favorite text editor or IDE to see the current code running.
* Replace or modify the `code.py` file to customize the device behavior!
* [CircuitPython Essentials](https://learn.adafruit.com/circuitpython-essentials/circuitpython-essentials)
* [More About CircuitPython](https://learn.adafruit.com/welcome-to-circuitpython/what-is-circuitpython)

## Device Variants

- **dn_key (ESP32-S3)**: The latest version featuring both Wi-Fi and Bluetooth. It mounts as **`DN-S3-PY`** when connected to a computer.
- **dn_key (ESP32-S2)**: An earlier version that only supports Wi-Fi. It mounts as **`DEEPNET-PY`** when connected. Though no longer in production, support remains available for this variant.

## Features
* ESP32-S3FN4R2 or ESP32-S2 based device
* Wi-Fi (and Bluetooth on ESP32-S3)
* 320KB SRAM, 128KB ROM, 8MB PSRAM, and 4MB Flash memory
* USB-C male plug
* RGB addressable LEDs in eyes
* CircuitPython supported
* USB-HID capable

## Usage Ideas
* WiFi KVM
* Mouse jiggler
* "Bad" USB
* Ducky Script injector
* WiFi beacon
* More...

## Example Code
You can find example code on our GitHub page:
* [dn_key Example Code](https://github.com/deepnetstore/dn_key/tree/main/CODE)

## Debugging
For persistent serial monitor connections during debugging, you can use the helper script found in the **helpers** folder:
* [macOS/Linux Serial Monitor Persistence Script](https://github.com/deepnetstore/dn_key/tree/main/CODE/helpers/macOS_Linux)

## Updating CircuitPython
To update the CircuitPython build, follow these steps using the DEEPNET-provided UF2 file:

1. **Download the UF2 File:** Get the latest UF2 file from the [DEEPNET GitHub](https://github.com/deepnetstore/dn_key).
2. **Enter Bootloader Mode:** Double-tap the Reset button on the back side of your dn_key. If successful, the device will appear as `DN_BOOT`.
3. **Install the UF2 File:** Drag and drop the UF2 file into the `DN_BOOT` drive. The device will reboot and show up as either `DN-S3-PY` or `DEEPNET-PY`.
4. **Verify the Update:** Modify and save the `code.py` file, then reconnect the device to verify the changes are saved.

## License
This project is licensed under the MIT License.

## Support and Contributions
For questions or contributions, open an issue or submit a pull request on our [GitHub repository](https://github.com/deepnetstore/dn_key).



