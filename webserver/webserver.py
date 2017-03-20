#!/usr/bin/env python3

from http_server import HTTPServer
from print import ColoredPrint as print

def main(useThreads=False):
    """
    Create the Server and listen on each incomming request.
    """
    print.init()
    server = HTTPServer()

    server.start(useThreads)

    print.term('Stop Server', print.INFO)


if __name__ == '__main__':
    main()
