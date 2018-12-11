#!/usr/bin/python
""" 2018-12-11

The HuCon queue class for log messages.

Author: Sascha.MuellerzumHagen@baslerweb.com
"""

import Queue

class HuConLogMessage():

    # Queue to store the messages.
    _queue = None

    def __init__(cls):
        """ Create the queue to store the log messages.
        """
        cls._queue = Queue.Queue()

    def empty(cls):
        """ Returns true when the log is empty, otherwise false.
        """
        return cls._queue.empty()

    def get_message(cls):
        """ Return the message if there is any one. Otherwise the string ins empty
        """
        message = []
        while cls._queue.empty() is False:
            message += [cls._queue.get()]

        return message

    def requeue(cls, message):
        """ Put the message into the queue and do not add a new line.
        """
        cls._queue.put(message)

    def put(cls, message):
        """ Put the message into the queue.
        """
        cls._queue.put(message)
