#!/usr/bin/env python3
import os
from glob import glob

# List of all files which should be removed.
files_to_remove = [
    # uglified files
    '../webserver/www/js/webserver.blockly.min.js',
    '../webserver/www/js/webserver.ace.min.js',
    # gzipped files
    '../webserver/www/css/main.css.gz',
    '../webserver/www/ace/ace.js.gz',
    '../webserver/www/ace/mode-python.js.gz',
    '../webserver/www/ace/theme-tomorrow_night.js.gz',
    '../webserver/www/blockly/blockly_compressed.js.gz',
    '../webserver/www/blockly/blocks_compressed.js.gz',
    '../webserver/www/blockly/en.js.gz',
    '../webserver/www/blockly/python_compressed.js.gz',
    '../webserver/www/blockly/python_compressed.js.gz',
    '../webserver/www/docReady/docready.js.gz',
    '../webserver/www/js/webserver.blockly.min.js.gz',
    '../webserver/www/js/webserver.ace.min.js.gz',
    '../webserver/www/xml/toolbox.xml.gz'
]

# List of all files which should be gzipped.
files_to_gzip = [
    '../webserver/www/ace/ace.js',
    '../webserver/www/ace/mode-python.js',
    '../webserver/www/ace/theme-tomorrow_night.js',
    '../webserver/www/blockly/blockly_compressed.js',
    '../webserver/www/blockly/blocks_compressed.js',
    '../webserver/www/blockly/en.js',
    '../webserver/www/blockly/python_compressed.js',
    '../webserver/www/blockly/python_compressed.js',
    '../webserver/www/css/main.css',
    '../webserver/www/docReady/docready.js',
    '../webserver/www/js/webserver.blockly.min.js',
    '../webserver/www/js/webserver.ace.min.js',
    '../webserver/www/xml/toolbox.xmz'
]

# remove all uglified files
print('Removing files:')
for filename in files_to_remove:
    if os.path.exists(filename):
        print('  %s' % filename)
        os.remove(filename)

# uglify the javascript files
print('Uglify JS files:')
print('  ../webserver/www/js/webserver.blockly.min.js')
os.system('uglifyjs -c \
    -o ../webserver/www/js/webserver.blockly.min.js \
    ../webserver/www/js/custom_blocks_machine.js \
    ../webserver/www/js/custom_blocks_neopixel.js \
    ../webserver/www/js/custom_blocks_servo.js \
    ../webserver/www/js/webserver_blockly.js \
    ../webserver/www/js/webserver_functions.js')

print('  ../webserver/www/js/webserver.ace.min.js')
os.system('uglifyjs -c \
    -o ../webserver/www/js/webserver.ace.min.js \
    ../webserver/www/js/webserver_ace.js \
    ../webserver/www/js/webserver_functions.js')

# gzip all files
print('GZip files:')
for filename in files_to_gzip:
    if os.path.exists(filename):
        print('  %s' % filename)
        os.system('gzip -k -f %s' % filename)
