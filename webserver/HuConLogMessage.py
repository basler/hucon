#!/usr/bin/python
""" HuConLogMessage.py - The HuCon queue class for log messages.

    Copyright (C) 2019 Basler AG
    All rights reserved.

    This software may be modified and distributed under the terms
    of the BSD license.  See the LICENSE file for details.
"""

import Queue

class HuConLogMessage():

    # Queue to store the messages.
    _queue = None

    def __init__(self):
        """ Create the queue to store the log messages.
        """
        self._queue = Queue.Queue()

    def empty(self):
        """ Returns true when the log is empty, otherwise false.
        """
        return self._queue.empty()

    def get_message(self):
        """ Return the message if there is any one. Otherwise the string ins empty
        """
        message = []
        while self._queue.empty() is False:
            message += [self._queue.get()]

        return message

    def requeue(self, message):
        """ Put the message into the queue and do not add a new line.
        """
        self._queue.put(message)

    def put(self, message):
        """ Put the message into the queue.
        """
        self._queue.put(message)
