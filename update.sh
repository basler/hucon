#!/bin/sh -e
# 2018-12-11
#
# Update the system or return the latest released version from github.
#
# Author: Sascha.MuellerzumHagen@baslerweb.com

SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"

while :; do
    case $1 in
        -c|--check) do_check=1
        ;;
        -u|--update) do_update=1
        ;;
        -r|--reboot) do_reboot=1
        ;;
        -s|--shutdown) do_shutdown=1
        ;;
        *) break
    esac
    shift
done

# Get the latest/current version from the website.
latestVersion=$(curl -k https://github.com/juwis/hackerschool/releases/latest 2>/dev/null | sed "s/[a-zA-Z<> \"\/=:]//g" | sed "s/^\.//g" | sed "s/\.$//g")
currentVersion="unknown"

if [ -f $SCRIPT_DIR/__version__ ]; then
    currentVersion=$(cat $SCRIPT_DIR/__version__)
fi

# Print the latest version.
if [ $do_check ]; then
    if [ "$latestVersion" != "" ]; then
        echo "The latest version is: $latestVersion"
        if [ "$latestVersion" != "$currentVersion" ]; then
            echo "There is an update available."
            exit 1
        else
            echo "You are using the up to date version."
        fi
    else
        echo "Could not read the version from github."
    fi
fi

# Update the package?
if [ $do_update ]; then
    if [ "$latestVersion" != "$currentVersion" ]; then
        echo "Update the system from $currentVersion to $latestVersion"

        # remove the old package if needed.
        if [ -f hucon.run ]; then
            rm hucon.run
        fi

        # download the new package
        downloadUrl="https://github.com/juwis/hackerschool/releases/download/$latestVersion/hucon.run"

        # Download the new package
        wget $downloadUrl

        # and install it.
        sh hucon.run
    else
        echo "You are using the up to date version."
    fi
fi

# Reboot the system if needed.
if [ $do_reboot ]; then
    echo "Reboot the system, wait untile the server is started ..."
    reboot
fi

# Shutdown the system.
if [ $do_shutdown ]; then
    echo "Shutdown the system ..."
    sleep 2
    echo "o" >/proc/sysrq-trigger
fi
