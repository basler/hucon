#!/usr/bin/env python3

from hs_http_server import HSHttpServer
from hs_term import HSTerm

def main(useThreads=False):
    """
    Create the Server and listen on each incomming request.
    """
    server = HSHttpServer()

    server.start(useThreads)

    HSTerm.term('Stop Server')


if __name__ == '__main__':
    main()
