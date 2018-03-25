#!/usr/bin/python

import time
import threading

class HSLogMessage():

    def __init__(self):
        """
        Create the event and lock objects for the threaded access.
        """
        self.data = ''
        self.event = threading.Event()
        self.lock = threading.Lock()
        self.event.clear()

    def wait(self):
        """
        Wait until a new message is set and return the data of it.
        """
        self.event.wait()
        return self.data

    def post(self, data):
        """
        Save the data and set/clear the event to post them.
        Sleep for 100 milliseconds to give the browser a chance to receive them.
        """
        with self.lock:
            self.data = data
            self.event.set()
            self.event.clear()
            time.sleep(0.1)
