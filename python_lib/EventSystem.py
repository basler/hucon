""" 2018-12-11

The event system is using SIGRT signals from linux.

Author: Sascha.MuellerzumHagen@baslerweb.com
"""

import signal
import tempfile
import os
import json


GLOB_EVENT_CALLBACK_DICT = None


class EventBase(object):
    """ Base class for all event based objects.
    """
    callback = None
    x = 0
    y = 0
    width = 1
    height = 1

    def __init__(self, register_callback, x, y, width, height):
        self.callback = register_callback
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class ButtonEvent(EventBase):
    """ Button event object. Can be assigned to one event per instance.
    """

    def __init__(self, register_callback, x=0, y=0, width=1, height=1):
        super(Button, self).__init__(register_callback, x, y, width, height)


class EventSystem(object):
    """ Receive events over a signal event.
    """
    _POSSIBLE_EVENTS_FILE = os.path.join(tempfile.gettempdir(), 'possible_events')

    _run = True

    def __init__(self, events_dict):
        """ Set the handler to catch the signal for the process.
        """
        global GLOB_EVENT_CALLBACK_DICT

        GLOB_EVENT_CALLBACK_DICT = {}
        GRID_WIDTH = 8
        GRID_HEIGHT = 8

        # Generate a map of numbers to handle the events and add it to the events to catch
        index = 0
        events_to_catch = {}

        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if 'Y' not in events_to_catch:
                    events_to_catch['Y'] = {}

                if str(y) not in events_to_catch['Y']:
                    events_to_catch['Y'][str(y)] = {}

                if 'X' not in events_to_catch['Y'][str(y)]:
                    events_to_catch['Y'][str(y)]['X'] = {}

                if str(x) in events_to_catch['Y'][str(y)]['X']:
                    print('[red] Error')

                events_to_catch['Y'][str(y)]['X'][str(x)] = None

        for key in events_dict:
            value = events_dict[key]

            # Add a simple button event
            GLOB_EVENT_CALLBACK_DICT[index] = value.callback

            # check if the space is empty to put the object into it
            for y in range(value.y, value.y + value.height):
                for x in range(value.x, value.x + value.width):
                    if events_to_catch['Y'][str(y)]['X'][str(x)] is not None:
                        name = events_to_catch['Y'][str(y)]['X'][str(x)]['Name']
                        raise Exception("[red] Error: '%s' and '%s' are using the same space (x: %s / y: %s)" % (key, name, x, y))

            events_to_catch['Y'][str(value.y)]['X'][str(value.x)] = {'Type': 'Button', 'Name': key, 'Event': index, 'Width': value.width, 'Height': value.height}

            # Use a place holder to signalize a none empty space
            for y in range(value.y, value.y + value.height):
                for x in range(value.x, value.x + value.width):
                    if events_to_catch['Y'][str(y)]['X'][str(x)] is None:
                        events_to_catch['Y'][str(y)]['X'][str(x)] = {'Type': 'PlaceHolder', 'Name': key}

            # Increment the index
            index += 1

        # Write the possible events into the list for the web page.
        with open(self._POSSIBLE_EVENTS_FILE, 'w') as file_handle:
            json.dump(events_to_catch, file_handle)
        file_handle.close()

        if len(GLOB_EVENT_CALLBACK_DICT) > (signal.SIGRTMAX - signal.SIGRTMIN):
            raise Exception('There are not enough events available!')

        # Connect all SIRGT signal to the global reachable function.
        for i in range(signal.SIGRTMAX - signal.SIGRTMIN):
            signal.signal(signal.SIGRTMIN + i, EventSystem.receive_signal)

    def run(self):
        """ Run in an endless loop to catch all events.
        """
        while self._run:
            pass

    def stop(self):
        """ Stop the current running endless loop
        """
        self._run = False

    @staticmethod
    def receive_signal(signum, stack):
        """ The signal was received, so call the event handler with the event from the file.
        """
        del stack # unused
        global GLOB_EVENT_CALLBACK_DICT

        if GLOB_EVENT_CALLBACK_DICT is not None:
            index = signum - signal.SIGRTMIN
            # check the index also
            GLOB_EVENT_CALLBACK_DICT[index]()
