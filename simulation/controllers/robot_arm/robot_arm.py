from RobotController import RobotController
import numpy as np
import time
from ikpy.utils import geometry
IKPY_MAX_ITERATIONS = 4
TIMESTEP = 128

# Initialize the Webots Supervisor.
robot_controller = RobotController(timestep=TIMESTEP)

was_released = False

relative_target = np.array([0, 0.1678, 0.04])
x_pos = -.5 # go close to target in increments of .01
while robot_controller.step(TIMESTEP) != -1:
    is_present = robot_controller.suction_cup.getPresence()
    is_locked = robot_controller.suction_cup.isLocked()

    # lock the parcel, set the next target as the transport position for the parcel
    if is_present and not was_released and not is_locked:
        robot_controller.suction_cup.lock()
    if is_locked:
        robot_controller.park_parcel()
    else:
        x_pos = robot_controller.try_pickup(x_pos)