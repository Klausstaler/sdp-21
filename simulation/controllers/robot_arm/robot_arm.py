from RobotController import RobotController
import numpy as np
IKPY_MAX_ITERATIONS = 4
TIMESTEP = 128

# Initialize the Webots Supervisor.
robot_controller = RobotController(timestep=TIMESTEP)

was_released = False

x_pos = -.5 # go close to target in increments of .01
while robot_controller.step(TIMESTEP) != -1:
    is_present = robot_controller.suction_cup.getPresence()
    is_locked = robot_controller.suction_cup.isLocked()
    print("NEXT RUN")
    print(robot_controller.arm_chain.forward_kinematics(robot_controller.get_joint_config())[:3, 3])
    print(robot_controller.getSelf().getPosition())
    print(robot_controller.arm_chain.forward_kinematics(robot_controller.get_joint_config())[:3, 3]+ robot_controller.getSelf().getPosition())
    if is_present and not was_released and not is_locked:
        robot_controller.suction_cup.lock()
    if is_locked:
        robot_controller.park_parcel()
    else:
        robot_controller.lift_motor.setPosition(.73)
        x_pos = robot_controller.try_pickup(x_pos)
        print(x_pos)