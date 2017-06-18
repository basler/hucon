#!/usr/bin/env python3

try:
    from hs_http_server import HSHttpServer
    from hs_term import HSTerm
except Exception as e:
    print('Could not import the http server: %s' % str(e))

def main():
    """
    Create the Server and listen on each incomming request.
    """

    # Default key is hacker:school base64 coded.
    key = 'aGFja2VyOnNjaG9vbA=='

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
