""" Move servo to angle.

    Copyright (C) 2019 Basler AG
    All rights reserved.

    This software may be modified and distributed under the terms
    of the BSD license.  See the LICENSE file for details.
"""

from hucon import Servo

servo = None


print('Set the servo to 90 degrees.')
servo = Servo(2)
servo.set_angle(90)
