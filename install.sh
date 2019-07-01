#!/bin/sh -e
# 2018-12-11
#
# Install all packages and copy bundled files.
#
# Author: Sascha.MuellerzumHagen@baslerweb.com

SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"

# add the hackerschool to the site packages (only for old code)
if [ -L $1/usr/lib/python2.7/site-packages/hackerschool ]; then
	rm $1/usr/lib/python2.7/site-packages/hackerschool
fi
ln -s "/opt/hucon/python_lib" $1/usr/lib/python2.7/site-packages/hackerschool

# add the hucon to the site packages
if [ -L $1/usr/lib/python2.7/site-packages/hucon ]; then
	rm $1/usr/lib/python2.7/site-packages/hucon
fi
ln -s "/opt/hucon/python_lib" $1/usr/lib/python2.7/site-packages/hucon
