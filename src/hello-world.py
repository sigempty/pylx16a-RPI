from math import sin, cos
from pylx16a.lx16a import *
import time

LX16A.initialize("/dev/ttyUSB0", 0.1)

print ("Please input the servo ID you want to move")
id = int(input())
print ("The id is {}".format(id))

try:
    servo = LX16A(id)
    servo.set_angle_limits(0, 240)
except ServoTimeoutError as e:
    print(f"Servo {e.id_} is not responding. Exiting...")
    quit()

while True:
    degree = servo.get_physical_angle()
    print ("Before move is {}".format(degree))
    degree = float(input())
    try:
        servo.move(degree)
    except ServoTimeoutError as e:
        print(f"Servo {e.id_} is not responding. Exiting...")
        quit()
    time.sleep(1)
    try:
        degree = servo.get_physical_angle()
    except ServoTimeoutError as e:
        print(f"Servo {e.id_} is not responding. Exiting...")
        quit()
    print ("degree is moved to {}".format(degree))
 
