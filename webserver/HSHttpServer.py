#!/usr/bin/python


import SimpleHTTPServer
from BaseHTTPServer import HTTPServer
import os
import json

from HSTerm import HSTerm


class HSRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="HackerSchool"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        ''' Present frontpage with user authentication. '''
        if self.headers.get('Authorization') is None:
            self.do_AUTHHEAD()
            self.wfile.write('no auth header received')

        elif self.headers.get('Authorization') == 'Basic ' + str(self.server._authorization_key):
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

        else:
            self.do_AUTHHEAD()
            self.wfile.write('not authenticated')

    def do_POST(self):
        ''' Present frontpage with user authentication. '''
        if self.headers.get('Authorization') is None:
            self.do_AUTHHEAD()
            self.wfile.write('no auth header received')
            self.wfile.close()

        elif self.headers.get('Authorization') == 'Basic ' + str(self.server._authorization_key):

            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            # HSTerm.term("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n" % (str(self.path), str(self.headers), post_data.decode('utf-8')))

            # Clear the exec file.
            HSTerm.clear_exec()

            # Set the filename to the exec file anyway.
            filename = HSTerm.exec_filename()

            if self.path.startswith('/__FILE_ACCESS__?'):
                try:
                    # Extract the variables and handle the file access
                    variables = HSHttpServer.get_dict_from_url(self.path)

                    HSTerm.term('FileAccess: %s' % variables['command'])

                    if variables['command'] == 'save':
                        # Store all incomming data into the file.
                        HSTerm.term('Save file %s' % variables['filename'])
                        savename = HSHttpServer._CODE_ROOT + '/' + variables['filename']
                        with open(savename, 'wb') as file:
                            file.write(post_data)
                        HSTerm.term_exec('File %s saved.' % savename)
                        HSTerm.term_exec('%d bytes written.' % content_length)
                        self.sendFile(200, filename)

                    elif variables['command'] == 'execute':
                        # Execute the code from RAM when the content is smaller than 1k
                        HSTerm.term('Execute from RAM.')

                        post_data = post_data.decode('utf-8')

                        # Execute the give data.
                        try:
                            exec(post_data, globals())
                            self.sendFile(200, filename)
                        except Exception as e:
                            HSTerm.term_exec('Error: %s' % str(e))
                            self.sendFile(500, filename)

                    elif variables['command'] == 'load':
                        # Return the file.
                        filename = self.server._CODE_ROOT + '/' + variables['filename']
                        self.sendFile(200, filename)

                    else:
                        # The given command is not known.
                        self.sendFile(404, '404.html')

                except Exception as e:
                    HSTerm.term_exec('Internal Error:\n%s' % str(e))
                    self.sendFile(500, filename)

            elif self.path.startswith('/__COMMAND__'):
                try:
                    # Convert the json data into a key/value dictionary.
                    args = json.loads(post_data.decode('utf-8'))

                    HSTerm.term('Command: "%s"' % args['command'])

                    # Save the new password key only when the oldkey is the same with the current.
                    if args['command'] == 'save_password':
                        if (args['oldKey'] == self.server._authorization_key and args['newKey'] != ''):

                            HSTerm.term('Store the new password')
                            # Store the password.
                            self.server._authorization_key = args['newKey']
                            with open('password', 'w') as file:
                                file.write(self.server._authorization_key)

                            HSTerm.term_exec('New password written.')

                        else:
                            HSTerm.term('auth key: %s' % self.server._authorization_key)
                            HSTerm.term('old key: %s' % args['oldKey'])
                            HSTerm.term('new key: %s' % args['newKey'])
                            HSTerm.term_exec('Error: Could not store the password.')
                            HSTerm.term_exec('The current Password is not the same!')
                        self.sendFile(200, filename)

                    # Get the list of all available code files.
                    elif args['command'] == 'get_file_list':

                        data = {}
                        data['files'] = os.listdir(self.server._CODE_ROOT)
                        data['files'].sort()
                        json_dump = json.dumps(data)

                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write(json_dump)
                        return

                    # Run the file which is saved on the device
                    elif args['command'] == 'run':
                        run_file = self.server._CODE_ROOT + '/' + args['filename']
                        try:
                            exec(open(run_file).read(), globals())
                        except Exception as e:
                            HSTerm.term_exec('Error: %s' % str(e))

                    else:
                        # The given command is not known.
                        self.sendFile(404, '404.html')
                        return

                except Exception as e:
                    HSTerm.term_exec('Internal Error:\n%s' % str(e))
                    self.sendFile(500, filename)
                    return

                else:
                    self.sendFile(200, filename)
                    return

        else:
            self.do_AUTHHEAD()
            self.wfile.write('Invalid credentials')

    def send_error(self, code, message):
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        f = open('404.html', 'rb')
        self.wfile.write(f.read())
        f.close()

    def sendFile(self, response, filename):
        if not os.path.exists(filename):
            filename = os.path.join(self.server._DOCUMENT_ROOT, '404.hml')
            response = 404

        self.send_response(response)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        f = open(filename, 'rb')
        self.wfile.write(f.read())
        f.close()


class HSHttpServer(HTTPServer):
    """
    This implementation is a simple HTTP Server which works on Windows, Linux and macOS with different Browser.
    """

    # Folder where all files for the server are stored.
    _DOCUMENT_ROOT = os.path.abspath(os.path.join(os.getcwd(), 'www'))

    # Folder where all custom code files are stored.
    _CODE_ROOT = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), 'code')

    # Define the port on which the server should listening on.
    _LISTENING_PORT = 8080

    # Private key for the authorization to the key.
    _authorization_key = ''

    def __init__(self, key):
        """
        Create a socket to get its own ip address.
        """
        HSTerm.term("Code path: '%s'" % self._CODE_ROOT)
        HSTerm.term("WWW path: '%s'\n" % self._DOCUMENT_ROOT)
        self._authorization_key = key
        HTTPServer.__init__(self, ('', 8080), HSRequestHandler)

    def get_auth_key(self):
        return self._authorization_key

    def start(self):
        """
        Configure the server completly and start it forever.
        """
        HSTerm.term('Starting server, use <Ctrl+C> to stop.')
        os.chdir(self._DOCUMENT_ROOT)
        try:
            self.serve_forever()
        except KeyboardInterrupt:
            pass
        self.server_close()

    @staticmethod
    def get_dict_from_url(url):
        """
        Get a dict of all variables from an url.
        """
        variables = url.split('?')[1]
        variables = variables.replace('&', '","')
        variables = variables.replace('=', '":"')
        variables = '{"%s"}' % variables
        variables = json.loads(variables)
        return variables
