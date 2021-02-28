from RobotController import RobotController
from NetworkInterface import NetworkInterface
from Task import TaskType

IKPY_MAX_ITERATIONS = 4
TIMESTEP = 128

# Init network interface
net_interface = NetworkInterface()

# Initialize the Webots Supervisor.
robot_controller = RobotController(timestep=TIMESTEP)



while robot_controller.step(TIMESTEP) != -1:
    success, curr_task = False, net_interface.get_current_task()
    
    if success:
        print("Finished", curr_task.task_type)
        net_interface.send_response(curr_task.task_type.value)
    #robot_controller.nav.set_wheel_speeds(10, 10, 10, 10)
    """
    msg = robot_controller.nfc_reader.read()
    if msg:
        print("The message is: ", msg)
    else:
        print("No message received")
    """
