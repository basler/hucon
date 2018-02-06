#!/bin/sh -e

SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"

# update the system
opkg update

# install needed packages
opkg install python python-light pyOnionI2C pyPwmExp libonioni2c
opkg upgrade libonioni2c pyOnionI2C

# insert the python interpreter for the cgi-modules
grep -q 'list interpreter' /etc/config/uhttpd || sed -i "/^config uhttpd 'main'/a \\        list interpreter '.py=/usr/bin/python3'
" /etc/config/uhttpd

# and restart the micro http deamon
/etc/init.d/uhttpd restart

# add the hs_py_lib to the site packages
ln -s "$SCRIPT_DIR/hs_py_lib" /usr/lib/python2.7/site-packages/hs_py_lib

# add the server to start at boot
sed -i '/hs_start_server.sh/d' /etc/rc.local
sed -i "/^exit 0/i sh $SCRIPT_DIR/hs_start_server.sh" /etc/rc.local
