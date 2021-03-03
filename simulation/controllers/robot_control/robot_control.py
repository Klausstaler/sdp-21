from RobotController import RobotController
from NetworkInterface import NetworkInterface
from Task import TaskType, Tasks_dic
from functools import partial
import copy

IKPY_MAX_ITERATIONS = 4
TIMESTEP = 128

# Initialize the Webots Supervisor.
robot_controller = RobotController(timestep=TIMESTEP)

# Init network interface
net_interface = NetworkInterface(robot_controller.getName())

class TaskCompletion():
    def __init__(self, robot_controller:RobotController) -> None:
        self.robot_controller = robot_controller
        self.completed = False
        self.running = False
        self.init_param = {}
        self.func = None
        self.params = {}
        self.completition_func = lambda x:x

    def reset(self):
        self.__init__(self.robot_controller)

    def set_func(self, task_func= None, init_param = {}, params = {}, completition_func= None):
        self.func = task_func
        self.init_param = init_param
        self.params = params
        self.completition_func = completition_func
        
    def next_step(self):
        if self.running and not self.completed:
            self.completed = self.completition_func(
                self.func(**self.params)
                )
        elif not self.completed:
            self.func(**self.init_param)
            self.running = True
            
        if self.completed:
            self.robot_controller.nav.stop()

        return self.completed

    def set_task(self, task_type: TaskType, init_params:dict, time=0):
        
        params = copy.deepcopy(init_params)
        if task_type in [TaskType.TURN_UNTIL, TaskType.MOVEMENT]:
            init_params["new"] = True
            params["new"] = False
            
        if task_type in [TaskType.MOVEMENT]:
            params["time"] = time
            init_params["time"] = time
        if completition_func:= Tasks_dic[task_type]["completition_func"] is None:
            completition_func = lambda x:x

        self.set_func(
            task_func   = Tasks_dic[task_type]["task_func"](controller=self.robot_controller), 
            init_param  = init_params,
            params      = params,
            completition_func = completition_func
        )

task_completion = TaskCompletion(robot_controller)
time = 0
while robot_controller.step(TIMESTEP) != -1:
    success, curr_task = False, net_interface.get_current_task()
    if curr_task.task_type!= TaskType.NO_TASK:
        task_completion.set_task(curr_task.task_type, curr_task.params, time=time)
        success = task_completion.next_step()
    if success:
        print("Finished", curr_task.task_type)
        task_completion.reset()
        net_interface.send_response(curr_task.task_type.value)
    time+=1