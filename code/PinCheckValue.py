from machine import Pin

eingang = None


# Erzeuge eine Variable mit den Eigenschaften eines Pins.
eingang = Pin(2)
# Überprüfe den Wert des Eingangs.
if eingang.value() == 1:
  HSTerm.term_exec('Ja ich empfange ein Signal am Eingang.')
else:
  HSTerm.term_exec('Hmmm, ich kann nichts sehen.')
