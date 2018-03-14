![Hacker School](webserver/www/images/Logo.svg)

This project was created to teach children about programming on a self-built robot.
The base is the Omega2+ from www.onion.io. In addition to WLAN and the integrated python, this offers a good basis.


This project was is using the Omega2+ microcontroller from onion.io with an integrated WiFi Module. This microcontoller is using the python and some python written modules.

The main module is the webserver, which provides a [Blockly](https://developers.google.com/blockly/) webpage with custom modules. The Custom modules are used for the hardware to build your own robotic device. A python webserver with a Blockly interface was installed on it.

## Installation
To install this project on your Omega2+, do the follwing steps on your console::

    # get the sources and install it
    wget k https://github.com/juwis/hackerschool/releases/download/[ReleaseName]/hackerschool.run
    sh hackerschool.run

## Usage
After restarting the system, the webserver is started automatically. Visit http://Omega-ABCD.local:8080 with a browser. ABCD must be replaced with the last four characters of your device's MAC address.
