import math
from pylx16a.lx16a import *
import argparse
import time
import copy

f_step_0 = [120.96, 135.36, 115.92, 118.56, 118.8, 109.2, 129.84, 114.72]
f_step_1 = [139.68, 115.68, 114.96, 117.36, 98.64, 120.0, 130.56, 117.36]
f_step_2 = [139.68, 116.4, 114.72, 102.24, 96.96, 117.84, 131.28, 131.52]
home_targets = [120.24, 121.2, 115.92, 118.8, 119.76, 117.84, 129.12, 114.24]
#f_step_2 = [120.96, 120.48, 95.52, 124.8, 118.56, 116.16, 150.48, 110.88]

sit_targets = [117.6, 155.76, 115.92, 86.4, 117.36, 80.88, 128.4, 151.44]
stand_targets = [160.32, 40.08, 70.8, 216.0, 80.64, 199.92, 165.6, 39.84]
bend_forward = [117.12, 155.76, 119.76, 86.4, 96.72, 157.44, 152.4, 75.84]

def smooth_transition(x, y, t): 
    # From x to y with t intervals
    radians = (1 - math.cos(t * math.pi)) / 2
    return x * (1 - radians) + y * radians 

def GetServos(num_of_servos: int):
    servos = []
    try: 
        for i in range(1, num_of_servos + 1, 1):
            servo = LX16A(i)
            print ("Servo {} added to the list".format(i))
            servos.append(servo)
            servos[i-1].set_angle_limits(35, 240)
    except ServoTimeoutError as e:
        print(f"Servo {e.id_} is not responding. Exiting...")
        quit()
    return servos

def SmoothTogether(servos, targets, set_times):
    left = 0
    runtime_targets = copy.deepcopy(targets)
    servo_move_degrees = []
    for i in range(len(targets)):
        servo = servos[i]
        try:
            degree = servo.get_physical_angle()
        except ServoTimeoutError as e:
            print ("Timeout. Try again.")
            try:
                degree = servo.get_physical_angle()
            except ServoTimeoutError as e:
                print ("Double timeout. Exit...")
                exit()
        move_degree = []
        for j in range(set_times):
            move_degree.append(smooth_transition(degree, targets[i], j * 1.0/set_times))
        servo_move_degrees.append(move_degree)
        time.sleep(0.06)
    for i in range(set_times):
        for j in range(len(targets)):
            servo = servos[j]
            servo.move(servo_move_degrees[j][i])
            # print ("Servo {} move to {}".format(j+1, servo_move_degrees[j][i]))
        time.sleep(0.06)

def main():
    parser = argparse.ArgumentParser(description='Disable Scripts')
    parser.add_argument('--action', help='''
        home - the robot will set to the running gesture.
        stand - the robot will stand up.
        sit - the robot will sit.
        
        You can input a sequence of gestures to the robot (e.g., home_stand_sit_stand_home)
        ''', type=str, default="home"
    )
    parser.add_argument('--loopcnt', help="The number of sequences to execute", type=int, default=1)
    args = parser.parse_args()
    motions = args.action.split(',')
    LX16A.initialize("/dev/ttyUSB0")
    num_of_servos = 8
    servos = GetServos(num_of_servos)

    for i in range(args.loopcnt):
        for m in motions:
            if m == "home":
                SmoothTogether(servos, home_targets, 20)
            elif m == "sit":
                SmoothTogether(servos, sit_targets, 20)
            elif m == "stand":
                SmoothTogether(servos, stand_targets, 20)
            elif m == "bend":
                SmoothTogether(servos, bend_forward, 20)
            elif m == "step0":
                SmoothTogether(servos, f_step_0, 20)
            elif m == "step1":
                SmoothTogether(servos, f_step_1, 20)
            elif m == "step2":
                SmoothTogether(servos, f_step_2, 20)
            else:
                print ("No such action supported {}".format(m))
        #time.sleep(0.3)
    
    # time.sleep(1)
    # print (servos)
    # SmoothTogether(servos, stand_targets, 20)
    # print ("Reset to stand position")
    # time.sleep(1)
    # SmoothTogether(servos, sit_targets, 20)
    # print ("Sit down!")
    # time.sleep(1)
    # return
    # SmoothTogether(servos, stand_targets, 20)
    # print ("Stand up again!")
    # time.sleep(1)
    # SmoothTogether(servos, fullstand_targets, 20)
    # print ("Full Stand")

if __name__ == "__main__":
    main()
