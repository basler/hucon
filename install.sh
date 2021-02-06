#!/bin/bash -e
# install.sh - Install all packages and copy bundled files.
#
# Copyright (C) 2019 Basler AG
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

echo "Hucon-webserver installation started"

# update the system
echo "Update the system"
opkg update

# install needed packages
echo "Install needed packages"
opkg install curl python-light python-pip pyOnionI2C
pip install flask flask-socketio

echo "Linking new libraries"
# add the hackerschool to the site packages (only for old code)
if [[ -L /usr/lib/python3.6/site-packages/hackerschool ]]; then
    rm /usr/lib/python3.6/site-packages/hackerschool
fi
ln -s "/opt/hucon/python_lib/hucon" /usr/lib/python3.6/site-packages/hackerschool

# add the hucon to the site packages
if [[ -L /usr/lib/python3.6/site-packages/hucon ]]; then
    rm /usr/lib/python3.6/site-packages/hucon
fi
ln -s "/opt/hucon/python_lib/hucon" /usr/lib/python3.6/site-packages/hucon

echo "Removing old server startup"
sed -i '/start_server.sh/d' /etc/rc.local

if [[ -e /etc/init.d/HuconWebserver ]]; then
    /etc/init.d/HuconWebserver disable
    rm /etc/init.d/HuconWebserver
fi

echo "Deploying new server startup"
cp /opt/hucon/init.d/HuconWebserver /etc/init.d/HuconWebserver
chmod +x /etc/init.d/HuconWebserver
/etc/init.d/HuconWebserver enable

echo "Removing old i2c startup"
if [[ -e /etc/init.d/i2c_led ]] || [[ -e /etc/init.d/I2C_led ]]; then
    if [[ -e /etc/init.d/i2c_led ]]; then
        /etc/init.d/i2c_led disable
        rm /etc/init.d/i2c_led
    else
        /etc/init.d/I2C_led disable
        rm /etc/init.d/I2C_led
    fi
fi

echo "Deploying new I2C/Eyes startup"
cp /opt/hucon/init.d/I2C_led /etc/init.d/I2C_led
chmod +x /etc/init.d/I2C_led
/etc/init.d/I2C_led enable

echo "Install finished"