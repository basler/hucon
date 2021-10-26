#!/usr/bin/python
""" HuConJsonRpc.py - The JSON RPC class to handle all incoming requests and return a well formed response.

    Copyright (C) 2019 Basler AG
    All rights reserved.

    This software may be modified and distributed under the terms
    of the BSD license.  See the LICENSE file for details.
"""

import threading
from datetime import datetime, timedelta
import os
from os.path import expanduser
import json
import subprocess
import time
import tempfile
import signal
import socket
import typing

from HuConLogMessage import HuConLogMessage
import HuConMAC
from PyUci import WirelessHelper


class HuConJsonRpc:
    """ This class implements the functionality of the which will the server provide.
    """

    # Name for the server to identification
    _SERVER_NAME = 'HuConRobot'

    # Folder where all custom code files are stored.
    _CODE_ROOT = os.path.join(expanduser("~"), 'hucon', 'code')

    # Folder where all custom code files are stored.
    _EXAMPLE_ROOT = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), 'code')

    # Path to the version file.
    _VERSION_FILE = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), '__version__')

    # Path to the update file.
    _UPDATE_FILE = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), 'update.sh')

    # Define the port on which the server should listening on.
    _LISTENING_PORT = 8080

    # Current version of the server.
    _version = 'beta'

    # Store the current running state
    _is_running = False

    # Store the current process to communicate with a running process
    _current_proc = None

    # Queue for all log messages
    _log = HuConLogMessage()

    # Wireless Helper object for handle wireless settings
    _wifi = WirelessHelper(_log)

    _message_buffer_for_input: typing.List[str] = []

    def __init__(self):
        """ Initialize the RPC server.
        """
        if os.path.exists(self._VERSION_FILE):
            with open(self._VERSION_FILE, 'r') as file:
                self._version = file.readline()

        if not os.path.exists(self._CODE_ROOT):
            os.makedirs(self._CODE_ROOT)

        print('%s v. %s' % (self._SERVER_NAME, self._version))
        print('Custom code path: \'%s\'' % self._CODE_ROOT)
        print('Example code path: \'%s\'' % self._EXAMPLE_ROOT)

    def handle_control(self, rpc_request):
        """ Handle the JSON RPC request.
        """
        if rpc_request['method'] == 'get_version':
            return self._get_version(rpc_request)
        elif rpc_request['method'] == 'get_robot_info':
            return self._get_robot_info(rpc_request)
        elif rpc_request['method'] == 'poll':
            return self._poll(rpc_request)
        elif rpc_request['method'] == 'get_file_list':
            return self._get_file_list(rpc_request)
        elif rpc_request['method'] == 'create_folder':
            return self._create_folder(rpc_request)
        elif rpc_request['method'] == 'load_file':
            return self._load_file(rpc_request)
        elif rpc_request['method'] == 'save_file':
            return self._save_file(rpc_request)
        elif rpc_request['method'] == 'is_running':
            return self._get_is_running(rpc_request)
        elif rpc_request['method'] == 'execute':
            return self._execute(rpc_request)
        elif rpc_request['method'] == 'run':
            return self._run(rpc_request)
        elif rpc_request['method'] == 'push_input':
            return self._receive_input(rpc_request)
        elif rpc_request['method'] == 'kill':
            return self._kill(rpc_request)
        elif rpc_request['method'] == 'get_possible_post_data':
            return self._get_possible_post_data(rpc_request)
        elif rpc_request['method'] == 'event':
            return self._event(rpc_request)
        elif rpc_request['method'] == 'check_update':
            return self._check_update(rpc_request)
        elif rpc_request['method'] == 'update':
            return self._update(rpc_request)
        elif rpc_request['method'] == 'shutdown':
            return self._shutdown(rpc_request)
        elif rpc_request['method'] == 'get_saved_wifi_networks':
            return self._get_saved_wifi_networks(rpc_request)
        elif rpc_request['method'] == 'get_wifi_found':
            return self._get_wifi_found(rpc_request)
        elif rpc_request['method'] == 'add_wifi':
            return self._add_wifi(rpc_request)
        elif rpc_request['method'] == 'move_wifi_up':
            return self._move_wifi_up(rpc_request)
        elif rpc_request['method'] == 'move_wifi_down':
            return self._move_wifi_down(rpc_request)
        elif rpc_request['method'] == 'remove_wifi':
            return self._remove_wifi(rpc_request)
        elif rpc_request['method'] == 'connect_wifi':
            return self._connect_wifi(rpc_request)
        elif rpc_request['method'] == 'enable_sta_wifi':
            return self._enable_sta_wifi(rpc_request)
        elif rpc_request['method'] == 'disable_sta_wifi':
            return self._disable_sta_wifi(rpc_request)
        elif rpc_request['method'] == 'get_ap_settings':
            return self._get_ap_settings(rpc_request)
        elif rpc_request['method'] == 'enable_ap_wifi':
            return self._enable_ap_wifi(rpc_request)
        elif rpc_request['method'] == 'disable_ap_wifi':
            return self._disable_ap_wifi(rpc_request)
        elif rpc_request['method'] == 'set_ap_settings':
            return self._set_ap_settings(rpc_request)
        else:
            return self._return_error(rpc_request['id'], 'Command not known.')

    @staticmethod
    def _get_rpc_response(rpc_id):
        """ Return a json rpc response message.
        """
        rpc_response = {
            'jsonrpc': '2.0',
            'id': rpc_id}

        return rpc_response

    @staticmethod
    def _return_error(rpc_id, error, status_code=400):
        """ Return an well formed error.
        """
        rpc_response = {'jsonrpc': '2.0',
                        'error': error,
                        'id': rpc_id}

        return json.dumps(rpc_response), status_code

    @staticmethod
    def _replace_hucon_requests(message):
        """ Print an answer from HuCon whenever the the message 'Hello HuCon!' is found.
        """
        search_string = 'print(\'Hello HuCon!\')'
        replace_string = 'print(\'Hello HuCon!\\n\\nHello human!\\nI am a Hu[man] Con[trolled] robot.\\n\')'
        if search_string in message:
            message = message.replace(search_string, replace_string)
        return message

    _file_runner = None

    def _run_file(self, filename):
        """ This function takes care about starting and stopping the thread for running user python scripts
        """
        if self._file_runner is not None:
            self._kill_process()
            self._file_runner.join()
            self._file_runner = None

        self._file_runner = threading.Thread(target=self._run_file_worker, args=(filename,))
        self._file_runner.start()

    def _run_file_worker(self, filename):
        """ Threaded worker function for running the user scripts.
        It catches all outputs and provides input functions for the process
        """
        error_detected = False
        # I am feeling very guilty - but it seems to be a very effective solution
        ugly_hack = '#!/usr/bin/env python\n' \
                    '# -*- coding: utf-8 -*-\n' \
                    'def input(enquiry):\n' \
                    '    print(enquiry + u"\u2504")\n' \
                    '    return globals()[\'__builtins__\'].input(\'\')\n' \
                    'exec(open(r\'' + filename + '\').read())'

        self._current_proc = subprocess.Popen(['python3', '-X utf8', '-c', ugly_hack],
                                              bufsize=1,
                                              stdin=subprocess.PIPE,
                                              stdout=subprocess.PIPE,
                                              stderr=subprocess.STDOUT,
                                              encoding='utf-8',
                                              universal_newlines=True)
        self._is_running = True
        while True:
            output = self._current_proc.stdout.readline()
            if output == '' and self._current_proc.poll() is not None:
                break
            if output:
                # this is an input inquiry (https://en.wikipedia.org/wiki/Unicode_control_characters 0x2405 is ENQ)
                if output.endswith("\u2504\n"):
                    timeout_time = datetime.now() + timedelta(minutes=5)

                    line = output.replace("\u2504\n", "")
                    self._log.put_input(line)

                    while len(self._message_buffer_for_input) == 0:
                        if datetime.now() >= timeout_time:
                            self._message_buffer_for_input.append("Timeout!\n")
                            break

                    # I know that this is not the preferred method of communication with
                    # sub processes, but communicate does not provide on demand communication as stdin/stdout does
                    # but just collects all inputs and writes all outputs at the end
                    self._current_proc.stdin.write(self._message_buffer_for_input.pop() + '\n')
                else:
                    file_error_string = 'File "' + filename + '", l'
                    if output.find(file_error_string) != -1:
                        error_detected = True
                    # Replace the file error like 'File "/tmp/execute.py", line x, in'
                    line = output.replace(file_error_string, '[red]Error: L')
                    self._log.put_output(line)

        self._current_proc.poll()
        self._is_running = False
        if not error_detected:
            self._log.put_output('')
            self._log.put_output('[green]Done ...')

        # Wait until the queue is empty or the timout occurred
        timeout = 0
        while (self._log.empty() is False) and (timeout < 30):
            time.sleep(0.1)
            timeout += 1

    # ------------------------------------------------------------------------------------------------------------------
    # JSON RPC API Methods
    # ------------------------------------------------------------------------------------------------------------------

    def _get_version(self, rpc_request):
        """ Get the version of this project.
        """
        try:
            rpc_response = self._get_rpc_response(rpc_request['id'])
            rpc_response['result'] = self._version
            json_dump = json.dumps(rpc_response)
        except Exception as ex:
            return self._return_error(rpc_request['id'], 'Could not determine version. (%s)' % str(ex))
        else:
            return json_dump

    def _get_robot_info(self, rpc_request):
        """ Get information about the individual robot
        """
        try:
            hucon_name = socket.gethostname()
            mac_address = HuConMAC.get_mac_address()
            rpc_response = self._get_rpc_response(rpc_request['id'])
            rpc_response['result'] = {
                'name': hucon_name,
                'mac_address': mac_address
            }
            json_dump = json.dumps(rpc_response)
        except Exception as ex:
            return self._return_error(
                rpc_request['id'],
                'Could not get robot info. (%s)' % str(ex)
            )
        return json_dump

    def _poll(self, rpc_request):
        """ Return the log messages to the browser.
        """
        messages = self._log.get_messages()
        # noinspection PyBroadException
        try:
            rpc_response = self._get_rpc_response(rpc_request['id'])
            rpc_response['messages'] = messages
            json_dump = json.dumps(rpc_response, default=lambda x: x.serialize())
        except Exception:
            # The message could not transferred to the browser. So re queue it!
            self._log.requeue(messages)
        else:
            return json_dump

    def _get_file_list(self, rpc_request):
        """ Return the list of all files/folder to the browser.
        """
        try:
            code_folder = os.path.join(self._CODE_ROOT, rpc_request['params'].strip('/\\'))
            example_folder = os.path.join(self._EXAMPLE_ROOT, rpc_request['params'].strip('/\\'))

            files_usercode = []
            rpc_response = self._get_rpc_response(rpc_request['id'])
            if os.path.exists(code_folder):
                files_usercode = os.listdir(code_folder)
                files_usercode.sort()
            files_examples = os.listdir(example_folder)
            files_examples.sort()
            rpc_response['result'] = files_examples + files_usercode
            rpc_response['result'].sort()
            json_dump = json.dumps(rpc_response)

        except Exception as e:
            return self._return_error(rpc_request['id'], 'Could not get a file list for the folder. (%s)' % str(e))
        else:
            return json_dump

    def _create_folder(self, rpc_request):
        """ Creates the folder on the device.
        """
        try:
            new_folder = os.path.join(self._CODE_ROOT, rpc_request['params'].strip('/\\'))

            if not os.path.exists(new_folder):
                os.makedirs(new_folder)

            rpc_response = self._get_rpc_response(rpc_request['id'])
            json_dump = json.dumps(rpc_response)
        except Exception as ex:
            return self._return_error(rpc_request['id'], 'Could not create the folder. (%s)' % str(ex))
        else:
            return json_dump

    def _load_file(self, rpc_request):
        """ Return the content of the file back to the browser.
        """
        try:
            # TODO: Extract file base path (examples/user code) from rpc call and remove this hack
            filename = os.path.join(self._CODE_ROOT, rpc_request['params'].strip('/\\'))
            if not os.path.exists(filename):
                filename = os.path.join(self._EXAMPLE_ROOT, rpc_request['params'].strip('/\\'))

            rpc_response = self._get_rpc_response(rpc_request['id'])
            f = open(filename, 'r')
            rpc_response['result'] = f.read()
            f.close()
            json_dump = json.dumps(rpc_response)
        except Exception as ex:
            return self._return_error(rpc_request['id'], 'Could not get the content of the file. (%s)' % str(ex))
        else:
            return json_dump

    def _save_file(self, rpc_request):
        """ Save the received content on the local disk.
        """
        # Store all incoming data into the file.
        try:
            rpc_response = self._get_rpc_response(rpc_request['id'])
            filename = os.path.join(self._CODE_ROOT, rpc_request['params']['filename'].strip('/\\'))
            with open(filename, 'w') as file:
                file.writelines(rpc_request['params']['data'])
            rpc_response['result'] = 'File %s saved.' % rpc_request['params']['filename']
            json_dump = json.dumps(rpc_response)
        except Exception as ex:
            return self._return_error(rpc_request['id'], 'Could not save the content of the file. (%s)' % str(ex))
        else:
            return json_dump

    def _get_is_running(self, rpc_request):
        """ Get the current running state of the device
        """
        try:
            rpc_response = self._get_rpc_response(rpc_request['id'])
            rpc_response['result'] = self._is_running
            json_dump = json.dumps(rpc_response)
        except Exception as ex:
            return self._return_error(rpc_request['id'],
                                      'Could not determine if there is a program running. (%s)' % str(ex))
        else:
            return json_dump

    def _execute(self, rpc_request):
        """ Store the data on a local file and execute them.
        """
        if self._is_running is False:
            try:
                self._is_running = True

                filename = os.path.join(tempfile.gettempdir(), 'execute.py')

                with open(filename, 'wt') as file:
                    file.writelines(self._replace_hucon_requests(rpc_request['params']))
                file.close()

                # Wait for a while until the file is really closed before it can be executed.
                time.sleep(0.2)

                self._run_file(filename)

            except Exception as ex:
                self._log.put_output('Error: "%s" Trace: "%s"' % str(ex) % str(ex.__traceback__))

            self._is_running = False
            self._current_proc = None

        else:
            return self._return_error(rpc_request['id'], 'There is a program running.', 503)

        rpc_response = self._get_rpc_response(rpc_request['id'])
        return json.dumps(rpc_response)

    def _run(self, rpc_request):
        """ Run the file which is saved on the device
        """
        if self._is_running is False:
            try:
                filename = os.path.join(self._CODE_ROOT, rpc_request['params'].strip('/\\'))

                self._is_running = True

                self._run_file(filename)

            except Exception as ex:
                self._log.put_output('Error: "%s" Trace: "%s"' % str(ex) % str(ex.__traceback__))

            self._is_running = False
            self._current_proc = None
        else:
            return self._return_error(rpc_request['id'], 'There is a program running.', 503)

        rpc_response = self._get_rpc_response(rpc_request['id'])
        return json.dumps(rpc_response)

    def _receive_input(self, rpc_request):
        """ Receives input from the client
        """
        try:
            self._message_buffer_for_input.append(rpc_request['message'])
        except Exception as ex:
            return self._return_error(rpc_request['id'], 'Could not forward the input. (%s)' % str(ex))

        rpc_response = self._get_rpc_response(rpc_request['id'])
        return json.dumps(rpc_response)

    def _kill(self, rpc_request):
        """ Kill the current running process
        """
        self._kill_process()

        rpc_response = self._get_rpc_response(rpc_request['id'])
        rpc_response['result'] = 'Application stopped.'
        return json.dumps(rpc_response)

    def _kill_process(self):
        signal_list = [signal.CTRL_C_EVENT,
                       signal.CTRL_C_EVENT,
                       signal.CTRL_BREAK_EVENT,
                       signal.SIGTERM,
                       signal.SIGABRT]
        for currentSignal in signal_list:
            if self._current_proc:
                # noinspection PyBroadException
                try:
                    self._current_proc.send_signal(currentSignal)
                    self._current_proc.wait(0.1)
                except Exception:
                    pass

        if self._current_proc:
            # noinspection PyBroadException
            try:
                self._current_proc.kill()
                self._current_proc.wait(0.1)
            except Exception:
                pass

    def _get_possible_post_data(self, rpc_request):
        """ Return the json of available post data events.
        """
        try:
            rpc_response = self._get_rpc_response(rpc_request['id'])
            with open(os.path.join(tempfile.gettempdir(), 'possible_events'), 'r') as file:
                rpc_response['result'] = json.load(file)
            file.close()
        except Exception as ex:
            return self._return_error(rpc_request['id'],
                                      'Could not retrieve the list of possible events. (%s)' % str(ex), 500)
        else:
            return json.dumps(rpc_response)

    def _event(self, rpc_request):
        """ Fire the event on the device.
        """
        if self._is_running:

            try:
                if os.name == 'nt':
                    return self._return_error(rpc_request['id'], 'Could not set the event on windows machines.', 500)

                os.kill(self._current_proc.pid, signal.SIGRTMIN + rpc_request['params'])
            except Exception as ex:
                return self._return_error(rpc_request['id'], 'Could not set the event. (%s)' % str(ex), 503)
        else:
            return self._return_error(rpc_request['id'], 'There is no program running.', 503)

        rpc_response = self._get_rpc_response(rpc_request['id'])
        return json.dumps(rpc_response)

    def _check_update(self, rpc_request):
        """ Check if there is an update available.
        """
        try:
            proc = subprocess.Popen(['bash', self._UPDATE_FILE, '-c'], bufsize=0, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, encoding='utf-8')

            while True:
                output = proc.stdout.readline()
                if output == '' and proc.poll() is not None:
                    break
                if output:
                    self._log.put_output(output.strip())
            proc.poll()

            rpc_response = self._get_rpc_response(rpc_request['id'])
            if proc.returncode == 1:
                rpc_response['result'] = True
            else:
                rpc_response['result'] = False
        except Exception as ex:
            return self._return_error(rpc_request['id'], 'Could not get a version. (%s)' % str(ex), 500)
        else:
            return json.dumps(rpc_response)

    def _update(self, rpc_request):
        """ Update all files from the project.
        """
        try:
            # Update the system first.
            self._log.put_output('The system will be updated and needs a few seconds.\n')
            proc = subprocess.Popen(['bash', self._UPDATE_FILE, '-u'], bufsize=0, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, encoding='utf-8')

            while True:
                output = proc.stdout.readline()
                if output == '' and proc.poll() is not None:
                    break
                if output:
                    self._log.put_output(output.strip())
            proc.poll()

            # Do a restart.
            proc = subprocess.Popen(['bash', self._UPDATE_FILE, '-r'], bufsize=0, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, encoding='utf-8')

            while True:
                output = proc.stdout.readline()
                if output == '' and proc.poll() is not None:
                    break
                if output:
                    self._log.put_output(output.strip())
            proc.poll()

        except Exception as ex:
            return self._return_error(rpc_request['id'], 'Could not perform an update. (%s)' % str(ex), 500)
        else:
            # This should never be reached in term of the system reboot
            return self._return_error(rpc_request['id'], 'Could not perform an update.', 500)

    def _shutdown(self, rpc_request):
        """ Shutdown the robot.
        """
        try:
            self._log.put_output('The system will be shutdown.\n')
            proc = subprocess.Popen(['bash', self._UPDATE_FILE, '-s'], bufsize=0, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, encoding='utf-8')

            while True:
                output = proc.stdout.readline()
                if output == '' and proc.poll() is not None:
                    break
                if output:
                    self._log.put_output(output.strip())
            proc.poll()
        except Exception as ex:
            return self._return_error(rpc_request['id'], 'Could not shutdown the system. (%s)' % str(ex), 500)
        else:
            # This should never be reached in term of the system shutdown.
            return self._return_error(rpc_request['id'], 'Could not shutdown the system.', 500)

    # Wireless settings section
    def _get_wifi_found(self, rpc_request):
        """
        Scan for Wi-Fi networks and returns searched as rpc_response
        :param rpc_request:
        :return: rpc_response
        """
        try:
            self._log.put_output('Search for WiFi.\n')
            device = json.dumps({"device": "ra0"})
            wifi_scan_output = json.loads(
                subprocess.check_output(['ubus', 'call', 'onion', 'wifi-scan', device]).decode())
            rpc_response = self._get_rpc_response(rpc_request['id'])
            rpc_response['result'] = wifi_scan_output['results']
        except Exception as ex:
            return self._return_error(rpc_request['id'], 'Could not search for WiFi. (%s)' % str(ex), 500)
        else:
            return json.dumps(rpc_response)

    def _get_saved_wifi_networks(self, rpc_request):
        """
        Returns saved networks as rpc_response
        :param rpc_request:
        :return: rpc_response
        """
        try:
            self._log.put_output('Read WiFi Settings.\n')
            wifi_disabled = self._wifi.is_wifi_disabled()
            wifi_output_list = self._wifi.get_saved_wifi_networks()
            rpc_response = self._get_rpc_response(rpc_request['id'])
            result = {"wifi_list": wifi_output_list, "wifi_disabled": wifi_disabled}
            rpc_response['result'] = result
        except Exception as ex:
            return self._return_error(rpc_request['id'], 'Could not read WiFi settings. (%s)' % str(ex), 500)
        else:
            return json.dumps(rpc_response)

    def _add_wifi(self, rpc_request):
        """
        Add new Wi-Fi network to configuration
        :param rpc_request:
        :return: rpc_response
        """
        try:
            self._log.put_output('Add new WiFi.\n')
            self._wifi.add_wifi(ssid=rpc_request['params'][0],
                                key=rpc_request['params'][1],
                                encryption=rpc_request['params'][2])
        except Exception as ex:
            return self._return_error(rpc_request['id'], 'Could not add new WiFi network. (%s)' % str(ex), 500)
        else:
            rpc_response = self._get_rpc_response(rpc_request['id'])
            return json.dumps(rpc_response)

    def _move_wifi_up(self, rpc_request):
        """
        Move Wi-Fi network up in priority list
        :param rpc_request:
        :return: rpc_response
        """
        try:
            self._log.put_output('Move WiFi up.\n')
            self._wifi.move_wifi_up(rpc_request['params'][0])
        except Exception as ex:
            return self._return_error(rpc_request['id'], 'Could not move WiFi network up. (%s)' % str(ex), 500)
        else:
            rpc_response = self._get_rpc_response(rpc_request['id'])
            return json.dumps(rpc_response)

    def _move_wifi_down(self, rpc_request):
        """
        Move Wi-Fi network up in priority list
        :param rpc_request:
        :return: rpc_response
        """
        try:
            self._log.put_output('Move WiFi down.\n')
            self._wifi.move_wifi_down(rpc_request['params'][0])
        except Exception as ex:
            return self._return_error(rpc_request['id'], 'Could not move WiFi network down. (%s)' % str(ex), 500)
        else:
            rpc_response = self._get_rpc_response(rpc_request['id'])
            return json.dumps(rpc_response)

    def _remove_wifi(self, rpc_request):
        """
        Remove Wi-Fi network from settings
        :param rpc_request:
        :return:
        """
        try:
            self._log.put_output('Remove WiFi down.\n')
            self._wifi.remove_wifi(rpc_request['params'][0])
        except Exception as ex:
            return self._return_error(rpc_request['id'], 'Could not remove WiFi network. (%s)' % str(ex), 500)
        else:
            rpc_response = self._get_rpc_response(rpc_request['id'])
            return json.dumps(rpc_response)

    def _connect_wifi(self, rpc_request):
        """
        Connect selected Wi-Fi network
        :param rpc_request:
        :return: rpc_response
        """
        try:
            self._log.put_output('Connect WiFi.\n')
            self._wifi.connect_wifi(rpc_request['params'][0])
        except Exception as ex:
            return self._return_error(rpc_request['id'], 'Could not remove WiFi network. (%s)' % str(ex), 500)
        else:
            rpc_response = self._get_rpc_response(rpc_request['id'])
            return json.dumps(rpc_response)

    def _enable_sta_wifi(self, rpc_request):
        """
        Enable STA radio
        :param rpc_request:
        :return: rpc_response
        """
        try:
            self._log.put_output('Enable WiFi.\n')
            self._wifi.enable_sta_wifi()
        except Exception as ex:
            return self._return_error(rpc_request['id'], 'Could not enable WiFi. (%s)' % str(ex), 500)
        else:
            rpc_response = self._get_rpc_response(rpc_request['id'])
            return json.dumps(rpc_response)

    def _disable_sta_wifi(self, rpc_request):
        """
        Disable STA radio
        :param rpc_request:
        :return: rpc_response
        """
        try:
            self._log.put_output('Disable WiFi.\n')
            self._wifi.disable_sta_wifi()
        except Exception as ex:
            return self._return_error(rpc_request['id'], 'Could not disable WiFi. (%s)' % str(ex), 500)
        else:
            rpc_response = self._get_rpc_response(rpc_request['id'])
            return json.dumps(rpc_response)

    def _get_ap_settings(self, rpc_request):
        """
        Returns AP Settings in rpc_response
        :param rpc_request:
        :return: rpc_response
        """
        try:
            self._log.put_output('Get AP Settings.\n')
            rpc_response = self._get_rpc_response(rpc_request['id'])
            rpc_response['result'] = self._wifi.get_ap_settings()
        except Exception as ex:
            return self._return_error(rpc_request['id'], 'Could not get AP settings. (%s)' % str(ex), 500)
        else:
            return json.dumps(rpc_response)

    def _enable_ap_wifi(self, rpc_request):
        """
        Enable AP radio
        :param rpc_request:
        :return: rpc_response
        """
        try:
            self._log.put_output('Enable AP WiFi.\n')
            self._wifi.enable_ap_wifi()
        except Exception as ex:
            return self._return_error(rpc_request['id'], 'Could not enable AP WiFi. (%s)' % str(ex), 500)
        else:
            rpc_response = self._get_rpc_response(rpc_request['id'])
            return json.dumps(rpc_response)

    def _disable_ap_wifi(self, rpc_request):
        """
        Disable AP radio
        :param rpc_request:
        :return: rpc_response
        """
        try:
            self._log.put_output('Disable AP WiFi.\n')
            self._wifi.disable_ap_wifi()
        except Exception as ex:
            return self._return_error(rpc_request['id'], 'Could not disable WiFi. (%s)' % str(ex), 500)
        else:
            rpc_response = self._get_rpc_response(rpc_request['id'])
            return json.dumps(rpc_response)

    def _set_ap_settings(self, rpc_request):
        """
        Set AP WiFi settings
        :param rpc_request:
        :return: rpc_response
        """
        try:
            self._log.put_output('Set AP WiFi Settings.\n')
            self._wifi.set_ap_settings(ssid=rpc_request['params'][0],
                                       key=rpc_request['params'][1],
                                       encryption=rpc_request['params'][2],
                                       ip=rpc_request['params'][3])
        except Exception as ex:
            return self._return_error(rpc_request['id'], 'Could not configure AP WiFi settings. (%s)' % str(ex), 500)
        else:
            rpc_response = self._get_rpc_response(rpc_request['id'])
            return json.dumps(rpc_response)
