import signal
import tempfile
import os

_internal_event_handler = None

_events_to_catch = None


def receive_signal(signum, stack):
    """
    The signal was received, so call the event handler with the event from the file.
    """
    global _internal_event_handler
    global _events_to_catch

    if _internal_event_handler is not None:
        index = signum - signal.SIGRTMIN
        _internal_event_handler(_events_to_catch[index])


class ProcessEvent():
    """
    Receive events over a signal event.
    """

    _EVENT_FILE = os.path.join(tempfile.gettempdir(), 'event')

    _POSSIBLE_EVENTS_FILE = os.path.join(tempfile.gettempdir(), 'possible_events')

    def __init__(cls, event_handler, events_to_catch):
        """
        Set the handler to catch the signal for the process.
        """
        global _internal_event_handler
        global _events_to_catch

        _internal_event_handler = event_handler
        _events_to_catch = events_to_catch

        with open(cls._POSSIBLE_EVENTS_FILE, 'w') as file:
            file.write(str({"PostCommands": events_to_catch}).replace("'", '"'))
        file.close()

        cls._events_to_catch = events_to_catch
        for x in range(signal.SIGRTMAX - signal.SIGRTMIN):
            signal.signal(signal.SIGRTMIN + x, receive_signal)

    def run(cls):
        """
        Run in an endless loop to catch all events.
        """
        while True:
            pass
