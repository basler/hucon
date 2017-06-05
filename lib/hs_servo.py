#!/usr/bin/env python3
from machine import PWM
import math


class HSServo:
    """
    A simple class for controlling hobby servos.

    Args:
        pin (machine.Pin): The pin where servo is connected. Must support PWM.
        freq (int): The frequency of the signal, in hertz.
        min_us (int): The minimum signal length supported by the servo.
        max_us (int): The maximum signal length supported by the servo.
        angle (int): The angle between the minimum and maximum positions.

    """
    def __init__(self, pin, freq=50, min_us=600, max_us=2400, angle=180):
        self.min_us = min_us
        self.max_us = max_us
        self.us = 0
        self.freq = freq
        self.angle = angle
        self.pwm = PWM(pin, freq=freq, duty=0)

    def set_angle(self, degrees):
        """Move to the specified angle in ``degrees`` or ``radians``."""
        if degrees < 0:
            degrees = 0
        if degrees > 180:
            degrees = 180
        total_range = self.max_us - self.min_us
        us = self.min_us + total_range * degrees // self.angle
        self.write_us(us)