from RobotController import RobotController
from NetworkInterface import NetworkInterface
from Task import TaskType

IKPY_MAX_ITERATIONS = 4
TIMESTEP = 128

# Init network interface
net_interface = NetworkInterface()

# Initialize the Webots Supervisor.
robot_controller = RobotController(timestep=TIMESTEP)

class TaskCompletion():
    def __init__(self, robot_controller:RobotController) -> None:
        self.robot_controller = robot_controller
        self.completed = False
        self.running = False
        self.init_param = None
        self.func = None

    def reset(self):
        self.__init__(self.robot_controller)

    def set_func(self, task_func= None, init_param = None):
        self.func = task_func
        self.init_param = init_param
        
    def next_step(self):
        if self.running and not self.completed:
            self.completed = self.func()
        elif not self.completed:
            self.func(**self.init_param)
            self.running = True
        return self.completed

    def set_task(self, task_type: TaskType, init_params:dict):
        if task_type == TaskType.REACH_NODE:
            task_func = self.robot_controller.reach_node#(params["node"])
        elif task_type == TaskType.TURN_UNTIL:
            task_func = self.robot_controller.nav.turn_until_line_n #(int(params["n"]))
        elif task_type == TaskType.PICKUP_PARCEL:
            task_func = self.robot_controller.arm.try_pickup#()
        elif task_type == TaskType.RAISE_PLATFORM:
            task_func = self.robot_controller.raise_platform#(**params)
        self.set_func(task_func, init_params)
    

task_completion = TaskCompletion(robot_controller)

while robot_controller.step(TIMESTEP) != -1:
    success, curr_task = False, net_interface.get_current_task()
    task_completion.set_task(curr_task.task_type, curr_task.params)
    success = task_completion.next_step()
    if success:
        print("Finished", curr_task.task_type)
        task_completion.reset()
        net_interface.send_response(curr_task.task_type.value)