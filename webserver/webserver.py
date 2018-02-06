#!/usr/bin/python


from hs_http_server import HSHttpServer
from hs_term import HSTerm


# Default key is hacker:school base64 coded.
key = 'aGFja2VyOnNjaG9vbA=='


def main():
    """
    Create the Server and listen on each incomming request.
    """
    global key

    # Load the password if possible.
    try:
        with open('password', 'r') as file:
            key = file.read()
    except Exception as e:
        pass

    # Create the server and start it.
    server = HSHttpServer(key)
    server.start()

    HSTerm.term('Stop Server')


if __name__ == '__main__':
    main()
