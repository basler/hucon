#!/usr/bin/env python3
import gc
import time

try:
    # Import different packages on the micro python.
    import uos as os
    import usocket as socket
    import ujson as json
except:
    import os
    import socket
    import json

from hs_term import HSTerm

# Call the garbage collector.
gc.collect()

class HSHttpServer:
    """
    This implementation is a simple HTTP Server which works on Windows, Linux and macOS with different Browser.
    It is written to work with the micro python an a ESP8266 device.
    """

    # Name of this server for the HTTP header.
    _SERVER_NAME = 'HackerSchool Custon Webserver'

    # Folder where all files for the server are stored.
    _DOCUMENT_ROOT = os.getcwd() + '/www'

    # Folder where all custom code files are stored.
    _CODE_ROOT = os.getcwd() + '/code'

    # Define the port on which the server should listening on.
    _LISTENING_PORT = 8080

    # Private server socket to listen for new connections.
    _server_socket = None

    # Private variable to store its own ip address.
    _own_ip = ''

    # Private key for the authorization to the key.
    _authorization_key = ''

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

    # Mark to search for the content length during the receive of the bytestream.
    _HTTP_CONTENT_LENGTH_MARK_BYTE = b'Content-Length: '

    # Length of the content mark.
    _HTTP_CONTENT_LENGTH_SIZE_BYTE = 16

    # Mark to search for a line end during the receive of the bytestream.
    _HTTP_LINE_END_MARK_BYTE = b'\r\n'

    # Mark to search for the end of the header end during the receive of the bytestream.
    _HTTP_HEADER_END_MARK_BYTE = b'\r\n\r\n'

    # Length of the header end mark.
    _HTTP_HEADER_END_SIZE_BYTE = 4

    @classmethod
    def __init__(cls, key: str):
        """
        Create a socket to get its own ip address.
        """
        cls._authorization_key = key
        try:
            cls._own_ip = str(socket.gethostbyname(socket.gethostname()))
            return
        except Exception as e:
            cls._own_ip = ''
            HSTerm.term('Could not read my own ip address. :(')

    @classmethod
    def start(cls):
        """
        Get a socket object and start the listening on the defined port.
        If the _use_threads_ is True, every new connection will be handled within a new thread.
        """
        try:
            # Create the socket.
            cls._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cls._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            HSTerm.term('Socket created')

            # Binding to all interfaces - server will be accessible to other hosts!
            address_info = socket.getaddrinfo('0.0.0.0', cls._LISTENING_PORT)
            addr = address_info[0][-1]

            cls._server_socket.bind(addr)
            HSTerm.term('Socket bind complete.')
        except Exception as e:
            HSTerm.term('Create socket error: ' + str(e))
            cls._server_socket.close()
            cls._server_socket = None
            return

        # Start the socket listening.
        cls._server_socket.listen(5)
        HSTerm.term('Listening, connect your browser to http://' + cls._own_ip + ':' + str(cls._LISTENING_PORT))

        # Listening in an endless loop for new connections.
        while True:
            addr = None
            clientsocket = None
            try:
                gc.collect()
                clientsocket, addr = cls._server_socket.accept()
                ip, port = str(addr[0]), str(addr[1])
                gc.collect()

                HSTerm.term('\nConnection accpted from ' + ip + ':' + port)
                cls.handle_connection(clientsocket, ip, port)

            except KeyboardInterrupt:
                HSTerm.term('\nClose socket.')
                if clientsocket:
                    clientsocket.close()
                break
            except Exception as e:
                HSTerm.term('Main loop error: %s' % str(e))

        # Close the socket listening after the user want to stop it.
        cls._server_socket.close()

    @classmethod
    def handle_connection(cls, clientsocket: socket.socket, ip: str, port: str, max_buffer_size: int = 512):
        """
        Handle every connection within this function.
        This function can be called within a new thread or within the main thread.
        """
        header = ''
        data = ''
        content_length = 0
        gc.collect()
        #  receive the first package.
        receive_buffer = clientsocket.recv(max_buffer_size)

        # Try to find the end of the HTTP header.
        while receive_buffer.find(cls._HTTP_HEADER_END_MARK_BYTE) == -1:
            receive_buffer += clientsocket.recv(max_buffer_size)

        # Try to find a 'Content-Length' within the HTTP header to check the length after the '\r\n\r\n' statement.
        # This is needed for large packages when the server received post data.
        index = receive_buffer.find(cls._HTTP_CONTENT_LENGTH_MARK_BYTE)
        if index > 0:
            # Found a 'Content Length' mark.
            # So, try to find the end of the line to catch up the additional content length.
            index += cls._HTTP_CONTENT_LENGTH_SIZE_BYTE
            gc.collect()
            line_end = receive_buffer.find(cls._HTTP_LINE_END_MARK_BYTE, index)
            gc.collect()
            content_length = int(receive_buffer[index:line_end])
            gc.collect()

        index = receive_buffer.find(cls._HTTP_HEADER_END_MARK_BYTE)
        packet_len = index + cls._HTTP_HEADER_END_SIZE_BYTE + content_length

        # Receive additional data until the package is complete.
        while len(receive_buffer) < packet_len:
            receive_buffer += clientsocket.recv(max_buffer_size)

        #  Split the header/data from the receive buffer.
        (header, data) = receive_buffer.split(cls._HTTP_HEADER_END_MARK_BYTE)

        # Decode the byet stream into a utf-8 string
        header = header.decode('utf-8')
        data = data.decode('utf-8')

        # Handle the request if there is an header.
        if header:
            (header, filename) = cls.handle_request(header, data)

            # Send the response if there is a header. :)
            if '' != header:
                clientsocket.sendall(bytes(header, 'utf-8'))
                try:
                    with open(filename, 'rb') as file:
                        start_time = time.time()
                        sent_data = 0
                        bytes_read = file.read(max_buffer_size)
                        count = 0
                        gc.collect()
                        while bytes_read:
                            clientsocket.sendall(bytes_read)
                            sent_data += max_buffer_size
                            count += 1
                            if count > (1024 * 10 / max_buffer_size):
                                ttime = time.time() - start_time
                                if ttime == 0:
                                    ttime = 1

                                HSTerm.term(
                                    '%d Bytes sent in %d seconds with %d Bytes/second' % (
                                        sent_data, ttime, sent_data / ttime
                                    )
                                )
                                count = 0
                                gc.collect()
                            bytes_read = file.read(max_buffer_size)
                except Exception as e:
                    HSTerm.term('Handle connection error: %s' % str(e))

        # So, the 'keep-alive' statement is not supported by this implementation. Close it!
        clientsocket.close()
        gc.collect()

    @classmethod
    def file_exists(cls, filename: str) -> bool:
        """
        Try to open the file. If there is an exeption, return false.
        """
        try:
            open(filename, 'rb')
            return True
        except Exception:
            return False

    @classmethod
    def get_file_length(cls, filename: str) -> int:
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

    @classmethod
    def not_found_page(cls) -> (str, str):
        """
        Get the file content and header for the 'Not Found' page.
        """
        filename = cls._DOCUMENT_ROOT + '/404.html'
        header = cls.get_html_header(404, filename)

        return (header, filename)

    @classmethod
    def get_html_header(cls, status: int, filename: str, accept_gzip: bool = False) -> str:
        """
        Get the header base on the
        """

        fileext = filename[filename.rfind('.') + 1:]
        if fileext == 'gz':
            end_index = filename.rfind('.')
            start_index = filename.rfind('.', 0, end_index) + 1
            fileext = filename[start_index:end_index]

        header = ''
        header += 'HTTP/1.1 %s\r\n' % cls._HTML_STATUS[status]
        header += 'Server: %s\r\n' % cls._SERVER_NAME
        header += 'Connection: close\r\n'
        if fileext in cls._MIME_TYPE:
            header += 'Content-Type: %s\r\n' % cls._MIME_TYPE[fileext]
        else:
            header += 'Content-Type: %s\r\n' % cls._MIME_TYPE['txt']
        header += 'Content-Length: %d\r\n' % cls.get_file_length(filename)
        if accept_gzip:
            header += 'Content-Encoding: gzip\r\n'
        if status == 401:
            header += 'WWW-Authenticate: Basic realm="%s"\n\n' % cls._SERVER_NAME
        header += '\r\n'

        return header

    @classmethod
    def handle_request(cls, header: str, data: str) -> (str, str):
        """
        Handle the request.
        """

        # The first line is the one we need to get the information about the request.
        header_lines = header.split('\r\n')
        header_line = header_lines[0]
        header_line = header_line.split()

        # Break down the request line into components
        (header_method,  # GET
         header_path,    # /hello
         header_version  # HTTP/1.1
         ) = header_line

        HSTerm.term('Method: ' + header_method)
        HSTerm.term('Path: ' + header_path)

        accept_gzip = False
        authorized = False
        for line in header_lines:
            if 'Accept-Encoding' in line:
                if 'gzip' in line:
                    accept_gzip = True
            if 'Authorization' in line:
                if cls._authorization_key in line:
                    authorized = True

        header = ''
        filename = ''

        # Stop if the user has no authorization to get any page.
        if not authorized:
            filename = cls._DOCUMENT_ROOT + '/index.html'
            header = cls.get_html_header(401, filename)
            return (header, filename)

        # Handle a POST request
        if 'POST' == header_method:

            # Clear the exec file.
            HSTerm.clear_exec()

            # Set the filename to the exec file anyway.
            filename = HSTerm.exec_filename()

            # Handle a set command.
            header_path = header_path.strip('/')
            if '__COMMAND__' == header_path:
                try:
                    # Convert the data into a key/value dictionary.
                    args = json.loads(data)

                    print(args)

                    # Execute the data which are within the code argument.
                    if args['command'] == 'execute':

                        # Replace all 'print' statements with 'HSTerm.term_exec'
                        code = args['code'].replace('print', 'HSTerm.term_exec')

                        # Execute the give data.
                        try:
                            exec(code)
                        except Exception as e:
                            HSTerm.term_exec('Error: %s' % str(e))

                    # Save the new password key only when the oldkey is the same with the current.
                    elif args['command'] == 'save_password':

                        if (args['oldKey'] == cls._authorization_key and args['newKey'] != ''):

                            HSTerm.term('Store the new password')
                            # Store the password.
                            cls._authorization_key = args['newKey']
                            with open('password', 'w') as file:
                                file.write(cls._authorization_key)

                            HSTerm.term_exec('New password written.')

                        else:
                            HSTerm.term_exec('Error: Could not store the password.')
                            HSTerm.term_exec('The current Password is not the same!')

                    # Get the list of all available code files.
                    elif args['command'] == 'get_file_list':
                        data = {}
                        data['files'] = os.listdir(cls._CODE_ROOT)
                        HSTerm.term_exec(json.dumps(data))

                    # Get the data from a specific code file.
                    elif args['command'] == 'get_file_data':
                        filename = cls._CODE_ROOT + '/' + args['filename']

                    # Save the data within the given file name.
                    elif args['command'] == 'save_file_data':
                        savename = cls._CODE_ROOT + '/' + args['filename']
                        with open(savename, 'w') as file:
                            file.write(args['code'])
                        HSTerm.term_exec('File %s saved.' % savename)

                except Exception as e:
                    HSTerm.term_exec('Internal Error:\n%s' % str(e))
                    header = cls.get_html_header(500, filename)
                else:
                    header = cls.get_html_header(200, filename)
                finally:
                    # Return the result header and the response from the password save.
                    return header, filename

        # Handle a GET request.
        if 'GET' == header_method:

            # Get the filename with the extension.
            header_path = header_path.strip('/')

            # Split the arguments from the file path.
            path_with_arguments = header_path.split('?')

            # Ignore the arguments. We need only the file path.
            if len(path_with_arguments) > 0:
                filename = path_with_arguments[0]

            # use the index.html when the path is empty.
            if '' == filename:
                filename = 'index.html'

            # add the document path to the filename
            filename = cls._DOCUMENT_ROOT + '/' + filename

            if accept_gzip:
                if cls.file_exists(filename + '.gz'):
                    HSTerm.term('Sending gzip version of %s' % filename)

                    # prepare everything for a gzip file response.
                    filename += '.gz'
                    header = cls.get_html_header(200, filename, accept_gzip)

                    # Return the result header and response for the GET.
                    return (header, filename)
                else:
                    HSTerm.term('no compressed file found :(')

            if cls.file_exists(filename):
                HSTerm.term('Sending %s' % filename)
                header = cls.get_html_header(200, filename)

                # Return the result header and response for the GET.
                return (header, filename)

        HSTerm.term('File %s not found.' % filename)
        return cls.not_found_page()
