#!/bin/sh -e

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
