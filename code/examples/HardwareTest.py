from hackerschool import Eye
from hackerschool import Servo
from hackerschool import Motor
import time

eyes = None
servo = None
motor = None
j = None
eye = None
i = None

"""Describe this function...
"""
def test_eyes():
  global eyes, servo, motor, j, eye, i
  eyes = [Eye(1, Eye.RGB), Eye(2, Eye.RGB), Eye(3, Eye.RGB), Eye(4, Eye.RGB)]
  servo = Servo(2)
  motor = Motor(2)
  for j in range(1, 5):
    eye = eyes[int(j - 1)]
    for i in range(0, 256, 25):
      time.sleep(0.2)
      eye.set_color(i, i, i)
  servo.set_angle(90)
  time.sleep(0.2)

"""Describe this function...
"""
def test_servo():
  global eyes, servo, motor, j, eye, i
  print('Test the servo on channel 2')
  servo = Servo(1)
  servo.set_angle(90)
  time.sleep(0.5)
  servo.set_angle(0)
  time.sleep(0.5)
  servo.set_angle(180)
  time.sleep(0.5)
  servo.set_angle(90)

"""Describe this function...
"""
def test_motor():
  global eyes, servo, motor, j, eye, i
  print('Test the motor on channel 1')
  motor = Motor(2)
  motor.set_speed(0)
  time.sleep(0.5)
  motor.set_speed((-100))
  time.sleep(0.5)
  motor.set_speed(100)
  time.sleep(0.5)
  motor.set_speed(0)


print('Do a test for the hardware.')
test_eyes()
test_servo()
test_motor()
