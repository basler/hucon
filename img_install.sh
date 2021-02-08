#!/bin/sh -e
# img_install.sh - Install all packages and copy bundled files.
#
# Copyright (C) 2019 Basler AG
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"

# add the hackerschool to the site packages (only for old code)
if [ -L $1/usr/lib/python3.6/site-packages/hackerschool ]; then
    rm $1/usr/lib/python3.6/site-packages/hackerschool
fi
ln -s "/opt/hucon/python_lib" $1/usr/lib/python3.6/site-packages/hackerschool

# add the hucon to the site packages
if [ -L $1/usr/lib/python3.6/site-packages/hucon ]; then
    rm $1/usr/lib/python3.6/site-packages/hucon
fi
ln -s "/opt/hucon/python_lib" $1/usr/lib/python3.6/site-packages/hucon
