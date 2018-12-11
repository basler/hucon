""" 2018-12-11

Set the speed form the motor.

Author: Sascha.MuellerzumHagen@baslerweb.com
"""

from hucon import Motor

motor = None


print('Set the motor to full speed forward.')
motor = Motor(2)
motor.set_speed(100)
