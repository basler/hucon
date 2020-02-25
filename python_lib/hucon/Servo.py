#!/usr/bin/env python
""" Servo.py - Driver module for leds, with PCA9685

    Copyright (C) 2019 Basler AG
    All rights reserved.

    This software may be modified and distributed under the terms
    of the BSD license.  See the LICENSE file for details.
"""

from .PCA9685 import PCA9685

class Servo(object):
    """ Servo driver class.

        The PCA9685 is working with a frequency of 50Hz. That result in a period of 20 ms.
        This period has a range of 4096 steps which will result in a step of 4.88 us.
        Normal servos are working with a pulse width from 1 to 2 ms. I Think it is better
        to support a bigger range from 0.6 to 2.4 ms to get it to work.
    """
    _MIN_PULSE_WIDTH = 122.88 #  600 us * 4096 / 20000 us
    _MAX_PULSE_WIDTH = 491.52 # 2400 us * 4096 / 20000 us
    _DEGREE_STEP = 2.048 # (self._MAX_PULSE_WIDTH - self._MIN_PULSE_WIDTH) / 180.0

    def __init__(self, channel, offset=0, lock=True, address=0x5A):
        """ Init a servo on specific channel
        """
        if channel not in range(16):
            raise ValueError('Servo channel "{0}" is not in (0, 15).'.format(channel))

        self._channel = channel
        self._offset = offset
        self._lock = lock
        self._pwm = PCA9685(address)

        self.set_angle(90)

    def _angle_to_pwm(self, angle):
        """ Calculate 12-bit analog value from giving angle.
            The angle from 0 to 180 degrees has to be recalculated to a range from _MIN_PULSE_WIDTH to _MAX_PULSE_WIDTH.
            0 degree equivalent to _MIN_PULSE_WIDTH and 180 degree is equivalent to _MAX_PULSE_WIDTH.
        """
        pwm_value = int(angle * self._DEGREE_STEP + self._MIN_PULSE_WIDTH + 0.5)
        return pwm_value

    @property
    def offset(self):
        """ Returns the offset.
        """
        return self._offset

    @offset.setter
    def offset(self, value):
        """ Set offset for much user-friendly
        """
        self._offset = value

    def set_angle(self, angle):
        """ Turn the servo with giving angle.
        """
        if self._lock:
            angle = max(min(angle, 180), 0)
        else:
            if angle not in range(181):
                message = 'Servo "{0}" turn angle "{1}" is not in range (0, 180).'.format(self._channel, angle)
                raise ValueError(message)
        angle += self.offset
        val = self._angle_to_pwm(angle)
        self._pwm.set_channel(self._channel, val)

    def set_all_off(self):
        """ Turn all pwm channels of.
        """
        self._pwm.set_all_channel(0)

def range_test():
    """ Servo driver test on channel 0
    """
    import time
    servo = Servo(0)
    print ("Set Angle: 0")
    servo.set_angle(0)
    time.sleep(1)
    print ("Set Angle: 90")
    servo.set_angle(90)
    time.sleep(1)
    print ("Set Angle: 180")
    servo.set_angle(180)
    time.sleep(1)
    print ("Set Angle: 90")
    servo.set_angle(90)
    time.sleep(1)

    servo.set_all_off()

def test():
    """ Servo driver test on channel 0
    """
    import time
    servo = Servo(0)
    for i in range(0, 180, 5):
        print (i)
        servo.set_angle(i)
        time.sleep(0.1)
    for i in range(180, 0, -5):
        print (i)
        servo.set_angle(i)
        time.sleep(0.1)
    for i in range(0, 91, 2):
        servo.set_angle(i)
        time.sleep(0.05)
    print (i)

    servo.set_all_off()

def install():
    """ Run a simple install test.
    """
    for i in range(16):
        servo = Servo(i)
        servo.set_angle(90)

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        if sys.argv[1] == "install":
            install()
        elif sys.argv[1] == "range_test":
            range_test()
    else:
        test()
