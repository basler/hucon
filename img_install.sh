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
ln -s "/opt/hucon/python_lib" $1/usr/lib/python3.6/site-packages/hackerschool

ln -s "/opt/hucon/python_lib/hucon" $1/usr/lib/python3.6/site-packages/hucon
