#!/bin/sh -e
# start_server.sh - Run the python2 web server.
#
# Copyright (C) 2019 Basler AG
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"

EXECUTABLE=webserver.py
PARAMETERS=""
INTERPRETER=python

DEBUG=0

if [ $DEBUG != 0 ];
then
    PARAMETERS="$PARAMETERS --debug 2>/var/log/hucon_err.log >/var/log/hucon.log"
fi

if [ $( uname -a | grep -c Omega ) -eq 0 ] ;then
    PYTHONPATH="$SCRIPT_DIR/python_lib:$PYTHONPATH"
    export PYTHONPATH
fi

# change directory
cd $SCRIPT_DIR/webserver

# start the server in background
$INTERPRETER $EXECUTABLE $PARAMETERS &

HUCON_PID=$!

echo $HUCON_PID > /var/run/hucon.pid

# wait for server to stop (needed for procd-service)
wait $HUCON_PID
