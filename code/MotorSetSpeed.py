from hackerschool import Motor

motor = None


HSTerm.term_exec('Set the motor to full speed forward.')
motor = Motor(2)
motor.set_speed(100)
