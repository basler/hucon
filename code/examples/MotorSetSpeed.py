from hucon import Motor

motor = None


print('Set the motor to full speed forward.')
motor = Motor(2)
motor.set_speed(100)
