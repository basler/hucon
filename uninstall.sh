#!/bin/sh -e

# remove the hackerschool into the site packages
rm /usr/lib/python2.7/site-packages/hackerschool

# add the server to start at boot
sed -i '/start_server.sh/d' /etc/rc.local
