#!/usr/bin/env python
""" Motor.py - Driver module for servo-motor, with PCA9685

    Copyright (C) 2019 Basler AG
    All rights reserved.

    This software may be modified and distributed under the terms
    of the BSD license.  See the LICENSE file for details.
"""

from .PCA9685 import PCA9685

class Motor(object):
    """ Motor driver class.

        The PCA9685 is working with a frequency of 50Hz. That result in a period of 20 ms.
        This period has a range of 4096 steps which will result in a step of 4.88 us.
        Normal servos are working with a pulse width from 1 to 2 ms. I Think it is better
        to support a bigger range from 0.6 to 2.4 ms to get it to work.
    """
    _MIN_PULSE_WIDTH = 122.88 #  600 us * 4096 / 20000 us
    _MAX_PULSE_WIDTH = 491.52 # 2400 us * 4096 / 20000 us
    _SPEED_STEP = 1.8432 # (self._MAX_PULSE_WIDTH - self._MIN_PULSE_WIDTH) / 200.0

    def __init__(self, channel, offset=0, lock=True, address=0x5A):
        """ Init a motor on specific channel
        """
        if channel not in range(16):
            raise ValueError("Motor channel \"{0}\" is not in (0, 15).".format(channel))

        self._channel = channel
        self._offset = offset
        self._lock = lock

        self._pwm = PCA9685(address=address)

        self.set_speed(0)

    def _speed_to_pwm(self, speed):
        """ Calculate 12-bit analog value from giving speed.
            The speed from -100 to 100 has to be recalculated to a range from _MIN_PULSE_WIDTH to _MAX_PULSE_WIDTH.
            -100 is equivalent to _MIN_PULSE_WIDTH and 100 is equivalent to _MAX_PULSE_WIDTH.
        """

        pwm_value = 0
        if speed != 0:
            speed += 100
            pwm_value = int(speed * self._SPEED_STEP + self._MIN_PULSE_WIDTH + 0.5)

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

    def set_speed(self, speed):
        """ Turn the motor with giving speed.
        """
        if self._lock:
            speed = max(min(speed, 100), -100)
        else:
            if speed not in range(-100, 101):
                raise ValueError("Motor \"{0}\" turn speed \"{1}\" is not in (-100, 100).".format(self._channel, speed))

        speed = speed + self.offset
        val = self._speed_to_pwm(speed)
        self._pwm.set_channel(self._channel, val)

    def set_all_off(self):
        """ Turn all pwm channels of.
        """
        self._pwm.set_all_channel(0)

def range_test():
    """ Motor driver test on channel 0
    """
    import time
    motor = Motor(0)
    print("Set Speed: -100")
    motor.set_speed(-100)
    time.sleep(0.2)
    print("Set Speed: 0")
    motor.set_speed(0)
    time.sleep(0.2)
    print("Set Speed: 100")
    motor.set_speed(100)
    time.sleep(0.2)
    print("Set Speed: 0")
    motor.set_speed(0)

def test():
    """ Motor driver test on channel 0
    """
    import time
    motor = Motor(0)
    for i in range(-100, 100, 10):
        print(i)
        motor.set_speed(i)
        time.sleep(0.1)
    for i in range(100, -100, -10):
        print(i)
        motor.set_speed(i)
        time.sleep(0.1)
    for i in range(-100, 0, 5):
        motor.set_speed(i)
        time.sleep(0.05)
    print(i)


def install():
    """ Run a simple install test.
    """
    for i in range(16):
        motor = Motor(i)
        motor.set_speed(90)

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        if sys.argv[1] == "install":
            install()
        elif sys.argv[1] == "range_test":
            range_test()
    else:
        test()
