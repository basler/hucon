#!/bin/bash
# 2018-12-11
#
# Bundle installation data into a tar.gz file and prepend it with a bash script for self extracting / installation.
#
# Author: Sascha.MuellerzumHagen@baslerweb.com

BASEDIR=`dirname "${0}"`
TMP_FILENAME=hucon-${1}.tar.gz
FILENAME=hucon-${1}.run

cd "$BASEDIR"


# compress the needed files into one tar image
echo $1 > __version__
tar -czvf "$TMP_FILENAME" __version__ README.md code/ init.d/ python_lib/ webserver/ i2c_led.sh install.sh img_install.sh start_server.sh uninstall.sh update.sh

# generate a self extracting tar image
tmp=__extract__$RANDOM

printf "#!/bin/sh
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

if [ -z $2 ] || [ $2 != unpack ]; then
    sh \$path/install.sh
fi

exit 0
__PAYLOAD_BELOW__\n" > "$tmp"

cat "$tmp" "$TMP_FILENAME" > "$FILENAME" && rm "$tmp" && rm "$TMP_FILENAME" && rm __version__
chmod +x "$FILENAME"
sha256sum "$FILENAME"
