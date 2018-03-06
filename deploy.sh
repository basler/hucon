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
mkdir hackerschool | tail -n+\$PAYLOAD_LINE \$0 | tar -xvzC ./hackerschool

sh hackerschool/install.sh

exit 0
__PAYLOAD_BELOW__\n" > "$tmp"

cat "$tmp" "hackerschool.tar.gz" > "hackerschool.run" && rm "$tmp"
chmod +x "hackerschool.run"