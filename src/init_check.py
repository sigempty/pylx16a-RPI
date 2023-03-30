from math import sin, cos
from pylx16a.lx16a import *
import time

LX16A.initialize("/dev/ttyUSB0", 0.1)
def InitOnCheckStatus(num: int):
    servos = []
    targets = []
    for i in range(0, num, 1):
        try:
            servo = LX16A(i+1) 
            servo.set_angle_limits(0, 240)
            if servo != None:
                angle = servo.get_physical_angle()
                print ("servo {}'s current angle is {}".format(i+1, angle))
                servos.append(servo)
                targets.append(angle)
        except ServoTimeoutError as e:
            print(f"Servo {e.id_} is not responding. Exiting...")
    print (targets)
    return servos

def main():
    servos = InitOnCheckStatus(8)
    print ("exit...")
 
if __name__=="__main__":
    main()

