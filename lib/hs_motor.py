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
    def __init__(cls, pin: machine.Pin, offset: int = 0, freq: int = 50):
        cls.center = 512 + offset
        cls.pwm = PWM(pin, freq = freq, duty = 0)

    @classmethod
    def set_speed(cls, speed):
        """Set the signal to be `%`. Zero disables it."""

        # Stop the motor at null speed
        duty = 0
        # Forward speed.
        if speed > 0:
            duty = (1023 - cls.center) * speed / 100 + cls.center
        # Backward speed.
        if speed < 0:
            duty = cls.center * speed / 100 + cls.center

        duty = min(1023, max(0, duty))
        cls.pwm.duty(duty)
