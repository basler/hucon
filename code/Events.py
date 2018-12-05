from hackerschool import ProcessEvent
from hackerschool import Eye

# Events to deal with
events = ['up', 'down', 'left', 'right']

# Define the event handler method
def event_handler(event):
    """
    This event handler is called whenever an event is fired from the event side.
    """
    if event == 'up':
        Eye(1, Eye.GRB).set_color(255, 0, 0)
        print('up-Event received')

    elif event == 'down':
        Eye(2, Eye.GRB).set_color(0, 255, 0)
        print('down-Event received')

    elif event == 'left':
        Eye(3, Eye.GRB).set_color(0, 0, 255)
        print('left-Event received')

    elif event == 'right':
        Eye(4, Eye.GRB).set_color(255, 255, 255)
        print('right-Event received')

# Create a process event object to handle the events
process_event = ProcessEvent(event_handler, events)

print('Waiting for events ...')

process_event.run()

print('Stop the programm')
