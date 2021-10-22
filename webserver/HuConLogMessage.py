#!/usr/bin/python
""" HuConLogMessage.py - The HuCon queue class for log messages.

    Copyright (C) 2019 Basler AG
    All rights reserved.

    This software may be modified and distributed under the terms
    of the BSD license.  See the LICENSE file for details.
"""
from enum import Enum
from typing import List
import queue


# warning if this is changed, change enum in webserver.js accordingly
class MessageType(Enum):
    INPUT_ENQUIRY = 1
    OUTPUT = 2


class Message:
    content_type = None
    content = ''

    def __init__(self, content: str, content_type=MessageType.OUTPUT):
        self.content = content
        self.content_type = content_type

    def serialize(self):
        result = {'content': self.content, 'content_type': self.content_type.value}
        return result


class HuConLogMessage:
    # Queue to store the messages.
    _queue = None

    def __init__(self):
        """ Create the queue to store the log messages.
        """
        self._queue = queue.Queue()

    def empty(self):
        """ Returns true when the log is empty, otherwise false.
        """
        return self._queue.empty()

    def get_messages(self) -> List[Message]:
        """ Return the message if there is any one. Otherwise the string ins empty
        """
        message = []
        while self._queue.empty() is False:
            message += [self._queue.get()]

        return message

    def requeue(self, messages: List[Message]):
        """ Put the message into the input queue and do not add a new line.
        """
        for message in messages:
            self._queue.put(message)

    def put_input(self, message: str):
        """ Put the message into the input queue.
        """
        self._queue.put(Message(content=message, content_type=MessageType.INPUT_ENQUIRY))

    def put_output(self, message: str):
        """ Put the message into the output queue.
        """
        self._queue.put(Message(content=message, content_type=MessageType.OUTPUT))
