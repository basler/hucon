#!/usr/bin/env python
'''
**********************************************************************
* Filename    : Motor.py
* Description : Driver module for leds, with PCA9685
* Author      : Sascha Mueller zum Hagen
**********************************************************************
'''

import PCA9685

class Eye(object):
    '''Eye driver class'''
    _MIN_PULSE_WIDTH = 0
    _MAX_PULSE_WIDTH = 1024
    _DEFAULT_PULSE_WIDTH = 0
    _FREQUENCY = 60

    _DEBUG = False
    _DEBUG_INFO = 'DEBUG "Eye.py":'

    def __init__(self, position, lock=True, address=0x4A):
        ''' Init an eye on specific position, this offset '''
        if position<1 or position>4:
            raise ValueError("Eye position \"{0}\" is not in (1, 4).".format(position))
        if self._DEBUG:
            print self._DEBUG_INFO, "Debug on"
        self.position = position
        self.lock = lock

        self.pwm = PCA9685.PWM(address=address)
        self.pwm.setup()
        self.frequency = self._FREQUENCY
        self._set_channel(position)
        self.red = 0
        self.green = 0
        self.blue = 0
        self.set_color(self.red, self.green, self.blue)

    def _set_channel(self, position):
        if position == 1:
            self.channel_red   = 2
            self.channel_green = 1
            self.channel_blue  = 0
        elif position == 2:
            self.channel_red   = 15
            self.channel_green = 14
            self.channel_blue  = 13
        elif position == 3:
            self.channel_red   = 7
            self.channel_green = 6
            self.channel_blue  = 5
        else:
            self.channel_red   = 12
            self.channel_green = 11
            self.channel_blue  = 10

    def _color_to_analog(self, color):
        ''' Calculate 12-bit analog value from giving color '''
        pulse_wide   = self.pwm.map(color, 0, 255, self._MIN_PULSE_WIDTH, self._MAX_PULSE_WIDTH)
        analog_value = int(float(pulse_wide) / 1000000 * self.frequency * 4096)
        if self._DEBUG:
            print self._DEBUG_INFO, 'Color %d equals Analog_value %d' % (color, analog_value)
        return analog_value

    @property
    def red(self):
        return self._red

    @red.setter
    def red(self, value):
        self._red = value

    @property
    def green(self):
        return self._green

    @green.setter
    def green(self, value):
        self._green = value

    @property
    def blue(self):
        return self._blue

    @blue.setter
    def blue(self, value):
        self._blue = value

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, value):
        self._frequency = value
        self.pwm.frequency = value

    def set_color(self, red=None, green=None, blue=None):

        if red == None:
            red = self.red
        else:
            self.red = red
        if green == None:
            green = self.green
        else:
            self.green = green
        if blue == None:
            blue = self.blue
        else:
            self.blue = blue

        ''' Set the color on the pre seted eye. '''
        if self.lock:
            if red > 255:
                red = 255
            if red < 0:
                red = 0
            if green > 255:
                green = 255
            if green < 0:
                green = 0
            if blue > 255:
                blue = 255
            if blue < 0:
                blue = 0
        else:
            if red<0 or red>255 or green<0 or green>255 or blue<0 or blue>255:
                raise ValueError("Eye \"{0}\" RGB({1}, {2}, {3}) is not in (0, 255).".format(self.channel, red, green, blue))
        val_red = self._color_to_analog(red)
        val_green = self._color_to_analog(green)
        val_blue = self._color_to_analog(blue)

        self.pwm.write(self.channel_red,   0, val_red)
        self.pwm.write(self.channel_green, 0, val_green)
        self.pwm.write(self.channel_blue,  0, val_blue)
        if self._DEBUG:
            print self._DEBUG_INFO, 'Set color = %d %d %d' % (red, green, blue)

    @property
    def debug(self):
        return self._DEBUG

    @debug.setter
    def debug(self, debug):
        ''' Set if debug information shows '''
        if debug in (True, False):
            self._DEBUG = debug
        else:
            raise ValueError('debug must be "True" (Set debug on) or "False" (Set debug off), not "{0}"'.format(debug))

        if self._DEBUG:
            print self._DEBUG_INFO, "Set debug on"
        else:
            print self._DEBUG_INFO, "Set debug off"

def test():
    '''Eye driver test on all position'''
    import time

    for position in range(1, 5):
        print "Position: ", position
        eye = Eye(position)

        for i in range(0, 256, 5):
            print "R: ", i
            eye.red = i
            eye.set_color()
            time.sleep(0.02)

        eye.set_color(0,0,0)
        for i in range(0, 256, 5):
            print "G: ", i
            eye.green = i
            eye.set_color()
            time.sleep(0.02)

        eye.set_color(0,0,0)
        for i in range(0, 256, 5):
            print "B: ", i
            eye.blue = i
            eye.set_color()
            time.sleep(0.02)

        eye.set_color(0,0,0)

def install():
    '''Eye driver install test on all position'''
    import time

    eye1 = Eye(1)
    eye2 = Eye(2)
    eye3 = Eye(3)
    eye4 = Eye(4)

    eye1.set_color(255, 0, 0)
    eye2.set_color(0, 255, 0)
    eye3.set_color(0, 0, 255)
    eye4.set_color(255, 255, 255)

    time.sleep(2)

    eye1.set_color(0, 0, 0)
    eye2.set_color(0, 0, 0)
    eye3.set_color(0, 0, 0)
    eye4.set_color(0, 0, 0)


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        if sys.argv[1] == "install":
            install()
    else:
        test()