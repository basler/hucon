""" 2018-12-11

Register four events into the event system and run an endless loop to catch all.
Register also a fifth callback to call the stop function of the event system.
Set an eye on every callback to show the event catch.

Author: Sascha.MuellerzumHagen@baslerweb.com
"""

from hucon import Eye
from hucon import EventSystem, ButtonEvent

eye = None


def call_a():
  """ Callback for Button 'Name A' event.
  """
  global eye
  print('Top left')
  eye = Eye(1, Eye.GRB)
  eye.set_color(255, 0, 0)


def call_b():
  """ Callback for Button 'Name B' event.
  """
  global eye
  print('Top right')
  eye = Eye(2, Eye.GRB)
  eye.set_color(255, 0, 0)


def call_c():
  """ Callback for Button 'Name C' event.
  """
  global eye
  print('Bottom left')
  eye = Eye(3, Eye.GRB)
  eye.set_color(255, 0, 0)


def call_d():
  """ Callback for Button 'Name D' event.
  """
  global eye
  print('Bottom right')
  eye = Eye(4, Eye.GRB)
  eye.set_color(255, 0, 0)

def call_stop():
  """ Callback for Button 'Stop' event.
  """
  global process_events, eye
  print('Stop')
  process_events.stop()


# Map event name to callback.
events_dict = {
  "Name A": ButtonEvent(register_callback=call_a, x=0, y=0, width=1, height=1),
  "Name B": ButtonEvent(register_callback=call_b, x=7, y=0, width=1, height=1),
  "Name C": ButtonEvent(register_callback=call_c, x=0, y=7, width=1, height=1),
  "Name D": ButtonEvent(register_callback=call_d, x=7, y=7, width=1, height=1),
  "Name Stop": ButtonEvent(register_callback=call_stop, x=3, y=3, width=2, height=2)
}

# Setup event system.
process_events = EventSystem(events_dict)

print('Start')

# Run forever.
process_events.run()

print('End')
