# dn_key  
#haxxd

([DEEPNET.STORE](https://deepnet.store))

## Features
* ESP32-S2FN4R2 - WiFi capable device
* It has 320KB SRAM, 128KB ROM, 8MB PSRAM, and 4MB Flash memory
* USB-C male plug
* RGB addressable LEDs in eyes
* CircuitPython supported
* USB-HID capable

## Usage ideas
* WiFi KVM
* Mouse jiggler
* "Bad" USB
* Ducky Script injector
* WiFi beacon
* More...

## Example code
* ([USB HID Mouse Jiggler](github.....))

## Attention:
If you purchased a DN_Key from the Deepnet Team before Auguest 18th, 2023, you MUST update CircuitPython in order to properly save any edited code. Unfortunately, a bug was found in our edits to the CircuitPython build that forced the code.py file to be over writen when the DN_Key was booted. This may have resulted in any code you wrote being lost entirely. We sincerly appologize for this mistake and hope you patch this issue asap.
The update is extremely simple.

## Update CircuitPython
* Step 1:  
    * Download the `dn_key_circuitpython_20230820_FIX.uf2` file from the DEEPNET github: ([https://github.com/deepnetstore/dn_key])(https://github.com/deepnetstore/dn_key)  
* Step 2:  
    * Double tap the Reset button on the back side of your DN_Key. Besure to get the timing right so that "DN_BOOT" shows up as a drive on your computer. If you have any issues with timing, try to press the Reset button the second time after the DN_Key Eyes have turned purple. Along with the "DN_BOOT" drive appearing, the eye LEDs will turn Solid Green if successful. (If the eyes are 'breathing/fading in-out' the original sketch is still running, try step 2 again.)
* Step 3:  
    * Drag and drop the `dn_key_circuitpython_20230820_FIX.uf2` file into the `DN_BOOT` drive and let the file upload completely. Once the file is fully uploaded, the DN_Key will automatically reboot itself and the updated CircuitPython build will now be installed. You will see `DEEPNET-PY` appear as a mounted drive again.  
* Step 4:  
    * Verify the new build is working by editing some code in `code.py`, save the file, eject your `DEEPNET-PY` drive, unplug the DN_Key and then reinsert the DN_Key so the `DEEPNET-PY` drive appears once again. Open `code.py` and see if your changes remained. If the changes you made are not saved, try again starting at Step 2.