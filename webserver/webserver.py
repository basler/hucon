#!/usr/bin/python
import argparse

from HSHttpServer import HSHttpServer


# Default key is empty
key = ''


def main():
    """
    Create the Server and listen on each incomming request.
    """
    parser = argparse.ArgumentParser(description='Start the HuCon webserver.')
    parser.add_argument('--debug',
                        dest='debug',
                        action='store_true',
                        help='Print more debug messages on the console during running.')

    args = parser.parse_args()

    global key

    # Load the password if possible.
    try:
        with open(HSHttpServer._PASSWORD_FILE, 'r') as file:
            key = file.read()
    except Exception as e:
        pass

    # Create the server and start it.
    server = HSHttpServer(key, args.debug)
    server.start()

    print('Stop Server')


if __name__ == '__main__':
    main()
