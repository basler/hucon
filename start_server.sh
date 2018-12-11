#!/bin/sh -e
# 2018-12-11
#
# Run the python2 web server.
#
# Author: Sascha.MuellerzumHagen@baslerweb.com

SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"

# change directory
cd $SCRIPT_DIR/webserver

# start the server
python webserver.py
