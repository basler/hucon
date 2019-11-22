""" Print the gyro sensor data.

    Copyright (C) 2019 Basler AG
    All rights reserved.

    This software may be modified and distributed under the terms
    of the BSD license.  See the LICENSE file for details.
"""

from hucon import Mpu6050

mpu = None


print('Get the data from the accelerometer.')
mpu = Mpu6050()
print(mpu.get_accel_data())
