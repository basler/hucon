#!/usr/bin/env python3

try:
    # Import different packages on the micro python.
    import uos as os
    import usocket as socket
except:
    import os
    import socket

from print import ColoredPrint as print


class HTTPServer:
    """
    This implementation is a simple HTTP Server which works on Windows, Linux and macOS with different Browser.
    It is written to work with the micro python an a ESP8266 device.
    """

    # Name of this server for the HTTP header.
    _SERVER_NAME = b"My Custon Webserver"

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
        'js': b'application/javascript',
        'json': b'application/json',
        'woff': b'application/font-woff',
        'woff2': b'application/font-woff2',

        'gif': b'image/gif',
        'jpeg': b'image/jpeg',
        'jpg': b'image/jpeg',
        'png': b'image/png',
        'ico': b'image/x-icon',

        'css': b'text/css',
        'htm': b'text/html',
        'html': b'text/html',
        'js': b'text/javascript',
        'txt': b'text/plain',
    }

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
            print.term('Could not define its onw ip address. :(', print.ERROR)

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
            print.term('Socket created', print.INFO)

            # Binding to all interfaces - server will be accessible to other hosts!
            address_info = socket.getaddrinfo('0.0.0.0', cls._LISTENING_PORT)
            addr = address_info[0][-1]

            cls._server_socket.bind(addr)
            print.term('Socket bind complete.', print.INFO)
        except Exception as e:
            print.term('Create socket error: ' + str(e), print.ERROR)
            cls._server_socket.close()
            cls._server_socket = None
            return

        if use_threads:
            from threading import Thread
            print.term('Threads are used.', print.INFO)
        else:
            print.term('No threads are used.', print.INFO)

        # Start the socket listening.
        cls._server_socket.listen(5)
        print.term('Listening, connect your browser to http://' + cls._own_ip + ':' + str(cls._LISTENING_PORT), print.INFO)

        # Change the root directory to 'www'
        os.chdir('./www')

        # Listening in an endless loop for new connections.
        while True:
            addr = None
            clientsocket = None
            try:
                clientsocket, addr = cls._server_socket.accept()
                ip, port = str(addr[0]), str(addr[1])
                print.term('Connection accpted from ' + ip + ':' + port, print.INFO)

                try:
                    if use_threads:
                        Thread(target=HTTPServer.handle_connection, args=(clientsocket, ip, port)).start()
                    else:
                        HTTPServer.handle_connection(clientsocket, ip, port)
                except Exception as e:
                    print.term('Thread error!', print.ERROR)
                    print.term(str(e), print.ERROR)
            except KeyboardInterrupt:
                print.term('Close socket.', print.INFO)
                if clientsocket:
                    clientsocket.close()
                break

        # Close the socket listening after the user want to stop it.
        cls._server_socket.close()

    _HTTP_CONTENT_LENGTH_MARK = b'Content-Length: '
    _HTTP_CONTENT_LENGTH_SIZE = 16
    _HTTP_LINE_END_MARK = b'\r\n'
    _HTTP_LINE_END_SIZE = 2
    _HTTP_HEADER_END_MARK = b'\r\n\r\n'
    _HTTP_HEADER_END_SIZE = 4

    @staticmethod
    def handle_connection(clientsocket: socket.socket, ip: str, port: str, max_buffer_size: int = 4096):
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
        index = receive_buffer.find(HTTPServer._HTTP_CONTENT_LENGTH_MARK)
        if index > 0:
            # Found a 'Content Length' mark.
            # So, try to find the end of the line to catch up the additional content length.
            index += HTTPServer._HTTP_CONTENT_LENGTH_SIZE
            line_end = receive_buffer.find(HTTPServer._HTTP_LINE_END_MARK, index)
            content_length = int(receive_buffer[index:line_end])

        # Try to find the end of the HTTP header.
        while receive_buffer.find(HTTPServer._HTTP_HEADER_END_MARK) == -1:
            receive_buffer += clientsocket.recv(max_buffer_size)
        index = receive_buffer.find(HTTPServer._HTTP_HEADER_END_MARK)
        packet_len = index + HTTPServer._HTTP_HEADER_END_SIZE + content_length

        # Receive additional data until the package is complete.
        while len(receive_buffer) < packet_len:
            receive_buffer += clientsocket.recv(max_buffer_size)

        #  Split the header/data from the receive buffer.
        (header, data) = receive_buffer.split(HTTPServer._HTTP_HEADER_END_MARK)

        # Decode the byet stream into a utf-8 string
        header = header.decode('utf-8')
        data = data.decode('utf-8')

        # Handle the request if there is an header.
        if header:
            (header, content) = HTTPServer.handle_request(header, data)

            # Send the response if there is a header. :)
            if header != '':
                clientsocket.send(header)
                clientsocket.send(content)

        # So, the 'keep-alive' statement is not supported by this implementation. Close it!
        clientsocket.close()

    @staticmethod
    def get_file_content(filename: str) -> bytes:
        """
        Get the file content from the defined file.
        """
        content = b''
        try:
            with open(filename, 'rb') as file:
                content = file.read()
        except:
            pass
        return content

    @staticmethod
    def not_found_page() -> (bytes, bytes):
        """
        Get the file content and header for the 'Not Found' page.
        """
        header = b''
        content = b''

        content = HTTPServer.get_file_content('404.html')

        header += b'HTTP/1.1 404 Not Found\r\n'
        header += b'Server: ' + HTTPServer._SERVER_NAME + b'\r\n'
        header += b'Content-Type: ' + HTTPServer._MIME_TYPE["html"] + b'\r\n'
        header += b'Content-Length: %d\r\n' % len(content)
        header += b'\r\n'

        return (header, content)

    @staticmethod
    def handle_request(header, data) -> (bytes, bytes):
        """
        Handle the request.
        """

        # The first line is the one we need to get the information about the request.
        header_line = header.split("\r\n")[0]
        header_line = header_line.split()

        # Break down the request line into components
        (header_method,  # GET
         header_path,    # /hello
         header_version  # HTTP/1.1
         ) = header_line

        print.term('Method: ' + header_method, print.DEBUG)
        print.term('Path: ' + header_path, print.DEBUG)
        print.term('Version: ' + header_version, print.DEBUG)

        header = b''
        content = b''

        # Handle a POST request
        if header_method == "POST":

            # Handle the access on a '__Execute__' page.
            header_path = header_path.strip('/')
            if '__Execute__' == header_path:

                # Replace all 'print' statements with 'print.term'
                data = data.replace('print', 'print.term')

                # Execute the give data.
                exec(data)

                # TODO: result the printed messages!
                content = b"Done ..."

                header += b'HTTP/1.1 200 OK\r\n'
                header += b'Server: ' + HTTPServer._SERVER_NAME + b'\r\n'
                header += b'Content-Type: ' + HTTPServer._MIME_TYPE['txt'] + b'\r\n'
                header += b'Content-Length: %d\r\n' % len(content)
                header += b'\r\n'

                # Return the result header and the response from the executed data.
                return header, content

            # Return 'Not Found'
            return HTTPServer.not_found_page()

        # Handle a GET request.
        if header_method == "GET":

            # Get the filename with the extension.
            header_path = header_path.strip('/')

            # Split the arguments from the file path.
            path_with_arguments = header_path.split('?')

            # Ignore the arguments. We need only the file path.
            filename = ''
            if len(path_with_arguments) > 0:
                filename = path_with_arguments[0]

            # use the index.html when the path is empty.
            if filename == '':
                filename = 'index.html'
            fileext = filename[filename.rfind('.') + 1:]

            # Check the extension.
            # If the extension is not defined, send a 'Not Found' Status.
            if fileext in HTTPServer._MIME_TYPE:

                content = HTTPServer.get_file_content(filename)

                header += b'HTTP/1.1 200 OK\r\n'
                header += b'Server: ' + HTTPServer._SERVER_NAME + b'\r\n'
                header += b'Content-Type: ' + HTTPServer._MIME_TYPE[fileext] + b'\r\n'
                header += b'Content-Length: %d\r\n' % len(content)
                header += b'\r\n'

                # Return the result header and response for the GET.
                return (header, content)

            # Return the 'Not Found' page.
            return HTTPServer.not_found_page()
