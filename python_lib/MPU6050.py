"""This program handles the communication over I2C
between a Raspberry Pi and a MPU-6050 Gyroscope / Accelerometer combo.
Made by: MrTijn/Tijndagamer
Released under the MIT License
Copyright (c) 2015, 2016, 2017 MrTijn/Tijndagamer
**********************************************************************
* Sascha Mueller zum Hagen:
* Adapted to work with the onion Omega2+ Board
**********************************************************************
"""

from OmegaExpansion import onionI2C

class Mpu6050(object):
    """ Gyroscope class.
    """

    # Global Variables
    GRAVITIY_MS2 = 9.80665
    address = None
    i2c = None

    # Scale Modifiers
    ACCEL_SCALE_MODIFIER_2G = 16384.0
    ACCEL_SCALE_MODIFIER_4G = 8192.0
    ACCEL_SCALE_MODIFIER_8G = 4096.0
    ACCEL_SCALE_MODIFIER_16G = 2048.0

    GYRO_SCALE_MODIFIER_250DEG = 131.0
    GYRO_SCALE_MODIFIER_500DEG = 65.5
    GYRO_SCALE_MODIFIER_1000DEG = 32.8
    GYRO_SCALE_MODIFIER_2000DEG = 16.4

    # Pre-defined ranges
    ACCEL_RANGE_2G = 0x00
    ACCEL_RANGE_4G = 0x08
    ACCEL_RANGE_8G = 0x10
    ACCEL_RANGE_16G = 0x18

    GYRO_RANGE_250DEG = 0x00
    GYRO_RANGE_500DEG = 0x08
    GYRO_RANGE_1000DEG = 0x10
    GYRO_RANGE_2000DEG = 0x18

    # MPU-6050 Registers
    PWR_MGMT_1 = 0x6B
    PWR_MGMT_2 = 0x6C

    ACCEL_XOUT0 = 0x3B
    ACCEL_YOUT0 = 0x3D
    ACCEL_ZOUT0 = 0x3F

    TEMP_OUT0 = 0x41

    GYRO_XOUT0 = 0x43
    GYRO_YOUT0 = 0x45
    GYRO_ZOUT0 = 0x47

    ACCEL_CONFIG = 0x1C
    GYRO_CONFIG = 0x1B

    def __init__(self, address=0x68):
        self.address = address
        self.i2c = onionI2C.OnionI2C()
        # Wake up the MPU-6050 since it starts in sleep mode
        self.i2c.writeByte(self.address, self.PWR_MGMT_1, 0x00)

    # I2C communication methods

    def read_i2c_word(self, register):
        """ Read two i2c registers and combine them.

        register -- the first register to read from.
        Returns the combined read results.
        """
        # Read the data from the registers
        value = self.i2c.readBytes(self.address, register, 2)
        value = (value[0] << 8) + value[1]

        if value >= 0x8000:
            return -((65535 - value) + 1)

        return value

    # MPU-6050 Methods

    def get_temp(self):
        """Reads the temperature from the onboard temperature sensor of the MPU-6050.

        Returns the temperature in degrees Celcius.
        """
        raw_temp = self.read_i2c_word(self.TEMP_OUT0)

        # Get the actual temperature using the formule given in the
        # MPU-6050 Register Map and Descriptions revision 4.2, page 30
        actual_temp = (raw_temp / 340.0) + 36.53

        return actual_temp

    def set_accel_range(self, accel_range):
        """Sets the range of the accelerometer to range.

        accel_range -- the range to set the accelerometer to. Using a
        pre-defined range is advised.
        """
        # First change it to 0x00 to make sure we write the correct value later
        self.i2c.writeByte(self.address, self.ACCEL_CONFIG, 0x00)

        # Write the new range to the ACCEL_CONFIG register
        self.i2c.writeByte(self.address, self.ACCEL_CONFIG, accel_range)

    def read_accel_range(self, raw=False):
        """Reads the range the accelerometer is set to.

        If raw is True, it will return the raw value from the ACCEL_CONFIG
        register
        If raw is False, it will return an integer: -1, 2, 4, 8 or 16. When it
        returns -1 something went wrong.
        """
        raw_data = self.i2c.readBytes(self.address, self.ACCEL_CONFIG, 1)[0]

        if raw is True:
            return raw_data
        elif raw is False:
            if raw_data == self.ACCEL_RANGE_2G:
                return 2
            elif raw_data == self.ACCEL_RANGE_4G:
                return 4
            elif raw_data == self.ACCEL_RANGE_8G:
                return 8
            elif raw_data == self.ACCEL_RANGE_16G:
                return 16

        return -1

    def get_accel_data(self, gravity=False):
        """Gets and returns the X, Y and Z values from the accelerometer.

        If g is True, it will return the data in g
        If g is False, it will return the data in m/s^2
        Returns a dictionary with the measurement results.
        """
        x_axis = self.read_i2c_word(self.ACCEL_XOUT0)
        y_axis = self.read_i2c_word(self.ACCEL_YOUT0)
        z_axis = self.read_i2c_word(self.ACCEL_ZOUT0)

        accel_scale_modifier = None
        accel_range = self.read_accel_range(True)

        if accel_range == self.ACCEL_RANGE_2G:
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_2G
        elif accel_range == self.ACCEL_RANGE_4G:
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_4G
        elif accel_range == self.ACCEL_RANGE_8G:
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_8G
        elif accel_range == self.ACCEL_RANGE_16G:
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_16G
        else:
            print 'Unkown range - accel_scale_modifier set to self.ACCEL_SCALE_MODIFIER_2G'
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_2G

        x_axis = x_axis / accel_scale_modifier
        y_axis = y_axis / accel_scale_modifier
        z_axis = z_axis / accel_scale_modifier

        if gravity is True:
            return {'x': x_axis, 'y': y_axis, 'z': z_axis}

        x_axis = x_axis * self.GRAVITIY_MS2
        y_axis = y_axis * self.GRAVITIY_MS2
        z_axis = z_axis * self.GRAVITIY_MS2
        return {'x': x_axis, 'y': y_axis, 'z': z_axis}

    def set_gyro_range(self, gyro_range):
        """Sets the range of the gyroscope to range.

        gyro_range -- the range to set the gyroscope to. Using a pre-defined
        range is advised.
        """
        # First change it to 0x00 to make sure we write the correct value later
        self.i2c.writeByte(self.address, self.GYRO_CONFIG, 0x00)

        # Write the new range to the ACCEL_CONFIG register
        self.i2c.writeByte(self.address, self.GYRO_CONFIG, gyro_range)

    def read_gyro_range(self, raw=False):
        """Reads the range the gyroscope is set to.

        If raw is True, it will return the raw value from the GYRO_CONFIG
        register.
        If raw is False, it will return 250, 500, 1000, 2000 or -1. If the
        returned value is equal to -1 something went wrong.
        """
        raw_data = self.i2c.readBytes(self.address, self.GYRO_CONFIG, 1)[0]

        if raw is True:
            return raw_data
        elif raw is False:
            if raw_data == self.GYRO_RANGE_250DEG:
                return 250
            elif raw_data == self.GYRO_RANGE_500DEG:
                return 500
            elif raw_data == self.GYRO_RANGE_1000DEG:
                return 1000
            elif raw_data == self.GYRO_RANGE_2000DEG:
                return 2000

        return -1

    def get_gyro_data(self):
        """Gets and returns the X, Y and Z values from the gyroscope.

        Returns the read values in a dictionary.
        """
        x_axis = self.read_i2c_word(self.GYRO_XOUT0)
        y_axis = self.read_i2c_word(self.GYRO_YOUT0)
        z_axis = self.read_i2c_word(self.GYRO_ZOUT0)

        gyro_scale_modifier = None
        gyro_range = self.read_gyro_range(True)

        if gyro_range == self.GYRO_RANGE_250DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_250DEG
        elif gyro_range == self.GYRO_RANGE_500DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_500DEG
        elif gyro_range == self.GYRO_RANGE_1000DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_1000DEG
        elif gyro_range == self.GYRO_RANGE_2000DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_2000DEG
        else:
            print 'Unkown range - gyro_scale_modifier set to self.GYRO_SCALE_MODIFIER_250DEG'
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_250DEG

        x_axis = x_axis / gyro_scale_modifier
        y_axis = y_axis / gyro_scale_modifier
        z_axis = z_axis / gyro_scale_modifier

        return {'x': x, 'y': y, 'z': z}

if __name__ == "__main__":
    mpu = Mpu6050()
    print 'Temperatur: %0.2f' % mpu.get_temp()

    accel_data = mpu.get_accel_data()
    print '\nAccelerometer Data'
    print 'x: %0.2f' % accel_data['x']
    print 'y: %0.2f' % accel_data['y']
    print 'z: %0.2f' % accel_data['z']

    gyro_data = mpu.get_gyro_data()
    print '\nGyroscope Data'
    print 'x: %0.2f' % gyro_data['x']
    print 'y: %0.2f' % gyro_data['y']
    print 'z: %0.2f' % gyro_data['z']
