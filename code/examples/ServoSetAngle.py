""" 2018-12-11

Move servo to angle.

Author: Sascha.MuellerzumHagen@baslerweb.com
"""

from hucon import Servo

servo = None


print('Set the servo to 90 degrees.')
servo = Servo(2)
servo.set_angle(90)
