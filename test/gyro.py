from Adafruit_BNO055 import BNO055
import time

bno = BNO055.BNO055(serial_port='/dev/ttyAMA0', rst=18)

if not bno.begin():
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')
sys, gyro, accel, mag = bno.get_calibration_status()
status, self_test, error = bno.get_system_status()
print('System status: {0}'.format(status))
print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
# Print out an error if system status is in error mode.
if status == 0x01:
    print('System error: {0}'.format(error))
    print('See datasheet section 4.3.59 for the meaning.')

while True:
    Ll= bno.read_linear_acceleration()
    L= bno.read_quaternion()#w,x,y,z =
    print(L)
    print(Ll)
    time.sleep(0.001)