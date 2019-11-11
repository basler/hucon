#!/bin/sh -e
# uninstall.sh - Remove all hucon files from the system.
#
# Copyright (C) 2019 Basler AG
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

# remove the hackerschool into the site packages
if [ -L /usr/lib/python2.7/site-packages/hackerschool ]; then
    rm /usr/lib/python2.7/site-packages/hackerschool
fi

# remove the hucon into the site packages
if [ -L /usr/lib/python2.7/site-packages/hucon ]; then
    rm /usr/lib/python2.7/site-packages/hucon
fi

# remove the i2c_led hucon into the site packages
if [ -L /etc/init.d/i2c_led ]; then
    rm /etc/init.d/i2c_led
fi

# remove the server to start at boot
sed -i '/start_server.sh/d' /etc/rc.local
