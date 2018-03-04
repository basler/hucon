# hackerschool
HackerSchool project

This project is using the Omega2+ microcontroller from onion.io with an integrated WiFi Module. This microcontoller is using the python and some python written modules.

The main module is the webserver, which provides a [Blockly](https://developers.google.com/blockly/) webpage with custom modules. The Custom modules are used for the hardware to build your own robotic device.

To install this project on your Omega2+ do the follwing steps on your console::

    # get the sources as tar file and un-tar it
    cd /root
    wget https://github.com/juwis/hackerschool/archive/master.tar.gz
    tar -zxvf master.tar.gz
    cd hackerschool-master
    sh install.sh
