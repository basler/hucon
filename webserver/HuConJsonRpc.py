import os
import json
import subprocess
import time
import tempfile
import signal

from HuConLogMessage import HuConLogMessage


class HuConJsonRpc():
    """
    This class implements the functionality of the which will the server provide.
    """

    # Name for the server to identification
    _SERVER_NAME = 'HuConRobot'

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
    _version = 'beta'

    # Store the current running state
    _is_running = False

    # Store the current process to communicate with a running process
    _current_proc = None

    # Possible post data events stored as json format
    _possible_post_data = None

    # Queue for all log messages
    _log = HuConLogMessage()

    def __init__(cls):
        """
        Initialize the RPC server.
        """
        if os.path.exists(cls._VERSION_FILE):
            with open(cls._VERSION_FILE, 'r') as file:
                cls._version = file.readline()

        print('%s v. %s' % (cls._SERVER_NAME, cls._version))
        print('Code path: \'%s\'' % cls._CODE_ROOT)

    def handle_control(cls, rpc_request):
        """
        Handle the JSON RPC request.
        """
        if rpc_request['method'] == 'get_version':
            return cls._get_version(rpc_request)
        elif rpc_request['method'] == 'poll':
            return cls._poll(rpc_request)
        elif rpc_request['method'] == 'get_file_list':
            return cls._get_file_list(rpc_request)
        elif rpc_request['method'] == 'create_folder':
            return cls._create_folder(rpc_request)
        elif rpc_request['method'] == 'load_file':
            return cls._load_file(rpc_request)
        elif rpc_request['method'] == 'save_file':
            return cls._save_file(rpc_request)
        elif rpc_request['method'] == 'is_running':
            return cls._get_is_running(rpc_request)
        elif rpc_request['method'] == 'execute':
            return cls._execute(rpc_request)
        elif rpc_request['method'] == 'run':
            return cls._run(rpc_request)
        elif rpc_request['method'] == 'kill':
            return cls._kill(rpc_request)
        elif rpc_request['method'] == 'get_possible_post_data':
            return cls._get_possible_post_data(rpc_request)
        elif rpc_request['method'] == 'event':
            return cls._event(rpc_request)
        elif rpc_request['method'] == 'check_update':
            return cls._check_update(rpc_request)
        elif rpc_request['method'] == 'update':
            return cls._update(rpc_request)
        elif rpc_request['method'] == 'shutdown':
            return cls._shutdown(rpc_request)
        elif rpc_request['method'] == 'save_password':
            return cls._save_password(rpc_request)
        else:
            return cls._return_error(rpc_request['id'], 'Command not known.')

    def _get_rpc_response(cls, rpc_id):
        """
        Return a json rpc response message.
        """
        rpc_response = {}
        rpc_response['jsonrpc'] = '2.0'
        rpc_response['result'] = ''
        rpc_response['id'] = rpc_id

        return rpc_response

    def _return_error(cls, rpc_id, error, status_code=400):
        """
        Return an well formed error.
        """
        rpc_response = {}
        rpc_response['jsonrpc'] = '2.0'
        rpc_response['error'] = error
        rpc_response['id'] = rpc_id

        return (json.dumps(rpc_response), status_code)

    def _replace_hucon_requests(cls, message):
        """
        Print an answer from HuCon whenever the the message 'Hello HoCon!' is found.
        """
        search_string = 'print(\'Hello HuCon!\')'
        replace_string = 'print(\'Hello HuCon!\\n\\nHello human!\\nI am a Hu[man] Con[trolled] robot.\\n\')'
        if search_string in message:
            message = message.replace(search_string, replace_string)
        return message

    def _run_file(cls, filename):
        """
        Run the file and catch all output of it.
        """
        cls._current_proc = subprocess.Popen(['python', '-u', filename],
                                             bufsize=1,
                                             stdin=subprocess.PIPE,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.STDOUT)

        while True:
            output = cls._current_proc.stdout.readline()
            if output == '' and cls._current_proc.poll() is not None:
                break
            if output:
                # Replace the file error like 'File "/tmp/execute.py", line x, in'
                line = output.replace('File "' + filename + '", l', 'Error: L')
                cls._log.put(line)

        cls._current_proc.poll()

        # Wait until the queue is empty or the timout occured
        timeout = 0
        while (cls._log.empty() is False) and (timeout < 30):
            time.sleep(0.1)
            timeout = timeout + 1

# ----------------------------------------------------------------------------------------------------------------------
# JSON RPC API Methods
# ----------------------------------------------------------------------------------------------------------------------

    def _get_version(cls, rpc_request):
        """
        Get the version of this project.
        """
        try:
            rpc_response = cls._get_rpc_response(rpc_request['id'])
            rpc_response['result'] = cls._version
            json_dump = json.dumps(rpc_response)
        except Exception as e:
            return cls._return_error(rpc_request['id'], 'Could not determine version. (%s)' % str(e))
        else:
            return json_dump

    def _poll(cls, rpc_request):
        """
        Return the log messages to the browser.
        """
        try:
            rpc_response = cls._get_rpc_response(rpc_request['id'])
            rpc_response['result'] = cls._log.get_message()
            json_dump = json.dumps(rpc_response)
        except Exception as e:
            # The message could not transfered to the browser. So re queue it!
            cls._log.requeue(rpc_response['result'])
        else:
            return json_dump

    def _get_file_list(cls, rpc_request):
        """
        Return the list of all files/folder to the browser.
        """
        try:
            code_folder = os.path.join(cls._CODE_ROOT, rpc_request['params'].strip('/\\'))

            rpc_response = cls._get_rpc_response(rpc_request['id'])
            rpc_response['result'] = os.listdir(code_folder)
            rpc_response['result'].sort()
            json_dump = json.dumps(rpc_response)
        except Exception as e:
            return cls._return_error(rpc_request['id'], 'Could not get a file list for the folder. (%s)' % str(e))
        else:
            return json_dump

    def _create_folder(cls, rpc_request):
        """
        Creates the folder on the device.
        """
        try:
            new_folder = os.path.join(cls._CODE_ROOT, rpc_request['params'].strip('/\\'))

            if not os.path.exists(new_folder):
                os.makedirs(new_folder)

            rpc_response = cls._get_rpc_response(rpc_request['id'])
            json_dump = json.dumps(rpc_response)
        except Exception as e:
            return cls._return_error(rpc_request['id'], 'Could not create the folder. (%s)' % str(e))
        else:
            return json_dump

    def _load_file(cls, rpc_request):
        """
        Return the content of the file back to the browser.
        """
        try:
            filename = os.path.join(cls._CODE_ROOT, rpc_request['params'].strip('/\\'))

            rpc_response = cls._get_rpc_response(rpc_request['id'])
            f = open(filename, 'r')
            rpc_response['result'] = f.read()
            f.close()
            json_dump = json.dumps(rpc_response)
        except Exception as e:
            return cls._return_error(rpc_request['id'], 'Could not get the content of the file. (%s)' % str(e))
        else:
            return json_dump

    def _save_file(cls, rpc_request):
        """
        Save the received content on the local disk.
        """
        # Store all incoming data into the file.
        try:
            rpc_response = cls._get_rpc_response(rpc_request['id'])
            filename = os.path.join(cls._CODE_ROOT, rpc_request['params']['filename'].strip('/\\'))
            with open(filename, 'w') as file:
                file.write(rpc_request['params']['data'])
            rpc_response['result'] = 'File %s saved.' % rpc_request['params']['filename']
            json_dump = json.dumps(rpc_response)
        except Exception as e:
            return cls._return_error(rpc_request['id'], 'Could not save the content of the file. (%s)' % str(e))
        else:
            return json_dump

    def _get_is_running(cls, rpc_request):
        """
        Get the current running state of the device
        """
        try:
            rpc_response = cls._get_rpc_response(rpc_request['id'])
            rpc_response['result'] = cls._is_running
            json_dump = json.dumps(rpc_response)
        except Exception as e:
            return cls._return_error(rpc_request['id'], 'Could not determine if there is a program running. (%s)' % str(e))
        else:
            return json_dump

    def _execute(cls, rpc_request):
        """
        Store the data on a local file and execute them.
        """
        if cls._is_running is False:
            try:
                cls._is_running = True

                filename = os.path.join(tempfile.gettempdir(), 'execute.py')

                with open(filename, 'w') as f:
                    f.write(cls._replace_hucon_requests(rpc_request['params']))
                f.close()

                # Wait for a while until the file is really closed before it can be executed.
                time.sleep(0.2)

                cls._run_file(filename)

            except Exception as e:
                cls._log.put('Error: %s' % str(e))

            cls._is_running = False
            cls._current_proc = None

        else:
            return cls._return_error(rpc_request['id'], 'There is a program running.', 503)

        rpc_response = cls._get_rpc_response(rpc_request['id'])
        return json.dumps(rpc_response)

    def _run(cls, rpc_request):
        """
        Run the file which is saved on the device
        """
        if cls._is_running is False:
            try:
                filename = os.path.join(cls._CODE_ROOT, rpc_request['params'].strip('/\\'))

                cls._is_running = True

                cls._run_file(filename)

            except Exception as e:
                cls._log.put('Error: %s' % str(e))

            cls._is_running = False
            cls._current_proc = None
        else:
            return cls._return_error(rpc_request['id'], 'There is a program running.', 503)

        rpc_response = cls._get_rpc_response(rpc_request['id'])
        return json.dumps(rpc_response)

    def _kill(cls, rpc_request):
        """
        Kill the current running process
        """
        if cls._current_proc:
            try:
                cls._current_proc.send_signal(signal.CTRL_C_EVENT)
            except Exception:
                pass
        if cls._current_proc:
            try:
                cls._current_proc.send_signal(signal.CTRL_BREAK_EVENT)
            except Exception:
                pass
        if cls._current_proc:
            try:
                cls._current_proc.send_signal(signal.SIGTERM)
            except Exception:
                pass
        time.sleep(0.1)

        rpc_response = cls._get_rpc_response(rpc_request['id'])
        rpc_response['result'] = 'Application stopped.'
        return json.dumps(rpc_response)

    def _get_possible_post_data(cls, rpc_request):
        """
        Return the json of available post data events.
        """
        try:
            rpc_response = cls._get_rpc_response(rpc_request['id'])
            with open(os.path.join(tempfile.gettempdir(), 'possible_events'), 'r') as file:
                rpc_response['result'] = json.load(file)
            file.close()
        except Exception as e:
            return cls._return_error(rpc_request['id'], 'Could not retrieve the list of possible events. (%s)' % str(e), 500)
        else:
            return json.dumps(rpc_response)

    def _event(cls, rpc_request):
        """
        Fire the event on the device.
        """
        if cls._is_running:

            try:
                if os.name == 'nt':
                    return cls._return_error(rpc_request['id'], 'Could not set the event on windows machines.', 500)
                else:
                    os.kill(cls._current_proc.pid, signal.SIGRTMIN + rpc_request['params'])
            except Exception as e:
                return cls._return_error(rpc_request['id'], 'Could not set the event. (%s)' % str(e), 503)
        else:
            return cls._return_error(rpc_request['id'], 'There is no program running.', 503)

        rpc_response = cls._get_rpc_response(rpc_request['id'])
        return json.dumps(rpc_response)

    def _check_update(cls, rpc_request):
        """
        Check if there is an update available.
        """
        try:
            proc = subprocess.Popen(['sh', cls._UPDATE_FILE, '-c'], bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            while True:
                output = proc.stdout.readline()
                if output == '' and proc.poll() is not None:
                    break
                if output:
                    cls._log.put(output.strip())
            proc.poll()

            rpc_response = cls._get_rpc_response(rpc_request['id'])
            if proc.returncode == 1:
                rpc_response['result'] = True
            else:
                rpc_response['result'] = False
        except Exception as e:
            return cls._return_error(rpc_request['id'], 'Could not get a version. (%s)' % str(e), 500)
        else:
            return json.dumps(rpc_response)

    def _update(cls, rpc_request):
        """
        Update all files from the project.
        """
        try:
            # Update the system first.
            cls._log.put('The system will be updated and needs a few seconds.\n')
            proc = subprocess.Popen(['sh', cls._UPDATE_FILE, '-u'], bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            while True:
                output = proc.stdout.readline()
                if output == '' and proc.poll() is not None:
                    break
                if output:
                    cls._log.put(output.strip())
            proc.poll()

            # Do a restart.
            proc = subprocess.Popen(['sh', cls._UPDATE_FILE, '-r'], bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            while True:
                output = proc.stdout.readline()
                if output == '' and proc.poll() is not None:
                    break
                if output:
                    cls._log.put(output.strip())
            proc.poll()

        except Exception as e:
            return cls._return_error(rpc_request['id'], 'Could not perform an update. (%s)' % str(e), 500)
        else:
            # This should never be reached in term of the system reboot
            return cls._return_error(rpc_request['id'], 'Could not perform an update.', 500)

    def _shutdown(cls, rpc_request):
        """
        Shutdown the robot.
        """
        try:
            cls._log.put('The system will be shutdown.\n')
            proc = subprocess.Popen(['sh', cls._UPDATE_FILE, '-s'], bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            while True:
                output = proc.stdout.readline()
                if output == '' and proc.poll() is not None:
                    break
                if output:
                    cls._log.put(output.strip())
            proc.poll()
        except Exception as e:
            return cls._return_error(rpc_request['id'], 'Could not shutdown the system. (%s)' % str(e), 500)
        else:
            # This should never be reached in term of the system shutdown.
            return cls._return_error(rpc_request['id'], 'Could not shutdown the system.', 500)

    def _save_password(cls, rpc_request):
        """
        Save the new password key only when the oldkey is the same with the current.
        """
        try:
            rpc_response = cls._get_rpc_response(rpc_request['id'])

            remove = False
            oldKey = ''
            newKey = ''

            if 'remove' in rpc_request['params'].keys():
                remove = rpc_request['params']['remove']
            if 'oldKey' in rpc_request['params'].keys():
                oldKey = rpc_request['params']['oldKey']
            if 'newKey' in rpc_request['params'].keys():
                newKey = rpc_request['params']['newKey']

            # Remove the password
            if (oldKey == cls._authorization_key and remove):
                cls._authorization_key = ''
                with open(cls._PASSWORD_FILE, 'w') as file:
                    file.write(cls._authorization_key)
                rpc_response['result'] += 'Password removed.'

            # Store the password.
            elif ((cls._authorization_key == '' or oldKey == cls._authorization_key) and newKey != ''):
                cls._authorization_key = newKey
                with open(cls._PASSWORD_FILE, 'w') as file:
                    file.write(cls._authorization_key)
                rpc_response['result'] += 'New password written.'

            else:
                if remove:
                    rpc_response['result'] += 'Error: Could not remove the password.\n'
                else:
                    rpc_response['result'] += 'Error: Could not store the password.\n'
                rpc_response['result'] += 'The current Password is not correct!'
        except Exception as e:
            return cls._return_error(rpc_request['id'], 'Could not save the password. (%s)' % str(e), 500)
        else:
            return json.dumps(rpc_response)
