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

## Disclaimer

This device is intended **solely for educational purposes** and **security research** by responsible professionals and enthusiasts. As blue team engineers, we are dedicated to improving security awareness, resilience, and ethical practices.

While this device is capable of emulating human interface devices (HID) like keyboards and mice, allowing it to execute commands on connected systems, **it must never be used for malicious purposes**. **We do not support, condone, or provide examples of any illegal activities**, including unauthorized access, data exfiltration, or any form of hacking that compromises the privacy and security of individuals or organizations.

### **By using this device, you agree to the following:**
- You will only use the device in compliance with all applicable laws and regulations.
- You will obtain proper authorization before using the device in any environment where it may affect systems or data that you do not own or control.
- You acknowledge that improper use of this device can result in legal consequences, and **you assume full responsibility for any actions performed with the device**.

We strongly encourage users to adhere to ethical standards and **only use this device for legitimate purposes** such as testing your own systems, enhancing security defenses, or contributing to the cybersecurity community.

### **Liability**
We, the creators, will not be held responsible for any damages, legal issues, or liabilities resulting from the use or misuse of this device. By using this device, you agree to accept full responsibility for any actions you take.

Remember: **With great power comes great responsibility**. Let's work together to build a safer digital world.




