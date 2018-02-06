from neopixel import NeoPixel
from machine import Pin

np = None


# Erzeuge eine Liste mit die alle LED beinhaltet.
np = NeoPixel(Pin(14), 2)
# Setze die erste LED auf Rot
np[0] = (0, 255, 0)
# Setze die erste LED auf Rot
np[1] = (153, 0, 0)
# Schreiben den Wert in die LED um diese auch zu setzen.
np.write()
