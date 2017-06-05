#!/usr/bin/env python3
from machine import PWM
import math


class HSMotor:
    """
    A simple class for controlling hobby servos which are modified to a motor.

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

    def set_speed(self, speed):
        """Set the signal to be ``us`` microseconds long. Zero disables it."""
        if speed < -100:
            speed = -100
        if speed > 100:
            speed = 100
        if speed == 0:
            self.pwm.duty(0)
            return
        speed = min(self.max_us, max(self.min_us, speed))
        duty = speed * 1024 * self.freq // 1000000
        self.pwm.duty(duty)
