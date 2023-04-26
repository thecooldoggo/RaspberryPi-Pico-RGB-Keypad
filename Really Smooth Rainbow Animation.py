# Drop the `pmk` folder
# into your `lib` folder on your `CIRCUITPY` drive.

import math
from pmk import PMK, number_to_xy, hsv_to_rgb
from pmk.platform.rgbkeypadbase import RGBKeypadBase as Hardware  # for Pico RGB Keypad Base

# Set up Keybow
keybow = PMK(Hardware())
keys = keybow.keys

# Increment step to shift animation across keys.
step = 0

while True:
    keybow.update()

    step += 1

    for i in range(16):
        # Convert the key number to an x/y coordinate to calculate the hue
        # in a matrix style-y.
        x, y = number_to_xy(i)

        # Calculate the hue.
        hue = (math.atan2(y - 8, x - 8) + step / 20 + math.pi) / (2 * math.pi)
        hue = hue - int(hue)
        hue = hue - math.floor(hue)

        # Convert the hue to RGB values.
        r, g, b = hsv_to_rgb(hue, 1, 1)

        # Make the output RGB value lower. If you want it brighter increase value.
        r = (r * 0.05)
        g = (g * 0.05)
        b = (b * 0.05)
        keys[i].set_led(r, g, b)
