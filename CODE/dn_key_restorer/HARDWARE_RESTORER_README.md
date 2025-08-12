# DN-KEY Hardware Restorer

A user-friendly tool to recover bricked DN-KEY devices by restoring the firmware and bootloader.

## 🚨 When to Use This Tool

Use this tool if your DN-KEY device:
- Won't connect to your computer
- Shows up as an unknown device
- Won't mount as a drive
- Is completely unresponsive
- Has corrupted firmware

## 📋 Prerequisites

### Required Software
- **macOS or Linux** (Windows users can use WSL)
- **esptool.py** - Install with: `pip install esptool`
- **Bash shell**

### Required Firmware Files
Download these files from the [DN-KEY GitHub repository](https://github.com/deepnetstore/dn_key):

1. **TinyUF2 Build Directory** - Extract from `TinyUF2.zip`
2. **CircuitPython UF2 File** - Download the latest `.uf2` file for ESP32-S3
3. **Optional: Test Code** - Any simple `code.py` to verify functionality

## 🔧 Setup Instructions

### Step 1: Download Firmware Files
1. Go to [https://github.com/deepnetstore/dn_key](https://github.com/deepnetstore/dn_key)
2. Download the latest release files:
   - `TinyUF2.zip` - Extract to a folder
   - `dn_key_s3_circuitpython_YYYYMMDD.uf2` - CircuitPython firmware

### Step 2: Update Script Configuration
Edit `hardware_restorer.sh` and update these paths:

```bash
# 1. TinyUF2 build directory (extract from TinyUF2.zip)
TINYUF2_DIR="/path/to/extracted/TinyUF2/ports/espressif"

# 2. CircuitPython UF2 file
CIRCUITPYTHON_UF2="/path/to/dn_key_s3_circuitpython_YYYYMMDD.uf2"

# 3. Optional: Test code to verify functionality
TEST_CODE="/path/to/test/code.py"
```

### Step 3: Prepare Your Device
1. **Disconnect** your DN-KEY from USB
2. **Double-tap** the reset button on the back of your DN-KEY
3. **Reconnect** to USB while holding the reset button
4. The device should appear as `/dev/cu.usbmodemXXXXX` (download mode)

## 🚀 Usage

### Basic Usage
```bash
./hardware_restorer.sh
```

### What the Script Does
1. **Scans** for connected DN-KEY devices
2. **Validates** firmware files and requirements
3. **Erases** flash memory completely
4. **Flashes** TinyUF2 bootloader
5. **Installs** CircuitPython firmware
6. **Optionally installs** test code
7. **Verifies** the restoration was successful

### Example Output
```
==========================================
    DN-KEY Hardware Restorer
==========================================

[INFO] This tool will help you restore bricked DN-KEY devices
[INFO] Make sure you have downloaded the required firmware files

[STEP] Checking requirements...
[SUCCESS] All requirements met!

[STEP] Scanning for DN-KEY devices...
[INFO] Scan 1/3...
[INFO] Found device: /dev/cu.usbmodem113201 (ID: 42:CE:A4:D1:EE:4F)
[SUCCESS] Found 1 device(s)

[WARNING] Found 1 device(s) to restore:
[INFO]   - /dev/cu.usbmodem113201 (ID: 42:CE:A4:D1:EE:4F)

Do you want to proceed with restoration? (y/N): y

[STEP] Processing device: 42:CE:A4:D1:EE:4F
[STEP] Starting restoration for device: 42:CE:A4:D1:EE:4F
[STEP] [42:CE:A4:D1:EE:4F] Erasing flash memory...
[SUCCESS] [42:CE:A4:D1:EE:4F] Flash erased successfully
[STEP] [42:CE:A4:D1:EE:4F] Flashing TinyUF2 bootloader...
[SUCCESS] [42:CE:A4:D1:EE:4F] TinyUF2 flashed successfully
[STEP] [42:CE:A4:D1:EE:4F] Installing CircuitPython...
[SUCCESS] [42:CE:A4:D1:EE:4F] DN_BOOT volume detected
[SUCCESS] [42:CE:A4:D1:EE:4F] CircuitPython UF2 copied to DN_BOOT
[SUCCESS] [42:CE:A4:D1:EE:4F] DN-S3-PY volume detected - CircuitPython installed!
[SUCCESS] [42:CE:A4:D1:EE:4F] Device restoration completed successfully!

==========================================
    RESTORATION SUMMARY
==========================================

[SUCCESS] All 1 device(s) restored successfully!

[INFO] Your DN-KEY device(s) should now be working!
[INFO] Check the /Volumes/DN-S3-PY drive for the CircuitPython volume
```

## 🔍 Troubleshooting

### "No DN-KEY devices found"
- Make sure your device is in download mode (double-tap reset button)
- Try a different USB cable
- Try a different USB port
- Check if the device appears in Device Manager (Windows) or System Information (macOS)

### "esptool.py not found"
```bash
pip install esptool
```

### "Flash erase failed"
- Try disconnecting and reconnecting the device
- Double-tap the reset button again
- Try a different USB cable
- Make sure no other programs are using the device

### "DN_BOOT volume not detected"
- Wait longer (the script waits up to 30 seconds)
- Try manually ejecting and reconnecting the device
- Check if the device is properly powered

### "DN-S3-PY volume not detected"
- The device may need more time to reboot
- Try manually ejecting and reconnecting
- Check if the CircuitPython UF2 file is valid

## 📁 File Structure After Restoration

After successful restoration, your device should show:
```
/Volumes/DN-S3-PY/
├── code.py          # Your test code (if provided)
├── lib/             # CircuitPython libraries
└── boot_out.txt     # Boot log
```

## ⚠️ Important Notes

- **This tool completely erases your device** - all data will be lost
- **Use at your own risk** - the authors are not responsible for any damage
- **Always backup important code** before restoration
- **Test the device** after restoration to ensure it's working properly

## 🆘 Getting Help

If you encounter issues:
1. Check the troubleshooting section above
2. Verify your firmware files are correct and up-to-date
3. Try the restoration process multiple times
4. Check the [DN-KEY GitHub issues](https://github.com/deepnetstore/dn_key/issues) for similar problems

## 📄 License

This tool is provided as-is for educational purposes. Use responsibly and in accordance with all applicable laws and regulations.
