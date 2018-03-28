#!/usr/bin/python

import time
import Queue

class HSLogMessage():

    def __init__(self):
        """
        Create the event and lock objects for the threaded access.
        """
        self.queue = Queue.Queue()

    def clear(self):
        self.queue.clear()

    def join(self):
        self.queue.join()

    def empty(self):
        return self.queue.empty()

    def requeue(self, message):
        return self.queue.put(message)

    def wait(self):
        """
        Wait until a new message is set and return the data of it.
        """
        while self.queue.empty() is True:
            time.sleep(0.1)

        data = ''
        while self.queue.empty() is False:
            data += self.queue.get()
        return data

    def post(self, data):
        """
        Save the data and set/clear the event to post them.
        Sleep for 100 milliseconds to give the browser a chance to receive them.
        """
        self.queue.put(data + '\n')
