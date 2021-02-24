from RobotController import RobotController
import numpy as np
IKPY_MAX_ITERATIONS = 4
TIMESTEP = 64

encoder = {"straight": 1, "left": 2, "right": 3, "back": 4}

start = 19
end = 21

# 19 -> 24 -> 23 -> 18 -> 17 -> 22 -> 21

ans = [19, 24, 23, 18, 17, 22, 21]
dir = [1, 3, 3, 2, 2, 3]


FSM_state = {'start':1, 'forward':2, 'opt':3, 'pick':4, 'lift':5, 'finish':6, 'stop':7}

FSM_state = 2
last_state = 2

# Initialize the Webots Supervisor.
robot_controller = RobotController(timestep=TIMESTEP)

was_released = False

x_pos = -.5 # go close to target in increments of .01

opt =1 
while robot_controller.step(TIMESTEP) != -1:

    if FSM_state == 7: #if FSM_state == 'stop'
        robot_controller.strafeForward(0)
    
    if FSM_state == 2: #FSM_state == 'forward':
        last_state = 2
        robot_controller.line_tracking()
    

    
    if FSM_state == 3: #FSM_state == 'opt'
        assert msg != ans[0] 
        opt = dir[0]
        last_state = 3 #last_state = 'opt'
        if opt == 1: 
            print("opt: ",opt)
            robot_controller.line_tracking()

        elif opt == 2:
            print("opt: ",opt)
            robot_controller.strafeLeft(6)
            
        elif opt == 3:
            print("opt: ",opt)
            robot_controller.strafeRight(6)
 

            
    msg = robot_controller.nfc_reader.read()
    if msg:
        FSM_state = 3
        if len(dir) == 0:
           FSM_state = 7 # stop
    else:
        #print(len(ans))
        #print(len(dir))
        #print("no message received")

        if last_state == 3: # if opt
            ans.pop(0)
            dir.pop(0)
        FSM_state = 2 # move forward


    """
    is_present = robot_controller.arm.suction_cup.getPresence()
    is_locked = robot_controller.arm.suction_cup.isLocked()
    if is_present and not was_released and not is_locked:
        robot_controller.arm.suction_cup.lock()
    if is_locked:
        robot_controller.arm.park_parcel()
    else:
        robot_controller.lift_motor.setPosition(.73)
        x_pos = robot_controller.arm.try_pickup(x_pos)
        print(x_pos)
    """   
    
