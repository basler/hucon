#!/usr/bin/python

import SimpleHTTPServer
import os
import json
import subprocess
import time

from HSTerm import HSTerm

class HSRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_AUTHHEAD(self):
        """
        Send a 'Authentication' response to the browser.
        """
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
        if self.headers.get('Authorization') == 'Basic ' + str(self.server._authorization_key):
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

        else:
            self.do_AUTHHEAD()

    def do_POST(self):
        """
        Present frontpage with user authentication.
        """
        if self.headers.get('Authorization') == 'Basic ' + str(self.server._authorization_key):

            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            args = {}
            if post_data != '':
                args = json.loads(post_data.decode('utf-8'))
            data = {}

            if self.path == '/file_save':
                # Store all incomming data into the file.
                HSTerm.term('Save file %s' % args['filename'])

                savename = self.server._CODE_ROOT + '/' + args['filename']
                with open(savename, 'w') as file:
                    file.write(args['data'])
                HSTerm.term_exec('File %s saved. %d bytes written.' % (savename, content_length))

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write('Done ...')

            elif self.path == '/file_load':
                # Return the file to the browser.
                HSTerm.term('Load file %s' % args['filename'])

                filename = self.server._CODE_ROOT + '/' + args['filename']
                f = open(filename, 'r')
                data['data'] = f.read()
                f.close()
                json_dump = json.dumps(data)

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(json_dump)

            elif self.path == '/execute':
                # Execute the code from RAM when the content is smaller than 1k
                HSTerm.term('Execute from RAM.')
                try:
                    HSTerm.term_exec('Run ...\n')
                    exec(args['data'], globals())
                    HSTerm.term_exec('\n... Done\n\n')
                except Exception as e:
                    HSTerm.term_exec('Error: %s' % str(e))

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write('Done ...')

            elif self.path == '/run':
                # Run the file which is saved on the device
                HSTerm.term('Run file %s' % args['filename'])
                run_file = self.server._CODE_ROOT + '/' + args['filename']
                try:
                    HSTerm.term_exec('Run ...\n')
                    exec(open(run_file).read(), globals())
                    HSTerm.term_exec('\n... Done\n\n')
                except Exception as e:
                    HSTerm.term_exec('Error: %s' % str(e))

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write('Done ...')

            elif self.path == '/get_file_list':
                # Return the list of all files to the browser.
                data['files'] = os.listdir(self.server._CODE_ROOT)
                data['files'].sort()
                json_dump = json.dumps(data)

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(json_dump)

            elif self.path == '/get_version':
                # Get the version of this project.
                data['version'] = self.server._version
                json_dump = json.dumps(data)

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(json_dump)

            elif self.path == '/update':
                # Update all files from the project.
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

            elif self.path == '/save_password':
                # Save the new password key only when the oldkey is the same with the current.
                if (args['oldKey'] == self.server._authorization_key and args['newKey'] != ''):

                    HSTerm.term('Store the new password')
                    # Store the password.
                    self.server._authorization_key = args['newKey']
                    with open(self.server._PASSWORD_FILE, 'w') as file:
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

            elif self.path == '/poll':
                message = HSTerm.get_message_wait()

                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(message)

            else:
                # The given command is not known.
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write('Command not known.')

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
