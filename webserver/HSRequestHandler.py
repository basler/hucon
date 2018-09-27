#!/usr/bin/python

import SimpleHTTPServer
import os
import json
import subprocess
import time
import tempfile
import sys
import signal

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

    def replace_hucon_requests(self, message):

        search_string = 'print(\'Hello HuCon!\')'
        replace_string = 'print(\'Hello HuCon!\\n\\nHello human!\\nI am a human controlled robot.\\n\\n\')'
        if search_string in message:
            message = message.replace(search_string, replace_string)
        return message


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
                print('Save file %s' % args['filename'])

                savename = self.server._CODE_ROOT + '/' + args['filename']
                with open(savename, 'w') as file:
                    file.write(args['data'])
                self.server._log.put('File %s saved. %d bytes written.' % (savename, content_length))

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write('Done ...')

            elif self.path == '/file_load':
                # Return the file to the browser.
                print('Load file %s' % args['filename'])

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
                message = 'Done ...'

                if self.server._is_running is False:
                    try:
                        self.server._is_running = True

                        # save the data into a file
                        filename = os.path.join(tempfile.gettempdir(), 'execute.py')

                        with open(filename, 'w') as f:
                            f.write(self.replace_hucon_requests(args['data']))
                        f.close()

                        proc = subprocess.Popen(['python', '-u', filename], bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                        self.server._current_pid = proc.pid

                        while True:
                            output = proc.stdout.readline()
                            if output == '' and proc.poll() is not None:
                                break
                            if output:
                                # Replace the file error like 'File "/tmp/execute.py", line x, in'
                                output = output.replace('File "/tmp/execute.py", l', 'L')
                                self.server._log.put(output.strip())
                        proc.poll()

                    except Exception as e:
                        self.server._log.put('Error: %s' % str(e))

                    time.sleep(0.1)
                    # Wait until the queue is empty
                    while self.server._log.empty() is False:
                        time.sleep(0.1)

                    self.server._is_running = False
                    self.server._current_pid = None

                else:
                    message = 'There is a programm running.'

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(message)

            elif self.path == '/run':
                # Run the file which is saved on the device
                message = 'Done ...'

                if self.server._is_running is False:
                    print('Run file %s' % args['filename'])
                    run_file = self.server._CODE_ROOT + '/' + args['filename']
                    try:
                        self.server._is_running = True

                        proc = subprocess.Popen(['python', '-u', run_file], bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                        self.server._current_pid = proc.pid

                        while True:
                            output = proc.stdout.readline()
                            if output == '' and proc.poll() is not None:
                                break
                            if output:
                                # Replace the file error like 'File "/tmp/execute.py", line x, in'
                                output = output.replace('File "/tmp/execute.py", l', 'L')
                                self.server._log.put(output.strip())
                        proc.poll()

                    except Exception as e:
                        self.server._log.put('Error: %s' % str(e))

                    time.sleep(0.1)
                    # Wait until the queue is empty
                    while self.server._log.empty() is False:
                        time.sleep(0.1)

                    self.server._is_running = False
                    self.server._current_pid = None
                else:
                    message = 'There is a programm running.'

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(message)

            elif self.path == '/get_file_list':
                # Return the list of all files to the browser.
                data['files'] = os.listdir(self.server._CODE_ROOT)
                data['files'].sort()
                json_dump = json.dumps(data)

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(json_dump)

            elif self.path == '/is_running':
                # Get the current running state of the device
                data['is_running'] = self.server._is_running
                json_dump = json.dumps(data)

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(json_dump)

            elif self.path == '/kill':
                # Kill the current running process
                if self.server._current_pid != None:
                    os.kill(self.server._current_pid, signal.SIGKILL)
                    time.sleep(0.1)

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write('Done ...')

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
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write('')

                # Update the system first.
                self.server._log.put('The system will be updated and needs a few seconds.\n')
                proc = subprocess.Popen(['sh', self.server._UPDATE_FILE, '-u'], bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                while True:
                    output = proc.stdout.readline()
                    if output == '' and proc.poll() is not None:
                        break
                    if output:
                        self.server._log.put(output.strip())
                proc.poll()

                # Do a restart.
                proc = subprocess.Popen(['sh', self.server._UPDATE_FILE, '-r'], bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                while True:
                    output = proc.stdout.readline()
                    if output == '' and proc.poll() is not None:
                        break
                    if output:
                        self.server._log.put(output.strip())
                proc.poll()

            elif self.path == '/shutdown':
                # Shutdown the robot.
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write('')

                # Update the system first.
                self.server._log.put('The system will be shutdown.\n')
                proc = subprocess.Popen(['sh', self.server._UPDATE_FILE, '-s'], bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                while True:
                    output = proc.stdout.readline()
                    if output == '' and proc.poll() is not None:
                        break
                    if output:
                        self.server._log.put(output.strip())
                proc.poll()

            elif self.path == '/check_update':
                # Check if ther is an update available
                proc = subprocess.Popen(['sh', self.server._UPDATE_FILE, '-c'], bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                while True:
                    output = proc.stdout.readline()
                    if output == '' and proc.poll() is not None:
                        break
                    if output:
                        self.server._log.put(output.strip())
                proc.poll()

                if proc.returncode == 1:
                    data['is_update_available'] = True
                else:
                    data['is_update_available'] = False

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(json.dumps(data))

            elif self.path == '/save_password':
                # Save the new password key only when the oldkey is the same with the current.
                message = ''
                if (args['oldKey'] == self.server._authorization_key and args['newKey'] != ''):

                    print('Store the new password')
                    # Store the password.
                    self.server._authorization_key = args['newKey']
                    with open(self.server._PASSWORD_FILE, 'w') as file:
                        file.write(self.server._authorization_key)

                    message = 'New password written.'

                else:
                    print('The current used key is wrong.')
                    message += 'Error: Could not store the password.\n'
                    message += 'The current Password is not correct!'

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(message)

            elif self.path == '/poll':
                message = self.server._log.get_message_wait()

                try:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/plain')
                    self.end_headers()
                    self.wfile.write(message)
                except Exception as e:
                    # The message could not transfered to teh browser. So requeue it!
                    self.server._log.requeue(message)

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
