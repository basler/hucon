import signal
import tempfile
import os
import json


glob_event_callback_dict = None

class Button():
    """
    Button event type. This type has only one event which can be called.
    """
    callback = None
    x = 0
    y = 0

    def __init__(cls, callback, x=1, y=1):
        cls.callback = callback
        cls.x = x
        cls.y = y


class Event():
    """
    Receive events over a signal event.
    """
    _POSSIBLE_EVENTS_FILE = os.path.join(tempfile.gettempdir(), 'possible_events')

    _run = True

    def __init__(cls, events_dict):
        """
        Set the handler to catch the signal for the process.
        """
        global glob_event_callback_dict

        glob_event_callback_dict = {}

        # Generate a map of numbers to handle the events and add it to the events to catch
        index = 0
        events_to_catch = {}
        for key in events_dict:
            value = events_dict[key]

            # Add a simple button event
            glob_event_callback_dict[index] = value.callback
            if 'Button' in events_to_catch:
                events_to_catch['Button'] += [{'Name': key, 'Event': index, 'X': value.x, 'Y': value.y}]
            else:
                events_to_catch['Button'] = [{'Name': key, 'Event': index, 'X': value.x, 'Y': value.y}]

            # Increment the index
            index += 1

        # Write the possible events into the list for the web page.
        with open(cls._POSSIBLE_EVENTS_FILE, 'w') as file:
            json.dump(events_to_catch, file)
        file.close()

        if len(glob_event_callback_dict) > (signal.SIGRTMAX - signal.SIGRTMIN):
            raise(Exception('There are not enough events available!'))

        # Connect all SIRGT signal to the global reachable function.
        for x in range(signal.SIGRTMAX - signal.SIGRTMIN):
            signal.signal(signal.SIGRTMIN + x, Event.receive_signal)

    def run(cls):
        """
        Run in an endless loop to catch all events.
        """
        while cls._run:
            pass

    def stop(cls):
        """
        Stop the current running endless loop
        """
        cls._run = False

    @staticmethod
    def receive_signal(signum, stack):
        """
        The signal was received, so call the event handler with the event from the file.
        """
        global glob_event_callback_dict

        if glob_event_callback_dict is not None:
            index = signum - signal.SIGRTMIN
            # check the index also
            glob_event_callback_dict[index]()
