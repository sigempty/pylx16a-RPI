from pylx16a.lx16a import *
import argparse
import time

def GetServos(num_of_servos: int):
    servos = []
    try: 
        for i in range(1, num_of_servos + 1, 1):
            servo = LX16A(i)
            print ("Servo {} added to the list".format(i))
            servos.append(servo)
            servos[i-1].set_angle_limits(40, 240)
    except ServoTimeoutError as e:
        print(f"Servo {e.id_} is not responding. Exiting...")
        quit()
    return servos

def DisableAll(servos):
    for servo in servos:
        servo.disable_torque()
        time.sleep(0.2)

def EnableAll(servos):
    for servo in servos:
        servo.enable_torque()
        time.sleep(0.2)

def main():
    parser = argparse.ArgumentParser(description='Disable Scripts')
    parser.add_argument('--val', help='val = 0 (disable), val = 1 (enable)', required=True, type=int)
    args = parser.parse_args()
    LX16A.initialize("/dev/ttyUSB0")
    num_of_servos = 8
    servos = GetServos(num_of_servos)
    if args.val == 0:
        DisableAll(servos)
    else:
        EnableAll(servos)
    time.sleep(1)
    for servo in servos:   
        print ("Servo {}'s torque is enabled? {}".format(servo.get_id(), servo.is_torque_enabled()))

if __name__ == "__main__":
    main() 