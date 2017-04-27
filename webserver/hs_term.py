#!/usr/bin/env python3

try:
    # Import different packages on the micro python.
    import uos as os
    import usocket as socket
except:
    import os
    import socket

class HSTerm:

    def term(message):
        print(message)
