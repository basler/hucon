#!/usr/bin/python
""" 2018-12-11

Flask based web server to handle all legal requests.

Author: Sascha.MuellerzumHagen@baslerweb.com
"""

import argparse
import logging
from flask import Flask
from flask import abort
from flask import request
from flask import Response
from flask import render_template
from functools import wraps

from HuConJsonRpc import HuConJsonRpc

json_rpc = HuConJsonRpc()

app = Flask(json_rpc._SERVER_NAME)


def check_auth(username, password):
    """ This function is called to check if a user-name /
        password combination is valid.
    """
    return username == 'hucon' and password == 'robot'


def authenticate():
    """ Sends a 401 response that enables basic auth
    """
    return Response('You have to login',
                    401,
                    {'WWW-Authenticate': 'Basic realm="%s"' % json_rpc._SERVER_NAME})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/blockly.html')
# @requires_auth
def blockly():
    return render_template('blockly.html')


@app.route('/editor.html')
# @requires_auth
def editor():
    return render_template('editor.html')


@app.route('/mobile.html')
# @requires_auth
def mobile():
    return render_template('mobile.html')


@app.route('/settings.html')
def settings():
    return render_template('settings.html')


@app.route('/remote_control.html')
def remote_control():
    return render_template('remote_control.html')


@app.route('/API', methods=['GET', 'POST'])
def api():
    if request.method == 'POST':
        data = request.get_json(force=True)
        if not data:
            return ('Bad Request.', 400)

        return json_rpc.handle_control(data)
    else:
        return render_template('api.html')


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

    app.run(host='0.0.0.0', port=json_rpc._LISTENING_PORT, debug=args.debug)
