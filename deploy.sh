#!/bin/bash
BASEDIR=`dirname "${0}"`
cd "$BASEDIR"

# compress the needed files into one tar image
echo $1 >> __version__
tar -czvf hackerschool.tar.gz __version__ README.md code/ install.sh python_lib/ start_server.sh uninstall.sh webserver/

# generate a self extracting tar image
tmp=__extract__$RANDOM

printf "#!/bin/bash
PAYLOAD_LINE=\`awk '/^__PAYLOAD_BELOW__/ {print NR + 1; exit 0; }' \$0\`
path=/root/hackerschool
if [ \$1 ]
then
    path=\"\$1\"hackerschool
fi

mkdir -p \$path | tail -n+\$PAYLOAD_LINE \$0 | tar -xvzC \$path

sh \$path/install.sh

exit 0
__PAYLOAD_BELOW__\n" > "$tmp"

cat "$tmp" "hackerschool.tar.gz" > "hackerschool.run" && rm "$tmp" && rm "hackerschool.tar.gz"
chmod +x "hackerschool.run"