#!/usr/bin/python
""" webserver.py - Flask based web server to handle all legal requests.

    Copyright (C) 2019 Basler AG
    All rights reserved.

    This software may be modified and distributed under the terms
    of the BSD license.  See the LICENSE file for details.
"""


def set_led(red, green, blue):
    """ Use the hucon eye driver to set the eye color.
    """
    try:
        from hucon.hucon import Eye

        Eye(1, Eye.RGB).set_color(red, green, blue)
        Eye(2, Eye.RGB).set_color(red, green, blue)
        Eye(3, Eye.RGB).set_color(red, green, blue)
        Eye(4, Eye.RGB).set_color(red, green, blue)

    except Exception as ex:
        print(ex)


# Set the led eyes to yellow at the beginning
set_led(249, 166, 2)

import argparse
import logging
import time

try:
    import httplib
except:
    import http.client as httplib
from flask import Flask
from flask import request
from flask import render_template
from flask_socketio import SocketIO

from HuConJsonRpc import HuConJsonRpc

json_rpc = HuConJsonRpc()

COLLECT_STATIC_ROOT = "/opt/hucon/webserver/static"
COLLECT_STORAGE = 'flask_collect.storage.file'

app = Flask(json_rpc._SERVER_NAME)
app.config["SECRET_KEY"] = "SECRET_KEY"
socketio = SocketIO(app, logger=True)#, async_mode='eventlet'

@app.context_processor
def detect_browser_language():
    """ Returns the current user browser language.
    """
    supported_browser_languages = ["en", "de"]
    lang = request.accept_languages.best_match(supported_browser_languages)
    if lang == None:
        lang = 'en'
    return dict(browser_language=lang)

@app.route('/')
@app.route('/index.html')
def index():
    """ Returns index page
    """
    return render_template('index.html')


@app.route('/blockly.html')
def blockly():
    """ Returns blockly programming page
    """
    return render_template('blockly.html')


@app.route('/editor.html')
def editor():
    """ Returns python editor page
    """
    return render_template('editor.html')


@app.route('/mobile.html')
def mobile():
    """ Returns mobile page
    """
    return render_template('mobile.html')


@app.route('/settings.html')
def settings():
    """ Returns settings page
    """
    return render_template('settings.html')


@app.route('/remote_control.html')
def remote_control():
    """ Returns remote control page
    """
    return render_template('remote_control.html')


@app.route('/API', methods=['GET', 'POST'])
def api():
    """ Returns api page or handle the request on POST
    """
    if request.method == 'POST':
        data = request.get_json(force=True)
        if not data:
            return ('Bad Request.', 400)

        return json_rpc.handle_control(data)

    return render_template('api.html')


@app.before_first_request
def before_first_reuqest():
    """ Set the eyes to green and after a while to off.
        This will gibe the user teh ability to see that the service is running.
    """
    set_led(0, 255, 0)
    time.sleep(2)
    set_led(0, 0, 0)


def check_service():
    """ Check if the page is running.
    """
    not_started = True
    while not_started:
        time.sleep(10)
        try:
            conn = httplib.HTTPConnection('localhost', json_rpc._LISTENING_PORT, timeout=1)
            conn.request('GET', '/')
            res = conn.getresponse()
            if res.status == 200:
                not_started = False
        except Exception as ex:
            pass
            # print(ex)


if __name__ == '__main__':
    """ Create the Server and listen on each incoming request.
    """
    parser = argparse.ArgumentParser(description='Start the %s web server.' % json_rpc._SERVER_NAME)
    parser.add_argument('--debug',
                        dest='debug',
                        action='store_true',
                        help='Print more debug messages on the console during running.')

    args = parser.parse_args()

    if not args.debug:
        # Reduce the log messages.
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

    # Run a thread to check the flask service.
    # thread = threading.Thread(target=check_service)
    # thread.start()
    socketio.start_background_task(target=check_service)
    socketio.run(app, host='0.0.0.0', port=json_rpc._LISTENING_PORT, debug=args.debug)
