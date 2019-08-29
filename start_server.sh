#!/bin/sh -e
# 2018-12-11
#
# Run the python2 web server.
#
# Author: Sascha.MuellerzumHagen@baslerweb.com

SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"

EXECUTABLE=webserver.py
PARAMETERS=""
INTERPRETER=python

DEBUG=0

if [ $DEBUG != 0 ];
then
        PARAMETERS=$PARAMETERS + " 2>/var/log/hucon_err.log >/var/log/hucon.log"
fi

# change directory
cd $SCRIPT_DIR/webserver

# start the server in background
$INTERPRETER $EXECUTABLE $PARAMETERS &

HUCON_PID=$!

echo $HUCON_PID > /var/run/hucon.pid

# wait for server to stop (needed for procd-service)
wait $HUCON_PID
