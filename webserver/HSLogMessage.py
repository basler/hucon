#!/usr/bin/python

import time
import Queue

class HSLogMessage():

    # Queue to store the messages.
    _queue = None

    def __init__(self):
        """
        Create the queue to store the log messages.
        """
        self._queue = Queue.Queue()

    def empty(self):
        """
        Returns true when the log is empty, otherwise false.
        """
        return self._queue.empty()

    def get_message_wait(self):
        """
        Wait until a new message is set and return the message of it.
        """
        while self._queue.empty() is True:
            time.sleep(0.1)

        message = ''
        while self._queue.empty() is False:
            message += self._queue.get()
        return message

    def requeue(self, message):
        """
        Put the message into the queue and do not add a new line.
        """
        self._queue.put(message)

    def put(self, message):
        """
        Put the message into the queue.
        """
        self._queue.put(message + '\n')
