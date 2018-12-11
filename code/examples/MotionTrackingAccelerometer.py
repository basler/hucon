""" 2018-12-11

Print the gyro sensor data.

Author: Sascha.MuellerzumHagen@baslerweb.com
"""

from hucon import Mpu6050

mpu = None


print('Get the data from the accelerometer.')
mpu = Mpu6050()
print(mpu.get_accel_data())
