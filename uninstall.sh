#!/bin/sh -e

# remove the hs_py_lib into the site packages
rm /usr/lib/python2.7/site-packages/hs_py_lib

# add the server to start at boot
sed -i '/hs_start_server.sh/d' /etc/rc.local
