from hucon import Eye
from hucon import Event, Button

eye = None

def A():
  global process_events, eye
  print('Top left')
  eye = Eye(1, Eye.GRB)
  eye.set_color(255, 0, 0)

def B():
  global process_events, eye
  print('Top right')
  eye = Eye(2, Eye.GRB)
  eye.set_color(255, 0, 0)

def C():
  global process_events, eye
  print('Bottom left')
  eye = Eye(3, Eye.GRB)
  eye.set_color(255, 0, 0)

def D():
  global process_events, eye
  print('Bottom right')
  eye = Eye(4, Eye.GRB)
  eye.set_color(255, 0, 0)

def Stop():
  global process_events, eye
  print('Stop')
  process_events.stop()


events_dict = {
  "A": Button(A),
  "B": Button(B),
  "C": Button(C),
  "D": Button(D),
  "Stop": Button(Stop)
}

process_events = Event(events_dict)
print('Start')
process_events.run()
print('End')
