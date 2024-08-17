/*
 * The MIT License (MIT)
 *
 * Copyright (c) 2020 Ha Thach (tinyusb.org) for Adafruit Industries
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

#ifndef DEEPNET_ESP32_S2_HOODIE_USBKEY_H_
#define DEEPNET_ESP32_S2_HOODIE_USBKEY_H_

//--------------------------------------------------------------------+
// Button
//--------------------------------------------------------------------+

// Enter UF2 mode if GPIO is pressed while 2nd stage bootloader indicator
// is on e.g RGB = Purple. If it is GPIO0, user should not hold this while
// reset since that will instead run the 1st stage ROM bootloader
#define PIN_BUTTON_UF2 0

// GPIO that implement 1-bit memory with RC components which hold the
// pin value long enough for double reset detection.
#define PIN_DOUBLE_RESET_RC 10

//--------------------------------------------------------------------+
// LED
//--------------------------------------------------------------------+

// GPIO connected to Neopixel data
#define NEOPIXEL_PIN 2
#define PIN_APA102_DATA 38
#define PIN_APA102_SCK 37
// #define PIN_APA102_PWR 5 // no power pin...

// #define NEOPIXEL_POWER_STATE 1

// Brightness percentage from 1 to 255
#define NEOPIXEL_BRIGHTNESS 60

// Number of neopixels
#define NEOPIXEL_NUMBER 2

// LED for indicator
// If not defined neopixel will be use for flash writing instead
// #define LED_PIN               42
// #define LED_STATE_ON          1

//--------------------------------------------------------------------+
// USB UF2
//--------------------------------------------------------------------+

#define USB_VID 0x239A // idk what numbers are what... look em up...
#define USB_PID 0x0119

#define USB_MANUFACTURER "DEEPNET"
#define USB_PRODUCT "DN_ESP32S2_USBKEY"

#define UF2_PRODUCT_NAME USB_MANUFACTURER " " USB_PRODUCT
#define UF2_BOARD_ID "DEEPNET_HOODIE_KEY"
#define UF2_VOLUME_LABEL "DN_BOOT"
#define UF2_INDEX_URL "https://deepnet.store"

#define TINYUF2_FAVICON_HEADER "favicon_adafruit_256.h"

#endif // DEEPNET_ESP32_S2_HOODIE_USBKEY_H_
