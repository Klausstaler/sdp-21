from RobotController import RobotController
from scipy.spatial.transform import Rotation as R
import numpy as np
import time
IKPY_MAX_ITERATIONS = 4

# Initialize the Webots Supervisor.
robot_controller = RobotController(timestep=128)

# Get the arm and target
target = robot_controller.getFromDef("CONNECTOR_BOX1")
arm = robot_controller.getSelf() # get base of robot arm

for i in [0, 1, 2]:
    robot_controller.arm_chain.active_links_mask[i] = False
# enable robot connector
robot_connector = robot_controller.getDevice("robot_box_connector")
robot_connector.enablePresence(128)

final_target = [2.5, 0.2, 1.26]
was_released = False
was_first = False
#robot_controller.arm_chain.links[2].
#print(robot_controller.arm_chain)
"""
while robot_controller.step(robot_controller.timestep) != -1:
    robot_controller.motors[0].setPosition(0.3)
    initial_joints = [0, 0] + [m.getPositionSensor().getValue() for m in robot_controller.motors]
    end_effector_pos = robot_controller.arm_chain.forward_kinematics(initial_joints)[:3, 3] + arm.getPosition()
    print(initial_joints)
    print(end_effector_pos)
    print(arm.getPosition())
    #print(np.asarray(robot_controller.arm_chain.links[2].get_link_frame_matrix({"theta": .3})))
    #print(robot_controller.arm_chain.links[2].translation_vector)
    print(robot_controller.arm_chain.links[2].symbolic_transformation_matrix(.3))
    print(robot_controller.arm_chain.links[2].rotation)
    print(robot_controller.arm_chain.forward_kinematics(initial_joints))
    print("NEXT RUn")
"""
robot_controller.motors[0].setPosition(.2)
time.sleep(.5)
while robot_controller.step(robot_controller.timestep) != -1:
    # Get the absolute postion of the target and the arm base.
    arm_pos, target_pos = arm.getPosition(), target.getPosition()
    # Compute the position of the target relatively to the arm.
    #if robot_connector.isLocked(): # we have the object
    #    target_pos = final_target
    # later we need to define a transform from the world frame to the robot frame
    x = target_pos[0] - arm_pos[0]
    y = target_pos[1] - arm_pos[1]
    z = target_pos[2] - arm_pos[2]
    
    # First 0 for base link, rest of the links have a joint associated with them
    initial_joints = [0, 0] + [m.getPositionSensor().getValue() for m in robot_controller.motors]
    ik_results = robot_controller.arm_chain.inverse_kinematics([x,y,z], max_iter=IKPY_MAX_ITERATIONS, initial_position=initial_joints)
    end_effector_pos = robot_controller.arm_chain.forward_kinematics(ik_results)[:3, 3] + arm_pos
    print(initial_joints)
    print(end_effector_pos)
    print(target_pos)
    print("NEXT TURN")
    """

    if np.linalg.norm(end_effector_pos - final_target) < 0.03 and robot_connector.isLocked():
        robot_connector.unlock()
        if was_first:
            was_released = True
            print("Package dropped off")
        else:
            was_first = True
    """

    is_present = robot_connector.getPresence()
    if is_present and not was_released and not robot_connector.isLocked():
        robot_connector.lock()
    if not was_released:
        for i, motor in enumerate(robot_controller.motors):
            if i > 0:
                motor.setPosition(ik_results[i+2]) # ignore first joint as it does not have an associated motor
""""""""