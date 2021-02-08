""" Set motor to speed.

    Copyright (C) 2019 Basler AG
    All rights reserved.

    This software may be modified and distributed under the terms
    of the BSD license.  See the LICENSE file for details.
"""

from hucon.hucon import Motor

motor = None


print('Set the motor to full speed forward.')
motor = Motor(2)
motor.set_speed(100)
