#!/usr/bin/python

import SimpleHTTPServer
import os
import json
import subprocess
import time

from HSTerm import HSTerm

class HSRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="HackerSchool"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write('not authenticated')
        self.wfile.close()

    def do_GET(self):
        """
        Present frontpage with user authentication.
        """
        if self.headers.get('Authorization') is None:
            self.do_AUTHHEAD()

        elif self.headers.get('Authorization') == 'Basic ' + str(self.server._authorization_key):

            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

        else:
            self.do_AUTHHEAD()

    def do_POST(self):
        """
        Present frontpage with user authentication.
        """
        if self.headers.get('Authorization') is None:
            self.do_AUTHHEAD()

        elif self.headers.get('Authorization') == 'Basic ' + str(self.server._authorization_key):

            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            if self.path.startswith('/__FILE_ACCESS__?'):
                try:
                    # Extract the variables and handle the file access
                    variables = self.get_dict_from_url(self.path)

                    HSTerm.term('FileAccess: %s' % variables['command'])

                    if variables['command'] == 'save':
                        # Store all incomming data into the file.
                        HSTerm.term('Save file %s' % variables['filename'])
                        savename = HSHttpServer._CODE_ROOT + '/' + variables['filename']
                        with open(savename, 'wb') as file:
                            file.write(post_data)
                        HSTerm.term_exec('File %s saved.' % savename)
                        HSTerm.term_exec('%d bytes written.' % content_length)

                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write('Done ...')

                    elif variables['command'] == 'execute':
                        # Execute the code from RAM when the content is smaller than 1k
                        HSTerm.term('Execute from RAM.')

                        post_data = post_data.decode('utf-8')

                        # Execute the given data.
                        try:
                            HSTerm.term_exec('Run ...\n')
                            exec(post_data, globals())
                            HSTerm.term_exec('\n... Done\n\n')
                        except Exception as e:
                            HSTerm.term_exec('Error: %s' % str(e))

                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write('Done ...')

                    elif variables['command'] == 'load':
                        # Return the file.
                        filename = self.server._CODE_ROOT + '/' + variables['filename']

                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        f = open(filename, 'rb')
                        self.wfile.write(f.read())
                        f.close()

                    else:
                        # The given command is not known.
                        self.send_response(404)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write('Command not known.')

                except Exception as e:
                    HSTerm.term_exec('Internal Error:\n%s' % str(e))
                    self.send_response(500)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write('Done ...')

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

                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write('Done ...')

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

                    # Get the version of this project.
                    elif args['command'] == 'get_version':

                        data = {}
                        data['version'] = self.server._version
                        json_dump = json.dumps(data)

                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write(json_dump)

                    # Run the file which is saved on the device
                    elif args['command'] == 'run':
                        run_file = self.server._CODE_ROOT + '/' + args['filename']
                        try:
                            exec(open(run_file).read(), globals())
                        except Exception as e:
                            HSTerm.term_exec('Error: %s' % str(e))

                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write('Done ...')

                    # Update all files from the project.
                    elif args['command'] == 'update':

                        # Run the update script and save the content to send.
                        bash = subprocess.Popen(['sh', self.server._UPDATE_FILE, '-c'], stdout=subprocess.PIPE)
                        data = bash.communicate()[0]

                        HSTerm.term_exec(data)

                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write('Done ...')

                        # Reboot only if there is an update.
                        if bash.returncode == 1:
                            HSTerm.term_exec('\nThe system will be updated / reboot and is available in a few seconds.\n\n\n')
                            subprocess.check_output(['sh', self.server._UPDATE_FILE, '-u', '-r'])

                    else:
                        # The given command is not known.
                        self.send_response(404)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write('Command not known.')

                except Exception as e:
                    HSTerm.term_exec('Internal Error:\n%s' % str(e))

                    self.send_response(500)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write('Internal Error.')

            elif self.path == '/poll':
                message = HSTerm.get_message_wait()

                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(message)

        else:
            self.do_AUTHHEAD()

    def get_dict_from_url(self, url):
        """
        Get a dict of all variables from an url.
        """
        variables = url.split('?')[1]
        variables = variables.replace('&', '","')
        variables = variables.replace('=', '":"')
        variables = '{"%s"}' % variables
        variables = json.loads(variables)
        return variables
