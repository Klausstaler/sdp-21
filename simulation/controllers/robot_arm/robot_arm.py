from RobotController import RobotController
import tempfile, qrtools
open("test.png", "w").close()
def read_qr_code(img):
    filename = None
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as file:
        filename = file.name
        file.write(img)
    qr = qrtools.QR()
    if qr.decode(filename):
        return qr.data
    return None

IKPY_MAX_ITERATIONS = 4

# Initialize the Webots Supervisor.
robot_controller = RobotController(timestep=128)

# Get the arm and target
target = robot_controller.getFromDef("CONNECTOR_BOX1")
arm = robot_controller.getSelf() # get base of robot arm


# freeze base,first and sixth joint (currently don't freeze first)
for i in [0, 1, 6]:
    robot_controller.arm_chain.active_links_mask[i] = False
print(robot_controller.arm_chain)
# enable robot connector
robot_connector = robot_controller.getDevice("robot_box_connector")
robot_connector.enablePresence(128)

camera = robot_controller.getDevice("arm_camera")
camera.enable(128)

final_target = [2.5, 0.2, 1.26]
was_released = False
was_first = False
while robot_controller.step(robot_controller.timestep) != -1:
    # Get the absolute postion of the target and the arm base.
    arm_pos, target_pos = arm.getPosition(), target.getPosition()
    """
    qr_data = read_qr_code(camera.getImage())
    if qr_data:
        print(f"Found qr code!Stored {qr_data} on it.")
        """
    # Compute the position of the target relatively to the arm.
    if robot_connector.isLocked(): # we have the object
        target_pos = final_target
    x = target_pos[0] - arm_pos[0]
    #y = target_pos[1] - arm_pos[1]
    z = target_pos[2] - arm_pos[2]

    # First 0 for base link, rest of the links have a joint associated with them
    initial_joints = [0] + [m.getPositionSensor().getValue() for m in robot_controller.motors]
    y = robot_controller.arm_chain.forward_kinematics(initial_joints)[1, 3]
    print(robot_controller.arm_chain.forward_kinematics(initial_joints)[:3, 3] + arm_pos, target_pos)
    ik_results = robot_controller.arm_chain.inverse_kinematics([x,y,z], max_iter=IKPY_MAX_ITERATIONS, initial_position=initial_joints)
    end_effector_pos = robot_controller.arm_chain.forward_kinematics(ik_results)[:3, 3] + arm_pos
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
            motor.setPosition(ik_results[i+1]) # ignore first joint as it does not have an associated motor
            """
"""