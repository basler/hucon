#!/usr/bin/env python3
from machine import PWM
import math


class HSMotor:
    """
    A simple class for controlling hobby servos which are modified to a motor.

    Args:
        pin    : The pin where servo is connected. Must support PWM.
        offset : The offset which is needed to stop the motor.
        freq   : The frequency of the signal, in hertz.

    """
    @classmethod
    def __init__(cls, pin: machine.Pin, offset: int = 0, freq: int = 50, min_us: int = 1100, max_us: int = 1900):
        cls.freq = freq
        cls.min_us = min_us
        cls.max_us = max_us
        cls.total_range = max_us - min_us
        cls.offset = offset
        cls.pwm = PWM(pin, freq = cls.freq, duty = 0)

    @classmethod
    def write_us(cls, us: int):
        """Set the signal to be ``us`` microseconds long. Zero disables it."""
        us = min(cls.max_us, max(cls.min_us, us))
        duty = us * 1024 * cls.freq // 1000000
        cls.pwm.duty(duty)

    @classmethod
    def set_speed(cls, speed):
        """Set the signal to be `%`. Zero disables it."""

        speed = min(100, max(-100, speed))
        if speed == 0:
            cls.pwm.duty(0)
            return

        speed = speed + cls.offset

        us = cls.min_us + (cls.total_range * (speed + 100) // 200)
        print('us: %d' % us)
        cls.write_us(us)
