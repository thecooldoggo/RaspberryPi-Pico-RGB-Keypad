# Drop the `pmk` folder
# into your `lib` folder on your `CIRCUITPY` drive.

import time
import math
from pmk import PMK, number_to_xy, hsv_to_rgb
from pmk.platform.rgbkeypadbase import RGBKeypadBase as Hardware
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode


keybow = PMK(Hardware())
keys = keybow.keys

keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

consumer_control = ConsumerControl(usb_hid.devices)

key_mapping = {2: Keycode.F,
               3: Keycode.K,
               4: Keycode.ZERO,
               5: Keycode.ONE,
               6: ConsumerControlCode.VOLUME_DECREMENT,
               7: ConsumerControlCode.SCAN_PREVIOUS_TRACK,
               8: Keycode.BACKSPACE,
               9: Keycode.TWO,
               10: ConsumerControlCode.MUTE,
               11: ConsumerControlCode.PLAY_PAUSE,
               12: Keycode.ENTER,
               13: Keycode.THREE,
               14: ConsumerControlCode.VOLUME_INCREMENT,
               15: ConsumerControlCode.SCAN_NEXT_TRACK}

debounce = 0.18

# Increment step to shift animation across keys.
step = 0

while True:
    keybow.update()

    # Iterate over all keys and perform the desired action for each key
    for k in key_mapping.keys():
        if keys[k].pressed and not keys[k].held:
            # If the key is a media control key, send the corresponding consumer control code
            if k in [6, 7, 10, 11, 14, 15]:
                consumer_control.send(key_mapping[k])
            # If the key is a regular key, send the corresponding key press
            else:
                keyboard.press(key_mapping[k])
                keyboard.release_all()

    step += 9

    for i in range(16):
        # Convert the key number to an x/y coordinate to calculate the hue
        # in a matrix style-y.
        x, y = number_to_xy(i)

        # Calculate the hue.
        hue = (x + y + (step / 20)) / 8
        hue = hue - int(hue)
        hue = hue - math.floor(hue)

        # Convert the hue to RGB values.
        r, g, b = hsv_to_rgb(hue, 1, 1)

        # Make the output RGB value 95% lower.
        r = (r * 0.05)
        g = (g * 0.05)
        b = (b * 0.05)
        keys[i].set_led(r, g, b)

    time.sleep(debounce)
