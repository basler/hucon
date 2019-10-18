import random

class OnionI2C(object):
	def __init__(self):
		print('[orange]I2C: init onionI2C')

	def writeByte(self, devAddress, address, value):
		print('[orange]I2C: write to device "%x" on address 0x%02x the value 0x%02x' % (devAddress, address, value))

	def readBytes(self, devAddress, address, size):
		print('[orange]I2C: read from device "%x" at address 0x%02x the amount of %d bytes' % (devAddress, address, size))
		ret_list = []
		for i in range(size):
			ret_list.append(random.randint(0, 255))

		return ret_list
