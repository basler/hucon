#!/bin/bash -e
# update.sh - Update the system or return the latest released version from github.
#
# Copyright (C) 2019 Basler AG
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"

UPDATE_SOURCE_REPO=JonasTrampe/hucon

while :; do
    case $1 in
        -c|--check) do_check=1
        ;;
        -b|--beta) use_beta=1
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

# get the list of all available versions and sort the list
versions=$(curl --silent "https://api.github.com/repos/$UPDATE_SOURCE_REPO/releases" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/' | sort -r)

# determine the latest version based on the settings from the command line
# Go through the list and check the version string for a 'b'-char which marks a beta version.
# Stop if the version is marked as beta and the user will also see the beta version.
# Otherwise go to the next string to find a released version.
for version in $versions
do

    case "$version" in
        *b*)
            if [ $use_beta ]; then
                echo "The latest version is a beta version."
                latestVersion=$version
                break
            else
                continue
            fi
    esac

    latestVersion=$version
    break
done

currentVersion="0.0.0"

if [ -f $SCRIPT_DIR/__version__ ]; then
    currentVersion=$(cat $SCRIPT_DIR/__version__)
fi

# Print the latest version.
if [ $do_check ]; then
    if [ "$latestVersion" != "" ]; then

        echo "Your version is: $currentVersion"
        echo "The latest version is: $latestVersion"

        result=$(/bin/bash version_compare.sh "${currentVersion}" "${latestVersion}")

        if [ "${result}" -eq 0 ]; then
            echo "There is no new version!"
        elif  [ "${result}" -eq 1 ]; then
             echo "Your version is newer than the available version!"
        elif  [ "${result}" -eq 2 ]; then
            echo "There is a new stable version!"
        elif  [ "${result}" -eq 3 ]; then
            echo "You have an unstable version, but hey it's the newest one"
        elif  [ "${result}" -eq 4 ]; then
            echo "Your unstable version is newer than the available version!"
        elif  [ "${result}" -eq 5 ]; then
            echo "There is a new unstable (alpha/beta/rc) version! It is highly experimental and discouraged to be installed!"
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
        downloadUrl="https://github.com/$UPDATE_SOURCE_REPO/releases/download/$latestVersion/hucon-$latestVersion.run"

        # Download the new package
        wget $downloadUrl -O hucon.run

        echo "Check if existing code can be moved to /root/hucon/code..."
        if [[ ! -e /root/hucon/code ]]; then
            echo "Copying existing code to /root/hucon/code..."
            cp -r ./code /root/hucon/
        fi

        if [[ -e /root/hucon/code/examples ]]; then
            echo "Removing old examples - new ones will be sourced from the /opt/hucon/code/examples folder..."
            rm -rf /root/hucon/code/examples
        fi

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
