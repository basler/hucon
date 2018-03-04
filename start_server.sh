#!/bin/sh -e

SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"

# change directory
cd $SCRIPT_DIR/webserver

# start the server
python webserver.py
