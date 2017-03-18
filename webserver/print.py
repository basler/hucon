#!/usr/bin/env python3

try:
    # Import different packages on the micro python.
    import uos as os
    import usocket as socket
except:
    import os
    import socket

import colorama

class ColoredPrint:

    RESET = 0
    DEBUG = 1
    INFO = 2
    WARN = 3
    ERROR = 4

    _COLOR_CODES = {
        RESET: colorama.Fore.RESET,
        DEBUG: colorama.Fore.CYAN,
        INFO: colorama.Fore.GREEN,
        WARN: colorama.Fore.YELLOW,
        ERROR: colorama.Fore.RED,
    }

    def init():
        colorama.init()

    def term(message, color=RESET):
        print(ColoredPrint._COLOR_CODES[color] + message + colorama.Style.RESET_ALL)
