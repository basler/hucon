#!/bin/sh -e
# 2018-12-11
#
# Remove all hucon files from the system.
#
# Author: Sascha.MuellerzumHagen@baslerweb.com

# remove the hackerschool into the site packages
if [ -f /usr/lib/python2.7/site-packages/hackerschool ]; then
    rm /usr/lib/python2.7/site-packages/hackerschool
fi

# remove the hucon into the site packages
if [ -f /usr/lib/python2.7/site-packages/hucon ]; then
    rm /usr/lib/python2.7/site-packages/hucon
fi

# add the server to start at boot
sed -i '/start_server.sh/d' /etc/rc.local
