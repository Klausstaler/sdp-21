from RobotController import RobotController
from NetworkInterface import NetworkInterface
from Task import TaskType, task_type_to_func

IKPY_MAX_ITERATIONS = 4
TIMESTEP = 128

# Init network interface
net_interface = NetworkInterface()

# Initialize the Webots Supervisor.
robot_controller = RobotController(timestep=TIMESTEP)

x_pos = -.5 # go close to target in increments of .01
while robot_controller.step(TIMESTEP) != -1:
    success, curr_task = False, net_interface.get_current_task()
    if curr_task.task_type == TaskType.PICKUP_PARCEL:
        success = robot_controller.arm.try_pickup()
    elif curr_task.task_type == TaskType.RAISE_PLATFORM:
        success = robot_controller.raise_platform(**curr_task.params)
    if success:
        print("Finished", curr_task.task_type)
        net_interface.send_response(task_type_to_func[curr_task.task_type])
    """
    msg = robot_controller.nfc_reader.read()
    if msg:
        print("The message is: ", msg)
    else:
        print("No message received")
    """
