from neopixel import NeoPixel
from machine import Pin
import time

index = None
np = None
np_value_2 = None
np_value_1 = None
g = None
r = None

"""
Diese Funktion lässt die LED's in unterschiedlichen Farben leuchten.

Hier wird nur die Funktion definiert aber nicht ausgeführt!
"""
def LED_Leuchten():
  global index, np, np_value_2, np_value_1, g, r
  np = NeoPixel(Pin(14), 2)
  index = 0
  for count in range(255):
    r = 255 - index
    g = index
    np_value_1 = (0, r, 0)
    np_value_2 = (g, 0, 0)
    np[0] = np_value_1
    np[1] = np_value_2
    np.write()
    index = index + 1
    time.sleep(0.1)


# Führe die Funktion LED_Leuchten aus.
LED_Leuchten()
