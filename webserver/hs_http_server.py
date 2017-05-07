#!/usr/bin/env python3

try:
    # Import different packages on the micro python.
    import uos as os
    import usocket as socket
except:
    import os
    import socket

from hs_term import HSTerm


class HSHttpServer:
    """
    This implementation is a simple HTTP Server which works on Windows, Linux and macOS with different Browser.
    It is written to work with the micro python an a ESP8266 device.
    """

    # Name of this server for the HTTP header.
    _SERVER_NAME = 'My Custon Webserver'

    # Folder where all files for the server are stored.
    _DOCUMENT_ROOT = os.path.join(os.getcwd(), 'www')

    # Private server socket to listen for new connections.
    _server_socket = None

    # Define the port on which the server should listening on.
    _LISTENING_PORT = 8080

    # Private variable to store its own ip address.
    _own_ip = ''

    # Define the HTML MIME Types which are possible to send with this webserver implementation.
    # There are more types defined here: https://wiki.selfhtml.org/wiki/Referenz:MIME-Typen
    _MIME_TYPE = {
        # ext  : MIME-Type,
        'js': 'application/javascript',
        'json': 'application/json',
        'woff': 'application/font-woff',
        'woff2': 'application/font-woff2',

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
        404: '404 Not Found'
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
    def __init__(cls):
        """
        Create a socket to get its own ip address.
        """
        try:
            cls._own_ip = str(socket.gethostbyname(socket.gethostname()))
            return
        except Exception as e:
            cls._own_ip = ''
            HSTerm.term('Could not read my own ip address. :(')

    @classmethod
    def start(cls, use_threads: bool):
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

        if use_threads:
            from threading import Thread
            HSTerm.term('Threads are used.')
        else:
            HSTerm.term('No threads are used.')

        # Start the socket listening.
        cls._server_socket.listen(5)
        HSTerm.term('Listening, connect your browser to http://' + cls._own_ip + ':' + str(cls._LISTENING_PORT))

        # Listening in an endless loop for new connections.
        while True:
            addr = None
            clientsocket = None
            try:
                clientsocket, addr = cls._server_socket.accept()
                ip, port = str(addr[0]), str(addr[1])
                HSTerm.term('\nConnection accpted from ' + ip + ':' + port)

                if use_threads:
                    try:
                        Thread(target=HSHttpServer.handle_connection, args=(clientsocket, ip, port)).start()
                    except Exception as e:
                        HSTerm.term('Thread error!')
                        HSTerm.term(str(e))
                else:
                    HSHttpServer.handle_connection(clientsocket, ip, port)
            except KeyboardInterrupt:
                HSTerm.term('Close socket.')
                if clientsocket:
                    clientsocket.close()
                break

        # Close the socket listening after the user want to stop it.
        cls._server_socket.close()

    @staticmethod
    def handle_connection(clientsocket: socket.socket, ip: str, port: str, max_buffer_size: int = 2048):
        """
        Handle every connection within this function.
        This function can be called within a new thread or within the main thread.
        """
        header = ''
        data = ''
        content_length = 0

        #  receive the first package.
        receive_buffer = clientsocket.recv(max_buffer_size)

        # Try to find a 'Content-Length' within the HTTP header to check the length after the '\r\n\r\n' statement.
        # This is needed for large packages when the server received post data.
        index = receive_buffer.find(HSHttpServer._HTTP_CONTENT_LENGTH_MARK_BYTE)
        if index > 0:
            # Found a 'Content Length' mark.
            # So, try to find the end of the line to catch up the additional content length.
            index += HSHttpServer._HTTP_CONTENT_LENGTH_SIZE_BYTE
            line_end = receive_buffer.find(HSHttpServer._HTTP_LINE_END_MARK_BYTE, index)
            content_length = int(receive_buffer[index:line_end])

        # Try to find the end of the HTTP header.
        while receive_buffer.find(HSHttpServer._HTTP_HEADER_END_MARK_BYTE) == -1:
            receive_buffer += clientsocket.recv(max_buffer_size)
        index = receive_buffer.find(HSHttpServer._HTTP_HEADER_END_MARK_BYTE)
        packet_len = index + HSHttpServer._HTTP_HEADER_END_SIZE_BYTE + content_length

        # Receive additional data until the package is complete.
        while len(receive_buffer) < packet_len:
            receive_buffer += clientsocket.recv(max_buffer_size)

        #  Split the header/data from the receive buffer.
        (header, data) = receive_buffer.split(HSHttpServer._HTTP_HEADER_END_MARK_BYTE)

        # Decode the byet stream into a utf-8 string
        header = header.decode('utf-8')
        data = data.decode('utf-8')

        # Handle the request if there is an header.
        if header:
            (header, filename) = HSHttpServer.handle_request(header, data)

            # Send the response if there is a header. :)
            if '' != header:
                clientsocket.send(bytes(header, 'utf-8'))
                try:
                    with open(filename, 'rb') as file:
                        bytes_read = file.read(max_buffer_size)
                        while bytes_read:
                            clientsocket.send(bytes_read)
                            bytes_read = file.read(max_buffer_size)
                except Exception as e:
                    HSTerm.term(str(e))

        # So, the 'keep-alive' statement is not supported by this implementation. Close it!
        clientsocket.close()

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
            size_in_bytes = statinfo.st_size
        except Exception as e:
            HSTerm.term(str(e))
        return size_in_bytes

    @staticmethod
    def not_found_page() -> (str, str):
        """
        Get the file content and header for the 'Not Found' page.
        """
        filename = os.path.join(HSHttpServer._DOCUMENT_ROOT, '404.html')
        header = HSHttpServer.get_html_header(404, filename)

        return (header, filename)

    @staticmethod
    def get_html_header(status: int, filename: str, accept_gzip: bool = False) -> str:
        """
        Get the header base on the
        """

        fileext = filename[filename.rfind('.') + 1:]

        header = ''
        header += 'HTTP/1.1 %s\r\n' % HSHttpServer._HTML_STATUS[status]
        header += 'Server: %s\r\n' % HSHttpServer._SERVER_NAME
        header += 'Connection: close\r\n'
        if fileext in HSHttpServer._MIME_TYPE:
            header += 'Content-Type: %s\r\n' % HSHttpServer._MIME_TYPE[fileext]
        header += 'Content-Length: %d\r\n' % HSHttpServer.get_file_length(filename)
        if accept_gzip:
            header += 'Content-Encoding: gzip\r\n'
        header += '\r\n'

        return header

    @staticmethod
    def handle_request(header, data) -> (str, str):
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

        HSTerm.term('%s: %s' % (header_method, header_path))

        accept_gzip = False
        for line in header_lines:
            if 'Accept-Encoding' in line:
                if 'gzip' in line:
                    accept_gzip = True

        header = ''
        filename = ''

        # Handle a POST request
        if 'POST' == header_method:

            # Handle the access on a '__Execute__' page.
            header_path = header_path.strip('/')
            if '__Execute__' == header_path:

                # Clear the exec file.
                HSTerm.clear_exec()

                # Replace all 'print' statements with 'HSTerm.term_exec'
                data = data.replace('print', 'HSTerm.term_exec')

                # Execute the give data.
                exec(data)

                # Get the filename and generate the header.
                filename = HSTerm.exec_filename()
                header = HSHttpServer.get_html_header(200, filename)

                # Return the result header and the response from the executed data.
                return header, filename

            # Return 'Not Found'
            return HSHttpServer.not_found_page()

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
            filename = os.path.join(HSHttpServer._DOCUMENT_ROOT, filename)

            if accept_gzip:
                if HSHttpServer.file_exists(filename + '.gz'):
                    HSTerm.term('Sending gzip version of %s' % filename)

                    # prepare everything for a gzip file response.
                    filename += '.gz'
                    header = HSHttpServer.get_html_header(200, filename, accept_gzip)

                    # Return the result header and response for the GET.
                    return (header, filename)
                else:
                    HSTerm.term('no compressed file found :(')

            if HSHttpServer.file_exists(filename):
                header = HSHttpServer.get_html_header(200, filename)

                # Return the result header and response for the GET.
                return (header, filename)

            HSTerm.term('File %s not found' % filename)
            return HSHttpServer.not_found_page()
