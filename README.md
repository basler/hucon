![Hacker School](webserver/static/images/Logo.svg)

This project was created to teach children about programming on a self-built robot.
The base is the Omega2+ from www.onion.io. In addition to WLAN and the integrated python, this offers a good basis.


This project was is using the Omega2+ microcontroller from onion.io with an integrated WiFi Module. This microcontroller is using the python and some python written modules.

The main module is the web server, which provides a [Blockly](https://developers.google.com/blockly/) web page with custom modules. The Custom modules are used for the hardware to build your own robotic device. A python web server with a Blockly interface was installed on it.

## Installation
To install this project on your Omega2+, do the following steps on your console::

    # get the sources and install it
    curl -s https://api.github.com/repos/juwis/hackerschool/releases/latest \
        | grep -oP '"browser_download_url": "\K(.*)(?=")' \
        | wget -

    wget https://github.com/juwis/hackerschool/releases/download/[ReleaseName]/hucon.run
    sh hucon.run

## Usage
After restarting the system, the web server is started automatically. Visit http://Omega-ABCD.local:8080 with a browser. ABCD must be replaced with the last four characters of your device's MAC address.

## TODO

- [x] Support folder to save the code. (File explorer)
- [x] Make the examples read only.
- [x] Ask the server if there is a running application on page load to set the buttons correctly.
- [ ] The menu bar is to big for a smart phone device.
- [x] Create a block for the events.
- [x] Check the maximum size for the events array.
- [x] Define a proper interface for the events list to use more complex button types.