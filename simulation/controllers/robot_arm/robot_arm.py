from RobotController import RobotController
import numpy as np
import time
from ikpy.utils import geometry
IKPY_MAX_ITERATIONS = 4

# Initialize the Webots Supervisor.
robot_controller = RobotController(timestep=128)

# Get the arm and target
target = robot_controller.getFromDef("CONNECTOR_BOX1")
arm = robot_controller.getSelf() # get base of robot arm

for i in [0, 1]:
    robot_controller.arm_chain.active_links_mask[i] = False
# enable robot connector
robot_connector = robot_controller.getDevice("robot_box_connector")
robot_connector.enablePresence(128)

imu = robot_controller.getDevice("robot_imu")
imu.enable(128)

was_released = False
was_first = False
print(arm.getPosition())
final_target = [-.1, 0, 0.]
while robot_controller.step(robot_controller.timestep) != -1:
    is_present = robot_connector.getPresence()
    is_locked = robot_connector.isLocked()

    rot_mat = geometry.rpy_matrix(*imu.getRollPitchYaw())
    print(rot_mat)
    print(imu.getRollPitchYaw())
    # Get the absolute postion of the target and the arm base.
    arm_pos, target_pos = np.array(arm.getPosition()), np.array(target.getPosition())
    #target_pos = np.array(target_pos)@rot_mat
    # Compute the position of the target relatively to the arm.

    # later we need to define a transform from the world frame to the robot frame
    relative_pos = target_pos - arm_pos
    relative_pos[0] += 0.01
    relative_pos = relative_pos@rot_mat
    x,y,z = relative_pos
    print(x,y,z)
    print("ARM POS", arm_pos)
    print("TARGET POS", target_pos)
    """
    x = target_pos[0] - arm_pos[0] + 0.01 # small constant to not hit the box
    y = target_pos[1] - arm_pos[1]
    z = target_pos[2] - arm_pos[2]
    """

    if is_locked:
        x, y, z = final_target
    # First 0 for base link, rest of the links have a joint associated with them
    initial_joints = [0, 0] + [m.getPositionSensor().getValue() for m in robot_controller.motors]
    ik_results = robot_controller.arm_chain.inverse_kinematics([x,y,z], target_orientation=[-1,0,1],
                                                               orientation_mode="Z",
                                                               max_iter=IKPY_MAX_ITERATIONS, initial_position=initial_joints)
    end_effector_pos = robot_controller.arm_chain.forward_kinematics(ik_results)[:3, 3] + arm_pos
    #print(ik_results)
    #print(target_pos)
    print("NEXT TURN")
    if is_present and not was_released and not is_locked:
        #joint_config = initial_joints[:]
        #joint_config[2] = 0.0
        final_target[1], final_target[2] = y, z

        robot_connector.lock()
    if not was_released:
        #print(ik_results)
        for i, motor in enumerate(robot_controller.motors):
            motor.setPosition(ik_results[i+2]) # ignore first joint as it does not have an associated motor
""""""""