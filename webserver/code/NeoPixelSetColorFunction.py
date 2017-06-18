from neopixel import NeoPixel
from machine import Pin

np = None
right_eye = None
left_eye = None

"""Describe this function...
"""
def set_led(left_eye, right_eye):
  global np
  np = NeoPixel(Pin(14), 2)
  np[0] = left_eye
  np[1] = right_eye
  np.write()


set_led((255, 51, 51), (0, 255, 0))
