#!/usr/bin/env bash
# start_server.sh - Run the python2 web server.
#
# Copyright (C) 2019 Basler AG
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"

EXECUTABLE=webserver.py
PYTHON_PARAMETERS="-X utf8"
SCRIPT_PARAMETERS=""
INTERPRETER=python3

DEBUG=1

if [ $DEBUG != 0 ];
then
    SCRIPT_PARAMETERS="$SCRIPT_PARAMETERS --debug"
fi

if [ $( uname -a | grep -c Omega ) -eq 0 ] ;then
    PYTHONPATH="$SCRIPT_DIR/python_lib:$PYTHONPATH"
    export PYTHONPATH
fi

# change directory
cd $SCRIPT_DIR/webserver

# start the server in background
if [ $DEBUG != 0 ];
then
    echo "Starting server"
    $INTERPRETER $PYTHON_PARAMETERS $EXECUTABLE $SCRIPT_PARAMETERS >/var/log/hucon.log 2>/var/log/hucon_err.log &
else
    $INTERPRETER $PYTHON_PARAMETERS $EXECUTABLE $SCRIPT_PARAMETERS &
fi

HUCON_PID=$!

echo $HUCON_PID > /var/run/hucon.pid

# wait for server to stop (needed for procd-service)
wait $HUCON_PID
