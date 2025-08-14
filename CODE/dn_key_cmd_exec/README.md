# DN-KEY OS Detection & Command Execution

A CircuitPython script for the DN-KEY ESP32-S3 device that automatically detects the operating system and executes OS-specific commands with touch controls.

## Features

- **Auto OS Detection**: Touch-based selection during startup
- **Silent Command Execution**: Runs commands in background with output saved to files
- **Touch Controls**: Physical touch sensors for interaction
- **LED Status Indicators**: Visual feedback through colored LEDs
- **Cross-Platform**: Supports Windows, Linux, and macOS
- **Configurable Commands**: Easy to modify commands for different use cases

## Hardware Requirements

- DN-KEY ESP32-S3 device
- 2x NeoPixel LEDs (eyes)
- 2x Touch sensors (eyes and logo)
- USB connection to target computer

## Installation

1. Upload the script as `code.py` to the device
2. Connect the device to your target computer via USB

## How It Works

### Startup Sequence

1. **Hardware Initialization (7-9 seconds)**
   - Blinking blue LEDs indicate hardware detection
   - USB HID setup and stabilization
   - Touch sensor calibration

2. **OS Selection (3 seconds)**
   - Yellow LEDs indicate selection mode
   - Touch the **EYES** sensor to select your OS:
     - **No touch**: Windows (default)
     - **1 touch**: Linux
     - **2 touches**: macOS
   - White flash confirms each touch

3. **Initial Command Execution (3-4 seconds)**
   - Orange LEDs indicate command execution
   - Runs the configured command for selected OS
   - Saves output to temporary file

4. **Ready State**
   - Green LEDs indicate ready for touch controls

## LED Color Guide

| Color | Status | Description |
|-------|--------|-------------|
| 🔵 **Blinking Blue** | Hardware Init | Device initializing, detecting hardware |
| 🔵 **Solid Blue** | USB Setup | USB HID initialization complete |
| 🟡 **Yellow** | OS Selection | Waiting for OS selection (3 seconds) |
| ⚪ **White Flash** | Touch Acknowledged | Touch detected and registered |
| 🔵 **Blue** | Windows Selected | Windows OS selected |
| 🟠 **Orange** | Linux Selected/Executing | Linux OS selected or command running |
| 🟣 **Purple** | macOS Selected | macOS OS selected |
| 🟢 **Green** | Ready/Idle | System ready, waiting for touch input |
| 🔴 **Red** | Locking System | Screen lock in progress |
| ⚫ **Off** | Shutdown | Device shutting down |

## Touch Controls

### During OS Selection (Yellow LEDs)
- **Eyes Sensor**: 
  - No touch (wait 3 seconds) → Windows
  - Touch once → Linux
  - Touch twice → macOS

### During Normal Operation (Green LEDs)
- **Eyes Sensor**: Lock the system
  - Windows: `Win + L`
  - Linux: `Super + L`
  - macOS: `Cmd + Ctrl + Q`

- **Logo Sensor**: Rerun the command
  - Executes the same command again
  - Creates new timestamped output file

## Default Commands

The script comes with pre-configured commands for each OS:

| OS | Command | Purpose |
|----|---------|---------|
| **Windows** | `type C:\Windows\System32\drivers\etc\hosts` | Display hosts file |
| **Linux** | `cat /etc/passwd` | Display user accounts |
| **macOS** | `cat /etc/hosts` | Display hosts file |

### Output Files

Commands save output to timestamped files:
- **Windows**: `%TEMP%\dnkey_output_[timestamp].txt`
- **Linux**: `/tmp/dnkey_output_[timestamp].txt`
- **macOS**: `/tmp/dnkey_output_[timestamp].txt`

## Customization

### Modifying Commands

Edit the `COMMANDS` dictionary in the script:

```python
COMMANDS = {
    'windows': 'your_windows_command_here',
    'linux': 'your_linux_command_here',
    'macos': 'your_macos_command_here'
}
```

### Changing Output Locations

Edit the `OUTPUTS` dictionary:

```python
OUTPUTS = {
    'windows': 'C:\\your\\path\\output',
    'linux': '/your/path/output',
    'macos': '/your/path/output'
}
```

### Adjusting Touch Sensitivity

Modify the touch threshold:

```python
eyes_touch.threshold = 30000  # Adjust this value
logo_touch.threshold = 30000  # Adjust this value
```

## Usage Examples

### Example 1: System Information Gathering
```python
COMMANDS = {
    'windows': 'systeminfo',
    'linux': 'uname -a && lsb_release -a',
    'macos': 'system_profiler SPSoftwareDataType'
}
```

### Example 2: Network Information
```python
COMMANDS = {
    'windows': 'ipconfig /all',
    'linux': 'ip addr show && route -n',
    'macos': 'ifconfig && netstat -rn'
}
```

### Example 3: Process Listing
```python
COMMANDS = {
    'windows': 'tasklist',
    'linux': 'ps aux',
    'macos': 'ps aux'
}
```

## Timing Reference

| Phase | Duration | LED Color | Description |
|-------|----------|-----------|-------------|
| Hardware Init | 7 seconds | Blinking Blue | USB detection and setup |
| USB Setup | 2 seconds | Solid Blue | HID initialization |
| OS Selection | 3 seconds | Yellow | Touch-based OS selection |
| Command Execution | 3-4 seconds | Orange | Running selected command |
| Ready State | Indefinite | Green | Waiting for touch input |

## Troubleshooting

### Device Not Recognized
- Ensure CircuitPython is properly installed
- Check USB cable connection
- Try different USB port
- Wait for full hardware initialization (9 seconds)

### Commands Not Executing
- Verify OS selection was correct
- Check if target system requires administrator privileges
- Ensure output directory is writable
- Try simpler commands first

### Touch Sensors Not Responding
- Adjust touch threshold values
- Check sensor connections
- Ensure proper grounding

### LED Colors Wrong
- Check NeoPixel connections
- Verify power supply
- Adjust brightness if needed

## Security Considerations

- Commands run with current user privileges
- Output files are created in temporary directories
- No network communication (local execution only)
- Commands are visible in system process lists during execution
- Consider the security implications of your custom commands
