from hs_servo import HSServo
from machine import Pin

servo = None


HSTerm.term_exec('Set the servo to 90 degrees.')
# Erzeuge eine Variable mit den Eigenschaften
# eines Servos und setze den Winkel auf 90 Grad.
servo = HSServo(Pin(13))
servo.set_angle(90)
