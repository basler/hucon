#!/usr/bin/env python3
from machine import PWM
import math


class HSServo:
    """
    A simple class for controlling hobby servos.

    Args:
        pin : The pin where servo is connected. Must support PWM.
        freq : The frequency of the signal, in hertz.
        min_us : The minimum signal length supported by the servo.
        max_us : The maximum signal length supported by the servo.

    """
    @classmethod
    def __init__(cls, pin: machine.Pin, freq: int = 50, min_us: int = 1100, max_us: int = 1900):
        cls.min_us = min_us
        cls.total_range = max_us - min_us
        cls.pwm = PWM(pin, freq = freq, duty = 0)

    def set_angle(cls, degrees):
        """Move to the specified angle in `degrees`."""
        degrees = min(180, max(0, degrees))
        us = cls.min_us + (cls.total_range * degrees / 180)
        cls.write_us(us)
