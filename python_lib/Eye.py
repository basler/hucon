#!/usr/bin/env python
""" 2019-01-18

Driver module for leds, with PCA9685

Author: Sascha.MuellerzumHagen@baslerweb.com
"""

from .PCA9685 import PCA9685

class Eye(object):
    """ Eye driver class.
    """

    RGB = [2, 1, 0]
    RBG = [2, 0, 1]
    GBR = [1, 0, 2]
    GRB = [1, 2, 0]
    BGR = [0, 1, 2]
    BRG = [0, 2, 1]

    red = 0
    green = 0
    blue = 0

    def __init__(self, position, color_coding=None, lock=True, address=0x4A):
        """Init an eye on specific position
        """
        if position not in range(1, 5):
            raise ValueError("Eye position \"{0}\" is not in (1, 4).".format(position))

        self._position = position
        if color_coding is None:
            self._color_coding = Eye.RGB
        else:
            self._color_coding = color_coding
        self._lock = lock

        self._pwm = PCA9685(address)
        self.set_color(self.red, self.green, self.blue)

    def _get_rgb_channel(self, position):

        offset = 0

        if position == 1:
            offset = 0
        elif position == 2:
            offset = 13
        elif position == 3:
            offset = 5
        else:
            offset = 10

        cha_r = offset + self._color_coding[0]
        cha_g = offset + self._color_coding[1]
        cha_b = offset + self._color_coding[2]

        return (cha_r, cha_g, cha_b)

    def set_color(self, red=None, green=None, blue=None):
        """ Set the color for the eye.
        """

        if red is None:
            red = self.red
        else:
            self.red = red
        if green is None:
            green = self.green
        else:
            self.green = green
        if blue is None:
            blue = self.blue
        else:
            self.blue = blue

        if self._lock:
            self.red = max(min(red, 255), 0)
            self.green = max(min(green, 255), 0)
            self.blue = max(min(blue, 255), 0)
        else:
            if red not in range(256) or green not in range(256) or blue not in range(256):
                message = 'Eye "%d" RGB(%d, %d, %d) is not in range of (0, 255).' % (self._position, red, green, blue)
                raise ValueError(message)

        (cha_r, cha_g, cha_b) = self._get_rgb_channel(self._position)

        self._pwm.set_channel(cha_r, self.red)
        self._pwm.set_channel(cha_g, self.green)
        self._pwm.set_channel(cha_b, self.blue)

    def set_all_color(self, red, green, blue):
        """ Set the color for all eyes.
        """

        if self._lock:
            red = max(min(red, 255), 0)
            green = max(min(green, 255), 0)
            blue = max(min(blue, 255), 0)
        else:
            if red not in range(256) or green not in range(256) or blue not in range(256):
                raise ValueError("All eyes RGB({0}, {1}, {2}) are not in range of (0, 255).".format(red, green, blue))

        for position in range(1, 5):
            (cha_r, cha_g, cha_b) = self._get_rgb_channel(position)

            self._pwm.set_channel(cha_r, red)
            self._pwm.set_channel(cha_g, green)
            self._pwm.set_channel(cha_b, blue)

def test():
    """ Eye driver test on all position
    """
    import time

    for position in range(1, 5):
        print 'Position: ', position
        eye = Eye(position)

        for i in range(0, 256, 5):
            print 'R: ', i
            eye.red = i
            eye.set_color()
            time.sleep(0.02)

        eye.set_color(0, 0, 0)
        for i in range(0, 256, 5):
            print 'G: ', i
            eye.green = i
            eye.set_color()
            time.sleep(0.02)

        eye.set_color(0, 0, 0)
        for i in range(0, 256, 5):
            print 'B: ', i
            eye.blue = i
            eye.set_color()
            time.sleep(0.02)

        eye.set_color(0, 0, 0)

def install():
    """ Eye driver install test on all position
    """
    import time

    print 'Create objects'
    eye1 = Eye(1)
    eye2 = Eye(2)
    eye3 = Eye(3)
    eye4 = Eye(4)

    print 'Set eye color'
    eye1.set_color(255, 0, 0)
    eye2.set_color(0, 255, 0)
    eye3.set_color(0, 0, 255)
    eye4.set_color(255, 255, 255)

    time.sleep(2)

    eye1.set_all_color(0, 0, 0)


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        if sys.argv[1] == "install":
            install()
    else:
        test()
