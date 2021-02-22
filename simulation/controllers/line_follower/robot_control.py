from RobotController import RobotController
import numpy as np
IKPY_MAX_ITERATIONS = 4
TIMESTEP = 128

encoder = {"straight": 1, "left": 2, "right": 3, "back": 4}

direction_arr = [2, 2, 3, 2, 3, 3, 3, 3, 2, 3, 2, 2]



# Initialize the Webots Supervisor.
robot_controller = RobotController(timestep=TIMESTEP)

was_released = False

x_pos = -.5 # go close to target in increments of .01
while robot_controller.step(TIMESTEP) != -1:
    #robot_controller.strafeForward(8.0)
    robot_controller.line_tracking()
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
    
