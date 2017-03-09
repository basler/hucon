# Try to import the packages for the micro python environment, otherwise import the default python environment.
try:
    import uos as os
    import usocket as socket
except:
    import os
    import socket

# Server name which is used for the HTML header
SERVER_NAME = b"My Custon Webserver"

# Define the HTML MIME Types which are possible to send with this webserver implementation.
# There are more types defined here: https://wiki.selfhtml.org/wiki/Referenz:MIME-Typen
MIME_Type = {
    # ext  : [MIME-Type,                 binary]
    'js'   : [b'application/javascript', False],
    'json' : [b'application/json',       False],
    'woff' : [b'application/font-woff',  True],
    'woff2': [b'application/font-woff2', True],

    'gif'  : [b'image/gif',              True],
    'jpeg' : [b'image/jpeg',             True],
    'jpg'  : [b'image/jpeg',             True],
    'png'  : [b'image/png',              True],
    'ico'  : [b'image/x-icon',           True],

    'css'  : [b'text/css',               False],
    'htm'  : [b'text/html',              False],
    'html' : [b'text/html',              False],
    'js'   : [b'text/javascript',        False],
    'txt'  : [b'text/plain',             False],
}


def get_file_content(filename, mode = 'rb'):
    content = b''
    try:
        with open(filename, mode) as file:
            content = file.read()
    except:
        pass
    return content


def handle_request(request):
    """
    Handle the request.
    """
    if request != '':
        # The first line is the one we need to get the information about the request.
        request_line = request.split("\r\n")[0]
        request_line = request_line.split()

        # Break down the request line into components
        (request_method,  # GET
         request_path,    # /hello
         request_version  # HTTP/1.1
         ) = request_line

        print("Method:", request_method)
        print("Path:", request_path)
        print("Version:", request_version)

        if request_method == "POST":
            print(request)
            pass
        if request_method == "GET":

            # Get the filename with the extension.
            request_path = request_path.strip('/')
            path_with_arguments = request_path.split('?')
            filename = ''
            get_arguments = ''
            if len(path_with_arguments) > 0:
                filename = path_with_arguments[0]
            if len(path_with_arguments) > 1:
                get_arguments = path_with_arguments[1]

            if filename == '':
                filename = 'index.html'
            fileext = filename[filename.rfind('.') + 1:]

            header = b''

            # Check the extension.
            # If the extension is not defined, send a 'Not Found' Status.
            if fileext in MIME_Type:

                if True: #MIME_Type[fileext][1]:
                    print("binary based file")
                    content = get_file_content(filename)
                else:
                    print("text based file")
                    content = get_file_content(filename, 'rt')

                header += b'HTTP/1.1 200 OK\r\n'
                header += b'Server: ' + SERVER_NAME + b'\r\n'
                header += b'Content-Type: ' + MIME_Type[fileext][0] + b'\r\n'
                header += b'Content-Length: %d\r\n' % len(content)
                header += b'\r\n'

            else:
                print("Error 404 Not Found.")
                content = get_file_content('404.html')

                header += b'HTTP/1.1 404 Not Found\r\n'
                header += b'Server: ' + SERVER_NAME + b'\r\n'
                header += b'Content-Type: ' + MIME_Type["html"][0] + b'\r\n'
                header += b'Content-Length: %d\r\n' % len(content)
                header += b'\r\n'

            return header, content


def main(use_stream=False):
    """
    Create the Server and listen on each incomming request.
    """
    s = socket.socket()

    # Binding to all interfaces - server will be accessible to other hosts!
    address_info = socket.getaddrinfo("0.0.0.0", 8080)
    addr = address_info[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    print("Listening, connect your browser to http://<this_host>:8080/")

    # Change the root directory to 'www'
    os.chdir("./www")

    while True:
        res = s.accept()
        client_s = res[0]
        client_addr = res[1]
        if use_stream:
            # MicroPython socket objects support stream (aka file) interface
            # directly.
            header, content = handle_request(client_s.recv(4096).decode('utf-8'))
            if header != '':
                client_s.write(header)
                totalsent = 0
                while totalsent < len(content):
                    sent = client_s.write(content)
                    totalsent += len(sent)
        else:
            rec = client_s.recv(4096)
            if rec:
                header, content = handle_request(rec.decode('utf-8'))
                print('length of content:' + str(len(content)))
                print(header)
                print()
                if header != '':
                    client_s.send(header)
                    client_s.send(content)
        client_s.close()

if __name__ == '__main__':
    main()
