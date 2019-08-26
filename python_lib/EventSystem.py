""" 2018-12-11

The event system is using SIGRT signals from linux.

Author: Sascha.MuellerzumHagen@baslerweb.com
"""

import signal
import tempfile
import os
import json


GLOB_EVENT_CALLBACK_DICT = None


class Button(object):
    """ Button event object. Can be assigned to one event per instance.
    """
    callback = None
    x = 0
    y = 0

    def __init__(self, register_callback, x=1, y=1):
        self.callback = register_callback
        self.x = x
        self.y = y


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

        # Generate a map of numbers to handle the events and add it to the events to catch
        index = 0
        events_to_catch = {}
        for key in events_dict:
            value = events_dict[key]

            # Add a simple button event
            GLOB_EVENT_CALLBACK_DICT[index] = value.callback
            if 'Button' in events_to_catch:
                events_to_catch['Button'] += [{'Name': key, 'Event': index, 'X': value.x, 'Y': value.y}]
            else:
                events_to_catch['Button'] = [{'Name': key, 'Event': index, 'X': value.x, 'Y': value.y}]

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
