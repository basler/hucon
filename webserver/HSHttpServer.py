#!/usr/bin/python

from BaseHTTPServer import HTTPServer
from SocketServer import ThreadingMixIn
import os

from HSLogMessage import HSLogMessage
from HSRequestHandler import HSRequestHandler

ThreadingMixIn.daemon_threads = True
class HSHttpServer(ThreadingMixIn, HTTPServer):
    """
    This implementation is a simple HTTP Server which works on Windows, Linux and macOS with different Browser.
    """

    # Name for the server to identificate
    _SERVER_NAME = 'HuCon'

    # Folder where all files for the server are stored.
    _DOCUMENT_ROOT = os.path.abspath(os.path.join(os.getcwd(), 'www'))

    # Folder where all custom code files are stored.
    _CODE_ROOT = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), 'code')

    # Path to the version file.
    _VERSION_FILE = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), '__version__')

    # Path to the password file.
    _PASSWORD_FILE = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), 'password')

    # Path to the update file.
    _UPDATE_FILE = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), 'update.sh')

    # Define the port on which the server should listening on.
    _LISTENING_PORT = 8080

    # Print more debug messages
    _debug = False

    # Private key for the authorization to the key.
    _authorization_key = ''

    # Current version of the server.
    _version = 'beta\n'

    # Store the current running state
    _is_running = False

    # Store the current process to comunicate with a runing process
    _current_proc = None

    # Possible post data events stored as json format
    _possible_post_data = None

    # Queue for all log messages
    _log = HSLogMessage()

    def __init__(cls, key, debug=False):
        """
        Create a socket to get its own ip address.
        """
        if os.path.exists(cls._VERSION_FILE):
            with open(cls._VERSION_FILE, 'r') as file:
                cls._version = file.readline()

        print('%s v. %s' % (cls._SERVER_NAME, cls._version))
        print('Code path: \'%s\'' % cls._CODE_ROOT)
        print('WWW path:  \'%s\'\n' % cls._DOCUMENT_ROOT)
        cls._authorization_key = key
        cls._debug = debug
        HTTPServer.__init__(cls, ('', cls._LISTENING_PORT), HSRequestHandler)

    def get_auth_key(cls):
        """
        Returns the authorization key for the webpages.
        """
        return cls._authorization_key

    def start(cls):
        """
        Configure the server completly and start it forever.
        """
        print('Starting server, use <Ctrl+C> to stop.')
        cls._log.put('\n\nServer started ...\n\n')
        os.chdir(cls._DOCUMENT_ROOT)
        try:
            cls.serve_forever()
        except KeyboardInterrupt:
            pass
        cls.server_close()
