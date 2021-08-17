#!/bin/bash -e
# deploy.sh - Bundle installation data into a tar.gz file and prepend it with
#             a bash script for self extracting / installation.
#
# Copyright (C) 2019 Basler AG
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

BASEDIR=`dirname "${0}"`
TMP_FILENAME=hucon-${1}.tar.gz
FILENAME=hucon-${1}.run
RELEASE_DIR=release
TEMP_DIR=$RELEASE_DIR/temp
cd "$BASEDIR"

# create release dir, create version file and copy to the release folder
mkdir -p $TEMP_DIR
echo $1 > __version__
cp LICENSE README.md code/ init.d/ python_lib/ webserver/ i2c_led.sh install.sh img_install.sh start_server.sh uninstall.sh update.sh $RELEASE_DIR/tmp

cd $TEMP_DIR
#minification of JS files
find js/ -type f \
    -name "*.js" ! -name "*.min.*" ! -name "vfs_fonts*" \
    -exec echo {} \; \
    -exec yui-compressor -o {}.min {} \; \
    -exec rm {} \; \
    -exec mv {}.min {} \;

#minification of CSS files
find css/ -type f \
    -name "*.css" ! -name "*.min.*" \
    -exec echo {} \; \
    -exec yui-compressor -o {}.min {} \; \
    -exec rm {} \; \
    -exec mv {}.min {} \;

# compress the needed files into one tar image
tar -czvf "$TMP_FILENAME" __version__ LICENSE README.md code/ init.d/ python_lib/ webserver/ i2c_led.sh install.sh img_install.sh start_server.sh uninstall.sh update.sh

mv "$TMP_FILENAME" ..

cd ..

rm -rf $TEMP_DIR

# generate a self extracting tar image
tmp=__extract__$RANDOM

printf "#!/bin/bash -e
PAYLOAD_LINE=\`awk '/^__PAYLOAD_BELOW__/ {print NR + 1; exit 0; }' \$0\`

path=/opt/hucon
if [ \$1 ]; then
    path=\"\$1\"hucon
fi

if [ -d \$path ]; then
    echo \"Remove old installation from \$path\"
    rm -rf \$path
fi

echo \"Unpack new files to \$path\"
echo \"This will take some time.\"
mkdir -p \$path | tail -n+\$PAYLOAD_LINE \$0 | tar -xzC \$path

if [ -z \$2 ] || [ \$2 != unpack ]; then
    sh \$path/install.sh
fi

exit 0
__PAYLOAD_BELOW__\n" > "$tmp"

cat "$tmp" "$TMP_FILENAME" > "$FILENAME" && rm "$tmp" && rm "$TMP_FILENAME" && rm __version__
chmod +x "$FILENAME"
sha256sum "$FILENAME"
