#!/bin/bash
# This script connects to the first available USB serial device found on macOS or Linux.
# It continuously attempts to reconnect to the device if the connection is lost.

# Set the baud rate for the connection
BAUD_RATE=115200

while true; do
    # Find the first .usbmodem (macOS) or ttyACM/ttyUSB (Linux) device
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # For macOS, use tty.usbmodem devices
        SERIAL_PORT=$(ls /dev/tty.usbmodem* 2>/dev/null | head -n 1)
    else
        # For Linux, use ttyACM or ttyUSB devices
        SERIAL_PORT=$(ls /dev/ttyACM* /dev/ttyUSB* 2>/dev/null | head -n 1)
    fi

    # Check if a serial device was found
    if [ -z "$SERIAL_PORT" ]; then
        echo "No USB serial device found. Retrying in 2 seconds..."
        sleep 2  # Wait before retrying to find the device
        continue
    fi

    # Attempt to connect to the found USB serial device
    echo "Attempting to connect to $SERIAL_PORT at $BAUD_RATE baud..."
    screen $SERIAL_PORT $BAUD_RATE

    # If disconnected, try to reconnect
    echo "Disconnected from $SERIAL_PORT. Reconnecting..."
    sleep 2  # Wait a moment before trying to reconnect
done



