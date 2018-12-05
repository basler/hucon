#!/usr/bin/python

import SimpleHTTPServer
import os
import json
import subprocess
import time
import tempfile
import signal

class HSRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def log_message(cls, format, *args):
        """
        Overwrite the log method to disable all log messages during run.
        """
        if cls.server._debug:
            print("%s - [%s] %s" % (cls.client_address[0], cls.log_date_time_string(), format % args))

    def do_AUTHHEAD(cls):
        """
        Send a 'Authentication' response to the browser.
        """
        cls.send_response(401)
        cls.send_header('WWW-Authenticate', 'Basic realm="%s"' % cls.server._SERVER_NAME)
        cls.send_header('Content-type', 'text/html')
        cls.end_headers()
        cls.wfile.write('not authenticated')
        cls.wfile.close()

    def do_GET(cls):
        """
        Overwrite the default get method to handle authentication to the server if needed.
        """
        if cls._is_authorized():
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(cls)

        else:
            cls.do_AUTHHEAD()

    def do_POST(cls):
        """
        Overwrite the default post method to handle all post request directly.
        """
        if cls._is_authorized():

            content_length = int(cls.headers['Content-Length'])
            post_data = cls.rfile.read(content_length)
            args = {}
            if post_data != '':
                args = json.loads(post_data.decode('utf-8'))

            if cls.path == '/file_save':
                cls._save_file(args, content_length)

            elif cls.path == '/file_load':
                cls._load_file(args)

            elif cls.path == '/execute':
                cls._execute(args)

            elif cls.path == '/run':
                cls._run(args)

            elif cls.path == '/event':
                cls._event(args)

            elif cls.path == '/get_file_list':
                cls._get_file_list()

            elif cls.path == '/get_possible_post_data':
                cls._get_possible_post_data()

            elif cls.path == '/is_running':
                cls._is_running()

            elif cls.path == '/kill':
                cls._kill()

            elif cls.path == '/get_version':
                cls._get_version()

            elif cls.path == '/check_update':
                cls._check_update()

            elif cls.path == '/update':
                cls._update()

            elif cls.path == '/shutdown':
                cls._shutdown()

            elif cls.path == '/save_password':
                cls._save_password(args)

            elif cls.path == '/poll':
                cls._poll()

            else:
                # The given command is not known.
                cls._response(404, 'text/html', 'Command not known.\n')

        else:
            cls.do_AUTHHEAD()

    def _save_file(cls, args, content_length):
        """
        Save the received content on the local disk.
        """
        # Store all incoming data into the file.
        savename = cls.server._CODE_ROOT + '/' + args['filename']
        try:
            with open(savename, 'w') as file:
                file.write(args['data'])
        except Exception as e:
            cls._response(500, 'text/html', str(e))
        else:
            cls._response(200, 'text/html', 'File %s saved. %d bytes written.\n' % (savename, content_length))

    def _load_file(cls, args):
        """
        Return the content of the file back to the browser.
        """
        data = {}

        filename = cls.server._CODE_ROOT + '/' + args['filename']
        try:
            f = open(filename, 'r')
            data['data'] = f.read()
            f.close()
            json_dump = json.dumps(data)
        except Exception as e:
            cls._response(500, 'text/html', str(e))
        else:
            cls._response(200, 'text/html', json_dump)

    def _execute(cls, args):
        """
        Store the data on a local file and execute them.
        """
        if cls.server._is_running is False:
            try:
                cls.server._is_running = True

                # save the data into a file
                filename = os.path.join(tempfile.gettempdir(), 'execute.py')

                with open(filename, 'w') as f:
                    f.write(cls._replace_hucon_requests(args['data']))
                f.close()

                # Wait fgor a while until the file is realy closed before it can be executed.
                time.sleep(0.2)

                cls._run_file(filename)

            except Exception as e:
                cls.server._log.put('Error: %s' % str(e))

            time.sleep(0.1)
            # Wait until the queue is empty
            while cls.server._log.empty() is False:
                time.sleep(0.1)

            cls.server._is_running = False
            cls.server._current_proc = None

            cls._response(200, 'text/html', '')
        else:
            cls._response(503, 'text/html', 'There is a program running.\n')

    def _run(cls, args):
        """
        Run the file which is saved on the device
        """
        if cls.server._is_running is False:
            print('Run file %s' % args['filename'])
            filename = cls.server._CODE_ROOT + '/' + args['filename']
            try:
                cls.server._is_running = True

                cls._run_file(filename)

            except Exception as e:
                cls.server._log.put('Error: %s' % str(e))

            time.sleep(0.1)
            # Wait until the queue is empty
            while cls.server._log.empty() is False:
                time.sleep(0.1)

            cls.server._is_running = False
            cls.server._current_proc = None
            cls._response(200, 'text/html', '')
        else:
            cls._response(503, 'text/html', 'There is a program running.')

    def _event(cls, args):
        """
        Store the event on a file and call the
        """
        if cls.server._current_proc:
            if os.name == 'nt':
                cls._response(500, 'text/html', 'Could not set the event.')
            else:
                os.kill(cls.server._current_proc.pid, signal.SIGRTMIN + args['EventNumber'])
                cls._response(200, 'text/html', 'OK')
        else:
            cls._response(503, 'text/html', 'There is no program running')

    def _get_file_list(cls):
        """
        Return the list of all files to the browser.
        """
        try:
            data = {}
            data['files'] = os.listdir(cls.server._CODE_ROOT)
            data['files'].sort()
            json_dump = json.dumps(data)
        except Exception as e:
            cls._response(500, 'text/html', str(e))
        else:
            cls._response(200, 'text/html', json_dump)

    def _get_possible_post_data(cls):
        """
        Return the json of available post data events.
        """
        try:
            data = ''
            # with open(ProcessEvent._EVENT_FILE, 'r') as file:
            with open(os.path.join(tempfile.gettempdir(), 'possible_events'), 'r') as file:
                data = file.read()
            file.close()
        except Exception as e:
            cls._response(500, 'text/html', str(e))
        else:
            cls._response(200, 'text/html', data)

    def _is_running(cls):
        """
        Get the current running state of the device
        """
        try:
            data = {}
            data['is_running'] = cls.server._is_running
            json_dump = json.dumps(data)
        except Exception as e:
            cls._response(500, 'text/html', str(e))
        else:
            cls._response(200, 'text/html', json_dump)

    def _kill(cls):
        """
        Kill the current running process
        """
        if cls.server._current_proc:
            try:
                cls.server._current_proc.send_signal(signal.CTRL_C_EVENT)
            except:
                pass
        if cls.server._current_proc:
            try:
                cls.server._current_proc.send_signal(signal.CTRL_BREAK_EVENT)
            except:
                pass
        if cls.server._current_proc:
            try:
                cls.server._current_proc.send_signal(signal.SIGTERM)
            except:
                pass
        time.sleep(0.1)

        cls._response(200, 'text/html', 'Application stopped.\n')

    def _get_version(cls):
        """
        Get the version of this project.
        """
        try:
            data = {}
            data['version'] = cls.server._version
            json_dump = json.dumps(data)
        except Exception as e:
            cls._response(500, 'text/html', str(e))
        else:
            cls._response(200, 'text/html', json_dump)

    def _check_update(cls):
        """
        Check if there is an update available
        """
        try:
            raise Exception('Error')
            proc = subprocess.Popen(['sh', cls.server._UPDATE_FILE, '-c'], bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            while True:
                output = proc.stdout.readline()
                if output == '' and proc.poll() is not None:
                    break
                if output:
                    cls.server._log.put(output.strip())
            proc.poll()

            data = {}
            if proc.returncode == 1:
                data['is_update_available'] = True
            else:
                data['is_update_available'] = False
        except Exception as e:
            cls._response(500, 'text/html', str(e))
        else:
            cls._response(200, 'text/html', json.dumps(data))

    def _update(cls):
        """
        Update all files from the project.
        """
        try:
            cls._response(200, 'text/html', '')

            # Update the system first.
            cls.server._log.put('The system will be updated and needs a few seconds.\n')
            proc = subprocess.Popen(['sh', cls.server._UPDATE_FILE, '-u'], bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            while True:
                output = proc.stdout.readline()
                if output == '' and proc.poll() is not None:
                    break
                if output:
                    cls.server._log.put(output.strip())
            proc.poll()

            # Do a restart.
            proc = subprocess.Popen(['sh', cls.server._UPDATE_FILE, '-r'], bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            while True:
                output = proc.stdout.readline()
                if output == '' and proc.poll() is not None:
                    break
                if output:
                    cls.server._log.put(output.strip())
            proc.poll()
        except Exception as e:
            cls.server._log.put(str(e))

    def _shutdown(cls):
        """
        Shutdown the robot.
        """
        try:
            cls._response(200, 'text/html', '')

            # Update the system first.
            cls.server._log.put('The system will be shutdown.\n')
            proc = subprocess.Popen(['sh', cls.server._UPDATE_FILE, '-s'], bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            while True:
                output = proc.stdout.readline()
                if output == '' and proc.poll() is not None:
                    break
                if output:
                    cls.server._log.put(output.strip())
            proc.poll()
        except Exception as e:
            cls.server._log.put(str(e))

    def _save_password(cls, args):
        """
        Save the new password key only when the oldkey is the same with the current.
        """
        try:
            message = ''
            # Remove the password
            if (args['oldKey'] == cls.server._authorization_key and args['remove']):
                cls.server._authorization_key = ''
                with open(cls.server._PASSWORD_FILE, 'w') as file:
                    file.write(cls.server._authorization_key)
                message = 'Password removed.'

            # Store the password.
            elif ((cls.server._authorization_key == '' or args['oldKey'] == cls.server._authorization_key) and args['newKey'] != ''):
                cls.server._authorization_key = args['newKey']
                with open(cls.server._PASSWORD_FILE, 'w') as file:
                    file.write(cls.server._authorization_key)
                message = 'New password written.'

            else:
                if args['remove']:
                    message += 'Error: Could not remove the password.\n'
                else:
                    message += 'Error: Could not store the password.\n'
                message += 'The current Password is not correct!'
        except Exception as e:
            cls._response(500, 'text/html', str(e))
        else:
            cls._response(200, 'text/html', message)

    def _poll(cls):
        """
        Return the log messages to the browser.
        """
        try:
            data = {}
            data['message'] = cls.server._log.get_message()
            cls._response(200, 'text/plain', json.dumps(data))
        except Exception as e:
            # The message could not transfered to the browser. So re queue it!
            cls.server._log.requeue(data['message'])

    def _replace_hucon_requests(cls, message):
        """
        Print an answer from HuCon whenever the the message 'Hello HoCon!' is found.
        """
        search_string = 'print(\'Hello HuCon!\')'
        replace_string = 'print(\'Hello HuCon!\\n\\nHello human!\\nI am a human controlled robot.\\n\\n\')'
        if search_string in message:
            message = message.replace(search_string, replace_string)
        return message

    def _run_file(cls, filename):
        """
        Run the file and catch all output of it.
        """
        cls.server._current_proc = subprocess.Popen(['python', '-u', filename],
                                                    bufsize=1,
                                                    stdin=subprocess.PIPE,
                                                    stdout=subprocess.PIPE,
                                                    stderr=subprocess.STDOUT)

        while True:
            output = cls.server._current_proc.stdout.readline()
            if output == '' and cls.server._current_proc.poll() is not None:
                break
            if output:
                # Replace the file error like 'File "/tmp/execute.py", line x, in'
                line = output.replace('File "' + filename + '", l', 'Error: L')

                cls.server._log.put(line)
        cls.server._current_proc.poll()

    def _response(cls, status, content_type, data):
        """
        Send the response back to the server.
        """
        try:
            cls.send_response(status)
            cls.send_header('Content-type', content_type)
            cls.end_headers()
            cls.wfile.write(data)
        except Exception as e:
            print('error on response')
            print(str(e))
            print(status)
            print(content_type)
            print(data)

    def _is_authorized(cls):
        """
        Return true when the authorization is OK.
        This is always good when the key is empty.
        """
        authenticated = False

        if cls.server._authorization_key == '':
            authenticated = True

        elif cls.headers.get('Authorization') == 'Basic ' + str(cls.server._authorization_key):
            authenticated = True

        return authenticated

    def get_dict_from_url(cls, url):
        """
        Get a dictionary of all variables from an URL.
        """
        variables = url.split('?')[1]
        variables = variables.replace('&', '","')
        variables = variables.replace('=', '":"')
        variables = '{"%s"}' % variables
        variables = json.loads(variables)
        return variables
