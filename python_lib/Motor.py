#!/usr/bin/env python
""" 2018-12-11

Driver module for servo-motor, with PCA9685

Author: Sascha.MuellerzumHagen@baslerweb.com
"""

import PCA9685

class Motor(object):
    """ Motor driver class
    """
    _MIN_PULSE_WIDTH = 600
    _MAX_PULSE_WIDTH = 2400
    _DEFAULT_PULSE_WIDTH = 1500
    _FREQUENCY = 60

    _DEBUG = False
    _DEBUG_INFO = 'DEBUG "Motor.py":'

    def __init__(self, channel, offset=0, lock=True, address=0x5A):
        """ Init a motor on specific channel
        """
        if channel<0 or channel > 16:
            raise ValueError("Motor channel \"{0}\" is not in (0, 15).".format(channel))
        if self._DEBUG:
            print self._DEBUG_INFO, "Debug on"
        self.channel = channel
        self.offset = offset
        self.lock = lock

        self.pwm = PCA9685.PWM(address=address)
        self.pwm.setup()
        self.frequency = self._FREQUENCY
        self.set_speed(0)

    def _speed_to_analog(self, speed):
        """ Calculate 12-bit analog value from giving speed
        """
        pulse_wide   = self.pwm.map(speed, -100, 100, self._MIN_PULSE_WIDTH, self._MAX_PULSE_WIDTH)
        analog_value = int(float(pulse_wide) / 1000000 * self.frequency * 4096)
        if self._DEBUG:
            print self._DEBUG_INFO, 'Speed %d equals Analog_value %d' % (speed, analog_value)
        return analog_value

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, value):
        self._frequency = value
        self.pwm.frequency = value

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        """ Set offset for much user-friendly
        """
        self._offset = value
        if self._DEBUG:
            print self._DEBUG_INFO, 'Set offset to %d' % self.offset

    def set_speed(self, speed):
        """ Turn the motor with giving speed. """
        if self.lock:
            if speed > 100:
                speed = 100
            if speed < -100:
                speed = -100
        else:
            if speed<-100 or speed>100:
                raise ValueError("Motor \"{0}\" turn speed \"{1}\" is not in (-100, 100).".format(self.channel, speed))

        speed = speed + self.offset
        val = self._speed_to_analog(speed)
        self.pwm.write(self.channel, 0, val)
        if self._DEBUG:
            print self._DEBUG_INFO, 'Turn speed = %d' % speed

    @property
    def debug(self):
        return self._DEBUG

    @debug.setter
    def debug(self, debug):
        """ Set if debug information shows
        """
        if debug in (True, False):
            self._DEBUG = debug
        else:
            raise ValueError('debug must be "True" (Set debug on) or "False" (Set debug off), not "{0}"'.format(debug))

        if self._DEBUG:
            print self._DEBUG_INFO, "Set debug on"
        else:
            print self._DEBUG_INFO, "Set debug off"

def range_test():
    """ Motor driver test on channel 0
    """
    import time
    a = Motor(0)
    print self._DEBUG_INFO, "Set Speed: -100"
    a.set_speed(-100)
    time.sleep(0.2)
    print self._DEBUG_INFO, "Set Speed: 0"
    a.set_speed(0)
    time.sleep(0.2)
    print self._DEBUG_INFO, "Set Speed: 100"
    a.set_speed(100)
    time.sleep(0.2)
    print self._DEBUG_INFO, "Set Speed: 0"
    a.set_speed(0)

def test():
    """ Motor driver test on channel 0
    """
    import time
    a = Motor(0)
    for i in range(-100, 100, 10):
        print i
        a.set_speed(i)
        time.sleep(0.1)
    for i in range(100, -100, -10):
        print i
        a.set_speed(i)
        time.sleep(0.1)
    for i in range(-100, 0, 5):
        a.set_speed(i)
        time.sleep(0.05)
    print i

def install():
    all_motor = [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0]
    for i in range(16):
        all_motor[i] = Motor(i)
    for motor in all_motor:
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