#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This tiny web server is able to show the web page for the hacker school.
"""

import os
import socketserver
import urllib
from http.server import SimpleHTTPRequestHandler

# Default port
PORT = 8080


class HackerSchoolRequestHandler(SimpleHTTPRequestHandler):
    """
    Override the SimpleHTTPRequestHandler to catch the __SetValue__ page
    and handle the request from the web page.
    """

    def do_POST(self):
        print("Request: %s" % self.path)
        if self.path.startswith('/__SetValue__'):
            print("New values received ...")

            # Get the data from the post request
            length = int(self.headers['Content-Length'])
            post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
            if 'execute' in post_data:
                print("execute detected")
                code = post_data["execute"][0]
                with open('tmpfile.py', 'w') as target:
                    target.write(code)

                with open('tmpfile.py', 'r') as target:
                    exec(target.read())

            # Send response status code
            self.send_response(200)

            # Send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # Send message back to client
            message = "TBD"

            # Write content as utf-8 data
            self.wfile.write(bytes(message, "utf8"))
            return
        return SimpleHTTPRequestHandler.do_POST(self)


def main():
    """
    Change the web server root folder to 'www' and start the listening
    defined port.
    """

    print("Start the Hacker School web server ...")

    # Change the root directory to 'www'
    os.chdir("./www")

    with socketserver.TCPServer(("localhost", PORT), HackerSchoolRequestHandler) as httpd:
        print("Serving at port:", PORT)
        print("Hit CTRL+C to stop the web server.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()


if __name__ == '__main__':
    main()
