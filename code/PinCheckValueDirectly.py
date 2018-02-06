from machine import Pin


# Überprüfe den Wert des Eingangs.
if Pin(2).value() == 1:
  HSTerm.term_exec('Ja ich empfange ein Signal am Eingang.')
else:
  HSTerm.term_exec('Hmmm, ich kann nichts sehen.')
