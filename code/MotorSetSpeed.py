from hs_motor import HSMotor
from machine import Pin

motor = None


HSTerm.term_exec('Set the Motor to full speed forward.')
# Erzeuge eine Variable mit den Eigenschaften eines Motor.
motor = HSMotor(Pin(12), 0)
motor.set_speed(100)
