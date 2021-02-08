from RobotController import RobotController
import numpy as np
import time
from ikpy.utils import geometry
IKPY_MAX_ITERATIONS = 4

# Initialize the Webots Supervisor.
robot_controller = RobotController(timestep=128)

# Get the arm and target
target = robot_controller.getFromDef("CONNECTOR_BOX1")

was_released = False

final_target = np.array([-.1, 0, 0.])
while robot_controller.step(robot_controller.timestep) != -1:
    is_present = robot_controller.suction_cup.getPresence()
    is_locked = robot_controller.suction_cup.isLocked()


    # Get the absolute postion of the target
    target_pos = np.array(target.getPosition())
    relative_target = robot_controller.convert_relative(target_pos)
    if is_locked:
        relative_target = final_target

    # lock the parcel, set the next target as the transport position for the parcel
    if is_present and not was_released and not is_locked:
        final_target[1], final_target[2] = relative_target[1:]
        robot_controller.suction_cup.lock()
    if not was_released:
        robot_controller.move_endeffector(relative_target)