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

    # Private key for the authorization to the key.
    _authorization_key = ''

    # Current version of the server.
    _version = 'beta\n'

    # Store the current running state
    _is_running = False

    # Store the current process id
    _current_pid = None

    # Queue for all log messages
    _log = HSLogMessage()

    def __init__(self, key):
        """
        Create a socket to get its own ip address.
        """
        if os.path.exists(self._VERSION_FILE):
            with open(self._VERSION_FILE, 'r') as file:
                self._version = file.readline()

        print('HackerSchool v. %s' % self._version)
        print('Code path: \'%s\'' % self._CODE_ROOT)
        print('WWW path: \'%s\'\n' % self._DOCUMENT_ROOT)
        self._authorization_key = key
        HTTPServer.__init__(self, ('', 8080), HSRequestHandler)

    def get_auth_key(self):
        """
        Returns the authorization key for the webpages.
        """
        return self._authorization_key

    def start(self):
        """
        Configure the server completly and start it forever.
        """
        print('Starting server, use <Ctrl+C> to stop.')
        self._log.put('Server started ...')
        os.chdir(self._DOCUMENT_ROOT)
        try:
            self.serve_forever()
        except KeyboardInterrupt:
            pass
        self.server_close()
