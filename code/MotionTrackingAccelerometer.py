from hackerschool import Mpu6050

mpu = None


HSTerm.term_exec('Get the data from the accelerometer.')
mpu = Mpu6050()
HSTerm.term_exec(mpu.get_accel_data())
