#!/usr/bin/env python
""" 2019-01-16

Driver module for PCA9685

Author: Sascha.MuellerzumHagen@baslerweb.com
"""

import time
from OmegaExpansion import onionI2C

# Set of all addresses which are successfully initialized.
_INITIALIZED_DRIVER = set()


class PCA9685(object):
    """ Class to to handle multiple initialization from the PCA9685 at the same time.
        This class will setup the PCA9685 once the first 'init' function is called.
        After that, the setup routine will not called any more.
    """

    _address = None
    _i2c = None

    _MODE1 = 0x00
    _MODE2 = 0x01
    _PRESCALE = 0xFE

    _LED0_ON_L = 0x06
    _ALL_LED_ON_L = 0xFA

    def __init__(self, address):
        """ Initialize the module and the PCS9685 driver if this is not initialized at the moment.
        """
        global _INITIALIZED_DRIVER

        self._address = address
        self._i2c = onionI2C.OnionI2C()

        # Initialize the PCA9685 for the first time.
        if self._address not in _INITIALIZED_DRIVER:
            self._setup()
            _INITIALIZED_DRIVER.add(self._address)


    def _setup(self):
        """ Set the PCA into a working state.
        """
        self.set_all_channel(0)

        # Set default Mode2 register
        self._i2c.writeByte(self._address, self._MODE2, 0x04)

        # Set sleep on.
        self._i2c.writeByte(self._address, self._MODE1, 0x11)

        # Set a frequency of 50 Hz
        # pre-scale = round(25Mhz/(4096*50Hz))-1 = 121
        self._i2c.writeByte(self._address, self._PRESCALE, 121)

        # Release sleep.
        self._i2c.writeByte(self._address, self._MODE1, 0x01)

        time.sleep(0.005)

        # Reset device.
        self._i2c.writeByte(self._address, self._MODE1, 0x81)


    def set_channel(self, channel, value):
        """ Write the specific channel
        """
        if channel not in range(16):
            raise Exception('The channel must be in range from 0 to 15!')
        if value not in range(4096):
            raise Exception('The value must be in range from 0 to 4095!')

        register_address = self._LED0_ON_L + channel * 4

        # Set the on always to 0 and the off value will set the duration of the on state.
        self._i2c.writeByte(self._address, register_address + 0, 0)
        self._i2c.writeByte(self._address, register_address + 1, 0)
        self._i2c.writeByte(self._address, register_address + 2, value & 0xFF)
        self._i2c.writeByte(self._address, register_address + 3, value >> 8)

    def set_all_channel(self, value):
        """ Write to all channels with the write ALL_LED register.
        """
        if value not in range(4096):
            raise Exception('The value must be in range from 0 to 4095!')

        # Set the on always to 0 and the off value will set the duration of the on state.
        self._i2c.writeByte(self._address, self._ALL_LED_ON_L + 0, 0)
        self._i2c.writeByte(self._address, self._ALL_LED_ON_L + 1, 0)
        self._i2c.writeByte(self._address, self._ALL_LED_ON_L + 2, value & 0xFF)
        self._i2c.writeByte(self._address, self._ALL_LED_ON_L + 3, value >> 8)


if __name__ == '__main__':

    pwm = PCA9685(0x4A)

    for cha in range(16):
        print 'Channel %d\n' % cha
        pwm.set_channel(cha, 255)
        time.sleep(1)

    pwm.set_all_channel(0)
