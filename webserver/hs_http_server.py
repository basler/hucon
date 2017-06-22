#!/usr/bin/env python3
import gc
import time

# Call the garbage collector.
gc.collect()

try:
    # Import different packages on the micro python.
    import uos as os
    import usocket as socket
    import ujson as json
except:
    import os
    import socket
    import json

# Call the garbage collector.
gc.collect()

from hs_term import HSTerm
import hs_network

# Call the garbage collector.
gc.collect()

class HSHttpServer:
    """
    This implementation is a simple HTTP Server which works on Windows, Linux and macOS with different Browser.
    It is written to work with the micro python an a ESP8266 device.
    """

    # Name of this server for the HTTP header.
    _SERVER_NAME = 'HackerSchool Custom Webserver'

    # Folder where all files for the server are stored.
    _DOCUMENT_ROOT = os.getcwd() + '/www'

    # Folder where all custom code files are stored.
    _CODE_ROOT = os.getcwd() + '/code'

    # Define the port on which the server should listening on.
    _LISTENING_PORT = 80

    # Private server socket to listen for new connections.
    _server_socket = None

    # Private variable to store its own ip address.
    _own_ip = ''

    # Private key for the authorization to the key.
    _authorization_key = ''

    # Maximal size of data nibbles which can be directly handled.
    # Must be a pow of 2!
    _MAX_BUFFER_SIZE = 256

    # Define the HTML MIME Types which are possible to send with this webserver implementation.
    # There are more types defined here: https://wiki.selfhtml.org/wiki/Referenz:MIME-Typen
    _MIME_TYPE = {
        # ext  : MIME-Type,
        'js': 'application/javascript',
        'json': 'application/json',
        'woff': 'application/font-woff',
        'woff2': 'application/font-woff2',
        'xml': 'application/xml ',

        'gif': 'image/gif',
        'jpeg': 'image/jpeg',
        'jpg': 'image/jpeg',
        'png': 'image/png',
        'ico': 'image/x-icon',

        'css': 'text/css',
        'htm': 'text/html',
        'html': 'text/html',
        'txt': 'text/plain',
    }

    # Definition of all supported status codes.
    _HTML_STATUS = {
        200: '200 OK',
        401: '401 Unauthorized',
        403: '403 Forbidden',
        404: '404 Not Found',
        500: '500 Internal Server Error',
    }

    # Mark to search for the end of the header end during the receive of the bytestream.
    _HTTP_HEADER_END_MARK_BYTE = b'\r\n\r\n'

    def __init__(self, key: str):
        """
        Create a socket to get its own ip address.
        """
        self._authorization_key = key
        try:
            self._own_ip = hs_network.get_ip_address()
            return
        except Exception as e:
            self._own_ip = ''
            HSTerm.term('Could not read my own ip address. :(')

    def start(self):
        """
        Get a socket object and start the listening on the defined port.
        If the _use_threads_ is True, every new connection will be handled within a new thread.
        """
        try:
            # Create the socket.
            self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            HSTerm.term('Socket created')

            # Binding to all interfaces - server will be accessible to other hosts!
            address_info = socket.getaddrinfo('0.0.0.0', HSHttpServer._LISTENING_PORT)
            addr = address_info[0][-1]

            self._server_socket.bind(addr)
            HSTerm.term('Socket bind complete.')
        except Exception as e:
            HSTerm.term('Create socket error: ' + str(e))
            self._server_socket.close()
            self._server_socket = None
            return

        # Start the socket listening.
        self._server_socket.listen(5)
        HSTerm.term('Listening, connect your browser to http://' + self._own_ip + ':' + str(HSHttpServer._LISTENING_PORT))

        # Listening in an endless loop for new connections.
        while True:
            addr = None
            clientsocket = None
            try:
                gc.collect()
                clientsocket, addr = self._server_socket.accept()
                ip, port = str(addr[0]), str(addr[1])
                gc.collect()

                HSTerm.term('\nConnection accpted from ' + ip + ':' + port)
                clientsocket.settimeout(5.0)

                try:
                    gc.collect()
                    self.handle_connection(clientsocket, ip, port)
                except Exception as e:
                    HSTerm.term('Connection error: %s' % str(e))
                finally:
                    clientsocket.close()
                    gc.collect()
                    try:
                        HSTerm.term('Free memory: %d' % gc.mem_free())
                    except:
                        pass

            except KeyboardInterrupt:
                HSTerm.term('\nClose socket.')
                if clientsocket:
                    clientsocket.close()
                break
            except Exception as e:
                HSTerm.term('Main loop error: %s' % str(e))

        # Close the socket listening after the user want to stop it.
        self._server_socket.close()

    def handle_connection(self, clientsocket: socket.socket, ip: str, port: str):
        """
        Handle every connection within this function.
        This function can be called within a new thread or within the main thread.
        """
        header = ''
        data = ''
        content_length = 0

        #  receive the first package.
        receive_buffer = clientsocket.recv(HSHttpServer._MAX_BUFFER_SIZE)

        # Try to find the end of the HTTP header.
        while receive_buffer.find(HSHttpServer._HTTP_HEADER_END_MARK_BYTE) == -1:
            receive_buffer += clientsocket.recv(HSHttpServer._MAX_BUFFER_SIZE)

        #  Split the header/data from the receive buffer.
        (header, data) = receive_buffer.split(HSHttpServer._HTTP_HEADER_END_MARK_BYTE)

        # Decode the byet stream into a utf-8 string
        header = header.decode('utf-8')
        header_lines = header.split('\r\n')

        # Parse some parameter from the header.
        accept_gzip = False
        authorized = False
        content_length = None
        for line in header_lines:
            if 'Accept-Encoding' in line:
                if 'gzip' in line:
                    accept_gzip = True
            if 'Authorization' in line:
                if self._authorization_key in line:
                    authorized = True
            if 'Content-Length' in line:
                content_length = int(line[line.find(':') + 1:])

        # Stop if the user has no authorization to get any page.
        if not authorized:
            HSTerm.term('no authorisation')
            filename = HSHttpServer._DOCUMENT_ROOT + '/401.html'
            header = HSHttpServer.get_html_header(401, filename)
            HSHttpServer.send_response(clientsocket, header, filename)
            return

        # The first line is the one we need to get the information about the request.
        header_line = header_lines[0]
        header_line = header_line.split()

        # Break down the request line into components
        (method, path, version) = header_line
        path = path.strip('/')

        HSTerm.term('Method: ' + method)
        HSTerm.term('Path: ' + path)

        # The POST request can be a file access or a special command. Handle the file access a little bit different
        # because the file can be bigger than the free space in ram. For the file access it is needed to get the
        # parameter before the data is received to store the data directly.
        # The GET parameter is a direct read access.
        if method == 'POST':

            # Clear the exec file.
            HSTerm.clear_exec()

            # Set the filename to the exec file anyway.
            filename = HSTerm.exec_filename()

            if path.startswith('__FILE_ACCESS__?'):
                try:
                    # Extract the variables and handle the file access
                    variables = HSHttpServer.get_dict_from_url(path)

                    HSTerm.term('FileAccess: %s' % variables['command'])

                    if variables['command'] == 'save':
                        # Store all incomming data into the file.
                        HSTerm.term('Save file %s' % variables['filename'])
                        savename = HSHttpServer._CODE_ROOT + '/' + variables['filename']
                        with open(savename, 'wb') as file:
                            file.write(data)
                            received_data = len(data)
                            while received_data < content_length:
                                data = clientsocket.recv(HSHttpServer._MAX_BUFFER_SIZE)
                                file.write(data)
                                received_data += len(data)
                        HSTerm.term_exec('File %s saved.' % savename)
                        HSTerm.term_exec('%d bytes written.' % received_data)

                    elif variables['command'] == 'execute':
                        # Execute the code from RAM when the content is smaller than 1k
                        if content_length < 1024:
                            HSTerm.term('Execute from RAM.')

                            while len(data) < content_length:
                                data += clientsocket.recv(HSHttpServer._MAX_BUFFER_SIZE)
                            data = data.decode('utf-8')

                            # Execute the give data.
                            try:
                                exec(data, globals())
                            except Exception as e:
                                HSTerm.term_exec('Error: %s' % str(e))

                        else:
                            # Store the data into a file and execute them.
                            HSTerm.term('Execute from file exec_file.py')
                            savename = '/exec_file.py'
                            with open(savename, 'wb') as file:
                                file.write(data)
                                received_data = len(data)
                                while received_data < content_length:
                                    data = clientsocket.recv(HSHttpServer._MAX_BUFFER_SIZE)
                                    file.write(data)
                                    received_data += len(data)

                            # Execute the give data.
                            try:
                                exec(open(savename).read(), globals())
                            except Exception as e:
                                HSTerm.term_exec('Error: %s' % str(e))

                    elif variables['command'] == 'load':
                        # Return the file.
                        filename = HSHttpServer._CODE_ROOT + '/' + variables['filename']

                    else:
                        # The given command is not known.
                        filename = HSHttpServer._DOCUMENT_ROOT + '/404.html'
                        header = HSHttpServer.get_html_header(404, filename)
                        HSHttpServer.send_response(clientsocket, header, filename)
                        return

                except Exception as e:
                    HSTerm.term_exec('Internal Error:\n%s' % str(e))
                    header = HSHttpServer.get_html_header(500, filename)
                else:
                    header = HSHttpServer.get_html_header(200, filename)

            elif path.startswith('__COMMAND__'):
                try:
                    # Receive additional data until the package is complete.
                    # These data package is small, so load it into ram.
                    while len(data) < content_length:
                        data += clientsocket.recv(HSHttpServer._MAX_BUFFER_SIZE)
                    data = data.decode('utf-8')

                    # Convert the json data into a key/value dictionary.
                    args = json.loads(data)

                    HSTerm.term('Command: %s' % args['command'])

                    # Set the wifi connection and reset the device.
                    if args['command'] == 'set_wifi':
                        HSTerm.term('Set wifi connection to %s@%s' % (args['apName'], args['password']))
                        hs_network.set_wifi(args['apName'], args['password'])

                    # Get the list of all available wifis.
                    elif args['command'] == 'get_wifis':
                        data = {}
                        data['wifis'] = hs_network.get_wifis()
                        json_dump = json.dumps(data)
                        HSTerm.term_exec(json_dump)
                        HSTerm.term('Returns: %s' % json_dump)

                    # Save the new password key only when the oldkey is the same with the current.
                    elif args['command'] == 'save_password':

                        if (args['oldKey'] == self._authorization_key and args['newKey'] != ''):

                            HSTerm.term('Store the new password')
                            # Store the password.
                            self._authorization_key = args['newKey']
                            with open('password', 'w') as file:
                                file.write(self._authorization_key)

                            HSTerm.term_exec('New password written.')

                        else:
                            HSTerm.term('auth key: %s' % self._authorization_key)
                            HSTerm.term('old key: %s' % args['oldKey'])
                            HSTerm.term('new key: %s' % args['newKey'])
                            HSTerm.term_exec('Error: Could not store the password.')
                            HSTerm.term_exec('The current Password is not the same!')

                    # Get the list of all available code files.
                    elif args['command'] == 'get_file_list':

                        data = {}
                        data['files'] = os.listdir(HSHttpServer._CODE_ROOT)
                        json_dump = json.dumps(data)
                        HSTerm.term_exec(json_dump)
                        HSTerm.term('Returns: %s' % json_dump)

                    # Run the file which is saved on the device
                    elif args['command'] == 'run':
                        run_file = HSHttpServer._CODE_ROOT + '/' + args['filename']
                        print('run: %s' % run_file)
                        try:
                            exec(open(run_file).read(), globals())
                        except Exception as e:
                            HSTerm.term_exec('Error: %s' % str(e))

                    else:
                        # The given command is not known.
                        filename = HSHttpServer._DOCUMENT_ROOT + '/404.html'
                        header = HSHttpServer.get_html_header(404, filename)
                        HSHttpServer.send_response(clientsocket, header, filename)
                        return

                except Exception as e:
                    HSTerm.term_exec('Internal Error:\n%s' % str(e))
                    header = HSHttpServer.get_html_header(500, filename)
                else:
                    header = HSHttpServer.get_html_header(200, filename)

            else:
                filename = HSHttpServer._DOCUMENT_ROOT + '/404.html'
                header = HSHttpServer.get_html_header(404, filename)

        elif method == 'GET':

            # Split the arguments from the file path.
            path_with_arguments = path.split('?')

            # Ignore the arguments. We need only the file path.
            if len(path_with_arguments) > 0:
                filename = path_with_arguments[0]

            # use the index.html when the path is empty.
            if '' == filename:
                filename = 'index.html'

            # add the document path to the filename
            filename = HSHttpServer._DOCUMENT_ROOT + '/' + filename

            if accept_gzip:
                if HSHttpServer.file_exists(filename + '.gz'):
                    HSTerm.term('Sending gzip version of %s' % filename)

                    # prepare everything for a gzip file response.
                    filename += '.gz'
                    header = HSHttpServer.get_html_header(200, filename, accept_gzip)
                else:
                    HSTerm.term('no compressed file found :(')
                    HSTerm.term('Sending %s' % filename)
                    header = HSHttpServer.get_html_header(200, filename)

            elif HSHttpServer.file_exists(filename):
                HSTerm.term('Sending %s' % filename)
                header = HSHttpServer.get_html_header(200, filename)

            else:
                HSTerm.term('File %s not found.' % filename)
                filename = HSHttpServer._DOCUMENT_ROOT + '/404.html'
                header = HSHttpServer.get_html_header(404, filename)

        else:
            HSTerm.term('Unknown HTML method.')
            filename = HSHttpServer._DOCUMENT_ROOT + '/404.html'
            header = HSHttpServer.get_html_header(404, filename)

        HSHttpServer.send_response(clientsocket, header, filename)

    @staticmethod
    def send_response(clientsocket: socket.socket, header: str, filename: str):
        # Send the response back to the client.
        clientsocket.sendall(bytes(header, 'utf-8'))
        try:
            with open(filename, 'rb') as file:
                start_time = time.time()
                sent_data = 0
                bytes_read = file.read(HSHttpServer._MAX_BUFFER_SIZE)
                count = 0
                while bytes_read:
                    clientsocket.sendall(bytes_read)
                    sent_data += HSHttpServer._MAX_BUFFER_SIZE
                    count += 1
                    if count > (1024 * 10 / HSHttpServer._MAX_BUFFER_SIZE):
                        ttime = time.time() - start_time
                        if ttime == 0:
                            ttime = 1

                        HSTerm.term(
                            '    %d Bytes sent in %d seconds with %d KB/second' % (
                                sent_data, ttime, sent_data / ttime / 1024
                            )
                        )
                        count = 0
                    bytes_read = file.read(HSHttpServer._MAX_BUFFER_SIZE)
        except Exception as e:
            HSTerm.term('Send response error: %s' % str(e))

    @staticmethod
    def file_exists(filename: str) -> bool:
        """
        Try to open the file. If there is an exeption, return false.
        """
        try:
            open(filename, 'rb')
            return True
        except Exception:
            return False

    @staticmethod
    def get_file_length(filename: str) -> int:
        """
        Get the length of the file in bytes.
        """
        size_in_bytes = 0
        try:
            statinfo = os.stat(filename)
            size_in_bytes = statinfo[6]
            HSTerm.term('Size: %d' % size_in_bytes)
        except Exception as e:
            HSTerm.term('Get file length error: %s' % str(e))
        return size_in_bytes

    @staticmethod
    def get_html_header(status: int, filename: str, accept_gzip: bool = False) -> str:
        """
        Get the header base on the
        """

        fileext = filename[filename.rfind('.') + 1:]
        if fileext == 'gz':
            end_index = filename.rfind('.')
            start_index = filename.rfind('.', 0, end_index) + 1
            fileext = filename[start_index:end_index]

        header = ''
        header += 'HTTP/1.1 %s\r\n' % HSHttpServer._HTML_STATUS[status]
        header += 'Server: %s\r\n' % HSHttpServer._SERVER_NAME
        header += 'Connection: close\r\n'
        if fileext in HSHttpServer._MIME_TYPE:
            header += 'Content-Type: %s\r\n' % HSHttpServer._MIME_TYPE[fileext]
        else:
            header += 'Content-Type: %s\r\n' % HSHttpServer._MIME_TYPE['txt']
        header += 'Content-Length: %d\r\n' % HSHttpServer.get_file_length(filename)
        if accept_gzip:
            header += 'Content-Encoding: gzip\r\n'
        if status == 401:
            header += 'WWW-Authenticate: Basic realm="%s"\n\n' % HSHttpServer._SERVER_NAME
        header += '\r\n'

        return header

    @staticmethod
    def get_dict_from_url(url: str) -> str:
        """
        Get a dict of all variables from an url.
        """
        variables = url.split('?')[1]
        variables = variables.replace('&', '","')
        variables = variables.replace('=', '":"')
        variables = '{"%s"}' % variables
        variables = json.loads(variables)
        return variables
