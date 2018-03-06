#!/bin/sh -e

while :; do
    case $1 in
        -c|--check) check=1
        ;;
        -r|--reboot) do_reboot=1
        ;;
        *) break
    esac
    shift
done

# Get the latest/current version from the website.
latestVersion=$(curl https://github.com/juwis/hackerschool/releases/latest 2>/dev/null | sed "s/[a-zA-Z<> \"\/=:]//g" | sed "s/^\.//g" | sed "s/\.$//g")
currentVersion=$(cat __version__)

# Print the latest version.
if [ $check ]
then
    echo $latestVersion
    exit 0
fi

# Update the package?
if [ "$latestVersion" != "$currentVersion" ]
then
    echo "Update the system from $currentVersion to $latestVersion"
    downloadUrl="https://github.com/juwis/hackerschool/releases/download/$latestVersion/hackerschool.run"

    # Download the new package
    wget $downloadUrl

    # and install it.
    sh hackerschool.run
fi

# Reboot the system if needed.
if [ $do_reboot ]
then
    echo "Reboot the system ..."
    reboot
fi