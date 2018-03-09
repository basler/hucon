#!/bin/sh -e

SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"

while :; do
    case $1 in
        -c|--check) do_check=1
        ;;
        -u|--update) do_update=1
        ;;
        -r|--reboot) do_reboot=1
        ;;
        *) break
    esac
    shift
done

# Get the latest/current version from the website.
latestVersion=$(curl https://github.com/juwis/hackerschool/releases/latest 2>/dev/null | sed "s/[a-zA-Z<> \"\/=:]//g" | sed "s/^\.//g" | sed "s/\.$//g")
currentVersion="unknown"

if [ -f $SCRIPT_DIR/__version__ ]; then
    currentVersion=$(cat $SCRIPT_DIR/__version__)
fi

# Print the latest version.
if [ $do_check ]; then
    echo "The latest version is: $latestVersion"
fi

# Update the package?
if [ $do_update ]; then
    if [ "$latestVersion" != "$currentVersion" ]; then
        echo "Update the system from $currentVersion to $latestVersion"
        downloadUrl="https://github.com/juwis/hackerschool/releases/download/$latestVersion/hackerschool.run"

        # Download the new package
        wget $downloadUrl

        # and install it.
        sh hackerschool.run
    else
        echo "You are using the up to date version."
        exit 1
    fi
fi

# Reboot the system if needed.
if [ $do_reboot ]; then
    echo "Reboot the system ..."
    reboot
fi
